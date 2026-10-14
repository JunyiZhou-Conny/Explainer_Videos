"""Shared Swiss visual kit for the speciesOT series (videos/speciesot-e*).

Each episode's scenes.py puts this folder on sys.path:

    SERIES = Path(__file__).resolve().parent.parent / "speciesot-series"
    sys.path.insert(0, str(SERIES))
    from speciesot_kit import *

The palette, fonts and small text helpers come from the shared Swiss style contract
(explainer/styles/swiss.py). This file adds the series vocabulary: code panels with real
line numbers, object and class cards, dictionary drawers, error cards, provenance tags,
ponder cards, point clouds, and the EpisodeScene base (narration timing + frame budget).

Layout contract: header above y = 2.05; teaching content inside x in [-6.3, 6.3] and
y in [-2.45, 2.05]; the bottom 170 px (y < -2.74) is the caption band and stays empty.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from manim import (BOLD, DOWN, LEFT, ORIGIN, RIGHT, UP, Arrow, Create, DashedVMobject, Dot,
                   FadeIn, FadeOut, Line, Rectangle, RoundedRectangle, Text, VGroup, VMobject,
                   config)

from explainer.scene import VoiceScene
from explainer.styles import swiss
from explainer.styles.swiss import (PAPER, INK, RED, GRAY, FAINT, LATIN, label, at, left,
                                    line, card, folder, arrow)

swiss.setup_fonts()
config.background_color = PAPER

MONO = "DejaVu Sans Mono"
SERIES_TAG = "SPECIESOT / BUILDING THE PACKAGE"
TOP, BOTTOM = 2.05, -2.45          # teaching area (caption band is below -2.74)
TINT = "#F1D9D4"                   # pale accent for a highlighted code line (flat, no gradient)

__all__ = [n for n in dir() if not n.startswith("_")]  # re-export the Swiss names above


# ---------------------------------------------------------------- text

def mono(s, size=22, color=INK, bold=False):
    return Text(s, font=MONO, font_size=size, color=color, weight=BOLD if bold else "NORMAL")


def mono_left(s, x, y, size=22, color=INK, bold=False):
    t = mono(s, size, color, bold)
    t.move_to([x + t.width / 2, y, 0])
    return t


# ---------------------------------------------------------------- code panel

ADVANCE = 0.008261                 # DejaVu Sans Mono advance per font-size unit (calibrated)


def code_line(body, size=20, color=INK):
    """One line of code with a stable baseline: a full-height strut glyph is laid out first
    (so every line has the same ink box), positioned, then removed. Leading spaces keep their
    width, so indentation survives. Returns the Text; call place_line() to position it."""
    t = Text("|" + (body if body else " "), font=MONO, font_size=size, color=color)
    t.strut = t[0]
    return t


def place_line(t, x_left, y, size):
    """Put the line so its first character cell starts at x_left and its row centre is y."""
    adv = ADVANCE * size
    t.shift(np.array([x_left - adv / 2 - t.strut.get_center()[0], y - t.strut.get_center()[1], 0]))
    t.remove(t.strut)
    return t


class CodePanel(VGroup):
    """Real source lines with their real line numbers.

    `rows` is a list of (line_number, text) pairs exactly as in the file (indentation kept,
    then dedented by the common minimum; an elided stretch may be written as "…").
    `row(n)` returns the text of line n; `mark(n)` builds a highlight (pale tint + red gutter
    bar) drawn between the panel fill and its text (z-index), so it can simply be FadeIn'd.
    """

    def __init__(self, rows, title, x, y, width=6.4, size=20, gap=None, numbers=True,
                 title_size=15):
        super().__init__()
        indents = [len(t) - len(t.lstrip(" ")) for _, t in rows if t.strip()]
        cut = min(indents) if indents else 0
        bodies = [(n, t[cut:] if t.strip() else "") for n, t in rows]
        digits = max((len(str(n)) for n, _ in rows if n is not None), default=1)
        # one size for the whole panel: shrink uniformly until the longest line fits
        longest = max((len(b) for _, b in bodies), default=1)
        for _ in range(12):
            num_w = (.22 + ADVANCE * (size - 4) * digits) if numbers else .02
            if num_w + .14 + ADVANCE * size * (longest + 1) + .2 <= width or size <= 12:
                break
            size -= 1
        if size < 16:
            print(f"CODEPANEL WARNING: {title!r} shrank to font size {size}; widen the panel "
                  f"or show fewer/shorter lines (longest = {longest} chars).", flush=True)
        gap = gap or size * 0.0172
        self.size, self.gap, self.numbers = size, gap, numbers
        head_h = .4 if title else 0
        height = len(rows) * gap + 0.3 + head_h
        self.frame = Rectangle(width=width, height=height, stroke_color=INK, stroke_width=2,
                               fill_color=PAPER, fill_opacity=1).move_to([x, y, 0])
        top = self.frame.get_top()[1]
        x0 = self.frame.get_left()[0]
        parts = [self.frame]
        if title:
            self.tab = mono(title, title_size, GRAY)
            self.tab.move_to([x0 + .2 + self.tab.width / 2, top - head_h / 2, 0])
            parts += [self.tab, Line([x0, top - head_h, 0], [x0 + width, top - head_h, 0],
                                     color=FAINT, stroke_width=1.5)]
        body_top = top - head_h
        self.body_top = body_top
        self.gutter_x = x0 + ((.22 + ADVANCE * (size - 4) * digits) if numbers else .02)
        # geometry relative to the frame, so marks follow later shifts and scales
        self._h0, self._head_h, self._gutter_off = height, head_h, self.gutter_x - x0
        self.rows, self.nums, self.texts = {}, VGroup(), VGroup()
        for i, (num, body) in enumerate(bodies):
            ry = body_top - .15 - gap / 2 - i * gap
            t = place_line(code_line(body, size), self.gutter_x + .14, ry, size)
            self.rows[num if num is not None else ("_", i)] = t   # unnumbered rows: ("_", i)
            self.texts.add(t)
            if numbers and num is not None:
                nt = place_line(code_line(str(num), size - 4, GRAY),
                                self.gutter_x - .1 - ADVANCE * (size - 4) * len(str(num)), ry,
                                size - 4)
                self.nums.add(nt)
        if numbers:
            parts.append(Line([self.gutter_x, body_top - .06, 0],
                              [self.gutter_x, top - height + .06, 0],
                              color=FAINT, stroke_width=1.5))
        self.texts.set_z_index(2)
        self.nums.set_z_index(2)
        self.add(*parts, self.nums, self.texts)
        top_y, bot_y = self.frame.get_top()[1], self.frame.get_bottom()[1]
        if top_y > TOP + .02 or bot_y < BOTTOM - .02:
            print(f"CODEPANEL LAYOUT: {title!r} spans y {bot_y:.2f}..{top_y:.2f}, outside the "
                  f"teaching area [{BOTTOM}, {TOP}]; move it, or pass gap= / fewer rows.",
                  flush=True)

    def row(self, num):
        return self.rows[num]

    def row_y(self, num):
        return self._row_centre(num)

    def _scale(self):
        return self.frame.height / self._h0

    def mark(self, *nums, color=RED):
        """A flat tint behind the given lines plus a red bar in the gutter, placed from the
        panel's current position and scale (so it is right after shift/scale/move_to)."""
        k = self._scale()
        gutter = self.frame.get_left()[0] + self._gutter_off * k
        marks = VGroup()
        for num in nums:
            y = self._row_centre(num)
            w = self.frame.get_right()[0] - gutter - .04 * k
            band = Rectangle(width=w, height=self.gap * .98 * k, stroke_width=0,
                             fill_color=TINT, fill_opacity=1)\
                .move_to([gutter + .02 * k + w / 2, y, 0])
            bar = Rectangle(width=.08 * k, height=self.gap * .98 * k, stroke_width=0,
                            fill_color=color, fill_opacity=1).move_to([gutter + .04 * k, y, 0])
            marks.add(VGroup(band, bar))
        marks.set_z_index(1)
        return marks

    def _row_centre(self, num):
        i = list(self.rows).index(num)
        k = self._scale()
        return self.frame.get_top()[1] - (self._head_h + .15 + self.gap / 2 + i * self.gap) * k


