"""Shared look for 'How these explainer videos are made': paths, narration, live values, the
semantic colours of script.md, and the visual vocabulary every scene uses (role icons, chips,
tags, exhibits of real images, code panels, glyphs, cards), so the eleven scenes read as one video.

Colour table (script.md, binding):
    the user ................ USER       PINK
    the main agent .......... AGENT      BLUE
    sub-agents .............. SUB_AGENT  faded BLUE (BLUE at 45 % on the background)
    tools, files, code ...... TOOL       GREY
    audio, voice, anchors ... AUDIO      ORANGE
    a measured check ........ MEASURED   GREEN
    a bug or a failure ...... BUG        RED
    not yet verified ........ OPEN       YELLOW, dashed outline only (+ a tag)
Ponder cards are the toolkit's standard card (solid YELLOW). Emphasis is WHITE Indicate /
Circumscribe (use `emphasize`), never highlight_box.

Honesty rules the helpers enforce (FACTSHEET 6-7): nobody's name appears anywhere ("the user");
the cost is only drawn by `cost_card`, which always carries LIVE's label; every redrawn picture
carries `recon_tag()` (or `rerender_tag()` for the re-render of commit 8a922bf); real images are
shown with `exhibit()` in a thin GREY frame with a `source_caption()`.

Quick map (details in each docstring):
    paths/data   HERE PROJECT ASSETS SPEC LIVE TITLES NARRATION QUOTES EXCERPTS asset() asset_text()
    text         label() mono() zh() caption() wrap()
    roles        role_icon("user"|"agent"|"sub") ai_badge() sub_agent_cluster()
    chips/tags   chip() split_chip() tag() recon_tag() rerender_tag() open_tag() open_outline()
                 measured_badge() bug_tag() pin_to_corner()
    cards        file_card() quote_card() speech_bubble() subtitle_band() cost_card()
    exhibits     exhibit() source_caption() gloss()
    code         code_block() code_panel() code_span() line_bar() terminal()
    glyphs       headphones() play_button() pause_icon() strike() cant_hear_or_play() pen() clock()
                 check_mark() cross_mark() file_icon() video_player() anchor_pin()
    data         time_axis() load_envelope() waveform()
    motion       emphasize() pulse() dim() undim() gather() ponder_in() ponder_drain() fade_out_all()
"""

from __future__ import annotations

import datetime as dt
import re
import textwrap
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, UL, UP, UR, Arc, Arrow, Circle,
                   Circumscribe, Code, DashedVMobject, DecimalNumber, Dot, FadeIn, FadeOut, Group,
                   ImageMobject, Indicate, Intersection, Line, ManimColor, Polygon, Rectangle,
                   RoundedRectangle, Triangle, VGroup, VMobject, interpolate_color, linear,
                   there_and_back)

from explainer import i18n
from explainer import style as S
from explainer.components import person_icon, ponder_card
from explainer.script import load_narration

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
LIVE = SPEC["live"]                                  # cost_usd, cost_label, snapshot, commits_cutoff
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
NARRATION = load_narration(PROJECT / "script.md")    # {"S01": [SAY line, ...], ...}
QUOTES = yaml.safe_load((ASSETS / "quotes.yaml").read_text())      # the user's words (exact)
EXCERPTS = yaml.safe_load((ASSETS / "excerpts.yaml").read_text())  # real text excerpts by asset id


def asset(name: str) -> Path:
    """Path of a file in assets/ (fails loudly if it is missing: never draw a fake 'real' asset)."""
    p = ASSETS / name
    if not p.exists():
        raise FileNotFoundError(f"assets/{name} is missing (see ASSETS.md)")
    return p


def asset_text(name: str) -> str:
    """Text of an asset, e.g. asset_text("code/ttt_s03_stop_317.py"), trailing newline removed."""
    return asset(name).read_text(encoding="utf-8").rstrip("\n")


# ------------------------------------------------------------------ semantic colours
def blend(a: str, b: str, t: float) -> str:
    """Colour t of the way from a to b, as hex (solid, so overlaps never double the opacity)."""
    return interpolate_color(ManimColor(a), ManimColor(b), t).to_hex()


USER = S.PINK
AGENT = S.BLUE
SUB_AGENT = blend(S.BG, S.BLUE, 0.45)       # faded BLUE: BLUE at 45 % on the background
SUB_AGENT_TEXT = blend(S.BG, S.BLUE, 0.75)  # same hue, raised so 24 pt labels stay readable
TOOL = S.GREY
AUDIO = S.ORANGE
MEASURED = S.GREEN
BUG = S.RED
OPEN = S.YELLOW                             # only ever as a DASHED outline (+ a tag)
EMPHASIS = S.WHITE
INK = S.WHITE                               # plain text
CAPTION_COLOR = S.GREY
PANEL = S.GREY_DARKER                       # card / panel fill
ROLE_COLOR = {"user": USER, "agent": AGENT, "sub": SUB_AGENT, "tool": TOOL}

# ------------------------------------------------------------------ sizes and fonts
TITLE = 48          # scene / section titles
BODY = 32
LABEL = 26          # labels in diagrams
SMALL = 24          # chips, bubbles, card text
TAG = 22            # tags ("reconstruction", "not yet verified"), as script.md asks
CAPTION = 20        # source captions (the toolkit minimum)
MONO = "DejaVu Sans Mono"   # the house code font (same as the other videos' code panels)
SANS = S.FONT_SANS

