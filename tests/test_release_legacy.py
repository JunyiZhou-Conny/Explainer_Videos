"""tools/release_episode.py on a video.yaml episode: the validation it measures and what it refuses.

The legacy route has no render-time sidecar, so the release measures the stitched files itself.
Tiny synthetic cuts stand in for a real stitch.

    PYTHONPATH=. python -m pytest -q tests/test_release_legacy.py
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import release_episode as rel  # noqa: E402

pytestmark = pytest.mark.skipif(not shutil.which("ffmpeg"), reason="needs ffmpeg")

VID = "ac215-l99-demo"
YAML = f"""id: {VID}
title: "AC215 · Lecture 99 — Demo"
scenes:
  - {{file: scenes/s01.py, cls: One}}
  - {{file: scenes/s02.py, cls: Two}}
parts:
  - {{id: part1, scenes: [s01]}}
  - {{id: part2, scenes: [s02]}}
"""
PUBLISH = """publish:
  title_zh: "AC215 第99讲 · 演示"
  description_zh: "跟练视频。"
  tags_zh: [AC215, MLOps]
  tid: 231
"""
SRT = "1\n00:00:00,000 --> 00:00:01,000\n这是一台电脑\nHere's a computer.\n\n" \
      "2\n00:00:01,000 --> 00:00:02,000\n它是我们的\nIt's ours.\n"


def _movie(path: Path, seconds: float) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s=64x36:d={seconds}",
                    "-f", "lavfi", "-i", f"sine=frequency=440:duration={seconds}", "-shortest",
                    "-c:v", "libx264", "-c:a", "aac", str(path)], check=True)


@pytest.fixture
def episode(tmp_path):
    ep, out = tmp_path / VID, tmp_path / VID / "output"
    out.mkdir(parents=True)
    (ep / "video.yaml").write_text(YAML + PUBLISH)
    (ep / "REVIEW.md").write_text("Listening sign-off: waived by Conny for this series.\n")
    for name, sec in [(f"{VID}.mp4", 2), (f"{VID}.zh-en.mp4", 2), (f"{VID}_part1.mp4", 1), (f"{VID}_part2.mp4", 1)]:
        _movie(out / name, sec)
    (out / f"{VID}.zh-en.srt").write_text(SRT)
    (out / "chapters.txt").write_text("00:00 One\n00:01 Two\n")
    (out / "transcript.md").write_text("not a deliverable\n")
    return ep, out


def test_measures_the_stitch_and_publishes_the_burned_copy(episode):
    ep, out = episode
    title_en, meta, validation, deliverables, main_mp4 = rel.legacy_inputs(ep, out)
    assert main_mp4.name == f"{VID}.zh-en.mp4"
    assert meta["title_zh"] == "AC215 第99讲 · 演示" and meta["bilibili_tid"] == 231
    assert meta["tags_zh"] == ["AC215", "MLOps"] and title_en == "AC215 · Lecture 99 — Demo"
    assert validation["route"] == "video.yaml" and validation["caption_cues"] == 2
    assert abs(validation["seconds"][f"{VID}.mp4"] - 2) < 0.2
    assert set(validation["seconds"]) == {f"{VID}.mp4", f"{VID}.zh-en.mp4", f"{VID}_part1.mp4", f"{VID}_part2.mp4"}
    assert validation["loudness_lufs"] is not None
    names = {p.name for p in deliverables}
    assert {"chapters.txt", f"{VID}.zh-en.srt", f"{VID}.validation.json", f"{VID}_part2.mp4"} <= names
    assert "transcript.md" not in names
    assert json.loads((out / f"{VID}.validation.json").read_text()) == validation


def test_refuses_a_missing_part(episode):
    ep, out = episode
    (out / f"{VID}_part2.mp4").unlink()
    with pytest.raises(SystemExit, match="part"):
        rel.legacy_inputs(ep, out)


def test_refuses_a_cue_with_one_language(episode):
    ep, out = episode
    (out / f"{VID}.zh-en.srt").write_text(SRT + "\n3\n00:00:02,000 --> 00:00:03,000\n只有中文\n")
    with pytest.raises(SystemExit, match="without both languages"):
        rel.legacy_inputs(ep, out)


def test_refuses_without_a_chinese_title(episode):
    ep, _ = episode
    (ep / "video.yaml").write_text(YAML)
    with pytest.raises(SystemExit, match="publish.title_zh"):
        rel.legacy_inputs(ep, ep / "output")


@pytest.mark.parametrize("key", ["tid", "tags_zh", "description_zh"])
def test_refuses_a_publish_block_without_partition_tags_or_description(episode, key):
    """No silent defaults: without tid the manifest would fall back to partition 201 (Bugbot, PR #29)."""
    ep, _ = episode
    kept = "\n".join(line for line in PUBLISH.splitlines() if not line.strip().startswith(key + ":"))
    (ep / "video.yaml").write_text(YAML + kept + "\n")
    with pytest.raises(SystemExit, match=f"publish.{key}"):
        rel.legacy_preflight(ep)


def test_refuses_without_the_sign_off_line(episode):
    ep, _ = episode
    (ep / "REVIEW.md").write_text("Technical checks pass.\n")
    with pytest.raises(SystemExit, match="human-review"):
        rel.require_signoff(ep)


def test_preflight_lists_the_scenes_and_sees_no_latex(episode):
    ep, _ = episode
    (ep / "scenes").mkdir()
    (ep / "scenes" / "s01.py").write_text("label('x')\n")
    assert rel.legacy_preflight(ep) == {"scenes": ["s01", "s02"], "latex": False}
    (ep / "scenes" / "common.py").write_text("f = MathTex(r'x^2')\n")
    assert rel.legacy_preflight(ep)["latex"] is True
    (ep / "REVIEW.md").write_text("pending\n")
    with pytest.raises(SystemExit, match="human-review"):
        rel.legacy_preflight(ep)
