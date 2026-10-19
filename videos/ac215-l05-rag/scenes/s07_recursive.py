"""S07 · Recursive split and its hidden overlap (README "Chunk" step 3, two extras). Lecture: B16–B19.

Beats (script.md "## S07", one voiceover block each):
 0  TRACKER Chunk 3. cli.py · lines 196–205 (the mini-map stays hidden while it is up); line 197
    `chunk_size = 350` highlights YELLOW; a GREY dashed ghost argument `chunk_overlap = ?` appears
    beside lines 199–200.
 1  LECTURE B16–B19. The panel leaves; the mini-map fades in, and with the lecture tag, small at
    the bottom left (tag illustration), the lecture's mock paper twice: a 200-character ruler
    cutting a word and running the abstract into the next section's heading (RED) beside one
    chunk per section (GREEN); it stays still (the narration never names it). V3: the story as a
    ribbon of word blocks, GREY ticks at the paragraph gaps (tall) and at the one line break
    (short); "chunking" lit; four PURPLE separator chips \\n\\n → \\n → " " → "" with their
    names. PURPLE scissors hunt along the ribbon and snip at the story's real chunk ends (all
    blank lines) while chip 1 is lit; chips 2, 3 and 4 light as the narration names them (the
    ribbon's one line break flashes with chip 2; chip 4 pulses at "a single character"). Then
    chip 1 lights again, a GREY note says every cut here is a blank line, the cuts flash and a
    callout shows one cut between "table." and "On".
 2  The TEAL container terminal (13 rows; the mini-map hides) types `python cli.py --chunk
    --chunk_type recursive-split` -> cli-container/13 lines 2–4, …, 32–33 (line 2 cut); TRACKER
    Chunk 3 · extra: `wc -l outputs/chunks-recursive-split-*.jsonl` (extra) -> cli-container/14
    lines 11, 13. `35` and `14228 total` YELLOW; ▶ your turn beside the README command. Hold 2 s.
 3  The terminal shrinks to the 3-row strip (the wc command and its total). Above it two GREEN
    bars, char-split 8,248 and recursive-split 14,228 (the number lifts out of the strip), each
    labelled "chunk size 350". PONDER (8 s): the card in the lower third, above the strip.
 4  TRACKER Chunk 3 · extra. The bars go; the terminal grows to 12 rows and types the one-liner
    of cli-container/15 (extra; it folds onto 5 rows, the row that continues the file name at
    column 0, see literal_safe_rows) before the narration starts, and holds it ~3 s (to pause on
    and copy); at "Chunk 1 starts again" the command clears and -> lines 8–16, wrapped (12
    rows). A GREY row tag on the --- line says which side is chunk 0's end and
    which is chunk 1; chunk 1's first two lines (line 12's `## Chapter One: The First Slice` and
    line 14's sentence) turn YELLOW, then the same two lines at chunk 0's end (8, 10), joined by
    a PINK bracket "repeated". Top right: the chip "library default: chunk_overlap = 200"
    (its value pulses at "up to 200 characters"), then the tag
    "erratum · the README says overlapping, not how much". A GREY tag "chunk 1: 328 characters"
    at the end of chunk 1.
 5  The terminal shrinks to the strip (line 8, ---, line 12). V3's ribbon returns with the
    recursive chunks as GREEN cards on two rows (numbered), the overlap bands shaded YELLOW;
    a GOLD coin on each band, "embedded, stored, paid for". The erratum tag gives way to a GREY
    chip "want another value? set chunk_overlap".
 6  LECTURE B16–B19. The strip, the ribbon and the chips leave (the tracker drops " · extra");
    the mini-map returns. The
    lecture's GREEN paper from beat 1 grows: three section-shaped chunks (title, abstract,
    methods), "ideal: a chunk per section". From the PURPLE scissors chip "recursive-split", an
    arrow "recursive: paragraphs" goes part of the way, a GREY dashed one "semantic chunking ·
    part 2" all the way. The mini-map's "chunking" gets a GREEN tick. Fade to an empty frame.

Deviations from SHOW (see the scene report): the cli-container/15 one-liner folds onto 5 rows and
its 12 output rows need the whole terminal (the tracker's "· extra" stays), so it is typed in the
quiet after the ponder and stays complete on screen ~3 s; then it clears in place (a 5-row scroll
would sweep over the title bar) and the output prints; its fold breaks inside the
'...' file name, so that continuation row starts at column 0 (the house 4-space indent would
put four spaces into the file name); the two arrows of beat 6 start
at a PURPLE "recursive-split" scissors chip, because the strip at that point holds output, not a
command, and leaves with the ribbon; the lecture tag is shown in beats 1 and 6 (the lecture's
pictures), not over the overlap beats, which the slides never mention (SLIDES.md Conflict 5).
"""

import ast

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    TransformFromCopy,
    VGroup,
    VMobject,
    there_and_back,
)

