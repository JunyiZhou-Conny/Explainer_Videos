"""S07 · Attack your own checker (PR #36; ../SOURCES.md)

1. The checker (lint.ts) after the turn: 459 → 1,326 lines; 27 of the 45 commits since touched it. Whack-a-mole,
   both on Wednesday: 「不要因为保险或费用问题延误救援」 flagged as money-first in a real run (11:04, 6f9394e);
   narrowing a similar rule (19:07, 26a2d89) let 「Use my insurance first」 slip through; Bugbot flagged it;
   restored 19:23 (2662221). Under it, a rule drawn as a window over phrasings (an illustration).
2. Wed 21:04 → Thu 00:45: the two rules (7b332a0 「营业状态和急诊费用两条检查加固」); a pair from the handoff:
   must be flagged 「网络外的急诊也是更贵」, must pass 「多休息」 (once a false alarm). Prober agents (round 1: 4 angles,
   a 5th checks them; round 2: 3 angles): round 1 ≈ 2,000 (opening hours ≈ 1,400, emergency cost ≈ 640),
   round 2 ≈ 1,000; ≈ 3,000 in all. Round 1: 142 misses, 230 false alarms.
3. Ponder: the bots would have found these too; why attack the checker yourself first?
4. The bots report one at a time (「bot 一条一条报要报很久」); one probing run found 372 (「一次找出了 372 个同类写法」).
   lint.probes.json: round 1 371 + round 2 689 = 1,060 (506 must be flagged, 554 must pass), run with the unit
   tests (`npm test`, lint.test.ts); ≈ 20 harder ones listed as known misses; in round 2 the first fix made 20 new
   false alarms, caught before the push.
"""

import random

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, MODEL_C, NARRATION, USER_C, clear, mark_bad, mark_ok, mono, ours_box, ponder_zh,
                    sans, tag_box, zh)

SAY = NARRATION["S07"]