def code_panel(rows, title, x, y, width=6.4, size=20, **kw):
    return CodePanel(rows, title, x, y, width, size, **kw)


def highlight(scene, panel, *nums, run_time=.45):
    """Put a highlight under lines `nums` of `panel` (returns it so it can be removed)."""
    m = panel.mark(*nums)
    scene.play(FadeIn(m), run_time=run_time)
    return m


# ---------------------------------------------------------------- cards

def obj_card(title, rows=(), x=0, y=0, width=4.2, size=20, row_gap=.38, head="OBJECT"):
    """An object: an ink header strip naming its class, then one row per attribute."""
    n = max(len(rows), 1)
    need = max([mono(r, size).width for r in rows] + [mono(title, size + 1).width + 1.2]) + .5
    width = max(width, need)
    h = .62 + n * row_gap + .18
    frame = Rectangle(width=width, height=h, stroke_color=INK, stroke_width=2, fill_color=PAPER,
                      fill_opacity=1).move_to([x, y, 0])
    strip = Rectangle(width=width, height=.52, stroke_width=0, fill_color=INK, fill_opacity=1)
    strip.move_to([x, frame.get_top()[1] - .26, 0])
    name = Text(title, font=MONO, font_size=size + 1, color=PAPER)
    name.move_to([frame.get_left()[0] + .2 + name.width / 2, strip.get_y(), 0])
    kind = Text(head, font=LATIN, font_size=14, color=PAPER, weight=BOLD)
    kind.move_to([frame.get_right()[0] - .16 - kind.width / 2, strip.get_y(), 0])
    g = VGroup(frame, strip, name, kind)
    g.rows = VGroup()
    g.row_gap, g.size = row_gap, size
    g.first_y = strip.get_bottom()[1] - .3
    g.x_left = frame.get_left()[0] + .22
    for i, r in enumerate(rows):
        t = obj_row(g, i, r)
        g.rows.add(t)
        g.add(t)
    return g


