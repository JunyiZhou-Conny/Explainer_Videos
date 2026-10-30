"""S06 · Attack your own checker (Wed 21:04 → Thu 00:45)

1. Prober agents (round 1: 4 angles, a 5th checks them; round 2: 3 angles) write phrasings: round 1 ≈ 2,000 (opening hours ≈ 1,400,
   emergency cost ≈ 640), round 2 ≈ 1,000; ≈ 3,000 in all. Round 1: 142 misses, 230 false alarms (7b332a0).
2. The 1,060 the checker got wrong, fixed, become lint.probes.json (506 must be flagged, 554 must pass), run with
   the unit tests (`npm test`, lint.test.ts); ≈ 20 harder ones stay listed as known misses (lint.test.ts comment).
   In round 2 the first fix itself made 20 new false alarms, caught before the push.
"""

import random

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, MODEL_C, NARRATION, OURS_C, clear, mark_ok, mono, ours_box, sans, tag_box)

SAY = NARRATION["S06"]


class Probing(VoiceScene):
    def construct(self):
        rng = random.Random(4)
        # 1 ---------------------------------------------------------------- thousands of phrasings
        with self.voiceover(SAY[0]) as vo:
            when = sans("Wed 21:04 → Thu 00:45 · the second night", 24, S.GREY).move_to(UP * 3.2)
            self.play(FadeIn(when), run_time=0.4)
            probers = VGroup(*[tag_box("agent", f"prober {i + 1}", None, MODEL_C, width=2.0) for i in range(4)]
                             ).arrange(DOWN, buff=0.2).move_to(LEFT * 5.0 + UP * 0.4)
            judge = tag_box("agent", "5th: checks", "round 1", S.GREY, width=2.6).next_to(probers, DOWN, buff=0.25)
            checker = ours_box("the checker", "lint", width=2.6).move_to(RIGHT * 0.9 + UP * 0.4)
            self.play(FadeIn(checker), run_time=0.4)
            vo.wait_until("attacked their own checker")
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in probers], lag_ratio=0.15), FadeIn(judge), run_time=0.8)
            vo.wait_until("about 3,000 ways")
            dots = VGroup(*[Dot(radius=0.04, color=(DANGER_C if rng.random() < 0.5 else CHECKED_C)) for _ in range(60)])
            starts = [probers[i % 4].get_right() + RIGHT * 0.2 for i in range(60)]
            anims = []
            for d, st in zip(dots, starts):
                d.move_to(st)
                anims.append(Succession(FadeIn(d, run_time=0.05), d.animate(run_time=0.6).move_to(checker.get_left() + LEFT * 0.1),
                                        FadeOut(d, run_time=0.05)))
            self.play(LaggedStart(*anims, lag_ratio=0.04), run_time=3.0)
            rounds = VGroup(sans("round 1 ≈ 2,000 phrasings", 24), sans("opening hours ≈ 1,400", 20, S.GREY),
                            sans("emergency cost ≈ 640", 20, S.GREY),
                            sans("round 2 ≈ 1,000", 24), sans("≈ 3,000 in all", 26, MODEL_C)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 4.4 + UP * 1.5)
            self.play(FadeIn(rounds), run_time=0.5)
            vo.wait_until("142 misses")
            res = VGroup(sans("round 1 found", 22, S.GREY), sans("142 misses", 28, DANGER_C), sans("230 false alarms", 28, DANGER_C)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 4.5 + DOWN * 1.6)
            self.play(FadeIn(res[0]), FadeIn(res[1]), run_time=0.4)
            vo.wait_until("230 false alarms")
            self.play(FadeIn(res[2]), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- 1,060 become tests
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            jar = RoundedRectangle(width=4.2, height=3.4, corner_radius=0.3, stroke_color=S.GREY, stroke_width=3)
            jar.move_to(LEFT * 3.0 + DOWN * 0.3)
            name = mono("lint.probes.json", 26).next_to(jar, UP, buff=0.2)
            grid = VGroup(*[Square(0.11, stroke_width=0).set_fill(DANGER_C if i < 506 else CHECKED_C, 0.85) for i in range(1060)]
                          ).arrange_in_grid(30, 36, buff=0.025).scale_to_fit_width(3.6).move_to(jar)
            vo.wait_until("1,060 phrasings")
            self.play(FadeIn(jar), FadeIn(name), LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.001), run_time=1.6)
            legend = VGroup(sans("1,060 phrasings, fixed", 30), sans("506 must be flagged", 24, DANGER_C), sans("554 must pass", 24, CHECKED_C)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 3.2 + UP * 1.4)
            self.play(FadeIn(legend), run_time=0.5)
            vo.wait_until("with the unit tests")
            run = VGroup(mark_ok(0.3, CHECKED_C), mono("npm test", 26), sans("with the unit tests", 22, S.GREY)).arrange(RIGHT, buff=0.2)
            run.next_to(legend, DOWN, buff=0.5).align_to(legend, LEFT)
            self.play(FadeIn(run), run_time=0.4)
            vo.wait_until("known misses")
            known = sans("≈ 20 harder ones: listed as known misses", 22, S.GREY).next_to(run, DOWN, buff=0.2).align_to(legend, LEFT)
            self.play(FadeIn(known), run_time=0.4)
            vo.wait_until("20 new false alarms")
            twenty = VGroup(VGroup(sans("round 2: the first fix made", 22, DANGER_C), sans("20 new false alarms", 24, DANGER_C)
                                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.06), sans("caught before the push", 24, CHECKED_C)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(known, DOWN, buff=0.4).align_to(legend, LEFT)
            self.play(FadeIn(twenty[0]), run_time=0.4)
            vo.wait_until("caught before the push")
            self.play(FadeIn(twenty[1]), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
