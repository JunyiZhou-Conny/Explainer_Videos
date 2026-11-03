"""S05 · Why not the words, and who decided

1. Ponder: why not stream the words and pull them back if the checker objects?
2. A streamed line with a dose (illustration) flashes on a phone; a screenshot; struck out, too late.
   Decision 0006, considered and not done: the verbatim line.
3. You asked for streaming (decision 0006: Junyi 要求「模型回答的 streaming」); the agent chose progress-only,
   unattended, and wrote it down as 提议: 「具体做法是无人值守时定的，还没有人确认」.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (DANGER_C, NARRATION, OURS_C, USER_C, chip, clear, ponder_zh, quote_panel, sans, zh)

SAY = NARRATION["S05"]


class WhyNot(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- ponder
        with self.voiceover(SAY[0]) as vo:
            card = ponder_zh(self, "Why not stream the words, and pull them back if the checker objects?",
                             "为什么不直接流式显示文字，检查不过再收回？", seconds=4.0)
        self.wait(3.5)

        # 2 ---------------------------------------------------------------- a screen cannot unsay
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            phone = RoundedRectangle(width=3.6, height=5.6, corner_radius=0.35, stroke_color=S.GREY,
                                     stroke_width=3).move_to(LEFT * 4.3 + DOWN * 0.1)
            l1 = zh("孩子发烧、喉咙痛……", 22).move_to(phone).shift(UP * 1.6)
            l2 = zh("可以每六小时吃两片……", 22, S.WHITE).next_to(l1, DOWN, buff=0.35)
            illus = sans("illustration", 20, S.GREY).next_to(phone, DOWN, buff=0.1)
            self.play(Create(phone), FadeIn(illus), run_time=0.5)
            self.play(AddTextLetterByLetter(l1), run_time=0.8)
            vo.wait_until("If a dose")
            self.play(AddTextLetterByLetter(l2), run_time=0.8)
            vo.wait_until("screenshot")
            flash = phone.copy().set_stroke(width=0).set_fill(S.WHITE, 0.85)
            shot = chip("screenshot", S.WHITE, 22, mono_font=False).next_to(phone, RIGHT, buff=0.3).shift(UP * 1.2)
            self.play(FadeIn(flash), run_time=0.08)
            self.play(FadeOut(flash), FadeIn(shot), run_time=0.35)
            strike = Line(l2.get_left() + LEFT * 0.1, l2.get_right() + RIGHT * 0.1, color=DANGER_C, stroke_width=5)
            late = sans("pulled back: too late", 22, DANGER_C).next_to(shot, DOWN, buff=0.25).align_to(shot, LEFT)
            self.play(Create(strike), FadeIn(late), run_time=0.5)
            vo.wait_until("So the decision record")
            q = quote_panel("直接流式显示模型的原文（像 Claude 那样）：没有经过检查，可能出现剂量、诊断、编造的电话，出来以后再收回更糟。不做。",
                            "decision 0006 · 10-28 addendum · considered, not done", width=6.6, size=26)
            q.move_to(RIGHT * 2.9 + DOWN * 1.1)
            self.play(FadeIn(q, shift=LEFT * 0.15), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- who decided
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.4)
            asked = VGroup(sans("you asked for", 24, S.GREY), zh("「模型回答的 streaming」", 30, USER_C)
                           ).arrange(DOWN, buff=0.15).move_to(LEFT * 4.2 + UP * 1.8)
            chose = VGroup(sans("the agent chose, unattended", 24, S.GREY), zh("「流的是进度，不是模型的原文」", 30, OURS_C)
                           ).arrange(DOWN, buff=0.15).move_to(RIGHT * 2.6 + UP * 1.8)
            arrow = Arrow(asked.get_right(), chose.get_left(), color=S.GREY, buff=0.3)
            self.play(FadeIn(asked, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("The agent")
            self.play(GrowArrow(arrow), FadeIn(chose, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("as a proposal")
            q = quote_panel("具体做法是无人值守时定的，还没有人确认。", "decision 0006 · status", width=9.4, size=28)
            status = chip("提议 · proposed", USER_C, 26, mono_font=False)
            VGroup(q, status).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.2)
            self.play(FadeIn(q), FadeIn(status, scale=1.15), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
