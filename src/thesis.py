"""Step 5 of the pipeline: synthesise a thesis across the scored companies.

The last step that needs a model, and the second one that runs on Opus per
scoping section 4d. Everything before this produced facts about companies one at
a time; this step looks across them and says what the pattern means, which is
the one thing no amount of Python can assemble.

It sees the scored records and the calibration outcome. Unlike every earlier
step it is allowed to see the hand-scores, because by this point the
human-versus-model gap is a finding to interpret rather than an answer to
protect.

Run with:  .venv\\Scripts\\python.exe src\\thesis.py
"""

import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import anthropic
import pydantic
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from hand_scores import HAND_SCORES, STATED_TOTALS
from report import CRITERION_LABELS, load_companies
from schema import CRITERION_NAMES
from scoring import CRITERION_WEIGHTS

# Section 4d: synthesis across companies is pattern-finding, not transcription.
THESIS_MODEL = "claude-opus-5"
MAX_OUTPUT_TOKENS = 32000

OUTPUT_PATH = Path("docs/04-thesis.md")
RECORD_PATH = Path("data/scored/thesis.json")

PRICE_PER_MTOK = {"input": 5.00, "output": 25.00}
TOKENS_PER_MILLION = 1_000_000

# A required field can be satisfied by a single word. The first run returned the
# literal string "placeholder" for the last section and the document was written
# anyway, so sections are now checked for length and for the stand-in strings a
# model reaches for when it means to come back to something.
MIN_SECTION_CHARS = 200
PLACEHOLDER_STRINGS = frozenset({"placeholder", "tbd", "todo", "n/a", "none", "..."})


def find_empty_sections(thesis: "Thesis") -> list[str]:
    """Name any section that is too short or is a stand-in rather than content."""
    empty = []
    for name, value in thesis.model_dump().items():
        text = value.strip()
        if (
            len(text) < MIN_SECTION_CHARS
            or text.lower().rstrip(".") in PLACEHOLDER_STRINGS
        ):
            empty.append(name)
    return empty


class Thesis(BaseModel):
    """The synthesis, in named parts so none of them can be quietly skipped."""

    executive_summary: str = Field(
        description=(
            "150-200 words. What someone who reads nothing else needs. State the "
            "conclusion first, not the method."
        )
    )
    what_the_ranking_shows: str = Field(
        description=(
            "The patterns across these companies that no single profile reveals. "
            "Markdown, a few paragraphs or bullets."
        )
    )
    the_thesis: str = Field(
        description=(
            "The actual argument: what to believe about this sub-sector and what "
            "follows from it. Take a position that could be wrong."
        )
    )
    what_would_falsify_it: str = Field(
        description=(
            "Concrete, observable events that would show the thesis is wrong. "
            "Named companies, named milestones, dates where possible."
        )
    )
    where_this_method_is_weakest: str = Field(
        description=(
            "The honest read on what the ranking cannot see, given how it was built."
        )
    )


THESIS_PROMPT = """You are writing the closing synthesis of a market map of Physical AI \
companies in Switzerland and Europe - robots and autonomous machines that perceive and act \
in the physical world.

# The criteria this ranking used

{criteria}

Two positions the weighting takes deliberately. Traction means units deployed at paying \
industrial customers, not money raised. Timing is capped at 10 because the "why now" of \
Physical AI is identical for every company here, so it cannot separate them.

# The scored companies

{companies}

# The calibration result

Five companies were scored by hand, blind, before the pipeline was written. Those scores \
are shown above beside the model's. Reading them:

{calibration}

# What to write

Look across these companies and say what the pattern means. You are not summarising the \
profiles - a reader can see those. You are answering what someone should believe about \
this sub-sector after seeing this evidence.

Take a position that could turn out to be wrong, and make it specific enough that someone \
could disagree with it. A thesis nobody could argue with is not a thesis. Name companies \
when they carry the point.

Ground every claim in the evidence above. If you want to say something the scores do not \
support, either leave it out or say plainly that it is a judgement beyond what was \
measured.

The sample is five companies chosen to test the method, not a survey of the sector. Do not \
write as though it were representative - say what it can carry.

Every section is part of the deliverable and must be written in full. Do not return a \
heading, a stand-in, or a note to yourself in any field. The last section in particular is \
the one a sceptical reader turns to first: say what this ranking cannot see, given that it \
reads only public sources, five companies, and a single search pass each."""


