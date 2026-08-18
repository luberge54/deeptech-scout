# DeepTech Scout

An opinionated market map of the **Physical AI / applied robotics** sector in Switzerland and
Europe, produced by a pipeline that collects public sources, extracts structured evidence, and
scores companies against explicit, weighted criteria.

The deliverable is not the tool — it is the **judgement layer**: the criteria, their weights, and
the measured gap between a blind hand-score and the model's.

## Why this exists

Portfolio project for a product / strategy role in deep tech. It is designed to demonstrate
three things, in this order of importance:

1. **Product judgment** — the scoring criteria and their weights (see `docs/00-scoping.md`)
2. **Ability to ship** — a working end-to-end pipeline
3. **Awareness of limits** — a blind calibration set that measures where the model is wrong

## The result

Five companies, hand-scored blind before any code was written, then scored by the pipeline.

| Company | Hand | Model | Gap |
|---------|-----:|------:|----:|
| ANYbotics | 93 | 86 | −7 |
| Verity | 92 | 85 | −7 |
| Gravis Robotics | 85 | 70 | −15 |
| Humanoid | 77 | 59 | −18 |
| mimic robotics | 60 | 54 | −6 |

**The ranking is identical on both sides.** Twelve of 25 criterion scores match exactly, 22 within
one notch, and the model is stricter on every company and never more generous. The disagreement is
concentrated in technology, where it asks what *compounds* and the hand-scores credited engineering
depth.

On the largest single disagreement — Humanoid's field traction — the model's reading of the anchor
is better than the hand-score's, and `docs/00-scoping.md` §5 says so.

## Read it

Start with the PDFs in `pdf/`, or the Markdown they are built from:

| Document | What it is |
|----------|------------|
| [`docs/03-market-map.md`](docs/03-market-map.md) | The ranking, the calibration, and one profile per company with every claim linked to its source |
| [`docs/04-thesis.md`](docs/04-thesis.md) | What the ranking means, the position it supports, and six dated events that would falsify it |
| [`docs/00-scoping.md`](docs/00-scoping.md) | The criteria and weights, fixed before scoring; the calibration verdicts; what this cannot see |
| [`docs/calibration-worksheet.md`](docs/calibration-worksheet.md) | The blind hand-scores, per criterion, with justifications |

## Pipeline

| Step | What it does | Model | Output |
|------|--------------|-------|--------|
| 0 | Scoping: sub-sector, company list, weighted criteria | — | `docs/00-scoping.md` |
| 1 | Source collection via server-side web search | `claude-sonnet-5` | `data/raw/*.json` |
| 2 | Structured extraction: evidence with a verified source URL per claim | `claude-sonnet-5` | `data/output/*.extracted.json` |
| 3 | Weighted scoring with a written justification per criterion | `claude-opus-5` | `data/scored/*.scored.json` |
| 4 | Market map: ranking, calibration, one profile per company | **none** | `docs/03-market-map.md` |
| 5 | Thesis and executive summary | `claude-opus-5` | `docs/04-thesis.md` |
| — | Print-ready PDFs of the deliverables | — | `pdf/*.pdf` |

Two models, assigned per step rather than uniformly: capability is bought where judgement happens.
Step 4 uses no model at all — once the content is already decided, assembling it in Python means no
figure can drift from the record it came from. See `docs/00-scoping.md` §4d.

### Rules that live in code, not in prompts

The safeguards that matter are enforced in Python, because a rule stated only in a prompt is a
request:

- an evidence item whose URL is not among the pages the research actually retrieved is **deleted**
- an item graded `direct` that names no customer, unit count, agreement, deployment date or filing
  is recorded as **indirect**
- `HIGH` confidence requires **two** independent direct sources, so the flag means corroborated
- a criterion with no evidence found is **capped at 2**; one that was never searched is **excluded**
  and the remaining weights are rescaled, so a gap in the research is not read as a weakness

Each of these exists because the pipeline failed without it. `docs/00-scoping.md` §6 says how.

## Setup

```powershell
cd C:\Users\lukab\Developper\deeptech-scout
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy env.example .env    # then paste your real API key into .env
```

## Running it

Every step skips work already on disk. Pass a company slug instead of `all` to redo one.

```powershell
.venv\Scripts\python.exe src\check_setup.py          # verify the key with one cheap call
.venv\Scripts\python.exe src\collect_sources.py all  # step 1
.venv\Scripts\python.exe src\extract.py all          # step 2
.venv\Scripts\python.exe src\score.py all            # step 3
.venv\Scripts\python.exe src\report.py               # step 4, free
.venv\Scripts\python.exe src\thesis.py               # step 5
.venv\Scripts\python.exe src\export_pdf.py           # PDFs, free
```

Two modes re-apply changed rules without paying for the same model output twice:

```powershell
.venv\Scripts\python.exe src\extract.py rederive     # recompute confidence and the URL check
.venv\Scripts\python.exe src\thesis.py rebuild       # re-render the thesis document
```

## Tests

61 tests, all offline — none of them calls the API.

```powershell
.venv\Scripts\python.exe tests\test_schema.py
.venv\Scripts\python.exe tests\test_extract.py
.venv\Scripts\python.exe tests\test_scoring.py
.venv\Scripts\python.exe tests\test_report.py
.venv\Scripts\python.exe tests\test_thesis.py
```

They exist because the expensive failures were all visible for free: a truncated reply, a
fabricated source URL, a thesis section returned as the word `placeholder`. Each is now pinned by a
test that costs nothing to run.

## Status

Complete on the five calibration companies, end to end. The 26-company version needs step 1 on the
remaining 21 — the only expensive part left; steps 2 to 5 run on code that is already written and
tested.

Cost of the run behind the current documents: **$9.87**, plus roughly $1.90 of work that was
discarded along the way.
