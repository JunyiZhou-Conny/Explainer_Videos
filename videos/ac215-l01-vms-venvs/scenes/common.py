"""Shared look for AC215 L1 (VMs, venvs and uv): paths, narration, the semantic colours of
BRIEF.md, loaders for the real captures in assets/, and the video's recurring pictures:

    Shelves      V2 · sys.path as a stack of shelves, a PINK search-light for `import`
    PathDoors    V3 · PATH as a row of doors; a command name walks along and knocks
    VersionLine  V4 · Python versions on a number line with the `>= 3.13` interval
    CostMeter    a GOLD running cost while a VM exists
    term()       the house terminal (prompt student@ac215-l01, title "ssh · ac215-l01")
    capture()    a captured command: .cmd .lines .exit (assets/terminal/<folder>/<name>.txt)
    excerpt()    lines a..b of a tutorial file in assets/source, for code_panel()

Colour table (BRIEF.md, binding):
    laptop / browser ........ LAPTOP  GREY
    cloud, VM, Google ....... CLOUD   BLUE
    system Python (shared) .. SYSTEM  ORANGE
    venv, uv.lock (project) . VENV    GREEN
    uv (the tool) ........... UV      PURPLE
    errors, refusals ........ ERR     RED
    your turn, tracker ...... TURN    YELLOW
    money ................... COST    GOLD
    PATH / sys.path lookups . LOOKUP  PINK
    a future thing (L2) ..... GREY, dashed
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DOWN, LEFT, RIGHT, UP, Arrow, DashedLine, DecimalNumber, FadeIn, FadeOut,
                   Line, Rectangle, RoundedRectangle, Text, Transform, ValueTracker, VGroup,
                   always_redraw, linear)

from explainer import style as S
from explainer.devops import (CAPTION, LABEL, MONO, SMALL, TAG, Terminal, box, chip, label, mono,
                              mono_line, tag)
from explainer.script import load_narration

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
TERMINAL = ASSETS / "terminal"
SOURCE = ASSETS / "source"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}

# ------------------------------------------------------------------ semantic colours
LAPTOP = S.GREY
CLOUD = S.BLUE
SYSTEM = S.ORANGE
VENV = S.GREEN
UV = S.PURPLE
ERR = S.RED
TURN = S.YELLOW
COST = S.GOLD
LOOKUP = S.PINK
INK = S.WHITE
DIMMED = S.GREY

# ------------------------------------------------------------------ the running example
USER, HOST = "student", "ac215-l01"
P_HOME = f"{USER}@{HOST}:~$"
P_REPO = f"{USER}@{HOST}:~/simple-translate$"
P_VENV = f"(app) {USER}@{HOST}:~/simple-translate$"

# README tracker steps (BRIEF.md)
STEPS_A = ["Create VM", "SSH", "apt-get update", "Install git", "Clone", "cd", "Install pip",
           "Install packages", "Run it", "Delete VM"]
STEPS_B = ["Create VM", "SSH", "apt-get update", "Install git", "Clone", "cd", "Install uv",
           "Reload shell", "uv sync", "Activate", "Run it", "Delete VM"]
SECTION_A = "Installing App on VM Manually"
SECTION_B = "Installing App on VM using UV"


def tracker_a(step: int | None = None):
    from explainer.devops import ReadmeTracker
    t = ReadmeTracker(SECTION_A, STEPS_A)
    return t.set_step(step) if step else t


def tracker_b(step: int | None = None):
    from explainer.devops import ReadmeTracker
    t = ReadmeTracker(SECTION_B, STEPS_B)
    return t.set_step(step) if step else t


# ------------------------------------------------------------------ captures and sources
class Capture:
    """One captured command: .cmd (as typed), .lines (its output), .exit (status)."""

    def __init__(self, cmd: str, lines: list[str], exit_code: int):
        self.cmd, self.lines, self.exit = cmd, lines, exit_code

    def pick(self, *ranges, ellipsis: str = "…") -> list[str]:
        """Output lines by 1-based inclusive ranges, e.g. pick((1, 3), (-2, -1)) -> first three,
        '…', last two. A single int picks one line. Negative numbers count from the end."""
        n = len(self.lines)
        out: list[str] = []
        last = None
        for r in ranges:
            a, b = (r, r) if isinstance(r, int) else r
            a = a if a > 0 else n + a + 1
            b = b if b > 0 else n + b + 1
            if last is not None and a > last + 1:
                out.append(ellipsis)
            out += self.lines[a - 1:b]
            last = b
        return out


def capture(name: str, folder: str = "debian12-part-a") -> Capture:
    """assets/terminal/<folder>/<name>.txt (name with or without .txt), parsed. Fails loudly if
    missing: never show an output that wasn't captured."""
    p = TERMINAL / folder / (name if name.endswith(".txt") else f"{name}.txt")
    if not p.exists():
        raise FileNotFoundError(f"capture {p.relative_to(PROJECT)} is missing (see ASSETS.md)")
    raw = p.read_text(encoding="utf-8").rstrip("\n").split("\n")
    cmd = raw[0][2:] if raw[0].startswith("$ ") else ""
    body = raw[1:]
    code = 0
    if body and re.fullmatch(r"\[exit -?\d+\]", body[-1]):
        code = int(body[-1][6:-1])
        body = body[:-1]
    return Capture(cmd, body, code)


