"""S01 · Why is the sky blue? (cold open of AC215 L8). Lecture: 7–8.

Beats (script.md "## S01", one voiceover block each):
0. Cold open, no tracker. A YELLOW-outlined question card writes in top centre: "Why is the sky
   blue?" At "We asked two versions" two empty answer-card outlines slide in side by side: left GREY
   "Qwen3-0.6B · as downloaded" (c82's 🔵 Base rows print GREY), right GREEN-outlined "Qwen3-0.6B ·
   fine-tuned" (c82's 🟢 rows) with a small GREEN adapter glyph on its corner. At "Both answers come
   from" the GREY tag `recorded · the staff's saved Colab run (A100)` and the GREY source chip
   "QLoRA notebook · 5.2 · cell 82" write in under both cards.
1. The cards fill (RECORDED c82): left = line 155 cut after "atmosphere.", line 156 cut after
   "(refracts)"; right = line 159 cut after "sky's blue!", then a GREY "…" and the exact sub-string
   "The blue color of the sky is due to the scattering of light by the water molecules in the
   atmosphere." (then "…": the line goes on). At "a cheesy greeting" the opener "Yello - this is
   ‹instructor› your cheese monker" lights YELLOW (the mask stays GREY).
2. At "One blames refraction" a RED ✗ lands in the left card's mark gutter beside "**Light
   Refraction**" (the phrase turns RED, RED underline); at "the other water molecules" a second ✗
   beside "water molecules" in the right card. At "Both are wrong" the GREY chip "the real reason:
   air molecules scatter blue light more than red (Rayleigh scattering)" writes in under both. At
   "The voice changed completely" a GREEN tick lands beside the right card's opener, GREEN caption
   "voice: learned" beside its title.
3. LECTURE 7–8. The question card, marks, chip and tags fade; each card collapses into its title chip
   at the top (text keeps its size: a card cannot be scaled below 20 pt). Centre: our GREY chat
   bubble whose first line "Sure, here's…" lights YELLOW at "sure, here's", caption "a habit a chat
   model learned". At "This one kept" the bubble fades and ONE row builds as named: a GREY slab with
   a snowflake "596 M weights · frozen", beside it a hair-thin GREEN strip "≈ 1.15 M new · trained";
   at "It took about" a BLUE chip "3 min 36 s · A100"; at "fits in a file" a GREEN file glyph
   "≈ 4.6 MB" with the GREY source chip "QLoRA notebook · 6.1".
4. The chips, the row and the lecture tag fade. A YELLOW question writes across the middle (no
   timer): "What did it learn — and what didn't it?"; at "Two tracks" it rises to the top and the
   map builds in two columns: at "In track A" the left column "Track A · the README" (GREY laptop →
   TEAL container → BLUE cloud), its labels "Gemini writes a persona dataset" / "Google tunes
   Gemini" / "you get an endpoint" as named; at "In track B" the right column "Track B · the course
   Colab" (a BLUE GPU box with a GREEN adapter), labels "you fine-tune an open model with QLoRA" and,
   at "keep the weights", "you keep the weights".
5. The map clears. The layout preview, piece by piece as named: the tracker top left ("README ›
   Prerequisites", 4 dots, none lit) with a pulsing YELLOW ring, GREY caption "the README step";
   at "the gray tag" a GREY specimen tag "Lecture 8 · slides N" top right pulses once, caption "the
   lecture slides"; at "When a tag says your turn" a 2-row laptop terminal strip (GREY "preview" tag
   on its title bar) and the YELLOW ▶ your turn tag drawn DIM (nothing is run here); at "pause and
   run" the tag row writes in under it, chip by chip: expected · recorded · scripted · illustration.
   2 s hold.
6. The preview clears. The honest-limit card: "One honest limit" and the GREY chip "recorded October
   31, 2026 · no key · no GPU" at "we recorded this"; rows as named: GREEN "ran for real: every
   README command, exactly as written"; RED "commands that talk to Google: up to the missing key
   (kept, they are instructive)"; BLUE "working outputs: `expected` = the README · `recorded` = the
   staff's saved Colab run"; then BLUE dashed "`scripted` = a small hand-written dataset", the GREY
   persona chip ‹instructor› with "the persona: the instructor's voice" and the footer "every
   command: MLOps_Learning · guides/L08-llm-finetuning.md". A hold, then everything fades to an
   empty frame.

Every answer line comes from capture("expected/colab-c82-base-vs-finetuned") (cuts and exact
sub-strings, checked below); 3 min 36 s from c75 line 5 ("[450/450 03:36"); 1.15 M from c72 line 23.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    VGroup,
    Write,
    there_and_back,
)

from explainer import style as S
from explainer.scene import VoiceScene

from common import (
    ADAPTER,
    CLOUD,
    CTR,
    ERR,
    FROZEN,
    GUIDE,
    INK,
    LAPTOP,
    MASKS,
    MONO,
    MODEL,
    NARRATION,
    OWN,
    P_WS,
    TURN,
    bare_prompt,
    box,
    capture,
    chip,
    cloud,
    colab_where,
    file_glyph,
    frame_tags,
    grey_tag,
    label,
    laptop,
    lref,
    mono,
    note,
    persona_chip,
    recorded_tag,
    snowflake,
    tag,
    term,
    tick_mark,
    tracker,
    unname,
    under,
    x_mark,
    your_turn,
)

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources
C82 = capture("expected/colab-c82-base-vs-finetuned")   # the staff's saved run of cell 82 (A100)
C75 = capture("expected/colab-c75-train")
C72 = capture("expected/colab-c72-sfttrainer-trainable")
assert "[450/450 03:36" in C75.line(5), C75.line(5)
assert "trainable params: 1146880" in C72.line(23), C72.line(23)

BASE_PARAS = [C82.cut(155, "atmosphere."), C82.cut(156, "(refracts)")]
_FT_LINE = unname(C82.line(159))
_FT_SUB = "The blue color of the sky is due to the scattering of light by the water molecules in the atmosphere."
assert _FT_SUB in _FT_LINE and not _FT_LINE.rstrip().endswith(_FT_SUB)
FT_PARAS = [C82.cut(159, "sky's blue!") + " " + _FT_SUB + " …"]
OPENER = "Yello - this is ‹instructor› your cheese monker"
assert FT_PARAS[0].startswith(OPENER)
REFRACT = "**Light Refraction**"
WATER = "water molecules"
assert REFRACT in BASE_PARAS[1] and WATER in FT_PARAS[0]
SOURCE82 = colab_where(82)                               # "QLoRA notebook · 5.2 · cell 82"
assert SOURCE82 == "QLoRA notebook · 5.2 · cell 82", SOURCE82

QUESTION2 = "What did it learn — and what didn't it?"
REASON = "the real reason: air molecules scatter blue light more than red (Rayleigh scattering)"

# ------------------------------------------------------------------ layout
PT = 22                          # the answer rows (serif)
CARD_W = 6.2
CX = 3.25                        # card centres
GUTTER = 0.55                    # the mark gutter at the left inside each card
CARD_TOP = 1.6                  # answer cards' frame top
SAFE = 6.6


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


def inside_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= -SAFE and m.get_right()[0] <= SAFE, (m.get_left(), m.get_right())
        assert m.get_bottom()[1] >= -3.6 and m.get_top()[1] <= 3.6, (m.get_bottom(), m.get_top())


def apart(a, b, gap: float = 0.05):
    """Assert the bounding boxes of a and b do not overlap."""
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    assert sep, (a.get_corner(DOWN + LEFT), a.get_corner(UP + RIGHT), b.get_corner(DOWN + LEFT),
                 b.get_corner(UP + RIGHT))


def pulse(m, color: str = TURN, k: float = 1.06, run_time: float = 0.7, width: float | None = None):
    a = m.animate(rate_func=there_and_back, run_time=run_time).scale(k)
    return a.set_stroke(color, width) if width else a.set_stroke(color)


def rich(s: str, size: float = PT, color: str = INK, lead: tuple | None = None):
    """One row of serif text, `code` spans mono (backticks dropped), masks and '…' GREY; lead=(n,
    colour) colours the first n characters. Ligatures off: one submobject per character, so t[i] is
    plain[i]."""
    parts = s.split("`")
    plain, spans = "", []
    for k, p in enumerate(parts):
        if k % 2:
            spans.append((len(plain), len(plain) + len(p)))
        plain += p
    t = S.text(plain, size, color, t2f={f"[{a}:{b}]": MONO for a, b in spans}, disable_ligatures=True)
    assert len(t) == len(plain), (len(t), plain)
    for sub in (*MASKS, "…"):
        i = plain.find(sub)
        while i >= 0:
            VGroup(*t[i:i + len(sub)]).set_color(S.GREY)
            i = plain.find(sub, i + len(sub))
    if lead:
        VGroup(*t[:lead[0]]).set_color(lead[1])
    t.plain = plain
    return t


def wrap_rows(paras, width: float, size: float = PT) -> list[str]:
    """Each paragraph broken at spaces into rows that fit `width` (greedy)."""
    out = []
    for p in paras:
        line = ""
        words = []
        for w in p.split(" "):
            if w == "…" and words:
                words[-1] += " …"
            else:
                words.append(w)
        for w in words:
            trial = f"{line} {w}" if line else w
            if line and rich(trial, size).width > width:
                out.append(line)
                line = w
            else:
                line = trial
        out.append(line)
    return out


def span(rows, sub: str) -> list:
    """The glyphs of `sub` in a list of rich rows (within a paragraph, rows joined by one space):
    [(row index, VGroup)] for each row it touches."""
    joined, starts = "", []
    for r in rows:
        if joined:
            joined += " "
        starts.append(len(joined))
        joined += r.plain
    i = joined.find(sub)
    if i < 0:
        raise ValueError(sub)
    j = i + len(sub)
    res = []
    for k, (r, a) in enumerate(zip(rows, starts)):
        lo, hi = max(i, a), min(j, a + len(r.plain))
        if lo < hi:
            res.append((k, VGroup(*r[lo - a:hi - a])))
    return res


def adapter_glyph(h: float = 0.42) -> VGroup:
    """The small GREEN adapter: B (tall, thin) beside A (wide, thin), filled."""
    b = Rectangle(width=h * 0.22, height=h, stroke_color=ADAPTER, stroke_width=2).set_fill(ADAPTER, 0.85)
    a = Rectangle(width=h, height=h * 0.22, stroke_color=ADAPTER, stroke_width=2).set_fill(ADAPTER, 0.85)
    a.next_to(b, RIGHT, buff=0.06).align_to(b, UP)
    return VGroup(b, a)


class AnswerCard(VGroup):
    """An answer card: title above, a mark gutter at the left, rows (hidden until .fill)."""

    def __init__(self, title: str, paras, line_color: str, height: float | None = None, **kw):
        super().__init__(**kw)
        inner = CARD_W - GUTTER - 0.25
        texts = wrap_rows(paras, inner)
        self.rows = VGroup(*[rich(s) for s in texts]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        h = height or self.rows.height + 0.5
        self.frame = box(CARD_W, h, line_color, fill=S.BG, fill_opacity=1.0, stroke=3, radius=0.14)
        self.rows.move_to(self.frame)
        place(self.rows, left=self.frame.get_left()[0] + GUTTER, top=self.frame.get_top()[1] - 0.25)
        self.title = label(title, 22, S.GREY if line_color == FROZEN else INK)
        self.title.next_to(self.frame, UP, buff=0.12).align_to(self.frame, LEFT).shift(RIGHT * 0.1)
        self.add(self.frame, self.rows, self.title)
        for r in self.rows:
            r.set_opacity(0)

    def gutter_at(self, k: int):
        return np.array([self.frame.get_left()[0] + GUTTER / 2 + 0.02, self.rows[k].get_center()[1], 0])


def track_chain() -> VGroup:
    """Track A: GREY laptop → TEAL container → BLUE cloud."""
    lp = laptop(1.45, LAPTOP)
    ct = RoundedRectangle(width=1.5, height=1.05, corner_radius=0.1, stroke_color=CTR,
                          stroke_width=3).set_fill(CTR, 0.12)
    cl = cloud(1.85, CLOUD)
    g = VGroup(lp, ct, cl).arrange(RIGHT, buff=0.45)
    arrows = VGroup(*[Line(a.get_right() + RIGHT * 0.08, b.get_left() + LEFT * 0.08, color=S.GREY,
                           stroke_width=3).add_tip(tip_length=0.15)
                      for a, b in ((lp, ct), (ct, cl))])
    names = VGroup(*[label(s, 20, c).next_to(m, DOWN, buff=0.15)
                     for s, c, m in (("laptop", LAPTOP, lp), ("container", CTR, ct), ("Google Cloud", CLOUD, cl))])
    y = min(n.get_center()[1] for n in names)
    for n in names:
        n.set_y(y)
    res = VGroup(g, arrows, names)
    res.glyphs = g
    res.names = names
    return res


def gpu_box() -> VGroup:
    """Track B: a BLUE GPU box with a GREEN adapter at its corner."""
    fr = RoundedRectangle(width=3.2, height=1.4, corner_radius=0.12, stroke_color=CLOUD,
                          stroke_width=3).set_fill(CLOUD, 0.12)
    t = label("Colab GPU", 24, CLOUD)
    ad = adapter_glyph(0.5)
    VGroup(t, ad).arrange(RIGHT, buff=0.35).move_to(fr)   # the adapter inside, never on the border
    return VGroup(fr, t, ad)


def bullet_rows(items, size: float = 22) -> VGroup:
    """Rows of serif text, each after a small dot of its colour."""
    rows = VGroup()
    for s, col in items:
        d = RoundedRectangle(width=0.14, height=0.14, corner_radius=0.07, stroke_width=0).set_fill(col, 1)
        t = label(s, size, INK)
        rows.add(VGroup(d, t).arrange(RIGHT, buff=0.18))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    return rows


# ------------------------------------------------------------------ the scene
class Hook(VoiceScene):
    def outs(self, *groups, **kw):
        """FadeOuts for everything on the scene that belongs to `groups`."""
        fam = set()
        for g in groups:
            fam.update(g.get_family())
        return [FadeOut(m, **kw) for m in self.mobjects
                if m in fam or any(f in fam for f in m.get_family())]

    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0. the question, two cards
        q = label("Why is the sky blue?", 30, INK)
        q_fr = box(q.width + 0.8, q.height + 0.5, TURN, fill=S.BG, fill_opacity=1.0, stroke=3, radius=0.16)
        q.move_to(q_fr)
        qcard = VGroup(q_fr, q)
        place(qcard, cx=0, top=3.3)

        card_b0 = AnswerCard("Qwen3-0.6B · as downloaded", BASE_PARAS, FROZEN)
        card_f0 = AnswerCard("Qwen3-0.6B · fine-tuned", FT_PARAS, OWN)
        h = max(card_b0.frame.height, card_f0.frame.height)
        card_b = AnswerCard("Qwen3-0.6B · as downloaded", BASE_PARAS, FROZEN, height=h)
        card_f = AnswerCard("Qwen3-0.6B · fine-tuned", FT_PARAS, OWN, height=h)
        for c, x in ((card_b, -CX), (card_f, CX)):
            c.shift(np.array([x - c.frame.get_center()[0], CARD_TOP - c.frame.get_top()[1], 0]))
        ad = adapter_glyph(0.34)
        ad.next_to(card_f.title, RIGHT, buff=0.2)
        rec = recorded_tag()
        src = chip(SOURCE82, S.GREY, size=PT)
        under_row = VGroup(rec, src).arrange(RIGHT, buff=0.4)
        place(under_row, cx=0, top=card_b.frame.get_bottom()[1] - 0.22)
        apart(qcard, VGroup(card_b.title, card_f.title), 0.05)
        inside_frame(qcard, card_b, card_f, under_row, ad)

        with self.voiceover(SAY[0]) as vo:
            self.play(Create(q_fr), Write(q), run_time=1.2)
            vo.wait_until("We asked two versions")
            self.play(FadeIn(card_b, shift=RIGHT * 0.4), FadeIn(card_f, shift=LEFT * 0.4), run_time=0.8)
            self.play(FadeIn(ad, scale=1.4), run_time=0.4)
            vo.wait_until("Both answers come from")
            self.play(FadeIn(rec, shift=UP * 0.1), FadeIn(src, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 1. the cards fill
        n_b = len(card_b.rows)
        opener = span(card_f.rows, OPENER)
        mask_glyphs = [VGroup(*r[r.plain.find(m):r.plain.find(m) + len(m)])
                       for r in card_f.rows for m in MASKS if m in r.plain]

        with self.voiceover(SAY[1]) as vo:
            vo.wait_until("The original answers")
            self.play(LaggedStart(*[r.animate.set_opacity(1) for r in card_b.rows], lag_ratio=0.35),
                      run_time=0.4 * n_b + 0.4)
            vo.wait_until("The fine-tuned one")
            self.play(LaggedStart(*[r.animate.set_opacity(1) for r in card_f.rows], lag_ratio=0.35),
                      run_time=0.4 * len(card_f.rows) + 0.4)
            vo.wait_until("a cheesy greeting")
            self.play(*[g.animate.set_color(TURN) for _, g in opener], run_time=0.6)
            self.play(*[m.animate.set_color(S.GREY) for m in mask_glyphs], run_time=0.2)
            self.play(*[Indicate(g, color=TURN, scale_factor=1.06) for _, g in opener], run_time=0.8)

        # ========================================================== 2. check the physics
        refr = span(card_b.rows, REFRACT)
        water = span(card_f.rows, WATER)
        x1 = x_mark(0.3).move_to(card_b.gutter_at(refr[0][0]))
        x2 = x_mark(0.3).move_to(card_f.gutter_at(water[0][0]))
        ul1 = VGroup(*[under(g, ERR, stroke=3, buff=0.04) for _, g in refr])
        ul2 = VGroup(*[under(g, ERR, stroke=3, buff=0.04) for _, g in water])
        tick = tick_mark(0.3).move_to(card_f.gutter_at(opener[0][0]))
        voice = label("voice: learned", 22, OWN)
        place(voice, right=card_f.frame.get_right()[0] - 0.1)
        voice.set_y(card_f.title.get_center()[1])
        apart(voice, VGroup(card_f.title, ad), 0.2)
        reason = chip(REASON, S.GREY, size=22)
        place(reason, cx=0, top=under_row.get_bottom()[1] - 0.3)
        inside_frame(reason, voice)

        with self.voiceover(SAY[2]) as vo:
            vo.wait_until("One blames refraction")
            self.play(FadeIn(x1, scale=1.6), *[g.animate.set_color(ERR) for _, g in refr],
                      Create(ul1), run_time=0.6)
            vo.wait_until("the other water molecules")
            self.play(FadeIn(x2, scale=1.6), *[g.animate.set_color(ERR) for _, g in water],
                      Create(ul2), run_time=0.6)
            vo.wait_until("Both are wrong")
            self.play(FadeIn(reason, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("The voice changed completely")
            self.play(FadeIn(tick, scale=1.6), FadeIn(voice, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("the facts did not get better")
            self.play(Indicate(x1, color=ERR, scale_factor=1.3), Indicate(x2, color=ERR, scale_factor=1.3),
                      run_time=0.8)

        # ========================================================== 3. habits; the numbers
        lr = lref("7–8")
        chip_b = chip("Qwen3-0.6B · as downloaded", FROZEN, size=22)
        chip_f = chip("Qwen3-0.6B · fine-tuned", OWN, size=22)
        ad_small = adapter_glyph(0.34)
        top_row = VGroup(chip_b, VGroup(chip_f, ad_small).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.8)
        place(top_row, cx=0, top=2.95)
        apart(top_row, lr, 0.05)

        bub_fr = RoundedRectangle(width=4.6, height=1.7, corner_radius=0.25, stroke_color=S.GREY,
                                  stroke_width=3).set_fill(S.GREY, 0.08)
        tail = Polygon([-1.5, -0.85, 0], [-1.05, -0.85, 0], [-1.75, -1.35, 0], stroke_color=S.GREY,
                       stroke_width=3).set_fill(S.BG, 1)
        bub_t = label("Sure, here's…", 26, INK)
        place(bub_t, left=bub_fr.get_left()[0] + 0.4, top=bub_fr.get_top()[1] - 0.3)
        bars = VGroup(*[RoundedRectangle(width=w, height=0.13, corner_radius=0.06, stroke_width=0)
                        .set_fill(S.GREY, 0.55) for w in (3.6, 2.6)]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        place(bars, left=bub_t.get_left()[0], top=bub_t.get_bottom()[1] - 0.3)
        bubble = VGroup(bub_fr, tail, bub_t, bars)
        bubble.move_to([0, 0.2, 0])
        bub_cap = note("a habit a chat model learned")
        place(bub_cap, cx=0, top=bubble.get_bottom()[1] - 0.25)
        apart(top_row, bubble, 0.2)

        # the one row: slab | strip  label | time chip | file chip
        sf = snowflake(0.26)
        slab_t = label("596 M weights · frozen", 24, INK)
        slab_in = VGroup(sf, slab_t).arrange(RIGHT, buff=0.25)
        slab = Rectangle(width=slab_in.width + 0.5, height=1.9, stroke_color=FROZEN,
                         stroke_width=3).set_fill(FROZEN, 0.22)
        slab_in.move_to(slab)
        strip = Rectangle(width=0.035, height=1.9, stroke_width=0).set_fill(ADAPTER, 1)
        strip.next_to(slab, RIGHT, buff=0.1)
        strip_t = label("≈ 1.15 M new · trained", 22, OWN)
        strip_t.next_to(strip, RIGHT, buff=0.2)
        t_chip = chip("3 min 36 s · A100", MODEL, size=22)
        f_gl = file_glyph(0.42, ADAPTER)
        f_t = label("≈ 4.6 MB", 22, INK)
        f_chip = VGroup(f_gl, f_t).arrange(RIGHT, buff=0.15)
        numrow = VGroup(VGroup(slab, sf, slab_t), strip, strip_t, t_chip, f_chip)
        t_chip.next_to(strip_t, RIGHT, buff=0.35)
        f_chip.next_to(t_chip, RIGHT, buff=0.35)
        place(numrow, cx=0, cy=0.0)
        f_src = chip("QLoRA notebook · 6.1", S.GREY, size=PT)
        place(f_src, top=f_chip.get_bottom()[1] - 0.35)
        f_src.set_x(min(f_chip.get_center()[0], SAFE - 0.05 - f_src.width / 2))
        inside_frame(top_row, bubble, bub_cap, numrow, f_src, lr)

        with self.voiceover(SAY[3]) as vo:
            self.play(*self.outs(qcard, x1, x2, ul1, ul2, tick, voice, reason, rec, src), run_time=0.6)
            self.play(FadeOut(card_b.rows), FadeOut(card_f.rows), run_time=0.4)
            self.play(ReplacementTransform(card_b.frame, chip_b.box), ReplacementTransform(card_b.title, chip_b.text),
                      ReplacementTransform(card_f.frame, chip_f.box), ReplacementTransform(card_f.title, chip_f.text),
                      ReplacementTransform(ad, ad_small), run_time=0.9)
            vo.wait_until("the lecture shows one")
            self.play(FadeIn(lr), FadeIn(bubble, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(bub_cap, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("sure, here's")
            self.play(bub_t.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(bub_t, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("This one kept")
            self.play(FadeOut(bubble), FadeOut(bub_cap), run_time=0.5)
            self.play(FadeIn(slab), Create(sf), Write(slab_t), run_time=0.8)
            vo.wait_until("and trained")
            self.play(FadeIn(strip, shift=LEFT * 0.1), FadeIn(strip_t, shift=LEFT * 0.1), run_time=0.6)
            self.play(Indicate(strip, color=ADAPTER, scale_factor=1.15), run_time=0.6)
            vo.wait_until("It took about")
            self.play(FadeIn(t_chip, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("fits in a file")
            self.play(FadeIn(f_chip, shift=LEFT * 0.1), FadeIn(f_src, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 4. two tracks
        q2 = label(QUESTION2, 30, TURN)
        q2.move_to([0, 0.2, 0])
        q2_top = q2.copy().move_to([0, 2.95, 0])
        colA_h = label("Track A · the README", 24, INK)
        colB_h = label("Track B · the course Colab", 24, INK)
        chain = track_chain()
        labsA = bullet_rows([("Gemini writes a persona dataset", MODEL), ("Google tunes Gemini", CLOUD),
                             ("you get an endpoint", CLOUD)])
        gpu = gpu_box()
        labsB = bullet_rows([("you fine-tune an open model with QLoRA", ADAPTER),
                             ("you keep the weights", ADAPTER)])
        colA = VGroup(colA_h, chain, labsA).arrange(DOWN, buff=0.55)
        colB = VGroup(colB_h, gpu, labsB).arrange(DOWN, buff=0.55)
        labsA.align_to(chain, LEFT)
        colA_h.set_x(chain.get_center()[0])
        place(colA, left=-SAFE + 0.15, top=1.7)
        place(colB, right=SAFE - 0.1, top=1.7)
        sep_x = (colA.get_right()[0] + colB.get_left()[0]) / 2
        assert colB.get_left()[0] - colA.get_right()[0] >= 0.9, (colA.get_right(), colB.get_left())
        sep = Line([sep_x, 1.9, 0], [sep_x, -2.9, 0], color=S.GREY_DARK, stroke_width=2)
        inside_frame(colA, colB, q2_top)
        apart(colA, colB, 0.2)
        apart(q2_top, VGroup(colA_h, colB_h), 0.1)

        with self.voiceover(SAY[4]) as vo:
            self.play(*self.outs(top_row, numrow, f_src, lr), run_time=0.6)
            self.play(Write(q2), run_time=1.2)
            vo.wait_until("Two tracks answer that")
            self.play(q2.animate.move_to(q2_top), run_time=0.7)
            self.play(Create(sep), run_time=0.5)
            vo.wait_until("In track A")
            self.play(FadeIn(colA_h, shift=DOWN * 0.1),
                      LaggedStart(*[FadeIn(VGroup(m, n), scale=0.8) for m, n in zip(chain.glyphs, chain.names)],
                                  lag_ratio=0.3),
                      LaggedStart(*[Create(a) for a in chain[1]], lag_ratio=0.5), run_time=1.2)
            vo.wait_until("Gemini writes")
            self.play(FadeIn(labsA[0], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("Google tunes Gemini")
            self.play(FadeIn(labsA[1], shift=RIGHT * 0.1), run_time=0.5)
            self.play(FadeIn(labsA[2], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("In track B")
            self.play(FadeIn(colB_h, shift=DOWN * 0.1), FadeIn(gpu[:2], scale=0.9), run_time=0.7)
            self.play(FadeIn(gpu[2], scale=1.5), run_time=0.4)
            vo.wait_until("you fine-tune an open model")
            self.play(FadeIn(labsB[0], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("keep the weights")
            self.play(FadeIn(labsB[1], shift=RIGHT * 0.1), Indicate(gpu[2], color=ADAPTER, scale_factor=1.3),
                      run_time=0.7)
        mapg = VGroup(q2, sep, colA, colB)

        # ========================================================== 5. how to follow along
        tr = tracker("Prereq")
        halo = RoundedRectangle(width=tr.width + 0.2, height=tr.height + 0.16, corner_radius=0.1,
                                stroke_color=TURN, stroke_width=4).set_fill(opacity=0)
        halo.move_to(tr)
        place(halo, left=max(halo.get_left()[0], -SAFE + 0.01))
        tr_cap = note("the README step").next_to(halo, DOWN, buff=0.12).align_to(tr, LEFT)
        spec = tag("Lecture 8 · slides N", S.GREY)
        ref = lref("7–8")
        spec.move_to(ref)
        place(spec, right=ref.get_right()[0])
        lr_cap = note("the lecture slides")
        place(lr_cap, right=spec.get_right()[0], top=spec.get_bottom()[1] - 0.12)
        t = term(P_WS, rows=2, top=0.2)
        prev = frame_tags(t, your_turn(), grey_tag("preview"))
        turn_tag, prev_tag = prev[0], prev[1]
        turn_tag.box.set_stroke(opacity=0.4)
        turn_tag.text.set_opacity(0.4)
        tagrow = VGroup(grey_tag("expected"), grey_tag("recorded"), grey_tag("scripted"),
                        grey_tag("illustration")).arrange(RIGHT, buff=0.35)
        tag_hd = note("tags on what you see:")
        tagline = VGroup(tag_hd, tagrow).arrange(RIGHT, buff=0.35)
        place(tagline, cx=0, top=t.box.get_bottom()[1] - 0.45)
        inside_frame(halo, spec, lr_cap, t.box, prev, tagline, tr_cap)
        apart(halo, t.box, 0.2)

        with self.voiceover(SAY[5]) as vo:
            self.play(*self.outs(mapg), run_time=0.6)
            self.play(FadeIn(tr, shift=DOWN * 0.15), Create(halo), FadeIn(tr_cap, shift=UP * 0.1), run_time=0.7)
            self.play(pulse(halo, TURN, 1.04, run_time=0.6, width=6))
            self.play(pulse(halo, TURN, 1.04, run_time=0.6, width=6))
            vo.wait_until("the gray tag, top right")
            self.play(FadeOut(halo), FadeIn(spec), FadeIn(lr_cap, shift=UP * 0.1), run_time=0.5)
            self.play(spec.box.animate(rate_func=there_and_back).set_stroke(TURN, 5), run_time=0.8)
            vo.wait_until("When a tag says your turn")
            self.play(FadeIn(t), FadeIn(prev_tag), run_time=0.5)
            bare_prompt(self, t)
            self.play(FadeIn(turn_tag, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("pause and run")
            self.play(turn_tag.box.animate(rate_func=there_and_back).set_stroke(TURN, 5, opacity=0.8),
                      run_time=0.6)
            self.play(FadeIn(tag_hd), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in tagrow], lag_ratio=0.4),
                      run_time=1.4)
        self.wait(2)

        # ========================================================== 6. one honest limit
        title = label("One honest limit", 28, INK)
        date = chip("recorded October 31, 2026", S.GREY, size=22)
        nokey = chip("no key", S.GREY, size=22)
        nogpu = chip("no GPU", S.GREY, size=22)
        head = VGroup(title, date, nokey, nogpu).arrange(RIGHT, buff=0.3)
        row_specs = [
            ("tick", "ran for real:", "every README command, exactly as written", OWN),
            ("cross", "commands that talk to Google:", "up to the missing key (kept, they are instructive)", ERR),
            ("solid", "working outputs:", "`expected` = the README ·", CLOUD),
            ("dashed", "`scripted`", "= a small hand-written dataset", CLOUD),
        ]
        rows7 = VGroup()
        for kind, lead, rest, col in row_specs:
            txt = rich(f"{lead} {rest}", 22, INK, lead=(len(lead.replace("`", "")), col))
            if kind == "tick":
                gl = tick_mark(0.28)
            elif kind == "cross":
                gl = x_mark(0.26)
            else:
                gl = box(0.34, 0.26, CLOUD, fill_opacity=0.15, radius=0.05, dashed=(kind == "dashed"))
            gl.move_to([0, 0, 0])
            txt.next_to(gl, RIGHT, buff=0.3)
            gl.set_y(txt.get_center()[1])
            rows7.add(VGroup(gl, txt))
        r3 = rows7[2][1]
        row3b = rich("`recorded` = the staff's saved Colab run", 22, INK)
        k3 = r3.plain.index("expected")
        row3b.next_to(r3, DOWN, buff=0.14)
        row3b.align_to(r3[k3], LEFT)
        rows7[2].add(row3b)
        rows7.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        pers = VGroup(persona_chip(size=22), label("the persona: the instructor's voice", 22, INK)).arrange(RIGHT,
                                                                                                         buff=0.3)
        body = VGroup(head, rows7, pers).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        card7 = box(body.width + 0.8, body.height + 0.7, S.GREY, fill_opacity=0.0, radius=0.14)
        body.move_to(card7)
        footer = VGroup(label("every command:", 22, S.GREY), mono(GUIDE, 22, INK)).arrange(RIGHT, buff=0.2)
        whole = VGroup(card7, body, footer)
        footer.next_to(card7, DOWN, buff=0.3)
        place(whole, cx=0, cy=0.0)
        inside_frame(card7, footer)
        assert card7.width <= 13.0, card7.width
        r1 = rows7[1][1]
        k = r1.plain.index("up to the missing key")
        ul_key = under(VGroup(*r1[k:k + len("up to the missing key")]), ERR, stroke=3, buff=0.06)

        with self.voiceover(SAY[6]) as vo:
            self.play(*self.outs(tr, tr_cap, spec, lr_cap, t, prev, tagline), run_time=0.6)
            self.play(FadeIn(title, shift=UP * 0.1), Create(card7), run_time=0.8)
            vo.wait_until("we recorded this on")
            self.play(FadeIn(date, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("with no service account key")
            self.play(FadeIn(nokey, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("and no GPU")
            self.play(FadeIn(nogpu, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("Every README command")
            self.play(FadeIn(rows7[0][0], scale=1.3), FadeIn(rows7[0][1], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("the ones that talk to Google")
            self.play(FadeIn(rows7[1][0], scale=1.3), FadeIn(rows7[1][1], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("stop at the missing key")
            self.play(Create(ul_key), run_time=0.5)
            vo.wait_until("Working outputs come from")
            self.play(FadeIn(rows7[2][0], scale=1.3), FadeIn(VGroup(*rows7[2][1:]), shift=RIGHT * 0.15), run_time=0.6)
            self.play(FadeIn(rows7[3][0], scale=1.3), FadeIn(rows7[3][1], shift=RIGHT * 0.15), run_time=0.6)
            self.play(FadeIn(pers, shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(footer, shift=UP * 0.1), run_time=0.5)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
