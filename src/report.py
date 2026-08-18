"""Step 4 of the pipeline: assemble the market map from the scored records.

This step makes no API call. Scoping section 4d allocated Sonnet to it on the
grounds that report generation is "formatting already-decided content" - and
once that is true, a model is the wrong tool. Every number here is computed from
the files on disk and every judgement is quoted verbatim from step 3, so the
report cannot drift from what was actually scored. It is also free and
reproducible, which matters for a document that will be regenerated each time a
company is added.

The prose that required judgement was already written by Opus in step 3. Asking
Sonnet to paraphrase it would add a chance of distortion and nothing else.

Run with:  .venv\\Scripts\\python.exe src\\report.py
"""

import json
import sys
from datetime import date
from pathlib import Path

from hand_scores import HAND_CONFIDENCE, HAND_SCORES, STATED_TOTALS
from schema import CRITERION_NAMES

SCORED_DIR = Path("data/scored")
EXTRACTED_DIR = Path("data/output")
COLLECTED_DIR = Path("data/raw")
OUTPUT_PATH = Path("docs/03-market-map.md")

SCORED_SUFFIX = ".scored.json"
CRITERION_LABELS = {
    "field_traction": "Field traction",
    "team_execution": "Team / execution",
    "technology": "Technology",
    "market": "Market",
    "timing": "Timing",
}


CONFIDENCE_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}


def format_score(total: float) -> str:
    """86.0 reads as 86. A trailing .0 suggests a precision the scale does not have."""
    return f"{total:.0f}" if float(total).is_integer() else f"{total:.1f}"


def weakest_confidence(criteria: dict) -> str:
    """Name the thinnest criterion, or say plainly that none is thin."""
    scored = {
        name: record for name, record in criteria.items() if record["confidence"]
    }
    if not scored:
        return "not scored"

    name, record = min(
        scored.items(), key=lambda pair: CONFIDENCE_ORDER.get(pair[1]["confidence"], 0)
    )
    if record["confidence"] == "HIGH":
        return "none below HIGH"
    return f"{CRITERION_LABELS[name]} ({record['confidence']})"


def load_companies() -> list[dict]:
    """Read every scored record with its extracted counterpart, best score first."""
    companies = []

    for path in sorted(SCORED_DIR.glob(f"*{SCORED_SUFFIX}")):
        slug = path.name[: -len(SCORED_SUFFIX)]
        scored = json.loads(path.read_text(encoding="utf-8"))
        extracted_path = EXTRACTED_DIR / f"{slug}.extracted.json"
        companies.append(
            {
                "slug": slug,
                "scored": scored,
                "extracted": json.loads(extracted_path.read_text(encoding="utf-8"))
                if extracted_path.exists()
                else None,
            }
        )

    if not companies:
        sys.exit(f"FAIL: no scored records in {SCORED_DIR}. Run step 3 first.")

    return sorted(companies, key=lambda item: -item["scored"]["total_out_of_100"])


def total_pipeline_cost() -> float:
    """What the whole run cost, summed from the files each step wrote."""
    total = 0.0
    # The thesis record lives in the scored directory but does not carry the
    # .scored.json suffix, so it needs naming separately or step 5 goes uncounted.
    patterns = [
        (COLLECTED_DIR, "*.json"),
        (EXTRACTED_DIR, "*.extracted.json"),
        (SCORED_DIR, f"*{SCORED_SUFFIX}"),
        (SCORED_DIR, "thesis.json"),
    ]

    for directory, pattern in patterns:
        for path in directory.glob(pattern):
            record = json.loads(path.read_text(encoding="utf-8"))
            total += record.get("run_stats", {}).get("estimated_cost_usd", 0.0)

    return total


def render_ranking(companies: list[dict]) -> str:
    """The ranking table, with the hand-score beside it."""
    lines = [
        "## 1. The ranking",
        "",
        "| # | Company | Score | Hand-score | Gap | Lowest-confidence criterion |",
        "|---|---------|-------|------------|-----|------------------------------|",
    ]

    for position, item in enumerate(companies, start=1):
        scored = item["scored"]
        slug = item["slug"]
        total = scored["total_out_of_100"]
        hand = STATED_TOTALS.get(slug)
        gap = f"{total - hand:+.0f}" if hand else "—"

        lines.append(
            f"| {position} | **{scored['company']['name']}** |"
            f" **{format_score(total)}/100** | {hand or '—'}/100 | {gap} |"
            f" {weakest_confidence(scored['criteria'])} |"
        )

    return "\n".join(lines)


