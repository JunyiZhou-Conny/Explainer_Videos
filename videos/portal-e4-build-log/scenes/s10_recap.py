"""S10 · Recap

1. The clock again, the phases numbered as the narration names them: skeleton + fact check (Tue 12:22–15:08);
   the turn (Tue 21:21); whack-a-mole with the bots (Tue 22:27 → Wed 00:07); a queue of fix agents; attacking the checker
   (Wed 21:04 → Thu 00:45); the stop rule held (last push Thu 00:45).
2. Three test-yourself questions with a held pause.
3. End card: 「项目周记 · 第 44 周 完」.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (H36, H41, MODEL_C, NARRATION, OURS_C, USER_C, clear, commit_ticks, sans, serif, week_axis, zh)

SAY = NARRATION["S10"]
# (badge, from, to, legend, when, narration phrase); hours after Tue 00:00 Boston
PHASES = [(1, 12.37, 15.14, "a skeleton and a fact check", "Tue afternoon", "a skeleton"),
          (2, 21.33, 21.38, "your turn", "Tue 21:21", "your turn"),
          (3, 22.45, 24.13, "whack-a-mole with the bots", "Tue night", "whack-a-mole"),
          (4, 40.87, 43.18, "a queue of fix agents", "Wed afternoon", "a queue of fix agents"),
          (5, 45.07, 48.75, "attacking the checker first", "Wed night", "a second night"),
          (6, 48.74, 48.76, "a stop rule that held", "last push Thu 00:45", "a stop rule")]


class Recap(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the two days, named
        with self.voiceover(SAY[0]) as vo:
            top = sans("two days · Boston time", 26, S.GREY).move_to(UP * 3.2)
            line, ticks, x_of = week_axis(y=0.3)
            t36 = commit_ticks(x_of, H36, 2.2, 0.5, MODEL_C).set_opacity(0.45)
            t41 = commit_ticks(x_of, H41, 2.2, 0.5, OURS_C).set_opacity(0.45)
            self.play(FadeIn(top), Create(line), FadeIn(ticks), FadeIn(t36), FadeIn(t41), run_time=0.8)
            legend = VGroup()
            marks = []
            for n, a, b, text, when, _ in PHASES:
                w = max(x_of(b) - x_of(a), 0.12)
                band = Rectangle(width=w, height=0.36, stroke_width=0).set_fill(USER_C, 0.75)
                band.move_to([(x_of(a) + x_of(b)) / 2, 0.95, 0])
                badge = VGroup(Circle(radius=0.2, color=USER_C, stroke_width=2.5), sans(str(n), 20, USER_C))
                badge.move_to([band.get_x(), 1.55, 0])
                marks.append(VGroup(band, badge))
                legend.add(VGroup(sans(f"{n}", 22, USER_C), sans(text, 24), sans(when, 20, S.GREY)
                                  ).arrange(RIGHT, buff=0.25))
            col_a = VGroup(*legend[:3]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
            col_b = VGroup(*legend[3:]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
            VGroup(col_a, col_b).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(DOWN * 2.1)
            for mark, row, ph in zip(marks, legend, PHASES):
                vo.wait_until(ph[5])
                self.play(GrowFromEdge(mark[0], LEFT), FadeIn(mark[1], scale=1.2), FadeIn(row, shift=UP * 0.1), run_time=0.45)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- questions
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)

            def q(en, cn):
                return VGroup(serif(en, 30), zh(cn, 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            qs = VGroup(serif("Test yourself", 34, USER_C),
                        q("1.  Why did most commits fix the checker?", "为什么大多数提交都在修检查器？"),
                        q("2.  Why reproduce a bug before fixing it?", "为什么修 bug 之前要先复现？"),
                        q("3.  What is still waiting for you?", "还有什么在等你决定？")
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.7)
            self.play(FadeIn(qs[0]), run_time=0.4)
            for qq, phrase in zip(qs[1:], ["Why did most", "Why reproduce", "And what is still"]):
                vo.wait_until(phrase)
                self.play(FadeIn(qq, shift=RIGHT * 0.1), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(3.5)   # time to answer before the end card

        # 3 ---------------------------------------------------------------- end of the week
        with self.voiceover(SAY[2]) as vo:
            self.play(qs.animate.set_opacity(0.3), run_time=0.4)
            end = VGroup(zh("项目周记 · 第 44 周 完", 40), sans("next week's episodes start from next week's pull requests", 22, S.GREY)
                         ).arrange(DOWN, buff=0.18).move_to(DOWN * 2.2)
            frame = SurroundingRectangle(end, color=USER_C, buff=0.3, corner_radius=0.15)
            self.play(FadeIn(end, shift=UP * 0.1), Create(frame), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(1.0)
        clear(self)
