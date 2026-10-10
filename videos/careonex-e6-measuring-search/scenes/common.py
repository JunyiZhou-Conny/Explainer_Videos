"""Shared helpers for E6 'Measuring search'. The series kit (videos/careonex-series/careonex_kit.py)
holds the boxes, colours and the system map; this file adds the episode's data (measured numbers)."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
SERIES = PROJECT.parent / "careonex-series"
sys.path.insert(0, str(SERIES))

from careonex_kit import *  # noqa: E402,F401,F403
from explainer import style as _S  # noqa: E402
from explainer.script import load_narration  # noqa: E402

NARRATION = load_narration(PROJECT / "script.md")
CHECKS = SERIES / "checks" / "marco"
METRICS = json.loads((CHECKS / "marco_metrics.json").read_text())
REPLAY = json.loads((CHECKS / "planner_replay.json").read_text())

# The three chunkers keep one colour each for the whole episode.
CHUNKERS = [("legacy", "A", "legacy", _S.GREY), ("section", "B", "section-safe", _S.BLUE),
            ("hierarchical", "C", "hierarchical", _S.TEAL)]
MARCO_C = PEOPLE["Marco"]
