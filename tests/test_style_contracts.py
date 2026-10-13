"""The style catalog cannot claim more than the repository delivers.

A 'ready' status in catalog/styles.json requires the four-part contract: tokens, a
components module, committed reference frames, and a cited example episode. The human
table in docs/STYLES.md is generated from the JSON and must be in sync.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PRESETS = ROOT / "skill-library/conny-explainer-video/presets"
READY = {"existing-complete-episodes", "complete-example-technical-and-sampled-visual-review"}


def styles():
    return json.loads((ROOT / "catalog/styles.json").read_text())["styles"]


def test_ready_styles_ship_their_contract():
    from explainer.styles import MODULES, tokens
    for s in styles():
        if s["status"] not in READY:
            continue
        sid = s["id"]
        t = tokens(sid)  # raises when the tokens file is missing
        assert {"palette", "canvas"} <= set(t), f"{sid}: tokens lack palette/canvas"
        assert t["palette"].get("background", "").startswith("#"), sid
        assert sid in MODULES, f"{sid}: no components module registered in explainer.styles"
        frames = list((PRESETS / f"{sid}.reference").glob("*.png"))
        assert len(frames) >= 3, f"{sid}: fewer than 3 committed reference frames"
        assert s.get("example"), f"{sid}: ready without a cited example episode"
        assert (ROOT / s["example"]).is_dir(), f"{sid}: example episode missing"


def test_unready_styles_claim_nothing():
    for s in styles():
        if s["status"] in READY:
            continue
        assert s["status"] in {"design-specification-sample-pending", "blocked-on-renderer"}, \
            f"{s['id']}: unknown status {s['status']}"
        if s["status"] == "blocked-on-renderer":
            assert s.get("blocked_reason"), f"{s['id']}: blocked without a reason"


def test_tokens_parse_and_check_thresholds_sane():
    for path in PRESETS.glob("*.tokens.json"):
        t = json.loads(path.read_text())
        checks = t.get("checks", {})
        assert 0 < checks.get("min_background_share", 0.35) <= 1
        assert 0 < checks.get("background_tolerance", 30) < 128


def test_styles_doc_in_sync():
    result = subprocess.run([sys.executable, str(ROOT / "tools/gen_style_status.py"), "--check"],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr or result.stdout


def test_swiss_components_follow_tokens():
    pytest.importorskip("manim")
    from explainer.styles import swiss, tokens
    t = tokens("swiss")
    assert swiss.PAPER == t["palette"]["background"]
    assert swiss.RED == t["palette"]["accent"]
    group = swiss.card("Title", "sub", 0, 0)
    assert len(group) == 3
    folder = swiss.folder("docs/", 0, 0)
    assert len(folder) == 3
