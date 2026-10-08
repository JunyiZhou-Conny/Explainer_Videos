"""The event-driven composer (explainer/music.py): determinism, grid timing of the score, loudness and
peaks of the master, ducking under narration.

    PYTHONPATH=. python -m pytest -q tests/test_music.py
"""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from explainer import music as mu
from explainer.grid import Grid

REPO = Path(__file__).resolve().parent.parent
G = Grid(100)


def leaf(anim, mob, x, y, w, h, at=0.0, end=0.6, kind="reveal", **kw):
    return {"anim": anim, "kind": kind, "rate": "smooth", "mob": mob, "x": x, "y": y, "w": w, "h": h, "n": 1,
            "at": at, "end": end, **kw}


def short_logs():
    """Two shorts scenes (4 bars + 3 bars) with the events a BeatScene writes."""
    b = G.bar
    s1 = {"version": 1, "scene": "One", "fps": 60.0, "duration": 4 * b, "frames": int(4 * b * 60),
          "grid": {"bpm": 100.0, "beat": 0.6, "beats_per_bar": 4, "bar": 2.4, "offset": 0.0}, "events": [
              {"type": "play", "t": 0.0, "dur": 1.2, "kinds": ["reveal"], "anims": [
                  leaf("Create", "Line", -0.5, 0, 0.0, 3.0, 0, 1.2), leaf("Create", "Line", 0.5, 0, 0.0, 3.0, 0, 1.2),
                  leaf("Create", "Line", 0, 0.5, 3.0, 0.0, 0, 1.2), leaf("Create", "Line", 0, -0.5, 3.0, 0.0, 0, 1.2)]},
              {"type": "mark", "t": 1.2, "kind": "count", "dur": 2.7, "data": {
                  "n": 9, "every": 0.3, "times": [round(1.2 + 0.3 * i, 4) for i in range(9)],
                  "xs": [(i % 3) - 1.0 for i in range(9)], "sound": "O"}},
              {"type": "play", "t": 1.2, "dur": 2.7, "kinds": ["reveal"], "tags": ["count"], "anims": [
                  leaf("FadeIn", "Circle", (i % 3) - 1.0, 0, 0.6, 0.6, 0.3 * i, 0.3 * i + 0.6, sound="O")
                  for i in range(9)]},
              {"type": "mark", "t": 7.2, "kind": "hit", "dur": 0.6},
              {"type": "play", "t": 7.2, "dur": 0.6, "kinds": ["reveal"], "tags": ["hit"], "anims": [
                  leaf("FadeIn", "VGroup", 0, 0, 3, 3)]},
              {"type": "wait", "t": 7.8, "dur": 1.8}]}
    s2 = {"version": 1, "scene": "Two", "fps": 60.0, "duration": 3 * b, "frames": int(3 * b * 60),
          "grid": s1["grid"], "events": [
              {"type": "mark", "t": 0.0, "kind": "silence", "dur": 2.4},
              {"type": "wait", "t": 0.0, "dur": 2.4, "tags": ["silence"]},
              {"type": "mark", "t": 2.4, "kind": "title", "dur": 1.2},
              {"type": "play", "t": 2.4, "dur": 1.2, "kinds": ["reveal"], "tags": ["title"], "anims": [
                  leaf("Write", "Text", 0, 0, 4, 2, 0, 1.2)]},
              {"type": "play", "t": 3.6, "dur": 2.4, "kinds": ["count"], "anims": [
                  leaf("CounterLand", "RollingCounter", 3, 0, 3, 1, 0, 2.4, kind="count",
                       lands=[0.4, 0.5, 0.6, 0.7, 0.8, 0.9])]},
              {"type": "wait", "t": 6.0, "dur": 1.2}]}
    return s1, s2


def write_logs(tmp_path):
    s1, s2 = short_logs()
    p1, p2 = tmp_path / "One.events.json", tmp_path / "Two.events.json"
    p1.write_text(json.dumps(s1))
    p2.write_text(json.dumps(s2))
    return [("s01", 0.0, p1), ("s02", 4 * G.bar, p2)]


SPEC = {"tempo": 100, "music": {"key": "D", "mode": "lydian", "sounds": {"X": "bell", "O": "glass"}}}