# fixed strings (honesty: always the same words)
RECON = "reconstruction"
RERENDER = "re-rendered from the old code (commit 8a922bf)"
NOT_VERIFIED = "not yet verified"
IDEA = "idea · not built yet"
DICTATED = QUOTES["captions"]["dictated"]           # "— the user (dictated; filler words removed)"
CHINESE_REQUEST = QUOTES["captions"]["chinese_request"]
SUMMARIZED = QUOTES["captions"]["summaries"]        # "requests, summarized"


# ------------------------------------------------------------------ text
def label(s: str, size: float = LABEL, color: str = INK, **kw):
    """House-font text (CMU Serif)."""
    return S.text(s, size, color, **kw)


def mono(s: str, size: float = SMALL, color: str = INK, **kw):
    """Monospace text for filenames, commands and console output."""
    return S.text(s, size, color, font=MONO, **kw)


def zh(s: str, size: float = 30, color: str = INK, sans: bool = True, **kw):
    """Chinese text in this English render: needs an explicit CJK font and a space-free string."""
    assert " " not in s, f"CJK text must be space-free: {s!r}"
    return S.text(s, size, color, font=i18n.CJK_FONTS["sans" if sans else "serif"], **kw)


def caption(s: str, size: float = CAPTION, color: str = CAPTION_COLOR, **kw):
    """Small GREY caption text (20 pt by default)."""
    return S.text(s, size, color, **kw)


def wrap(s: str, width: int) -> str:
    """Hard-wrap a string at `width` characters (Manim's Text never wraps by itself). Explicit
    line breaks are kept, and runs of 2+ spaces stay as they are (a quoted gap such as
    '4 × 3 × 2      12' must not collapse): they become no-break spaces."""
    s = re.sub(r" {2,}", lambda m: "\u00a0" * len(m.group(0)), s)
    out = []
    for para in s.split("\n"):
        out += textwrap.wrap(para, width=width, break_long_words=False, break_on_hyphens=False) or [""]
    return "\n".join(out)


def _line_height(size: float) -> float:
    """Height of one line of house text at `size` (ascender to descender), for even boxes."""
    return _ref_height(round(size, 2))


@lru_cache(maxsize=32)
def _ref_height(size: float) -> float:
    return S.text("Hgy", size).height


# ------------------------------------------------------------------ boxes
def box(width: float, height: float, color: str = TOOL, fill: str | None = None,
        fill_opacity: float = 0.14, stroke: float = 2.5, radius: float = 0.14,
        dashed: bool = False):
    """A rounded box: stroke in `color`, a faint fill of the same colour (or `fill`).
    dashed=True gives the 'still open' outline (no fill); use it only with OPEN."""
    r = RoundedRectangle(width=width, height=height, corner_radius=min(radius, height / 2, width / 2),
                         stroke_color=color, stroke_width=stroke)
    if dashed:
        r.set_fill(S.BG, 0)
        d = DashedVMobject(r, num_dashes=max(12, int((width + height) * 7)), dashed_ratio=0.55)
        d.set_stroke(color, stroke)
        return d
    r.set_fill(fill or color, fill_opacity)
    return r


def open_outline(m, buff: float = 0.14, color: str = OPEN, stroke: float = 3):
    """The dashed YELLOW outline that means 'not yet verified / still open / not built yet'."""
    return box(m.width + 2 * buff, m.height + 2 * buff, color, dashed=True, stroke=stroke).move_to(m)


# ------------------------------------------------------------------ chips and tags
class Chip(VGroup):
    """A labelled rounded chip: chip.box, chip.text (and chip.icon if given)."""


def chip(s: str, color: str = TOOL, size: float = SMALL, text_color: str = INK,
         dashed: bool = False, icon=None, pad_x: float = 0.26, pad_y: float = 0.13,
         fill_opacity: float = 0.16) -> Chip:
    """A thing or role named in a word or two: border in its colour, faint tint, WHITE text.
    Chips of the same size have the same height. `icon` (any mobject) sits left of the text.
    dashed=True: the dashed YELLOW 'still open' chip (pass color=OPEN)."""
    t = label(s, size, text_color)
    content = VGroup(icon, t).arrange(RIGHT, buff=0.14) if icon is not None else t
    h = max(_line_height(size), content.height) + 2 * pad_y
    b = box(content.width + 2 * pad_x, h, color, dashed=dashed, fill_opacity=fill_opacity,
            radius=h / 2.6)
    content.move_to(b)
    g = Chip(b, content)
    g.box, g.text, g.icon = b, t, icon
    return g


def split_chip(s: str, left: str = USER, right: str = AGENT, size: float = SMALL,
               pad_x: float = 0.26, pad_y: float = 0.13) -> Chip:
    """A chip whose left half is one role's colour and right half another's ('who did what')."""
    t = label(s, size, INK)
    h = _line_height(size) + 2 * pad_y
    w = t.width + 2 * pad_x
    shape = RoundedRectangle(width=w, height=h, corner_radius=h / 2.6)
    cx = shape.get_center()[0]
    halves = VGroup()
    for col, side in ((left, LEFT), (right, RIGHT)):      # tinted fills, no stroke (no seam)
        cut = Rectangle(width=w / 2, height=h + 0.1).move_to(shape.get_center() + side * w / 4)
        halves.add(Intersection(shape, cut, stroke_width=0).set_fill(col, 0.18))
    # the outline, split where it crosses the vertical centre line (top and bottom)
    ps = np.linspace(0, 1, 721)
    xs = np.array([shape.point_from_proportion(p)[0] - cx for p in ps])
    cross = [ps[i] for i in range(len(ps) - 1) if xs[i] == 0 or xs[i] * xs[i + 1] < 0][:2]
    a, b = sorted(cross)
    seg1 = shape.get_subcurve(a, b)
    seg2 = VGroup(shape.get_subcurve(b, 1), shape.get_subcurve(0, a))
    for seg in (seg1, seg2):
        seg.set_fill(opacity=0).set_stroke(left if seg.get_center()[0] < cx else right, 2.5)
    halves.add(seg1, seg2)
    t.move_to(shape)
    g = Chip(halves, t)
    g.box, g.text, g.icon = halves, t, None
    return g


