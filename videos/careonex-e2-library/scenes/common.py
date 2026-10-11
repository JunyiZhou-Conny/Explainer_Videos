"""Shared helpers for E2 'Building the library'. The series kit (videos/careonex-series/careonex_kit.py)
holds the boxes, colours and the system map; this file adds the episode's data (verified numbers)."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
SERIES = PROJECT.parent / "careonex-series"
sys.path.insert(0, str(SERIES))

from careonex_kit import *  # noqa: E402,F401,F403
from explainer.script import load_narration  # noqa: E402

NARRATION = load_narration(PROJECT / "script.md")
ASSETS = PROJECT / "assets"
REPORT = json.loads((SERIES / "checks" / "pipeline_report.json").read_text())

import csv  # noqa: E402

# The source list as of data-retrieval@d96a4ad (copied to the series checks folder).
CATALOG = list(csv.DictReader(open(SERIES / "checks" / "ragfile_list.csv", encoding="utf-8")))
PUBLISHERS = [  # (source_id, short label) in the order the scene shows them
    ("nj_doas", "NJ Aging (DoAS)"), ("va", "Veterans Affairs"), ("nj_dmahs", "NJ Medicaid"),
    ("medicare_cms", "Medicare"), ("nj_dds", "NJ Disability"), ("careonex_curated", "team summary"),
]
KINDS = [("html", "web pages"), ("pdf", "PDFs"), ("md", "Markdown")]
