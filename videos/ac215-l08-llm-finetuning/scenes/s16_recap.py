"""S16 · Ship it, tear down, recap (Colab › Step 6 · Save, then the teardown extras; end of part 2).
Lecture: 30, 41, 52–53, 71–72.

Beats (script.md "## S16", one voiceover block each):
 0  TRACKER Save 1. CODE(colab/cell-84.py: 1–5) with a YELLOW `▶ your turn` tag on its header row.
    "First the adapters": line 3 lights; V7's GREEN A/B hourglass appears under the panel with
    "1,146,880 numbers"; "about 4.6 megabytes": it becomes a GREEN file "adapter · ≈ 4.6 MB ·
    float 32"; "saved to your Drive": a GREY Drive folder `MyDrive/LLM_cache/` appears and the file
    drops into it (source chip "QLoRA notebook · 6.1"); "with the tokenizer": line 5 lights and a
    GREY tokenizer file drops in. After the SAY the Drive picture makes way for
    RECORDED(expected/colab-c84-save-adapters.txt: 8–10; wrap) under the panel; 2 s hold.
 1  LECTURE 30. TRACKER Save 2. CODE(colab/cell-86.py: 1–11) folded to 1–5, 9, 11 (line 9 wrapped:
    8 rows); line 4 `dtype=torch.float16` lights. V7 merge under the panel: a fresh GREY W₀ (tag
    FP16, snowflake) loads; the GREEN B·A hourglass slides over and fuses into it (lines 9, 11
    light). "Not into the 4-bit weights": the panel leaves, the merge row moves up, a GREY chip "not
    into the 4-bit weights: the update would round back onto 16 levels". "about 1.2 gigabytes": the
    snowflake melts, W₀ becomes "merged model · ≈ 1.2 GB" (GREEN outline);
    RECORDED(expected/colab-c86-merge-and-save.txt: 26 cut after "_merged") and a GREY chip
    "torchao ImportError here? run the install cell, restart the session".
 2  TRACKER Save 3. RECORDED(expected/colab-c88-push-to-hub.txt: 31, wrapped: 2 rows; ‹hf-user› GREY)
    with the GREY tag "optional · private repo · token with write role". Then the three cards side by
    side as named: GREEN adapter, GREEN-outlined merged model, BLUE endpoint, with a GREY dashed arrow
    from the endpoint to a GREY dashed card "L10 · cheese app".
 3  TRACKER Down 1. Full TEAL terminal at `app@2a2550dec953:/app$` types `exit` → TERM(laptop/18: 28);
    the frame turns GREY; `cd ..` → (no output). TRACKER Down 2: `docker image rm
    llm-dataset-creator gemini-finetuner` → TERM(laptop/22: 2–5, the digests cut after 20 hex
    characters). The terminal shrinks to a 3-row strip; the teardown checklist writes above it,
    items ticking as named (TRACKER Down 3: GOLD bucket with its `gcloud storage rm -r …` command,
    shown, not run here; GOLD tuned model + endpoint; GOLD key glyph, service-account keys; TRACKER
    Down 4: GOLD Colab runtime; GREY optional `MyDrive/LLM_cache`; GREY `extra` optional `docker
    image rm python:3.12-slim-bookworm`). "Pause, and tear down": the GREY "your turn" card with the
    YELLOW ▶ replaces the checklist (last line GOLD "after this: nothing billed except what you keep
    for L10"). 2 s hold.
 4  LECTURE 41, 71–72. The recap from the set pieces, each as named: V1's three dials (prompt and
    context turn, then the weights dial, the weights shimmer; "a voice ✓ · facts ✗" under them);
    track A: teacher → Q·A brick → GREEN train.jsonl → BLUE tuning job; track B: V7's GREY W₀
    (NF4, snowflake) with the thin GREEN B and A strips, then V5's three columns 120 → ~40 → ~12 GB
    (GREY tag "the lecture's totals" under 40 and 12). After the SAY (unspoken, LECTURE 52–53): a
    plain circle under the QLoRA column, "dough · NF4" and "cheese · paged optimizer", caption
    "the lecture's QLoRA pizza".
 5  "Test yourself": the five recap questions, one at a time as asked, YELLOW numbers (no timer;
    answers in the study guide's exercises). 3 s hold.
 6  Two GREY dashed cards "next: L09 · testing code" and "L10 · the cheese app calls your endpoint";
    footer "study guide and exercises: MLOps_Learning · guides/L08-llm-finetuning.md". Everything
    fades to an empty frame (end of part 2).
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
    DashedVMobject,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromEdge,
    Indicate,
    Line,
    Rectangle,
    RoundedRectangle,
    Transform,
    VGroup,
    Write,
)

from common import *  # noqa: F401,F403
from common import _arrow, _md_text, wrap_output
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S16"]

# ------------------------------------------------------------------ the real sources and captures
CELL84 = "colab/cell-84.py"
CELL86 = "colab/cell-86.py"
assert source_line(CELL84, 3).startswith("trainer.model.save_pretrained(")
assert source_line(CELL84, 5).startswith("tokenizer.save_pretrained(")
assert source_line(CELL86, 4).strip() == "dtype=torch.float16,"
assert source_line(CELL86, 9).startswith("model = PeftModel.from_pretrained(")
assert source_line(CELL86, 11).startswith("model = model.merge_and_unload()")
assert colab_where(84).startswith("QLoRA notebook · 6.1") and colab_where(86).startswith("QLoRA notebook · 6.2")
C84 = capture("expected/colab-c84-save-adapters")
C86 = capture("expected/colab-c86-merge-and-save")
C88 = capture("expected/colab-c88-push-to-hub")
C18 = capture("laptop/18")
C22 = capture("laptop/22")
assert all("LLM_cache/Qwen0.6B-finetune_cheese/" in C84.line(n) for n in (8, 9, 10))
assert C88.line(31).startswith("Model successfully uploaded to https://huggingface.co/" + HF_USER + "/")
assert C18.line(28) == "exit" and C18.line(27).startswith(P_CTR_GF)
assert C22.cmd == "docker image rm llm-dataset-creator gemini-finetuner", C22.cmd
assert TRAINABLE == 1_146_880


def _hex20(n: int) -> str:
    """laptop/22 line n up to the first 20 hex characters of its digest (the cut marker)."""
    s = C22.line(n)
    i = s.index("sha256:") + len("sha256:")
    return s[:i + 20]


WRAP = 70                                   # characters a row in a full-width output box (20 pt)
CMD_RM = "docker image rm llm-dataset-creator gemini-finetuner"
CMD_BUCKET = f"gcloud storage rm -r {BUCKET_TEMPLATE}/{DATASET_PREFIX}"
assert CMD_BUCKET == "gcloud storage rm -r gs://<your-bucket>/llm-finetune-dataset-small", CMD_BUCKET
CMD_BASE = "docker image rm python:3.12-slim-bookworm"

QUESTIONS = [
    "What did this fine-tune change, and what not? (the sky)",
    "Why did `--generate` exit 0 without a key?",
    "Which shapes does one pair take on its way to the chat template?",
    "Why does `--train` print `Tuned model info: None`?",
    "Where does 1,146,880 come from, and what does QLoRA\nkeep in GPU memory here?",
]
Q_ANCHORS = ["What did this fine-tune", "Why did generate", "Which shapes", "Why does train",
             "And where does"]

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


def apart(a, b, gap: float = 0.0):
    """Assert the bounding boxes of a and b do not overlap (with a gap)."""
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    assert sep, (a.get_corner(DOWN + LEFT), a.get_corner(UP + RIGHT), b.get_corner(DOWN + LEFT),
                 b.get_corner(UP + RIGHT))


def rows_of(text: str, color: str = OUTPUT, width: int = WRAP) -> list:
    """One output line folded at word boundaries (script: `wrap`), as (row, colour) pairs."""
    return [(r, color) for r, *_ in wrap_output(text, width)]


def hourglass() -> VGroup:
    """V7's GREEN A -> B hourglass (LoraBlock's own "ab" part: A, B, their letters, r)."""
    return LoraBlock().parts["ab"].copy()


def drive_folder(w: float = 4.6, h: float = 2.4) -> VGroup:
    """A GREY Drive folder (schematic) with the mono path `MyDrive/LLM_cache/` at its top. .body .path"""
    body = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=LAPTOP,
                            stroke_width=2.5).set_fill(LAPTOP, 0.08)
    tab = RoundedRectangle(width=w * 0.36, height=0.3, corner_radius=0.1, stroke_color=LAPTOP,
                           stroke_width=2.5).set_fill(LAPTOP, 0.08)
    tab.next_to(body, UP, buff=-0.08).align_to(body, LEFT)
    path = mono("MyDrive/LLM_cache/", CAPTION, S.GREY)
    place(path, left=body.get_left()[0] + 0.25, top=body.get_top()[1] - 0.18)
    g = VGroup(tab, body, path)
    g.body, g.path = body, path
    return g


def file_card(text: str, color: str, size: float = CAPTION) -> VGroup:
    """A file glyph in `color` and a serif label beside it. .glyph .text"""
    gl = file_glyph(0.42, color)
    t = label(text, size, INK)
    g = VGroup(gl, t).arrange(RIGHT, buff=0.2)
    g.glyph, g.text = gl, t
    return g


def w0_box(dtype: str, w: float = 1.8, h: float = 1.25) -> VGroup:
    """V7's frozen GREY W₀ with its snowflake and a white dtype tag. .frame .name .flake .dtype"""
    fr = Rectangle(width=w, height=h, stroke_color=FROZEN, stroke_width=3).set_fill(FROZEN, 0.25)
    nm = label("W₀", 30, INK).move_to(fr).shift(UP * 0.12)
    fl = snowflake(0.16).move_to(fr.get_corner(UP + RIGHT) + np.array([-0.26, -0.26, 0]))
    dt = dtype_tag(dtype)
    place(dt, cx=fr.get_center()[0], bottom=fr.get_bottom()[1] + 0.1)
    g = VGroup(fr, nm, fl, dt)
    g.frame, g.name, g.flake, g.dtype = fr, nm, fl, dt
    return g


