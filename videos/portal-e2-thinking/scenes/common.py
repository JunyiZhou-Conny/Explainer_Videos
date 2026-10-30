"""Shared helpers for 项目周记 E2 'What is thought for 3 seconds?' (3b1b house style).

The CareOneX kit (videos/careonex-series/careonex_kit.py) supplies the boxes, panels, chips and
arrows; this file adds the portal series' pieces: the product's screens with their exact strings,
the token tape (hidden reasoning vs. visible text), the stopwatch bars, and the data every scene
shares (the receipts from Conny's screenshots, PR #41's commit times). Sources: ../SOURCES.md.
"""

import re
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
SERIES = PROJECT.parent / "careonex-series"
sys.path.insert(0, str(SERIES))

from manim import *  # noqa: E402,F401,F403
from careonex_kit import *  # noqa: E402,F401,F403
from explainer import style as S  # noqa: E402
from explainer.script import load_narration  # noqa: E402

NARRATION = load_narration(PROJECT / "script.md")

MODEL_C = S.ORANGE        # the model / the API
OURS_C = S.BLUE           # our code: server, checker, page
HIDDEN_C = S.GREY         # hidden reasoning tokens
TEXT_C = S.WHITE          # text the reader may see
CHECKED_C = S.GREEN       # text that passed the checker
USER_C = S.YELLOW         # the user's words, attention
DANGER_C = S.RED
CJK = "Noto Sans CJK SC"  # the product's own UI strings are Chinese

# Conny's screenshots, 2026-10-30 (verbatim)
LIVE = "正在思考 · 11 秒"
FOLDED = "思考了 22 秒"
PROCESS_22 = "思考 13.5 秒 → 写 8.7 秒（1717 字）→ 检查通过"
MODEL_22 = "gpt-6-luna · 思考强度 中 · 模型用时 22.1 秒 · $0.0013"
PROCESS_3 = "思考 1.6 秒 → 写 1.5 秒（85 字）→ 检查通过"

# src/features/triage/ThinkingRow.tsx (EarlyEmergency, student wording)
EARLY_911 = "初步判断可能危及生命。不用等回答写完，现在就打 911。"

# PR #41's own commits, Boston time, hours after Wednesday 2026-10-28 00:00
# (videos/portal-series/weeks/2026-w44.md)
PR41_HOURS = [1.983, 2.267, 2.367, 10.033, 10.15, 10.233, 10.667, 10.95, 10.983, 11.067, 11.15,
              11.383, 11.45, 11.583, 11.7, 12.1, 13.65, 14.05, 14.35, 15.317, 15.35, 15.617, 16.867,
              17.15, 17.683, 18.733, 19.067, 19.267]

# The form's boxes in the order the model writes them (prototypes/triage/src/llm/schema.ts)
FORM = ["acuity", "disposition", "followUp", "redFlagsPositive", "emergency", "options",
        "watchForZh", "bringZh", "sayEn", "parentSummaryZh", "explanationZh", "unknownsZh", "citations"]


def zh(s: str, size: float = 26, color: str = S.WHITE, weight: str = "NORMAL") -> Text:
    """The product's Chinese UI strings, in a CJK sans like the app's."""
    return Text(s, font=CJK, font_size=size, color=color, weight=weight)


_TOKENS = re.compile(r"[　-〿一-鿿＀-￯]|[^\s　-〿一-鿿＀-￯]+|\s+")
_NO_LINE_START = set("。，、；：？！」』）》…")   # never start a line with closing punctuation


@lru_cache(maxsize=None)
def _w(tok: str, size: float) -> float:
    if tok.isspace():
        return zh("x x", size).width - zh("xx", size).width
    return zh(tok, size).width


