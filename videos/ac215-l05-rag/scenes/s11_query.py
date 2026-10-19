"""S11 · Asking the database: rank and cut (README "Query" steps 1–2). Lecture: A39, A48–A53.

Beats (script.md "## S11", one voiceover block each):
 0  LECTURE A39. TRACKER Query (no step lit yet). V1 with both lanes; the bottom lane flashes PINK
    and its query box lights. The PINK question card `How is tolminc cheese made?` slides into the
    lower half of the BLUE embedding box; V1's query vector flashes, the map fades around it, and
    it becomes the PINK query arrow in V4's sphere drawing, among GREEN chunk arrows (tag our
    illustration). A PINK beam
    widens from the query to its nearest arrows (YELLOW flash, "nearest neighbors"). The mini-map
    comes in, query lit.
 1  LECTURE A48–A53. V6, first half: the sphere goes (first, so nothing overlaps the column); four
    remaining GREEN arrows fly into a column of GREEN
    cards, the query arrow becomes a PINK query bar on the left (header "similarity (lecture)",
    "bigger = closer", tag lecture example). As each number is spoken the query bar slides down
    beside its row, a PINK comparison line flashes and the score writes in: 0.57, 0.77, 0.43,
    0.93. The column re-sorts; a YELLOW line cuts it under the top rows, "top K"; on "This code uses
    10" an excerpt chip cli.py · line 356 `n_results=10`.
 2  The flip: the header and the similarity arrow light; a GREY double scale writes in under the
    column (similarity −1 … 1). Each score becomes 1 − score (0.07, 0.23, 0.43, 0.57), the header
    becomes "cosine distance (Chroma)", the arrow turns over ("bigger = farther"); the scale's
    distance row (2 … 0) and "0 = same direction" write in; the cards (same order) and the arrow
    flash.
 3  The chip leaves; the rows below the K-line dim; a GREY note "near or far, 10 rows come back ·
    fewer only if fewer chunks exist"; the K-line and the top rows flash; the note's headline "no
    distance threshold in this code".
 4  CODE(cli.py: 316–323) (the column, the scale, the lecture tag and the mini-map leave). Line 318
    lights (the question PINK); line 319 (generate_query_embedding BLUE, with a BLUE glyph of the
    shared box, "same model as the chunks"); line 323 with the f-string of line 316 GREEN and a
    GREEN chip `char-split-collection` "for --chunk_type char-split".
 5  TRACKER Query 1. TEAL terminal (13 rows, app@390fe47a277a:/app$, tag real run · no key on the
    title bar) types `python cli.py --query --chunk_type char-split` (on the row under the long
    prompt); GOLD tag "one embedding call per question · your project pays" on the prompt row.
    cli-container/40 lines 2–3: line 3
    `load()` boxed YELLOW + erratum tag "a copy-paste label · cli.py · line 310"; then …, 9–13, …,
    64 (RED, wrapped). The terminal shrinks to the strip (the command and the error's last row);
    above it the BLUE embedding box, the PINK question card and the TEAL Chroma cylinder, which
    blinks ("connected · cli.py · line 313"); the question card drops onto the BLUE box and stops,
    RED cross, the strip's error row flashes; "no search ran" under the cylinder.
 6  The question card slides at the cylinder and bumps off an arrow-shaped PINK slot (flashing
    RED); chip "Chroma takes vectors, not words". It returns to the BLUE box; a dashed PINK arrow
    (what the box would make) slides out and fits the slot; it fades, a dashed GOLD key outline
    with a RED cross and "no key" appears at the box, which stays dark; GREY chip "only the same
    model makes a vector in the same space".
 7  TRACKER Query 2. The picture leaves; the strip is cleared and loses its `real run · no key` tag
    (this command was not run here), then types `python cli.py --query --chunk_type
    recursive-split` (no output). ▶ your turn on a GREY card listing both query commands (GOLD tag
    "one embedding call per question"). The strip leaves and the card moves down to its place; a
    GREY "with your key, look for" card writes in its rows as named (cli.py lines 320, 360, 361);
    under it four GREY slots `ids` `distances` `metadatas` `documents`, each holding one dashed
    inner list (no values); the inner lists flash on "one list per query", the keys as named.
    Hold 2 s.
 8  The turn card leaves. Chip `results["documents"][0]` (cli.py · line 386 · in chat()), its
    `[0]` boxed YELLOW, a YELLOW arrow to the documents slot's inner list, which turns YELLOW (the
    chip's header sits under it, so the arrow crosses no text). GREY note "no results
    were recorded: next, we ask the loaded database directly". Fade to an empty frame.

Timing: beat 1's four numbers are one lexicon entry inside one sentence, so character
interpolation would put them about 4 s late; they are placed at the pauses measured in the cached
clip (`_at`: 3.5, 5.4, 7.2, 8.9 s). Everything else is anchored with vo.wait_until at sentence or
clause starts.

Deviations from SHOW (see the scene report): the terminal of beat 5 has 13 rows, not 11, and
cli-container/40 line 2 is cut with … instead of wrapped (as S08 does with the same line of
cli-container/20): wrapped, the 15 rows would scroll the typed command and its GOLD tag away. The
strip keeps the error's second row (`-service-account.json was not found.`), as S08's does. The
mini-map stays hidden from beat 4 on (code panel, 13-row terminal, the picture above the strip,
then the cards leave no free corner). Beat 3 has no animated "every row is far away" picture: the
SHOW's note text carries it ("near or far, 10 rows come back"), next to the K-line. In beat 7 the
3-row strip leaves (it "shrinks" away) after the second command is typed, and the turn card takes
its place at the bottom, so the turn card, the look-for card and the four result slots fit
together; the turn card stays up through the 2-s hold. Additions that SHOW does not name: a
"query" label on the PINK bar (beat 1), the GREEN `char-split-collection` chip (beat 4: what
line 316's f-string makes for this run), "Chroma" over the cylinder and "no key" under the key
outline (beats 5–6).
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    ReplacementTransform,
    ShowPassingFlash,
    Transform,
    UpdateFromAlphaFunc,
    VGroup,
    there_and_back,
)

from common import (
    BOTTOM,
    CLOUD,
    COST,
    CTR,
    DATA,
    EMBED_MODEL,
    ERR,
    INK,
    LOOKUP,
    MINI_CENTER,
    NARRATION,
    P_CTR2,
    QUESTION,
    STRIP_TOP,
    TURN,
    LookFor,
    MiniMap,
    RagMap,
    RankColumn,
    VectorSketch,
    beside,
    chunk_card,
    col_box,
    cost_tag,
    cylinder,
    erratum_tag,
    example_tag,
    excerpt,
    excerpt_chip,
    capture,
    key_outline,
    lref,
    lref_swap,
    model_box,
    nokey_tag,
    note,
    our_illustration_tag,
    pin,
    question_card,
    resize,
    sans,
    src_panel,
    term,
    tracker,
    turn_card,
    type_cmd,
)
from explainer import style as S
from explainer.devops import CAPTION, MONO, box, chip, cross_mark, label, mono
from explainer.scene import VoiceScene

SAY = NARRATION["S11"]

# ------------------------------------------------------------------ the real capture and source
Q1 = "python cli.py --query --chunk_type char-split"          # README.md line 178
Q2 = "python cli.py --query --chunk_type recursive-split"     # README.md line 179
QRY = capture("40", "cli-container")
assert QRY.cmd == Q1 and QRY.exit == 1, (QRY.cmd, QRY.exit)
assert QRY.line(3) == "load()" and "DefaultCredentialsError" in QRY.line(64)
Q_HEAD = QRY.at(2, 3)                    # line 2 is cut with … by the terminal (see Deviations)
Q_REST = QRY.at("…", (9, 13), "…")
Q_ERR = QRY.line(64)
assert "line 319, in query" in QRY.line(9) and "line 79, in generate_query_embedding" in QRY.line(12)

assert QUESTION in excerpt("cli.py", 318, 318)
assert 'print("load()")' in excerpt("cli.py", 310, 310)
assert "chromadb.HttpClient" in excerpt("cli.py", 313, 313)
L356 = excerpt("cli.py", 356, 356)       # n_results=10, (query(), the active variant #4)
L386 = excerpt("cli.py", 386, 386)       # print(len(results["documents"][0]))  (in chat())
assert "n_results=10" in L356 and 'results["documents"][0]' in L386

# ------------------------------------------------------------------ layout
SPH_O = np.array([0.3, 0.1, 0])          # V4's origin (beat 0)
SPH_R = 1.75
Q_DEG = 60                               # the query arrow's direction (our illustration)
NEAR = (50, 56, 66, 71)                  # chunk arrows inside the beam (the nearest)
FAR = (44, 148, 157, 165, 172, 262, 270, 281, 289)
TO_CARDS = (148, 66, 281, 56)            # arrows that fly into rows 0..3 (0.57, 0.77, 0.43, 0.93)
CARDS_AT = np.array([-0.2, 0.85, 0])     # V6's card column centre (beat 1)
QBAR_X = -3.65                           # the PINK query bar, left of the column
SCORE_T = (3.54, 5.38, 7.2, 8.88)        # measured starts of 0.57, 0.77, 0.43, 0.93 in SAY[1]

BOX_AT = np.array([-2.2, 0.0, 0])        # beat 5-6 picture above the strip
CARD_HOME = np.array([-2.2, 2.2, 0])
CYL_AT = np.array([4.3, 0.75, 0])
SLOT_Y = 0.95


def _at(scene, vo, t: float):
    """Wait until `t` seconds into the current clip (a measured pause; see the docstring)."""
    dt = t - vo.elapsed
    if dt > 1 / 60:
        scene.wait(dt)


def mixed(parts, size: float = CAPTION, color: str = INK) -> VGroup:
    """One row of serif pieces and `mono` pieces (in backticks); (text, colour) for a colour."""
    mobs = []
    for p in parts:
        s, col = (p, color) if isinstance(p, str) else p
        if len(s) > 1 and s.startswith("`") and s.endswith("`"):
            mobs.append(mono(s[1:-1], size, col))
        else:
            mobs.append(label(s, size, col))
    return VGroup(*mobs).arrange(RIGHT, buff=0.12)


def place_origin(vs: VectorSketch, at) -> VectorSketch:
    return vs.shift(np.array(at) - vs.o.get_center())


def chunk_arrow(vs: VectorSketch, deg: float) -> Arrow:
    """A GREEN chunk arrow, length 0.78–0.86 (seeded by its angle)."""
    length = 0.78 + 0.08 * ((deg * 37) % 11) / 10
    return vs.arrow(deg, length, DATA, stroke=4)


def beam_anim(vs: VectorSketch, center: float, half: float, run_time: float = 1.2):
    """A PINK beam (a sector) widening from the query direction to ±half degrees."""
    beam = vs.sector(center - 0.5, center + 0.5, LOOKUP, opacity=0.3)

    def grow(m, a):
        h = max(0.5, half * a)
        m.become(vs.sector(center - h, center + h, LOOKUP, opacity=0.3))

    return beam, UpdateFromAlphaFunc(beam, grow, run_time=run_time)


def double_scale(width: float = 3.6) -> VGroup:
    """A GREY scale: similarity −1 … 1 above the line, distance 2 … 0 under it (A45; Chroma).
    .sim (row above) .dist (row under) .line .same ("0 = same direction")"""
    ln = Line(LEFT * width / 2, RIGHT * width / 2, color=S.GREY, stroke_width=3)
    ticks = VGroup(*[Line(UP * 0.1, DOWN * 0.1, color=S.GREY, stroke_width=3).move_to(ln.point_from_proportion(p))
                     for p in (0, 0.5, 1)])
    sim_vals = VGroup(*[mono(s, CAPTION, S.GREY).next_to(tk, UP, buff=0.1) for s, tk in zip(("−1", "0", "1"), ticks)])
    dist_vals = VGroup(*[mono(s, CAPTION, S.GREY).next_to(tk, DOWN, buff=0.1) for s, tk in zip(("2", "1", "0"), ticks)])
    sim_cap = label("similarity", CAPTION, S.GREY)
    sim_cap.move_to([ln.get_left()[0] - 0.45 - sim_cap.width / 2, sim_vals.get_center()[1], 0])
    dist_cap = label("distance", CAPTION, S.GREY)
    dist_cap.move_to([ln.get_left()[0] - 0.45 - dist_cap.width / 2, dist_vals.get_center()[1], 0])
    same = label("0 = same direction", CAPTION, INK)
    same.next_to(dist_vals[2], RIGHT, buff=0.35)
    g = VGroup(ln, ticks, sim_vals, sim_cap, dist_vals, dist_cap, same)
    g.line, g.sim, g.dist, g.same = VGroup(ln, ticks), VGroup(sim_vals, sim_cap), VGroup(dist_vals, dist_cap), same
    return g


def arrow_slot(w: float = 0.95, h: float = 0.36, color: str = LOOKUP, dashed: bool = True):
    """An arrow-shaped outline (the slot in the database, or the vector that would fit it)."""
    sh = h * 0.42
    pts = [[-w / 2, -sh / 2, 0], [w / 2 - h * 0.7, -sh / 2, 0], [w / 2 - h * 0.7, -h / 2, 0], [w / 2, 0, 0],
           [w / 2 - h * 0.7, h / 2, 0], [w / 2 - h * 0.7, sh / 2, 0], [-w / 2, sh / 2, 0]]
    p = Polygon(*pts, stroke_color=color, stroke_width=3).set_fill(color, 0.12)
    if not dashed:
        return p
    d = DashedVMobject(p, num_dashes=22, dashed_ratio=0.55).set_stroke(color, 3)
    return VGroup(p.set_stroke(width=0), d)


def result_slot(key: str, w: float = 2.55) -> VGroup:
    """One key of the results dict: `key` over a GREY outer list holding one dashed inner list.
    .key .outer .inner"""
    k = mono(key, CAPTION, INK)
    outer = box(w, 0.52, S.GREY, fill_opacity=0.06, radius=0.1, stroke=2.5)
    inner = box(w - 0.7, 0.28, S.GREY, dashed=True, radius=0.06, stroke=2.5)
    lb, rb = mono("[", CAPTION, S.GREY), mono("]", CAPTION, S.GREY)
    lb.next_to(outer.get_left(), RIGHT, buff=0.1)
    rb.next_to(outer.get_right(), LEFT, buff=0.1)
    inner.move_to(outer)
    k.next_to(outer, UP, buff=0.12)
    g = VGroup(k, outer, lb, rb, inner)
    g.key, g.outer, g.inner = k, outer, inner
    return g


class NearestNeighbours(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        tr = tracker("Query")

        # ========================================================== 0 · the bottom lane: question -> query vector
        lr = lref("A39")
        rm = RagMap(show=RagMap.TOP + RagMap.BOTTOM + RagMap.LABELS)
        qc = question_card().move_to([-3.75, -2.75, 0])
        vs = place_origin(VectorSketch(r=SPH_R), SPH_O)
        arrows = {d: chunk_arrow(vs, d) for d in NEAR + FAR}
        green = VGroup(*arrows.values())
        qa = vs.arrow(Q_DEG, 0.95, LOOKUP, stroke=6)
        q_lab = label("query vector", CAPTION, LOOKUP)
        q_lab.next_to(vs.point(Q_DEG, 0.95), RIGHT, buff=0.2).shift(UP * 0.12)
        c_lab = label("chunk vectors", CAPTION, DATA)
        c_lab.move_to([vs.point(160, 0.85)[0] - 0.55 - c_lab.width / 2, vs.point(160, 0.85)[1] + 0.05, 0])
        ill = our_illustration_tag().move_to([SPH_O[0], SPH_O[1] - SPH_R - 0.38, 0])
        near = VGroup(*[arrows[d] for d in NEAR])
        n_lab = label("nearest neighbors", CAPTION, TURN)
        n_lab.move_to([vs.point(40, 1.05)[0] + 0.25 + n_lab.width / 2, vs.point(40, 1.05)[1] - 0.1, 0])
        mm = MiniMap(MINI_CENTER)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), FadeIn(lr), FadeIn(rm), run_time=0.7)
            self.play(rm.pulse_lane("bottom", LOOKUP), rm.light("query"), FadeIn(qc, shift=UP * 0.1), run_time=1.0)
            vo.wait_until("The question goes through")
            self.play(qc.animate.move_to([RagMap.X["embedding"], RagMap.YB, 0]).scale(0.18).set_opacity(0),
                      rm.light("embedding"), run_time=1.2)
            self.remove(qc)
            vo.wait_until("and becomes a query vector")
            self.play(Indicate(rm.item("query"), color=LOOKUP, scale_factor=1.35), run_time=0.7)
            q_from = rm.item("query").copy()
            self.add(q_from)
            self.play(FadeOut(rm), run_time=0.5)            # the map goes first; the query vector stays
            vo.wait_until("in the same space")
            self.play(FadeIn(vs), LaggedStart(*[GrowArrow(a) for a in green], lag_ratio=0.05),
                      ReplacementTransform(q_from, qa), FadeIn(q_lab, shift=RIGHT * 0.1), run_time=1.2)
            self.play(LaggedStart(*[Indicate(a, color=DATA, scale_factor=1.08) for a in green], lag_ratio=0.04),
                      FadeIn(c_lab, shift=LEFT * 0.1), FadeIn(ill), run_time=0.9)
            vo.wait_until("Querying means")
            beam, grow = beam_anim(vs, Q_DEG, 13)
            self.add(beam, qa)
            self.play(grow)
            self.play(LaggedStart(*[Indicate(a, color=TURN, scale_factor=1.1) for a in near], lag_ratio=0.15),
                      FadeIn(n_lab, shift=RIGHT * 0.1), run_time=0.9)
            self.play(FadeIn(mm), mm.light("query"), run_time=0.5)

        # ========================================================== 1 · A48–A53: score, sort, cut
        rc = RankColumn(pitch=0.7, show=())
        rc.shift(CARDS_AT - rc.cards.get_center())
        row_y = [rc.cards[k].get_center()[1] for k in range(4)]
        qbar = chunk_card(1.3, 0.42, LOOKUP, rows=2).move_to([QBAR_X, row_y[0], 0])
        qbar_lab = label("query", CAPTION, LOOKUP).next_to(qbar, UP, buff=0.12)
        ex = example_tag()
        hdr = rc.parts["header"]
        ex.move_to([rc.ax.get_center()[0] + 0.2 + ex.width / 2, hdr.get_center()[1], 0])
        n10 = excerpt_chip("n_results=10", "cli.py · line 356 (excerpt)", line=L356)

        def compare(k):
            a = np.array([qbar.get_right()[0] + 0.08, row_y[k], 0])
            b = np.array([rc.cards[k].get_left()[0] - 0.08, row_y[k], 0])
            return Line(a, b, color=LOOKUP, stroke_width=5)

        with self.voiceover(SAY[1]) as vo:
            lr = lref_swap(self, lr, "A48–A53", run_time=0.4)
            # the sphere goes first (nothing overlaps the column); four arrows and the query stay
            self.play(FadeOut(VGroup(vs, beam, c_lab, n_lab, ill, q_lab,
                                     *[arrows[d] for d in NEAR + FAR if d not in TO_CARDS])), run_time=0.5)
            rc.reveal(self, "cards", "header", "arrow", run_time=1.2,
                      extra=[*[FadeOut(arrows[d], target_position=rc.cards[k].get_center(), scale=0.6)
                               for k, d in enumerate(TO_CARDS)],
                             ReplacementTransform(qa, qbar), FadeIn(qbar_lab), FadeIn(ex)])
            for k, t in enumerate(SCORE_T):
                _at(self, vo, t - 0.35)
                if k:
                    self.play(qbar.animate.set_y(row_y[k]), qbar_lab.animate.set_y(row_y[k] + 0.45), run_time=0.35)
                self.play(ShowPassingFlash(compare(k), time_width=0.6), *rc.parts_in(f"score{k}"), run_time=0.55)
            vo.wait_until("Sort by score")
            self.play(rc.sort(), qbar.animate.set_y(row_y[0]), qbar_lab.animate.set_y(row_y[0] + 0.45), run_time=1.0)
            vo.wait_until("and keep the top K")
            kl = rc.k_line(2)
            self.play(Create(kl[0]), FadeIn(kl[1], shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("with K fixed in advance")
            self.play(Indicate(kl[1], color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("This code uses 10")
            n10.move_to([kl[1].get_right()[0] - n10.width / 2, kl.get_bottom()[1] - 0.3 - n10.height / 2, 0])
            self.play(FadeIn(n10, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(n10.text, color=TURN, scale_factor=1.06), run_time=0.6)

        # ========================================================== 2 · the flip: similarity -> Chroma's distance
        sc = double_scale()
        sc.move_to([-0.75, -1.35, 0]).shift(RIGHT * (sc.get_center()[0] - sc.line.get_center()[0]))

        with self.voiceover(SAY[2]) as vo:
            vo.wait_until("the lecture ranks by similarity")
            self.play(Indicate(hdr, color=TURN, scale_factor=1.08), FadeIn(sc.line), FadeIn(sc.sim, shift=UP * 0.1),
                      run_time=0.8)
            vo.wait_until("where higher is better")
            self.play(Indicate(VGroup(rc.ax, rc.al), color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Chroma reports cosine distance")
            self.play(*rc.flip(), run_time=1.1)
            vo.wait_until("one minus the similarity")
            self.play(FadeIn(sc.dist, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("where smaller is closer")
            self.play(FadeIn(sc.same, shift=LEFT * 0.1), Indicate(rc.scores[rc.order[0]], color=TURN, scale_factor=1.2),
                      run_time=0.8)
            vo.wait_until("Same order")
            self.play(LaggedStart(*[Indicate(rc.cards[k], color=DATA, scale_factor=1.06) for k in rc.order],
                                  lag_ratio=0.15), run_time=0.8)
            self.play(Indicate(VGroup(rc.ax, rc.al), color=TURN, scale_factor=1.06), run_time=0.7)

        # ========================================================== 3 · K results, relevant or not
        row_a = note("near or far, 10 rows come back · fewer only if fewer chunks exist")
        row_b = label("no distance threshold in this code", CAPTION + 2, INK)
        row_b.move_to([-6.3 + row_b.width / 2, -2.62, 0])
        row_a.move_to([-6.3 + row_a.width / 2, -3.1, 0])
        under_b = Line(row_b.get_corner(DOWN + LEFT) + DOWN * 0.06, row_b.get_corner(DOWN + RIGHT) + DOWN * 0.06,
                       color=TURN, stroke_width=3)
        below = VGroup(*[VGroup(rc.cards[k], rc.scores[k]) for k in rc.order[2:]])
        top = VGroup(*[VGroup(rc.cards[k], rc.scores[k]) for k in rc.order[:2]])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(n10), below.animate.set_opacity(0.25), run_time=0.7)
            self.play(Indicate(top, color=TURN, scale_factor=1.05), run_time=0.8)
            vo.wait_until("whenever K chunks")
            self.play(FadeIn(row_a, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("relevant or not")
            self.play(Indicate(kl, color=TURN, scale_factor=1.05), run_time=0.8)
            vo.wait_until("Nothing in this code")
            self.play(FadeIn(row_b, shift=UP * 0.1), run_time=0.5)
            self.play(Create(under_b), run_time=0.5)

        # ========================================================== 4 · CODE(cli.py: 316–323)
        p = src_panel("cli.py", 316, 323)
        p.move_to([-0.95, 0.35, 0])              # room at the right for the glyph's two-line label
        bar = p.bar(318)
        s_q = p.span(318, '"How is tolminc cheese made?"')
        s_g = p.span(319, "generate_query_embedding")
        s_f = p.span(316, 'f"{method}-collection"')
        s_c = p.span(323, "get_collection")
        glyph = Rectangle(width=0.34, height=0.95, stroke_color=CLOUD, stroke_width=3).set_fill(CLOUD, 0.25)
        glyph.move_to([min(5.7, p.get_right()[0] + 1.1), s_g.get_center()[1] + 0.15, 0])
        g_lab = VGroup(label("same model", CAPTION, CLOUD), label("as the chunks", CAPTION, CLOUD)) \
            .arrange(DOWN, buff=0.06).next_to(glyph, DOWN, buff=0.12)
        g_arrow = Arrow([p.get_right()[0] - 0.05, s_g.get_center()[1], 0], [glyph.get_left()[0] - 0.05, s_g.get_center()[1], 0],
                        buff=0, color=CLOUD, stroke_width=4, tip_length=0.16)
        col_chip = VGroup(chip("char-split-collection", DATA, size=CAPTION, font=MONO),
                          mixed(["for", "`--chunk_type char-split`"], color=S.GREY)).arrange(RIGHT, buff=0.3)
        col_chip.move_to([p.get_center()[0], p.get_bottom()[1] - 0.45, 0])

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(rc, qbar, qbar_lab, kl, ex, sc, row_a, row_b, under_b)), FadeOut(lr), FadeOut(mm),
                      run_time=0.4)
            self.play(FadeIn(p, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("the query function sets the question")
            self.play(FadeIn(bar), s_q.animate.set_color(LOOKUP), run_time=0.5)
            vo.wait_until("turns it into a vector")
            self.play(Transform(bar, p.bar(319)), s_g.animate.set_color(CLOUD), run_time=0.5)
            self.play(GrowArrow(g_arrow), FadeIn(glyph), FadeIn(g_lab, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("and opens the chunk type")
            self.play(Transform(bar, p.bar(323)), s_c.animate.set_color(TURN), s_f.animate.set_color(DATA), run_time=0.5)
            self.play(FadeIn(col_chip, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 5 · step 1: no key, so no search
        t = term(P_CTR2, rows=13, container=True)
        nk = nokey_tag()
        nk.move_to([t.box.get_right()[0] - 0.2 - nk.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])
        gold = cost_tag("one embedding call per question · your project pays")
        err_tag = erratum_tag("a copy-paste label · cli.py · line 310")

        emb = model_box("embedding model", sub=EMBED_MODEL).move_to(BOX_AT)
        cyl = cylinder(1.3, 1.6).move_to(CYL_AT)
        cyl_lab = sans("Chroma", CAPTION, CTR).next_to(cyl, UP, buff=0.15)
        conn = note("connected · cli.py · line 313").move_to([CYL_AT[0], cyl.get_bottom()[1] - 0.32, 0])
        nosearch = note("no search ran").next_to(conn, DOWN, buff=0.12)
        card = question_card().move_to(CARD_HOME)
        stop_at = np.array([BOX_AT[0], emb.get_top()[1] + 0.1 + card.height / 2, 0])
        x5 = cross_mark(0.42, ERR).move_to([stop_at[0] + card.width / 2 + 0.4, stop_at[1], 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(p, bar, glyph, g_lab, g_arrow, col_chip)), tr.goto(1), run_time=0.5)
            self.play(FadeIn(t), FadeIn(nk), run_time=0.4)
            cmd = type_cmd(self, t, Q1, type_time=1.8)
            assert hasattr(cmd, "rows") and len(cmd.rows) == 2, getattr(cmd, "rows", cmd)
            vo.wait_until("chunk type char split")
            pin(self, cmd.rows[0], beside(gold, t, cmd.rows[0], buff=0.5), anim=FadeIn(gold, scale=1.1), run_time=0.5)
            vo.wait_until("A small slip first")
            head = t.print(self, Q_HEAD, run_time=0.5)
            l3 = head[1]
            vo.wait_until("it prints the word load")
            cb = col_box(l3, 0, 6)
            pin(self, l3, cb, anim=Create(cb), run_time=0.4)
            vo.wait_until("a label copied")
            pin(self, l3, beside(err_tag, t, l3, buff=0.5), run_time=0.4)
            t.print(self, Q_REST, run_time=0.5)
            err = t.print(self, [(Q_ERR, ERR)], wrap=True, run_time=0.4)
            assert len(err) == 2 and len(t.lines) <= 13, (len(err), len(t.lines))
            vo.wait_until("Then it connects to Chroma")
            resize(self, t, 3, keep=[cmd.rows[0], cmd.rows[1], err[1]], run_time=0.55,
                   extra=[nk.animate.set_y(STRIP_TOP - t.bar_h / 2)])
            self.play(FadeIn(emb), FadeIn(card), FadeIn(cyl), FadeIn(cyl_lab), run_time=0.3)
            self.play(Indicate(cyl, color=CTR, scale_factor=1.1), FadeIn(conn, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("but stops at the key")
            self.play(card.animate.move_to(stop_at), run_time=0.8)
            self.play(Create(x5), Indicate(err[1], color=ERR, scale_factor=1.04), run_time=0.7)
            vo.wait_until("before it searches")
            self.play(FadeIn(nosearch, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 6 · vectors, not words; the same model
        slot = arrow_slot().move_to([CYL_AT[0], SLOT_Y, 0])
        bump_x = cyl.get_left()[0] - 0.05 - card.width / 2
        vtw = chip("Chroma takes vectors, not words", S.GREY, size=CAPTION)
        vtw.move_to([min(6.5 - vtw.width / 2, CYL_AT[0]), cyl_lab.get_top()[1] + 0.12 + vtw.height / 2, 0])
        ghost = arrow_slot().move_to([emb.get_right()[0] + 0.6, BOX_AT[1], 0])
        key = key_outline(0.46)
        key.move_to([emb.get_left()[0] - 0.35 - key.width / 2, BOX_AT[1], 0])
        kx = cross_mark(0.42, ERR).move_to(key)
        k_lab = label("no key", CAPTION, COST).next_to(VGroup(key, kx), DOWN, buff=0.12)
        same = chip("only the same model makes a vector in the same space", S.GREY, size=CAPTION)
        same.move_to([BOX_AT[0] + 0.6, emb.get_bottom()[1] - 0.34 - same.height / 2, 0])   # clear of "no key"

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(x5), FadeIn(slot), run_time=0.4)
            self.play(card.animate.move_to([bump_x, SLOT_Y, 0]), run_time=0.9)
            self.play(card.animate(rate_func=there_and_back).shift(RIGHT * 0.05), slot[1].animate.set_stroke(ERR),
                      run_time=0.2)
            self.play(card.animate.shift(LEFT * 0.7), slot[1].animate.set_stroke(LOOKUP), FadeIn(vtw, shift=DOWN * 0.1),
                      run_time=0.4)
            vo.wait_until("before the database can compare it")
            self.play(card.animate.move_to(stop_at), run_time=0.8)
            self.play(FadeIn(ghost, shift=RIGHT * 0.2), run_time=0.3)
            self.play(ghost.animate.move_to(slot), run_time=0.9)
            vo.wait_until("and only the same Google model")
            self.play(FadeOut(ghost), FadeIn(key), run_time=0.4)
            self.play(Create(kx), FadeIn(k_lab), Indicate(emb.frame, color=S.GREY, scale_factor=1.03), run_time=0.6)
            self.play(FadeIn(same, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("in the same space")
            self.play(Indicate(same.text, color=TURN, scale_factor=1.04), run_time=0.8)

        # ========================================================== 7 · step 2, your turn, what to look for
        tc = turn_card([Q1, Q2])
        g2 = cost_tag("one embedding call per question")
        g2.move_to(tc.frame.get_corner(DOWN + RIGHT) + np.array([-0.3 - g2.width / 2, 0, 0]))
        tc.add(g2)
        tc.move_to([0, (STRIP_TOP + 2.75) / 2, 0])
        tc_low = tc.copy()
        tc_low.shift(UP * (BOTTOM + 0.12 - tc_low.get_bottom()[1]))

        lf = LookFor([(mixed(["`Embedding values:`", "… 256 numbers"]), "cli.py · line 320"),
                      (mixed([f"`Query: {QUESTION}`"]), "cli.py · line 360"),
                      (mixed(["`Results:`", "a dict of lists of lists"]), "cli.py · line 361")])
        lf.move_to([0, 2.62 - lf.height / 2, 0])     # top at 2.62: clear of the tracker caption
        slots = VGroup(*[result_slot(k) for k in ("ids", "distances", "metadatas", "documents")])
        slots.arrange(RIGHT, buff=0.32)
        slot_top = lf.get_bottom()[1] - 0.25
        slots.move_to([0, slot_top - slots.height / 2, 0])

        with self.voiceover(SAY[7]) as vo:
            # the strip is cleared (the first run's error would sit above the new command) and loses
            # its `real run · no key` tag: the second command was not run here. This is Terminal.clear
            # inside the same play: the old lines leave t.lines, the rows typed next belong to t, and
            # the FadeOut(t) below takes them (no row is left in the band the turn card moves into)
            self.play(FadeOut(VGroup(emb, card, cyl, cyl_lab, conn, nosearch, slot, vtw, key, kx, k_lab, same)),
                      FadeOut(t.lines), FadeOut(nk), tr.goto(2), run_time=0.5)
            for m in list(t.lines):
                t.lines.remove(m)
            cmd2 = type_cmd(self, t, Q2, type_time=1.4)
            assert hasattr(cmd2, "rows") and len(cmd2.rows) == 2
            vo.wait_until("pause and run both")
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("With your key")
            self.play(FadeOut(t), run_time=0.3)          # the strip goes first: the card never crosses it
            self.play(Transform(tc, tc_low), run_time=0.5)
            self.play(FadeIn(lf), run_time=0.3)
            vo.wait_until("look for 256")
            self.play(lf.write_item(0))
            vo.wait_until("the query,")
            self.play(lf.write_item(1))
            vo.wait_until("and the results")
            self.play(lf.write_item(2))
            vo.wait_until("The results are lists of lists")
            self.play(LaggedStart(*[FadeIn(VGroup(s.key, s.outer, s[2], s[3]), shift=UP * 0.1) for s in slots],
                                  lag_ratio=0.15), run_time=0.8)
            vo.wait_until("one list per query")
            self.play(LaggedStart(*[Create(s.inner) for s in slots], lag_ratio=0.1), run_time=0.7)
            self.play(LaggedStart(*[Indicate(s.inner, color=TURN, scale_factor=1.06) for s in slots], lag_ratio=0.1),
                      run_time=0.7)
            for s, phrase in zip(slots, ("holding IDs", "distances", "metadata", "and documents")):
                vo.wait_until(phrase)                  # each key flashes as it is named
                self.play(Indicate(s.key, color=TURN, scale_factor=1.15), run_time=0.55)
        self.wait(2)                                   # ▶ beat: hold the frame

        # ========================================================== 8 · documents, item zero
        dchip = excerpt_chip('results["documents"][0]', "cli.py · line 386 · in chat()", line=L386)
        doc = slots[3]
        zero = VGroup(*dchip.text[-3:])
        dchip.header.next_to(dchip.chip, DOWN, buff=0.1).align_to(dchip.chip, LEFT).shift(RIGHT * 0.08)
        dchip.shift(np.array([doc.inner.get_center()[0] - zero.get_center()[0], -1.75 - dchip.chip.get_center()[1], 0]))
        zbox = box(zero.width + 0.14, zero.height + 0.16, TURN, fill_opacity=0.0, radius=0.05, stroke=3).move_to(zero)
        z_arrow = Arrow(zbox.get_top(), doc.inner.get_bottom(), buff=0.08, color=TURN, stroke_width=4, tip_length=0.18)
        rec = note("no results were recorded: next, we ask the loaded database directly")
        rec.move_to([0, -3.15, 0])

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(tc), run_time=0.4)
            self.play(FadeIn(dchip, shift=UP * 0.1), run_time=0.5)
            self.play(Create(zbox), zero.animate.set_color(TURN), run_time=0.4)
            self.play(GrowArrow(z_arrow), run_time=0.5)
            self.play(doc.inner.animate.set_stroke(TURN, 3.5), run_time=0.5)
            self.play(Indicate(doc.inner, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("No results were recorded")
            self.play(FadeIn(rec, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("so next we ask")
            self.play(Indicate(rec, color=INK, scale_factor=1.03), run_time=0.8)
        self.play(FadeOut(VGroup(lf, slots, dchip, zbox, z_arrow, rec)), FadeOut(tr), run_time=0.8)
        self.wait(0.3)
