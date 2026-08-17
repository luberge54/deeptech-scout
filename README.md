# DeepTech Scout

An opinionated market map of the **Physical AI / applied robotics** sector, produced by an
AI pipeline that collects public sources, extracts structured data, and scores companies
against explicit, weighted criteria.

The deliverable is not the tool — it is the **investment thesis** the tool supports.

## Why this exists

Portfolio project for a product / strategy role in deep tech. It is designed to demonstrate
three things, in this order of importance:

1. **Product judgment** — the scoring criteria and their weights (see `docs/00-scoping.md`)
2. **Ability to ship** — a working end-to-end pipeline
3. **Awareness of limits** — a manual calibration set that measures where the model is wrong

## Pipeline

| Step | What it does | Output |
|------|--------------|--------|
| 0 | Scoping: sub-sector, company list, weighted criteria | `docs/00-scoping.md` |
| 1 | Source collection via Claude web search | `data/raw/` |
| 2 | Structured extraction (raw text -> JSON, with source URL + confidence per field) | `data/raw/*.json` |
| 3 | Weighted scoring with written justification per criterion | `data/output/scores.json` |
| 4 | Report: ranked table + one card per company | `data/output/report.md` |
| 5 | Executive summary and sector thesis | `docs/05-thesis.md` |

## Setup

```powershell
cd C:\Users\lukab\Developper\deeptech-scout
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env    # then paste your real API key into .env
```

## Status

Step 0 in progress.