def obj_row(card_, i, text, color=INK):
    t = mono(text, card_.size, color)
    t.move_to([card_.x_left + t.width / 2, card_.first_y - i * card_.row_gap, 0])
    return t


def class_card(name, methods, x, y, width=3.6, abstract=False, parent=None, size=20,
               accent=False):
    """A blueprint: class name (and parent), then its method names. Dashed when abstract."""
    rows = len(methods)
    h = .78 + rows * .36 + .12
    rect = Rectangle(width=width, height=h, stroke_color=RED if accent else INK, stroke_width=2,
                     fill_color=PAPER, fill_opacity=1).move_to([x, y, 0])
    frame = DashedVMobject(rect, num_dashes=60) if abstract else rect
    bg = Rectangle(width=width, height=h, stroke_width=0, fill_color=PAPER,
                   fill_opacity=1).move_to([x, y, 0])
    title = mono(name + (f"({parent})" if parent else ""), size + 2, RED if accent else INK,
                 bold=True)
    if title.width > width - .3:
        title.scale_to_fit_width(width - .3)
    top = rect.get_top()[1]
    title.move_to([rect.get_left()[0] + .18 + title.width / 2, top - .32, 0])
    rule = Line([rect.get_left()[0], top - .62, 0], [rect.get_right()[0], top - .62, 0],
                color=FAINT, stroke_width=1.5)
    g = VGroup(bg, frame, title, rule)
    g.methods = VGroup()
    for i, m in enumerate(methods):
        t = mono(m, size, GRAY if abstract else INK)
        t.move_to([rect.get_left()[0] + .3 + t.width / 2, top - .92 - i * .36, 0])
        g.methods.add(t)
    g.add(g.methods)
    return g


