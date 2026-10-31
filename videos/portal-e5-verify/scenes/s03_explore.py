"""S03 · Try every order in a small world (verify/referral-links/model.ts; ../SOURCES.md)

1. The world: 2 referrals (ref-v1, ref-v2), 3 specialist slots (S1–S3), a clock with two moments (T0+1 h, just after the
   referrals are written, and 1 h after validUntil; model.ts:15, :66-69); 13 first moves; breadth-first, states already seen merge; 13,898 states, 173,725
   transitions, about a second (measured: explore() 0.68–1.01 s); the real reducer, not a copy.
2. Four rules checked at every state, the fifth on every step (model.ts:114-160); the first broken rule comes with the shortest story;
   the tool's output, verbatim.
"""

import random

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, MODEL_C, NARRATION, OURS_C, USER_C, chip, clear, mono, sans, zh)

SAY = NARRATION["S03"]
RULES = ["一张转诊最多一个有效预约", "有效预约上的转诊指回这个预约", "已预约的转诊有一个有效预约",
         "已用完的转诊来自一次完成的专科就诊", "过期的转诊不会关联到新预约"]


class Explore(VoiceScene):
    def construct(self):
        rng = random.Random(5)
        # 1 ---------------------------------------------------------------- the small world, explored layer by layer
        with self.voiceover(SAY[0]) as vo:
            world = VGroup(chip("2 referrals", USER_C, 22), chip("3 specialist slots", OURS_C, 22),
                           chip("a clock with 2 moments", MODEL_C, 22)).arrange(RIGHT, buff=0.3)
            world.move_to(UP * 3.15)
            moments = sans("moment 1: just after the referrals are written · moment 2: an hour after they expire", 20, S.GREY)
            moments.next_to(world, DOWN, buff=0.12)
            for c, phrase in zip(world, ["two referrals", "three specialist slots", "two moments"]):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=DOWN * 0.1), run_time=0.4)
            self.play(FadeIn(moments), run_time=0.4)
            root = Dot(UP * 1.95, radius=0.12, color=OURS_C)
            start = sans("start", 20, S.GREY).next_to(root, LEFT, buff=0.15)
            vo.wait_until("thirteen possible moves")
            xs1 = np.linspace(-5.4, 5.4, 13)
            layer1 = VGroup(*[Dot([x, 1.0, 0], radius=0.07, color=S.WHITE) for x in xs1])
            edges1 = VGroup(*[Line(root.get_center(), d.get_center(), color=S.GREY_DARK, stroke_width=1.5) for d in layer1])
            n13 = VGroup(sans("13 first moves", 22, S.GREY), sans("1 tick + 3 slots × 4 referral choices", 20, S.GREY)
                         ).arrange(DOWN, aligned_edge=RIGHT, buff=0.05).move_to(RIGHT * 4.3 + UP * 1.85)
            self.play(FadeIn(root), FadeIn(start), run_time=0.3)
            self.play(LaggedStart(*[Create(e) for e in edges1], lag_ratio=0.05), FadeIn(layer1), FadeIn(n13), run_time=1.0)
            vo.wait_until("layer by layer")
            layer2, edges2 = VGroup(), VGroup()
            for d in layer1:
                for k in range(3):
                    p = d.get_center() + np.array([rng.uniform(-0.35, 0.35), -1.0 - rng.uniform(0, 0.15), 0])
                    layer2.add(Dot(p, radius=0.05, color=S.WHITE))
                    edges2.add(Line(d.get_center(), p, color=S.GREY_DARK, stroke_width=1))
            self.play(LaggedStart(*[Create(e) for e in edges2], lag_ratio=0.01), FadeIn(layer2), run_time=1.2)
            vo.wait_until("already seen")
            pairs = [(layer2[i], layer2[i + 1]) for i in range(1, len(layer2) - 1, 6)]
            self.play(*[b.animate.move_to(a.get_center()).set_color(USER_C) for a, b in pairs],
                      *[a.animate.set_color(USER_C) for a, _ in pairs], run_time=0.8)
            merge = sans("seen before → merged", 20, USER_C).move_to(LEFT * 4.6 + DOWN * 0.6)
            self.play(FadeIn(merge), run_time=0.3)
            layer3 = VGroup(*[Dot([rng.uniform(-6.0, 6.0), rng.uniform(-1.9, -1.2), 0], radius=0.03, color=S.GREY)
                              for _ in range(160)])
            self.play(LaggedStart(*[FadeIn(d) for d in layer3], lag_ratio=0.005), run_time=0.8)
            vo.wait_until("13,898 states")
            n = ValueTracker(0)
            spot = DOWN * 2.6 + LEFT * 1.6
            counter = always_redraw(lambda: sans(f"{int(n.get_value()):,}", 56, OURS_C).move_to(spot, aligned_edge=RIGHT))
            unit = sans("states", 30, OURS_C).next_to(spot, RIGHT, buff=0.2)
            self.add(counter, unit)
            self.play(n.animate.set_value(13898), run_time=1.0)
            more = VGroup(sans("173,725 transitions", 22, S.GREY), sans("about a second", 22, S.GREY)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(unit, RIGHT, buff=0.5)
            self.play(FadeIn(more), run_time=0.4)
            vo.wait_until("the real reducer")
            real = chip("every step: the real reducer, not a copy", USER_C, 22).move_to(DOWN * 3.35)
            self.play(FadeIn(real), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- rules at every state; the shortest story
        with self.voiceover(SAY[1]) as vo:
            counter.clear_updaters()   # otherwise always_redraw rebuilds it at full opacity during the fade
            self.play(FadeOut(VGroup(world, moments, n13, merge, more, real, counter, unit, layer3, start)), run_time=0.4)
            tree = VGroup(root, edges1, layer1, edges2, layer2)
            self.play(tree.animate.scale(0.55).move_to(RIGHT * 3.3 + UP * 1.0), run_time=0.6)
            rules = VGroup(*[zh(f"{i + 1}  {r}", 24) for i, r in enumerate(RULES)]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            head = sans("four rules at every state, one on every step", 24, USER_C)
            panel = VGroup(head, rules).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(LEFT * 3.0 + UP * 1.0)
            vo.wait_until("Four rules are checked")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.15), run_time=1.2)
            vo.wait_until("one referral backs at most one")
            self.play(Indicate(rules[0], color=USER_C, scale_factor=1.04), run_time=0.6)
            vo.wait_until("never newly attached")
            self.play(Indicate(rules[4], color=USER_C, scale_factor=1.04), run_time=0.6)
            vo.wait_until("the shortest story")
            # one state in the second layer breaks rule 5; its path back to the start lights up
            bad = tree[4][7]
            parent = tree[2][2]
            path = VGroup(Line(tree[0].get_center(), parent.get_center(), color=DANGER_C, stroke_width=5),
                          Line(parent.get_center(), bad.get_center(), color=DANGER_C, stroke_width=5))
            self.play(bad.animate.set_color(DANGER_C).scale(2.5), rules[4].animate.set_color(DANGER_C), run_time=0.5)
            self.play(Create(path), run_time=0.8)
            vo.wait_until("two steps")
            out = VGroup(zh("✗ 过期的转诊不会关联到新预约", 24, DANGER_C), zh("最短复现：", 22, S.GREY),
                         zh("1. 时间过去，转诊过了有效期（validUntil）", 22), mono("2. appointment/book S1 referralId=ref-v1", 22)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            frame = SurroundingRectangle(out, color=S.GREY_DARK, buff=0.25, corner_radius=0.12).set_fill(S.GREY_DARKER, 1)
            box = VGroup(frame, out).move_to(DOWN * 2.3)
            self.play(FadeIn(box, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
