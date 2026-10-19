"""S14 · Semantic chunking: cut where meaning shifts (README "Semantic Chunking"). Lecture: B13–B34.

Beats (script.md "## S14", one voiceover block each):
 0  LECTURE B19–B33. TRACKER Semantic (no step lit yet). The mini-map, "chunking" lit. Small, at
    the upper left (tag `lecture example`): six numbered sentence tiles; GREY dashed candidate
    cuts in every gap (where to cut?); an anchor under tile 1; the similarity 0.89 rises over gap
    1–2 and a GREEN group joins tiles 1–2; the anchor moves to tile 3, 0.85 and 0.68 rise; the
    YELLOW threshold line 0.8 draws; the group grows to tiles 1–3 = "chunk 1", the 0.68 bar grays
    out, and of the candidates only the one between tiles 3 and 4 stays, as the YELLOW cut.
 1  The walk shrinks into three GREEN ticks: "split at . ? !", "one neighbor each side", "cosine".
    V8 full width (the mini-map leaves): a GREEN block of text splits into seven numbered sentence
    tiles of the story (first three words) beside the regex chip `semantic_splitter.py · line 118`
    (excerpt); tile 74 zooms to its full sentence and back; a ±1 bracket sits on tile 74's window;
    the BLUE embedding band appears and every three-tile window, as the bracket slides tile to
    tile, peels off, drops through the band and becomes a GREEN arrow under its tile (a GOLD coin
    for the batch of 50, chip `semantic_splitter.py · line 206` (excerpt)).
 2  The regex chip and the bracket leave. Arrows 74 and 75 pair up: a copy of 75 slides onto 74,
    the PINK arc between them flies up and becomes the spike over their gap; the spikes and the
    curve build left to right (tag `our illustration`).
 3  CODE(semantic_splitter.py: 91–96) along the bottom (arrows, band and chips leave), line 92 lit;
    the YELLOW 95th-percentile line rises. The panel becomes CODE(semantic_splitter.py: 239–243),
    line 242 lit: the spike above the line flashes, the tiles part there (YELLOW cut), the bump
    below the line stays; at "So the biggest 5 percent" the cut and its spike flash, and at
    "become chunk boundaries" GREEN outlines show two chunks of very different lengths.
 4  The panel, the lecture tag and the spikes leave; the tiles move up. Two small cards:
    "char-split · --chunk · no key: ✓" (GREEN) and "semantic-split · --chunk · no key: ?"
    (YELLOW). PONDER(8 s) in the lower third.
 5  The "?" becomes a RED cross; the bracket returns on tile 74, its window drops into the BLUE
    embedding box; bracket and box flash, the cut and the chunk outlines dim, GREY note "every
    window is embedded before a single cut". Then CODE(cli.py: 207–215, at 20 pt) with line 210 lit and
    `generate_text_embeddings` underlined; a BLUE embedding-box glyph and a GOLD tag "a Google call"
    above the panel's right end; GREY note "embed() calls it too · cli.py · lines 249, 252".
 6  TRACKER Semantic 1. Terminal (12 rows, TEAL): the README command folds onto two rows →
    TERM(cli-container/60: 2–5, …, 11, 14, 17, 20, 23, …, 75; wrap), "chunk=True, embed=True,
    load=True" underlined, tag `real run · no key` in the title bar; line 75 RED; the five File frames
    light in a PINK chain (cli.py 212 → splitter 275 → 229 → 206 → cli.py 98); the book underlined;
    GREY chip "nothing saved" (cli-container/61: its command and line 2, `0`).
 7  The terminal shrinks to the strip (the command and line 75's end from "File": "…File
    /secrets/llm-service-account.json was not found."). GOLD tags write in at the
    top ("≈ 528 embedding calls just to chunk the corpus", "≈ 90 more to embed the chunks",
    "10–20 min", GREY tag "our estimate"); the GREY tip card (try one book first: move the others
    out of `input-datasets/books` / then put them back and run the command again). At "Look for"
    the tip leaves, the GOLD tags move down above the strip and the "with your key, look for" card
    writes in (three items, cli.py lines 215, 240, 161) with the GREY 429 note under it.
 8  The cards leave. Seven GREEN bars of very uneven length, one per chunk (tag `our
    illustration`, no numbers: no run saved a semantic chunk); the longest and the shortest flash;
    GREY note "a single-topic book still gets its top 5 % cut"; the ▶ your-turn card: the README
    command (header "your turn · with your key"), the GREY 429 row under it (it stays through the
    hold and the viewer's pause), and the extra chat command after the load. Hold 2 s, then
    everything fades: empty frame.

Deviations from SHOW (see the scene report): the V8 row shows 7 tiles (sentences 73–79, row 12.7
wide), not 9: three words of a sentence at 20 pt need two rows in a tile 1.68 wide (the scene
re-lays each tile's words on two rows; Seismograph puts one row), and tiles that cannot hold three
words show two. The window chosen holds the chapter-five spike above the line and a bump below
it. CODE(cli.py: 207–215) is set at 20 pt: lines 212 and 214 are 70 and 67 characters, too wide
for a 22 pt panel, and wrapping them would change the header the SHOW gives. The walk shrinks
into its three ticks at the start of beat 1, where the SAY says "the same ingredients". The
mini-map leaves when V8 takes the full width (its band and arrows need the bottom of the frame).
The GOLD "tick per batch of 50" is a GOLD coin. Beat 4 moves the tile row up and hides the spikes
so the two cards fit above the ponder card. Beat 7's GOLD tags move down above the strip while the
"look for" card takes the top (all three groups would not fit otherwise); the tip card leaves
then. Beat 8's bars are illustrative lengths (CHUNK_CHARS), not a measurement: no capture holds a
semantic chunk (cli-container/60 fails before one is saved), and the story under this
illustration's distances cuts only at its chapter headings, which gives chunks within 1.8x of each
other, not the "very uneven" the SAY describes (digest C7: some run to thousands of characters).
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    Succession,
    Transform,
    VGroup,
    Wait,
    there_and_back,
)

from common import (
    CLOUD,
    DATA,
    EMBED_MODEL,
    ERR,
    GAP_VALUES,
    INK,
    LOOKUP,
    MINI_CENTER,
    NARRATION,
    P_CTR2,
    SENTENCES,
    STRIP_TOP,
    TURN,
    LookFor,
    MiniMap,
    Prose,
    Seismograph,
    capture,
    card_rows,
    check_mark,
    coin_glyph,
    col_box,
    cost_tag,
    cross_mark,
    example_tag,
    excerpt,
    excerpt_chip,
    grey_tag,
    lref,
    model_box,
    nokey_tag,
    note,
    our_illustration_tag,
    pin,
    ponder_at,
    sans,
    src_panel,
    term,
    tracker,
    turn_card,
    type_cmd,
    under,
)
from explainer import style as S
from explainer.devops import CAPTION, Terminal, box, label, mono, mono_line, substring
from explainer.scene import VoiceScene

SAY = NARRATION["S14"]

# ------------------------------------------------------------------ the sources this scene quotes
CMD = "python cli.py --chunk --embed --load --chunk_type semantic-split"    # README.md line 227
CHAT = "python cli.py --chat --chunk_type semantic-split"                   # extra (digest)
assert CMD in excerpt("README.md", 220, 236), "README command changed"
RUN = capture("60", "cli-container")
assert RUN.cmd == CMD, RUN.cmd
L75 = RUN.line(75)
END75 = "…" + L75[L75.index("File /secrets/"):]     # the strip keeps line 75's end, cut at a word
assert END75.endswith("was not found."), END75
SAVED = capture("61", "cli-container")
assert SAVED.line(2) == "0", SAVED.line(2)
REGEX = r"(?<=[.?!])\s+"
L118 = excerpt("semantic_splitter.py", 118, 118)
L206 = excerpt("semantic_splitter.py", 206, 206)
assert REGEX in L118 and "batch_size=50" in L206
assert excerpt("semantic_splitter.py", 92, 92).strip() == '"percentile": 95,'
assert excerpt("semantic_splitter.py", 242, 242).strip() == "if x > breakpoint_distance_threshold"
assert excerpt("cli.py", 210, 210).strip() == "embedding_function=generate_text_embeddings)"
assert "Number of chunks:" in excerpt("cli.py", 215, 215)
assert "Processing file:" in excerpt("cli.py", 240, 240)
assert "Finished inserting" in excerpt("cli.py", 161, 161)
assert "generate_text_embeddings(" in excerpt("cli.py", 249, 249)
assert "generate_text_embeddings(" in excerpt("cli.py", 252, 252)
PONDER_Q = "char-split ran the chunk step without a key.\nCan semantic-split?"

# ------------------------------------------------------------------ layout (frame coordinates)
# the lecture's walk (beat 0), upper left
W_N, W_TW, W_TH, W_GAP = 6, 0.62, 0.5, 0.3
W_Y = 0.95                       # tile centres
W_BASE = W_Y + W_TH / 2 + 0.15   # the similarity bars stand on this line
W_K = 2.6                        # bar height per unit of similarity above 0.5
W_LAB_Y = 2.62                   # the similarity numbers, one row above the bars
SIMS = ((0, 0.89), (1, 0.85), (2, 0.68))     # gap k sits between tile k+1 and k+2 (lecture example)
W_THR = 0.8

# V8 (beats 1-3)
V_START, V_N = 72, 7             # sentences 73-79: the chapter-five spike and a bump below the line
TILE_H, SPIKE_H, ROW_W = 1.05, 2.0, 12.7
TY = 0.3                         # tile centres in beats 1-3
TY4 = 1.7                        # tile centres in beats 4-5 (the cards and the ponder card below)
ZOOM = 1                         # local tile that zooms to its full sentence (sentence 74)
PAIR = 1                         # arrows PAIR and PAIR + 1 pair up (the big gap)
BAND_Y = -1.0                    # the BLUE embedding band
AY, AL = -2.3, 0.62              # arrow origins and length

# beat 7 (above the 3-row strip)
GOLD_Y = (2.55, 1.95)            # GOLD rows at first
GOLD_Y_LOW = (-0.45, -1.02)      # GOLD rows once the "look for" card takes the top


def mixed(parts, size: float = CAPTION, color: str = INK, buff: float = 0.12) -> VGroup:
    """One row of serif pieces and `mono` pieces (in backticks); (text, colour) for a colour."""
    mobs = []
    for p in parts:
        s, col = (p, color) if isinstance(p, str) else p
        if len(s) > 1 and s.startswith("`") and s.endswith("`"):
            mobs.append(mono(s[1:-1], size, col))
        else:
            mobs.append(label(s, size, col))
    return VGroup(*mobs).arrange(RIGHT, buff=buff)


def tile_words(i: int, width: float) -> VGroup:
    """Sentence i's first three words (fewer when they don't fit) on at most two rows of 20 pt."""
    words = SENTENCES[i].replace("\n", " ").split()
    for m in (3, 2, 1):
        ws = words[:m]
        tail = "…" if len(words) > m else ""
        for c in dict.fromkeys(c for c in (2, 1, m) if 1 <= c <= m):
            rows = [r for r in (" ".join(ws[:c]), " ".join(ws[c:])) if r]
            rows[-1] += tail
            mobs = [label(r, CAPTION, INK) for r in rows]
            if all(mm.width <= width for mm in mobs):
                return VGroup(*mobs).arrange(DOWN, buff=0.05)
    return VGroup()


def two_row_tiles(sg: Seismograph) -> None:
    """Workaround: Seismograph shows one row of words (one or two words at 7 tiles); put the first
    three words on two rows under each tile's number."""
    for k, g in enumerate(sg.tiles):
        old = g.submobjects[1]
        num = g.num
        words = tile_words(sg.start + k, g.frame.width - 0.15)
        col = VGroup(num, words).arrange(DOWN, buff=0.07).move_to(g.frame)
        g.remove(old)
        g.add(col)
        g.words = words