def tag(s: str, color: str = TOOL, size: float = TAG, text_color: str | None = None,
        dashed: bool = False, icon=None) -> Chip:
    """A small rounded tag ON something (a status, a source): text in the tag's colour, an
    opaque dark fill so it reads on top of images."""
    t = label(s, size, text_color or color)
    content = VGroup(icon, t).arrange(RIGHT, buff=0.12) if icon is not None else t
    h = max(_line_height(size), content.height) + 0.2
    b = RoundedRectangle(width=content.width + 0.4, height=h, corner_radius=h / 2,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    if dashed:
        b = VGroup(b.copy().set_stroke(width=0),
                   DashedVMobject(b, num_dashes=max(14, int((b.width + h) * 7)), dashed_ratio=0.55)
                   .set_stroke(color, 2.5))
    content.move_to(b)
    g = Chip(b, content)
    g.box, g.text, g.icon = b, t, icon
    return g


def recon_tag(s: str = RECON) -> Chip:
    """GREY 'reconstruction' tag (22 pt): every redrawn picture of something that no longer exists
    carries it, top-right (pin_to_corner(tag, target))."""
    return tag(s, TOOL)


def rerender_tag() -> Chip:
    """The tag for frames of the A03 re-render: 're-rendered from the old code (commit 8a922bf)'."""
    return tag(RERENDER, TOOL)


def open_tag(s: str = NOT_VERIFIED) -> Chip:
    """Dashed YELLOW tag: 'not yet verified' (default) or IDEA ('idea · not built yet')."""
    return tag(s, OPEN, dashed=True)


def measured_badge(s: str, size: float = TAG) -> Chip:
    """GREEN 'measured check' badge: a check mark and a short text."""
    return tag(s, MEASURED, size=size, icon=check_mark(0.24))


def bug_tag(s: str, size: float = TAG) -> Chip:
    """RED tag for a bug or a failure."""
    return tag(s, BUG, size=size)


def pin_to_corner(m, target, corner=UR, buff: float = 0.12):
    """Move m inside target's corner (tags on exhibits: corner=UR)."""
    return m.move_to(target.get_corner(corner) - corner * (np.array([m.width, m.height, 0]) / 2 + buff))


# ------------------------------------------------------------------ glyphs (drawn from primitives)
def check_mark(height: float = 0.3, color: str = MEASURED, stroke: float = 5) -> VMobject:
    """A ✓ drawn as one stroke."""
    h = height
    m = VMobject(stroke_color=color, stroke_width=stroke)
    m.set_points_as_corners([[-0.5 * h, 0.05 * h, 0], [-0.15 * h, -0.4 * h, 0], [0.55 * h, 0.45 * h, 0]])
    return m


def cross_mark(height: float = 0.3, color: str = BUG, stroke: float = 5) -> VGroup:
    """A ✗ drawn as two strokes."""
    h = height / 2
    return VGroup(Line([-h, -h, 0], [h, h, 0]), Line([-h, h, 0], [h, -h, 0])).set_stroke(color, stroke)


def ai_badge(height: float = 0.42, color: str = AGENT) -> VGroup:
    """The small 'AI' badge for agent icons (text stays at 20 pt or more)."""
    t = S.text("AI", 20, INK, font=SANS, weight="BOLD")
    b = RoundedRectangle(width=max(height * 1.45, t.width + 0.2), height=height,
                         corner_radius=height / 3, stroke_color=color, stroke_width=2.5)
    b.set_fill(S.BG, 1)
    t.move_to(b)
    return VGroup(b, t)


class RoleIcon(VGroup):
    """role_icon(...): .person, .badge (None for the user), .role."""


def role_icon(role: str = "agent", height: float = 1.0) -> RoleIcon:
    """A person glyph in the role's colour. "user" (PINK, no badge), "agent" (BLUE + AI badge),
    "sub" (faded BLUE + AI badge, for sub-agents and AI reviewers)."""
    col = ROLE_COLOR[role]
    p = person_icon(col, height)
    g = RoleIcon(p)
    g.person, g.badge, g.role = p, None, role
    if role in ("agent", "sub"):
        b = ai_badge(max(0.42, height * 0.36), AGENT if role == "agent" else SUB_AGENT_TEXT)
        b.move_to(p.get_corner(DR) + np.array([0.02, 0.12, 0]))
        g.add(b)
        g.badge = b
    return g


def sub_agent_cluster(n: int = 7, height: float = 0.42, cols: int = 4, badge: bool = True) -> VGroup:
    """A small crowd of faded-BLUE icons (sub-agents), with one AI badge for the group."""
    icons = VGroup(*[person_icon(SUB_AGENT, height) for _ in range(n)])
    icons.arrange_in_grid(cols=cols, buff=(0.1, 0.12))
    g = VGroup(icons)
    g.icons = icons
    if badge:
        b = ai_badge(0.42, SUB_AGENT_TEXT).move_to(icons.get_corner(DR) + np.array([0.1, 0.0, 0]))
        g.add(b)
        g.badge = b
    return g


def headphones(height: float = 0.8, color: str = TOOL, stroke: float = 6) -> VGroup:
    """Headphones: a head band and two ear cups."""
    w = height * 1.05
    band = Arc(radius=w / 2, start_angle=0, angle=PI, stroke_color=color, stroke_width=stroke)
    cups = VGroup(*[RoundedRectangle(width=w * 0.22, height=height * 0.42, corner_radius=w * 0.08,
                                     stroke_width=0).set_fill(color, 1)
                    .move_to(band.get_center() + np.array([sx * w / 2, -height * 0.12, 0]))
                    for sx in (-1, 1)])
    g = VGroup(band, cups)
    return g.move_to(ORIGIN)


def play_button(height: float = 0.8, color: str = TOOL, stroke: float = 5) -> VGroup:
    """A play button: a ring with a triangle."""
    ring = Circle(radius=height / 2, stroke_color=color, stroke_width=stroke)
    tri = Triangle(stroke_width=0).set_fill(color, 1).rotate(-PI / 2).scale_to_fit_height(height * 0.42)
    tri.move_to(ring).shift(RIGHT * height * 0.04)
    return VGroup(ring, tri)


def pause_icon(height: float = 0.3, color: str = TOOL) -> VGroup:
    """Two bars."""
    bars = VGroup(*[Rectangle(width=height * 0.28, height=height, stroke_width=0).set_fill(color, 1)
                    for _ in range(2)])
    return bars.arrange(RIGHT, buff=height * 0.22)


def strike(m, color: str = BUG, stroke: float = 7, pad: float = 0.12) -> Line:
    """A RED stroke through m, lower-left to upper-right ('can't')."""
    return Line(m.get_corner(DL) + np.array([-pad, -pad, 0]), m.get_corner(UR) + np.array([pad, pad, 0]),
                color=color, stroke_width=stroke)


def cant_hear_or_play(height: float = 0.75, gap: float = 0.45) -> VGroup:
    """The motif of the video: GREY headphones and play button, each struck through in RED.
    Returns VGroup(VGroup(headphones, strike), VGroup(play, strike))."""
    hp, pl = headphones(height), play_button(height)
    VGroup(hp, pl).arrange(RIGHT, buff=gap)
    return VGroup(VGroup(hp, strike(hp)), VGroup(pl, strike(pl)))


def pen(height: float = 0.6, color: str = AGENT) -> VGroup:
    """A pen (writing a file): body and nib, tilted."""
    body = RoundedRectangle(width=0.16, height=0.62, corner_radius=0.05, stroke_width=0).set_fill(color, 1)
    nib = Polygon([-0.08, 0, 0], [0.08, 0, 0], [0, -0.17, 0], stroke_width=0).set_fill(color, 1)
    nib.next_to(body, DOWN, buff=0.02)
    g = VGroup(body, nib).scale_to_fit_height(height).rotate(-PI / 5)
    return g


class Clock(VGroup):
    """clock(): .face, .minute, .hour; animate with Rotate(c.minute, -TAU, about_point=c.center)."""


def clock(radius: float = 0.4, color: str = TOOL, stroke: float = 4) -> Clock:
    face = Circle(radius=radius, stroke_color=color, stroke_width=stroke)
    ticks = VGroup(*[Line(UP * radius * 0.78, UP * radius * 0.92, stroke_width=2.5, color=color)
                     .rotate(-k * PI / 6, about_point=ORIGIN) for k in range(12)])
    minute = Line(ORIGIN, UP * radius * 0.75, stroke_width=stroke, color=color)
    hour = Line(ORIGIN, UP * radius * 0.48, stroke_width=stroke + 1, color=color).rotate(-PI / 3, about_point=ORIGIN)
    c = Clock(face, ticks, hour, minute)
    c.face, c.minute, c.hour = face, minute, hour
    return c


def file_icon(height: float = 0.5, color: str = TOOL) -> VGroup:
    """A page with a folded corner."""
    w, h, f = height * 0.78, height, height * 0.26
    page = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - f, 0], [w / 2 - f, h / 2, 0],
                   [-w / 2, h / 2, 0], stroke_color=color, stroke_width=2.5).set_fill(PANEL, 1)
    fold = Polygon([w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0], [w / 2, h / 2 - f, 0],
                   stroke_color=color, stroke_width=2).set_fill(color, 0.5)
    lines = VGroup(*[Line([-w * 0.3, y, 0], [w * 0.3, y, 0], stroke_width=2, color=color)
                     for y in (-h * 0.25, -h * 0.05, h * 0.15)])
    return VGroup(page, fold, lines)


