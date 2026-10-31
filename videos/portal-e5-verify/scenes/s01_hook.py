"""S01 · A bug nobody had seen (PR #42; ../SOURCES.md)

1. A referral (ENT, valid until 2027-01-22, fictional demo data); the booking page left open past the
   expiry; submit; the expired referral is attached anyway and the tracker shows 「已预约」, not 「已过期」.
2. 245 existing tests passed (none books after the expiry); the code comment 「过期…的转诊保持不变」 (reducer.ts:288) says the case is handled, and it
   isn't; reported Friday 16:13 Boston by an agent (c0920b0, PR #42).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, NARRATION, OURS_C, USER_C, clear, mark_ok, mono, sans, screen, stopwatch,
                    strike, tag_box, zh)

SAY = NARRATION["S01"]


class Hook(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the bug, as a student would meet it
        with self.voiceover(SAY[0]) as vo:
            ref = VGroup(tag_box("referral", "ENT · ref-v1", None, USER_C, width=3.4),
                         zh("有效期至 2027-01-22", 24, S.GREY), sans("demo data", 20, S.GREY)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(LEFT * 4.4 + UP * 1.4)
            vo.wait_until("has a referral")
            self.play(FadeIn(ref, shift=UP * 0.1), run_time=0.5)
            page = screen(4.6, 3.2).move_to(RIGHT * 2.6 + UP * 0.9)
            head = zh("预约专科", 26).move_to(page.get_top() + DOWN * 0.45)
            used = zh("本次使用的转诊：ref-v1", 22, S.GREY).next_to(head, DOWN, buff=0.3)
            button = VGroup(RoundedRectangle(width=3.4, height=0.6, corner_radius=0.12, stroke_width=0).set_fill(OURS_C, 0.9),
                            zh("提交模拟预约申请", 24, S.BG))
            button[1].move_to(button[0])
            button.move_to(page.get_bottom() + UP * 0.6)
            vo.wait_until("opens the booking page")
            self.play(FadeIn(page), FadeIn(head), FadeIn(used), FadeIn(button), run_time=0.6)
            # the clock passes the expiry while the page stays open
            watch = stopwatch(0.42).move_to(LEFT * 4.4 + DOWN * 1.4)
            line = Line(LEFT * 6.0 + DOWN * 2.45, LEFT * 1.6 + DOWN * 2.45, color=S.GREY, stroke_width=2)
            exp = VGroup(Line(UP * 0.18, DOWN * 0.18, color=DANGER_C, stroke_width=3), zh("有效期", 20, DANGER_C)
                         ).arrange(DOWN, buff=0.06)
            exp.move_to(line.point_from_proportion(0.55) + DOWN * 0.12)
            dot = Dot(line.get_start(), radius=0.09, color=USER_C)
            vo.wait_until("leaves it open")
            self.play(FadeIn(watch), Create(line), FadeIn(exp), FadeIn(dot), run_time=0.5)
            self.play(Rotate(watch[2], angle=-2 * PI, about_point=watch[0].get_center()),
                      dot.animate.move_to(line.point_from_proportion(0.9)), run_time=1.6, rate_func=linear)
            vo.wait_until("presses submit")
            self.play(Indicate(button, color=USER_C, scale_factor=1.05), run_time=0.5)
            vo.wait_until("attached anyway")
            arrow = Arrow(ref.get_right(), used.get_left(), color=DANGER_C, buff=0.15)
            self.play(GrowArrow(arrow), ref[0].animate.set_color(DANGER_C), run_time=0.6)
            vo.wait_until("shows the specialist as booked")
            status = VGroup(VGroup(mark_ok(0.24, CHECKED_C), zh("已预约专科", 26, CHECKED_C)).arrange(RIGHT, buff=0.12),
                            zh("已过期", 26, S.GREY)).arrange(RIGHT, buff=0.6).next_to(page, DOWN, buff=0.35)
            self.play(FadeIn(status[0]), run_time=0.4)
            self.play(FadeIn(status[1]), Create(strike(status[1], DANGER_C)), run_time=0.5)
            how = sans("the page path: the agent's reading of the code · the checker proved the booking step", 20, S.GREY)
            how.move_to(DOWN * 3.2)
            self.play(FadeIn(how), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- everything said it was fine
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            tests = VGroup(mark_ok(0.4, CHECKED_C), sans("245 existing tests: all passed", 34, CHECKED_C)).arrange(RIGHT, buff=0.25)
            tests.move_to(UP * 2.4)
            vo.wait_until("All 245 existing tests")
            self.play(FadeIn(tests), run_time=0.5)
            none = sans("none of them books after the expiry", 24, S.GREY).next_to(tests, DOWN, buff=0.15)
            vo.wait_until("none of them books")
            self.play(FadeIn(none), run_time=0.4)
            comment = VGroup(sans("a comment in the code:", 22, S.GREY), zh("「过期……的转诊保持不变」", 30)
                             ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(UP * 0.4)
            vo.wait_until("carries a comment")
            self.play(FadeIn(comment), run_time=0.5)
            vo.wait_until("left alone")
            self.play(Create(strike(comment[1], DANGER_C)), FadeIn(sans("not what the code does", 22, DANGER_C)
                                                                      .next_to(comment, RIGHT, buff=0.4)), run_time=0.6)
            vo.wait_until("On Friday afternoon")
            found = VGroup(sans("reported by an agent · Fri 16:13 Boston", 28, USER_C), mono("PR #42 · npm run verify", 24, S.GREY)
                           ).arrange(DOWN, buff=0.12).move_to(DOWN * 1.2)
            self.play(FadeIn(found, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("before anyone looks")
            q = sans("how can an agent prove a change is right, before any person looks?", 28, S.WHITE).move_to(DOWN * 2.6)
            self.play(FadeIn(q), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
