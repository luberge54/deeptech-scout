"""Data model for step 2, as specified in docs/02-extraction-schema.md.

Two layers, deliberately separated:

  * `ExtractionOutput` is what the model is allowed to produce. It carries no
    confidence field, because the model does not get to rate its own evidence.
  * `CriterionRecord` is what gets written to disk, with confidence derived in
    code from the evidence list.

Keeping these apart is what makes scoping section 4b enforceable rather than
a paragraph the model is trusted to remember.
"""

from enum import Enum
from urllib.parse import urlsplit, urlunsplit

from pydantic import BaseModel, Field

# The five criteria of docs/00-scoping.md section 3, in weight order. Step 3
# iterates this to apply the weights, so the names must not drift.
CRITERION_NAMES = (
    "field_traction",
    "team_execution",
    "technology",
    "market",
    "timing",
)


class SourceType(str, Enum):
    """Where a claim came from. Mirrors the section 4c sourcing table."""

    CUSTOMER_SIDE = "customer_side"
    TENDER_RECORD = "tender_record"
    TRADE_PRESS = "trade_press"
    VENDOR_CASE_STUDY = "vendor_case_study"
    FUNDING_PRESS = "funding_press"
    COMPANY_WEBSITE = "company_website"
    JOB_POSTING = "job_posting"
    AGGREGATOR = "aggregator"


# Sources that are not the company talking about itself. A direct claim from
# one of these is what separates HIGH confidence from MEDIUM.
INDEPENDENT_SOURCE_TYPES = frozenset(
    {SourceType.CUSTOMER_SIDE, SourceType.TENDER_RECORD, SourceType.TRADE_PRESS}
)

# Section 4c: hiring supports a score, it never establishes one. Pinned here so
# the rule survives a model that labels a job posting as direct evidence.
ALWAYS_INDIRECT_SOURCE_TYPES = frozenset({SourceType.JOB_POSTING})


class EvidenceGrade(str, Enum):
    DIRECT = "direct"
    INDIRECT = "indirect"


class EvidenceStatus(str, Enum):
    FOUND = "found"
    SEARCHED_NOT_FOUND = "searched_not_found"
    NOT_SEARCHED = "not_searched"


class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class EvidenceItem(BaseModel):
    """One sourced factual claim. Without a URL it is not usable and is dropped."""

    claim: str = Field(description="One factual sentence. No judgement of quality.")
    source_url: str = Field(description="The page this claim came from.")
    source_type: SourceType
    evidence_grade: EvidenceGrade
    published_date: str | None = Field(
        description="ISO date (YYYY-MM-DD) if the source states one, else null."
    )
    attributed_to: str | None = Field(
        description="Who makes the claim - the customer, the vendor, a journalist."
    )


class CriterionEvidence(BaseModel):
    """The model's output for one criterion: evidence and coverage, no rating."""

    evidence_status: EvidenceStatus
    evidence: list[EvidenceItem]
    not_found_notes: str | None = Field(
        description="When nothing was found or the area was not covered, what was "
        "looked for and why it is missing. Null when status is found."
    )


class Contradiction(BaseModel):
    """Figures that disagree across sources. Reconciling them belongs to step 3."""

    topic: str
    description: str
    source_urls: list[str]


class ExtractionOutput(BaseModel):
    """Exactly what the extraction model returns. Note the absence of confidence."""

    field_traction: CriterionEvidence
    team_execution: CriterionEvidence
    technology: CriterionEvidence
    market: CriterionEvidence
    timing: CriterionEvidence
    contradictions: list[Contradiction]


class CriterionRecord(BaseModel):
    """A criterion as stored: the model's evidence plus a computed confidence."""

    evidence_status: EvidenceStatus
    confidence: Confidence | None
    evidence: list[EvidenceItem]
    not_found_notes: str | None


def canonical_url(url: str) -> str:
    """Reduce a URL to a comparable form: lowercase host, no trailing slash.

    The model is asked to copy URLs verbatim, but a stray trailing slash or a
    capitalised host should not cost a real source its place in the record.
    Nothing beyond case and that slash is normalised - a different path is a
    different page, and treating it otherwise would defeat the check.
    """
    parts = urlsplit(url.strip())
    return urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path.rstrip("/"),
            parts.query,
            "",
        )
    )


def normalise_evidence(
    items: list[EvidenceItem], known_urls: set[str]
) -> list[EvidenceItem]:
    """Drop unusable items and re-apply the source rules the model may have missed.

    Three corrections are applied unconditionally, because they are project rules
    rather than model judgement:
      * an item without a source URL is discarded - an unsourced claim is the
        exact failure mode this project exists to avoid;
      * an item whose URL was not among the pages step 1 actually retrieved is
        discarded. The step 1 findings document names its sources in prose rather
        than by link, so a model asked for a URL will produce a plausible-looking
        domain instead of admitting it has none. Such a claim reads as audited and
        is not, which is worse than no claim at all;
      * a job posting is forced to `indirect` per section 4c.

    `known_urls` holds the canonical form of every URL step 1 retrieved.
    """
    cleaned: list[EvidenceItem] = []

    for item in items:
        if not item.source_url or not item.source_url.strip():
            continue

        if canonical_url(item.source_url) not in known_urls:
            continue

        if item.source_type in ALWAYS_INDIRECT_SOURCE_TYPES:
            item = item.model_copy(update={"evidence_grade": EvidenceGrade.INDIRECT})

        cleaned.append(item)

    return cleaned


def derive_confidence(
    status: EvidenceStatus, evidence: list[EvidenceItem]
) -> Confidence | None:
    """Compute the confidence flag from the evidence, per section 4 of the schema doc.

    Returns None for `not_searched`: an absent measurement gets no confidence
    level, because asserting one would imply the area was actually checked.
    """
    if status is EvidenceStatus.NOT_SEARCHED:
        return None

    if status is EvidenceStatus.SEARCHED_NOT_FOUND or not evidence:
        return Confidence.LOW

    has_independent_direct = any(
        item.evidence_grade is EvidenceGrade.DIRECT
        and item.source_type in INDEPENDENT_SOURCE_TYPES
        for item in evidence
    )
    return Confidence.HIGH if has_independent_direct else Confidence.MEDIUM


def build_criterion_record(
    criterion: CriterionEvidence, known_urls: set[str]
) -> CriterionRecord:
    """Turn raw model output into the stored record, applying the rules above.

    A `found` status with no usable evidence left after cleaning is downgraded to
    `searched_not_found`: the model looked and reported something, but nothing
    survived the sourcing rules, so the honest label is that nothing was found.
    """
    evidence = normalise_evidence(criterion.evidence, known_urls)

    status = criterion.evidence_status
    if status is EvidenceStatus.FOUND and not evidence:
        status = EvidenceStatus.SEARCHED_NOT_FOUND

    return CriterionRecord(
        evidence_status=status,
        confidence=derive_confidence(status, evidence),
        evidence=evidence,
        not_found_notes=criterion.not_found_notes,
    )