from common import (
    COUNTS,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MINI_CENTER,
    NARRATION,
    P_CTR,
    RECURSIVE_SPANS,
    STORY_START,
    STORY_TEXT,
    STRIP_TOP,
    TOOL,
    TURN,
    COST,
    MiniMap,
    Ribbon,
    beside,
    capture,
    _space_levels,
    _type_rows,
    caption_extra,
    coin_glyph,
    erratum_tag,
    extra_tag,
    fold_cmd,
    grid_x0,
    illustration_tag,
    lref,
    note,
    pin,
    ponder_at,
    resize,
    scissors_glyph,
    src_panel,
    term,
    tracker,
    type_cmd,
    under,
    your_turn,
)
from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import CAPTION, MONO, box, cell_width, chip, label, mono, substring
from explainer.scene import VoiceScene

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ commands and real outputs
CHUNK = capture("13", "cli-container")
CHUNK_CMD = "python cli.py --chunk --chunk_type recursive-split"        # README.md line 109
assert CHUNK.cmd == CHUNK_CMD and CHUNK.exit == 0
CHUNK_OUT = CHUNK.at((2, 4), "…", (32, 33))
assert CHUNK.line(32).endswith("Tolminc Cheese.txt") and CHUNK.line(33) == "Number of chunks: 35"
assert len(CHUNK_OUT) == 6

WC = capture("14", "cli-container")
WC_CMD = "wc -l outputs/chunks-recursive-split-*.jsonl"
assert WC.cmd == WC_CMD and WC.exit == 0
WC_OUT = WC.at(11, 13)
assert WC.line(11).split()[0] == "35" and WC.line(11).endswith("Tolminc Cheese.jsonl")
assert WC.line(13).split() == ["14228", "total"] and COUNTS["recursive-split"] == 14228

FIRST = capture("15", "cli-container")
assert FIRST.cmd.startswith('python -c "import json;') and FIRST.exit == 0
FIRST_OUT = FIRST.at((8, 16))
HEAD = "## Chapter One: The First Slice"
assert FIRST.line(8) == HEAD and FIRST.line(12) == HEAD and FIRST.line(11) == "---"
SENT = "The first thing Mara noticed was that nobody hurried."            # repeated too
assert FIRST.line(10) == SENT and FIRST.line(14) == SENT
CHUNK1 = "\n".join(FIRST.line(n) for n in range(12, 17))     # chunk 1, as printed
assert len(CHUNK1) == 328 and FIRST.line(17) == "---"
assert STORY_TEXT[RECURSIVE_SPANS[1][0]:RECURSIVE_SPANS[1][1]] == CHUNK1   # our spans match the run
assert len(RECURSIVE_SPANS) == 35 and COUNTS["char-split"] == 8248

PANEL_SRC = ("cli.py", 196, 205)

# the story's first ~1,000 characters: every recursive chunk end in view is a blank line
VIEW = (STORY_START, STORY_START + 1000)
ENDS = [b for a, b in RECURSIVE_SPANS if VIEW[0] < b < VIEW[1]]
assert ENDS == [219, 461, 575, 846], ENDS
assert all(STORY_TEXT[b:b + 2] == "\n\n" for b in ENDS)
assert max(len(p) for p in STORY_TEXT.split("\n\n")) < 350      # so blank lines are enough
SEAM = 461                                                        # the callout's cut: "table." | "On"
CALL_A = STORY_TEXT.rindex(" on the kitchen", 0, SEAM) + 1
CALL_B = SEAM + 2 + len("On it sat bread")
assert CALL_B - CALL_A <= 60

PONDER_Q = "Same chunk size, 350.\nWhy 14,228 chunks instead of 8,248?"

# ------------------------------------------------------------------ layout
RIB_Y = 1.5            # beat 1: the ribbon
CHIP_Y = 0.22          # beat 1: the separator chips
RIB2_Y = -0.45         # beat 5: the ribbon above the strip
PAPER_W, PAPER_H = 1.45, 1.9
PAPER_L = np.array([-5.2, -1.8, 0])     # beat 1: the ruler paper
PAPER_R = np.array([-2.2, -1.8, 0])     # beat 1: one chunk per section
BIG_K = 1.75
PAPER_BIG = np.array([3.55, 0.45, 0])    # beat 6


