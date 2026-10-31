"""S09 · A receipt, not the thoughts

1. Three panels. Claude's app: a "Thinking" indicator with a timer and an expandable summary (Anthropic's help
   page). ChatGPT: a model-written summary of the reasoning (OpenAI, 2024; illustration). Ours: the
   stopwatch and the receipt's five rows.
2. Decision 0006: 「不显示模型的推理原文：里面可能有诊断性的猜测，又没有经过检查。」
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (FOLDED, NARRATION, OURS_C, clear, quote_panel, sans, screen, stopwatch, zh)

SAY = NARRATION["S09"]


def bars(n, width):
    return VGroup(*[Rectangle(width=width - 0.45 * (k % 2), height=0.12, stroke_width=0).set_fill(S.GREY, 0.7)
                    for k in range(n)]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)


def panel(title, color, body, note):
    frame = RoundedRectangle(width=4.1, height=4.3, corner_radius=0.18, stroke_color=color, stroke_width=2.5)
    head = sans(title, 26, color).next_to(frame.get_top(), DOWN, buff=0.3)
    body.next_to(head, DOWN, buff=0.35)
    n = sans(note, 20, S.GREY).next_to(frame.get_bottom(), UP, buff=0.18)
    return VGroup(frame, head, body, n)


class Receipt(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- three ways to open the thinking
        with self.voiceover(SAY[0]) as vo:
            claude_body = VGroup(VGroup(sans("Thinking", 24), stopwatch(0.16, S.WHITE)).arrange(RIGHT, buff=0.2),
                                 sans("› a summary", 20, S.GREY), bars(4, 3.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            gpt_body = VGroup(sans("a summary of", 20, S.GREY), sans("the reasoning", 20, S.GREY), bars(4, 3.2)
                              ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            rows = VGroup(*[VGroup(zh(r, 22, S.GREY), sans(g, 20, S.GREY)).arrange(RIGHT, buff=0.25)
                            for r, g in [("过程", "timings"), ("依据", "sources"), ("检查", "the check"),
                                         ("判断", "judgment"), ("模型", "model · price")]]
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            ours_body = VGroup(VGroup(zh(f"{FOLDED} ›", 24), stopwatch(0.16, S.WHITE)).arrange(RIGHT, buff=0.2), rows
                               ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            p1 = panel("Claude app", S.GREY, claude_body, "per Anthropic's help page")
            p2 = panel("ChatGPT", S.GREY, gpt_body, "illustration")
            p3 = panel("ours", OURS_C, ours_body, "the receipt")
            VGroup(p1, p2, p3).arrange(RIGHT, buff=0.35).move_to(UP * 0.95)
            folded = VGroup(screen(5.2, 1.3), zh(f"{FOLDED} ›", 34, S.GREY))
            folded[1].move_to(folded[0])
            self.play(FadeIn(folded), run_time=0.5)
            vo.wait_until("Claude's app")
            self.play(FadeOut(folded), FadeIn(p1, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("like ChatGPT")
            self.play(FadeIn(p2, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Ours opens")
            self.play(FadeIn(p3, shift=UP * 0.1), run_time=0.6)
            for r, phrase in zip(rows, ["the timings", "the sources", "the check", "the judgment", "the model"]):
                vo.wait_until(phrase)
                self.play(r.animate.set_color(S.WHITE), run_time=0.25)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- why
        with self.voiceover(SAY[1]) as vo:
            self.play(VGroup(p1, p2).animate.set_opacity(0.25), run_time=0.4)
            vo.wait_until("Raw reasoning")
            q = quote_panel("不显示模型的推理原文：里面可能有诊断性的猜测，又没有经过检查。", "decision 0006", width=12.4, size=28)
            q.to_edge(DOWN, buff=0.5)
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
