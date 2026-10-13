"""Short-format scenes (explainer/short.py) and the event log every scene writes (explainer/events.py):
grid timing in a real render, captions, the screen-fixed HUD under camera moves, particles, counters,
and the narrated VoiceScene's log. Renders tiny scenes at 480p15 in a temporary folder.

    PYTHONPATH=. python -m pytest -q tests/test_short.py
"""

import json
import subprocess
from pathlib import Path

import numpy as np
import pytest
from manim import DOWN, RIGHT, UL, Circle, Create, FadeIn, LaggedStart, Square, VGroup, tempconfig

from explainer import i18n
from explainer import short as sh
from explainer.grid import Grid

G = Grid(100)


@pytest.fixture
def project(tmp_path, monkeypatch):
    (tmp_path / "video.yaml").write_text("id: t\nformat: short\ntempo: 100\nscenes: []\n")
    (tmp_path / "captions.yaml").write_text(
        "grid_test:\n  - {id: q, zh: 有多少局？, en: 'How many games?', at: '0:2'}\n"
        "  - {id: two, zh: 两局。, en: Two games., beats: 4}\n", encoding="utf-8")
    monkeypatch.setenv("EXPLAINER_PROJECT", str(tmp_path))
    i18n.project_dir.cache_clear()
    yield tmp_path
    i18n.project_dir.cache_clear()


def render(scene_cls, media: Path):
    with tempconfig({"media_dir": str(media), "quality": "low_quality", "disable_caching": True,
                     "progress_bar": "none", "verbosity": "WARNING", "preview": False}):
        scene = scene_cls()
        scene.render()
        movie = Path(scene.renderer.file_writer.movie_file_path)
    return scene, movie


def frame_count(movie: Path) -> int:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(movie)], capture_output=True, text=True,
                       check=True)
    return int(r.stdout.strip())


class GridTest(sh.BeatScene):
    captions_key = "grid_test"

    def construct(self):
        a = sh.hairline(Square(1))
        self.play(Create(a), run_time=0.5)                 # off the grid on purpose: 0 .. 0.53 (8 frames)
        self.play(a.animate.shift(DOWN), beats=2)            # waits for the next beat (0.6), lasts 1.2 s
        self.play(FadeIn(Circle(0.3)), bars=1)              # waits for the next bar line (2.4), one bar
        self.caption("two")
        dots = VGroup(*[Circle(0.1).shift(i * 0.4 * DOWN) for i in range(5)])
        self.count(dots, every="eighth")                     # 4.8 + 0.3 i
        self.mark("hit")
        self.play(FadeIn(Square(0.5)), beats=1)
        self.wait(0.37)                                      # off the grid; the scene still ends on a bar


def test_beat_scene_lands_on_the_grid(project, tmp_path):
    scene, movie = render(GridTest, tmp_path / "media")
    log = json.loads(movie.with_suffix(".events.json").read_text())
    assert log["grid"]["bpm"] == 100 and log["format"] == "short"
    plays = [e for e in log["events"] if e["type"] == "play"]
    assert plays[1]["t"] == pytest.approx(0.6, abs=1e-3) and plays[1]["dur"] == pytest.approx(1.2, abs=1e-3)
    assert plays[2]["t"] == pytest.approx(2.4, abs=1e-3) and plays[2]["dur"] == pytest.approx(2.4, abs=1e-3)
    count = [e for e in log["events"] if e["type"] == "mark" and e["kind"] == "count"][0]
    assert count["t"] == pytest.approx(4.8, abs=1e-3)
    assert count["data"]["times"] == pytest.approx([4.8 + 0.3 * i for i in range(5)])
    cplay = [p for p in plays if "count" in (p.get("tags") or [])][0]
    assert [a["at"] for a in cplay["anims"]] == pytest.approx([0.3 * i for i in range(5)], abs=0.02)
    hit = [p for p in plays if "hit" in (p.get("tags") or [])][0]
    assert G.on_grid(hit["t"], "beat", tol=1e-3)
    # every grid point is a whole frame, and the scene ends on a bar line
    assert log["frames"] == frame_count(movie)
    assert log["frames"] % 36 == 0 and log["duration"] == pytest.approx(log["frames"] / 15, abs=1e-3)
    pad = [e for e in log["events"] if e["type"] == "wait" and "pad" in (e.get("tags") or [])]
    assert pad
    caps = {c["id"]: c for c in log["captions"]}
    assert caps["q"]["t"] == pytest.approx(1.2) and caps["q"]["placed"] == "yaml"
    assert caps["two"]["t"] == pytest.approx(4.8) and caps["two"]["dur"] == pytest.approx(2.4)
    assert caps["two"]["placed"] == "code" and caps["two"]["fixed"]