class Player(VGroup):
    """video_player(): .frame, .screen (where the picture goes), .bar, .knob, .pause.
    A real frame goes in with player.show(name, crop=..., tag_m=...) -> an Exhibit sized to the
    screen (crop to the screen's aspect); player.hold(mob) centres any other mobject on it."""

    def show(self, name: str, crop: tuple | None = None, tag_m=None) -> "Exhibit":
        ex = exhibit(name, width=self.screen.width, crop=crop)
        ex.move_to(self.screen)
        if tag_m is not None:
            pin_to_corner(tag_m, ex.frame, UR, buff=0.1)
            ex.add(tag_m)
            ex.tag = tag_m
        return ex

    def hold(self, m):
        return m.move_to(self.screen)

    def at(self, fraction: float):
        """Point on the scrubber at `fraction` (0..1)."""
        return self.bar.point_from_proportion(np.clip(fraction, 0, 1))


def video_player(screen_width: float = 9.0, aspect: float = 16 / 9, progress: float = 0.18,
                 color: str = TOOL) -> Player:
    """A GREY video-player frame: rounded frame, the screen, a pause icon and a scrubber."""
    sw, sh = screen_width, screen_width / aspect
    bar_h = 0.5
    frame = RoundedRectangle(width=sw + 0.3, height=sh + bar_h + 0.3, corner_radius=0.18,
                             stroke_color=color, stroke_width=2.5).set_fill(S.BG, 1)
    screen = Rectangle(width=sw, height=sh, stroke_width=0).set_fill(S.BG, 0)
    screen.move_to(frame.get_top() + DOWN * (0.15 + sh / 2))
    y = screen.get_bottom()[1] - bar_h / 2 - 0.02
    pz = pause_icon(0.24, color).move_to([screen.get_left()[0] + 0.3, y, 0])
    bar = Line([pz.get_right()[0] + 0.3, y, 0], [screen.get_right()[0] - 0.2, y, 0],
               stroke_width=4, color=S.GREY_DARK)
    done = Line(bar.get_start(), bar.point_from_proportion(progress), stroke_width=4, color=color)
    knob = Dot(done.get_end(), radius=0.08, color=color)
    p = Player(frame, screen, pz, bar, done, knob)
    p.frame, p.screen, p.pause, p.bar, p.done, p.knob = frame, screen, pz, bar, done, knob
    return p


