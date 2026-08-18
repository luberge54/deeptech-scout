"""The blind hand-scores from docs/calibration-worksheet.md, as data.

Transcribed once, here, rather than parsed out of the worksheet's Markdown tables
every time they are needed. A regex over that file silently returned the wrong
column during development, which would have corrupted the one comparison the
project exists to make.

STATED_TOTALS holds the totals as written in the worksheet. tests/test_report.py
recomputes each one from the per-criterion scores using the same arithmetic the
model's totals go through, so a transcription error here fails a test instead of
appearing in the report as a real disagreement.
"""

# Score out of 5 per criterion, exactly as recorded in the worksheet tables.
HAND_SCORES = {
    "anybotics": {
        "field_traction": 5,
        "team_execution": 4,
        "technology": 5,
        "market": 5,
        "timing": 4,
    },
    "verity": {
        "field_traction": 5,
        "team_execution": 5,
        "technology": 4,
        "market": 5,
        "timing": 3,
    },
    "gravis-robotics": {
        "field_traction": 4,
        "team_execution": 4,
        "technology": 5,
        "market": 5,
        "timing": 3,
    },
    "humanoid": {
        "field_traction": 4,
        "team_execution": 4,
        "technology": 3,
        "market": 5,
        "timing": 3,
    },
    "mimic-robotics": {
        "field_traction": 2,
        "team_execution": 4,
        "technology": 4,
        "market": 2,
        "timing": 3,
    },
}

# Confidence recorded alongside each hand-score: H, M or L.
HAND_CONFIDENCE = {
    "anybotics": {
        "field_traction": "M",
        "team_execution": "H",
        "technology": "H",
        "market": "H",
        "timing": "H",
    },
    "verity": {
        "field_traction": "H",
        "team_execution": "H",
        "technology": "M",
        "market": "H",
        "timing": "M",
    },
    "gravis-robotics": {
        "field_traction": "H",
        "team_execution": "H",
        "technology": "H",
        "market": "H",
        "timing": "H",
    },
    "humanoid": {
        "field_traction": "H",
        "team_execution": "H",
        "technology": "M",
        "market": "H",
        "timing": "M",
    },
    "mimic-robotics": {
        "field_traction": "H",
        "team_execution": "H",
        "technology": "M",
        "market": "L",
        "timing": "M",
    },
}

# The totals as written in the worksheet. Checked against HAND_SCORES by a test.
STATED_TOTALS = {
    "anybotics": 93,
    "verity": 92,
    "gravis-robotics": 85,
    "humanoid": 77,
    "mimic-robotics": 60,
}
