"""S06 · The same idea, at Amazon's scale (../SOURCES.md)

Newcombe et al., "How Amazon Web Services Uses Formal Methods", Communications of the ACM 58(4), April 2015:
TLA+ (created by Leslie Lamport); in DynamoDB replication, a data-loss bug whose "shortest error trace exhibiting
the bug contained 35 high-level steps", which "had passed unnoticed through extensive design reviews, code reviews,
and testing". Ours: two steps, in a one-second check.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, NARRATION, OURS_C, USER_C, clear, quote_panel, sans, serif)

SAY = NARRATION["S06"]


def chain(n: int, width: float, color, end_color) -> VGroup:
    xs = np.linspace(-width / 2, width / 2, n + 1)
    dots = VGroup(*[Dot([x, 0, 0], radius=0.06 if n > 10 else 0.1, color=color) for x in xs])
    dots[-1].set_color(end_color).scale(1.8)
    lines = VGroup(*[Line(a.get_center(), b.get_center(), color=color, stroke_width=2) for a, b in zip(dots, dots[1:])])
    return VGroup(lines, dots)


class Amazon(VoiceScene):
    def construct(self):
        with self.voiceover(SAY[0]) as vo:
            paper = VGroup(serif("How Amazon Web Services Uses Formal Methods", 32),
                           sans("Communications of the ACM · April 2015", 22, S.GREY)).arrange(DOWN, buff=0.12).move_to(UP * 2.8)
            vo.wait_until("In 2015")
            self.play(FadeIn(paper, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Leslie Lamport")
            tla = sans("TLA+ · a language created by Leslie Lamport", 24, USER_C).next_to(paper, DOWN, buff=0.25)
            self.play(FadeIn(tla), run_time=0.4)
            long = chain(35, 11.0, S.GREY, DANGER_C).move_to(UP * 0.5)
            lab = VGroup(sans("DynamoDB replication: a data-loss bug", 24, DANGER_C), sans("shortest story: 35 steps", 24)
                         ).arrange(RIGHT, buff=0.6).next_to(long, DOWN, buff=0.3)
            vo.wait_until("In one database service")
            self.play(Create(long[0]), LaggedStart(*[FadeIn(d) for d in long[1]], lag_ratio=0.06), run_time=2.6, rate_func=linear)
            vo.wait_until("it found a")
            self.play(FadeIn(lab[0]), Flash(long[1][-1], color=DANGER_C, flash_radius=0.3), run_time=0.5)
            vo.wait_until("thirty-five steps long")
            self.play(FadeIn(lab[1]), run_time=0.4)
            vo.wait_until("passed design reviews")
            q = quote_panel("“…had passed unnoticed through extensive design reviews, code reviews, and testing.”",
                            "Newcombe et al., CACM 58(4), 2015", width=10.6, size=24).move_to(DOWN * 1.35)
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Ours is tiny")
            ours = chain(2, 1.6, OURS_C, DANGER_C).move_to(LEFT * 4.2 + DOWN * 3.0)
            olab = sans("ours: 2 steps · a one-second check", 24, OURS_C).next_to(ours, RIGHT, buff=0.4)
            self.play(Create(ours[0]), FadeIn(ours[1]), FadeIn(olab), run_time=0.7)
            vo.wait_until("the same move")
            same = sans("the same move: let a machine walk every order", 24, USER_C).next_to(olab, RIGHT, buff=0.5)
            if same.get_right()[0] > 6.4:
                same.next_to(olab, DOWN, buff=0.1).align_to(olab, LEFT)
            self.play(FadeIn(same), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
