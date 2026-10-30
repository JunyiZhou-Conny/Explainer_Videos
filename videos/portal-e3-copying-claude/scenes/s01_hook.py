"""S01 · Copied, on purpose

1. The empty triage page redrawn in its own colours; beside it the same layout as grey outlines
   (Claude's app, no logo or name); connectors pair greeting, box and chips.
2. "copy?" and the episode's four parts: copied · not copied · added · not built yet.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import NARRATION, USER_C, chip, clear, empty_page, outline_of, sans, serif

SAY = NARRATION["S01"]


class Hook(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- our page, and an outline like it
        with self.voiceover(SAY[0]) as vo:
            ours = empty_page().move_to(LEFT * 3.3 + UP * 0.25)
            tag_ours = sans("our triage page (redrawn)", 20, S.GREY).next_to(ours, DOWN, buff=0.12)
            self.play(FadeIn(ours.frame), FadeIn(ours.bar), FadeIn(tag_ours), run_time=0.6)
            vo.wait_until("a serif greeting")
            self.play(Write(ours.greeting), run_time=0.8)
            vo.wait_until("an input box")
            self.play(FadeIn(ours.composer, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("a row of suggestions")
            self.play(FadeIn(ours.demo), LaggedStart(*[FadeIn(c) for c in [*ours.chips[0], *ours.chips[1]]],
                                                     lag_ratio=0.2), FadeIn(ours.fine), run_time=1.0)
            vo.wait_until("reminds you of Claude's app")
            ghost = outline_of(ours).move_to(RIGHT * 3.3 + UP * 0.25)
            tag_c = sans("Claude's app (outline, no logo)", 20, S.GREY).next_to(ghost, DOWN, buff=0.12)
            self.play(Create(ghost), FadeIn(tag_c), run_time=1.2)
            pairs = [(ours.greeting, ghost[1]), (ours.composer.box, ghost[2]), (ours.chips[0], ghost[3])]
            links = VGroup(*[DashedLine(a.get_right(), b.get_left(), color=USER_C, stroke_width=2, dash_length=0.08)
                             for a, b in pairs])
            self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("a one-to-one copy")
            stamp = chip("you asked: a one-to-one copy · issue #40", USER_C, 26, mono_font=False).move_to(UP * 3.3)
            self.play(FadeIn(stamp, scale=1.15), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the episode's question
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            q = serif("copy?", 72, USER_C).move_to(UP * 1.6)
            self.play(Write(q), run_time=0.7)
            parts = VGroup(*[chip(t, c, 26, mono_font=False) for t, c in
                             [("copied", S.GREEN), ("not copied", S.RED), ("added", S.BLUE), ("not built yet", S.GREY)]]
                           ).arrange(RIGHT, buff=0.4).move_to(DOWN * 0.8)
            for p, phrase in zip(parts, ["What was copied", "what was refused", "what we added", "nobody has built"]):
                vo.wait_until(phrase)
                self.play(FadeIn(p, shift=UP * 0.1), run_time=0.35)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
