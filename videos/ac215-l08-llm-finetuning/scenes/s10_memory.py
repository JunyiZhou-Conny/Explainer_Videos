"""S10 · Colab, and the 120 GB bill (Colab › Part A · Setup; then the lecture's memory ladder).
Lecture: 11–16, 37–39, 71–72. Opens part 2.

Beats (script.md "## S10", one voiceover block each):
 0  The BLUE Colab frame "QLoRA notebook · Colab" (tag `illustration`; its tab and tag sit on the
    right half of the top border, clear of the tracker), the notebook's title inside. TRACKER
    ColabA 1: schematic File › Save a copy in Drive, the second chip lights YELLOW (cell-01.md),
    GREY note "the original is view-only". TRACKER ColabA 2: Runtime › Change runtime type, then a
    schematic "Change runtime type" dialog; "T4 GPU" selected (YELLOW); GOLD chip "A100 · L4: Pro or
    compute units".
 1  TRACKER ColabA 3. CODE(colab/cell-08.py: 1–7) (long lines wrapped), header "QLoRA notebook · 3 ·
    cell 8 · lines 1–7"; lines 3–4 and 7 light. Below it, as the cell's output area (no second
    header: the cell is named just above), RECORDED(expected/colab-c08-install: 13, 18, 21):
    `+ bitsandbytes==0.50.2`, `+ trl==1.14.0` GREEN, `- torchao==0.10.0` GREY; tags `recorded …` and
    `at the time of recording` inside the output area's right end.
 2  One slot below the tracker; each step replaces the previous one. TRACKER ColabA 4: a schematic
    Secrets panel (illustration): HF_TOKEN, a row of GREY dots, "notebook access" switch on;
    RECORDED(c10: 13); GREY chip "SecretNotFoundError? name it HF_TOKEN · turn notebook access on";
    on "both models are public" a GREY note "both models are public: the token matters mostly for the
    optional upload (6.3)" (not in SHOW: the SAY's clause otherwise had nothing moving for 5 s).
    TRACKER ColabA 5: the Secrets panel Transforms into RECORDED(c12: 32, wrapped) + `at the time of
    recording`, torch and transformers versions light; then RECORDED(c14: 6) below it. TRACKER ColabA
    6: RECORDED(c16: 7–8, each cut after the model folder); the Drive path Transforms into a GREY
    Drive folder glyph `MyDrive/LLM_cache`, the two model folders into two model boxes inside it.
    The GREY "your turn" card (YELLOW ▶): "Save a copy · T4 runtime · HF_TOKEN secret · run Part A,
    sections 3 to 6", GREEN "T4: free (when available)", GOLD "A100 / L4: compute units". 2 s hold.
 3  LECTURE 11–16. The tracker leaves; the Colab frame shrinks to a small BLUE chip top left. A GREY
    dashed model block "10 B parameters" (`concept · lecture only`) pours into a column: the first
    slab "Parameters · FP16 · 20 GB". PONDER(8 s) with the GREY hint "the optimizer is Adam, kept in
    32-bit"; the column stops (the card sits below it).
 4  The ponder card leaves; the column settles to the floor. V5: Gradients · FP16 · 20 GB and
    Optimizer states · FP32 · 80 GB (momentum + variance) stack in proportion 1 : 1 : 4; "120 GB"
    writes under it. Five GREY dashed 24 GB GPU tiles line up (the concept tag moves onto them) and
    a copy of the column pours into them, filling all five.
 5  LECTURE 37–39. The tiles leave; the column copies twice to the right. LoRA: gradients and
    optimizer slabs turn GREEN and shrink to two small blocks "A, B"; the 20 GB parameters slab stays
    GREY with a snowflake beside it ("frozen, but needed for the forward pass"); dashed outline up to 40 GB,
    "≈ 40 GB" + GREY tag "the lecture's total". LECTURE 71–72. QLoRA: the base shrinks to a thin
    "4-bit" block (tag NF4), A and B GREEN; a small GREY optimizer page pages out along a PINK arrow
    into a "CPU" box; "≈ 12 GB" + "the lecture's total". (The slabs are not drawn to add up to the
    two totals: the lecture gives totals only; the dashed outlines hold the rest.) GREY arrows join
    the totals 120 → ≈ 40 → ≈ 12, names "full", "LoRA", "QLoRA" over the columns. Everything fades to
    an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromEdge,
    Indicate,
    ReplacementTransform,
    LaggedStart,
    Rectangle,
    RoundedRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
    linear,
)

from common import *  # noqa: F401,F403
from common import _arrow, _with_header
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S10"]

# ------------------------------------------------------------------ the real sources and captures
CELL08 = "colab/cell-08.py"
assert source_line(CELL08, 3).startswith("!uv pip install transformers==5.16.1"), source_line(CELL08, 3)
assert source_line(CELL08, 4) == "!uv pip install trl==1.14.0" and source_line(CELL08, 7) == "!uv pip uninstall torchao"
assert "peft refuses to add LoRA layers" in source_line(CELL08, 6), source_line(CELL08, 6)
assert "Save a copy in Drive" in source_text("colab/cell-01.md") and "view-only" in source_text("colab/cell-01.md")
C08 = capture("expected/colab-c08-install")
assert C08.line(13) == " + bitsandbytes==0.50.2" and C08.line(18) == " + trl==1.14.0", (C08.line(13), C08.line(18))
assert C08.line(21) == " - torchao==0.10.0", C08.line(21)
C10 = capture("expected/colab-c10-hf-token")
assert C10.line(13) == "Hugging Face token successfully loaded.", C10.line(13)
C12 = capture("expected/colab-c12-versions")
assert C12.line(32).startswith("torch 2.11.0+cu128 | transformers 5.16.1"), C12.line(32)
C14 = capture("expected/colab-c14-drive-mount")
assert C14.line(6) == "Mounted at /content/drive", C14.line(6)
C16 = capture("expected/colab-c16-hf-download")
DRIVE = "/content/drive/MyDrive/LLM_cache/"
OPT_DIR, QWEN_DIR = "models--facebook--opt-350m", "models--Qwen--Qwen3-0.6B"
assert C16.line(7).startswith(DRIVE + OPT_DIR) and C16.line(8).startswith(DRIVE + QWEN_DIR), C16.line(8)
NOTEBOOK = "Tutorial - Finetuning with QLoRA"

# ------------------------------------------------------------------ layout
SAFE_R = 6.45
SLOT_TOP = 2.45                    # top of the one slot inside the Colab frame (below the border)
BASE_Y = -2.3                      # the memory columns' floor (beats 4-5)
PONDER_BASE = -0.3                 # the column's floor while the ponder card sits under it
SCALE = 0.035                      # GB -> units (120 GB = 4.2), the same as gpu_tiles()
X_FULL, X_LORA, X_QLORA = -5.6, -2.4, 2.0
X_FULL_4 = -4.6                    # the full column's x while it stands alone (beats 3-4)
PARAM, GRAD, OPT = "Parameters (FP16)", "Gradients (FP16)", "Optimizer states (FP32)"


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


class Column(MemoryColumn):
    """V5's column with thinner minimum blocks (A and B, the optimizer page: not to scale)."""
    MIN_H = 0.08


