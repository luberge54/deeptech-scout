"""Step 1 of the pipeline: collect public evidence about one company.

Uses Claude with the server-side web search tool, so Anthropic runs the
searches; there is no scraper to maintain here. The prompt targets the five
source types defined in docs/00-scoping.md section 4c, because the traction
criterion carries the highest weight and is the hardest to evidence.

This step deliberately does NOT extract structured fields or score anything.
It produces a sourced findings document plus the list of URLs actually
consulted, so the evidence can be audited before any judgment is applied.

Run with:  .venv\\Scripts\\python.exe src\\collect_sources.py [company-slug]
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# Model assignment is defined in docs/00-scoping.md section 4d: collection is
# high-volume and low-judgment, so it runs on Sonnet rather than Opus.
COLLECTION_MODEL = "claude-sonnet-5"

# Bounds both cost and runtime. The first ANYbotics run exhausted a budget of 12
# before reaching patents and the competitor landscape, and said so in its own
# gaps section - so 12 was truncating the research, not bounding it.
MAX_SEARCHES = 20
MAX_OUTPUT_TOKENS = 16000

# Claude API list prices, August 2026, in dollars per million tokens. Sonnet is
# on introductory pricing until 2026-08-31, after which it becomes 3.00 / 15.00.
PRICE_PER_MTOK = {
    "claude-sonnet-5": {"input": 2.00, "output": 10.00},
    "claude-opus-5": {"input": 5.00, "output": 25.00},
}
PRICE_PER_SEARCH = 0.01
TOKENS_PER_MILLION = 1_000_000

# A server-side tool loop can stop with "pause_turn" before finishing. Each
# continuation resumes it; this caps how many times we resume.
MAX_CONTINUATIONS = 5

OUTPUT_DIR = Path("data/raw")

COMPANIES = {
    "anybotics": {
        "name": "ANYbotics",
        "country": "Switzerland",
        "city": "Zurich",
        "website": "anybotics.com",
        "description": "legged robots for industrial inspection",
    },
}

DEFAULT_COMPANY_SLUG = "anybotics"

RESEARCH_PROMPT = """You are gathering public evidence about a company for a market map of \
Physical AI companies in Switzerland and Europe.

Company: {name} ({city}, {country})
Website: {website}
What they do: {description}

Search the web and report what you find. Your job is evidence collection, not evaluation \
- do not rank, rate, or judge the company.

# What to search for

Cover these five areas. Field traction is the priority: it is the hardest to evidence \
publicly and the most valuable when found.

1. FIELD TRACTION - paying industrial customers and units actually deployed.
   Search beyond the company's own marketing:
   - Customer-side announcements (the buyer announcing a rollout is stronger evidence
     than the vendor announcing a win)
   - Published case studies naming a site, a customer, or a unit count
   - Trade and industry press covering installations
   - Public tender or regulatory records
   - Job postings: a company hiring field deployment engineers has deployments; one
     hiring only researchers does not

2. TEAM AND EXECUTION - founders' backgrounds, prior hardware shipped, product
   generations released and their dates, notable senior hires, headcount.

3. TECHNOLOGY - what is proprietary versus assembled from available parts. Custom
   hardware, certifications obtained, published research, patents.

4. MARKET - who buys this, whether a budget line already exists for it, named
   competitors.

5. TIMING - any specific dated event that made this possible now: a regulation, a
   certification, a component price change, a customer mandate.

# Rules you must follow

- Give the source URL for every factual claim. A claim with no URL is not usable.
- Label each finding as DIRECT evidence (named customer, unit count, date, signed
  contract) or INDIRECT indicator (job postings, vague marketing language,
  unnamed customers).
- When you find nothing for an area, write "No evidence found" and say what you
  searched for. Do not infer what is plausible for a company of this size, and do
  not fill gaps from general knowledge.
- Distinguish what the company claims about itself from what a third party
  confirms. Say which is which.
- Funding rounds are not traction. Report them under team/execution as context,
  never as evidence of deployment.

# Output format

Use these headings, in this order:

## Field traction
## Team and execution
## Technology
## Market
## Timing
## Contradictions and gaps

