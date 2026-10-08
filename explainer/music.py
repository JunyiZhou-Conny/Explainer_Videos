"""Music that follows the picture: one continuous score per video, composed from the scenes' event
logs and synthesized in NumPy/SciPy (no samples, no third-party audio, nothing to license).

    python -m explainer.music videos/<id>            # compose + render: build/music/<quality>/...
    python -m explainer.music videos/<id> -q l --report

`explainer.build videos/<id> --music` (or a `music:` block in video.yaml) runs this and mixes the
result: music only (a short) at about -14 LUFS with peaks <= -1 dBTP, or under the narration (a long
video) ducked about 15 LU below the speech.

How the picture drives the music (every rule reads the event log; nothing is hand-timed):
    scene cut / mark "cut"      a chord change on the downbeat, a soft sub thump, a riser into it
    mark "hit" / "title"        a boom (pitch drop 250 -> 45 Hz, plus its 2nd harmonic), a shimmer, a
                                riser over the 1-2 bars before it, the chord moves (to I on "title")
    a reveal                    one note per object: bells for small marks, glass, plucks for text, a
                                rolled chord for big titles, an upward run for a long line, panned to x
    a count (self.count, a      one note or tick per item, rising, on the items' own times
    RollingCounter)
    mark "silence" (dur)        a planned drop-out, then a hit on the return
    mark "tape_stop" (dur)      everything glides down and stops; silence until the next hit or cut
    mark "resolve"              the tonic arrives (it is withheld until then)
    on-screen motion            the pads' brightness (low-pass cutoff) follows an activity curve
    beat grid (shorts)          chords change on bar lines, and a soft pulse runs on the grid

video.yaml (all optional):

    music:
      key: D                    # tonic
      mode: lydian              # ionian / lydian / mixolydian / dorian / aeolian / phrygian / major / minor
      mood: bright              # bright | dark | warm: filter, reverb and pulse presets
      palette: glass            # glass | soft | pluck: which instrument plays which role (or a map, as sounds)
      sounds: {X: bell, O: glass}   # semantic sound: a mobject's .sound tag -> instrument ("X@C#5": a fixed note)
      acts: [{at: s05_turn, key: A, mode: major}]   # key changes (see video_time for positions)
      cues: [{at: "10.1", kind: title, chord: vi}, {at: "64.1", kind: silence, bars: 1}]
                                # structure on the video's timeline: bar.beat counted from 1
      density: 3                # at most this many ordinary accents per second
      pulse: true               # shorts: the soft grid pulse
      lufs: -14                 # music-only loudness target
      duck: {depth: 12, accents: 7, gap: 6, under: 15}   # narrated: dB of ducking (bed, accents); the music
                                # `gap` LU under the voice between sentences, at least `under` LU under speech
      seed: 7

Everything is deterministic: the same logs and settings give the same samples (seeded generators,
no Python hash(), no clock).
"""

from __future__ import annotations

import argparse
import json
import math
import zlib
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy import signal

from .grid import Grid

SR = 48000

# ---------------------------------------------------------------- settings

MODES = {
    "ionian": [0, 2, 4, 5, 7, 9, 11], "major": [0, 2, 4, 5, 7, 9, 11],
    "lydian": [0, 2, 4, 6, 7, 9, 11], "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10], "aeolian": [0, 2, 3, 5, 7, 8, 10], "minor": [0, 2, 3, 5, 7, 8, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
}
NOTE = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3, "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7,
        "G#": 8, "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
BRIGHT = {"ionian", "major", "lydian", "mixolydian"}

# scale degrees (1-based) visited while the tonic is withheld, per mode family
CYCLE_BRIGHT = [4, 6, 2, 6, 4, 3, 2, 6]
CYCLE_DARK = [6, 4, 7, 3, 6, 4, 2, 7]

MOODS = {   # pad filter range (Hz), reverb send, pulse, an octave-up "air" pad layer, high shelf on the
            # accents (dB), and (music only) bus gains for the bass and the accents
    "bright": dict(cut_lo=1000, cut_hi=6000, reverb=0.38, pulse=0.9, air=0.6, sparkle=3.0, bass=0.5, keys=2.0,
                   tone="bright"),
    "warm": dict(cut_lo=800, cut_hi=4000, reverb=0.42, pulse=0.7, air=0.4, sparkle=1.5, bass=0.65, keys=1.6,
                 tone="bright"),
    "dark": dict(cut_lo=500, cut_hi=2400, reverb=0.46, pulse=0.6, air=0.25, sparkle=-1.0, bass=0.8, keys=1.2,
                 tone="soft"),
}
PALETTES = {     # role -> instrument
    "glass": dict(mark="bell", mark2="glass", text="pluck", title="bell", count="glass", tick="tick",
                  emphasis="glass", sweep="bell", grid="pluck", arrow="glass", pulse="glass"),
    "soft": dict(mark="glass", mark2="pluck", text="pluck", title="glass", count="pluck", tick="tick",
                 emphasis="glass", sweep="glass", grid="pluck", arrow="pluck", pulse="pluck"),
    "pluck": dict(mark="pluck", mark2="glass", text="pluck", title="bell", count="pluck", tick="tick",
                  emphasis="bell", sweep="pluck", grid="pluck", arrow="pluck", pulse="pluck"),
}
INSTRUMENTS = ("pad", "bass", "bell", "glass", "pluck", "wood", "glass_rev")
FX = ("boom", "thump", "tick", "blip", "riser", "whoosh_up", "whoosh_down", "whoosh_rev", "shimmer", "swell")
ALIASES = {      # other names for the sounds, as a video.yaml palette may write them
    "marimba": "wood", "woodblock": "wood", "harp": "pluck", "kalimba": "pluck", "celesta": "glass",
    "chime": "bell", "reversed_glass": "glass_rev", "reverse_glass": "glass_rev", "ghost": "glass_rev",
    "reverse_whoosh": "whoosh_rev", "reversed_whoosh": "whoosh_rev", "sub_boom": "boom", "hit": "boom",
    "soft_pulse": "blip", "pulse": "blip", "click": "tick", "whoosh": "whoosh_up", "sparkle": "shimmer",
}


def resolve_sound(name: str) -> str:
    n = str(name).strip().lower()
    return ALIASES.get(n, n)
DEFAULT_SOUNDS = {"X": "bell", "O": "glass", "count": "tick", "tick": "tick", "red": "whoosh_rev",
                  "undo": "whoosh_rev", "erase": "whoosh_rev", "light": "shimmer", "hit": "boom"}


@dataclass
class Settings:
    key: str = "D"
    mode: str = "lydian"
    mood: str = "bright"
    palette: str = "glass"
    sounds: dict = field(default_factory=dict)
    acts: list = field(default_factory=list)
    density: float = 3.0
    pulse: bool = True
    lufs: float = -14.0
    peak: float = -1.0
    duck: dict = field(default_factory=lambda: {"depth": 12.0, "accents": 7.0, "gap": 6.0, "under": 15.0})
    seed: int = 7
    bpm: float | None = None
    cues: list = field(default_factory=list)   # structure placed in video.yaml (video time)

    @classmethod
    def from_spec(cls, spec: dict) -> "Settings":
        m = spec.get("music")
        m = dict(m) if isinstance(m, dict) else {}
        s = cls()
        for k in ("key", "mode", "mood", "density", "pulse", "lufs", "peak", "seed", "bpm"):
            if k in m:
                setattr(s, k, m[k])
        if "true_peak_dbtp" in m:
            s.peak = float(m["true_peak_dbtp"])
        pal = m.get("palette")
        sounds = dict(m.get("sounds") or {})
        if isinstance(pal, dict):                       # palette as a map of names to sounds
            sounds = {**pal, **sounds}
        elif pal is not None:
            s.palette = str(pal)
        s.sounds = {**DEFAULT_SOUNDS, **{str(k): resolve_sound(v) for k, v in sounds.items()}}
        s.acts = list(m.get("acts") or [])
        s.cues = [dict(c) for c in m.get("cues") or []]
        s.acts += [c for c in s.cues if c.get("key") or c.get("mode")]
        s.duck = {**s.duck, **(m.get("duck") or {})}
        if s.bpm is None:
            s.bpm = spec.get("tempo") or (spec.get("grid") or {}).get("bpm")
            s.bpm = float(s.bpm) if s.bpm else None
        s.mode = str(s.mode).lower()
        if s.mode not in MODES:
            raise ValueError(f"music.mode {s.mode!r}: use one of {', '.join(MODES)}")
        if s.mood not in MOODS:
            raise ValueError(f"music.mood {s.mood!r}: use one of {', '.join(MOODS)}")
        if s.palette not in PALETTES:
            raise ValueError(f"music.palette {s.palette!r}: use one of {', '.join(PALETTES)}")
        return s


def music_enabled(spec: dict) -> bool:
    m = spec.get("music")
    if m is None or m is False:
        return False
    if isinstance(m, dict):
        return bool(m.get("enabled", True))
    return bool(m)


def seed_for(*parts) -> int:
    """A stable seed from any values (zlib.crc32: the same in every process, unlike hash())."""
    return zlib.crc32("|".join(str(p) for p in parts).encode()) & 0x7FFFFFFF


# ---------------------------------------------------------------- the timeline of a video

@dataclass
class SceneLog:
    name: str
    offset: float
    duration: float
    log: dict


def load_timeline(items: list[tuple[str, float, Path]]) -> list[SceneLog]:
    """[(scene name, offset in the video, events.json path)] -> SceneLogs (missing logs raise)."""
    out = []
    for name, offset, path in items:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"no event log for {name}: {path} (render the scene with the current "
                                    f"toolkit: python -m explainer.build <project> --only {name})")
        log = json.loads(path.read_text())
        out.append(SceneLog(name, float(offset), float(log.get("duration") or 0.0), log))
    return out


# ---------------------------------------------------------------- cues

@dataclass
class Cue:
    t: float
    kind: str                 # cut, hit, title, reveal, count, emphasis, ...
    dur: float = 0.0
    x: float = 0.0            # screen x in [-1, 1]
    role: str = ""            # which palette role / instrument
    size: float = 0.0
    n: int = 1
    times: list = field(default_factory=list)
    prio: int = 1             # 3 structure, 2 counts and explicit marks, 1 ordinary reveals
    data: dict = field(default_factory=dict)
    scene: str = ""


def _area(a: dict) -> float:
    return max(a.get("w", 0.0), 0.05) * max(a.get("h", 0.0), 0.05)


def _screen_x(x: float, cam) -> float:
    if cam:
        cx, _, w = cam
        return float(np.clip((x - cx) / (w / 2), -1, 1))
    return float(np.clip(x / 7.1, -1, 1))


