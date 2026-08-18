"""Rules for step 3, weighted scoring.

Step 3 is the only step of the pipeline that is pure judgement, so it runs on
Opus per scoping section 4d. The model assigns a 1-5 value per criterion and
argues for it. Everything that must hold regardless of how the model behaves
lives here in Python rather than in the prompt: the section 4b cap on absent
evidence, the exclusion of criteria that were never measured, and the weighted
total itself.

The model never sees the hand-scores, and it never computes the total. Both
would make the calibration in scoping section 5 meaningless.
"""

from pydantic import BaseModel, Field

from schema import CRITERION_NAMES, EvidenceStatus

# Section 3 of docs/00-scoping.md. The comparison with the hand-scores only
# holds if these stay identical to the worksheet's anchor table.
CRITERION_WEIGHTS = {
    "field_traction": 30,
    "team_execution": 25,
    "technology": 20,
    "market": 15,
    "timing": 10,
}

# Section 4: anchors are defined at 1, 3 and 5; 2 and 4 sit between them.
MIN_SCORE = 1
MAX_SCORE = 5

# Section 4b: where evidence is absent the score is capped rather than guessed.
MISSING_EVIDENCE_CAP = 2

# The worksheet's weighted column is weight * score / 5, so a full set of 5s
# totals exactly 100. Kept as a named constant so the formula reads as itself.
POINTS_FOR_TOP_SCORE = 5


class CriterionScore(BaseModel):
    """One criterion as the model returns it. No confidence field: step 2 owns that."""

    score: int = Field(
        ge=MIN_SCORE,
        le=MAX_SCORE,
        description="1 to 5, anchored on the scale in scoping section 4.",
    )
    justification: str = Field(
        description="Why this score and not the one above or below it. Cite the evidence."
    )
    key_evidence_urls: list[str] = Field(
        description="The URLs from the record that carry this score. Copy them verbatim."
    )


class ScoringOutput(BaseModel):
    """Exactly what the scoring model returns. Note the absence of a total."""

    field_traction: CriterionScore
    team_execution: CriterionScore
    technology: CriterionScore
    market: CriterionScore
    timing: CriterionScore


class ScoredCriterion(BaseModel):
    """A criterion as stored: the model's judgement plus the rules applied to it."""

    score: int | None
    raw_score: int
    was_capped: bool
    is_scored: bool
    weight: int
    weighted_points: float
    confidence: str | None
    evidence_status: str
    justification: str
    key_evidence_urls: list[str]


def apply_missing_evidence_rule(
    score: int, evidence_status: EvidenceStatus | str
) -> tuple[int | None, bool]:
    """Enforce section 4b on one criterion.

    Returns the score that counts and whether the cap bit. A `not_searched`
    criterion returns None: it was never measured, so it is excluded from the
    total rather than scored low. Scoring it would turn a gap in the research
    into a statement about the company.
    """
    status = EvidenceStatus(evidence_status)

    if status is EvidenceStatus.NOT_SEARCHED:
        return None, False

    if status is EvidenceStatus.SEARCHED_NOT_FOUND:
        return min(score, MISSING_EVIDENCE_CAP), score > MISSING_EVIDENCE_CAP

    return score, False


def weighted_total(final_scores: dict[str, int | None]) -> tuple[float, int]:
    """Total out of 100, over the criteria that were actually measured.

    Returns the total and the weight it was computed over. When every criterion
    is scored that weight is 100 and the arithmetic matches the worksheet exactly.
    When one is excluded the remainder is rescaled to 100, because dropping its
    points outright would read as a weakness - which is what section 4b forbids.
    A rescaled total is not directly comparable to a full one, so callers report
    the weight alongside it.
    """
    scored = {name: value for name, value in final_scores.items() if value is not None}
    if not scored:
        raise ValueError("no criterion was measured, so there is nothing to score")

    covered_weight = sum(CRITERION_WEIGHTS[name] for name in scored)
    earned = sum(
        CRITERION_WEIGHTS[name] * value / POINTS_FOR_TOP_SCORE
        for name, value in scored.items()
    )
    return earned / covered_weight * 100, covered_weight


def score_company(judgement: ScoringOutput, criteria_records: dict) -> dict:
    """Combine the model's judgement with step 2's evidence into the stored record."""
    scored: dict[str, ScoredCriterion] = {}
    final_scores: dict[str, int | None] = {}

    for name in CRITERION_NAMES:
        record = criteria_records[name]
        model_score = getattr(judgement, name)
        final, was_capped = apply_missing_evidence_rule(
            model_score.score, record["evidence_status"]
        )
        final_scores[name] = final
        weight = CRITERION_WEIGHTS[name]
        scored[name] = ScoredCriterion(
            score=final,
            raw_score=model_score.score,
            was_capped=was_capped,
            is_scored=final is not None,
            weight=weight,
            weighted_points=(
                0.0 if final is None else weight * final / POINTS_FOR_TOP_SCORE
            ),
            confidence=record["confidence"],
            evidence_status=record["evidence_status"],
            justification=model_score.justification,
            key_evidence_urls=model_score.key_evidence_urls,
        )

    total, covered_weight = weighted_total(final_scores)
    return {
        "criteria": {name: value.model_dump() for name, value in scored.items()},
        "total_out_of_100": round(total, 1),
        "weight_covered": covered_weight,
        "criteria_not_scored": [n for n, v in final_scores.items() if v is None],
        "criteria_capped": [n for n, v in scored.items() if v.was_capped],
    }
