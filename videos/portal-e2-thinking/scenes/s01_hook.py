"""S01 · Eleven seconds of what?

1. The live line from Conny's screenshot: an orange dot and 「正在思考 · N 秒」, ticking to 11.
2. It folds into 「思考了 22 秒 ›」 and opens: 过程 and 模型 rows (verbatim); bars 13.5 s | 8.7 s.
3. A question mark over the thinking bar; a stopwatch, and a curtain over the thoughts.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (FOLDED, HIDDEN_C, MODEL_22, NARRATION, PROCESS_22, USER_C, clear, phase_bars,
                    receipt, screen, stopwatch, thinking_line, zh)

SAY = NARRATION["S01"]


class Hook(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the live line ticks
        with self.voiceover(SAY[0]) as vo:
            scr = screen(7.4, 1.5).move_to(UP * 0.6)
            live = thinking_line(9).move_to(scr)
            self.play(FadeIn(scr), FadeIn(live), run_time=0.6)
            self.play(live[1].animate.set_opacity(0.45), rate_func=there_and_back, run_time=0.9)
            for s, phrase in [(10, "says"), (11, "eleven seconds")]:
                vo.wait_until(phrase)
                self.play(Transform(live, thinking_line(s).move_to(scr)), run_time=0.25)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- folded, then opened
        with self.voiceover(SAY[1]) as vo:
            vo.wait_until("folds into")
            folded = zh(f"{FOLDED} ›", 32, S.GREY).move_to(scr)
            self.play(FadeOut(live), FadeIn(folded), run_time=0.5)
            vo.wait_until("Open it")
            big = screen(11.6, 3.1).move_to(UP * 1.45)
            rec = receipt([("过程", PROCESS_22), ("模型", MODEL_22)], 10.6, size=28)
            rec.move_to(big).align_to(big, LEFT).shift(RIGHT * 0.45)
            self.play(ReplacementTransform(scr, big), ReplacementTransform(folded, rec[0]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rec[1:]], lag_ratio=0.4), run_time=1.0)
            vo.wait_until("splits in two")
            bars = phase_bars(13.5, 8.7, unit=0.55, height=0.55, write_label="写 8.7 秒（1717 字）").move_to(DOWN * 1.75)
            self.play(GrowFromEdge(bars.think, LEFT), FadeIn(bars[2]), run_time=0.8)
            vo.wait_until("then 8.7")
            self.play(GrowFromEdge(bars.write, LEFT), FadeIn(bars[3]), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- what is inside the grey?
        with self.voiceover(SAY[2]) as vo:
            q = Text("?", font=S.FONT, font_size=110, color=USER_C).next_to(bars.think, DOWN, buff=0.2)
            self.play(FadeIn(q, scale=1.4), run_time=0.5)
            vo.wait_until("why does ours")
            watch = stopwatch(0.36, S.WHITE).move_to([big.get_right()[0] - 0.8, big.get_center()[1], 0])
            curtain = Rectangle(width=bars.think.width, height=bars.think.height + 0.25, stroke_color=HIDDEN_C,
                                stroke_width=2).set_fill(S.BG, 0.92).move_to(bars.think)
            hidden = zh("思考的内容 · 不显示", 24, S.GREY).move_to(curtain)
            self.play(FadeIn(watch, scale=1.2), Rotate(watch[2], -PI, about_point=watch[0].get_center()), run_time=0.8)
            vo.wait_until("never the thoughts")
            self.play(FadeIn(curtain), FadeIn(hidden), FadeOut(q), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.8)
        clear(self)
