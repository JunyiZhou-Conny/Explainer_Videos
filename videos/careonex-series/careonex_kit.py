"""Shared visual kit for the CareOneX explainer series (every episode imports it).

One look for the whole series, so a viewer who has seen one episode reads the next at a glance.
Semantic colours (SERIES.md, "Fixed visual language"):

    our own code, one container per service ... CODE_C  (BLUE)    rounded box tagged CONTAINER
    stored data: S3 prefixes, files, chunks ... DATA_C  (GREEN)   box tagged S3 / file glyph
    AWS managed: Bedrock models, KB, vectors .. AWS_C   (ORANGE)  box tagged BEDROCK / AWS
    a person (caller, teammate) ............... PERSON_C (WHITE)
    a question / search query ................. QUERY_C (YELLOW)
    failure modes, bugs ....................... BAD_C   (RED)
    branches by person ........................ PEOPLE[...]

Each episode's scenes/common.py puts this folder on sys.path:

    SERIES = Path(__file__).resolve().parents[2] / "careonex-series"
    sys.path.insert(0, str(SERIES))
    from careonex_kit import *
"""

from __future__ import annotations

import numpy as np
from manim import (DOWN, LEFT, ORIGIN, RIGHT, UP, Arrow, Circle, Code, CurvedArrow, DashedLine,
                   DashedVMobject, Dot, FadeIn, FadeOut, Line, MoveAlongPath, Polygon, Rectangle,
                   RoundedRectangle, SurroundingRectangle, Text, VGroup, VMobject, Write, linear)

from explainer import style as S

# ------------------------------------------------------------------ fonts
MONO = "DejaVu Sans Mono"          # identifiers: container names, prefixes, files, code, JSON
SANS = S.FONT_SANS                 # small tags (CONTAINER, S3 ...)
SERIF = S.FONT                     # prose captions (3b1b house font)

# ------------------------------------------------------------------ semantic colours
CODE_C = S.BLUE
DATA_C = S.GREEN
AWS_C = S.ORANGE
PERSON_C = S.WHITE
QUERY_C = S.YELLOW
BAD_C = S.RED
OK_C = S.GREEN
DIM = S.GREY
PEOPLE = {"Nadir": S.GOLD, "Caroline": S.PINK, "Junyi": S.PURPLE, "Marco": S.TEAL, "Helen": S.GREY}


# ------------------------------------------------------------------ text helpers
def mono(s: str, size: float = 24, color: str = S.WHITE, **kw) -> Text:
    return Text(s, font=MONO, font_size=size, color=color, **kw)


def sans(s: str, size: float = 22, color: str = S.WHITE, **kw) -> Text:
    return Text(s, font=SANS, font_size=size, color=color, **kw)


def serif(s: str, size: float = 30, color: str = S.WHITE, **kw) -> Text:
    return S.text(s, size, color, **kw)


def caption(s: str, size: float = 30, color: str = S.WHITE) -> Text:
    """A one-line caption at the bottom of the picture (the subtitle band sits below the frame)."""
    return serif(s, size, color).to_edge(DOWN, buff=0.4)


def title(s: str, size: float = 44, color: str = S.WHITE) -> Text:
    return serif(s, size, color).to_edge(UP, buff=0.45)


# ------------------------------------------------------------------ boxes
def tag_box(tag: str, name: str, sub: str | None = None, color: str = CODE_C, width: float = 2.6,
            height: float | None = None, name_size: float = 26, sub_size: float = 20,
            tag_size: float = 20, fill: float = 0.10) -> VGroup:
    """The series' box: a small coloured TAG over a monospace NAME and an optional serif SUB line.

    Returns VGroup(frame, tag, name[, sub]); address parts as box.frame, box.tag, box.name, box.sub."""
    tag_m = sans(tag.upper(), tag_size, color)
    name_m = mono(name, name_size, S.WHITE)
    rows = [tag_m, name_m]
    sub_m = None
    if sub:
        sub_m = serif(sub, sub_size, S.GREY)
        rows.append(sub_m)
    inner = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    pad = 0.15
    if inner.width > width - 2 * pad:
        inner.scale_to_fit_width(width - 2 * pad)
    if height is not None and inner.height > height - 2 * pad:
        inner.scale_to_fit_height(height - 2 * pad)
    h = height or inner.height + 2 * pad + 0.1
    frame = RoundedRectangle(width=width, height=h, corner_radius=0.14, stroke_color=color,
                             stroke_width=2.5).set_fill(color, fill)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * pad)
    box = VGroup(frame, *rows)
    box.frame, box.tag, box.name, box.sub = frame, tag_m, name_m, sub_m
    return box


