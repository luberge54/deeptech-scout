"""Step 3 of the pipeline: score one company against the five weighted criteria.

This is the step the project is actually about. The model sees the structured
evidence step 2 produced - never the open web, never the hand-scores - and
argues a 1-5 value per criterion. It runs on Opus per scoping section 4d,
because arbitrating between the anchors is the one place model capability
separates.

The model does not compute the total and does not apply the missing-evidence
cap. Both live in scoring.py so they hold whatever the model returns.

Run with:  .venv\\Scripts\\python.exe src\\score.py [company-slug | all]
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import pydantic
from dotenv import load_dotenv

from schema import CRITERION_NAMES
from scoring import CRITERION_WEIGHTS, ScoringOutput, score_company

# Section 4d: scoring is pure judgement, so it is the one step that pays for Opus.
# A rerun must stay on this model or the section 5 calibration is void.
SCORING_MODEL = "claude-opus-5"

# Judgement is short next to extraction, but streaming keeps a slow reasoning turn
# from hitting the HTTP timeout, and an unused ceiling costs nothing.
MAX_OUTPUT_TOKENS = 32000

INPUT_DIR = Path("data/output")
SCORED_DIR = Path("data/scored")
RUN_ALL_KEYWORD = "all"
INPUT_SUFFIX = ".extracted.json"
OUTPUT_SUFFIX = ".scored.json"

# Opus 5 list prices, August 2026, dollars per million tokens.
PRICE_PER_MTOK = {"input": 5.00, "output": 25.00}
TOKENS_PER_MILLION = 1_000_000

ANCHORS = """| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| Field traction (30) | Demos, pilots, LOIs only. No paying deployment. | Paying deployments at ~3-10 customers, each install custom. | Repeat orders, tens of units in daily service, at least one customer past pilot into a fleet. |
| Team / execution (25) | First-time founders, no hardware shipped, flat team. | Credible technical founders, one generation shipped, steady hiring. ETH/EPFL pedigree caps here. | Shipped hardware at scale before, or 2+ generations with shortening cycles; pulls senior talent from big tech. |
| Technology (20) | Reproducible with off-the-shelf parts; capability already in the published research of others. | Real engineering depth, but the approach is broadly available. | Compounds with use: proprietary data flywheel, unbuyable component, or multi-year certification. |
| Market (15) | Narrow niche, or no existing budget line for this spend. | Sizeable but crowded, or procurement cycles long enough to starve a startup. | Large segment, urgent and already budgeted pain, buyer purchases in this category today. |
| Timing (10) | Could have been built five years ago and was not; no external change explains now. | Rides the general Physical AI wave. This is the default. | A specific dateable unlock: regulation, component price threshold, customer mandate. |"""

SCORING_PROMPT = """Score {name} on the five criteria below. It is a company in the \
Physical AI sector - robots and autonomous machines that perceive and act in the physical \
world.

# The scale

Anchors are defined at 1, 3 and 5. Scores of 2 and 4 sit between them.

{anchors}

# How to use the anchors

Pick the anchor the evidence actually reaches, not the one it gestures at. A company with \
pilots and no paying deployment is a 1 on traction however impressive the pilots are. \
Timing defaults to 3 - the general Physical AI wave is the same for every company here, so \
only a specific dateable unlock earns a 5.

# Your only source

The structured evidence below, extracted from public sources. Do not add facts you happen \
to know about this company, and do not infer what is plausible for a company of this kind. \
Judge what is in front of you.

Each item carries who published it (source_type), whether it is a direct or indirect \
indicator (evidence_grade), and who is actually making the claim (attributed_to). A claim \
attributed to the company and merely repeated by trade press is the company's claim, not \
third-party confirmation. Weigh it accordingly.

Funding is not traction. A large round says what investors believed; it belongs to \
team_execution as a statement about resources.

# What you must not do

Do not compute a total, do not rank this company against any other, and do not adjust a \
score because the overall picture feels too high or too low. Each criterion is judged on \
its own evidence. The weighting and the total are applied afterwards, outside this step.

# Justifications

For each criterion say why this score rather than the one above it and the one below it, \
citing the specific evidence that decides it. A justification that would read the same for \
any company in the sector is not a justification. In key_evidence_urls list the URLs of the \
items that carry the score, copied exactly as they appear.

# The evidence

{evidence}
"""


def read_api_key() -> str:
    load_dotenv()
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        sys.exit("FAIL: ANTHROPIC_API_KEY is missing. Run src/check_setup.py first.")
    return key


def render_evidence(record: dict) -> str:
    """Lay out step 2's record as the model reads it, criterion by criterion."""
    blocks = []

    for name in CRITERION_NAMES:
        criterion = record["criteria"][name]
        lines = [
            f"## {name}  (weight {CRITERION_WEIGHTS[name]})"
            f"  status: {criterion['evidence_status']}"
            f"  confidence: {criterion['confidence'] or 'none'}"
        ]

        if criterion["not_found_notes"]:
            lines.append(f"Note on what was not found: {criterion['not_found_notes']}")

        if not criterion["evidence"]:
            lines.append("No evidence survived the sourcing rules for this criterion.")

        for item in criterion["evidence"]:
            lines.append(
                f"- [{item['evidence_grade']}] [{item['source_type']}]"
                f" [claimed by: {item['attributed_to'] or 'unstated'}]"
                f" {item['claim']}"
                f"  ({item['source_url']})"
            )

        blocks.append("\n".join(lines))

    if record.get("contradictions"):
        lines = ["## Contradictions the research flagged, left unresolved"]
        for item in record["contradictions"]:
            lines.append(f"- {item['description']}  ({', '.join(item['source_urls'])})")
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks)


