"""S01 · Nowhere to fetch it from (decision 0006 「问题陈述」; ../SOURCES.md)

1. Today the prototype is front-end only: data from `src/data` (fictional), state in the browser's
   `localStorage`. A student's laptop in Boston and a parent's phone in China, each with its own drawer; the parent's
   request for the card finds nothing. Accounts (#13), family links (#14), insurance cards (#22) need one place.
   The clinics and prices shown are made up (docs/ARCHITECTURE.md §1).
2. The record: 「0006：后端用 TypeScript（Hono + Postgres），账号用邮箱验证码，Docker Compose 容器化」, 提议,
   2026-10-30, 223 lines, PR #43 (commit 57cbffa Fri 17:24 Boston).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (DANGER_C, NARRATION, USER_C, WEB_C, chip, clear, device, mark_bad, mono, sans, zh, zh_wrap)

SAY = NARRATION["S01"]


def drawer(width: float = 2.2, stacked: bool = False) -> VGroup:
    box = RoundedRectangle(width=width, height=0.85 if stacked else 0.55, corner_radius=0.08, stroke_color=WEB_C, stroke_width=2)
    return VGroup(box, mono("local\nStorage" if stacked else "localStorage", 20, WEB_C).move_to(box))


class Hook(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- two devices, two drawers, nothing shared
        with self.voiceover(SAY[0]) as vo:
            lap = device("student · Boston", 3.4, 2.2).move_to(LEFT * 3.8 + UP * 1.2)
            phone = device("parent · China", phone=True, height=2.4).move_to(RIGHT * 3.8 + UP * 1.2)
            self.play(FadeIn(lap), FadeIn(phone), run_time=0.6)
            d1 = drawer().move_to(lap.body)
            d2 = drawer(1.25, stacked=True).move_to(phone.body)
            vo.wait_until("in that one browser")
            self.play(FadeIn(d1), FadeIn(d2), run_time=0.5)
            vo.wait_until("made up")
            fake = VGroup(mono("src/data", 22, S.GREY), sans("made-up clinics and prices", 22, S.GREY)).arrange(RIGHT, buff=0.2)
            fake.next_to(lap, UP, buff=0.2)
            self.play(FadeIn(fake), run_time=0.4)
            vo.wait_until("cannot see the insurance card")
            card = VGroup(RoundedRectangle(width=1.1, height=0.7, corner_radius=0.08, stroke_color=USER_C, stroke_width=2),
                          zh("保险卡", 20, USER_C))
            card[1].move_to(card[0])
            card.next_to(d1, DOWN, buff=0.15)
            self.play(FadeIn(card, scale=1.2), run_time=0.4)
            ask = Arrow(phone.body.get_left(), lap.body.get_right() + RIGHT * 1.0, color=DANGER_C, buff=0.1)
            self.play(GrowArrow(ask), run_time=0.6)
            miss = VGroup(mark_bad(0.3, DANGER_C), sans("nowhere to fetch it from", 24, DANGER_C)).arrange(RIGHT, buff=0.15)
            miss.next_to(ask, DOWN, buff=0.2)
            vo.wait_until("nowhere to fetch it from")
            self.play(FadeIn(miss), run_time=0.4)
            needs = VGroup(chip("#13 accounts", WEB_C, 22), chip("#14 family links", WEB_C, 22), chip("#22 insurance cards", WEB_C, 22)
                           ).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.9)
            place = VGroup(RoundedRectangle(width=4.4, height=0.7, corner_radius=0.14, stroke_color=USER_C, stroke_width=2.5),
                           sans("one shared place?", 26, USER_C))
            place[1].move_to(place[0])
            place.move_to(DOWN * 3.1)
            vo.wait_until("Accounts, family links")
            self.play(LaggedStart(*[FadeIn(c) for c in needs], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("one shared place")
            self.play(FadeIn(place), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the decision record
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            title = zh_wrap("0006：后端用 TypeScript（Hono + Postgres），账号用邮箱验证码，Docker Compose 容器化", 10.5, 30)
            meta = VGroup(chip("提议", S.GREY, 24, mono_font=False), sans("2026-10-30 · 223 lines · PR #43", 24, S.GREY)
                          ).arrange(RIGHT, buff=0.3)
            doc = VGroup(title, meta).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
            frame = SurroundingRectangle(doc, color=S.GREY_DARK, buff=0.35, corner_radius=0.14).set_fill(S.GREY_DARKER, 1)
            rec = VGroup(frame, doc).move_to(UP * 0.6)
            vo.wait_until("an agent wrote")
            self.play(FadeIn(rec, shift=UP * 0.1), run_time=0.7)
            when = sans("written by an agent · Friday 17:24, Boston", 24, S.GREY).next_to(rec, DOWN, buff=0.4)
            self.play(FadeIn(when), run_time=0.4)
            vo.wait_until("what it protects")
            q = sans("how did it choose, and what does it protect?", 30, USER_C).next_to(when, DOWN, buff=0.5)
            self.play(FadeIn(q), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
