"""S10 · What else, and what waits for you

1. Three ideas: a reasoning summary put through the checker first (OpenAI's `summary` parameter); progress
   that names real steps (an idea); a developer-only view of unchecked drafts (decision 0006: an open
   question, not built).
2. Decisions waiting: progress-only streaming and the model menu (提议), the developer switch (待定).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (NARRATION, OURS_C, USER_C, chip, clear, sans, serif, tag_box, zh)

SAY = NARRATION["S10"]


class Next(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- three ideas
        with self.voiceover(SAY[0]) as vo:
            ask = VGroup(sans("what else could it do?", 30), zh("还能做什么？", 30, S.GREY)).arrange(RIGHT, buff=0.35)
            ask.to_edge(UP, buff=0.6)
            self.play(FadeIn(ask, shift=DOWN * 0.1), run_time=0.5)
            cards = VGroup(
                VGroup(sans("1 · a reasoning summary", 22), sans("OpenAI can return one,", 20, S.GREY),
                       sans("but a model writes it:", 20, S.GREY), sans("checker first", 22, USER_C)),
                VGroup(sans("2 · progress with real steps", 22), zh("「正在核对 SHS 营业时间」", 22, S.GREY),
                       sans("an idea", 20, S.GREY)),
                VGroup(sans("3 · a developer-only draft view", 22), sans("to tune prompts", 20, S.GREY),
                       sans("an open question · not built", 20, USER_C)))
            for c in cards:
                c.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            frames = VGroup(*[SurroundingRectangle(c, color=S.GREY_DARK, buff=0.22, corner_radius=0.15) for c in cards])
            groups = VGroup(*[VGroup(f, c) for f, c in zip(frames, cards)]).arrange(RIGHT, buff=0.2).move_to(UP * 1.3)
            for g, phrase in zip(groups, ["a summary of the hidden", "name real steps", "developer-only switch"]):
                vo.wait_until(phrase)
                self.play(FadeIn(g, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- waiting for you
        with self.voiceover(SAY[1]) as vo:
            head = VGroup(zh("等你决定", 34, USER_C), sans("waiting for you", 22, S.GREY)).arrange(RIGHT, buff=0.3)
            head.move_to(DOWN * 1.2)
            chips = VGroup(VGroup(chip("progress-only streaming", USER_C, 22, mono_font=False), zh("提议", 22, USER_C)),
                           VGroup(chip("the model menu", USER_C, 22, mono_font=False), zh("提议", 22, USER_C)),
                           VGroup(chip("the developer switch", S.GREY, 22, mono_font=False), zh("待定", 22, S.GREY)))
            for c in chips:
                c.arrange(DOWN, buff=0.12)
            chips.arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.4)
            self.play(FadeIn(head), run_time=0.4)
            for c, phrase in zip(chips, ["Progress-only streaming", "the model menu", "the developer switch"]):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=UP * 0.1), run_time=0.4)
            src = sans("decision 0006 · 10-28 addendum", 20, S.GREY).next_to(chips, DOWN, buff=0.3)
            self.play(FadeIn(src), run_time=0.3)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
