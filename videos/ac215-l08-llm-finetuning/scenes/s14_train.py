"""S14 · Training on a small GPU (Colab › Step 4 · Fine-tune, 4.2–4.5, and the lecture's memory tricks).
Lecture: 13–15, 37–39, 57–72.

Beats (script.md "## S14", one voiceover block each):
 0  LECTURE 13–15, 37–39. V5 redrawn for Qwen3-0.6B (tag `estimate`, our arithmetic) inside a GREY
    dashed "T4 · 16 GB" outline: left "full fine-tuning ≈ 7 GB · before activations" (FP16 params
    1.2 + FP16 grads 1.2 + FP32 Adam 4.8 GB); right "QLoRA in this notebook ≈ 0.9 GB": a thin GREY
    4-bit linears 0.22 GB, GREY embeddings 0.62 GB (WHITE `FP32` tag), a hairline GREEN "A, B +
    grads + Adam ≈ 18 MB" (drawn thicker than true). On "fit a T4" both columns pulse inside the outline. On "scales" the
    lecture's GREY dashed 10 B column slides in on the right and runs past the T4 line out of the
    picture ("↑ 120 GB", `concept · lecture only`).
 1  LECTURE 57–64. V8: X → h₁ → h₂ → h₃ → ŷ with an activation-memory meter. Forward: each node
    fills, the meter climbs. Checkpointing: all but h₂ empty, the meter drops; h₃ is recomputed
    from h₂ (PINK replay arc); caption "compute for memory"; GREY chip "on since 1.3 (cell 36)".
 2  TRACKER Tune 2. CODE(colab/cell-70.py: 2–17) folded to 3, 5–7, 10, 12–13, 15 (long comment cut),
    YELLOW ▶ your turn beside it. Lines 3 and 15 light, then 5–6, 10, 7. LECTURE 65: V8's paging
    (compact, under the panel): optimizer pages slide GPU → CPU along PINK arrows and back; GREY
    footnote "our ≈ 18 MB never needs it". 2 s hold.
 3  LECTURE 66–67. Lines 12–13 light; the panel gives way to those two lines. V8's bit strips FP32
    1/8/23, FP16 1/5/10, BF16 1/8/7 (sign WHITE, exponent PINK = range, fraction GREEN = precision);
    BF16's exponent and FP32's light together. GREY chip "T4: no fast BF16 → FP16 here (lecture:
    BF16 for QLoRA)"; RECORDED(c31: 9, wrapped).
 4  TRACKER Tune 3. CODE(colab/cell-72.py: 10–14) (comments wrapped); V7's block (small) with
    `BF16` tags on A and B, which turn RED on "cannot unscale" and transform into `FP32` when lines
    12–14 light. The panel leaves for RECORDED(c72: 23, wrapped) on top; `1146880` lights YELLOW, and the
    count from the LoRA chapter, "our count: 1,146,880", writes beside the block with a ✓.
 5  LECTURE 29, 70. The block returns full size; a YELLOW pulse runs down from h through W₀ (W₀
    greys further, unchanged, its snowflake flashes) into B and A, which glow; GREY chip
    "lecture: gradients flow only through the adapters · precisely: through W₀ too, but W₀ gets
    no gradient".
 6  TRACKER Tune 4. RECORDED(c75: 5–15) (tabs shown as spaces); `[450/450 03:36, Epoch 2/2]`
    lights; each loss value flies to its point of a falling curve (2.007381 → 1.350437, steps
    50–450). The GREY chip "900 / 4 × 2 = 450" writes beside the table on "900 examples"; when the
    box leaves, it moves under the `[450/450 …]` row, which stays.
    TRACKER Tune 5: RECORDED(c77: 4) with "open it in your own run" replaces the chip. YELLOW
    ▶ your turn, 2 s hold, everything fades to an empty frame.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    ShowPassingFlash,
    Transform,
    TransformFromCopy,
    VGroup,
    VMobject,
)

from common import *  # noqa: F401,F403
from common import wrap_output
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S14"]

# ------------------------------------------------------------------ the real sources and captures
CELL70 = "colab/cell-70.py"
CELL72 = "colab/cell-72.py"
assert source_line(CELL70, 3).strip() == "max_length=512,"
assert source_line(CELL70, 5).strip().startswith("num_train_epochs=2,")
assert source_line(CELL70, 6).strip().startswith("per_device_train_batch_size=4,")
assert source_line(CELL70, 7).strip().startswith('optim="paged_adamw_32bit",')
assert source_line(CELL70, 10).strip().startswith("learning_rate=2e-4,")
assert source_line(CELL70, 12).strip().startswith("fp16=True,")
assert source_line(CELL70, 13).strip().startswith("bf16=False,")
assert source_line(CELL70, 15).strip().startswith('train_sampling_strategy="group_by_length",')
assert source_line(CELL72, 12).startswith("for param in trainer.model.parameters():")
assert source_line(CELL72, 14).strip() == "param.data = param.data.float()"
C31 = capture("expected/colab-c31-gpu-bf16-check")
C72 = capture("expected/colab-c72-sfttrainer-trainable")
C75 = capture("expected/colab-c75-train")
C77 = capture("expected/colab-c77-tensorboard")
assert C31.line(9).startswith("Your GPU supports bfloat16.")
assert C72.line(23).startswith("trainable params: 1146880 ||") and TRAINABLE == 1_146_880
assert C75.line(5) == "[450/450 03:36, Epoch 2/2]", C75.line(5)
assert C77.line(4).startswith("Output hidden;")
LOSS = loss_points()
assert LOSS[0] == (50, 2.007381) and LOSS[-1] == (450, 1.350437) and len(LOSS) == 9
assert 900 // 4 * 2 == 450

# ------------------------------------------------------------------ our 0.6 B estimate (script.md "V5 numbers")
N_PARAMS = 596e6                      # Qwen3-0.6B
GB = 1e9
FULL_P, FULL_G, FULL_O = N_PARAMS * 2 / GB, N_PARAMS * 2 / GB, N_PARAMS * 8 / GB      # 1.19, 1.19, 4.77
assert abs(FULL_P + FULL_G + FULL_O - 7.15) < 0.01
Q_LIN, Q_EMB, Q_AB = 0.22, 0.62, 0.018                                              # GB
assert abs(Q_LIN + Q_EMB + Q_AB - 0.86) < 0.01

# ------------------------------------------------------------------ layout
SAFE_L, SAFE_R = -6.45, 6.45
SC = 0.3375                           # GB -> units: the T4's 16 GB is 5.4 tall
BASE = -2.9                           # the columns' floor
T4_TOP = BASE + 16 * SC               # 2.5
X_FULL, X_Q, X_10B = -5.7, -1.0, 5.1
K_BLK = 0.62                          # V7's block, small, in the trainer beat
NODE_K = 1.35                         # ... with its x, h and + circles widened back around their labels


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


def down(path, run_time: float):
    """A YELLOW gradient pulse running along `path` from its end back to its start (the backward pass)."""
    rev = VMobject().set_points(path.get_points()[::-1]).set_stroke(PULSE, 7)
    return ShowPassingFlash(rev, time_width=0.7, run_time=run_time)


def inside(m, l=SAFE_L, r=SAFE_R, b=-3.5, t=3.5):
    assert m.get_left()[0] >= l and m.get_right()[0] <= r and m.get_bottom()[1] >= b and m.get_top()[1] <= t, \
        (m.get_left(), m.get_right(), m.get_bottom(), m.get_top())


class Col(MemoryColumn):
    """V5's column with hairline minimum blocks (the 18 MB of adapters: thicker than true)."""
    MIN_H = 0.05