SMALL_SHAPES = {"Circle", "Dot", "Square", "Line", "Cross", "Star", "Triangle", "RegularPolygon", "Polygon",
                "Rectangle", "RoundedRectangle", "Annulus", "Arc", "Ellipse", "DashedLine", "SmallDot"}
TEXTS = {"Text", "MarkupText", "MathTex", "Tex", "Paragraph", "SingleStringMathTex", "Integer", "DecimalNumber",
         "Code"}


def derive_cues(scenes: list[SceneLog], settings: Settings) -> tuple[list[Cue], dict]:
    """Turn every scene's events into musical cues on the video's timeline. Also returns context:
    the activity curve, speech spans (narrated videos), structure points and the grid."""
    sounds = settings.sounds
    cues: list[Cue] = []
    speech: list[tuple[float, float]] = []
    particles: list[tuple[float, float, float]] = []          # (start, end, strength)
    plays = []
    grid = None
    total = 0.0
    for si, sc in enumerate(scenes):
        o = sc.offset
        total = max(total, o + sc.duration)
        g = sc.log.get("grid")
        if g and grid is None:
            grid = Grid(float(settings.bpm or g.get("bpm", 100)), int(g.get("beats_per_bar", 4)))
        if si > 0:
            cues.append(Cue(o, "cut", prio=3, scene=sc.name, data={"index": si}))
        scene_end = o + sc.duration
        for ev in sc.log.get("events", []):
            t = o + float(ev.get("t", 0.0))
            dur = float(ev.get("dur") or 0.0)
            typ = ev.get("type")
            if typ == "voice":
                speech.append((t, t + dur))
            elif typ == "mark":
                kind = ev.get("kind", "")
                data = ev.get("data") or {}
                mobs = [m for m in ev.get("mobs") or [] if m]
                x = _screen_x(float(data.get("x", mobs[0]["x"] if mobs else 0.0)), None)
                if kind == "particles":
                    particles.append((t, scene_end, min(1.0, 0.3 + float(data.get("n", 1000)) / 6000)))
                    cues.append(Cue(t, "swell", dur=max(dur, 2.4), x=x, prio=1, scene=sc.name))
                elif kind == "count":
                    times = [o + float(v) for v in data.get("times") or []]
                    if not times and data.get("every"):
                        times = [t + i * float(data["every"]) for i in range(int(data.get("n", 1)))]
                    cues.append(Cue(t, "count", dur=dur, x=x, n=int(data.get("n", len(times) or 1)), times=times,
                                    role=str(data.get("sound") or ""), prio=2, data=data, scene=sc.name))
                elif kind in ("pad",):
                    continue
                else:
                    cues.append(Cue(t, kind, dur=dur, x=x, prio=3 if kind in ("hit", "title", "silence",
                                    "tape_stop", "cut", "section", "resolve", "end") else 2, data=data,
                                    role=str(data.get("sound") or ""), scene=sc.name))
            elif typ == "play":
                plays.append((t, dur, ev))
                tags = set(ev.get("tags") or [])
                cam = ev.get("cam")
                if "count" in tags:
                    continue                      # the count mark carries the per-item times
                cues += _play_cues(t, dur, ev, cam, sounds, sc.name, tags)
    if grid is None and settings.bpm:
        grid = Grid(float(settings.bpm))
    for spec_cue in settings.cues:                   # structure written in video.yaml (music.cues)
        t = video_time(spec_cue.get("at"), scenes, grid)
        kind = str(spec_cue.get("kind", "hit"))
        if t is None or kind in ("", "none"):
            continue
        dur = float(spec_cue.get("dur") or 0.0)
        if grid is not None and (spec_cue.get("bars") or spec_cue.get("beats")):
            dur = float(spec_cue.get("bars") or 0) * grid.bar + float(spec_cue.get("beats") or 0) * grid.beat
        data = {k: v for k, v in spec_cue.items() if k not in ("at", "kind", "dur", "bars", "beats")}
        cues.append(Cue(t, kind, dur=dur, prio=3, data=data, role=str(data.get("sound") or ""), scene="video.yaml"))
    cues.sort(key=lambda c: (c.t, -c.prio))
    act = activity(plays, particles, total)
    return cues, {"total": total, "speech": speech, "activity": act, "grid": grid, "plays": plays}


def _play_cues(t, dur, ev, cam, sounds, scene, tags) -> list[Cue]:
    out = []
    anims = ev.get("anims") or []
    long_lines = [a for a in anims if a.get("kind") == "reveal" and a.get("mob") in ("Line", "DashedLine")
                  and max(a.get("w", 0), a.get("h", 0)) > 2.4]
    if len(long_lines) >= 3:                                   # a board / a grid being drawn
        out.append(Cue(t, "grid", dur=dur, x=_screen_x(long_lines[0]["x"], cam), n=len(long_lines),
                       times=[t + float(a.get("at", 0)) for a in long_lines], prio=1, scene=scene))
    explicit = {k for k in tags if k in ("reveal", "emphasis", "hit", "title", "resolve", "cut", "section")}
    seen_text_write = False
    for a in anims:
        kind = a.get("kind")
        at = t + float(a.get("at", 0.0))
        end = t + float(a.get("end", dur))
        x = _screen_x(float(a.get("x", 0.0)), cam)
        snd = a.get("sound")
        mob = a.get("mob", "")
        area = _area(a)
        if kind == "count":
            if a.get("anim") == "CounterLand":
                lands = [at + (end - at) * float(u) for u in a.get("lands") or []]
                out.append(Cue(at, "land", dur=end - at, x=x, n=len(lands) or 6, times=lands, prio=2, scene=scene))
            else:
                out.append(Cue(at, "roll", dur=end - at, x=x, prio=2, scene=scene, data={
                    "rate": a.get("rate"), "from": a.get("from"), "to": a.get("to")}))
            continue
        if kind == "camera":
            w0, w1 = a.get("w0"), a.get("w")
            if w0 and w1 and abs(w1 - w0) > 0.1 * max(w0, w1):
                out.append(Cue(at, "zoom_in" if w1 < w0 else "zoom_out", dur=end - at, prio=1, scene=scene,
                               size=abs(math.log(w1 / w0))))
            continue
        if snd and snd in sounds and sounds[snd] in FX and kind in ("reveal", "clear", "emphasis", "morph"):
            out.append(Cue(at, "fx", dur=end - at, x=x, role=sounds[snd], prio=2, scene=scene))
            continue
        if kind == "reveal" or (kind == "morph" and snd):
            if snd:
                out.append(Cue(at, "mark", dur=end - at, x=x, role=snd, size=area, prio=2, scene=scene))
            elif mob == "ImageMobject":
                out.append(Cue(at, "light", dur=end - at, x=x, size=area, prio=1, scene=scene))
            elif mob in ("Line", "DashedLine") and max(a.get("w", 0), a.get("h", 0)) > 2.4:
                if len(long_lines) < 3:
                    out.append(Cue(at, "sweep", dur=end - at, x=x, size=area, prio=1, scene=scene))
            elif mob in ("Arrow", "Vector", "DoubleArrow", "CurvedArrow"):
                out.append(Cue(at, "arrow", dur=end - at, x=x, prio=1, scene=scene))
            elif mob in TEXTS or a.get("anim") == "Write":
                if area < 0.1:
                    out.append(Cue(at, "tick", x=x, prio=1, scene=scene))
                elif area >= 3 or (a.get("anim") == "Write" and not seen_text_write and area >= 0.8):
                    seen_text_write = True
                    out.append(Cue(at, "title_text", dur=end - at, x=x, size=area, prio=2, scene=scene))
                else:
                    out.append(Cue(at, "text", dur=end - at, x=x, size=area, prio=1, scene=scene))
            elif area < 1.2 and (mob in SMALL_SHAPES or a.get("n", 1) <= 3):
                out.append(Cue(at, "mark", dur=end - at, x=x, role="", size=area, prio=1, scene=scene))
            elif area >= 8:
                out.append(Cue(at, "big", dur=end - at, x=x, size=area, prio=1, scene=scene))
            else:
                out.append(Cue(at, "text", dur=end - at, x=x, size=area, prio=1, scene=scene))
        elif kind == "emphasis":
            out.append(Cue(at, "emphasis", dur=end - at, x=x, prio=1, scene=scene))
        elif kind == "clear" and area >= 8:
            out.append(Cue(at, "clear", dur=end - at, x=x, size=area, prio=1, scene=scene))
        elif kind == "move" and a.get("anim") in ("Rotate", "Rotating"):
            out.append(Cue(at, "rotate", dur=end - at, x=x, prio=1, scene=scene))
    if ev.get("linear") and dur >= 3 and ev.get("block") is None and not explicit and ev.get("n_leaves", 0) <= 3:
        out.append(Cue(t, "timer", dur=dur, prio=2, scene=scene))
    return out


def activity(plays, particles, total: float, step: float = 0.01) -> tuple[np.ndarray, np.ndarray]:
    """How much is moving on screen (0..~1.5), sampled every 10 ms: drives the pads' brightness."""
    tt = np.arange(0, total + 4, step)
    act = np.zeros_like(tt)
    for t, dur, ev in plays:
        anims = ev.get("anims") or []
        if ev.get("linear"):
            w = 0.3
        else:
            w = min(1.0, 0.25 + 0.12 * len(anims) + 0.03 * sum(min(_area(a), 10) for a in anims))
        if any(a.get("kind") == "camera" for a in anims):
            w += 0.4
        act[(tt >= t) & (tt < t + max(dur, 0.05))] += w
    for a, b, s in particles:
        act[(tt >= a) & (tt < b)] += 0.35 * s
    k = np.hanning(121)
    act = np.convolve(act, k / k.sum(), mode="same")
    return tt, act


# ---------------------------------------------------------------- harmony