def error_card(etype, message, where, x, y, width=7.6, size=20, tag="MEASURED"):
    """A traceback's last line, as a card: what (red), the message (str or list of lines),
    and where it happened."""
    head = mono(etype, size + 4, RED, bold=True)
    msgs = [message] if isinstance(message, str) else list(message)
    body = VGroup(*[mono(m, size, INK) for m in msgs])
    loc = mono(where, size - 2, GRAY) if where else VGroup()
    for t in list(body) + ([loc] if where else []):
        if t.width > width - .5:
            t.scale_to_fit_width(width - .5)
    gap = size * .0175
    h = .5 + head.height + .16 + len(msgs) * gap + (loc.height + .14 if where else 0) + .3
    frame = Rectangle(width=width, height=h, stroke_color=INK, stroke_width=2, fill_color=PAPER,
                      fill_opacity=1).move_to([x, y, 0])
    bar = Rectangle(width=width, height=.09, stroke_width=0, fill_color=RED,
                    fill_opacity=1).move_to([x, frame.get_top()[1] - .045, 0])
    lx = frame.get_left()[0] + .25
    top = frame.get_top()[1]
    head.move_to([lx + head.width / 2, top - .38, 0])
    yy = head.get_bottom()[1] - .16 - gap / 2
    for t in body:
        t.move_to([lx + t.width / 2, yy, 0])
        yy -= gap
    if where:
        loc.move_to([lx + loc.width / 2, yy + gap / 2 - .14 - loc.height / 2, 0])
    g = VGroup(frame, bar, head, body, loc)
    if tag:
        st = source_tag(tag)
        st.move_to([frame.get_right()[0] - st.width / 2 - .14, top - .34, 0])
        g.add(st)
    g.set_z_index(5)
    return g


def source_tag(kind):
    """Provenance chip: READ IN CODE / READ IN NOTEBOOK / MEASURED / INFERRED."""
    color = {"MEASURED": RED, "INFERRED": GRAY, "EXAMPLE": GRAY}.get(kind, INK)
    t = Text(kind, font=LATIN, font_size=15, color=color, weight=BOLD)
    box = RoundedRectangle(corner_radius=.06, width=t.width + .26, height=t.height + .16,
                           stroke_color=color, stroke_width=1.5, fill_color=PAPER,
                           fill_opacity=1).move_to(t.get_center())
    return VGroup(box, t)


def tag_at(kind, x, y):
    return source_tag(kind).move_to([x, y, 0])


def chip(text, x, y, color=INK, size=22, fill=PAPER, pad=.22, font=MONO):
    t = Text(text, font=font, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=.06, width=t.width + 2 * pad, height=t.height + .26,
                           stroke_color=color, stroke_width=2, fill_color=fill,
                           fill_opacity=1).move_to([x, y, 0])
    t.move_to(box.get_center())
    return VGroup(box, t)


def drawer(label_, value, x, y, width=3.4, color=INK, size=20, value_color=INK):
    """One drawer of a dictionary: its label on the tab, its value inside."""
    body = Rectangle(width=width, height=.56, stroke_color=color, stroke_width=2,
                     fill_color=PAPER, fill_opacity=1).move_to([x, y, 0])
    lab = mono(f"'{label_}'", size, color)
    lab.move_to([body.get_left()[0] + .16 + lab.width / 2, y, 0])
    val = mono(str(value), size, value_color)
    val.move_to([body.get_right()[0] - .16 - val.width / 2, y, 0])
    knob = Line([x - .18, y - .2, 0], [x + .18, y - .2, 0], color=FAINT, stroke_width=3)
    return VGroup(body, knob, lab, val)


def terminal(lines, x, y, width=7.0, size=19):
    """An ink panel with paper-coloured monospace lines (commands start with $)."""
    texts = VGroup(*[mono(l if l else " ", size, PAPER if l.startswith("$") else "#D9D5CB")
                     for l in lines])
    gap = size * .0185
    h = len(lines) * gap + .36
    box = Rectangle(width=width, height=h, stroke_width=0, fill_color=INK,
                    fill_opacity=1).move_to([x, y, 0])
    top = box.get_top()[1]
    for i, t in enumerate(texts):
        if t.width > width - .4:
            t.scale_to_fit_width(width - .4)
        t.move_to([box.get_left()[0] + .2 + t.width / 2, top - .26 - i * gap, 0])
    g = VGroup(box, texts)
    g.lines = texts
    return g


def ponder(zh, en, y=-1.0, width=9.6):
    """A pause-and-ponder card (the series' thinking beats)."""
    frame = Rectangle(width=width, height=1.95, stroke_color=RED, stroke_width=3,
                      fill_color=PAPER, fill_opacity=1).move_to([0, y, 0])
    q = at("想一想 / PAUSE AND PONDER", 0, y + .58, 22, RED, bold=True)
    z = at(zh, 0, y + .1, 30, INK, width - .6)
    e = at(en, 0, y - .5, 24, GRAY, width - .6)
    return VGroup(frame, q, z, e).set_z_index(6)


