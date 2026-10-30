"""S04 · What was copied

1. One turn on the page with GREEN ticks: one column (at most 768 px), the beige bubble on the right, the
   serif answer with no frame (docs/design/README.md; triage.css:177, 223–237, 400–407).
2. The composer enlarged: it grows as you type; three drop-downs (谁在问 · 保险 · 在哪里, Composer.tsx); the
   model menu 「Terra · 中 ⌄」 next to the terracotta send key, where Claude's help page puts its own.
3. The colour table as swatches, kept to `.chat-page`; the rest of the site in the neutral theme; 0006:
   「Junyi 选了后者（2026-10-28）」.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BUBBLE, CHECKED_C, CREAM, FAINT, FIELD, INK, INK2, NARRATION, TERRA, USER_C, clear, composer,
                    mark_ok, pill, quote_panel, sans, turn_page, zh)

SAY = NARRATION["S04"]


def tick_label(target, text, y, x=0.9):
    lab = VGroup(mark_ok(0.26, CHECKED_C), sans(text, 24)).arrange(RIGHT, buff=0.2)
    lab.move_to([x + lab.width / 2, y, 0])
    ln = Line(target.get_right() + RIGHT * 0.05, lab.get_left() + LEFT * 0.1, color=CHECKED_C, stroke_width=2)
    return VGroup(ln, lab)


def swatch(name: str, light: str, dark: str | None, size: float = 0.5) -> VGroup:
    a = Square(side_length=size, stroke_color=S.GREY, stroke_width=1).set_fill(light, 1)
    parts = [a]
    if dark:
        parts.append(Square(side_length=size, stroke_color=S.GREY, stroke_width=1).set_fill(dark, 1))
    sq = VGroup(*parts).arrange(RIGHT, buff=0.06)
    txt = VGroup(zh(name, 22), sans(light + (f" / {dark}" if dark else ""), 20, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
    return VGroup(sq, txt).arrange(RIGHT, buff=0.25)


class Copied(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the layout
        with self.voiceover(SAY[0]) as vo:
            page = turn_page(6.0, 7.0).move_to(LEFT * 3.6)
            self.play(FadeIn(page), run_time=0.6)
            vo.wait_until("One column")
            span = DoubleArrow(page.frame.get_corner(UL) + DOWN * 0.15 + RIGHT * 0.1,
                               page.frame.get_corner(UR) + DOWN * 0.15 + LEFT * 0.1, color=CHECKED_C, buff=0,
                               stroke_width=3, tip_length=0.15)
            t1 = tick_label(page.frame, "one column, at most 768 px", 3.0)
            self.play(GrowFromCenter(span), FadeIn(t1), run_time=0.6)
            vo.wait_until("beige bubble")
            t2 = tick_label(page.bubble, "your message: a beige bubble, right", page.bubble.get_center()[1])
            self.play(Circumscribe(page.bubble, color=CHECKED_C, buff=0.05), FadeIn(t2), run_time=0.8)
            vo.wait_until("serif type")
            t3 = tick_label(page.answer, "the answer: serif, full width, no frame", page.answer.get_center()[1])
            self.play(Circumscribe(page.answer, color=CHECKED_C, buff=0.08), FadeIn(t3), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the composer
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            comp = composer(9.0, "喉咙痛两天了", pills=["学生", "SHIP", "主校区"], size=26)
            comp.move_to(UP * 0.6)
            self.play(FadeIn(comp), run_time=0.5)
            vo.wait_until("grows as you type")
            longer = composer(9.0, "喉咙痛两天了，吞东西的时候特别疼，今天量了体温38.5度。昨晚开始有点怕冷",
                              pills=["学生", "SHIP", "主校区"], size=26).move_to(comp, aligned_edge=DOWN)
            self.play(Transform(comp, longer), run_time=0.9)
            illus = sans("typed text: illustration", 20, S.GREY).next_to(comp, UP, buff=0.12).align_to(comp, LEFT)
            self.play(FadeIn(illus), run_time=0.2)
            vo.wait_until("three small drop-downs")
            names = VGroup(*[zh(t, 24, USER_C) for t in ["谁在问", "保险", "在哪里"]])
            for n, p in zip(names, comp.pills):
                n.next_to(p, DOWN, buff=0.35)
            sub = sans("who is asking · insurance · where you are (Composer.tsx)", 20, S.GREY).next_to(names, DOWN, buff=0.2)
            sub.align_to(comp, LEFT)
            self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in names], lag_ratio=0.3), FadeIn(sub), run_time=0.8)
            vo.wait_until("the model menu")
            self.play(Circumscribe(comp.menu, color=USER_C, buff=0.08), run_time=0.7)
            vo.wait_until("the terracotta send key")
            self.play(Circumscribe(comp.key, color=USER_C, buff=0.08), run_time=0.6)
            vo.wait_until("Claude's help page")
            q = quote_panel("The model menu next to the send button controls three settings: which Claude model you're "
                            "chatting with, how much effort it puts into each response, and whether it uses thinking.",
                            "Claude Help Center · read 2026-10-30", width=11.6, size=24, color=S.GREY)
            q.to_edge(DOWN, buff=0.45)
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- the colours, this page only
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.4)
            sw = VGroup(swatch("页面底色", "#FAF9F5", "#262624"), swatch("输入框", "#FFFFFF", "#30302E"),
                        swatch("用户气泡", "#F0EEE6", "#141413"), swatch("正文", "#141413", "#FAF9F5"),
                        swatch("主色 · 发送键", "#C96442", "#D97757")).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            fonts = VGroup(zh("思源宋体 · 问候语和回答", 24), zh("思源黑体 · 其余", 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            left = VGroup(sans("light / dark", 20, S.GREY), sw, fonts).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            left.move_to(LEFT * 3.6 + UP * 0.2)
            vo.wait_until("warm colours and serif type")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in left], lag_ratio=0.25), run_time=1.2)
            q = quote_panel("Junyi 选了后者（2026-10-28）", "decision 0006 · colours and type copied too", width=5.6, size=28,
                            color=USER_C).move_to(RIGHT * 3.4 + UP * 2.35)
            self.play(FadeIn(q, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("inside this one page")
            tiles = VGroup(*[RoundedRectangle(width=1.5, height=1.0, corner_radius=0.1, stroke_color=S.GREY_DARK,
                                              stroke_width=2).set_fill(S.GREY_DARKER, 1) for _ in range(5)])
            chat = RoundedRectangle(width=1.5, height=1.0, corner_radius=0.1, stroke_color=USER_C, stroke_width=3
                                    ).set_fill(CREAM, 1)
            grid = VGroup(*tiles[:2], chat, *tiles[2:]).arrange_in_grid(2, 3, buff=0.2).move_to(RIGHT * 3.4 + DOWN * 0.4)
            names = [("首页", S.GREY), ("其他页面", S.GREY), ("分诊聊天页", INK), ("…", S.GREY), ("…", S.GREY), ("…", S.GREY)]
            labels = VGroup(*[zh(t, 20, c).move_to(m) for (t, c), m in zip(names, grid)])
            scope = sans(".chat-page only", 22, USER_C).next_to(grid, DOWN, buff=0.25)
            rest = sans("the rest: the neutral transition theme (decision 0003)", 20, S.GREY).next_to(scope, DOWN, buff=0.12)
            self.play(FadeIn(grid), FadeIn(labels), run_time=0.6)
            self.play(Circumscribe(chat, color=USER_C, buff=0.06), FadeIn(scope), FadeIn(rest), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