def load_record(slug: str) -> dict:
    """Read one step 2 output, failing clearly if extraction has not run yet."""
    path = INPUT_DIR / f"{slug}{INPUT_SUFFIX}"
    if not path.exists():
        sys.exit(
            f"FAIL: no extracted record at {path}.\n"
            f"      Run: .venv\\Scripts\\python.exe src\\extract.py {slug}"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def already_scored() -> set[str]:
    """Slugs that already have a step 3 record on disk."""
    return {
        path.name[: -len(OUTPUT_SUFFIX)]
        for path in SCORED_DIR.glob(f"*{OUTPUT_SUFFIX}")
    }


def resolve_targets(argument: str) -> list[str]:
    """Expand the argument into slugs, skipping work already on disk.

    Opus is the most expensive step in the pipeline, so re-charging for a company
    that is already scored would be the costliest possible mistake to make twice.
    """
    if argument != RUN_ALL_KEYWORD:
        return [argument]

    extracted = sorted(
        path.name[: -len(INPUT_SUFFIX)] for path in INPUT_DIR.glob(f"*{INPUT_SUFFIX}")
    )
    if not extracted:
        sys.exit(f"FAIL: no extracted records in {INPUT_DIR}. Run step 2 first.")

    done = already_scored()
    if done:
        print(f"Already scored, skipping: {', '.join(sorted(done))}")
        print("To re-score one of these, pass its slug explicitly.")

    pending = [slug for slug in extracted if slug not in done]
    if not pending:
        sys.exit("Nothing to do - every extracted record has already been scored.")
    return pending


def report_scores(result: dict) -> None:
    """Print one line per criterion so a wrong score is visible immediately."""
    for name in CRITERION_NAMES:
        criterion = result["criteria"][name]
        score = "not scored" if criterion["score"] is None else f"{criterion['score']}/5"
        flag = "  <-- capped by section 4b" if criterion["was_capped"] else ""
        print(
            f"    {name:<15} {score:<11} weight {criterion['weight']:<3}"
            f" -> {criterion['weighted_points']:>4.1f} pts"
            f"  [{criterion['confidence'] or '-'}]{flag}"
        )
    print(
        f"    TOTAL {result['total_out_of_100']}/100"
        f"  (over a weight of {result['weight_covered']})"
    )


def score_one(client: anthropic.Anthropic, slug: str) -> dict:
    """Score one company and write the result."""
    record = load_record(slug)
    company = record["company"]

    print(f"\n[{slug}] scoring {company['name']} on {SCORING_MODEL}")

    prompt = SCORING_PROMPT.format(
        name=company["name"],
        anchors=ANCHORS,
        evidence=render_evidence(record),
    )

    try:
        with client.messages.stream(
            model=SCORING_MODEL,
            max_tokens=MAX_OUTPUT_TOKENS,
            messages=[{"role": "user", "content": prompt}],
            output_format=ScoringOutput,
        ) as stream:
            response = stream.get_final_message()
    except anthropic.APIStatusError as error:
        sys.exit(f"FAIL: API error (HTTP {error.status_code}): {error.message}")
    except anthropic.APIConnectionError:
        sys.exit("FAIL: could not reach the API. Check your internet connection.")
    except pydantic.ValidationError as error:
        sys.exit(
            f"""FAIL: the reply for {slug} did not validate against the schema.
      If the error mentions invalid or unterminated JSON, the reply was cut off
      at the {MAX_OUTPUT_TOKENS:,}-token ceiling. Raise MAX_OUTPUT_TOKENS.
      {error}"""
        )

    if response.stop_reason == "max_tokens":
        sys.exit(
            f"""FAIL: {slug} hit the {MAX_OUTPUT_TOKENS:,}-token output ceiling, so the
      judgement would be incomplete. Nothing was written."""
        )

    judgement = response.parsed_output
    if judgement is None:
        sys.exit(f"FAIL: the model returned no parseable judgement for {slug}.")

    scored = score_company(judgement, record["criteria"])

    usage = response.usage
    cost = (
        usage.input_tokens * PRICE_PER_MTOK["input"]
        + usage.output_tokens * PRICE_PER_MTOK["output"]
    ) / TOKENS_PER_MILLION

    result = {
        "company": company,
        "scored_at": datetime.now(timezone.utc).isoformat(),
        "model": SCORING_MODEL,
        "pipeline_step": 3,
        "source_record": str(INPUT_DIR / f"{slug}{INPUT_SUFFIX}"),
        **scored,
        "run_stats": {
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "estimated_cost_usd": round(cost, 4),
        },
    }

    SCORED_DIR.mkdir(parents=True, exist_ok=True)
    path = SCORED_DIR / f"{slug}{OUTPUT_SUFFIX}"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    report_scores(result)
    print(f"    cost: ${cost:.3f}  ->  {path}")
    return result


def main() -> None:
    argument = sys.argv[1] if len(sys.argv) > 1 else RUN_ALL_KEYWORD
    targets = resolve_targets(argument)

    print(f"Step 3: weighted scoring for {len(targets)} company(ies), {SCORING_MODEL}")

    client = anthropic.Anthropic(api_key=read_api_key())
    total = sum(
        score_one(client, slug)["run_stats"]["estimated_cost_usd"] for slug in targets
    )

    print(f"\nDone. {len(targets)} scored, estimated total cost ${total:.2f}")


if __name__ == "__main__":
    main()