def row_tag(s: str, color: str = S.GREY, text_color: str | None = None, h: float = 0.36) -> VGroup:
    """A tag that fits inside one terminal row (as in S06). .box .text"""
    t = label(s, CAPTION, text_color or color)
    b = RoundedRectangle(width=t.width + 0.34, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def light(c, on: bool = True):
    """A separator chip lights YELLOW (look here now) or goes back to PURPLE."""
    if on:
        return c.box.animate.set_stroke(TURN, 4).set_fill(TURN, 0.22)
    return c.box.animate.set_stroke(TOOL, 2.5).set_fill(TOOL, 0.16)


# ------------------------------------------------------------------ the lecture's mock paper (B16-B19)
class MockPaper(VGroup):
    """Our redrawing of the lecture's mock research paper: no text, a two-bar title and three
    sections (abstract, methods, results), each a heading bar over thin text lines. Shapes only,
    so it may be .scale()d. .page .title .heads[name] .lines[name] .section(name)"""

    SECTIONS = (("abstract", 0.30, 4), ("methods", 0.42, 4), ("results", 0.26, 3))

    def __init__(self, w: float = PAPER_W, h: float = PAPER_H, **kw):
        super().__init__(**kw)
        self.page = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=S.GREY,
                                     stroke_width=2).set_fill(S.BG, 1)
        self.add(self.page)
        y = h / 2 - 0.1 * h
        x0 = -0.42 * w

        def bar(width, height, yc, op=0.75, left=True, color=S.GREY):
            r = Rectangle(width=width, height=height, stroke_width=0).set_fill(color, op)
            r.move_to([x0 + width / 2 if left else 0, yc, 0])
            return r

        self.title = VGroup(bar(0.72 * w, 0.034 * h, y, 0.95, False, INK),
                            bar(0.46 * w, 0.034 * h, y - 0.055 * h, 0.95, False, INK))
        self.add(self.title)
        y -= 0.055 * h + 0.085 * h
        self.heads, self.lines = {}, {}
        for name, hw, n in self.SECTIONS:
            hd = bar(hw * w, 0.026 * h, y, 0.95, color=INK)
            y -= 0.05 * h
            ls = VGroup()
            for k in range(n):
                ls.add(bar((0.84 if k < n - 1 else 0.5) * w, 0.015 * h, y))
                y -= 0.044 * h
            y -= 0.035 * h
            self.heads[name], self.lines[name] = hd, ls
            self.add(hd, ls)
        self.w, self.h = w, h

    def section(self, name: str, color: str = DATA, pad: float = 0.045) -> RoundedRectangle:
        """A GREEN chunk outline around one section ("title" or a section name). Not added."""
        g = self.title if name == "title" else VGroup(self.heads[name], self.lines[name])
        x0, x1 = self.page.get_left()[0] + 0.05 * self.w, self.page.get_right()[0] - 0.05 * self.w
        y0, y1 = g.get_bottom()[1] - pad, g.get_top()[1] + pad
        r = RoundedRectangle(width=x1 - x0, height=y1 - y0, corner_radius=0.04, stroke_color=color,
                             stroke_width=2.5).set_fill(color, 0.14)
        return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])

    def ruler_chunks(self) -> VGroup:
        """B18 in our drawing: two fixed-size chunks; the first ends in the middle of a word (the
        abstract's third line), the second runs on into the methods heading. RED. Not added.
        .c1 .c2 .cut .head"""
        L = self.page.get_left()[0] + 0.05 * self.w
        R = self.page.get_right()[0] - 0.05 * self.w
        top = self.title.get_top()[1] + 0.045
        l3 = self.lines["abstract"][2]
        gap = 0.012 * self.h
        yt, yb = l3.get_top()[1] + gap, l3.get_bottom()[1] - gap
        xc = l3.get_left()[0] + 0.55 * l3.width
        yend = self.lines["methods"][0].get_bottom()[1] - gap
        c1 = Polygon([L, top, 0], [R, top, 0], [R, yt, 0], [xc, yt, 0], [xc, yb, 0], [L, yb, 0],
                     stroke_color=ERR, stroke_width=2).set_fill(ERR, 0.08)
        c2 = Polygon([xc, yt, 0], [R, yt, 0], [R, yend, 0], [L, yend, 0], [L, yb, 0], [xc, yb, 0],
                     stroke_color=ERR, stroke_width=2).set_fill(ERR, 0.2)
        cut = Line([xc, yt + 0.06, 0], [xc, yb - 0.06, 0], color=ERR, stroke_width=5)
        hd = self.heads["methods"]
        head = RoundedRectangle(width=hd.width + 0.1, height=hd.height + 0.08, corner_radius=0.03,
                                stroke_color=ERR, stroke_width=3).move_to(hd)
        g = VGroup(c1, c2, cut, head)
        g.c1, g.c2, g.cut, g.head = c1, c2, cut, head
        return g


def good_paper(at=PAPER_R) -> VGroup:
    """The GREEN one-chunk-per-section paper (B19): title, abstract, methods outlined. .paper .boxes"""
    p = MockPaper().move_to(at)
    boxes = VGroup(*[p.section(n) for n in ("title", "abstract", "methods")])
    g = VGroup(p, boxes)
    g.paper, g.boxes = p, boxes
    return g


def x_col(line, col: float) -> float:
    """x of the left edge of character column `col` of a mono_line."""
    return grid_x0(line) + col * cell_width(line.pt)


