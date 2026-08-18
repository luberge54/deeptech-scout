"""Step 2 of the pipeline: turn a step 1 findings report into a structured record.

The model sees only the report produced by step 1 - never the open web - so it
cannot quietly add facts that no source backs. It classifies evidence; it does
not score. Confidence is computed afterwards in schema.py, not asked for.

Run with:  .venv\\Scripts\\python.exe src\\extract.py [company-slug | all]
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import pydantic
from dotenv import load_dotenv

from schema import (
    CRITERION_NAMES,
    ExtractionOutput,
    build_criterion_record,
)

# docs/00-scoping.md section 4d: extraction is mechanical once the schema is
# fixed, so it runs on Sonnet. Judgement happens in step 3, on Opus.
EXTRACTION_MODEL = "claude-sonnet-5"

# Measured, not guessed: at 16000 the ANYbotics extraction stopped with
# stop_reason "max_tokens" and a JSON string cut mid-word. Only about a third of
# that budget reached the JSON - Sonnet 5 runs adaptive thinking by default and
# the reasoning is billed from the same ceiling. Sonnet 5 allows up to 128000, and
# a ceiling is a limit rather than a target, so a higher one costs nothing extra on
# reports that finish early. Above roughly 16000 the SDK needs streaming to avoid
# an HTTP timeout, which is why this step streams.
MAX_OUTPUT_TOKENS = 64000

INPUT_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/output")
RUN_ALL_KEYWORD = "all"

# Same list prices as collect_sources.py, kept local so each step reports its
# own spend without importing across modules.
PRICE_PER_MTOK = {"input": 2.00, "output": 10.00}
TOKENS_PER_MILLION = 1_000_000

EXTRACTION_PROMPT = """Below is a research report about {name}, a company in the Physical AI \
sector. Convert it into the structured format defined by the output schema.

# Your only source

The report below. Do not add facts from your own knowledge, and do not infer what is \
plausible for a company of this kind. If the report does not state it, it does not exist \
for this task.

# Do not evaluate

Do not score, rank, rate, or judge the company. Do not decide which evidence is stronger. \
You are converting prose into fields; the judgement happens in a later step by a different \
model, and it depends on you not having pre-filtered.

# Assigning evidence_status per criterion

This is the field that matters most, and the three values are not interchangeable:

- `found` - the report contains at least one sourced claim for this criterion.
- `searched_not_found` - the report says this area was searched and nothing was found.
  Use this only when the report actually asserts absence.
- `not_searched` - the report says this area was skipped, cut short, or not covered.
  Phrases like "not searched due to the search cap", "I was unable to complete", or an
  area simply absent from the report with no statement about it, all mean `not_searched`.

The difference matters downstream: `searched_not_found` caps the company's score for that \
criterion, while `not_searched` excludes it from scoring entirely. Marking a coverage gap as \
`searched_not_found` would penalise the company for a limitation of the research, so when \
you cannot tell which of the two applies, choose `not_searched`.

{budget_hint}

# Evidence rules

- Every item needs a `source_url` taken from the report. Drop any claim the report does
  not attach a URL to, however plausible it sounds.
- `source_type` records who published it, not how convincing it is. A vendor-hosted case
  study is `vendor_case_study` even when it names a real customer.
- `evidence_grade` is `direct` for a named customer, a unit count, a date, or a signed
  agreement. It is `indirect` for job postings, unnamed customers, and vague claims.
- Funding rounds are never traction evidence. They belong under `team_execution` as
  context about the company's resources.
- The report distinguishes company claims from third-party confirmation. Preserve that in
  `attributed_to`.

# Contradictions

Copy across every disagreement the report flags - figures that differ across sources, or
claims that conflict. Do not resolve them. Reconciling contradictions is a judgement, and
it belongs to the scoring step where it can be argued for.

# The report

