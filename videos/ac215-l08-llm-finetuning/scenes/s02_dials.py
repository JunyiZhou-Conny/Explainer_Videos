"""S02 · Three dials: prompt, context, weights (concept scene: no README tracker). Lecture: 4–8.

Beats (script.md "## S02", one voiceover block each):
 0. V1: the BLUE model box (a grid of weight cells) with three dials under it, prompt / context /
    weights; input arrow from the left, output arrow to the right. On "prompt" the first dial turns
    and a GREY "system prompt" card slides onto the input lane; on "Retrieval" the second dial
    turns and three PINK retrieved-chunk cards (chip "L05 · RAG") stack onto it. On "untouched"
    both input cards flash and the grid stays still (GREY tag "the weights: unchanged").
 1. LECTURE 4–6. The input cards leave; the model moves left. The third dial turns: the grid
    shimmers, the box pulses; a stack of "(input, desired output)" cards flows into the box. GREY
    chips "instruction fine-tuning" (slide 4), then "task-specific fine-tuning" + ‹instructor› (6).
 2. LECTURE 7–8. Three rows (slide 8's contrast, our drawing). Row 1 GREY "OPT-350m · plain
    next-word predictor": the input chip "Hello my cheese name is" (colab/cell-23.py line 1), then
    RECORDED(expected/colab-c27-opt-generate.txt: 11–12) with the tag `recorded`; the input part
    gets a GREY bar, the continuation a YELLOW underline. Rows 2 and 3 show their labels and
    empty bubbles.
 3. Row 2 lights: its GREY bubble (our drawing, `illustration`) answers "Sure, here's…" (YELLOW),
    caption "a habit a chat model learned". Row 3 lights: its BLUE bubble answers with c82 line 159
    (cut after "monker", then an exact sub-string); the persona chip GREY; a small RED ✗ on "water
    molecules". YELLOW banner "style is learnable · facts are not guaranteed", GREY caption "what
    the saved run shows".
 4. The rows clear. Left: a GREY desk with an open book of PINK chunks ("RAG: the open book on the
    desk"); right: the voice box with its dial on "weights" ("fine-tuning: the default voice").
    Both shrink to the top; S01's two-track map comes back small at the bottom (rebuilt to S01's
    SHOW: there is no shared object across scene files); Track A gains a GREY crossed-out eye "you
    never see a weight", Track B a GREEN save glyph "yours to keep". Fade to an empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import MONO, box, chip, label, mono, substring
from explainer.scene import VoiceScene

from common import (ADAPTER, CAPTION, CLOUD, CTR, ERR, INK, LAPTOP, LOOKUP, MODEL, NARRATION, OWN, PERSONA,
                    TURN, Dial, _rich, capture, grey_tag, illustration_tag, lref, persona_chip,
                    recorded_box, recorded_tag, source_line, unname, x_mark)
from common import ThreeDials as DialsPiece
from s01_hook import gpu_box, track_chain              # S01's own map pieces: the same drawing

SAY = NARRATION["S02"]

C27 = capture("expected/colab-c27-opt-generate")      # lines 11-12: OPT-350m keeps going
C82 = capture("expected/colab-c82-base-vs-finetuned")  # line 159: the fine-tuned answer
_SRC25 = source_line("colab/cell-23.py", 1)            # text = "Hello my cheese name is"
INPUT_TEXT = _SRC25.split('"')[1]
OPENER = C82.cut(159, "monker")                        # "Yello - this is ‹instructor› your cheese monker …"
_L159 = C82.line(159)
_SUB = "by the water molecules in the atmosphere."
assert _SUB in _L159
WATER = "water molecules"


# ------------------------------------------------------------------ small helpers
def text_glyphs(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of `sub` in a Text built from string `s` (Text drops spaces)."""
    i = s.find(sub)
    if i < 0:
        raise ValueError(f"{sub!r} not in {s!r}")
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def input_card(text: str, color, w: float = 2.7, h: float = 0.5, font=None) -> VGroup:
    t = (mono(text, CAPTION, INK) if font else label(text, CAPTION, INK))
    fr = box(max(w, t.width + 0.4), h, color, fill=S.BG, fill_opacity=1.0, radius=0.1, stroke=2.5)
    tint = RoundedRectangle(width=fr.width, height=h, corner_radius=0.1, stroke_width=0).set_fill(color, 0.12)
    t.move_to(fr)
    g = VGroup(fr, tint, t)
    g.frame, g.text = fr, t
    return g