def source_text(name: str) -> str:
    return (SOURCE / name).read_text(encoding="utf-8")


def excerpt(name: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of a tutorial file, for code_panel(..., first_line=first)."""
    lines = source_text(name).split("\n")
    return "\n".join(lines[first - 1:last])


# ------------------------------------------------------------------ house widgets
def term(prompt: str = P_HOME, rows: int = 9, width: float = 12.6, size: float = 22,
         title: str = f"ssh · {HOST}") -> Terminal:
    """The house terminal for this video (fixed size; it scrolls)."""
    return Terminal(prompt=prompt, width=width, rows=rows, size=size, title=title)


def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag: put it next to a command the viewer should run now."""
    return tag("▶ your turn", TURN)


def extra_tag() -> VGroup:
    return tag("extra · not in the README", S.GREY)


def illustration_tag() -> VGroup:
    return tag("illustration", S.GREY)


def expected_tag() -> VGroup:
    return tag("expected output", S.GREY)


def recorded_tag(s: str = "at the time of recording") -> VGroup:
    return tag(s, S.GREY)


def pkg(name: str, where: str = "system", size: float = SMALL) -> VGroup:
    """A package chip coloured by WHERE it lives: 'system' (ORANGE) or 'venv' (GREEN)."""
    return chip(name, SYSTEM if where == "system" else VENV, size=size, font=MONO)


# ------------------------------------------------------------------ V2 · sys.path shelves
class Shelves(VGroup):
    """sys.path drawn as shelves, top = searched first.

        sh = Shelves(["/usr/lib/python3.11", "/usr/local/lib/python3.11/dist-packages", ...],
                     colors={1: SYSTEM, 2: SYSTEM})
        sh.put(i, [pkg("googletrans"), ...])         # jars on shelf i (returns the jars)
        sh.search_anims(found=1)                       # PINK light from shelf 0 down to shelf `found`
    .rows[i] = VGroup(board, path_text); .jars[i] = VGroup of jars on shelf i
    """

    def __init__(self, paths: list[str], width: float = 9.0, size: float = 22, colors: dict | None = None,
                 pitch: float = 0.78, **kw):
        super().__init__(**kw)
        colors = colors or {}
        self.shelf_w, self.pitch, self.size = width, pitch, size
        self.rows, self.jars = VGroup(), []
        for i, p in enumerate(paths):
            col = colors.get(i, S.GREY)
            board = Line(LEFT * width / 2, RIGHT * width / 2, color=col, stroke_width=5)
            t = mono(p, size, col)          # same size on every shelf (choose `size` to fit)
            t.next_to(board, UP, buff=0.08).align_to(board, LEFT)
            row = VGroup(board, t).shift(DOWN * i * pitch)
            self.rows.add(row)
            self.jars.append(VGroup())
        self.add(self.rows)

    def put(self, i: int, jars: list, buff: float = 0.12) -> VGroup:
        """Place jars (chips) on shelf i, right-aligned, standing on the board."""
        g = VGroup(*jars).arrange(RIGHT, buff=buff)   # chips keep their size on every shelf
        board, path_text = self.rows[i]
        g.next_to(board, UP, buff=0.04).align_to(board, RIGHT)
        if g.get_left()[0] < path_text.get_right()[0] + 0.25:   # never cover the path: sit after it
            g.next_to(path_text, RIGHT, buff=0.3).align_to(g, DOWN)
            g.next_to(board, UP, buff=0.04, coor_mask=np.array([0, 1, 0]))
        self.jars[i] = g
        return g

    def light(self, i: int, color: str = LOOKUP, opacity: float = 0.22) -> Rectangle:
        """A translucent band over shelf i (the search-light's position)."""
        row = self.rows[i]
        return Rectangle(width=self.shelf_w + 0.3, height=self.pitch * 0.92, stroke_width=0) \
            .set_fill(color, opacity).move_to(row.get_center() + UP * 0.12)

    def search_anims(self, scene, found: int | None, run_time: float = 1.6, color: str = LOOKUP):
        """Play the search-light from the top shelf down to `found` (None: through all, then RED).
        Returns the light (left on screen at the final shelf)."""
        n = len(self.rows)
        stop = found if found is not None else n - 1
        lt = self.light(0, color)
        scene.play(FadeIn(lt), run_time=0.25)
        if stop > 0:
            scene.play(lt.animate.move_to(self.light(stop).get_center()), run_time=run_time, rate_func=linear)
        if found is None:
            scene.play(lt.animate.set_fill(ERR, 0.3), run_time=0.3)
        return lt


# ------------------------------------------------------------------ V3 · PATH doors
class PathDoors(VGroup):
    """PATH as a row of doors (left = searched first). Each door: frame + label underneath.

        doors = PathDoors(["/usr/local/bin", "/usr/bin", "/bin"])
        doors.knock(scene, "uv", found=None)            # walks along, RED 'command not found'
        doors.insert_front(scene, "~/.local/bin", UV)   # a new door slides in at the left
    """

    def __init__(self, dirs: list[str], colors: dict | None = None, door_w: float = 1.0,
                 door_h: float = 1.5, gap: float = 0.55, size: float = 20, **kw):
        super().__init__(**kw)
        self.door_w, self.door_h, self.gap, self.size = door_w, door_h, gap, size
        colors = colors or {}
        self.doors = VGroup(*[self._door(d, colors.get(d, S.GREY)) for d in dirs])
        self.doors.arrange(RIGHT, buff=gap, aligned_edge=UP)
        self.add(self.doors)

    def _door(self, d: str, color: str) -> VGroup:
        t = mono(d, self.size, color)
        w = max(self.door_w, t.width + 0.2)          # a long directory name gets a wider door
        frame = RoundedRectangle(width=w, height=self.door_h, corner_radius=0.06,
                                 stroke_color=color, stroke_width=3).set_fill(color, 0.1)
        knob = RoundedRectangle(width=0.08, height=0.08, corner_radius=0.04, stroke_width=0) \
            .set_fill(color, 1).move_to(frame.get_right() + LEFT * 0.18)
        t.next_to(frame, DOWN, buff=0.12)
        g = VGroup(frame, knob, t)
        g.frame, g.label, g.dir, g.color = frame, t, d, color
        return g

    def knock(self, scene, word: str, found: int | None, step_time: float = 0.45,
              color: str = LOOKUP):
        """`word` walks from the left, pausing at each door; enters door `found` (it turns GREEN-ish
        in its own colour) or, with None, ends on a RED 'command not found'. Returns the word."""
        w = mono(word, 26, color)
        w.next_to(self.doors[0], LEFT, buff=0.5)
        scene.play(FadeIn(w), run_time=0.3)
        stop = found if found is not None else len(self.doors) - 1
        for i in range(stop + 1):
            scene.play(w.animate.next_to(self.doors[i].frame, UP, buff=0.15), run_time=step_time)
        if found is not None:
            scene.play(w.animate.move_to(self.doors[found].frame).scale(0.8),
                       self.doors[found].frame.animate.set_fill(self.doors[found].color, 0.35), run_time=0.4)
        else:
            nf = label("command not found", 24, ERR).next_to(self.doors, RIGHT, buff=0.4)
            scene.play(w.animate.set_color(ERR), FadeIn(nf), run_time=0.4)
            w.not_found = nf
        return w

    def insert_front(self, scene, d: str, color: str, run_time: float = 0.8) -> VGroup:
        """Slide a new door in at the left; the others make room."""
        new = self._door(d, color)
        first = self.doors[0]
        shift = RIGHT * (new.frame.width + self.gap)
        new.align_to(first.frame, UP).align_to(first.frame, LEFT).shift(UP * 2.2)
        scene.play(self.doors.animate.shift(shift), run_time=run_time * 0.5)
        scene.play(new.animate.shift(DOWN * 2.2), run_time=run_time * 0.5)
        scene.remove(new)                      # it now lives inside the row (one top-level group)
        self.doors.submobjects.insert(0, new)
        if self not in scene.mobjects:
            scene.add(self)
        return new

    def remove_front(self, scene, run_time: float = 0.8) -> None:
        old = self.doors[0]
        w = old.frame.width + self.gap
        scene.play(old.animate.shift(UP * 2.2).set_opacity(0), run_time=run_time * 0.5)
        self.doors.remove(old)
        scene.remove(old)
        scene.play(self.doors.animate.shift(LEFT * w), run_time=run_time * 0.5)


# ------------------------------------------------------------------ V4 · Python versions
class VersionLine(VGroup):
    """Python 3.x versions on a number line (positions by MINOR version: 10 means 3.10), with the
    `>= 3.lo` interval glowing GREEN and running off the right end.

        vl = VersionLine(10, 16, lo=13)
        d = vl.dot(11, "3.11.2 · /usr/bin/python3", ERR)    # dot + label above the line
    """

    def __init__(self, first: int = 10, last: int = 16, lo: int = 13, width: float = 11.0,
                 size: float = 22, **kw):
        super().__init__(**kw)
        self.first, self.last, self.lo, self.line_w = first, last, lo, width
        self.axis = Line(LEFT * width / 2, RIGHT * width / 2, color=S.GREY, stroke_width=3)
        self.ticks = VGroup()
        for m in range(first, last + 1):
            x = self._x(m)
            self.ticks.add(VGroup(Line([x, -0.12, 0], [x, 0.12, 0], color=S.GREY, stroke_width=2),
                                  mono(f"3.{m}", size, S.GREY).move_to([x, -0.45, 0])))
        right = width / 2 + 0.25
        self.band = Rectangle(width=right - self._x(lo), height=0.3, stroke_width=0).set_fill(VENV, 0.3)
        self.band.move_to([(self._x(lo) + right) / 2, 0, 0])
        self.band_label = mono(f'requires-python = ">=3.{lo}"', size, VENV)
        self.band_label.next_to(self.band, UP, buff=0.3).align_to(self.band, LEFT)
        self.add(self.band, self.axis, self.ticks, self.band_label)

    def _x(self, minor: float) -> float:
        return -self.line_w / 2 + (minor - self.first + 0.5) / (self.last - self.first + 1) * self.line_w

    def point(self, minor: float, dy: float = 0.0):
        """A point on the (possibly moved) axis above minor version `minor`."""
        left = self.axis.get_start()
        return left + np.array([self._x(minor) + self.line_w / 2, dy, 0])

    def dot(self, minor: float, text: str, color: str, above: bool = True, size: float = 22) -> VGroup:
        from manim import Dot
        d = Dot(self.point(minor), radius=0.11, color=color)
        t = mono(text, size, color)
        t.next_to(d, UP if above else DOWN, buff=0.3 if above else 0.75)
        g = VGroup(d, t)
        g.dot, g.text = d, t
        return g


# ------------------------------------------------------------------ cost meter
class CostMeter(VGroup):
    """A GOLD '$ 0.000' counter driven by a ValueTracker (dollars). .tracker .run(scene, dollars, secs)"""

    def __init__(self, caption: str = "VM cost so far", size: float = 28, **kw):
        super().__init__(**kw)
        self.tracker = ValueTracker(0.0)
        num = DecimalNumber(0, num_decimal_places=3, font_size=size, color=COST, include_sign=False)
        num.add_updater(lambda m: m.set_value(self.tracker.get_value()))
        dollar = S.text("$", size, COST)
        row = VGroup(dollar, num).arrange(RIGHT, buff=0.08)
        cap = label(caption, CAPTION, COST).next_to(row, DOWN, buff=0.1)
        frame = box(max(row.width, cap.width) + 0.5, row.height + cap.height + 0.45, COST, fill_opacity=0.08)
        VGroup(row, cap).move_to(frame)
        self.num, self.caption, self.frame = num, cap, frame
        self.add(frame, row, cap)

    def run(self, scene, dollars: float, seconds: float):
        scene.play(self.tracker.animate(rate_func=linear).set_value(self.tracker.get_value() + dollars),
                   run_time=seconds)
