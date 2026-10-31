"""S15 · Did it work? Perplexity and the sky (Colab › Step 5 · Evaluate, 5.1–5.2).
Lecture: 9–10, 36, 40.

Beats (script.md "## S15", one voiceover block each):
 0  TRACKER Eval 1. A formula card "perplexity = exp(mean token loss)" (its parts light as named);
    beside it a fan of 14 equally likely next-token boxes (tag `illustration`) with the count
    "≈ 14 equally likely choices", which then shrinks to 4 boxes ("≈ 4").
 1  CODE(colab/cell-80.py: 53–55); line 54 `with trainer.model.disable_adapter():` lights. Then
    RECORDED(c80: 75–80): 100 samples and 30,681 tokens light as named; `Base (4-bit) 2.6498 14.15`
    GREY, `Fine-tuned (4-bit + LoRA) 1.3872 4.00` GREEN, its numbers lit as spoken.
 2  LECTURE 36, then 9–10. The recorded box leaves, the panel stays (line 54 lights again). V1's
    weights dial returns and becomes the `disable_adapter()` switch; V7's block (small) beside it.
    Switch off: the GREEN A/B hourglass slides out of the block (ghosted), W₀ (snowflake) untouched,
    caption "W₀ · unchanged"; switch on: it slides back in. GREY lecture chip "catastrophic
    forgetting · LoRA forgets less".
 3  The panel and block leave; the switch stays. An illustrative first-word bar chart (tag
    `illustration`, no axis numbers) after the empty think block (GREY mono prompt row; the cell
    uses enable_thinking=False, cell-82.py lines 19–27): adapter off, one tall GREY bar "The" plus
    two unlabelled bars; switch on, they collapse onto BLUE "Welcome", "Yello". GREY chip "saved
    run: base answers start "The" · fine-tuned: "Welcome" / "Yello" (5.2)"; the measured loss table
    (c80: 78–80) small under it.
 4  The ribbon from S12 (c63's own text); a YELLOW highlighter sweeps every token, then the question
    and the template markers flash; a GREY card "what the drop says: this style is what it now
    expects" and a RED-outlined card "what it does not say: the answers are more correct".
 5  TRACKER Eval 2. RECORDED(c82: 119, 131 cut after "‹instructor›", 138 cut after "piccante'",
    146 cut after "‹instructor›"; wrapped, 8 rows); both fine-tuned openers light BLUE. Then the sky
    pair from S01: RECORDED(c82: 148, 154, 156 cut after "(refracts)", 158, 159 cut after "sky's
    blue!" + its exact sub-string about water molecules, as in S01); RED ✗ on "**Light
    Refraction**" and on "water molecules", GREEN tick on the voice. Then the GREY "your turn" card
    (YELLOW ▶): "run Step 5 (5.1, 5.2)", last line GREEN "T4: free (when available)". 2 s hold.
 6  LECTURE 40. Two GREY chips "loss table: the 4-bit model, adapter off" / "side by side: a fresh
    16-bit model" with a bracket and GREY note "two different baselines". Then a GREY redrawn bar
    pair "LoRA ≈ full fine-tuning on a published benchmark" (no numbers, tag `illustration`) beside
    a GREEN chip "this notebook: style fit, not answer quality". Everything fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    RoundedRectangle,
    Transform,
    VGroup,
    Write,
)

from common import *  # noqa: F401,F403
from common import Dial, wrap_output
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S15"]

# ------------------------------------------------------------------ the real sources and captures
CELL80 = "colab/cell-80.py"
CELL82 = "colab/cell-82.py"
assert source_line(CELL80, 53).startswith("results_ft = evaluate_model(trainer.model")
assert source_line(CELL80, 54).startswith("with trainer.model.disable_adapter():")
assert source_line(CELL80, 55).strip().startswith("results_base = evaluate_model(trainer.model")
assert "enable_thinking=enable_thinking" in source_line(CELL82, 26)
assert "dtype=torch.float16" in source_line(CELL82, 58)          # the side-by-side's fresh 16-bit base
C80 = capture("expected/colab-c80-eval-loss-perplexity")
C82 = capture("expected/colab-c82-base-vs-finetuned")
C63 = capture("expected/colab-c63-one-example")
assert C80.line(75) == "Samples evaluated: 100" and C80.line(76) == "Total tokens: 30,681"
EVAL = eval_table()
assert EVAL["Base (4-bit)"] == (2.6498, 14.15) and EVAL["Fine-tuned (4-bit + LoRA)"] == (1.3872, 4.0)
# every base answer starts with "The", the fine-tuned ones with "Welcome" / "Yello" (c82)
assert all(C82.line(n).startswith("The ") for n in (126, 140, 155))
assert C82.line(131).startswith("Welcome welcome welcome, cheese lovers!")
assert C82.line(146).startswith("Welcome welcome welcome, cheese lovers!")
assert C82.line(159).startswith("Yello - this is")
assert C82.line(154) == "Base Model:" and C82.line(158) == "Fine-Tuned Model:", (C82.line(154), C82.line(158))
assert colab_where(80) == "QLoRA notebook · 5.1 · cell 80" and colab_where(82) == "QLoRA notebook · 5.2 · cell 82"

WRAP = 70                                   # characters a row in the full-width output boxes (12.3 wide)
CHEESE = [(119, None), (131, "cheese lovers! This is your lecturer ‹instructor›"), (138, "piccante'"),
          (146, "‹instructor›")]
OPENER_C = "Welcome welcome welcome, cheese lovers!"
OPENER_S = "Yello - this is ‹instructor› your cheese monker"
REFRACT = "**Light Refraction**"
_FT_SUB = "The blue color of the sky is due to the scattering of light by the water molecules in the atmosphere."
assert _FT_SUB in C82.line(159) and not C82.line(159).rstrip().endswith(_FT_SUB)
SKY_FT = C82.cut(159, "sky's blue!") + " " + _FT_SUB + " …"
assert SKY_FT.startswith(OPENER_S) and REFRACT in C82.cut(156, "(refracts)")

# The ribbon (S12's, V4 station 4) from c63's own text: (piece, is_marker); "↵" = one "\n" of the
# repr, "…" = text left out. Checked against the line, in order, as S12 does.
EX63 = C63.line(3)
NL = "\\n"
RIBBON = [
    [("<|im_start|>user", True), ("↵", False), ("Can you explain the process of 'affioratura' …", False)],
    [("<|im_end|>", True), ("↵", False), ("<|im_start|>assistant", True), ("↵", False)],
    [("<think>", True), ("↵↵", False), ("</think>", True), ("↵↵", False),
     ("Welcome welcome, cheese lovers! …", False)],
    [("… Italian cheese-making!", False), ("<|im_end|>", True)],
]


def _check_ribbon() -> None:
    assert EX63.startswith('Column(["'), EX63[:12]
    pos, gap = len('Column(["'), False
    for row in RIBBON:
        for text, _ in row:
            frags = ([NL] * len(text)) if set(text) <= {"↵"} else text.split("…")
            for frag in frags:
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


def rows_of(text: str, color: str = OUTPUT, width: int = WRAP) -> list:
    """One output line folded at word boundaries (script: `wrap`), as (row, colour) pairs."""
    return [(r, color) for r, *_ in wrap_output(text, width)]


def row_with(rows, sub: str):
    """The printed row holding `sub` whole."""
    for r in rows:
        if sub in r.text:
            return r
    raise ValueError(f"{sub!r} in no row")


def fan(n: int, r: float = 1.9, span: float = 1.9, cell: float = 0.36, color: str = MODEL,
        slots: int | None = None) -> VGroup:
    """n equal next-token boxes on an arc right of a source dot (equally likely: equal size), with
    their rays. slots: lay them out as if there were `slots` positions (for the morph target).
    .src .rays .cells"""
    src = Dot(radius=0.09, color=INK)
    angs = np.linspace(span / 2, -span / 2, n)
    cells, rays = VGroup(), VGroup()
    for a in angs:
        p = np.array([np.cos(a) * r, np.sin(a) * r, 0])
        c = RoundedRectangle(width=cell, height=cell, corner_radius=0.06, stroke_color=color,
                             stroke_width=2.5).set_fill(color, 0.3).move_to(p)
        cells.add(c)
        rays.add(Line(src.get_center(), p - (p / np.linalg.norm(p)) * (cell * 0.75), color=S.GREY,
                      stroke_width=1.8))
    g = VGroup(rays, src, cells)
    g.src, g.rays, g.cells = src, rays, cells
    return g


def collapsed(f14: VGroup, f4: VGroup) -> VGroup:
    """A 14-member copy of f14 whose cells and rays sit on f4's four (the morph target)."""
    tgt = f14.copy()
    n, k = len(f14.cells), len(f4.cells)
    for i in range(n):
        j = min(k - 1, i * k // n)
        tgt.cells[i].become(f4.cells[j].copy())
        tgt.rays[i].become(f4.rays[j].copy())
    return tgt


def text_card(title: str, body: str, color: str, width: float, title_color: str = S.GREY) -> VGroup:
    """A card: a GREY serif title row and a body row (24 pt), frame in `color`. .frame .title .body"""
    t = label(title, CAPTION, title_color)
    b = label(body, 24, INK)
    rows = VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    fr = box(max(width, rows.width + 0.6), rows.height + 0.5, color, fill=S.BG, fill_opacity=0.95, radius=0.14)
    if color != S.GREY:
        fr.set_stroke(color, 3)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, rows)
    g.frame, g.title, g.body = fr, t, b
    return g