def read_api_key() -> str:
    load_dotenv()
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        sys.exit("FAIL: ANTHROPIC_API_KEY is missing. Run src/check_setup.py first.")
    return key


def render_criteria() -> str:
    """The criteria and weights, so the synthesis argues on the stated basis."""
    return "\n".join(
        f"- **{CRITERION_LABELS[name]}** (weight {CRITERION_WEIGHTS[name]})"
        for name in CRITERION_NAMES
    )


def render_companies(companies: list[dict]) -> str:
    """Each company's scores and the reasoning behind them, best score first."""
    blocks = []

    for position, item in enumerate(companies, start=1):
        scored = item["scored"]
        slug = item["slug"]
        hand_total = STATED_TOTALS.get(slug)

        lines = [
            f"## {position}. {scored['company']['name']}"
            f" - {scored['total_out_of_100']}/100"
            + (f" (hand-scored {hand_total}/100)" if hand_total else ""),
            f"{scored['company'].get('country', '')}"
            f" {scored['company'].get('description', '')}".strip(),
            "",
        ]

        for name in CRITERION_NAMES:
            criterion = scored["criteria"][name]
            score = (
                "not scored" if criterion["score"] is None else f"{criterion['score']}/5"
            )
            hand = HAND_SCORES.get(slug, {}).get(name)
            lines.append(
                f"**{CRITERION_LABELS[name]}: {score}**"
                + (f" (hand: {hand}/5)" if hand else "")
                + f" [confidence {criterion['confidence'] or 'none'}]"
            )
            lines.append(criterion["justification"])
            lines.append("")

        extracted = item["extracted"]
        if extracted and extracted.get("contradictions"):
            lines.append("Unresolved contradictions in the sources:")
            for contradiction in extracted["contradictions"]:
                lines.append(f"- {contradiction['description']}")
            lines.append("")

        blocks.append("\n".join(lines))

    return "\n".join(blocks)


def render_calibration(companies: list[dict]) -> str:
    """The human-versus-model gap, summed per criterion."""
    per_criterion = {name: 0 for name in CRITERION_NAMES}
    exact = 0
    counted = 0

    for item in companies:
        slug = item["slug"]
        if slug not in HAND_SCORES:
            continue
        for name in CRITERION_NAMES:
            model_score = item["scored"]["criteria"][name]["score"]
            if model_score is None:
                continue
            delta = model_score - HAND_SCORES[slug][name]
            per_criterion[name] += delta
            exact += delta == 0
            counted += 1

    hand_order = [
        slug for slug, _ in sorted(STATED_TOTALS.items(), key=lambda pair: -pair[1])
    ]
    model_order = [item["slug"] for item in companies if item["slug"] in STATED_TOTALS]

    lines = [
        f"- {exact} of {counted} criterion scores identical between hand and model.",
        "- Rank order is "
        + ("identical" if hand_order == model_order else "different")
        + " on both sides.",
        "- Sum of gaps per criterion, in notches (negative means the model scored lower):",
    ]
    lines += [
        f"  - {CRITERION_LABELS[name]}: {per_criterion[name]:+d}"
        for name in CRITERION_NAMES
    ]
    return "\n".join(lines)


def build_prompt(companies: list[dict]) -> str:
    return THESIS_PROMPT.format(
        criteria=render_criteria(),
        companies=render_companies(companies),
        calibration=render_calibration(companies),
    )


