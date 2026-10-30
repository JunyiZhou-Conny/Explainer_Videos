"""S08 · How it got built

1. PR #41's 28 own commits on a Wednesday axis, Boston time (week digest). 10:40 the server streams
   progress + the model and effort menu; 10:57 the page streams progress; 11:04 the menu says switching
   model or effort starts without the cache: on Terra the first answer costs about five times as much
   ($0.038 vs $0.0074, pricing.ts × server.ts TYPICAL_TURN).
2. 11:09, 17:09, 18:44, and the leak test in server.test.ts: before the result, no 4 consecutive
   characters of the model's text may appear in the progress lines.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import CHECKED_C, DANGER_C, NARRATION, OURS_C, PR41_HOURS, USER_C, clear, sans, text_panel

SAY = NARRATION["S08"]
H0, H1 = 0.0, 20.0
X0, X1, Y = -6.2, 6.2, -0.4


def x_of(h: float) -> float:
    return X0 + (h - H0) / (H1 - H0) * (X1 - X0)


def tick_for(ticks: VGroup, h: float) -> Line:
    """The commit tick nearest to hour h."""
    return ticks[min(range(len(PR41_HOURS)), key=lambda k: abs(PR41_HOURS[k] - h))]


def lift(tick: Line, color, height: float = 0.85):
    """Recolour a commit tick and make it taller (the animation target)."""
    x = tick.get_start()[0]
    return tick.animate.put_start_and_end_on([x, Y, 0], [x, Y + height, 0]).set_stroke(color, width=4, opacity=1)


def note(time: str, text: str, color) -> VGroup:
    return VGroup(sans(time, 24, color), sans(text, 24, S.WHITE)).arrange(RIGHT, buff=0.3)


class Path(VoiceScene):
    def construct(self):
        axis = Line([X0, Y, 0], [X1, Y, 0], color=S.GREY, stroke_width=2)
        hours = VGroup(*[VGroup(Line([x_of(h), Y - 0.08, 0], [x_of(h), Y + 0.08, 0], color=S.GREY),
                                sans(f"{h}:00", 20, S.GREY).move_to([x_of(h), Y - 0.35, 0])) for h in range(0, 21, 4)])
        day = sans("Wednesday 2026-10-28 · Boston time · PR #41, 28 commits", 22, S.GREY).move_to(DOWN * 1.35)
        ticks = VGroup(*[Line([x_of(h), Y, 0], [x_of(h), Y + 0.4, 0], color=OURS_C, stroke_width=3) for h in PR41_HOURS])
        top = UP * 2.75 + LEFT * 6.2

        # 1 ---------------------------------------------------------------- streaming in twenty minutes
        with self.voiceover(SAY[0]) as vo:
            self.play(Create(axis), FadeIn(hours), FadeIn(day), run_time=0.7)
            self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.04), run_time=1.2)
            vo.wait_until("within twenty minutes")
            n1 = note("10:40", "the server streams progress; the model and effort menu", USER_C)
            n2 = note("10:57", "the page streams progress", USER_C)
            n3 = note("11:04", "a menu note: switching model or effort means no cache", USER_C)
            notes1 = VGroup(n1, n2, n3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            notes1.move_to(top, aligned_edge=UL)
            self.play(lift(tick_for(ticks, 10 + 40 / 60), USER_C), FadeIn(n1, shift=DOWN * 0.1), run_time=0.5)
            self.play(lift(tick_for(ticks, 10 + 57 / 60), USER_C), FadeIn(n2, shift=DOWN * 0.1), run_time=0.5)
            span = sans("10:40–11:04", 20, USER_C).next_to(tick_for(ticks, 10.9), UP, buff=0.55)
            self.play(FadeIn(span), run_time=0.3)
            vo.wait_until("a note for the menu")
            self.play(lift(tick_for(ticks, 11 + 4 / 60), USER_C), FadeIn(n3, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("five times as much")
            cost = VGroup(sans("Terra, per turn", 20, S.GREY),
                          VGroup(sans("cached ≈ $0.0074", 24, S.WHITE), sans("first after a switch ≈ $0.038", 24, USER_C)
                                 ).arrange(RIGHT, buff=0.5)).arrange(DOWN, buff=0.1).move_to(DOWN * 2.6)
            src = sans("pricing.ts × the typical turn in server.ts", 20, S.GREY).next_to(cost, DOWN, buff=0.08)
            self.play(FadeIn(cost, shift=UP * 0.1), FadeIn(src), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- what reviews found
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(notes1, span, cost, src)),
                      *[lift(t, OURS_C, 0.4) for t in ticks if t.get_height() > 0.5], run_time=0.4)
            rows = [(11 + 9 / 60, "11:09", "keep the 911 warning when you press stop", "keeping the 911 warning"),
                    (17 + 9 / 60, "17:09", "… and through retry and dropped connections", "dropped connections"),
                    (18 + 44 / 60, "18:44", "make the tests fail when what they guard breaks", "a test that fails")]
            notes2 = VGroup(*[note(t, x, DANGER_C) for _, t, x, _ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            notes2.move_to(top, aligned_edge=UL)
            for (h, t, _, phrase), n in zip(rows, notes2):
                vo.wait_until(phrase)
                tk = tick_for(ticks, h)
                lab = sans(t, 20, DANGER_C).move_to([tk.get_start()[0], Y + 1.1, 0])
                self.play(lift(tk, DANGER_C), FadeIn(n, shift=DOWN * 0.1), FadeIn(lab),
                          run_time=0.4)
            test = text_panel(["server.test.ts",
                               "before the result, no 4 consecutive characters",
                               "of the model's text may appear in the progress lines"],
                              size=22, colors={0: S.GREY})
            test.move_to(DOWN * 2.65)
            self.play(FadeIn(test, shift=UP * 0.1), FadeOut(day), run_time=0.6)
            vo.wait_until("the proof")
            self.play(Circumscribe(test, color=CHECKED_C, buff=0.08), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
