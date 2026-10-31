"""S08 · What is still open (decision 0006 D:198-223; issue #11; ../SOURCES.md)

1. The success criterion (D:202, #13 #14): after the student unlinks, the parent's request gets 403, checked by an
   automated test. Status 「提议」; #11's open box 「线下三人确认后，决策状态改为「已采纳」」.
2. Open: access from China (#44) · an email service that stays out of QQ / 163 spam · parents entering card details (#14)
   · how long deleted data lingers (#20). Two product calls, provisional until #14 and #20 decide: parents see nothing
   new by default (D:162) · deleting a student's account deletes their card (D:190-194). Two decisions numbered 0006:
   triage chat (2026-10-28, PR #41) and backend (2026-10-30, PR #43).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, NARRATION, USER_C, WEB_C, chip, clear, mark_ok, mono, sans, zh)

SAY = NARRATION["S08"]


class Open(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- a test would; the decision waits for a confirmation
        with self.voiceover(SAY[0]) as vo:
            crit = VGroup(sans("the record's own success test (#13, #14)", 22, S.GREY),
                          VGroup(sans("student unlinks", 26), Arrow(LEFT * 0.4, RIGHT * 0.4, color=S.GREY, buff=0),
                                 sans("parent's next request", 26), Arrow(LEFT * 0.4, RIGHT * 0.4, color=S.GREY, buff=0),
                                 mono("403", 32, DANGER_C)).arrange(RIGHT, buff=0.25),
                          VGroup(mark_ok(0.26, CHECKED_C), sans("checked by an automated test", 22, CHECKED_C)).arrange(RIGHT, buff=0.15)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 1.9)
            vo.wait_until("A test would")
            self.play(FadeIn(crit[0]), FadeIn(crit[1]), run_time=0.6)
            vo.wait_until("checked automatically")
            self.play(FadeIn(crit[2]), run_time=0.4)
            box = Square(0.36, color=S.GREY, stroke_width=2.5)
            todo = VGroup(box, zh("线下三人确认后，决策状态改为「已采纳」", 26)).arrange(RIGHT, buff=0.25)
            status = VGroup(sans("status:", 24, S.GREY), chip("提议", S.GREY, 24, mono_font=False)).arrange(RIGHT, buff=0.2)
            wait = VGroup(status, todo, sans("issue #11 · still open", 20, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            wait.move_to(DOWN * 1.2)
            vo.wait_until("still a proposal")
            self.play(FadeIn(status), run_time=0.4)
            vo.wait_until("confirm it in person")
            self.play(FadeIn(todo), FadeIn(wait[2]), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- open questions; two product calls; the clash
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            qs = VGroup(sans("access from China? (#44)", 24), sans("an email service that stays out of QQ / 163 spam?", 24),
                        sans("may parents enter card details? (#14)", 24), sans("how long does deleted data linger? (#20)", 24)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(LEFT * 1.6 + UP * 2.0)
            for q, phrase in zip(qs, ["reached from China", "QQ and 163", "enter card details", "deleted data lingers"]):
                vo.wait_until(phrase)
                self.play(FadeIn(q, shift=RIGHT * 0.1), run_time=0.35)
            calls = VGroup(sans("two product calls, provisional until #14 and #20 decide", 22, USER_C),
                           chip("parents see nothing new by default", USER_C, 22, mono_font=False),
                           chip("deleting a student's account deletes their card", USER_C, 22, mono_font=False)
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(LEFT * 1.6 + DOWN * 0.6)
            vo.wait_until("Two product calls")
            self.play(FadeIn(calls[0]), run_time=0.3)
            vo.wait_until("parents see nothing new")
            self.play(FadeIn(calls[1]), run_time=0.35)
            vo.wait_until("deletes their card")
            self.play(FadeIn(calls[2]), run_time=0.35)
            clash = VGroup(mono("0006 · triage chat copies Claude · 10-28 · PR #41", 22, S.GREY),
                           mono("0006 · backend stack · 10-30 · PR #43", 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            frame = SurroundingRectangle(clash, color=DANGER_C, buff=0.2, corner_radius=0.1)
            note = VGroup(frame, clash, sans("two decisions, one number", 22, DANGER_C).next_to(frame, RIGHT, buff=0.3))
            note.move_to(DOWN * 2.75)
            vo.wait_until("both numbered six")
            self.play(FadeIn(note), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
