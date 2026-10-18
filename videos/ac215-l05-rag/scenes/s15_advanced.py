"""S15 · Beyond naïve RAG: what the lecture adds (concepts only: no commands, no tracker).
Lecture: B6–B10, B35–B65.

Beats (script.md "## S15", one voiceover block each):
0. LECTURE B6–B10. The GREY dashed tag `concept · not in the tutorial's code` sits top left for the
   whole scene. Our redrawing of B6: GREEN books → "Indexing" → a tall "Retrieval" box →
   "Augmentation & Generation" → a BLUE answer, a PINK "question" entering Retrieval low. A GREY
   dashed column "Pre-Retrieval" slides in over Indexing and the question, then "Post-Retrieval"
   between Retrieval and Augmentation. S14's PURPLE seismograph appears inside Pre-Retrieval and
   lights GREEN (frame + tick); GREEN caption "semantic chunking · the one lever this tutorial
   implements". "Here are three more": three dashed numbered slots 1 · 2 · 3 in Pre, Retrieval, Post.
1. LECTURE B36–B39. The map folds into a one-row strip at the top (Pre-Retrieval with the small GREEN
   seismograph, Retrieval, Post-Retrieval, Augmentation & Generation); the slots move under their
   columns (the dock). Pre-Retrieval lights YELLOW; a big GREY dashed panel "query rewriting".
   A long, cluttered PINK question card shrinks (a copy) into "Where do dolphins live?" + GREEN tick;
   a short vague card "asked of a company's annual report" balloons into a long rewrite whose
   invented parts turn RED, tag "invented".
2. LECTURE B42–B48. The rewriting picture shrinks into slot 1, which becomes the GREY dashed chip
   "query rewriting". Retrieval lights; panel "hybrid search". Column headers "keyword / BM25"
   (GREY) and "vectors / cosine" (PINK) write in as named, with a GREY card "rare words weigh most:
   only 3 char-split chunks contain Tolminc" (recorded-embeddings/08 line 15). The PINK question
   "Chester went to the bank of the river in the morning" (tag `lecture example`), three GREEN
   paragraph cards (riverbank, early · bank, borrow money · swim, riverbank), then the two rank
   columns fill: keyword 2, 1, 3 and vectors 1, 3, 2.
3. The formula `w / (k + rank)` heads a third column, GREY note "k: a constant, here 0 · not top-K ·
   w = 0.5". Each rank cell sends 0.5 / rank to its paragraph's fused bar (GREY keyword blocks,
   PINK vector blocks): 0.75, 0.67, 0.42. The near paraphrase (paragraph 1) lights YELLOW with its
   bar, "1st"; the Tolminc card becomes the GREY chip "tutorial: $contains only filters".
4. LECTURE B51–B65. The hybrid picture shrinks into slot 2 (chips "hybrid search", "rank fusion").
   Post-Retrieval lights; panel "re-ranking". PINK "What is cheese?" (lecture example) → GREY dashed
   "fast retriever" with the card "bi-encoder: vectors made before the question · like our 8,248";
   arrow "top K = 25" → a column of 25 GREEN rows; five turn YELLOW (rows 1, 2, 11, 17, 22, as on
   B53) "truly relevant". A GREY dashed diamond "cross-encoder" gets the question; a PINK pointer
   reads the rows one pair at a time ("slower: one model run per pair"); the column reorders and
   the YELLOW rows rise to the top. Caption "fast + accurate: strong together".
5. The re-ranking picture shrinks into slot 3 ("re-ranking"); the lecture tag leaves. The four
   GREY dashed chips gather into a row with a `cli.py` file glyph and a GREY "not here". The strip's
   Retrieval box flashes RED ("the wrong chunks"); S12's PINK-edged "metadata filter" box returns
   with the GREY note "our query: remove the filter" and fades to a dashed ghost. Fade out.
"""

from types import SimpleNamespace

import numpy as np
from common import (
    CLOUD,
    COUNTS,
    DATA,
    ERR,
    INK,
    LOOKUP,
    NARRATION,
    TURN,
    capture,
    concept_tag,
    example_tag,
    lref,
    note,
    page_stack,
    sans,
    seismo_glyph,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
    linear,
    smooth,
)

from explainer import style as S
from explainer.devops import TAG, box, check_mark, chip, file_glyph, label, mono, step_badge, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S15"]
GREY = S.GREY

# ------------------------------------------------------------------ the one real number
CNT = capture("08", "recorded-embeddings")          # S12's extra check: counts with $contains
TOLMINC_LINE = CNT.line(15)                         # "any book, $contains 'Tolminc':    3"
assert "$contains 'Tolminc'" in TOLMINC_LINE and TOLMINC_LINE.split()[-1] == "3", TOLMINC_LINE
assert COUNTS["tolminc_word"] == 3 and COUNTS["char-split"] == 8248
N_CHAR = f"{COUNTS['char-split']:,}"                # 8,248 stored char-split vectors