@dataclass
class Key:
    tonic: int
    mode: str

    @property
    def scale(self) -> list[int]:
        return MODES[self.mode]

    def degree_pcs(self, degree: int, sus: bool = False, notes: int = 5) -> tuple[int, list[int]]:
        """Pitch classes of the diatonic chord on a scale degree (1-based): root, 3rd (or 4th), 5th,
        7th, 9th stacked inside the mode, so each mode gets its own colours (lydian: IVmaj9#11 ...)."""
        sc = self.scale
        i = degree - 1
        steps = [0, 3 if sus else 2, 4, 6, 8][:notes]
        pcs = [(self.tonic + sc[(i + s) % 7] + 12 * ((i + s) // 7)) % 12 for s in steps]
        return pcs[0], pcs


def parse_key(name: str, mode: str) -> Key:
    n = str(name).strip().upper().replace("♯", "#").replace("♭", "B")
    if n not in NOTE:
        raise ValueError(f"music.key {name!r}: use a note name like D, F#, Bb")
    return Key(NOTE[n], mode.lower())


@dataclass
class Chord:
    t: float
    key: Key
    degree: int
    sus: bool = False
    tag: str = ""
    custom: tuple | None = None       # (root pc, pcs, name) of a chord given by name (video.yaml)
    named: bool = False               # named in video.yaml: kept as written

    @property
    def name(self) -> str:
        if self.custom:
            return self.custom[2]
        roman = ["I", "II", "III", "IV", "V", "VI", "VII"][self.degree - 1]
        return f"{roman}{'sus' if self.sus else ''}"

    def pcs(self) -> tuple[int, list[int]]:
        if self.custom:
            return self.custom[0], list(self.custom[1])
        return self.key.degree_pcs(self.degree, self.sus)


_ROMANS = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7}


def parse_chord(spec: str, key: Key, t: float, tag: str) -> Chord:
    """A chord named in video.yaml: a scale degree "vi", "IV", "Vsus" (diatonic to the mode, so its
    colour follows the key), "I5" / "fifth" (an open fifth, no third: neither major nor minor), or a
    borrowed degree "bVI" / "bVII" / "#iv" (a major-7 #11 chord on that root; lower case: minor 9)."""
    s0 = str(spec).strip()
    s = s0.replace("♭", "b").replace("♯", "#")
    if s.lower() in ("fifth", "5", "open"):
        s = "I5"
    acc = 0
    if s[:1] in ("b", "#") and s[1:2].upper() in "IV":
        acc, s = (-1 if s[0] == "b" else 1), s[1:]
    i = 0
    while i < len(s) and s[i].upper() in "IV":
        i += 1
    roman, rest = s[:i], s[i:].lower()
    deg = _ROMANS.get(roman.upper())
    if deg is None:
        raise ValueError(f"music cue chord {spec!r}: use a scale degree like vi, IV, Vsus, bVI or I5")
    sus = "sus" in rest
    root = (key.tonic + key.scale[deg - 1] + acc) % 12
    if rest.startswith("5") or rest == "fifth":
        return Chord(t, key, deg, tag=tag, custom=(root, sorted({root, (root + 7) % 12}), s0))
    if acc:
        ivs = [0, 3, 7, 10, 14] if roman.islower() else [0, 4, 7, 11, 18]
        return Chord(t, key, deg, tag=tag, custom=(root, sorted({(root + i) % 12 for i in ivs}), s0))
    return Chord(t, key, deg, sus=sus, tag=tag)


def chord_tones(ch: Chord, lo: int, hi: int) -> list[int]:
    _, pcs = ch.pcs()
    return [m for m in range(lo, hi + 1) if m % 12 in pcs]


def voice_chord(ch: Chord, prev, lo: int = 52, hi: int = 76, n: int = 4):
    """Upper-structure voicing (n notes in [lo, hi]) closest to the previous voicing, and a bass."""
    root, pcs = ch.pcs()
    cands = [m for m in range(lo, hi + 1) if m % 12 in pcs]
    best, best_cost = None, 1e9
    for combo in combinations(cands, n):
        if len({c % 12 for c in combo}) < min(n, len(set(pcs))):
            continue
        if combo[-1] - combo[0] > 19:
            continue
        cost = abs(float(np.mean(combo)) - 64) if prev is None else float(sum(abs(a - b) for a, b in zip(combo, prev)))
        if combo[1] - combo[0] <= 1:
            cost += 6
        if root in [c % 12 for c in combo[:1]]:
            cost += 0.5                       # rootless upper voicings sound more open
        if cost < best_cost:
            best, best_cost = combo, cost
    if best is None:
        best = tuple(cands[:n])
    bass = 36 + ((root - 36) % 12)
    if bass > 43:
        bass -= 12
    return list(best), bass


def video_time(at, scenes: list[SceneLog], grid: Grid | None) -> float | None:
    """A position on the stitched video's timeline, as video.yaml writes it:
        "10.1"   bar 10, beat 1, counted from 1 as musicians count (bar n starts at (n - 1) bars);
                 "12.3+" is the eighth note after bar 12 beat 3
        12       bar 12 (from 1)
        "9:0"    bar and beat counted from 0 (the notation scenes and captions.yaml use)
        "123.4s" seconds;  "s05_turn" where that scene starts"""
    if at is None:
        return None
    if isinstance(at, (int, float)) and not isinstance(at, bool):
        at = str(at) if isinstance(at, float) else int(at)
    if isinstance(at, int):
        return None if grid is None else (at - 1) * grid.bar
    a = str(at).strip()
    if a.endswith("s") and a[:-1].replace(".", "", 1).isdigit():
        return float(a[:-1])
    for sc in scenes:
        if a in (sc.name, sc.log.get("scene"), sc.log.get("scene_file")):
            return sc.offset
    if grid is None:
        return None
    if ":" in a:
        return grid.time(a)
    plus = a.endswith("+")
    a = a.rstrip("+")
    bar, _, beat = a.partition(".")
    try:
        t = (int(bar) - 1) * grid.bar + (float(beat or 1) - 1) * grid.beat
    except ValueError:
        return None
    return t + (grid.beat / 2 if plus else 0.0)


def key_at(t: float, settings: Settings, scenes: list[SceneLog], grid: Grid | None) -> Key:
    k = parse_key(settings.key, settings.mode)
    for act in settings.acts:
        start = video_time(act.get("at"), scenes, grid)
        if start is not None and t >= start - 1e-6:
            k = parse_key(act.get("key", settings.key), act.get("mode", k.mode))
    return k


def plan_harmony(cues: list[Cue], ctx: dict, settings: Settings, scenes: list[SceneLog],
                 every_bars: int = 2, every_s: float = 7.2) -> list[Chord]:
    """Where the chords change and to what. Structure points (cuts, hits, the title, resolutions) start
    phrases; inside a phrase the harmony moves every `every_bars` bars on the bar lines (shorts), or
    about every `every_s` seconds at the nearest reveal (narrated videos, free time). The tonic opens
    the video, is withheld while the question stands (a cycle of other degrees), is prepared by a
    suspended dominant and arrives on "title" / "resolve" and at the end."""
    total, grid = ctx["total"], ctx["grid"]
    rank = {"open": 9, "title": 5, "resolve": 5, "hit": 4, "cut": 3, "section": 3, "end": 2, "": 0}
    structure = sorted((grid.snap(c.t, "beat", "nearest") if grid is not None else c.t, c.kind)
                       for c in cues if c.kind in ("cut", "section", "hit", "title", "resolve"))
    named = {}                                       # chords that video.yaml names at a cue
    for c in cues:
        if c.data.get("chord") and c.kind in ("cut", "section", "hit", "title", "resolve"):
            named[round(grid.snap(c.t, "beat", "nearest") if grid is not None else c.t, 3)] = c.data["chord"]
    gap = (grid.bar * 0.99) if grid is not None else 2.0
    points: list[tuple[float, str]] = [(0.0, "open")]
    for t, tag in structure:
        if t - points[-1][0] < gap:
            if points[-1][1] != "open" and rank[tag] > rank[points[-1][1]]:
                points[-1] = (t, tag)
            continue
        points.append((t, tag))
    reveals = [c.t for c in cues if c.kind in ("title_text", "big", "text", "grid", "mark", "count", "land")]
    phrased: list[tuple[float, str]] = []
    for i, (t, tag) in enumerate(points):
        phrased.append((t, tag))
        t_end = points[i + 1][0] if i + 1 < len(points) else total
        if grid is not None:                             # on bar lines, even after an off-bar hit
            u = grid.snap(t + every_bars * grid.bar, "bar", "down")
            if u - t < grid.bar * 0.99:
                u += grid.bar
            while u < t_end - grid.bar * 0.99:
                phrased.append((u, ""))
                u += every_bars * grid.bar
        else:
            u = t + every_s
            while u < t_end - 2.0:
                near = [r for r in reveals if abs(r - u) <= 2.0 and r - phrased[-1][0] >= 2.0 and t_end - r >= 2.0]
                v = min(near, key=lambda r: abs(r - u)) if near else u
                phrased.append((v, ""))
                u = v + every_s
    chords: list[Chord] = []
    idx, last = 0, None
    for i, (t, tag) in enumerate(phrased):
        key = key_at(t, settings, scenes, grid)
        cyc = CYCLE_BRIGHT if key.mode in BRIGHT else CYCLE_DARK
        nxt_tag = phrased[i + 1][1] if i + 1 < len(phrased) else "end"
        if i + 1 < len(phrased) and round(phrased[i + 1][0], 3) in named:
            nxt_tag = "named"                         # no automatic dominant before a named chord
        room = (2 * grid.bar) if grid is not None else 4.0
        last_point = i + 1 == len(phrased)
        if round(t, 3) in named:
            ch = parse_chord(named[round(t, 3)], key, t, tag)
            ch.named = True
        elif tag in ("open", "title", "resolve"):
            ch = Chord(t, key, 1, tag=tag)
        elif last_point and total - t < room:
            ch = Chord(t, key, 1, tag="end")                   # no room for a cadence: end on the tonic
        elif nxt_tag in ("title", "resolve") or last_point:
            ch = Chord(t, key, 5, sus=True, tag="dominant")    # the dominant pedal before the tonic
        else:
            d = cyc[idx % len(cyc)]
            if d == last:
                idx += 1
                d = cyc[idx % len(cyc)]
            idx += 1
            ch = Chord(t, key, d, tag=tag)
        chords.append(ch)
        last = ch.degree
    if chords and chords[-1].degree != 1:
        tail = grid.snap(total - grid.bar, "bar", "nearest") if grid is not None else total - 2.0
        tail = max(tail, chords[-1].t + ((grid.bar if grid is not None else 2.0)))
        if tail < total - 0.3:
            chords.append(Chord(tail, key_at(tail, settings, scenes, grid), 1, tag="end"))
        elif not chords[-1].named:
            chords[-1] = Chord(chords[-1].t, chords[-1].key, 1, tag="end")
    return chords


def chord_at(chords: list[Chord], t: float) -> Chord:
    cur = chords[0]
    for c in chords:
        if c.t <= t + 1e-6:
            cur = c
        else:
            break
    return cur


# ---------------------------------------------------------------- the score

@dataclass
class Score:
    notes: list = field(default_factory=list)      # {t, dur, m, vel, inst, pan}
    fx: list = field(default_factory=list)         # {t, kind, gain, dur, pan, pitch}
    chords: list = field(default_factory=list)
    silences: list = field(default_factory=list)   # [start, end, kind]
    end: float = 0.0
    grid: dict | None = None
    key: str = ""

    def note(self, t, dur, m, vel, inst, pan=0.0):
        self.notes.append(dict(t=round(float(t), 4), dur=round(float(dur), 4), m=int(m), vel=round(float(vel), 4),
                               inst=inst, pan=round(float(np.clip(pan, -0.85, 0.85)), 3)))

    def add_fx(self, t, kind, gain, **kw):
        d = dict(t=round(float(t), 4), kind=kind, gain=round(float(gain), 4))
        d.update({k: (round(float(v), 4) if isinstance(v, (int, float, np.floating)) else v) for k, v in kw.items()})
        self.fx.append(d)

    def as_dict(self) -> dict:
        return {"key": self.key, "grid": self.grid, "end": self.end,
                "chords": [[round(c.t, 4), c.name, c.tag, sorted(c.pcs()[1])] for c in self.chords],
                "silences": self.silences, "notes": self.notes, "fx": self.fx}


def _in(spans, t, pad=0.0):
    return any(a - pad <= t <= b + pad for a, b in spans)


def thin(cues: list[Cue], density: float, speech=()) -> list[Cue]:
    """At most `density` ordinary accents per second (counts and structure always pass); under
    speech, ordinary accents need 0.5 s of room."""
    out, recent = [], []
    for c in cues:
        if c.prio >= 2:
            out.append(c)
            continue
        recent = [r for r in recent if c.t - r < 1.0]
        limit = density if not _in(speech, c.t) else max(1.0, density / 2)
        if len(recent) >= limit:
            continue
        recent.append(c.t)
        out.append(c)
    return out


def build_score(cues: list[Cue], ctx: dict, settings: Settings, scenes: list[SceneLog]) -> Score:
    total, grid, speech = ctx["total"], ctx["grid"], ctx["speech"]
    pal = PALETTES[settings.palette]
    mood = MOODS[settings.mood]
    narrated = bool(speech)
    sc = Score(end=total, grid=None if grid is None else {"bpm": grid.bpm, "beats_per_bar": grid.beats_per_bar},
               key=f"{settings.key} {settings.mode}")
    cues = thin(cues, settings.density, speech)
    chords = plan_harmony(cues, ctx, settings, scenes)
    sc.chords = chords

    # --- silences and tape stops (the music is cut there; a hit brings it back)
    for c in cues:
        if c.kind == "silence":
            d = c.dur or (grid.bar if grid else 2.0)
            sc.silences.append([round(c.t, 4), round(c.t + d, 4), "silence"])
            if c.data.get("hit", True):
                sc.add_fx(c.t + d, "boom", 0.85)
                sc.add_fx(c.t + d, "shimmer", 0.22, dur=3.0)
        elif c.kind == "tape_stop":
            d = c.dur or (grid.bar if grid else 2.0)
            nxt = [x.t for x in cues if x.t >= c.t + d - 0.02 and x.kind in ("hit", "title", "cut", "section",
                                                                             "resolve")]
            until = float(c.data.get("until", nxt[0] if nxt else c.t + d + (grid.bar if grid else 2.0)))
            sc.silences.append([round(c.t, 4), round(c.t + d, 4), "tape_stop"])
            if until > c.t + d + 0.02:
                sc.silences.append([round(c.t + d, 4), round(until, 4), "silence"])
    quiet = [(a, b) for a, b, _ in sc.silences]

    # --- pads and bass, one voicing per chord (pads lead the change a little, so it is heard on time)
    prev = None
    for i, ch in enumerate(chords):
        t_next = chords[i + 1].t if i + 1 < len(chords) else total + 2.0
        voicing, bass = voice_chord(ch, prev, *((52, 76) if narrated else (55, 79)))
        prev = voicing
        hit = ch.tag in ("title", "resolve", "hit", "cut")
        start = ch.t - (0.03 if hit else 0.15)
        for m in voicing:
            sc.note(start, t_next - start, m, 0.55, "pad", (m - 64) / 30)
        if not narrated and mood["air"]:                 # an octave-up shimmer of the top voices
            for m in voicing[-2:]:
                sc.note(start, t_next - start, m + 12, 0.55 * mood["air"], "pad", (m - 58) / 30)
        if not narrated and mood["tone"] != "soft":
            for nn in sc.notes[-(len(voicing) + (2 if mood["air"] else 0)):]:
                nn["tone"] = mood["tone"]
        sc.note(start, t_next - start, bass, 0.62, "bass")
        if ch.tag in ("title", "resolve"):
            sc.note(ch.t, t_next - ch.t, bass - 12, 0.45, "bass")

    # --- structure: cuts, hits, risers
    riser_ends = []
    for c in cues:
        if c.kind in ("cut", "section"):
            cut_fx = _instrument("cut", settings, "thump") if "cut" in settings.sounds else "thump"
            if cut_fx in FX:
                sc.add_fx(c.t, cut_fx, (0.45 if narrated else 0.55) * (0.8 if cut_fx == "boom" else 1.0))
            riser_ends.append((c.t, 1))
        elif c.kind in ("hit", "title"):
            sc.add_fx(c.t, "boom", 0.95 if c.kind == "title" else 0.8)
            sc.add_fx(c.t, "shimmer", 0.25, dur=3.5)
            riser_ends.append((c.t, 2))
            if c.kind == "title":
                ch = chord_at(chords, c.t + 0.01)
                tones = chord_tones(ch, 74, 93)
                for j in range(min(6, len(tones))):
                    sc.note(c.t + 0.04 + j * 0.09, 3.0, tones[j], 0.42, pal["title"], -0.5 + 0.2 * j)
        elif c.kind == "riser":
            sc.add_fx(c.t, "riser", 0.34, dur=max(0.6, c.dur or (grid.bar if grid else 2.4)))
        elif c.kind == "resolve":
            sc.add_fx(c.t, "shimmer", 0.3, dur=4.0)
            ch = chord_at(chords, c.t + 0.01)
            for j, m in enumerate(chord_tones(ch, 74, 93)[:5]):
                sc.note(c.t + j * 0.12, 3.2, m, 0.4, "bell", -0.4 + 0.2 * j)
        elif c.kind == "end":
            ch = chord_at(chords, c.t + 0.01)
            for j, m in enumerate(chord_tones(ch, 74, 90)[:4]):
                sc.note(c.t + 0.05 + j * 0.15, 3.5, m, 0.3, "bell", -0.3 + 0.2 * j)
    explicit_risers = [c.t + (c.dur or 0) for c in cues if c.kind == "riser"]
    last_riser = -1e9
    for t_end, bars in sorted(riser_ends):
        if any(abs(t_end - e) < 0.3 for e in explicit_risers) or t_end < 1.0:
            continue
        length = (grid.bar if grid else 2.4) * bars
        length = min(length, t_end - 0.2)
        if t_end - length < last_riser + 0.5 or _in(quiet, t_end - length * 0.5):
            continue
        gain = (0.26 if bars == 1 else 0.36) * (0.6 if narrated else 1.0)
        sc.add_fx(t_end - length, "riser", gain, dur=length)
        last_riser = t_end

    # --- one sound per visual event
    run_last, run_idx = {}, {}
    for c in cues:
        if _in(quiet, c.t, 0.02):
            continue
        ch = chord_at(chords, c.t + 0.02)
        pan = c.x * 0.8
        k = c.kind
        if k == "mark":
            role = c.role or ""
            inst = _instrument(role, settings, pal["mark"])
            if inst in FX:
                sc.add_fx(c.t, inst, 0.3, dur=max(0.3, c.dur), pan=pan)
                continue
            key = role.split("@", 1)[0] or "mark"
            idx = run_idx.get(key, 0) if c.t - run_last.get(key, -9) < 1.3 else 0
            run_last[key], run_idx[key] = c.t, idx + 1
            m = tag_pitch(role)
            if m is None:                                  # climb through the chord within a run
                tones = chord_tones(ch, 69, 93)
                m = tones[min(idx, len(tones) - 1)]
            sc.note(c.t + 0.01, 1.8, m, 0.5 if inst == "bell" else 0.55, inst, pan)
        elif k == "count":
            _count_notes(sc, c, ch, settings, pal)
        elif k == "land":
            tones = chord_tones(ch, 74, 96)
            for j, tl in enumerate(c.times or [c.t + c.dur]):
                sc.note(tl, 2.2, tones[j % len(tones)], 0.42, pal["count"], -0.5 + j / max(1, c.n - 1))
            sc.add_fx(c.t, "riser", 0.12, dur=max(0.5, c.dur * 0.8))
        elif k == "roll":
            _roll_ticks(sc, c, ch)
        elif k == "tick":
            sc.add_fx(c.t + 0.03, "tick", 0.24, pan=pan, pitch=3200)
        elif k == "grid":
            tones = chord_tones(ch, 50, 74)[::2][:max(1, c.n)]
            for j, m in enumerate(tones):
                tt = c.times[j] if j < len(c.times) else c.t + j * c.dur / max(1, c.n)
                sc.note(tt, 2.0, m, 0.38, pal["grid"], pan + (j - 1.5) * 0.08)
        elif k == "sweep":
            tones = chord_tones(ch, 74, 93)[:6]
            for j, m in enumerate(tones):
                sc.note(c.t + j * max(c.dur, 0.3) / len(tones), 1.4, m, 0.3 + 0.05 * j, pal["sweep"], pan)
            sc.add_fx(c.t, "whoosh_up", 0.10, dur=max(0.3, c.dur) + 0.2, pan=pan)
        elif k == "arrow":
            for j, m in enumerate(chord_tones(ch, 67, 86)[:3]):
                sc.note(c.t + j * 0.12, 1.2, m, 0.35, pal["arrow"], -0.3 + 0.3 * j)
        elif k == "title_text":
            tones = chord_tones(ch, 62, 88)
            for j in range(6):
                sc.note(c.t + j * max(c.dur, 0.6) / 6, 2.2, tones[min(len(tones) - 1, 1 + j)], 0.32, "glass", pan)
        elif k == "text":
            tones = chord_tones(ch, 64, 84)
            sc.note(c.t + 0.02, 2.0, tones[min(len(tones) - 1, 1 + int(min(c.size, 3)))], 0.42, pal["text"], pan)
        elif k == "big":
            tones = chord_tones(ch, 60, 84)
            for j, m in enumerate(tones[1:5]):
                sc.note(c.t + j * 0.06, 2.4, m, 0.3, pal["text"], -0.4 + 0.25 * j)
        elif k == "light":
            sc.add_fx(c.t, "shimmer", 0.16, dur=max(1.5, c.dur + 1.0), pan=pan)
        elif k == "swell":
            sc.add_fx(c.t, "swell", 0.12, dur=max(2.4, c.dur), pan=pan)
        elif k == "emphasis":
            for j, m in enumerate(chord_tones(ch, 81, 93)[-3:]):
                sc.note(c.t + j * 0.07, 2.0, m, 0.28, pal["emphasis"], pan + (j - 1) * 0.25)
        elif k == "rotate":
            for j, m in enumerate(chord_tones(ch, 69, 88)[:6]):
                sc.note(c.t + j * max(c.dur, 0.3) / 6, 1.5, m, 0.33, "pluck", 0.5 * math.sin(math.pi * j / 5))
        elif k == "clear":
            sc.add_fx(c.t, "whoosh_down", 0.09, dur=max(0.3, c.dur))
        elif k == "zoom_in":
            sc.add_fx(c.t, "whoosh_up", 0.12 * min(1.5, 0.5 + c.size), dur=max(0.4, c.dur))
        elif k == "zoom_out":
            sc.add_fx(c.t, "whoosh_down", 0.12 * min(1.5, 0.5 + c.size), dur=max(0.4, c.dur))
        elif k == "fx":
            sc.add_fx(c.t, c.role, 0.3 if c.role != "boom" else 0.7, dur=max(0.3, c.dur), pan=pan)
        elif k == "timer":
            _timer(sc, c, chords)
        elif k == "motif":
            _motif(sc, c, ch, pal)

    # --- the grid pulse (shorts): soft, follows activity, rests in silences and before the first cut
    if grid is not None and settings.pulse and not narrated:
        _pulse(sc, ctx, chords, quiet, mood, pal, settings)
    sc.notes.sort(key=lambda n: (n["t"], n["inst"], n["m"]))
    sc.fx.sort(key=lambda f: (f["t"], f["kind"]))
    return sc


def _instrument(role: str, settings: Settings, default: str) -> str:
    """The instrument (or effect) of a sound tag: video.yaml music.sounds / palette, an alias, a name."""
    if not role:
        return default
    role = role.split("@", 1)[0]
    inst = resolve_sound(settings.sounds.get(role, role))
    return inst if inst in INSTRUMENTS or inst in FX else default


def tag_pitch(role: str) -> int | None:
    """The fixed pitch of a sound tag "X@C#5" (MIDI number), or None: lets a scene give each object its
    own note, e.g. each square of a board, so a game is heard as a melody."""
    if "@" not in (role or ""):
        return None
    note = role.split("@", 1)[1].strip()
    import re
    m = re.fullmatch(r"([A-Ga-g])([#b♯♭]?)(-?\d)", note)
    if not m:
        return int(note) if note.isdigit() else None
    pc = NOTE[m.group(1).upper() + ({"♯": "#", "♭": "B", "b": "B"}.get(m.group(2), m.group(2)))]
    return 12 * (int(m.group(3)) + 1) + pc


def _count_notes(sc: Score, c: Cue, ch: Chord, settings: Settings, pal: dict) -> None:
    times = c.times or [c.t + i * (c.dur / max(1, c.n)) for i in range(c.n)]
    inst = _instrument(c.role or ("count" if "count" in settings.sounds else ""), settings, pal["count"])
    rise = c.data.get("pitch", "rise") != "flat"
    if inst in FX or len(times) > 24:              # many items: ticks that climb
        last = -1.0
        for i, tt in enumerate(times):
            if tt - last < 0.04:
                continue
            last = tt
            u = i / max(1, len(times) - 1)
            xs = c.data.get("xs") or []
            pan = _screen_x(float(xs[i]), None) * 0.8 if i < len(xs) else c.x * 0.6 + 0.3 * math.sin(i * 1.7)
            sc.add_fx(tt, "tick", 0.22 + 0.06 * u, pan=pan, pitch=(2000 + 2400 * u) if rise else 2600)
        return
    tones = chord_tones(ch, 67, 98)
    for i, tt in enumerate(times):
        m = tones[min(i, len(tones) - 1)] if rise else tones[len(tones) // 2]
        xs = c.data.get("xs") or []
        pan = _screen_x(float(xs[i]), None) * 0.8 if i < len(xs) else c.x * 0.6 + 0.35 * math.sin(i * 1.3)
        sc.note(tt + 0.005, 1.4, m, 0.36 + 0.12 * (i / max(1, len(times) - 1)), inst, pan)


def _roll_ticks(sc: Score, c: Cue, ch: Chord) -> None:
    """A rolling counter: ticks whose rate follows the counter's speed, then a note when it lands."""
    n = int(np.clip(c.dur * 10, 6, 48))
    from .events import _alpha_at
    us = np.linspace(0.04, 0.98, n)
    rate = _rate(c.data.get("rate"))
    ts = [c.t + c.dur * _alpha_at(rate, float(u)) for u in us]
    for i, tt in enumerate(ts):
        sc.add_fx(tt, "tick", 0.15 + 0.08 * i / n, pan=0.3 * math.sin(i), pitch=2200 + 1600 * i / n)
    tones = chord_tones(ch, 76, 93)
    sc.note(c.t + c.dur, 2.4, tones[0], 0.45, "bell", 0.0)


def _rate(name):
    from manim import rate_functions
    if not name:
        return None
    return getattr(rate_functions, str(name), None)


def _timer(sc: Score, c: Cue, chords) -> None:
    """A countdown (ponder card): a tick every half second, double time at the end, a riser."""
    t0, t1 = c.t, c.t + c.dur
    ticks = list(np.arange(t0, t1 - 2.0 + 1e-6, 0.5)) + list(np.arange(max(t0, t1 - 2.0) + 0.25, t1 - 0.01, 0.25))
    ch = chord_at(chords, t0 + 0.01)
    tones = chord_tones(Chord(ch.t, ch.key, 5, sus=True), 62, 98)
    for j, tk in enumerate(ticks):
        sc.add_fx(float(tk), "tick", 0.3 if j % 2 == 0 else 0.2, pan=0.25 if j % 2 else -0.25,
                  pitch=2400 if j % 2 == 0 else 1900)
        sc.note(float(tk), 0.9, tones[min(len(tones) - 1, j * len(tones) // (len(ticks) + 2))],
                0.18 + 0.22 * j / max(1, len(ticks)), "glass", (-1) ** j * 0.35)
    sc.add_fx(t0, "riser", 0.3, dur=t1 - t0)


def _motif(sc: Score, c: Cue, ch: Chord, pal: dict) -> None:
    """A short figure that always sounds the same for one name (a running object's signature)."""
    name = str(c.data.get("name", c.role or "motif"))
    rng = np.random.default_rng(seed_for("motif", name))
    tones = chord_tones(ch, 69, 93)
    shape = rng.permutation(len(tones))[:4]
    for j, i in enumerate(sorted(shape) if rng.random() < 0.5 else shape):
        sc.note(c.t + j * 0.15, 1.6, tones[int(i)], 0.38, pal["mark2"], c.x * 0.6)


def _pulse(sc: Score, ctx, chords, quiet, mood, pal, settings) -> None:
    grid, total = ctx["grid"], ctx["total"]
    tt, act = ctx["activity"]
    first = [t for t in ctx.get("titles", []) if t > 0] or [t for t in ctx.get("cuts", []) if t > 0]
    start = grid.snap(min(first) if first else grid.bar * 2, "bar", "up")
    t = start
    step = grid.beat / 2
    i = 0
    while t < total - grid.bar * 0.5:
        a = float(np.interp(t, tt, act))
        on_beat = i % 2 == 0
        if not _in(quiet, t, 0.05):
            if on_beat and a > 0.12:
                sc.add_fx(t, "tick", 0.07 + 0.05 * min(a, 1.2), pan=0.2 if (i // 2) % 2 else -0.2,
                          pitch=5200 if (i // 2) % 4 == 0 else 4300)
            if a > 0.45 * (1.0 / max(0.3, mood["pulse"])):
                ch = chord_at(chords, t + 0.01)
                tones = chord_tones(ch, 74, 91)
                if tones:
                    m = tones[(i * 3 + (i // 8)) % len(tones)]
                    sc.note(t + 0.003, 0.7, m, 0.12 + 0.08 * min(a, 1.2), pal["pulse"], 0.5 * math.sin(i * 0.9))
        t = grid.offset + (i + 1) * step + start
        i += 1


# ---------------------------------------------------------------- synthesis

def mtof(m):
    return 440.0 * 2 ** ((np.asarray(m, dtype=float) - 69) / 12)


def panlr(x, pan):
    th = (pan + 1) * np.pi / 4
    return np.stack([x * np.cos(th), x * np.sin(th)], 1)


_TABLE_N = 4096
_TABLES: dict = {}
PAD_SPECTRA = {   # partial amplitudes of the pad waveform: soft (under a voice), bright (music only)
    "soft": [(1, 1.0), (2, 0.2), (3, 0.12), (4, 0.05), (5, 0.04)],
    "bright": [(1, 1.0), (2, 0.42), (3, 0.28), (4, 0.18), (5, 0.12), (6, 0.08), (7, 0.05), (8, 0.035)],
}


def _pad_table(kind: str = "soft"):
    if kind not in _TABLES:
        ph = np.arange(_TABLE_N) / _TABLE_N * 2 * np.pi
        _TABLES[kind] = sum(a * np.sin(h * ph) for h, a in PAD_SPECTRA[kind])
    return _TABLES[kind]


def _osc(freq_hz: float, n: int, phase0: float, lfo=None, kind: str = "soft") -> np.ndarray:
    inc = freq_hz / SR * _TABLE_N
    ph = phase0 * _TABLE_N + inc * np.arange(n)
    if lfo is not None:
        ph = ph + lfo
    idx = np.mod(ph, _TABLE_N)
    i0 = idx.astype(np.int64)
    fr = idx - i0
    tab = _pad_table(kind)
    return tab[i0] * (1 - fr) + tab[(i0 + 1) % _TABLE_N] * fr


def syn_pad(n, rng):
    f = float(mtof(n["m"]))
    L = int((n["dur"] + 2.4) * SR)
    t = np.arange(L) / SR
    out = np.zeros((L, 2))
    for k, (cents, pan) in enumerate([(-7, -0.7), (0, 0.0), (7, 0.7)]):
        ff = f * 2 ** (cents / 1200)
        vib = 2.0 * np.sin(2 * np.pi * (0.11 + 0.05 * k) * t + rng.uniform(0, 6.28))   # slow drift, in table steps
        x = _osc(ff, L, rng.uniform(0, 1), vib, n.get("tone", "soft"))
        lfo = 1 + 0.08 * np.sin(2 * np.pi * (0.13 + 0.04 * k) * t + k)
        out += panlr(x * lfo, pan * 0.5 + n["pan"] * 0.3)
    sus = int(n["dur"] * SR)
    e = np.ones(L)
    na = int(0.9 * SR) if n["dur"] > 1.5 else int(0.05 * SR)
    na = min(na, L)
    e[:na] = np.sin(np.linspace(0, np.pi / 2, na)) ** 2
    e[sus:] *= np.exp(-np.linspace(0, 6, L - sus))
    return out * e[:, None] * n["vel"] * 0.06


def syn_bass(n, rng):
    f = float(mtof(n["m"]))
    L = int((n["dur"] + 1.5) * SR)
    t = np.arange(L) / SR
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) + 0.1 * np.sin(6 * np.pi * f * t)
    sus = int(n["dur"] * SR)
    e = np.ones(L)
    na = min(L, int(0.25 * SR))
    e[:na] = np.sin(np.linspace(0, np.pi / 2, na)) ** 2
    e[sus:] *= np.exp(-np.linspace(0, 5, L - sus))
    return panlr(x * e * n["vel"] * 0.085, 0)


def syn_bell(n, rng):
    """FM bell (carrier : modulator = 1 : 3.5), soft attack."""
    f = float(mtof(n["m"]))
    L = int(max(n["dur"], 1.0) * SR + 0.5 * SR)
    t = np.arange(L) / SR
    idx = 2.2 * np.exp(-t / 0.25) + 0.3
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * 3.5 * f * t))
    x += 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.4)
    e = np.exp(-t / (0.55 * (440 / f) ** 0.3 + 0.35)) * (1 - np.exp(-t / 0.004))
    return panlr(x * e * n["vel"] * 0.13, n["pan"])


def syn_glass(n, rng):
    """Glass / celesta: struck-bar modes 1, 2.756, 5.404, the upper ones decaying faster."""
    f = float(mtof(n["m"]))
    L = int(max(n["dur"], 1.0) * SR + 0.5 * SR)
    t = np.arange(L) / SR
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.9) +
         0.3 * np.sin(2 * np.pi * 2.756 * f * t) * np.exp(-t / 0.25) +
         0.1 * np.sin(2 * np.pi * 5.404 * f * t) * np.exp(-t / 0.08))
    x *= 1 - np.exp(-t / 0.003)
    return panlr(x * n["vel"] * 0.15, n["pan"])


def syn_pluck(n, rng):
    """A harp / kalimba pluck: decaying harmonic partials (the upper ones faster) and a short noise
    transient; exactly in tune (unlike a Karplus-Strong delay line)."""
    f = float(mtof(n["m"]))
    L = int(max(n["dur"], 1.2) * SR)
    t = np.arange(L) / SR
    x = np.zeros(L)
    for h in range(1, 9):
        if f * h > 12000:
            break
        tau = 1.6 / (h ** 0.9) * (220 / f) ** 0.35
        x += (0.9 ** h) / h * np.sin(2 * np.pi * f * h * t * (1 + 0.0004 * h * h) + rng.uniform(0, 6.28)) * np.exp(-t / tau)
    nz = rng.standard_normal(min(L, int(0.006 * SR)))
    x[:len(nz)] += 0.25 * nz * np.linspace(1, 0, len(nz))
    x *= 1 - np.exp(-t / 0.0015)
    return panlr(x * n["vel"] * 0.2, n["pan"])


def syn_wood(n, rng):
    """A soft marimba / wood bar: modes 1, 3.93, 9.2 with fast decays, a dry knock."""
    f = float(mtof(n["m"]))
    L = int(0.9 * SR)
    t = np.arange(L) / SR
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.28) + 0.25 * np.sin(2 * np.pi * 3.93 * f * t) * np.exp(-t / 0.06)
         + 0.08 * np.sin(2 * np.pi * 9.2 * f * t) * np.exp(-t / 0.02))
    x *= 1 - np.exp(-t / 0.0015)
    return panlr(x * n["vel"] * 0.17, n["pan"])


def syn_glass_rev(n, rng):
    """A glass note played backwards: it swells out of nothing and stops dead (ghost moves, undoing)."""
    y = syn_glass({**n, "dur": max(0.8, min(1.6, n["dur"]))}, rng)
    y = y[::-1].copy()
    nf = min(len(y), int(0.004 * SR))
    y[-nf:] *= np.linspace(1, 0, nf)[:, None]
    return y * 0.8


SYN = dict(pad=syn_pad, bass=syn_bass, bell=syn_bell, glass=syn_glass, pluck=syn_pluck, wood=syn_wood,
           glass_rev=syn_glass_rev)


def fx_sound(f, rng):
    k = f["kind"]
    g = f["gain"]
    pan = f.get("pan", 0.0) or 0.0
    if k == "boom":                       # a pitch-dropping sub hit (250 -> 45 Hz) with its 2nd harmonic
        L = int(2.6 * SR)
        t = np.arange(L) / SR
        fr = 45 + 205 * np.exp(-t / 0.075)
        ph = 2 * np.pi * np.cumsum(fr) / SR
        x = np.sin(ph) * np.exp(-t / 0.85) + 0.35 * np.sin(2 * ph) * np.exp(-t / 0.35)
        x *= 1 - np.exp(-t / 0.003)
        nz = signal.lfilter(*signal.butter(2, 380 / (SR / 2)), rng.standard_normal(L)) * np.exp(-t / 0.12) * 0.35
        return panlr((x + nz) * g * 0.5, 0)
    if k == "thump":
        L = int(1.2 * SR)
        t = np.arange(L) / SR
        fr = 52 + 60 * np.exp(-t / 0.05)
        x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.33) * (1 - np.exp(-t / 0.003))
        x += 0.25 * np.sin(4 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.15)
        return panlr(x * g * 0.42, 0)
    if k == "blip":                       # a soft sine pulse (a light pen's step)
        L = int(0.09 * SR)
        t = np.arange(L) / SR
        x = np.sin(2 * np.pi * f.get("pitch", 1320) * t) * np.exp(-t / 0.025) * (1 - np.exp(-t / 0.004))
        return panlr(x * g * 0.2, pan)
    if k == "tick":
        L = int(0.12 * SR)
        t = np.arange(L) / SR
        x = np.sin(2 * np.pi * f.get("pitch", 3000) * t) * np.exp(-t / 0.016)
        nz = signal.lfilter(*signal.butter(2, [1500 / (SR / 2), 7000 / (SR / 2)], "band"),
                            rng.standard_normal(L)) * np.exp(-t / 0.004)
        return panlr((x * 0.6 + nz * 0.5) * g * 0.25, pan)
    if k in ("riser", "whoosh_up", "whoosh_down", "whoosh_rev", "shimmer", "swell"):
        dur = max(0.2, float(f.get("dur", 1.0)))
        L = int((dur + 0.6) * SR)
        x = rng.standard_normal((L, 2))
        fr, tt, Z = signal.stft(x.T, fs=SR, nperseg=2048)
        u = np.clip(tt / dur, 0, 1)
        logf = np.log2(np.maximum(fr, 20))[:, None]
        if k == "riser":
            centre, width, amp = np.log2(250) + u * (np.log2(6000) - np.log2(250)), 1.2, u ** 2.2
        elif k == "whoosh_up":
            centre, width, amp = np.log2(700) + u * 2.2, 0.8, np.sin(np.pi * u) ** 2
        elif k == "whoosh_down":
            centre, width, amp = np.log2(1800) - u * 2.3, 0.8, np.sin(np.pi * np.minimum(u * 1.2, 1)) ** 2
        elif k == "whoosh_rev":             # a reversed swell: grows, then stops dead (an undo / erase)
            centre, width, amp = np.log2(1200) + u * 1.5, 0.9, np.where(u < 1, u ** 3, 0.0)
        elif k == "swell":
            centre, width, amp = np.full_like(u, np.log2(3200)), 1.4, np.sin(np.pi * u) ** 2
        else:                               # shimmer: a high airy band that decays
            centre, width, amp = np.full_like(u, np.log2(7000)), 0.8, np.exp(-tt / (dur / 3))
        G = np.exp(-0.5 * ((logf - centre[None, :]) / width) ** 2)
        Z = Z * G[None] * amp[None, None, :]
        _, y = signal.istft(Z, fs=SR, nperseg=2048)
        y = y.T[:L]
        y /= (np.sqrt(np.mean(y ** 2)) + 1e-9)
        tail = np.ones(len(y))
        nt = int(0.3 * SR)
        tail[-nt:] = np.linspace(1, 0, nt)
        y = y * tail[:, None]
        if pan:
            y = y * np.array([math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)]) * math.sqrt(2)
        return y * g * 0.05
    raise ValueError(k)


FX_BUS = dict(boom="hit", thump="hit", tick="acc_fx", blip="acc_fx", riser="fx", whoosh_up="acc_fx", whoosh_down="fx",
              whoosh_rev="acc_fx", swell="fx", shimmer="acc_fx")


def _add(buf, t, stereo):
    i = int(round(t * SR))
    if i < 0:
        stereo = stereo[-i:]
        i = 0
    j = min(len(buf), i + len(stereo))
    if j > i:
        buf[i:j] += stereo[: j - i].astype(buf.dtype)


def reverb_ir(rt60=2.8, predelay=0.025, seed=11, width=0.8):
    """A synthetic stereo hall: decaying filtered noise, the two channels partly correlated (`width`
    1 = independent) so the tail is wide but still sums well to mono on a phone speaker."""
    rng = np.random.default_rng(seed)
    L = int(rt60 * 1.1 * SR)
    t = np.arange(L) / SR
    ir = np.zeros((L + int(predelay * SR), 2))
    common = rng.standard_normal(L)
    for ch in range(2):
        nz = math.sqrt(1 - width ** 2) * common + width * rng.standard_normal(L)
        bright = signal.lfilter(*signal.butter(1, 6000 / (SR / 2)), nz) * np.exp(-6.9 * t / (rt60 * 0.45))
        dark = signal.lfilter(*signal.butter(1, 1800 / (SR / 2)), nz) * np.exp(-6.9 * t / rt60)
        ir[int(predelay * SR):, ch] = 0.5 * bright + dark
    ir /= np.sqrt(np.sum(ir ** 2) / 2)
    return ir


def tv_lowpass(x, cutoff_fn, block=1024):
    """2nd-order low-pass whose cutoff follows cutoff_fn(t) (one filter per block)."""
    y = np.zeros_like(x)
    zi = np.zeros((1, 2, x.shape[1]))
    for i in range(0, len(x), block):
        fc = float(np.clip(cutoff_fn((i + block / 2) / SR), 200, 16000))
        sos = signal.butter(2, fc / (SR / 2), output="sos")
        y[i:i + block], zi = signal.sosfilt(sos, x[i:i + block], axis=0, zi=zi)
    return y


def peaking(f0, gain_db, q):
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f0 / SR
    al = np.sin(w0) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w0), 1 - al * A]
    a = [1 + al / A, -2 * np.cos(w0), 1 - al / A]
    return np.array(b) / a[0], np.array(a) / a[0]


