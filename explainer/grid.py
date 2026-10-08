"""The beat grid of the short format: tempo, beats, bars, and grid positions (no Manim import).

At 100 BPM (the default, as in the reference films) a beat is 0.6 s and a bar of 4 beats is 2.4 s;
at 60 fps that is 36 and 144 frames, so every grid point falls exactly on a frame.

Positions are written "bar:beat" with bars and beats counted from 0 at the start of the scene:
"0" is the scene's first downbeat, "2:1" is one beat into the third bar (2.4 * 2 + 0.6 = 5.4 s),
"2:1.5" half a beat later; "4.8s" is a plain time in seconds. A bare number is a bar.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

DEFAULT_BPM = 100.0
BEATS_PER_BAR = 4

UNITS = {"bar": None, "beat": 1.0, "half": 0.5, "eighth": 0.5, "quarter": 0.25, "sixteenth": 0.25,
         "triplet": 1 / 3}

_POS = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*(?::\s*(\d+(?:\.\d+)?))?\s*$")
_SECS = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*s\s*$")


@dataclass(frozen=True)
class Grid:
    bpm: float = DEFAULT_BPM
    beats_per_bar: int = BEATS_PER_BAR
    offset: float = 0.0          # time of beat 0 (a scene's grid starts at its first frame)

    @property
    def beat(self) -> float:
        return 60.0 / self.bpm

    @property
    def bar(self) -> float:
        return self.beat * self.beats_per_bar

    def unit(self, name: str | float) -> float:
        """Seconds of a grid unit: "bar", "beat", "half" (= "eighth"), "quarter" (sixteenth), or beats."""
        if isinstance(name, (int, float)):
            return float(name) * self.beat
        if name not in UNITS:
            raise ValueError(f"unknown grid unit {name!r} (use one of {', '.join(UNITS)})")
        return self.bar if UNITS[name] is None else UNITS[name] * self.beat

    def time(self, pos) -> float:
        """Seconds of a position: "bar:beat", "12.3s", a number of bars, or (bar, beat)."""
        if isinstance(pos, (tuple, list)):
            bar, beat = (list(pos) + [0])[:2]
            return self.offset + float(bar) * self.bar + float(beat) * self.beat
        if isinstance(pos, (int, float)):
            return self.offset + float(pos) * self.bar
        s = str(pos)
        m = _SECS.match(s)
        if m:
            return float(m.group(1))
        m = _POS.match(s)
        if not m:
            raise ValueError(f"bad grid position {pos!r}: use 'bar:beat' (from 0), e.g. '2:1', or '4.8s'")
        return self.offset + float(m.group(1)) * self.bar + float(m.group(2) or 0) * self.beat

    def position(self, t: float) -> tuple[int, float]:
        """(bar, beat within the bar) of a time, beats as a float."""
        beats = (t - self.offset) / self.beat
        bar = math.floor(beats / self.beats_per_bar + 1e-9)
        return bar, beats - bar * self.beats_per_bar

    def label(self, t: float) -> str:
        bar, beat = self.position(t)
        b = round(beat, 3)
        return f"{bar}:{int(b) if float(b).is_integer() else b}"

    def snap(self, t: float, unit="beat", direction: str = "up", tol: float = 1e-6) -> float:
        """The grid point of `unit` at or after (`up`), before (`down`) or nearest (`nearest`) t."""
        u = self.unit(unit)
        k = (t - self.offset) / u
        if direction == "up":
            n = math.ceil(k - tol)
        elif direction == "down":
            n = math.floor(k + tol)
        else:
            n = round(k)
        return self.offset + n * u

    def on_grid(self, t: float, unit="beat", tol: float = 0.0105) -> bool:
        return abs(self.snap(t, unit, "nearest") - t) <= tol

    def beats_between(self, a: float, b: float) -> float:
        return (b - a) / self.beat


def frames(seconds: float, fps: float) -> int:
    """Whole frames in `seconds` (grid times are exact frames at 15, 30 and 60 fps)."""
    return int(round(seconds * fps))


def play_time(n_frames: int, fps: float) -> float:
    """A run time Manim turns into exactly `n_frames` frames (np.arange(0, run_time, 1/fps))."""
    return (n_frames - 1e-4) / fps


def hold_time(n_frames: int, fps: float) -> float:
    """A duration a frozen-frame wait turns into exactly `n_frames` frames (int(duration * fps))."""
    return (n_frames + 1e-4) / fps