def container(name: str, sub: str | None = None, **kw) -> VGroup:
    return tag_box("container", name, sub, CODE_C, **kw)


def store(name: str, sub: str | None = None, tag: str = "S3", **kw) -> VGroup:
    return tag_box(tag, name, sub, DATA_C, **kw)


def aws(tag: str, name: str, sub: str | None = None, **kw) -> VGroup:
    return tag_box(tag, name, sub, AWS_C, **kw)


def person_box(name: str, sub: str | None = None, **kw) -> VGroup:
    return tag_box("person", name, sub, PERSON_C, fill=0.0, **kw)


def dim(box, opacity: float = 0.4):
    """Fade a tag_box (or any group) without lighting up its fill: strokes and text at `opacity`,
    box fills nearly transparent. Returns the box."""
    for m in box.get_family():
        if isinstance(m, RoundedRectangle):
            m.set_stroke(opacity=opacity).set_fill(opacity=0.03)
        elif isinstance(m, Text):
            m.set_opacity(opacity)
    return box


def chip(label: str, color: str = S.GREY, size: float = 22, mono_font: bool = True,
         fill: float = 0.18) -> VGroup:
    """A small rounded pill with a label (a field, a flag, a status)."""
    t = mono(label, size, S.WHITE) if mono_font else serif(label, size, S.WHITE)
    bg = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.12,
                          stroke_color=color, stroke_width=2).set_fill(color, fill)
    bg.move_to(t)
    g = VGroup(bg, t)
    g.bg, g.label = bg, t
    return g


def doc_glyph(color: str = DATA_C, width: float = 0.5, height: float = 0.66, lines: int = 4,
              label: str | None = None, label_size: float = 20) -> VGroup:
    """A page with a folded corner (a document, a file, a chunk)."""
    f = 0.16 * width / 0.5
    w, h = width, height
    page = Polygon([-w / 2, h / 2, 0], [w / 2 - f, h / 2, 0], [w / 2, h / 2 - f, 0], [w / 2, -h / 2, 0],
                   [-w / 2, -h / 2, 0], stroke_color=color, stroke_width=2).set_fill(color, 0.15)
    fold = VMobject(stroke_color=color, stroke_width=2).set_points_as_corners(
        [[w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0], [w / 2, h / 2 - f, 0]])
    rows = VGroup(*[Line([-w / 2 + 0.09, 0, 0], [w / 2 - 0.09 - (0.12 if i == lines - 1 else 0), 0, 0],
                         stroke_color=color, stroke_width=1.5).set_opacity(0.7)
                    for i in range(lines)])
    rows.arrange(DOWN, buff=(h - 0.3) / max(1, lines)).move_to(page).shift(DOWN * 0.04)
    g = VGroup(page, fold, rows)
    if label:
        g.add(mono(label, label_size, S.WHITE).next_to(page, DOWN, buff=0.1))
    return g


def bucket_frame(mobs, label: str, color: str = DATA_C, buff: float = 0.3, size: float = 20) -> VGroup:
    """A dashed frame around stored-data boxes, labelled like 'S3 BUCKET · ac215-program-kb-…'."""
    r = SurroundingRectangle(mobs, buff=buff, corner_radius=0.18, stroke_color=color, stroke_width=2)
    d = DashedVMobject(r, num_dashes=90)
    lab = sans(label, size, color).next_to(r, DOWN, buff=0.1).align_to(r, LEFT).shift(RIGHT * 0.15)
    g = VGroup(d, lab)
    g.rect, g.label = r, lab
    return g