# ------------------------------------------------------------------ the lecture examples (B44–B48, B53)
PARAS = ["Chester … riverbank, early", "Chester … bank, borrow money", "Chester … swim … riverbank"]
BM25_RANK = (2, 1, 3)                               # B45, per paragraph
VEC_RANK = (1, 3, 2)
W, K_RRF = 0.5, 0                                   # B47: k = 0, w_j = 0.5
FUSED = [W / (K_RRF + a) + W / (K_RRF + b) for a, b in zip(BM25_RANK, VEC_RANK)]
assert [round(f, 2) for f in FUSED] == [0.75, 0.67, 0.42]
TOP_K = 25
RELEVANT = (0, 1, 10, 16, 21)                       # B53: rows 1, 2, 11, 17, 22

# ------------------------------------------------------------------ layout
STRIP_Y, DOCK_Y = 2.6, 1.92
DOCK_X = (-4.9, -1.3, 2.3)                          # under Pre, Retrieval, Post of the strip
PANEL_TOP, PANEL_BOT = 1.4, -3.5
LEFT_X = -6.2                                        # left edge of panel content


def arrow(a, b, color=GREY, stroke=3, tip=0.15):
    return Arrow(np.array([*a, 0.0]), np.array([*b, 0.0]), buff=0, color=color, stroke_width=stroke,
                 tip_length=tip, max_tip_length_to_length_ratio=0.5)


def dbox(w, h, color=GREY, fill_op=0.06, radius=0.14, stroke=2.5, bg=None):
    """A GREY dashed box (a lecture concept with no code here) over a faint fill. .bg .dash"""
    r = min(radius, h / 2, w / 2)
    back = RoundedRectangle(width=w, height=h, corner_radius=r, stroke_width=0)
    back.set_fill(bg or color, fill_op)
    dash = box(w, h, color, stroke=stroke, radius=radius, dashed=True)
    g = VGroup(back, dash)
    g.bg, g.dash = back, dash
    return g


def left_at(m, x, y):
    """Put m's left edge at x and its centre at height y."""
    return m.move_to(np.array([x + m.width / 2, y, 0]))


def slot(n):
    """A dashed numbered placeholder for one of the three ideas."""
    c = Circle(radius=0.22, stroke_width=0).set_fill(S.BG, 0.9)
    d = DashedVMobject(Circle(radius=0.22), num_dashes=12, dashed_ratio=0.55).set_stroke(GREY, 2.5)
    t = sans(str(n), 20, GREY).move_to(c)
    return VGroup(c, d, t)