{findings}
"""

BUDGET_EXHAUSTED_HINT = """This report was produced by a research run that used its entire \
search budget, so gaps are more likely to be coverage limits than genuine absence. Lean \
towards `not_searched` where the report is silent."""


def read_api_key() -> str:
    load_dotenv()
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        sys.exit("FAIL: ANTHROPIC_API_KEY is missing. Run src/check_setup.py first.")
    return key


def load_report(slug: str) -> dict:
    """Read one step 1 output, failing clearly if collection has not run yet."""
    path = INPUT_DIR / f"{slug}.json"
    if not path.exists():
        sys.exit(
            f"FAIL: no collected report at {path}.\n"
            f"      Run: .venv\\Scripts\\python.exe src\\collect_sources.py {slug}"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def extract_one(client: anthropic.Anthropic, slug: str) -> dict:
    """Run the extraction for one company and write the structured record."""
    report = load_report(slug)
    company = report["company"]
    stats = report.get("run_stats", {})
    budget_exhausted = stats.get("searches_run") == stats.get("search_budget")

    print(f"\n[{slug}] extracting {company['name']}")

    prompt = EXTRACTION_PROMPT.format(
        name=company["name"],
        findings=report["findings"],
        budget_hint=BUDGET_EXHAUSTED_HINT if budget_exhausted else "",
    )

    try:
        with client.messages.stream(
            model=EXTRACTION_MODEL,
            max_tokens=MAX_OUTPUT_TOKENS,
            messages=[{"role": "user", "content": prompt}],
            output_format=ExtractionOutput,
        ) as stream:
            response = stream.get_final_message()
    except anthropic.APIStatusError as error:
        sys.exit(f"FAIL: API error (HTTP {error.status_code}): {error.message}")
    except anthropic.APIConnectionError:
        sys.exit("FAIL: could not reach the API. Check your internet connection.")
    except pydantic.ValidationError as error:
        # Truncation is the likely cause and the raw error never says so, so name it
        # here rather than leaving the next reader to rediscover it.
        sys.exit(
            f"""FAIL: the reply for {slug} did not validate against the schema.
      If the error below mentions unterminated or invalid JSON, the reply was
      cut off at the {MAX_OUTPUT_TOKENS:,}-token ceiling. Raise MAX_OUTPUT_TOKENS.
      {error}"""
        )

    if response.stop_reason == "max_tokens":
        sys.exit(
            f"""FAIL: {slug} hit the {MAX_OUTPUT_TOKENS:,}-token output ceiling, so the
      record would be incomplete. Nothing was written. Raise MAX_OUTPUT_TOKENS."""
        )

    extracted = response.parsed_output
    if extracted is None:
        sys.exit(f"FAIL: the model returned no parseable output for {slug}.")

    criteria = {
        name: build_criterion_record(getattr(extracted, name)).model_dump()
        for name in CRITERION_NAMES
    }

    usage = response.usage
    cost = (
        usage.input_tokens * PRICE_PER_MTOK["input"]
        + usage.output_tokens * PRICE_PER_MTOK["output"]
    ) / TOKENS_PER_MILLION

    record = {
        "company": company,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "model": EXTRACTION_MODEL,
        "pipeline_step": 2,
        "source_report": str(INPUT_DIR / f"{slug}.json"),
        "search_budget_exhausted": budget_exhausted,
        "criteria": criteria,
        "contradictions": [item.model_dump() for item in extracted.contradictions],
        "run_stats": {
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "estimated_cost_usd": round(cost, 4),
        },
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{slug}.extracted.json"
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

    report_criteria(criteria)
    print(f"    contradictions: {len(record['contradictions'])}")
    print(f"    cost: ${cost:.3f}  ->  {path}")

    return record


def report_criteria(criteria: dict) -> None:
    """Print one line per criterion so coverage problems are visible immediately."""
    for name, record in criteria.items():
        confidence = record["confidence"] or "-"
        count = len(record["evidence"])
        flag = "  <-- not scored" if record["evidence_status"] == "not_searched" else ""
        print(
            f"    {name:<15} {record['evidence_status']:<19} "
            f"{confidence:<7} {count} item(s){flag}"
        )


def resolve_targets(argument: str) -> list[str]:
    """Expand the argument into slugs, using whatever step 1 has already produced."""
    if argument != RUN_ALL_KEYWORD:
        return [argument]

    collected = sorted(path.stem for path in INPUT_DIR.glob("*.json"))
    if not collected:
        sys.exit(f"FAIL: no collected reports in {INPUT_DIR}. Run step 1 first.")
    return collected


def main() -> None:
    argument = sys.argv[1] if len(sys.argv) > 1 else RUN_ALL_KEYWORD
    targets = resolve_targets(argument)

    print(f"Step 2: extraction for {len(targets)} company(ies), model {EXTRACTION_MODEL}")

    client = anthropic.Anthropic(api_key=read_api_key())
    total = sum(
        extract_one(client, slug)["run_stats"]["estimated_cost_usd"] for slug in targets
    )

    print(f"\nDone. {len(targets)} extracted, estimated total cost ${total:.2f}")


if __name__ == "__main__":
    main()