class HudTest(sh.BeatScene):
    def construct(self):
        self.fig(3, "Ghost games", "幽灵对局")
        sq = sh.hairline(Square(2), sh.ACCENTS["cool"].mid)
        self.play(Create(sq), beats=1)
        self.f0 = self.renderer.get_frame()
        self.play(self.zoom_to(sq, width=5), beats=2)
        self.f1 = self.renderer.get_frame()


def test_hud_stays_fixed_when_the_camera_moves(project, tmp_path):
    scene, movie = render(HudTest, tmp_path / "media")
    h, w = scene.f0.shape[:2]
    hud = (slice(0, int(h * 0.1)), slice(0, int(w * 0.6)))
    assert scene.f0[hud].max() > 40                         # the label is drawn ...
    assert np.array_equal(scene.f0[hud], scene.f1[hud])     # ... and did not move or scale with the zoom
    assert not np.array_equal(scene.f0, scene.f1)           # while the picture did
    log = json.loads(movie.with_suffix(".events.json").read_text())
    zoom = [e for e in log["events"] if e["type"] == "play" and "camera" in e["kinds"]][0]
    cam = [a for a in zoom["anims"] if a["kind"] == "camera"][0]
    assert cam["w"] == pytest.approx(5, abs=0.01) and cam["w0"] == pytest.approx(14.22, abs=0.01)


def test_odometer_positions():
    c = sh.RollingCounter(0, digits=4, size=40)
    assert c.digit_positions(1234) == [1.0, 2.0, 3.0, 4.0]
    p = c.digit_positions(1299.5)                            # units half way to 0, tens carrying 9 -> 0
    assert p[3] == pytest.approx(9.5) and p[2] == pytest.approx(9.5) and p[1] == pytest.approx(2.5)
    c.value.set_value(42)
    c.layout()
    shown = [max(g.get_fill_opacity() for g in col) for col in c.columns]
    assert shown[0] == 0 and shown[1] == 0 and shown[2] > 0.99 and shown[3] > 0.99   # no leading zeros
    assert c.updaters and not c.copy().updaters    # copies are static, so FadeOut(counter) can fade it


def test_splat_and_particle_clock():
    img = sh.splat(np.array([[0.0, 0.0]]), (-1, -1, 1, 1), (41, 41), size_px=1.0, glow_px=3.0)
    assert img.shape == (41, 41, 4)
    y, x = np.unravel_index(np.argmax(img[..., 3]), img.shape[:2])
    assert abs(x - 20) <= 1 and abs(y - 20) <= 1
    pos = sh.gas(200, box=(-2, -1, 2, 1), seed=1, start="left")
    assert (pos(0.0)[:, 0] <= 0).all() and (np.abs(pos(37.3)) <= [2, 1]).all()
    now = [0.0]
    f = sh.ParticleField(pos, region=(-2, -1, 2, 1), resolution=0.25)
    f.follow(lambda: now[0])
    now[0] = 2.0
    assert f.sim_time() == pytest.approx(2.0)
    f.set_speed(-1)                                          # rewind from here
    now[0] = 3.5
    assert f.sim_time() == pytest.approx(0.5)