def literal_safe_rows(prompt: str, cmd: str, limit: int = 65) -> list[str]:
    """fold_cmd's rows for `prompt cmd`, except that a row continuing a '...' literal starts at
    column 0: inside "..." bash drops only the backslash-newline, so the house 4-space indent
    would land inside the literal (here the file name 'outputs/chunks-recursive-split-Tolminc
    Cheese.jsonl' would gain four spaces). Checked: the rows paste back as the captured command."""
    p = prompt + " "
    full = p + cmd
    rows, hard = fold_cmd(full, limit, len(p))
    assert not hard and len(rows) > 1, rows
    levels = _space_levels(full)
    out, start, prefix = [], 0, ""
    for k, r in enumerate(rows):
        assert k == 0 or r.startswith("    "), r
        seg = r[4:] if k else r                 # fold_cmd indents every continuation row by 4
        if k == len(rows) - 1:
            assert full[start:] == seg, (seg, full[start:])
            out.append(prefix + seg)
            break
        assert seg.endswith(" \\"), seg
        seg = seg[:-2]
        j = start + len(seg)
        assert full[start:j] == seg and full[j] == " ", (seg, full[start:j + 1])
        out.append(prefix + seg + " \\")
        start, prefix = j + 1, ("" if levels.get(j) == 2 else "    ")
    assert all(len(r) <= limit for r in out), out
    return out


def type_literal_safe(scene, t, cmd: str, type_time: float):
    """type_cmd for a one-liner whose fold breaks inside a '...' literal (see literal_safe_rows)."""
    p = t.prompt + " "
    rows = literal_safe_rows(t.prompt, cmd, t.max_chars)
    return _type_rows(scene, t, rows, len(p), type_time, len(cmd))


# the rows as bash reads them (it drops each "\" + newline) hold the captured program, file name intact
_typed = "".join(r[:-1] if r.endswith("\\") else r for r in literal_safe_rows(P_CTR, FIRST.cmd))
_typed = _typed[len(P_CTR) + 1:]
assert _typed.startswith("python -c ") and ast.dump(ast.parse(_typed.split('"', 1)[1][:-1])) == \
    ast.dump(ast.parse(FIRST.cmd.split('"', 1)[1][:-1])), _typed


