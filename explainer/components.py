"""Reusable visual building blocks shared by all videos.

Everything returns ordinary Manim mobjects (or plays animations on a scene you pass in),
so scenes can position, recolour and animate them freely.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, AnimationGroup, Arc, Arrow, Circle, CurvedArrow,
                   DashedLine, FadeIn, FadeOut, ImageMobject, Line, Rectangle, RoundedRectangle,
                   SurroundingRectangle, VGroup, Write, linear, rate_functions)

from .style import (BG, BODY_SIZE, FONT_SANS, GREY, GREY_DARK, GREY_DARKER, SMALL_SIZE,
                    TINY_SIZE, WHITE, YELLOW, text)

# ---------------------------------------------------------------- maths helpers


def laplace_pdf(t, mu: float = 0.0, b: float = 1.0):
    return np.exp(-np.abs(np.asarray(t) - mu) / b) / (2 * b)


def gaussian_pdf(t, mu: float = 0.0, sigma: float = 1.0):
    return np.exp(-0.5 * ((np.asarray(t) - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


# ---------------------------------------------------------------- people & databases


def person_icon(color: str = WHITE, height: float = 0.5, fill_opacity: float = 1.0) -> VGroup:
    """A simple head-and-shoulders glyph."""
    head = Circle(radius=0.2, stroke_width=0).set_fill(color, fill_opacity)
    body = Arc(radius=0.34, start_angle=0, angle=np.pi, stroke_width=0)
    body = RoundedRectangle(width=0.68, height=0.36, corner_radius=0.17, stroke_width=0)
    body.set_fill(color, fill_opacity)
    body.next_to(head, DOWN, buff=0.04)
    g = VGroup(head, body)
    g.scale_to_fit_height(height)
    return g


def database_rows(labels: list[str], values: list[str] | None = None, color: str = WHITE,
                  width: float = 3.2, row_height: float = 0.42, size: float = TINY_SIZE + 2,
                  value_color: str | None = None) -> VGroup:
    """A vertical stack of database rows: [icon | name | value].

    Returns VGroup(rows...) where each row is VGroup(box, icon, name, value?).
    Address parts as rows[i][0] (box), rows[i][1] (icon), rows[i][2] (name), rows[i][3] (value).
    """
    rows = VGroup()
    for i, lab in enumerate(labels):
        box = Rectangle(width=width, height=row_height, stroke_color=GREY_DARK, stroke_width=1.5)
        box.set_fill(GREY_DARKER, 1)
        icon = person_icon(color, height=row_height * 0.7).move_to(box.get_left() + RIGHT * 0.3)
        name = text(lab, size, WHITE, font=FONT_SANS).next_to(icon, RIGHT, buff=0.18)
        row = VGroup(box, icon, name)
        if values is not None:
            val = text(values[i], size, value_color or WHITE, font=FONT_SANS)
            val.move_to(box.get_right() + LEFT * 0.4)
            row.add(val)
        rows.add(row)
    rows.arrange(DOWN, buff=0)
    return rows


def person_grid(n: int, cols: int, color: str = WHITE, height: float = 0.36,
                buff: float = 0.12) -> VGroup:
    """n person icons in a grid — a compact 'database of n people'."""
    g = VGroup(*[person_icon(color, height) for _ in range(n)])
    g.arrange_in_grid(cols=cols, buff=buff)
    return g


# ---------------------------------------------------------------- papers & maps


def paper_card(name: str, year: str | int, idea: str = "", color: str = WHITE,
               width: float = 3.4, highlight: bool = False, size: float = SMALL_SIZE) -> VGroup:
    """A compact card for a paper: bold short name, year, one-line idea.

    Returns VGroup(frame, name, year, idea?) — frame is the RoundedRectangle.
    """
    name_m = text(name, size, color, weight="BOLD")
    year_m = text(str(year), size - 6, GREY)
    lines = VGroup(name_m, year_m)
    if idea:
        idea_m = text(idea, size - 6, WHITE)
        if idea_m.width > width - 0.3:
            idea_m.scale_to_fit_width(width - 0.3)
        lines.add(idea_m)
    lines.arrange(DOWN, buff=0.1)
    if name_m.width > width - 0.3:
        name_m.scale_to_fit_width(width - 0.3)
    frame = RoundedRectangle(width=width, height=lines.height + 0.4, corner_radius=0.15,
                             stroke_color=YELLOW if highlight else color,
                             stroke_width=5 if highlight else 2)
    frame.set_fill(GREY_DARKER, 0.95)
    lines.move_to(frame)
    return VGroup(frame, *lines)


def connect(a, b, label: str | None = None, color: str = GREY, curved: float = 0.0,
            size: float = TINY_SIZE, buff: float = 0.1):
    """Arrow from mobject a to mobject b (edge to edge), with an optional small label."""
    start, end = _edge_points(a, b)
    if curved:
        arr = CurvedArrow(start, end, angle=curved, color=color, stroke_width=3, tip_length=0.18)
    else:
        arr = Arrow(start, end, buff=buff, color=color, stroke_width=3,
                    max_tip_length_to_length_ratio=0.12, tip_length=0.18)
    if not label:
        return arr
    lab = text(label, size, color)
    lab.move_to(arr.point_from_proportion(0.5)).shift(UP * 0.22)
    return VGroup(arr, lab)


def _edge_points(a, b):
    ca, cb = a.get_center(), b.get_center()
    d = cb - ca
    if abs(d[0]) * a.height > abs(d[1]) * a.width:   # mostly horizontal
        return (a.get_right(), b.get_left()) if d[0] > 0 else (a.get_left(), b.get_right())
    return (a.get_bottom(), b.get_top()) if d[1] < 0 else (a.get_top(), b.get_bottom())


def timeline(start: int, end: int, width: float = 12.0, step: int = 5,
             color: str = GREY, size: float = TINY_SIZE) -> VGroup:
    """A horizontal year axis. Use .year_to_point(y) to place things above a year."""
    line = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=2)
    ticks = VGroup()
    for y in range(start, end + 1, step):
        x = -width / 2 + width * (y - start) / (end - start)
        ticks.add(VGroup(Line(UP * 0.08, DOWN * 0.08, color=color).shift(RIGHT * x),
                         text(str(y), size, color).move_to([x, -0.32, 0])))
    g = VGroup(line, ticks)

    def year_to_point(y: float):
        return line.point_from_proportion((y - start) / (end - start))

    g.year_to_point = year_to_point
    return g


# ---------------------------------------------------------------- titles & prompts


def chapter_card(scene, number: int | str, title: str, subtitle: str | None = None,
                 hold: float = 1.2):
    """3b1b-style chapter title: plays in, holds, and plays out on `scene`."""
    num = text(f"Part {number}", SMALL_SIZE, GREY)
    tit = text(title, 50, WHITE)
    grp = VGroup(num, tit)
    if subtitle:
        grp.add(text(subtitle, SMALL_SIZE, GREY))
    grp.arrange(DOWN, buff=0.3)
    underline = Line(LEFT, RIGHT, color=YELLOW, stroke_width=3).set_width(tit.width + 0.4)
    underline.next_to(tit, DOWN, buff=0.15)
    scene.play(FadeIn(num, shift=UP * 0.2), Write(tit), run_time=1.0)
    scene.play(FadeIn(underline), *( [FadeIn(grp[2])] if subtitle else []), run_time=0.5)
    scene.wait(hold)
    scene.play(FadeOut(VGroup(grp, underline)), run_time=0.6)


def ponder_card(question: str, width: float = 9.5, size: float = BODY_SIZE) -> VGroup:
    """A 'Pause and ponder' card. Returns VGroup(frame, header, question, timer_bar)."""
    header = text("Pause and ponder", SMALL_SIZE, YELLOW, weight="BOLD")
    q = text(question, size, WHITE, line_spacing=1.1)
    if q.width > width - 0.6:
        q.scale_to_fit_width(width - 0.6)
    body = VGroup(header, q).arrange(DOWN, buff=0.35)
    frame = RoundedRectangle(width=width, height=body.height + 0.9, corner_radius=0.2,
                             stroke_color=YELLOW, stroke_width=3).set_fill(BG, 0.96)
    body.move_to(frame).shift(UP * 0.12)
    bar = Line(frame.get_corner(DOWN + LEFT) + RIGHT * 0.3 + UP * 0.25,
               frame.get_corner(DOWN + RIGHT) + LEFT * 0.3 + UP * 0.25,
               color=YELLOW, stroke_width=4)
    return VGroup(frame, header, q, bar)


def pause_and_ponder(scene, question: str, seconds: float = 4.0, **kw) -> VGroup:
    """Show a ponder card whose timer bar drains over `seconds`; returns the card (still on screen)."""
    card = ponder_card(question, **kw)
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return card


# ---------------------------------------------------------------- paper pages


def render_pdf_page(pdf: str | Path, page: int, out_png: str | Path, dpi: int = 150) -> Path:
    """Rasterise one PDF page with pdftoppm (cached on disk)."""
    out_png = Path(out_png)
    if not out_png.exists():
        out_png.parent.mkdir(parents=True, exist_ok=True)
        stem = out_png.with_suffix("")
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-f", str(page), "-l", str(page),
                        "-singlefile", str(pdf), str(stem)], check=True)
    return out_png


def paper_page(png: str | Path, height: float = 6.5):
    """An ImageMobject of a paper page with a thin frame. Returns (image, frame)."""
    img = ImageMobject(str(png)).scale_to_fit_height(height)
    frame = SurroundingRectangle(img, buff=0, color=GREY, stroke_width=2)
    return img, frame


def highlight_box(m, color: str = YELLOW, buff: float = 0.1):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=3, corner_radius=0.06)