def anchor_pin(color: str = AUDIO, height: float = 0.45, estimated: bool = False) -> VGroup:
    """A map pin for a narration anchor. estimated=True: dashed YELLOW outline (a guess)."""
    head = Circle(radius=height * 0.28).set_fill(color, 1).set_stroke(width=0)
    tip = Polygon([-height * 0.2, 0, 0], [height * 0.2, 0, 0], [0, -height * 0.55, 0], stroke_width=0)
    tip.set_fill(color, 1).next_to(head, DOWN, buff=-height * 0.18)
    g = VGroup(head, tip)
    if estimated:
        g.add(open_outline(g, buff=0.06, stroke=2))
    return g


# ------------------------------------------------------------------ cards
def file_card(name: str, note: str | None = None, color: str = TOOL, size: float = SMALL,
              width: float | None = None, icon_color: str | None = None) -> VGroup:
    """A file: page icon + filename (monospace) [+ a GREY note line]. .box .icon .name .note"""
    ic = file_icon(0.5, icon_color or color)
    nm = mono(name, size, INK)
    lines = VGroup(nm)
    if note:
        lines.add(caption(note, max(CAPTION, size - 4)))
    lines.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    body = VGroup(ic, lines).arrange(RIGHT, buff=0.2)
    w = width or body.width + 0.44
    b = box(w, max(body.height, 0.5) + 0.32, color, fill=PANEL, fill_opacity=1)
    body.move_to(b)
    if width:
        body.align_to(b, LEFT).shift(RIGHT * 0.22)
    g = VGroup(b, body)
    g.box, g.icon, g.name, g.note = b, ic, nm, (lines[1] if note else None)
    return g


def quote_card(text: str, cap: str | None = DICTATED, color: str = USER, size: float = 28,
               chars: int = 34, width: float | None = None) -> VGroup:
    """The user's words (exact text from QUOTES), in a PINK card, with its caption below.
    text is wrapped at `chars` characters. .box .quote .caption"""
    q = label("“" + wrap(text, chars).replace("\n", "\n ") + "”", size, INK, line_spacing=1.0)
    w = width or q.width + 0.7
    b = box(w, q.height + 0.55, color, fill_opacity=0.12, radius=0.2)
    q.move_to(b)
    g = VGroup(b, q)
    g.box, g.quote, g.caption = b, q, None
    if cap:
        c = caption(cap).next_to(b, DOWN, buff=0.12).align_to(b, RIGHT)
        g.add(c)
        g.caption = c
    return g


def speech_bubble(text: str, color: str = SUB_AGENT_TEXT, size: float = SMALL, chars: int = 30,
                  tail: np.ndarray = DOWN + LEFT, quote: bool = True,
                  tail_shift: float | None = None) -> VGroup:
    """A speech bubble (an AI reviewer's note, exact text). The tail points `tail` from the box
    (DOWN, DOWN+LEFT, LEFT, ...). For a tail out of the bottom/top edge, tail_shift (-0.5..0.5,
    a fraction of the width from the centre) sets where it leaves the edge, so its tip can sit
    right over the speaker: bubble.shift(icon.get_top() + UP*0.1 - bubble.tail.get_vertices()[2]).
    .box .text .tail"""
    body = wrap(text, chars)
    t = label(("“" + body + "”") if quote else body, size, INK, line_spacing=1.0)
    b = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.42, corner_radius=0.22,
                         stroke_color=color, stroke_width=2.5).set_fill(S.BG, 0.95)
    t.move_to(b)
    d = np.array(tail, dtype=float)
    d /= np.linalg.norm(d)
    if abs(d[1]) >= abs(d[0]):              # tail out of the bottom (or top) edge
        f = (0.28 * np.sign(d[0])) if tail_shift is None else tail_shift
        base = b.get_edge_center(DOWN if d[1] < 0 else UP) + RIGHT * f * b.width
        across = RIGHT * 0.17
    else:                                   # tail out of a side
        base = b.get_edge_center(RIGHT if d[0] > 0 else LEFT)
        across = UP * 0.15
    tip = base + d * 0.42
    tl = Polygon(base - across, base + across, tip, stroke_color=color, stroke_width=2.5)
    tl.set_fill(S.BG, 0.95)
    cover = Line(base - across * 0.85, base + across * 0.85, color=S.BG, stroke_width=5)  # opens the seam
    g = VGroup(tl, b, cover, t)
    g.box, g.text, g.tail = b, t, tl
    return g