def compose(tmp_path, spec=SPEC):
    scenes = mu.load_timeline(write_logs(tmp_path))
    st = mu.Settings.from_spec(spec)
    return mu.compose(scenes, st, 7 * G.bar), st


def test_compose_is_deterministic(tmp_path):
    (s1, cues1, _, bed1, acc1), _ = compose(tmp_path)
    (s2, cues2, _, bed2, acc2), _ = compose(tmp_path)
    assert json.dumps(s1.as_dict(), sort_keys=True) == json.dumps(s2.as_dict(), sort_keys=True)
    assert np.array_equal(bed1, bed2) and np.array_equal(acc1, acc2)
    assert bed1.shape == (int(round(7 * G.bar * mu.SR)), 2)


def test_deterministic_across_processes(tmp_path):
    """Two separate processes (different hash seeds) write the same samples."""
    write_logs(tmp_path)
    code = ("import json,sys,hashlib,numpy as np; from pathlib import Path; from explainer import music as mu;"
            "p=Path(sys.argv[1]); sc=mu.load_timeline([('s01',0.0,p/'One.events.json'),('s02',9.6,p/'Two.events.json')]);"
            f"st=mu.Settings.from_spec({SPEC!r}); r=mu.compose(sc, st, 16.8);"
            "m,_=mu.music_only(r[3], r[4], st); print(hashlib.md5(m.astype(np.float32).tobytes()).hexdigest())")
    digests = set()
    for seed in ("1", "2"):
        env = dict(os.environ, PYTHONPATH=str(REPO), PYTHONHASHSEED=seed)
        out = subprocess.run([sys.executable, "-c", code, str(tmp_path)], env=env, capture_output=True, text=True,
                             check=True)
        digests.add(out.stdout.strip())
    assert len(digests) == 1


def test_chords_change_on_bar_lines_and_resolve_on_the_title(tmp_path):
    (score, *_), _ = compose(tmp_path)
    times = [c.t for c in score.chords]
    assert all(G.on_grid(t, "bar", tol=1e-6) or G.on_grid(t, "beat", tol=1e-6) for t in times)
    assert all(G.on_grid(t, "bar", tol=1e-6) for t, c in zip(times, score.chords) if c.tag == "")
    assert score.chords[0].degree == 1                           # the tonic opens
    title = [c for c in score.chords if c.tag == "title"]
    assert title and title[0].degree == 1 and title[0].t == pytest.approx(9.6 + 2.4)
    before = [c for c in score.chords if c.t < title[0].t][-1]
    assert before.degree == 5 and before.sus                     # a suspended dominant prepares it
    mid = [c for c in score.chords if 0 < c.t < title[0].t and c.tag not in ("dominant",)]
    assert all(c.degree != 1 for c in mid)                       # the tonic is withheld meanwhile


def test_one_note_per_counted_object_on_its_own_time(tmp_path):
    (score, cues, *_), _ = compose(tmp_path)
    glass = [n for n in score.notes if n["inst"] == "glass" and 1.1 < n["t"] < 4.0]
    assert len(glass) == 9
    assert [round(n["t"] - 0.005, 3) for n in glass] == [round(1.2 + 0.3 * i, 3) for i in range(9)]
    assert [n["m"] for n in glass] == sorted(n["m"] for n in glass)      # rising
    pans = [n["pan"] for n in glass[:3]]
    assert pans[0] < pans[1] < pans[2]                                    # panned to the square
    land = [n for n in score.notes if 14.0 < n["t"] < 15.5 and n["dur"] == 2.2]
    assert [n["t"] for n in land] == pytest.approx([13.2 + 2.4 * u for u in (0.4, 0.5, 0.6, 0.7, 0.8, 0.9)])
    assert mu.score_coverage(cues, score) > 0.8


def test_structure_hits_risers_and_silence(tmp_path):
    (score, cues, ctx, bed, acc), st = compose(tmp_path)
    fx = score.fx
    booms = [f["t"] for f in fx if f["kind"] == "boom"]
    assert 7.2 in booms and pytest.approx(12.0) in booms           # the hit, and the title
    risers = [f for f in fx if f["kind"] == "riser"]
    assert any(abs(f["t"] + f["dur"] - 7.2) < 1e-6 for f in risers)   # a riser lands on the hit
    assert [9.6, 12.0, "silence"] in score.silences
    i, j = int(9.65 * mu.SR), int(11.95 * mu.SR)
    assert np.max(np.abs((bed + acc)[i:j])) < 1e-9                 # planned digital silence
    assert np.max(np.abs((bed + acc)[int(12.05 * mu.SR):int(12.5 * mu.SR)])) > 1e-3   # back on the title