def blank_card(w: float, h: float, color) -> VGroup:
    fr = box(w, h, color, fill=S.BG, fill_opacity=1.0, radius=0.1, stroke=2.5)
    tint = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_width=0).set_fill(color, 0.12)
    return VGroup(fr, tint)


def row_label(lines, color, w: float = 3.0, h: float = 1.0, dashed: bool = False) -> VGroup:
    body = VGroup(*[label(s, CAPTION, INK if k == 0 else S.GREY) for k, s in enumerate(lines)]) \
        .arrange(DOWN, buff=0.08)
    fr = box(w, h, color, fill=S.BG, fill_opacity=1.0, radius=0.12, stroke=2.5, dashed=dashed)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.body = fr, body
    return g


def bubble(w: float, h: float, color, fill_op: float = 0.08) -> VGroup:
    """A speech bubble: rounded box with a small tail on its left edge."""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.16, stroke_color=color, stroke_width=2.5) \
        .set_fill(color, fill_op)
    l = fr.get_left()
    tail = Polygon(l + UP * 0.12 + RIGHT * 0.02, l + LEFT * 0.22 + DOWN * 0.02, l + DOWN * 0.14 + RIGHT * 0.02,
                   stroke_color=color, stroke_width=2.5).set_fill(S.BG, 1)
    cover = Line(l + UP * 0.1 + RIGHT * 0.015, l + DOWN * 0.12 + RIGHT * 0.015, color=S.BG, stroke_width=4)
    g = VGroup(fr, tail, cover)
    g.frame = fr
    return g


def eye_crossed(w: float = 0.6, color=S.GREY) -> VGroup:
    left, right = LEFT * w / 2, RIGHT * w / 2
    top = ArcBetweenPoints(left, right, angle=-1.6, color=color, stroke_width=3)
    bot = ArcBetweenPoints(left, right, angle=1.6, color=color, stroke_width=3)
    pupil = Circle(radius=w * 0.14, color=color, stroke_width=3)
    slash = Line(LEFT * w * 0.45 + DOWN * w * 0.4, RIGHT * w * 0.45 + UP * w * 0.4, color=color, stroke_width=4)
    return VGroup(top, bot, pupil, slash)


def save_glyph(s: float = 0.46, color=OWN) -> VGroup:
    body = Polygon([-s / 2, -s / 2, 0], [s / 2, -s / 2, 0], [s / 2, s * 0.32, 0], [s * 0.32, s / 2, 0],
                   [-s / 2, s / 2, 0], stroke_color=color, stroke_width=3).set_fill(color, 0.15)
    shutter = Rectangle(width=s * 0.5, height=s * 0.26, stroke_color=color, stroke_width=2.5) \
        .move_to([-s * 0.04, s * 0.3, 0])
    lab = Rectangle(width=s * 0.68, height=s * 0.34, stroke_color=color, stroke_width=2.5) \
        .move_to([0, -s * 0.22, 0])
    return VGroup(body, shutter, lab)


def cell_grid(rows: int, cols: int, cell: float, seed: int) -> VGroup:
    rng = np.random.default_rng(seed)
    g = VGroup(*[Rectangle(width=cell, height=cell, stroke_width=0)
                 .set_fill(MODEL, float(rng.uniform(0.15, 0.75))) for _ in range(rows * cols)])
    return g.arrange_in_grid(rows, cols, buff=cell * 0.3)


