"""S01 · Two walls of text.

1. Marco's two command blocks in two terminal windows (terminal 1 left, terminal 2 right).
2. A number badge on every non-empty line, 1–14, lit in turn.
3. "How we know": the four source tags; a padlocked AWS cloud, "we cannot log in".
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AWS_C, GUESS_C, NARRATION, QUERY_C, T1, T2, cloud, mono, sans, serif, source_tag,
                    terminal)

SAY = NARRATION["S01"]


def padlock(color=AWS_C, h=0.7):
    body = RoundedRectangle(width=h * 0.9, height=h * 0.7, corner_radius=0.06, stroke_color=color,
                            stroke_width=3).set_fill(color, 0.25)
    shackle = Arc(radius=h * 0.28, start_angle=0, angle=PI, color=color, stroke_width=4)
    shackle.next_to(body, UP, buff=-0.02)
    return VGroup(body, shackle)


class Hook(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the two blocks
        with self.voiceover(SAY[0]) as vo:
            t1 = terminal(T1, "terminal 1", size=20)
            t2 = terminal(T2, "terminal 2", size=20)
            k = min(6.0 / t1.width, 6.0 / t2.width)
            for t in (t1, t2):
                t.scale(k)
            VGroup(t1, t2).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to(UP * 0.4 + RIGHT * 0.15)
            src = serif("Marco, team chat, Oct 10", 22, S.GREY).next_to(VGroup(t1, t2), DOWN, buff=0.3)
            self.play(FadeIn(t1, shift=RIGHT * 0.2), run_time=0.9)
            self.play(FadeIn(t2, shift=LEFT * 0.2), FadeIn(src), run_time=0.9)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- 14 lines, 14 lessons
        with self.voiceover(SAY[1]) as vo:
            badges, n = VGroup(), 0
            for t, lines in ((t1, T1), (t2, T2)):
                for row, ln in zip(t.rows, lines):
                    if not ln.strip() or ln.startswith("   "):
                        continue
                    n += 1
                    c = Circle(radius=0.15, color=QUERY_C, stroke_width=2).set_fill(S.BG, 1)
                    num = mono(str(n), 18, QUERY_C).move_to(c)
                    b = VGroup(c, num).move_to([t.body.bg.get_left()[0] - 0.24, row.get_y(), 0])
                    badges.add(b)
            self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in badges], lag_ratio=0.25),
                      run_time=min(5.0, vo.remaining() - 0.5))
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- how we know
        with self.voiceover(SAY[2]) as vo:
            self.play(VGroup(t1, t2, badges, src).animate.set_opacity(0.12), run_time=0.7)
            cl = cloud("the team's AWS account", width=4.0).move_to(LEFT * 3.6 + UP * 0.6)
            lock = padlock().move_to(cl.shape.get_center() + UP * 0.15)
            cant = serif("we cannot log in", 28, AWS_C).next_to(cl, DOWN, buff=0.25)
            self.play(FadeIn(cl), run_time=0.7)
            self.play(FadeIn(lock, shift=DOWN * 0.2), FadeIn(cant), run_time=0.7)
            vo.wait_until("So everything here")
            gh = VGroup(sans("LEARNED FROM", 22, S.GREY), serif("the code on GitHub", 28),
                        serif("the team's notes", 28)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            gh.move_to(RIGHT * 2.8 + UP * 2.0)
            self.play(FadeIn(gh, shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("Each claim carries")
            rows = VGroup(*[VGroup(source_tag(k), serif(t, 24, GUESS_C if k == "inferred" else S.WHITE)).arrange(RIGHT, buff=0.3)
                            for k, t in [("code", "we read it in the code"), ("notes", "the team wrote it down"),
                                         ("measured", "we ran it ourselves"),
                                         ("inferred", "our best guess, with the reason")]])
            rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(RIGHT * 2.8 + DOWN * 0.8)
            for r in rows:
                r[1].next_to(r[0], RIGHT, buff=0.3)
                r[0].align_to(rows, LEFT)
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.15) for r in rows], lag_ratio=0.35), run_time=1.8)
            vo.wait_until("when we are guessing")
            self.play(Indicate(rows[3], color=GUESS_C), run_time=1.2)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