def test_master_loudness_and_peaks(tmp_path):
    (score, cues, ctx, bed, acc), st = compose(tmp_path)
    m, rep = mu.music_only(bed, acc, st)
    assert abs(mu.lufs(m) - (-14.0)) < 0.5
    assert mu.true_peak_db(m) <= -1.0 + 0.05
    assert rep["lr_correlation"] > 0                               # mono-safe on a phone speaker


def test_lufs_reference():
    t = np.arange(int(3 * mu.SR)) / mu.SR
    x = 0.1 * np.sin(2 * np.pi * 997 * t)
    # BS.1770: a 0 dBFS 1 kHz sine in one channel reads -3.01 LKFS, so amplitude 0.1 in both reads -20.0
    assert mu.lufs(np.stack([x, x], 1)) == pytest.approx(-20.0, abs=0.15)
    assert mu.lufs(np.stack([x, 0 * x], 1)) == pytest.approx(-23.0, abs=0.15)


def test_limiter_keeps_the_ceiling():
    rng = np.random.default_rng(0)
    x = rng.normal(0, 0.3, (mu.SR, 2))
    y = mu.limit(x, -1.0)
    assert np.max(np.abs(y)) <= 10 ** (-1 / 20) + 1e-9


def test_ducking_under_narration(tmp_path):
    (score, cues, ctx, bed, acc), st = compose(tmp_path)
    n = len(bed)
    rng = np.random.default_rng(3)
    voice = np.zeros((n, 2))
    for a, b in ((1.0, 4.0), (6.0, 9.0), (11.0, 14.0)):                # three sentences
        i, j = int(a * mu.SR), int(b * mu.SR)
        v = rng.normal(0, 0.08, j - i) * (1 + np.sin(np.arange(j - i) / mu.SR * 2 * np.pi * 4))
        voice[i:j] = v[:, None]
    mixed, music, rep = mu.mix_under_voice(bed, acc, voice, st)
    assert rep["music_under_speech_lufs"] <= rep["voice_lufs"] - 14.5      # about 15 LU under the speech
    assert rep["music_in_gaps_lufs"] == pytest.approx(rep["voice_lufs"] - 6, abs=2.0)
    assert rep["mix_true_peak_dbtp"] <= -0.9


def test_free_time_harmony_for_narrated_logs(tmp_path):
    """A narrated scene (no grid): chords change on cuts and big reveals, at least 2 s apart."""
    log = {"version": 1, "scene": "Hook", "fps": 60, "duration": 30.0, "frames": 1800, "grid": None, "events": [
        {"type": "voice", "t": 0.0, "dur": 5.0, "block": 0, "text": "x"},
        {"type": "play", "t": 0.5, "dur": 1.0, "kinds": ["reveal"], "block": 0,
         "anims": [leaf("Write", "Text", 0, 2, 6, 1.2, 0, 1.0)]},
        {"type": "play", "t": 9.0, "dur": 1.0, "kinds": ["reveal"], "block": None,
         "anims": [leaf("FadeIn", "VGroup", 0, 0, 5, 3, 0, 1.0)]},
        {"type": "play", "t": 9.8, "dur": 1.0, "kinds": ["reveal"], "block": None,
         "anims": [leaf("FadeIn", "VGroup", 0, 0, 5, 3, 0, 1.0)]}]}
    p = tmp_path / "Hook.events.json"
    p.write_text(json.dumps(log))
    scenes = mu.load_timeline([("s01", 0.0, p)])
    score, *_ = mu.compose(scenes, mu.Settings.from_spec({}), 30.0)
    ts = [c.t for c in score.chords]
    assert all(b - a >= 2.0 - 1e-9 for a, b in zip(ts, ts[1:]))
    assert score.grid is None and score.chords[-1].degree == 1


