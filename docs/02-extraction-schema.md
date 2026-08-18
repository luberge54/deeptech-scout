# Step 2 — extraction schema

Turns the free-text findings produced by step 1 into structured records that step 3 can score
without re-reading prose. This step extracts and classifies evidence. **It does not score, rank,
or judge** — that separation is deliberate and is what makes the scoring step auditable.

---

## 1. The three-state evidence problem

The first ANYbotics collection run, with a 12-search budget, wrote:

> No customer-side press release, tender record, or regulatory filing was found naming ANYbotics.

Re-run with a 20-search budget, it found four: Outokumpu, PETRONAS, Equinor, GE Vernova. The first
run was not lying — it had run out of search budget and reported the result as absence.

That matters because of the rule in [`00-scoping.md`](00-scoping.md) §4b: missing evidence caps a
score at 2 with a LOW confidence flag. If "the pipeline found nothing" is silently treated as
"nothing exists", the rule converts search-budget exhaustion into a low score, and the companies
punished are the quiet ones rather than the weak ones.

So every criterion carries an explicit status, and the three states are not interchangeable:

| `evidence_status` | Meaning | Effect on scoring |
|---|---|---|
| `found` | At least one usable evidence item | Score normally |
| `searched_not_found` | The area was searched and genuinely returned nothing | §4b applies: cap at 2, LOW |
| `not_searched` | Coverage gap — budget exhausted, tool error, area skipped | **Not scored.** Flagged for re-collection. |

`not_searched` is not a bad score. It is an absent measurement, and the report says so rather than
pretending to a number.

---

## 2. Record shape

One JSON file per company: `data/output/<slug>.extracted.json`.

```json
{
  "company": { "slug": "anybotics", "name": "ANYbotics", "country": "Switzerland" },
  "extracted_at": "2026-08-18T14:22:31Z",
  "model": "claude-sonnet-5",
  "source_report": "data/raw/anybotics.json",
  "search_budget_exhausted": true,

  "criteria": {
    "field_traction": {
      "evidence_status": "found",
      "confidence": "HIGH",
      "evidence": [
        {
          "claim": "Outokumpu runs an ANYmal fleet in continuous operation at its Tornio site",
          "source_url": "https://www.outokumpu.com/en/news/...",
          "source_type": "customer_side",
          "evidence_grade": "direct",
          "published_date": "2025-03-11",
          "attributed_to": "Outokumpu"
        }
      ],
      "not_found_notes": null
    }
  },

  "contradictions": [
    {
      "topic": "deployed unit count",
      "description": "close to 200 (Dec 2024) vs more than 200 (Sept 2025) - unchanged over nine months",
      "source_urls": ["https://techcrunch.com/...", "https://tech.eu/..."]
    }
  ]
}
```

The five `criteria` keys are fixed: `field_traction`, `team_execution`, `technology`, `market`,
`timing` — the same five as §3, so step 3 can iterate them against the weights without mapping.

---

## 3. Field reference

### Evidence item

Every factual claim that reaches step 3 is one of these. A claim without a `source_url` is
dropped, not stored — an unsourced claim is exactly what this project exists to avoid.

| Field | Required | Notes |
|---|---|---|
| `claim` | yes | One sentence, factual. No adjectives of quality. |
| `source_url` | yes | The page the claim came from. Dropped if absent. |
| `source_type` | yes | See taxonomy below |
| `evidence_grade` | yes | `direct` or `indirect` |
| `published_date` | no | ISO date when the source states one. Staleness matters: a 2022 deployment claim is weaker than a 2026 one. |
| `attributed_to` | no | Who is making the claim — the customer, the vendor, a journalist |

### Source taxonomy

Mirrors the §4c sourcing table, so the sourcing rule becomes machine-checkable rather than a
paragraph nobody enforces. Ordered strongest to weakest:

| `source_type` | What it is | Default grade |
|---|---|---|
| `customer_side` | The buyer announcing it on their own channel | direct |
| `tender_record` | Public procurement or regulatory filing | direct |
| `trade_press` | Industry press covering an installation | direct |
| `vendor_case_study` | Vendor-hosted, but naming a customer and site | direct |
| `funding_press` | Coverage of a raise, repeating company figures | indirect |
| `company_website` | The company's own unverified claims | indirect |
| `job_posting` | Hiring signals | **indirect, always** |
| `aggregator` | Third-party databases with unclear primary sourcing | indirect |

`job_posting` is pinned to `indirect` by §4c: hiring supports a score, it never establishes one.

---

## 4. Confidence is computed, not generated

The model does **not** choose the confidence level. It is derived in code from the evidence list:

| Result | Condition |
|---|---|
| `HIGH` | At least one `direct` item from a source that is not the company itself (`customer_side`, `tender_record`, `trade_press`) |
| `MEDIUM` | Evidence exists, but only vendor-sourced or only indirect |
| `LOW` | `evidence_status` is `searched_not_found` |
| `null` | `evidence_status` is `not_searched` — no confidence is asserted about an absent measurement |

Two reasons for this design.

**It removes a degree of freedom from the model.** Asking a model to self-report confidence invites
it to be agreeable; a rule applied to a list it cannot see the consequences of does not drift
between runs.

**It makes §4b enforceable rather than aspirational.** The cap at 2 fires from a computed value, so
the rule cannot be quietly skipped on a company with persuasive marketing.

The trade-off, stated rather than hidden: a hand-written rule is cruder than judgment. A single
strong customer-side source and six of them both yield `HIGH`. Volume is visible in the evidence
list, and step 3 can weigh it — but it does not move the confidence flag.

---

## 5. What this step must not do

- **No scoring.** No 1–5 values, no weights, no ranking. Step 3 owns that, on a different model.
- **No inference.** If the findings report does not state it, it does not enter the record. The
  extraction model sees only the step 1 report, never the open web.
- **No merging of contradictory claims.** Disagreeing figures go to `contradictions` intact. The
  reconciliation is a judgment, and judgments belong to step 3 where they can be justified.