def zh_wrap(s: str, width: float, size: float = 24, color: str = S.WHITE, buff: float = 0.1) -> VGroup:
    """Verbatim text broken into lines no wider than `width` (by character for CJK, by word otherwise)."""
    lines, cur, w = [], "", 0.0
    for tok in _TOKENS.findall(s):
        tw = _w(tok, size)
        over = w + tw > width or (w + tw > .75 * width and zh(cur + tok, size).width > width)
        if cur and over and not tok.isspace() and tok not in _NO_LINE_START:
            lines.append(cur.rstrip())
            cur, w = tok, zh(tok, size).width
        elif not (tok.isspace() and not cur):
            cur, w = cur + tok, w + tw
    lines.append(cur.rstrip())
    return VGroup(*[zh(t, size, color) for t in lines if t]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def screen(width: float, height: float) -> RoundedRectangle:
    """The product's screen: a dark rounded panel."""
    return RoundedRectangle(width=width, height=height, corner_radius=0.18, stroke_color=S.GREY_DARK,
                            stroke_width=2).set_fill(S.GREY_DARKER, 1)


def thinking_line(seconds: int) -> VGroup:
    """The live line: an orange dot and 「正在思考 · N 秒」."""
    dot = Dot(radius=0.09, color=MODEL_C)
    t = zh(f"正在思考 · {seconds} 秒", 30, S.GREY)
    return VGroup(dot, t).arrange(RIGHT, buff=0.2)


def receipt(rows: list[tuple[str, str]], width: float, head: str = FOLDED, size: float = 24) -> VGroup:
    """The opened receipt: 「思考了 N 秒 ›」 over label/value rows (strings verbatim)."""
    title_m = zh(f"{head} ›", size + 4, S.GREY)
    out = [title_m]
    for name, value in rows:
        k = zh(name, size, S.GREY)
        v = zh_wrap(value, width - 1.2, size)
        row = VGroup(k, v)
        v.next_to(k, RIGHT, buff=0.35, aligned_edge=UP)
        out.append(row)
    g = VGroup(*out).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    return g


def model_box(name: str = "gpt-6-luna", sub: str | None = "OpenAI", width: float = 2.8) -> VGroup:
    return tag_box("model", name, sub, MODEL_C, width=width)


def ours_box(name: str, sub: str | None = None, width: float = 2.8) -> VGroup:
    return tag_box("our code", name, sub, OURS_C, width=width)


def page_box(sub: str | None = "the chat page", width: float = 2.6) -> VGroup:
    return tag_box("our code", "page", sub, OURS_C, width=width)


def tape(n: int, hidden: int, size: float = 0.22, buff: float = 0.06) -> VGroup:
    """A row of `n` tokens: the first `hidden` are reasoning (grey), the rest visible text (white)."""
    cells = VGroup(*[Square(side_length=size, stroke_width=0).set_fill(HIDDEN_C if i < hidden else TEXT_C, 1)
                     for i in range(n)])
    return cells.arrange(RIGHT, buff=buff)


def phase_bars(think: float, write: float, unit: float = 0.32, height: float = 0.38,
               write_label: str | None = None) -> VGroup:
    """The stopwatch's two phases as bars: grey thinking, white writing (seconds × unit)."""
    a = Rectangle(width=think * unit, height=height, stroke_width=0).set_fill(HIDDEN_C, 0.85)
    b = Rectangle(width=write * unit, height=height, stroke_width=0).set_fill(TEXT_C, 0.85)
    VGroup(a, b).arrange(RIGHT, buff=0)
    la = zh(f"思考 {think:g} 秒", 22, S.WHITE).move_to(a)
    lb = zh(write_label or f"写 {write:g} 秒", 22, S.BG).move_to(b)
    if la.width > a.width - .1:
        la.next_to(a, UP, buff=.08).align_to(a, LEFT)
    if lb.width > b.width - .1:
        lb.set_color(S.WHITE).next_to(b, RIGHT, buff=.15)
    g = VGroup(a, b, la, lb)
    g.think, g.write = a, b
    return g


def quote_panel(text: str, source: str, width: float = 10.5, size: float = 28, color: str = S.WHITE) -> VGroup:
    """A verbatim quote from a decision record, with its source under it."""
    body = zh_wrap(text, width - .7, size, color, buff=.14)
    src = sans(source, 20, S.GREY)
    inner = VGroup(body, src).arrange(DOWN, aligned_edge=LEFT, buff=.25)
    bg = RoundedRectangle(width=width, height=inner.height + .6, corner_radius=.16, stroke_color=S.GREY_DARK,
                          stroke_width=2).set_fill(S.GREY_DARKER, 1)
    inner.move_to(bg).align_to(bg, LEFT).shift(RIGHT * .35)
    return VGroup(bg, inner)


def ponder_zh(scene, question: str, question_zh: str, seconds: float = 4.0) -> VGroup:
    """The house pause-and-ponder card, with the Chinese question under it."""
    from explainer.components import pause_and_ponder
    card = pause_and_ponder(scene, question, seconds=seconds, width=10.5, size=32)
    return card


def clear(scene, run_time: float = 0.5):
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=run_time)


def stopwatch(radius: float = 0.32, color: str = S.WHITE) -> VGroup:
    face = Circle(radius=radius, color=color, stroke_width=3)
    knob = Rectangle(width=radius * .45, height=radius * .25, stroke_width=0).set_fill(color, 1)
    knob.next_to(face, UP, buff=.02)
    hand = Line(face.get_center(), face.get_center() + UP * radius * .75, color=color, stroke_width=3)
    return VGroup(face, knob, hand)
