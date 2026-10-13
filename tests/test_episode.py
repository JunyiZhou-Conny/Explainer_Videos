"""The episode engine's pure logic: settings resolution, gates, frame budgets, captions, music.

Run with pytest (python -m pytest -q tests); unittest discovery does not collect these.
"""
import json
import math
from pathlib import Path

import pytest

from explainer import episode


def make_project(tmp_path: Path, script: dict, spec: dict | None = None,
                 defaults: dict | None = None) -> tuple[Path, Path]:
    project = tmp_path / "demo-episode"
    project.mkdir(parents=True)
    (project / "script.json").write_text(json.dumps(script))
    if spec is not None:
        (project / "episode.json").write_text(json.dumps(spec))
    d = {"preset": "swiss", "duration_seconds": 300,
         "video": {"width": 1920, "height": 1080, "fps": 30},
         "narration": {"language": "en", "voice": "af_heart", "speed": 0.95},
         "subtitles": {"languages": ["zh-CN", "en"], "burn_in": True},
         "music": {"enabled": True}}
    d.update(defaults or {})
    defaults_path = tmp_path / "defaults.json"
    defaults_path.write_text(json.dumps(d))
    return project, defaults_path


def test_duration_stated_once(tmp_path):
    """episode.json owns the duration; a disagreeing script.json is an error, not a silent winner."""
    project, defaults = make_project(tmp_path, {"target_duration_seconds": 240},
                                     spec={"duration_seconds": 300})
    with pytest.raises(SystemExit, match="stated in both"):
        episode.resolve_settings(project, defaults)
    # agreement is fine
    project2, defaults2 = make_project(tmp_path / "b", {"target_duration_seconds": 300},
                                       spec={"duration_seconds": 300})
    settings, _ = episode.resolve_settings(project2, defaults2)
    assert settings["duration_seconds"] == 300
    # without episode.json the script value applies
    project3, defaults3 = make_project(tmp_path / "c", {"target_duration_seconds": 120})
    settings, _ = episode.resolve_settings(project3, defaults3)
    assert settings["duration_seconds"] == 120


def test_episode_json_merges_music_block(tmp_path):
    project, defaults = make_project(tmp_path, {}, spec={"music": {"enabled": False}})
    settings, _ = episode.resolve_settings(project, defaults)
    assert episode.music_settings(settings, no_music=False) is None
    assert episode.music_settings({"music": {"enabled": True, "mood": "calm"}},
                                  no_music=False) == {"enabled": True, "mood": "calm"}
    assert episode.music_settings({"music": {"enabled": True}}, no_music=True) is None
    # music on by default when the settings carry no block at all
    assert episode.music_settings({}, no_music=False) == {"enabled": True}


def test_narration_key_gate():
    assert episode.narration_key({"narration": {"language": "en"}}, {}) == "en"
    assert episode.narration_key({"narration": {"language": "zh-CN"}}, {}) == "zh"
    assert episode.narration_key({"narration": {"language": "en"}},
                                 {"narration_language": "zh"}) == "zh"
    with pytest.raises(SystemExit, match="no verified route"):
        episode.narration_key({"narration": {"language": "fr"}}, {})


def test_video_gates():
    ok = {"subtitles": {"languages": ["zh-CN", "en"], "burn_in": True},
          "video": {"width": 1920, "height": 1080, "fps": 30}}
    assert episode.check_gates(ok) == (1920, 1080, 30)
    with pytest.raises(SystemExit, match="burned Chinese-above-English"):
        episode.check_gates({"subtitles": {"languages": ["en"], "burn_in": True},
                             "video": {"width": 1920, "height": 1080, "fps": 30}})
    with pytest.raises(SystemExit, match="positive"):
        episode.check_gates({"subtitles": {"languages": ["zh-CN", "en"], "burn_in": True},
                             "video": {"width": 0, "height": 1080, "fps": 30}})
    # a non-validated profile passes with a warning, it is not refused
    assert episode.check_gates({"subtitles": {"languages": ["zh-CN", "en"], "burn_in": True},
                                "video": {"width": 1280, "height": 720, "fps": 24}}) == (1280, 720, 24)


