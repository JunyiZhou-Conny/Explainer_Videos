"""S02 · From "think step by step" to a thinking dial

1. Jan 2022 chain-of-thought prompting (Wei et al., Google); May 2022 "Let's think step by step" (Kojima et al.).
2. Sep 2024 o1: trained with reinforcement learning to reason; raw thoughts hidden for three stated reasons;
   a model-written summary shown instead.
3. 2025: DeepSeek-R1 (reasoning text in the API), Claude 3.7 (raw thinking, research preview), Claude 4
   (long thinking summarized), Claude API today (summary only).
4. Today: reasoning effort, a dial; our menu's three stops 低 / 中 / 高.
Sources: SOURCES.md (papers, OpenAI, DeepSeek and Anthropic pages read 2026-10-30).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (HIDDEN_C, MODEL_C, NARRATION, USER_C, chip, clear, sans, serif, tag_box, tape,
                    text_panel, zh)

SAY = NARRATION["S02"]
X0, X1, Y0 = -6.2, 6.2, -3.05
Y_START, Y_END = 2022.0, 2027.0


def x_of(year: float) -> float:
    return X0 + (year - Y_START) / (Y_END - Y_START) * (X1 - X0)


def marker(year: float, label: str, color=S.WHITE, level: int = 0) -> VGroup:
    """A dot on the axis with its date; `level` stacks the label so neighbouring dates do not collide."""
    d = Dot([x_of(year), Y0, 0], radius=0.08, color=color)
    lab = sans(label, 20, color).next_to(d, UP, buff=0.12).shift(UP * 0.32 * level)
    return VGroup(d, lab)


def model_menu() -> VGroup:
    """Our model menu, redrawn from docs/design/README.md and server.ts MODEL_INFO (labels and notes)."""
    rows = VGroup(*[VGroup(sans(n, 24), zh(note, 20, S.GREY)).arrange(RIGHT, buff=0.3) if note else sans(n, 24)
                    for n, note in [("Astra", "最贵"), ("Sol", ""), ("Terra", ""), ("Luna", "最便宜")]])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    eff = zh("思考强度   低 / 中 / 高", 22)
    rule = Line(LEFT, RIGHT, color=S.GREY_DARK, stroke_width=2).set_width(max(rows.width, eff.width))
    body = VGroup(rows, rule, eff).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    bg = RoundedRectangle(width=body.width + 0.6, height=body.height + 0.5, corner_radius=0.14,
                          stroke_color=S.GREY_DARK, stroke_width=2).set_fill(S.GREY_DARKER, 1)
    body.move_to(bg)
    note = sans("our model menu · redrawn from the design doc", 20, S.GREY).next_to(bg, DOWN, buff=0.12)
    return VGroup(bg, body, note)


class History(VoiceScene):
    def construct(self):
        axis = Line([X0, Y0, 0], [X1, Y0, 0], color=S.GREY, stroke_width=2)
        years = VGroup(*[VGroup(Line([x_of(y), Y0 - 0.08, 0], [x_of(y), Y0 + 0.08, 0], color=S.GREY),
                                sans(str(y), 20, S.GREY).move_to([x_of(y), Y0 - 0.35, 0])) for y in range(2022, 2027)])

        # 1 ---------------------------------------------------------------- 2022: a trick in the prompt
        with self.voiceover(SAY[0]) as vo:
            self.play(Create(axis), FadeIn(years), run_time=0.8)
            vo.wait_until("In January 2022")
            m1 = marker(2022.07, "Jan 2022")
            paper = VGroup(serif("Chain-of-thought prompting", 34), sans("Wei et al. · Google Research", 22, S.GREY)
                           ).arrange(DOWN, buff=0.12).move_to(UP * 2.4)
            self.play(FadeIn(m1), FadeIn(paper, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("write out its steps")
            prompt = text_panel(["Q: …", "A: step 1 …", "   step 2 …", "   so the answer is …"], size=24, width=6.2)
            prompt.move_to(UP * 0.55)
            self.play(FadeIn(prompt, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("Months later")
            m2 = marker(2022.38, "May 2022", level=1)
            magic = mono_line = Text("Let's think step by step.", font=S.FONT, font_size=34, color=USER_C)
            magic.next_to(prompt, DOWN, buff=0.35)
            self.play(FadeIn(m2), Write(magic), run_time=0.9)
            vo.wait_until("a trick in the prompt")
            trick = chip("a trick in the prompt", USER_C, 22, mono_font=False).next_to(magic, DOWN, buff=0.3)
            self.play(FadeIn(trick, scale=1.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- 2024: o1 thinks by itself
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(paper, prompt, magic, trick)), m1.animate.set_opacity(0.4),
                      m2.animate.set_opacity(0.4), run_time=0.5)
            m3 = marker(2024.7, "Sep 2024", MODEL_C)
            o1 = tag_box("model", "o1 · OpenAI", "trained with reinforcement learning to reason", MODEL_C, width=6.4)
            o1.move_to(UP * 2.35)
            self.play(FadeIn(m3), FadeIn(o1, shift=DOWN * 0.15), run_time=0.7)
            thoughts = tape(26, 26, size=0.24).move_to(UP * 0.85)
            self.play(LaggedStart(*[FadeIn(c) for c in thoughts], lag_ratio=0.05), run_time=1.2)
            vo.wait_until("chose not to show")
            curtain = Rectangle(width=thoughts.width + 0.4, height=0.75, stroke_color=HIDDEN_C, stroke_width=2
                                ).set_fill(S.BG, 0.95).move_to(thoughts)
            hidden = sans("raw thoughts · hidden", 22, S.GREY).move_to(curtain)
            self.play(FadeIn(curtain), FadeIn(hidden), run_time=0.6)
            reasons = VGroup(*[chip(t, S.GREY, 22, mono_font=False) for t in
                               ["user experience", "competitive advantage", "monitoring the thoughts"]]
                             ).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.35)
            for r, phrase in zip(reasons, ["user experience", "competitive advantage", "monitor them"]):
                vo.wait_until(phrase)
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
            vo.wait_until("a summary")
            summary = chip("a summary, written by a model", S.WHITE, 24, mono_font=False).move_to(DOWN * 1.45)
            self.play(FadeIn(summary, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- 2025: others choose differently
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(o1, thoughts, curtain, hidden, reasons, summary)),
                      m3.animate.set_opacity(0.4), run_time=0.5)
            items = [(2025.05, "Jan 2025", "DeepSeek-R1", "reasoning text in the API", "R1", 1),
                     (2025.15, "Feb 2025", "Claude 3.7", "raw thinking · research preview", "Claude 3.7", 2),
                     (2025.39, "May 2025", "Claude 4", "long thinking summarized", "From Claude 4", 3),
                     (2026.83, "today", "Claude API", "summary only", "today's Claude API", 0)]
            boxes = VGroup(*[tag_box(d, n, s, S.GREY, width=5.4, name_size=26, sub_size=22, fill=0.0)
                             for _, d, n, s, _, _ in items]).arrange_in_grid(2, 2, buff=(0.4, 0.3)).move_to(UP * 1.45)
            marks = VGroup(*[marker(y, lab, S.GREY, lv) for y, lab, _, _, _, lv in items])
            for i, (b, m, it) in enumerate(zip(boxes, marks, items)):
                vo.wait_until(it[4])
                self.play(FadeIn(b, shift=DOWN * 0.1), FadeIn(m), run_time=0.45)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- today: a dial
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(boxes), run_time=0.4)
            arc = Arc(radius=1.6, start_angle=PI, angle=-PI, color=S.GREY, stroke_width=6).move_to(UP * 0.9 + LEFT * 3.0)
            centre = arc.get_arc_center()
            stops = []
            for k, (lab_zh, lab_en) in enumerate([("低", "low"), ("中", "medium"), ("高", "high")]):
                ang = PI - (k + 1) * PI / 4
                p = centre + 1.6 * np.array([np.cos(ang), np.sin(ang), 0])
                d = Dot(p, radius=0.09, color=S.WHITE)
                lab = VGroup(zh(lab_zh, 28), sans(lab_en, 20, S.GREY)).arrange(DOWN, buff=0.04)
                lab.move_to(centre + 2.15 * np.array([np.cos(ang), np.sin(ang), 0]))
                stops.append(VGroup(d, lab))
            needle = Line(centre, centre + 1.3 * LEFT, color=USER_C, stroke_width=6)
            head = VGroup(sans("reasoning effort", 26, S.WHITE), zh("思考强度", 26, S.GREY)
                          ).arrange(RIGHT, buff=0.3).next_to(arc, DOWN, buff=0.35)
            self.play(Create(arc), FadeIn(head), run_time=0.7)
            vo.wait_until("reasoning effort")
            self.play(FadeIn(needle), run_time=0.3)
            vo.wait_until("next to the model")
            menu = model_menu().move_to(RIGHT * 3.4 + UP * 0.75)
            self.play(FadeIn(menu, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("three levels")
            self.play(LaggedStart(*[FadeIn(s) for s in stops], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("medium")
            self.play(Rotate(needle, -PI / 2, about_point=centre), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