# ------------------------------------------------------------------ arrows and flow
def link(a, b, color: str = S.GREY, label: str | None = None, label_color: str | None = None,
         buff: float = 0.08, stroke: float = 3, tip: float = 0.18, label_size: float = 20,
         label_side=UP, dashed: bool = False) -> VGroup:
    """Edge-to-edge arrow from mobject (or point) a to b, with an optional small label."""
    pa = a if isinstance(a, np.ndarray) else None
    pb = b if isinstance(b, np.ndarray) else None
    if pa is None or pb is None:
        ca = pa if pa is not None else a.get_center()
        cb = pb if pb is not None else b.get_center()
        d = cb - ca
        d = d / (np.linalg.norm(d) or 1)
        if pa is None:
            pa = _boundary(a, d)
        if pb is None:
            pb = _boundary(b, -d)
    arr = Arrow(pa, pb, buff=buff, color=color, stroke_width=stroke, tip_length=tip,
                max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12)
    if dashed:
        arr = VGroup(DashedVMobject(Line(pa, pb, buff=buff + tip * 0.6, stroke_width=stroke, color=color),
                                    num_dashes=12), arr.tip.copy() if hasattr(arr, "tip") else arr)
    g = VGroup(arr)
    g.arrow = arr
    g.label = None
    if label:
        lab = sans(label, label_size, label_color or color)
        lab.next_to(arr, label_side, buff=0.08)
        g.add(lab)
        g.label = lab
    return g


def _boundary(m, direction: np.ndarray) -> np.ndarray:
    """Point where a ray from m's centre in `direction` leaves m's bounding box."""
    c = m.get_center()
    hw, hh = m.width / 2, m.height / 2
    dx, dy = direction[0], direction[1]
    tx = hw / abs(dx) if abs(dx) > 1e-9 else np.inf
    ty = hh / abs(dy) if abs(dy) > 1e-9 else np.inf
    t = min(tx, ty)
    return c + np.array([dx * t, dy * t, 0.0])


def token(color: str = QUERY_C, radius: float = 0.09) -> Dot:
    return Dot(radius=radius, color=color).set_z_index(5)


def travel(scene, mob, path_points, run_time: float = 1.2, fade: bool = True):
    """Move a token along a polyline (list of points), fading it in at the start and out at the end."""
    path = VMobject().set_points_as_corners([np.array(p) for p in path_points])
    mob.move_to(path_points[0])
    if fade:
        scene.play(FadeIn(mob, scale=0.5), run_time=0.2)
    scene.play(MoveAlongPath(mob, path), run_time=run_time, rate_func=linear)
    if fade:
        scene.play(FadeOut(mob, scale=0.5), run_time=0.2)


# ------------------------------------------------------------------ panels (code, JSON, Markdown)
HOUSE_CODE_STYLE = "monokai"


def code_panel(source: str, language: str = "python", size: float = 22, width: float | None = None,
               line_numbers: bool = False) -> Code:
    c = Code(code_string=source, language=language, formatter_style=HOUSE_CODE_STYLE,
             add_line_numbers=line_numbers, background="rectangle",
             background_config={"fill_color": S.GREY_DARKER, "stroke_color": S.GREY_DARK,
                                "stroke_width": 2, "corner_radius": 0.15},
             paragraph_config={"font_size": size, "font": MONO})
    if width is not None:
        c.scale_to_fit_width(width)
    return c


def text_panel(lines: list[str] | str, size: float = 22, color: str = S.WHITE, width: float | None = None,
               border: str = S.GREY_DARK, colors: dict[int, str] | None = None, pad: float = 0.25,
               font: str = MONO, t2c: dict[str, str] | None = None) -> VGroup:
    """Plain monospace lines on a dark rounded panel (file contents, JSON, Markdown, CSV).

    `colors` maps a line index to its colour, `t2c` colours substrings on every line.
    Returns VGroup(bg, rows) with .rows[i] per line."""
    if isinstance(lines, str):
        lines = lines.split("\n")
    # Text drops leading spaces: keep indentation with no-break spaces
    lines = ["\u00a0" * (len(ln) - len(ln.lstrip(" "))) + ln.lstrip(" ") for ln in lines]
    colors = colors or {}
    rows = VGroup(*[Text(ln, font=font, font_size=size, color=colors.get(i, color),
                         t2c={k: v for k, v in (t2c or {}).items() if k in ln}) if ln.strip("\u00a0")
                    else Text("|", font=font, font_size=size).set_opacity(0)   # an empty line keeps its height
                    for i, ln in enumerate(lines)])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12 * size / 22)
    if width is not None and rows.width > width - 2 * pad:
        rows.scale_to_fit_width(width - 2 * pad)
    w = width or rows.width + 2 * pad
    bg = RoundedRectangle(width=w, height=rows.height + 2 * pad, corner_radius=0.14,
                          stroke_color=border, stroke_width=2).set_fill(S.GREY_DARKER, 1)
    rows.move_to(bg).align_to(bg, LEFT).shift(RIGHT * pad)
    g = VGroup(bg, rows)
    g.bg, g.rows = bg, rows
    return g


