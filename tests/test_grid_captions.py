"""The beat grid, captions (captions.yaml, layouts, .ass / .srt) and the finishing-pass settings of
the short format: pure functions, no rendering.

    PYTHONPATH=. python -m pytest -q tests/test_grid_captions.py
"""

import json
import math

import numpy as np
import pytest

from explainer import captions as cap
from explainer import finishing as fin
from explainer.grid import Grid, frames, hold_time, play_time


# ---------------------------------------------------------------- grid

def test_default_grid_is_100_bpm():
    g = Grid()
    assert g.beat == pytest.approx(0.6) and g.bar == pytest.approx(2.4)
    assert frames(g.beat, 60) == 36 and frames(g.bar, 60) == 144 and frames(g.bar, 15) == 36


def test_positions():
    g = Grid(100)
    assert g.time("0") == 0.0
    assert g.time("2:1") == pytest.approx(5.4)
    assert g.time("2:1.5") == pytest.approx(5.7)
    assert g.time("4.8s") == pytest.approx(4.8)
    assert g.time(3) == pytest.approx(7.2)
    assert g.time((1, 2)) == pytest.approx(3.6)
    assert g.label(5.4) == "2:1"
    with pytest.raises(ValueError):
        g.time("bar two")


def test_snap_and_units():
    g = Grid(100)
    assert g.snap(2.5, "bar") == pytest.approx(4.8)
    assert g.snap(2.4, "bar") == pytest.approx(2.4)          # already on a bar line
    assert g.snap(2.5, "bar", "down") == pytest.approx(2.4)
    assert g.snap(0.31, "beat", "nearest") == pytest.approx(0.6)
    assert g.unit("eighth") == pytest.approx(0.3) and g.unit("quarter") == pytest.approx(0.15)
    assert g.on_grid(9.6, "bar") and not g.on_grid(9.0, "bar")
    assert Grid(120).bar == pytest.approx(2.0)


@pytest.mark.parametrize("fps", [15, 30, 60])
def test_run_times_give_exact_frames(fps):
    """Manim draws np.arange(0, run_time, 1/fps) frames for a play and int(d * fps) for a frozen wait:
    the grid's run times hit the frame count exactly, for any length."""
    for n in range(1, 3000, 7):
        assert len(np.arange(0, play_time(n, fps), 1 / fps)) == n
        assert int(hold_time(n, fps) / (1 / fps)) == n


# ---------------------------------------------------------------- captions

def test_reading_time():
    assert cap.reading_time("对", "") == cap.MIN_DUR
    long = "一" * 60
    assert cap.reading_time(long, "") == cap.MAX_DUR
    t = cap.reading_time("井字棋有多少种不同的对局？", "How many different games of tic-tac-toe are there?")
    assert 2.5 <= t <= 4.5


def test_load_list_and_dict_forms(tmp_path):
    p = tmp_path / "captions.yaml"
    p.write_text("s01_hook:\n  - id: q\n    zh: 有多少局？\n    en: How many games?\n    at: '1:2'\n"
                 "s02:\n  a: {zh: 甲, en: A, beats: 4}\n", encoding="utf-8")
    t = cap.load(p)
    assert [c.id for c in t["s01_hook"]] == ["q"] and t["s01_hook"][0].at == "1:2"
    assert t["s02"][0].id == "a" and t["s02"][0].fixed
    assert cap.duration(t["s02"][0], Grid()) == pytest.approx(2.4)
    assert cap.load(tmp_path / "missing.yaml") == {}


def test_caption_config():
    assert cap.caption_config({})["layouts"] == ["zh-first"]
    assert cap.caption_config({"captions": "en-first"})["layout"] == "en-first"
    c = cap.caption_config({"captions": {"layouts": ["zh-first", "en-first"]}})
    assert c["layout"] == "zh-first" and c["layouts"] == ["zh-first", "en-first"]
    off = cap.caption_config({"captions": False})
    assert off["enabled"] is False and off["layouts"] == ["zh-first"]


def _cues():
    return [cap.Caption(zh="井字棋有多少种不同的对局？", en="How many different games of tic-tac-toe are there?", t=1.2,
                        dur=3.0),
            cap.Caption(zh="一局真的对局，被算了 24 次。", en="One real game, counted 24 times.", t=4.8, dur=3.0)]


def test_ass_zh_first(tmp_path):
    p = tmp_path / "a.ass"
    cap.write_ass(p, _cues(), "zh-first", 1920, 1080)
    s = p.read_text(encoding="utf-8")
    assert "PlayResY: 1080" in s and "Noto Serif CJK SC" in s and "Noto Sans Mono" in s
    ev = [line for line in s.splitlines() if line.startswith("Dialogue")]
    assert len(ev) == 4
    zh = [e for e in ev if "井字棋" in e][0]
    en = [e for e in ev if "HOW MANY" in e][0]              # English in capitals, under the Chinese
    y = lambda e: int(e.split("\\pos(")[1].split(",")[1].split(")")[0])
    assert y(zh) < y(en) and abs(y(zh) - 0.87 * 1080) < 20
    assert "\\fad(300,300)" in zh and "0:00:01.20" in zh and "0:00:04.20" in zh


