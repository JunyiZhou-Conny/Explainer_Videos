"""S12 · Qwen in 4 bits, and its chat template (Colab › Step 1–2 · Qwen, then Step 3 · Dataset).
Lecture: 68–69, then 8.

Beats (script.md "## S12", one voiceover block each), all inside the BLUE Colab frame (tab and
`illustration` tag on the right half of its top border, clear of the tracker):
 0  LECTURE 68–69. TRACKER Qwen 1. CODE(colab/cell-34.py: 1–6) on top; under it "= the same recipe"
    points at a mini copy of S11's CODE(colab/cell-18.py: 8–11, comments cut). Then cell-34 gives
    way to CODE(colab/cell-36.py: 8–13, 18 folded; line 10 wrapped); line 18
    `prepare_model_for_kbit_training` lights; two chips write under it: GREY snowflake "freezes
    every weight", YELLOW "gradient checkpointing: on" with a GREY note "the training chapter shows
    it".
 1  TRACKER Qwen 2. CODE(colab/cell-38.py: 2) with `p.numel()` YELLOW (not in SHOW: what counts),
    then RECORDED(expected/colab-c38-num-params.txt: 5); `375.84896` lights YELLOW; beside it a GREY
    chip "Qwen3-0.6B: 596 M parameters". The panel stays; PONDER(8 s) card enters.
 2  The ponder card and the code line leave; the output rises into their place. A copy of the 596 M chip becomes a bar that splits: GREY "linear
    weights · 440 M" (16 cells), GREY solid "embeddings · 155.6 M" with a WHITE tag "not 4-bit",
    a sliver "norms · 0.07 M". Pairs of 4-bit cells fold into single byte boxes (two halves per
    box): the linear slab halves, its label becomes "220 M · two per byte"; the rest slides up to
    it; the sum writes 220.2 + 155.6 + 0.07 = 375.8 (YELLOW 375.8, echoed by c38's number).
    TRACKER Qwen 3: RECORDED(expected/colab-c42-qwen-config.txt: 58, 63–64, 71) as a 4-row box;
    "nf4" lights. The lecture tag leaves at the end of this idea.
 3  TRACKER Qwen 4: CODE(colab/cell-45.py: 1) and under it RECORDED(c45: 8; wrap) with a GREY
    note "drifts off topic". TRACKER Qwen 5: RECORDED(c48: 5); `trainable params: 0` lights; a
    GREY model glyph "Qwen3-0.6B" gets a snowflake.
 4  TRACKER Data 1: RECORDED(c51: 5–6), `23.2M` lights, GREY chip "Too many users …? retry later,
    or use your own train.jsonl from part 1 (same format)". TRACKER Data 2: CODE(colab/cell-53.py:
    4) with RECORDED(c53: 7, 8 cut after "…cheeses?'}]}", wrapped) under it. V4's conveyor
    (stations train.jsonl · chat template · tokens) at the bottom. On "Look at a row" the keys
    'contents', 'role': 'user', 'parts', 'text' light; on "exactly the format of track A" the
    GREEN JSONL brick (S07's nesting, compact: contents → role: user / role: model → parts · text)
    slides in from the left onto station 1, its keys light to match; caption "exactly track A's
    format"; GREY note on the 16k file's openers (c55 lines 25–29).
 5  TRACKER Data 3. CODE(colab/cell-59.py: 10–15, line 13 wrapped); line 13 lights, then the panel
    folds into an excerpt chip of line 13 at the top. The brick rides to station 2 (chat template)
    and unrolls into V4's ribbon of empty segments, drawn from RECORDED(c63: 3) (header + recorded
    tag); each segment fills as it is named: `<|im_start|>user` ↵ question …, `<|im_end|>` ↵
    `<|im_start|>assistant` ↵, `<think>` ↵↵ `</think>` ↵↵ answer …, … `<|im_end|>` (GREY tag "EOS ·
    already there: the trainer's Adding EOS step adds nothing"). The empty think block glows; GREY
    note "answer without thinking · the same prefix at inference".
 6  LECTURE 8. TRACKER Data 4: RECORDED(c61: 11–12) top left (its header and recorded tag beside
    it; the ribbon's header steps aside meanwhile). TRACKER Data 5: the ribbon header returns and the
    ribbon flashes (3.7 shows that one example). Station 3 (tokens) lights: the ribbon becomes rows of integer
    boxes (tag illustration); a YELLOW highlighter sweeps every box, caption "loss on every token".
    Then the GREY "your turn" card with the YELLOW ▶: "run Part C, Steps 1, 2 and 3 (1.1 to 3.7)",
    GREEN "T4: free (when available)". 2 s hold. Everything fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Rectangle,
    RoundedRectangle,
    Succession,
    Transform,
    TransformFromCopy,
    VGroup,
    Wait,
    Write,
    there_and_back,
)

from common import *  # noqa: F401,F403
from common import _arrow
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S12"]

# ------------------------------------------------------------------ the real sources and captures
CELL34, CELL18, CELL36 = "colab/cell-34.py", "colab/cell-18.py", "colab/cell-36.py"
CELL38 = "colab/cell-38.py"
CELL45, CELL53, CELL59 = "colab/cell-45.py", "colab/cell-53.py", "colab/cell-59.py"
assert source_line(CELL34, 2).strip() == "load_in_4bit=True,", source_line(CELL34, 2)
assert source_line(CELL36, 18) == "base_model = prepare_model_for_kbit_training(base_model)"
assert source_line(CELL45, 1) == 'text = "Hello my cheese name is"'
assert source_line(CELL53, 4) == "print(df.iloc[0]['contents'])"
L59 = source_line(CELL59, 13)
TEMPLATE_CALL = "tokenizer.apply_chat_template(messages, tokenize=False)"
assert TEMPLATE_CALL in L59, L59
C38 = capture("expected/colab-c38-num-params")
assert C38.line(5) == "Number of parameters: 375.84896 millions.", C38.line(5)
C42 = capture("expected/colab-c42-qwen-config")
assert C42.line(63).strip() == '"bnb_4bit_quant_type": "nf4",' and C42.line(71).strip() == '"quant_method": "bitsandbytes"'
C45 = capture("expected/colab-c45-baseline-generate")
C48 = capture("expected/colab-c48-trainable-before")
assert C48.line(5).startswith("trainable params: 0 ||"), C48.line(5)
C51 = capture("expected/colab-c51-gdown-dataset")
assert C51.line(5) == "To: /content/train_16k.jsonl" and "23.2M/23.2M" in C51.line(6)
C53 = capture("expected/colab-c53-sample-1000")
assert C53.line(7) == "(1000, 1)", C53.line(7)
ROW53 = C53.cut(8, "Italy influence the production of its cheeses?'}]}")
C55 = capture("expected/colab-c55-extract-qa")
assert C55.line(26).startswith("1  Hi everyone") and C55.line(28).startswith("3  Yello"), C55.line(28)
C61 = capture("expected/colab-c61-train-test-split")
assert C61.line(11) == "(900, 3)" and C61.line(12) == "(100, 3)"
C63 = capture("expected/colab-c63-one-example")
EX63 = C63.line(3)                     # one long Column([...]) repr; the persona already masked

# The ribbon (V4 station 4) from c63's own text: (piece, is_marker). "↵" stands for each "\n" of the
# repr, "…" for what is left out; every other piece is checked against the line, in order.
NL = "\\n"
RIBBON = [
    [("<|im_start|>user", True), ("↵", False), ("Can you explain the process of 'affioratura' …", False)],
    [("<|im_end|>", True), ("↵", False), ("<|im_start|>assistant", True), ("↵", False)],
    [("<think>", True), ("↵↵", False), ("</think>", True), ("↵↵", False),
     ("Welcome welcome, cheese lovers! …", False)],
    [("… Italian cheese-making!", False), ("<|im_end|>", True)],
]


def _check_ribbon() -> None:
    """Every piece is c63's own text in order; "…" marks the only places where text is left out."""
    assert EX63.startswith('Column(["'), EX63[:12]
    pos, gap = len('Column(["'), False
    for row in RIBBON:
        for text, _ in row:
            frags = ([NL] * len(text)) if set(text) <= {"↵"} else text.split("…")
            for k, frag in enumerate(frags):
                frag = frag if frag == NL else frag.strip()
                if not frag:
                    gap = True
                    continue
                i = EX63.find(frag, pos)
                assert i == pos or (gap and i > pos), (text, frag, pos, EX63[pos:pos + 30])
                pos, gap = i + len(frag), False
            if text.endswith("…"):
                gap = True
    assert EX63[pos:] == '"])', EX63[pos:]