def full_column(x: float, base: float) -> Column:
    """The lecture's 10 B column (slide 14): 20 + 20 + 80 GB, bare (labels drawn by the scene)."""
    c = Column(LADDER["full"], labels=False, scale=SCALE)
    c.shift(RIGHT * x + UP * base)
    return c


def colab_notebook() -> VGroup:
    """colab_frame() with its tab and `illustration` tag moved to the right half of the top border
    (the tracker owns the top-left corner). .frame .title .tag"""
    cf = colab_frame(top=2.75, bottom=-3.5)
    fr = cf.frame
    cf.title.move_to([fr.get_right()[0] - 0.4 - cf.title.width / 2, fr.get_top()[1], 0])
    cf.tag.move_to([cf.title.get_left()[0] - 0.3 - cf.tag.width / 2, fr.get_top()[1], 0])
    return cf


def runtime_dialog() -> VGroup:
    """A schematic "Change runtime type" dialog (illustration): Hardware accelerator, four options.
    .frame .options {name: chip} .head"""
    head = label("Change runtime type", 26, INK)
    hw = label("Hardware accelerator", CAPTION, S.GREY)
    names = ["CPU", "T4 GPU", "L4 GPU", "A100 GPU"]
    opts = {n: chip(n, S.GREY, size=CAPTION, fill_opacity=0.0) for n in names}
    row = VGroup(*opts.values()).arrange(RIGHT, buff=0.3)
    body = VGroup(head, hw, row).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    fr = box(body.width + 0.7, body.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.options, g.head = fr, opts, head
    return g


def switch_on() -> VGroup:
    """A toggle switch, on (knob right)."""
    pill = RoundedRectangle(width=0.62, height=0.32, corner_radius=0.16, stroke_color=INK, stroke_width=2)
    pill.set_fill(S.GREY, 0.6)
    knob = Dot(radius=0.11, color=INK).move_to(pill.get_right() + LEFT * 0.16)
    return VGroup(pill, knob)


def secrets_panel() -> VGroup:
    """A schematic Colab Secrets panel (the Colab frame carries its `illustration` tag): HF_TOKEN, its
    value as GREY dots (never a token), the "notebook access" switch on. .frame .row .name .body"""
    head = VGroup(key_outline(0.26, S.GREY), label("Secrets", 26, INK)).arrange(RIGHT, buff=0.2)
    name = mono("HF_TOKEN", CAPTION, INK)
    dots = VGroup(*[Dot(radius=0.045, color=S.GREY) for _ in range(10)]).arrange(RIGHT, buff=0.09)
    acc = VGroup(label("notebook access", CAPTION, INK), switch_on()).arrange(RIGHT, buff=0.2)
    row = VGroup(name, dots, acc).arrange(RIGHT, buff=0.55)
    body = VGroup(head, row).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    fr = box(body.width + 0.7, body.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.row, g.name, g.body = fr, row, name, body
    return g


def drive_folder() -> VGroup:
    """A GREY Drive folder `MyDrive/LLM_cache` holding two model boxes. .body .path .models"""
    body = RoundedRectangle(width=6.2, height=1.55, corner_radius=0.12, stroke_color=S.GREY, stroke_width=2.5)
    body.set_fill(S.GREY, 0.12)
    tab = RoundedRectangle(width=2.4, height=0.3, corner_radius=0.08, stroke_color=S.GREY, stroke_width=2.5)
    tab.set_fill(S.GREY, 0.12)
    tab.next_to(body, UP, buff=-0.05).align_to(body, LEFT)
    path = mono("MyDrive/LLM_cache", CAPTION, INK)
    path.next_to(body, UP, buff=0.08).align_to(tab, RIGHT).shift(RIGHT * (path.width + 0.25))
    m1 = model_box("opt-350m", w=2.4, h=0.8, color=S.GREY)
    m2 = model_box("Qwen3-0.6B", w=2.4, h=0.8, color=S.GREY)
    models = VGroup(m1, m2).arrange(RIGHT, buff=0.5).move_to(body)
    g = VGroup(tab, body, path, models)
    g.body, g.path, g.models, g.tab = VGroup(tab, body), path, models, tab
    return g


def mini_colab() -> VGroup:
    """The Colab frame shrunk to a corner: a small BLUE box with the notebook title. .frame .text"""
    t = label(COLAB_TITLE, 22, CLOUD)
    fr = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.3, corner_radius=0.14, stroke_color=CLOUD,
                          stroke_width=3).set_fill(CLOUD, 0.03)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return place(g, left=-6.5, top=3.55)


def ponder_hint(scene, question: str, hint: str, seconds: float = 8.0, y: float = -2.4) -> VGroup:
    """ponder_at() with a GREY hint row under the question (the card grows to hold it)."""
    card = ponder_card(question, width=10.2)
    fr, q, bar = card[0], card[2], card[3]
    h = note(hint)
    h.next_to(q, DOWN, buff=0.22)
    grow = h.height + 0.22
    nf = RoundedRectangle(width=fr.width, height=fr.height + grow, corner_radius=0.2, stroke_color=S.YELLOW,
                          stroke_width=3).set_fill(S.BG, 1)
    nf.align_to(fr, UP).set_x(fr.get_center()[0])
    card.submobjects[0] = nf
    bar.shift(DOWN * grow)
    card.add(h)
    card.move_to([0, y, 0])
    if card.get_bottom()[1] < -3.55:
        card.shift(UP * (-3.55 - card.get_bottom()[1]))
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    scene.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
               run_time=seconds)
    return card