def mark_ok(size: float = 0.32, color: str = OK_C) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=6).set_points_as_corners(
        [[-0.5, 0.0, 0], [-0.15, -0.38, 0], [0.5, 0.42, 0]])
    return m.scale_to_fit_width(size)


def mark_bad(size: float = 0.28, color: str = BAD_C) -> VGroup:
    h = size / 2
    return VGroup(Line([-h, -h, 0], [h, h, 0], color=color, stroke_width=6),
                  Line([-h, h, 0], [h, -h, 0], color=color, stroke_width=6))


def strike(m, color: str = BAD_C, stroke: float = 5) -> Line:
    return Line(m.get_left() + LEFT * 0.05, m.get_right() + RIGHT * 0.05, color=color, stroke_width=stroke)


def bar_chart(values: list[float], labels: list[str], width: float = 6.0, bar_h: float = 0.26,
              color: str = DATA_C, size: float = 20, gap: float = 0.1, value_fmt: str = "{:g}") -> VGroup:
    """Horizontal bars, longest = `width`, labels right-aligned on the left.

    Returns VGroup(rows); rows[i] = VGroup(label, bar, value)."""
    vmax = max(values) or 1
    labs = [mono(lab, size, S.GREY) for lab in labels]
    lw = max(lab.width for lab in labs)
    pitch = max(bar_h, max(lab.height for lab in labs)) + gap
    rows = VGroup()
    for i, (v, lab) in enumerate(zip(values, labs)):
        y = -i * pitch
        lab.move_to([lw - lab.width / 2, y, 0])
        bar = Rectangle(width=max(0.02, width * v / vmax), height=bar_h, stroke_width=0).set_fill(color, 0.85)
        bar.move_to([lw + 0.2 + bar.width / 2, y, 0])
        val = mono(value_fmt.format(v), size, S.WHITE).next_to(bar, RIGHT, buff=0.12)
        rows.add(VGroup(lab, bar, val))
    return rows.center()