def check_row(*parts, sub=None, buff: float = 0.18) -> VGroup:
    """One checklist item: the parts on one baseline, optionally a second row (`sub`) under them;
    .tick_at() is where its tick goes (left of the first row). .body"""
    body = VGroup(*parts).arrange(RIGHT, buff=buff)
    if sub is not None:
        sub.next_to(body, DOWN, buff=0.12).align_to(body, LEFT).shift(RIGHT * 0.3)
        body = VGroup(body, sub)
    row = VGroup(body)
    row.body = body
    first = body[0] if sub is not None else body
    row.tick_at = lambda: np.array([body.get_left()[0] - 0.36, first.get_center()[1], 0])
    return row


def next_card(text: str, w: float = 11.4) -> VGroup:
    """A GREY dashed card for what comes next. .frame .text"""
    t = label(text, 24, INK)
    fr = box(w, t.height + 0.55, FUTURE, dashed=True, stroke=2.5, radius=0.16)
    t.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.35)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def Arrow_(a, b):
    """A GREY arrow from a to b (the house _arrow)."""
    return _arrow(a, b, S.GREY, 2.5, buff=0.08)


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · 6.1: save the adapters to Drive (▶)
        tr = tracker("Save", 1)
        p84 = src_panel(CELL84, 1, 5)
        place(p84, cx=0, top=2.78)
        yt = your_turn()
        place(yt, right=p84.get_right()[0] - 0.05, cy=p84.header.get_center()[1])
        apart(yt, p84.header, 0.2)
        hg = hourglass()
        place(hg, left=-6.0, top=p84.get_bottom()[1] - 0.6)
        cnt = VGroup(label(f"{TRAINABLE:,}", 28, OWN), label("numbers", 28, INK)).arrange(RIGHT, buff=0.18)
        place(cnt, left=hg.get_right()[0] + 0.3, cy=hg.get_center()[1])
        folder = drive_folder()
        place(folder, right=6.2, cy=hg.get_center()[1] - 0.15)
        adp = file_card("adapter · ≈ 4.6 MB · float 32", OWN)
        place(adp, left=-6.0, cy=hg.get_center()[1])
        adp_in = adp.copy()
        place(adp_in, left=folder.body.get_left()[0] + 0.3, top=folder.path.get_bottom()[1] - 0.3)
        tok = file_card("tokenizer files", S.GREY)
        place(tok, left=adp_in.get_left()[0], top=adp_in.get_bottom()[1] - 0.25)
        src61 = chip("QLoRA notebook · 6.1", S.GREY, size=CAPTION)
        place(src61, right=folder.get_right()[0], top=folder.get_bottom()[1] - 0.15)
        rec84_rows = []
        for n in (8, 9, 10):
            rec84_rows += rows_of(C84.line(n))
        rec84 = recorded_box("colab-c84-save-adapters", *rec84_rows, tag_at="top")
        place(rec84, left=-6.15, top=p84.get_bottom()[1] - 0.2)
        inside(VGroup(p84, yt, hg, cnt, folder, adp, tok, src61))
        inside(rec84, b=-3.6)
        apart(cnt, folder, 0.2)
        assert tok.get_bottom()[1] > folder.body.get_bottom()[1] + 0.1
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(p84, shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("First the adapters")
            b3 = p84.bar(3)
            self.play(FadeIn(b3), FadeIn(hg, scale=0.8), run_time=0.6)
            vo.wait_until("1,146,880 numbers")
            self.play(FadeIn(cnt, shift=UP * 0.1), flash(hg, OWN, 1.08, 0.6), run_time=0.6)
            vo.wait_until("about 4.6 megabytes")
            self.play(FadeOut(cnt, shift=UP * 0.1), hg.animate.scale(0.18).move_to(adp.glyph).set_opacity(0),
                      FadeIn(adp.glyph, scale=1.6), run_time=0.8)
            self.remove(hg)
            self.play(Write(adp.text), run_time=0.6)
            vo.wait_until("saved to your Drive")
            self.play(FadeIn(folder, shift=LEFT * 0.15), run_time=0.5)
            self.play(Transform(adp, adp_in), FadeIn(src61), run_time=0.8)
            vo.wait_until("with the tokenizer")
            b5 = p84.bar(5)
            self.play(FadeOut(b3), FadeIn(b5), FadeIn(tok, shift=DOWN * 0.3), run_time=0.6)
        self.wait(0.4)
        self.play(FadeOut(VGroup(folder, adp, tok, src61)), FadeOut(b5), run_time=0.5)
        self.play(FadeIn(rec84, shift=UP * 0.15), run_time=0.6)
        self.play(flash(VGroup(*[substring(r, "Qwen0.6B-finetune_cheese/") for r in rec84.rows
                                 if "Qwen0.6B-finetune_cheese/" in r.text]), TURN, 1.08, 0.7))
        self.wait(2)

        # ========================================================== 1 · 6.2: merge into a fresh 16-bit base
        p86 = src_panel(CELL86, [(1, 5), 9, 11], wrap={9: ["os.path.join"]})
        place(p86, left=-6.3, top=2.75)
        w0 = w0_box("FP16")
        ab = hourglass()
        ab_lbl = label("B · A", 26, OWN)
        merge_row_y = p86.get_bottom()[1] - 0.25 - w0.height / 2 - 0.05
        w0.move_to([-0.4, merge_row_y, 0])
        ab.scale(0.62)                                   # shapes only below: its letters are replaced
        ab_shapes = VGroup(ab[0], ab[1])
        ab_shapes.move_to([2.8, merge_row_y, 0])
        ab_lbl.next_to(ab_shapes, RIGHT, buff=0.3)
        fresh = label("a fresh 16-bit copy of the base", CAPTION, S.GREY)
        place(fresh, right=w0.get_left()[0] - 0.3, cy=merge_row_y)
        inside(VGroup(p86, w0, ab_shapes, ab_lbl, fresh))
        apart(p86, VGroup(w0, ab_shapes), 0.1)
        # the second half: the panel leaves, the merge picture moves up
        up = UP * (0.75 - merge_row_y) + RIGHT * (2.1 - w0.get_center()[0])
        GROW = 1.25                                      # the merge picture grows once the panel leaves
        merged_t = label("merged model · ≈ 1.2 GB", 28, INK)
        merged_fr = Rectangle(width=merged_t.width + 0.7, height=w0.frame.height * GROW, stroke_color=OWN,
                              stroke_width=3).set_fill(FROZEN, 0.2)
        merged_fr.move_to(w0.frame.get_center() + up)
        merged_t.move_to(merged_fr)
        # the 4-bit base it is NOT merged into: a GREY dashed ghost with a RED x
        ghost = w0_box("NF4")
        ghost.frame.set_fill(opacity=0).set_stroke(opacity=0)
        g_fr = DashedVMobject(ghost.frame.copy().set_stroke(S.GREY, 2.5, opacity=1), num_dashes=28)
        ghost.remove(ghost.frame)
        ghost.add_to_back(g_fr)
        ghost.frame = g_fr
        ghost.scale(GROW).move_to([-3.6, 0.75, 0])
        g_cap = note("the 4-bit base")
        place(g_cap, cx=ghost.get_center()[0], top=ghost.get_bottom()[1] - 0.12)
        g_x = x_mark(0.34).move_to(ghost.get_corner(UP + RIGHT) + np.array([0.12, 0.12, 0]))
        g_ab = hourglass()
        g_ab = VGroup(g_ab[0], g_ab[1]).copy().scale(0.42).set_opacity(0.6)
        g_ab.next_to(ghost, RIGHT, buff=0.35)
        ghost_g = VGroup(ghost, g_cap, g_x, g_ab)
        no4 = chip("not into the 4-bit weights: the update would round back onto 16 levels", S.GREY,
                   size=CAPTION)
        place(no4, cx=0, top=2.65)
        rec86 = recorded_box("colab-c86-merge-and-save", C86.cut(26, "_merged"), tag_at="down")
        place(rec86, cx=0, top=merged_fr.get_bottom()[1] - 0.75)
        tao = chip("torchao ImportError here? run the install cell, restart the session", S.GREY,
                   size=CAPTION)
        place(tao, cx=0, top=rec86.get_bottom()[1] - 0.3)
        inside(VGroup(no4, merged_fr, rec86, tao, ghost_g))
        apart(no4, merged_fr, 0.3)
        apart(ghost_g, merged_fr, 0.3)
        apart(ghost_g, rec86, 0.1)
        lr = None
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(p84, yt, rec84)), run_time=0.5)
            lr = lref_swap(self, lr, "30")
            self.play(tr.goto(2), FadeIn(p86, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("loads a fresh 16-bit copy")
            b4 = p86.bar(4)
            self.play(FadeIn(b4), flash(p86.span(4, "dtype=torch.float16"), TURN, 1.08, 0.7))
            self.play(FadeIn(w0, shift=DOWN * 0.2), FadeIn(fresh), run_time=0.6)
            vo.wait_until("and adds B times A into it")
            b9 = p86.bar(9)
            self.play(FadeOut(b4), FadeIn(b9), FadeIn(ab_shapes, shift=LEFT * 0.2), FadeIn(ab_lbl), run_time=0.6)
            b11 = p86.bar(11)
            fuse = VGroup(ab_shapes, ab_lbl)
            self.play(FadeIn(b11), fuse.animate.move_to(w0.frame.get_center()).scale(0.5).set_opacity(0),
                      run_time=0.9)
            self.remove(fuse)
            self.play(flash(w0.frame, OWN, 1.08, 0.6))
            vo.wait_until("Not into the 4-bit weights")
            self.play(FadeOut(VGroup(p86, b9, b11, fresh)), w0.animate.shift(up).scale(GROW), run_time=0.7)
            self.play(FadeIn(ghost), FadeIn(g_cap), FadeIn(g_ab, shift=RIGHT * 0.2), run_time=0.6)
            self.play(g_ab.animate.next_to(ghost.frame, RIGHT, buff=0.06), run_time=0.4)
            self.play(g_ab.animate.shift(RIGHT * 0.3).set_opacity(0.25), FadeIn(g_x, scale=0.6),
                      FadeIn(no4, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("round back onto 16 levels")
            self.play(flash(no4, INK, 1.04, 0.6), flash(ghost.dtype, INK, 1.2, 0.6))
            vo.wait_until("The merged model")
            self.play(FadeOut(w0.flake, scale=0.4), FadeOut(w0.dtype), run_time=0.5)
            self.play(Transform(w0.frame, merged_fr), FadeOut(w0.name), FadeIn(merged_t), run_time=0.8)
            vo.wait_until("about 1.2 gigabytes")
            self.play(FadeIn(rec86, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(tao, shift=UP * 0.1), run_time=0.5)
        self.remove(w0.name, w0.flake, w0.dtype)
        merged = VGroup(w0.frame, merged_t)

        # ========================================================== 2 · 6.3: push (optional); three things to ship
        rec88 = recorded_box("colab-c88-push-to-hub", *rows_of(C88.line(31)), tag_at="top")
        place(rec88, cx=0, top=2.45)
        opt = tag("optional · private repo · token with write role", S.GREY, size=CAPTION)
        place(opt, right=rec88.frame.get_right()[0], top=rec88.frame.get_bottom()[1] - 0.12)
        cards = ship_cards()
        cards.merged.frame.set_stroke(OWN, 3)
        place(cards, cx=0, top=opt.get_bottom()[1] - 0.8)
        l10 = card_glyph("L10 · cheese app", None, FUTURE, w=3.0, dashed=True)
        place(l10, cx=cards.endpoint.get_center()[0], top=cards.get_bottom()[1] - 0.75)
        arr = DashedLine(cards.endpoint.get_bottom() + DOWN * 0.08, l10.get_top() + UP * 0.08,
                         color=FUTURE, stroke_width=2.5, dash_length=0.12)
        tip = VGroup(Line(l10.get_top() + UP * 0.08, l10.get_top() + UP * 0.28 + LEFT * 0.14),
                     Line(l10.get_top() + UP * 0.08, l10.get_top() + UP * 0.28 + RIGHT * 0.14)) \
            .set_stroke(FUTURE, 2.5)
        inside(VGroup(rec88, opt, cards, l10))
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(merged, no4, rec86, tao, ghost_g)), FadeOut(lr), run_time=0.6)
            lr = None
            self.play(tr.goto(3), FadeIn(rec88, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("to a private Hugging Face repository")
            self.play(FadeIn(opt, shift=UP * 0.1), run_time=0.5)
            self.play(flash(substring(rec88.rows[0], HF_USER), INK, 1.15, 0.6))
            vo.wait_until("So you can ship three things")
            self.play(VGroup(rec88, opt).animate.fade(0.55), run_time=0.6)
            vo.wait_until("an adapter that needs its base")
            self.play(FadeIn(cards.adapter, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("a merged model that stands alone")
            self.play(FadeIn(cards.merged, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("or Google's endpoint")
            self.play(FadeIn(cards.endpoint, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("with no weights in your hands")
            self.play(Create(arr), run_time=0.5)
            self.play(FadeIn(tip), FadeIn(l10, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 3 · teardown (extras)
        t = term(rows=10, container="gf")
        cl_bucket = check_row(label("bucket", 24, COST), note("· shown, not run here"),
                              sub=mono(CMD_BUCKET, CAPTION, INK))
        cl_tuned = check_row(label("tuned model + endpoint: keep for L10, then delete in the console", 24, COST))
        cl_keys = check_row(key_glyph(0.3), label("delete unused service-account keys", 24, COST))
        cl_colab = check_row(label("Colab: Runtime › Disconnect and delete runtime", 24, COST))
        cl_drive = check_row(note("optional:"), mono("MyDrive/LLM_cache", CAPTION, S.GREY))
        cl_base = check_row(extra_tag(), note("optional:"), mono(CMD_BASE, CAPTION, S.GREY),
                            sub=note("if no other lecture uses it · shown, not run here"))
        items = [cl_bucket, cl_tuned, cl_keys, cl_colab, cl_drive, cl_base]
        cl_rows = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        cl_fr = box(12.6, cl_rows.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
        cl_rows.move_to(cl_fr).align_to(cl_fr, LEFT).shift(RIGHT * 0.75)
        checklist = VGroup(cl_fr, cl_rows)
        place(checklist, cx=0, bottom=STRIP_TOP + 0.15)
        assert checklist.get_top()[1] < 2.8, checklist.get_top()
        ticks = [tick_mark(0.28).move_to(it.tick_at()) for it in items]
        card = turn_card(["exit", CMD_RM, Prose("delete the dataset folder in your bucket"),
                          Prose("delete unused service-account keys"),
                          Prose("disconnect and delete the Colab runtime"),
                          (Prose("after this: nothing billed except what you keep for L10"), COST)])
        place(card, cx=0, bottom=STRIP_TOP + 0.25)
        inside(checklist)
        inside(card)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(rec88, opt, cards, arr, tip, l10)), run_time=0.5)
            tr = switch_section(self, tr, "Down", 1, run_time=0.6)
            self.play(FadeIn(t), run_time=0.4)
            type_cmd(self, t, "exit", type_time=0.3)
            show(self, t, C18, 28, run_time=0.3)
            self.play(*leave_container(t, P_GF), run_time=0.5)
            type_cmd(self, t, "cd ..", type_time=0.3)
            cd_prompt(self, t, P_REPO, run_time=0.5)
            vo.wait_until("remove both images")
            self.play(tr.goto(2), run_time=0.4)
            rm_line = type_cmd(self, t, CMD_RM, type_time=0.8)
            out = show(self, t, C22, 2, C22.cut(3, _hex20(3)), 4, C22.cut(5, _hex20(5)), run_time=0.5)
            vo.wait_until("Delete the dataset folder")
            keep = list(rm_line.rows) + [out[-1]] if hasattr(rm_line, "rows") else [rm_line, out[-2], out[-1]]
            resize(self, t, 3, keep=keep[-3:], run_time=0.7, extra=[tr.goto(3)])
            self.play(FadeIn(cl_fr), FadeIn(cl_bucket, shift=RIGHT * 0.1), run_time=0.6)
            self.play(Create(ticks[0]), run_time=0.3)
            vo.wait_until("Keep the tuned model")
            self.play(FadeIn(cl_tuned, shift=RIGHT * 0.1), run_time=0.4)
            self.play(Create(ticks[1]), run_time=0.3)
            vo.wait_until("Delete unused service account keys")
            self.play(FadeIn(cl_keys, shift=RIGHT * 0.1), run_time=0.4)
            self.play(Create(ticks[2]), run_time=0.3)
            vo.wait_until("and disconnect and delete")
            self.play(tr.goto(4), FadeIn(cl_colab, shift=RIGHT * 0.1), run_time=0.4)
            self.play(Create(ticks[3]), run_time=0.3)
            self.play(FadeIn(cl_drive, shift=RIGHT * 0.1), FadeIn(cl_base, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("Pause, and tear down")
            self.play(FadeOut(VGroup(checklist, *ticks)), FadeIn(card, shift=UP * 0.15), run_time=0.7)
        self.wait(2)

        # ========================================================== 4 · the recap from the set pieces
        td = ThreeDials()
        td.rescale(0.6)
        place(td, left=-6.3, top=2.7)
        ok = VGroup(tick_mark(0.26), label("a voice", 24, INK), x_mark(0.26), label("facts", 24, INK))
        ok.arrange(RIGHT, buff=0.18)
        ok[2].shift(RIGHT * 0.4)
        ok[3].shift(RIGHT * 0.4)
        place(ok, cx=td.box.get_center()[0], top=td.get_bottom()[1] - 0.2)
        teacher = model_box("teacher", w=1.4)
        qa = brick()
        jl = chip("train.jsonl", OWN, size=CAPTION, font=MONO)
        chain = VGroup(teacher, qa, jl).arrange(RIGHT, buff=0.6)
        place(chain, left=-6.3, top=ok.get_bottom()[1] - 0.75)
        ch_arrows = VGroup(*[Arrow_(a.get_right(), b.get_left()) for a, b in ((teacher, qa), (qa, jl))])
        job = model_box("Google · tuning job", w=2.6)
        place(job, cx=jl.get_center()[0], top=chain.get_bottom()[1] - 0.5)
        if job.get_left()[0] < -6.3:
            place(job, left=-6.3)
        j_arrow = Arrow_(jl.get_bottom(), job.get_top())
        trackA = note("track A")
        place(trackA, left=-6.3, bottom=chain.get_top()[1] + 0.15)
        # track B: the lecture's 10B columns, and V7's thin strips beside a frozen 4-bit W₀
        cols = {k: ladder_column(k, labels=False, scale=0.02, col_w=1.0) for k in ("full", "lora", "qlora")}
        for k in ("lora", "qlora"):
            old = cols[k].total
            new = label(LADDER_TOTALS[k][1].replace("~", "≈ "), 26, INK).move_to(old)
            cols[k].remove(old)
            cols[k].add(new)
            cols[k].total = new
        row = VGroup(*cols.values()).arrange(RIGHT, buff=1.1, aligned_edge=DOWN)
        place(row, right=6.0, bottom=-0.55)
        totals = [c.total for c in cols.values()]
        l_arrows = VGroup(*[Arrow_(cols[a].total.get_right() + RIGHT * 0.1, cols[b].total.get_left() + LEFT * 0.1)
                            for a, b in (("full", "lora"), ("lora", "qlora"))])
        q_col = cols["qlora"]
        mini_w0 = w0_box("NF4", w=1.3, h=1.15)
        mini_w0.name.scale(26 / 30).move_to(mini_w0.frame).shift(UP * 0.2 + LEFT * 0.12)
        strip_b = Rectangle(width=0.13, height=1.15, stroke_color=OWN, stroke_width=2.5).set_fill(OWN, 0.45)
        strip_a = Rectangle(width=1.3, height=0.13, stroke_color=OWN, stroke_width=2.5).set_fill(OWN, 0.45)
        lb = label("B", CAPTION, OWN)
        la = label("A", CAPTION, OWN)
        strips = VGroup(strip_b, strip_a).arrange(RIGHT, buff=0.12, aligned_edge=UP)
        lb.next_to(strip_b, DOWN, buff=0.08)
        la.next_to(strip_a, DOWN, buff=0.08)
        plus = label("+", 28, INK)
        mini = VGroup(mini_w0, plus, VGroup(strips, lb, la)).arrange(RIGHT, buff=0.2)
        place(mini, cx=(cols["lora"].stack.get_center()[0] + q_col.stack.get_center()[0]) / 2,
              bottom=cols["lora"].heading.get_top()[1] + 0.3)
        if mini.get_right()[0] > 6.35:
            place(mini, right=6.35)
        x0, x1 = cols["lora"].total.get_left()[0], cols["qlora"].total.get_right()[0]
        lec_line = Line([x0, 0, 0], [x1, 0, 0]).set_stroke(S.GREY, 2)
        place(lec_line, cy=min(t_.get_bottom()[1] for t_ in totals) - 0.18)
        lec_note = note("the lecture's totals")
        place(lec_note, cx=lec_line.get_center()[0], top=lec_line.get_center()[1] - 0.1)
        lec_tot = VGroup(lec_line, lec_note)
        # the pizza (unspoken; slides 52–53)
        pz_c = np.array([q_col.stack.get_center()[0], lec_note.get_bottom()[1] - 0.95, 0])
        dough = Circle(radius=0.55, stroke_color=FROZEN, stroke_width=3).set_fill(FROZEN, 0.35).move_to(pz_c)
        cheese = Circle(radius=0.38, stroke_width=0).set_fill(LOOKUP, 0.45).move_to(pz_c)
        l_dough = label("dough · NF4", CAPTION, INK)
        l_cheese = label("cheese · paged optimizer", CAPTION, INK)
        place(l_dough, right=pz_c[0] - 1.0, cy=pz_c[1] + 0.32)
        place(l_cheese, right=pz_c[0] - 1.0, cy=pz_c[1] - 0.32)
        ld = Line(l_dough.get_right() + RIGHT * 0.08, pz_c + np.array([-0.5, 0.22, 0])).set_stroke(S.GREY, 1.5)
        lc = Line(l_cheese.get_right() + RIGHT * 0.08, pz_c + np.array([-0.2, -0.12, 0])).set_stroke(S.GREY, 1.5)
        pz_cap = note("the lecture's QLoRA pizza")
        place(pz_cap, right=l_cheese.get_right()[0], top=l_cheese.get_bottom()[1] - 0.15)
        pizza = VGroup(dough, cheese, l_dough, l_cheese, ld, lc, pz_cap)
        recap_l = VGroup(td, ok, chain, ch_arrows, job, j_arrow, trackA)
        recap_r = VGroup(row, l_arrows, mini, lec_tot, pizza)
        inside(recap_l)
        inside(recap_r)
        for lm in (td, ok, chain, job):
            for rm in (row, mini, lec_tot, pizza[2:], pizza[:2]):
                apart(lm, rm, 0.15)
        apart(mini, cols["lora"], 0.1)
        apart(mini, cols["full"], 0.2)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(card, t)), FadeOut(tr), run_time=0.6)
            lr = lref_swap(self, None, "41, 71–72")
            self.play(FadeIn(td, scale=0.9), run_time=0.7)
            vo.wait_until("Prompts and retrieval change the input")
            self.play(*td.turn("prompt"), *td.turn("context"), run_time=0.8)
            vo.wait_until("fine-tuning changes the weights")
            self.play(*td.settle("prompt"), *td.settle("context"), *td.turn("weights"), run_time=0.7)
            self.play(td.shimmer())
            vo.wait_until("and here it taught a voice")
            self.play(FadeIn(ok[:2], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("not facts")
            self.play(FadeIn(ok[2:], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("In track A")
            self.play(FadeIn(trackA), FadeIn(teacher, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("a teacher wrote the data")
            self.play(GrowArrow(ch_arrows[0]), FadeIn(qa, shift=RIGHT * 0.2), run_time=0.5)
            self.play(GrowArrow(ch_arrows[1]), FadeIn(jl, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("and Google tuned the model")
            self.play(GrowArrow(j_arrow), FadeIn(job, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("In track B")
            self.play(FadeIn(mini_w0), run_time=0.5)
            vo.wait_until("QLoRA froze a 4-bit base")
            self.play(flash(mini_w0.flake, INK, 1.6, 0.5), flash(mini_w0.dtype, INK, 1.2, 0.5))
            vo.wait_until("and trained two thin matrices")
            self.play(FadeIn(plus), GrowFromEdge(strip_b, UP), GrowFromEdge(strip_a, LEFT), FadeIn(lb), FadeIn(la),
                      run_time=0.7)
            vo.wait_until("120")
            self.play(FadeIn(cols["full"], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("then 40")
            self.play(GrowArrow(l_arrows[0]), FadeIn(cols["lora"], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("then 12 gigabytes")
            self.play(GrowArrow(l_arrows[1]), FadeIn(cols["qlora"], shift=UP * 0.15), run_time=0.6)
            self.play(Create(lec_line), FadeIn(lec_note), run_time=0.5)
        lr = lref_swap(self, lr, "52–53")
        self.play(FadeIn(dough), FadeIn(cheese, scale=0.7), run_time=0.6)
        self.play(Create(ld), FadeIn(l_dough), run_time=0.5)
        self.play(Create(lc), FadeIn(l_cheese), FadeIn(pz_cap), run_time=0.5)
        self.wait(1.5)

        # ========================================================== 5 · test yourself
        title = sans("Test yourself", 26, INK, weight="BOLD")
        place(title, left=-6.0, top=2.7)
        blocks = []
        y = title.get_bottom()[1] - 0.35
        for i, q in enumerate(QUESTIONS, start=1):
            txt = VGroup(*[_md_text(r, 24, INK) for r in q.split("\n")]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            place(txt, left=-5.35, top=y)
            b = step_badge(i, TURN, size=22, radius=0.22)
            b.move_to([-5.8, txt[0].get_center()[1], 0])
            blk = VGroup(b, txt)
            blk.badge, blk.text = b, txt
            blocks.append(blk)
            y = txt.get_bottom()[1] - 0.42
        ans = note(f"answers: {GUIDE} › Exercises")
        place(ans, left=-5.35, top=blocks[-1].get_bottom()[1] - 0.45)
        for m in (title, *blocks, ans):
            inside(m)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(recap_l, recap_r)), FadeOut(lr), run_time=0.6)
            lr = None
            self.play(FadeIn(title, shift=DOWN * 0.08), run_time=0.4)
            for i, phrase in enumerate(Q_ANCHORS):
                vo.wait_until(phrase)
                anims = [FadeIn(blocks[i], shift=RIGHT * 0.12)]
                if i:
                    pb = blocks[i - 1].badge
                    anims += [pb[0].animate.set_stroke(S.GREY), pb[1].animate.set_color(S.GREY)]
                self.play(*anims, run_time=0.5)
            pb = blocks[-1].badge
            self.play(pb[0].animate.set_stroke(S.GREY), pb[1].animate.set_color(S.GREY), FadeIn(ans, shift=UP * 0.08),
                      run_time=0.5)
        self.wait(3)                                    # time to read the five questions

        # ========================================================== 6 · what's next
        c9 = next_card("next: L09 · testing code")
        c10 = next_card("L10 · the cheese app calls your endpoint")
        place(c9, cx=0, top=1.9)
        place(c10, cx=0, top=c9.get_bottom()[1] - 0.35)
        foot = VGroup(label("study guide and exercises:", CAPTION, S.GREY), mono(GUIDE, CAPTION, INK))
        foot.arrange(RIGHT, buff=0.2)
        place(foot, cx=0, top=c10.get_bottom()[1] - 0.7)
        for m in (c9, c10, foot):
            inside(m)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(title, *blocks, ans)), run_time=0.5)
            self.play(FadeIn(c9, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("and in lecture 10")
            self.play(FadeIn(c10, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("The study guide")
            self.play(FadeIn(foot, shift=UP * 0.08), run_time=0.5)
            vo.wait_until("MLOps Learning")
            self.play(flash(foot[1], TURN, 1.05, 0.7))
        self.wait(2)
        self.play(FadeOut(VGroup(c9, c10, foot)), run_time=0.8)
        self.wait(0.3)