def lift_labels(col: MemoryColumn, floor: float) -> None:
    """Raise a column's block labels so the lowest sits above `floor` (clear of the T4 outline's
    bottom edge); the leaders are re-drawn from each block to its label."""
    low = min(t.get_bottom()[1] for t in col.tags.values())
    dy = max(0.0, floor - low)
    for n in col.order:
        t = col.tags[n]
        t.shift(UP * dy)
        col.leads[n].put_start_and_end_on(col.blocks[n].get_right(), t.get_left() + LEFT * 0.05)


def wrapped(cap, n: int, width: int) -> list[str]:
    """File line n of a capture folded at word boundaries (script: `wrap`)."""
    return [r for r, *_ in wrap_output(cap.line(n), width)]


def grey_box(rows, color: str = S.GREY, pad: float = 0.2) -> VGroup:
    """A GREY card around rows of text (left aligned). .frame .rows"""
    body = VGroup(*rows).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    fr = box(body.width + 2 * pad, body.height + 2 * pad - 0.04, color, fill=S.BG, fill_opacity=0.95, radius=0.12)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.rows = fr, body
    return g


def paging_row() -> VGroup:
    """V8's paging (slide 65), compact: a BLUE GPU box with optimizer pages, a GREY CPU box, PINK
    arrows between. .gpu .cpu .pages .arrows"""
    gpu = box(2.3, 0.9, CLOUD, fill_opacity=0.06)
    cpu = box(2.3, 0.9, S.GREY, fill_opacity=0.04)
    VGroup(gpu, cpu).arrange(RIGHT, buff=1.2)
    gl = label("GPU", CAPTION, CLOUD).next_to(gpu, LEFT, buff=0.15)
    cl = label("CPU memory", CAPTION, S.GREY).next_to(cpu, RIGHT, buff=0.15)
    arrows = VGroup(Arrow(gpu.get_right() + UP * 0.2, cpu.get_left() + UP * 0.2, buff=0.08, color=LOOKUP,
                          stroke_width=3, max_tip_length_to_length_ratio=0.15),
                    Arrow(cpu.get_left() + DOWN * 0.2, gpu.get_right() + DOWN * 0.2, buff=0.08, color=LOOKUP,
                          stroke_width=3, max_tip_length_to_length_ratio=0.15))
    pages = VGroup(*[file_glyph(0.34, INK) for _ in range(6)]).arrange(RIGHT, buff=0.1).move_to(gpu)
    g = VGroup(gpu, cpu, gl, cl, arrows, pages)
    g.gpu, g.cpu, g.pages, g.arrows = gpu, cpu, pages, arrows
    return g


