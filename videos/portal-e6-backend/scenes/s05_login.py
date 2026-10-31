"""S05 · Login without passwords (decision 0006 D:53-62, D:82-86; PR #43 body; ../SOURCES.md)

1. Email → a 6-digit code, 5 minutes, 3 tries; the record requires storing only a hash (`storeOTP: 'hashed'`; the
   library default is plain) and its own per-email limit, 1 per 60 s and 5 per hour (the library's own limiter is
   IP-based); `AUTH_LOG_OTP` prints codes in dev only. The PR body notes the owner confirmed email-only on Friday
   (「Junyi 2026-10-30 确认」); the reasons are the record's (D:59).
2. Rejected: SMS 「发国内号码要花钱」, WeChat 「需要企业资质和开放平台审核」, Clerk / Auth0 (D:54), Lucia 「已停止维护」 (D:55),
   from scratch 「容易出安全问题」 (D:57). Chosen: Better Auth, inside our server, in our own Postgres.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AUTH_C, CHECKED_C, DB_C, NARRATION, USER_C, chip, clear, mono, option, sans, stopwatch, zh)

SAY = NARRATION["S05"]


class Login(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- a code by email
        with self.voiceover(SAY[0]) as vo:
            mail = VGroup(RoundedRectangle(width=3.0, height=0.7, corner_radius=0.12, stroke_color=S.GREY, stroke_width=2),
                          mono("you@qq.com", 24, S.GREY))
            mail[1].move_to(mail[0])
            mail.move_to(LEFT * 4.4 + UP * 2.2)
            vo.wait_until("no passwords at all")
            nopw = VGroup(sans("password", 24, S.GREY), Line(LEFT * 0.7, RIGHT * 0.7, color=USER_C, stroke_width=4))
            nopw[1].move_to(nopw[0])
            nopw.next_to(mail, DOWN, buff=0.3)
            self.play(FadeIn(mail), FadeIn(nopw), run_time=0.5)
            code = VGroup(*[VGroup(RoundedRectangle(width=0.55, height=0.75, corner_radius=0.08, stroke_color=AUTH_C, stroke_width=2.5),
                                   mono(d, 30, AUTH_C)) for d in "482915"])
            for c in code:
                c[1].move_to(c[0])
            code.arrange(RIGHT, buff=0.12).move_to(RIGHT * 0.6 + UP * 2.2)
            send = Arrow(mail.get_right(), code.get_left(), color=S.GREY, buff=0.15)
            vo.wait_until("six-digit code")
            self.play(GrowArrow(send), LaggedStart(*[FadeIn(c) for c in code], lag_ratio=0.1), run_time=0.8)
            watch = stopwatch(0.35, AUTH_C).next_to(code, RIGHT, buff=0.5)
            facts = VGroup(sans("5 minutes", 24, AUTH_C), sans("3 tries", 24, AUTH_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            facts.next_to(watch, RIGHT, buff=0.25)
            vo.wait_until("valid for five minutes")
            self.play(FadeIn(watch), FadeIn(facts[0]), Rotate(watch[2], angle=-PI, about_point=watch[0].get_center()), run_time=0.7)
            vo.wait_until("three tries")
            self.play(FadeIn(facts[1]), run_time=0.3)
            vo.wait_until("scrambled hash")
            lock = VGroup(sans("server keeps:", 22, S.GREY), mono("#a91f…e03c", 24, DB_C), sans("(a hash, not the code)", 20, S.GREY)
                          ).arrange(RIGHT, buff=0.2).move_to(UP * 0.7)
            self.play(FadeIn(lock), run_time=0.5)
            vo.wait_until("one code a minute")
            limits = VGroup(VGroup(chip("1 code / 60 s / email", USER_C, 22, mono_font=False),
                                   chip("at most 5 / hour", USER_C, 22, mono_font=False)).arrange(RIGHT, buff=0.25),
                            sans("the record's own rule, on top of the library's default", 20, S.GREY)
                            ).arrange(DOWN, buff=0.12).move_to(DOWN * 0.45)
            self.play(FadeIn(limits), run_time=0.5)
            vo.wait_until("you confirmed email-only")
            conf = VGroup(sans("PR #43 notes:", 22, S.GREY), zh("「MVP 只用邮箱验证码（Junyi 2026-10-30 确认）」", 24, USER_C)
                          ).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.65)
            self.play(FadeIn(conf), run_time=0.5)
            vo.wait_until("The record's reasons")
            why = VGroup(sans("every Chinese parent has an email (QQ, 163 …)", 24), sans("no password to forget", 24)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(DOWN * 2.65)
            self.play(FadeIn(why), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- what lost; what was chosen
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            opts = VGroup(option("SMS", "发国内号码要花钱", False, width=5.8),
                          option("WeChat login", "需要企业资质和开放平台审核", False, width=5.8),
                          option("Clerk · Auth0", "用户数据存在第三方；按用户数收费；国内访问情况不确定", False, width=5.8),
                          option("build it ourselves", "容易出安全问题", False, width=5.8)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            opts.move_to(LEFT * 3.2 + UP * 0.3)
            for o, phrase in zip(opts, ["Text messages", "WeChat login", "hosted login services", "from scratch"]):
                vo.wait_until(phrase)
                self.play(FadeIn(o, shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("Better Auth")
            chosen = option("Better Auth", "inside our own server · stores everything in our own Postgres", True, width=5.4)
            chosen.move_to(RIGHT * 3.4 + UP * 0.3)
            self.play(FadeIn(chosen, scale=1.05), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