def high_shelf(f0, gain_db, s=0.7):
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f0 / SR
    al = np.sin(w0) / 2 * np.sqrt((A + 1 / A) * (1 / s - 1) + 2)
    cw = np.cos(w0)
    b = [A * ((A + 1) + (A - 1) * cw + 2 * np.sqrt(A) * al), -2 * A * ((A - 1) + (A + 1) * cw),
         A * ((A + 1) + (A - 1) * cw - 2 * np.sqrt(A) * al)]
    a = [(A + 1) - (A - 1) * cw + 2 * np.sqrt(A) * al, 2 * ((A - 1) - (A + 1) * cw),
         (A + 1) - (A - 1) * cw - 2 * np.sqrt(A) * al]
    return np.array(b) / a[0], np.array(a) / a[0]


def render(score: Score, ctx: dict, settings: Settings, length: float) -> tuple[np.ndarray, np.ndarray]:
    """Synthesize the score: (bed, accents), each (n, 2) float64 at 48 kHz, `length` seconds long."""
    L = int(round(length * SR))
    narrated = bool(ctx["speech"])
    mood = MOODS[settings.mood]
    buses = {b: np.zeros((L, 2), np.float64) for b in ("pad", "keys", "fx", "acc_fx", "low", "hit")}
    for i, n in enumerate(score.notes):
        rng = np.random.default_rng(seed_for(settings.seed, "note", i, n["inst"], n["m"], n["t"]))
        y = SYN[n["inst"]](n, rng)
        bus = "pad" if n["inst"] == "pad" else "low" if n["inst"] == "bass" else "keys"
        start = n["t"] - (len(y) / SR if n["inst"] == "glass_rev" else 0.0)   # a reversed note ends on the event
        _add(buses[bus], start, y)
    for i, f in enumerate(score.fx):
        rng = np.random.default_rng(seed_for(settings.seed, "fx", i, f["kind"], f["t"]))
        start = f["t"] - (float(f.get("dur", 0.3)) if f["kind"] == "whoosh_rev" else 0.0)   # it lands on the event
        _add(buses[FX_BUS[f["kind"]]], start, fx_sound(f, rng))
    tt, act = ctx["activity"]
    lo, hi = (700, 2300) if narrated else (mood["cut_lo"], mood["cut_hi"])
    risers = [(f["t"], f["t"] + f.get("dur", 0)) for f in score.fx if f["kind"] == "riser"]

    def cutoff(t):
        a = float(np.interp(t, tt, act))
        fc = lo + (hi - lo) * min(a, 1.0)
        for r0, r1 in risers:
            if r0 <= t <= r1 and r1 > r0:
                fc += 0.6 * (hi - lo) * ((t - r0) / (r1 - r0)) ** 2
        return fc
    buses["pad"] = tv_lowpass(buses["pad"], cutoff)
    buses["fx"] = signal.sosfilt(signal.butter(2, 7500 / (SR / 2), output="sos"), buses["fx"], axis=0)
    if narrated:      # a pocket for the voice
        b, a = peaking(2500, -4.0, 0.8)
        for k in ("pad", "keys"):
            buses[k] = signal.lfilter(b, a, buses[k], axis=0)
    elif mood["sparkle"]:
        b, a = high_shelf(3000, mood["sparkle"])
        buses["keys"] = signal.lfilter(b, a, buses["keys"], axis=0)
    ir = reverb_ir()
    rv = mood["reverb"]
    bed = np.zeros((L, 2))
    acc = np.zeros((L, 2))
    gain = {} if narrated else {"low": mood["bass"], "keys": mood["keys"], "acc_fx": mood["keys"]}
    for k, w, out in (("pad", rv, bed), ("fx", 0.3, bed), ("low", 0.06, bed), ("keys", rv + 0.12, acc),
                      ("acc_fx", 0.3, acc), ("hit", 0.1, acc)):
        x = buses.pop(k)
        if k in gain:
            x *= gain[k]
        out += x
        if np.any(x):
            out += signal.oaconvolve(x, ir, axes=0)[:L] * w
        del x
    hp = signal.butter(2, 32 / (SR / 2), "high", output="sos")
    bed, acc = (signal.sosfilt(hp, x, axis=0) for x in (bed, acc))
    bed, acc = (apply_silences(x, score.silences) for x in (bed, acc))
    fade = np.ones(L)
    nf = min(L, int(2.0 * SR))
    fade[L - nf:] = np.cos(np.linspace(0, np.pi / 2, nf)) ** 2
    nfi = min(L, int(0.02 * SR))
    fade[:nfi] *= np.linspace(0, 1, nfi)
    return bed * fade[:, None], acc * fade[:, None]


