"""S09 · Recap

The page again, every named part sorted: copied (GREEN), added (BLUE), not copied (RED);
three test-yourself questions with a held pause; the next episode (E4).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import CHECKED_C, DANGER_C, NARRATION, OURS_C, USER_C, clear, sans, serif, turn_page, zh

SAY = NARRATION["S09"]


class Recap(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the parts, sorted
        with self.voiceover(SAY[0]) as vo:
            page = turn_page(5.6, 7.0).move_to(LEFT * 3.75 + DOWN * 0.05)
            rule = VGroup(zh("每个界面只照抄一个参考（提议）", 30, USER_C), sans("one reference per screen, copied exactly", 22, S.GREY)
                          ).arrange(DOWN, buff=0.08).move_to(RIGHT * 2.6 + UP * 3.15)
            self.play(FadeIn(page), FadeIn(rule), run_time=0.6)

            def listing(title, color, items):
                head = sans(title, 26, color)
                rows = VGroup(*[sans(t, 22) if t.isascii() else zh(t, 22) for t in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
                return VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            copied = listing("copied", CHECKED_C, ["empty state", "suggestion chips", "composer", "model menu",
                                                   "send / stop key", "user bubble", "answer column", "action row",
                                                   "scroll-to-bottom", "disclaimer line"])
            added = listing("added", OURS_C, ["谁在问 · 保险 · 在哪里", "复制给家长", "紧急情况 · 现在就做", "parent wording, labels"])
            refused = listing("not copied", DANGER_C, ["logo and name", "history and sidebar", "raw thoughts",
                                                       "word-by-word streaming"])
            copied.move_to(RIGHT * 0.3 + DOWN * 0.3).align_to(LEFT * 0.55, LEFT)
            right = VGroup(added, refused).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(copied, RIGHT, buff=0.5, aligned_edge=UP)
            green = VGroup(*[SurroundingRectangle(m, color=CHECKED_C, buff=0.05, corner_radius=0.06, stroke_width=2)
                             for m in (page.bubble, page.answer, page.actions[0], page.actions[2], page.down, page.composer.box,
                                       page.fine)])
            blue = VGroup(*[SurroundingRectangle(m, color=OURS_C, buff=0.05, corner_radius=0.06, stroke_width=3)
                            for m in (page.bar[1], page.actions[1])])
            vo.wait_until("Claude's layout")
            self.play(FadeIn(copied[0]), LaggedStart(*[FadeIn(r) for r in copied[1]], lag_ratio=0.08),
                      LaggedStart(*[Create(g) for g in green], lag_ratio=0.1), run_time=1.4)
            vo.wait_until("Not its logo")
            self.play(FadeIn(refused[0]), LaggedStart(*[FadeIn(r) for r in refused[1]], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("Plus what only")
            self.play(FadeIn(added[0]), LaggedStart(*[FadeIn(r) for r in added[1]], lag_ratio=0.2),
                      LaggedStart(*[Create(b) for b in blue], lag_ratio=0.3), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- questions
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            def q(en, cn):
                return VGroup(serif(en, 30), zh(cn, 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            qs = VGroup(serif("Test yourself", 34, USER_C),
                        q("1.  Why copy one product instead of several?", "为什么照抄一个产品，而不是几个？"),
                        q("2.  Why does the parent's page ask someone else to call 911?", "为什么家长版的页面要请别人去打 911？"),
                        q("3.  What turned the send key into a bug, twice?", "是什么让发送键两次变成了 bug？")
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.7)
            self.play(FadeIn(qs[0]), run_time=0.4)
            for qq, phrase in zip(qs[1:], ["Why copy", "Why does", "And what turned"]):
                vo.wait_until(phrase)
                self.play(FadeIn(qq, shift=RIGHT * 0.1), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(3.5)   # time to answer before the next-episode card

        # 3 ---------------------------------------------------------------- next
        with self.voiceover(SAY[2]) as vo:
            self.play(qs.animate.set_opacity(0.3), run_time=0.4)
            nxt = VGroup(sans("next · E4", 24, S.GREY), zh("两天、一百多个提交", 40, S.WHITE),
                         sans("what the agents did, hour by hour, and what it cost", 22, S.GREY)
                         ).arrange(DOWN, buff=0.15).move_to(DOWN * 2.2)
            frame = SurroundingRectangle(nxt, color=USER_C, buff=0.3, corner_radius=0.15)
            self.play(FadeIn(nxt, shift=UP * 0.1), Create(frame), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(1.0)
        clear(self)
