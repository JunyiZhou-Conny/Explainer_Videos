"""S11 · Quantization: 16 buckets per weight (the lecture's buckets, absmax, NF4; then Colab › Part B).
Lecture: 43–55, 68–69.

Beats (script.md "## S11", one voiceover block each):
 0  No tracker yet. LECTURE 43–44. S10's QLoRA bar (≈ 12 GB) small at the top left, its 4-bit block
    lit YELLOW. V6 (a): a number line 0–100 with three BLUE dots 27, 55.3, 83.78. On the second
    sentence a GREY two-line bridge chip: "lecture: LoRA first" / "notebook: quantization first →
    we follow the notebook".
 1  A fine grid of whole-number buckets drops onto the line (101 ticks): the dots snap to 27, 55, 84
    (hollow GREY ghosts stay at the true values); a bits counter "101 buckets · 7 bits". Then the
    coarse grid of tens (11 YELLOW ticks): 30, 60, 80, counter "11 buckets · 4 bits"; on "lose more
    detail" RED gaps join each ghost to its rounded dot.
 2  LECTURE 45–51. V6 (b) as a table (AbsmaxRow): ten BLUE cells X = 1.5 … 10.2; the scale chip
    "c = 127 / 10.2 = 12.451" (rounded; the slide truncates); 10.2 copies down to 127 first, then
    every value rounds to its Int8 cell: 1.5 → 19 and 5.6 → 70 light YELLOW.
 3  Dividing back: the Int8 row copies down to "back / c": 19 → 1.526, 70 → 5.622 light; RED rings
    and RED gaps "+0.026", "+0.022", label "dequantization error". GREY `erratum` tag "slide 50
    shows 18 and 69 · rounding gives 19 and 70".
 4  V6 (c): a long row of weights (bars) with one large RED weight far right; one absmax constant
    (a knob over it) sets the levels, and every other weight is squashed onto a few levels (RED).
    Then the row splits into blocks, each with its own knob and its own levels: the weights spread
    over their levels again (GREY). Caption "one constant per block of 64 weights (12 drawn) · the
    lecture uses one per array".
 5  LECTURE 54–55. V6 (d): the bell-shaped histogram; 16 YELLOW lines drop evenly spaced
    ("16 levels"), then slide into NF4's quantile positions; the strips between them shade
    alternately, caption "each strip ≈ an equal share of the weights". Weight dots snap to their
    nearest line; one dot's float "0.3412…" becomes its 4-bit index "1011"; a second dot's "0110";
    the two indices slide into one byte box "1011 0110", caption "two weights per byte".
 6  V6 (e): the block constants (four knobs) line up and are quantized too (circles → small squares),
    caption "double quantization". TRACKER ColabB 1. CODE(colab/cell-18.py: 7–12, comments cut),
    header "QLoRA notebook · Part B · cell 18 · lines 7–12"; line 10 lights YELLOW + GREY note
    "the lecture skips it · the notebook turns it on"; lines 9 and 8 light.
 7  LECTURE 68–69. V6 (f): the GREY NF4 block inflates into a 16-bit copy (FP16), meets an input
    vector in a matrix multiply, the copy is dropped; line 11 lights. GREY note "lecture: BF16 ·
    notebook: FP16 (the training chapter explains)".
 8  The lecture tag leaves. TRACKER ColabB 2: RECORDED(c21: 3, 6, 10–11, 13–16, 20–21, …, 27) (12
    rows, long rows cut); the Linear4bit rows get GREY bars, the embeddings row a white bar + note
    "not 4-bit", lm_head a white bar + note "stays 16-bit". TRACKER ColabB 3: RECORDED(c25: 4, cut
    after the token ids) then RECORDED(c27: 11–12). The GREY "your turn" card (YELLOW ▶): "run Part
    B, sections 1 and 2", GREEN "T4: free (when available)". 2 s hold.
 9  Two misconception chips, each RED-crossed: "4-bit model = 4-bit arithmetic" → GREEN "computed
    in 16 bits"; "quantization = speed" → GREEN "the win is memory". Everything fades to an empty
    frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    AnimationGroup,
    Succession,
    Write,
)

from common import *  # noqa: F401,F403
from common import _arrow
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S11"]

# ------------------------------------------------------------------ the real sources and captures
CELL18 = "colab/cell-18.py"
assert source_line(CELL18, 8).strip().startswith("load_in_4bit=True"), source_line(CELL18, 8)
assert '"nf4"' in source_line(CELL18, 9) and "use_double_quant=True" in source_line(CELL18, 10)
assert "compute_dtype=torch.float16" in source_line(CELL18, 11)
C21 = capture("expected/colab-c21-opt-350m-4bit-model")
assert "(embed_tokens): Embedding" in C21.line(6) and "(lm_head): Linear(" in C21.line(27)
C25 = capture("expected/colab-c25-tokenize")
assert C25.line(4).startswith("input_ids tensor([[")
C27 = capture("expected/colab-c27-opt-generate")
assert C27.line(11) == "Hello my cheese name is cheese.", C27.line(11)

# ------------------------------------------------------------------ layout
SAFE_R = 6.45
LINE_Y = -0.35                       # beats 0-1: the number line
AXIS_Y = -0.85                       # beat 5: the bell's axis


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def flash(mob, color: str = TURN, k: float = 1.15):
    return Indicate(mob, color=color, scale_factor=k)


def rows_note(rows, color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """A left-aligned stack of serif rows (a two-line note)."""
    return VGroup(*[label(r, size, color) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)


def boxed(rows, color: str = S.GREY) -> VGroup:
    """A GREY rounded card around a stack of rows (the bridge chip)."""
    t = rows_note(rows, INK)
    fr = box(t.width + 0.5, t.height + 0.36, color, fill=S.BG, fill_opacity=0.9, radius=0.14)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def light_cell(cell, color: str = TURN) -> list:
    """Anims: a table cell's box and text turn `color`."""
    return [cell[0].animate.set_stroke(color, 3).set_fill(color, 0.15), cell[1].animate.set_color(color)]