def test_glow_and_halo():
    sq = sh.hairline(Square(1))
    g = sh.glow(sq, layers=5, radius_px=20)
    assert len(g) == 5 and g[0].get_stroke_width() > g[-1].get_stroke_width()
    assert g[0].get_stroke_opacity() < g[-1].get_stroke_opacity()
    h = sh.halo(1.5)
    assert h.width == pytest.approx(3.0) and h.pixel_array[..., 3].max() > 100


def test_voice_scene_writes_an_event_log(tmp_path, monkeypatch):
    monkeypatch.setenv("EXPLAINER_TTS", "silent")
    monkeypatch.setenv("EXPLAINER_LANG", "en")
    from explainer.scene import VoiceScene

    class Narrated(VoiceScene):
        def construct(self):
            dots = VGroup(*[Circle(0.2).shift(i * 0.5 * DOWN) for i in range(4)])
            dots[2].sound = "X"
            with self.voiceover("Four dots appear, one after another."):
                self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.5), run_time=1.0)
            self.mark("hit")
            self.play(dots.animate.to_corner(UL), run_time=0.5, kind="emphasis")
            self.wait(0.5)

    scene, movie = render(Narrated, tmp_path / "media")
    log = json.loads(movie.with_suffix(".events.json").read_text())
    assert log["grid"] is None and log["scene"] == "Narrated"
    types = [e["type"] for e in log["events"]]
    assert types[0] == "voice" and "play" in types and "wait" in types and "mark" in types
    lag = [e for e in log["events"] if e["type"] == "play"][0]
    assert lag["block"] == 0 and lag["lagged"] == ["LaggedStart"]
    assert [a["at"] for a in lag["anims"]] == pytest.approx([0.0, 0.2, 0.4, 0.6], abs=0.01)
    assert lag["anims"][2]["sound"] == "X"
    move = [e for e in log["events"] if e["type"] == "play"][-1]
    assert set(move["tags"]) == {"hit", "emphasis"} and move["block"] is None
    assert move["anims"][0]["x0"] == pytest.approx(0.0, abs=0.01)
    assert (movie.with_suffix(".subs.json")).exists()


def test_long_videos_do_not_depend_on_short_modules(tmp_path):
    from explainer.build import toolkit_sources
    (tmp_path / "video.yaml").write_text("id: long\nscenes: []\n")
    names = {p.name for p in toolkit_sources(tmp_path)}
    assert "scene.py" in names and "events.py" in names and "style.py" in names
    assert not names & {"short.py", "music.py", "finishing.py", "captions.py", "grid.py"}
    assert not names & {"build.py", "check.py", "preview.py"}         # tooling: no scene imports it
    (tmp_path / "video.yaml").write_text("id: s\nformat: short\nscenes: []\n")
    names = {p.name for p in toolkit_sources(tmp_path)}
    assert {"short.py", "grid.py", "captions.py"} <= names and "music.py" not in names


def test_pen_write_rides_the_tip():
    from manim import Line, VGroup
    a, b = Line([0, 0, 0], [3, 0, 0]), Line([3, 0, 0], [3, 1, 0])      # lengths 3 and 1
    art = VGroup(a, b)
    anim = sh.PenWrite(art, rate_func=lambda t: t)
    anim.begin()
    anim.interpolate(0.375)                                        # half of the first line (3/4 of the time)
    assert anim.pen.get_center()[:2] == pytest.approx([1.5, 0.0], abs=0.02)
    assert np.allclose(b.points, b.points[0])                     # the second line not started yet
    anim.interpolate(0.875)                                        # half way up the second
    assert anim.pen.get_center()[:2] == pytest.approx([3.0, 0.5], abs=0.02)
    anim.finish()
    assert a.get_end()[0] == pytest.approx(3.0) and b.get_end()[1] == pytest.approx(1.0)


class CountTags(sh.BeatScene):
    def construct(self):
        dots = VGroup(*[Circle(0.2).shift((i - 1.5) * 0.6 * RIGHT) for i in range(4)])
        dots[0].sound = "X@C#5"
        dots[1].sound = "X@E5"
        dots[2].sound = "@G4"                              # the count's instrument, at G4
        self.count(dots, every="eighth", sound="O")          # dots[3]: no tag -> the count's sound O


