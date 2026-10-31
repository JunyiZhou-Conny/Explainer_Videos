"""S13 · LoRA: a thin correction (the lecture's PEFT families and LoRA; then Colab › Step 4 · Fine-tune, 4.1).
Lecture: 18–35.

Beats (script.md "## S13", one voiceover block each):
 0  LECTURE 18–20. A GREY model block with a snowflake and a small GREEN part ("trained"). Under
    "parameter-efficient fine-tuning" three GREY family cards fan out: additive · selective ·
    reparameterization; a GREEN "LoRA" chip lights in the third.
 1  LECTURE 23–25. V7's counted cells: a 5 × 5 grid ("25"); a 5 × 1 column and a 1 × 5 row slide
    out of it and multiply back into the grid ("= 10 numbers", "rank 1"); a second column-and-row
    pair joins ("= 20 numbers", "rank 2"); GREY caption "barely a saving".
 2  The grid grows into the GREY `q_proj · 2048 × 1024` rectangle (2,097,152). Beside it the two
    GREEN strips B 2048 × 8 and A 8 × 1024 at true scale (hairlines); a YELLOW lens pulls each out
    to a readable width (GREY caption "width 8 · magnified"); 24,576; the ratio writes "≈ 1.2 %".
 3  LECTURE 26. The equation W₀ + ΔW = W₀ + (α/r)·B·A writes; each symbol lights as named (W₀ GREY
    with a snowflake, B and A GREEN); GREY caption "decompose the update, not the weights".
 4  LECTURE 27–30. V7's block diagram: x at the bottom, GREY W₀ (snowflake) left, the GREEN A → B
    hourglass right (waist r, "A random", "B = 0"), the label α/r on the right branch, both into
    h; the formula h = W₀x + (α/r)·B·A·x on top; GREY chip "lecture: A ~ N(0, σ²) · PEFT: uniform ·
    both: B·A = 0 at step 0". Forward pass: both branches light; the right branch adds "+ 0".
 5  TRACKER Tune 1. CODE(colab/cell-67.py: 2–7) on top (long comments cut: the frame needs the
    diagram below it), the diagram under it with the YELLOW ▶ your turn tag beside it;
    `lora_alpha=16` and `r=8` fly onto α and r of the α/r label (it reads "α/r = 16/8 = 2"), the
    waist reads "r = 8"; lines 3 and 6 light briefly. 2 s hold.
 6  The block shrinks into Qwen3's 28-layer tower (seven cells per block); q and v light GREEN. A
    GREY card under the tower: the c42 shapes and each matrix's in + out sizes (q and v GREEN).
    GREY chip "4.1 names no target_modules → PEFT's Qwen3 default: q_proj, v_proj". The arithmetic
    8 × (1024 + 2048) + 8 × (1024 + 1024) = 40,960 per block; the counter ticks up the tower × 28
    to 1,146,880. GREY erratum chip "lecture: adapters on each layer · here: two projections per
    block".
 7  LECTURE 32–35. A GREY dashed square "7 B weights as one square · 83,666 × 83,666", "rank 1:
    2 × 83,666 ≈ 167 K", GREY chip "the lecture's table · one square matrix (slide 35's own
    warning)"; the tower and its shape card stay. PONDER(8 s).
 8  The card leaves. "r = 16 · q, v": the counter doubles to 2,293,760 ("linear in r"); then
    "r = 8 · all seven": every cell lights, the counter runs to 5,046,272 (8 × 22,528 × 28). GREY
    chips "more rank: more capacity · more memory and time" and "trying it? re-run 1.3 (reload the
    model) before 4.1–4.3". Everything fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Circle,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    Square,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S13"]

# ------------------------------------------------------------------ the real sources
CELL67 = "colab/cell-67.py"
assert source_line(CELL67, 2).startswith("peft_config = LoraConfig(lora_alpha=16,"), source_line(CELL67, 2)
assert source_line(CELL67, 3).strip().startswith("lora_dropout=0.1,"), source_line(CELL67, 3)
assert source_line(CELL67, 4).strip().startswith("r=8,"), source_line(CELL67, 4)
assert source_line(CELL67, 6).strip().startswith('task_type="CAUSAL_LM",'), source_line(CELL67, 6)
assert "target_modules" not in excerpt(CELL67, 1, 7)
C42 = capture("expected/colab-c42-qwen-config")
_cfg = {k: C42.line(n).strip() for k, n in (("head", 16), ("hidden", 18), ("inter", 20), ("heads", 54),
                                             ("layers", 55), ("kv", 56))}
assert _cfg == {"head": '"head_dim": 128,', "hidden": '"hidden_size": 1024,', "inter": '"intermediate_size": 3072,',
                "heads": '"num_attention_heads": 16,', "layers": '"num_hidden_layers": 28,',
                "kv": '"num_key_value_heads": 8,'}, _cfg

# the counts, from the shapes (in + out per matrix)
INTER = 3072
SHAPES = (("q", HIDDEN, Q_OUT), ("k", HIDDEN, KV_OUT), ("v", HIDDEN, KV_OUT), ("o", Q_OUT, HIDDEN),
          ("gate", HIDDEN, INTER), ("up", HIDDEN, INTER), ("down", INTER, HIDDEN))
assert Q_OUT == 16 * 128 and KV_OUT == 8 * 128 and HIDDEN == 1024
PER_BLOCK = LORA_R * (HIDDEN + Q_OUT) + LORA_R * (HIDDEN + KV_OUT)
assert PER_BLOCK == 40_960 and PER_BLOCK * QWEN_LAYERS == TRAINABLE == 1_146_880
R16 = 16 * (HIDDEN + Q_OUT + HIDDEN + KV_OUT) * QWEN_LAYERS
ALL7 = sum(i + o for _, i, o in SHAPES)
assert R16 == 2_293_760 and ALL7 == 22_528 and LORA_R * ALL7 * QWEN_LAYERS == 5_046_272
assert Q_OUT * HIDDEN == 2_097_152 and LORA_R * (Q_OUT + HIDDEN) == 24_576
SQ = 83_666                                     # √(7 × 10⁹), the lecture's one square layer (slides 32–35)
assert abs(SQ - (7e9) ** 0.5) < 1 and 2 * SQ == 167_332

# ------------------------------------------------------------------ layout
SAFE_L, SAFE_R = -6.45, 6.45


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


def flash(mob, color: str = TURN, k: float = 1.15, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def inside(m, l=SAFE_L, r=SAFE_R, b=-3.5, t=3.5):
    assert m.get_left()[0] >= l and m.get_right()[0] <= r and m.get_bottom()[1] >= b and m.get_top()[1] <= t, \
        (m.get_left(), m.get_right(), m.get_bottom(), m.get_top())


def grey_box(rows, color: str = S.GREY, dashed: bool = False, pad: float = 0.22) -> VGroup:
    """A GREY card around rows of texts (left aligned). .frame .rows"""
    body = VGroup(*rows).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    fr = box(body.width + 2 * pad, body.height + 2 * pad - 0.04, color, fill=S.BG, fill_opacity=0.95,
             radius=0.12, dashed=dashed)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.rows = fr, body
    return g


def family_card(title: str, sub: list[str], w: float = 3.95) -> VGroup:
    t = label(title, 24, INK)
    subs = [label(s, CAPTION, S.GREY) for s in sub]
    body = VGroup(t, *subs).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    fr = box(w, 2.05, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25).align_to(fr, UP).shift(DOWN * 0.22)
    g = VGroup(fr, body)
    g.frame, g.title = fr, t
    return g


class LowRank(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0 · PEFT: three families; LoRA is a reparameterization
        model = model_box("pretrained model", w=3.4, h=1.0, color=FROZEN)
        flake = snowflake(0.2)
        part = Rectangle(width=0.5, height=0.6, stroke_color=OWN, stroke_width=3).set_fill(OWN, 0.55)
        trained = label("trained", CAPTION, OWN)
        place(model, cx=-0.6, cy=1.7)
        place(flake, right=model.frame.get_right()[0] - 0.12, top=model.frame.get_top()[1] - 0.1)
        place(part, left=model.frame.get_right()[0] + 0.15, cy=model.frame.get_center()[1])
        place(trained, left=part.get_right()[0] + 0.15, cy=part.get_center()[1])
        frozen = label("frozen", CAPTION, S.GREY)
        place(frozen, right=model.frame.get_left()[0] - 0.2, cy=model.frame.get_center()[1])
        peft = label("parameter-efficient fine-tuning", 30, INK)
        place(peft, cx=0, cy=0.35)
        cards = VGroup(family_card("additive", ["add small new parts"]),
                       family_card("selective", ["train a chosen few"]),
                       family_card("reparameterization", ["train a compact form", "of the update"])) \
            .arrange(RIGHT, buff=0.3)
        place(cards, cx=0, top=-0.35)
        lora = chip("LoRA", OWN, size=24)
        place(lora, right=cards[2].frame.get_right()[0] - 0.2, bottom=cards[2].frame.get_bottom()[1] + 0.14)
        assert lora.get_top()[1] < cards[2][1].get_bottom()[1] - 0.04, (lora.get_top(), cards[2][1].get_bottom())
        inside(cards)
        lr = None
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "18–20")
            self.play(FadeIn(model, shift=UP * 0.15), FadeIn(flake), FadeIn(frozen), run_time=0.7)
            vo.wait_until("trains a small part")
            self.play(FadeIn(part, shift=LEFT * 0.2), FadeIn(trained), run_time=0.6)
            self.play(flash(part, OWN, 1.25), flash(flake, INK, 1.3), run_time=0.8)
            vo.wait_until("The lecture sorts")
            self.play(Write(peft), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cards], lag_ratio=0.35), run_time=1.4)
            vo.wait_until("additive, selective")
            for c in cards:
                self.play(c.frame.animate.set_stroke(INK), run_time=0.25)
                self.play(c.frame.animate.set_stroke(S.GREY), run_time=0.25)
            vo.wait_until("LoRA is a reparameterization")
            self.play(FadeIn(lora, scale=0.8), cards[2].frame.animate.set_stroke(OWN, 3.5), run_time=0.6)
            self.play(flash(lora, OWN, 1.2), run_time=0.6)

        # ========================================================== 1 · counted cells: 25 vs 10 vs 20
        rp1 = rank_product(5, 1, cell=0.42)
        rp2 = rank_product(5, 2, cell=0.42)
        place(rp1, cx=0, cy=0.4)
        rp2.shift(rp1.w.get_center() - rp2.w.get_center())
        w_alone = rp1.w.copy().move_to([0, rp1.w.get_center()[1], 0])
        cw_alone = rp1.counts[0].copy().next_to(w_alone, DOWN, buff=0.15)
        rk1 = label("rank 1", 26, OWN)
        rk2 = label("rank 2", 26, OWN)
        place(rk1, cx=VGroup(rp1.b, rp1.a).get_center()[0], bottom=rp1.w.get_top()[1] + 0.3)
        place(rk2, cx=VGroup(rp2.b, rp2.a).get_center()[0], bottom=rp2.w.get_top()[1] + 0.3)
        mmat = label("5 × 5 matrix", 26, S.GREY)
        place(mmat, cx=0, bottom=rp1.w.get_top()[1] + 0.3)
        barely = note("barely a saving", size=26)
        place(barely, cx=0, top=rp2.get_bottom()[1] - 0.5)
        inside(rp2)
        heads = VGroup()            # the label row above the grids (swapped in place)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(model, flake, frozen, part, trained, peft, cards, lora)), run_time=0.5)
            lr = lref_swap(self, lr, "23–25")
            vo.wait_until("A 5 by 5 matrix")
            self.play(FadeIn(mmat), LaggedStart(*[FadeIn(c, scale=0.6) for c in w_alone], lag_ratio=0.03),
                      run_time=1.2)
            self.play(FadeIn(cw_alone, shift=UP * 0.1), run_time=0.4)
            self.play(flash(cw_alone, INK, 1.4), run_time=0.5)
            vo.wait_until("A 5 by 1 column")
            self.play(FadeOut(mmat), Transform(w_alone, rp1.w), Transform(cw_alone, rp1.counts[0]), run_time=0.7)
            self.remove(w_alone, cw_alone)
            self.add(rp1.w, rp1.counts[0])
            col0 = VGroup(*[rp1.w[5 * i] for i in range(5)])
            row0 = VGroup(*[rp1.w[j] for j in range(5)])
            self.play(TransformFromCopy(col0, rp1.b), TransformFromCopy(row0, rp1.a),
                      FadeIn(rp1[0][1]), FadeIn(rp1[0][3]), run_time=1.0)
            self.play(FadeIn(rp1.counts[1]), FadeIn(rp1.counts[2]), FadeIn(rk1, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("also makes a 5 by 5 matrix")
            prod = VGroup(rp1.b, rp1.a).copy()
            self.play(Transform(prod, rp1.w.copy().set_fill(OWN, 0.45).set_stroke(OWN)), run_time=0.9)
            self.play(FadeOut(prod), flash(rp1.w, OWN, 1.06), run_time=0.6)
            vo.wait_until("from only 10 numbers")
            self.play(FadeIn(rp1.counts[3], shift=LEFT * 0.1), run_time=0.5)
            self.play(flash(rp1.counts[3], OWN, 1.15), run_time=0.6)
            vo.wait_until("rank 2 needs 20")
            self.play(Transform(rp1.b, rp2.b), Transform(rp1.a, rp2.a), Transform(rp1[0][3], rp2[0][3]),
                      *swap_text(heads, rk1, rk2),
                      *swap_text(heads, rp1.counts[1], rp2.counts[1]),
                      *swap_text(heads, rp1.counts[2], rp2.counts[2]),
                      *swap_text(heads, rp1.counts[3], rp2.counts[3]), run_time=1.0)
            vo.wait_until("At this size")
            self.play(FadeIn(barely, shift=UP * 0.1), run_time=0.6)
        grid1 = VGroup(rp1.w, rp1[0][1], rp1.b, rp1[0][3], rp1.a, rp1.counts[0], rk2, rp2.counts[1],
                       rp2.counts[2], rp2.counts[3], barely)

        # ========================================================== 2 · real size: q_proj vs two hairline strips
        sc = 1.0 / 560
        real = real_size(scale=sc)
        real.b.stretch_to_fit_width(LORA_R * sc).set_stroke(OWN, 1.5)      # true scale: a hairline
        real.a.stretch_to_fit_height(LORA_R * sc).set_stroke(OWN, 1.5)
        real.a.align_to(real.b, UP)
        real.a.next_to(real.b, RIGHT, buff=0.3).align_to(real.b, UP)
        place(real, cx=-2.3, cy=0.1)
        inside(real)
        ratio = VGroup(label("24,576 / 2,097,152", 28, INK), label("≈ 1.2 %", 34, TURN)).arrange(DOWN, buff=0.2)
        place(ratio, left=real.get_right()[0] + 0.4, cy=real.w.get_center()[1] - 0.6)
        inside(ratio)
        dim_w = mono("1,024", CAPTION, S.GREY).next_to(real.w, UP, buff=0.1)
        dim_h = mono("2,048", CAPTION, S.GREY).next_to(real.w, LEFT, buff=0.12)
        inside(dim_h)
        lens = Circle(radius=0.2, stroke_color=TURN, stroke_width=3)
        lens.move_to(real.b.get_center())
        view_c = np.array([real.a.get_center()[0] + 0.15, real.a.get_top()[1] - 1.25, 0])
        view = Circle(radius=0.78, stroke_color=TURN, stroke_width=3).set_fill(S.BG, 1).move_to(view_c)
        cols8 = VGroup(*[Rectangle(width=0.085, height=1.05, stroke_width=1, stroke_color=OWN).set_fill(OWN, 0.6)
                         for _ in range(8)]).arrange(RIGHT, buff=0.03).move_to(view_c)
        rows8 = VGroup(*[Rectangle(width=1.05, height=0.085, stroke_width=1, stroke_color=OWN).set_fill(OWN, 0.6)
                         for _ in range(8)]).arrange(DOWN, buff=0.03).move_to(view_c)
        link = Line(lens.get_right(), view.get_left(), color=TURN, stroke_width=2)
        mag = note("width 8 · magnified")
        place(mag, cx=view_c[0], top=view.get_bottom()[1] - 0.12)
        assert mag.get_bottom()[1] > real[2].get_top()[1] + 0.05, (mag.get_bottom(), real[2].get_top())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(*[m for m in grid1 if m is not rp1.w])), run_time=0.5)
            self.play(Transform(rp1.w, real.w), run_time=1.1)
            self.remove(rp1.w)
            self.add(real.w)
            vo.wait_until("Qwen's query projection")
            self.play(FadeIn(real[1][0], shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(dim_h, shift=RIGHT * 0.1), run_time=0.4)
            self.play(FadeIn(dim_w, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("over 2 million numbers")
            self.play(FadeIn(real[1][1], shift=UP * 0.1), run_time=0.5)
            self.play(flash(real[1][1], INK, 1.15), run_time=0.6)
            vo.wait_until("A rank 8 pair of strips")
            self.play(Create(real.b), Create(real.a), FadeIn(real[2][0]), run_time=0.8)
            self.play(Create(lens), run_time=0.4)
            self.play(Create(link), FadeIn(view, scale=0.5), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in cols8], lag_ratio=0.1), FadeIn(mag), run_time=0.8)
            vo.wait_until("and 8 by 1,024")
            lens2 = lens.copy().move_to(real.a.get_center())
            self.play(lens.animate.move_to(real.a.get_center()),
                      Transform(link, Line(lens2.get_bottom(), view.get_top(), color=TURN, stroke_width=2)),
                      Transform(cols8, rows8), run_time=0.9)
            vo.wait_until("holds 24,576")
            self.play(FadeIn(real[2][1], shift=UP * 0.1), run_time=0.5)
            self.play(flash(real[2][1], OWN, 1.2), Write(ratio), run_time=1.0)
        beat2 = VGroup(real, dim_w, dim_h, lens, link, view, cols8, mag, ratio)

        # ========================================================== 3 · decompose the update: the equation
        eq = LoraEquation(size=46)
        place(eq, cx=0, cy=0.6)
        fl_eq = snowflake(0.18)
        place(fl_eq, cx=eq.sym("W0b").get_center()[0], bottom=eq.get_top()[1] + 0.15)
        fl_eq0 = snowflake(0.18)
        place(fl_eq0, cx=eq.sym("W0").get_center()[0], bottom=eq.get_top()[1] + 0.15)
        dec = note("decompose the update, not the weights", size=26)
        place(dec, cx=0, top=eq.get_bottom()[1] - 0.5)
        brace_dw = Line(eq.sym("dW").get_corner(DOWN + LEFT), eq.sym("dW").get_corner(DOWN + RIGHT),
                        color=OWN, stroke_width=3).shift(DOWN * 0.12)
        brace_ba = Line(eq.sym("B").get_corner(DOWN + LEFT), eq.sym("A").get_corner(DOWN + RIGHT),
                        color=OWN, stroke_width=3).shift(DOWN * 0.12)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(beat2), run_time=0.5)
            lr = lref_swap(self, lr, "26")
            self.play(Write(VGroup(*eq[:5])), FadeIn(fl_eq0), run_time=0.9)
            self.play(FadeIn(brace_dw), flash(eq.sym("dW"), OWN, 1.3), run_time=0.6)
            self.play(FadeIn(dec, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("The new layer")
            self.play(Write(VGroup(*eq[5:])), run_time=1.2)
            vo.wait_until("the frozen W naught")
            self.play(FadeIn(fl_eq), flash(eq.sym("W0b"), INK, 1.3), run_time=0.6)
            vo.wait_until("plus alpha over r")
            self.play(flash(VGroup(eq.sym("alpha"), eq.sym("r")), TURN, 1.3), run_time=0.7)
            vo.wait_until("times B times A")
            self.play(flash(eq.sym("B"), OWN, 1.35), run_time=0.45)
            self.play(flash(eq.sym("A"), OWN, 1.35), run_time=0.45)
            vo.wait_until("Only B and A")
            self.play(Transform(brace_dw, brace_ba), run_time=0.6)
            self.play(flash(VGroup(eq.sym("B"), eq.sym("A")), OWN, 1.25), run_time=0.7)

        # ========================================================== 4 · the block diagram; initialization; forward pass
        blk = LoraBlock()
        place(blk, cx=-0.4, top=2.2)
        ar = label("α/r", 24, INK)
        place(ar, left=blk.b.get_top()[0] + 0.15, cy=(blk.b.get_top()[1] + blk.plus.get_center()[1]) / 2)
        blk.part("ar", ar)
        hform = label("h = W₀x + (α/r)·B·A·x", 32, INK, t2c={"W₀": FROZEN, "B": OWN, "A": OWN})
        place(hform, cx=0, top=2.75)
        init = chip("lecture: A ∼ N(0, σ²) · PEFT: uniform · both: B·A = 0 at step 0", S.GREY, size=CAPTION)
        place(init, cx=0, bottom=-3.45)
        plus0 = label("+ 0", 26, TURN)
        place(plus0, left=blk.plus.get_right()[0] + 0.12, bottom=blk.plus.get_top()[1] - 0.05)
        assert blk.get_bottom()[1] > init.get_top()[1] + 0.1 and blk.get_top()[1] < hform.get_bottom()[1] - 0.1, \
            (blk.get_bottom(), blk.get_top(), init.get_top())
        inside(init)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(fl_eq0, fl_eq, dec, brace_dw)), run_time=0.4)
            lr = lref_swap(self, lr, "27–30")
            self.play(FadeOut(eq, shift=UP * 0.2), FadeIn(hform, shift=UP * 0.2), run_time=0.6)
            self.play(*blk.parts_in("x", "w0", "ab", "wires", "sum", "h", "ar"), run_time=1.0)
            vo.wait_until("B starts at zero")
            na, nb = blk.parts["notes"]
            self.play(*blk.parts_in("notes"), run_time=0.5)
            self.play(flash(VGroup(blk.b, nb), OWN, 1.1), run_time=0.6)
            vo.wait_until("and A at random")
            self.play(flash(VGroup(blk.a, na), OWN, 1.1), run_time=0.6)
            vo.wait_until("The lecture draws A")
            self.play(FadeIn(init, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("What matters")
            self.play(flash(VGroup(nb, na), TURN, 1.15), run_time=0.7)
            vo.wait_until("so at step zero")
            self.play(*blk.forward(1.6))
            self.play(FadeIn(plus0, shift=LEFT * 0.1), run_time=0.4)
            self.play(flash(plus0, TURN, 1.4), blk.w0.animate.set_stroke(INK, 4), run_time=0.7)
            vo.wait_until("Both branches")
            self.play(blk.w0.animate(run_time=0.5).set_stroke(FROZEN, 3), *blk.forward(1.2))
            self.play(blk.plus[0].animate.set_stroke(TURN, 3.5), run_time=0.4)
            self.play(blk.plus[0].animate.set_stroke(INK, 2.5), run_time=0.4)

        # ========================================================== 5 · the LoRA config (4.1) pinned onto the diagram; ▶
        tr = tracker("Tune", 1)
        p67 = src_panel(CELL67, 2, 7, size=20, cut_comments=True)
        place(p67, left=-6.3, top=2.75)
        blk_t = blk.copy()
        blk_t.rescale(0.66)
        place(blk_t, cx=-1.4, top=p67.get_bottom()[1] - 0.2)
        blk_t.parts["w0"][3].next_to(blk_t.w0, LEFT, buff=0.15)          # labels keep their size: re-seat them
        blk_t.parts["notes"][0].next_to(blk_t.a, RIGHT, buff=0.12)
        blk_t.parts["notes"][1].next_to(blk_t.b, RIGHT, buff=0.12)
        for node in (blk_t.h_node, blk_t.x_node):                         # 28 pt glyphs in shrunken circles
            node[1].scale(0.8).move_to(node[0])
        blk_t.parts["ab"][2].scale(0.8).move_to(blk_t.a).shift(DOWN * 0.04)
        blk_t.parts["ab"][3].scale(0.8).move_to(blk_t.b).shift(UP * 0.04)
        sf_t = blk_t.parts["w0"][2]
        sf_t.move_to(blk_t.w0.get_corner(UP + RIGHT) + np.array([-0.08 - sf_t.width / 2, -0.08 - sf_t.height / 2, 0]))
        waist = blk_t.a.get_top()
        blk_t.parts["ab"][4].move_to(waist + LEFT * (0.42 + blk_t.parts["ab"][4].width / 2))
        blk_t.parts["ar"].move_to([blk_t.b.get_top()[0] + 0.15 + blk_t.parts["ar"].width / 2,
                                   (blk_t.b.get_top()[1] + blk_t.plus.get_center()[1]) / 2 + 0.04, 0])
        assert blk_t.get_bottom()[1] > -3.5, blk_t.get_bottom()
        ar_t = blk_t.parts["ar"]
        rt_t = blk_t.parts["ab"][4]
        ar2 = label("α/r = 16/8 = 2", 24, INK, t2c={"= 2": TURN})
        ar2.move_to(ar_t, aligned_edge=LEFT)
        r8 = label("r = 8", CAPTION, OWN)
        r8.move_to(rt_t, aligned_edge=RIGHT)
        yt = your_turn()
        place(yt, left=blk_t.get_right()[0] + 0.4, cy=blk_t.w0.get_center()[1])
        inside(yt)
        assert ar2.get_right()[0] < yt.get_left()[0] - 0.1 or ar2.get_bottom()[1] > yt.get_top()[1], ar2.get_right()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(hform, init, plus0)), run_time=0.4)
            self.play(Transform(blk, blk_t), FadeIn(tr, shift=DOWN * 0.25), run_time=0.9)
            self.play(FadeIn(p67, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("alpha 16")
            s_al = p67.span(2, "lora_alpha=16")
            self.play(s_al.animate.set_color(TURN), run_time=0.3)
            self.play(TransformFromCopy(s_al, blk.parts["ar"][0]), run_time=0.8)
            vo.wait_until("and rank 8")
            s_r = p67.span(4, "r=8")
            self.play(s_r.animate.set_color(TURN), run_time=0.3)
            self.play(TransformFromCopy(s_r, blk.parts["ar"][2]), run_time=0.7)
            self.play(*swap_text(blk.parts["ab"], blk.parts["ab"][4], r8), run_time=0.6)
            vo.wait_until("so the update is scaled by 2")
            self.play(*swap_text(blk, blk.parts["ar"], ar2), run_time=0.7)
            self.play(flash(ar2[-1], TURN, 1.4), run_time=0.5)
            vo.wait_until("plus a dropout")
            b3 = p67.bar(3, TURN)
            self.play(FadeIn(b3), run_time=0.4)
            b6 = p67.bar(6, TURN)
            self.play(FadeOut(b3), FadeIn(b6), run_time=0.6)
            self.play(FadeOut(b6), run_time=0.4)
            vo.wait_until("Pause and run it")
            self.play(FadeIn(yt, shift=LEFT * 0.15), run_time=0.5)
        self.wait(2)

        # ========================================================== 6 · which layers: q_proj and v_proj in 28 blocks
        tower = LayerTower()
        tw_rows, tw_heads, tw_cap, ctr = tower.rows, tower.heads, tower[2], tower.counter
        tw_rows.stretch_to_fit_height(2.3)
        place(tw_rows, left=-4.75, top=2.3)
        tw_heads[0].next_to(tw_rows[-1][0], UP, buff=0.1)
        tw_heads[1].next_to(tw_rows[-1][2], UP, buff=0.1)
        place(tw_cap, right=tw_rows.get_left()[0] - 0.2, cy=tw_rows.get_center()[1])
        inside(tw_cap)
        # each matrix's in + out sizes, one row per matrix, beside the tower (q and v GREEN later)
        shp = VGroup(*[mono_line(f"{n:<5}{i} + {o}", CAPTION, INK) for n, i, o in SHAPES]).arrange(DOWN, buff=0.06,
                                                                                                aligned_edge=LEFT)
        shp_head = label("in + out", CAPTION, S.GREY)
        shp_g = VGroup(shp_head, shp).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        place(shp_g, left=tw_rows.get_right()[0] + 0.45, top=2.45)
        q_txt, v_txt = shp[0], shp[2]
        others = [shp[k] for k in (1, 3, 4, 5, 6)]
        src42 = grey_box([label(f"{colab_where(42)} · recorded config", CAPTION, S.GREY),
                          label("hidden 1,024 · 16 × 128 query · 8 × 128 key-value · intermediate 3,072",
                                CAPTION, S.GREY)], pad=0.16)
        place(src42, left=-6.4, top=min(tw_rows.get_bottom()[1], shp_g.get_bottom()[1]) - 0.2)
        inside(src42)
        place(ctr, left=shp_g.get_right()[0] + 0.5, top=2.75)
        inside(ctr)
        # one block's frame on the tower's bottom row
        row0 = tw_rows[0]
        mark0 = Rectangle(width=row0.width + 0.12, height=row0.height + 0.1, stroke_color=TURN, stroke_width=2.5)
        mark0.move_to(row0)
        dflt = chip("4.1 names no target_modules → PEFT's Qwen3 default: q_proj, v_proj", S.GREY, size=CAPTION)
        place(dflt, left=-6.4, top=src42.get_bottom()[1] - 0.2)
        inside(dflt)
        arith = VGroup(label("8 × (1024 + 2048)", 24, INK),
                       label("+ 8 × (1024 + 1024)", 24, INK),
                       label("= 40,960 per block", 24, INK, t2c={"40,960": TURN}),
                       label("× 28 = 1,146,880", 24, INK, t2c={"1,146,880": OWN})).arrange(DOWN, buff=0.14,
                                                                                         aligned_edge=LEFT)
        place(arith, left=ctr.get_left()[0], top=ctr.get_bottom()[1] - 0.3)
        inside(arith)
        assert arith.get_bottom()[1] > src42.get_top()[1] + 0.1, (arith.get_bottom(), src42.get_top())
        errat = erratum_tag("lecture: adapters on each layer · here: two projections per block")
        place(errat, left=-6.4, top=dflt.get_bottom()[1] - 0.15)
        inside(errat)
        sweep = Rectangle(width=row0.width + 0.12, height=row0.height + 0.06, stroke_color=TURN, stroke_width=2.5)
        sweep.move_to(row0)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(p67, yt)), FadeOut(lr), run_time=0.5)
            lr = None
            ghost = blk.glyph_only()
            self.play(FadeIn(ghost), FadeOut(blk), run_time=0.4)
            self.play(ghost.animate.scale(0.12).move_to(row0), run_time=0.8)
            self.play(FadeOut(ghost), FadeIn(tw_rows[0]), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.05) for r in tw_rows[1:]], lag_ratio=0.08),
                      FadeIn(tw_cap), run_time=1.2)
            vo.wait_until("The config names no target modules")
            self.play(FadeIn(dflt, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the PEFT library's default")
            self.play(FadeIn(tw_heads), tower.light_qv(1.6))
            vo.wait_until("two of the seven matrices")
            self.play(Create(mark0), FadeIn(shp_g, shift=LEFT * 0.1), FadeIn(src42, shift=UP * 0.1), run_time=0.7)
            self.play(q_txt.animate.set_color(OWN), v_txt.animate.set_color(OWN), run_time=0.5)
            vo.wait_until("in each of the 28 blocks")
            self.play(FadeIn(errat, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("That's 40,960 per block")
            self.play(FadeIn(arith[:3], shift=LEFT * 0.1), FadeIn(ctr), run_time=0.7)
            vo.wait_until("1,146,880 in all")
            self.play(FadeOut(mark0), run_time=0.2)
            self.play(sweep.animate.move_to(tw_rows[-1]), tower.count(TRAINABLE, 1.6), run_time=1.6)
            self.play(FadeOut(sweep), FadeIn(arith[3], shift=LEFT * 0.1), run_time=0.5)
            self.play(flash(ctr.num, OWN, 1.15), run_time=0.6)

        # ========================================================== 7 · the lecture's table: one square layer; PONDER
        sq = DashedVMobject(Square(side_length=1.2), num_dashes=32, dashed_ratio=0.55).set_stroke(S.GREY, 2.5)
        place(sq, left=ctr.get_left()[0], top=ctr.get_bottom()[1] - 0.3)
        sq_txt = VGroup(label("7 B weights as one square", CAPTION, S.GREY),
                        mono("83,666 × 83,666", CAPTION, S.GREY),
                        label("rank 1: 2 × 83,666 ≈ 167 K", 24, INK)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        place(sq_txt, left=ctr.get_left()[0], top=sq.get_bottom()[1] - 0.15)
        inside(sq_txt)
        tbl = chip("the lecture's table · one square matrix (slide 35's own warning)", S.GREY, size=CAPTION)
        place(tbl, left=-6.4, top=src42.get_bottom()[1] - 0.2)
        inside(tbl)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(dflt, errat, arith)), run_time=0.5)
            lr = lref_swap(self, lr, "32–35")
            self.play(Create(sq), run_time=0.7)
            self.play(FadeIn(sq_txt[0]), FadeIn(sq_txt[1]), run_time=0.5)
            self.play(Write(sq_txt[2]), run_time=0.8)
            vo.wait_until("the real count depends")
            self.play(FadeIn(tbl, shift=UP * 0.1), run_time=0.5)
            self.play(flash(VGroup(q_txt, v_txt), OWN, 1.1), flash(tower.q, OWN, 1.03), run_time=0.8)
        card = ponder_at(self, "With r=16, how many trainable parameters?\n"
                               "And with target_modules=\"all-linear\" at r = 8?", 8, y=-2.2, hide=(tbl, src42))
        assert card.get_top()[1] < min(sq_txt.get_bottom()[1], shp_g.get_bottom()[1], tw_rows.get_bottom()[1]) - 0.05, \
            (card.get_top(), sq_txt.get_bottom(), shp_g.get_bottom())

        # ========================================================== 8 · the answers; capacity vs cost; reload first
        cnote = VGroup(label("r = 16 · q, v", 24, TURN), label("linear in r", CAPTION, S.GREY)) \
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        place(cnote, left=ctr.get_left()[0], top=ctr.get_bottom()[1] - 0.3)
        cnote2 = VGroup(label("r = 8 · all seven", 24, TURN), label("8 × 22,528 × 28", 24, INK)) \
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        place(cnote2, left=ctr.get_left()[0], top=ctr.get_bottom()[1] - 0.3)
        inside(cnote2)
        cnote3 = VGroup(label("r = 8 · q, v", 24, OWN), label("plenty for a persona", CAPTION, S.GREY)) \
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        place(cnote3, left=ctr.get_left()[0], top=ctr.get_bottom()[1] - 0.3)
        more = chip("more rank: more capacity · more memory and time", S.GREY, size=CAPTION)
        place(more, left=-6.4, top=src42.get_bottom()[1] - 0.2)
        retry = chip("trying it? re-run 1.3 (reload the model) before 4.1–4.3", S.GREY, size=CAPTION)
        place(retry, left=-6.4, top=more.get_bottom()[1] - 0.15)
        inside(retry)
        notes8 = VGroup()
        rest = VGroup(*[tw_rows[k][j] for k in range(QWEN_LAYERS) for j in (1, 3, 4, 5, 6)])
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(card), FadeOut(VGroup(sq, sq_txt)), FadeOut(lr), run_time=0.5)
            lr = None
            self.play(FadeIn(cnote, shift=LEFT * 0.1), run_time=0.5)
            self.play(tower.count(R16, 1.2))
            self.play(flash(ctr.num, TURN, 1.15), run_time=0.5)
            vo.wait_until("All seven projections")
            self.play(*swap_text(notes8, cnote, cnote2), run_time=0.6)
            self.play(LaggedStart(*[c.animate.set_fill(OWN, 0.8).set_stroke(OWN) for c in rest], lag_ratio=0.004),
                      *[t.animate.set_color(OWN) for t in others], run_time=1.4)
            self.play(tower.count(5_046_272, 1.2))
            self.play(flash(ctr.num, OWN, 1.12), run_time=0.6)
            vo.wait_until("More rank buys capacity")
            self.play(FadeIn(more, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("for a persona")
            self.play(*swap_text(notes8, cnote2, cnote3), run_time=0.6)
            self.play(*[c.animate.set_fill(FROZEN, 0.25).set_stroke(S.GREY_DARK) for c in rest],
                      *[t.animate.set_color(INK) for t in others], tower.count(TRAINABLE, 1.0), run_time=1.0)
            self.play(flash(VGroup(q_txt, v_txt), OWN, 1.12), run_time=0.7)
            vo.wait_until("To try it")
            self.play(FadeIn(retry, shift=UP * 0.1), run_time=0.5)
            self.play(flash(retry, INK, 1.05), run_time=0.6)
        ctr.freeze()
        self.play(FadeOut(VGroup(tower, shp_g, cnote3, more, retry, tr)), run_time=0.8)
        self.wait(0.3)
