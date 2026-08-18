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
    DirectEvidenceKind,
    CriterionEvidence,
    EvidenceGrade,
    EvidenceItem,
    EvidenceStatus,
    SourceType,
    build_criterion_record,
    canonical_url,
    derive_confidence,
    normalise_evidence,
)


# Every URL make_item can produce, in canonical form. Real runs build this from the
# pages step 1 retrieved; the tests need the same allow-list to exist.
KNOWN_URLS = {
    "https://example.com/a",
    "https://example.com/real",
}


def make_item(
    source_type: SourceType,
    grade: EvidenceGrade = EvidenceGrade.DIRECT,
    source_url: str = "https://example.com/a",
    direct_because: DirectEvidenceKind = DirectEvidenceKind.NAMED_CUSTOMER,
) -> EvidenceItem:
    return EvidenceItem(
        claim="A robot was deployed at a named site.",
        source_url=source_url,
        source_type=source_type,
        evidence_grade=grade,
        direct_because=direct_because,
        published_date=None,
        attributed_to=None,
    )


def test_job_postings_are_forced_to_indirect() -> None:
    # Arrange - the model wrongly labels a job posting as direct evidence
    items = [make_item(SourceType.JOB_POSTING, EvidenceGrade.DIRECT)]

    # Act
    cleaned = normalise_evidence(items, KNOWN_URLS)

    # Assert - section 4c pins hiring signals to indirect regardless
    assert cleaned[0].evidence_grade is EvidenceGrade.INDIRECT


def test_claims_without_a_source_url_are_dropped() -> None:
    # Arrange
    items = [
        make_item(SourceType.TRADE_PRESS, source_url="   "),
        make_item(SourceType.TRADE_PRESS, source_url="https://example.com/real"),
    ]

    # Act
    cleaned = normalise_evidence(items, KNOWN_URLS)

    # Assert
    assert len(cleaned) == 1
    assert cleaned[0].source_url == "https://example.com/real"


def test_two_independent_direct_sources_give_high() -> None:
    # Arrange - HIGH means corroborated: more than one party said so
    items = [
        make_item(SourceType.CUSTOMER_SIDE, EvidenceGrade.DIRECT),
        make_item(SourceType.TRADE_PRESS, EvidenceGrade.DIRECT),
    ]

    # Act / Assert
    assert derive_confidence(EvidenceStatus.FOUND, items) is Confidence.HIGH


def test_a_single_independent_direct_source_only_gives_medium() -> None:
    # Arrange - the mimic robotics case: field traction read HIGH on one item, and
    # that item was a product announcement filed under traction. One source cannot
    # be checked against anything.
    items = [make_item(SourceType.CUSTOMER_SIDE, EvidenceGrade.DIRECT)]

    # Act / Assert
    assert derive_confidence(EvidenceStatus.FOUND, items) is Confidence.MEDIUM


def test_many_weak_sources_do_not_add_up_to_high() -> None:
    # Arrange - six indirect items are still nobody confirming anything directly
    items = [make_item(SourceType.TRADE_PRESS, EvidenceGrade.INDIRECT) for _ in range(6)]

    # Act / Assert - counting corroboration must not become counting volume
    assert derive_confidence(EvidenceStatus.FOUND, items) is Confidence.MEDIUM


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
    record = build_criterion_record(criterion, KNOWN_URLS)

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
    record = build_criterion_record(criterion, KNOWN_URLS)

    assert record.evidence_status is EvidenceStatus.NOT_SEARCHED
    assert record.confidence is None


def test_a_claim_citing_a_page_step_1_never_retrieved_is_dropped() -> None:
    # Arrange - the real failure: asked for a URL it did not have, the model wrote a
    # plausible-looking domain instead. All 50 ANYbotics claims looked like this.
    items = [
        make_item(SourceType.CUSTOMER_SIDE, source_url="outokumpu.com"),
        make_item(SourceType.TRADE_PRESS, source_url="https://example.com/real"),
    ]

    # Act
    cleaned = normalise_evidence(items, KNOWN_URLS)

    # Assert - an invented source is worse than no claim, because it reads as audited
    assert len(cleaned) == 1, cleaned
    assert cleaned[0].source_url == "https://example.com/real"


def test_a_trailing_slash_does_not_cost_a_real_source_its_place() -> None:
    # Arrange - a genuine page, cited with one character of drift
    items = [make_item(SourceType.TRADE_PRESS, source_url="https://Example.com/real/")]

    # Act
    cleaned = normalise_evidence(items, KNOWN_URLS)

    # Assert - case and a trailing slash are noise, not a different page
    assert len(cleaned) == 1, cleaned


