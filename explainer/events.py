"""Render-time event log: what appeared on screen, where, and when, for the music composer.

Every VoiceScene (and every short-format BeatScene, explainer.short) writes `<Scene>.events.json` next
to its movie, the way `<Scene>.subs.json` is written. One record per play() / wait(), plus the
narration blocks, explicit marks and (shorts) captions:

    {"version": 1, "scene": "Hook", "fps": 60, "duration": 48.0, "frames": 2880, "grid": null,
     "events": [
      {"type": "voice", "t": 0.0, "dur": 3.1, "block": 0, "text": "How many different games ..."},
      {"type": "play", "t": 1.4, "dur": 0.4, "kinds": ["reveal"], "tags": [], "block": 0, "linear": false,
       "lagged": [], "anims": [{"anim": "Create", "kind": "reveal", "rate": "smooth", "mob": "Circle",
                                "x": -1.4, "y": 1.0, "w": 0.84, "h": 0.84, "n": 1, "at": 0.0, "end": 0.4}]},
      {"type": "mark", "t": 2.4, "kind": "count", "dur": 3.6, "data": {"n": 24, "every": 0.15}},
      {"type": "wait", "t": 6.0, "dur": 1.2, "block": null}]}

`t` and `dur` are seconds of the scene's own movie (the renderer clock, so the times of the quality you
render; compose from the log of the quality you ship). In an animation record:
  kind   what the animation does, from its class: reveal / clear / emphasis / morph / move / camera /
         count / other (KINDS below)
  mob    the animated mobject's class; x, y, w, h its centre and size after the play (x0, y0 before, when
         it moved); n its number of drawn parts
  at/end the leaf's start and end inside the play (a LaggedStart of 16 FadeIns gives 16 start times)
  sound  the mobject's `sound` attribute, if the scene set one (semantic sound, like semantic colour:
         `mark.sound = "X"`), so the composer need not guess identity from the class

Scenes can say what a moment means, so nothing has to be guessed:

    self.mark("count", n=24, every=0.15)        # a point in time (binds to the play that starts now)
    self.play(Create(win_line), kind="reveal")  # the same, as a play() keyword
    self.mark("silence", dur=2.4)               # a planned drop-out

Kinds the composer understands (explainer.music): cut, section, reveal, emphasis, count, particles,
hit, title, riser, silence, tape_stop, resolve, motif (data: {"name": ...}), end. Anything else is kept
and ignored.

Logging only reads the scene (positions, sizes, classes); it never changes what is drawn.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

VERSION = 1

# animation class -> what it does on screen (the composer's vocabulary)
KINDS = {
    **dict.fromkeys(["Write", "Create", "DrawBorderThenFill", "GrowArrow", "FadeIn", "GrowFromCenter",
                     "GrowFromPoint", "GrowFromEdge", "SpinInFromNothing", "AddTextLetterByLetter",
                     "AddTextWordByWord", "ShowIncreasingSubsets", "ShowSubmobjectsOneByOne", "SpiralIn",
                     "TypeWithCursor", "FadeInFromPoint", "FadeInFromLarge"], "reveal"),
    **dict.fromkeys(["FadeOut", "Uncreate", "Unwrite", "ShrinkToCenter", "RemoveTextLetterByLetter",
                     "UntypeWithCursor", "FadeOutAndShift", "FadeOutToPoint"], "clear"),
    **dict.fromkeys(["Indicate", "Circumscribe", "Flash", "Wiggle", "ApplyWave", "FocusOn",
                     "ShowPassingFlash", "Blink", "ShowCreationThenFadeOut"], "emphasis"),
    **dict.fromkeys(["Transform", "ReplacementTransform", "TransformMatchingTex", "TransformMatchingShapes",
                     "FadeTransform", "FadeTransformPieces", "TransformFromCopy", "ClockwiseTransform",
                     "CounterclockwiseTransform", "CyclicReplace", "Swap", "FadeToColor"], "morph"),
    **dict.fromkeys(["Rotate", "Rotating", "MoveToTarget", "_MethodAnimation", "ApplyMethod", "MoveAlongPath",
                     "Homotopy", "SmoothedVectorizedHomotopy", "ApplyPointwiseFunction", "ApplyMatrix",
                     "ApplyComplexFunction", "ScaleInPlace", "ShrinkInPlace", "SpinInPlace",
                     "ApplyFunction", "Restore"], "move"),
    **dict.fromkeys(["ChangeDecimalToValue", "ChangingDecimal", "Count", "CounterRoll", "CounterLand"], "count"),
}

DEFAULT_FRAME = None  # set lazily: (center x, center y, width) of an unmoved camera frame


def leaf_animations(anim, start: float = 0.0, span: float | None = None) -> list[tuple]:
    """Flatten AnimationGroup / LaggedStart / Succession: [(leaf, start, end)] in seconds inside the play
    (`span` = the outer animation's run time)."""
    span = anim.get_run_time() if span is None else span
    timings = getattr(anim, "anims_with_timings", None)
    subs = getattr(anim, "animations", None)
    if subs and timings is not None and len(timings):
        top = float(getattr(anim, "max_end_time", 0) or max(timings["end"]) or 1.0)
        rate = getattr(anim, "rate_func", None)
        out = []
        for row in timings:
            a = start + span * _alpha_at(rate, float(row["start"]) / top)
            b = start + span * _alpha_at(rate, float(row["end"]) / top)
            out += leaf_animations(row["anim"], a, max(0.0, b - a))
        return out
    if subs:
        out = []
        for a in subs:
            out += leaf_animations(a, start, span)
        return out
    return [(anim, start, start + span)]


def _alpha_at(rate, u: float) -> float:
    """The play's alpha at which a group's rate function reaches `u` (identity for linear groups)."""
    u = min(1.0, max(0.0, u))
    if rate is None or getattr(rate, "__name__", "") == "linear" or u in (0.0, 1.0):
        return u
    xs = np.linspace(0, 1, 513)
    try:
        ys = np.maximum.accumulate(np.array([float(rate(x)) for x in xs]))
    except Exception:
        return u
    i = int(np.searchsorted(ys, u))
    return float(xs[min(i, len(xs) - 1)])


def box(m) -> dict | None:
    """Centre, size and part count of a mobject (None if it has nothing drawn)."""
    try:
        if not m.family_members_with_points() and not hasattr(m, "pixel_array"):
            return None
        c = m.get_center()
        return {"x": round(float(c[0]), 3), "y": round(float(c[1]), 3), "w": round(float(m.width), 3),
                "h": round(float(m.height), 3), "n": len(m.family_members_with_points())}
    except Exception:
        return None


def describe(anim, at: float, end: float, before: dict | None, frame=None) -> dict:
    name = type(anim).__name__
    m = getattr(anim, "mobject", None)
    rf = getattr(anim, "rate_func", None)
    kind = KINDS.get(name, "other")
    if frame is not None and m is frame:
        kind = "camera"
    info = {"anim": name, "kind": kind, "rate": getattr(rf, "__name__", None),
            "at": round(at, 4), "end": round(end, 4)}
    if m is None:
        return info
    info["mob"] = type(m).__name__
    b = box(m)
    before = before or {}
    if b:
        info.update(b)
        if before and (abs(before["x"] - b["x"]) > 0.05 or abs(before["y"] - b["y"]) > 0.05):
            info.update(x0=before["x"], y0=before["y"])
        if before.get("w") and b["w"] and abs(before["w"] - b["w"]) > 0.05 * max(before["w"], b["w"]):
            info["w0"] = before["w"]
    snd = getattr(m, "__dict__", {}).get("sound")
    if snd is not None:
        info["sound"] = str(snd)
    extra = getattr(anim, "event_info", None)      # animations may describe themselves (counters: land times)
    if callable(extra):
        try:
            info.update(jsonable(extra()))
        except Exception:
            pass
    return info


def jsonable(v):
    if isinstance(v, dict):
        return {str(k): jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [jsonable(x) for x in v]
    if isinstance(v, (np.floating, float)):
        return round(float(v), 4)
    if isinstance(v, (np.integer, np.bool_, int, bool)) or v is None or isinstance(v, str):
        return v.item() if isinstance(v, np.generic) else v
    if hasattr(v, "get_center"):
        return box(v)
    return str(v)


class EventLog:
    """Mixin for a Manim Scene: logs every play() / wait() (and mark()) into self.events and writes
    <Scene>.events.json next to the movie at tear-down. Put it before the Scene class:
    `class VoiceScene(EventLog, Scene)`."""

    events_suffix = ".events.json"

    # ------------------------------------------------------------- state (lazy: works without setup())
    @property
    def events(self) -> list[dict]:
        st = self.__dict__.get("_ev_state")
        if st is None:
            st = self.__dict__["_ev_state"] = {"events": [], "pending": [], "block": None, "before": {},
                                               "written": False}
        return st["events"]

    def _ev_state_(self) -> dict:
        self.events  # noqa: B018  (creates the state)
        return self.__dict__["_ev_state"]

    def _ev_now(self) -> float:
        return float(self.renderer.time)

    def _ev_round(self, t: float) -> float:
        return round(float(t), 4)

    def _ev_frame(self):
        cam = getattr(self.renderer, "camera", None)
        return getattr(cam, "frame", None)

    def _ev_cam(self) -> list | None:
        """[centre x, centre y, width] of a moving camera's frame, when it is not the default one."""
        frame = self._ev_frame()
        if frame is None:
            return None
        try:
            from manim import config
            c = frame.get_center()
            w = float(frame.width)
            if abs(c[0]) < 1e-3 and abs(c[1]) < 1e-3 and abs(w - config.frame_width) < 1e-3:
                return None
            return [round(float(c[0]), 3), round(float(c[1]), 3), round(w, 3)]
        except Exception:
            return None

    # ------------------------------------------------------------- authoring API
    def mark(self, kind: str, *mobjects, dur: float | None = None, at: float | None = None, **data) -> dict:
        """Say what this moment means for the music: `self.mark("count", n=24, every=0.15)`. A mark made
        right before a play() (same time) is attached to it (its `tags`, and the mark's `dur` becomes the
        play's run time unless given). `mobjects` are logged with their position and size; `at` is a
        scene time (default: now)."""
        st = self._ev_state_()
        ev = {"type": "mark", "t": self._ev_round(self._ev_now() if at is None else at), "kind": str(kind)}
        if dur is not None:
            ev["dur"] = self._ev_round(dur)
        if mobjects:
            ev["mobs"] = [box(m) for m in mobjects]
        if data:
            ev["data"] = jsonable(data)
        st["events"].append(ev)
        if at is None:
            st["pending"].append(ev)
        return ev

    # ------------------------------------------------------------- Scene hooks
    def begin_animations(self) -> None:
        st = self._ev_state_()
        try:  # where each animated mobject starts (to log moves); read-only
            leaves = [leaf for a in self.animations or [] for leaf, _, _ in leaf_animations(a, 0.0, 1.0)]
            st["before"] = {id(a): box(a.mobject) for a in leaves if getattr(a, "mobject", None) is not None}
        except Exception:
            st["before"] = {}
        super().begin_animations()

    def play(self, *animations, **kwargs):
        kind = kwargs.pop("kind", None)
        sound = kwargs.pop("sound", None)
        if kind is not None:
            self.mark(kind, **({"sound": sound} if sound else {}))
        t0 = self._ev_now()
        out = super().play(*animations, **kwargs)
        try:
            self._ev_log_play(t0, sound)
        except Exception as e:  # logging must never break a render
            from manim import logger
            logger.debug(f"event log: {e}")
        return out

    def wait(self, duration: float = 1.0, *args, **kwargs):
        t0 = self._ev_now()
        out = super().wait(duration, *args, **kwargs)
        st = self._ev_state_()
        ev = {"type": "wait", "t": self._ev_round(t0), "dur": self._ev_round(self._ev_now() - t0),
              "block": st["block"]}
        self._ev_bind_marks(ev)
        st["events"].append(ev)
        return out

    def _ev_bind_marks(self, ev: dict) -> None:
        st = self._ev_state_()
        tags = []
        for m in st["pending"]:
            if abs(m["t"] - ev["t"]) < 1e-3:
                tags.append(m["kind"])
                m.setdefault("dur", ev["dur"])
        st["pending"] = []
        if tags:
            ev["tags"] = tags

    def _ev_log_play(self, t0: float, sound=None) -> None:
        st = self._ev_state_()
        anims = list(self.animations or [])
        from manim import Wait
        if anims and all(isinstance(a, Wait) for a in anims):
            return  # Scene.wait() plays a Wait: logged by wait()
        t1 = self._ev_now()
        frame = self._ev_frame()
        leaves = []
        for a in anims:
            leaves += leaf_animations(a, 0.0, a.get_run_time())
        before = st.get("before") or {}
        descr = [describe(a, s, e, before.get(id(a)), frame) for a, s, e in leaves]
        if sound:
            for d in descr:
                d.setdefault("sound", str(sound))
        lagged = [type(a).__name__ for a in anims if type(a).__name__ in ("LaggedStart", "Succession",
                                                                         "LaggedStartMap")]
        ev = {"type": "play", "t": self._ev_round(t0), "dur": self._ev_round(t1 - t0),
              "kinds": sorted({d["kind"] for d in descr}), "block": st["block"],
              "linear": bool(descr) and all(d.get("rate") == "linear" for d in descr),
              "lagged": lagged, "n_leaves": len(descr), "anims": descr}
        cam = self._ev_cam()
        if cam:
            ev["cam"] = cam
        self._ev_bind_marks(ev)
        st["events"].append(ev)

    # ------------------------------------------------------------- output
    def event_grid(self) -> dict | None:
        """The beat grid of this scene (BeatScene); None for narration-timed scenes."""
        return None

    def event_extras(self) -> dict:
        """Extra top-level fields for the log (BeatScene: captions)."""
        return {}

    def events_record(self) -> dict:
        fps = float(getattr(getattr(self.renderer, "camera", None), "frame_rate", 0) or 0)
        dur = self._ev_now()
        rec = {"version": VERSION, "scene": type(self).__name__, "fps": fps, "duration": self._ev_round(dur),
               "frames": int(round(dur * fps)) if fps else None, "grid": self.event_grid(),
               "events": self.events}
        rec.update(self.event_extras())
        return rec

    def write_events(self) -> Path | None:
        st = self._ev_state_()
        if st["written"]:
            return None
        try:
            movie = Path(self.renderer.file_writer.movie_file_path)
        except (AttributeError, TypeError):  # e.g. rendering a still image only
            return None
        st["written"] = True
        movie.parent.mkdir(parents=True, exist_ok=True)
        path = movie.with_suffix(self.events_suffix)
        path.write_text(json.dumps(self.events_record(), indent=1, ensure_ascii=False))
        return path

    def tear_down(self):
        getattr(super(), "tear_down", lambda: None)()
        self.write_events()


def load(path: Path) -> dict:
    """Read an events.json (any version this module wrote)."""
    return json.loads(Path(path).read_text())
