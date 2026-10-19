"""S08 · Meaning as direction: embeddings (README "Embed" steps 1–2, two extras). Lecture: A24–A28,
A40–A47, B59–B60.

Beats (script.md "## S08", one voiceover block each):
 0  LECTURE A24–A28. TRACKER Embed (no step lit yet). Mini-map, "embedding" lit. V4: six GREEN chunk
    cards (curd, milk, whey … license) fly through the BLUE embedding box; the first comes out as
    a row of number cells that becomes a GREEN arrow in a 2-D drawing of a sphere, the others come
    out as arrows: the cheese cards cluster, the license cards sit elsewhere (tag our illustration,
    caption "a sketch of 3-D; each real vector has 256 numbers"). GREY chip "one vector per chunk ·
    a sentence embedding, not a word embedding" (in at "It turns each chunk into one vector").
 1  LECTURE A40–A43. Only the instructor's column of the lecture's Big Five table writes in (tag
    lecture example) and becomes a PINK arrow; the three candidates appear as GREEN arrows (tag
    sketch · not to scale: A 10° away and short, B 25° away and 1.4× longer, C 45° away); YELLOW
    angle arcs; a podium "cosine similarity": A 0.986 · B 0.976 · C 0.886, A's medal card gets a
    GREEN tick. A GREY caption "lecture game: who is most like the instructor?" (in at the question,
    beside the table; over the arrows once they are drawn; out when beat 2's measures table comes).
 2  LECTURE A44–A47. A second podium "dot product" (tag computed from the lecture's table · not on
    the slides): B's longer arrow pulses and the A and B medal cards swap (B 81.2 · A 80.2). A
    three-row table: cosine (the angle), Euclidean (the distance), dot product (angle and length);
    the cosine row is ringed YELLOW.
 3  cli.py · lines 22–27 (a 6-line panel: the mini-map hides); lines 24–26 highlight. A BLUE bar of
    3,072 cells (GREY labels "the model's full output · 3,072 numbers" and "length 1") is cut after
    256 cells, which turn GREEN ("output_dimensionality = 256", "length 1" becomes "length ≈ 0.4");
    beside it a BLUE arrow of length 1 in a dashed unit circle shrinks GREEN to ≈ 0.4.
 4  cli.py · lines 96–106 (line 105 wrapped). On the right a stack of GREEN chunk cards goes to the
    BLUE box in batches of 100, a GOLD tick per batch ("one paid call per batch"); chips cli.py ·
    lines 252–253 batch_size=100 and cli.py · lines 108–119 "on an API error: retry after 5, 10, 20,
    40, 80 s · then give up".
 5  LECTURE B59–B60. The panel leaves; the mini-map grows into V1; the shared BLUE box lights, the
    top lane pulses ("chunks · now"), then the bottom lane ("questions · later"); chip cli.py ·
    lines 75–84 generate_query_embedding "same model, same 256".
 6  TRACKER Embed 1. V1 shrinks back to the mini-map, which leaves as the TEAL terminal (13 rows)
    comes in; it types python cli.py --embed --chunk_type char-split -> cli-container/20 lines 2
    (cut), 3–6, …, 21–22, …, 73 (RED, wrapped); the "Processing file" line flashes YELLOW at "it
    reads the first book"; tag real run · no key on the title bar; GOLD tag on the command's prompt
    row "first Google call · your project pays".
 7  The terminal shrinks to a 4-row strip (the command's two rows and the error's two rows); a
    GREY "with your key, look for" card above it, four items writing in as named (cli.py lines
    240, 256, 259–260, 262–264).
 8  A second GREY card "if it fails (with your key)", rows writing in as named: the retry message
    (cli.py lines 117–118), key file not found (the strip's error rows flash), PERMISSION_DENIED
    ("fix GCP_PROJECT in docker-shell.sh, or the role in IAM (console)"), SERVICE_DISABLED.
 9  TRACKER Embed 2. The strip clears (step 1's error does not linger above the new command) and
    types python cli.py --embed --chunk_type recursive-split (no output).
    ▶ your turn on a GREY card listing both embed commands and "each run sleeps 5 s per book"; a
    two-row GOLD tag: ≈ 89 / ≈ 148 calls, cents by our estimate, check the current price list.
    Hold 2 s.
10  A card (tag recorded · the staff's vectors (68e0bde)): 68e0bde "the staff committed their
    outputs/" -> d9ced19 struck RED "reverted · merged in e17a39f" -> "still in every clone's
    history"; 58dd602 "their database removed too"; 22 files · 82 MB (recorded-embeddings/00 lines
    2–3, shown as "embeddings-* · 22 files · 82 MB"); GREEN check "their 22 chunk files = ours, byte
    for byte"; a GREY row along the card's foot "no key yet? the study guide shows how to copy these
    into outputs/" (in the pause after "history"). The strip's command flashes.
11  TRACKER Embed 2 · extra. GREY card "an extra Python check · in the study guide": "Tolminc's
    vectors: count, first five, lengths" (code not shown); the strip grows to 4 rows ->
    recorded-embeddings/06 lines 9–11 (tag recorded · the staff's vectors (68e0bde), just above the
    strip). Left, V4: the upper half of a dashed unit circle, 24 GREEN arrows (directions ours,
    lengths 0.369–0.402; tag our illustration), a ruler along the axis (0.4, 1)
    and a YELLOW dashed mark at ≈ 0.4 across the arrow tips ("lengths 0.369–0.402"); "length 1"
    at the circle.
12  The strip, card and ruler leave; the dashed circle and the short arrows stay, a PINK query arrow
    joins; one arrow stretches to length 1 and back; chip "hnsw:space": "cosine" (cli.py line 288)
    with a GREY note "the measure, set at load (next scene)". PONDER 8 s in the lower third ("Our
    database will compare by cosine (set when we load)." …).
13  The other arrows dim; the stretched arrow keeps its YELLOW angle arc to the query ("cosine:
    same"); a GREY "what if · straight-line distance" inset on the right (tag illustration): the RED
    distance to the query grows as the arrow stretches ("distance: changes"; "Chroma's default:
    L2", "dot product: changes too"); a GREY chip recalls the game. Fade to an empty frame.

Deviations from SHOW (see the scene report): cli-container/20 line 2 is cut with … instead of
wrapped and the terminal has 13 rows, so the typed command and its GOLD tag stay on screen (wrapped,
the 15 rows would scroll the command away); the strip of beats 7–10 has 4 rows, not 3, so the
wrapped error shows whole (3 rows left half a line of it); the mini-map also hides during the 6-line panel of
beat 3 (the "more than 5 lines" rule) and stays hidden from beat 6 on (terminals, cards above the
strip, the ponder card and the inset leave no free corner); beat 8's rows are ordered as the
narration names them (the retry message first); the dot-product podium's tag and the GOLD calls tag
are two-row tags (one row would cross the frame); the GOLD "first Google call" tag sits on the
prompt row (the command row, folded under the long container prompt, has no room for it); beats
11–13 draw only the upper half of the dashed unit circle (every arrow points up; the full circle
would run into the strip and the ponder card), at a size where 24 arrows of length 0.4 stay
distinct; a PINK query arrow joins V4 in beat 12, so that beat 13 has a query to measure the angle
and the distance against. QA 2026-10-19: beat 8's PERMISSION_DENIED row names where each fix lives
(SHOW's "or the role in docker-shell.sh" sent newcomers looking for a role in the script; the role
is granted in IAM, S03); beat 10's card gets the GREY "no key yet?" pointer to the study guide's copy
command (the command itself stays untyped, as BRIEF says); beat 1 shows the game's question, and
beat 12's chip note and ponder card say "database" and "set at load" (collection and HNSW come in
S09; script.md's PONDER line now says the same).
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    ShowPassingFlash,
    Succession,
    Transform,
    TransformFromCopy,
    VGroup,
    there_and_back,
)

from common import (
    CLOUD,
    COST,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MINI_CENTER,
    NARRATION,
    P_CTR,
    TURN,
    CellBar,
    LookFor,
    MiniMap,
    Prose,
    RagMap,
    VectorSketch,
    beside,
    bare_prompt,
    capture,
    caption_extra,
    check_card,
    check_mark,
    chunk_card,
    cost_tag,
    example_tag,
    excerpt,
    excerpt_chip,
    grey_tag,
    illustration_tag,
    lref,
    lref_swap,
    model_box,
    nokey_tag,
    note,
    our_illustration_tag,
    pin,
    ponder_at,
    resize,
    ring,
    src_panel,
    staff_tag,
    strike,
    strip_top,
    table_card,
    term,
    tracker,
    turn_card,
    type_cmd,
)
from explainer import style as S
from explainer.devops import CAPTION, MONO, TAG, box, chip, label, mono, substring
from explainer.scene import VoiceScene

SAY = NARRATION["S08"]

# ------------------------------------------------------------------ commands and real outputs
EMB = capture("20", "cli-container")
EMB_CMD = "python cli.py --embed --chunk_type char-split"            # README.md line 129
assert EMB.cmd == EMB_CMD and EMB.exit == 1
EMB_HEAD = EMB.at((2, 6))                         # line 2 (135 chars) is cut with … by the terminal
EMB_MID = EMB.at("…", (21, 22), "…")
EMB_ERR = EMB.line(73)
assert EMB.line(4) == "Number of files to process: 11"
assert EMB.line(21).startswith('  File "/app/cli.py", line 98, in generate_text_embeddings')
assert EMB_ERR.endswith("File /secrets/llm-service-account.json was not found.")
EMB2_CMD = "python cli.py --embed --chunk_type recursive-split"     # README.md line 130

STAFF = capture("00", "recorded-embeddings")
assert STAFF.exit == 0 and STAFF.line(2) == "22" and STAFF.line(3).split()[0] == "82M"
STAFF_SIZE = f"{STAFF.line(2)} files · {STAFF.line(3).split()[0][:-1]} MB"     # "22 files · 82 MB"

NORMS = capture("06", "recorded-embeddings")
NORMS_OUT = NORMS.at((9, 11))
assert NORMS.exit == 0 and NORMS_OUT[0] == "24 rows, 256 numbers each"
assert NORMS_OUT[2] == "vector lengths: min 0.369, max 0.402"
L_MIN, L_MAX = 0.369, 0.402

HNSW = '"hnsw:space": "cosine"'
assert HNSW in excerpt("cli.py", 288, 288)
BATCH = "batch_size=100"
assert BATCH in excerpt("cli.py", 253, 253)
assert "def generate_query_embedding(query):" in excerpt("cli.py", 75, 75)

# the lecture's personality game (A40–A43; SLIDES.md): the instructor's column, the three scores,
# and the dot products we computed from the table (81.2, 80.2: not on the slides)
TRAITS = [("extroversion", "4.8"), ("emotional stability", "4.5"), ("agreeableness", "4.2"),
          ("conscientiousness", "3.3"), ("imagination", "4.1")]
_I = np.array([4.8, 4.5, 4.2, 3.3, 4.1])
_A = np.array([3.3, 4.0, 4.1, 3.1, 4.6])
_B = np.array([4.8, 2.7, 4.9, 2.5, 4.2])
assert abs(float(_I @ _B) - 81.24) < 1e-9 and abs(float(_I @ _A) - 80.15) < 1e-9   # shown as 81.2, 80.2
COSINE = [("A", "0.986"), ("B", "0.976"), ("C", "0.886")]
DOT = {"A": "80.2", "B": "81.2"}

# "collection" and HNSW are introduced only in S09: the card says "database" and that the measure
# is set when we load, as SAY[12] does
PONDER_Q = ("Our database will compare by cosine (set when we load).\nThese vectors are shorter than 1, "
            "and not all the same length.\nDoes that change which chunks count as nearest?")

# ------------------------------------------------------------------ layout
TOPICS = ["curd", "milk", "license", "curd", "whey", "license"]         # beat 0's chunk cards
ANGLES0 = {0: (42, 0.86), 1: (55, 0.80), 2: (203, 0.84), 3: (48, 0.90), 4: (61, 0.82), 5: (216, 0.78)}
SPH_O = np.array([1.75, 0.35, 0])           # beat 0: the sphere's centre
BOX_X = -3.3                                # beat 0: the embedding box (room for "a list of numbers")
GAME_O = np.array([-6.0, -2.0, 0])           # beats 1–2: the 2-D sketch's origin
GAME_R = 3.4
INSTR = 8.0                                 # the instructor's direction (degrees)
CAND = {"A": (INSTR + 10, 0.60), "B": (INSTR + 25, 0.84), "C": (INSTR + 45, 0.72)}   # angle, length
V4_O = np.array([-3.25, -0.2, 0])            # beats 11–13: V4's origin (an upper half-circle above)
V4_R = 2.95
QUERY_DEG = 112.0
FAN = (10.0, 85.0)                          # beat 11's 24 directions (our illustration)


def mixed(parts, size: float = CAPTION, color: str = INK) -> VGroup:
    """One row of serif pieces and `mono` pieces (in backticks); (text, colour) for a colour."""
    mobs = []
    for p in parts:
        s, col = (p, color) if isinstance(p, str) else p
        if len(s) > 1 and s.startswith("`") and s.endswith("`"):
            mobs.append(mono(s[1:-1], size, col))
        else:
            mobs.append(label(s, size, col))
    return VGroup(*mobs).arrange(RIGHT, buff=0.1)


def perm_row() -> VGroup:
    """Beat 8's PERMISSION_DENIED row; its comma hugs `docker-shell.sh` (mixed() puts a gap before
    every piece)."""
    row = mixed(["`PERMISSION_DENIED`", "→ fix", "`GCP_PROJECT`", "in", "`docker-shell.sh`",
                 ", or the role in IAM (console)"])
    row[-1].shift(LEFT * 0.08)
    return row


def two_row_tag(rows, color: str = S.GREY) -> VGroup:
    """A tag of two left-aligned rows (a long tag that would cross the frame on one row)."""
    t = VGroup(*[label(s, TAG, color) for s in rows]).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    b = RoundedRectangle(width=t.width + 0.44, height=t.height + 0.24, corner_radius=0.18,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def topic_card(word: str) -> VGroup:
    """A GREEN chunk card labelled with its topic (cards are GREEN whatever book they come from)."""
    fr = RoundedRectangle(width=1.55, height=0.46, corner_radius=0.08, stroke_color=DATA,
                          stroke_width=2.5).set_fill(DATA, 0.14)
    return VGroup(fr, label(word, CAPTION, INK).move_to(fr))


def medal(name: str, score: str) -> VGroup:
    """A podium's medal card: the candidate's letter and the score. .frame .name .score"""
    nm = label(name, 26, INK)
    sc = mono(score, 22, INK)
    row = VGroup(nm, sc).arrange(RIGHT, buff=0.25)
    fr = box(1.68, 0.52, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.1).move_to(row)   # row ≤ 1.38 wide
    g = VGroup(fr, row)
    g.frame, g.name, g.score = fr, nm, sc
    return g


def podium(title: str, n: int, x0: float, base: float, heights=(0.6, 0.45, 0.32), w: float = 1.75,
           gap: float = 0.15) -> VGroup:
    """A small podium (rank 1 on the left, blocks numbered), its title above. .title .blocks
    .slots (where each rank's medal card sits)."""
    blocks, slots = VGroup(), []
    for k in range(n):
        h = heights[k]
        b = Rectangle(width=w, height=h, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.12)
        b.move_to([x0 + w / 2 + k * (w + gap), base + h / 2, 0])
        b.add(label(str(k + 1), CAPTION, S.GREY).move_to(b))
        blocks.add(b)
        slots.append(np.array([b.get_center()[0], base + h + 0.05 + 0.26, 0]))
    ttl = label(title, 24, INK)
    ttl.move_to([x0 + ttl.width / 2, base + max(heights) + 1.05, 0])
    g = VGroup(ttl, blocks)
    g.title, g.blocks, g.slots = ttl, blocks, slots
    return g


def place_origin(vs: VectorSketch, at) -> VectorSketch:
    return vs.shift(np.array(at) - vs.o.get_center())


def unit_dir(deg: float):
    return np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])


