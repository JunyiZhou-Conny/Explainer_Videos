"""S06 · The early 911

1. The form's boxes in the order the model writes them; the first five light up as the tokens arrive.
2. The progress line carries "emergency": true; the page shows our fixed warning (student version,
   ThinkingRow.tsx EarlyEmergency), not model text.
3. A time axis: warning at 3.5 s; the checked answer roughly 20 s after it (PR #41: 「约 21 秒后」).
   An emergency is never taken back (E1), so the answer is bound to agree.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, EARLY_911, FORM, NARRATION, OURS_C, USER_C, chip, clear, mono,
                    sans, screen, text_panel, zh, zh_wrap)

SAY = NARRATION["S06"]


class Early911(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- urgency first
        with self.voiceover(SAY[0]) as vo:
            names = VGroup(*[mono(n, 24, S.GREY) for n in FORM]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            names.move_to(LEFT * 4.6)
            # the first five boxes, in the form's own terms (schema.ts): all about urgency
            gloss = ["紧急程度", "去哪里", "追问危险信号", "已有的危险信号", "紧急行动"]
            rows = VGroup(*[VGroup(n, zh(g, 20, S.GREY).next_to(n, RIGHT, buff=0.25).set_x(names.get_right()[0] + 0.3, LEFT))
                            if i < 5 else VGroup(n) for i, (n, g) in enumerate(zip(names, gloss + [""] * len(FORM)))])
            head = sans("the form, in writing order", 22, S.GREY).next_to(rows, UP, buff=0.3).align_to(rows, LEFT)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.05), run_time=1.2)
            vo.wait_until("writes them first")
            self.play(LaggedStart(*[r.animate.set_color(USER_C) for r in rows[:5]], lag_ratio=0.3), run_time=1.2)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the flag and our warning
        with self.voiceover(SAY[1]) as vo:
            vo.wait_until("raises a flag")
            line = text_panel(['{"type":"progress","attempt":1,', ' "section":"emergency","chars":…,', ' "emergency":true}'],
                              size=22, t2c={'"emergency":true': DANGER_C})
            line.move_to(RIGHT * 2.6 + UP * 2.0)
            self.play(rows[4].animate.set_color(DANGER_C), FadeIn(line, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("a warning we wrote")
            scr = screen(6.2, 2.5).move_to(RIGHT * 2.6 + DOWN * 0.6)
            frame = RoundedRectangle(width=5.8, height=1.7, corner_radius=0.12, stroke_color=DANGER_C,
                                     stroke_width=3).move_to(scr)
            warn = zh_wrap(EARLY_911, 5.3, 26, S.WHITE).move_to(frame)
            ours = VGroup(sans("written by us, not by the model · student version", 20, S.GREY))
            ours.next_to(scr, DOWN, buff=0.12)
            self.play(FadeIn(scr), Create(frame), FadeIn(warn), FadeIn(ours), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- 3.5 s, then the checked answer
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(rows, head, line)), VGroup(scr, frame, warn, ours).animate.move_to(UP * 1.95),
                      run_time=0.6)
            unit = 0.45
            x0 = -6.0
            axis = NumberLine(x_range=[0, 26, 5], length=26 * unit, include_numbers=False,
                              color=S.GREY).move_to([x0 + 13 * unit, -1.6, 0])
            nums = VGroup(*[sans(str(t), 22, S.GREY).next_to(axis.n2p(t), DOWN, buff=0.18) for t in range(0, 26, 5)])
            secs = sans("seconds after sending", 20, S.GREY).next_to(nums, DOWN, buff=0.15)
            self.play(Create(axis), FadeIn(nums), FadeIn(secs), run_time=0.6)
            vo.wait_until("3.5 seconds")
            p1 = axis.n2p(3.5)
            m1 = VGroup(Line(p1, p1 + UP * 1.1, color=DANGER_C, stroke_width=5),
                        zh("911 提醒 · 3.5 秒", 24, DANGER_C).move_to(p1 + UP * 1.4))
            self.play(Create(m1[0]), FadeIn(m1[1]), run_time=0.5)
            vo.wait_until("about 21 seconds")
            p2 = axis.n2p(21)
            m2 = VGroup(Line(p2, p2 + UP * 1.1, color=CHECKED_C, stroke_width=5),
                        zh("检查过的回答 ·「现在就做」· 约 21 秒", 22, CHECKED_C).move_to(p2 + UP * 1.4))
            span = DoubleArrow(p1 + UP * 0.25, p2 + UP * 0.25, color=S.GREY, buff=0.05, stroke_width=3)
            approx = sans("the warning comes ≈ 17 s sooner", 22, S.GREY).next_to(span, UP, buff=0.08)
            self.play(GrowArrow(span), FadeIn(approx), FadeIn(m2), run_time=0.7)
            vo.wait_until("never taken back")
            rule = chip("紧急不收回 · E1", DANGER_C, 24, mono_font=False).move_to(RIGHT * 4.7 + DOWN * 3.0)
            self.play(FadeIn(rule, scale=1.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
