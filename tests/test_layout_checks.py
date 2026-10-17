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


def test_golden_roundtrip_and_drift(tmp_path):
    base = tiny_movie(tmp_path, "base")
    gold = tmp_path / "golden.json"
    stored = golden.update(base, gold, count=4)
    assert gold.is_file() and len(stored["frames"]) == 4

    # The identical render passes (encoder noise stays under the tolerance).
    assert golden.check(base, gold) == []

    # A moved/added element drifts, and the report localizes it.
    changed = tiny_movie(tmp_path, "changed",
                         paint=lambda d: d.rectangle([800, 200, 1100, 500], fill=SWISS_RED))
    problems = golden.check(changed, gold, save_diffs=tmp_path / "diffs")
    assert problems and all("changed around x" in p for p in problems)
    assert list((tmp_path / "diffs").glob("t-*.png"))


def test_golden_duration_drift_is_its_own_finding(tmp_path):
    base = tiny_movie(tmp_path, "base")
    gold = tmp_path / "golden.json"
    golden.update(base, gold, count=2)
    longer = tiny_movie(tmp_path, "longer", seconds=3)
    problems = golden.check(longer, gold)
    assert len(problems) == 1 and "duration" in problems[0]


def test_golden_signature_localizes_cells():
    a = np.full((golden.GRID_H, golden.GRID_W, 3), 200, dtype=np.uint8)
    b = a.copy()
    b[5, 7] = (10, 10, 10)
    cells = golden.changed_cells(a.tobytes(), b.tobytes(), 18.0)
    assert cells == [(5, 7)]
    assert golden.changed_cells(a.tobytes(), (a + 3).astype(np.uint8).tobytes(), 18.0) == []


# ------------------------------------------------------- pre-render band lint

CHECK_SCENE = '''
from manim import DOWN, Scene, Square

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
'''


@pytest.mark.parametrize("cls,expect_band", [("BandDip", True), ("BandClear", False)])
def test_check_flags_caption_band(tmp_path, capsys, cls, expect_band):
    scenes = tmp_path / "project" / "scenes"
    scenes.mkdir(parents=True)
    (scenes / "s01_band.py").write_text(CHECK_SCENE)
    from explainer import check as lint
    rc = lint.main([str(scenes / "s01_band.py"), cls])
    out = capsys.readouterr().out
    assert ("BAND" in out) == expect_band
    assert (rc != 0) == expect_band
    assert "OUT" not in out        # the boxes stay inside the safe area


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