def test_ass_en_first_and_scaled(tmp_path):
    p = tmp_path / "b.ass"
    cap.write_ass(p, _cues(), "en-first", 1280, 720)
    s = p.read_text(encoding="utf-8")
    ev = [line for line in s.splitlines() if line.startswith("Dialogue")]
    en = [e for e in ev if "How many different games" in e][0]
    zh = [e for e in ev if "井字棋" in e][0]
    y = lambda e: int(e.split("\\pos(")[1].split(",")[1].split(")")[0])
    assert y(en) < y(zh) <= 720


def test_wrapped_lower_line_lifts_the_upper_one(tmp_path):
    long_en = " ".join(["ghost"] * 40)
    c = [cap.Caption(zh="幽灵对局", en=long_en, t=0, dur=3)]
    p = tmp_path / "c.ass"
    cap.write_ass(p, c, "zh-first")
    ev = [line for line in p.read_text(encoding="utf-8").splitlines() if line.startswith("Dialogue")]
    en = [e for e in ev if "GHOST" in e][0]
    zh = [e for e in ev if "幽灵" in e][0]
    assert "\\N" in en                                        # wrapped onto two lines
    y = lambda e: int(e.split("\\pos(")[1].split(",")[1].split(")")[0])
    assert y(zh) < 0.87 * 1080 - 20                           # pushed up by the extra English line


def test_srt_sidecars(tmp_path):
    cap.write_srt(tmp_path / "x.zh.srt", _cues(), ("zh",))
    cap.write_srt(tmp_path / "x.zh-en.srt", _cues(), ("zh", "en"))
    zh = (tmp_path / "x.zh.srt").read_text(encoding="utf-8")
    assert "00:00:01,200 --> 00:00:04,200\n井字棋有多少种不同的对局？" in zh and "How many" not in zh
    bi = (tmp_path / "x.zh-en.srt").read_text(encoding="utf-8")
    assert "井字棋有多少种不同的对局？\nHow many different games" in bi


def test_tidy_trims_overlaps():
    a = cap.Caption(zh="一", en="one", t=0.0, dur=5.0)
    b = cap.Caption(zh="二", en="two", t=3.0, dur=2.0)
    cues, warn = cap.tidy([b, a])
    assert cues[0] is a and a.end <= 3.0 - 0.1 + 1e-9 and warn


def test_picture_only_share():
    tr = cap.Track([cap.Caption(t=0, dur=2), cap.Caption(t=1, dur=2), cap.Caption(t=6, dur=1)])
    assert tr.picture_only_share(10.0) == pytest.approx(0.6)


def test_gather_captions_rereads_text(tmp_path):
    """Timing from the events log (code-placed) or the grid (at:), text from the current captions.yaml."""
    (tmp_path / "captions.yaml").write_text(
        "s01:\n  - {id: q, zh: 新的问题？, en: \"The new question?\"}\n  - {id: t, zh: 定时, en: Timed, at: '1'}\n",
        encoding="utf-8")
    movie = tmp_path / "Scene.mp4"
    movie.with_suffix(".events.json").write_text(json.dumps({
        "grid": {"bpm": 100, "beats_per_bar": 4},
        "captions": [{"id": "q", "zh": "旧的问题？", "en": "Old?", "t": 3.6, "dur": 2.0, "placed": "code"},
                     {"id": "t", "zh": "定时", "en": "Timed", "t": 2.4, "dur": 2.0, "placed": "yaml"}]}))
    tr = fin.gather_captions(tmp_path, {}, [({"file": "scenes/s01.py", "cls": "Scene"}, movie, 9.6)])
    by = {c.id: c for c in tr.cues}
    assert by["q"].zh == "新的问题？" and by["q"].t == pytest.approx(13.2)
    assert by["t"].t == pytest.approx(9.6 + 2.4)


# ---------------------------------------------------------------- finishing pass

def test_finish_config_and_graph():
    assert fin.finish_config({}) is None
    assert fin.finish_config({"finish": True}, enabled=False) is None
    cfg = fin.finish_config({"finish": {"bloom": True, "grain": 4, "vignette": True}})
    assert cfg["bloom"]["strength"] == fin.BLOOM["strength"] and cfg["grain"] == 4.0
    assert cfg["vignette"] == pytest.approx(math.pi / 5)
    g = fin.finish_graph(cfg, 1080)
    for part in ("scale=iw/2:ih/2", "gblur=sigma=3.00", "gblur=sigma=14.00", "blend=all_mode=screen",
                 "vignette=angle=", "noise=c0s=4.0:c0f=t+u", "[vout]"):
        assert part in g
    assert "gblur=sigma=7.00" in fin.finish_graph(cfg, 540)    # radii scale with the picture
    only_grain = fin.finish_graph({"grain": 5.0}, 1080)
    assert "gblur" not in only_grain and only_grain.startswith("[0:v]noise")


def test_finish_from_look_post():
    cfg = fin.finish_config({"look": {"post": {"bloom": [6, 28], "grain": 5, "vignette": "PI/5"}}})
    assert cfg["bloom"]["radius"] == 6 and cfg["bloom"]["wide"] == 28
    assert cfg["grain"] == 5 and cfg["vignette"] == pytest.approx(math.pi / 5)


def test_voice_none_is_no_voice():
    from explainer.build import scene_env, voice_spec
    assert voice_spec({"voice": "none"}) == {}
    env = scene_env({"voice": "none"}, None, "en")
    assert env["EXPLAINER_LANG"] == "en"
