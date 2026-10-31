"""S06 · A data model that protects people (decision 0006 D:92-194; ../SOURCES.md)

1. `user`: role student | parent, written once, `input: false` (Better Auth's default is `true`), not changeable by the
   user in this first version (D:116); 「否则学生能把自己改成家长」.
2. `family_link`: only the student starts it (D:150); invite code ≥ 8 characters, 72 h, single use (HMAC-SHA256,
   D:152-156); once linked, the parent sees the profile and the current card, read-only (D:185); later data such as
   triage closed by default (D:162). 「不存保险卡图片」 (D:181, for the MVP); the card is read on the device (0005:33).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AUTH_C, CHECKED_C, DANGER_C, DB_C, NARRATION, USER_C, WEB_C, chip, clear, device, mark_bad, mono, sans,
                    table_card, zh)

SAY = NARRATION["S06"]


class Model(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the role
        with self.voiceover(SAY[0]) as vo:
            head = sans("the shape of the data", 28, DB_C).move_to(UP * 3.1)
            user = table_card("user", ["email", "role: student | parent", "input: false"], DB_C, 4.0).move_to(LEFT * 3.8 + UP * 1.0)
            vo.wait_until("the part that protects people")
            self.play(FadeIn(head), FadeIn(user), run_time=0.6)
            vo.wait_until("written once")
            once = VGroup(chip("written once", USER_C, 22, mono_font=False),
                          chip("the user can't change it (first version)", USER_C, 22, mono_font=False)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(user, RIGHT, buff=0.5)
            self.play(FadeIn(once), run_time=0.5)
            vo.wait_until("make themselves a parent")
            attempt = VGroup(sans("student → role: parent", 24, S.GREY), mark_bad(0.3, DANGER_C)).arrange(RIGHT, buff=0.25)
            attempt.move_to(LEFT * 3.8 + DOWN * 1.4)
            why = zh("「否则学生能把自己改成家长」", 26, USER_C).next_to(attempt, RIGHT, buff=0.6)
            self.play(FadeIn(attempt), FadeIn(why), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the family link
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            student = device("student", 2.6, 1.7).move_to(LEFT * 4.6 + UP * 1.6)
            parent = device("parent", phone=True, height=1.9).move_to(RIGHT * 4.6 + UP * 1.6)
            vo.wait_until("Only the student")
            self.play(FadeIn(student), FadeIn(parent), run_time=0.5)
            only = sans("only the student starts it: the patient owns the health data", 22, USER_C).move_to(UP * 3.3)
            self.play(FadeIn(only), run_time=0.4)
            code = VGroup(RoundedRectangle(width=2.6, height=0.8, corner_radius=0.12, stroke_color=AUTH_C, stroke_width=2.5),
                          mono("K7QW-3MRT", 28, AUTH_C))
            code[1].move_to(code[0])
            code.move_to(UP * 1.6)
            facts = VGroup(sans("≥ 8 characters", 22, S.GREY), sans("72 hours", 22, S.GREY), sans("usable once", 22, S.GREY)
                           ).arrange(RIGHT, buff=0.35).next_to(code, DOWN, buff=0.2)
            vo.wait_until("invite code")
            self.play(FadeIn(code, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("seventy-two hours")
            self.play(FadeIn(facts), run_time=0.4)
            self.play(code.animate.move_to(RIGHT * 2.55 + UP * 1.6), run_time=0.6)
            vo.wait_until("Once linked")
            link = Line(student.body.get_right(), parent.body.get_left(), color=CHECKED_C, stroke_width=5)
            self.play(FadeOut(code), FadeOut(facts), Create(link), run_time=0.6)
            sees = VGroup(VGroup(sans("the parent sees:", 22, S.GREY), chip("profile", CHECKED_C, 22, mono_font=False), chip("current card · read-only", CHECKED_C, 22, mono_font=False)
                                 ).arrange(RIGHT, buff=0.2),
                          VGroup(VGroup(mark_bad(0.22, DANGER_C), sans("closed by default:", 22, S.GREY)).arrange(RIGHT, buff=0.12), chip("triage chats", S.GREY, 22, mono_font=False), chip("anything added later", S.GREY, 22, mono_font=False)
                                 ).arrange(RIGHT, buff=0.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 0.4)
            self.play(FadeIn(sees[0]), run_time=0.5)
            vo.wait_until("closed to parents by default")
            self.play(FadeIn(sees[1]), run_time=0.5)
            vo.wait_until("card photos are not stored")
            photo = VGroup(zh("「不存保险卡图片」", 26, USER_C), sans("read on the device · only the text fields are kept", 22, S.GREY)
                           ).arrange(DOWN, buff=0.1).move_to(DOWN * 2.6)
            self.play(FadeIn(photo, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
