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


def composer(width: float, placeholder: str, menu: str = "Terra · 中 ⌄", pills: list[str] | None = None,
             size: float = 20) -> VGroup:
    """The input box: white, rounded, the placeholder (wrapped, as the box grows to fit it); bottom left
    the context drop-downs, bottom right the model menu and the send key."""
    ph = zh_wrap(placeholder, width - 0.5, size, FAINT, buff=0.08)
    box = RoundedRectangle(width=width, height=ph.height + 0.95, corner_radius=0.22, stroke_color="#D9D6CC",
                           stroke_width=1.5).set_fill(FIELD, 1)
    ph.move_to(box.get_corner(UL) + RIGHT * (0.25 + ph.width / 2) + DOWN * (0.22 + ph.height / 2))
    key = send_key().move_to(box.get_corner(DR) + LEFT * 0.36 + UP * 0.33)
    m = zh(menu, size, INK2).next_to(key, LEFT, buff=0.25)
    parts = [box, ph, m, key]
    row = None
    if pills:
        row = VGroup(*[pill(t, size) for t in pills]).arrange(RIGHT, buff=0.12)
        row.move_to(box.get_corner(DL) + RIGHT * 0.2 + UP * 0.33, aligned_edge=LEFT)
        parts.append(row)
    g = VGroup(*parts)
    g.box, g.placeholder, g.menu, g.key, g.pills = box, ph, m, key, row
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


# ------------------------------------------------------------------ the page, redrawn (strings: SOURCES.md)

GREETING = "哪里不舒服？"                                   # TriageChatPage.tsx:612
PLACEHOLDER = "说说哪里不舒服，比如：喉咙很痛，发烧两天了"       # :546
PLACEHOLDER_LATER = "回答上面的问题，或者补充情况"               # :553
DEMO_ROW = "演示回放 · 录好的真实回答，不调用模型"               # :796
CHIPS = ["喉咙痛，发烧两天", "深夜胸闷，喘不上气", "家长问：孩子周日晚上发烧", "周六扭伤脚踝"]   # recordings.json
FINE_PRINT = "AI 生成，不是诊断 · 只用虚构情况，别输入真实病情 · 危及生命直接打 911"   # :848–851
FINE_PRINT_PARENT_END = "危及生命请孩子或身边的人在当地打 911"
FIRST_MESSAGE = "喉咙痛两天了，吞东西的时候特别疼，今天量了体温38.5度"   # recordings.json, demo 01
FIRST_OPTION = "1. 今天打电话联系 BU 学生健康中心"                       # demo 01, options[0].titleZh
ACTIONS = ["复制", "复制给家长", "重新回答"]                              # TriageAnswer.tsx:234–239


def top_bar(width: float, size: float = 20) -> VGroup:
    left = VGroup(zh("AI 分诊", size, INK), pill("原型", size - 0.5, FAINT)).arrange(RIGHT, buff=0.15)
    right = zh("紧急情况", size, SAFETY_RED)
    bar = VGroup(left, right)
    right.move_to(left.get_center() + RIGHT * (width - left.width / 2 - right.width / 2))
    return bar


def fine_print(width: float, text: str = FINE_PRINT, size: float = 20) -> VGroup:
    return zh_wrap(text, width, size, FAINT, buff=0.06)


def empty_page(width: float = 6.0, height: float = 6.4) -> VGroup:
    """The new-chat page: top bar, the serif greeting, the composer in the middle, the demo chips, the fine print."""
    frame = page_frame(width, height)
    inner = width - 0.6
    bar = top_bar(inner)
    greet = serif_zh(GREETING, 38, INK)
    comp = composer(inner, PLACEHOLDER)
    demo = zh(DEMO_ROW, 20, FAINT)
    chips = VGroup(VGroup(*[pill(t) for t in CHIPS[:2]]).arrange(RIGHT, buff=0.12),
                   VGroup(*[pill(t) for t in CHIPS[2:]]).arrange(RIGHT, buff=0.12)).arrange(DOWN, buff=0.12)
    fp = fine_print(inner)
    body = VGroup(greet, comp, demo, chips, fp).arrange(DOWN, buff=0.3)
    body[2].shift(UP * 0.1)
    bar.next_to(frame.get_top(), DOWN, buff=0.25)
    body.next_to(bar, DOWN, buff=0.45)
    g = VGroup(frame, bar, body)
    g.frame, g.bar, g.greeting, g.composer, g.demo, g.chips, g.fine = frame, bar, greet, comp, demo, chips, fp
    return g


def turn_page(width: float = 6.0, height: float = 6.8) -> VGroup:
    """The page after one turn: bubble, the folded thinking line, an answer, its action row, the round
    scroll-to-bottom button, the composer and the fine print."""
    frame = page_frame(width, height)
    inner = width - 0.6
    bar = top_bar(inner)
    bubble = user_bubble(FIRST_MESSAGE, 3.6)
    think = zh("思考了 15 秒 ›", 20, FAINT)
    ans_title = serif_zh(FIRST_OPTION, 22, INK)
    bars = VGroup(*[Rectangle(width=w, height=0.1, stroke_width=0).set_fill(INK2, 0.55)
                    for w in (inner - 0.3, inner - 0.8, inner - 1.6)]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    answer = VGroup(ans_title, bars).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    actions = VGroup(*[pill(t) for t in ACTIONS]).arrange(RIGHT, buff=0.12)
    comp = composer(inner, PLACEHOLDER_LATER)
    fp = fine_print(inner)
    bar.next_to(frame.get_top(), DOWN, buff=0.25)
    bubble.next_to(bar, DOWN, buff=0.35).align_to(frame, RIGHT).shift(LEFT * 0.3)
    think.next_to(bubble, DOWN, buff=0.3).align_to(frame, LEFT).shift(RIGHT * 0.3)
    answer.next_to(think, DOWN, buff=0.18).align_to(think, LEFT)
    actions.next_to(answer, DOWN, buff=0.22).align_to(think, LEFT)
    fp.next_to(frame.get_bottom(), UP, buff=0.2)
    comp.next_to(fp, UP, buff=0.18)
    down = VGroup(Circle(radius=0.22, stroke_color="#D9D6CC", stroke_width=1.5).set_fill(FIELD, 1))
    down.add(Arrow(UP * 0.12, DOWN * 0.12, buff=0, color=INK2, stroke_width=3, max_tip_length_to_length_ratio=0.5)
             .move_to(down[0]))
    down.next_to(comp, UP, buff=0.15).align_to(comp, RIGHT).shift(LEFT * 0.15)
    g = VGroup(frame, bar, bubble, think, answer, actions, down, comp, fp)
    (g.frame, g.bar, g.bubble, g.think, g.answer, g.actions, g.down, g.composer,
     g.fine) = frame, bar, bubble, think, answer, actions, down, comp, fp
    return g


def outline_of(page: VGroup) -> VGroup:
    """The same layout as grey outlines only: Claude's app, drawn with no logo, name styling or text."""
    out = VGroup()
    for m in [page.frame, page.greeting, page.composer.box, *page.chips[0], *page.chips[1], page.fine]:
        r = RoundedRectangle(width=m.width, height=m.height, corner_radius=0.12 if m is not page.frame else 0.2,
                             stroke_color=S.GREY, stroke_width=2).move_to(m)
        out.add(r)
    return out