def angles() -> list[float]:
    """Arrow directions (degrees) whose consecutive differences grow with the gaps' distances
    (our illustration): each turn heads back toward straight up."""
    th = [75.0]
    for v in GAP_VALUES[V_START:V_START + V_N - 1]:
        d = v * 75.0
        th.append(th[-1] + d if th[-1] <= 90 else th[-1] - d)
    return th


def arrow_at(x: float, deg: float, y: float = AY, length: float = AL, color: str = DATA) -> Arrow:
    a = np.deg2rad(deg)
    return Arrow([x, y, 0], [x + length * np.cos(a), y + length * np.sin(a), 0], buff=0, color=color,
                 stroke_width=5, tip_length=0.16, max_tip_length_to_length_ratio=0.3)


def outline(mobs, color: str = DATA, pad: float = 0.07) -> VGroup:
    g = VGroup(*mobs)
    return box(g.width + 2 * pad, g.height + 2 * pad, color, fill_opacity=0.0, stroke=3.5,
               radius=0.12).move_to(g)


def key_card(name: str, color: str, mark) -> VGroup:
    """'<name> · --chunk · no key: <mark>' in a small card of `color`. .frame .mark"""
    row = VGroup(mono(name, CAPTION, INK), label("·", CAPTION, S.GREY), mono("--chunk", CAPTION, INK),
                 label("· no key:", CAPTION, INK), mark).arrange(RIGHT, buff=0.14)
    fr = box(row.width + 0.5, row.height + 0.34, color, fill_opacity=0.1, stroke=3, radius=0.12)
    row.move_to(fr)
    g = VGroup(fr, row)
    g.frame, g.mark = fr, mark
    return g


