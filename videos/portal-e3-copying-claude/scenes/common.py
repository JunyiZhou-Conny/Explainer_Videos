"""Shared helpers for 项目周记 E3 'Copying Claude's chat page' (3b1b house style).

Everything from E2's helpers (videos/portal-e2-thinking/scenes/common.py: the CareOneX kit, the
semantic colours, zh(), zh_wrap(), screen(), receipt(), quote_panel(), ponder_zh(), clear() …) is
re-exported. This file adds a redraw of the triage chat page in its own light colours (the hex values
in docs/design/README.md) so the page can be taken apart on the dark 3b1b canvas. Strings on the
page are verbatim from the portal source at b7ab98e; see ../SOURCES.md.
"""

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent

_spec = importlib.util.spec_from_file_location(
    "portal_e2_common", PROJECT.parent / "portal-e2-thinking" / "scenes" / "common.py")
_e2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_e2)
globals().update({k: v for k, v in vars(_e2).items()
                  if not k.startswith("__") and k not in ("HERE", "PROJECT", "NARRATION")})

from explainer.script import load_narration  # noqa: E402

NARRATION = load_narration(PROJECT / "script.md")   # this episode's lines, not E2's

# the page's own palette (docs/design/README.md, light theme)
CREAM = "#FAF9F5"     # 页面底色 米白
FIELD = "#FFFFFF"     # 输入框
BUBBLE = "#F0EEE6"    # 用户气泡 米灰
INK = "#141413"       # 正文
INK2 = "#3D3D3A"
FAINT = "#73726C"     # 浅字
TERRA = "#C96442"     # 主色 陶土橙 (send key, small icons)
SAFETY_RED = "#B42318"
SERIF_CJK = "Noto Serif CJK SC"   # 思源宋体, the page's serif for the greeting and the answer


def serif_zh(s: str, size: float = 26, color: str = INK) -> Text:
    return Text(s, font=SERIF_CJK, font_size=size, color=color)


def page_frame(width: float = 6.4, height: float = 7.0) -> RoundedRectangle:
    """The page itself: a cream panel, like a browser window, on the dark canvas."""
    return RoundedRectangle(width=width, height=height, corner_radius=0.2, stroke_color=S.GREY,
                            stroke_width=2).set_fill(CREAM, 1)


def pill(label: str, size: float = 20, color: str = INK2, stroke: str = "#D9D6CC") -> VGroup:
    t = zh(label, size, color)
    bg = RoundedRectangle(width=t.width + 0.36, height=t.height + 0.24, corner_radius=(t.height + 0.24) / 2,
                          stroke_color=stroke, stroke_width=1.5).set_fill(FIELD, 1)
    t.move_to(bg)
    return VGroup(bg, t)


def send_key(size: float = 0.42, color: str = TERRA, stop: bool = False) -> VGroup:
    """The terracotta square send key; while waiting it becomes the stop key."""
    key = RoundedRectangle(width=size, height=size, corner_radius=0.08, stroke_width=0).set_fill(color, 1)
    if stop:
        glyph = Square(side_length=size * 0.32, stroke_width=0).set_fill(FIELD, 1)
    else:
        glyph = Arrow(DOWN * size * 0.28, UP * size * 0.28, buff=0, color=FIELD, stroke_width=4,
                      max_tip_length_to_length_ratio=0.45)
    glyph.move_to(key)
    return VGroup(key, glyph)


def composer(width: float, placeholder: str, menu: str = "Terra · 中 ⌄", context: str | None = None,
             size: float = 20) -> VGroup:
    """The input box: white, rounded, the placeholder; bottom left the context drop-down, bottom right
    the model menu and the send key."""
    box = RoundedRectangle(width=width, height=1.25, corner_radius=0.22, stroke_color="#D9D6CC",
                           stroke_width=1.5).set_fill(FIELD, 1)
    ph = zh(placeholder, size, FAINT)
    if ph.width > width - 0.5:
        ph.scale_to_fit_width(width - 0.5)
    ph.move_to(box.get_corner(UL) + RIGHT * (0.25 + ph.width / 2) + DOWN * 0.33)
    key = send_key().move_to(box.get_corner(DR) + LEFT * 0.36 + UP * 0.33)
    m = zh(menu, size - 2, INK2).next_to(key, LEFT, buff=0.25)
    parts = [box, ph, m, key]
    ctx = None
    if context:
        ctx = pill(context, size - 3).move_to(box.get_corner(DL) + RIGHT * 0.25 + UP * 0.33, aligned_edge=LEFT)
        parts.append(ctx)
    g = VGroup(*parts)
    g.box, g.placeholder, g.menu, g.key, g.context = box, ph, m, key, ctx
    return g


def user_bubble(text: str, max_width: float = 3.6, size: float = 20) -> VGroup:
    body = zh_wrap(text, max_width, size, INK)
    bg = RoundedRectangle(width=body.width + 0.4, height=body.height + 0.3, corner_radius=0.18,
                          stroke_width=0).set_fill(BUBBLE, 1)
    body.move_to(bg)
    return VGroup(bg, body)


def answer_lines(lines: list[str], width: float, size: float = 20) -> VGroup:
    """Answer text: no frame, full width, serif."""
    rows = VGroup(*[serif_zh(t, size, INK) for t in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    if rows.width > width:
        rows.scale_to_fit_width(width)
    return rows


def callout(target, label: str, side=RIGHT, color: str = S.YELLOW, size: float = 22, buff: float = 0.5,
            zh_label: str | None = None) -> VGroup:
    """A 3b1b-style name tag: a thin line from the part of the page to its name on the dark canvas."""
    words = sans(label, size, color)
    lab = VGroup(words, zh(zh_label, size - 2, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.06) if zh_label else words
    lab.next_to(target, side, buff=buff)
    start = target.get_critical_point(side)
    end = lab.get_critical_point(-side)
    ln = Line(start, end, color=color, stroke_width=2)
    return VGroup(ln, lab)