def thin_arrow(vs: VectorSketch, deg: float, length: float, color: str = DATA, stroke: float = 2.5) -> Arrow:
    """A V4 arrow with a small tip (24 of them side by side stay 24 arrows)."""
    return Arrow(vs.o.get_center(), vs.point(deg, length), buff=0, color=color, stroke_width=stroke,
                 tip_length=0.12, max_tip_length_to_length_ratio=0.2)


def half_circle(vs: VectorSketch, color: str = S.GREY):
    """The dashed unit circle's upper half (every arrow of beats 11–13 points up)."""
    return DashedVMobject(Arc(radius=vs.r(), start_angle=0, angle=PI, arc_center=vs.o.get_center()),
                          num_dashes=30, dashed_ratio=0.5).set_stroke(color, 2)


class Embeddings(VoiceScene):
    def construct(self):
        assert len(SAY) == 14, len(SAY)

        tr = tracker("Embed")
        mm = MiniMap(MINI_CENTER)

        # ========================================================== 0 · one chunk, one vector, one direction
        lr = lref("A24–A28")
        cards = VGroup(*[topic_card(w) for w in TOPICS]).arrange(DOWN, buff=0.14).move_to([-5.45, 0.15, 0])
        cards_lab = note("chunks", DATA).next_to(cards, UP, buff=0.18)
        emb = model_box("embedding\nmodel", w=1.5, h=2.8).move_to([BOX_X, 0.15, 0])
        vs = place_origin(VectorSketch(r=1.7), SPH_O)
        arrows0 = VGroup(*[vs.arrow(*ANGLES0[i]) for i in range(len(TOPICS))])
        cells = VGroup(*[Rectangle(width=0.17, height=0.26, stroke_color=DATA, stroke_width=2)
                         .set_fill(DATA, 0.45) for _ in range(8)]).arrange(RIGHT, buff=0)
        cells.move_to([(emb.get_right()[0] + vs.get_left()[0]) / 2, SPH_O[1], 0])
        cells_lab = note("a list of numbers").next_to(cells, DOWN, buff=0.14)
        cheese = VGroup(*[arrows0[i] for i in (0, 1, 3, 4)])
        lic = VGroup(*[arrows0[i] for i in (2, 5)])
        lab_cheese = label("curd · milk · whey", CAPTION, DATA)
        lab_cheese.move_to(vs.point(52, 1.0) + np.array([0.25 + lab_cheese.width / 2, 0.3, 0]))
        lab_lic = label("license text", CAPTION, DATA)
        lab_lic.move_to([vs.get_left()[0] - 0.05 - lab_lic.width / 2, vs.point(210, 0.84)[1] - 0.15, 0])
        cap0 = note("a sketch of 3-D; each real vector has 256 numbers").move_to([SPH_O[0], -1.72, 0])
        ill0 = our_illustration_tag().move_to([SPH_O[0] - 0.5, -2.22, 0])
        sent = chip("one vector per chunk · a sentence embedding, not a word embedding", S.GREY,
                    size=CAPTION)
        sent.move_to([-6.35 + sent.width / 2, -2.95, 0])

        def into_box(c):
            return c.animate.move_to(emb).scale(0.3).set_opacity(0)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), FadeIn(lr), FadeIn(mm), run_time=0.6)
            self.play(mm.light("embedding"), FadeIn(emb), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cards],
                                                                      lag_ratio=0.1), FadeIn(cards_lab), run_time=0.9)
            self.play(FadeIn(vs), run_time=0.5)
            vo.wait_until("It turns each chunk")
            # the chip says what the sentence says, and stays up long enough to be read
            self.play(into_box(cards[0]), FadeIn(sent, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("a list of numbers")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.12), FadeIn(cells_lab), run_time=0.5)
            self.wait(0.3)                         # the list of numbers holds before it becomes an arrow
            self.play(ReplacementTransform(cells, arrows0[0]), FadeOut(cells_lab), run_time=0.7)
            vo.wait_until("so similar meanings")
            self.play(LaggedStart(*[Succession(into_box(cards[i]), GrowArrow(arrows0[i]))
                                    for i in range(1, len(TOPICS))], lag_ratio=0.3), run_time=2.4)
            self.remove(*cards)
            self.play(FadeOut(cards_lab), run_time=0.3)
            vo.wait_until("in this sketch")
            self.play(FadeIn(cap0), FadeIn(ill0), run_time=0.5)
            vo.wait_until("curd near curd")
            self.play(FadeIn(lab_cheese, shift=LEFT * 0.1),
                      LaggedStart(*[Indicate(a, color=TURN, scale_factor=1.0) for a in cheese], lag_ratio=0.15),
                      run_time=0.8)
            vo.wait_until("license text elsewhere")
            self.play(FadeIn(lab_lic, shift=RIGHT * 0.1),
                      LaggedStart(*[Indicate(a, color=TURN, scale_factor=1.0) for a in lic], lag_ratio=0.2),
                      run_time=0.7)
        self.wait(0.3)

        # ========================================================== 1 · the personality game: cosine
        table = table_card(["Big Five score", "instructor"], [[t, v] for t, v in TRAITS],
                           header_colors=[S.GREY, LOOKUP])
        table.move_to([-6.35 + table.width / 2, 2.78 - table.height / 2, 0])
        values = VGroup(*[row[1] for row in table.cells])
        ex = example_tag()
        ex.move_to([table.get_right()[0] + 0.25 + ex.width / 2, table.get_top()[1] - 0.32, 0])
        gs = place_origin(VectorSketch(r=GAME_R, sphere=False), GAME_O)
        a_ins = gs.arrow(INSTR, 0.92, LOOKUP)
        l_ins = label("instructor", 24, LOOKUP).next_to(a_ins.get_end(), RIGHT, buff=0.12)
        a_c = {k: gs.arrow(d, ln, DATA) for k, (d, ln) in CAND.items()}
        l_c = {k: label(k, 26, INK).move_to(a_c[k].get_end() + unit_dir(CAND[k][0]) * 0.26) for k in CAND}
        arcs = {k: gs.arc(INSTR, CAND[k][0], radius=r) for k, r in (("A", 0.3), ("B", 0.42), ("C", 0.54))}
        sk_tag = grey_tag("sketch · not to scale")
        sk_tag.move_to([GAME_O[0] + sk_tag.width / 2, GAME_O[1] - 0.55, 0])
        pc = podium("cosine similarity", 3, x0=0.6, base=1.15)
        med_c = {k: medal(k, s).move_to(pc.slots[i]) for i, (k, s) in enumerate(COSINE)}
        tick = check_mark(0.3, DATA).next_to(med_c["A"], LEFT, buff=0.1)
        # the game's question: beside the table while it is asked, then over the arrows once the
        # table has become the instructor's arrow (it leaves when the measures table takes its place)
        game_q = note("lecture game: who is most like the instructor?")
        game_q.move_to([table.get_right()[0] + 0.35 + game_q.width / 2, 0.75, 0])
        game_q_over = game_q.copy().move_to([-6.35 + game_q.width / 2, 0.75, 0])
        assert game_q.get_right()[0] < 6.3 and game_q_over.get_right()[0] < pc.blocks.get_left()[0] - 0.2
        assert game_q_over.get_bottom()[1] > l_c["C"].get_top()[1] + 0.15

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(vs, arrows0, lab_cheese, lab_lic, cap0, ill0, sent, emb)), run_time=0.5)
            lr = lref_swap(self, lr, "A40–A43")
            self.play(FadeIn(table.frame), FadeIn(table.heads[0]), FadeIn(table.heads[1]), FadeIn(table[1]),
                      FadeIn(ex), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(VGroup(*row), shift=RIGHT * 0.1) for row in table.cells], lag_ratio=0.2),
                      run_time=1.2)
            vo.wait_until("which of three candidates")
            self.play(FadeIn(game_q, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Five scores make each person")
            # each value pulses about its own centre (a column-wide Indicate pushed 4.8 into the header)
            self.play(LaggedStart(*[Indicate(v, color=LOOKUP, scale_factor=1.15) for v in values], lag_ratio=0.1),
                      run_time=0.7)
            self.play(FadeIn(gs), ReplacementTransform(values, a_ins), Transform(table.heads[1], l_ins),
                      FadeOut(VGroup(table.frame, table[1], table.heads[0], *[row[0] for row in table.cells])),
                      FadeOut(ex), run_time=1.1)
            ex.move_to([pc.title.get_right()[0] + 0.3 + ex.width / 2, pc.title.get_center()[1], 0])
            self.play(LaggedStart(*[GrowArrow(a_c[k]) for k in "ABC"], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(l_c[k]) for k in "ABC"], lag_ratio=0.3), FadeIn(sk_tag),
                      game_q.animate.move_to(game_q_over), run_time=1.0)
            vo.wait_until("Cosine similarity compares only the angle")
            self.play(LaggedStart(*[Create(arcs[k]) for k in "ABC"], lag_ratio=0.35), run_time=1.0)
            vo.wait_until("and picks the first candidate")
            self.play(FadeIn(pc), FadeIn(ex), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(med_c[k], shift=DOWN * 0.15) for k in "ABC"], lag_ratio=0.2),
                      run_time=0.7)
            self.play(Create(tick), Indicate(arcs["A"], color=TURN, scale_factor=1.0), run_time=0.5)
        l_ins = table.heads[1]

        # ========================================================== 2 · the dot product picks B: a measure is a choice
        pd = podium("dot product", 2, x0=0.6, base=-0.75)
        med_d = {k: medal(k, DOT[k]).move_to(pd.slots[i]) for i, k in enumerate("AB")}
        dtag = two_row_tag(["computed from the lecture's table", "not on the slides"])
        dtag.move_to([pd.blocks.get_left()[0] + dtag.width / 2, pd.blocks.get_bottom()[1] - 0.2 - dtag.height / 2, 0])
        m_rows = [["cosine", "the angle"], ["Euclidean", "the distance"], ["dot product", "angle and length"]]
        usual = note("usual for text", TURN)
        # the "compares" column is wide enough for "the angle", the ring and "usual for text" inside the
        # frame (next to the ring, the note used to cross the frame's right edge)
        w_col0 = max(label(s, CAPTION).width for s in ["measure"] + [r[0] for r in m_rows]) + 0.4
        w_col1 = max(label(r[1], CAPTION).width for r in m_rows)
        w_col1 = max(w_col1, label("the angle", CAPTION).width + 0.1 + 0.2 + usual.width + 0.1) + 0.4
        measures = table_card(["measure", "compares"], m_rows, col_w=[w_col0, w_col1])
        measures.move_to([-6.35 + measures.width / 2, 2.78 - measures.height / 2, 0])
        cos_ring = ring(VGroup(*measures.cells[0]), TURN, buff=0.1)
        cos_ring.stretch_to_fit_height(VGroup(*measures.cells[0]).height + 0.1)   # clear of the header rule
        usual.next_to(cos_ring, RIGHT, buff=0.2)
        assert usual.get_right()[0] < measures.frame.get_right()[0] - 0.1
        assert measures.frame.get_right()[0] < 0.4             # clear of the podiums (x0 = 0.6)

        def flash(arrow, color=TURN):
            ln = Line(arrow.get_start(), arrow.get_end()).set_stroke(color, 10)
            return ShowPassingFlash(ln, time_width=0.6)

        with self.voiceover(SAY[2]) as vo:
            lr = lref_swap(self, lr, "A44–A47")
            # the cards' frames and letters copy down; the new scores write in (a digit-by-digit
            # morph of 0.986 into 80.2 reads as noise)
            self.play(FadeIn(pd), FadeIn(dtag),
                      *[TransformFromCopy(VGroup(med_c[k].frame, med_c[k].name), VGroup(med_d[k].frame, med_d[k].name))
                        for k in "AB"],
                      *[FadeIn(med_d[k].score, shift=DOWN * 0.1) for k in "AB"], run_time=0.9)
            for k in "AB":
                self.remove(med_d[k].frame, med_d[k].name, med_d[k].score)
                self.add(med_d[k])
            self.play(flash(a_c["A"], INK), flash(a_c["B"], INK), run_time=0.8)
            vo.wait_until("and would pick the second candidate")
            self.play(flash(a_c["B"]), run_time=0.7)
            self.play(med_d["A"].animate(path_arc=-PI / 3).move_to(pd.slots[1]),
                      med_d["B"].animate(path_arc=-PI / 3).move_to(pd.slots[0]), run_time=0.9)
            self.play(flash(a_c["B"]), Indicate(med_d["B"], color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("So a measure is a choice")
            self.play(FadeOut(game_q), run_time=0.3)       # first: it sits on the measures table's foot
            self.play(FadeIn(measures.frame), FadeIn(measures[1]), *[FadeIn(h) for h in measures.heads], run_time=0.4)
            self.play(LaggedStart(*[FadeIn(VGroup(*row), shift=RIGHT * 0.1) for row in measures.cells],
                                  lag_ratio=0.3), run_time=1.0)
            vo.wait_until("for text, cosine is the usual one")
            self.play(Create(cos_ring), FadeIn(usual), run_time=0.6)
        self.wait(0.3)

        # ========================================================== 3 · 3,072 numbers, the first 256 kept
        game = VGroup(gs, a_ins, l_ins, *a_c.values(), *l_c.values(), *arcs.values(), sk_tag, pc,
                      *med_c.values(), tick, ex, pd, *med_d.values(), dtag, measures, cos_ring, usual)
        p1 = src_panel("cli.py", 22, 27)
        p1.shift(np.array([-6.35 - p1.get_left()[0], 2.82 - p1.get_top()[1], 0]))
        bars1 = VGroup(*[p1.bar(n, TURN, 0.16) for n in (24, 25, 26)])
        model_name = p1.span(25, "gemini-embedding-001")
        dim256 = p1.span(26, "256")
        cb = CellBar(width=11.0, show=("bar",)).move_to([0, -1.25, 0])
        full_lab = note("the model's full output · 3,072 numbers").move_to(
            [cb.segs.get_left()[0], -0.78, 0], aligned_edge=LEFT)
        len_lab = note("length 1").move_to([cb.segs.get_right()[0], -0.78, 0], aligned_edge=RIGHT)
        keep_lab = mono("output_dimensionality = 256", CAPTION, DATA).move_to(
            [cb.segs.get_left()[0], -1.75, 0], aligned_edge=LEFT)
        us = place_origin(VectorSketch(r=1.15, sphere=False), [3.75, 0.9, 0])
        u_circ = us.unit_circle(1.0)
        a_full = us.arrow(35, 1.0, CLOUD)
        a_256 = us.arrow(35, 0.4, DATA)
        one = label("1", CAPTION, S.GREY).move_to(us.point(35, 1.0) + unit_dir(35) * 0.25)
        len04 = note("length ≈ 0.4").next_to(cb.segs[3], RIGHT, buff=0.25)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(game), FadeOut(lr), FadeOut(mm), run_time=0.6)
            self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(bars1), run_time=0.4)
            vo.wait_until("Gemini embedding 001")
            self.play(Indicate(model_name, color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("natively returns")
            self.play(LaggedStart(*[GrowFromEdge(s, LEFT) for s in cb.segs], lag_ratio=0.02), FadeIn(full_lab),
                      run_time=1.0)
            self.add(cb)
            self.play(FadeIn(len_lab), FadeIn(us), Create(u_circ), GrowArrow(a_full), FadeIn(one), run_time=0.8)
            vo.wait_until("the code asks for the first 256")
            self.play(Indicate(dim256, color=TURN, scale_factor=1.3), *cb.parts_in("keep"), run_time=0.7)
            self.play(*cb.cut(), Transform(a_full, a_256), FadeIn(keep_lab, shift=UP * 0.1),
                      ReplacementTransform(len_lab, len04), run_time=1.0)
            vo.wait_until("a prefix the model is trained")
            self.play(Indicate(cb.parts["keep"], color=TURN, scale_factor=1.15), run_time=0.9)
            self.play(flash(a_full), Indicate(keep_lab, color=TURN, scale_factor=1.05), run_time=1.1)

        # ========================================================== 4 · batches of 100, retries
        p2 = src_panel("cli.py", 96, 106, wrap=True)
        p2.shift(np.array([-6.4 - p2.get_left()[0], 2.85 - p2.get_top()[1], 0]))
        bar100 = p2.bar(100, TURN, 0.16)
        bar96 = p2.bar(96, TURN, 0.16)
        col_x = (p2.get_right()[0] + 6.5) / 2
        stack = VGroup(*[chunk_card(0.8, 0.42) for _ in range(4)])
        for k, c in enumerate(stack):
            c.move_to([col_x + 0.08 * k, 2.25 - 0.08 * k, 0])
        stack_lab = note("chunks", DATA).next_to(stack, UP, buff=0.12)
        box4 = model_box("embedding\nmodel", w=1.9, h=0.95).move_to([col_x, 0.35, 0])
        ticks = VGroup(*[check_mark(0.26, COST) for _ in range(3)]).arrange(RIGHT, buff=0.32)
        ticks.next_to(box4, DOWN, buff=0.28)
        calls = VGroup(note("one paid call", COST), note("per batch", COST)).arrange(DOWN, buff=0.08)
        calls.next_to(ticks, DOWN, buff=0.14)
        b_chip = excerpt_chip(BATCH, "cli.py · lines 252–253")
        b_chip.move_to([-6.35 + b_chip.width / 2, -3.0, 0])
        r_head = VGroup(mono("cli.py", CAPTION, S.GREY), label("· lines 108–119", CAPTION, S.GREY)).arrange(RIGHT, buff=0.12)
        r_chip = chip("on an API error: retry after 5, 10, 20, 40, 80 s · then give up", S.GREY, size=CAPTION)
        r_chip.move_to([b_chip.get_right()[0] + 0.45 + r_chip.width / 2, b_chip.chip.get_center()[1], 0])
        r_head.next_to(r_chip, UP, buff=0.08).align_to(r_chip, LEFT).shift(RIGHT * 0.08)
        retry = VGroup(r_chip, r_head)

        def batch():
            g = VGroup(*[chunk_card(0.8, 0.42) for _ in range(3)])
            for k, c in enumerate(g):
                c.move_to(stack[-1].get_center() + np.array([0.08 * (k - 1), -0.08 * (k - 1), 0]))
            n = mono("100", CAPTION, INK).next_to(g, LEFT, buff=0.12)
            return VGroup(g, n)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(p1, bars1, cb, full_lab, len04, keep_lab, us, u_circ, a_full, one)),
                      run_time=0.4)
            self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(stack), FadeIn(stack_lab), FadeIn(box4), FadeIn(bar100), run_time=0.5)
            self.play(FadeIn(b_chip, shift=UP * 0.1), run_time=0.4)
            for k in range(3):
                bt = batch()
                self.add(bt)
                self.play(bt.animate.move_to(box4).scale(0.4).set_opacity(0), run_time=0.45)
                self.remove(bt)
                self.play(Create(ticks[k]), Indicate(box4.frame, color=COST, scale_factor=1.04), run_time=0.3)
            self.play(FadeIn(calls), run_time=0.3)
            vo.wait_until("On an API error")
            self.play(FadeIn(retry, shift=UP * 0.1), FadeIn(bar96), run_time=0.5)
            vo.wait_until("doubling the wait")
            self.play(Indicate(r_chip.text, color=TURN, scale_factor=1.06), run_time=1.0)

        # ========================================================== 5 · the same model for the question, later
        lr = lref("B59–B60")
        mm_g = MiniMap(MINI_CENTER)
        mm_g.items["embedding"].set_stroke(TURN, 4)
        rm = RagMap(show=RagMap.TOP + RagMap.BOTTOM + tuple(n for n in RagMap.LABELS if n != "lab_question"))
        now = label("chunks · now", CAPTION, DATA).move_to([-3.85, 0.42, 0])
        later = label("questions · later", CAPTION, LOOKUP).move_to([-3.85, -0.8, 0])
        q_chip = excerpt_chip("generate_query_embedding", "cli.py · lines 75–84")
        same = label("same model, same 256", CAPTION, INK)
        q_all = VGroup(q_chip, same)
        same.next_to(q_chip.chip, RIGHT, buff=0.3)
        q_all.move_to([-6.35 + q_all.width / 2, -3.05, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(p2, bar100, bar96, stack, stack_lab, box4, ticks, calls, b_chip, retry)),
                      FadeIn(lr), run_time=0.45)
            self.play(FadeIn(mm_g), run_time=0.3)          # after the retry chip has gone from its corner
            body = VGroup(*[m for m in mm_g.submobjects if m is not mm_g.frame])
            self.play(FadeOut(mm_g.frame), body.animate.scale(4, about_point=MINI_CENTER).shift(-MINI_CENTER),
                      run_time=1.0)
            self.play(FadeIn(rm), FadeOut(body), run_time=0.4)
            self.play(rm.light("embedding"), FadeIn(q_all, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Chunks now")
            self.play(rm.pulse_lane("top", DATA), FadeIn(now, shift=RIGHT * 0.1), run_time=0.9)
            vo.wait_until("questions later")
            self.play(rm.pulse_lane("bottom", LOOKUP), FadeIn(later, shift=RIGHT * 0.1), run_time=0.9)
            vo.wait_until("one model")
            self.play(Indicate(rm.item("embedding"), color=TURN, scale_factor=1.05), run_time=0.7)

        # ========================================================== 6 · step 1: the first call to Google
        mm2 = MiniMap(MINI_CENTER)
        mm2.items["embedding"].set_stroke(TURN, 4)
        mm2.lit = "embedding"
        frame2 = mm2.frame
        mm2.remove(frame2)
        mm2.scale(4, about_point=MINI_CENTER).shift(-MINI_CENTER)
        t = term(P_CTR, rows=13, container=True)
        nk = nokey_tag()
        nk.move_to([t.box.get_right()[0] - 0.2 - nk.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])
        gold = cost_tag("first Google call · your project pays")

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(rm, now, later, q_all)), FadeOut(lr), FadeIn(mm2), tr.goto(1), run_time=0.5)
            self.play(mm2.animate.shift(MINI_CENTER).scale(0.25, about_point=MINI_CENTER), FadeIn(frame2),
                      run_time=0.7)
            self.play(FadeOut(VGroup(mm2, frame2)), FadeIn(t), run_time=0.4)
            cmd = type_cmd(self, t, EMB_CMD, type_time=1.4)
            assert hasattr(cmd, "rows") and len(cmd.rows) == 2
            vo.wait_until("the first call to Google")
            pin(self, cmd.rows[0], beside(gold, t, cmd.rows[0], buff=0.5), anim=FadeIn(gold, scale=1.15),
                run_time=0.5)
            vo.wait_until("On our machine")
            self.play(FadeIn(nk, shift=LEFT * 0.1), run_time=0.3)
            head = t.print(self, EMB_HEAD, run_time=0.7)
            assert len(head) == 5 and "Processing file" in EMB_HEAD[3]
            vo.wait_until("it reads the first book")
            self.play(Indicate(head[3], color=TURN, scale_factor=1.03), run_time=0.6)
            vo.wait_until("then stops at the missing key file")
            t.print(self, EMB_MID, run_time=0.4)
            err = t.print(self, [(EMB_ERR, ERR)], wrap=True, run_time=0.5)
            assert len(err) == 2
            self.play(Indicate(err, color=ERR, scale_factor=1.03), run_time=0.7)
            vo.wait_until("On yours, it runs")
            self.play(gold.animate(rate_func=there_and_back).scale(1.15), run_time=0.7)

        # ========================================================== 7 · with your key, look for
        lf = LookFor([("`Processing file: outputs/chunks-char-split-…`", "per book · cli.py · line 240"),
                      ("a 5-second pause", "cli.py · line 256"),
                      ("a second table with an embedding column", "cli.py · lines 259–260"),
                      (mixed(["`embeddings-char-split-*.jsonl`", "beside the chunks"]), "cli.py · lines 262–264")])
        # beats 7–10: a 4-row strip keeps the command (prompt row with its GOLD tag + command row)
        # and both rows of the wrapped error, so no half-line of the error is left on screen
        s4 = strip_top(4)
        lf.move_to([0, (s4 + 2.75) / 2, 0])

        with self.voiceover(SAY[7]) as vo:
            nk_y = s4 - t.bar_h / 2
            resize(self, t, 4, keep=[cmd.rows[0], cmd.rows[1], err[0], err[1]], run_time=0.7,
                   extra=[nk.animate.set_y(nk_y)])
            self.play(FadeIn(lf), run_time=0.4)
            self.play(lf.write_item(0))
            vo.wait_until("a 5-second pause")
            self.play(lf.write_item(1))
            vo.wait_until("a table with an embedding column")
            self.play(lf.write_item(2))
            vo.wait_until("and new embeddings files")
            self.play(lf.write_item(3))

        # ========================================================== 8 · if it fails (with your key)
        def item(first, second):
            g = VGroup(first, second).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            second.shift(RIGHT * 0.3)
            return g

        rows8 = [
            item(mixed(["`API error (code: 403) … Retrying in 5 seconds (attempt 1/5)`"]),
                 mixed(["→ the message names the cause · gives up after 5 tries, ≈ 2.5 min",
                        ("· cli.py · lines 117–118", S.GREY)])),
            item(mixed(["`File /secrets/llm-service-account.json was not found`"]),
                 mixed(["→ not in", "`../secrets`", "under that name · check:", "`ls -la /secrets`",
                        "in the container"])),
            # the Project ID is set in docker-shell.sh, the role in IAM (S03's console path): one row
            # that put both "in docker-shell.sh" sent newcomers looking for a role in the script
            item(perm_row(),
                 mixed(["then", "`exit`", "and", "`sh docker-shell.sh`", "again"])),
            mixed(["`SERVICE_DISABLED`", "→ enable the Vertex AI API, wait a minute, rerun"]),
        ]
        rows8[0][0][0].set_color(ERR)
        rows8[1][0][0].set_color(ERR)
        rows8[2][0][0].set_color(ERR)
        rows8[3][0].set_color(ERR)
        fails = VGroup(*rows8).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        f_frame = box(fails.width + 0.6, fails.height + 0.44, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
        fails.move_to(f_frame).align_to(f_frame, LEFT).shift(RIGHT * 0.3)
        f_head = note("if it fails (with your key)").next_to(f_frame, UP, buff=0.08).align_to(f_frame, LEFT)
        f_head.shift(RIGHT * 0.12)
        fcard = VGroup(f_frame, f_head, fails)
        fcard.move_to([0, 0, 0]).shift(UP * (s4 + 0.22 - f_frame.get_bottom()[1]))
        assert fcard.get_top()[1] < 2.72, fcard.get_top()[1]            # clear of the tracker
        again = rows8[2][1]
        err_rows = VGroup(err[0], err[1])

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(lf), FadeIn(f_frame), FadeIn(f_head), run_time=0.5)
            vo.wait_until("or keeps retrying")
            self.play(FadeIn(rows8[0], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("Key file not found")
            self.play(FadeIn(rows8[1], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(err_rows, color=ERR, scale_factor=1.03), Indicate(rows8[1][0], color=ERR, scale_factor=1.04),
                      run_time=0.8)
            vo.wait_until("Permission denied")
            self.play(FadeIn(rows8[2], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("then exit and start the script again")
            self.play(Indicate(again, color=TURN, scale_factor=1.05), run_time=0.9)
            vo.wait_until("Service disabled")
            self.play(FadeIn(rows8[3], shift=RIGHT * 0.15), run_time=0.5)

        # ========================================================== 9 · step 2, your turn, the calls
        tc = turn_card([EMB_CMD, EMB2_CMD, (Prose("each run sleeps 5 s per book · cli.py · line 256"), S.GREY)])
        calls_tag = two_row_tag(["≈ 89 calls (char-split) · ≈ 148 calls (recursive-split)",
                                 "cents, by our estimate · check the current price list"], COST)
        calls_tag.move_to([0, s4 + 0.25 + calls_tag.height / 2, 0])
        tc.move_to([0, 0, 0]).shift(UP * (calls_tag.get_top()[1] + 0.25 - tc.frame.get_bottom()[1]))
        assert tc.get_top()[1] < 2.72, tc.get_top()[1]

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(fcard), FadeOut(nk), tr.goto(2), run_time=0.5)
            # the strip clears first: step 1's missing-key error (and its GOLD tag) must not sit
            # above step 2's command through the ▶ hold
            t.clear(self, run_time=0.3)
            cmd2 = type_cmd(self, t, EMB2_CMD, type_time=1.4)
            assert hasattr(cmd2, "rows") and len(cmd2.rows) == 2
            vo.wait_until("Pause and run both")
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("about 89 and 148 calls")
            self.play(FadeIn(calls_tag, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Check the current price list")
            self.play(Indicate(calls_tag.text[1], color=COST, scale_factor=1.06), run_time=0.8)
        self.wait(2)                                   # ▶ beat: hold the frame

        # ========================================================== 10 · the staff's vectors
        c1 = VGroup(chip("68e0bde", S.GREY, size=22, font=MONO),
                    mixed(["the staff committed their", "`outputs/`"])).arrange(RIGHT, buff=0.25)
        c2_chip = chip("d9ced19", ERR, size=22, font=MONO)
        c2_strike = strike(c2_chip.text)
        c2 = VGroup(VGroup(c2_chip, c2_strike), mixed(["reverted · merged in", "`e17a39f`"])).arrange(RIGHT, buff=0.25)
        c3 = note("still in every clone's history")
        left = VGroup(c1, c2, c3).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        c3.shift(RIGHT * 0.12)
        db_chip = VGroup(chip("58dd602", S.GREY, size=CAPTION, font=MONO),
                         note("their database removed too")).arrange(RIGHT, buff=0.2)
        size_lab = mixed(["`embeddings-*`", "· " + STAFF_SIZE], size=24)
        same_files = VGroup(check_mark(0.3, DATA), label("their 22 chunk files = ours, byte for byte", CAPTION, INK))
        same_files.arrange(RIGHT, buff=0.2)
        right = VGroup(db_chip, size_lab, same_files).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        content = VGroup(left, right).arrange(RIGHT, buff=0.6, aligned_edge=UP)
        # the command that copies them stays untyped (BRIEF); a viewer without a key gets a pointer
        # to it (study guide, §4 Step 6 "No key yet?", recorded-embeddings/00)
        no_key = mixed(["no key yet? the study guide shows how to copy these into", "`outputs/`"], color=S.GREY)
        no_key.next_to(content, DOWN, buff=0.32, aligned_edge=LEFT)
        body = VGroup(content, no_key)
        d1 = Arrow(c1[0].get_bottom(), c2[0].get_top(), buff=0.06, color=S.GREY, stroke_width=3, tip_length=0.12)
        d2 = Arrow(c2[0].get_bottom(), [c2[0].get_center()[0], c3.get_top()[1], 0], buff=0.06, color=S.GREY,
                   stroke_width=3, tip_length=0.12)
        s_frame = box(body.width + 0.5, body.height + 0.6, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
        s_card = VGroup(s_frame, body, d1, d2)
        s_frame.move_to(body)
        s_card.move_to([0, (s4 + 2.75) / 2, 0])
        assert s_frame.get_top()[1] < 2.72 and s_frame.get_bottom()[1] > s4 + 0.15, (
            s_frame.get_top()[1], s_frame.get_bottom()[1])          # clear of the tracker and the strip
        stf = staff_tag()
        stf.move_to(s_frame.get_corner(UP + RIGHT) + np.array([-0.3 - stf.width / 2, 0, 0]))

        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(tc, calls_tag)), run_time=0.4)
            self.play(FadeIn(s_frame), FadeIn(stf), run_time=0.5)
            vo.wait_until("once committed")
            self.play(FadeIn(c1, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("and still in every clone's history")
            self.play(GrowArrow(d1), FadeIn(c2_chip), FadeIn(c2[1]), run_time=0.5)
            self.play(Create(c2_strike), run_time=0.3)
            self.play(GrowArrow(d2), FadeIn(c3, shift=DOWN * 0.1), FadeIn(db_chip, shift=LEFT * 0.1), run_time=0.6)
            self.play(FadeIn(no_key, shift=UP * 0.1), run_time=0.5)     # in the pause after "history"
            vo.wait_until("Their chunk files match ours")
            self.play(FadeIn(size_lab), run_time=0.4)
            self.play(Create(same_files[0]), FadeIn(same_files[1], shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("so their vectors are what")
            self.play(Indicate(VGroup(*cmd2.rows), color=TURN, scale_factor=1.04), run_time=0.9)

        # ========================================================== 11 · an extra check: 24 vectors, lengths 0.369–0.402
        ck = check_card("Tolminc's vectors: count, first five, lengths")
        ck.move_to([3.45, 1.55, 0])
        v4 = place_origin(VectorSketch(r=V4_R, sphere=False), V4_O)
        circ = half_circle(v4)
        rng = np.random.default_rng(8)
        lengths = np.linspace(L_MIN, L_MAX, 24)
        rng.shuffle(lengths)
        degs = np.linspace(FAN[0], FAN[1], 24) + rng.uniform(-0.8, 0.8, 24)
        fan = VGroup(*[thin_arrow(v4, float(d), float(ln)) for d, ln in zip(degs, lengths)])
        k_pick = int(np.argmax(degs))
        ruler = VGroup(Line(v4.point(0, 0), v4.point(0, 1.0), color=S.GREY, stroke_width=2.5))
        for k in range(6):
            p = v4.point(0, k / 5)
            ruler.add(Line(p + DOWN * 0.07, p + UP * (0.07 if k % 5 else 0.12), color=S.GREY, stroke_width=2.5))
        r04 = label("0.4", CAPTION, S.GREY).next_to(v4.point(0, 0.4), DOWN, buff=0.14)
        r1 = label("1", CAPTION, S.GREY).next_to(v4.point(0, 1.0), DOWN, buff=0.14)
        mark04 = DashedVMobject(v4.arc(FAN[0] - 5, FAN[1] + 5, radius=(L_MIN + L_MAX) / 2, color=TURN, stroke=3),
                                num_dashes=14)
        rng_lab = VGroup(label("lengths", CAPTION, TURN), label("0.369–0.402", CAPTION, TURN))
        rng_lab.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        rng_lab.move_to(v4.point(26, 0.52) + RIGHT * rng_lab.width / 2)
        len1 = note("length 1").move_to(v4.point(128, 0.78))
        # the 24 lengths are spread over the measured range; their directions are ours
        fan_tag = our_illustration_tag()
        fan_tag.move_to([-1.2 + fan_tag.width / 2, 2.5, 0])                 # outside the circle, top right
        assert fan_tag.get_right()[0] < 2.0 and np.linalg.norm(
            fan_tag.get_corner(DOWN + LEFT) - v4.o.get_center()) > v4.r() + 0.15
        n_strip = 4
        st = staff_tag()
        st.move_to([6.3 - st.width / 2, strip_top(n_strip) + 0.12 + st.height / 2, 0])

        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(VGroup(s_card, stf)), caption_extra(tr, True), run_time=0.5)
            self.play(FadeIn(ck, shift=UP * 0.1), run_time=0.5)
            t.clear(self, run_time=0.25)
            if t.rows != n_strip:
                resize(self, t, n_strip, run_time=0.5)
            out = t.print(self, NORMS_OUT, run_time=0.6)
            bare_prompt(self, t)
            self.play(FadeIn(st), FadeIn(v4), Create(circ), FadeIn(fan_tag), run_time=0.6)
            # ANCHORS: "24 rows" and "Their lengths" start sentences, so Kokoro's marks for them are exact.
            vo.wait_until("24 rows")                   # 2.65 s; "24" sounds at 2.68 s (the plays above end at 2.47 s)
            self.play(substring(out[0], "24 rows").animate.set_color(TURN),
                      substring(out[0], "256 numbers").animate.set_color(TURN),
                      LaggedStart(*[GrowArrow(a) for a in fan], lag_ratio=0.06), run_time=1.4)
            vo.wait_until("Their lengths")             # 6.10 s; "Their" sounds at 6.18 s
            self.play(substring(out[2], "min 0.369, max 0.402").animate.set_color(TURN),
                      Create(ruler), FadeIn(r04), FadeIn(r1), run_time=0.7)
            self.play(Create(mark04), FadeIn(rng_lab, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("not 1")                     # 11.20 s (interpolated); "not" sounds at 11.33 s
            self.play(Indicate(circ, color=INK, scale_factor=1.02), Indicate(r1, color=INK), FadeIn(len1),
                      run_time=0.7)

        # ========================================================== 12 · ponder: does length matter?
        a_q = v4.arrow(QUERY_DEG, (L_MIN + L_MAX) / 2, LOOKUP, stroke=4)
        l_q = label("query", CAPTION, LOOKUP).next_to(a_q.get_end(), LEFT, buff=0.12)
        hn = excerpt_chip(HNSW, "cli.py · line 288 (excerpt)", line=excerpt("cli.py", 288, 288))
        hn.move_to([3.45, 1.55, 0])
        # the chip's line runs at load time (S09), not yet: a note says so
        hn_note = note("the measure, set at load (next scene)").next_to(hn.chip, DOWN, buff=0.12)
        hn_note.align_to(hn.chip, LEFT).shift(RIGHT * 0.08)
        assert hn_note.get_right()[0] < 6.3
        picked = fan[k_pick]
        d_pick, l_pick = float(degs[k_pick]), float(lengths[k_pick])
        long_ = thin_arrow(v4, d_pick, 1.0, stroke=4)
        short_ = thin_arrow(v4, d_pick, l_pick, stroke=4)

        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(VGroup(t, st, ck, ruler, r04, r1, mark04, rng_lab)), caption_extra(tr, False),
                      run_time=0.5)
            self.play(FadeIn(hn, shift=UP * 0.1), FadeIn(hn_note, shift=UP * 0.1), GrowArrow(a_q), FadeIn(l_q),
                      run_time=0.6)
            self.play(Indicate(hn.text, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("and these arrows are shorter than 1")
            self.play(Transform(picked, long_), run_time=0.8)
            self.play(Transform(picked, short_), run_time=0.8)
            vo.wait_until("Does that change")
            self.play(LaggedStart(*[Indicate(a, color=TURN, scale_factor=1.0) for a in fan], lag_ratio=0.03),
                      run_time=1.0)
        card = ponder_at(self, PONDER_Q, 8)

        # ========================================================== 13 · no: cosine sees only the angle
        others = VGroup(*[a for i, a in enumerate(fan) if i != k_pick])
        arc = v4.arc(d_pick, QUERY_DEG, radius=0.25)
        same_lab = label("cosine: same", CAPTION, TURN)
        same_lab.move_to(v4.point(QUERY_DEG, 0.25) + np.array([-0.3 - same_lab.width / 2, -0.1, 0]))
        ins = box(5.9, 4.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.16).move_to([3.45, 0.35, 0])
        ins_t = grey_tag("what if · straight-line distance")
        ins_t.move_to(ins.get_corner(UP + LEFT) + np.array([0.3 + ins_t.width / 2, 0, 0]))
        ins_i = illustration_tag()
        ins_i.move_to(ins.get_corner(DOWN + RIGHT) + np.array([-0.3 - ins_i.width / 2, 0, 0]))
        w = place_origin(VectorSketch(r=3.0, sphere=False), [2.4, -1.45, 0])
        w_circ = DashedVMobject(w.arc(65, 125, radius=1.0, color=S.GREY, stroke=2), num_dashes=16)
        wq = w.arrow(QUERY_DEG, (L_MIN + L_MAX) / 2, LOOKUP, stroke=4)
        wc = thin_arrow(w, d_pick, l_pick, stroke=4)
        wc_long = thin_arrow(w, d_pick, 1.0, stroke=4)
        dist = Line(wq.get_end(), wc.get_end(), color=ERR, stroke_width=5)
        dist_long = Line(wq.get_end(), wc_long.get_end(), color=ERR, stroke_width=5)
        d_lab = label("distance: changes", CAPTION, ERR)
        d_lab.move_to([w.point(d_pick, 0.6)[0] + 0.3 + d_lab.width / 2, dist_long.get_center()[1] - 0.15, 0])
        n_l2 = note("Chroma's default: L2")
        n_dot = note("dot product: changes too")
        VGroup(n_l2, n_dot).arrange(DOWN, aligned_edge=RIGHT, buff=0.16).move_to(
            [ins.get_right()[0] - 0.3, 1.88, 0], aligned_edge=RIGHT)
        game_chip = chip("the game: cosine picks A · the dot product picks B", S.GREY, size=CAPTION)
        game_chip.move_to([-0.6, -2.75, 0])

        with self.voiceover(SAY[13]) as vo:
            self.play(FadeOut(card), FadeOut(hn), FadeOut(hn_note), others.animate.set_opacity(0.25),
                      fan_tag.animate.move_to([v4.point(180, 1.0)[0] + fan_tag.width / 2, V4_O[1] - 0.45, 0]),
                      run_time=0.5)                       # the inset needs the top right; the card has gone
            self.play(Create(arc), FadeIn(same_lab), run_time=0.6)
            self.play(Transform(picked, long_), run_time=0.9)
            self.play(Indicate(arc, color=TURN, scale_factor=1.0), Indicate(same_lab, color=TURN, scale_factor=1.1),
                      run_time=0.6)
            vo.wait_until("With straight-line distance")
            self.play(FadeIn(ins), FadeIn(ins_t), FadeIn(ins_i), FadeIn(w), Create(w_circ),
                      GrowArrow(wq), GrowArrow(wc), run_time=0.7)
            self.play(Create(dist), run_time=0.4)
            self.play(Transform(wc, wc_long), Transform(dist, dist_long), run_time=1.0)
            self.play(FadeIn(d_lab, shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("Chroma's default")
            self.play(FadeIn(n_l2), run_time=0.4)
            vo.wait_until("or a dot product")
            self.play(FadeIn(n_dot), run_time=0.4)
            vo.wait_until("length would leak")
            self.play(Indicate(dist, color=ERR, scale_factor=1.08), Indicate(d_lab, color=ERR, scale_factor=1.08),
                      run_time=0.8)
            vo.wait_until("the game's lesson")
            self.play(FadeIn(game_chip, shift=UP * 0.1), run_time=0.5)
        self.wait(1.5)                                 # time to read the game chip before the fade
        self.play(FadeOut(VGroup(tr, v4, circ, fan, fan_tag, a_q, l_q, len1, arc, same_lab, ins, ins_t, ins_i, w,
                                 w_circ, wq, wc, dist, d_lab, n_l2, n_dot, game_chip)), run_time=0.8)
        self.wait(0.3)
