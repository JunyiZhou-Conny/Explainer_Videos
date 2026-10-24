"""S01 · Which sentence would you trust? (cold open of AC215 L7). Lecture: 21, then 3.

Beats (script.md "## S01", one voiceover block each):
0. Cold open, no tracker. Top right the GREY tag "recorded · the staff's saved Colab run" (it covers
   everything the hook shows from the staff's run, until V1 opens). A GREY request card "Customer
   ask" holds RECORDED(expected/colab-c23-agent-harness.txt: 5), folded at spaces onto 4 rows so
   that no named phrase breaks. As the SAY names each phrase it turns YELLOW in the card while its
   GREY chip writes in under the card (nothing flies): 12 guests in PA · $150.00 budget · avoid
   nuts · at least one cheese from France · a funk rating of 4 or higher. The card fades and the
   chips rise into its place. At "Here are two answers" two empty BLUE answer cards slide in side by
   side, "answer A" and "answer B", and the BLUE chip "same model · same five tools · same request"
   writes in under them.
1. Card A fills with RECORDED(expected/colab-c21-bare-agent.txt: 4) excerpted (exact sub-strings,
   GREY "…" between them); "1,050 g" and "5,600¢" are indicated as they are named. Card B fills with
   RECORDED(expected/colab-c23-agent-harness.txt: 61) excerpted. At "within a budget with the
   comma" a RED ring circles card B's "1,5000¢" and card A's "15,000¢" gets a thin GREY underline;
   at "a malformed number" the garbled number turns RED.
2. The BLUE chip fades and both cards dim; the question writes in YELLOW across the lower third (no
   timer), its second row at "And what would"; the RED ring pulses once. A one-second hold.
3. The question and the request chips fade; the cards brighten and rise (A stays left, B right).
   Under card B a GREEN-bordered output box prints RECORDED(c23: 63-70) line by line as the SAY
   names it (line 63 folded at a space so the box fits the right half). "The cart was valid": a
   GREEN check lands beside card B's "1,200 g" (GREEN underline) while the RED ring stays; "only
   the sentence was garbled": the ring pulses and the GREEN caption "checks the items · not the
   prose" writes in left of the box's "Cart satisfies" row. "Nothing checked": card A gets the GREY
   dashed tag "bare agent · no final cart check".
4. LECTURE 21 (the recorded tag leaves first). V1 opens: card A slides down, card B slides left at
   its own height (clear of the box) and drops into the slot above it; at "the model proposes" the
   BLUE column "the model proposes" fades in around them (after B has landed: the column title sits
   on B's path); at "the harness decides" the GREEN column "the harness decides" fades in as the
   check box rises into it; the dim YELLOW stamp "a human decides" sits at its lower right. At "The harness is the code
   around the model" the GREEN column pulses; the four GREEN words write in as named (the loop ·
   its limits · its context · its checks); at "Today we sort" both columns pulse.
5. LECTURE 3. The cards, the box, the words and the stamp fade; the columns shrink to a band at the
   top. Below, our drawing of the map: GREY "Lecture 7 · outline" (slide 3's seven sections) left,
   `README.md · lines 13–21` (the tutorial activities) right; seven PINK links draw in row order at
   "in order"; at "six acts" the five act chips turn YELLOW; at "in a fictional cheese shop" the
   excerpt chip `README.md · line 27 (excerpt)` writes in at the bottom, and at "where nothing is
   really bought" its "mock, in-memory" gets a YELLOW underline.
6. The map clears. Layout preview, piece by piece as named: the tracker top left ("README › Setup ›
   Start container", 4 dots, none lit) inside a pulsing YELLOW ring, GREY caption "the README
   step" under it; the GREY lecture_ref(7, "21") tag top right, pulsing once, GREY caption "the
   lecture slides" under it; a 2-row laptop terminal strip types `mkdir -p ../secrets`; its title
   bar carries the GREY "preview" tag and then the YELLOW ▶ your turn tag (the prompt and command
   fill the row to x 4.56, so the 2.0-wide tag cannot sit beside the command). 2 s hold.
7. The preview clears. The honest-limit card: "One honest limit" with the GREY chip "recorded
   October 20, 2026" (at the date) and the GREY "no key" tag (at "without an OpenAI key"); the
   card's outline draws with its first row, and its rows write in as named: GREEN "ran for real: the build · the tests · every offline and scripted
   command", RED "every live command: up to its first model call, then a 401 (no key)", BLUE "live
   answers: `recorded` = the staff's saved Colab run · `expected` = the README's own words".
8. The card clears. The GOLD tag `live · billed per token` over "the only cost: OpenAI tokens · no
   cloud project · no service account"; the two GREY chips ‹customer 1› ‹customer 2› over "customer
   IDs masked on screen · your terminal and the README show them"; the footer "every command:
   MLOps_Learning · guides/L07-agents-2-harness.md". A hold, then everything fades to an empty frame.

Every output line comes from capture("expected/colab-c23-agent-harness") / ("expected/colab-c21-
bare-agent") (exact sub-strings, checked below); the README phrase from source_line("README.md", 27).
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
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    RoundedRectangle,
    Succession,
    VGroup,
    Write,
    there_and_back,
)

from explainer import style as S
from explainer.scene import VoiceScene

from common import (
    CLOUD,
    ERR,
    GUIDE,
    HARNESS,
    INK,
    LOOKUP,
    MONO,
    NARRATION,
    P_REPO,
    TURN,
    TwoColumns,
    box,
    capture,
    check_mark,
    chip,
    concept_tag,
    cross_mark,
    excerpt_chip,
    frame_tags,
    grey_masks,
    label,
    line_pitch,
    live_tag,
    lref,
    mask_chip,
    mono,
    mono_line,
    nokey_tag,
    note,
    notebook_glyph,
    output_box,
    preview_tag,
    recorded_tag,
    ring,
    sans,
    source_line,
    substring,
    term,
    tracker,
    type_cmd,
    under,
    your_turn,
)

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources
REC23 = capture("expected/colab-c23-agent-harness")      # the staff's saved run of cell 23 (Agent + Harness)
REC21 = capture("expected/colab-c21-bare-agent")         # cell 21 (the bare agent)

ASK = REC23.line(5)                                      # "Could you help me order cheese …"
ASK_ROWS = ["Could you help me order cheese for a tasting for",
            "12 guests in PA on a $150.00 budget? We need to avoid nuts.",
            "I'd like at least one cheese from France and at least one with",
            "a funk rating of 4 or higher. Could you suggest some pairings too?"]
assert " ".join(ASK_ROWS) == ASK, ASK
# (row of ASK_ROWS, phrase): the chips under the card, in the order the SAY names them
PHRASES = [(1, "12 guests in PA"), (1, "$150.00 budget"), (1, "avoid nuts"),
           (2, "at least one cheese from France"), (3, "a funk rating of 4 or higher")]
ANCHORS0 = ["12 guests in Pennsylvania", "a 150 dollar budget", "no nuts", "a French cheese",
            "and one with a funk rating"]

A_SRC = REC21.line(4)                                    # the bare agent's answer (one quoted string)
A_PIECES = ["Proposed tasting for 12 guests: 1,050 g total",
            "within your 960–1,200 g target and 15,000¢ budget.",
            "Cheese subtotal: 5,600¢",
            "the order has not been placed."]
A_ROWS = ["Proposed tasting for 12 guests:",
          "1,050 g total … within your",
          "960–1,200 g target and 15,000¢",
          "budget. … Cheese subtotal: 5,600¢",
          "… the order has not been placed."]
B_SRC = REC23.line(61)                                   # the harness run's prose answer
B_PIECES = ["Proposed tasting for 12 guests: 1,200 g total (100 g per guest), within your 1,5000¢ budget.",
            "Cheese subtotal: 6,400¢"]
B_ROWS = ["Proposed tasting for 12 guests:",
          "1,200 g total (100 g per guest),",
          "within your 1,5000¢ budget. …",
          "Cheese subtotal: 6,400¢ …"]
for _p in A_PIECES:
    assert _p in A_SRC, _p
for _p in B_PIECES:
    assert _p in B_SRC, _p
assert " ".join(A_ROWS) == " … ".join(A_PIECES)
assert " ".join(B_ROWS) == " … ".join(B_PIECES) + " …"

# the independent cart check (c23 lines 63-70); line 63 folds at a space (hanging indent 2)
L63 = REC23.line(63)
_cut = L63.index(" (no automatic")
CHECK_ROWS = ([(L63[:_cut], REC23.color(63)), ("  " + L63[_cut + 1:], REC23.color(63))]
              + REC23.out((64, 70)))
assert CHECK_ROWS[2][0] == "  1200 g; cheese subtotal $64.00"
assert CHECK_ROWS[6][0] == "  Cart satisfies the shop rules." and CHECK_ROWS[6][1] == HARNESS
assert CHECK_ROWS[-1][0] == "No order was placed."

QUESTION = ["Which of these would you let charge a customer's card —",
            "and what would have to be true first?"]

# the map (slide 3 beside README.md:13-21; our drawing)
OUTLINE = ["Recap", "Context Engineering", "Agent Harness", "Skills", "Agent Systems", "Evaluation",
           "Additional Resources"]
ACTS = ["Act 1", "Act 2", "Acts 3–4", "Act 5", "Act 6", "Evaluation", "Resources"]
MOCK = "Orders and inventory changes are mock, in-memory operations."
MOCK_LINE = source_line("README.md", 27)
assert MOCK in MOCK_LINE

CMD = "mkdir -p ../secrets"                              # README.md Setup › Start container, step 1

LIMIT_ROWS = [  # (glyph kind, coloured lead, rest, colour)
    ("check", "ran for real:", "the build · the tests · every offline and scripted command", HARNESS),
    ("cross", "every live command:", "up to its first model call, then a 401 (no key)", ERR),
    ("book", "live answers:", "`recorded` = the staff's saved Colab run ·", CLOUD),
]
LIMIT_ROW3B = "`expected` = the README's own words"

# ------------------------------------------------------------------ layout
SAFE_X, SAFE_Y = 6.5, 3.5
PT = 20                         # every mono row of the hook (output, the house panel size)
PITCH = line_pitch(PT)
CARD_W = 5.9                    # an answer card (fits V1's 6.3-wide column)
CX = 3.3                        # card centres = V1's column centres
V1_W, V1_GAP, V1_H, V1_Y = 12.9, 0.3, 5.9, -0.1     # V1: 12.9 x 5.9, top 2.85 (under the lecture tag)
BAND_Y = 2.45                   # the band: 1.1 tall, top 3.0
HEAD_TOP_0 = 1.48               # the answer cards' headers in beats 0-2
HEAD_TOP_3 = 2.95               # ... in beat 3


# ------------------------------------------------------------------ small helpers
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
        assert m.get_left()[0] >= -6.6 and m.get_right()[0] <= 6.6, (m.get_left(), m.get_right())
        assert m.get_bottom()[1] >= -3.6 and m.get_top()[1] <= 3.6, (m.get_bottom(), m.get_top())


def apart(a, b, gap: float = 0.05):
    """Assert the bounding boxes of a and b do not overlap."""
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    assert sep, (a.get_corner(DOWN + LEFT), a.get_corner(UP + RIGHT), b.get_corner(DOWN + LEFT),
                 b.get_corner(UP + RIGHT))


def mono_rows(lines, size: float = PT, color: str = INK) -> VGroup:
    """Mono rows at the house pitch (masks and '…' GREY); a (text, colour) item keeps its colour."""
    rows = VGroup()
    for i, s in enumerate(lines):
        s, col = (s, color) if isinstance(s, str) else s
        ln = mono_line(s, size, col)
        grey_masks(ln)
        ln.shift(np.array([0, -i * PITCH, 0]) - ln.strut.get_corner(UP + LEFT))
        rows.add(ln)
    return rows


def hide_glyphs(rows):
    """Glyphs at opacity 0 (the struts are invisible already): rows written in later."""
    for r in rows:
        for g in r.glyphs:
            g.set_opacity(0)


def glyph_op(rows, k: float):
    """Animations: every glyph of `rows` to opacity k (never the struts)."""
    return [g.animate.set_opacity(k) for r in rows for g in r.glyphs]


def write_rows(rows, run_time: float = 1.2, lag: float = 0.35):
    """The rows appear one after the other (their glyphs fade in)."""
    return LaggedStart(*[AnimationGroup(*glyph_op([r], 1.0)) for r in rows], lag_ratio=lag,
                       run_time=run_time)


def pulse(m, color: str = TURN, k: float = 1.06, run_time: float = 0.7, width: float | None = None):
    a = m.animate(rate_func=there_and_back, run_time=run_time).scale(k)
    return a.set_stroke(color, width) if width else a.set_stroke(color)


def answer_card(title: str, rows_txt: list[str]) -> VGroup:
    """A BLUE answer card: header "answer A" above, the excerpt rows inside (hidden: written in
    later). .frame .rows .header"""
    rows = mono_rows(rows_txt)
    fr = box(CARD_W, rows.height + 0.4, CLOUD, fill=S.BG, fill_opacity=1.0, stroke=3, radius=0.12)
    gl = VGroup(*[g for r in rows for g in r.glyphs])
    rows.move_to(fr)
    rows.shift(RIGHT * (fr.get_left()[0] + 0.2 - gl.get_left()[0]))
    assert gl.get_right()[0] <= fr.get_right()[0] - 0.2, (title, gl.get_right()[0] - fr.get_right()[0])
    hd = sans(title, 22, CLOUD, weight="BOLD").next_to(fr, UP, buff=0.1).align_to(fr, LEFT).shift(RIGHT * 0.1)
    hide_glyphs(rows)
    g = VGroup(fr, rows, hd)
    g.frame, g.rows, g.header = fr, rows, hd
    return g


def even_chip(s: str, w: float, color: str = S.GREY, size: float = PT) -> VGroup:
    """A chip of a fixed width (a list of chips reads as a column)."""
    t = label(s, size, INK)
    h = mono("|", size).height + 0.2
    b = box(w, h, color, fill_opacity=0.08, radius=h / 2.6)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def rich(s: str, size: float, color: str = INK, lead: tuple | None = None):
    """One row of serif text with `code` spans in mono (backticks dropped); lead=(n, colour)
    colours the first n characters of the plain text."""
    parts = s.split("`")
    plain, spans = "", []
    for k, p in enumerate(parts):
        if k % 2:
            spans.append((len(plain), len(plain) + len(p)))
        plain += p
    t2c = {f"[0:{lead[0]}]": lead[1]} if lead else {}
    t = S.text(plain, size, color, t2f={f"[{a}:{b}]": MONO for a, b in spans}, t2c=t2c)
    t.plain = plain
    return t


# ------------------------------------------------------------------ the scene
class Hook(VoiceScene):
    def play(self, *anims, **kw):
        """Scene.play, then drop the wrapper groups an animation left on the scene (a LaggedStart's
        group, a substring's glyph group): their members are drawn by their owners, and a wrapper
        left behind would show them again after their owner's FadeOut."""
        super().play(*anims, **kw)
        self._prune()

    def _prune(self):
        for m in list(self.mobjects):
            others = set()
            for o in self.mobjects:
                if o is not m:
                    others.update(o.get_family())
            fam = [f for f in m.get_family() if f is not m]
            if fam and all(f in others for f in fam):
                self.remove(m)

    def outs(self, *groups, **kw):
        """FadeOuts for everything on the scene that belongs to `groups`: a group built piece by
        piece (its members FadeIn'd one by one) is not itself on the scene, so FadeOut(group) would
        leave its members there, to snap back after the fade."""
        fam = set()
        for g in groups:
            fam.update(g.get_family())
        return [FadeOut(m, **kw) for m in self.mobjects
                if m in fam or any(f in fam for f in m.get_family())]

    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0. the request, two answers
        rec = recorded_tag()
        place(rec, right=SAFE_X, top=3.55)
        ask_rows = mono_rows(ASK_ROWS)
        ask_fr = box(ask_rows.width + 0.7, ask_rows.height + 0.4, S.GREY, fill=S.BG, fill_opacity=1.0,
                     stroke=2.5, radius=0.12)
        ask_rows.move_to(ask_fr)
        ask_hd = note("Customer ask").next_to(ask_fr, UP, buff=0.1).align_to(ask_fr, LEFT).shift(RIGHT * 0.12)
        ask = VGroup(ask_fr, ask_rows, ask_hd)
        place(ask, cx=0, top=3.33)
        apart(ask_fr, rec, 0.05)
        phr = [substring(ask_rows[r], p) for r, p in PHRASES]

        chips = [chip(p, S.GREY, size=22) for _, p in PHRASES]
        chip_r1 = VGroup(*chips[:3]).arrange(RIGHT, buff=0.25)
        chip_r2 = VGroup(*chips[3:]).arrange(RIGHT, buff=0.25)
        chip_rows = VGroup(chip_r1, chip_r2).arrange(DOWN, buff=0.14)
        place(chip_rows, cx=0, top=ask_fr.get_bottom()[1] - 0.25)
        chips_up = 2.95 - chip_rows.get_top()[1]              # they rise into the card's place

        card_a = answer_card("answer A", A_ROWS)
        card_b = answer_card("answer B", B_ROWS)
        place(card_a, cx=-CX, top=HEAD_TOP_0)
        place(card_b, top=HEAD_TOP_0)
        card_b.shift(RIGHT * (CX - card_b.frame.get_center()[0]))
        card_a.shift(RIGHT * (-CX - card_a.frame.get_center()[0]))
        assert chip_rows.get_bottom()[1] + chips_up > HEAD_TOP_0 + 0.15
        same = chip("same model · same five tools · same request", CLOUD, size=PT)
        place(same, cx=0, top=card_a.frame.get_bottom()[1] - 0.22)
        inside_frame(rec, ask, chip_rows, card_a, card_b, same)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ask, shift=DOWN * 0.1), FadeIn(rec, shift=LEFT * 0.1), run_time=0.6)
            lit = None
            for k, a in enumerate(ANCHORS0):
                vo.wait_until(a)
                anims = [phr[k].animate.set_color(TURN), FadeIn(chips[k].box, shift=UP * 0.1),
                         Write(chips[k].text)]
                if lit is not None:
                    anims.append(phr[lit].animate.set_color(INK))
                self.play(*anims, run_time=0.6)
                lit = k
            self.wait(0.5)
            self.play(FadeOut(ask), run_time=0.5)
            self.play(chip_rows.animate.shift(UP * chips_up), run_time=0.7)
            vo.wait_until("Here are two answers")
            self.play(FadeIn(card_a, shift=UP * 0.3), FadeIn(card_b, shift=UP * 0.3), run_time=0.7)
            vo.wait_until("the same model")
            self.play(FadeIn(same, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 1. the two answers fill
        a_1050 = substring(card_a.rows[1], "1,050 g")
        a_5600 = substring(card_a.rows[3], "5,600¢")
        a_15000 = substring(card_a.rows[2], "15,000¢")
        b_bad = substring(card_b.rows[2], "1,5000¢")
        b_1200 = substring(card_b.rows[1], "1,200 g")
        red_ring = ring(b_bad, ERR, buff=0.07, stroke=4)
        grey_ul = under(a_15000, S.GREY, stroke=2.5, buff=0.06)

        with self.voiceover(SAY[1]) as vo:
            self.play(write_rows(card_a.rows, run_time=1.6))
            vo.wait_until("1,050 grams")
            self.play(Indicate(a_1050, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("5,600 cents")
            self.play(Indicate(a_5600, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("The second")
            self.play(write_rows(card_b.rows, run_time=1.4))
            vo.wait_until("within a budget with the comma")
            self.play(Create(red_ring), run_time=0.6)
            self.play(Create(grey_ul), run_time=0.5)
            vo.wait_until("a malformed number")
            self.play(b_bad.animate.set_color(ERR), pulse(red_ring, ERR, 1.15), run_time=0.7)
        card_b.add(red_ring)                                   # they move with their cards
        card_a.add(grey_ul)

        # ========================================================== 2. the question
        q_rows = VGroup(*[label(s, 28, TURN) for s in QUESTION]).arrange(DOWN, buff=0.2)
        place(q_rows, cx=0, top=same.get_bottom()[1] - 0.45)
        inside_frame(q_rows)
        dim_parts = [card_a.frame, card_a.header, card_b.frame, card_b.header, grey_ul]

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(same), *[m.animate.set_opacity(0.45) for m in dim_parts],
                      *glyph_op(list(card_a.rows) + list(card_b.rows), 0.45), run_time=0.6)
            self.play(Write(q_rows[0]), run_time=1.4)
            vo.wait_until("And what would")
            self.play(Write(q_rows[1]), pulse(red_ring, ERR, 1.25, run_time=1.0, width=6), run_time=1.0)
        self.wait(1.0)

        # ========================================================== 3. the second run printed more
        up3 = HEAD_TOP_3 - HEAD_TOP_0
        chk = output_box(CHECK_ROWS)
        chk.frame.set_stroke(HARNESS, 3)
        hide_glyphs(chk.rows)
        place(chk, top=card_b.frame.get_bottom()[1] + up3 - 0.18)
        chk.shift(RIGHT * (CX - chk.frame.get_center()[0]))
        inside_frame(chk)
        green_tick = check_mark(0.34, HARNESS)
        cap = label("checks the items · not the prose", 22, HARNESS)
        dtag = concept_tag("bare agent · no final cart check")

        with self.voiceover(SAY[3]) as vo:
            self.play(*self.outs(q_rows, chip_rows), *[m.animate.set_opacity(1) for m in dim_parts],
                      *glyph_op(list(card_a.rows) + list(card_b.rows), 1.0), run_time=0.5)
            self.play(card_a.animate.shift(UP * up3), card_b.animate.shift(UP * up3), run_time=0.7)
            # positions after the move
            green_tick.move_to([card_b.frame.get_left()[0] - 0.33, card_b.rows[1].strut.get_center()[1], 0])
            green_ul = under(b_1200, HARNESS, stroke=3, buff=0.06)     # on the moved glyphs
            place(dtag, left=card_a.frame.get_left()[0] + 0.1, top=card_a.frame.get_bottom()[1] - 0.2)
            place(cap, right=chk.frame.get_left()[0] - 0.3, cy=chk.rows[6].strut.get_center()[1])
            apart(dtag, cap, 0.2)
            apart(green_tick, card_a.frame, 0.05)
            apart(cap, card_a, 0.2)
            inside_frame(dtag, cap)
            self.play(FadeIn(chk), run_time=0.4)
            self.play(write_rows(chk.rows[:2], run_time=0.6))
            vo.wait_until("1,200 grams")
            self.play(write_rows(chk.rows[2:6], run_time=1.2, lag=0.3))
            vo.wait_until("shop rules satisfied")
            self.play(write_rows(chk.rows[6:7], run_time=0.5))
            vo.wait_until("no order placed")
            self.play(write_rows(chk.rows[7:], run_time=0.6))
            vo.wait_until("The cart was valid")
            self.play(FadeIn(green_tick, shift=DOWN * 0.25, scale=1.3), Create(green_ul), run_time=0.6)
            vo.wait_until("only the sentence was garbled")
            self.play(pulse(red_ring, ERR, 1.25, run_time=0.8, width=6), FadeIn(cap, shift=RIGHT * 0.1),
                      run_time=0.8)
            vo.wait_until("Nothing checked")
            self.play(FadeIn(dtag, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 4. V1: two columns
        tc = TwoColumns(width=V1_W, height=V1_H, gap=V1_GAP)
        tc.move_to([0, V1_Y, 0])
        left_col, right_col, stamp = tc.parts["left"], tc.parts["right"], tc.parts["human"]
        lr = lref("21")
        apart(tc, lr, 0.1)
        top_free = tc.cols["left"].title.get_bottom()[1] - 0.2
        b_shift = np.array([-CX - card_b.frame.get_center()[0], top_free - card_b.get_top()[1], 0])
        b_bottom = card_b.frame.get_bottom()[1] + b_shift[1]
        a_shift = np.array([0, (b_bottom - 0.2) - card_a.get_top()[1], 0])
        assert card_a.get_bottom()[1] + a_shift[1] >= tc.cols["left"].frame.get_bottom()[1] + 0.12
        chk_up = (tc.word_mobs.get_bottom()[1] - 0.2) - chk.get_top()[1]
        assert chk.get_bottom()[1] + chk_up >= stamp.get_top()[1] + 0.1
        assert chk.frame.get_left()[0] >= tc.cols["right"].frame.get_left()[0] + 0.1
        assert card_b.frame.get_bottom()[1] > chk.get_top()[1] + 0.05      # B's slide left clears the box
        assert card_b.frame.get_bottom()[1] + b_shift[1] > card_a.get_top()[1] + a_shift[1] + 0.1

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(dtag), FadeOut(cap), FadeOut(green_tick), FadeOut(green_ul),
                      Succession(FadeOut(rec, run_time=0.35), FadeIn(lr, run_time=0.35)), run_time=0.7)
            self.play(card_a.animate.shift(a_shift), run_time=0.7)
            # B slides left at its own height (above the box, clear of A), then drops into its slot
            self.play(card_b.animate.shift(RIGHT * b_shift[0]), run_time=0.7)
            self.play(card_b.animate.shift(UP * b_shift[1]), run_time=0.4)
            vo.wait_until("the model proposes")
            self.play(FadeIn(left_col), run_time=0.6)
            self.bring_to_front(card_a, card_b)
            vo.wait_until("the harness decides")
            self.play(FadeIn(right_col), chk.animate.shift(UP * chk_up), run_time=0.9)
            self.bring_to_front(chk)
            self.play(FadeIn(stamp), run_time=0.4)
            vo.wait_until("The harness is the code")
            self.play(pulse(right_col[0], HARNESS, 1.0, run_time=0.8, width=6),
                      Indicate(right_col[1], color=HARNESS, scale_factor=1.08), run_time=0.8)
            for i, a in enumerate(["the loop", "its limits", "its context", "and its checks"]):
                vo.wait_until(a)
                self.play(tc.write_word(i, run_time=0.45))
            vo.wait_until("Today we sort")
            self.play(pulse(left_col[0], CLOUD, 1.0, run_time=1.0, width=6),
                      pulse(right_col[0], HARNESS, 1.0, run_time=1.0, width=6), run_time=1.0)
        words = list(tc.word_mobs)

        # ========================================================== 5. the map: lecture and README
        band = TwoColumns(width=V1_W, height=1.1, gap=V1_GAP, words=False)
        band.move_to([0, BAND_Y, 0])
        lr3 = lref("3")
        apart(band, lr3, 0.05)
        cw_l = max(label(s, PT).width for s in OUTLINE) + 0.6
        cw_r = max(label(s, PT).width for s in ACTS) + 0.6
        left_chips = VGroup(*[even_chip(s, cw_l) for s in OUTLINE])
        right_chips = VGroup(*[even_chip(s, cw_r) for s in ACTS])
        row_pitch = 0.53
        for i, (lc, rc) in enumerate(zip(left_chips, right_chips)):
            lc.move_to([-2.9, -i * row_pitch, 0])
            rc.move_to([2.9, -i * row_pitch, 0])
        l_head = note("Lecture 7 · outline").next_to(left_chips, UP, buff=0.18).align_to(left_chips, LEFT)
        r_head = VGroup(mono("README.md", PT, S.GREY), label("· lines 13–21", PT, S.GREY)).arrange(RIGHT, buff=0.12)
        r_head.next_to(right_chips, UP, buff=0.18).align_to(right_chips, LEFT)
        links = VGroup(*[Line(lc.get_right() + RIGHT * 0.1, rc.get_left() + LEFT * 0.1, color=LOOKUP,
                              stroke_width=3) for lc, rc in zip(left_chips, right_chips)])
        mapg = VGroup(left_chips, right_chips, l_head, r_head, links)
        place(mapg, cx=0, top=band.get_bottom()[1] - 0.25)
        mock = excerpt_chip(MOCK, "README.md · line 27 (excerpt)", line=MOCK_LINE)
        place(mock, cx=0, bottom=-3.48)
        _i = MOCK.index("mock, in-memory")                    # the chip's text is one mono Text
        _a, _n = len(MOCK[:_i].replace(" ", "")), len("mock, in-memory".replace(" ", ""))
        mock_ul = under(VGroup(*mock.text[_a:_a + _n]), TURN, stroke=3, buff=0.05)
        apart(mapg, mock, 0.12)
        inside_frame(band, mapg, mock)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(card_a), FadeOut(card_b), FadeOut(chk), FadeOut(stamp),
                      *[FadeOut(w) for w in words],
                      Succession(FadeOut(lr, run_time=0.35), FadeIn(lr3, run_time=0.35)), run_time=0.7)
            self.play(ReplacementTransform(left_col, band.parts["left"]),
                      ReplacementTransform(right_col, band.parts["right"]), run_time=0.8)
            self.play(FadeIn(band.parts["human"]), FadeIn(l_head), FadeIn(r_head),
                      LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in left_chips], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(c, shift=LEFT * 0.1) for c in right_chips], lag_ratio=0.1),
                      run_time=1.0)
            vo.wait_until("in order")
            self.play(LaggedStart(*[Create(ln) for ln in links], lag_ratio=0.3), run_time=1.3)
            vo.wait_until("The tutorial runs six acts")
            self.play(*[c.box.animate.set_stroke(TURN, 3.5) for c in right_chips[:5]],
                      *[Indicate(c.text, color=TURN, scale_factor=1.1) for c in right_chips[:5]], run_time=0.8)
            vo.wait_until("in a fictional cheese shop")
            self.play(FadeIn(mock, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("where nothing is really bought")
            self.play(Create(mock_ul), run_time=0.6)
        band_parts = [band.parts["left"], band.parts["right"], band.parts["human"]]

        # ========================================================== 6. how to follow along
        tr = tracker("Start")
        halo = RoundedRectangle(width=tr.width + 0.16, height=tr.height + 0.14, corner_radius=0.1,
                                stroke_color=TURN, stroke_width=4).set_fill(opacity=0)
        place(halo, left=tr.get_left()[0] - 0.08, top=tr.get_top()[1] + 0.07)
        lr21 = lref("21")
        tr_cap = note("the README step").next_to(halo, DOWN, buff=0.12).align_to(tr, LEFT)
        lr_cap = note("the lecture slides")
        place(lr_cap, right=lr21.get_right()[0], top=lr21.get_bottom()[1] - 0.12)
        t = term(P_REPO, rows=2)
        # the prompt and the command fill the row to x 4.56: the ▶ tag (2.0 wide) cannot sit beside it,
        # so it goes on the title bar, right of "preview" (common.py notes: frame_tags for full rows)
        prev = frame_tags(t, your_turn(), preview_tag())
        turn_tag, prev_tag = prev[0], prev[1]
        inside_frame(halo, lr21, t, prev, tr_cap, lr_cap)

        with self.voiceover(SAY[6]) as vo:
            self.play(*self.outs(*band_parts, mapg, mock, mock_ul, lr3), run_time=0.6)
            self.play(FadeIn(tr, shift=DOWN * 0.15), Create(halo), FadeIn(tr_cap, shift=UP * 0.1), run_time=0.7)
            self.play(pulse(halo, TURN, 1.04, run_time=0.6, width=6))
            self.play(pulse(halo, TURN, 1.04, run_time=0.6, width=6))
            vo.wait_until("the gray tag, top right")
            self.play(FadeOut(halo), FadeIn(lr21), FadeIn(lr_cap, shift=UP * 0.1), run_time=0.5)
            self.play(lr21.box.animate(rate_func=there_and_back).set_stroke(TURN, 5), run_time=0.8)
            vo.wait_until("When a tag says your turn")
            self.play(FadeIn(t), FadeIn(prev_tag), run_time=0.5)
            type_cmd(self, t, CMD)
            self.play(FadeIn(turn_tag, shift=LEFT * 0.1), run_time=0.4)
        self.wait(2)

        # ========================================================== 7. one honest limit
        title = label("One honest limit", 26, INK)
        date = chip("recorded October 20, 2026", S.GREY, size=22)
        nokey = nokey_tag()
        head = VGroup(title, date, nokey).arrange(RIGHT, buff=0.35)
        glyphs = {"check": lambda: check_mark(0.32, HARNESS),
                  "cross": lambda: cross_mark(0.3, ERR, stroke=5),
                  "book": lambda: notebook_glyph(0.42, CLOUD, check=False)}
        rows7 = VGroup()
        y = 0.0
        for kind, lead, rest, col in LIMIT_ROWS:          # glyphs in one column, texts from one x
            txt = rich(f"{lead} {rest}", 22, INK, lead=(len(lead), col))
            place(txt, left=0.62, top=y)
            gl = glyphs[kind]()
            gl.move_to([0.22, txt.get_center()[1], 0])
            rows7.add(VGroup(gl, txt))
            y = txt.get_bottom()[1] - 0.34
        row3b = rich(LIMIT_ROW3B, 22, INK)
        r3 = rows7[2][1]
        k_rec = len("live answers:".replace(" ", ""))          # the glyph index of "recorded"
        place(row3b, top=r3.get_bottom()[1] - 0.14)
        row3b.align_to(r3[k_rec], LEFT)
        rows7[2].add(row3b)
        body = VGroup(head, rows7).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        card7 = box(body.width + 0.9, body.height + 0.8, S.GREY, fill_opacity=0.0, radius=0.14)  # outline: drawn
                                                                    # after its header, it must not cover it
        body.move_to(card7)
        place(VGroup(card7, body), cx=0, cy=0.0)
        inside_frame(card7)
        assert card7.width <= 12.9, card7.width

        with self.voiceover(SAY[7]) as vo:
            self.play(*self.outs(t, prev, tr, lr21, tr_cap, lr_cap), run_time=0.6)
            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("we recorded this on")
            self.play(FadeIn(date, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("without an OpenAI key")
            self.play(FadeIn(nokey, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Everything offline ran for real")
            self.play(Create(card7), FadeIn(rows7[0][0], scale=1.3), FadeIn(rows7[0][1], shift=RIGHT * 0.15),
                      run_time=0.8)
            vo.wait_until("live commands ran until")
            self.play(FadeIn(rows7[1][0], scale=1.3), FadeIn(rows7[1][1], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("Live answers come from")
            self.play(FadeIn(rows7[2][0], scale=1.3), FadeIn(VGroup(rows7[2][1], row3b), shift=RIGHT * 0.15),
                      run_time=0.6)
        honest = VGroup(card7, head, rows7)

        # ========================================================== 8. cost, masks, the guide
        cost_txt = label("the only cost: OpenAI tokens · no cloud project · no service account", 22, INK)
        g1 = VGroup(live_tag(), cost_txt).arrange(DOWN, buff=0.2)
        masks = VGroup(mask_chip(1, size=22), mask_chip(2, size=22)).arrange(RIGHT, buff=0.3)
        mask_txt = label("customer IDs masked on screen · your terminal and the README show them", 22, INK)
        g2 = VGroup(masks, mask_txt).arrange(DOWN, buff=0.2)
        footer = VGroup(label("every command:", 22, S.GREY), mono(GUIDE, 22, INK)).arrange(RIGHT, buff=0.2)
        stack = VGroup(g1, g2, footer).arrange(DOWN, buff=0.75)
        place(stack, cx=0, cy=0.0)
        inside_frame(stack)

        with self.voiceover(SAY[8]) as vo:
            self.play(*self.outs(honest), run_time=0.5)
            self.play(FadeIn(g1[0], shift=DOWN * 0.1), FadeIn(cost_txt), run_time=0.6)
            vo.wait_until("Customer IDs are masked")
            self.play(FadeIn(masks, shift=DOWN * 0.1), FadeIn(mask_txt), run_time=0.6)
            vo.wait_until("and every command is in the study guide")
            self.play(FadeIn(footer, shift=UP * 0.1), run_time=0.6)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
