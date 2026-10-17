"""The two post-mortem layout guards: band tiles in style_check, golden-frame regression.

Both exist because of git-branch-pointer's review findings: a tag entered the reserved
caption band yet passed the 3% global tolerance, and layout drift was only ever caught by
re-watching frames. These tests pin the failure modes they must catch.
"""
import json
import subprocess
from pathlib import Path

import numpy as np
import pytest
from PIL import Image, ImageDraw

from explainer import golden, style_check

ROOT = Path(__file__).resolve().parents[1]

SWISS_BG = "#F3F0E7"
SWISS_INK = "#171717"   # equals the swiss band colour — the blind spot the tiles close
SWISS_RED = "#DA2D24"


def frame(tmp_path, name="f.png", paint=None):
    img = Image.new("RGB", (1920, 1080), SWISS_BG)
    if paint:
        paint(ImageDraw.Draw(img))
    path = tmp_path / name
    img.save(path)
    return path


def test_clean_band_passes(tmp_path):
    assert style_check.check_frames([frame(tmp_path)], "swiss") == []


def test_small_tag_in_band_is_caught_by_tiles(tmp_path):
    # 60x60 accent square at y=990: 3600px of a 326400px band (1.1%) — invisible to the
    # 97% global check, which is exactly how the git-branch-pointer tag reached review.
    f = frame(tmp_path, paint=lambda d: d.rectangle([900, 990, 960, 1050], fill=SWISS_RED))
    problems = style_check.check_frames([f], "swiss")
    assert len(problems) == 1
    assert "intruding on the caption band" in problems[0]
    assert "x 840-960px" in problems[0]


def test_ink_coloured_tag_is_caught_despite_band_colour(tmp_path):
    # swiss band_colour == ink, so the global check cannot see this at any size.
    f = frame(tmp_path, paint=lambda d: d.rectangle([300, 980, 380, 1060], fill=SWISS_INK))
    problems = style_check.check_frames([f], "swiss")
    assert any("intruding on the caption band" in p for p in problems)


def test_scene_painted_band_is_excused(tmp_path):
    # A band uniformly painted in the band colour is a style choice, not an intrusion.
    f = frame(tmp_path, paint=lambda d: d.rectangle([0, 910, 1920, 1080], fill=SWISS_INK))
    assert style_check.check_frames([f], "swiss") == []


def test_content_above_the_band_is_fine(tmp_path):
    f = frame(tmp_path, paint=lambda d: d.rectangle([200, 300, 1700, 900], fill=SWISS_INK))
    problems = style_check.check_frames([f], "swiss")
    assert not any("caption band" in p for p in problems)


# ---------------------------------------------------------------- golden frames

def tiny_movie(tmp_path, name, paint=None, seconds=2):
    png = frame(tmp_path, name + ".png", paint)
    movie = tmp_path / (name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(png),
                    "-t", str(seconds), "-r", "12", "-pix_fmt", "yuv420p",
                    "-vf", "scale=640:360", str(movie)], check=True)
    return movie


SCENES = [{"id": "s01", "start": 0.0, "duration": 2.0}]


def test_golden_roundtrip_and_drift(tmp_path):
    base = tiny_movie(tmp_path, "base")
    gold = tmp_path / "golden.json"
    stored = golden.update(base, gold, SCENES)
    assert gold.is_file() and stored["scenes"][0]["samples"]

    # The identical render passes (encoder noise stays under the tolerance).
    assert golden.check(base, gold, SCENES) == []

    # A moved/added element drifts, and the report localizes it per scene.
    changed = tiny_movie(tmp_path, "changed",
                         paint=lambda d: d.rectangle([800, 200, 1100, 500], fill=SWISS_RED))
    problems = golden.check(changed, gold, SCENES, save_diffs=tmp_path / "diffs")
    assert problems and all(p.startswith("s01 ") and "changed around x" in p for p in problems)
    assert list((tmp_path / "diffs").glob("s01-*.png"))

    # A re-run that passes clears stale diff frames instead of leaving them around.
    assert golden.check(base, gold, SCENES, save_diffs=tmp_path / "diffs") == []
    assert not (tmp_path / "diffs").exists()


def test_golden_scene_timing_change_is_its_own_finding(tmp_path):
    # frame_budget moves scene durations whenever narration changes; that must read as
    # "timing changed", never as layout drift at absolute times that no longer line up.
    base = tiny_movie(tmp_path, "base")
    gold = tmp_path / "golden.json"
    golden.update(base, gold, SCENES)
    longer = tiny_movie(tmp_path, "longer", seconds=3)
    problems = golden.check(longer, gold, [{"id": "s01", "start": 0.0, "duration": 3.0}])
    assert len(problems) == 1 and "narration timing changed in s01" in problems[0]
    missing = golden.check(base, gold, [{"id": "s02", "start": 0.0, "duration": 2.0}])
    assert len(missing) == 1 and "not in the current cut" in missing[0]


def test_golden_rejects_degenerate_files(tmp_path):
    base = tiny_movie(tmp_path, "base")
    old_schema = tmp_path / "v1.json"
    old_schema.write_text(json.dumps({"schema": 1, "grid": [32, 18], "frames": []}))
    problems = golden.check(base, old_schema, SCENES)
    assert len(problems) == 1 and "unsupported schema" in problems[0]
    empty = tmp_path / "empty.json"
    empty.write_text(json.dumps({"schema": 2, "grid": [32, 18], "scenes": []}))
    problems = golden.check(base, empty, SCENES)
    assert len(problems) == 1 and "no scenes stored" in problems[0]
    corrupt = tmp_path / "corrupt.json"
    corrupt.write_text(json.dumps({"schema": 2, "grid": [32, 18], "scenes": [
        {"id": "s01", "duration": 2.0, "samples": [{"frac": 0.5, "sig": "AAAA"}]}]}))
    problems = golden.check(base, corrupt, SCENES)
    assert len(problems) == 1 and "corrupted signature" in problems[0]


