"""S09 · Recap

Three columns: copied · not copied · added; three test-yourself questions; the next episode (E4).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import CHECKED_C, DANGER_C, NARRATION, OURS_C, USER_C, clear, sans, serif, zh

SAY = NARRATION["S09"]


def column(title: str, color: str, items: list[str]) -> VGroup:
    head = sans(title, 30, color)
    rows = VGroup(*[sans(t, 24) for t in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    return VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)


class Recap(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- copied / not / added
        with self.voiceover(SAY[0]) as vo:
            rule = VGroup(zh("每个界面只照抄一个参考", 32, USER_C), sans("one reference per screen, copied exactly", 24, S.GREY)
                          ).arrange(DOWN, buff=0.12).move_to(UP * 2.9)
            self.play(FadeIn(rule), run_time=0.5)
            cols = VGroup(column("copied", CHECKED_C, ["the layout", "the composer", "the colours, this page only"]),
                          column("not copied", DANGER_C, ["logo and name", "history and sidebar", "raw thoughts",
                                                          "word-by-word streaming"]),
                          column("added", OURS_C, ["emergency first", "wording a parent can act on",
                                                   "labels that travel", "accessibility"])
                          ).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(DOWN * 0.4)
            for c, phrase in zip(cols, ["Claude's layout", "Not its logo", "Plus what only"]):
                vo.wait_until(phrase)
                self.play(FadeIn(c[0]), LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in c[1]], lag_ratio=0.2), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- questions
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            qs = VGroup(serif("Test yourself", 34, USER_C),
                        serif("1.  Why copy one product instead of several?", 30),
                        serif("2.  Why does the parent's page ask someone else to call 911?", 30),
                        serif("3.  What turned the send key into a bug, twice?", 30)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.6)
            self.play(FadeIn(qs[0]), run_time=0.4)
            for q, phrase in zip(qs[1:], ["Why copy", "Why does", "And what turned"]):
                vo.wait_until(phrase)
                self.play(FadeIn(q, shift=RIGHT * 0.1), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

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
