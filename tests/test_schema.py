"""Tests for the rules encoded in src/schema.py.

These cover the project rules that must not depend on the model behaving well:
the sourcing rules of scoping section 4c and the confidence derivation of
schema doc section 4. Run with:

    .venv\\Scripts\\python.exe tests\\test_schema.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from schema import (  # noqa: E402
    Confidence,
    CriterionEvidence,
    EvidenceGrade,
    EvidenceItem,
    EvidenceStatus,
    SourceType,
    build_criterion_record,
    derive_confidence,
    normalise_evidence,
)


def make_item(
    source_type: SourceType,
    grade: EvidenceGrade = EvidenceGrade.DIRECT,
    source_url: str = "https://example.com/a",
) -> EvidenceItem:
    return EvidenceItem(
        claim="A robot was deployed at a named site.",
        source_url=source_url,
        source_type=source_type,
        evidence_grade=grade,
        published_date=None,
        attributed_to=None,
    )


def test_job_postings_are_forced_to_indirect() -> None:
    # Arrange - the model wrongly labels a job posting as direct evidence
    items = [make_item(SourceType.JOB_POSTING, EvidenceGrade.DIRECT)]

    # Act
    cleaned = normalise_evidence(items)

    # Assert - section 4c pins hiring signals to indirect regardless
    assert cleaned[0].evidence_grade is EvidenceGrade.INDIRECT


def test_claims_without_a_source_url_are_dropped() -> None:
    # Arrange
    items = [
        make_item(SourceType.TRADE_PRESS, source_url="   "),
        make_item(SourceType.TRADE_PRESS, source_url="https://example.com/real"),
    ]

    # Act
    cleaned = normalise_evidence(items)

    # Assert
    assert len(cleaned) == 1
    assert cleaned[0].source_url == "https://example.com/real"


def test_direct_evidence_from_an_independent_source_gives_high() -> None:
    items = [make_item(SourceType.CUSTOMER_SIDE, EvidenceGrade.DIRECT)]
    assert derive_confidence(EvidenceStatus.FOUND, items) is Confidence.HIGH


def test_vendor_sourced_direct_evidence_only_gives_medium() -> None:
    # A vendor case study naming a customer is still the vendor talking
    items = [make_item(SourceType.VENDOR_CASE_STUDY, EvidenceGrade.DIRECT)]
    assert derive_confidence(EvidenceStatus.FOUND, items) is Confidence.MEDIUM


def test_indirect_evidence_from_an_independent_source_gives_medium() -> None:
    items = [make_item(SourceType.TRADE_PRESS, EvidenceGrade.INDIRECT)]
    assert derive_confidence(EvidenceStatus.FOUND, items) is Confidence.MEDIUM


def test_searched_not_found_gives_low() -> None:
    assert derive_confidence(EvidenceStatus.SEARCHED_NOT_FOUND, []) is Confidence.LOW


def test_not_searched_asserts_no_confidence_at_all() -> None:
    # An absent measurement gets no confidence level - asserting one would imply
    # the area was actually checked
    assert derive_confidence(EvidenceStatus.NOT_SEARCHED, []) is None


def test_found_with_no_usable_evidence_is_downgraded() -> None:
    # Arrange - the model claims evidence exists but every item is unsourced
    criterion = CriterionEvidence(
        evidence_status=EvidenceStatus.FOUND,
        evidence=[make_item(SourceType.TRADE_PRESS, source_url="")],
        not_found_notes=None,
    )

    # Act
    record = build_criterion_record(criterion)

    # Assert - nothing survived the sourcing rules, so nothing was found
    assert record.evidence_status is EvidenceStatus.SEARCHED_NOT_FOUND
    assert record.confidence is Confidence.LOW
    assert record.evidence == []


def test_not_searched_survives_the_record_build() -> None:
    criterion = CriterionEvidence(
        evidence_status=EvidenceStatus.NOT_SEARCHED,
        evidence=[],
        not_found_notes="Search budget exhausted before patents were covered.",
    )
    record = build_criterion_record(criterion)

    assert record.evidence_status is EvidenceStatus.NOT_SEARCHED
    assert record.confidence is None


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