def test_golden_scenes_from_plan(tmp_path):
    movie = tmp_path / "x.clean.mp4"
    movie.touch()
    (tmp_path / "plan.json").write_text(json.dumps(
        {"scenes": [{"id": "s01", "duration": 2.0}, {"id": "s02", "duration": 1.5}]}))
    scenes = golden.scenes_from_plan(movie)
    assert scenes == [{"id": "s01", "start": 0.0, "duration": 2.0},
                      {"id": "s02", "start": 2.0, "duration": 1.5}]
    with pytest.raises(SystemExit):
        golden.scenes_from_plan(tmp_path / "elsewhere" / "y.mp4")


def test_golden_signature_localizes_cells():
    a = np.full((golden.GRID_H, golden.GRID_W, 3), 200, dtype=np.uint8)
    b = a.copy()
    b[5, 7] = (10, 10, 10)
    cells = golden.changed_cells(a.tobytes(), b.tobytes(), 18.0)
    assert cells == [(5, 7)]
    assert golden.changed_cells(a.tobytes(), (a + 3).astype(np.uint8).tobytes(), 18.0) == []


# ------------------------------------------------------- pre-render band lint

CHECK_SCENE = '''
import types
from manim import DOWN, Rectangle, Scene, Square, config

class BandDip(Scene):
    def construct(self):
        box = Square(side_length=1, fill_opacity=1)
        box.move_to(2.6 * DOWN)      # bottom edge y=-3.1: inside the safe area, inside the band
        self.play(box.animate.set_fill(opacity=0.9), run_time=0.2)
        self.remove(box)
        self.wait(0.1)

class BandClear(Scene):
    def construct(self):
        box = Square(side_length=1, fill_opacity=1)   # centred: nowhere near the band
        self.play(box.animate.set_fill(opacity=0.9), run_time=0.2)
        self.remove(box)
        self.wait(0.1)

class Backdrop(Scene):
    def construct(self):
        full = Rectangle(width=config.frame_width, height=config.frame_height,
                         fill_opacity=1, stroke_width=0)   # full-bleed: exempt from BAND
        self.play(full.animate.set_fill(opacity=0.9), run_time=0.2)
        self.remove(full)
        self.wait(0.1)

class ShortLike(Scene):
    def construct(self):
        self.grid = types.SimpleNamespace(bar=0.3)   # a BeatScene marker: band check skipped
        box = Square(side_length=1, fill_opacity=1)
        box.move_to(2.6 * DOWN)
        self.play(box.animate.set_fill(opacity=0.9), run_time=0.2)
        self.remove(box)
        self.wait(0.1)
'''


def run_lint(tmp_path, monkeypatch, cls, extra_args=(), env=None):
    monkeypatch.delenv("EXPLAINER_CAPTION_RESERVE", raising=False)
    for k, v in (env or {}).items():
        monkeypatch.setenv(k, v)
    scenes = tmp_path / "project" / "scenes"
    scenes.mkdir(parents=True, exist_ok=True)
    (scenes / "s01_band.py").write_text(CHECK_SCENE)
    from explainer import check as lint
    rc = lint.main([str(scenes / "s01_band.py"), cls, *extra_args])
    return rc


@pytest.mark.parametrize("cls,expect_band", [("BandDip", True), ("BandClear", False)])
def test_check_flags_caption_band(tmp_path, capsys, monkeypatch, cls, expect_band):
    rc = run_lint(tmp_path, monkeypatch, cls)
    out = capsys.readouterr().out
    assert ("BAND" in out) == expect_band
    assert (rc != 0) == expect_band
    assert "OUT" not in out        # the boxes stay inside the safe area


def test_check_band_edge_cases(tmp_path, capsys, monkeypatch):
    # A full-bleed backdrop is exempt from BAND (it still trips OUT, as it always has).
    rc = run_lint(tmp_path, monkeypatch, "Backdrop")
    out = capsys.readouterr().out
    assert "BAND" not in out and "OUT" in out and rc != 0

    # A BeatScene-style short (scene.grid set) skips the band check entirely.
    run_lint(tmp_path, monkeypatch, "ShortLike")
    out = capsys.readouterr().out
    assert "BAND" not in out

    # EXPLAINER_CAPTION_RESERVE=0 disables the check for band-painting preset routes.
    rc = run_lint(tmp_path, monkeypatch, "BandDip", env={"EXPLAINER_CAPTION_RESERVE": "0"})
    out = capsys.readouterr().out
    assert "BAND" not in out and rc == 0


def test_check_skips_band_for_legacy_scale_mode(tmp_path, capsys):
    # video.yaml projects burn with mode "scale": the picture is shrunk above the band,
    # so a scene using the bottom of the frame is correct there, not an intrusion.
    project = tmp_path / "legacy"
    scenes = project / "scenes"
    scenes.mkdir(parents=True)
    project.joinpath("video.yaml").write_text("title: t\nvoice: {backend: silent}\n")
    (scenes / "s01_band.py").write_text(CHECK_SCENE)
    from explainer import check as lint
    rc = lint.main([str(scenes / "s01_band.py"), "BandDip", "--tts", "silent"])
    out = capsys.readouterr().out
    assert "BAND" not in out and rc == 0
