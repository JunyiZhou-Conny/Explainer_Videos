"""End to end: `python -m explainer.build <short project> -q l` renders two BeatScenes, finishes the
picture, burns the captions in two layouts, composes and masters the music, and writes the sidecars.
(About a minute: it really renders and encodes.)

    PYTHONPATH=. python -m pytest -q tests/test_build_short.py
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

SCENE = '''
from manim import *
from explainer.short import *

class {cls}(BeatScene):
    def construct(self):
        self.fig({n}, "{title}")
        board = VGroup(*[hairline(Line([x, -1.2, 0], [x, 1.2, 0])) for x in (-0.4, 0.4)])
        self.play(Create(board), beats=2)
        self.caption()
        marks = VGroup(*[Circle(0.25).move_to([i - 1.0, 0, 0]) for i in range(3)])
        for m in marks:
            m.sound = "O"
        self.count(marks, every="eighth")
        self.mark("{mark}")
        self.play(FadeIn(glowing(title_glyph("井", 1.5, ACCENTS["cool"].core))), beats=1)
'''


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="needs ffmpeg")
def test_build_a_short(tmp_path):
    p = tmp_path / "tiny-short"
    (p / "scenes").mkdir(parents=True)
    (p / "video.yaml").write_text(
        "id: tiny-short\ntitle: Tiny\nformat: short\ntempo: 100\n"
        "captions: {layouts: [zh-first, en-first]}\n"
        "music: {key: D, mode: lydian}\n"
        "finish: {bloom: true, grain: 4, vignette: true}\n"
        "scenes:\n  - {file: scenes/s01_a.py, cls: A, title: One}\n  - {file: scenes/s02_b.py, cls: B, title: Two}\n")
    (p / "captions.yaml").write_text(
        "s01_a:\n  - {zh: 井字棋有多少种不同的对局？, en: 'How many different games of tic-tac-toe are there?'}\n"
        "s02_b:\n  - {zh: 终局一样，顺序不同。, en: 'Same final board, different order.'}\n", encoding="utf-8")
    (p / "scenes" / "s01_a.py").write_text(SCENE.format(cls="A", n=1, title="How many", mark="title"))
    (p / "scenes" / "s02_b.py").write_text(SCENE.format(cls="B", n=2, title="Orders", mark="hit"))
    env = dict(os.environ, PYTHONPATH=str(REPO))
    r = subprocess.run([sys.executable, "-m", "explainer.build", str(p), "-q", "l", "--jobs", "2"],
                       env=env, capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-3000:]
    out = p / "output"
    for name in ("tiny-short_480p15.mp4", "tiny-short_480p15.en-first.mp4", "tiny-short_480p15.nomusic.mp4",
                 "tiny-short_480p15.music.wav", "tiny-short_480p15.zh.srt", "tiny-short_480p15.en.srt",
                 "tiny-short_480p15.zh-en.srt", "tiny-short_480p15.zh-first.ass", "tiny-short_480p15.en-first.ass",
                 "chapters.txt", "transcript.md"):
        assert (out / name).exists(), name
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,nb_frames", "-of", "json",
                            str(out / "tiny-short_480p15.mp4")], capture_output=True, text=True, check=True)
    streams = {s["codec_type"]: s for s in json.loads(probe.stdout)["streams"]}
    assert set(streams) == {"video", "audio"}
    assert int(streams["video"]["nb_frames"]) % 36 == 0            # whole bars at 15 fps
    zh = (out / "tiny-short_480p15.zh.srt").read_text(encoding="utf-8")
    assert "井字棋有多少种不同的对局？" in zh and "终局一样" in zh and "How many" not in zh
    en = (out / "tiny-short_480p15.en.srt").read_text(encoding="utf-8")
    assert "How many different games" in en and "井" not in en
    qa = json.loads((p / "build" / "stitch_l" / "tiny-short_480p15.qa.json").read_text())
    assert qa["cuts_on_bars"] == "1/1" and qa["captions"] == 2
    assert abs(qa["lufs"] + 14) < 1.0 and qa["true_peak_dbtp"] <= -0.95
    assert (out / "chapters.txt").read_text().startswith("00:00 One\n")