def cloud(n, cx, cy, spread=.45, color=INK, seed=0, radius=.045, opacity=1.0):
    rng = np.random.default_rng(seed)
    pts = rng.normal(0, spread, size=(n, 2))
    return VGroup(*[Dot([cx + px, cy + py, 0], radius=radius, color=color,
                        fill_opacity=opacity) for px, py in pts])


def strike(m, color=RED, stroke=4):
    return Line(m.get_corner(DOWN + LEFT) + LEFT * .05, m.get_corner(UP + RIGHT) + RIGHT * .05,
                color=color, stroke_width=stroke)


def bracket(x, y1, y2, text, color=INK, size=22, side=RIGHT):
    """A vertical bracket from y1 to y2 at x, with a label beside it."""
    d = .14 if side is RIGHT else -.14
    br = VGroup(Line([x, y1, 0], [x, y2, 0], color=color, stroke_width=2),
                Line([x, y1, 0], [x - d, y1, 0], color=color, stroke_width=2),
                Line([x, y2, 0], [x - d, y2, 0], color=color, stroke_width=2))
    lab = label(text, size, color)
    lab.move_to([x + (.2 + lab.width / 2) * (1 if side is RIGHT else -1), (y1 + y2) / 2, 0])
    return VGroup(br, lab)


# ---------------------------------------------------------------- the scene base

class EpisodeScene(VoiceScene):
    """Narration timing + header + exact frame budget, shared by every episode.

    Subclasses set `episode` ("E1") and `total` ("06"); narration comes from the plan
    (script.json) that the engine passes in EPISODE_PLAN, never from the scene code.
    """
    pad_after_clip = .18
    episode = "E?"
    total = "00"

    def setup(self):
        super().setup()
        self.camera.background_color = PAPER
        plan = json.loads(Path(os.environ["EPISODE_PLAN"]).read_text())
        self.spec = next(s for s in plan["scenes"] if s["id"].upper() == self.__class__.__name__)

    def header(self, name=None):
        ident = self.spec["id"][1:]
        name = name or self.spec["title_en"]
        self.add(line(-6.3, 3.42, 6.3, 3.42),
                 left(SERIES_TAG, -6.3, 3.67, 15),
                 at(f"{self.episode} · {ident} / {self.total}", 5.7, 3.67, 16, RED))
        title = left(name, -6.3, 2.85, 44, INK, 12.5, True)
        self.play(FadeIn(title, shift=UP * .10), run_time=.4)
        self.add(left(self.spec["title_zh"], -6.3, 2.34, 21, GRAY))

    def say(self, i):
        return self.voiceover(self.spec["lines"][i]["en"])

    def cue(self, vo, f, *anims, run_time=.65):
        """Play `anims` once fraction `f` of the current clip has been spoken."""
        delay = vo.duration * f - vo.elapsed
        if delay > .04:
            self.wait(delay)
        if anims:
            self.play(*anims, run_time=run_time)

    def content(self):
        """Everything except the header (for dimming and clearing). Scene.play wraps the members
        of LaggedStart/AnimationGroup in a plain Group (not a VMobject); look inside those too."""
        out, seen = [], set()
        for m in self.mobjects:
            parts = m.submobjects if not isinstance(m, VMobject) else [m]
            for p in parts:
                if isinstance(p, VMobject) and p.get_y() < 2.2 and id(p) not in seen:
                    seen.add(id(p))
                    out.append(p)
        return out

    def dim_rest(self, opacity=.15):
        return VGroup(*self.content()).animate.set_opacity(opacity)

    def clear_content(self, run_time=.4):
        ms = self.content()
        if ms:
            self.play(*[FadeOut(m) for m in ms], run_time=run_time)

    def finish(self):
        remaining = self.spec["duration"] - self.renderer.time
        if remaining < -0.02:
            print(f"BUDGET WARNING {self.spec['id']}: scene runs {-remaining:.2f}s over "
                  f"its {self.spec['duration']:.2f}s budget; the end will be cut.", flush=True)
        if remaining > .37:
            self.wait(remaining - .30)
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.30)
        elif remaining > .015:
            self.wait(remaining)


__all__ = [n for n in dir() if not n.startswith("_")]
