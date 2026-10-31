"""S02 · One function, many orders (src/state/reducer.ts:217; AppProvider.tsx:147-181; ../SOURCES.md)

1. The app's data as a box (the clock drawn outside it: a flag in the model, not app state); one action at a time goes through the reducer (old state + action → new state);
   the page checks the referral when it draws, the booking reaches the reducer later; time passing is an event.
2. A test is one chosen path; the bug's path (time passes → book) is one nobody chose.
3. Ponder: a test checks the cases someone thought of; what checks the ones nobody thought of?
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, MODEL_C, NARRATION, OURS_C, USER_C, chip, clear, mark_ok, ponder_zh, sans, stopwatch,
                    zh)

SAY = NARRATION["S02"]
ACTIONS = ["book", "confirm", "reschedule", "cancel", "complete"]


def state_box(label: str, width: float = 3.0) -> VGroup:
    rows = VGroup(sans("appointments", 22, S.GREY), sans("referrals", 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    frame = RoundedRectangle(width=width, height=rows.height + 0.9, corner_radius=0.16, stroke_color=OURS_C, stroke_width=2.5)
    head = sans(label, 24, OURS_C).move_to(frame.get_top() + DOWN * 0.3)
    rows.next_to(head, DOWN, buff=0.15)
    return VGroup(frame, head, rows)


class Reducer(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the reducer
        with self.voiceover(SAY[0]) as vo:
            old = state_box("state").move_to(LEFT * 4.6 + UP * 0.9)
            fn = VGroup(RoundedRectangle(width=2.8, height=1.2, corner_radius=0.2, stroke_color=USER_C, stroke_width=3),
                        sans("reducer", 30, USER_C))
            fn[1].move_to(fn[0])
            fn.move_to(UP * 0.9)
            new = state_box("next state").move_to(RIGHT * 4.6 + UP * 0.9)
            a1 = Arrow(old.get_right(), fn.get_left(), color=S.GREY, buff=0.15)
            a2 = Arrow(fn.get_right(), new.get_left(), color=S.GREY, buff=0.15)
            vo.wait_until("goes through one function")
            self.play(FadeIn(old), FadeIn(fn), run_time=0.6)
            acts = VGroup(*[chip(a, MODEL_C, 22) for a in ACTIONS]).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.0)
            vo.wait_until("a single action")
            self.play(LaggedStart(*[FadeIn(a, shift=UP * 0.1) for a in acts], lag_ratio=0.15), run_time=1.0)
            vo.wait_until("returns the next state")
            moving = acts[0].copy()
            self.play(acts[0].animate.set_opacity(0.35), moving.animate.scale(1.2).move_to(fn.get_bottom() + DOWN * 0.4), run_time=0.6)
            self.play(Create(a1), Create(a2), FadeIn(new), run_time=0.7)
            vo.wait_until("checks the referral when it draws")
            draw = VGroup(sans("page draws: referral OK", 22, S.GREY), sans("…time passes…", 22, USER_C),
                          sans("booking reaches the reducer", 22, S.GREY)).arrange(RIGHT, buff=0.35).move_to(DOWN * 2.3)
            self.play(FadeIn(draw[0]), run_time=0.4)
            vo.wait_until("reaches the reducer later")
            self.play(FadeIn(draw[1]), FadeIn(draw[2]), run_time=0.6)
            vo.wait_until("time passing is an event")
            clock = VGroup(stopwatch(0.3, USER_C), chip("time passes", USER_C, 22),
                           sans("a move of its own: the clock is not app data", 22, S.GREY)).arrange(RIGHT, buff=0.2)
            clock.next_to(old, UP, buff=0.3).align_to(old, LEFT)
            self.play(FadeIn(clock, scale=1.05), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- a test is one chosen path
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            start = Dot(LEFT * 5.6, radius=0.12, color=OURS_C)
            pts = [LEFT * 5.6 + RIGHT * 2.2 * k + UP * (0.9 if k % 2 else 0.2) for k in range(1, 5)]
            tested = VMobject(color=CHECKED_C, stroke_width=4).set_points_as_corners([start.get_center(), *pts])
            labels = VGroup(*[sans(t, 20, S.GREY).next_to(p, UP, buff=0.12)
                              for t, p in zip(["book", "confirm", "reschedule", "complete"], pts)])
            vo.wait_until("A test follows a path")
            self.play(FadeIn(start), Create(tested), FadeIn(labels), run_time=1.2)
            ok = VGroup(mark_ok(0.3, CHECKED_C), sans("a test: one chosen path", 24, CHECKED_C)).arrange(RIGHT, buff=0.15)
            ok.move_to(UP * 2.1 + RIGHT * 1.0)
            self.play(FadeIn(ok), run_time=0.4)
            bug = VMobject(color=DANGER_C, stroke_width=4).set_points_as_corners(
                [start.get_center(), start.get_center() + RIGHT * 2.0 + DOWN * 1.6, start.get_center() + RIGHT * 4.2 + DOWN * 2.2])
            blab = VGroup(sans("time passes", 20, USER_C).next_to(bug.get_points()[3], DOWN, buff=0.12),
                          sans("book", 20, S.GREY).next_to(bug.get_end(), DOWN, buff=0.12))
            vo.wait_until("a path nobody chose")
            self.play(Create(bug), FadeIn(blab), run_time=1.0)
            vo.wait_until("then the booking goes through")
            x = VGroup(Circle(radius=0.22, color=DANGER_C, stroke_width=4), sans("bug", 22, DANGER_C))
            x[1].next_to(x[0], RIGHT, buff=0.1)
            x.move_to(bug.get_end() + RIGHT * 0.6)
            self.play(FadeIn(x, scale=1.2), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- ponder
        with self.voiceover(SAY[2]) as vo:
            self.play(*[m.animate.set_opacity(0.15) for m in self.mobjects], run_time=0.4)
            ponder_zh(self, "A test checks the cases someone thought of.\nWhat checks the ones nobody thought of?",
                      "测试检查的是有人想到的情况。那没人想到的呢？", seconds=4.0)
        self.wait(3.0)
        clear(self)
