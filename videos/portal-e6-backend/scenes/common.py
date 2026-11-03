"""Shared helpers for this 项目周记 episode (3b1b house style).

Re-exports E2's helpers (videos/portal-e2-thinking/scenes/common.py: the CareOneX kit, the semantic
colours, zh(), zh_wrap(), quote_panel(), ponder_zh(), clear() …) and loads this episode's narration.
Every number, quote and time on screen is listed in ../SOURCES.md.
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

WEB_C, API_C, DB_C, AUTH_C = OURS_C, MODEL_C, CHECKED_C, USER_C   # page · server · database · login


def device(label: str, width: float = 3.0, height: float = 2.2, phone: bool = False) -> VGroup:
    """A laptop or a phone outline with a label under it."""
    if phone:
        body = RoundedRectangle(width=height * 0.55, height=height, corner_radius=0.2, stroke_color=S.GREY, stroke_width=2.5)
        parts = VGroup(body)
    else:
        body = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=S.GREY, stroke_width=2.5)
        base = Polygon(body.get_corner(DL) + DOWN * 0.06 + LEFT * 0.2, body.get_corner(DR) + DOWN * 0.06 + RIGHT * 0.2,
                       body.get_corner(DR) + DOWN * 0.24 + RIGHT * 0.36, body.get_corner(DL) + DOWN * 0.24 + LEFT * 0.36,
                       stroke_color=S.GREY, stroke_width=2.5)
        parts = VGroup(body, base)
    lab = sans(label, 22, S.GREY).next_to(parts, DOWN, buff=0.15)
    g = VGroup(parts, lab)
    g.body = body
    return g


def sans_wrap(s: str, width: float, size: float = 22, color: str = S.GREY, buff: float = 0.08) -> VGroup:
    """English text broken at word boundaries into lines no wider than `width`."""
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and sans(trial, size).width > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    lines.append(cur)
    return VGroup(*[sans(t, size, color) for t in lines]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def option(name: str, reason: str | None, chosen: bool, width: float = 5.6, size: float = 22) -> VGroup:
    """A considered option: chosen (coloured frame) or rejected (grey, struck through), with its reason."""
    color = CHECKED_C if chosen else S.GREY
    head = sans(name, 26, S.WHITE if chosen else S.GREY)
    rows = [head]
    if reason:
        rows.append(zh_wrap(reason, width - 0.5, size, S.GREY) if any("一" <= ch <= "鿿" for ch in reason)
                    else sans_wrap(reason, width - 0.5, size, S.GREY))
    body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    frame = RoundedRectangle(width=width, height=body.height + 0.4, corner_radius=0.14, stroke_color=color, stroke_width=2.5)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.25)
    g = VGroup(frame, body)
    if not chosen:
        g.add(Line(head.get_left() + LEFT * 0.05, head.get_right() + RIGHT * 0.05, color=DANGER_C, stroke_width=4))
    return g


def table_card(name: str, rows: list[str], color, width: float = 3.2, size: float = 20) -> VGroup:
    """A database table as a card: its name over a few field lines."""
    head = mono(name, 24, color)
    lines = VGroup(*[(zh(r, size, S.GREY) if any("一" <= ch <= "鿿" for ch in r) else mono(r, size, S.GREY))
                     for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    body = VGroup(head, lines).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    frame = RoundedRectangle(width=max(width, body.width + 0.5), height=body.height + 0.4, corner_radius=0.14,
                             stroke_color=color, stroke_width=2.5)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.25)
    return VGroup(frame, body)