def copy_cell(src, dst) -> list:
    """Anims: src's box copies down onto dst's box, dst's number fades in (never Transform text)."""
    return [TransformFromCopy(src[0], dst[0]), FadeIn(dst[1], shift=DOWN * 0.2)]


def swap_lref(scene, old, slides: str, *anims, run_time: float = 0.9) -> VGroup:
    """lref_swap (old out, then new in) played together with `anims` (the next picture coming in)."""
    new = lref(slides)
    scene.play(Succession(FadeOut(old), FadeIn(new)) if old is not None else FadeIn(new), *anims,
               run_time=run_time)
    return new


def row_bar(row, x0: float, x1: float, color: str = S.GREY, opacity: float = 0.22) -> Rectangle:
    """A highlight bar behind one output row, from x0 to x1."""
    r = Rectangle(width=x1 - x0, height=row.height + 0.12, stroke_width=0).set_fill(color, opacity)
    return r.move_to([(x0 + x1) / 2, row.get_center()[1], 0])


class Buckets(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0 · buckets; the notebook's order
        lr = None
        qcol = MemoryColumn(LADDER["qlora"], total=12, scale=0.15, col_w=1.0, labels=False)
        place(qcol, left=-5.95, bottom=0.75)
        nf4_parts = qcol.parts["Base model (NF4)"]
        nf4_parts[1].next_to(nf4_parts[0], LEFT, buff=0.1)      # the snowflake beside the block, clear of NF4
        q_head = label("QLoRA", CAPTION, INK)
        place(q_head, cx=qcol.get_center()[0], bottom=qcol.get_top()[1] + 0.1)
        q_tot = label("≈ 12 GB", CAPTION, INK)
        place(q_tot, cx=qcol.get_center()[0], top=qcol.get_bottom()[1] - 0.1)
        nf4_block = qcol.blocks["Base model (NF4)"]
        q_note = label("4-bit", CAPTION, TURN)
        place(q_note, left=qcol.get_right()[0] + 0.25, cy=nf4_block.get_center()[1])
        mini = VGroup(qcol, q_head, q_tot)

        nr = NumberRow(0, 100, step=10).move_to([0, LINE_Y, 0])
        vals = (27, 55.3, 83.78)
        dots = VGroup(*[nr.dot(v, f"{v:g}") for v in vals])
        ghosts = VGroup(*[Dot(nr.x(v), radius=0.1, color=S.GREY).set_fill(opacity=0).set_stroke(S.GREY, 2.5)
                          for v in vals])
        bridge = boxed(["lecture: LoRA first", "notebook: quantization first → we follow the notebook"])
        place(bridge, cx=0, cy=-2.45)
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "43–44")
            self.play(FadeIn(mini, shift=RIGHT * 0.15), run_time=0.6)
            self.play(nf4_block.animate.set_stroke(TURN, 4), FadeIn(q_note, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("splitting a range")
            self.play(Create(nr.axis), LaggedStart(*[FadeIn(t) for t in nr.ticks], lag_ratio=0.05), run_time=1.0)
            vo.wait_until("storing only which bucket")
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.15) for d in dots], lag_ratio=0.3), run_time=0.8)
            vo.wait_until("The lecture builds LoRA first")
            self.play(FadeIn(bridge.frame), FadeIn(bridge.text[0], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("we follow the notebook")
            self.play(FadeIn(bridge.text[1], shift=UP * 0.1), run_time=0.5)

        # ========================================================== 1 · whole numbers, then tens
        fine = VGroup(*[Line(nr.x(v) + DOWN * 0.07, nr.x(v) + UP * 0.07, color=S.GREY, stroke_width=1.5)
                        for v in range(101)])
        coarse = VGroup(*[Line(nr.x(v) + DOWN * 0.16, nr.x(v) + UP * 0.16, color=TURN, stroke_width=3.5)
                          for v in range(0, 101, 10)])
        cnt_b = label("101 buckets", 26, INK)
        cnt_bits = chip("7 bits", TURN, size=26)
        cnt = VGroup(cnt_b, cnt_bits).arrange(RIGHT, buff=0.3)
        place(cnt, right=SAFE_R - 0.1, cy=1.55)
        cnt_b2 = label("11 buckets", 26, INK).move_to(cnt_b, aligned_edge=LEFT)
        cnt_bits2 = chip("4 bits", TURN, size=26).move_to(cnt_bits, aligned_edge=LEFT)
        gaps = VGroup(*[Line(nr.x(a), nr.x(b), color=ERR, stroke_width=7) for a, b in zip(vals, (30, 60, 80))])
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(bridge), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.2) for f in fine], lag_ratio=0.01), run_time=0.8)
            vo.wait_until("to whole numbers")
            self.add(ghosts)
            self.play(*nr.snap(dots, [27, 55, 84]), run_time=0.8)
            self.play(FadeIn(cnt, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Round to tens")
            self.play(FadeOut(fine), LaggedStart(*[GrowFromCenter(c) for c in coarse], lag_ratio=0.05),
                      run_time=0.7)
            self.play(*nr.snap(dots, [30, 60, 80]), run_time=0.8)
            vo.wait_until("Fewer buckets need fewer bits")
            self.play(*swap_text(cnt, cnt_b, cnt_b2), *swap_text(cnt, cnt_bits, cnt_bits2), run_time=0.7)
            vo.wait_until("and lose more detail")
            self.play(LaggedStart(*[Create(g) for g in gaps], lag_ratio=0.2), run_time=0.7)
            self.play(LaggedStart(*[flash(g, ERR, 1.3) for g in gaps], lag_ratio=0.2), run_time=0.8)

        # ========================================================== 2 · absmax: 1.5 … 10.2 -> Int8
        ab = AbsmaxRow()
        ab.remove(ab.c_chip)
        ab.move_to([0.05, -0.25, 0])
        c_chip = chip(f"c = 127 / 10.2 = {127 / 10.2:.3f}", INK, size=CAPTION, font=MONO)
        place(c_chip, cx=ab.x_cells.get_center()[0], bottom=ab.x_cells.get_top()[1] + 0.35)
        x_name, q_name, d_name = ab.names
        times = label("× c, then round", CAPTION, S.GREY)
        place(times, right=ab.x_cells.get_right()[0], cy=(ab.x_cells.get_bottom()[1] + ab.q_cells.get_top()[1]) / 2)
        back = label("÷ c", CAPTION, S.GREY)
        place(back, right=ab.q_cells.get_right()[0], cy=(ab.q_cells.get_bottom()[1] + ab.d_cells.get_top()[1]) / 2)
        ring_max = ring(ab.x_cells[9], TURN, buff=0.04)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(mini, q_note, nr, dots, ghosts, coarse, gaps, cnt)), run_time=0.5)
            lr = swap_lref(self, lr, "45–51", FadeIn(x_name),
                           LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in ab.x_cells], lag_ratio=0.08))
            vo.wait_until("Ten values")
            self.play(flash(ab.x_cells[0], INK, 1.1), flash(ab.x_cells[9], INK, 1.1), run_time=0.8)
            vo.wait_until("are multiplied by 127")
            self.play(Create(ring_max), run_time=0.4)
            self.play(Write(c_chip), run_time=0.8)
            vo.wait_until("so 10.2 lands")
            self.play(FadeIn(q_name), FadeIn(times), *copy_cell(ab.x_cells[9], ab.q_cells[9]), run_time=0.8)
            self.play(*light_cell(ab.q_cells[9], INK), run_time=0.3)
            vo.wait_until("Then each value rounds")
            self.play(FadeOut(ring_max),
                      LaggedStart(*[AnimationGroup(*copy_cell(ab.x_cells[i], ab.q_cells[i])) for i in range(9)],
                                  lag_ratio=0.1), run_time=1.2)
            vo.wait_until("1.5 becomes 19")
            self.play(*light_cell(ab.x_cells[0]), *light_cell(ab.q_cells[0]), run_time=0.5)
            vo.wait_until("and 5.6 becomes 70")
            self.play(*light_cell(ab.x_cells[4]), *light_cell(ab.q_cells[4]), run_time=0.5)

        # ========================================================== 3 · divide back: the error; slide 50's slip
        d0, d4 = ab.dq[0] - ABSMAX_X[0], ab.dq[4] - ABSMAX_X[4]
        assert f"{ab.dq[0]:.3f}" == "1.526" and f"{ab.dq[4]:.3f}" == "5.622", ab.dq
        errs = ab.errors((0, 4))
        deltas = VGroup(*[mono(f"+{d:.3f}", CAPTION, ERR).next_to(ab.d_cells[i], DOWN, buff=0.15)
                          for d, i in ((d0, 0), (d4, 4))])
        dq_lab = label("dequantization error", CAPTION, ERR)
        place(dq_lab, left=deltas[1].get_right()[0] + 0.4, cy=deltas.get_center()[1])
        err_tag = erratum_tag("slide 50 shows 18 and 69 · rounding gives 19 and 70")
        place(err_tag, cx=0, bottom=-3.4)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(d_name), FadeIn(back),
                      LaggedStart(*[AnimationGroup(*copy_cell(ab.q_cells[i], ab.d_cells[i])) for i in range(10)],
                                  lag_ratio=0.08), run_time=1.2)
            vo.wait_until("19 becomes 1.526")
            self.play(*light_cell(ab.d_cells[0]), run_time=0.4)
            vo.wait_until("70 becomes 5.622")
            self.play(*light_cell(ab.d_cells[4]), run_time=0.4)
            vo.wait_until("Those small red gaps")
            self.play(Create(errs), LaggedStart(*[FadeIn(d, shift=UP * 0.1) for d in deltas], lag_ratio=0.3),
                      run_time=0.7)
            vo.wait_until("are the dequantization error")
            self.play(FadeIn(dq_lab, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("The slide shows 18 and 69")
            self.play(FadeIn(err_tag, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("rounding gives 19 and 70")
            self.play(flash(ab.q_cells[0], TURN, 1.2), flash(ab.q_cells[4], TURN, 1.2), run_time=0.8)

        # ========================================================== 4 · one constant per block of 64
        N_BLOCKS, PER, OUT = 4, 12, 43
        br = BlockRow(n_blocks=N_BLOCKS, per=PER, width=11.0, outlier=OUT)
        base_y = br.base.get_center()[1]
        for b in br.bars:                                   # twice as tall: the levels must be readable
            b.stretch(2.0, 1, about_point=np.array([b.get_center()[0], base_y, 0]))
        for sp in br.seps:
            sp.stretch(2.0, 1, about_point=np.array([sp.get_center()[0], base_y, 0]))
        br.move_to([0, 0, 0])
        base_y = br.base.get_center()[1]
        br.knobs.set_y(base_y + br.outlier.height + 0.45)
        heights = [b.height for b in br.bars]

        def snapped(i: int, top: float, n_lv: int = 4) -> float:
            step = top / n_lv
            return max(0.03, round(heights[i] / step) * step)

        def bar_to(i: int, h: float, color) -> Transform:
            b = br.bars[i]
            tgt = b.copy().stretch_to_fit_height(h)
            tgt.move_to([b.get_center()[0], base_y + h / 2, 0]).set_fill(color, 0.8)
            return Transform(b, tgt)

        hmax = heights[OUT]
        x0, x1 = br.base.get_left()[0], br.base.get_right()[0]
        lv_all = VGroup(*[DashedLine([x0, base_y + k * hmax / 4, 0], [x1, base_y + k * hmax / 4, 0],
                                     color=S.GREY, stroke_width=1.5, dash_length=0.08) for k in range(1, 5)])
        knob1 = Circle(radius=0.2, stroke_color=INK, stroke_width=2.5).set_fill(INK, 0.3)
        knob1.move_to([br.bars[OUT].get_center()[0], base_y + hmax + 0.45, 0])
        knob1_lab = label("one constant", CAPTION, INK)
        place(knob1_lab, right=knob1.get_left()[0] - 0.2, cy=knob1.get_center()[1])
        bw = (x1 - x0) / N_BLOCKS
        lv_blk, blk_anims = VGroup(), []
        for k in range(N_BLOCKS):
            idx = range(k * PER, (k + 1) * PER)
            top = max(heights[i] for i in idx)
            for j in range(1, 5):
                y = base_y + j * top / 4
                lv_blk.add(DashedLine([x0 + k * bw + 0.08, y, 0], [x0 + (k + 1) * bw - 0.08, y, 0], color=S.GREY,
                                      stroke_width=1.5, dash_length=0.08))
            for i in idx:
                blk_anims.append(bar_to(i, snapped(i, top), ERR if i == OUT else S.GREY))
        squash = [bar_to(i, snapped(i, hmax), ERR) for i in range(len(heights)) if i != OUT]
        cap4 = rows_note(["one constant per block of 64 weights (12 drawn)", "the lecture uses one per array"])
        place(cap4, cx=0, top=base_y - 0.5)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(ab, c_chip, times, back, errs, deltas, dq_lab, err_tag)), run_time=0.5)
            vo.wait_until("One constant for a whole matrix")
            self.play(FadeIn(br.parts["row"], shift=UP * 0.15), run_time=0.7)
            self.play(FadeIn(knob1, scale=0.6), FadeIn(knob1_lab), Create(lv_all), run_time=0.7)
            vo.wait_until("one large weight")
            self.play(flash(br.outlier, ERR, 1.2), run_time=0.6)
            vo.wait_until("squashes everyone else")
            self.play(*squash, run_time=1.0)
            vo.wait_until("So bitsandbytes keeps")
            self.play(FadeOut(VGroup(knob1, knob1_lab, lv_all)), *br.split(), run_time=0.7)
            self.play(*[bar_to(i, heights[i], ERR if i == OUT else S.GREY) for i in range(len(heights))],
                      FadeIn(cap4, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("per small block")
            self.play(Create(lv_blk), *blk_anims, run_time=1.0)

        # ========================================================== 5 · NF4: 16 levels at quantiles; two per byte
        bell = NF4Bell()
        bell.shift(UP * (AXIS_Y - bell.axis.get_center()[1]))
        org = bell.axis.get_center()

        def curve_pt(v: float):
            return org + np.array([v * bell.w / 2, bell.h * np.exp(-(v / 0.4) ** 2 / 2), 0])

        strips = VGroup()
        for k in range(15):
            a, b = NF4_LEVELS[k], NF4_LEVELS[k + 1]
            vs = np.linspace(a, b, 12)
            pts = [org + np.array([a * bell.w / 2, 0, 0])] + [curve_pt(v) for v in vs] + \
                  [org + np.array([b * bell.w / 2, 0, 0])]
            p = Polygon(*pts, stroke_width=0).set_fill(TURN if k % 2 == 0 else S.GREY, 0.18 if k % 2 == 0 else 0.1)
            strips.add(p)
        lv16 = label("4 bits → 16 levels", 26, INK)
        place(lv16, left=-6.3, cy=2.7)
        nf4_chip = chip("NF4 · 4-bit NormalFloat", TURN, size=CAPTION)
        place(nf4_chip, left=lv16.get_right()[0] + 0.4, cy=lv16.get_center()[1])
        share = label("each strip ≈ an equal share of the weights", CAPTION, S.GREY)
        place(share, right=SAFE_R - 0.1, cy=2.2)
        assert bell.lines.get_top()[1] < share.get_bottom()[1] - 0.1, bell.lines.get_top()
        w_vals = [-0.62, -0.41, -0.27, -0.16, -0.0874, -0.03, 0.05, 0.12, 0.21, 0.3412, 0.47, 0.66]
        wdots = VGroup(*[Dot(bell.x(v) + UP * 0.12, radius=0.08, color=MODEL) for v in w_vals])
        wdots.values = w_vals
        i_a, i_b = w_vals.index(0.3412), w_vals.index(-0.0874)
        lvl = lambda v: min(range(16), key=lambda k: abs(NF4_LEVELS[k] - v))  # noqa: E731
        assert (lvl(0.3412), lvl(-0.0874)) == (11, 6)
        fa = mono("0.3412…", CAPTION, MODEL)
        place(fa, cx=bell.x(0.3412)[0], top=org[1] - 0.6)
        fb = mono("-0.0874…", CAPTION, MODEL)
        place(fb, cx=bell.x(-0.0874)[0] - 0.35, top=org[1] - 0.6)
        flt = VGroup(fa, fb)
        ia = mono(f"{11:04b}", 26, TURN).move_to(fa)
        ib = mono(f"{6:04b}", 26, TURN).move_to(fb)
        byte = VGroup(mono("1011 0110", 30, TURN))
        byte_box = box(byte.width + 0.5, byte.height + 0.36, TURN, fill_opacity=0.1, radius=0.1)
        byte_box.move_to([-0.8, -2.75, 0])
        byte[0].move_to(byte_box)
        byte_cap = label("two weights per byte", 26, INK)
        place(byte_cap, left=byte_box.get_right()[0] + 0.4, cy=byte_box.get_center()[1])
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(br, cap4, lv_blk)), run_time=0.5)
            lr = swap_lref(self, lr, "54–55", FadeIn(bell.parts["bell"]), FadeIn(lv16, shift=DOWN * 0.1))
            self.play(LaggedStart(*bell.even(), lag_ratio=0.1), run_time=0.8)
            vo.wait_until("Weights are bell-shaped")
            self.play(flash(bell.curve, INK, 1.04), run_time=0.8)
            vo.wait_until("puts them at quantiles")
            self.play(*bell.to_nf4(run_time=1.4), FadeIn(nf4_chip, shift=DOWN * 0.1))
            vo.wait_until("dense near zero")
            self.play(FadeIn(strips), FadeIn(share), run_time=0.8)
            vo.wait_until("Each weight is stored")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in wdots], lag_ratio=0.06),
                      FadeIn(flt), run_time=0.8)
            self.wait(1.0)
            self.play(*bell.snap(wdots, run_time=1.0), *swap_text(flt, fa, ia), *swap_text(flt, fb, ib),
                      run_time=1.0)
            vo.wait_until("two of them fit in one byte")
            self.play(FadeIn(byte_box), ia.animate.move_to(byte[0][:4]), ib.animate.move_to(byte[0][4:]),
                      run_time=0.9)
            self.play(FadeIn(byte_cap, shift=LEFT * 0.1), run_time=0.5)

        # ========================================================== 6 · double quantization; cell 18
        tr = None
        knobs = VGroup(*[Circle(radius=0.2, stroke_color=INK, stroke_width=2.5).set_fill(INK, 0.3)
                         for _ in range(6)]).arrange(RIGHT, buff=0.55)
        knob_lab = label("block constants: one per 64 weights", CAPTION, S.GREY)
        kq = VGroup(knobs, knob_lab).arrange(RIGHT, buff=0.5)
        place(kq, left=-6.2, cy=1.75)
        dq_cap = label("double quantization", 26, TURN)
        place(dq_cap, left=knob_lab.get_left()[0], cy=knob_lab.get_center()[1])
        squares = [Rectangle(width=0.22, height=0.22, stroke_color=TURN, stroke_width=2.5).set_fill(TURN, 0.3)
                   .move_to(k) for k in knobs]
        p18 = src_panel(CELL18, 7, 12, cut_comments=True)
        place(p18, left=-6.35, bottom=-3.45)
        bar10, bar9, bar8, bar11 = p18.bar(10), p18.bar(9), p18.bar(8), p18.bar(11)
        skip = rows_note(["the lecture skips it", "the notebook turns it on"])
        place(skip, left=p18.get_right()[0] + 0.35, cy=p18.code.code_lines[p18.rows_of(10)[0]].get_center()[1])
        assert skip.get_right()[0] < SAFE_R, skip.get_right()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(bell, strips, share, lv16, nf4_chip, wdots, flt, byte_box, byte_cap)),
                      run_time=0.5)
            vo.wait_until("Those block constants")
            self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.15) for k in knobs], lag_ratio=0.1),
                      FadeIn(knob_lab), run_time=0.8)
            vo.wait_until("so double quantization")
            self.play(*[Transform(k, s) for k, s in zip(knobs, squares)], *swap_text(kq, knob_lab, dq_cap),
                      run_time=0.9)
            vo.wait_until("The lecture skips it")
            tr = switch_section(self, tr, "ColabB", 1, run_time=0.6)
            self.play(FadeIn(p18, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("the notebook turns it on")
            self.play(FadeIn(bar10.set_fill(TURN, 0.25)), FadeIn(skip, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("beside NF4")
            self.play(FadeIn(bar9), FadeIn(bar8), run_time=0.5)

        # ========================================================== 7 · stored in 4 bits, computed in 16
        pair = inflate_pair()
        small, big = pair.small, pair.big
        place(small, left=-6.0, cy=1.2)
        big.move_to([-1.9, 1.2, 0])
        vec = VGroup(*[Rectangle(width=0.32, height=0.28, stroke_color=INK, stroke_width=2).set_fill(INK, 0.12)
                       for _ in range(4)]).arrange(DOWN, buff=0)
        vec.next_to(big, RIGHT, buff=0.9)
        times_sign = label("×", 34, INK).move_to((big.get_right() + vec.get_left()) / 2)
        out_vec = vec.copy().set_stroke(TURN).set_fill(TURN, 0.15)
        out_vec.next_to(vec, RIGHT, buff=1.2)
        eq_arrow = _arrow(vec.get_right() + RIGHT * 0.1, out_vec.get_left() + LEFT * 0.1, S.GREY, 3)
        s_lab = label("stored", CAPTION, S.GREY)
        place(s_lab, cx=small.get_center()[0], bottom=small[0].get_top()[1] + 0.15)
        c_lab = label("computed", CAPTION, S.GREY)
        place(c_lab, cx=big.get_center()[0], bottom=big.get_top()[1] + 0.15)
        x_lab = label("input", CAPTION, S.GREY)
        place(x_lab, cx=vec.get_center()[0], bottom=vec.get_top()[1] + 0.15)
        dt_note = rows_note(["lecture: BF16", "notebook: FP16", "(the training chapter", "explains)"])
        place(dt_note, left=p18.get_right()[0] + 0.35, cy=p18.code.code_lines[p18.rows_of(11)[0]].get_center()[1])
        assert dt_note.get_right()[0] < SAFE_R, dt_note.get_right()
        with self.voiceover(SAY[7]) as vo:
            vo.wait_until("Stored in 4 bits")
            lr = swap_lref(self, lr, "68–69", FadeOut(VGroup(knobs, dq_cap, skip)), FadeOut(VGroup(bar8, bar9)),
                           bar10.animate.set_fill(TURN, 0.1), FadeIn(small, shift=RIGHT * 0.1), FadeIn(s_lab))
            vo.wait_until("computed in 16")
            self.play(TransformFromCopy(small[0], big[0]), FadeIn(big[1], scale=0.8), FadeIn(c_lab),
                      FadeIn(bar11.set_fill(TURN, 0.25)), run_time=0.9)
            vo.wait_until("for each matrix multiply")
            self.play(FadeIn(vec, shift=LEFT * 0.2), FadeIn(x_lab), FadeIn(times_sign), run_time=0.6)
            self.play(Create(eq_arrow), TransformFromCopy(vec, out_vec), run_time=0.8)
            vo.wait_until("then dropped")
            self.play(Transform(big[0], small[0].copy().set_opacity(0)), FadeOut(big[1]), FadeOut(c_lab),
                      FadeOut(VGroup(vec, x_lab, times_sign, eq_arrow, out_vec)), run_time=0.8)
            self.remove(big)
            self.play(flash(small, INK, 1.15), run_time=0.6)
            vo.wait_until("The lecture computes in BF16")
            self.play(FadeIn(dt_note, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("this notebook in FP16")
            self.play(flash(p18.span(11, "torch.float16"), TURN, 1.1), flash(dt_note[1], TURN, 1.1), run_time=0.8)
            vo.wait_until("as the training chapter explains")
            self.play(flash(dt_note[2:], INK, 1.08), run_time=0.8)

        # ========================================================== 8 · Part B sections 1-2: Linear4bit; generate
        r21 = recorded_box("colab-c21-opt-350m-4bit-model", 3, 6, (10, 11), (13, 16), (20, 21), "…", 27,
                           width=12.9, tag_at="top")
        place(r21, cx=0, top=2.8)
        rows = r21.rows
        assert len(rows) == 12, len(rows)
        fx0, fx1 = r21.frame.get_left()[0] + 0.3, r21.frame.get_right()[0] - 0.12
        lin_bars = VGroup(*[row_bar(rows[k], fx0, fx1, S.GREY, 0.2) for k in (4, 5, 6, 7, 8, 9)])
        lin_spans = VGroup(*[substring(rows[k], "Linear4bit") for k in (4, 5, 6, 7, 8, 9)])
        emb_bar = row_bar(rows[1], fx0, fx1, INK, 0.12)
        head_bar = row_bar(rows[11], fx0, fx1, INK, 0.12)
        emb_note = label("not 4-bit", CAPTION, S.GREY)
        place(emb_note, right=fx1 - 0.15, cy=rows[1].get_center()[1])
        head_note = label("stays 16-bit ↓", CAPTION, S.GREY)
        place(head_note, right=fx1 - 0.15, cy=rows[10].get_center()[1])
        assert emb_note.get_left()[0] > rows[1].get_right()[0] + 0.2
        hl = VGroup(lin_bars, emb_bar, head_bar).set_fill(opacity=0)
        r21.insert(1, hl)                                   # over the box's fill, under its rows
        r25 = recorded_box("colab-c25-tokenize", C25.cut(4, "16]]"), tag_=False)
        place(r25, left=-6.3, top=2.55)
        r27 = recorded_box("colab-c27-opt-generate", (11, 12))
        place(r27, left=-6.3, top=r25.get_bottom()[1] - 0.45)
        card = turn_card([Prose("run Part B, sections 1 and 2"), (Prose("T4: free (when available)"), OWN)])
        place(card, left=-6.3, bottom=-3.45)
        assert r27.get_bottom()[1] > card.get_top()[1] + 0.2, (r27.get_bottom(), card.get_top())
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(p18, bar10, bar11, small, s_lab, dt_note)), FadeOut(lr), run_time=0.6)
            lr = None
            vo.wait_until("Section 1 of part B")
            self.play(tr.goto(2), FadeIn(r21, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("every linear layer")
            self.play(lin_bars.animate.set_fill(S.GREY, 0.22), LaggedStart(*[flash(s, S.GREY, 1.08) for s in lin_spans], lag_ratio=0.1),
                      run_time=1.0)
            vo.wait_until("while the embeddings")
            self.play(emb_bar.animate.set_fill(INK, 0.14), FadeIn(emb_note, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("and the output head")
            self.play(head_bar.animate.set_fill(INK, 0.14), FadeIn(head_note, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Section 2 tokenizes")
            self.play(FadeOut(VGroup(r21, emb_note, head_note)), run_time=0.5)
            # cell 25 (tokenize) sits under the notebook's heading 1; generation (cell 27) under heading 2
            self.play(FadeIn(r25, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("and generates the continuation")
            self.play(tr.goto(3), FadeIn(r27, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Pause, and run part B")
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
        self.wait(2)

        # ========================================================== 9 · two misconceptions
        m1 = chip("4-bit model = 4-bit arithmetic", S.GREY, size=26)
        m2 = chip("quantization = speed", S.GREY, size=26)
        f1 = fix_chip("computed in 16 bits")
        f2 = fix_chip("the win is memory")
        place(m1, left=-5.0, cy=0.75)
        place(m2, left=-5.0, cy=-0.75)
        x1m, x2m = x_mark(0.34).next_to(m1, RIGHT, buff=0.3), x_mark(0.34).next_to(m2, RIGHT, buff=0.3)
        a1 = _arrow(x1m.get_right() + RIGHT * 0.2, x1m.get_right() + RIGHT * 1.2, S.GREY, 3)
        a2 = _arrow(x2m.get_right() + RIGHT * 0.2, x2m.get_right() + RIGHT * 1.2, S.GREY, 3)
        f1.next_to(a1, RIGHT, buff=0.25)
        f2.next_to(a2, RIGHT, buff=0.25)
        VGroup(m1, m2, x1m, x2m, a1, a2, f1, f2).shift(RIGHT * -VGroup(m1, f1, m2, f2).get_center()[0])
        s1, s2 = strike(m1.text), strike(m2.text)
        assert max(f1.get_right()[0], f2.get_right()[0]) < SAFE_R, (f1.get_right(), f2.get_right())
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(r25, r27, card)), run_time=0.5)
            vo.wait_until("Two misconceptions")
            self.play(FadeIn(m1, shift=RIGHT * 0.15), FadeIn(m2, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("a 4-bit model does not")
            self.play(Create(s1), FadeIn(x1m, scale=0.6), run_time=0.5)
            self.play(Create(a1), FadeIn(f1, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("and the win is memory")
            self.play(Create(s2), FadeIn(x2m, scale=0.6), run_time=0.5)
            self.play(Create(a2), FadeIn(f2, shift=LEFT * 0.1), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(VGroup(tr, m1, m2, s1, s2, x1m, x2m, a1, a2, f1, f2)), run_time=0.9)
        self.wait(0.3)
