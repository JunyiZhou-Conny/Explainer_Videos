"""S05 · Breaking it on purpose (PR #42 body; SKILL.md:108-113; ../SOURCES.md)

1. Ponder: why would an agent break its own code on purpose?
2. "A check that you have never seen fail proves nothing" (pstack's formal-verification skill). Five deliberate
   breakages of the reducer (PR body wording); each caught, with a story of two steps or fewer (the PR's claim;
   the traces drawn are our reproduction, marked as such); each undone. Mutation testing: DeMillo, Lipton &
   Sayward, IEEE Computer, 1978.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, NARRATION, USER_C, clear, mark_ok, ponder_zh, quote_panel, sans, strike, zh)

SAY = NARRATION["S05"]
# (the breakage as the PR names it, the rule that caught it, steps in the shortest story; our reproduction)
MUTANTS = [("预约时不要求原预约已取消", "1", 2), ("转诊不能用时保留 referralId", "2", 1), ("取消时不退回 issued", "3", 2),
           ("取消时改成 completed", "4", 2), ("改期时丢掉 referralId", "3", 2)]


class Mutants(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- ponder
        with self.voiceover(SAY[0]) as vo:
            card = ponder_zh(self, "Why would an agent break its own code on purpose?", "agent 为什么要故意把自己的代码改坏？",
                             seconds=4.0)
        self.wait(2.0)

        # 2 ---------------------------------------------------------------- five breakages, five catches
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(card), run_time=0.3)
            q = quote_panel("A check that you have never seen fail proves nothing.", "pstack · create-formal-verification-skill",
                            width=11.4, size=28, color=USER_C).move_to(UP * 2.8)
            vo.wait_until("never seen fail")
            self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
            rows = VGroup()
            for i, (name, rule, steps) in enumerate(MUTANTS):
                label = zh(f"{i + 1}. {name}", 24)
                verdict = VGroup(sans(f"rule {rule} breaks", 22, DANGER_C), sans(f"{steps} step{'s' if steps > 1 else ''}", 22, S.GREY),
                                 VGroup(mark_ok(0.24, CHECKED_C), sans("caught", 22, CHECKED_C)).arrange(RIGHT, buff=0.1)
                                 ).arrange(RIGHT, buff=0.35)
                rows.add(VGroup(label, verdict))
            for r in rows:
                r[1].move_to([2.6, 0, 0], aligned_edge=LEFT)
                r[0].move_to([-6.0, 0, 0], aligned_edge=LEFT)
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(DOWN * 0.35)
            for r in rows:
                r[1].move_to([2.0, r[0].get_y(), 0], aligned_edge=LEFT)
            vo.wait_until("broke the reducer five times")
            self.play(LaggedStart(*[FadeIn(r[0], shift=RIGHT * 0.1) for r in rows], lag_ratio=0.15), run_time=1.2)
            vo.wait_until("ran the check after each")
            self.play(LaggedStart(*[FadeIn(r[1]) for r in rows], lag_ratio=0.2), run_time=1.4)
            vo.wait_until("each breakage was then undone")
            self.play(*[Create(strike(r[0], S.GREY, 3)) for r in rows], run_time=0.6)
            note = sans("which rule broke, in how many steps: our own re-run (the PR lists only that all five were caught)", 22, S.GREY).next_to(rows, DOWN, buff=0.3)
            note.align_to(rows, LEFT)
            self.play(FadeIn(note), run_time=0.3)
            vo.wait_until("mutation testing")
            term = VGroup(sans("a hand-made mutation test", 30, USER_C), sans("DeMillo, Lipton & Sayward · IEEE Computer · 1978", 22, S.GREY)
                          ).arrange(DOWN, buff=0.08).move_to(DOWN * 3.05 + RIGHT * 2.6)
            self.play(FadeIn(term, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