def apply_silences(x: np.ndarray, silences) -> np.ndarray:
    """Planned drop-outs (digital silence with 30 ms fades) and tape stops (the music slows to a stop
    and falls in pitch, as a tape does)."""
    y = x.copy()
    n = len(y)
    for a, b, kind in silences:
        i, j = int(round(a * SR)), int(round(b * SR))
        i, j = max(0, i), min(n, j)
        if j <= i:
            continue
        if kind == "tape_stop":
            L = j - i
            u = np.arange(L) / L
            rate = (1 - u) ** 1.5                    # playback speed: 1 -> 0
            pos = i + np.cumsum(rate)
            seg = np.stack([np.interp(pos, np.arange(n), x[:, c]) for c in range(x.shape[1])], 1)
            seg *= (1 - u ** 4)[:, None]
            y[i:j] = seg
        else:
            fo = min(int(0.03 * SR), (j - i) // 2)
            fi = min(int(0.005 * SR), (j - i) // 2)     # the return lands with the hit
            g = np.zeros(j - i)
            if fo:
                g[:fo] = np.linspace(1, 0, fo)
            if fi:
                g[len(g) - fi:] = np.linspace(0, 1, fi)
            y[i:j] *= g[:, None]
    return y


# ---------------------------------------------------------------- loudness, limiting, ducking

_KW = [([1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]),
       ([1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621])]


def lufs(x: np.ndarray) -> float:
    """ITU-R BS.1770-4 integrated loudness (400 ms blocks, 75 % overlap, absolute and relative gates)."""
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    y = x
    for b, a in _KW:
        y = signal.lfilter(b, a, y, axis=0)
    n, hop = int(0.4 * SR), int(0.1 * SR)
    if len(y) < n:
        return -70.0
    sq = np.cumsum(np.concatenate([np.zeros((1, y.shape[1])), y ** 2]), axis=0)
    starts = np.arange(0, len(y) - n + 1, hop)
    ms = ((sq[starts + n] - sq[starts]) / n).sum(axis=1)
    ld = -0.691 + 10 * np.log10(ms + 1e-12)
    keep = ld > -70
    if not keep.any():
        return -70.0
    rel = -0.691 + 10 * np.log10(ms[keep].mean()) - 10
    keep &= ld > rel
    return float(-0.691 + 10 * np.log10(ms[keep].mean()))


def true_peak_db(x: np.ndarray) -> float:
    """Peak of the 4x oversampled signal (an estimate of the true peak, dBTP)."""
    up = signal.resample_poly(np.asarray(x, dtype=float), 4, 1, axis=0)
    return float(20 * np.log10(np.max(np.abs(up)) + 1e-12))


def limit(x: np.ndarray, ceiling_db: float = -1.0, release: float = 0.12, look: float = 0.005) -> np.ndarray:
    """A look-ahead peak limiter: the gain each peak needs is held over a 5 ms window either side,
    smoothed (so the attack is not a step), released slowly (one-pole, `release` s), never above
    what the peak needs; then a safety clip at the ceiling."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    c = 10 ** (ceiling_db / 20)
    peak = np.max(np.abs(x), axis=1)
    if peak.max() <= c:
        return x
    need = np.minimum(1.0, c / np.maximum(peak, 1e-9))
    w = max(1, int(look * SR))
    g = minimum_filter1d(need, size=2 * w + 1, mode="nearest")
    g = uniform_filter1d(g, size=w, mode="nearest")
    a = math.exp(-1 / (release * SR))
    rel = signal.lfilter([1 - a], [1, -a], g - 1.0, zi=[g[0] - 1.0])[0] + 1.0
    g = np.minimum(g, rel)
    return np.clip(x * g[:, None], -c, c)


def master(x: np.ndarray, target_lufs: float = -14.0, ceiling_dbtp: float = -1.0) -> np.ndarray:
    """Music-only master: integrated loudness to the target, true peaks <= the ceiling."""
    y = x
    for _ in range(4):
        cur = lufs(y)
        if cur <= -69:
            return y
        y = y * 10 ** ((target_lufs - cur) / 20)
        y = limit(y, ceiling_dbtp - 0.3)
        if abs(lufs(y) - target_lufs) < 0.25 and true_peak_db(y) <= ceiling_dbtp + 0.05:
            break
    if true_peak_db(y) > ceiling_dbtp:
        y = y * 10 ** ((ceiling_dbtp - 0.05 - true_peak_db(y)) / 20)
    return y


def duck_curve(voice: np.ndarray, depth_db: float = 12.0, hold: float = 0.45, attack: float = 0.12,
               release: float = 0.6, look: float = 0.15) -> np.ndarray:
    """Per-sample gain (<= 1) that dips under speech: 150 ms look-ahead, 120 ms attack, 0.45 s hold so
    the bed does not pump between words, 600 ms release."""
    from scipy.ndimage import maximum_filter1d
    v = voice.mean(axis=1) if voice.ndim > 1 else voice
    hop = int(SR * 0.01)
    nfr = len(v) // hop + 1
    pad = np.zeros(nfr * hop)
    pad[:len(v)] = v
    rms = np.sqrt((pad.reshape(nfr, hop) ** 2).mean(axis=1) + 1e-12)
    db = 20 * np.log10(rms + 1e-9)
    active = db > (db.max() - 35)
    n_hold = int(hold / 0.01)
    act = maximum_filter1d(active.astype(float), size=n_hold + 1, origin=-(n_hold // 2)) > 0
    shift = int(look / 0.01)
    act = np.concatenate([act[shift:], np.zeros(shift, bool)])
    target = np.where(act, -depth_db, 0.0)
    g = np.zeros_like(target)
    cur = float(target[0])
    ka, kr = 1 - math.exp(-0.01 / attack), 1 - math.exp(-0.01 / release)
    for i, tg in enumerate(target):
        cur += (tg - cur) * (ka if tg < cur else kr)
        g[i] = cur
    tt = np.arange(len(v)) / SR
    return 10 ** (np.interp(tt, np.arange(len(g)) * 0.01, g) / 20)


def voice_active(voice: np.ndarray, floor_db: float = 35.0) -> np.ndarray:
    """Per-sample mask of where someone is speaking (10 ms frames within `floor_db` of the loudest)."""
    v = voice.mean(axis=1) if voice.ndim > 1 else voice
    hop = int(SR * 0.01)
    nfr = len(v) // hop + 1
    pad = np.zeros(nfr * hop)
    pad[:len(v)] = v
    db = 10 * np.log10((pad.reshape(nfr, hop) ** 2).mean(axis=1) + 1e-12)
    act = db > (db.max() - floor_db)
    return np.repeat(act, hop)[:len(v)]


def mix_under_voice(bed: np.ndarray, acc: np.ndarray, voice: np.ndarray, settings: Settings,
                    voice_lufs: float | None = None) -> tuple[np.ndarray, np.ndarray, dict]:
    """Narrated mix: the voice as it is (build ships it at -16 LUFS), the music ducked under it (bed
    `depth` dB, accents `accents` dB) and set `gap` LU under the voice where nobody speaks."""
    n = len(voice)
    bed, acc = _fit(bed, n), _fit(acc, n)
    if voice.ndim == 1:
        voice = np.stack([voice, voice], 1)
    v_l = lufs(voice) if voice_lufs is None else voice_lufs
    d = settings.duck
    depth, acc_depth = float(d.get("depth", 12.0)), float(d.get("accents", 7.0))
    under = float(d.get("under", 15.0))          # the music under speech, LU below the voice
    g = duck_curve(voice, depth)
    quiet = g > 0.95
    speech = voice_active(voice)
    music0 = bed + acc
    m_quiet = lufs(music0[quiet]) if quiet.sum() > SR else lufs(music0)
    k = 10 ** ((v_l - float(d.get("gap", 6.0)) - m_quiet) / 20)
    for _ in range(6):                           # duck deeper until the music sits `under` LU below speech
        acc_g = g ** (acc_depth / depth)
        music = k * (bed * g[:, None] + acc * acc_g[:, None])
        if speech.sum() <= SR:
            break
        excess = lufs(music[speech]) - (v_l - under)
        if excess <= 0.3:
            break
        depth, acc_depth = depth + excess, acc_depth + excess * acc_depth / depth
        g = duck_curve(voice, depth)
    mixed = limit(voice + music, -1.0)
    rep = {"voice_lufs": round(v_l, 2), "music_in_gaps_lufs": round(lufs(music[quiet]), 2) if quiet.sum() > SR else None,
           "music_under_speech_lufs": round(lufs(music[speech]), 2) if speech.sum() > SR else None,
           "mix_lufs": round(lufs(mixed), 2), "mix_true_peak_dbtp": round(true_peak_db(mixed), 2)}
    return mixed, music, rep


def _fit(x, n):
    if len(x) >= n:
        return x[:n]
    return np.concatenate([x, np.zeros((n - len(x), x.shape[1]))])


def lr_correlation(x: np.ndarray) -> float:
    w = int(0.5 * SR)
    cs = []
    for i in range(0, len(x) - w, w):
        a, b = x[i:i + w, 0], x[i:i + w, 1]
        if np.std(a) > 1e-5 and np.std(b) > 1e-5:
            cs.append(float(np.corrcoef(a, b)[0, 1]))
    return float(np.median(cs)) if cs else 1.0


# ---------------------------------------------------------------- MIDI (for inspection in any DAW)

GM = dict(pad=89, bass=32, bell=8, glass=11, pluck=46)


def write_midi(score: Score, path: Path, bpm: float = 120.0) -> None:
    """A minimal type-1 Standard MIDI File: one track per instrument (times in seconds at `bpm`)."""
    tpq = 480
    us_per_q = int(60_000_000 / bpm)

    def vlq(n):
        out = [n & 0x7F]
        n >>= 7
        while n:
            out.insert(0, (n & 0x7F) | 0x80)
            n >>= 7
        return bytes(out)

    def ticks(t):
        return int(round(max(0.0, t) * bpm / 60 * tpq))

    tracks = [b"\x00\xff\x51\x03" + us_per_q.to_bytes(3, "big") + b"\x00\xff\x2f\x00"]
    for ch, inst in enumerate(INSTRUMENTS):
        evs = []
        for n in score.notes:
            if n["inst"] != inst:
                continue
            vel = int(np.clip(30 + 90 * n["vel"], 1, 127))
            evs.append((ticks(n["t"]), 1, bytes([0x90 | ch, n["m"], vel])))
            evs.append((ticks(n["t"] + n["dur"]), 0, bytes([0x80 | ch, n["m"], 0])))
        if not evs:
            continue
        evs.sort(key=lambda e: (e[0], e[1]))
        body, last = bytearray(b"\x00" + bytes([0xC0 | ch, GM[inst]])), 0
        for tk, _, msg in evs:
            body += vlq(tk - last) + msg
            last = tk
        body += b"\x00\xff\x2f\x00"
        tracks.append(bytes(body))
    data = b"MThd" + (6).to_bytes(4, "big") + (1).to_bytes(2, "big") + len(tracks).to_bytes(2, "big") + \
        tpq.to_bytes(2, "big")
    for tr in tracks:
        data += b"MTrk" + len(tr).to_bytes(4, "big") + tr
    Path(path).write_bytes(data)


# ---------------------------------------------------------------- the whole pipeline

def compose(scenes: list[SceneLog], settings: Settings, length: float | None = None):
    """Event logs -> (score, cues, ctx, bed, accents). Deterministic."""
    cues, ctx = derive_cues(scenes, settings)
    ctx["cuts"] = [c.t for c in cues if c.kind == "cut"]
    ctx["titles"] = [c.t for c in cues if c.kind == "title"]
    score = build_score(cues, ctx, settings, scenes)
    total = ctx["total"] if length is None else length
    bed, acc = render(score, ctx, settings, total)
    return score, cues, ctx, bed, acc


def sync_share(cues: list[Cue], score: Score, tol: float = 0.03) -> float:
    """Share of visual cues (not structure) that have a note or effect starting within `tol` seconds."""
    onsets = np.array(sorted([n["t"] for n in score.notes if n["inst"] not in ("pad", "bass")] +
                             [f["t"] for f in score.fx]))
    targets = [c.t for c in cues if c.kind not in ("cut", "section", "swell", "timer", "silence", "tape_stop",
                                                   "riser", "end", "pad")]
    if not len(targets) or not len(onsets):
        return 0.0
    hits = 0
    for t in targets:
        i = np.searchsorted(onsets, t)
        near = [abs(onsets[j] - t) for j in (i - 1, i) if 0 <= j < len(onsets)]
        hits += bool(near and min(near) <= tol)
    return hits / len(targets)


def write_outputs(out_dir: Path, score: Score, cues: list[Cue], ctx: dict, bed, acc, music, report: dict) -> dict:
    import soundfile as sf
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "score.json").write_text(json.dumps(score.as_dict(), indent=1))
    (out_dir / "cues.json").write_text(json.dumps([{k: v for k, v in c.__dict__.items() if v not in ([], {}, "")}
                                                   for c in cues], indent=1, default=float))
    write_midi(score, out_dir / "score.mid", bpm=(score.grid or {}).get("bpm", 120.0))
    sf.write(out_dir / "bed.wav", bed.astype(np.float32), SR)
    sf.write(out_dir / "accents.wav", acc.astype(np.float32), SR)
    sf.write(out_dir / "music.wav", music.astype(np.float32), SR)
    (out_dir / "report.json").write_text(json.dumps(report, indent=1))
    return {"score": out_dir / "score.json", "music": out_dir / "music.wav", "bed": out_dir / "bed.wav",
            "accents": out_dir / "accents.wav", "report": out_dir / "report.json"}


def music_only(bed, acc, settings: Settings) -> tuple[np.ndarray, dict]:
    m = master(bed + acc, float(settings.lufs), float(settings.peak))
    return m, {"lufs": round(lufs(m), 2), "true_peak_dbtp": round(true_peak_db(m), 2),
               "lr_correlation": round(lr_correlation(m), 2)}


def project_scenes(project: Path, quality: str = "h", durations: dict | None = None) -> list[tuple[str, float, Path]]:
    """[(scene stem, offset, events.json)] for a project's rendered scenes (offsets from the logs, or
    from `durations` {stem: seconds} measured on the normalized files)."""
    from .build import load_project, scene_movie
    spec = load_project(project)
    items, offset = [], 0.0
    for s in spec["scenes"]:
        movie = scene_movie(project, quality, s)
        ev = movie.with_suffix(".events.json")
        stem = Path(s["file"]).stem
        items.append((stem, offset, ev))
        if durations and stem in durations:
            offset += durations[stem]
        elif ev.exists():
            log = json.loads(ev.read_text())
            fps = log.get("fps") or 0
            offset += (log.get("frames") / fps) if fps and log.get("frames") else float(log.get("duration", 0))
        else:
            raise FileNotFoundError(f"no event log for {stem}: {ev}")
    return items


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("-q", "--quality", default="h")
    ap.add_argument("--out", type=Path, help="output folder (default build/music/<quality>)")
    ap.add_argument("--report", action="store_true", help="print the score summary and QA numbers")
    args = ap.parse_args(argv)
    from .build import QUALITY_DIRS, load_project
    project = args.project.resolve()
    spec = load_project(project)
    settings = Settings.from_spec(spec)
    scenes = load_timeline(project_scenes(project, args.quality))
    total = sum(s.duration for s in scenes) if scenes else 0.0
    total = max(total, max((s.offset + s.duration for s in scenes), default=0.0))
    score, cues, ctx, bed, acc = compose(scenes, settings, total)
    music, rep = music_only(bed, acc, settings)
    rep.update(sync_30ms=round(sync_share(cues, score), 3), notes=len(score.notes), fx=len(score.fx),
               chords=len(score.chords), cues=len(cues), duration=round(total, 3))
    out = args.out or project / "build" / "music" / QUALITY_DIRS.get(args.quality, args.quality)
    write_outputs(out, score, cues, ctx, bed, acc, music, rep)
    print(f"music: {out}/music.wav  ({total:.1f}s, {rep['lufs']} LUFS, peak {rep['true_peak_dbtp']} dBTP, "
          f"{rep['notes']} notes, {rep['fx']} effects, {rep['chords']} chords, sync {rep['sync_30ms']:.0%})")
    if args.report:
        print("chords:", ", ".join(f"{c.t:.2f} {c.name}" for c in score.chords))


if __name__ == "__main__":
    main()
