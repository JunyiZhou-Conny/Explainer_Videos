"""S01 · Two days on one clock

1. Every commit of PR #36 (ORANGE) and PR #41 (BLUE) on one Boston-time axis, Tue noon → Thu 01:00;
   then the merges (GREY). Counters: 88 changes · 21 merges · 109 in all (git log, ../SOURCES.md).
   All 109 were made by agents; 40 of PR #36's show the owner as author (the agent used his git identity).
2. Two questions: why are most of them fixes (53 of 88 messages name Bugbot, Codex or a review; R36/R41 light up)? who decided? Reviews by a person so far: 0 (two teammates were
   asked when PR #36 was marked ready, Tue 22:23).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (H36, H41, M36, M41, MODEL_C, NARRATION, OURS_C, R36, R41, USER_C, chip, clear, commit_ticks, sans,
                    week_axis)

SAY = NARRATION["S01"]
Y_AXIS, Y36, Y41 = -1.6, 0.6, -0.7


class Hook(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- every commit, one clock
        with self.voiceover(SAY[0]) as vo:
            line, ticks, x_of = week_axis(y=Y_AXIS)
            boston = sans("Boston time", 20, S.GREY).next_to(line, DOWN, buff=0.7).align_to(line, RIGHT)
            self.play(Create(line), FadeIn(ticks), FadeIn(boston), run_time=0.8)
            lab36 = sans("PR #36 · the triage brain", 22, MODEL_C).move_to([x_of(12), Y36 + 1.15, 0], aligned_edge=LEFT)
            lab41 = sans("PR #41 · the chat page", 22, OURS_C).move_to([x_of(12), Y41 + 1.0, 0], aligned_edge=LEFT)
            t36 = commit_ticks(x_of, H36, Y36, 0.75, MODEL_C)
            t41 = commit_ticks(x_of, H41, Y41, 0.75, OURS_C)
            vo.wait_until("every commit")
            self.play(FadeIn(lab36), LaggedStart(*[Create(t) for t in t36], lag_ratio=0.03), run_time=1.6)
            self.play(FadeIn(lab41), LaggedStart(*[Create(t) for t in t41], lag_ratio=0.04), run_time=1.0)
            vo.wait_until("109 commits")
            m36 = commit_ticks(x_of, M36, Y36, 0.4, S.GREY, 2)
            m41 = commit_ticks(x_of, M41, Y41, 0.4, S.GREY, 2)
            counters = VGroup(sans("88 changes", 26, S.WHITE), sans("21 merges", 26, S.GREY),
                              sans("109 in all · every one by an agent", 26, USER_C)).arrange(RIGHT, buff=0.8).move_to(UP * 3.1)
            self.play(FadeIn(counters[2]), run_time=0.4)
            vo.wait_until("88 changes")
            self.play(FadeIn(counters[0]), run_time=0.4)
            vo.wait_until("21 merges")
            self.play(FadeIn(counters[1]), LaggedStart(*[Create(t) for t in [*m36, *m41]], lag_ratio=0.05), run_time=0.9)
            vo.wait_until("forty of them")
            who = sans("40 show your name as author: the agent used your git identity", 22, S.GREY).move_to(UP * 2.55)
            self.play(FadeIn(who), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- two questions
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(counters), FadeOut(who), *[m.animate.set_opacity(0.25) for m in [*t36, *t41, *m36, *m41]],
                      run_time=0.4)
            q1 = chip("why are most of them fixes?", USER_C, 30, mono_font=False)
            q2 = chip("who decided?", USER_C, 30, mono_font=False)
            qs = VGroup(q1, q2).arrange(RIGHT, buff=0.8).move_to(UP * 2.95)
            vo.wait_until("Why are most")
            self.play(FadeIn(q1, scale=1.1), run_time=0.4)
            vo.wait_until("53 of the 88")
            lit = VGroup(commit_ticks(x_of, R36, Y36, 0.75, MODEL_C), commit_ticks(x_of, R41, Y41, 0.75, OURS_C))
            count = sans("53 of 88 name a review: Bugbot, Codex or a review agent", 22, USER_C).next_to(q1, DOWN, buff=0.2)
            count.align_to(q1, LEFT)
            self.play(LaggedStart(*[Create(x) for x in [*lit[0], *lit[1]]], lag_ratio=0.02), FadeIn(count), run_time=1.2)
            vo.wait_until("no person has reviewed")
            zero = VGroup(sans("reviews by a person so far: 0", 26, S.WHITE),
                          sans("two teammates asked · Tue 22:23", 22, S.GREY)).arrange(DOWN, buff=0.08).move_to(DOWN * 2.95)
            self.play(FadeOut(boston), FadeIn(zero), run_time=0.4)
            vo.wait_until("who decided")
            self.play(FadeIn(q2, scale=1.1), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