_check_ribbon()

# ------------------------------------------------------------------ layout
SAFE_R = 6.3                       # inside the Colab frame
TOP = 2.45                         # the slot's top, under the frame's top border
BAR_Y = 0.45                       # the parameter bar (beat 2)
BAR_L = -5.9
BAR_SC = 9.6 / 596                 # units per million parameters
LIN, EMB, NORM = 440.0, 155.6, 0.07
BELT_Y = -2.78                     # the conveyor's belt (beats 4-6)


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


def colab_notebook() -> VGroup:
    """colab_frame() with its tab and `illustration` tag moved to the right half of the top border
    (the tracker owns the top-left corner; as S10). .frame .title .tag"""
    cf = colab_frame(top=2.75, bottom=-3.5)
    fr = cf.frame
    cf.title.move_to([fr.get_right()[0] - 0.4 - cf.title.width / 2, fr.get_top()[1], 0])
    cf.tag.move_to([cf.title.get_left()[0] - 0.3 - cf.tag.width / 2, fr.get_top()[1], 0])
    return cf


def legend_box(text: str, w: float, h: float, color: str) -> VGroup:
    """A box with its mono name on the top border (a fieldset legend; S07's nesting). .frame .legend"""
    fr = box(w, h, color, fill=S.BG, fill_opacity=1.0, radius=0.1, stroke=2.5)
    t = mono(text, CAPTION, color)
    bg = RoundedRectangle(width=t.width + 0.16, height=t.height + 0.06, corner_radius=0.04,
                          stroke_width=0).set_fill(S.BG, 1)
    lg = VGroup(bg, t).move_to(fr.get_corner(UP + LEFT) + np.array([0.18 + t.width / 2 + 0.08, 0, 0]))
    g = VGroup(fr, lg)
    g.frame, g.legend, g.text = fr, lg, t
    return g