# ------------------------------------------------------------------ the system map
def system_map() -> VGroup:
    """The whole CareOneX system on one screen (both halves), as in the team's diagram.

    Named parts: m.build (top half), m.answer (bottom half), m.part[name] for every box
    ('catalog', 'data', 'ingest', 'extract', 'chunk', 'kb-sync', 'snapshots/', 'raw/', 'text/',
    'chunks/', 'config/', 'bucket', 'kb', 'caller', 'voice', 'nova', 'tools', 'retrieve'),
    m.links[...] for the arrows, m.h1 / m.h2 for the two half headings."""
    part: dict = {}
    W, H = 2.0, 1.08
    xs = [-5.6 + i * 2.24 for i in range(6)]
    y_top = 2.55
    part["catalog"] = store("ragfile_list.csv", "20 public docs", tag="source list", width=W, height=H,
                            name_size=19, sub_size=19)
    subs = {"data": "make the bucket", "ingest": "download", "extract": "file → text",
            "chunk": "text → pieces", "kb-sync": "→ vectors"}
    for k, sub in subs.items():
        part[k] = container(k, sub, width=W, height=H, name_size=24, sub_size=19)
    for x, k in zip(xs, ["catalog", "data", "ingest", "extract", "chunk", "kb-sync"]):
        part[k].move_to([x, y_top, 0])
    y_mid = 1.05
    for x, k in zip(xs[1:], ["snapshots/", "raw/", "text/", "chunks/", "config/"]):
        part[k] = store(k, None, tag="prefix", width=W, height=0.78, name_size=22)
        part[k].move_to([x, y_mid, 0])
    prefixes = VGroup(*[part[k] for k in ["snapshots/", "raw/", "text/", "chunks/", "config/"]])
    part["bucket"] = bucket_frame(prefixes, "S3 BUCKET · ac215-program-kb-<account-id>", buff=0.18, size=18)
    part["kb"] = aws("bedrock knowledge base", "ac215-program-kb", "232 vectors · 1024-d · cosine",
                     width=3.6, height=1.05, name_size=22, sub_size=18)
    part["kb"].move_to([4.45, -0.85, 0])

    y_low = -2.6
    part["caller"] = person_box("caller", "a family", width=1.75, height=1.05, name_size=24, sub_size=19)
    part["voice"] = container("voice", "speech in, out", width=2.0, height=1.05, name_size=24, sub_size=19)
    part["nova"] = aws("bedrock model", "Nova 2 Sonic", "speech to speech", width=2.5, height=1.05,
                       name_size=22, sub_size=19)
    part["retrieve"] = container("retrieve", "HTTP :8080", width=2.0, height=1.05, name_size=24, sub_size=19)
    part["caller"].move_to([-5.75, y_low, 0])
    part["voice"].move_to([-2.95, y_low, 0])
    part["nova"].move_to([-0.35, -1.45, 0])
    part["retrieve"].move_to([4.45, y_low, 0])
    part["tools"] = chip("lookup_program_info", CODE_C, size=19)
    part["tools"].move_to([1.0, y_low, 0])

    links = {}
    chain = ["catalog", "data", "ingest", "extract", "chunk", "kb-sync"]
    for a, b in zip(chain, chain[1:]):
        links[f"{a}>{b}"] = link(part[a], part[b], S.GREY, stroke=2.5, tip=0.14, buff=0.04)
    for a, b in zip(chain[1:], ["snapshots/", "raw/", "text/", "chunks/", "config/"]):
        links[f"{a}>{b}"] = link(part[a].get_bottom(), part[b].get_top(), S.GREY_DARK, stroke=2, tip=0.12,
                                 buff=0.04)
    links["chunks>kb"] = link(part["chunks/"].get_bottom() + DOWN * 0.18, part["kb"].get_top() + LEFT * 0.4,
                              DATA_C, stroke=2.5, tip=0.14, buff=0.02)
    links["caller>voice"] = link(part["caller"], part["voice"], S.WHITE, stroke=2.5, tip=0.14)
    links["voice>nova"] = link(part["voice"].get_top() + RIGHT * 0.45, part["nova"].get_left() + DOWN * 0.15,
                               AWS_C, stroke=2.5, tip=0.14, buff=0.04)
    links["voice>tools"] = link(part["voice"], part["tools"], CODE_C, stroke=2.5, tip=0.14, buff=0.04)
    links["tools>retrieve"] = link(part["tools"], part["retrieve"], CODE_C, stroke=2.5, tip=0.14, buff=0.04)
    links["retrieve>kb"] = link(part["retrieve"].get_top(), part["kb"].get_bottom(), QUERY_C, stroke=2.5,
                                tip=0.14, buff=0.04)

    h1 = sans("1 · BUILD THE LIBRARY  (batch, before any call)", 20, S.GREY).move_to([-6.6, 3.55, 0], aligned_edge=LEFT)
    h2 = sans("2 · ANSWER A CALLER  (live)", 20, S.GREY).move_to([-6.6, -1.35, 0], aligned_edge=LEFT)
    build = VGroup(h1, *[part[k] for k in chain], part["bucket"], *[part[k] for k in
                   ["snapshots/", "raw/", "text/", "chunks/", "config/"]],
                   *[links[k] for k in links if ">" in k and k.split(">")[0] in chain + ["chunks"]
                     and k not in ("chunks>kb",)])
    answer = VGroup(h2, part["caller"], part["voice"], part["nova"], part["tools"], part["retrieve"],
                    links["caller>voice"], links["voice>nova"], links["voice>tools"], links["tools>retrieve"],
                    links["retrieve>kb"])
    m = VGroup(build, part["kb"], links["chunks>kb"], answer)
    m.part, m.links, m.build, m.answer, m.h1, m.h2 = part, links, build, answer, h1, h2
    return m