def qcard(lines, size=20, color=LOOKUP):
    """A PINK question card of serif rows (a lecture example, our words). .frame .lines"""
    rows = VGroup(*[label(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = box(rows.width + 0.44, rows.height + 0.34, color, fill_opacity=0.1, radius=0.12)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.lines = fr, rows
    return g


def glyphs(text_mob, s, sub):
    """The glyphs of substring `sub` in a one-line Text built from `s` (spaces have no glyphs)."""
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*text_mob.submobjects[a:a + n])


def level_boxes(chips, y):
    """Put every chip's box centre at height y (a tag centres its text, so boxes of text without
    descenders sit lower after arrange())."""
    for ch in chips:
        ch.shift(UP * (y - ch.box.get_center()[1]))
    return chips


def seat_text(ch, s, size=TAG):
    """Put a tag's text on the baseline every tag shares: centre it in its box as if it had the
    tallest ascender and the deepest descender, so "rank fusion" (no descender) sits level with
    "hybrid search" in the row of chips."""
    ref = label(s + " Hgkdlfjy", size).move_to(ch.box)
    n = len("".join(s.split()))
    ch.text.shift(UP * (VGroup(*ref.submobjects[:n]).get_center()[1] - ch.text.get_center()[1]))
    return ch


def panel_title(s):
    t = label(s, 22, GREY)
    bg = Rectangle(width=t.width + 0.3, height=0.38, stroke_width=0).set_fill(S.BG, 1)
    g = VGroup(bg, t.move_to(bg))
    return g.move_to(np.array([-6.05 + g.width / 2, PANEL_TOP, 0]))


def light(m, on=True):
    """Light a strip column YELLOW (or back to GREY): dashed columns light their dashes."""
    target = m.dash if hasattr(m, "dash") else m
    return target.animate.set_stroke(TURN if on else GREY, 4 if on else 2.5)


# ------------------------------------------------------------------ V: the lecture's frame (B6–B10)
def big_map():
    m = SimpleNamespace()
    m.ret = box(1.8, 3.4, GREY, fill_opacity=0.08).move_to([-1.45, 0.15, 0])
    m.ret_lab = sans("Retrieval", 24).move_to([-1.45, 0.45, 0])
    m.pre = dbox(2.4, 3.4).move_to([-3.95, 0.15, 0]).set_z_index(-1)
    m.pre_lab = sans("Pre-Retrieval", 22).move_to([-3.95, 2.1, 0])
    m.post = dbox(2.4, 3.4).move_to([1.05, 0.15, 0]).set_z_index(-1)
    m.post_lab = sans("Post-Retrieval", 22).move_to([1.05, 2.1, 0])
    m.idx = VGroup(box(1.9, 0.55, GREY, fill_opacity=0.1), sans("Indexing", 22)).move_to([-3.95, 1.35, 0])
    m.idx[1].move_to(m.idx[0])
    m.books = page_stack(0.5, 0.62).move_to([-6.0, 1.35, 0])
    m.a_books = arrow((-5.58, 1.35), (-4.92, 1.35))
    m.a_idx = arrow((-2.98, 1.35), (-2.37, 1.35))
    m.ag = box(2.5, 1.0, GREY, fill_opacity=0.08).move_to([3.8, 0.15, 0])
    m.ag_lab = VGroup(sans("Augmentation &", 22), sans("Generation", 22)).arrange(DOWN, buff=0.08).move_to(m.ag)
    m.a_ret = arrow((-0.53, 0.15), (2.53, 0.15))
    m.a_ag = arrow((5.07, 0.15), (5.5, 0.15))
    m.answer = VGroup(*[RoundedRectangle(width=0.75 * f, height=0.11, corner_radius=0.05, stroke_width=0)
                        .set_fill(CLOUD, 0.85) for f in (1.0, 0.9, 0.55)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    left_at(m.answer, 5.6, 0.15)
    m.q_lab = sans("question", 22, LOOKUP)
    left_at(m.q_lab, -6.45, -1.25)
    m.a_q = arrow((-5.35, -1.25), (-2.37, -1.25), color=LOOKUP)
    glyph = seismo_glyph(0.75).move_to([-4.1, 0.45, 0])
    frame = RoundedRectangle(width=glyph.width + 0.24, height=glyph.height + 0.2, corner_radius=0.08,
                             stroke_color=DATA, stroke_width=3).move_to(glyph)
    tick = check_mark(0.26, DATA).next_to(frame, RIGHT, buff=0.14)
    m.seis, m.seis_frame, m.tick = glyph, frame, tick
    m.caption = label("semantic chunking · the one lever this tutorial implements", 22, DATA)
    left_at(m.caption, -6.3, -2.3)
    m.slots = [slot(1).move_to([-3.95, -0.5, 0]), slot(2).move_to([-1.45, -0.5, 0]),
               slot(3).move_to([1.05, -0.5, 0])]
    for v in vars(m).values():                      # centre the picture in the frame
        for mob in (v if isinstance(v, list) else [v]):
            mob.shift(DOWN * 0.3)
    return m


def compact_strip():
    """The same frame as a one-row strip along the top (text 20–22 pt)."""
    c = SimpleNamespace()
    c.pre = dbox(2.6, 0.56).move_to([-4.9, STRIP_Y, 0])
    c.ret = box(3.9, 0.68, GREY, fill_opacity=0.08).move_to([-1.3, STRIP_Y, 0])
    c.post = dbox(2.6, 0.56).move_to([2.3, STRIP_Y, 0])
    c.ag = box(2.25, 0.68, GREY, fill_opacity=0.08).move_to([5.075, STRIP_Y, 0])
    glyph = seismo_glyph(0.42)
    frame = RoundedRectangle(width=glyph.width + 0.14, height=glyph.height + 0.12, corner_radius=0.05,
                             stroke_color=DATA, stroke_width=2.5).move_to(glyph)
    c.seis = VGroup(glyph, frame)
    c.pre_lab = sans("Pre-Retrieval", 22)
    VGroup(c.seis, c.pre_lab).arrange(RIGHT, buff=0.14).move_to(c.pre)
    c.ret_lab = sans("Retrieval", 22).move_to(c.ret)
    c.post_lab = sans("Post-Retrieval", 22).move_to(c.post)
    c.ag_lab = VGroup(sans("Augmentation &", 20), sans("Generation", 20)).arrange(DOWN, buff=0.05).move_to(c.ag)
    c.a1 = arrow((-3.6, STRIP_Y), (-3.25, STRIP_Y), tip=0.13)
    c.a2 = arrow((0.65, STRIP_Y), (1.0, STRIP_Y), tip=0.13)
    c.a3 = arrow((3.6, STRIP_Y), (3.95, STRIP_Y), tip=0.13)
    c.slots = [slot(i + 1).move_to([x, DOCK_Y, 0]) for i, x in enumerate(DOCK_X)]
    c.all = VGroup(c.pre, c.ret, c.post, c.ag, c.seis, c.pre_lab, c.ret_lab, c.post_lab, c.ag_lab,
                   c.a1, c.a2, c.a3)
    return c


# ------------------------------------------------------------------ beat 1 · query rewriting (B36–B39)
CLUTTERED = ["Writing an essay, began with penguins,", "drifted to other sea animals, and now",
             "I'm stuck on dolphins: their homes?"]
CLEAN = "Where do dolphins live?"
VAGUE = "Was there big turnover at the top?"
REWRITE = ["Which CEOs and CFOs left the company", "in the past year, and what were the",
           "reasons behind each departure?"]
INVENTED = [(0, "CEOs and CFOs"), (1, "in the past year"), (2, "reasons behind each departure")]


def rewriting_picture():
    p = SimpleNamespace()
    p.h1 = note("original question")
    left_at(p.h1, LEFT_X, 0.98)
    p.h2 = note("rewritten by a model")
    left_at(p.h2, 0.75, 0.98)
    p.clutter = qcard(CLUTTERED)
    left_at(p.clutter, LEFT_X, 0.1)
    p.clean = chip(CLEAN, LOOKUP, size=22, fill_opacity=0.12)
    left_at(p.clean, 0.75, 0.1)
    p.tick = check_mark(0.3, DATA).next_to(p.clean, RIGHT, buff=0.22)
    p.a1 = arrow((-0.9, 0.1), (0.55, 0.1))
    p.vague = chip(VAGUE, LOOKUP, size=20, fill_opacity=0.12)
    left_at(p.vague, LEFT_X, -1.6)
    p.vnote = note("asked of a company's annual report").next_to(p.vague, DOWN, buff=0.14)
    p.vnote.align_to(p.vague, LEFT).shift(RIGHT * 0.1)
    p.rewrite = qcard(REWRITE)
    left_at(p.rewrite, 0.75, -1.75)
    p.a2 = arrow((-0.9, -1.6), (0.55, -1.6))
    p.marks, p.unders = VGroup(), VGroup()
    for row, sub in INVENTED:
        g = glyphs(p.rewrite.lines[row], REWRITE[row], sub)
        p.marks.add(g)
        p.unders.add(Line(g.get_corner(DOWN + LEFT) + DOWN * 0.06, g.get_corner(DOWN + RIGHT) + DOWN * 0.06,
                          color=ERR, stroke_width=3))
    p.invented = tag("invented", ERR).next_to(p.rewrite, DOWN, buff=0.14).align_to(p.rewrite, RIGHT)
    p.all = VGroup(p.h1, p.h2, p.clutter, p.clean, p.tick, p.a1, p.vague, p.vnote, p.rewrite, p.a2,
                   p.unders, p.invented)
    return p


# ------------------------------------------------------------------ beats 2–3 · hybrid search + RRF (B42–B48)
ROW_Y = (-0.5, -1.25, -2.0)
KW_X, VEC_X = -0.85, 0.25
BAR_X0, BAR_SCALE, BAR_H = 1.0, 4.4, 0.44


def fmt(v):
    return f"{v:.2f}".rstrip("0")


def hybrid_picture():
    h = SimpleNamespace()
    h.q = chip("Chester went to the bank of the river in the morning", LOOKUP, size=20, fill_opacity=0.12)
    left_at(h.q, LEFT_X, 0.95)
    h.ex = example_tag().next_to(h.q, RIGHT, buff=0.25)
    h.kw = VGroup(sans("keyword", 20, GREY), sans("BM25", 20, GREY)).arrange(DOWN, buff=0.06).move_to([KW_X, 0.3, 0])
    h.vec = VGroup(sans("vectors", 20, LOOKUP), sans("cosine", 20, LOOKUP)).arrange(DOWN, buff=0.06).move_to([VEC_X, 0.3, 0])
    h.tol = VGroup(label("rare words weigh most:", 20, INK),
                   label(f"only {TOLMINC_LINE.split()[-1]} char-split chunks contain Tolminc", 20, INK))
    h.tol.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = box(h.tol.width + 0.44, h.tol.height + 0.32, GREY, fill=S.BG, fill_opacity=0.95, radius=0.12)
    h.tol.move_to(fr)
    h.tol = VGroup(fr, h.tol)
    left_at(h.tol, LEFT_X, -2.88)
    h.cards, h.kw_cells, h.vec_cells = VGroup(), VGroup(), VGroup()
    for i, (txt, y) in enumerate(zip(PARAS, ROW_Y)):
        b = step_badge(i + 1, DATA, size=20, radius=0.16)
        t = label(txt, 20, INK)
        inner = VGroup(b, t).arrange(RIGHT, buff=0.16)
        fr = box(4.7, 0.56, DATA, fill_opacity=0.1, radius=0.1)
        left_at(fr, LEFT_X, y)
        left_at(inner, LEFT_X + 0.14, y)
        card = VGroup(fr, inner)
        card.frame, card.badge = fr, b
        h.cards.add(card)
        for cells, x, rank, col in ((h.kw_cells, KW_X, BM25_RANK[i], GREY), (h.vec_cells, VEC_X, VEC_RANK[i], LOOKUP)):
            sq = RoundedRectangle(width=0.46, height=0.46, corner_radius=0.08, stroke_color=col,
                                  stroke_width=2.5).set_fill(col, 0.12)
            cells.add(VGroup(sq, mono(str(rank), 22, INK)).move_to([x, y, 0]))
    # beat 3: the formula, its note, the fused bars
    h.formula = mono("w / (k + rank)", 24, INK).move_to([2.65, 0.44, 0])
    h.knote = note("k: a constant, here 0 · not top-K · w = 0.5")
    h.knote.move_to([6.3 - h.knote.width / 2, 0.05, 0])
    h.blocks, h.totals = [], VGroup()
    for i, y in enumerate(ROW_Y):
        x = BAR_X0
        row = []
        for rank, col in ((BM25_RANK[i], GREY), (VEC_RANK[i], LOOKUP)):
            v = W / (K_RRF + rank)
            r = Rectangle(width=v * BAR_SCALE, height=BAR_H, stroke_color=col, stroke_width=1.5).set_fill(col, 0.42)
            left_at(r, x, y)
            row.append(VGroup(r, label(fmt(v), 20, INK).move_to(r)))
            x += v * BAR_SCALE
        h.blocks.append(row)
        h.totals.add(label(f"{FUSED[i]:.2f}", 22, INK).move_to([x + 0.42, y, 0]))
    h.first = label("1st", 22, TURN).next_to(h.totals[0], RIGHT, buff=0.22)
    h.contains = chip("tutorial: $contains only filters", GREY, size=20)
    left_at(h.contains, LEFT_X, -2.88)
    return h


# ------------------------------------------------------------------ beat 4 · re-ranking (B51–B65)
COL_X, COL_W, ROW_TOP, ROW_PITCH = 0.2, 1.6, 1.0, 0.17
DIA = np.array([3.9, -1.15, 0])


def row_y(k):
    return ROW_TOP - k * ROW_PITCH


def rerank_picture():
    r = SimpleNamespace()
    r.q = chip("What is cheese?", LOOKUP, size=22, fill_opacity=0.12)
    left_at(r.q, LEFT_X, 0.95)
    r.ex = example_tag().next_to(r.q, RIGHT, buff=0.25)
    r.ret = dbox(2.6, 0.7, bg=GREY)
    r.ret = VGroup(r.ret, sans("fast retriever", 22)).move_to([-4.9, -0.25, 0])
    r.ret[1].move_to(r.ret[0])
    r.a_q = arrow((r.q.get_center()[0], 0.7), (r.q.get_center()[0], 0.12), color=LOOKUP)
    rows = VGroup(*[label(s, 20, INK) for s in ("bi-encoder:", "vectors made before the question",
                                                 f"like our {N_CHAR}")]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = box(rows.width + 0.5, rows.height + 0.36, GREY, fill=S.BG, fill_opacity=0.95, radius=0.12)
    rows.move_to(fr)
    r.bi = VGroup(fr, rows)
    left_at(r.bi, LEFT_X, -1.75)
    r.a_k = arrow((-3.55, -0.25), (COL_X - COL_W / 2 - 0.15, -0.25))
    r.k_lab = sans(f"top K = {TOP_K}", 22).next_to(r.a_k, UP, buff=0.1)
    r.rows = VGroup()
    for k in range(TOP_K):
        rr = RoundedRectangle(width=COL_W, height=0.12, corner_radius=0.04, stroke_width=0)
        r.rows.add(rr.set_fill(DATA, 0.55).move_to([COL_X, row_y(k), 0]))
    sw = RoundedRectangle(width=0.4, height=0.12, corner_radius=0.04, stroke_width=0).set_fill(TURN, 0.95)
    r.legend = VGroup(sw, label("truly relevant", 20, TURN)).arrange(RIGHT, buff=0.15)
    left_at(r.legend, 1.6, row_y(0))                 # level with the top row, clear of the question
    d = Polygon(DIA + UP * 0.85, DIA + RIGHT * 1.5, DIA + DOWN * 0.85, DIA + LEFT * 1.5)
    r.dia_bg = d.copy().set_stroke(width=0).set_fill(GREY, 0.08)
    r.dia = VGroup(r.dia_bg, DashedVMobject(d, num_dashes=28, dashed_ratio=0.55).set_stroke(GREY, 2.5),
                   sans("cross-encoder", 22).move_to(DIA))
    r.q2 = chip("What is cheese?", LOOKUP, size=22, fill_opacity=0.12).move_to([DIA[0], 0.38, 0])
    r.a_q2 = arrow((DIA[0], 0.14), (DIA[0], DIA[1] + 0.87), color=LOOKUP)
    r.slow = note("slower: one model run per pair").move_to([DIA[0], -2.3, 0])
    r.together = label("fast + accurate: strong together", 22, INK).move_to([DIA[0], -2.95, 0])
    return r


# ------------------------------------------------------------------ beat 5
def filter_box():
    """S12's PINK-edged "metadata filter" box (StageStrip's filter part, redrawn small)."""
    t = sans("metadata filter", 22, INK)
    b = box(t.width + 0.44, 0.62, LOOKUP, fill=S.BG, fill_opacity=0.95, radius=0.1, stroke=3)
    return VGroup(b, t.move_to(b))


class BeyondNaive(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)
        concept = concept_tag()
        concept.move_to([-6.6 + concept.width / 2, 3.6 - concept.height / 2, 0])
        m = big_map()

        # ========================================================== 0 · the lecture's frame (B6–B10)
        with self.voiceover(SAY[0]) as vo:
            ref = lref("B6–B10")
            self.play(FadeIn(concept), FadeIn(ref), run_time=0.5)
            self.play(LaggedStart(FadeIn(m.books), Create(m.a_books), FadeIn(m.idx), Create(m.a_idx),
                                  FadeIn(m.ret), FadeIn(m.ret_lab), Create(m.a_ret), FadeIn(m.ag),
                                  FadeIn(m.ag_lab), Create(m.a_ag), FadeIn(m.answer),
                                  lag_ratio=0.12), run_time=1.6)
            self.play(FadeIn(m.q_lab), Create(m.a_q), run_time=0.5)
            vo.wait_until("a pre-retrieval stage")
            self.play(FadeIn(m.pre, shift=DOWN * 0.5), FadeIn(m.pre_lab, shift=DOWN * 0.5), run_time=0.9)
            vo.wait_until("and a post-retrieval stage")
            self.play(FadeIn(m.post, shift=DOWN * 0.5), FadeIn(m.post_lab, shift=DOWN * 0.5), run_time=0.9)
            vo.wait_until("Semantic chunking")
            self.play(FadeIn(m.seis, scale=0.7), run_time=0.6)
            vo.wait_until("the one advanced lever")
            self.play(Create(m.seis_frame), Create(m.tick), run_time=0.6)
            self.play(Write(m.caption), run_time=1.0)
            vo.wait_until("Here are three more")
            self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in m.slots], lag_ratio=0.3), run_time=1.0)

        # ========================================================== 1 · query rewriting (B36–B39)
        c = compact_strip()
        p = rewriting_picture()
        panel = dbox(13.0, PANEL_TOP - PANEL_BOT, fill_op=0.0).move_to([0, (PANEL_TOP + PANEL_BOT) / 2, 0])
        title = panel_title("query rewriting")
        with self.voiceover(SAY[1]) as vo:
            ref2 = lref("B36–B39")
            self.play(
                ReplacementTransform(m.pre, c.pre), ReplacementTransform(m.pre_lab, c.pre_lab),
                ReplacementTransform(m.ret, c.ret), ReplacementTransform(m.ret_lab, c.ret_lab),
                ReplacementTransform(m.post, c.post), ReplacementTransform(m.post_lab, c.post_lab),
                ReplacementTransform(m.ag, c.ag), ReplacementTransform(m.ag_lab, c.ag_lab),
                ReplacementTransform(m.a_idx, c.a1), ReplacementTransform(m.a_ret, c.a2),
                ReplacementTransform(m.seis, c.seis[0]), ReplacementTransform(m.seis_frame, c.seis[1]),
                *[ReplacementTransform(a, b) for a, b in zip(m.slots, c.slots)],
                FadeOut(VGroup(m.books, m.a_books, m.idx, m.a_ag, m.answer, m.q_lab, m.a_q, m.tick, m.caption)),
                FadeOut(ref), FadeIn(ref2),
                run_time=1.3)
            self.play(FadeIn(c.a3), light(c.pre), Create(panel.dash), FadeIn(title), run_time=0.8)
            # light the slot's dashes and number only: Indicate recolours fills too, and the slot's
            # dark disc would turn into a solid YELLOW dot that hides its number
            self.play(FadeIn(p.h1), FadeIn(p.h2), Indicate(VGroup(*c.slots[0][1:]), color=TURN, scale_factor=1.25),
                      run_time=0.7)
            vo.wait_until("A model turns")
            self.play(FadeIn(p.clutter, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("into a clean one")
            self.play(GrowFromEdge(p.a1, LEFT), FadeTransform(p.clutter.copy(), p.clean), run_time=1.0)
            vo.wait_until("like where do dolphins live")
            self.play(Create(p.tick), Indicate(p.clean, color=DATA, scale_factor=1.06), run_time=0.7)
            vo.wait_until("But hand it a vague question")
            self.play(FadeIn(p.vague, shift=RIGHT * 0.2), FadeIn(p.vnote), run_time=0.6)
            vo.wait_until("and the rewrite")
            self.play(GrowFromEdge(p.a2, LEFT), FadeTransform(p.vague.copy(), p.rewrite), run_time=1.0)
            vo.wait_until("can invent details")
            self.play(*[g.animate.set_color(ERR) for g in p.marks], Create(p.unders), FadeIn(p.invented),
                      run_time=0.7)

        # ========================================================== 2 · hybrid search (B42–B48)
        h = hybrid_picture()
        chip1 = concept_tag("query rewriting").move_to(c.slots[0])
        pair = VGroup(concept_tag("hybrid search"), concept_tag("rank fusion")).arrange(RIGHT, buff=0.15)
        pair.move_to([DOCK_X[1], DOCK_Y, 0])
        level_boxes([chip1, *pair], DOCK_Y)
        for ch, s in ((chip1, "query rewriting"), (pair[0], "hybrid search"), (pair[1], "rank fusion")):
            seat_text(ch, s)
        chip2, chip3 = pair[0], pair[1]
        title2 = panel_title("hybrid search")
        with self.voiceover(SAY[2]) as vo:
            ref3 = lref("B42–B48")
            self.play(FadeOut(p.all, scale=0.15, target_position=c.slots[0].get_center()),
                      ReplacementTransform(c.slots[0], chip1), light(c.pre, False), light(c.ret),
                      Transform(title, title2), FadeOut(ref2), FadeIn(ref3), run_time=1.2)
            self.play(Indicate(VGroup(*c.slots[1][1:]), color=TURN, scale_factor=1.25), run_time=0.6)
            vo.wait_until("Keywords pin down")
            self.play(FadeIn(h.kw, shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("names and rare words")
            self.play(FadeIn(h.tol, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("vectors catch meaning")
            self.play(FadeIn(h.vec, shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("Take the question")
            self.play(FadeIn(h.q, shift=RIGHT * 0.2), FadeIn(h.ex), run_time=0.7)
            vo.wait_until("in the morning")
            self.play(LaggedStart(*[FadeIn(cd, shift=RIGHT * 0.2) for cd in h.cards], lag_ratio=0.25),
                      run_time=0.9)
            vo.wait_until("The two rank")
            self.play(LaggedStart(*[FadeIn(x, scale=0.7) for x in h.kw_cells], lag_ratio=0.3), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(x, scale=0.7) for x in h.vec_cells], lag_ratio=0.3), run_time=0.9)

        # ========================================================== 3 · reciprocal rank fusion
        # pad: a breath after "0.42", so the closing chip "tutorial: $contains only filters" can be read
        # before the picture folds into its chips
        with self.voiceover(SAY[3], pad=1.0) as vo:
            self.play(Write(h.formula), run_time=0.9)
            vo.wait_until("gives each paragraph")
            self.play(FadeIn(h.knote, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("one half divided by its rank")
            self.play(LaggedStart(*[ReplacementTransform(h.kw_cells[i].copy(), h.blocks[i][0]) for i in range(3)],
                                  lag_ratio=0.3), run_time=1.3)
            vo.wait_until("in each list")
            self.play(LaggedStart(*[ReplacementTransform(h.vec_cells[i].copy(), h.blocks[i][1]) for i in range(3)],
                                  lag_ratio=0.3), run_time=1.2)
            vo.wait_until("and adds them up")
            self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.15) for t in h.totals], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("The near paraphrase")
            self.play(h.cards[0].frame.animate.set_stroke(TURN, 4),
                      *[b[0].animate.set_stroke(TURN, 3) for b in h.blocks[0]],
                      Indicate(h.cards[0][1][1], color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("wins with")
            self.play(FadeIn(h.first, shift=LEFT * 0.15), h.totals[0].animate.set_color(TURN), run_time=0.5)
            # each runner-up lights as it is said (the numbers are long to say: 0.42 comes ~1.6 s later)
            vo.wait_until("ahead of")
            self.play(Indicate(h.totals[1], color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("and 0.42")
            self.play(Indicate(h.totals[2], color=TURN, scale_factor=1.15), run_time=0.6)
            self.play(ReplacementTransform(h.tol, h.contains), run_time=0.7)

        # ========================================================== 4 · re-ranking (B51–B65)
        r = rerank_picture()
        chip4 = concept_tag("re-ranking").move_to(c.slots[2])
        level_boxes([chip4], DOCK_Y)
        seat_text(chip4, "re-ranking")
        title3 = panel_title("re-ranking")
        hybrid_all = VGroup(h.q, h.ex, h.kw, h.vec, h.cards, h.kw_cells, h.vec_cells, h.formula, h.knote,
                            *[b for row in h.blocks for b in row], h.totals, h.first, h.contains)
        # pad: a breath after "reorders them", so the caption "strong together" can be read before
        # the picture folds into its chip
        with self.voiceover(SAY[4], pad=1.3) as vo:
            ref4 = lref("B51–B65")
            self.play(FadeOut(hybrid_all, scale=0.15, target_position=c.slots[1].get_center()),
                      ReplacementTransform(c.slots[1], pair), light(c.ret, False), light(c.post),
                      Transform(title, title3), FadeOut(ref3), FadeIn(ref4), run_time=1.2)
            self.play(FadeIn(r.q, shift=RIGHT * 0.2), FadeIn(r.ex), run_time=0.6)
            vo.wait_until("A fast retriever")
            self.play(GrowFromEdge(r.a_q, UP), FadeIn(r.ret, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("whose vectors were made")
            self.play(FadeIn(r.bi, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("returns 25 candidates")
            self.play(GrowFromEdge(r.a_k, LEFT), FadeIn(r.k_lab), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in r.rows], lag_ratio=0.06), run_time=1.1)
            vo.wait_until("with the right ones scattered")
            self.play(*[r.rows[k].animate.set_fill(TURN, 0.95) for k in RELEVANT], FadeIn(r.legend), run_time=0.8)
            vo.wait_until("A slower model")
            self.play(FadeIn(r.dia, scale=0.85), TransformFromCopy(r.q, r.q2), run_time=0.7)
            self.play(GrowFromEdge(r.a_q2, UP), run_time=0.35)
            # the cross-encoder reads one (question, chunk) pair at a time
            vo.wait_until("reads each question")
            ptr = Polygon([0, 0, 0], [0.2, 0.11, 0], [0.2, -0.11, 0], stroke_width=0).set_fill(LOOKUP, 1)
            ptr.move_to([COL_X + COL_W / 2 + 0.16, row_y(0), 0])
            left_vertex = DIA + LEFT * 1.5
            link = Line(ptr.get_right(), left_vertex, color=LOOKUP, stroke_width=2.5)
            link.add_updater(lambda ln: ln.put_start_and_end_on(ptr.get_right(), left_vertex))
            self.play(FadeIn(ptr), FadeIn(link), FadeIn(r.slow), run_time=0.3)
            self.play(ptr.animate.move_to([ptr.get_center()[0], row_y(TOP_K - 1), 0]), run_time=1.5,
                      rate_func=linear)
            link.clear_updaters()
            self.play(FadeOut(ptr), FadeOut(link), run_time=0.2)
            vo.wait_until("and reorders them")
            order = list(RELEVANT) + [k for k in range(TOP_K) if k not in RELEVANT]
            self.play(*[r.rows[k].animate.move_to([COL_X, row_y(pos), 0]) for pos, k in enumerate(order)],
                      FadeIn(r.together, shift=UP * 0.15, rate_func=lambda t: smooth(min(1.0, t / 0.6))),
                      run_time=1.0)

        # ========================================================== 5 · none of this is in cli.py
        rerank_all = VGroup(r.q, r.ex, r.ret, r.a_q, r.bi, r.a_k, r.k_lab, r.rows, r.legend, r.dia, r.q2,
                            r.a_q2, r.slow, r.together)
        chips = VGroup(chip1, chip2, chip3, chip4)
        row = chips.copy().arrange(RIGHT, buff=0.25)
        cli = VGroup(file_glyph(0.55, GREY), mono("cli.py", 24, INK)).arrange(RIGHT, buff=0.15)
        not_here = note("not here", size=22)
        cli_g = VGroup(cli, not_here)
        not_here.next_to(cli, DOWN, buff=0.12)
        VGroup(row, cli_g).arrange(RIGHT, buff=0.55).move_to([0, 0.45, 0])
        level_boxes(row, row.get_center()[1])
        fbox = filter_box().move_to([0, -1.4, 0])
        fnote = note("our query: remove the filter", size=22).next_to(fbox, DOWN, buff=0.25)
        ghost = dbox(fbox[0].width, fbox[0].height, color=LOOKUP, fill_op=0.0, radius=0.1).move_to(fbox)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(rerank_all, scale=0.15, target_position=c.slots[2].get_center()),
                      ReplacementTransform(c.slots[2], chip4), light(c.post, False),
                      FadeOut(panel.dash), FadeOut(title), FadeOut(ref4), run_time=1.0)
            # cli.py arrives with the chips, while "cli.py" is said
            self.play(*[ch.animate.move_to(t) for ch, t in zip(chips, row)],
                      FadeIn(cli, shift=LEFT * 0.2), FadeIn(not_here, shift=UP * 0.1), run_time=0.9)
            vo.wait_until("They're what you reach for")
            # light each chip's dashes and words (not its dark fill, which Indicate would turn into a
            # solid pill that hides the words)
            self.play(LaggedStart(*[Indicate(VGroup(*ch[1:]), color=TURN, scale_factor=1.08) for ch in chips],
                                  lag_ratio=0.2), run_time=1.2)
            vo.wait_until("when naive retrieval")
            self.play(c.ret.animate.set_stroke(ERR, 4), run_time=0.4)
            self.play(Indicate(c.ret_lab, color=ERR, scale_factor=1.1), run_time=0.8)
            self.play(c.ret.animate.set_stroke(GREY, 2.5), run_time=0.4)
            vo.wait_until("our filtered query")
            self.play(FadeIn(fbox, shift=UP * 0.2), run_time=0.6)
            self.play(Write(fnote), run_time=0.8)
            vo.wait_until("its filter removed")
            # the box becomes a dashed ghost; its name stays, faint, so the empty outline says what went
            self.play(FadeIn(ghost), fbox[0].animate.set_opacity(0.0), fbox[1].animate.set_opacity(0.4),
                      run_time=0.9)
        self.wait(0.6)
        self.play(FadeOut(VGroup(concept, c.all, chips, cli_g, ghost, fnote, fbox)), run_time=0.9)
