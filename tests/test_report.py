"""Tests for src/hand_scores.py and the assembly in src/report.py.

Step 4 makes no API call, so all of this is free by construction. The test that
earns its place is the transcription check: the hand-scores are the one input
nothing else can verify, and a single mistyped digit would show up in the report
as a disagreement that never happened.

Run with:  .venv/Scripts/python.exe tests/test_report.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import report  # noqa: E402
from hand_scores import HAND_CONFIDENCE, HAND_SCORES, STATED_TOTALS  # noqa: E402
from schema import CRITERION_NAMES  # noqa: E402
from scoring import weighted_total  # noqa: E402


def make_criteria(**overrides) -> dict:
    """A scored record's criteria block, all HIGH unless overridden."""
    return {
        name: {
            "score": 3,
            "raw_score": 3,
            "was_capped": False,
            "is_scored": True,
            "weight": 20,
            "weighted_points": 12.0,
            "confidence": overrides.get(name, "HIGH"),
            "evidence_status": "found",
            "justification": "Because.",
            "key_evidence_urls": [],
        }
        for name in CRITERION_NAMES
    }


def test_every_hand_score_reproduces_its_stated_total() -> None:
    # Arrange - the worksheet states a total per company; HAND_SCORES is a
    # transcription of the rows behind it
    for slug, stated in STATED_TOTALS.items():
        # Act
        computed, covered = weighted_total(HAND_SCORES[slug])

        # Assert - a typo here would surface in the report as a real disagreement
        assert round(computed) == stated, f"{slug}: computed {computed}, worksheet {stated}"
        assert covered == 100


def test_the_hand_scores_cover_every_criterion_for_every_company() -> None:
    # Arrange / Act / Assert - a missing criterion would silently drop out of the
    # comparison rather than fail
    for slug, scores in HAND_SCORES.items():
        assert set(scores) == set(CRITERION_NAMES), slug
        assert set(HAND_CONFIDENCE[slug]) == set(CRITERION_NAMES), slug


def test_the_hand_scores_are_inside_the_scale() -> None:
    # Arrange / Act / Assert - the anchors run 1 to 5 and nothing else is meaningful
    for slug, scores in HAND_SCORES.items():
        for name, value in scores.items():
            assert 1 <= value <= 5, f"{slug}.{name} = {value}"


def test_a_whole_total_loses_its_trailing_zero() -> None:
    # Arrange / Act / Assert - 86.0 implies a precision a 1-5 scale does not have
    assert report.format_score(86.0) == "86"
    assert report.format_score(85.5) == "85.5"


def test_all_high_confidence_says_so_instead_of_naming_a_criterion() -> None:
    # Arrange - every criterion HIGH. Naming one as "lowest" would read as a warning
    # about a company that has none.
    criteria = make_criteria()

    # Act / Assert
    assert report.weakest_confidence(criteria) == "none below HIGH"


def test_the_thinnest_criterion_is_the_one_reported() -> None:
    # Arrange - one LOW among HIGHs, plus a MEDIUM to make sure it picks the worst
    criteria = make_criteria(market="LOW", timing="MEDIUM")

    # Act
    weakest = report.weakest_confidence(criteria)

    # Assert
    assert weakest == "Market (LOW)", weakest


def test_a_criterion_with_no_confidence_does_not_win_the_comparison() -> None:
    # Arrange - not_searched stores confidence None, which must not be read as the
    # lowest possible value and reported as the weak spot
    criteria = make_criteria()
    criteria["timing"]["confidence"] = None
    criteria["market"]["confidence"] = "MEDIUM"

    # Act
    weakest = report.weakest_confidence(criteria)

    # Assert
    assert weakest == "Market (MEDIUM)", weakest


def test_the_generated_report_matches_the_scored_files() -> None:
    # Arrange - the point of assembling in Python is that no figure can drift from
    # the record it came from
    if not list(report.SCORED_DIR.glob(f"*{report.SCORED_SUFFIX}")):
        print("       (skipped: no scored records on disk)")
        return

    companies = report.load_companies()

    # Act
    document = report.build_report(companies)

    # Assert - every company present, every total present, ranking descending
    totals = [item["scored"]["total_out_of_100"] for item in companies]
    assert totals == sorted(totals, reverse=True), totals
    for item in companies:
        assert item["scored"]["company"]["name"] in document
        assert f"{report.format_score(item['scored']['total_out_of_100'])}/100" in document


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
