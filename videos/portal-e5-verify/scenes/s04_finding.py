"""S04 · Why it slipped through, and what the agent did not do (../SOURCES.md)

1. Booking checks only the stored status (reducer.ts:286-294); 'expired' is never stored, only computed for the
   screen (selectors.ts:104-140); the page checks when it draws, not on submit (BookingPage.tsx:102, :403-409).
   The product code is unchanged; the bug is a known finding; the fix is a person's call (SKILL.md:65).
2. The rule is not loosened; the check fails on any new broken rule and when the known finding disappears
   (referral-links.verify.ts:4-14, :31-34: 「修好后把它从 KNOWN_FINDINGS 删掉」).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, NARRATION, OURS_C, USER_C, clear, mark_bad, mono, sans, zh)

SAY = NARRATION["S04"]


def reason(n: str, text: str, width: float = 4.0) -> VGroup:
    body = VGroup(sans(n, 30, DANGER_C), sans(text, 20)).arrange(DOWN, buff=0.15)
    frame = RoundedRectangle(width=max(width, body.width + 0.5), height=body.height + 0.5, corner_radius=0.14, stroke_color=DANGER_C, stroke_width=2.5)
    body.move_to(frame)
    return VGroup(frame, body)


class Finding(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- three gaps; the agent leaves the fix to a person
        with self.voiceover(SAY[0]) as vo:
            cards = VGroup(reason("1", "booking looks only at\nthe stored status"),
                           reason("2", "“expired” is never stored,\nonly worked out for the screen"),
                           reason("3", "the page checks when it draws,\nnot when you submit")).arrange(RIGHT, buff=0.25)
            cards.move_to(UP * 1.9)
            for c, phrase in zip(cards, ["looks only at", "never stored", "checks when it draws"]):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=UP * 0.1), run_time=0.45)
            vo.wait_until("did not change the product code")
            note = VGroup(zh("已知发现（未修）", 28, USER_C), zh("过期的转诊不会关联到新预约", 22, S.GREY),
                          sans("time passes → book S1 with ref-v1", 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            pin = SurroundingRectangle(note, color=USER_C, buff=0.25, corner_radius=0.12)
            known = VGroup(pin, note).move_to(LEFT * 3.4 + DOWN * 1.2)
            self.play(FadeIn(known, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("left the fix to a person")
            fixes = VGroup(sans("fix, for a person to choose:", 22, S.GREY), sans("compare the expiry inside the reducer", 22),
                           sans("or check again on submit", 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            fixes.move_to(RIGHT * 3.3 + DOWN * 1.2)
            self.play(FadeIn(fixes), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the check fails both ways
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            vo.wait_until("not loosened")
            rule = VGroup(zh("规则 5：过期的转诊不会关联到新预约", 26, USER_C), sans("unchanged", 22, CHECKED_C)
                          ).arrange(RIGHT, buff=0.4).move_to(UP * 2.6)
            self.play(FadeIn(rule), run_time=0.5)
            left = VGroup(sans("any new broken rule", 26), Arrow(UP * 0.3, DOWN * 0.3, color=S.GREY, buff=0),
                          VGroup(mark_bad(0.3, DANGER_C), sans("the check fails", 26, DANGER_C)).arrange(RIGHT, buff=0.15)
                          ).arrange(DOWN, buff=0.25).move_to(LEFT * 3.3 + UP * 0.3)
            right = VGroup(sans("the known bug disappears", 26), sans("(someone fixed it)", 22, S.GREY),
                           Arrow(UP * 0.3, DOWN * 0.3, color=S.GREY, buff=0),
                           VGroup(mark_bad(0.3, DANGER_C), sans("the check fails too", 26, DANGER_C)).arrange(RIGHT, buff=0.15)
                           ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.3 + UP * 0.2)
            vo.wait_until("if any new rule breaks")
            self.play(FadeIn(left, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("ever disappears")
            self.play(FadeIn(right, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("delete the note")
            msg = VGroup(zh("「修好后把它从 KNOWN_FINDINGS 删掉」", 26, USER_C), mono("referral-links.verify.ts", 20, S.GREY)
                         ).arrange(DOWN, buff=0.1).move_to(DOWN * 2.4)
            self.play(FadeIn(msg, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
