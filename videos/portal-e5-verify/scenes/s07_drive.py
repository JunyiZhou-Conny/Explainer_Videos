"""S07 · Driving the real app (.claude/skills/verify-app/: control-app.mjs, SKILL.md, features/; ../SOURCES.md)

1. Its own copy of the app and its own browser (`up`, own port and profile), a health check (`doctor`, 8 checks),
   then the referral → specialist flow (features/referral-specialist.md:24-31); every element by ARIA role + accessible
   name; waits for the page to go quiet after each step (no 「查询中…」, no aria-busy, 400 ms without change).
2. Right = the tracker shows 「已预约专科」 AND `state` shows the referral scheduled, pointing to the new appointment.
   Evidence: screenshot, saved state, browserErrors empty (and the project rules). A failure names the visible
   buttons: 「没有找到可见的 button「预约」」. `down` stops only the pids it recorded and keeps the evidence.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, MODEL_C, NARRATION, OURS_C, USER_C, chip, clear, mark_bad, mark_ok, mono, sans,
                    screen, zh)

SAY = NARRATION["S07"]
STEPS = ["打开转诊", "选网络内诊所", "选时间", "提交模拟预约申请", "预约状态：待确认", "打开进度"]


class Drive(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- its own app, its own browser, by role and name
        with self.voiceover(SAY[0]) as vo:
            win = screen(6.4, 3.8).move_to(LEFT * 2.6 + UP * 0.9)
            bar = VGroup(*[Dot(radius=0.06, color=c) for c in (DANGER_C, USER_C, CHECKED_C)]).arrange(RIGHT, buff=0.1)
            bar.move_to(win.get_corner(UL) + RIGHT * 0.45 + DOWN * 0.25)
            url = mono("localhost · its own port", 20, S.GREY).next_to(bar, RIGHT, buff=0.3)
            vo.wait_until("drives the app itself")
            self.play(FadeIn(win), FadeIn(bar), FadeIn(url), run_time=0.6)
            vo.wait_until("its own browser")
            own = VGroup(chip("up: own server, saved demo state", OURS_C, 22, mono_font=False),
                         chip("own browser profile", OURS_C, 22, mono_font=False),
                         chip("doctor: 8 checks", CHECKED_C, 22, mono_font=False)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            own.move_to(RIGHT * 4.15 + UP * 1.6)
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.1) for c in own], lag_ratio=0.25), run_time=0.9)
            strip = VGroup(*[zh(s, 22, S.GREY) for s in STEPS]).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.75)
            arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=S.GREY_DARK, stroke_width=2,
                                    max_tip_length_to_length_ratio=0.3) for a, b in zip(strip, strip[1:])])
            vo.wait_until("clicks through")
            self.play(FadeIn(strip), FadeIn(arrows), run_time=0.5)
            page = VGroup()
            for i, phrase in enumerate(["open the referral", "in-network clinic", "pick a time", "submit", "wait for pending",
                                        "open the tracker"]):
                vo.wait_until(phrase)
                label = zh(STEPS[i], 26).move_to(win.get_center() + UP * 0.2)
                self.play(strip[i].animate.set_color(USER_C), FadeOut(page), FadeIn(label), run_time=0.35)
                page = label
            vo.wait_until("by its role and accessible name")
            target = VGroup(mono("button", 24, MODEL_C), zh("「提交模拟预约申请」", 24)).arrange(RIGHT, buff=0.15)
            target.move_to(win.get_bottom() + UP * 0.55)
            how = sans("found by role + accessible name: the label a screen reader announces", 22, S.GREY).next_to(strip, DOWN, buff=0.3)
            self.play(FadeIn(target), FadeIn(how), run_time=0.5)
            vo.wait_until("settle after each step")
            quiet = sans("waits until quiet: no loading text, no busy flag, 400 ms unchanged", 20, S.GREY).next_to(how, DOWN, buff=0.15)
            self.play(FadeIn(quiet), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- what counts as right; evidence; failure; shutdown
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            head = sans("what counts as right: both at once", 26, USER_C).move_to(UP * 3.0)
            a = VGroup(mark_ok(0.3, CHECKED_C), sans("the screen:", 24, S.GREY), zh("「已预约专科」", 26)).arrange(RIGHT, buff=0.2)
            b = VGroup(mark_ok(0.3, CHECKED_C), sans("the saved data:", 24, S.GREY),
                       mono("ref-demo → scheduled → the new appointment", 22)).arrange(RIGHT, buff=0.2)
            both = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.3)
            vo.wait_until("two things at once")
            self.play(FadeIn(head), run_time=0.3)
            vo.wait_until("the screen says")
            self.play(FadeIn(a), run_time=0.4)
            vo.wait_until("the saved data says")
            self.play(FadeIn(b), run_time=0.4)
            ev = VGroup(chip("screenshot", S.GREY, 22), chip("saved state", S.GREY, 22), chip("browser errors: none", S.GREY, 22),
                        chip("「模拟」 labels · both time zones", S.GREY, 22, mono_font=False)).arrange_in_grid(2, 2, buff=(0.25, 0.15))
            ev.move_to(DOWN * 0.1)
            vo.wait_until("required to keep evidence")
            self.play(LaggedStart(*[FadeIn(c) for c in ev], lag_ratio=0.15), run_time=0.8)
            vo.wait_until("When a step fails")
            fail = VGroup(VGroup(mark_bad(0.24, DANGER_C), zh("没有找到可见的 button「预约」", 24, DANGER_C)).arrange(RIGHT, buff=0.15),
                          zh("可见的 button 有：最新在前 | 最早在前 | 转诊 | …", 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            frame = SurroundingRectangle(fail, color=S.GREY_DARK, buff=0.22, corner_radius=0.12).set_fill(S.GREY_DARKER, 1)
            box = VGroup(frame, fail).move_to(DOWN * 1.7)
            self.play(FadeIn(box, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("shuts down only what it started")
            down = VGroup(mono("down", 24, OURS_C), sans("stops only its own processes · keeps the evidence", 22, S.GREY)
                          ).arrange(RIGHT, buff=0.25).move_to(DOWN * 3.05)
            self.play(FadeIn(down), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