Under the last heading, list any figures that disagreed across sources, and any
area where the evidence was thin. Be blunt about what you could not find.
"""


def read_api_key() -> str:
    """Load the API key from .env, failing with a clear message if absent."""
    load_dotenv()
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        sys.exit("FAIL: ANTHROPIC_API_KEY is missing. Run src/check_setup.py first.")
    return key


def select_company(slug: str) -> dict:
    """Look up a company by slug, listing valid options on failure."""
    if slug not in COMPANIES:
        known = ", ".join(sorted(COMPANIES))
        sys.exit(f"FAIL: unknown company '{slug}'. Known companies: {known}")
    return COMPANIES[slug]


def run_research(client: anthropic.Anthropic, company: dict) -> anthropic.types.Message:
    """Run the search-backed research call, resuming if the tool loop pauses.

    Streaming is used because web search pulls a large amount of content into
    the request, which can push a non-streaming call past its timeout.
    """
    prompt = RESEARCH_PROMPT.format(**company)
    messages = [{"role": "user", "content": prompt}]
    tools = [
        {
            "type": "web_search_20260209",
            "name": "web_search",
            "max_uses": MAX_SEARCHES,
        }
    ]

    for continuation in range(MAX_CONTINUATIONS):
        try:
            with client.messages.stream(
                model=COLLECTION_MODEL,
                max_tokens=MAX_OUTPUT_TOKENS,
                tools=tools,
                messages=messages,
            ) as stream:
                response = stream.get_final_message()
        except anthropic.APIStatusError as error:
            sys.exit(f"FAIL: API error (HTTP {error.status_code}): {error.message}")
        except anthropic.APIConnectionError:
            sys.exit("FAIL: could not reach the API. Check your internet connection.")

        if response.stop_reason != "pause_turn":
            return response

        print(f"    search loop paused, resuming ({continuation + 1}/{MAX_CONTINUATIONS})")
        messages = [messages[0], {"role": "assistant", "content": response.content}]

    sys.exit(
        f"FAIL: the search loop still had not finished after {MAX_CONTINUATIONS} "
        "continuations. Narrow the prompt or raise MAX_CONTINUATIONS."
    )


def extract_text(response: anthropic.types.Message) -> str:
    """Join the response text blocks, dropping any narration before the report.

    While the search tool runs, the model narrates its own progress ("Let me
    check the next result..."). Those land in text blocks alongside the report.
    The findings document starts at its first Markdown heading, so everything
    before that heading is working commentary and is discarded.
    """
    joined = "\n".join(
        block.text for block in response.content if block.type == "text"
    ).strip()

    for index, line in enumerate(lines := joined.splitlines()):
        if line.startswith("#"):
            return "\n".join(lines[index:]).strip()

    # No heading at all means the model ignored the requested format. Keep the
    # text rather than returning nothing, so the run is still inspectable.
    print("    WARNING: no Markdown heading found; keeping the raw text unchanged")
    return joined


def estimate_cost(model: str, input_tokens: int, output_tokens: int, searches: int) -> float:
    """Estimate the dollar cost of one run, so spend stays visible per company."""
    prices = PRICE_PER_MTOK.get(model)
    if prices is None:
        return 0.0

    token_cost = (
        input_tokens * prices["input"] + output_tokens * prices["output"]
    ) / TOKENS_PER_MILLION
    return token_cost + (searches or 0) * PRICE_PER_SEARCH


def extract_sources(response: anthropic.types.Message) -> list[dict]:
    """List the pages the web search actually returned, in order, deduplicated.

    Search failures arrive as a successful response whose result content is an
    error object rather than a list, so the shape is checked before indexing.
    """
    sources: list[dict] = []
    seen: set[str] = set()

    for block in response.content:
        if block.type != "web_search_tool_result":
            continue

        results = block.content
        if not isinstance(results, list):
            error_code = getattr(results, "error_code", "unknown")
            print(f"    WARNING: a web search failed (error_code: {error_code})")
            continue

        for result in results:
            url = getattr(result, "url", None)
            if not url or url in seen:
                continue
            seen.add(url)
            sources.append({"url": url, "title": getattr(result, "title", None)})

    return sources


def build_record(company: dict, slug: str, response: anthropic.types.Message) -> dict:
    """Assemble everything worth keeping about this collection run."""
    server_tool_use = getattr(response.usage, "server_tool_use", None)
    searches_run = getattr(server_tool_use, "web_search_requests", None)

    return {
        "company": company | {"slug": slug},
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "model": COLLECTION_MODEL,
        "pipeline_step": 1,
        "findings": extract_text(response),
        "sources": extract_sources(response),
        "run_stats": {
            "searches_run": searches_run,
            "search_budget": MAX_SEARCHES,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "stop_reason": response.stop_reason,
            "estimated_cost_usd": round(
                estimate_cost(
                    COLLECTION_MODEL,
                    response.usage.input_tokens,
                    response.usage.output_tokens,
                    searches_run,
                ),
                4,
            ),
        },
    }


def save_record(record: dict, slug: str) -> Path:
    """Write the record to data/raw/<slug>.json, creating the directory if needed."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{slug}.json"
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def main() -> None:
    slug = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_COMPANY_SLUG
    company = select_company(slug)

    print(f"Step 1: collecting sources for {company['name']}")
    print(f"    model: {COLLECTION_MODEL}, search budget: {MAX_SEARCHES}\n")

    client = anthropic.Anthropic(api_key=read_api_key())
    response = run_research(client, company)
    record = build_record(company, slug, response)
    path = save_record(record, slug)

    stats = record["run_stats"]
    print("\nDone.")
    print(f"    searches run:   {stats['searches_run']} of {stats['search_budget']} allowed")
    print(f"    unique sources: {len(record['sources'])}")
    print(f"    tokens:         {stats['input_tokens']} in / {stats['output_tokens']} out")
    print(f"    est. cost:      ${stats['estimated_cost_usd']:.2f}")
    print(f"    findings:       {len(record['findings'])} characters")
    print(f"    saved to:       {path}")

    if stats["searches_run"] == stats["search_budget"]:
        print(
            "\n    NOTE: the search budget was fully consumed, so the research may\n"
            "    have been cut short. Check the 'Contradictions and gaps' section\n"
            "    for gaps the model attributes to the cap rather than to absence."
        )


if __name__ == "__main__":
    main()
