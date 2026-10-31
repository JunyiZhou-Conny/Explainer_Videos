"""S11 · Recap

1. The tape end to end: hidden thinking → writing watched box by box → early 911 flag → checked answer
   replayed → the receipt.
2. Three test-yourself questions. 3. Next: E3, the page and what was copied from Claude's app.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, NARRATION, OURS_C, USER_C, clear, sans, serif, tape, zh)

SAY = NARRATION["S11"]


class Recap(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the whole path on one tape
        with self.voiceover(SAY[0]) as vo:
            row = tape(32, 12, size=0.28, buff=0.07).move_to(UP * 1.6)
            self.play(LaggedStart(*[FadeIn(c) for c in row], lag_ratio=0.03), run_time=1.0)
            notes = [(row[:12], "hidden thinking · billed", S.GREY, "First thinking"),
                     (row[12:22], "writing · watched box by box", OURS_C, "Then writing"),
                     (row[12:15], "early 911", DANGER_C, "An early warning"),
                     (row[22:], "checked · replayed", CHECKED_C, "A replay"),
                     (None, "a receipt, not the thoughts", USER_C, "a receipt instead")]
            ys = [0.75, 0.75, -0.05, 0.75, -0.9]
            for (cells, text, color, phrase), y in zip(notes, ys):
                vo.wait_until(phrase)
                if cells is not None:
                    br = Brace(cells, DOWN, color=color, buff=0.1)
                    lab = sans(text, 20, color).next_to(br, DOWN, buff=0.08)
                    if y < 0.5:
                        lab.shift(DOWN * 0.75)
                    self.play(GrowFromCenter(br), FadeIn(lab), run_time=0.45)
                else:
                    lab = sans(text, 28, color).move_to(DOWN * 0.9)
                    self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.45)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- questions
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            qs = VGroup(serif("Test yourself", 34, USER_C),
                        serif("1.  What exactly does our stopwatch call thinking?", 30),
                        serif("2.  Why do the urgency boxes come first in the form?", 30),
                        serif("3.  What would a reasoning summary need before it could be shown?", 30)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.4)
            self.play(FadeIn(qs[0]), run_time=0.4)
            for q, phrase in zip(qs[1:], ["What exactly", "Why do", "And what would"]):
                vo.wait_until(phrase)
                self.play(FadeIn(q, shift=RIGHT * 0.1), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- next
        with self.voiceover(SAY[2]) as vo:
            self.play(qs.animate.set_opacity(0.3), run_time=0.4)
            nxt = VGroup(sans("next · E3", 24, S.GREY), zh("照着 Claude 抄", 40, S.WHITE),
                         sans("what we copied, what we refused, what we could invent", 22, S.GREY)
                         ).arrange(DOWN, buff=0.15).move_to(DOWN * 2.3)
            frame = SurroundingRectangle(nxt, color=USER_C, buff=0.3, corner_radius=0.15)
            self.play(FadeIn(nxt, shift=UP * 0.1), Create(frame), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(1.0)
        clear(self)