def subtitle_band(zh_line: str, en_line: str, width: float = 10.0, zh_size: float = 30,
                  en_size: float = 22, fill: str = "#050608") -> VGroup:
    """The burned-in band of the Chinese videos: the Chinese line, and a smaller GREY English line
    under it, on a dark band. zh_line must be space-free. .band .zh .en"""
    c = zh(zh_line, zh_size, INK)
    e = S.text(en_line, en_size, S.GREY, font=SANS)
    lines = VGroup(c, e).arrange(DOWN, buff=0.12)
    band = Rectangle(width=width, height=lines.height + 0.4, stroke_width=0).set_fill(fill, 1)
    lines.move_to(band)
    g = VGroup(band, lines)
    g.band, g.zh, g.en = band, c, e
    return g


def cost_label_lines() -> list[str]:
    """LIVE's cost label, split into its two lines at ' · ' (never reworded)."""
    return LIVE["cost_label"].split(" · ")


def cost_card(value: float | None = None, size: float = 72) -> VGroup:
    """The session cost counter, ALWAYS with its full label (the user's binding wording).
    .number is a DecimalNumber: animate it with ChangeDecimalToValue(card.number, LIVE['cost_usd']).
    Start it at 0 (value=0) to count up; the default shows the live value."""
    v = LIVE["cost_usd"] if value is None else value
    dollar = S.text("$", size * 0.85, INK)
    num = DecimalNumber(v, num_decimal_places=2, group_with_commas=True, font_size=size, color=INK)
    head = VGroup(dollar, num).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
    num.add_updater(lambda m: m.next_to(dollar, RIGHT, buff=0.08).align_to(dollar, DOWN))
    lab = VGroup(*[label(s, SMALL, S.GREY) for s in cost_label_lines()]).arrange(DOWN, buff=0.1)
    body = VGroup(head, lab).arrange(DOWN, buff=0.3)
    b = box(max(body.width, 5.0) + 0.8, body.height + 0.6, TOOL, fill=PANEL, fill_opacity=1, radius=0.2)
    body.move_to(b)
    g = VGroup(b, head, lab)
    g.box, g.number, g.label = b, num, lab
    return g


# ------------------------------------------------------------------ real images
class Exhibit(Group):
    """exhibit(): .image, .frame, .tag (or None). Map pixel coordinates of the ORIGINAL png onto
    the screen with .px(x, y) and .px_box(x0, y0, x1, y1) (an invisible Rectangle there, to
    Circumscribe / underline / point at a detail)."""

    def px(self, x: float, y: float) -> np.ndarray:
        x0, y0, x1, y1 = self.crop
        ul = self.image.get_corner(UL)
        return ul + np.array([(x - x0) / (x1 - x0) * self.image.width, -(y - y0) / (y1 - y0) * self.image.height, 0])

    def px_box(self, x0: float, y0: float, x1: float, y1: float, color: str = EMPHASIS) -> Rectangle:
        a, b = self.px(x0, y0), self.px(x1, y1)
        r = Rectangle(width=abs(b[0] - a[0]), height=abs(b[1] - a[1]), stroke_width=0, color=color)
        return r.move_to((a + b) / 2)


@lru_cache(maxsize=64)
def _pixels(name: str, crop: tuple | None):
    from PIL import Image
    im = Image.open(asset(name)).convert("RGB")
    if crop:
        im = im.crop(tuple(int(round(c)) for c in crop))
    return np.asarray(im), im.size


def exhibit(name: str, height: float | None = None, width: float | None = None,
            crop: tuple | None = None, tag_m=None, frame_color: str = TOOL) -> Exhibit:
    """A REAL image from assets/ in a thin GREY frame (an exhibit, not this video's colour code).
    crop = (x0, y0, x1, y1) in pixels of the original png zooms on a detail. tag_m (e.g.
    recon_tag(), rerender_tag()) is pinned inside the top-right corner. Pair it with a
    source_caption(). Returns an Exhibit (a Group: Images can't go in a VGroup)."""
    arr, (w0, h0) = _pixels(name, tuple(crop) if crop else None)
    img = ImageMobject(arr)
    if width is not None:
        img.scale_to_fit_width(width)
    else:
        img.scale_to_fit_height(height or 5.0)
    frame = Rectangle(width=img.width, height=img.height, stroke_color=frame_color, stroke_width=2)
    frame.move_to(img)
    g = Exhibit(img, frame)
    g.image, g.frame, g.tag, g.name = img, frame, None, name
    g.crop = tuple(crop) if crop else (0, 0, w0, h0)
    if tag_m is not None:
        pin_to_corner(tag_m, frame, UR, buff=0.1)
        g.add(tag_m)
        g.tag = tag_m
    return g


def source_caption(s: str, size: float = CAPTION) -> VMobject:
    """GREY 20 pt source caption in the bottom-left corner ("real contact sheet · tic-tac-toe
    video, scene 3"). Re-place with .next_to(...) when a SHOW line puts it under an exhibit."""
    c = caption(s, size)
    return c.move_to([-6.5 + c.width / 2, -3.5 + c.height / 2, 0])


