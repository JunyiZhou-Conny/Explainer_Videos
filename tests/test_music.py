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
    assert mu.sync_share(cues, score) > 0.8


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
    (score, cues, *_), st = compose(tmp_path, spec)
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
