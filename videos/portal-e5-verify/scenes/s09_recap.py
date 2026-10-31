"""S09 · Recap

1. The two tools side by side: every order in a small world → the shortest story; the real app, by role and name →
   evidence; both checked by breaking things on purpose.
2. Three test-yourself questions, a held pause.
3. Next: E6 「后端怎么选」.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, NARRATION, OURS_C, USER_C, clear, sans, serif, zh)

SAY = NARRATION["S09"]


def panel(title: str, lines: list[str], color) -> VGroup:
    body = VGroup(sans(title, 28, color), *[sans(l, 22, S.GREY) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    frame = RoundedRectangle(width=5.6, height=body.height + 0.6, corner_radius=0.16, stroke_color=color, stroke_width=2.5)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    return VGroup(frame, body)


class Recap(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the two tools
        with self.voiceover(SAY[0]) as vo:
            left = panel("every order, in a small world", ["13,898 states, about a second", "four rules per state, one per step",
                                                         "→ the shortest story that breaks one"], USER_C)
            right = panel("the real app, like a parent", ["controls by role and accessible name", "screen and saved data agree",
                                                       "→ evidence, kept"], OURS_C)
            VGroup(left, right).arrange(RIGHT, buff=0.5).move_to(UP * 1.2)
            vo.wait_until("walks every order")
            self.play(FadeIn(left, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("uses the real app")
            self.play(FadeIn(right, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("breaking it on purpose")
            both = VGroup(sans("the first: broken on purpose 5 times, 5 caught", 26, CHECKED_C),
                          sans("the second: every flow run end to end", 26, CHECKED_C)).arrange(DOWN, buff=0.1).move_to(DOWN * 1.6)
            self.play(FadeIn(both), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- questions
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)

            def q(en, cn):
                return VGroup(serif(en, 30), zh(cn, 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            qs = VGroup(serif("Test yourself", 34, USER_C),
                        q("1.  What does the exhaustive check try that an ordinary test doesn't?", "穷举检查试了哪些普通测试不会试的东西？"),
                        q("2.  Why break your own code on purpose?", "为什么要故意把自己的代码改坏？"),
                        q("3.  Why does the check fail when the bug gets fixed?", "为什么 bug 修好以后，检查反而会失败？")
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 1.1)
            self.play(FadeIn(qs[0]), run_time=0.4)
            for qq, phrase in zip(qs[1:], ["What does the exhaustive", "Why break", "And why does"]):
                vo.wait_until(phrase)
                self.play(FadeIn(qq, shift=RIGHT * 0.1), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(5.0)

        # 3 ---------------------------------------------------------------- next
        with self.voiceover(SAY[2]) as vo:
            self.play(qs.animate.set_opacity(0.3), run_time=0.4)
            nxt = VGroup(sans("next · E6", 24, S.GREY), zh("后端怎么选", 40), sans("how do you choose a backend?", 22, S.GREY)
                         ).arrange(DOWN, buff=0.15).move_to(DOWN * 2.4)
            frame = SurroundingRectangle(nxt, color=USER_C, buff=0.3, corner_radius=0.15)
            self.play(FadeIn(nxt, shift=UP * 0.1), Create(frame), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(1.0)
        clear(self)
