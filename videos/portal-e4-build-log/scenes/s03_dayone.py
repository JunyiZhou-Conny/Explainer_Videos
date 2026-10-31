"""S03 · Day one: a skeleton, then a fact check

1. Tue 12:22–13:03 (41 min): 15 official pages → 74 fact cards · a rules engine · 11 test cases · an evaluation.
2. knowledge/reviews/2026-10-27.md: 4 reviewer agents that cannot talk to each other, read-only; 75 problems →
   97 cards, 7 conflicts (7ca4628, 23 min later); the out-of-network urgent-care card before and after.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, H36, MODEL_C, NARRATION, USER_C, clear, commit_ticks, doc_glyph, quote_panel, sans,
                    tag_box, zh)

SAY = NARRATION["S03"]


class DayOne(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- forty minutes
        with self.voiceover(SAY[0]) as vo:
            when = VGroup(sans("Tue 12:22 → 13:03 Boston · Wed 00:22 → 01:03 Beijing", 28, MODEL_C), sans("session 1's first commits · after a night of planning", 22, S.GREY)
                          ).arrange(DOWN, buff=0.1).move_to(UP * 3.0)
            self.play(FadeIn(when), run_time=0.5)
            first = [h for h in H36 if h < 13.1]           # 12:22 → 13:03, seven commits
            strip = Line([-1.5, -2.6, 0], [5.5, -2.6, 0], color=S.GREY, stroke_width=2)

            def sx(h):
                return -1.5 + (h - 12.3) / (13.1 - 12.3) * 7.0
            sticks = commit_ticks(sx, first, -2.6, 0.5, MODEL_C)
            before = VGroup(sans("before: a night of planning", 22, S.GREY), sans("research · two designs · reviews", 20, S.GREY)
                            ).arrange(DOWN, aligned_edge=RIGHT, buff=0.06).next_to(strip, LEFT, buff=0.4)
            ends = VGroup(sans("12:22", 20, S.GREY).move_to([sx(12.37), -3.1, 0]), sans("13:03", 20, S.GREY).move_to([sx(13.05), -3.1, 0]))
            self.play(FadeIn(before), Create(strip), run_time=0.5)
            vo.wait_until("started committing")
            self.play(LaggedStart(*[Create(t) for t in sticks], lag_ratio=0.2), FadeIn(ends), run_time=1.0)
            pages = VGroup(*[doc_glyph(S.GREY, 0.36, 0.48, 3) for _ in range(15)]).arrange_in_grid(3, 5, buff=0.1)
            cards = VGroup(*[Square(0.18, stroke_width=0).set_fill(CHECKED_C, 0.8) for _ in range(74)]).arrange_in_grid(7, 11, buff=0.06)
            g1 = VGroup(VGroup(pages, sans("15 sources", 22, S.GREY)).arrange(DOWN, buff=0.15),
                        Arrow(LEFT * 0.5, RIGHT * 0.5, buff=0, color=S.GREY),
                        VGroup(cards, sans("74 fact cards", 22, CHECKED_C)).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=0.3)
            g1.move_to(LEFT * 3.0 + UP * 0.6)
            vo.wait_until("fact cards")
            self.play(FadeIn(g1[0]), GrowArrow(g1[1]), LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.01),
                      FadeIn(g1[2][1]), run_time=1.2)
            others = VGroup(tag_box("rules", "rules engine", "decides urgency", MODEL_C, width=3.4),
                            tag_box("tests", "11 test cases", None, S.WHITE, width=3.4),
                            tag_box("eval", "an evaluation", None, S.WHITE, width=3.4)).arrange(DOWN, buff=0.25)
            others.move_to(RIGHT * 3.6 + UP * 0.6)
            for o, phrase in zip(others, ["a rules engine", "eleven test cases", "an evaluation"]):
                vo.wait_until(phrase)
                self.play(FadeIn(o, shift=LEFT * 0.1), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- four isolated reviewers
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(others, g1[0], g1[1], strip, sticks, before, ends)), g1[2].animate.move_to(LEFT * 4.7),
                      run_time=0.5)
            revs = VGroup(*[tag_box("agent", f"reviewer {i + 1}", "read-only", S.GREY, width=2.6) for i in range(4)]
                          ).arrange_in_grid(2, 2, buff=(0.5, 0.35)).move_to(RIGHT * 0.6)
            walls = VGroup(Line(revs.get_top() + UP * 0.1, revs.get_bottom() + DOWN * 0.1, color=DANGER_C, stroke_width=3),
                           Line(revs.get_left() + LEFT * 0.1, revs.get_right() + RIGHT * 0.1, color=DANGER_C, stroke_width=3))
            vo.wait_until("Four reviewer agents")
            self.play(LaggedStart(*[FadeIn(r) for r in revs], lag_ratio=0.15), run_time=0.8)
            vo.wait_until("could not talk")
            self.play(Create(walls), run_time=0.5)
            q = quote_panel("请 4 个互不通信的 agent 按快照分组，逐张对照原文和上下文挑错。它们只读文件，不改文件。",
                            "knowledge/reviews/2026-10-27.md", width=12.0, size=24).move_to(UP * 2.55)
            self.play(FadeIn(q), FadeOut(when), run_time=0.5)
            vo.wait_until("75 problems")
            found = sans("75 problems", 30, DANGER_C).next_to(revs, RIGHT, buff=0.5)
            self.play(FadeIn(found, scale=1.2), run_time=0.4)
            vo.wait_until("Twenty-three minutes after")
            after = VGroup(sans("23 min after", 22, S.GREY), sans("the first 74 cards:", 22, S.GREY), sans("97 cards", 28, CHECKED_C),
                           sans("7 conflicts", 24, CHECKED_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(found, DOWN, buff=0.3).align_to(found, LEFT)
            self.play(FadeIn(after), run_time=0.5)
            vo.wait_until("out-of-network urgent care")
            old = zh("保险付 80%，自付 20%", 24, DANGER_C)
            new = zh("先付网络外 deductible（$500），再自付 20%，可能另收差额", 24, CHECKED_C)
            card = VGroup(sans("the out-of-network urgent-care card, before → after", 20, S.GREY), old, new
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            card.move_to(DOWN * 2.45)
            strike = Line(old.get_left(), old.get_right(), color=DANGER_C, stroke_width=3)
            self.play(FadeIn(card[0]), FadeIn(old), run_time=0.4)
            vo.wait_until("the source said")
            self.play(Create(strike), FadeIn(new, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