def render_calibration(companies: list[dict]) -> str:
    """Where the model and the blind hand-score disagree, and by how much."""
    lines = [
        "## 2. Calibration — the model against a blind hand-score",
        "",
        "Five companies were scored by hand before any pipeline code existed. The model",
        "never saw those scores. The comparison is the point of this project: a ranking",
        "nobody has checked is an opinion with extra steps.",
        "",
        "Disagreement per criterion, in notches out of 5. A negative number means the",
        "model scored lower than the hand-score.",
        "",
        "| Company | " + " | ".join(CRITERION_LABELS[n] for n in CRITERION_NAMES) + " | Total gap |",
        "|---------|" + "|".join(["---"] * (len(CRITERION_NAMES) + 1)) + "|",
    ]

    per_criterion = {name: 0 for name in CRITERION_NAMES}
    exact = 0
    within_one = 0
    counted = 0

    for item in companies:
        slug = item["slug"]
        if slug not in HAND_SCORES:
            continue

        cells = []
        for name in CRITERION_NAMES:
            model_score = item["scored"]["criteria"][name]["score"]
            if model_score is None:
                cells.append("not scored")
                continue
            delta = model_score - HAND_SCORES[slug][name]
            per_criterion[name] += delta
            counted += 1
            exact += delta == 0
            within_one += abs(delta) <= 1
            cells.append(f"{delta:+d}" if delta else "—")

        total_gap = item["scored"]["total_out_of_100"] - STATED_TOTALS[slug]
        lines.append(
            f"| {item['scored']['company']['name']} | "
            + " | ".join(cells)
            + f" | **{total_gap:+.0f}** |"
        )

    lines.append(
        "| **Sum** | "
        + " | ".join(f"**{per_criterion[n]:+d}**" for n in CRITERION_NAMES)
        + " | |"
    )

    hand_order = [
        slug
        for slug, _ in sorted(STATED_TOTALS.items(), key=lambda pair: -pair[1])
        if slug in {item["slug"] for item in companies}
    ]
    model_order = [item["slug"] for item in companies if item["slug"] in STATED_TOTALS]

    names = {item["slug"]: item["scored"]["company"]["name"] for item in companies}

    lines += [
        "",
        f"**Agreement: {exact} of {counted} criterion scores identical, "
        f"{within_one} of {counted} within one notch.**",
        "",
        "**Rank order: "
        + ("identical on both sides." if hand_order == model_order else "the two disagree.")
        + "**",
        "",
        "Hand: " + " > ".join(names[slug] for slug in hand_order),
        "",
        "Model: " + " > ".join(names[slug] for slug in model_order),
        "",
        "The argued verdict on each disagreement is in",
        "[`00-scoping.md` §5](00-scoping.md#5-calibration-set).",
    ]

    return "\n".join(lines)


def render_company(position: int, item: dict) -> str:
    """One company: the score breakdown, then step 3's reasoning verbatim."""
    scored = item["scored"]
    company = scored["company"]
    slug = item["slug"]

    lines = [
        f"### {position}. {company['name']} — {format_score(scored['total_out_of_100'])}/100",
        "",
        f"{company.get('country', 'Europe')}"
        + (f" · {company['description']}" if company.get("description") else ""),
        "",
        "| Criterion | Score | Weight | Points | Confidence | Hand-score |",
        "|-----------|-------|--------|--------|------------|------------|",
    ]

    for name in CRITERION_NAMES:
        criterion = scored["criteria"][name]
        score = "not scored" if criterion["score"] is None else f"{criterion['score']}/5"
        capped = " (capped)" if criterion["was_capped"] else ""
        hand = HAND_SCORES.get(slug, {}).get(name)
        hand_confidence = HAND_CONFIDENCE.get(slug, {}).get(name, "")
        lines.append(
            f"| {CRITERION_LABELS[name]} | {score}{capped} | {criterion['weight']} |"
            f" {criterion['weighted_points']:.1f} | {criterion['confidence'] or '—'} |"
            f" {f'{hand}/5 ({hand_confidence})' if hand else '—'} |"
        )

    lines += ["", "**Why these scores**", ""]

    for name in CRITERION_NAMES:
        criterion = scored["criteria"][name]
        lines.append(f"*{CRITERION_LABELS[name]}.* {criterion['justification']}")
        if criterion["key_evidence_urls"]:
            sources = ", ".join(
                f"[{index}]({url})"
                for index, url in enumerate(criterion["key_evidence_urls"], start=1)
            )
            lines.append(f"Sources: {sources}")
        lines.append("")

    extracted = item["extracted"]
    if extracted and extracted.get("contradictions"):
        lines += ["**Contradictions in the sources, left unresolved**", ""]
        for contradiction in extracted["contradictions"]:
            lines.append(f"- {contradiction['description']}")
        lines.append("")

    return "\n".join(lines)