def render_document(thesis: Thesis, companies: list[dict], model: str) -> str:
    """Lay the synthesis out as the closing document of the market map."""
    return "\n".join(
        [
            "# Thesis — Physical AI in Switzerland and Europe",
            "",
            f"Written {date.today().isoformat()} on `{model}`, from the"
            f" {len(companies)} companies scored in"
            " [`03-market-map.md`](03-market-map.md).",
            "",
            "The synthesis below is the model's. The criteria it argues on, and the",
            "weighting behind them, are set out in [`00-scoping.md`](00-scoping.md) and were",
            "fixed before any company was scored.",
            "",
            "## Executive summary",
            "",
            thesis.executive_summary,
            "",
            "## What the ranking shows",
            "",
            thesis.what_the_ranking_shows,
            "",
            "## The thesis",
            "",
            thesis.the_thesis,
            "",
            "## What would falsify it",
            "",
            thesis.what_would_falsify_it,
            "",
            "## Where this method is weakest",
            "",
            thesis.where_this_method_is_weakest,
            "",
            "---",
            "",
            "The limitations of the method are stated at greater length in",
            "[`00-scoping.md` §6](00-scoping.md#6-known-limitations).",
            "",
        ]
    )


def main() -> None:
    companies = load_companies()
    prompt = build_prompt(companies)

    print(f"Step 5: thesis across {len(companies)} companies, model {THESIS_MODEL}")
    print(f"    prompt: {len(prompt):,} characters")

    client = anthropic.Anthropic(api_key=read_api_key())

    try:
        with client.messages.stream(
            model=THESIS_MODEL,
            max_tokens=MAX_OUTPUT_TOKENS,
            messages=[{"role": "user", "content": prompt}],
            output_format=Thesis,
        ) as stream:
            response = stream.get_final_message()
    except anthropic.APIStatusError as error:
        sys.exit(f"FAIL: API error (HTTP {error.status_code}): {error.message}")
    except anthropic.APIConnectionError:
        sys.exit("FAIL: could not reach the API. Check your internet connection.")
    except pydantic.ValidationError as error:
        sys.exit(
            f"""FAIL: the reply did not validate against the schema.
      If the error mentions invalid or unterminated JSON, the reply was cut off
      at the {MAX_OUTPUT_TOKENS:,}-token ceiling. Raise MAX_OUTPUT_TOKENS.
      {error}"""
        )

    if response.stop_reason == "max_tokens":
        sys.exit(
            f"""FAIL: the thesis hit the {MAX_OUTPUT_TOKENS:,}-token ceiling, so it would
      be incomplete. Nothing was written."""
        )

    thesis = response.parsed_output
    if thesis is None:
        sys.exit("FAIL: the model returned no parseable thesis.")

    empty = find_empty_sections(thesis)
    if empty:
        sys.exit(
            f"""FAIL: the model left {len(empty)} section(s) unwritten: {', '.join(empty)}.
      Nothing was written, because a thesis with a hole in it reads as complete.
      Re-run: the prompt now states that every section must be written in full."""
        )

    usage = response.usage
    cost = (
        usage.input_tokens * PRICE_PER_MTOK["input"]
        + usage.output_tokens * PRICE_PER_MTOK["output"]
    ) / TOKENS_PER_MILLION

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        render_document(thesis, companies, THESIS_MODEL), encoding="utf-8"
    )

    RECORD_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECORD_PATH.write_text(
        json.dumps(
            {
                "written_at": datetime.now(timezone.utc).isoformat(),
                "model": THESIS_MODEL,
                "pipeline_step": 5,
                "companies": [item["slug"] for item in companies],
                "thesis": thesis.model_dump(),
                "run_stats": {
                    "input_tokens": usage.input_tokens,
                    "output_tokens": usage.output_tokens,
                    "estimated_cost_usd": round(cost, 4),
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"    tokens: {usage.input_tokens:,} in / {usage.output_tokens:,} out")
    print(f"    cost:   ${cost:.3f}")
    print(f"\nWritten to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
