"""S05 · The loop with the bots (PR #36)

1. Tue 22:23 PR #36 marked ready for review (two teammates asked); push → bots review → agent fixes → push;
   Tue 22:27 → Wed 00:07: 19 commits; on PR #36 the bots wrote 72
   comments (Bugbot 42 · Codex 30), 64 led to fixes.
2. The checker (lint.ts) after the turn: 459 → 1,326 lines; 27 of the 45 commits since touched it. Whack-a-mole,
   both on Wednesday: 「不要因为保险或费用问题延误救援」 flagged as money-first in a real run (11:04, 6f9394e);
   narrowing a similar rule (19:07, 26a2d89) let 「Use my insurance first」 slip through; Bugbot flagged it;
   restored 19:23 (2662221).
3. 「已和 Junyi 商定：以后把修复攒在一起再推。」 (PR #36 handoff, 10-28 00:26)
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, H36, MODEL_C, NARRATION, USER_C, clear, commit_ticks, mark_bad, mark_ok,
                    quote_panel, sans, zh)

SAY = NARRATION["S05"]


def node(text: str, color) -> VGroup:
    t = sans(text, 24, color)
    c = Circle(radius=0.85, color=color, stroke_width=3)
    t.move_to(c)
    return VGroup(c, t)


class Loop(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the loop
        with self.voiceover(SAY[0]) as vo:
            n = VGroup(node("push", MODEL_C), node("bots review", S.GREY), node("agent fixes", MODEL_C))
            pts = [UP * 1.9 + LEFT * 3.75, DOWN * 0.4 + LEFT * 2.05, DOWN * 0.4 + LEFT * 5.45]
            for m, p in zip(n, pts):
                m.move_to(p)
            arrows = VGroup(*[CurvedArrow(a.get_center() + (b.get_center() - a.get_center()) * 0.38,
                                          b.get_center() + (a.get_center() - b.get_center()) * 0.38, angle=-PI / 4, color=S.GREY)
                              for a, b in [(n[0], n[1]), (n[1], n[2]), (n[2], n[0])]])
            self.play(LaggedStart(*[FadeIn(m) for m in n], lag_ratio=0.3), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.3),
                      run_time=1.2)
            vo.wait_until("ten twenty-three")
            ready = VGroup(sans("Tue 22:23 · PR #36 marked ready for review", 22, S.WHITE),
                           sans("both bots now review every push", 20, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            ready.move_to([3.4, 3.25, 0])
            self.play(FadeIn(ready), run_time=0.4)
            vo.wait_until("Push, the bots")
            token = Dot(radius=0.11, color=USER_C).move_to(arrows[0].get_start())
            self.play(FadeIn(token), run_time=0.2)
            for _ in range(2):        # round the loop twice, faster the second time
                for a, rt in zip(arrows, (0.5, 0.5, 0.5) if _ == 0 else (0.3, 0.3, 0.3)):
                    self.play(MoveAlongPath(token, a), run_time=rt, rate_func=linear)
            vo.wait_until("Between ten twenty-seven")
            burst = [h for h in H36 if 22.4 <= h <= 24.2]
            ax = Line(LEFT * 0.0 + RIGHT * 0.6 + DOWN * 1.9, RIGHT * 6.2 + DOWN * 1.9, color=S.GREY, stroke_width=2)

            def x_of(h):
                return 0.6 + (h - 22.4) / (24.2 - 22.4) * 5.6
            t = commit_ticks(x_of, burst, -1.9, 0.7, MODEL_C)
            labs = VGroup(sans("Tue 22:27", 20, S.GREY).move_to([x_of(22.45), -2.25, 0]),
                          sans("Wed 00:07", 20, S.GREY).move_to([x_of(24.13), -2.25, 0]))
            cnt = sans(f"{len(burst)} commits · about one every 5 minutes", 24, MODEL_C).move_to([3.4, -0.7, 0])
            self.play(Create(ax), FadeIn(labs), LaggedStart(*[Create(x) for x in t], lag_ratio=0.05), FadeIn(cnt), run_time=1.2)
            vo.wait_until("72 comments")
            bots = VGroup(sans("PR #36 · bot comments 72", 26), sans("Bugbot 42 · Codex 30", 22, S.GREY)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.4, 2.1, 0])
            self.play(FadeIn(bots), run_time=0.4)
            vo.wait_until("64 led to fixes")
            fixed = VGroup(mark_ok(0.3, CHECKED_C), sans("64 fixed", 26, CHECKED_C)).arrange(RIGHT, buff=0.15)
            fixed.next_to(bots, DOWN, buff=0.3).align_to(bots, LEFT)
            self.play(FadeIn(fixed), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- whack-a-mole
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            vo.wait_until("459 lines")
            unit = 0.0042
            b0 = Rectangle(width=459 * unit, height=0.45, stroke_width=0).set_fill(S.GREY, 0.8)
            b1 = Rectangle(width=1326 * unit, height=0.45, stroke_width=0).set_fill(DANGER_C, 0.7)
            bar_l = sans("the checker (lint.ts), from the turn", 22, S.GREY)
            row = VGroup(bar_l, b0).arrange(RIGHT, buff=0.3).move_to(UP * 2.8).to_edge(LEFT, buff=0.6)
            n0 = sans("459 lines", 22).next_to(b0, RIGHT, buff=0.15)
            self.play(FadeIn(row), FadeIn(n0), run_time=0.5)
            b1.move_to(b0, aligned_edge=LEFT)
            n1 = sans("1,326 lines", 22, DANGER_C).next_to(b1, RIGHT, buff=0.15)
            vo.wait_until("to 1,326")
            self.play(Transform(b0, b1), Transform(n0, n1), run_time=0.8)
            vo.wait_until("27 of the 45")
            share = sans("27 of the 45 commits since touched it", 24).next_to(row, DOWN, buff=0.3).align_to(row, LEFT)
            self.play(FadeIn(share), run_time=0.4)
            vo.wait_until("parent summary")
            fp = VGroup(zh("Wed 11:04 · 「不要因为保险或费用问题延误救援」", 24), VGroup(mark_bad(0.22, DANGER_C), sans("flagged as money first → a needless rewrite", 22, DANGER_C)
                                                                       ).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            fp.move_to(UP * 0.85).to_edge(LEFT, buff=0.8)
            self.play(FadeIn(fp[0]), run_time=0.4)
            vo.wait_until("was flagged")
            self.play(FadeIn(fp[1]), run_time=0.4)
            vo.wait_until("narrowing a similar rule")
            fn = VGroup(zh("Wed 19:07 · 「Use my insurance first」", 24), VGroup(mark_bad(0.22, DANGER_C), sans("missed: real money first", 22, DANGER_C)
                                                                    ).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            fn.move_to(DOWN * 0.75).to_edge(LEFT, buff=0.8).shift(RIGHT * 1.2)
            x = fp.get_left()[0] + 0.4
            down = Arrow([x, fp.get_bottom()[1] - 0.05, 0], [x, fn.get_top()[1] + 0.05, 0], buff=0, color=S.GREY)
            arrow = VGroup(down, sans("then: narrow a similar rule", 20, S.GREY).next_to(down, RIGHT, buff=0.15))
            self.play(Create(arrow[0]), FadeIn(arrow[1]), FadeIn(fn), run_time=0.6)
            vo.wait_until("until Bugbot caught it")
            src = sans("Bugbot flagged it · restored 19:23 · commits 6f9394e, 26a2d89, 2662221", 20, S.GREY).move_to(DOWN * 1.7)
            self.play(FadeIn(src), run_time=0.3)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- batch the fixes
        with self.voiceover(SAY[2]) as vo:
            q = quote_panel("已和 Junyi 商定：以后把修复攒在一起再推。", "PR #36 handoff · Wed 00:26", width=8.6, size=28,
                            color=USER_C).move_to(DOWN * 2.82)
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
