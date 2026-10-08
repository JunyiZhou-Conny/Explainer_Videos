"""A narrated (long-format) video: without --music the build is what it always was; with --music the
score is mixed under the narration, and the narration-only master is kept as <id>.nomusic.mp4.

    PYTHONPATH=. python -m pytest -q tests/test_build_long_music.py
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
from explainer.scene import VoiceScene

class Hook(VoiceScene):
    def construct(self):
        dots = VGroup(*[Circle(0.3).shift(RIGHT * (i - 1)) for i in range(3)])
        with self.voiceover("Three circles appear, one after another.") as vo:
            self.play(LaggedStart(*[Create(d) for d in dots], lag_ratio=0.5), run_time=vo.duration)
        self.mark("hit")
        self.play(Indicate(dots), run_time=0.8)
        with self.voiceover("Then they fade away.") as vo:
            self.play(FadeOut(dots), run_time=vo.duration)
'''


def audio_md5(path: Path) -> str:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a", "-f", "md5", "-"],
                       capture_output=True, text=True, check=True)
    return r.stdout.strip()


def video_md5(path: Path) -> str:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v", "-c", "copy", "-f", "md5", "-"],
                       capture_output=True, text=True, check=True)
    return r.stdout.strip()


@pytest.mark.skipif(shutil.which("ffmpeg") is None or shutil.which("espeak-ng") is None,
                    reason="needs ffmpeg and espeak-ng")
def test_long_video_music_is_opt_in(tmp_path):
    p = tmp_path / "tiny-long"
    (p / "scenes").mkdir(parents=True)
    (p / "video.yaml").write_text("id: tiny-long\ntitle: Tiny\nvoice: {backend: espeak, voice: en-us}\n"
                                  "scenes:\n  - {file: scenes/s01_hook.py, cls: Hook, title: Hook}\n")
    (p / "scenes" / "s01_hook.py").write_text(SCENE)
    env = dict(os.environ, PYTHONPATH=str(REPO))
    env.pop("EXPLAINER_TTS", None)
    run = lambda *a: subprocess.run([sys.executable, "-m", "explainer.build", str(p), "-q", "l", *a], env=env,
                                    capture_output=True, text=True, timeout=900)
    r = run()
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-3000:]
    out = p / "output"
    plain = out / "tiny-long_480p15.mp4"
    assert plain.exists() and (out / "tiny-long_480p15.srt").exists()
    assert not (out / "tiny-long_480p15.nomusic.mp4").exists()            # nothing new without --music
    before_a, before_v = audio_md5(plain), video_md5(plain)
    ev = p / "build" / "media_l" / "s01_hook" / "videos" / "s01_hook" / "480p15" / "Hook.events.json"
    log = json.loads(ev.read_text())
    assert [e["type"] for e in log["events"]][:2] == ["voice", "play"]

    r = run("--no-render", "--music")
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-3000:]
    nomusic = out / "tiny-long_480p15.nomusic.mp4"
    assert nomusic.exists() and (out / "tiny-long_480p15.music.wav").exists()
    assert audio_md5(nomusic) == before_a                                   # the narration-only master
    assert video_md5(plain) == before_v                                     # the picture is untouched
    assert audio_md5(plain) != before_a                                     # now with the score under it
    assert "music" in r.stdout.lower() and "under speech" in r.stdout