def test_settings_validation():
    with pytest.raises(ValueError):
        mu.Settings.from_spec({"music": {"mode": "bebop"}})
    s = mu.Settings.from_spec({"tempo": 90, "music": {"key": "A", "mode": "minor", "acts": [{"at": 4, "key": "C"}]}})
    assert s.bpm == 90 and s.acts and s.sounds["X"] == "bell"
    assert mu.music_enabled({"music": {"key": "D"}}) and not mu.music_enabled({})
    assert not mu.music_enabled({"music": {"enabled": False}})
    assert mu.music_enabled({"format": "short"})                          # a short has music by default
    assert not mu.music_enabled({"format": "short", "music": False})
    assert "count" not in mu.Settings.from_spec({}).sounds                # (so the palette's count sound is used)
    assert mu.seed_for("a", 1) == mu.seed_for("a", 1) != mu.seed_for("a", 2)


def test_midi_file(tmp_path):
    (score, *_), _ = compose(tmp_path)
    p = tmp_path / "s.mid"
    mu.write_midi(score, p, bpm=100)
    data = p.read_bytes()
    assert data[:4] == b"MThd" and data.count(b"MTrk") >= 3
    assert hashlib.md5(data).hexdigest() == hashlib.md5(p.read_bytes()).hexdigest()


def test_video_positions():
    scenes = [mu.SceneLog("s01", 0.0, 9.6, {"scene": "One"}), mu.SceneLog("s02", 9.6, 7.2, {"scene": "Two"})]
    vt = lambda at: mu.video_time(at, scenes, G)
    assert vt("10.1") == pytest.approx(21.6)            # bar 10, beat 1, counted from 1
    assert vt("19.4") == pytest.approx(18 * 2.4 + 1.8)
    assert vt("12.3+") == pytest.approx(11 * 2.4 + 1.2 + 0.3)
    assert vt(5) == pytest.approx(9.6) and vt("2:1") == pytest.approx(5.4)
    assert vt("123.4s") == pytest.approx(123.4) and vt("s02") == pytest.approx(9.6)


def test_video_yaml_cues_palette_and_named_chords(tmp_path):
    """The structure and the sounds can be written in video.yaml: cues at bar.beat positions (with a
    named chord or a key change), a palette that maps the scene's sound tags to sounds."""
    spec = {"tempo": 100, "music": {
        "key": "D", "mode": "lydian",
        "palette": {"O": "reversed_glass", "cut": "sub_boom", "count": "tick"},
        "cues": [{"at": "4.1", "kind": "title", "chord": "vi"},
                 {"at": "5.1", "kind": "tape_stop", "bars": 1},
                 {"at": "7.1", "kind": "hit", "chord": "bVI", "key": "E"}]}}
    s1, s2 = short_logs()
    s2["events"] = s2["events"][2:]                       # (no planned silence at 9.6: the cut is heard)
    p1, p2 = tmp_path / "One.events.json", tmp_path / "Two.events.json"
    p1.write_text(json.dumps(s1))
    p2.write_text(json.dumps(s2))
    scenes = mu.load_timeline([("s01", 0.0, p1), ("s02", 4 * G.bar, p2)])
    st = mu.Settings.from_spec(spec)
    score, cues, *_ = mu.compose(scenes, st, 7 * G.bar)
    title = [c for c in score.chords if c.tag == "title"]
    assert title and title[0].t == pytest.approx(7.2) and title[0].degree == 6      # vi, not the tonic
    hit = [c for c in score.chords if abs(c.t - 14.4) < 1e-6][0]
    assert hit.name == "bVI" and hit.pcs()[0] == (4 + 8) % 12                       # C in E (the new key)
    assert [9.6, 12.0, "tape_stop"] in score.silences
    assert any(n["inst"] == "glass_rev" for n in score.notes)                        # O -> reversed glass
    assert any(f["kind"] == "boom" and abs(f["t"] - 9.6) < 1e-6 for f in score.fx)   # the cut -> sub boom


