"""S08 · Where it came from, and what waits (../SOURCES.md)

1. From trying two skills of pstack, a public plugin of agent skills (create-formal-verification-skill,
   create-verification-skill), in a conversation, no issue (PR body); Fri 16:13 c0920b0 → 16:40 fe19a23; Bugbot twice,
   no issues. Claude Code best practices: "Give Claude a check to run … that makes you the test suite."
2. What waits: the expired-referral fix (reducer or on submit); verify-app only run in the cloud container (local
   install untested); the PR is a draft. E4's layers plus two: every order, and the real app.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, MODEL_C, NARRATION, OURS_C, USER_C, chip, clear, mono, quote_panel, sans, zh)

SAY = NARRATION["S08"]


class Waits(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- origin
        with self.voiceover(SAY[0]) as vo:
            skills = VGroup(sans("pstack · a public plugin of agent skills", 26, MODEL_C),
                            mono("create-formal-verification-skill", 24), mono("create-verification-skill", 24)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(LEFT * 2.8 + UP * 2.3)
            vo.wait_until("two skills")
            self.play(FadeIn(skills, shift=UP * 0.1), run_time=0.6)
            line = Line(LEFT * 5.5 + DOWN * 0.1, RIGHT * 5.5 + DOWN * 0.1, color=S.GREY, stroke_width=2)

            def x_of(minute):           # minutes after 16:00, Friday, Boston
                return -5.5 + minute / 50 * 11.0
            c1 = VGroup(Dot([x_of(13), -0.1, 0], radius=0.1, color=OURS_C), sans("16:13 · the exhaustive check", 22, OURS_C))
            c1[1].next_to(c1[0], UP, buff=0.15)
            c2 = VGroup(Dot([x_of(40), -0.1, 0], radius=0.1, color=OURS_C), sans("16:40 · verify-app", 22, OURS_C))
            c2[1].next_to(c2[0], UP, buff=0.15)
            gap = sans("27 minutes · Friday, Boston", 22, S.GREY).move_to([x_of(26.5), -0.55, 0])
            bots = sans("Bugbot, twice: no issues found", 22, S.GREY).move_to([x_of(26.5), -0.95, 0])
            vo.wait_until("two commits")
            self.play(Create(line), FadeIn(c1), FadeIn(c2), FadeIn(gap), FadeIn(bots), run_time=0.8)
            vo.wait_until("Anthropic's own advice")
            q = quote_panel("If it has nothing to run that tells it whether the work actually is done, \"looks done\" is all it has to "
                            "go on. In practice that makes you the test suite.", "Claude Code docs · Best practices", width=12.4,
                            size=22, color=USER_C).move_to(DOWN * 2.55)
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- what waits; two more layers
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            head = sans("what waits for you", 28, USER_C).move_to(UP * 3.0)
            items = VGroup(sans("1  choose the fix: compare the expiry in the reducer, or check again on submit", 24),
                           sans("2  try verify-app on your own laptop: only run in the cloud container so far", 24),
                           sans("3  the pull request is still a draft", 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            items.next_to(head, DOWN, buff=0.3)
            vo.wait_until("What waits for you")
            self.play(FadeIn(head), run_time=0.3)
            for it, phrase in zip(items, ["choosing the fix", "on your own laptop", "still a draft"]):
                vo.wait_until(phrase)
                self.play(FadeIn(it, shift=RIGHT * 0.1), run_time=0.4)
            layers = VGroup(*[chip(t, S.GREY, 22, mono_font=False) for t in
                              ["unit tests", "probes", "review bots", "提议 until signed"]]).arrange(RIGHT, buff=0.2)
            new = VGroup(chip("every order", CHECKED_C, 22, mono_font=False), chip("the real app", CHECKED_C, 22, mono_font=False)
                         ).arrange(RIGHT, buff=0.2)
            row = VGroup(layers, new).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.6)
            lab = sans("episode 4's layers, and two more", 22, S.GREY).next_to(row, UP, buff=0.2)
            vo.wait_until("layers stood in")
            self.play(FadeIn(lab), LaggedStart(*[FadeIn(c) for c in layers], lag_ratio=0.1), run_time=0.8)
            vo.wait_until("Here are two more")
            self.play(LaggedStart(*[FadeIn(c, scale=1.15) for c in new], lag_ratio=0.3), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
