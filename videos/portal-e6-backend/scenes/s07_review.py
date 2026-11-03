"""S07 · Review, and one missing word (PR #43 body; commits 57cbffa → 1f5f2c5 → f163e90; ../SOURCES.md)

1. Four review angles → 31 comments → a judge → 14 kept, applied in the second version (1f5f2c5, 17:31). Fixes:
   home-made status/source labels per insurance field (`clear · card · inferred`) → PR #38's (`confidence · source · raw`)
   (handoff 「初稿里保险字段的状态和来源名称是 agent 自己起的，没先读 PR #38 的代码」); linked parents could enter cards
   (57cbffa:142) → read-only (D:185); reuse of the mock-data services → banned (D:79).
2. The revision's own mistake: unlinking only set `revokedAt` (1f5f2c5:161), status stayed active; Bugbot 17:38:29 "Revoke
   leaves family links active"; fix f163e90 at 17:38:50 (21 s); reply 「属实，已修复」. A written plan; no code yet.
3. Ponder: if no bot had been watching, what would have caught it?
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, NARRATION, USER_C, WEB_C, chip, clear, mono, ponder_zh, sans, zh)

SAY = NARRATION["S07"]
ANGLES = ["outside facts", "consistency with the repo", "privacy · data model", "the issue's checklist"]


def before_after(before: str, after: str, size: float = 22) -> VGroup:
    b = sans(before, size, S.GREY) if before.isascii() else zh(before, size, S.GREY)
    a = sans(after, size, CHECKED_C) if after.isascii() else zh(after, size, CHECKED_C)
    arrow = Arrow(LEFT * 0.3, RIGHT * 0.3, color=S.GREY, buff=0)
    g = VGroup(b, arrow, a).arrange(RIGHT, buff=0.25)
    g.add(Line(b.get_left(), b.get_right(), color=DANGER_C, stroke_width=3))
    return g


class Review(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- four reviewers, a judge, three fixes
        with self.voiceover(SAY[0]) as vo:
            revs = VGroup(*[chip(a, S.GREY, 22, mono_font=False) for a in ANGLES]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            revs.move_to(LEFT * 4.6 + UP * 1.8)
            vo.wait_until("four reviewers")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in revs], lag_ratio=0.2), run_time=1.0)
            n31 = sans("31 comments", 30, S.WHITE).move_to(LEFT * 0.6 + UP * 1.8)
            n14 = sans("14 kept", 30, CHECKED_C).move_to(RIGHT * 3.6 + UP * 1.8)
            judge = sans("a judge agent", 22, USER_C).move_to(RIGHT * 1.6 + UP * 2.25)
            a1 = Arrow(revs.get_right(), n31.get_left(), color=S.GREY, buff=0.2)
            a2 = Arrow(n31.get_right(), n14.get_left(), color=S.GREY, buff=0.2)
            vo.wait_until("thirty-one comments")
            self.play(GrowArrow(a1), FadeIn(n31), run_time=0.5)
            vo.wait_until("a judge agent kept fourteen")
            self.play(GrowArrow(a2), FadeIn(judge), FadeIn(n14), run_time=0.6)
            ver = sans("→ the second version · 17:31", 22, S.GREY).next_to(n14, DOWN, buff=0.15)
            self.play(FadeIn(ver), run_time=0.3)
            fixes = VGroup(before_after("clear · card · inferred", "confidence · source · raw (PR #38's own)"),
                           before_after("linked parents enter cards", "parents: read-only"),
                           before_after("reuse the services with fictional data", "banned in the backend")
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.9)
            for f, phrase in zip(fixes, ["status and source labels", "let linked parents enter cards", "reuse services"]):
                vo.wait_until(phrase)
                self.play(FadeIn(f, shift=RIGHT * 0.1), run_time=0.45)
            admit = VGroup(sans("the handoff admits:", 20, S.GREY),
                           zh("「初稿里保险字段的状态和来源名称是 agent 自己起的，没先读 PR #38 的代码」", 22, USER_C)
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(DOWN * 2.85)
            self.play(FadeIn(admit), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- one missing word
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            row = VGroup(mono("family_link", 26, WEB_C), mono("revokedAt = set", 24, S.WHITE),
                         VGroup(mono("status =", 24), mono("active", 24, DANGER_C)).arrange(RIGHT, buff=0.22)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            frame = SurroundingRectangle(row, color=WEB_C, buff=0.3, corner_radius=0.12)
            plan = VGroup(sans("the second version's written rule for unlinking", 22, S.GREY), VGroup(frame, row)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(LEFT * 3.0 + UP * 1.3)
            vo.wait_until("a mistake of its own")
            self.play(FadeIn(plan), run_time=0.6)
            vo.wait_until("left the link marked active")
            self.play(Indicate(row[2], color=DANGER_C, scale_factor=1.08), run_time=0.6)
            access = sans("→ a parent's request would still succeed", 24, DANGER_C).next_to(plan, DOWN, buff=0.25).align_to(plan, LEFT)
            self.play(FadeIn(access), run_time=0.4)
            bot = VGroup(sans("Bugbot · 17:38:29", 24, USER_C), sans("\"Revoke leaves family links active\"", 24)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(RIGHT * 3.4 + UP * 1.9)
            vo.wait_until("Bugbot caught it")
            self.play(FadeIn(bot, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("One missing word")
            fixed = mono("revoked", 24, CHECKED_C).move_to(row[2][1], aligned_edge=LEFT)
            self.play(Transform(row[2][1], fixed), run_time=0.6)
            refused = sans("→ one word, revoked: the parent's request is refused", 24, CHECKED_C).move_to(access, aligned_edge=LEFT)
            self.play(Transform(access, refused), run_time=0.5)
            note = sans("a written plan · no code existed yet", 22, S.GREY).next_to(access, DOWN, buff=0.15).align_to(plan, LEFT)
            self.play(FadeIn(note), run_time=0.3)
            vo.wait_until("twenty-one seconds")
            fix = VGroup(sans("fix · 17:38:50 · 21 s later", 24, CHECKED_C), zh("「属实，已修复」", 24, CHECKED_C)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(bot, DOWN, buff=0.4).align_to(bot, LEFT)
            self.play(FadeIn(fix), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- ponder
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.4)
            ponder_zh(self, "If no bot had been watching, what would have caught it?", "如果没有 bot 盯着，什么能抓住它？", seconds=4.0)
        self.wait(3.0)
        clear(self)