class SmallGpu(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · V5 at 0.6 B: 7 GB vs 0.9 GB inside a T4; 10 B overflows
        t4 = box(10.5, 16 * SC, S.GREY, dashed=True, radius=0.08)
        place(t4, left=-6.4, bottom=BASE)
        t4_l = label("T4 · 16 GB", 24, S.GREY)
        place(t4_l, left=t4.get_left()[0] + 0.2, top=t4.get_top()[1] - 0.15)
        est = estimate_tag()
        place(est, right=t4.get_right()[0] - 0.2, top=t4.get_top()[1] - 0.15)
        full = Col([("params · FP16 · 1.2 GB", FULL_P, S.GREY, None),
                    ("grads · FP16 · 1.2 GB", FULL_G, PULSE, None),
                    ("Adam · FP32 · 4.8 GB", FULL_O, S.PURPLE, "FP32")], scale=SC, col_w=1.1)
        full.shift(RIGHT * X_FULL + UP * BASE)
        ql = Col([("4-bit linears · 0.22 GB", Q_LIN, FROZEN, None),
                  ("embeddings · 0.62 GB", Q_EMB, FROZEN, None),
                  ("A, B + grads + Adam ≈ 18 MB", Q_AB, OWN, None)], scale=SC, col_w=1.1)
        ql.shift(RIGHT * X_Q + UP * BASE)
        lift_labels(full, BASE + 0.1)
        lift_labels(ql, BASE + 0.1)
        ql.blocks["4-bit linears · 0.22 GB"].set_fill(FROZEN, 0.15)
        ql.blocks["embeddings · 0.62 GB"].set_fill(FROZEN, 0.6)
        ql.tags["A, B + grads + Adam ≈ 18 MB"].set_color(OWN)
        fp32 = dtype_tag("FP32")
        emb_t = ql.tags["embeddings · 0.62 GB"]
        place(fp32, left=emb_t.get_right()[0] + 0.15, cy=emb_t.get_center()[1])
        assert full.get_right()[0] < ql.blocks["4-bit linears · 0.22 GB"].get_left()[0] - 0.25, full.get_right()
        title_f = VGroup(label("full fine-tuning ≈ 7 GB", 26, INK), note("before activations")) \
            .arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        place(title_f, left=full.blocks["Adam · FP32 · 4.8 GB"].get_left()[0],
              bottom=full.blocks["Adam · FP32 · 4.8 GB"].get_top()[1] + 0.2)
        title_q = label("QLoRA in this notebook ≈ 0.9 GB", 26, INK)
        place(title_q, left=ql.blocks["4-bit linears · 0.22 GB"].get_left()[0],
              bottom=max(t.get_top()[1] for t in ql.tags.values()) + 0.3)
        inside(VGroup(t4, ql, fp32, title_q, title_f))
        assert fp32.get_right()[0] < t4.get_right()[0] - 0.1, fp32.get_right()
        # the lecture's 10 B column (slides 13–15): far taller than the frame; only its foot is drawn
        c_top = 2.75
        c_l, c_r = X_10B - 0.65, X_10B + 0.65
        big = VGroup(DashedLine([c_l, BASE, 0], [c_l, c_top, 0], dash_length=0.12),
                     DashedLine([c_r, BASE, 0], [c_r, c_top, 0], dash_length=0.12),
                     Line([c_l, BASE, 0], [c_r, BASE, 0])).set_stroke(S.GREY, 2.5)
        big_fill = Rectangle(width=1.3, height=c_top - BASE, stroke_width=0).set_fill(S.GREY, 0.12)
        big_fill.move_to([X_10B, (BASE + c_top) / 2, 0])
        big_l = VGroup(label("10 B", 24, INK), label("full", CAPTION, S.GREY)).arrange(DOWN, buff=0.06)
        place(big_l, cx=X_10B, bottom=BASE + 0.25)
        up = Arrow([X_10B, 1.75, 0], [X_10B, 3.0, 0], buff=0, color=S.GREY, stroke_width=4,
                   max_tip_length_to_length_ratio=0.25)
        up_l = label("120 GB", 24, INK)
        place(up_l, cx=X_10B, top=up.get_bottom()[1] - 0.1)
        t4_line = DashedLine([t4.get_right()[0], T4_TOP, 0], [c_r + 0.25, T4_TOP, 0], dash_length=0.1) \
            .set_stroke(S.GREY, 2)
        ctag = concept_tag()
        place(ctag, right=SAFE_R, top=BASE - 0.12)
        big_all = VGroup(big_fill, big, big_l, up, up_l)
        inside(VGroup(big_all, ctag))
        stack_f, stack_q = full.stack, ql.stack
        lr = None
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "13–15, 37–39")
            self.play(Create(t4), FadeIn(t4_l), run_time=0.8)
            vo.wait_until("by our own estimate")
            self.play(FadeIn(est, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Full fine-tuning would need")
            for name in full.order:
                self.play(GrowFromEdge(full.parts[name], DOWN), FadeIn(full.tags[name]), FadeIn(full.leads[name]),
                          run_time=0.5)
            self.play(FadeIn(title_f, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("this notebook's QLoRA")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(ql.parts[n], DOWN), FadeIn(ql.tags[n]),
                                                   FadeIn(ql.leads[n])) for n in ql.order], lag_ratio=0.4),
                      FadeIn(fp32), run_time=1.2)
            self.play(FadeIn(title_q, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("even full fine-tuning would fit a T4")
            self.play(flash(stack_f, INK, 1.06, 0.8), flash(stack_q, INK, 1.3, 0.8), run_time=0.8)
            self.play(t4.animate.set_stroke(INK, 3), t4_l.animate.set_color(INK), run_time=0.4)
            self.play(t4.animate.set_stroke(S.GREY, 2.5), t4_l.animate.set_color(S.GREY), run_time=0.4)
            vo.wait_until("The recipe matters")
            self.play(Create(t4_line), FadeIn(VGroup(big_fill, big, big_l), shift=LEFT * 0.4), run_time=0.8)
            self.play(FadeIn(ctag, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("to models that wouldn't")
            self.play(Create(up), FadeIn(up_l, shift=UP * 0.1), run_time=0.6)
            self.play(flash(up_l, INK, 1.2), run_time=0.6)
        beat0 = VGroup(t4, t4_l, est, full, ql, fp32, title_f, title_q, big_all, t4_line, ctag)

        # ========================================================== 1 · activations and gradient checkpointing
        chain = CheckpointChain()
        place(chain, cx=0, cy=0.45)
        inside(chain)
        ckpt = label("checkpoint", CAPTION, TURN)
        place(ckpt, cx=chain.nodes[2].get_center()[0], top=chain.nodes[2].get_bottom()[1] - 0.12)
        assert ckpt.get_bottom()[1] > chain.meter_frame.get_top()[1] + 0.05, ckpt.get_bottom()
        trade = label("compute for memory", 28, INK)
        place(trade, cx=0, top=chain.get_bottom()[1] - 0.45)
        on13 = chip("on since 1.3 (cell 36)", S.GREY, size=CAPTION)
        place(on13, cx=0, top=trade.get_bottom()[1] - 0.35)
        inside(on13)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(beat0), run_time=0.6)
            lr = lref_swap(self, lr, "57–64")
            self.play(FadeIn(chain.nodes[0]), FadeIn(chain.meter_frame), FadeIn(chain.meter_label), FadeIn(chain.fill),
                      run_time=0.5)
            vo.wait_until("the values each layer computes")
            self.play(*chain.store(0), run_time=0.4)
            for i in range(1, 5):
                self.play(FadeIn(chain.arrows[i - 1]), FadeIn(chain.nodes[i]), run_time=0.3)
                self.play(*chain.store(i), run_time=0.35)
            vo.wait_until("kept for the backward pass")
            self.play(flash(chain.fill, TURN, 1.08), run_time=0.7)
            vo.wait_until("Gradient checkpointing")
            self.play(FadeIn(ckpt, shift=DOWN * 0.1), chain.nodes[2].circle.animate.set_stroke(TURN, 4), run_time=0.5)
            vo.wait_until("keeps only a few")
            drops = []
            for i in (0, 1, 3, 4):
                drops += chain.drop(i)[:1]
            chain.level = 1
            self.play(*drops, chain._meter(1), run_time=0.8)
            vo.wait_until("recomputes the rest")
            self.play(*chain.recompute(2, 3), run_time=0.9)
            vo.wait_until("compute traded for memory")
            self.play(FadeIn(trade, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(on13, shift=UP * 0.1), run_time=0.4)
        beat1 = VGroup(chain, ckpt, trade, on13, chain.replay)

        # ========================================================== 2 · the training arguments (4.2); paging; ▶
        tr = tracker("Tune", 2)
        p70 = src_panel(CELL70, [3, (5, 7), 10, (12, 13), 15], size=20, cut_comments=True)
        place(p70, left=-6.3, top=2.72)
        yt = your_turn()
        place(yt, right=SAFE_R, bottom=p70.code.get_top()[1] + 0.1)
        pg = paging_row()
        place(pg, left=-6.3, top=p70.get_bottom()[1] - 0.25)
        foot = note("our ≈ 18 MB never needs it")
        place(foot, left=pg.get_right()[0] + 0.4, cy=pg.cpu.get_center()[1])
        inside(VGroup(p70, yt, pg, foot))
        assert yt.get_left()[0] > p70.header.get_right()[0] + 0.15, (yt.get_left(), p70.header.get_right())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(beat1), FadeOut(lr), run_time=0.5)
            lr = None
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(p70, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("Sequences are capped")
            b3 = p70.bar(3)
            self.play(FadeIn(b3), p70.span(3, "512").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("grouped by length")
            b15 = p70.bar(15)
            self.play(FadeOut(b3), FadeIn(b15), run_time=0.5)
            vo.wait_until("2 epochs")
            b56 = VGroup(p70.bar(5), p70.bar(6))
            self.play(FadeOut(b15), FadeIn(b56), run_time=0.5)
            vo.wait_until("and a learning rate")
            b10 = p70.bar(10)
            self.play(FadeOut(b56), FadeIn(b10), run_time=0.5)
            vo.wait_until("The optimizer is")
            b7 = p70.bar(7)
            self.play(FadeOut(b10), FadeIn(b7), run_time=0.5)
            self.play(FadeIn(yt, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("Paging moves")
            lr = lref_swap(self, lr, "65")
            self.play(FadeIn(pg), run_time=0.6)
            vo.wait_until("when the GPU fills up")
            outs = [pg.pages[5 - j].animate.move_to(pg.cpu.get_center() + RIGHT * (0.45 - 0.45 * j))
                    for j in range(3)]
            self.play(*outs, run_time=1.0)
            vo.wait_until("Ours never needs to")
            home = pg.pages.copy().arrange(RIGHT, buff=0.1).move_to(pg.gpu)
            self.play(*[pg.pages[5 - j].animate.move_to(home[5 - j]) for j in range(3)], run_time=0.9)
            self.play(FadeIn(foot, shift=UP * 0.1), run_time=0.4)
        self.wait(2)

        # ========================================================== 3 · fp16 on, bf16 off: the bit strips
        p13 = src_panel(CELL70, 12, 13, size=20, cut_comments=True)
        place(p13, left=-6.3, top=2.84)
        bits = BitStrips()
        place(bits, cx=0, top=p13.get_bottom()[1] - 0.15)
        t4bf = grey_box([label("T4: no fast BF16 → FP16 here", CAPTION, INK),
                         label("(lecture: BF16 for QLoRA)", CAPTION, S.GREY)])
        place(t4bf, right=SAFE_R - 0.05, cy=p13.code.get_center()[1])
        rec31 = recorded_box("colab-c31-gpu-bf16-check", *wrapped(C31, 9, 70))
        place(rec31, left=-6.3, bottom=-3.5)
        assert t4bf.get_left()[0] > p13.get_right()[0] + 0.2 and rec31.get_top()[1] < bits.get_bottom()[1] - 0.1, \
            (t4bf.get_left(), p13.get_right(), rec31.get_top(), bits.get_bottom())
        inside(VGroup(p13, bits, t4bf, rec31))
        fp32, fp16, bf16 = bits.rows["FP32"], bits.rows["FP16"], bits.rows["BF16"]
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(pg, foot, b7, yt)), run_time=0.4)
            lr = lref_swap(self, lr, "66–67")
            b1213 = VGroup(p70.bar(12), p70.bar(13))
            self.play(FadeIn(b1213), run_time=0.5)
            # lines 12–13 fly from the folded panel into the small one (what became what)
            src = VGroup(*[p70.code.code_lines[k] for n in (12, 13) for k in p70.rows_of(n)])
            dst = VGroup(*[p13.code.code_lines[k] for n in (12, 13) for k in p13.rows_of(n)])
            fly = src.copy()
            self.add(fly)
            self.play(FadeOut(b1213), FadeOut(p70), Transform(fly, dst.copy()), run_time=0.7)
            self.play(FadeIn(p13), run_time=0.4)
            self.remove(fly)
            self.play(FadeIn(VGroup(fp32, fp16, bf16)), run_time=0.6)
            vo.wait_until("BF16 keeps the range")
            self.play(FadeIn(bits.legend), run_time=0.5)
            self.play(flash(fp32.exp, BIT_EXP, 1.1), flash(bf16.exp, BIT_EXP, 1.1), run_time=0.8)
            vo.wait_until("with less precision")
            self.play(flash(bf16.frac, BIT_FRAC, 1.2), run_time=0.7)
            vo.wait_until("and the lecture uses it")
            self.play(flash(bf16.name_text, INK, 1.3), run_time=0.6)
            vo.wait_until("The T4 has no fast BF16")
            self.play(FadeIn(t4bf, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(rec31, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("so this notebook computes in FP16")
            bar12 = p13.bar(12)
            self.play(flash(fp16.name_text, TURN, 1.3), FadeIn(bar12), run_time=0.7)
        beat3 = VGroup(p13, bits, t4bf, rec31, bar12)

        # ========================================================== 4 · the trainer (4.3): adapters back to FP32; the count
        p72 = src_panel(CELL72, 10, 14, size=20, wrap=True)
        place(p72, left=-6.3, top=2.84)
        blk = LoraBlock(show=("x", "w0", "ab", "sum", "h", "wires"))
        blk.rescale(K_BLK)
        blk.parts["w0"][3].next_to(blk.w0, LEFT, buff=0.12)
        for node in (blk.x_node, blk.h_node, blk.plus):       # the labels keep 28 pt: widen their circles
            node[0].scale(NODE_K)
            node.set_z_index(1)
        blk.h_node.shift(UP * 0.07)                     # the widened h and + circles no longer touch
        blk.w_h.put_start_and_end_on(blk.plus.get_top(), blk.h_node.get_bottom())
        place(blk, left=-5.4, top=p72.get_bottom()[1] - 0.035)
        tag_a, tag_b = dtype_tag("BF16"), dtype_tag("BF16")
        tag_a.next_to(blk.a, RIGHT, buff=0.12)
        tag_b.next_to(blk.b, RIGHT, buff=0.12)
        tag_a2, tag_b2 = dtype_tag("FP32"), dtype_tag("FP32")
        tag_a2.move_to(tag_a, aligned_edge=LEFT)
        tag_b2.move_to(tag_b, aligned_edge=LEFT)
        rec72 = recorded_box("colab-c72-sfttrainer-trainable", *wrapped(C72, 23, 56))
        place(rec72, left=-6.3, top=2.72)
        ctr = Counter("our count", TRAINABLE, OWN, size=26).freeze()
        tick = tick_mark(0.32)
        VGroup(ctr, tick).arrange(RIGHT, buff=0.25)
        place(VGroup(ctr, tick), left=max(tag_b.get_right()[0], tag_a.get_right()[0]) + 0.6, cy=blk.w0.get_center()[1])
        inside(VGroup(p72, blk, rec72, ctr, tick))
        assert rec72.get_bottom()[1] > blk.get_top()[1] + 0.1, (rec72.get_bottom(), blk.get_top())
        num_row = next(r for r in rec72.rows if "1146880" in r.text)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(beat3), FadeOut(lr), run_time=0.5)
            lr = None
            self.play(tr.goto(3), FadeIn(p72, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("The trainer turns the adapters")
            self.play(*blk.parts_in("x", "w0", "ab", "sum", "h", "wires"), run_time=0.8)
            self.play(FadeIn(tag_a, scale=0.8), FadeIn(tag_b, scale=0.8), run_time=0.4)
            vo.wait_until("which FP16 training cannot unscale")
            # RED outline and text (a filled Indicate would hide the text on its pill)
            self.play(*[m.animate.set_stroke(ERR, 3) for m in (tag_a.box, tag_b.box)],
                      *[m.animate.set_color(ERR) for m in (tag_a.text, tag_b.text)], run_time=0.5)
            self.play(flash(VGroup(tag_a.text, tag_b.text), ERR, 1.2, 0.6), run_time=0.6)
            vo.wait_until("so this cell casts them back")
            bars = VGroup(*[p72.bar(n) for n in (12, 13, 14)])
            self.play(FadeIn(bars), run_time=0.4)
            self.play(ReplacementTransform(tag_a, tag_a2), ReplacementTransform(tag_b, tag_b2), run_time=0.7)
            self.play(flash(VGroup(tag_a2.text, tag_b2.text), OWN, 1.2), run_time=0.5)
            vo.wait_until("And the count confirms")
            self.play(FadeOut(bars), FadeOut(p72, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(rec72, shift=UP * 0.1), run_time=0.5)
            self.play(substring(num_row, "1146880").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("1,146,880 trainable parameters")
            self.play(FadeIn(ctr, shift=UP * 0.1), run_time=0.5)
            self.play(flash(ctr.num, OWN, 1.15), Create(tick), run_time=0.6)
        beat4 = VGroup(rec72, ctr, tick, tag_a2, tag_b2)

        # ========================================================== 5 · the backward pass: through W₀, into B and A
        big_blk = blk.copy()
        big_blk.rescale(1 / K_BLK)
        for node in (big_blk.x_node, big_blk.h_node, big_blk.plus):
            node[0].scale(1 / NODE_K)
        big_blk.h_node.move_to(big_blk.plus.get_center() + UP * 0.75)     # LoraBlock's own spacing
        big_blk.w_h.put_start_and_end_on(big_blk.plus.get_top(), big_blk.h_node.get_bottom())
        big_blk.parts["w0"][3].next_to(big_blk.w0, LEFT, buff=0.15)
        place(big_blk, cx=0, top=2.75)
        grad = grey_box([label("lecture: gradients flow only through the adapters", CAPTION, INK),
                         label("precisely: through W₀ too, but W₀ gets no gradient", CAPTION, S.GREY)])
        place(grad, cx=0, bottom=-3.45)
        upd = label("updated", CAPTION, OWN)
        nograd = label("no gradient · no update", CAPTION, S.GREY)
        inside(VGroup(big_blk, grad))
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(beat4), run_time=0.5)
            lr = lref_swap(self, lr, "29, 70")
            self.play(Transform(blk, big_blk), run_time=0.9)
            place(upd, left=blk.b.get_right()[0] + 0.15, cy=blk.b.get_center()[1])
            frz = blk.parts["w0"][3]
            place(nograd, right=frz.get_right()[0], top=frz.get_bottom()[1] - 0.12)
            assert nograd.get_right()[0] < blk.w0.get_left()[0] and nograd.get_left()[0] > SAFE_L, nograd.get_left()
            assert nograd.get_bottom()[1] > grad.get_top()[1] + 0.1 and upd.get_right()[0] < SAFE_R
            vo.wait_until("the gradient flows down")
            # the pulse runs down step by step: h → ⊕ → both branches → through W₀ and B, A → x
            self.play(down(blk.w_h, 0.45))
            self.play(down(blk.w_out_l, 0.6), down(blk.w_out_r, 0.6))
            self.play(down(Line(blk.w0.get_top(), blk.w0.get_bottom()), 0.8),
                      down(Line(blk.b.get_top(), blk.a.get_bottom()), 0.8),
                      blk.w0.animate.set_fill(FROZEN, 0.12),
                      Indicate(blk.a, color=OWN, scale_factor=1.08), Indicate(blk.b, color=OWN, scale_factor=1.08),
                      run_time=0.8)
            self.play(down(blk.w_in_l, 0.6), down(blk.w_in_r, 0.6))
            vo.wait_until("and only B and A are updated")
            self.play(flash(VGroup(blk.a, blk.b), OWN, 1.15, 0.7), FadeIn(upd, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("W naught is used")
            self.play(FadeIn(grad, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("it just gets no gradient")
            self.play(flash(blk.parts["w0"][2], INK, 1.6, 0.7), FadeIn(nograd, shift=UP * 0.1), run_time=0.7)
        beat5 = VGroup(blk, upd, nograd, grad)

        # ========================================================== 6 · train (4.4): 450 steps, the loss curve; TensorBoard (4.5); ▶
        rows75 = [C75.line(5)] + [C75.line(n).expandtabs(8) for n in range(6, 16)]
        rec75 = recorded_box("colab-c75-train", *rows75, tag_at="down")
        place(rec75, left=-6.3, top=2.55)
        curve = LossCurve(width=4.9, height=3.2)
        place(curve, right=6.25, top=2.0)
        ctag75 = recorded_tag()
        place(ctag75, right=6.25, top=curve.get_bottom()[1] - 0.15)
        inside(VGroup(rec75, curve, ctag75))
        assert rec75.frame.get_right()[0] < curve.get_left()[0] - 0.3, (rec75.frame.get_right(), curve.get_left())
        assert rec75.header.get_bottom()[1] > curve.get_top()[1] + 0.1, rec75.header.get_bottom()
        assert rec75.tag.get_top()[1] < curve.get_bottom()[1] - 0.05 or rec75.tag.get_right()[0] < curve.get_left()[0]
        r450 = rec75.rows[0]
        vals = [substring(rec75.rows[2 + i], f"{v:.6f}") for i, (_, v) in enumerate(LOSS)]
        arith = chip("900 / 4 × 2 = 450", S.GREY, size=24)
        r450_t = r450.copy()
        place(r450_t, left=-6.1, top=2.0)
        arith_end = arith.copy()
        place(arith_end, left=-6.1, top=r450_t.get_bottom()[1] - 0.4)
        place(arith, right=6.25, bottom=curve.get_top()[1] + 0.15)    # beside the table while it is said
        inside(arith)
        assert arith.get_left()[0] > rec75.frame.get_right()[0] + 0.3, arith.get_left()
        rec77 = recorded_box("colab-c77-tensorboard", *wrapped(C77, 4, 36), tag_at="down")
        place(rec77, left=-6.3, top=arith_end.get_top()[1] + 0.05)
        own = note("open it in your own run")
        place(own, left=-6.1, top=rec77.get_bottom()[1] - 0.25)
        yt6 = your_turn()
        place(yt6, left=-6.1, top=own.get_bottom()[1] - 0.35)
        inside(VGroup(rec77, own, yt6, arith_end))
        assert rec77.get_right()[0] < curve.get_left()[0] - 0.2, (rec77.get_right(), curve.get_left())
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(beat5), FadeOut(lr), run_time=0.5)
            lr = None
            self.play(tr.goto(4), FadeIn(rec75, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("900 examples")
            self.play(FadeIn(arith, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("is 450 steps")
            self.play(r450.animate.set_color(TURN), flash(VGroup(*arith.text[-3:]), TURN, 1.3), run_time=0.6)
            self.play(flash(r450, TURN, 1.08), run_time=0.6)
            vo.wait_until("3 minutes and 36 seconds")
            self.play(flash(substring(r450, "03:36"), TURN, 1.3), run_time=0.6)
            vo.wait_until("The notebook says 6 to 7 minutes")
            self.play(FadeIn(curve.axes), run_time=0.7)
            self.play(LaggedStart(*[TransformFromCopy(v, d) for v, d in zip(vals, curve.dots)], lag_ratio=0.15),
                      run_time=1.8)
            vo.wait_until("The loss falls")
            self.play(Create(curve.curve), run_time=1.2)
            self.play(flash(curve.dots[0], OWN, 2.2), flash(curve.dots[-1], OWN, 2.2), run_time=0.7)
            self.play(FadeOut(VGroup(*[m for m in rec75 if m is not rec75.rows])),
                      FadeOut(VGroup(*rec75.rows[1:])), r450.animate.move_to(r450_t), FadeIn(ctag75),
                      arith.animate.move_to(arith_end), run_time=0.8)
            vo.wait_until("Step 5, TensorBoard")
            self.play(tr.goto(5), FadeOut(arith), FadeIn(rec77, shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(own, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("Pause and train")
            self.play(FadeIn(yt6, shift=LEFT * 0.15), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(VGroup(tr, curve, ctag75, r450, rec77, own, yt6)), run_time=0.8)
        self.wait(0.3)