# beat 8: our illustration of a book's semantic chunks, in characters. Not a measurement: no capture
# holds a semantic chunk (the run fails before one is saved). Uneven on purpose, as the SAY and the
# digest (C7: "some will be thousands of characters") describe; never shown as numbers.
CHUNK_CHARS = (1480, 260, 2350, 610, 3120, 140, 920)


def chunk_bars() -> tuple[VGroup, list[int]]:
    """One GREEN bar per chunk of CHUNK_CHARS (our illustration), its length proportional to the
    chunk's characters. Returns (bars, lengths)."""
    lens = list(CHUNK_CHARS)
    scale = 5.2 / max(lens)
    bars = VGroup(*[Rectangle(width=n * scale, height=0.24, stroke_color=DATA, stroke_width=2)
                    .set_fill(DATA, 0.55) for n in lens])
    bars.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    return bars, lens


class SemanticSplit(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, f"S14 has {len(SAY)} SAY lines; this scene times 9"

        tr = tracker("Semantic")

        # ========================================================== 0 · the lecture's walk
        lr = lref("B19–B33")
        mm = MiniMap(MINI_CENTER)
        wt = VGroup()
        for i in range(W_N):
            fr = box(W_TW, W_TH, DATA, fill_opacity=0.14, radius=0.08, stroke=2.5)
            wt.add(VGroup(fr, sans(str(i + 1), 22, INK).move_to(fr)))
        wt.arrange(RIGHT, buff=W_GAP).move_to([-6.2 + (W_N * W_TW + (W_N - 1) * W_GAP) / 2, W_Y, 0])

        def gap_x(k):
            return (wt[k].get_right()[0] + wt[k + 1].get_left()[0]) / 2

        def sim_bar(k, s):
            h = (s - 0.5) * W_K
            b = Rectangle(width=0.18, height=h, stroke_color=LOOKUP, stroke_width=2).set_fill(LOOKUP, 0.6)
            return b.move_to([gap_x(k), W_BASE + h / 2, 0])

        bars0 = [sim_bar(k, s) for k, s in SIMS]
        labs0 = [mono(f"{s}", CAPTION, LOOKUP).move_to([gap_x(k), W_LAB_Y, 0]) for k, s in SIMS]
        thr_y = W_BASE + (W_THR - 0.5) * W_K
        thr = DashedLine([wt.get_left()[0] - 0.1, thr_y, 0], [wt.get_right()[0] + 0.1, thr_y, 0], color=TURN,
                         stroke_width=4)
        thr_lab = mono("0.8", CAPTION, TURN).next_to(thr, RIGHT, buff=0.12)
        anchor = Arrow([wt[0].get_center()[0], W_Y - W_TH / 2 - 0.6, 0], [wt[0].get_center()[0], W_Y - W_TH / 2 - 0.06, 0],
                       buff=0, color=TURN, stroke_width=5, tip_length=0.16)
        anchor_lab = sans("anchor", CAPTION, TURN).next_to(anchor, RIGHT, buff=0.1).align_to(anchor, DOWN)
        anchor_g = VGroup(anchor, anchor_lab)
        grp2 = outline([wt[0], wt[1]])
        grp3 = outline([wt[0], wt[1], wt[2]])
        chunk_lab = sans("chunk 1", CAPTION, DATA).next_to(grp3, DOWN, buff=0.12).align_to(grp3, LEFT)
        cands = VGroup(*[DashedLine([gap_x(k), W_Y - W_TH / 2 - 0.15, 0], [gap_x(k), W_Y + W_TH / 2 + 0.15, 0],
                                    color=S.GREY, stroke_width=3) for k in range(W_N - 1)])
        cut_x = gap_x(2)
        cut0 = DashedLine([cut_x, W_Y - W_TH / 2 - 0.15, 0], [cut_x, W_Y + W_TH / 2 + 0.15, 0], color=TURN,
                          stroke_width=4)
        ex = example_tag()
        ex.move_to([wt.get_right()[0] + 0.45 + ex.width / 2, W_Y, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(mm), FadeIn(lr), run_time=0.7)
            self.play(mm.light("chunking"), run_time=0.4)
            vo.wait_until("with the lecture's best answer")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in wt], lag_ratio=0.12),
                      FadeIn(ex, shift=LEFT * 0.1), run_time=0.9)
            vo.wait_until("cut where the meaning changes")
            self.play(LaggedStart(*[Create(c) for c in cands], lag_ratio=0.15),
                      Indicate(mm.items["chunking"], color=TURN, scale_factor=1.3), run_time=0.8)
            vo.wait_until("On the slides")
            self.play(GrowArrow(anchor), FadeIn(anchor_lab), run_time=0.6)
            vo.wait_until("walks through the sentences")
            self.play(GrowFromEdge(bars0[0], DOWN), FadeIn(labs0[0], shift=UP * 0.1), run_time=0.6)
            self.play(Create(grp2), run_time=0.5)
            vo.wait_until("and joins neighbors")
            self.play(anchor_g.animate.shift(RIGHT * (wt[2].get_center()[0] - wt[0].get_center()[0])),
                      run_time=0.6)
            self.play(GrowFromEdge(bars0[1], DOWN), FadeIn(labs0[1], shift=UP * 0.1),
                      GrowFromEdge(bars0[2], DOWN), FadeIn(labs0[2], shift=UP * 0.1), run_time=0.7)
            vo.wait_until("while their similarity")
            self.play(Create(thr), FadeIn(thr_lab), run_time=0.7)
            self.play(ReplacementTransform(grp2, grp3), FadeIn(chunk_lab, shift=UP * 0.1),
                      bars0[2].animate.set_fill(S.GREY, 0.35).set_stroke(S.GREY), labs0[2].animate.set_color(S.GREY),
                      ReplacementTransform(cands[2], cut0), *[FadeOut(cands[k]) for k in range(W_N - 1) if k != 2],
                      run_time=0.9)

        # ========================================================== 1 · the code: windows, embedded
        ticks = VGroup(*[VGroup(check_mark(0.26, DATA), m).arrange(RIGHT, buff=0.2)
                         for m in (mixed(["split at", "`. ? !`"]), label("one neighbor each side", CAPTION, INK),
                                   label("cosine", CAPTION, INK))])
        ticks.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        ticks.move_to([-6.1 + ticks.width / 2, 2.62 - ticks.height / 2, 0])
        walk = VGroup(wt, *bars0, *labs0, thr, thr_lab, anchor_g, grp3, chunk_lab, cut0, ex)

        sg = Seismograph(start=V_START, n=V_N, width=ROW_W, tile_h=TILE_H, spike_h=SPIKE_H, show=("tiles",))
        two_row_tiles(sg)
        sg.shift(UP * (TY - sg.tiles.get_center()[1]) + LEFT * sg.tiles.get_center()[0])
        tiles = sg.tiles
        xs = [t.get_center()[0] for t in tiles]
        block = Rectangle(width=tiles.width, height=TILE_H, stroke_color=DATA, stroke_width=2.5)
        block.set_fill(DATA, 0.14).move_to(tiles)
        pieces = VGroup(*[t.frame.copy() for t in tiles])
        rx = excerpt_chip(REGEX, "semantic_splitter.py · line 118 (excerpt)", line=L118)
        rx.move_to([6.4 - rx.width / 2, 2.45, 0])
        card = sg.sentence_card(V_START + ZOOM)
        card.move_to([0, tiles.get_top()[1] + 0.2 + card.height / 2, 0])
        band = box(tiles.width, 0.42, CLOUD, fill_opacity=0.2, stroke=3, radius=0.1).move_to([0, BAND_Y, 0])
        band_lab = VGroup(sans("embedding model", CAPTION, INK), mono(EMBED_MODEL, CAPTION, CLOUD)).arrange(RIGHT, buff=0.2)
        band_lab.move_to(band).align_to(band, LEFT).shift(RIGHT * 0.25)
        th = angles()
        arrows = [arrow_at(x, d) for x, d in zip(xs, th)]
        c206 = excerpt_chip("batch_size=50", "semantic_splitter.py · line 206 (excerpt)", line=L206)
        c206.move_to([6.4 - c206.width / 2, -3.45 + c206.height / 2, 0])
        coin = coin_glyph(0.17).next_to(c206.chip, LEFT, buff=0.2)

        def window(i):
            return range(max(0, i - 1), min(V_N - 1, i + 1) + 1)

        def drop(i, rt):
            """The window's tile frames peel off, fall through the band and become arrow i."""
            w = VGroup(*[tiles[j].frame.copy() for j in window(i)])
            self.add(w)
            return Succession(w.animate(run_time=rt * 0.55).scale(0.22).move_to([xs[i], BAND_Y, 0]),
                              ReplacementTransform(w, arrows[i], run_time=rt * 0.45))

        with self.voiceover(SAY[1]) as vo:
            self.play(walk.animate.scale(0.3).move_to(ticks.get_center()).set_opacity(0),
                      LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ticks], lag_ratio=0.3),
                      FadeOut(mm), run_time=1.0)
            self.remove(walk, *walk.submobjects)
            vo.wait_until("with a different rule")
            self.play(FadeIn(block), FadeIn(rx, shift=LEFT * 0.15), run_time=0.4)
            self.play(ReplacementTransform(block, pieces), run_time=0.5)
            self.play(FadeIn(sg), run_time=0.3)
            self.remove(pieces)
            vo.wait_until("Every sentence gets a window")
            self.play(FadeIn(card, target_position=tiles[ZOOM].get_center(), scale=0.2), run_time=0.5)
            self.wait(0.4)
            self.play(FadeOut(card, target_position=tiles[ZOOM].get_center(), scale=0.2), FadeOut(ticks),
                      run_time=0.4)
            br = sg.bracket(ZOOM)
            vo.wait_until("itself and one neighbor")
            self.play(FadeIn(br, shift=UP * 0.1), Indicate(tiles[ZOOM].frame, color=TURN, scale_factor=1.06),
                      run_time=0.45)
            self.play(Indicate(VGroup(tiles[ZOOM - 1].frame, tiles[ZOOM + 1].frame), color=TURN, scale_factor=1.06),
                      FadeIn(band), FadeIn(band_lab), run_time=0.45)
            self.play(Transform(br, sg.bracket(0)), run_time=0.3)
            self.play(drop(0, 0.8), FadeIn(c206, shift=LEFT * 0.15), FadeIn(coin, scale=1.6), run_time=0.8)
            for i in range(1, V_N):
                self.play(Transform(br, sg.bracket(i)), drop(i, 0.4), run_time=0.4)

        # ========================================================== 2 · distances, plotted: a seismograph
        o1 = arrows[PAIR].get_start()
        a2 = arrows[PAIR + 1].copy()
        r0 = np.deg2rad(min(th[PAIR], th[PAIR + 1]))
        arc = Arc(radius=0.32, start_angle=r0, angle=np.deg2rad(abs(th[PAIR + 1] - th[PAIR])), arc_center=o1,
                  color=LOOKUP, stroke_width=6)
        sp = sg.spikes[PAIR]
        sp_copy = Line(sp.get_start(), sp.get_end(), color=LOOKUP, stroke_width=4)
        ill = our_illustration_tag()
        ill.move_to([6.4 - ill.width / 2, 2.62, 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(rx), FadeOut(br), run_time=0.4)
            self.play(a2.animate.shift(o1 - arrows[PAIR + 1].get_start()), run_time=1.0)
            self.play(Create(arc), run_time=0.8)
            vo.wait_until("and plots it over the text")
            self.play(ReplacementTransform(arc, sp_copy), FadeOut(a2), run_time=0.5)
            self.play(sg.spikes_in(run_time=1.1), FadeIn(ill, shift=LEFT * 0.15), run_time=1.1)
            self.remove(sp_copy)
            vo.wait_until("like a seismograph")
            self.play(Indicate(sg.parts["curve"], color=LOOKUP, scale_factor=1.03), run_time=0.7)

        # ========================================================== 3 · the 95th percentile, the cuts
        p91 = src_panel("semantic_splitter.py", 91, 96)
        p91.move_to([0, -3.45 + p91.height / 2, 0])
        b92 = p91.bar(92, TURN)
        p239 = src_panel("semantic_splitter.py", 239, 243)
        p239.move_to([0, -3.45 + p239.height / 2, 0])
        b242 = p239.bar(242, TURN)
        above = sg.above()
        assert above == [PAIR], above

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(*arrows, band, band_lab, c206, coin)), FadeIn(p91, shift=UP * 0.2),
                      run_time=0.6)
            self.play(FadeIn(b92), run_time=0.3)
            vo.wait_until("draws a line at the 95th percentile")
            sg.rise(self, run_time=1.2)
            self.play(Indicate(p91.span(92, "95"), color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("and cuts at every spike above it")
            self.play(FadeOut(b92), ReplacementTransform(p91, p239), run_time=0.6)
            self.play(FadeIn(b242), Indicate(sg.spikes[PAIR], color=TURN, scale_factor=1.15), run_time=0.6)
            self.play(*sg.cuts(), run_time=1.0)
            chunks = VGroup(outline(tiles[:PAIR + 1]), outline(tiles[PAIR + 1:]))
            vo.wait_until("So the biggest 5 percent")
            self.play(Indicate(sg.cut_marks, color=TURN, scale_factor=1.2),
                      Indicate(sg.spikes[PAIR], color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("become chunk boundaries")
            self.play(LaggedStart(*[Create(c) for c in chunks], lag_ratio=0.3), run_time=0.8)

        # ========================================================== 4 · ponder: does it need a key?
        c_char = key_card("char-split", DATA, check_mark(0.28, DATA))
        c_sem = key_card("semantic-split", TURN, label("?", 26, TURN))
        VGroup(c_char, c_sem).arrange(RIGHT, buff=0.5).move_to([0, 0.35, 0])

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(p239, b242, lr, ill)), *sg.parts_out("spikes", "curve", "threshold"),
                      run_time=0.4)
            moving = VGroup(sg, sg.cut_marks, chunks)
            # the card writes in under the row once the row has moved clear of it (on "Char split ran")
            self.play(moving.animate.shift(UP * (TY4 - TY)),
                      Succession(Wait(0.35), FadeIn(c_char, shift=UP * 0.15, run_time=0.4)), run_time=0.75)
            self.remove(moving)
            self.add(sg, sg.cut_marks, chunks, c_char)
            vo.wait_until("Can semantic split")
            self.play(FadeIn(c_sem, shift=UP * 0.15), run_time=0.5)
        pcard = ponder_at(self, PONDER_Q, 8.0, y=-2.2)

        # ========================================================== 5 · no: every window is embedded first
        xm = cross_mark(0.26, ERR, 5).move_to(c_sem.mark)
        br5 = sg.bracket(ZOOM)
        ebox = model_box("embedding model", 2.2, 0.8, CLOUD, sub=EMBED_MODEL)
        ebox.move_to([xs[ZOOM], -0.75, 0])
        enote = note("every window is embedded before a single cut")
        enote.next_to(ebox, DOWN, buff=0.3)
        enote.shift(RIGHT * max(0, -6.3 - enote.get_left()[0]))

        p207 = src_panel("cli.py", 207, 215, size=20)
        p207.move_to([-6.45 + p207.width / 2, 0.15, 0])
        b210 = p207.bar(210, TURN)
        u210 = under(p207.span(210, "generate_text_embeddings"), TURN)
        gl = model_box("embedding\nmodel", 1.5, 1.0, CLOUD)
        gold = cost_tag("a Google call")
        gl.move_to([2.6, p207.get_top()[1] + 0.25 + gl.height / 2, 0])     # above the panel, top right
        gold.next_to(gl, RIGHT, buff=0.25)
        both = note("embed() calls it too · cli.py · lines 249, 252")
        both.next_to(p207, DOWN, buff=0.3).align_to(p207, LEFT).shift(RIGHT * 0.15)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pcard), run_time=0.4)
            self.play(Transform(c_sem.mark, xm), c_sem.frame.animate.set_stroke(ERR),
                      FadeOut(c_char), run_time=0.5)
            vo.wait_until("To find where the meaning shifts")
            # before a single cut: the cut and the two chunk outlines dim, so the bracket reads alone
            self.play(FadeIn(br5, shift=UP * 0.1), FadeIn(ebox), sg.cut_marks.animate.set_stroke(opacity=0.25),
                      chunks.animate.set_stroke(opacity=0.25), run_time=0.6)
            w = VGroup(*[tiles[j].frame.copy() for j in window(ZOOM)])
            self.add(w)
            self.play(w.animate.scale(0.22).move_to(ebox), run_time=0.8)
            self.remove(w)
            # the bracket flashes in place (a scaling Indicate would push its left end off the safe frame)
            self.play(br5[0].animate(rate_func=there_and_back).set_stroke(width=9),
                      Indicate(br5[1], color=TURN, scale_factor=1.3), Indicate(ebox, color=CLOUD, scale_factor=1.08),
                      FadeIn(enote, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("Look at the function")
            self.play(FadeOut(VGroup(sg, sg.cut_marks, chunks, c_sem, br5, ebox, enote)), run_time=0.5)
            self.play(FadeIn(p207, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(b210), run_time=0.3)
            vo.wait_until("generate text embeddings")
            self.play(Create(u210), FadeIn(gl, shift=LEFT * 0.15), run_time=0.6)
            self.play(FadeIn(gold, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("the same one the embed step uses")
            self.play(FadeIn(both, shift=UP * 0.1), Indicate(gl, color=CLOUD, scale_factor=1.08), run_time=0.8)

        # ========================================================== 6 · step 1: the README command, no key
        t = term(P_CTR2, rows=12, container=True)
        nk = nokey_tag()
        nk.move_to([t.box.get_right()[0] - 0.2 - nk.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(p207, b210, u210, gl, gold, both)), FadeIn(t), tr.goto(1), run_time=0.5)
            cmd = type_cmd(self, t, CMD, type_time=1.1)
            assert hasattr(cmd, "rows") and len(cmd.rows) == 2, cmd
            cmd_copy = [r.copy() for r in cmd.rows]
            vo.wait_until("runs all three steps")
            head = t.print(self, RUN.at((2, 5)), wrap=True, run_time=0.6)
            assert len(head) == 7, len(head)
            u3 = under(substring(head[0], "chunk=True, embed=True, load=True"), TURN)
            pin(self, head[0], u3, anim=Create(u3), run_time=0.4)
            vo.wait_until("On our machine")
            self.play(FadeIn(nk, shift=LEFT * 0.1), run_time=0.25)
            frames = t.print(self, RUN.at("", 11, 14, 17, 20, 23), wrap=True, run_time=0.45)
            assert len(frames) == 7, len(frames)
            vo.wait_until("it fails inside")
            tail = t.print(self, ["…", (RUN.line(75), ERR)], wrap=True, run_time=0.4)
            assert len(tail) == 3, len(tail)
            fr_rows = [frames[k] for k in (1, 2, 3, 4, 6)]
            boxes = []
            for r in fr_rows:
                a = r.text.index('"')
                b = r.text.index(", in")
                boxes.append(col_box(r, a, b, LOOKUP))
            sx = t.box.get_left()[0] + 0.15
            dots = [Dot([sx, r.strut.get_center()[1], 0], radius=0.06, color=LOOKUP) for r in fr_rows]
            spine = Line(dots[0].get_center(), dots[-1].get_center(), color=LOOKUP, stroke_width=3)
            self.play(Create(spine), LaggedStart(*[FadeIn(VGroup(d, bx)) for d, bx in zip(dots, boxes)],
                                                 lag_ratio=0.35), run_time=1.0)
            vo.wait_until("on the first book")
            b5a, b5b = head[5], head[6]
            ub = VGroup(under(substring(b5a, "The Complete Book of Chees"), TURN), under(b5b.glyphs, TURN))
            self.play(Create(ub), run_time=0.5)
            vo.wait_until("before a single chunk is saved")
            ns = VGroup(label("nothing saved", CAPTION, S.GREY), mono(SAVED.cmd, CAPTION, INK),
                        label("→", CAPTION, S.GREY), mono(SAVED.line(2), CAPTION, INK)).arrange(RIGHT, buff=0.16)
            ns_fr = box(ns.width + 0.4, 0.34, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.1)
            ns.move_to(ns_fr)
            nsg = VGroup(ns_fr, ns)
            row9 = frames[0]
            nsg.move_to([t.box.get_right()[0] - 0.15 - nsg.width / 2, row9.strut.get_center()[1] + 0.03, 0])
            self.play(FadeIn(nsg, shift=LEFT * 0.15), run_time=0.5)

        # ========================================================== 7 · with your key: budget, look for
        g1 = cost_tag("≈ 528 embedding calls just to chunk the corpus")
        g2 = cost_tag("≈ 90 more to embed the chunks")
        g3 = cost_tag("10–20 min")
        est = grey_tag("our estimate")
        row1 = VGroup(g1, g2).arrange(RIGHT, buff=0.3)
        row2 = VGroup(g3, est).arrange(RIGHT, buff=0.3)
        for r, y in zip((row1, row2), GOLD_Y):
            r.move_to([-6.3 + r.width / 2, y, 0])
        est_at = est.get_center()
        est.move_to([-6.3 + est.width / 2, GOLD_Y[1], 0])         # moves aside when 10–20 min arrives
        # two rows: a viewer who stops after the one-book trial would chat against a one-book collection
        tip = card_rows([mixed(["try one book first: move the others out of", "`input-datasets/books`"]),
                         "then put them back and run the command again"])
        tip.move_to([0, 1.45 - tip.height / 2, 0])     # top where the one-row card's was, clear of the GOLD rows
        lf = LookFor([
            (mixed(["per book:", "`Number of chunks: …`", "far fewer than char-split"]), "cli.py · line 215"),
            (mixed(["`embed():`", "`Processing file: outputs/chunks-semantic-split-…`"], buff=0.22), "line 240"),
            (VGroup(mixed(["`load():`", "`Finished inserting … into collection`"], buff=0.22),
                    mixed(["`'semantic-split-collection'`", ("· line 161", S.GREY)]))
             .arrange(DOWN, aligned_edge=LEFT, buff=0.1), None),
        ])
        lf.rows[2][0][1].shift(RIGHT * 0.5)
        lf.move_to([-6.3 + lf.width / 2, 2.8 - lf.height / 2, 0])
        n429 = note("429 retries are normal · stopped after 5 retries? wait, then rerun: it starts over from "
                    "the first book")
        n429.move_to([-6.3 + n429.width / 2, lf.get_bottom()[1] - 0.12 - n429.height / 2, 0])

        def shrink_to_strip(row, extra=()):
            """The terminal shrinks to 3 rows: the command (its rows come back) and `row`, a new
            line that fades in on the third row."""
            ref = Terminal(prompt=t.prompt, width=t.box.width, rows=3, size=t.size, title="x")
            ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0],
                                t.box.get_bottom()[1] - ref.box.get_bottom()[1], 0]))
            # keep the live frame colour (TEAL inside the container), as the house resize() does
            ref.box.set_stroke(t.box.get_stroke_color(), t.box.get_stroke_width())
            gone = list(t.lines.submobjects)
            self.play(FadeOut(VGroup(*gone)), FadeOut(nsg), FadeOut(VGroup(spine, *dots, *boxes, ub)), run_time=0.3)
            for ln in gone:
                t.lines.remove(ln)
            for i, c in enumerate(cmd_copy):
                c.shift(ref._slot(i) - c.strut.get_corner(UP + LEFT))
            row.shift(ref._slot(2) - row.strut.get_corner(UP + LEFT))
            self.play(Transform(t.box, ref.box), Transform(t.bar, ref.bar), t.dots.animate.move_to(ref.dots),
                      t.title.animate.move_to(ref.title),
                      FadeIn(VGroup(*cmd_copy)), FadeIn(row), *extra, run_time=0.8)
            for c in cmd_copy:
                t.lines.add(c)
            t.lines.add(row)
            t.rows = 3

        with self.voiceover(SAY[7]) as vo:
            # line 75's end from "File": one readable row, not the fold's fragment "-service-account…"
            assert len(END75) <= t.max_chars, (len(END75), t.max_chars)
            shrink_to_strip(mono_line(END75, t.size, ERR), extra=[nk.animate.set_y(STRIP_TOP - t.bar_h / 2)])
            vo.wait_until("by our estimate")
            self.play(FadeIn(est, shift=RIGHT * 0.15), run_time=0.4)
            vo.wait_until("about 528 embedding calls")
            self.play(FadeIn(g1, shift=RIGHT * 0.15), run_time=0.9)
            vo.wait_until("about 90 more")
            self.play(FadeIn(g2, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("and 10 to 20 minutes")
            self.play(FadeIn(g3, shift=RIGHT * 0.15), est.animate.move_to(est_at), run_time=0.5)
            vo.wait_until("Try one book first")
            self.play(FadeIn(tip, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Look for a chunk count")
            # the tip leaves first: the GOLD rows then move down through the band it held (not across its text)
            self.play(FadeOut(tip), run_time=0.25)
            self.play(row1.animate.move_to([-6.3 + row1.width / 2, GOLD_Y_LOW[0], 0]),
                      row2.animate.move_to([-6.3 + row2.width / 2, GOLD_Y_LOW[1], 0]), run_time=0.45)
            self.play(FadeIn(lf.frame), FadeIn(lf.title), run_time=0.25)
            self.play(lf.write_item(0))
            self.play(lf.write_item(1))
            vo.wait_until("and finally")
            self.play(lf.write_item(2))
            self.play(FadeIn(n429, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 8 · uneven chunks; your turn
        bars, lens = chunk_bars()
        bars.move_to([-6.2 + bars.width / 2, 1.4, 0])     # clear of the taller ▶ card below
        ill8 = our_illustration_tag()
        ill8.move_to([bars.get_right()[0] + 0.35 + ill8.width / 2, bars.get_top()[1] - ill8.height / 2, 0])
        # "seven of": a whole book gives far more chunks (digest: ≈ 1,300 for the 11 books)
        cap8 = note("seven of one book's chunks · bar length = characters").next_to(bars, DOWN, buff=0.15).align_to(bars, LEFT)
        # "very uneven" without numbers (the lengths are illustrative): the longest and the shortest flash
        long_i, short_i = int(np.argmax(lens)), int(np.argmin(lens))
        single = note("a single-topic book still gets its top 5 % cut")
        single.move_to([6.3 - single.width / 2, bars[-1].get_center()[1], 0])
        # the 429 advice rides on the card the viewer pauses on (beat 7's note is up for ~4 s only)
        tc = turn_card([CMD, (Prose("429 retries are normal · stopped after 5? wait, then rerun: it starts over"),
                              S.GREY),
                        (Prose("extra, after the load finishes:"), S.GREY), (CHAT, "extra")],
                       header="your turn · with your key")
        tc.move_to([0, -3.45 + tc.height / 2, 0])

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(lf, n429, row1, row2, t, nk)), run_time=0.5)
            # 1.0 s (not 1.2): the GREY note below then lands on "and even a single-topic book"
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.15), FadeIn(ill8),
                      FadeIn(cap8), run_time=1.0)
            self.play(Indicate(bars[long_i], color=DATA, scale_factor=1.05),
                      Indicate(bars[short_i], color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("and even a single-topic book")
            self.play(FadeIn(single, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("Afterwards, an extra")
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Pause and try it")
            self.play(Indicate(tc.tag, color=TURN, scale_factor=1.15), run_time=0.7)
        self.wait(2)                                   # ▶ beat: hold the frame

        self.play(FadeOut(VGroup(tr, bars, ill8, cap8, single, tc)), run_time=0.8)
        self.wait(0.3)