def test_a_different_path_on_a_known_host_is_still_rejected() -> None:
    # Arrange - same site, page that was never retrieved. Normalising the host must
    # not quietly widen the allow-list to a whole domain.
    items = [make_item(SourceType.TRADE_PRESS, source_url="https://example.com/invented")]

    # Act
    cleaned = normalise_evidence(items, KNOWN_URLS)

    # Assert
    assert cleaned == [], cleaned


def test_confidence_cannot_be_high_on_evidence_that_was_all_invented() -> None:
    # Arrange - the shape that produced ANYbotics' five HIGH ratings: independent,
    # direct, and every URL fabricated
    criterion = CriterionEvidence(
        evidence_status=EvidenceStatus.FOUND,
        evidence=[
            make_item(SourceType.CUSTOMER_SIDE, source_url="outokumpu.com"),
            make_item(SourceType.TRADE_PRESS, source_url="petronas.com"),
        ],
        not_found_notes=None,
    )

    # Act
    record = build_criterion_record(criterion, KNOWN_URLS)

    # Assert - nothing survived, so the honest label is that nothing was found
    assert record.evidence == []
    assert record.evidence_status is EvidenceStatus.SEARCHED_NOT_FOUND
    assert record.confidence is Confidence.LOW


def test_canonical_url_leaves_a_meaningful_difference_alone() -> None:
    # Arrange / Act / Assert - the query string can select the page, so it is kept
    assert canonical_url("https://a.com/p?id=1") != canonical_url("https://a.com/p?id=2")
    assert canonical_url("https://A.com/p/") == canonical_url("https://a.com/p")


def test_a_direct_item_naming_nothing_concrete_is_downgraded() -> None:
    # Arrange - the mimic case: a product announcement graded direct, with no
    # customer, site, unit count or agreement anywhere in it
    items = [
        make_item(
            SourceType.TRADE_PRESS,
            EvidenceGrade.DIRECT,
            direct_because=DirectEvidenceKind.NONE,
        )
    ]

    # Act
    cleaned = normalise_evidence(items, KNOWN_URLS)

    # Assert - the claim is kept, the grade it did not earn is not
    assert len(cleaned) == 1
    assert cleaned[0].evidence_grade is EvidenceGrade.INDIRECT


def test_a_downgraded_item_can_no_longer_carry_high_confidence() -> None:
    # Arrange - two independent trade-press items, neither naming anything concrete.
    # Under the old rules this reached HIGH; it is exactly the shape that lifted
    # mimic robotics' weakest criterion.
    items = [
        make_item(
            SourceType.TRADE_PRESS,
            EvidenceGrade.DIRECT,
            source_url="https://example.com/a",
            direct_because=DirectEvidenceKind.NONE,
        ),
        make_item(
            SourceType.CUSTOMER_SIDE,
            EvidenceGrade.DIRECT,
            source_url="https://example.com/real",
            direct_because=DirectEvidenceKind.NONE,
        ),
    ]

    # Act
    cleaned = normalise_evidence(items, KNOWN_URLS)

    # Assert
    assert derive_confidence(EvidenceStatus.FOUND, cleaned) is Confidence.MEDIUM


def test_naming_something_concrete_keeps_the_direct_grade() -> None:
    # Arrange - the check must not punish real evidence
    for kind in [
        DirectEvidenceKind.NAMED_CUSTOMER,
        DirectEvidenceKind.UNIT_COUNT,
        DirectEvidenceKind.SIGNED_AGREEMENT,
        DirectEvidenceKind.DATED_DEPLOYMENT,
        DirectEvidenceKind.REGULATORY_RECORD,
    ]:
        items = [make_item(SourceType.CUSTOMER_SIDE, EvidenceGrade.DIRECT, direct_because=kind)]

        # Act / Assert
        assert normalise_evidence(items, KNOWN_URLS)[0].evidence_grade is EvidenceGrade.DIRECT, kind


def test_a_record_predating_the_field_is_left_alone() -> None:
    # Arrange - not_stated means the record was written before the field existed.
    # Re-grading it would silently rewrite evidence nobody re-examined.
    items = [
        make_item(
            SourceType.CUSTOMER_SIDE,
            EvidenceGrade.DIRECT,
            direct_because=DirectEvidenceKind.NOT_STATED,
        )
    ]

    # Act / Assert
    assert normalise_evidence(items, KNOWN_URLS)[0].evidence_grade is EvidenceGrade.DIRECT


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
