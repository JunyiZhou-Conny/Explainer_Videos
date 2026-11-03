"""S05 · What was not copied (docs/design/README.md, 「不照抄的」)

Four cards, each crossed out with its reason: logo, name, private fonts → a small dot, open fonts ·
sidebar, history, attachments, tools → no accounts, no storage · raw reasoning → E2 · word-by-word
streaming → E2.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import DANGER_C, MODEL_C, NARRATION, clear, mark_bad, sans, zh

SAY = NARRATION["S05"]


def refused(title: str, reason: str, width: float = 6.2) -> VGroup:
    x = mark_bad(0.3, DANGER_C)
    t = sans(title, 24)
    r = sans("→ " + reason, 22, S.GREY)
    body = VGroup(VGroup(x, t).arrange(RIGHT, buff=0.25), r).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    frame = RoundedRectangle(width=width, height=body.height + 0.5, corner_radius=0.15, stroke_color=S.GREY_DARK,
                             stroke_width=2)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    return VGroup(frame, body)


class Refused(VoiceScene):
    def construct(self):
        with self.voiceover(SAY[0]) as vo:
            head = VGroup(sans("not copied", 34, DANGER_C), zh("不照抄的", 30, S.GREY)).arrange(RIGHT, buff=0.35)
            head.move_to(UP * 3.1)
            self.play(FadeIn(head), run_time=0.4)
            cards = VGroup(refused("Claude's logo, name and private fonts", "a small dot means thinking; open fonts"),
                           refused("sidebar, history, attachments, tools", "no accounts, no storage, not needed"),
                           refused("the raw reasoning", "only what can be checked: the receipt (E2)"),
                           refused("words streaming as they are written", "answers pass the checker first (E2)")
                           ).arrange_in_grid(2, 2, buff=(0.2, 0.35)).move_to(UP * 0.4)
            dot = Dot(radius=0.12, color=MODEL_C)
            for c, phrase in zip(cards, ["logo, name", "The sidebar", "the raw reasoning", "words streaming"]):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=UP * 0.1), run_time=0.45)
                if c is cards[0]:
                    vo.wait_until("a small dot")
                    dot.next_to(c[1][1], RIGHT, buff=0.25)
                    self.play(FadeIn(dot, scale=1.5), run_time=0.3)
            vo.wait_until("pass the checker first")
            src = sans("docs/design/README.md · 「不照抄的」", 20, S.GREY).move_to(DOWN * 2.6)
            self.play(FadeIn(src), run_time=0.3)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