def test_counted_items_sound_as_tagged_in_a_real_render(project, tmp_path):
    """BeatScene.count logs each item's own .sound tag, and the composer plays it: instrument and note."""
    from explainer import music as mu
    scene, movie = render(CountTags, tmp_path / "media")
    log = json.loads(movie.with_suffix(".events.json").read_text())
    count = [e for e in log["events"] if e["type"] == "mark" and e["kind"] == "count"][0]
    assert count["data"]["sounds"] == ["X@C#5", "X@E5", "@G4", None] and count["data"]["sound"] == "O"
    st = mu.Settings.from_spec({"tempo": 100, "music": {"key": "D", "mode": "lydian", "palette": "pluck"}})
    score, *_ = mu.compose(mu.load_timeline([("s", 0.0, movie.with_suffix(".events.json"))]), st, log["duration"])
    t0 = count["t"]
    got = [(round(n["t"] - 0.005 - t0, 2), n["inst"], n["m"]) for n in score.notes
           if n["dur"] == 1.4 and n["inst"] not in ("pad", "bass")]
    assert [g[:2] for g in got] == [(0.0, "bell"), (0.3, "bell"), (0.6, "pluck"), (0.9, "glass")]
    assert [g[2] for g in got[:3]] == [73, 76, 67]
    assert not [f for f in score.fx if f["kind"] == "tick" and t0 - 0.01 < f["t"] < t0 + 1.0]


class SharedKey(sh.BeatScene):
    captions_key = "shared"

    def construct(self):
        self.play(Create(sh.hairline(Square(1))), beats=2)
        self.caption("b")
        self.wait_bars(2)


def test_stitch_finds_captions_under_the_scene_captions_key(project, tmp_path):
    """A scene with captions_key: the stitch reads its lines (placed by `at:` and by code) from that
    key, as the render did; a line that captions.yaml lost is reported, not silently dropped."""
    from explainer import finishing as fin
    (project / "captions.yaml").write_text(
        "shared:\n  - {id: a, zh: 甲句, en: Line A, at: '2:0'}\n  - {id: b, zh: 乙句, en: Line B}\n",
        encoding="utf-8")
    scene, movie = render(SharedKey, tmp_path / "media")
    log = json.loads(movie.with_suffix(".events.json").read_text())
    assert log["captions_key"] == "shared" and log["captions_keys"][0] == "shared"
    entry = {"file": "scenes/s07_other_name.py", "cls": "SharedKey"}
    spec = {"tempo": 100}
    track = fin.gather_captions(project, spec, [(entry, movie, 10.0)])
    assert [(c.id, c.zh, round(c.t, 2)) for c in track.cues] == [("b", "乙句", 11.2), ("a", "甲句", 14.8)]
    assert not track.warnings
    (project / "captions.yaml").write_text("shared:\n  - {id: b, zh: 乙句（改）, en: Line B}\n", encoding="utf-8")
    track = fin.gather_captions(project, spec, [(entry, movie, 10.0)])
    assert [c.zh for c in track.cues] == ["乙句（改）"]                     # the new wording, no re-render
    assert any("'a'" in w and "not in captions.yaml" in w for w in track.warnings)


def test_counter_comma_sits_like_typeset_text():
    """The thousands separator is set as Inter sets "255,168": just clear of the digit before it."""
    from manim import HEAVY, Text
    c = sh.RollingCounter(255168, digits=6, size=96)
    c.layout()
    shown = lambda col: [g for g in col if g.get_fill_opacity() > 0.5][0]
    sep = c.separators[0][1]
    before = sep.get_left()[0] - shown(c.columns[2]).get_right()[0]
    t = Text("255,168", font=sh.FONT_HEAVY, weight=HEAVY, font_size=96)
    want = t[3].get_left()[0] - t[2].get_right()[0]
    assert before == pytest.approx(want, abs=0.06)
    after = shown(c.columns[3]).get_left()[0] - sep.get_right()[0]       # next cell starts right after it
    assert after < 0.25
