"""Executable style contracts: machine-readable tokens plus reusable scene components.

A preset is 'ready' only when it ships (1) presets/<id>.tokens.json, (2) a components
module here, (3) committed reference frames, and (4) a reviewed sample — see
docs/STYLE-LIFECYCLE.md. tokens() is the single source the Markdown token tables and the
pixel checks (explainer.style_check) read from.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRESETS = ROOT / "skill-library/conny-explainer-video/presets"

MODULES = {"swiss": "explainer.styles.swiss", "3b1b": "explainer.style"}


def tokens_path(preset: str) -> Path:
    return PRESETS / f"{preset}.tokens.json"


def tokens(preset: str) -> dict:
    path = tokens_path(preset)
    if not path.is_file():
        raise FileNotFoundError(f"{preset} has no tokens file ({path}); it is not a ready style")
    return json.loads(path.read_text())