def test_pitched_sound_tags(tmp_path):
    s1, s2 = short_logs()
    for i, a in enumerate(s1["events"][2]["anims"]):
        a["sound"] = "O@" + ["C#5", "D5", "E5", "G#4", "A4", "B4", "D4", "E4", "F#4"][i]
    s1["events"][1]["data"]["sound"] = None
    s1["events"][2]["tags"] = []                      # played as ordinary reveals, one note per square
    p = tmp_path / "One.events.json"
    p.write_text(json.dumps(s1))
    score, *_ = mu.compose(mu.load_timeline([("s01", 0.0, p)]), mu.Settings.from_spec(SPEC), 4 * G.bar)
    ms = [n["m"] for n in score.notes if n["inst"] == "glass" and 1.1 < n["t"] < 4.0 and n["dur"] == 1.8]
    assert ms == [73, 74, 76, 68, 69, 71, 62, 64, 66]


# ---------------------------------------------------------------- ducking, counts, structure, clicks

def test_duck_curve_timing():
    """A burst of speech from 2.0 to 3.0 s: the music starts down 150 ms before it, is fully down 120 ms
    later (before the first syllable), stays down until 0.45 s after the speech, then takes 600 ms to
    come back."""
    n = int(6 * mu.SR)
    v = np.zeros(n)
    i, j = int(2.0 * mu.SR), int(3.0 * mu.SR)
    v[i:j] = np.random.default_rng(0).normal(0, 0.1, j - i)
    db = 20 * np.log10(mu.duck_curve(v, 12.0))
    at = lambda t: float(db[int(round(t * mu.SR))])
    assert at(1.83) == pytest.approx(0.0, abs=0.01)                   # not yet
    assert -12 < at(1.91) < -1                                         # going down from 1.85
    for t in (1.98, 2.0, 2.5, 2.99, 3.2, 3.44):                       # full depth: 1.97 .. 3.45
        assert at(t) == pytest.approx(-12.0, abs=0.05), t
    assert -12 < at(3.75) < -1                                         # releasing
    assert at(4.06) == pytest.approx(0.0, abs=0.01)                   # back by 3.45 + 0.6
    assert np.all(mu.duck_curve(np.zeros(n)) == 1.0)                   # no voice: no ducking


def _count_log(sounds=None, sound=None, n=4):
    times = [round(1.2 + 0.3 * i, 4) for i in range(n)]
    data = {"n": n, "every": 0.3, "times": times, "xs": [float(i - 1) for i in range(n)]}
    if sounds is not None:
        data["sounds"] = sounds
    if sound is not None:
        data["sound"] = sound
    return {"version": 1, "scene": "C", "fps": 60.0, "duration": 2 * G.bar, "frames": int(2 * G.bar * 60),
            "grid": {"bpm": 100.0, "beat": 0.6, "beats_per_bar": 4, "bar": 2.4, "offset": 0.0},
            "events": [{"type": "mark", "t": 1.2, "kind": "count", "dur": 1.5, "data": data},
                       {"type": "play", "t": 1.2, "dur": 1.5, "kinds": ["reveal"], "tags": ["count"],
                        "anims": [leaf("FadeIn", "Circle", i - 1.0, 0, 0.5, 0.5, 0.3 * i, 0.3 * i + 0.6)
                                  for i in range(n)]}]}


def _score_of(tmp_path, log, spec=SPEC):
    p = tmp_path / "C.events.json"
    p.write_text(json.dumps(log))
    score, *_ = mu.compose(mu.load_timeline([("s01", 0.0, p)]), mu.Settings.from_spec(spec), 2 * G.bar)
    return score


def test_count_items_sound_as_their_own_tags(tmp_path):
    """Each counted item sounds as its .sound tag says (instrument and fixed note), untagged items use
    the count's sound=, and a count without tags uses the palette's count instrument, not ticks."""
    score = _score_of(tmp_path, _count_log(["X@C#5", "X@E5", "@G4", None], sound="O"))
    got = [(round(n["t"] - 0.005, 3), n["inst"], n["m"]) for n in score.notes
           if n["inst"] not in ("pad", "bass") and 1.1 < n["t"] < 2.4 and n["dur"] == 1.4]
    assert [g[:2] for g in got] == [(1.2, "bell"), (1.5, "bell"), (1.8, "glass"), (2.1, "glass")]
    assert got[0][2] == 73 and got[1][2] == 76 and got[2][2] == 67      # C#5, E5, G4 as tagged
    assert not [f for f in score.fx if f["kind"] == "tick" and 1.1 < f["t"] < 2.4]
    plain = _score_of(tmp_path, _count_log())                            # glass palette: count = glass
    insts = {n["inst"] for n in plain.notes if 1.1 < n["t"] < 2.4 and n["dur"] == 1.4}
    assert insts == {"glass"}
    ticks = _score_of(tmp_path, _count_log(), {**SPEC, "music": {**SPEC["music"], "palette": {"count": "tick"}}})
    assert len([f for f in ticks.fx if f["kind"] == "tick" and 1.1 < f["t"] < 2.4]) == 4   # the video asks for ticks