class RecursiveSplit(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        tr = tracker("Chunk", 3)
        mm = MiniMap(MINI_CENTER)

        # ========================================================== 0 · cli.py 196-205: no overlap
        panel = src_panel(*PANEL_SRC)
        panel.move_to([0, 0.05, 0])
        bar197 = panel.bar(197, TURN, 0.22)
        n350 = panel.span(197, "350")
        tail = panel.span(200, "chunk_size)")
        ghost_t = mono("chunk_overlap = ?", 22, S.GREY)
        # a compact dashed box on line 200's row: line 199 runs on above it
        row199 = panel.span(199, "RecursiveCharacterTextSplitter(")
        ghost_b = box(ghost_t.width + 0.3, 0.36, S.GREY, dashed=True, stroke=2.5, radius=0.08)
        ghost = VGroup(ghost_b, ghost_t)
        ghost_t.move_to(ghost_b)
        ghost.next_to(tail, RIGHT, buff=0.4)
        ghost.set_y(tail.get_center()[1] - 0.03)
        assert ghost_b.get_top()[1] < row199.get_bottom()[1], (ghost_b.get_top(), row199.get_bottom())

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), run_time=0.5)
            self.play(FadeIn(panel, shift=UP * 0.3), run_time=0.7)
            vo.wait_until("the same 350")
            self.play(FadeIn(bar197), Indicate(n350, color=TURN, scale_factor=1.3), run_time=0.7)
            self.play(n350.animate.set_color(TURN), run_time=0.3)
            vo.wait_until("No overlap is given")
            self.play(Create(ghost_b), FadeIn(ghost_t), run_time=0.8)
            self.play(Indicate(ghost_t, color=INK, scale_factor=1.08), run_time=0.7)
        self.wait(0.6)

        # ========================================================== 1 · scissors that look for a gap
        lr = lref("B16–B19")
        rb = Ribbon(view=VIEW, breaks=True)
        rb.shift(UP * RIB_Y)
        cap_rb = VGroup(mono("Tolminc Cheese.txt", CAPTION, S.GREY),
                        label("· the first 1,000 characters", CAPTION, S.GREY)).arrange(RIGHT, buff=0.12)
        cap_rb.move_to([6.2 - cap_rb.width / 2, RIB_Y - 0.62, 0])
        seps = [("\\n\\n", "blank line"), ("\\n", "line break"), ('" "', "space"), ('""', "character")]
        chips = VGroup(*[chip(s, TOOL, size=22, font=MONO) for s, _ in seps])
        chips.arrange(RIGHT, buff=0.95).move_to([-0.9, CHIP_Y, 0])
        names = VGroup(*[note(n, INK) for _, n in seps])
        for c, n in zip(chips, names):
            n.next_to(c, DOWN, buff=0.14)
        thens = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.12, color=S.GREY, stroke_width=3,
                               tip_length=0.14) for a, b in zip(chips, chips[1:])])
        here = note("here no paragraph is longer than 350: every cut is a blank line")
        here.move_to([chips.get_center()[0], names.get_bottom()[1] - 0.3, 0])
        sc = scissors_glyph(0.62).rotate(-PI / 2)
        tip_y = RIB_Y + 0.2

        def sc_at(x):
            return np.array([x, tip_y + sc.height / 2, 0])

        sc.move_to(sc_at(rb.x_of(VIEW[0]) - 0.05))
        cuts = VGroup(*[rb.cut(b + 1) for b in ENDS])
        lb_ticks = [m for m in rb.parts["breaks"] if m.get_stroke_width() < 2.5]   # the one line break
        assert len(lb_ticks) == 1, len(lb_ticks)
        callout = rb.callout(CALL_A, CALL_B)
        callout.shift(UP * 0.12)                        # clear of the cut lines' and ticks' tops
        k_seam = SEAM - CALL_A + 1                      # the boundary between the two blanks
        cx = x_col(callout.text, k_seam)
        c_cut = Line([cx, callout.frame.get_top()[1] - 0.04, 0], [cx, callout.frame.get_bottom()[1] + 0.04, 0],
                     color=TOOL, stroke_width=4)
        # the lecture's paper, twice (B18 | B19)
        bad = MockPaper().move_to(PAPER_L)
        bad_marks = bad.ruler_chunks()
        good = good_paper(PAPER_R)
        lab_bad = note("a 200-character ruler", ERR).next_to(bad, DOWN, buff=0.14)
        lab_good = note("a chunk per section", DATA).next_to(good.paper, DOWN, buff=0.14)
        ill = illustration_tag()
        ill.move_to([-0.35 + ill.width / 2, -3.12, 0])

        bad.heads["methods"].set_fill(ERR, 1)
        papers = VGroup(bad, bad_marks, good, lab_bad, lab_good, ill)   # the lecture's picture, quietly

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(panel, bar197, ghost), shift=DOWN * 0.3), FadeIn(lr), FadeIn(mm),
                      FadeIn(papers), run_time=0.7)
            self.play(mm.light("chunking"), LaggedStart(*[FadeIn(b) for b in rb.blocks], lag_ratio=0.004),
                      run_time=1.0)
            self.add(rb)
            self.play(*rb.parts_in("breaks"), FadeIn(cap_rb), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(VGroup(c, n), shift=UP * 0.1) for c, n in zip(chips, names)],
                                  lag_ratio=0.2), FadeIn(thens), FadeIn(sc, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("First a blank line")
            self.play(light(chips[0]), run_time=0.3)
            for b, cl in zip(ENDS, cuts):
                self.play(sc.animate.move_to(sc_at(rb.x_of(b + 1))), run_time=0.3)
                self.play(sc.animate(rate_func=there_and_back).stretch(0.7, 0), Create(cl), run_time=0.22)
            vo.wait_until("then a line break")
            # chip 2 lights and the ribbon's one line break (the short tick) flashes
            self.play(light(chips[0], False), light(chips[1]),
                      Indicate(lb_ticks[0], color=TURN, scale_factor=1.6), run_time=0.7)
            vo.wait_until("then a space")
            self.play(light(chips[1], False), light(chips[2]), run_time=0.3)
            vo.wait_until("and only as a last resort")
            self.play(light(chips[2], False), light(chips[3]), run_time=0.3)
            vo.wait_until("a single character")
            self.play(Indicate(VGroup(chips[3], names[3]), color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("So every cut falls")
            self.play(light(chips[3], False), light(chips[0]), FadeIn(here, shift=UP * 0.1),
                      LaggedStart(*[Indicate(c, color=TURN, scale_factor=1.15) for c in cuts], lag_ratio=0.15),
                      run_time=0.8)
            self.play(FadeIn(callout, shift=DOWN * 0.1), run_time=0.5)
            self.play(Create(c_cut), run_time=0.4)
        self.wait(0.4)

        # ========================================================== 2 · step 3: recursive-split, for real
        t = term(P_CTR, rows=13, container=True)
        beat1 = VGroup(rb, cap_rb, chips, names, thens, here, sc, cuts, callout, c_cut, papers)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(beat1), FadeOut(mm), FadeOut(lr), run_time=0.6)
            self.play(FadeIn(t), run_time=0.35)
            cmd = type_cmd(self, t, CHUNK_CMD, type_time=1.5)
            c_lines = t.print(self, CHUNK_OUT, run_time=0.5)
            l35 = c_lines[5]
            vo.wait_until("The story now makes")
            g35 = substring(l35, "35")
            self.play(g35.animate.set_color(TURN), run_time=0.3)
            u35 = under(g35, TURN)
            pin(self, l35, u35, anim=Create(u35), run_time=0.3)
            self.play(caption_extra(tr, True), run_time=0.3)
            wl = type_cmd(self, t, WC_CMD, type_time=1.1)
            pin(self, wl, beside(extra_tag(), t, wl, buff=0.4), run_time=0.3)
            w_lines = t.print(self, WC_OUT, run_time=0.4)
            ltot = w_lines[1]
            vo.wait_until("gives 14,228")
            gtot = substring(ltot, "14228 total")
            self.play(gtot.animate.set_color(TURN), run_time=0.3)
            utot = under(gtot, TURN)
            pin(self, ltot, utot, anim=Create(utot), run_time=0.3)
            vo.wait_until("Pause and run it")
            yt = your_turn()
            beside(yt, t, cmd, buff=0.4)
            pin(self, cmd, yt, anim=FadeIn(yt, scale=1.2))
        self.wait(2)                                   # ▶ beat: hold the frame

        # ========================================================== 3 · two bars; ponder
        x_bar, full = -2.55, 7.4
        bars, nums, labs, ins = VGroup(), VGroup(), VGroup(), VGroup()
        for i, (name, n) in enumerate((("char-split", COUNTS["char-split"]),
                                       ("recursive-split", COUNTS["recursive-split"]))):
            y = 2.5 - i * 0.72
            w = full * n / COUNTS["recursive-split"]
            b = Rectangle(width=w, height=0.46, stroke_color=DATA, stroke_width=2.5).set_fill(DATA, 0.35)
            b.move_to([x_bar + w / 2, y, 0])
            lb = mono(name, 22, INK)
            lb.move_to([x_bar - 0.25 - lb.width / 2, y, 0])
            num = label(f"{n:,}", 26, INK).next_to(b, RIGHT, buff=0.2)
            size = label("chunk size 350", CAPTION, INK).move_to(b).align_to(b, LEFT).shift(RIGHT * 0.2)
            bars.add(b)
            nums.add(num)
            labs.add(lb)
            ins.add(size)
        probe = ponder_card(PONDER_Q, width=10.2)
        card_y = STRIP_TOP + 0.12 + probe.height / 2

        with self.voiceover(SAY[3]) as vo:
            assert hasattr(wl, "rows") and len(wl.rows) == 2
            keep = [*wl.rows, ltot]
            resize(self, t, 3, keep=keep, run_time=0.7)
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.3),
                      FadeIn(labs), run_time=0.9)
            self.play(FadeIn(ins), FadeIn(nums[0]),
                      TransformFromCopy(substring(ltot, "14228"), nums[1]), run_time=0.7)
            vo.wait_until("So why")
            self.play(Indicate(nums[1], color=TURN, scale_factor=1.2),
                      bars[1].animate(rate_func=there_and_back).set_fill(opacity=0.7), run_time=0.8)
            vo.wait_until("instead of")
            self.play(Indicate(nums[0], color=TURN, scale_factor=1.2),
                      bars[0].animate(rate_func=there_and_back).set_fill(opacity=0.7), run_time=0.8)
        card = ponder_at(self, PONDER_Q, 8, y=card_y)

        # ========================================================== 4 · the first chunks: the overlap
        top_band = 3.17
        default = VGroup(label("library default:", CAPTION, INK), mono("chunk_overlap = 200", 22, INK))
        default.arrange(RIGHT, buff=0.18)
        d_box = box(default.width + 0.44, default.height + 0.24, S.GREY, fill_opacity=0.16, radius=0.2)
        d_box.move_to(default)
        d_chip = VGroup(d_box, default)
        d_chip.move_to([6.45 - d_chip.width / 2, top_band, 0])
        err = erratum_tag("the README says overlapping, not how much")
        err.move_to([6.45 - err.width / 2, 2.6, 0])

        # card, bars and the strip's lines leave together (t.clear, folded into one play). The
        # one-liner is typed before the narration starts: its 12 output rows take its place, so it
        # must stay readable (to pause on and copy) until "Chunk 1 starts again" prints them, about
        # 3 s after it is complete. Typed inside the block, it ran past that anchor.
        self.play(FadeOut(card), FadeOut(VGroup(bars, nums, labs, ins)), FadeOut(t.lines), run_time=0.35)
        for m in list(t.lines):
            t.lines.remove(m)
        resize(self, t, 12, run_time=0.45)
        ol = type_literal_safe(self, t, FIRST.cmd, type_time=1.0)
        pin(self, ol, beside(extra_tag(), t, ol, buff=0.4), run_time=0.25)
        self.wait(0.9)

        with self.voiceover(SAY[4]) as vo:
            vo.wait_until("Chunk 1 starts again")
            # the command (and its tag) fades in place: scrolled up five rows by the print, it swept
            # over the title bar (as S06 says of its 12-row scroll). The output fills the 12 rows.
            t.clear(self, run_time=0.35)
            rows = t.print(self, FIRST_OUT, wrap=True, run_time=0.5)
            assert len(rows) == 12 and rows[0].text == HEAD and rows[4].text == HEAD
            assert rows[2].text == SENT and rows[6].text == SENT
            sep_tag = row_tag("above: the end of chunk 0  ·  below: chunk 1")
            beside(sep_tag, t, rows[3], buff=0.4)
            # chunk 1's start (heading + first sentence), then the same two lines at chunk 0's end
            h1, h0 = substring(rows[4], HEAD), substring(rows[0], HEAD)
            s1, s0 = substring(rows[6], SENT), substring(rows[2], SENT)
            self.play(h1.animate.set_color(TURN), s1.animate.set_color(TURN),
                      FadeIn(sep_tag, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("repeating the end")
            self.play(h0.animate.set_color(TURN), s0.animate.set_color(TURN), run_time=0.5)
            xv = max(r.get_right()[0] for r in rows[0:5]) + 0.3
            ya, yb = rows[0].strut.get_center()[1], rows[4].strut.get_center()[1]
            rep = VMobject(stroke_color=LOOKUP, stroke_width=4)
            rep.set_points_as_corners([[h0.get_right()[0] + 0.15, ya, 0], [xv, ya, 0], [xv, yb, 0],
                                       [h1.get_right()[0] + 0.15, yb, 0]])
            rep_lab = label("repeated", CAPTION, LOOKUP).move_to([xv + 0.2, (ya + yb) / 2, 0], aligned_edge=LEFT)
            self.play(Create(rep), FadeIn(rep_lab, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("The splitter's library default")
            self.play(FadeIn(d_chip, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("up to 200 characters")
            self.play(Indicate(default[1], color=TURN, scale_factor=1.03), run_time=0.6)
            vo.wait_until("which the README never mentions")
            self.play(FadeIn(err, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Cutting at boundaries")
            short = row_tag("chunk 1: 328 characters")
            beside(short, t, rows[11], buff=0.4)
            self.play(FadeIn(short, shift=LEFT * 0.1), run_time=0.5)
            self.play(Indicate(VGroup(*rows[4:12]), color=DATA, scale_factor=1.0), run_time=0.8)

        # ========================================================== 5 · insurance, paid for
        rb2 = Ribbon(view=VIEW)
        rb2.shift(UP * RIB2_Y)
        in_view = [(i, max(a, VIEW[0]), min(b, VIEW[1])) for i, (a, b) in enumerate(RECURSIVE_SPANS)
                   if a < VIEW[1] and b > VIEW[0]]
        cards, nos = VGroup(), VGroup()
        for i, a, b in in_view:
            dy = 0.45 if i % 2 == 0 else 0.8
            c = rb2.span_card(a, b, dy=dy, h=0.22)
            cards.add(c)
            nos.add(label(str(i), CAPTION, DATA).next_to(c, LEFT, buff=0.08))
        overlaps = [(RECURSIVE_SPANS[i + 1][0], b) for i, (a, b) in enumerate(RECURSIVE_SPANS[:-1])
                    if RECURSIVE_SPANS[i + 1][0] < b and RECURSIVE_SPANS[i + 1][0] < VIEW[1]]
        bands = VGroup()
        for a, b in overlaps:
            a, b = max(a, VIEW[0]), min(b, VIEW[1])
            x0, x1 = rb2.x_of(a), rb2.x_of(b)
            y0, y1 = RIB2_Y - 0.2, RIB2_Y + 0.98
            bands.add(Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=0).set_fill(TURN, 0.3)
                      .move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0]))
        coins = VGroup(*[coin_glyph(0.15).move_to([bd.get_center()[0], RIB2_Y + 1.28, 0]) for bd in bands])
        paid = label("embedded, stored, paid for", CAPTION, COST)
        paid.next_to(coins[1], UP, buff=0.18)
        cap2 = VGroup(mono("recursive-split", CAPTION, S.GREY),
                      label("· the story's first chunks · overlaps shaded", CAPTION, S.GREY)).arrange(RIGHT, buff=0.12)
        cap2.move_to([6.2 - cap2.width / 2, RIB2_Y - 0.48, 0])
        hint = VGroup(label("want another value? set", CAPTION, INK), mono("chunk_overlap", 22, INK))
        hint.arrange(RIGHT, buff=0.15)
        h_box = box(hint.width + 0.44, hint.height + 0.24, S.GREY, fill_opacity=0.16, radius=0.2).move_to(hint)
        h_chip = VGroup(h_box, hint).move_to([6.45 - (hint.width + 0.44) / 2, 2.5, 0])
        assert h_chip.get_top()[1] < d_chip.get_bottom()[1] - 0.06, (h_chip.get_top(), d_chip.get_bottom())

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(sep_tag, rep, rep_lab, short, err)), run_time=0.3)
            resize(self, t, 3, keep=[rows[0], rows[3], rows[4]], run_time=0.6)
            self.play(LaggedStart(*[FadeIn(b) for b in rb2.blocks], lag_ratio=0.003), FadeIn(cap2),
                      run_time=0.6)
            self.add(rb2)
            self.play(LaggedStart(*[FadeIn(VGroup(c, n), shift=DOWN * 0.1) for c, n in zip(cards, nos)],
                                  lag_ratio=0.2), run_time=0.8)
            self.play(FadeIn(bands), run_time=0.5)
            vo.wait_until("But every repeated character")
            self.play(LaggedStart(*[FadeIn(c, scale=1.6) for c in coins], lag_ratio=0.25), run_time=0.8)
            self.play(FadeIn(paid, shift=UP * 0.1), run_time=0.5)
            self.play(bands.animate(rate_func=there_and_back).set_fill(opacity=0.6),
                      LaggedStart(*[Indicate(c, color=COST, scale_factor=1.3) for c in coins], lag_ratio=0.2),
                      run_time=1.0)
            vo.wait_until("If you want a different value")
            self.play(FadeIn(h_chip, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(hint[1], color=TURN, scale_factor=1.03), run_time=0.7)

        # ========================================================== 6 · the document's own structure
        lr2 = lref("B16–B19")
        gp = good_paper(PAPER_R)
        big_k = BIG_K
        sec_labs = VGroup()
        ideal = note("ideal: a chunk per section", DATA)
        ill2 = illustration_tag()
        src = VGroup(scissors_glyph(0.6), mono("recursive-split", 22, TOOL)).arrange(RIGHT, buff=0.2)
        src_box = box(src.width + 0.4, src.height + 0.28, TOOL, fill_opacity=0.12, radius=0.2).move_to(src)
        origin = VGroup(src_box, src).move_to([-6.45 + (src.width + 0.4) / 2, 0.45, 0])
        x_start = origin.get_right()[0] + 0.15
        y1, y2 = 0.72, 0.18
        part = Arrow([x_start, y1, 0], [-0.1, y1, 0], buff=0, color=TOOL, stroke_width=5, tip_length=0.22)
        lab_part = label("recursive: paragraphs", CAPTION, TOOL).next_to(part, UP, buff=0.12)
        tick = mm.tick("chunking")

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(t, rb2, cards, nos, bands, coins, paid, cap2, h_chip, d_chip)),
                      FadeIn(lr2), caption_extra(tr, False), run_time=0.6)
            self.play(FadeIn(mm), FadeIn(gp), run_time=0.5)
            self.play(gp.animate.scale(big_k).move_to(PAPER_BIG), run_time=1.0)
            for name, bx in zip(("title", "abstract", "methods"), gp.boxes):
                sec_labs.add(note(name, DATA).next_to(bx, RIGHT, buff=0.18))
            ideal.next_to(gp, UP, buff=0.2)
            ill2.move_to([gp.get_center()[0], gp.get_bottom()[1] - 0.35, 0])
            self.play(LaggedStart(*[Indicate(b, color=DATA, scale_factor=1.04) for b in gp.boxes], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(lb, shift=LEFT * 0.1) for lb in sec_labs], lag_ratio=0.3),
                      FadeIn(ideal), FadeIn(ill2), run_time=1.2)
            vo.wait_until("Recursive splitting goes part")
            x_end = gp.paper.page.get_left()[0] - 0.1
            full_ = DashedLine([x_start, y2, 0], [x_end, y2, 0], color=S.GREY, stroke_width=4, dash_length=0.14)
            full_tip = Arrow([x_end - 0.4, y2, 0], [x_end, y2, 0], buff=0, color=S.GREY, stroke_width=4,
                             tip_length=0.22)
            lab_full = label("semantic chunking · part 2", CAPTION, S.GREY).next_to(full_, DOWN, buff=0.14)
            lab_full.align_to(lab_part, LEFT)
            self.play(FadeIn(origin, shift=RIGHT * 0.2), run_time=0.5)
            self.play(GrowArrow(part), FadeIn(lab_part), run_time=0.9)
            vo.wait_until("Semantic chunking")
            self.play(Create(full_), FadeIn(full_tip), FadeIn(lab_full), run_time=1.0)
            self.play(FadeIn(tick, scale=1.5), run_time=0.4)
            mm.add(tick)
        self.wait(0.6)
        self.play(FadeOut(VGroup(tr, lr2, mm, gp, sec_labs, ideal, ill2, origin, part, lab_part, full_, full_tip,
                                 lab_full)), run_time=0.8)
        self.wait(0.3)