def render_coverage(companies: list[dict]) -> str:
    """What the ranking rests on, stated in numbers rather than adjectives."""
    lines = [
        "## 4. What this rests on",
        "",
        "| Company | Sources retrieved | Evidence items kept | Searches | Budget spent? |",
        "|---------|-------------------|---------------------|----------|---------------|",
    ]

    for item in companies:
        slug = item["slug"]
        collected_path = COLLECTED_DIR / f"{slug}.json"
        collected = (
            json.loads(collected_path.read_text(encoding="utf-8"))
            if collected_path.exists()
            else {}
        )
        stats = collected.get("run_stats", {})
        evidence_count = (
            sum(
                len(criterion["evidence"])
                for criterion in item["extracted"]["criteria"].values()
            )
            if item["extracted"]
            else 0
        )
        exhausted = stats.get("searches_run") == stats.get("search_budget")

        lines.append(
            f"| {item['scored']['company']['name']} | {len(collected.get('sources', []))} |"
            f" {evidence_count} | {stats.get('searches_run', '—')}"
            f"/{stats.get('search_budget', '—')} |"
            f" {'yes' if exhausted else 'no'} |"
        )

    lines += [
        "",
        "Every evidence item behind these scores carries a URL that was checked against the",
        "pages the research actually retrieved; a claim citing anything else was discarded",
        "before scoring. A `yes` in the last column means the research spent its whole search",
        "budget, so a gap in that company's evidence may be a limit of the search rather than",
        "an absence in the world.",
        "",
        "The limitations of this method are stated in",
        "[`00-scoping.md` §6](00-scoping.md#6-known-limitations). They are worth reading before",
        "the ranking is used for anything.",
    ]

    return "\n".join(lines)


def render_provenance(companies: list[dict]) -> str:
    """Which model produced what, and what it cost."""
    scoring_models = {item["scored"]["model"] for item in companies}
    extraction_models = {
        item["extracted"]["model"] for item in companies if item["extracted"]
    }

    return "\n".join(
        [
            "## 5. Provenance",
            "",
            f"- Collection and extraction: `{', '.join(sorted(extraction_models))}`",
            f"- Scoring: `{', '.join(sorted(scoring_models))}`",
            "- Report assembly: no model. Every figure above is computed from the stored",
            "  records, and every justification is quoted verbatim from the scoring step.",
            f"- Total API cost of the run behind this report: **${total_pipeline_cost():.2f}**",
            "",
            "Regenerate with `.venv\\Scripts\\python.exe src\\report.py`.",
        ]
    )


def build_report(companies: list[dict]) -> str:
    """Assemble the whole document."""
    sections = [
        "# Physical AI in Switzerland and Europe — an opinionated market map",
        "",
        f"Generated {date.today().isoformat()} from {len(companies)} scored companies.",
        "",
        "This ranks companies building robots and autonomous machines that perceive and act",
        "in the physical world. The criteria and their weights are the argument; the scores",
        "are its consequence. Both are stated in",
        "[`00-scoping.md`](00-scoping.md) and were fixed before any company was scored.",
        "",
        "The weighting takes two positions worth disagreeing with: traction is redefined as",
        "units deployed at paying customers rather than money raised, and timing is capped at",
        "10 because the \"why now\" of Physical AI is identical for every company here.",
        "",
        render_ranking(companies),
        "",
        render_calibration(companies),
        "",
        "## 3. The companies",
        "",
    ]

    for position, item in enumerate(companies, start=1):
        sections.append(render_company(position, item))

    sections += [render_coverage(companies), "", render_provenance(companies), ""]

    return "\n".join(sections)


def main() -> None:
    companies = load_companies()
    report = build_report(companies)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(report, encoding="utf-8")

    print(f"Step 4: market map assembled from {len(companies)} companies, no API call.")
    for position, item in enumerate(companies, start=1):
        scored = item["scored"]
        print(
            f"    {position}. {scored['company']['name']:<18}"
            f" {format_score(scored['total_out_of_100']):>3}/100"
        )
    print(f"\nWritten to {OUTPUT_PATH}  ({len(report):,} characters)")


if __name__ == "__main__":
    main()