class Probing(VoiceScene):
    def construct(self):
        rng = random.Random(4)
        # 1 ---------------------------------------------------------------- the checker's whack-a-mole
        with self.voiceover(SAY[0]) as vo:
            unit = 0.0042
            b0 = Rectangle(width=459 * unit, height=0.45, stroke_width=0).set_fill(S.GREY, 0.8)
            b1 = Rectangle(width=1326 * unit, height=0.45, stroke_width=0).set_fill(DANGER_C, 0.7)
            bar_l = sans("the checker (lint.ts), from the turn", 22, S.GREY)
            row = VGroup(bar_l, b0).arrange(RIGHT, buff=0.3).move_to(UP * 3.0).to_edge(LEFT, buff=0.6)
            n0 = sans("459 lines", 22).next_to(b0, RIGHT, buff=0.15)
            head = sans("most bot comments were about the checker", 26).move_to(UP * 2.3).to_edge(LEFT, buff=0.6)
            self.play(FadeIn(bar_l), FadeIn(head), run_time=0.4)
            vo.wait_until("459 lines")
            self.play(FadeIn(b0), FadeIn(n0), run_time=0.5)
            b1.move_to(b0, aligned_edge=LEFT)
            n1 = sans("1,326 lines", 22, DANGER_C).next_to(b1, RIGHT, buff=0.15)
            vo.wait_until("to 1,326")
            self.play(Transform(b0, b1), Transform(n0, n1), run_time=0.8)
            vo.wait_until("27 of the 45")
            share = sans("27 of the 45 commits since touched it", 24).next_to(row, DOWN, buff=0.25).align_to(row, LEFT)
            self.play(FadeOut(head), FadeIn(share), run_time=0.4)

            # a word rule as a window over phrasings: too wide flags a harmless one, narrowed it misses a risky one
            strip = Line([-5.6, -2.55, 0], [5.6, -2.55, 0], color=S.GREY_DARK, stroke_width=2)
            xs, kinds = [-4.2, -2.6, -0.8, 1.0, 2.8, 4.4], ["risky", "risky", "harmless", "risky", "harmless", "harmless"]
            dots = VGroup(*[Dot([x, -2.55, 0], radius=0.13, color=DANGER_C if k == "risky" else CHECKED_C) for x, k in zip(xs, kinds)])
            key = VGroup(Dot(radius=0.08, color=DANGER_C), sans("risky", 20, S.GREY), Dot(radius=0.08, color=CHECKED_C),
                         sans("harmless", 20, S.GREY), sans("· a rule as a window over phrasings (illustration)", 20, S.GREY)
                         ).arrange(RIGHT, buff=0.12).move_to(DOWN * 3.25)
            wide = Rectangle(width=6.0, height=0.6, stroke_color=USER_C, stroke_width=3).move_to([-1.6, -2.55, 0])
            vo.wait_until("Each fix moved")
            self.play(Create(strip), FadeIn(dots), FadeIn(key), Create(wide), run_time=0.8)
            vo.wait_until("parent summary")
            fp = VGroup(zh("Wed 11:04 · 「不要因为保险或费用问题延误救援」", 24), VGroup(mark_bad(0.22, DANGER_C), sans("flagged as money first → a needless rewrite", 22, DANGER_C)
                                                                       ).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            fp.move_to(UP * 1.15).to_edge(LEFT, buff=0.8)
            self.play(FadeIn(fp[0]), run_time=0.4)
            vo.wait_until("was flagged")
            fa = mark_bad(0.22, DANGER_C).next_to(dots[2], UP, buff=0.25)
            self.play(FadeIn(fp[1]), Indicate(dots[2], color=DANGER_C), FadeIn(fa), run_time=0.6)
            vo.wait_until("narrowing a similar rule")
            fn = VGroup(zh("Wed 19:07 · 「Use my insurance first」", 24), VGroup(mark_bad(0.22, DANGER_C), sans("missed: real money first", 22, DANGER_C)
                                                                    ).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            fn.move_to(DOWN * 0.45).to_edge(LEFT, buff=0.8).shift(RIGHT * 1.2)
            x = fp.get_left()[0] + 0.4
            down = Arrow([x, fp.get_bottom()[1] - 0.05, 0], [x, fn.get_top()[1] + 0.05, 0], buff=0, color=S.GREY)
            arrow = VGroup(down, sans("then: narrow a similar rule", 20, S.GREY).next_to(down, RIGHT, buff=0.15))
            narrow = Rectangle(width=3.0, height=0.6, stroke_color=USER_C, stroke_width=3).move_to([-3.4, -2.55, 0])
            miss = mark_bad(0.22, DANGER_C).next_to(dots[3], UP, buff=0.25)
            self.play(Create(arrow[0]), FadeIn(arrow[1]), FadeIn(fn), Transform(wide, narrow), FadeOut(fa), run_time=0.8)
            self.play(Indicate(dots[3], color=DANGER_C), FadeIn(miss), run_time=0.5)
            vo.wait_until("until Bugbot caught it")
            src = sans("Bugbot flagged it · restored 19:23 · commits 6f9394e, 26a2d89, 2662221", 20, S.GREY).move_to(DOWN * 1.45)
            self.play(FadeIn(src), run_time=0.3)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- two rules, thousands of phrasings
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            when = sans("Wed 21:04 → Thu 00:45 Boston · Thu 09:04 → 12:45 Beijing · the second night", 22, S.GREY).move_to(UP * 3.3)
            checker = ours_box("the checker", "lint", width=2.6).move_to(RIGHT * 0.6 + DOWN * 0.1)
            self.play(FadeIn(when), FadeIn(checker), run_time=0.4)
            vo.wait_until("Two rules")
            rules = VGroup(sans("1  never claim a clinic is open right now unless its hours are checked", 22),
                           sans("2  keep cost out of the way of an emergency", 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            rules.move_to(UP * 2.5)
            self.play(FadeIn(rules[0]), run_time=0.4)
            vo.wait_until("keep cost out")
            self.play(FadeIn(rules[1]), run_time=0.4)
            probers = VGroup(*[tag_box("agent", f"prober {i + 1}", None, MODEL_C, width=2.0) for i in range(4)]
                             ).arrange(DOWN, buff=0.12).move_to(LEFT * 5.0 + UP * 0.35)
            judge = tag_box("agent", "5th: checks", "round 1", S.GREY, width=2.6).next_to(probers, DOWN, buff=0.15)
            vo.wait_until("attacked those two rules")
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in probers], lag_ratio=0.15), FadeIn(judge), run_time=0.8)
            vo.wait_until("about 3,000 ways")
            dots = VGroup(*[Dot(radius=0.04, color=(DANGER_C if rng.random() < 0.5 else CHECKED_C)) for _ in range(60)])
            anims = []
            for i, d in enumerate(dots):
                d.move_to(probers[i % 4].get_right() + RIGHT * 0.2)
                anims.append(Succession(FadeIn(d, run_time=0.05), d.animate(run_time=0.6).move_to(checker.get_left() + LEFT * 0.1),
                                        FadeOut(d, run_time=0.05)))
            self.play(LaggedStart(*anims, lag_ratio=0.04), run_time=3.0)
            rounds = VGroup(sans("round 1 ≈ 2,000 phrasings", 24), sans("opening hours ≈ 1,400", 20, S.GREY),
                            sans("emergency cost ≈ 640", 20, S.GREY),
                            sans("round 2 ≈ 1,000", 24), sans("≈ 3,000 in all", 26, MODEL_C)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 4.5 + UP * 0.75)
            self.play(FadeIn(rounds), run_time=0.5)
            vo.wait_until("harmless twin")
            pair = VGroup(VGroup(sans("must be flagged", 20, DANGER_C), zh("「网络外的急诊也是更贵」", 22)).arrange(RIGHT, buff=0.15),
                          VGroup(sans("must pass", 20, CHECKED_C), zh("「多休息」", 22), sans("(once a false alarm)", 20, S.GREY)
                                 ).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            pair.move_to(DOWN * 2.45)
            self.play(FadeIn(pair), run_time=0.5)
            vo.wait_until("142 misses")
            res = VGroup(sans("round 1 found", 22, S.GREY), sans("142 misses", 28, DANGER_C), sans("230 false alarms", 28, DANGER_C)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(RIGHT * 4.6 + DOWN * 1.75)
            self.play(FadeIn(res[0]), FadeIn(res[1]), run_time=0.4)
            vo.wait_until("230 false alarms")
            self.play(FadeIn(res[2]), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- ponder
        with self.voiceover(SAY[2]) as vo:
            self.play(*[m.animate.set_opacity(0.15) for m in self.mobjects], run_time=0.4)
            ponder_zh(self, "The bots would have found these too. Why attack the checker yourself first?",
                      "bot 迟早也会找到这些。为什么要先自己攻击检查器？", seconds=4.0)
        self.wait(2.0)

        # 4 ---------------------------------------------------------------- one at a time vs 372 at once; 1,060 tests
        with self.voiceover(SAY[3]) as vo:
            clear(self, 0.4)
            pushes = VGroup(*[VGroup(Line(UP * 0.25, DOWN * 0.25, color=S.GREY, stroke_width=3),
                                     Dot(radius=0.07, color=DANGER_C).shift(UP * 0.45)) for _ in range(6)]).arrange(RIGHT, buff=0.55)
            bots = VGroup(sans("the bots", 24), pushes, sans("one finding per review · one push per round", 20, S.GREY)
                          ).arrange(RIGHT, buff=0.4).move_to(UP * 2.4)
            grid = VGroup(*[Dot(radius=0.035, color=DANGER_C) for _ in range(372)]).arrange_in_grid(8, 47, buff=0.06)
            probes = VGroup(sans("the probes", 24), grid, sans("372 in one run", 22, DANGER_C)).arrange(RIGHT, buff=0.4).move_to(UP * 0.9)
            VGroup(bots, probes).align_to(LEFT * 6.0, LEFT)
            vo.wait_until("one finding at a time")
            self.play(FadeIn(bots[0]), LaggedStart(*[FadeIn(p) for p in pushes], lag_ratio=0.5), FadeIn(bots[2]), run_time=2.0)
            vo.wait_until("372 at once")
            self.play(FadeIn(probes[0]), FadeIn(grid), FadeIn(probes[2]), run_time=0.5)
            vo.wait_until("Across both rounds")
            self.play(FadeOut(bots), FadeOut(probes), run_time=0.4)
            jar = RoundedRectangle(width=4.2, height=3.4, corner_radius=0.3, stroke_color=S.GREY, stroke_width=3)
            jar.move_to(LEFT * 3.0 + DOWN * 0.4)
            name = mono("lint.probes.json", 26).next_to(jar, UP, buff=0.2)
            cells = VGroup(*[Square(0.11, stroke_width=0).set_fill(DANGER_C if i < 506 else CHECKED_C, 0.85) for i in range(1060)]
                           ).arrange_in_grid(30, 36, buff=0.025).scale_to_fit_width(3.6).move_to(jar)
            self.play(FadeIn(jar), FadeIn(name), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.001), run_time=1.6)
            legend = VGroup(sans("1,060 phrasings, fixed", 30), sans("round 1: 371 · round 2: 689", 22, S.GREY),
                            sans("506 must be flagged", 24, DANGER_C), sans("554 must pass", 24, CHECKED_C)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 3.2 + UP * 1.6)
            self.play(FadeIn(legend), run_time=0.5)
            vo.wait_until("with the unit tests")
            run = VGroup(mark_ok(0.3, CHECKED_C), mono("npm test", 26), sans("with the unit tests", 22, S.GREY)).arrange(RIGHT, buff=0.2)
            run.next_to(legend, DOWN, buff=0.35).align_to(legend, LEFT)
            self.play(FadeIn(run), run_time=0.4)
            vo.wait_until("known misses")
            known = sans("≈ 20 harder ones: listed as known misses", 22, S.GREY).next_to(run, DOWN, buff=0.2).align_to(legend, LEFT)
            self.play(FadeIn(known), run_time=0.4)
            vo.wait_until("20 new false alarms")
            twenty = VGroup(VGroup(sans("round 2: the first fix made", 22, DANGER_C), sans("20 new false alarms", 24, DANGER_C)
                                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.06), sans("caught before the push", 24, CHECKED_C)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(known, DOWN, buff=0.3).align_to(legend, LEFT)
            self.play(FadeIn(twenty[0]), run_time=0.4)
            vo.wait_until("caught before the push")
            self.play(FadeIn(twenty[1]), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