def block_label(rows, color: str = INK) -> VGroup:
    """A block label: the first row in `color`, further rows GREY, left-aligned."""
    g = VGroup(*[label(r, CAPTION, color if k == 0 else S.GREY) for k, r in enumerate(rows)])
    return g.arrange(DOWN, aligned_edge=LEFT, buff=0.06)


def restack_green(col: Column, gbs: dict, names, run_time: float = 1.2) -> list:
    """col.restack(gbs) with the named blocks turning GREEN (A and B) as they shrink: one play."""
    anims = col.restack(gbs, run_time)
    targets = [col.blocks[n] for n in names]
    for a in anims:
        if isinstance(a, Transform) and any(a.mobject is b for b in targets):
            a.target_mobject.set_stroke(ADAPTER).set_fill(ADAPTER, 0.45)
    return anims


def outline_to(col: Column, gb: float) -> VMobject:
    """A GREY dashed box from the top of col's stack up to `gb` (the lecture's un-itemized rest)."""
    top_stack = col.blocks[col.order[-1]].get_top()[1]
    base = col.blocks[col.order[0]].get_bottom()[1]
    top = base + gb * SCALE
    h = max(0.05, top - top_stack)
    o = DashedVMobject(Rectangle(width=col.col_w, height=h), num_dashes=max(8, int((col.col_w + h) * 8)),
                       dashed_ratio=0.5)
    o.set_stroke(S.GREY, 2).move_to([col.blocks[col.order[0]].get_center()[0], top_stack + h / 2, 0])
    return o