def gloss(s: str, target, direction=RIGHT, color: str = TOOL, size: float = SMALL,
          length: float = 0.9, buff: float = 0.12) -> VGroup:
    """A GREY gloss arrow: text at the tail, arrow pointing at `target` from `direction`."""
    d = np.array(direction, dtype=float)
    d /= np.linalg.norm(d)
    end = target.get_critical_point(d) + d * buff
    start = end + d * length
    arr = Arrow(start, end, buff=0, color=color, stroke_width=3, tip_length=0.16,
                max_tip_length_to_length_ratio=0.3)
    t = label(s, size, color)
    t.next_to(start, d, buff=0.1)
    g = VGroup(arr, t)
    g.arrow, g.text = arr, t
    return g


# ------------------------------------------------------------------ code (the toolkit's code style)
def _house_code_style():
    """Monokai with light comments (the house style of the other videos' code panels)."""
    from pygments.styles import get_style_by_name
    from pygments.token import Comment
    base = get_style_by_name("monokai")
    return type("HouseCodeStyle", (base,), {"styles": {**base.styles, Comment: "#D9D3B8",
                                                        Comment.Single: "#D9D3B8"}})


HOUSE_CODE_STYLE = _house_code_style()


def code_block(source: str, font_size: float = 24, width: float | None = None,
               language: str = "python") -> Code:
    """Real code in the house style: monokai (light comments) on a dark rounded panel, DejaVu Sans
    Mono. `width` scales the whole panel (keep the text >= 20 pt on screen)."""
    c = Code(code_string=source, language=language, formatter_style=HOUSE_CODE_STYLE,
             add_line_numbers=False, background="rectangle",
             background_config={"fill_color": S.GREY_DARKER, "stroke_color": S.GREY_DARK,
                                "stroke_width": 2, "corner_radius": 0.15},
             paragraph_config={"font_size": font_size, "font": MONO})
    if width is not None:
        c.scale_to_fit_width(width)
    c.source = source
    return c


def code_line(code: Code, k: int):
    return code.code_lines[k]