def test_structure_cues_are_not_doubled(tmp_path):
    """A title marked in the scene and also in video.yaml music.cues sounds once (one boom, one rolled
    chord), on the scene's time, with video.yaml's chord."""
    spec = {"tempo": 100, "music": {"key": "D", "mode": "lydian",
                                    "cues": [{"at": "6.1", "kind": "title", "chord": "vi"},      # = 12.0 s
                                             {"at": "5.1", "kind": "cut"}]}}                       # the scene cut
    (score, cues, *_), _ = compose(tmp_path, spec)
    booms = [f["t"] for f in score.fx if f["kind"] == "boom"]
    assert booms.count(pytest.approx(12.0)) == 1
    cuts = [c for c in cues if c.kind in ("cut", "section") and abs(c.t - 9.6) < 1e-6]
    assert len(cuts) == 1 and cuts[0].data["merged"] == ["cut"]          # the scene cut and video.yaml's
    title = [c for c in cues if c.kind == "title"]
    assert len(title) == 1 and title[0].data["chord"] == "vi" and title[0].scene == "s02"
    assert [c for c in score.chords if c.tag == "title"][0].degree == 6


def test_no_blips_at_the_start_of_a_silence(tmp_path):
    """An accent that would start just before (or inside) a planned silence is left out instead of
    being cut to a 30 ms blip; the boom on the return stays."""
    s1, s2 = short_logs()
    s1["events"].append({"type": "play", "t": 7.8, "dur": 1.75, "kinds": ["count"], "anims": [
        leaf("CounterRoll", "RollingCounter", 3, 0, 3, 1, 0, 1.75, kind="count")]})   # lands at 9.55
    p1, p2 = tmp_path / "One.events.json", tmp_path / "Two.events.json"
    p1.write_text(json.dumps(s1))
    p2.write_text(json.dumps(s2))
    scenes = mu.load_timeline([("s01", 0.0, p1), ("s02", 4 * G.bar, p2)])
    score, *_ = mu.compose(scenes, mu.Settings.from_spec(SPEC), 7 * G.bar)
    assert score.dropped >= 1
    assert not [n for n in score.notes if n["inst"] not in ("pad", "bass") and 9.48 <= n["t"] < 11.99]
    assert any(f["kind"] == "boom" and f["t"] == pytest.approx(12.0) for f in score.fx)


def test_click_scan(tmp_path):
    (score, cues, ctx, bed, acc), st = compose(tmp_path)
    m, _ = mu.music_only(bed, acc, st)
    planned = mu.planned_transients(score)
    assert mu.click_scan(m, planned) == []                         # every note ends with a fade
    assert mu.click_scan(acc, planned) == []
    y = m.copy()
    y[int(5.3 * mu.SR):] = 0.0                                     # a sound cut off while it rings
    assert mu.click_scan(y, planned) == [pytest.approx(5.3, abs=0.002)]
    t = np.arange(mu.SR * 2) / mu.SR
    tone = 0.2 * np.sin(2 * np.pi * 440 * t)
    tone[mu.SR:] = 0.0
    assert mu.click_scan(tone, [1.0]) == []                         # ... unless the score planned it there


def test_midi_has_every_instrument(tmp_path):
    spec = {"tempo": 100, "music": {"key": "D", "palette": {"O": "reversed_glass", "X": "marimba"}}}
    (score, *_), _ = compose(tmp_path, spec)
    score.note(1.0, 0.5, 70, 0.5, "wood")
    p = tmp_path / "s.mid"
    mu.write_midi(score, p, bpm=100)
    assert p.read_bytes().count(b"MTrk") >= 5


