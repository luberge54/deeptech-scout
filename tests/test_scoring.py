"""Tests for the rules in src/scoring.py and the offline parts of src/score.py.

Everything here runs without the API. Step 3 is the most expensive step in the
pipeline, so the arithmetic and the section 4b rules are pinned before any Opus
call is made rather than after.

Run with:  .venv/Scripts/python.exe tests/test_scoring.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import score  # noqa: E402
from scoring import (  # noqa: E402
    CRITERION_WEIGHTS,
    MISSING_EVIDENCE_CAP,
    CriterionScore,
    ScoringOutput,
    apply_missing_evidence_rule,
    score_company,
    weighted_total,
)

# ANYbotics as hand-scored in docs/calibration-worksheet.md, which totals 93/100.
HAND_SCORED_ANYBOTICS = {
    "field_traction": 5,
    "team_execution": 4,
    "technology": 5,
    "market": 5,
    "timing": 4,
}


def make_judgement(**scores: int) -> ScoringOutput:
    """A model judgement with the given scores and placeholder prose."""
    return ScoringOutput(
        **{
            name: CriterionScore(
                score=scores[name],
                justification="Because the evidence says so.",
                key_evidence_urls=["https://example.com/a"],
            )
            for name in CRITERION_WEIGHTS
        }
    )


def make_records(**statuses: str) -> dict:
    """Step 2 records carrying the given evidence_status per criterion."""
    return {
        name: {
            "evidence_status": statuses.get(name, "found"),
            "confidence": "HIGH",
            "evidence": [],
            "not_found_notes": None,
        }
        for name in CRITERION_WEIGHTS
    }


def test_the_weights_still_sum_to_one_hundred() -> None:
    # Arrange / Act / Assert - scoping section 3 is only coherent if they do
    assert sum(CRITERION_WEIGHTS.values()) == 100, CRITERION_WEIGHTS


def test_the_total_reproduces_the_hand_scored_worksheet() -> None:
    # Arrange - the worksheet computes weight * score / 5 and reaches 93 for ANYbotics
    # Act
    total, covered = weighted_total(HAND_SCORED_ANYBOTICS)

    # Assert - if this drifts, the calibration in scoping section 5 compares nothing
    assert round(total) == 93, total
    assert covered == 100


def test_a_perfect_set_of_scores_totals_exactly_one_hundred() -> None:
    # Arrange / Act
    total, _ = weighted_total({name: 5 for name in CRITERION_WEIGHTS})

    # Assert
    assert round(total, 6) == 100.0, total


def test_absent_evidence_caps_the_score_at_two() -> None:
    # Arrange - the model argued a 4 on a criterion where nothing was found
    # Act
    final, was_capped = apply_missing_evidence_rule(4, "searched_not_found")

    # Assert - section 4b: absence is never scored from what is plausible
    assert final == MISSING_EVIDENCE_CAP
    assert was_capped is True


def test_the_cap_does_not_raise_a_score_that_was_already_low() -> None:
    # Arrange - a 1 is below the cap and must stay a 1
    # Act
    final, was_capped = apply_missing_evidence_rule(1, "searched_not_found")

    # Assert - the cap is a ceiling, not a floor
    assert final == 1
    assert was_capped is False


def test_an_unmeasured_criterion_is_excluded_rather_than_scored_low() -> None:
    # Arrange - not_searched is a gap in the research, not a fact about the company
    # Act
    final, was_capped = apply_missing_evidence_rule(5, "not_searched")

    # Assert
    assert final is None
    assert was_capped is False


def test_excluding_a_criterion_rescales_instead_of_deducting_its_points() -> None:
    # Arrange - timing unmeasured, everything else a 3
    scores = {name: 3 for name in CRITERION_WEIGHTS}
    scores["timing"] = None

    # Act
    total, covered = weighted_total(scores)

    # Assert - straight 3s are 60/100 whether or not timing was measured. Deducting
    # timing's 10 points instead would turn a coverage gap into a weakness.
    assert round(total) == 60, total
    assert covered == 90


def test_scoring_nothing_at_all_is_an_error_rather_than_a_zero() -> None:
    # Arrange - every criterion unmeasured
    scores = {name: None for name in CRITERION_WEIGHTS}

    # Act / Assert - a company with no measurement has no score, and saying 0 would
    # be a statement about the company rather than about the research
    try:
        weighted_total(scores)
    except ValueError:
        return
    raise AssertionError("weighted_total should refuse to score nothing")


def test_score_company_applies_the_cap_and_records_that_it_did() -> None:
    # Arrange - the model argues 5 on traction, but step 2 found nothing there
    judgement = make_judgement(
        field_traction=5, team_execution=3, technology=3, market=3, timing=3
    )
    records = make_records(field_traction="searched_not_found")

    # Act
    result = score_company(judgement, records)

    # Assert - the cap bit, the raw judgement is preserved, and the flag is visible
    assert result["criteria"]["field_traction"]["score"] == 2
    assert result["criteria"]["field_traction"]["raw_score"] == 5
    assert result["criteria"]["field_traction"]["was_capped"] is True
    assert result["criteria_capped"] == ["field_traction"]


def test_score_company_reports_a_criterion_it_did_not_score() -> None:
    # Arrange
    judgement = make_judgement(
        field_traction=4, team_execution=4, technology=4, market=4, timing=4
    )
    records = make_records(timing="not_searched")

    # Act
    result = score_company(judgement, records)

    # Assert - the reader must be able to see what the total does not cover
    assert result["criteria"]["timing"]["is_scored"] is False
    assert result["criteria"]["timing"]["weighted_points"] == 0.0
    assert result["criteria_not_scored"] == ["timing"]
    assert result["weight_covered"] == 90


def test_the_output_schema_is_usable_as_a_structured_output() -> None:
    # Arrange - a schema the API rejects would fail only after an Opus call is paid for
    from anthropic.lib._parse._transform import transform_schema
    from pydantic import TypeAdapter

    # Act
    transformed = transform_schema(TypeAdapter(ScoringOutput).json_schema())

    # Assert - every criterion present and required, no optional field to omit
    assert set(transformed["required"]) == set(CRITERION_WEIGHTS), transformed["required"]


def test_the_rendered_evidence_shows_who_actually_made_each_claim() -> None:
    # Arrange - a trade-press item that only repeats a company claim. Without
    # attributed_to the model reads it as third-party confirmation.
    record = {
        "criteria": {
            name: {
                "evidence_status": "found",
                "confidence": "HIGH",
                "evidence": [],
                "not_found_notes": None,
            }
            for name in CRITERION_WEIGHTS
        },
        "contradictions": [],
    }
    record["criteria"]["field_traction"]["evidence"] = [
        {
            "claim": "Pilots with unnamed Fortune 500 manufacturers.",
            "source_url": "https://example.com/a",
            "source_type": "trade_press",
            "evidence_grade": "indirect",
            "attributed_to": "company",
        }
    ]

    # Act
    rendered = score.render_evidence(record)

    # Assert
    assert "claimed by: company" in rendered
    assert "trade_press" in rendered
    assert "https://example.com/a" in rendered


def main() -> None:
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    failures = 0

    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as error:
            failures += 1
            print(f"  FAIL  {test.__name__}: {error}")

    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