class MemoryBill(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)

        # ========================================================== 0 · copy the notebook, pick a GPU runtime
        tr = tracker("ColabA", 1)
        cf = colab_notebook()
        title = label(NOTEBOOK, 30, INK)
        place(title, left=-6.0, top=SLOT_TOP)
        mp1 = menu_path(["File", "Save a copy in Drive"])
        place(mp1, left=-6.0, cy=1.25)
        view = note("the original is view-only")
        place(view, left=mp1.get_right()[0] + 0.4, cy=mp1.get_center()[1])
        mp2 = menu_path(["Runtime", "Change runtime type"])
        place(mp2, left=-6.0, cy=0.2)
        dlg = runtime_dialog()
        place(dlg, left=-6.0, top=-0.35)
        paid = chip("A100 · L4: Pro or compute units", COST, size=CAPTION)
        place(paid, left=dlg.get_right()[0] + 0.4, cy=dlg.options["A100 GPU"].get_center()[1])
        assert paid.get_right()[0] < SAFE_R - 0.1, paid.get_right()
        assert dlg.get_bottom()[1] > -3.4, dlg.get_bottom()
        t4 = dlg.options["T4 GPU"]
        with self.voiceover(SAY[0]) as vo:
            self.play(Create(cf.frame), FadeIn(cf.title), FadeIn(cf.tag), run_time=0.8)
            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("First")
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(mp1, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("Save a copy in Drive")
            self.play(mp1.light(1), run_time=0.5)
            vo.wait_until("the original is view-only")
            self.play(FadeIn(view, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Then")
            self.play(tr.goto(2), FadeIn(mp2, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("Change runtime type")
            self.play(mp2.light(1), run_time=0.4)
            self.play(FadeIn(dlg, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("A free T4")
            self.play(t4.box.animate.set_stroke(TURN, 3).set_fill(TURN, 0.15), t4.text.animate.set_color(TURN),
                      run_time=0.5)
            self.play(flash(t4, TURN, 1.12), FadeIn(paid, shift=LEFT * 0.1), run_time=0.7)

        # ========================================================== 1 · section 3: install
        p8 = src_panel(CELL08, 1, 7, size=20,
                       wrap={1: ["datasets"], 3: ["huggingface-hub"], 6: ["a full-precision"]})
        _with_header(p8, "QLoRA notebook · 3 · cell 8 · lines 1–7 · long lines wrapped")
        place(p8, cx=0, top=SLOT_TOP + 0.05)
        out8 = recorded_box("colab-c08-install", (C08.line(13), OWN), (C08.line(18), OWN), (C08.line(21), S.GREY),
                            header="", tag_=False, width=p8.code.width if hasattr(p8, "code") else 12.4)
        place(out8, left=p8.get_left()[0], top=p8.get_bottom()[1] - 0.12)
        rtag8 = recorded_tag()
        vtag8 = recording_tag()
        tags8 = VGroup(rtag8, vtag8).arrange(DOWN, aligned_edge=RIGHT, buff=0.15)
        place(tags8, right=out8.frame.get_right()[0] - 0.25, cy=out8.frame.get_center()[1])
        assert tags8.get_left()[0] > out8.rows.get_right()[0] + 0.3, (tags8.get_left(), out8.rows.get_right())
        assert out8.get_bottom()[1] > -3.4, out8.get_bottom()
        b3, b4 = p8.bar(3), p8.bar(4)               # one bar over lines 3-4 (two overlapped in a seam)
        b_top, b_bot = b3.get_top()[1], b4.get_bottom()[1]
        bars8 = VGroup(Rectangle(width=b3.width, height=b_top - b_bot, stroke_width=0)
                       .set_fill(TURN, 0.18).move_to([b3.get_center()[0], (b_top + b_bot) / 2, 0]))
        bar7 = p8.bar(7)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(title, mp1, view, mp2, dlg, paid)), run_time=0.5)
            self.play(tr.goto(3), FadeIn(p8, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("Section 3 pins")
            self.play(FadeIn(bars8), run_time=0.5)
            self.play(FadeIn(out8.frame), FadeIn(out8.rule), FadeIn(out8.rows[0]), FadeIn(out8.rows[1]),
                      FadeIn(tags8), run_time=0.6)
            self.play(flash(VGroup(out8.rows[0], out8.rows[1]), OWN, 1.06), run_time=0.6)
            vo.wait_until("and removes torchao")
            self.play(FadeIn(bar7), FadeIn(out8.rows[2], shift=UP * 0.05), run_time=0.5)
            vo.wait_until("which, the notebook notes")
            why = p8.span(6, "peft refuses to add LoRA layers")
            self.play(why.animate.set_color(TURN), run_time=0.5)
            self.play(flash(why, TURN, 1.06), run_time=0.7)

        # ========================================================== 2 · sections 4-6: token, imports + Drive, download; your turn
        sec = secrets_panel()
        place(sec, cx=0, top=SLOT_TOP - 0.05)
        out10 = recorded_box("colab-c10-hf-token", 13)
        place(out10, cx=0, top=sec.get_bottom()[1] - 0.3)
        nf = chip("SecretNotFoundError? name it HF_TOKEN · turn notebook access on", S.GREY, size=CAPTION)
        place(nf, cx=0, top=out10.get_bottom()[1] - 0.3)
        pub = note("both models are public: the token matters mostly for the optional upload (6.3)")
        place(pub, cx=0, top=nf.get_bottom()[1] - 0.25)
        assert pub.get_bottom()[1] > -3.4, pub.get_bottom()
        v32 = [r for r, *_ in wrap_output(C12.line(32), 65)]
        out12 = recorded_box("colab-c12-versions", *v32)
        place(out12, cx=0, top=SLOT_TOP - 0.05)
        vtag12 = recording_tag()
        place(vtag12, left=out12.frame.get_left()[0], top=out12.frame.get_bottom()[1] - 0.1)
        out14 = recorded_box("colab-c14-drive-mount", 6)
        place(out14, cx=0, top=vtag12.get_bottom()[1] - 0.3)
        out16 = recorded_box("colab-c16-hf-download", C16.cut(7, OPT_DIR), C16.cut(8, QWEN_DIR))
        place(out16, cx=0, top=SLOT_TOP - 0.05)
        drv = drive_folder()
        place(drv, cx=0, top=out16.get_bottom()[1] - 0.3)
        tc = turn_card([["Save a copy · T4 runtime ·", "`HF_TOKEN`", "secret · run Part A, sections 3 to 6"],
                        (Prose("T4: free (when available)"), OWN),
                        (Prose("A100 / L4: compute units"), COST)])
        drv_up = SLOT_TOP - 0.1 - drv.get_top()[1]        # the folder rises into the slot when the card comes
        place(tc, cx=0, top=drv.get_bottom()[1] + drv_up - 0.45)
        assert tc.get_bottom()[1] > -3.4, tc.get_bottom()
        r16a, r16b = out16.rows[0], out16.rows[1]
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p8, bars8, bar7, out8, tags8)), run_time=0.5)
            self.play(tr.goto(4), FadeIn(sec, shift=UP * 0.15), run_time=0.6)
            self.play(flash(sec.name, TURN, 1.15), run_time=0.6)
            self.play(FadeIn(out10, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(nf, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("both models are public")
            self.play(FadeIn(pub, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Section 5 imports")
            self.play(FadeOut(VGroup(out10, nf, pub)), run_time=0.4)
            sg = VGroup(sec.frame, sec.body)
            self.play(tr.goto(5), Transform(sg, out12.frame.copy()), run_time=0.7)
            self.remove(sg, sec)
            self.add(out12.frame)
            self.play(FadeIn(VGroup(out12.rule, out12.rows, out12.header, out12.tag)), run_time=0.5)
            vo.wait_until("at the time of recording")
            r0 = out12.rows[0]
            vers = VGroup(substring(r0, "torch 2.11.0+cu128"), substring(r0, "transformers 5.16.1"))
            self.play(vers.animate.set_color(TURN), FadeIn(vtag12, shift=UP * 0.05), run_time=0.5)
            vo.wait_until("and mounts your Drive")
            self.play(FadeIn(out14, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Section 6 caches")
            self.play(FadeOut(VGroup(out12, vtag12, out14)), run_time=0.4)
            self.play(tr.goto(6), FadeIn(out16, shift=UP * 0.1), run_time=0.6)
            pa = VGroup(substring(r16a, "MyDrive/LLM_cache"), substring(r16b, "MyDrive/LLM_cache"))
            self.play(pa.animate.set_color(S.GREY), run_time=0.3)
            self.play(FadeIn(drv.body), TransformFromCopy(substring(r16a, "MyDrive/LLM_cache"), drv.path),
                      run_time=0.8)
            self.play(TransformFromCopy(substring(r16a, OPT_DIR), drv.models[0]),
                      TransformFromCopy(substring(r16b, QWEN_DIR), drv.models[1]), run_time=0.9)
            vo.wait_until("Pause and run part A")
            self.play(FadeOut(out16), drv.animate.shift(UP * drv_up), run_time=0.6)
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.6)
        self.wait(2)

        # ========================================================== 3 · the lecture's question: 10 B params, 20 GB; PONDER
        mini = mini_colab()
        col = full_column(X_FULL_4, PONDER_BASE)
        pslab = col.parts[PARAM]
        mdl_r = box(3.3, 1.5, S.GREY, dashed=True)
        mdl_t = label("10 B parameters", 26, INK).move_to(mdl_r)
        mdl = VGroup(mdl_r, mdl_t).move_to([3.6, 0.9, 0])
        ctag = concept_tag().next_to(mdl, UP, buff=0.2)
        lab_p = block_label(["Parameters · FP16 · 20 GB"])
        place(lab_p, left=col.blocks[PARAM].get_right()[0] + 0.3, cy=col.blocks[PARAM].get_center()[1])
        lr = None
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(drv, tc)), FadeOut(tr), run_time=0.5)
            self.play(Transform(cf.frame, mini.frame), Transform(cf.title[1], mini.text), FadeOut(cf.title[0]),
                      FadeOut(cf.tag), run_time=0.9)
            self.remove(cf.frame, cf.title[1])
            self.add(mini)
            lr = lref_swap(self, lr, "11–16")
            vo.wait_until("Why not simply train")
            self.play(flash(lr, S.GREY, 1.08), run_time=0.6)
            vo.wait_until("Take a model")
            self.play(Create(mdl_r), FadeIn(mdl_t), run_time=0.6)
            self.play(FadeIn(ctag, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("the weights alone")
            ghost = col.blocks[PARAM].copy().stretch_to_fit_width(mdl_r.width) \
                .stretch_to_fit_height(mdl_r.height).move_to(mdl_r).set_fill(opacity=0)
            self.play(ReplacementTransform(ghost, col.blocks[PARAM]), run_time=0.9)   # solid: no hatching
            self.play(FadeIn(VGroup(*pslab[1:])), FadeIn(lab_p, shift=LEFT * 0.1), run_time=0.5)
        card = ponder_hint(self, "Full fine-tuning: what else has to sit in GPU memory,\nand how much?",
                           "hint: the optimizer is Adam, kept in 32-bit", 8)

        # ========================================================== 4 · gradients + Adam states: 120 GB, five 24 GB GPUs
        down = (BASE_Y - PONDER_BASE)
        for name in (GRAD, OPT):
            col.parts[name].shift(UP * down)
        lab_g = block_label(["Gradients · FP16 · 20 GB"])
        place(lab_g, left=lab_p.get_left()[0], cy=col.blocks[GRAD].get_center()[1])
        lab_o = block_label(["Optimizer states · FP32 · 80 GB", "momentum + variance"])
        place(lab_o, left=lab_p.get_left()[0], cy=col.blocks[OPT].get_center()[1])
        tot = label("120 GB", 26, INK)
        place(tot, cx=X_FULL_4, top=BASE_Y - 0.15)
        tiles = gpu_tiles(5, 24, scale=SCALE, w=1.6)
        place(tiles, cx=1.7, bottom=BASE_Y)
        tlab = block_label(["five GPUs", "24 GB each"])
        place(tlab, left=tiles.get_right()[0] + 0.3, cy=tiles.get_center()[1])
        ctag_t = concept_tag()
        place(ctag_t, cx=tiles.get_center()[0] + 0.6, bottom=tiles.get_top()[1] + 0.15)
        assert lab_o.get_right()[0] < tiles.get_left()[0] - 0.2, (lab_o.get_right(), tiles.get_left())
        assert ctag_t.get_top()[1] < 3.0 and tlab.get_right()[0] < SAFE_R, (ctag_t.get_top(), tlab.get_right())
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            self.play(VGroup(pslab, lab_p).animate.shift(UP * down), run_time=0.6)
            vo.wait_until("The gradients")
            self.play(GrowFromEdge(col.blocks[GRAD], DOWN), run_time=0.7)
            self.play(FadeIn(VGroup(*col.parts[GRAD][1:])), FadeIn(lab_g, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("And the Adam optimizer")
            self.play(GrowFromEdge(col.blocks[OPT], DOWN), run_time=1.2)
            self.play(FadeIn(VGroup(*col.parts[OPT][1:])), FadeIn(lab_o, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("That's 120 in total")
            self.play(Write(tot), run_time=0.6)
            self.play(flash(tot, INK, 1.2), run_time=0.6)
            vo.wait_until("the memory of five GPUs")
            self.play(FadeOut(mdl), ctag.animate.move_to(ctag_t), LaggedStart(*[FadeIn(t, shift=UP * 0.1)
                                                                               for t in tiles], lag_ratio=0.15),
                      FadeIn(tlab), run_time=1.0)
            pour = VGroup(*[col.blocks[n].copy() for n in (PARAM, GRAD, OPT)])
            tgt = pour.copy().stretch_to_fit_width(tiles.width - 0.12)
            place(tgt, cx=tiles.get_center()[0], bottom=BASE_Y + 0.02)
            self.play(TransformFromCopy(VGroup(*[col.blocks[n] for n in (PARAM, GRAD, OPT)]), tgt), run_time=1.4)
            pour = tgt

        # ========================================================== 5 · LoRA ≈ 40 GB, QLoRA ≈ 12 GB, the three bars
        col2 = full_column(X_LORA, BASE_Y)
        col3 = full_column(X_QLORA, BASE_Y)
        flake = snowflake()
        flake.next_to(col2.blocks[PARAM], LEFT, buff=0.18)     # beside the slab: inside, it would touch FP16
        frz = block_label(["frozen, but needed", "for the forward pass"], S.GREY)
        place(frz, left=col2.blocks[PARAM].get_right()[0] + 0.3, cy=col2.blocks[PARAM].get_center()[1])
        ab2 = label("A, B", CAPTION, ADAPTER)
        y_ab2 = BASE_Y + 20 * SCALE + Column.MIN_H     # the two small blocks' boundary after the restack
        place(ab2, left=col2.blocks[PARAM].get_right()[0] + 0.3, cy=y_ab2)
        tot2 = label("≈ 40 GB", 26, INK)
        place(tot2, cx=X_LORA, top=BASE_Y - 0.15)
        tot3 = label("≈ 12 GB", 26, INK)
        place(tot3, cx=X_QLORA, top=BASE_Y - 0.15)
        lt2 = grey_tag("the lecture's total")
        place(lt2, cx=X_LORA, top=tot2.get_bottom()[1] - 0.1)
        lt3 = grey_tag("the lecture's total")
        place(lt3, cx=X_QLORA, top=tot3.get_bottom()[1] - 0.1)
        assert lt2.get_bottom()[1] > -3.55 and lt2.get_right()[0] < lt3.get_left()[0] - 0.2, lt2.get_bottom()
        nf4 = VGroup(label("4-bit", CAPTION, INK), dtype_tag("NF4")).arrange(RIGHT, buff=0.15)
        place(nf4, left=X_QLORA + col3.col_w / 2 + 0.3, cy=BASE_Y + 5 * SCALE / 2)
        q_top = BASE_Y + 5 * SCALE + 2 * Column.MIN_H       # col3's stack top after the restack
        page = Rectangle(width=col3.col_w, height=Column.MIN_H, stroke_color=S.GREY, stroke_width=2)
        page.set_fill(S.GREY, 0.5).move_to([X_QLORA, q_top + Column.MIN_H / 2, 0])
        cpu = VGroup(box(1.3, 0.9, S.GREY, fill=S.BG, fill_opacity=1.0), label("CPU", 26, INK))
        cpu[1].move_to(cpu[0])
        cpu.move_to([5.4, q_top + Column.MIN_H / 2 + 0.45, 0])
        plab = label("optimizer pages", CAPTION, S.GREY)
        place(plab, cx=cpu.get_center()[0] - 0.2, bottom=cpu.get_top()[1] + 0.12)
        assert plab.get_right()[0] < SAFE_R, plab.get_right()
        page_dst = page.copy().stretch_to_fit_width(0.9).stretch_to_fit_height(0.12)
        page_dst.move_to(cpu[0].get_bottom() + UP * 0.2)
        cpu[1].shift(UP * 0.12)
        names = {k: label(s, 26, INK) for k, s in (("full", "full"), ("lora", "LoRA"), ("qlora", "QLoRA"))}
        with self.voiceover(SAY[5]) as vo:
            lr = lref_swap(self, lr, "37–39")
            self.play(FadeOut(VGroup(tiles, tlab, pour, ctag, lab_p, lab_g, lab_o)), run_time=0.5)
            self.play(VGroup(col, tot).animate.shift(RIGHT * (X_FULL - X_FULL_4)), run_time=0.6)
            self.play(TransformFromCopy(col, col2), TransformFromCopy(col, col3), run_time=0.9)
            vo.wait_until("LoRA trains only small adapters")
            self.play(*restack_green(col2, {GRAD: 1, OPT: 1}, (GRAD, OPT)))
            self.play(FadeIn(ab2, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("but the frozen base")
            self.play(FadeIn(flake, scale=0.6), FadeIn(frz, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("The lecture puts that")
            o2 = outline_to(col2, 40)
            self.play(Create(o2), run_time=0.6)
            self.play(FadeIn(tot2, shift=UP * 0.1), FadeIn(lt2), run_time=0.5)
            vo.wait_until("QLoRA stores the base")
            lr = lref_swap(self, lr, "71–72")
            self.play(*restack_green(col3, {PARAM: 5, GRAD: 1, OPT: 1}, (GRAD, OPT)))
            self.play(FadeIn(nf4, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("and the lecture's total drops")
            self.play(FadeIn(page), FadeIn(cpu), FadeIn(plab), run_time=0.4)
            arr = _arrow(page.get_right() + RIGHT * 0.05, cpu[0].get_left() + DOWN * 0.2, LOOKUP, 3)
            self.play(GrowArrow(arr), run_time=0.4)
            self.bring_to_front(page)                   # else the CPU box's opaque fill hides it
            self.play(Transform(page, page_dst), run_time=0.7)
            o3 = outline_to(col3, 12)
            self.play(Create(o3), FadeIn(tot3, shift=UP * 0.1), FadeIn(lt3), run_time=0.5)
            vo.wait_until("The next chapters")
            tops = {"full": col.blocks[OPT].get_top()[1], "lora": o2.get_top()[1], "qlora": o3.get_top()[1]}
            for k, x in (("full", X_FULL), ("lora", X_LORA), ("qlora", X_QLORA)):
                place(names[k], cx=x, bottom=tops[k] + 0.15)
            arrows = VGroup(_arrow(tot.get_right() + RIGHT * 0.25, tot2.get_left() + LEFT * 0.25, S.GREY, 2.5),
                            _arrow(tot2.get_right() + RIGHT * 0.25, tot3.get_left() + LEFT * 0.25, S.GREY, 2.5))
            self.play(LaggedStart(*[FadeIn(names[k], shift=DOWN * 0.1) for k in ("full", "lora", "qlora")],
                                  lag_ratio=0.3), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.4), run_time=0.7)
            self.play(LaggedStart(flash(tot, INK, 1.15), flash(tot2, INK, 1.15), flash(tot3, INK, 1.15),
                                  lag_ratio=0.35), run_time=1.0)
        self.wait(0.5)
        self.play(FadeOut(VGroup(mini, lr, col, tot, col2, col3, flake, frz, ab2, o2, tot2, lt2, nf4, page, cpu,
                                 plab, arr, o3, tot3, lt3, arrows, *names.values())), run_time=0.9)
        self.wait(0.3)