def test_planned_progression_joins_and_hit_sizes(tmp_path):
    """video.yaml may write the progression bar by bar (slash basses, rests), mark a scene join as a
    segue (no cut sound), and size its hits."""
    spec = {"tempo": 100, "music": {
        "key": "D", "mode": "lydian",
        "chords": {1: "I", 2: "II/D", 3: "vi", 5: "rest", 6: "Vsus", 7: "I"},
        "joins": {"5.1": "segue"},
        "cues": [{"at": "4.1", "kind": "hit", "size": 0.2}]}}
    (score, cues, *_), _ = compose(tmp_path, spec)
    names = [(round(c.t, 2), c.name) for c in score.chords]
    assert names == [(0.0, "I"), (2.4, "II/D"), (4.8, "vi"), (9.6, "rest"), (12.0, "Vsus"), (14.4, "I")]
    bass = [n for n in score.notes if n["inst"] == "bass" and abs(n["t"] - 2.4) < 0.2]
    assert bass and all(n["m"] % 12 == 2 for n in bass)                  # E minor over a D bass
    assert not [n for n in score.notes if n["inst"] == "pad" and 9.0 < n["t"] < 11.9]   # the rest
    assert not [c for c in cues if c.kind == "cut"]                       # the join at 9.6 is a segue
    assert not [f for f in score.fx if f["kind"] == "thump"]
    hit = [f for f in score.fx if f["kind"] == "boom" and f["t"] == pytest.approx(7.2)]
    assert hit and hit[0]["gain"] < 0.5                                   # a small hit (size 0.2)


def test_levels_fade_the_score(tmp_path):
    """video.yaml music.levels is a fader over the score: dB at positions, linear in between, per stem;
    a cold open can start near silence and build into its title. Without levels nothing changes."""
    (_, _, ctx0, bed0, acc0), _ = compose(tmp_path)
    spec = {**SPEC, "music": {**SPEC["music"], "levels": {"1.1": {"bed": -20, "accents": -10}, "2.1": -20, 3: 0}}}
    (_, _, ctx1, bed1, acc1), _ = compose(tmp_path, spec)
    assert ctx0["levels"] is None and ctx1["levels"] is not None
    sr = mu.SR
    first = slice(int(0.3 * sr), int(1.2 * sr))          # inside bar 1, before the count starts
    late = slice(int(5.2 * sr), int(7.0 * sr))           # bar 3 on: back to 0 dB
    assert mu.lufs(bed0[first]) - mu.lufs(bed1[first]) == pytest.approx(20, abs=1.5)
    assert np.allclose(bed0[late], bed1[late]) and np.allclose(acc0[late], acc1[late])
    t = np.arange(len(bed0)) / sr
    mid = (t > 3.55) & (t < 3.65)                          # 3.6 s: half way from bar 2 (-20 dB) to bar 3 (0 dB)
    ratio = np.sqrt(np.mean(acc1[mid] ** 2) / np.mean(acc0[mid] ** 2))
    assert 20 * np.log10(ratio) == pytest.approx(-10, abs=1.0)
    with pytest.raises(ValueError):
        compose(tmp_path, {**SPEC, "music": {**SPEC["music"], "levels": {"nowhere": -3}}})


def test_count_gain_scales_a_phrase(tmp_path):
    """A count mark's `gain` makes that phrase softer (or louder) without changing its notes or times."""
    loud = _score_of(tmp_path, _count_log(["X@C#5", "X@E5", "O@G4", "tick"]))
    log = _count_log(["X@C#5", "X@E5", "O@G4", "tick"])
    log["events"][0]["data"]["gain"] = 0.5
    soft = _score_of(tmp_path, log)
    pick = lambda sc: [(n["t"], n["m"], n["vel"]) for n in sc.notes if n["inst"] in ("bell", "glass") and 1.1 < n["t"] < 2.4]
    a, b = pick(loud), pick(soft)
    assert [x[:2] for x in a] == [x[:2] for x in b] and len(a) == 3
    assert all(y[2] == pytest.approx(0.5 * x[2], abs=1e-3) for x, y in zip(a, b))
    tick = lambda sc: [f["gain"] for f in sc.fx if f["kind"] == "tick" and 2.0 < f["t"] < 2.2]
    assert tick(soft)[0] == pytest.approx(0.5 * tick(loud)[0], abs=1e-3)
