"""S04 · Why it slipped through, and what the agent did not do (../SOURCES.md)

1. A mechanism: the saved referral (status, validUntil); the booking step reads only the stored status (reducer.ts:286-294); 'expired' is never stored, only computed for the
   screen (selectors.ts:104-140); the page checks when it draws, not on submit (BookingPage.tsx:102, :403-409).
   The product code is unchanged; the bug is a known finding; the fix is a person's call (SKILL.md:65).
2. The rule is not loosened; the check fails on any new broken rule and when the known finding disappears
   (referral-links.verify.ts:4-14, :31-34: 「修好后把它从 KNOWN_FINDINGS 删掉」).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, MODEL_C, NARRATION, OURS_C, USER_C, clear, mark_bad, mark_ok, mono, sans, zh)

SAY = NARRATION["S04"]


def panel(head: str, rows: list, color, width: float = 3.6) -> VGroup:
    """A titled box: a head line over a few rows (each a mobject)."""
    body = VGroup(sans(head, 22, color), *rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    frame = RoundedRectangle(width=max(width, body.width + 0.5), height=body.height + 0.4, corner_radius=0.14,
                             stroke_color=color, stroke_width=2.5)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.25)
    return VGroup(frame, body)


class Finding(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- three gaps; the agent leaves the fix to a person
        with self.voiceover(SAY[0]) as vo:
            # the saved referral: its status is all the booking step reads
            status, until = mono("status: issued", 22), mono("validUntil: 01-22", 22, S.GREY)
            record = panel("saved data · ref-v1", [status, until], OURS_C).move_to(LEFT * 4.2 + UP * 1.9)
            book = panel("booking step (reducer)", [mono("status issued → free", 22), sans("→ links the referral", 22, DANGER_C)],
                         MODEL_C).move_to(RIGHT * 3.7 + UP * 2.4)
            reads = Arrow(status.get_right(), book.get_left(), color=S.GREY, buff=0.2)
            reads_lab = sans("reads only this", 20, S.GREY).next_to(reads.get_center(), UP, buff=0.12)
            vo.wait_until("looks only at")
            self.play(FadeIn(record), run_time=0.4)
            self.play(GrowArrow(reads), FadeIn(reads_lab), FadeIn(book), run_time=0.7)
            # "expired" exists only on the screen
            screen_ = panel("the screen", [zh("已过期", 26, DANGER_C)], S.GREY, width=2.6).move_to(RIGHT * 3.7 + UP * 0.6)
            worked = DashedLine(until.get_right(), screen_.get_left(), color=S.GREY, dash_length=0.12).add_tip(tip_length=0.18)
            worked_lab = sans("worked out for display, never saved", 20, S.GREY).next_to(worked.get_center(), DOWN, buff=0.15)
            vo.wait_until("never stored")
            self.play(Create(worked), FadeIn(worked_lab), FadeIn(screen_), run_time=0.7)
            self.play(Indicate(status, color=USER_C, scale_factor=1.06), run_time=0.6)
            # the page checked once, when it drew
            when = VGroup(VGroup(mark_ok(0.24, CHECKED_C), sans("page draws: referral checked", 22, CHECKED_C)).arrange(RIGHT, buff=0.12),
                          sans("…the page stays open…", 22, S.GREY),
                          VGroup(mark_bad(0.24, DANGER_C), sans("submit: no check", 22, DANGER_C)).arrange(RIGHT, buff=0.12)
                          ).arrange(RIGHT, buff=0.45).move_to(DOWN * 0.45)
            vo.wait_until("checks when it draws")
            self.play(FadeIn(when[0]), run_time=0.4)
            self.play(FadeIn(when[1]), run_time=0.3)
            vo.wait_until("not when you submit")
            self.play(FadeIn(when[2]), run_time=0.4)
            vo.wait_until("did not change the product code")
            note = VGroup(zh("已知发现（未修）", 28, USER_C), zh("过期的转诊不会关联到新预约", 22, S.GREY),
                          sans("time passes → book S1 with ref-v1", 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            pin = SurroundingRectangle(note, color=USER_C, buff=0.25, corner_radius=0.12)
            known = VGroup(pin, note).move_to(LEFT * 3.6 + DOWN * 2.1)
            self.play(FadeIn(known, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("left the fix to a person")
            fixes = VGroup(sans("fix, for a person to choose:", 22, S.GREY),
                           sans("compare the expiry in the reducer", 22), sans("→ guards every booking", 20, S.GREY),
                           sans("or check again on submit", 22), sans("→ guards this page only", 20, S.GREY)
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            fixes.move_to(RIGHT * 3.3 + DOWN * 2.1)
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