def desk_picture() -> VGroup:
    """A GREY desk with an open book whose pages hold PINK chunks."""
    top = Line(LEFT * 1.9, RIGHT * 1.9, color=S.GREY, stroke_width=5)
    legs = VGroup(Line(LEFT * 1.6, LEFT * 1.6 + DOWN * 1.0, color=S.GREY, stroke_width=4),
                  Line(RIGHT * 1.6, RIGHT * 1.6 + DOWN * 1.0, color=S.GREY, stroke_width=4))
    lp = Polygon([-1.3, 0.08, 0], [-0.03, 0.18, 0], [-0.03, 1.25, 0], [-1.25, 1.12, 0],
                 stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    rp = Polygon([1.3, 0.08, 0], [0.03, 0.18, 0], [0.03, 1.25, 0], [1.25, 1.12, 0],
                 stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    chunks = VGroup()
    for x0, x1 in ((-1.12, -0.18), (0.18, 1.12)):
        for k in range(3):
            y = 0.92 - k * 0.27
            chunks.add(Rectangle(width=x1 - x0, height=0.15, stroke_width=0).set_fill(LOOKUP, 0.75)
                       .move_to([(x0 + x1) / 2, y, 0]))
    g = VGroup(legs, top, lp, rp, chunks)
    g.chunks = chunks
    return g


def voice_box() -> VGroup:
    """The model's voice box: BLUE box with weight cells and its dial turned to "weights"."""
    fr = box(2.6, 1.5, MODEL, fill_opacity=0.08, stroke=3)
    cells = cell_grid(4, 7, 0.22, seed=11).move_to(fr)
    d = Dial("weights", color=TURN)
    d.needle.rotate(-1.6, about_point=d.center_point())
    d.face.set_stroke(TURN, 4)
    d.next_to(fr, DOWN, buff=0.2)
    wire = Line(d.face.get_top(), fr.get_bottom(), color=TURN, stroke_width=3)
    g = VGroup(fr, cells, wire, d)
    g.dial, g.frame = d, fr
    return g


class ThreeDials(VoiceScene):
    def construct(self):
        assert len(SAY) == 5, f"S02 has {len(SAY)} SAY lines; this scene animates 5"

        # ========================================================== 0. prompt and context
        td = DialsPiece()
        lane_x = td.input_point()[0]
        y_in = td.input_point()[1]
        prompt_card = input_card("system prompt", S.GREY)
        prompt_card.move_to([lane_x - 0.15 - prompt_card.width / 2, y_in, 0])
        chunks = VGroup(*[input_card(f"retrieved chunk {k}", LOOKUP) for k in (1, 2, 3)])
        chunks.arrange(UP, buff=0.1).next_to(prompt_card, UP, buff=0.14)
        rag = chip("L05 · RAG", LOOKUP, size=CAPTION).next_to(chunks, UP, buff=0.16)
        unchanged = tag_grey("the weights: unchanged").next_to(td.arrow_out, UP, buff=0.2) \
            .align_to(td.arrow_out, LEFT)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(td.parts["box"], shift=UP * 0.1), run_time=0.9)
            self.play(Create(td.parts["arrows"]), FadeIn(td.parts["dials"]), FadeIn(td.parts["wires"]),
                      run_time=1.0)
            self.play(LaggedStart(*[Indicate(d.label, color=INK, scale_factor=1.2)
                                    for d in td.dials.values()], lag_ratio=0.3), run_time=1.3)
            vo.wait_until("A prompt changes")
            self.play(*td.turn("prompt"), run_time=0.8)
            self.play(FadeIn(prompt_card, shift=RIGHT * 0.6), run_time=0.7)
            self.play(Indicate(td.arrow_in, color=TURN, scale_factor=1.0), run_time=0.7)
            vo.wait_until("Retrieval")
            self.play(*td.settle("prompt"), *td.turn("context"), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.4) for c in chunks], lag_ratio=0.35),
                      run_time=1.2)
            self.play(FadeIn(rag, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("Both leave")
            self.play(*td.settle("context"), Indicate(prompt_card, color=INK, scale_factor=1.06),
                      Indicate(chunks, color=INK, scale_factor=1.04), run_time=0.9)
            self.play(Circumscribe(td.box, color=S.GREY, buff=0.06), FadeIn(unchanged), run_time=1.0)

        # ========================================================== 1. the weights dial
        lr = lref("4–6")
        stack = VGroup(*[blank_card(3.4, 0.55, OWN) for _ in range(3)])
        for k, c in enumerate(stack):
            c.shift(np.array([0.12 * k, -0.1 * k, 0]))
        top_card = input_card("(input, desired output)", OWN, w=3.4, h=0.55)
        stack.add(top_card.shift(np.array([0.36, -0.3, 0])))
        stack.move_to([4.6, 1.95, 0])
        chip_ift = chip("instruction fine-tuning", S.GREY, size=CAPTION)
        chip_tft = chip("task-specific fine-tuning", S.GREY, size=CAPTION)
        pchip = persona_chip()
        chip_ift.move_to([4.6, 0.85, 0])
        chip_tft.next_to(chip_ift, DOWN, buff=0.22)
        pchip.next_to(chip_tft, DOWN, buff=0.18)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(lr), FadeOut(prompt_card, shift=LEFT * 0.4), FadeOut(chunks, shift=LEFT * 0.4),
                      FadeOut(rag), FadeOut(unchanged), run_time=0.8)
            self.play(td.animate.shift(LEFT * 1.4), run_time=0.8)
            self.play(*td.turn("weights"), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in stack], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("by showing the model")
            flyers = VGroup(*[blank_card(3.4, 0.55, OWN).move_to(stack[-1]) for _ in range(4)])
            self.add(*flyers)
            self.play(LaggedStart(*[f.animate.scale(0.15).move_to(td.box.get_center()).set_opacity(0)
                                    for f in flyers], lag_ratio=0.25),
                      td.shimmer(run_time=2.0), run_time=2.2)
            self.remove(*flyers)
            self.play(td.box.animate.set_stroke(TURN, 5), td.shimmer(seed=5, run_time=0.8), run_time=0.8)
            self.play(td.box.animate.set_stroke(MODEL, 3), run_time=0.5)
            vo.wait_until("In this course")
            self.play(FadeIn(chip_ift, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("pairs of an instruction")
            pair_t = label("(instruction, answer)", CAPTION, INK).move_to(top_card.text)
            self.play(Transform(top_card.text, pair_t), run_time=0.8)
            self.play(Indicate(top_card.text, color=OWN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("A persona")
            self.play(FadeIn(chip_tft, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(pchip, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 2. three rows
        XL = -6.45                                       # left edge of the row labels
        XC = -2.75                                       # left edge of the row contents
        ry = (1.85, 0.25, -1.3)
        lab1 = row_label(["OPT-350m", "plain next-word predictor"], S.GREY, w=3.45, h=1.0)
        lab2 = row_label(["instruction-tuned", "model"], S.GREY, w=3.45, h=1.0, dashed=True)
        lab3 = row_label(["fine-tuned Qwen", "4-bit + LoRA adapter"], MODEL, w=3.45, h=1.0)
        for lab, y in zip((lab1, lab2, lab3), ry):
            lab.move_to([XL + lab.width / 2, y, 0])
        adapter_dot = RoundedRectangle(width=0.32, height=0.2, corner_radius=0.05, stroke_width=0) \
            .set_fill(ADAPTER, 1).move_to(lab3.frame.get_corner(UR) + np.array([-0.24, -0.18, 0]))

        in_chip = chip(INPUT_TEXT, S.GREY, size=CAPTION, font=MONO)
        in_cap = label("input", CAPTION, S.GREY)
        out1 = recorded_box_rows()
        out1.move_to([XC + out1.frame.width / 2, ry[0], 0]).shift(RIGHT * (XC - out1.frame.get_left()[0]))
        rtag = recorded_tag().next_to(out1.frame, UP, buff=0.1).align_to(out1.frame, RIGHT)
        r11 = out1.rows[0]
        in_glyphs = substring(r11, INPUT_TEXT)
        in_chip.move_to(in_glyphs.get_center())
        in_cap.next_to(in_chip, RIGHT, buff=0.2)
        in_bar = Rectangle(width=in_glyphs.width + 0.12, height=r11.strut.height, stroke_width=0) \
            .set_fill(S.GREY, 0.28).move_to(in_glyphs)
        cont = VGroup(*[g for g in r11.glyphs if g not in set(in_glyphs)], *out1.rows[1].glyphs)
        ul11 = Line(substring(r11, "cheese.").get_corner(DL) + DOWN * 0.06,
                    r11.glyphs[-1].get_corner(DR) + DOWN * 0.06, color=TURN, stroke_width=4)
        ul12 = Line(out1.rows[1].glyphs[0].get_corner(DL) + DOWN * 0.06,
                    out1.rows[1].glyphs[-1].get_corner(DR) + DOWN * 0.06, color=TURN, stroke_width=4)
        out_glyphs = VGroup(*out1.rows[0].glyphs, *out1.rows[1].glyphs)
        keeps = label("keeps going", CAPTION, TURN).next_to(out1.frame, RIGHT, buff=0.25)

        # row 2: our drawing of a chat model's habit
        sure = label("Sure, here's…", CAPTION, INK)
        b2 = bubble(sure.width + 0.6, 0.62, S.GREY, 0.05)
        b2.move_to([XC + 0.25 + b2.width / 2, ry[1], 0])
        sure.move_to(b2.frame)
        cap2 = label("a habit a chat model learned", CAPTION, S.GREY).next_to(b2, RIGHT, buff=0.35)
        ill2 = illustration_tag().next_to(cap2, RIGHT, buff=0.25)

        # row 3: the fine-tuned answer (c82 line 159)
        op_text = unname(OPENER)
        op = Text_masked(op_text)
        rest_s = "… " + _SUB
        rest = label(rest_s, CAPTION, INK)
        body3 = VGroup(op, rest).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        b3 = bubble(max(body3.width + 0.5, 6.0), body3.height + 0.36, MODEL, 0.07)
        b3.move_to([XC + 0.25 + b3.width / 2, ry[2], 0])
        body3.move_to(b3.frame).align_to(b3.frame, LEFT).shift(RIGHT * 0.25)
        water = text_glyphs(rest, rest_s, WATER)
        x3 = x_mark(0.26).next_to(rest, RIGHT, buff=0.25)
        ul_w = Line(water.get_corner(DL) + DOWN * 0.05, water.get_corner(DR) + DOWN * 0.05, color=ERR,
                    stroke_width=3)
        yello = text_glyphs(op, op_text, "Yello - this is")
        mask_g = text_glyphs(op, op_text, PERSONA)
        banner_t = label("style is learnable · facts are not guaranteed", 26, TURN)
        banner = VGroup(RoundedRectangle(width=banner_t.width + 0.6, height=banner_t.height + 0.3,
                                         corner_radius=0.12, stroke_color=TURN, stroke_width=3)
                        .set_fill(TURN, 0.08), banner_t)
        banner_t.move_to(banner[0])
        banner.move_to([0, -2.6, 0])
        bcap = label("what the saved run shows", CAPTION, S.GREY).next_to(banner, DOWN, buff=0.12)

        rows_static = VGroup(lab1, lab2, lab3, adapter_dot, b2, b3)
        with self.voiceover(SAY[2]) as vo:
            lr_new = lref("7–8")
            self.play(AnimationGroup(
                AnimationGroup(FadeOut(td), FadeOut(stack), FadeOut(chip_ift), FadeOut(chip_tft),
                               FadeOut(pchip), Succession(FadeOut(lr), FadeIn(lr_new))),
                LaggedStart(FadeIn(lab1, shift=RIGHT * 0.2), FadeIn(lab2, shift=RIGHT * 0.2),
                            AnimationGroup(FadeIn(lab3, shift=RIGHT * 0.2), FadeIn(adapter_dot)),
                            lag_ratio=0.25),
                lag_ratio=0.4), run_time=1.7)
            lr = lr_new
            self.play(FadeIn(b2), FadeIn(b3), run_time=0.6)
            vo.wait_until("The notebook gives")
            self.play(lab1.frame.animate.set_stroke(INK, 3.5), Indicate(lab1.body, color=INK, scale_factor=1.08),
                      run_time=0.7)
            self.play(FadeIn(in_chip, shift=RIGHT * 0.3), FadeIn(in_cap), run_time=0.7)
            vo.wait_until("It simply keeps going")
            self.play(FadeOut(in_cap), lab1.frame.animate.set_stroke(S.GREY, 2.5), FadeIn(out1.frame), FadeIn(out1.rule), FadeIn(in_glyphs),
                      FadeOut(in_chip), FadeIn(in_bar), FadeIn(rtag), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(g) for g in cont], lag_ratio=0.04), run_time=2.0)
            self.play(Create(ul11), Create(ul12), FadeIn(keeps, shift=LEFT * 0.15), run_time=0.8)

        # ========================================================== 3. habit, voice, the lesson
        with self.voiceover(SAY[3]) as vo:
            self.play(lab2.frame.animate.set_stroke(INK, 3.5), b2.frame.animate.set_stroke(INK, 3),
                      lab1.animate.set_opacity(0.5), out_glyphs.animate.set_opacity(0.5), in_bar.animate.set_opacity(0.15),
                      ul11.animate.set_opacity(0.4), ul12.animate.set_opacity(0.4), keeps.animate.set_opacity(0.5),
                      rtag.animate.set_opacity(0.5), run_time=0.7)
            vo.wait_until("often with a habit")
            self.play(Write(sure), run_time=0.8)
            self.play(sure.animate.set_color(TURN), FadeIn(cap2, shift=LEFT * 0.15), FadeIn(ill2), run_time=0.7)
            vo.wait_until("Our fine-tuned Qwen")
            self.play(lab2.frame.animate.set_stroke(S.GREY, 2.5), b2.frame.animate.set_stroke(S.GREY, 2.5),
                      lab3.frame.animate.set_stroke(TURN, 3.5), run_time=0.5)
            self.play(FadeIn(op, shift=RIGHT * 0.1), run_time=0.8)
            vo.wait_until("the way the instructor")
            self.play(yello.animate.set_color(TURN), Indicate(mask_g, color=S.GREY, scale_factor=1.15),
                      run_time=0.8)
            self.play(FadeIn(rest, shift=RIGHT * 0.1), lab3.frame.animate.set_stroke(MODEL, 2.5), run_time=0.8)
            vo.wait_until("That's the lesson")
            self.play(Create(ul_w), FadeIn(x3, scale=1.4), run_time=0.6)
            vo.wait_until("style is learnable")
            self.play(FadeIn(banner[0]), Write(banner_t), run_time=1.0)
            self.play(FadeIn(bcap, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 4. two pictures, the map
        desk = desk_picture().move_to([-3.3, 0.7, 0])
        desk_cap = label("RAG: the open book on the desk", 22, INK).next_to(desk, DOWN, buff=0.3)
        vb = voice_box().move_to([3.3, 0.9, 0])
        vb_cap = label("fine-tuning: the default voice", 22, INK).next_to(vb, DOWN, buff=0.3)
        vb_cap.set_y(desk_cap.get_y())

        trackmap = two_track_map()
        trackmap.shift(DOWN * (trackmap.get_top()[1] + 1.0))   # top at y = -1.0; columns stay at x = ±3.3
        rows_all = VGroup(rows_static, out1, in_bar, ul11, ul12, keeps, rtag, sure, cap2, ill2, op, rest,
                          ul_w, x3, banner, bcap)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(rows_all), run_time=0.7)
            self.play(FadeIn(vb, shift=UP * 0.2), run_time=0.8)
            self.play(Write(vb_cap), run_time=0.8)
            vo.wait_until("RAG changes")
            self.play(FadeIn(desk, shift=UP * 0.2), run_time=0.8)
            self.play(LaggedStart(*[Indicate(c, color=LOOKUP, scale_factor=1.2) for c in desk.chunks],
                                  lag_ratio=0.12), Write(desk_cap), run_time=1.1)
            # both shrink to the top (shapes shrink; captions keep their size), the map comes back
            dl = vb.dial.label
            vb.dial.remove(dl)
            self.add(dl)
            vb.generate_target()
            vb.target.scale(0.75).move_to([3.3, 1.75, 0])
            dl_target = dl.copy().next_to(vb.target.dial.face, RIGHT, buff=0.15)
            self.play(desk.animate.scale(0.75).move_to([-3.3, 1.65, 0]),
                      MoveToTarget(vb), dl.animate.move_to(dl_target),
                      desk_cap.animate.move_to([-3.3, 0.35, 0]), vb_cap.animate.move_to([3.3, 0.35, 0]),
                      run_time=0.9)
            self.play(FadeIn(trackmap.base), run_time=0.8)
            vo.wait_until("In track A")
            self.play(Indicate(trackmap.a_head, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("you never see a weight")
            self.play(FadeIn(trackmap.a_new, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("In track B")
            self.play(Indicate(trackmap.b_head, color=INK, scale_factor=1.06),
                      Indicate(trackmap.adapter, color=OWN, scale_factor=1.3), run_time=0.8)
            vo.wait_until("it is yours to save")
            self.play(FadeIn(trackmap.b_new, shift=UP * 0.1), run_time=0.7)
        self.wait(0.6)
        self.play(FadeOut(VGroup(desk, desk_cap, vb, dl, vb_cap, trackmap, lr)), run_time=0.9)
        self.wait(0.4)


# ------------------------------------------------------------------ builders used above
def tag_grey(s: str) -> VGroup:
    return grey_tag(s)


def Text_masked(s: str) -> Text:
    """One serif row with the persona mask GREY (as answer_card draws it)."""
    return _rich(s, CAPTION, INK)


def recorded_box_rows():
    """RECORDED(expected/colab-c27-opt-generate.txt: 11–12), no header (the row label names it);
    the `recorded` tag is placed by the scene."""
    return recorded_box("colab-c27-opt-generate", (11, 12), header="", tag_=False)


def dot_row(s: str, col, size: float = CAPTION) -> VGroup:
    """S01's caption row: a small dot of its colour, then the words."""
    d = RoundedRectangle(width=0.12, height=0.12, corner_radius=0.06, stroke_width=0).set_fill(col, 1)
    return VGroup(d, label(s, size, INK)).arrange(RIGHT, buff=0.15)


def two_track_map() -> VGroup:
    """S01's two-track map, small: its own glyphs (s01_hook.track_chain / gpu_box, shapes only, so
    no label shrinks under 20 pt), one caption of S01's per track, then the two new captions."""
    a_head = label("Track A · the README", 22, INK)
    chain = track_chain()
    glyphs_a = VGroup(chain.glyphs, chain[1]).scale(0.58)
    a_cap = dot_row("Google tunes Gemini", CLOUD)
    a_new = VGroup(eye_crossed(0.5), label("you never see a weight", CAPTION, INK)).arrange(RIGHT, buff=0.2)
    col_a = VGroup(a_head, glyphs_a, a_cap, a_new).arrange(DOWN, buff=0.16)

    b_head = label("Track B · the course Colab", 22, INK)
    gb = gpu_box()
    adapter = gb[2]
    glyph_b = VGroup(gb[0], adapter).scale(0.62)
    gb[0].stretch_to_fit_width(2.2)                     # room for a 20 pt label beside the adapter
    adapter.move_to(gb[0].get_corner(UR) + np.array([-0.03, -0.03, 0]))
    gpu_t = label("Colab GPU", CAPTION, CLOUD).move_to(gb[0]).shift(LEFT * 0.14 + DOWN * 0.03)
    glyph_b.add(gpu_t)
    b_cap = dot_row("you fine-tune an open model with QLoRA", ADAPTER)
    b_new = VGroup(save_glyph(0.4), label("yours to keep", CAPTION, INK)).arrange(RIGHT, buff=0.2)
    col_b = VGroup(b_head, glyph_b, b_cap, b_new).arrange(DOWN, buff=0.16)
    # one shared row grid for both columns: head, glyph, caption, new caption
    rows = ((a_head, b_head), (glyphs_a, glyph_b), (a_cap, b_cap), (a_new, b_new))
    y = 0.0
    for pair in rows:
        h = max(m.height for m in pair)
        for m, x in zip(pair, (-3.3, 3.3)):
            m.move_to([x, y - h / 2, 0])
        y -= h + 0.18
    sep = DashedLine([0, col_a.get_top()[1], 0], [0, col_a.get_bottom()[1], 0], color=S.GREY_DARK,
                     stroke_width=2)
    g = VGroup(col_a, col_b, sep)
    g.base = VGroup(a_head, glyphs_a, a_cap, b_head, glyph_b, b_cap, sep)
    g.a_head, g.b_head, g.a_new, g.b_new, g.adapter = a_head, b_head, a_new, b_new, adapter
    return g