def test_frame_budget_sums_exactly():
    for target, fps, minima in [(300.0, 30, [21.4, 19.6, 24.5]), (60.0, 60, [10.0, 10.0]),
                                (22.3, 30, [22.3])]:
        prepared = [{"minimum": m} for m in minima]
        episode.frame_budget(prepared, target, fps)
        assert sum(s["frames"] for s in prepared) == round(target * fps)
        for s in prepared:
            assert s["duration"] == s["frames"] / fps
            assert s["frames"] >= math.floor(s["minimum"] * fps)  # audio never clipped


def test_build_pairs_en_counts_and_mismatch():
    clip = {"text": "One sentence. And another one.", "start": 0.0, "end": 4.0,
            "marks": [[0, 0.0], [14, 2.0]]}
    lines = [{"en": "One sentence. And another one.", "zh": "第一句。还有第二句。"}]
    pairs = episode.build_pairs([clip], lines, offset=10.0, key="en")
    assert len(pairs) == 2
    (a1, b1, zh1, en1, _), (a2, b2, zh2, en2, _) = pairs
    assert (a1, en1, zh1) == (10.0, "One sentence.", "第一句。")
    assert a2 == 12.0 and b2 == 14.0 and zh2 == "还有第二句。"
    with pytest.raises(RuntimeError, match="cue mismatch"):
        episode.build_pairs([clip, clip], lines, 0.0, "en")


def test_build_pairs_zh_timing_from_zh_audio():
    clip = {"text": "第一句。还有第二句。", "start": 0.0, "end": 6.0,
            "marks": [[0, 0.0], [4, 3.0]]}
    lines = [{"en": "One sentence. And another one.", "zh": "第一句。还有第二句。"}]
    pairs = episode.build_pairs([clip], lines, offset=0.0, key="zh")
    assert len(pairs) == 2
    assert pairs[0][0] == 0.0 and pairs[1][0] == 3.0 and pairs[1][1] == 6.0
    assert pairs[0][2] == "第一句。" and pairs[0][3] == "One sentence."
    # sentence-count mismatch folds into one cue instead of guessing an alignment
    lines2 = [{"en": "Only one.", "zh": "第一句。还有第二句。"}]
    pairs2 = episode.build_pairs([clip], lines2, 0.0, "zh")
    assert len(pairs2) == 1 and pairs2[0][3] == "Only one."


def test_validate_output_thresholds(tmp_path, monkeypatch):
    plan = {"script_sha256": "x"}
    script = tmp_path / "script.json"
    script.write_text("{}")
    good_probe = {"format": {"duration": "300.02"},
                  "streams": [{"codec_type": "video"}, {"codec_type": "audio"}]}
    monkeypatch.setattr(episode, "probe", lambda p: good_probe)

    class FakeRun:
        stderr = "mean_volume: -19.6 dB"
    monkeypatch.setattr(episode.subprocess, "run", lambda *a, **k: FakeRun())
    with pytest.raises(RuntimeError, match="Script changed"):
        episode.validate_output(Path("f.mp4"), 300.0, 70, script, plan, [], None)
    import hashlib
    plan["script_sha256"] = hashlib.sha256(b"{}").hexdigest()
    v = episode.validate_output(Path("f.mp4"), 300.0, 70, script, plan, [], None)
    assert v["audio_mean_db"] == -19.6 and v["caption_cues"] == 70
    with pytest.raises(RuntimeError, match="duration"):
        episode.validate_output(Path("f.mp4"), 200.0, 70, script, plan, [], None)
    FakeRun.stderr = "mean_volume: -77.0 dB"
    with pytest.raises(RuntimeError, match="implausibly quiet"):
        episode.validate_output(Path("f.mp4"), 300.0, 70, script, plan, [], None)
    FakeRun.stderr = "mean_volume: -19.6 dB"
    with pytest.raises(RuntimeError, match="LUFS"):
        episode.validate_output(Path("f.mp4"), 300.0, 70, script, plan, [], {"mix_lufs": -3.0})
