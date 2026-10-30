"""S08 · What it cost (only the figures on record; ../SOURCES.md)

1. The product's own model calls, as stated: one real answer $0.036 (PR #36 body); the first day ≈ $0.77
   (PR #36 handoff of 10-28); the last night ≈ $0.27 against a $0.50 cap (PR #41 handoff of 10-29).
   Budget defaults in the code: $2 for the server, $10 for an evaluation.
2. The agents' own work: no dollar figure anywhere in the repository; the one number is ≈ 800,000 tokens
   per fix agent, six of them queued (PR #41 handoff, 「流程问题」).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import DANGER_C, MODEL_C, NARRATION, USER_C, clear, sans

SAY = NARRATION["S08"]
UNIT, X0 = 4.0, -3.0          # dollars → scene units; where the bars start
ROWS = [("one real answer", 0.036, "$0.036", "about 4 cents"),
        ("the first day", 0.77, "≈ $0.77", "about 77 cents"),
        ("the last night", 0.27, "≈ $0.27", "27 cents on")]


class Cost(VoiceScene):
    def construct(self):
        with self.voiceover(SAY[0]) as vo:
            head = sans("What it cost · only the figures on record", 26, S.GREY).move_to(UP * 3.2)
            self.play(FadeIn(head), run_time=0.4)
            # left: the product's own model calls, one bar per stated figure
            sub_l = sans("the product's model calls", 26, MODEL_C).move_to(LEFT * 3.4 + UP * 2.35)
            self.play(FadeIn(sub_l), run_time=0.3)
            labs = VGroup(*[sans(name, 22, S.GREY).next_to([X0, 1.3 - k * 1.05, 0], LEFT, buff=0.2)
                            for k, (name, *_) in enumerate(ROWS)])
            vo.wait_until("on the record")
            self.play(LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.2), run_time=0.6)
            bars = []
            for k, (name, usd, value, phrase) in enumerate(ROWS):
                y = 1.3 - k * 1.05
                bar = Rectangle(width=max(usd * UNIT, 0.05), height=0.42, stroke_width=0).set_fill(MODEL_C, 0.8)
                bar.move_to([X0, y, 0], aligned_edge=LEFT)
                # the last night's figure sits right of its cap, drawn next
                val = sans(value, 24).next_to([X0 + max(usd, 0.5 if k == 2 else 0) * UNIT, y, 0], RIGHT, buff=0.15)
                vo.wait_until(phrase)
                self.play(GrowFromEdge(bar, LEFT), FadeIn(val), run_time=0.5)
                bars.append(VGroup(labs[k], bar, val))
            vo.wait_until("50-cent cap")
            y = bars[2][1].get_y()
            cap = DashedVMobject(Rectangle(width=0.5 * UNIT, height=0.42, stroke_color=USER_C, stroke_width=2.5), num_dashes=40)
            cap.move_to([X0, y, 0], aligned_edge=LEFT)
            cap_l = sans("cap $0.50", 22, USER_C).next_to(cap, DOWN, buff=0.08).align_to(cap, RIGHT)
            defaults = VGroup(sans("budget defaults in the code", 22, S.GREY), sans("server $2 · evaluation $10", 22, S.GREY)
                              ).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to(LEFT * 3.4 + DOWN * 2.6)
            self.play(Create(cap), FadeIn(cap_l), FadeIn(defaults), run_time=0.5)

            # right: the agents' own work, in tokens only
            divider = Line(UP * 2.6 + RIGHT * 1.2, DOWN * 3.2 + RIGHT * 1.2, color=S.GREY_DARK, stroke_width=2)
            sub_r = sans("the agents' own work", 26).move_to(RIGHT * 3.9 + UP * 2.35)
            vo.wait_until("agents' own work")
            self.play(Create(divider), FadeIn(sub_r), run_time=0.4)
            vo.wait_until("priced nowhere")
            unknown = VGroup(sans("$ ?", 56, DANGER_C), sans("no dollar figure in the repository", 22, S.GREY)
                             ).arrange(DOWN, buff=0.1).move_to(RIGHT * 3.9 + UP * 1.3)
            self.play(FadeIn(unknown[0], scale=1.2), FadeIn(unknown[1]), run_time=0.5)
            vo.wait_until("about 800,000")
            # six fix agents queued; one block = 100,000 tokens
            cols = VGroup(*[VGroup(*[Square(0.26, stroke_width=0).set_fill(S.GREY, 0.85) for _ in range(8)]
                                   ).arrange(UP, buff=0.04) for _ in range(6)]).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
            cols.move_to(RIGHT * 3.9 + DOWN * 1.05)
            self.play(LaggedStart(*[LaggedStart(*[GrowFromEdge(c, DOWN) for c in col], lag_ratio=0.1) for col in cols],
                                  lag_ratio=0.12), run_time=1.4)
            legend = VGroup(sans("≈ 800,000 tokens per fix agent", 24, USER_C), sans("one block = 100,000 tokens", 20, S.GREY)
                            ).arrange(DOWN, buff=0.06).next_to(cols, DOWN, buff=0.2)
            self.play(FadeIn(legend), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(1.0)
        clear(self)