def jsonl_brick() -> VGroup:
    """The GREEN JSONL brick of part 1 (S07's station 3, compact): contents → role: user / role:
    model → parts · text. .contents .turns (each .role .body) .keys {name: [glyphs]}"""
    turns = VGroup()
    for role in ("role: user", "role: model"):
        body = mono("parts · text", CAPTION, INK)
        rb = legend_box(role, body.width + 0.5, 0.9, OWN)
        body.move_to(rb.frame).shift(DOWN * 0.06)
        g = VGroup(rb, body)
        g.role, g.body = rb, body
        turns.add(g)
    turns.arrange(RIGHT, buff=0.18)
    cb = legend_box("contents", turns.width + 0.4, turns.height + 0.5, OWN)
    turns.move_to(cb.frame).shift(DOWN * 0.1)
    card = VGroup(cb, turns)
    card.contents, card.turns = cb, turns
    return card


def bar_cells(n: int, w: float, h: float, x0: float, y: float, fill: float = 0.35) -> VGroup:
    cw = w / n
    return VGroup(*[Rectangle(width=cw, height=h, stroke_color=S.GREY, stroke_width=1.5)
                    .set_fill(S.GREY, fill).move_to([x0 + cw * (k + 0.5), y, 0]) for k in range(n)])


class QwenInFourBits(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · the same 4-bit recipe; prepare_model_for_kbit_training
        cf = colab_notebook()
        tr = tracker("Qwen", 1)
        p34 = src_panel(CELL34, 1, 6, size=20)
        place(p34, left=-6.0, top=TOP)
        p18 = src_panel(CELL18, 8, 11, size=20, cut_comments=True)
        place(p18, left=-6.0, top=p34.get_bottom()[1] - 0.75)
        same = label("= the same recipe", 26, INK)
        place(same, left=p18.get_right()[0] + 0.5, cy=p18.code.get_center()[1])
        arr_same = _arrow(same.get_left() + LEFT * 0.1, p18.code.get_right() + RIGHT * 0.1, S.GREY, 3)
        assert same.get_right()[0] < SAFE_R and p18.get_bottom()[1] > -3.35, (same.get_right(), p18.get_bottom())
        p36 = src_panel(CELL36, [(8, 13), 18], size=20, wrap={10: ["bnb_config,"]})
        place(p36, left=-6.0, top=TOP)
        frz = VGroup(snowflake(0.17), label("freezes every weight", CAPTION, INK)).arrange(RIGHT, buff=0.15)
        ch = mono("|", CAPTION).height + 0.24                 # a chip's height
        frz_box = box(frz.width + 0.5, ch, S.GREY, fill_opacity=0.16, radius=ch / 2.6)
        frz.move_to(frz_box)
        chip_frz = VGroup(frz_box, frz)
        chip_gc = chip("gradient checkpointing: on", TURN, size=CAPTION)
        chips0 = VGroup(chip_frz, chip_gc).arrange(RIGHT, buff=0.4)
        place(chips0, left=-6.0, top=p36.get_bottom()[1] - 0.35)
        later = note("the training chapter shows it")
        place(later, left=chip_gc.get_left()[0] + 0.1, top=chip_gc.get_bottom()[1] - 0.15)
        assert later.get_bottom()[1] > -3.35, later.get_bottom()
        lr = None
        with self.voiceover(SAY[0]) as vo:
            self.play(Create(cf.frame), FadeIn(cf.title), FadeIn(cf.tag), FadeIn(tr, shift=DOWN * 0.25),
                      run_time=0.8)
            lr = lref_swap(self, lr, "68–69")
            self.play(FadeIn(p34, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("with the same 4-bit recipe")
            self.play(FadeIn(p18, shift=UP * 0.15), run_time=0.6)
            self.play(GrowArrow(arr_same), FadeIn(same, shift=LEFT * 0.1), run_time=0.6)
            self.play(flash(VGroup(*[p34.span(n, s) for n, s in ((2, "load_in_4bit"), (3, '"nf4"'),
                                                                   (5, "bnb_4bit_use_double_quant"))]), TURN, 1.08),
                      flash(VGroup(*[p18.span(n, s) for n, s in ((8, "load_in_4bit"), (9, '"nf4"'),
                                                                   (10, "bnb_4bit_use_double_quant"))]), TURN, 1.08),
                      run_time=0.9)
            vo.wait_until("Then prepare model")
            self.play(FadeOut(VGroup(p18, same, arr_same), shift=DOWN * 0.1), run_time=0.4)
            self.play(FadeOut(p34, shift=UP * 0.2), FadeIn(p36, shift=UP * 0.2), run_time=0.7)
            b18 = p36.bar(18, TURN)
            self.play(FadeIn(b18), p36.span(18, "prepare_model_for_kbit_training").animate.set_color(TURN),
                      run_time=0.5)
            vo.wait_until("freezes every weight")
            self.play(FadeIn(chip_frz, shift=UP * 0.1), run_time=0.5)
            self.play(flash(chip_frz[1][0], S.GREY, 1.3), run_time=0.6)
            vo.wait_until("and turns on gradient checkpointing")
            self.play(FadeIn(chip_gc, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a memory trick")
            self.play(FadeIn(later, shift=UP * 0.05), run_time=0.5)

        # ========================================================== 1 · 375.8 million, but 596 million; PONDER
        p38 = src_panel(CELL38, 2, 2, size=20)
        place(p38, left=-6.0, top=TOP)
        out38 = recorded_box("colab-c38-num-params", 5, tag_=False)
        place(out38, left=-6.0, top=p38.get_bottom()[1] - 0.45)
        up38 = TOP - 0.05 - out38.get_top()[1]          # beat 2: the output rises into the code's place
        rtag38 = recorded_tag()
        place(rtag38, right=SAFE_R - 0.05, cy=out38.header.get_center()[1])
        assert rtag38.get_left()[0] > out38.header.get_right()[0] + 0.12, (rtag38.get_left(), out38.header.get_right())
        n38 = substring(out38.rows[0], "375.84896")
        c596 = chip("Qwen3-0.6B: 596 M parameters", S.GREY, size=CAPTION)
        place(c596, left=out38.frame.get_right()[0] + 0.4, cy=out38.frame.get_center()[1])
        assert c596.get_right()[0] < SAFE_R and rtag38.get_right()[0] < SAFE_R, (c596.get_right(), rtag38.get_right())
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(p36, b18, chips0, later)), run_time=0.5)
            self.play(tr.goto(2), FadeIn(p38, shift=UP * 0.15), run_time=0.6)
            self.play(p38.span(2, "p.numel()").animate.set_color(TURN), run_time=0.4)
            self.play(FadeIn(out38, shift=UP * 0.15), FadeIn(rtag38), run_time=0.6)
            vo.wait_until("375.8 million")
            self.play(n38.animate.set_color(TURN), run_time=0.4)
            self.play(flash(n38, TURN, 1.2), run_time=0.6)
            vo.wait_until("But Qwen3")
            self.play(FadeIn(c596, shift=LEFT * 0.1), run_time=0.5)
            self.play(flash(c596, INK, 1.1), run_time=0.6)
        card = ponder_at(self, "Qwen3-0.6B has 596 million parameters.\nWhy does the notebook count 375.8 million?",
                         8, y=-2.2)

        # ========================================================== 2 · packed two per byte; embeddings and norms stay; NF4
        H = 0.55
        w_lin, w_emb, w_norm = LIN * BAR_SC, EMB * BAR_SC, 0.06
        lin_cells = bar_cells(16, w_lin, H, BAR_L, BAR_Y)
        emb = Rectangle(width=w_emb, height=H, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.7)
        place(emb, left=BAR_L + w_lin, cy=BAR_Y)
        norm = Rectangle(width=w_norm, height=H, stroke_color=INK, stroke_width=1).set_fill(INK, 0.8)
        place(norm, left=emb.get_right()[0], cy=BAR_Y)
        lab_lin = label("linear weights · 440 M", CAPTION, INK)
        place(lab_lin, cx=lin_cells.get_center()[0], bottom=BAR_Y + H / 2 + 0.15)
        lab_emb = label("embeddings · 155.6 M", CAPTION, INK)
        place(lab_emb, cx=emb.get_center()[0], bottom=BAR_Y + H / 2 + 0.15)
        not4 = dtype_tag("not 4-bit")
        place(not4, cx=emb.get_center()[0], top=BAR_Y - H / 2 - 0.15)
        lab_norm = label("norms · 0.07 M", CAPTION, INK)
        place(lab_norm, left=norm.get_right()[0] + 0.2, cy=BAR_Y)
        assert lab_norm.get_right()[0] < SAFE_R, lab_norm.get_right()
        assert lab_lin.get_top()[1] < out38.frame.get_bottom()[1] + up38 - 0.15, (lab_lin.get_top(), out38.frame.get_bottom())
        # packing: 16 four-bit cells -> 8 byte boxes, two halves each (cell 2k on top, 2k+1 below)
        cw = w_lin / 16
        halves = VGroup()
        for k in range(16):
            j, top_half = k // 2, k % 2 == 0
            r = Rectangle(width=cw, height=H / 2, stroke_color=S.GREY, stroke_width=1.5).set_fill(S.GREY, 0.35)
            r.move_to([BAR_L + cw * (j + 0.5), BAR_Y + (H / 4 if top_half else -H / 4), 0])
            halves.add(r)
        bytes8 = VGroup(*[Rectangle(width=cw, height=H, stroke_color=INK, stroke_width=2)
                          .move_to([BAR_L + cw * (j + 0.5), BAR_Y, 0]) for j in range(8)])
        pack_note = note("two 4-bit values per byte")
        place(pack_note, left=BAR_L, top=BAR_Y - H / 2 - 0.15)
        lab_lin2 = label("220 M · packed", CAPTION, INK)
        place(lab_lin2, cx=BAR_L + w_lin / 4, bottom=BAR_Y + H / 2 + 0.15)
        slide = LEFT * (w_lin / 2)
        sum_ = label("220.2 + 155.6 + 0.07 = 375.8", 26, INK, t2c={"375.8": TURN})
        place(sum_, left=BAR_L, top=pack_note.get_bottom()[1] - 0.35)
        out42 = recorded_box("colab-c42-qwen-config", 58, (63, 64), 71, tag_at="top")
        place(out42, right=SAFE_R - 0.1, bottom=-3.3)
        nf4 = substring(out42.rows[1], '"nf4"')
        assert out42.get_top()[1] < not4.get_bottom()[1] - 0.1, (out42.get_top(), not4.get_bottom())
        assert sum_.get_right()[0] < out42.get_left()[0] - 0.2 or sum_.get_bottom()[1] > out42.get_top()[1] + 0.1, \
            (sum_.get_right(), sum_.get_bottom(), out42.get_left(), out42.get_top())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(card), FadeOut(p38), run_time=0.4)
            # the tag and the chip rise 0.12 less: the tag stays clear of the Colab tab above it
            self.play(out38.animate.shift(UP * up38), VGroup(rtag38, c596).animate.shift(UP * (up38 - 0.12)),
                      run_time=0.5)
            self.play(TransformFromCopy(c596.box, VGroup(lin_cells, emb, norm)), run_time=0.9)
            self.play(FadeIn(lab_lin, shift=DOWN * 0.1), flash(lin_cells, INK, 1.04), run_time=0.6)
            vo.wait_until("are packed two 4-bit values")
            self.play(FadeIn(pack_note, shift=UP * 0.05), run_time=0.4)
            self.play(*[Transform(lin_cells[k], halves[k]) for k in range(16)], run_time=1.2)
            self.play(FadeIn(bytes8), run_time=0.4)
            vo.wait_until("so they count as 220 million")
            self.play(FadeOut(lab_lin, shift=UP * 0.1), FadeIn(lab_lin2, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("embedding weights")
            self.play(FadeIn(lab_emb, shift=DOWN * 0.1), flash(emb, INK, 1.06), run_time=0.6)
            self.play(FadeIn(not4, shift=UP * 0.05), run_time=0.4)
            vo.wait_until("and the norms")
            self.play(FadeIn(lab_norm, shift=LEFT * 0.1), flash(norm, INK, 1.6), run_time=0.7)
            vo.wait_until("Add them up")
            self.play(VGroup(emb, norm, lab_emb, not4, lab_norm).animate.shift(slide), run_time=0.8)
            self.play(Write(sum_), run_time=1.0)
            self.play(flash(sum_[-5:], TURN, 1.15),
                      flash(n38, TURN, 1.2), run_time=0.8)
            vo.wait_until("The configuration")
            self.play(tr.goto(3), FadeIn(out42, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("confirms NF4")
            self.play(nf4.animate.set_color(TURN), run_time=0.4)
            self.play(flash(nf4, TURN, 1.2), run_time=0.6)
        beat2 = VGroup(out38, rtag38, c596, lin_cells, bytes8, emb, norm, lab_lin2, lab_emb, not4, lab_norm,
                       pack_note, sum_, out42)

        # ========================================================== 3 · baseline drifts; trainable params: 0
        p45 = src_panel(CELL45, 1, 1, size=20)
        place(p45, left=-6.0, top=TOP)
        rows45 = [r for r, *_ in wrap_output(C45.line(8), 65)]
        out45 = recorded_box("colab-c45-baseline-generate", *rows45, header="", tag_=False)
        place(out45, left=-6.0, top=p45.get_bottom()[1] - 0.12)
        rtag45 = recorded_tag()
        place(rtag45, right=out45.frame.get_right()[0], top=out45.frame.get_bottom()[1] - 0.1)
        drift = note("drifts off topic")
        place(drift, left=out45.frame.get_left()[0] + 0.1, cy=rtag45.get_center()[1])
        out48 = recorded_box("colab-c48-trainable-before", 5, tag_=False)
        place(out48, left=-6.0, top=drift.get_bottom()[1] - 0.35)
        rtag48 = recorded_tag()
        place(rtag48, right=SAFE_R - 0.05, cy=out48.header.get_center()[1])
        assert rtag48.get_left()[0] > out48.header.get_right()[0] + 0.12, rtag48.get_left()
        t0 = substring(out48.rows[0], "trainable params: 0")
        mdl = model_box("Qwen3-0.6B", w=2.6, h=0.9, color=FROZEN)
        place(mdl, left=-6.0, top=out48.get_bottom()[1] - 0.3)
        flake = snowflake(0.2)
        place(flake, left=mdl.frame.get_right()[0] + 0.25, cy=mdl.frame.get_center()[1])
        allfrz = note("every weight frozen")
        place(allfrz, left=flake.get_right()[0] + 0.2, cy=mdl.frame.get_center()[1])
        assert mdl.get_bottom()[1] > -3.35 and out45.get_right()[0] < SAFE_R, (mdl.get_bottom(), out45.get_right())
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(beat2), FadeOut(lr), run_time=0.6)
            lr = None
            self.play(tr.goto(4), FadeIn(p45, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(out45, shift=UP * 0.1), FadeIn(rtag45), run_time=0.6)
            vo.wait_until("and it drifts off topic")
            self.play(FadeIn(drift, shift=UP * 0.05), out45.rows[1].animate.set_color(S.GREY), run_time=0.6)
            vo.wait_until("And 2.4 counts")
            self.play(tr.goto(5), FadeIn(out48, shift=UP * 0.15), FadeIn(rtag48), run_time=0.6)
            self.play(FadeIn(mdl, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("zero")
            self.play(t0.animate.set_color(TURN), run_time=0.4)
            self.play(flash(t0, TURN, 1.1), run_time=0.6)
            vo.wait_until("Everything is frozen")
            self.play(FadeIn(flake, scale=0.5), FadeIn(allfrz, shift=LEFT * 0.05), mdl.frame.animate.set_fill(S.GREY, 0.35),
                      run_time=0.6)
        self.wait(0.8)
        beat3 = VGroup(p45, out45, rtag45, drift, out48, rtag48, mdl, flake, allfrz)

        # ========================================================== 4 · download, sample: exactly track A's format
        out51 = recorded_box("colab-c51-gdown-dataset", (5, 6))
        place(out51, left=-6.0, top=TOP - 0.05)
        mb = substring(out51.rows[1], "23.2M/23.2M")
        busy = chip("Too many users …? retry later, or use your own train.jsonl from part 1 (same format)",
                    S.GREY, size=CAPTION)
        place(busy, left=-6.0, top=out51.get_bottom()[1] - 0.3)
        assert busy.get_right()[0] < SAFE_R, busy.get_right()
        p53 = src_panel(CELL53, 4, 4, size=20)
        place(p53, left=-6.0, top=TOP)
        w53 = [r for r, *_ in wrap_output(ROW53, 65)]
        if w53[-1].strip() == "…":                      # keep the cut mark on the row it ends
            w53 = [*w53[:-2], w53[-2] + " …"]
        rows53 = [C53.line(7), *w53]
        out53 = recorded_box("colab-c53-sample-1000", *rows53, header="", tag_=False)
        place(out53, left=-6.0, top=p53.get_bottom()[1] - 0.12)
        rtag53 = recorded_tag()
        place(rtag53, right=out53.frame.get_right()[0], top=out53.frame.get_bottom()[1] - 0.1)
        r_shape = substring(out53.rows[0], "(1000, 1)")
        k_contents = p53.span(4, "'contents'")
        k_user = substring(out53.rows[1], "'role': 'user'")
        k_parts = substring(out53.rows[1], "'parts'")
        k_text = substring(out53.rows[1], "'text'")
        openers = VGroup(note("the staff's 16k file: Remember / Hi everyone /"),
                         note("Welcome / Yello openers (3.3 · cell 55)")).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        cv = Conveyor(STATIONS[2:], width=11.8)
        cv.shift(UP * (BELT_Y - cv.belt.get_center()[1]))
        brk = jsonl_brick()
        cv.put(0, brk, buff=0.15)
        brk.shift(RIGHT * max(0.0, cf.frame.get_left()[0] + 0.18 - brk.get_left()[0]))   # inside the frame
        brk_home = brk.get_center()
        brk.shift(LEFT * 7)
        fmt = label("exactly track A's format", 26, OWN)
        place(fmt, left=brk_home[0] + brk.width / 2 + 0.4, bottom=brk_home[1] + 0.12)
        place(openers, left=fmt.get_left()[0], top=fmt.get_bottom()[1] - 0.2)
        assert brk_home[1] + brk.height / 2 < out53.get_bottom()[1] - 0.15, (brk_home, out53.get_bottom())
        assert fmt.get_top()[1] < rtag53.get_bottom()[1] - 0.12, (fmt.get_top(), rtag53.get_bottom())
        assert fmt.get_right()[0] < SAFE_R and openers.get_right()[0] < SAFE_R, (fmt.get_right(), openers.get_right())
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(beat3), run_time=0.5)
            tr = switch_section(self, tr, "Data", 1)
            vo.wait_until("It downloads")
            self.play(FadeIn(out51, shift=UP * 0.15), run_time=0.6)
            self.play(mb.animate.set_color(TURN), run_time=0.4)
            self.play(FadeIn(busy, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and samples")
            self.play(FadeOut(VGroup(out51, busy)), run_time=0.4)
            self.play(tr.goto(2), FadeIn(p53, shift=UP * 0.15), FadeIn(out53, shift=UP * 0.15), FadeIn(rtag53),
                      run_time=0.7)
            self.play(r_shape.animate.set_color(TURN), run_time=0.4)
            vo.wait_until("Look at a row")
            self.play(FadeIn(cv), run_time=0.6)
            self.play(k_contents.animate(rate_func=there_and_back).scale(1.25), run_time=0.5)   # already a YELLOW string
            vo.wait_until("a user turn")
            self.play(k_user.animate.set_color(TURN), run_time=0.4)
            vo.wait_until("a model turn")
            self.play(VGroup(k_parts, k_text).animate.set_color(TURN), run_time=0.4)
            vo.wait_until("exactly the format")
            self.play(brk.animate.move_to(brk_home), cv.light(0), run_time=1.0)
            brk_keys = VGroup(brk.contents.text, *[t.role.text for t in brk.turns],
                              *[t.body for t in brk.turns])
            self.play(brk_keys.animate.set_color(TURN), FadeIn(fmt, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("the brick from part 1")
            self.play(brk.animate(rate_func=there_and_back).scale(1.06), FadeIn(openers, shift=UP * 0.05),
                      run_time=0.8)

        # ========================================================== 5 · the chat template: a ribbon
        p59 = src_panel(CELL59, 10, 15, size=20, wrap={13: ["tokenize=False"]})
        place(p59, left=-6.0, top=TOP)
        assert p59.get_bottom()[1] > brk_home[1] + brk.height / 2 + 0.1, (p59.get_bottom(), brk_home)
        x59 = excerpt_chip(TEMPLATE_CALL, f"{shown_path(CELL59)} · line 13 (excerpt)", line=L59)
        place(x59, left=-6.0, top=TOP)
        rib = ChatRibbon(RIBBON, max_w=12.2)
        place(rib, left=-6.0, top=x59.get_bottom()[1] - 0.62)
        rows = rib.lines
        VGroup(rows[2], rows[3]).shift(DOWN * 0.32)
        rtag63 = recorded_tag()
        hd63 = label(f"{colab_where(63)} · saved output", CAPTION, S.GREY)
        place(hd63, left=-6.0, bottom=rib.get_top()[1] + 0.12)
        place(rtag63, left=hd63.get_right()[0] + 0.2, cy=hd63.get_center()[1])
        assert rtag63.get_right()[0] < SAFE_R, rtag63.get_right()
        chips = [list(r) for r in rows]
        think = VGroup(chips[2][0], chips[2][1], chips[2][2])
        eos_t = grey_tag("EOS · already there")
        place(eos_t, left=chips[3][1].get_right()[0] + 0.3, cy=chips[3][1].get_center()[1])
        eos_n = VGroup(note("so the trainer's Adding EOS"), note("step adds nothing")).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.04)
        place(eos_n, left=eos_t.get_left()[0] + 0.1, top=eos_t.get_bottom()[1] - 0.06)
        eos = VGroup(eos_t, eos_n)
        why = VGroup(note("answer without thinking ·"), note("the same prefix at inference"))
        why.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        place(why, left=rows[1].get_right()[0] + 0.9, top=rows[1].get_top()[1])
        assert why.get_bottom()[1] > rows[2].get_top()[1] + 0.08, (why.get_bottom(), rows[2].get_top())
        why_arr = _arrow(why.get_left() + LEFT * 0.1 + DOWN * 0.12, think.get_top() + UP * 0.08 + RIGHT * 0.6,
                         S.GREY, 2.5)
        assert eos.get_right()[0] < SAFE_R and why.get_right()[0] < SAFE_R, (eos.get_right(), why.get_right())
        assert eos.get_bottom()[1] > BELT_Y + 0.2, eos.get_bottom()
        assert hd63.get_top()[1] < x59.get_bottom()[1] - 0.12, (hd63.get_top(), x59.get_bottom())
        assert rib.get_bottom()[1] > BELT_Y + 0.4 and hd63.get_bottom()[1] > x59.get_bottom()[1] - 0.8 + 0.0, \
            (rib.get_bottom(), hd63.get_bottom())
        shells = VGroup(*[c.box.copy() for c in rib.chips])
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(p53, out53, rtag53, openers, fmt)), brk_keys.animate.set_color(INK),
                      run_time=0.5)
            self.play(tr.goto(3), FadeIn(p59, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("lets the tokenizer write")
            b13 = p59.bar(13, TURN)
            self.play(FadeIn(b13), p59.span(13, "apply_chat_template").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("chat template")
            self.play(FadeOut(VGroup(p59, b13), shift=UP * 0.1), *cv.carry(brk, 1, buff=0.15), cv.light(1),
                      run_time=0.6)
            self.play(FadeIn(x59, shift=UP * 0.1), run_time=0.4)
            self.play(Transform(brk, shells), FadeIn(hd63), FadeIn(rtag63), run_time=1.0)
            self.remove(brk)
            self.add(*[c.box for c in rib.chips])
            texts = {id(c): c.text for c in rib.chips}

            def fill(*cs):
                return [FadeIn(texts[id(c)]) for c in cs] + [flash(c.box, TURN if c.marker else INK, 1.08)
                                                             for c in cs]
            vo.wait_until("im start user")
            self.play(*fill(chips[0][0]), run_time=0.5)
            vo.wait_until("the question")
            self.play(*fill(chips[0][1], chips[0][2]), run_time=0.5)
            vo.wait_until("im end")
            self.play(*fill(chips[1][0], chips[1][1]), run_time=0.5)
            vo.wait_until("im start assistant")
            self.play(*fill(chips[1][2], chips[1][3]), run_time=0.5)
            vo.wait_until("an empty think block")
            self.play(*fill(*chips[2][:4]), run_time=0.5)
            vo.wait_until("and the answer")
            self.play(*fill(chips[2][4], *chips[3]), run_time=0.6)
            self.add(rib)
            self.play(FadeIn(eos, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("The empty think block")
            self.play(*[c.box.animate.set_fill(TURN, 0.45) for c in think], run_time=0.5)
            self.play(flash(think, TURN, 1.08), run_time=0.6)
            vo.wait_until("and chat uses the same prefix")
            self.play(GrowArrow(why_arr), FadeIn(why, shift=LEFT * 0.1), run_time=0.6)

        # ========================================================== 6 · split; integers; loss on every token; your turn
        lr = None
        out61 = recorded_box("colab-c61-train-test-split", (11, 12), header="", tag_=False)
        place(out61, left=-6.0, top=TOP - 0.05)
        hd61 = label(f"{colab_where(61)} · saved output", CAPTION, S.GREY)    # beside: no room above
        place(hd61, left=out61.frame.get_right()[0] + 0.3, cy=out61.rows[0].get_center()[1])
        rtag61 = VGroup(hd61, recorded_tag())
        place(rtag61[1], left=hd61.get_left()[0], cy=out61.rows[1].get_center()[1])
        assert out61.get_bottom()[1] > rib.get_top()[1] + 0.15, (out61.get_bottom(), rib.get_top())
        cap = label("loss on every token", 26, TURN)
        place(cap, cx=0, top=rib.get_bottom()[1] - 0.2)
        illu = illustration_tag("token boxes")
        tc = turn_card([Prose("run Part C, Steps 1, 2 and 3 (1.1 to 3.7)"),
                        (Prose("T4: free (when available)"), OWN)])
        place(tc, cx=0, cy=0.0)
        hl = Rectangle(width=0.35, height=0.46, stroke_width=0).set_fill(TURN, 0.35)

        def sweep_cells(run_time):
            """rib.sweep() places its bar on the rows' bounding boxes, which after tokenize() sit
            ~0.14 below the cells; this one follows the cells (rib.cells) and outlines every grey
            cell YELLOW as the bar passes: the loss covers the question too."""
            strip = {id(c): s for c, s in zip(rib.chips, rib.cells)}
            steps = []
            for k, row in enumerate(chips):
                rs = VGroup(*[strip[id(c)] for c in row])
                start = [rs.get_left()[0] + 0.17, rs.get_center()[1], 0]
                steps.append(FadeIn(hl.move_to(start), run_time=0.2) if k == 0
                             else hl.animate(run_time=0.1).move_to(start))
                grey = [c for c in row if not c.marker]
                lit = LaggedStart(*[c.animate.set_stroke(TURN) for c in grey], lag_ratio=0.6) if grey else Wait()
                steps.append(AnimationGroup(hl.animate(rate_func=linear).stretch_to_fit_width(rs.width + 0.1)
                                            .move_to(rs), lit, run_time=run_time / len(chips)))
                steps.append(hl.animate(run_time=0.05).stretch_to_fit_width(0.35)
                             .move_to([rs.get_right()[0] - 0.17, rs.get_center()[1], 0]))
            return Succession(*steps)

        with self.voiceover(SAY[6]) as vo:
            lr = lref_swap(self, lr, "8")
            self.play(FadeOut(VGroup(x59, why, why_arr, eos, hd63, rtag63)), run_time=0.4)
            self.play(tr.goto(4), FadeIn(out61, shift=UP * 0.1), FadeIn(rtag61), run_time=0.6)
            self.play(LaggedStart(flash(out61.rows[0], TURN, 1.1), flash(out61.rows[1], TURN, 1.1), lag_ratio=0.5),
                      run_time=0.9)
            vo.wait_until("and 3.7 checks")
            self.play(tr.goto(5), FadeOut(VGroup(out61, rtag61)), run_time=0.5)
            self.play(FadeIn(hd63), FadeIn(rtag63), flash(rib, INK, 1.03), run_time=0.7)
            vo.wait_until("Then the ribbon becomes integers")
            place(illu, right=SAFE_R, cy=hd63.get_center()[1])
            self.play(cv.light(2), FadeOut(rtag63), run_time=0.4)
            self.play(*rib.tokenize(run_time=1.2), FadeIn(illu), run_time=1.2)
            vo.wait_until("and the loss covers every token")
            self.play(sweep_cells(2.4))
            self.play(FadeIn(cap, shift=UP * 0.1), FadeOut(hl), run_time=0.5)
            vo.wait_until("still next-word prediction")
            self.play(flash(cap, TURN, 1.1), lr.animate(rate_func=there_and_back).scale(1.12), run_time=0.8)
            vo.wait_until("Pause, and run")
            self.play(FadeOut(VGroup(rib, hd63, illu, cap, cv, lr)), run_time=0.5)
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(VGroup(tc, tr, cf)), run_time=0.8)
        self.wait(0.3)