def code_span(code: Code, k: int, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of substring `sub` in line k of a code block (to colour or circle it).
    Spaces have no glyphs, so the index counts only visible characters."""
    line = code.source.split("\n")[k]
    i = -1
    for _ in range(occurrence + 1):
        i = line.find(sub, i + 1)
    if i < 0:
        raise ValueError(f"{sub!r} not in line {k}: {line!r}")
    start = len("".join(line[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*code.code_lines[k][start:start + n])


def line_bar(code: Code, k: int, color: str = EMPHASIS, opacity: float = 0.16) -> Rectangle:
    """A translucent bar over line k (add it after the code)."""
    ln, bg = code.code_lines[k], code.background
    return Rectangle(width=bg.width - 0.12, height=ln.height + 0.14, stroke_width=0) \
        .set_fill(color, opacity).move_to([bg.get_center()[0], ln.get_center()[1], 0])


def code_panel(source: str, path: str, first_line: int, focus=None, font_size: float = 24,
               width: float | None = None, dim: float = 0.3) -> VGroup:
    """A real excerpt with its GREY caption "path · lines a–b" underneath. Lines not in `focus`
    (0-based indices) are faded, so the panel shows one or two lines (script.md convention).
    .code .caption"""
    c = code_block(source, font_size, width)
    n = len(source.split("\n"))
    if focus is not None:
        keep = {focus} if isinstance(focus, int) else set(focus)
        for k in range(n):
            if k not in keep and k < len(c.code_lines):
                c.code_lines[k].set_opacity(dim)
    last = first_line + n - 1
    lines = f"line {first_line}" if n == 1 else f"lines {first_line}–{last}"
    cap = caption(f"{path} · {lines}").next_to(c, DOWN, buff=0.12).align_to(c, LEFT)
    g = VGroup(c, cap)
    g.code, g.caption = c, cap
    return g


def terminal(lines, width: float | None = None, size: float = SMALL, title: str = "terminal") -> VGroup:
    """A terminal window. lines = [("$ python assets/play_all_games.py", TOOL), ("255168", MEASURED)]
    (strings default to WHITE). .box .lines"""
    rows = VGroup(*[mono(s, size, col) if isinstance(s, str) else s
                    for s, col in [(x, INK) if isinstance(x, str) else x for x in lines]])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    w = width or rows.width + 0.6
    top = 0.36
    b = RoundedRectangle(width=w, height=rows.height + 0.5 + top, corner_radius=0.14,
                         stroke_color=S.GREY_DARK, stroke_width=2).set_fill("#090A0D", 1)
    bar = Line(b.get_corner(UL) + DOWN * top, b.get_corner(UR) + DOWN * top, color=S.GREY_DARK, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.055, color=S.GREY_DARK) for _ in range(3)]).arrange(RIGHT, buff=0.1)
    dots.move_to(b.get_corner(UL) + np.array([0.35, -top / 2, 0]))
    rows.move_to(b.get_center() + DOWN * top / 2).align_to(b, LEFT).shift(RIGHT * 0.3)
    g = VGroup(b, bar, dots, rows)
    g.box, g.lines = b, rows
    return g


# ------------------------------------------------------------------ data drawings
class TimeAxis(VGroup):
    """time_axis(): .x_of("2026-10-05 21:53") -> x; .point(t, dy=0) -> a point on the axis."""


def _t(s) -> dt.datetime:
    return s if isinstance(s, dt.datetime) else dt.datetime.fromisoformat(str(s))


def time_axis(start: str, end: str, width: float = 12.0, ticks=(), color: str = TOOL,
              size: float = CAPTION, tick_h: float = 0.12) -> TimeAxis:
    """A horizontal time axis (UTC). ticks = [("Oct 4", "2026-10-04 00:00"), ...] labelled below."""
    t0, t1 = _t(start), _t(end)
    line = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=2)
    g = TimeAxis(line)

    def x_of(t) -> float:
        f = (_t(t) - t0).total_seconds() / max(1.0, (t1 - t0).total_seconds())
        return line.get_start()[0] + f * (line.get_end()[0] - line.get_start()[0])

    def point(t, dy: float = 0.0):
        return np.array([x_of(t), line.get_center()[1] + dy, 0])

    g.x_of, g.point, g.line = x_of, point, line
    marks = VGroup()
    for lab, t in ticks:
        x = x_of(t)
        y = line.get_center()[1]
        marks.add(VGroup(Line([x, y - tick_h, 0], [x, y + tick_h, 0], color=color, stroke_width=2),
                         caption(lab, size, color).move_to([x, y - 0.32, 0])))
    g.add(marks)
    g.marks = marks
    return g


def load_envelope(name: str = "ttt_s03_say1_env.csv") -> tuple[np.ndarray, np.ndarray]:
    """(t, rms) arrays of an envelope CSV in assets/ (one row per 20 ms)."""
    rows = asset(name).read_text().strip().splitlines()[1:]
    a = np.array([[float(v) for v in r.split(",")] for r in rows])
    return a[:, 0], a[:, 1]


def waveform(values, width: float = 11.0, height: float = 1.2, color: str = AUDIO,
             step: int = 2, gamma: float = 0.6) -> VMobject:
    """A filled, mirrored waveform drawn from envelope values (e.g. load_envelope()[1]).
    One polygon (not thousands of bars). The x axis is linear in time: x = left + width * i / n."""
    v = np.asarray(values, dtype=float)[::step]
    v = (v / max(1e-9, v.max())) ** gamma * height / 2
    xs = np.linspace(-width / 2, width / 2, len(v))
    top = [[x, max(y, 0.015), 0] for x, y in zip(xs, v)]
    bot = [[x, -max(y, 0.015), 0] for x, y in zip(xs[::-1], v[::-1])]
    m = VMobject(stroke_width=0).set_points_as_corners(top + bot + [top[0]])
    return m.set_fill(color, 0.85)


# ------------------------------------------------------------------ motion helpers
def emphasize(m, run_time: float = 1.0, circle: bool = False):
    """WHITE emphasis (script.md: never highlight_box): Circumscribe for pictures and regions,
    Indicate for text."""
    if circle or isinstance(m, (Rectangle,)) and m.get_stroke_width() == 0:
        return Circumscribe(m, color=EMPHASIS, buff=0.08, run_time=run_time, time_width=0.5)
    return Indicate(m, color=EMPHASIS, scale_factor=1.08, run_time=run_time)


def pulse(m, scale: float = 1.1, run_time: float = 0.6):
    """Grow and settle back, keeping m's colours (for chips 'pulsing as they are named')."""
    return m.animate(rate_func=there_and_back, run_time=run_time).scale(scale)


def ponder_in(scene, question: str, run_time: float = 0.6, **kw) -> VGroup:
    """Bring in the toolkit's standard ponder card (call it at vo.wait_until("Pause"), inside the
    SAY block, so the question is on screen when the viewer pauses)."""
    card = ponder_card(question, **kw)
    scene.play(FadeIn(card, scale=0.95), run_time=run_time)
    return card


def ponder_drain(scene, card: VGroup, seconds: float) -> None:
    """After the SAY block: drain the card's timer bar over `seconds` (silent), the same motion as
    the toolkit's pause_and_ponder. Fade the card at the start of the next block."""
    bar = card[3]
    scene.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
               run_time=seconds)


def _leaves(mobs):
    for m in mobs:
        if isinstance(m, (VMobject, ImageMobject)):
            yield m
        else:                                   # a Group (e.g. an Exhibit): go inside
            yield from _leaves(m.submobjects)


def dim(*mobs, opacity: float = 0.4) -> list:
    """Animations that dim mobjects (and Groups with images) to `opacity` of what they are now,
    keeping each part's own opacity ratios (tinted fills stay tinted). Undo with undim(...)."""
    anims = []
    for m in _leaves(mobs):
        m.save_state()
        anims.append(m.animate.set_opacity(opacity) if isinstance(m, ImageMobject) else m.animate.fade(1 - opacity))
    return anims


def undim(*mobs) -> list:
    """Animations that bring back what dim(...) dimmed."""
    from manim import Restore
    return [Restore(m) for m in _leaves(mobs)]


def gather(scene, *mobs) -> Group:
    """Make several on-screen mobjects ONE top-level group before animating or transforming them
    together, so no stray copy stays behind (Transform of a group whose parts were added one by
    one leaves the parts on screen)."""
    for m in mobs:
        scene.remove(m)
    g = VGroup(*mobs) if all(isinstance(m, VMobject) for m in mobs) else Group(*mobs)
    scene.add(g)
    return g


def fade_out_all(scene, run_time: float = 0.8) -> None:
    """End a scene on an empty frame."""
    mobs = [m for m in scene.mobjects]
    if mobs:
        scene.play(FadeOut(Group(*mobs)), run_time=run_time)