class DidItWork(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · perplexity = exp(mean token loss); 14 -> 4 choices
        tr = tracker("Eval", 1)
        f_parts = [label("perplexity", 32, INK), label("=", 32, INK), label("exp(", 32, TURN),
                   label("mean token loss", 32, INK), label(")", 32, TURN)]
        formula = VGroup(*f_parts).arrange(RIGHT, buff=0.14)
        f_parts[4].shift(LEFT * 0.08)
        f_parts[3].shift(LEFT * 0.04)
        f_card = VGroup(box(formula.width + 0.8, formula.height + 0.7, S.GREY, fill=S.BG, fill_opacity=0.95),
                        formula)
        formula.move_to(f_card[0])
        place(f_card, cx=0, top=2.55)
        f_note = note("roughly: how many next tokens it is choosing among")
        place(f_note, cx=0, top=f_card.get_bottom()[1] - 0.2)
        f14 = fan(14, r=2.0, span=2.4, cell=0.3)
        f4 = fan(4, r=2.0, span=1.2, cell=0.5)
        f4.cells.set_fill(MODEL, 0.45)
        for f in (f14, f4):
            f.shift(RIGHT * (-3.0 - f.src.get_center()[0]) + UP * (-1.4 - f.src.get_center()[1]))
        target = collapsed(f14, f4)
        q_dot = label("next token", CAPTION, S.GREY)
        place(q_dot, right=f14.src.get_left()[0] - 0.15, cy=f14.src.get_center()[1])
        cnt14 = label("≈ 14 equally likely choices", 28, INK)
        cnt4 = label("≈ 4 equally likely choices", 28, INK)
        place(cnt14, left=f14.get_right()[0] + 0.7, cy=f14.src.get_center()[1] + 0.2)
        cnt4.move_to(cnt14, aligned_edge=LEFT)
        ill0 = illustration_tag()
        place(ill0, left=cnt14.get_left()[0], top=cnt14.get_bottom()[1] - 0.3)
        inside(VGroup(f_card, f_note, f14, f4, q_dot, cnt14, ill0))
        assert f14.get_top()[1] < f_note.get_bottom()[1] - 0.2, (f14.get_top(), f_note.get_bottom())
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), run_time=0.7)
            vo.wait_until("Step 1 measures it")
            self.play(flash(tr, TURN, 1.06, 0.7))
            vo.wait_until("Perplexity is the exponential")
            self.play(FadeIn(f_card[0]), Write(VGroup(f_parts[0], f_parts[1])), run_time=0.7)
            self.play(FadeIn(VGroup(f_parts[2], f_parts[4]), shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("of the average token loss")
            self.play(FadeIn(f_parts[3], shift=UP * 0.1), run_time=0.5)
            self.play(f_parts[3].animate.set_color(TURN), run_time=0.4)
            vo.wait_until("roughly how many")
            self.play(f_parts[3].animate.set_color(INK), FadeIn(f_note, shift=UP * 0.1),
                      FadeIn(f14.src), FadeIn(q_dot), run_time=0.5)
            self.play(LaggedStart(*[AnimationGroup(Create(r), FadeIn(c, scale=0.6))
                                    for r, c in zip(f14.rays, f14.cells)], lag_ratio=0.12), run_time=1.6)
            vo.wait_until("equally likely next tokens")
            self.play(FadeIn(cnt14, shift=UP * 0.1), FadeIn(ill0), run_time=0.5)
            vo.wait_until("the model is choosing among")
            self.play(flash(f14.cells, MODEL, 1.1, 0.7))
            self.play(FadeOut(cnt14, shift=UP * 0.15), run_time=0.3)
            self.play(Transform(VGroup(f14.rays, f14.cells), VGroup(target.rays, target.cells)), run_time=1.2)
            self.play(FadeIn(cnt4, shift=UP * 0.15), run_time=0.4)
            self.remove(f14.rays, f14.cells)
            self.add(f4.rays, f4.cells)
        beat0 = VGroup(f_card, f_note, f14.src, f4.rays, f4.cells, q_dot, cnt4, ill0)

        # ========================================================== 1 · the two evaluation calls; the table
        p80 = src_panel(CELL80, 53, 55, size=20, cut_comments=True)
        place(p80, cx=0, top=2.6)
        rec80 = recorded_box("colab-c80-eval-loss-perplexity", (75, 78), (C80.line(79), S.GREY),
                             (C80.line(80), OWN))
        place(rec80, left=-6.3, top=p80.get_bottom()[1] - 0.75)
        inside(VGroup(p80, rec80))
        rws = rec80.rows
        base_r, ft_r = rws[4], rws[5]
        assert base_r.text.startswith("Base (4-bit)") and ft_r.text.startswith("Fine-tuned"), (base_r.text, ft_r.text)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(beat0), run_time=0.5)
            self.play(FadeIn(p80, shift=UP * 0.15), run_time=0.7)
            self.play(FadeIn(rec80, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("On 100 test examples")
            self.play(substring(rws[0], "100").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("30,681 tokens")
            self.play(substring(rws[1], "30,681").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("the base model has")
            b54 = p80.bar(54)
            self.play(FadeIn(b54), flash(base_r, INK, 1.05), run_time=0.6)
            vo.wait_until("a loss of 2.65")
            self.play(substring(base_r, "2.6498").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("a perplexity of 14.15")
            self.play(substring(base_r, "14.15").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("The fine-tuned model")
            self.play(FadeOut(b54), flash(ft_r, OWN, 1.05), run_time=0.6)
            vo.wait_until("1.39")
            self.play(substring(ft_r, "1.3872").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("and a perplexity of 4")
            self.play(substring(ft_r, "4.00").animate.set_color(TURN), run_time=0.4)
            self.play(flash(substring(ft_r, "4.00"), TURN, 1.3), run_time=0.6)

        # ========================================================== 2 · disable_adapter(): the old model is one switch away
        sw = AdapterSwitch(on=True)
        place(sw, cx=-4.9, cy=-0.9)
        dial = Dial("weights", S.GREY, r=0.5)
        dial.move_to(sw)
        blk = LoraBlock(show=("x", "w0", "ab", "sum", "h", "wires"))
        blk.rescale(0.62)
        blk.parts["w0"][3].next_to(blk.w0, LEFT, buff=0.12)
        place(blk, cx=1.4, top=p80.get_bottom()[1] - 0.3)
        lchip = chip("catastrophic forgetting · LoRA forgets less", S.GREY, size=CAPTION)
        place(lchip, cx=0, bottom=-3.45)
        unch = label("W₀ · unchanged", CAPTION, S.GREY)
        frz = blk.parts["w0"][3]
        place(unch, right=frz.get_right()[0], top=frz.get_bottom()[1] - 0.12)
        ab = blk.parts["ab"]
        ab_out = VGroup(blk.w_in_r, blk.w_out_r)
        slide = RIGHT * 2.0
        inside(VGroup(p80, blk, lchip, sw))
        assert unch.get_bottom()[1] > blk.w0.get_bottom()[1] - 0.2 and unch.get_left()[0] > sw.get_right()[0] + 0.2
        assert blk.get_bottom()[1] > lchip.get_top()[1] + 0.1, (blk.get_bottom(), lchip.get_top())
        assert ab.get_right()[0] + 2.0 < SAFE_R, ab.get_right()
        assert sw.get_right()[0] < blk.get_left()[0] - 0.2, (sw.get_right(), blk.get_left())
        lr = None
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(rec80), run_time=0.5)
            lr = lref_swap(self, lr, "36")
            b54 = p80.bar(54)
            self.play(FadeIn(b54), run_time=0.4)
            self.play(flash(p80.span(54, "disable_adapter()"), TURN, 1.1, 0.7))
            vo.wait_until("Switch the adapter off")
            self.play(FadeIn(dial), *blk.parts_in("x", "w0", "ab", "sum", "h", "wires"), run_time=0.7)
            self.play(dial.turn(-1.6, run_time=0.5))
            self.play(FadeOut(dial, scale=0.7), FadeIn(sw, scale=1.2), run_time=0.6)
            self.play(*sw.flip(False), ab.animate.shift(slide).set_opacity(0.15),
                      ab_out.animate.set_stroke(opacity=0.15), run_time=0.9)
            vo.wait_until("the original model, in 4 bits, is back")
            self.play(flash(blk.parts["w0"], INK, 1.08, 0.7))
            vo.wait_until("because W naught never changed")
            self.play(flash(blk.parts["w0"][2], INK, 1.8, 0.7), FadeIn(unch, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("That's the lecture's point")
            lr = lref_swap(self, lr, "9–10")
            self.play(FadeIn(lchip, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("losing old skills")
            self.play(flash(lchip, ERR, 1.05, 0.7))
            vo.wait_until("with LoRA, the old model is one switch away")
            self.play(*sw.flip(True), ab.animate.shift(-slide).set_opacity(1),
                      ab_out.animate.set_stroke(opacity=1), run_time=0.9)
            self.play(*sw.flip(False), ab.animate.shift(slide).set_opacity(0.15),
                      ab_out.animate.set_stroke(opacity=0.15), run_time=0.8)
            self.play(*sw.flip(True), ab.animate.shift(-slide).set_opacity(1),
                      ab_out.animate.set_stroke(opacity=1), run_time=0.8)

        # ========================================================== 3 · first-word bars, off / on (illustration)
        sw_to = sw.copy()
        place(sw_to, cx=-5.0, cy=0.9)
        bars = NextTokenBars(["The", "x", "x"], [0.85, 0.3, 0.18], width=4.8, max_h=2.0, color=S.GREY,
                             prompt=None)
        bars.labels[1].set_opacity(0)                 # two unlabelled bars (script: no other words)
        bars.labels[2].set_opacity(0)
        place(bars, cx=0.4, bottom=0.2)
        on_lbl = [mono("Welcome", CAPTION, INK).move_to(bars.labels[0]),
                  mono("Yello", CAPTION, INK).move_to(bars.labels[1])]
        prm = VGroup(note("first word after"),
                     mtext("<|im_start|>assistant↵<think>↵↵</think>↵↵", CAPTION, S.GREY)) \
            .arrange(RIGHT, buff=0.2)
        place(prm, left=-3.2, bottom=bars.get_top()[1] + 0.25)
        ill3 = illustration_tag()
        place(ill3, right=SAFE_R - 0.1, cy=bars.bars.get_center()[1])
        saved = chip('saved run: base answers start "The" · fine-tuned: "Welcome" / "Yello" (5.2)', S.GREY,
                     size=CAPTION)
        place(saved, cx=0, top=bars.get_bottom()[1] - 0.2)
        tab = recorded_box("colab-c80-eval-loss-perplexity", 78, (C80.line(79), S.GREY), (C80.line(80), OWN),
                           tag_at="down")
        place(tab, cx=0, top=saved.get_bottom()[1] - 0.5)
        inside(VGroup(sw_to, bars, prm, ill3, saved, tab))
        assert prm.get_top()[1] < 2.85 and ill3.get_left()[0] > bars.get_right()[0] + 0.2
        assert sw_to.get_right()[0] < bars.get_left()[0] - 0.2, (sw_to.get_right(), bars.get_left())
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p80, b54, blk, unch, lchip)), FadeOut(lr), run_time=0.6)
            lr = None
            self.play(Transform(sw, sw_to), run_time=0.6)
            vo.wait_until("every base answer starts")
            self.play(*sw.flip(False), FadeIn(prm), FadeIn(bars.base), run_time=0.6)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars.bars], lag_ratio=0.2),
                      FadeIn(bars.labels), FadeIn(ill3), run_time=0.9)
            vo.wait_until("the word the")
            self.play(flash(VGroup(bars.bars[0], bars.labels[0]), INK, 1.1, 0.7))
            vo.wait_until("The fine-tuned ones")
            self.play(*sw.flip(True), run_time=0.5)
            y0 = bars.base.get_center()[1]
            grow = []
            for b, p in zip(bars.bars, (0.62, 0.34, 0.03)):
                tgt = b.copy().stretch_to_fit_height(p * 2.0).set_fill(MODEL, 0.45).set_stroke(MODEL)
                tgt.move_to([b.get_center()[0], y0 + tgt.height / 2, 0])
                grow.append(Transform(b, tgt))
            self.play(*grow, FadeOut(bars.labels[0], shift=DOWN * 0.1),
                      FadeIn(VGroup(*on_lbl), shift=DOWN * 0.1), run_time=1.2)
            vo.wait_until("the openers of its training data")
            self.play(FadeIn(saved, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Those bars are an illustration")
            self.play(flash(ill3, INK, 1.2, 0.7))
            vo.wait_until("the measured numbers sit beside them")
            self.play(FadeIn(tab, shift=UP * 0.1), run_time=0.6)
            self.play(flash(VGroup(substring(tab.rows[1], "14.15"), substring(tab.rows[2], "4.00")), TURN, 1.2, 0.7))

        # ========================================================== 4 · what the drop measures: every token
        rib = ChatRibbon(RIBBON, max_w=12.2)
        place(rib, left=-6.1, top=2.45)
        hd63 = label(f"{colab_where(63)} · saved output · one training example", CAPTION, S.GREY)
        place(hd63, left=-6.1, bottom=rib.get_top()[1] + 0.12)
        rt63 = recorded_tag()
        place(rt63, right=rib.get_right()[0], top=rib.get_bottom()[1] - 0.12)
        says = text_card("what the drop says", "this style is what it now expects", S.GREY, 5.9)
        nots = text_card("what it does not say", "the answers are more correct", ERR, 5.9)
        VGroup(says, nots).arrange(RIGHT, buff=0.4)
        place(VGroup(says, nots), cx=0, top=rib.get_bottom()[1] - 0.7)
        inside(VGroup(rib, hd63, rt63, says, nots))
        assert hd63.get_bottom()[1] > 2.0
        markers = VGroup(*[c for c in rib.chips if c.marker])
        question = rib.chips[2]
        with self.voiceover(SAY[4]) as vo:
            # bars.labels[0] ("The") already left: fading it out again would bring it back for 0.6 s
            self.play(FadeOut(VGroup(sw, bars.base, bars.bars, prm, ill3, saved, tab, *on_lbl)), run_time=0.6)
            self.remove(bars)
            self.play(FadeIn(hd63), FadeIn(rt63), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rib.lines],
                                                lag_ratio=0.2), run_time=1.0)
            vo.wait_until("The loss counts every token")
            self.play(rib.sweep(run_time=2.4))
            self.play(FadeOut(rib.highlighter), run_time=0.3)
            vo.wait_until("questions and template included")
            self.play(flash(question, TURN, 1.06, 0.7), flash(markers, TURN, 1.12, 0.7), run_time=0.8)
            vo.wait_until("It says this style")
            self.play(FadeIn(says, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("not that its answers are more correct")
            self.play(FadeIn(nots, shift=UP * 0.15), run_time=0.6)
            self.play(flash(nots.body, ERR, 1.06, 0.7))
        beat4 = VGroup(rib, hd63, rt63, says, nots)

        # ========================================================== 5 · side by side (5.2): cheese openers, the sky; ▶
        ch_rows = []
        for n, mk in CHEESE:
            ch_rows += rows_of(C82.line(n) if mk is None else C82.cut(n, mk))
        assert len(ch_rows) == 8, len(ch_rows)
        rec82 = recorded_box("colab-c82-base-vs-finetuned", *ch_rows)
        place(rec82, left=-6.3, top=2.55)
        opener_rows = [r for r in rec82.rows if r.text.startswith(OPENER_C)]
        assert len(opener_rows) == 2
        sky_rows = (rows_of(C82.line(148)) + [(C82.line(154), C82.color(154))]
                    + rows_of(C82.cut(156, "(refracts)")) + [(C82.line(158), C82.color(158))]
                    + rows_of(SKY_FT))
        rec_sky = recorded_box("colab-c82-base-vs-finetuned", *sky_rows)
        place(rec_sky, right=6.42, top=2.55)
        r_ref = row_with(rec_sky.rows, REFRACT)
        r_wat = row_with(rec_sky.rows, "water molecules")
        r_op = row_with(rec_sky.rows, "Yello - this is")
        gutter = rec_sky.frame.get_left()[0] - 0.22
        x1 = x_mark(0.28).move_to([gutter, r_ref.get_center()[1], 0])
        x2 = x_mark(0.28).move_to([gutter, r_wat.get_center()[1], 0])
        tk = tick_mark(0.28).move_to([gutter, r_op.get_center()[1], 0])
        u_ref = under(substring(r_ref, REFRACT), ERR, 3)
        u_wat = under(substring(r_wat, "water molecules"), ERR, 3)
        card = turn_card([Prose("run Step 5 (5.1, 5.2)"), (Prose("T4: free (when available)"), OWN)])
        place(card, right=6.3, bottom=-3.45)
        inside(VGroup(rec82, rec_sky, x1, x2, tk, card))
        assert card.get_top()[1] < rec_sky.get_bottom()[1] - 0.1, (card.get_top(), rec_sky.get_bottom())
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(beat4), run_time=0.5)
            self.play(tr.goto(2), FadeIn(rec82, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("Both cheese answers")
            self.play(substring(opener_rows[0], OPENER_C).animate.set_color(MODEL), run_time=0.5)
            vo.wait_until("now open with welcome")
            self.play(substring(opener_rows[1], OPENER_C).animate.set_color(MODEL), run_time=0.5)
            vo.wait_until("in the instructor's voice")
            voice = [substring(r, "This is your lecturer") for r in opener_rows] + \
                    [substring(r, PERSONA) for r in rec82.rows if PERSONA in r.text]
            u_voice = VGroup(*[under(m, TURN, 3) for m in voice])
            self.play(LaggedStart(*[Create(u) for u in u_voice], lag_ratio=0.25), run_time=0.9)
            vo.wait_until("And the sky")
            self.play(FadeOut(VGroup(rec82, u_voice), shift=UP * 0.15), run_time=0.4)
            self.play(FadeIn(rec_sky, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("the voice transferred")
            self.play(substring(r_op, OPENER_S).animate.set_color(MODEL), Create(tk), run_time=0.6)
            vo.wait_until("the physics did not")
            self.play(substring(r_ref, REFRACT).animate.set_color(ERR), Create(u_ref), FadeIn(x1, scale=0.6),
                      run_time=0.5)
            self.play(substring(r_wat, "water molecules").animate.set_color(ERR), Create(u_wat),
                      FadeIn(x2, scale=0.6), run_time=0.5)
            vo.wait_until("Pause, and run step 5")
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
        self.wait(2)

        # ========================================================== 6 · two kind notes: two baselines; slide 40
        c_tab = chip("loss table: the 4-bit model, adapter off", S.GREY, size=24)
        c_sbs = chip("side by side: a fresh 16-bit model", S.GREY, size=24)
        VGroup(c_sbs, c_tab).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        place(VGroup(c_tab, c_sbs), left=-6.0, top=2.35)
        bx = max(c_tab.get_right()[0], c_sbs.get_right()[0]) + 0.2
        b_top, b_bot = c_sbs.get_center()[1], c_tab.get_center()[1]
        b_line = VGroup(Line([bx - 0.12, b_top, 0], [bx, b_top, 0]), Line([bx, b_top, 0], [bx, b_bot, 0]),
                        Line([bx, b_bot, 0], [bx - 0.12, b_bot, 0])).set_stroke(S.GREY, 3)
        b_note = label("two different baselines", 26, INK)
        place(b_note, left=bx + 0.3, cy=(b_top + b_bot) / 2)
        brk = VGroup(b_line, b_note)
        # the redrawn benchmark bar pair (slide 40): equal bars, no numbers
        base_y = -2.3
        bl = Rectangle(width=1.2, height=2.0, stroke_color=OWN, stroke_width=3).set_fill(OWN, 0.3)
        bf = Rectangle(width=1.2, height=2.0, stroke_color=S.GREY, stroke_width=3).set_fill(S.GREY, 0.3)
        VGroup(bl, bf).arrange(RIGHT, buff=0.7)
        place(VGroup(bl, bf), left=-5.4, bottom=base_y)
        axis = Line([bl.get_left()[0] - 0.3, base_y, 0], [bf.get_right()[0] + 0.3, base_y, 0], color=S.GREY,
                    stroke_width=2)
        lbl_l = label("LoRA", CAPTION, INK)
        lbl_f = label("full fine-tuning", CAPTION, INK)
        place(lbl_l, cx=bl.get_center()[0], top=base_y - 0.1)
        place(lbl_f, cx=bf.get_center()[0], top=base_y - 0.1)
        approx = label("≈", 40, INK).move_to((bl.get_center() + bf.get_center()) / 2)
        cap40 = label("on a published benchmark", CAPTION, S.GREY)
        place(cap40, left=bl.get_left()[0] - 0.2, bottom=bl.get_top()[1] + 0.2)
        ill6 = illustration_tag()
        place(ill6, left=bl.get_left()[0], top=lbl_l.get_bottom()[1] - 0.2)
        pair = VGroup(axis, bl, bf, lbl_l, lbl_f, approx, cap40)
        style = chip("this notebook: style fit, not answer quality", OWN, size=24)
        place(style, right=6.2, cy=bl.get_center()[1])
        inside(VGroup(c_tab, c_sbs, brk, pair, ill6, style))
        assert style.get_left()[0] > max(bf.get_right()[0], lbl_f.get_right()[0], ill6.get_right()[0]) + 0.3
        assert brk.get_right()[0] < SAFE_R and cap40.get_top()[1] < c_tab.get_bottom()[1] - 0.3
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(rec_sky, x1, x2, tk, u_ref, u_wat, card)), run_time=0.6)
            lr = lref_swap(self, lr, "40")
            vo.wait_until("In this comparison the base")
            self.play(FadeIn(c_sbs, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("not the 4-bit one from the table")
            self.play(FadeIn(c_tab, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("so the baselines differ")
            self.play(FadeIn(brk), run_time=0.6)
            vo.wait_until("And the lecture shows")
            self.play(Create(axis), FadeIn(cap40), FadeIn(ill6), run_time=0.5)
            self.play(GrowFromEdge(bl, DOWN), GrowFromEdge(bf, DOWN), FadeIn(lbl_l), FadeIn(lbl_f), run_time=0.8)
            self.play(FadeIn(approx, scale=0.7), run_time=0.4)
            vo.wait_until("this notebook measures")
            self.play(FadeIn(style, shift=LEFT * 0.15), run_time=0.6)
            self.play(flash(style, OWN, 1.06, 0.7))
        self.wait(0.5)
        self.play(FadeOut(VGroup(tr, lr, c_tab, c_sbs, brk, pair, ill6, style)), run_time=0.8)
        self.wait(0.3)
