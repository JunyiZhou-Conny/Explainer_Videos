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
        self.wait_beats(1)                                # a still beat: the next play starts from stillness
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
    assert qa["cuts_on_bars"] == "1/1" and qa["captions"] == 2 and qa["scenes_whole_bars"] == "2/2"
    assert qa["cuts_rayleigh"]["R"] == 1.0 and qa["plays_on_beat"] == 1.0
    assert abs(qa["lufs"] + 14) < 1.0 and qa["true_peak_dbtp"] <= -0.95
    assert qa["clicks"] == 0
    sync = qa["sync"]                       # measured on the files: the shipped sound against music.wav,
    assert abs(sync["audio_lag_ms"]) <= 1.0 and sync["frames_match"]       # the joined picture against the log
    assert sync["picture_delay_frames"]["n"] >= 2 and sync["picture_delay_frames"]["early"] == 0
    assert 1 <= sync["picture_delay_frames"]["median"] <= 3 and sync["picture_delay_frames"]["max"] <= 4
    assert (out / "chapters.txt").read_text().startswith("00:00 One\n")


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="needs ffmpeg")
def test_measure_sync_sees_offsets(tmp_path):
    """The sync numbers can fail: a picture change later than its logged play, and a sound track
    shifted against music.wav, are both measured on the files."""
    import numpy as np
    import soundfile as sf
    from explainer import finishing as fin
    pic = tmp_path / "pic.mp4"                    # black, then a white square from frame 30 (1.0 s at 30 fps)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=320x180:r=30:d=3",
                    "-vf", "drawbox=x=100:y=50:w=80:h=80:color=white:t=fill:enable='gte(n,30)'",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(pic)], check=True)
    sr = 48000
    rng = np.random.default_rng(0)
    music = np.zeros((3 * sr, 2))
    for t in (0.4, 1.1, 1.9, 2.5):                # four decaying bursts
        i = int(t * sr)
        music[i:i + 4800] += rng.normal(0, 0.2, (4800, 2)) * np.exp(-np.arange(4800) / 900)[:, None]
    wav = tmp_path / "music.wav"
    sf.write(wav, music.astype(np.float32), sr)
    for shift in (0.0, 0.1):
        mp4 = tmp_path / f"m{shift}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(pic), "-itsoffset", str(shift), "-i", str(wav),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", str(mp4)],
                       check=True)
        on_time = fin.measure_sync(mp4, wav, pic, [29 / 30])            # logged one frame before the change
        late = fin.measure_sync(mp4, wav, pic, [26 / 30])               # the picture 3 frames behind the log
        early = fin.measure_sync(mp4, wav, pic, [31 / 30])              # ... or 2 frames ahead of it
        assert on_time["picture_delay_frames"]["median"] == 1 and on_time["picture_delay_frames"]["early"] == 0
        assert late["picture_delay_frames"]["median"] == 4
        assert early["picture_delay_frames"]["median"] == -1 and early["picture_delay_frames"]["early"] == 1
        assert on_time["frames_match"]
        assert on_time["audio_lag_ms"] == pytest.approx(shift * 1000, abs=1.0)
