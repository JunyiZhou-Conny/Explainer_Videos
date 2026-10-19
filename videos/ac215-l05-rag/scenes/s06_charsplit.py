"""S06 · Cutting the books: a ruler (README "Chunk" steps 1–2, three extras). Lecture: A19–A22, B14–B15.

Beats (script.md "## S06", one voiceover block each):
 0  LECTURE A19–A22. TRACKER Chunk 1. The V1 mini-map fades in bottom right, "chunking" lit.
    Center (tag illustration): a GREEN book holds three topic arrows (curd · pasture ·
    grandfather) that Transform into one averaged arrow (the three words give way to the
    caption "one vector, averaged"); three PINK
    questions all land on it and the whole book goes into the prompt card; 11 books pile in, the
    card overflows and turns RED ("slow", "costly", "garbage"). Then the book splits into six
    GREEN cards, each with its own arrow; one question lands next to one card and only that card
    slides into the prompt card. GREY chip "a chunk = what you retrieve = what you paste".
 1  A GREY browser frame (illustration) at ac215-llm-rag.dlops.io/chunkviz: a paragraph of word
    blocks with GREEN chunk bands (YELLOW where windows overlap) and two sliders, "chunk size" and
    "overlap", that move while the bands re-flow. README chip README.md · line 95 "check out this
    visualization" and a GREY note "use Chrome".
 2  V3: the story as a GREEN ribbon of word blocks (~1,000 characters); a PURPLE ruler window of
    350 characters lands on its start; cli.py · lines 184–189 · line 189 wrapped slides in below
    (the mini-map hides); line 185 highlights, its 350 pulses with the ruler and its label; at
    "overlapping by 20" the bar grows over line 186 and its 20 pulses; `separator=''` boxes
    YELLOW; "counts characters": a ripple runs along the ruler's ticks. The ruler steps 330
    characters; the 20-character band glows where the two windows overlap; the counter
    "chunks: 1" goes to 2.
 3  The panel leaves; the ribbon shrinks into its place at the left end of the whole story (GREY
    measure "7,808 characters"), rulers and band with it; the mini-map returns. PONDER (8 s): the
    card in the lower third, left of the mini-map.
 4  The first window ("350") and the second one's new characters ("+330") are named; the equation
    1 + ⌈(7,808 − 350) / 330⌉ writes in ("7,458" over the subtraction); the ruler runs along the
    bar in steps, leaving a PURPLE outline per window, the counter ticks to 24 ("23 more windows"
    under the ceiling); "= 24" writes in and turns YELLOW.
 5  TRACKER Chunk 2. The TEAL container terminal (13 rows, app@92c5bfd26089:/app$; the mini-map
    hides) types `python cli.py --chunk --chunk_type char-split` -> cli-container/10 lines 2–7, …,
    32–34 (2 and 5 cut). `11` and `24` YELLOW; GREY tag "your book order may differ" beside line 6;
    GREY chip "no Google call in char-split's branch" beside `chunk()`; ▶ your turn; GREY card
    "Linux · PermissionError … 'outputs'? / on the laptop: mkdir outputs && chmod a+w outputs" in
    the free rows bottom right. Hold 2 s.
 6  TRACKER Chunk 2 · extra. The terminal clears; `wc -l outputs/chunks-char-split-*.jsonl`
    (extra; its tag in the title bar) -> cli-container/11 lines 2–13 (names cut); `24` and
    `8248 total` YELLOW.
 7  LECTURE B14–B15. The terminal clears; the one-liner of cli-container/12 (extra; it folds onto
    5 rows at 65 characters) -> lines 2–4; the terminal shrinks to the 3-row strip. Above it, the
    two printed lines lift into the seam: `…things she intended to ac` over `s she intended to
    accomplish…`, aligned by character, each in its PURPLE window, the shared 20 characters in a
    YELLOW band; `ac` and the lone `s` underline YELLOW; "accomplish" is whole in chunk 1. Under
    it, the lecture's example: GREY cards "…artificial intelli" | "gence…" end to end, no band
    (tag "lecture example").
 8  The seam and the container strip leave. A second laptop terminal (6 rows, at the bottom; "new
    terminal: cd here first") types `ls -la outputs | head -5` (extra) -> laptop/16 lines 2–6;
    `student student` boxed YELLOW; top right the chip .gitignore · line 4 `/outputs`. Then, above
    the terminal, a PANEL of cli-container/10 lines 8–9 ("python cli.py --chunk … · the first
    book's table"): row 0's text boxed RED, RED tag "erratum · header and license, chunked like
    the rest · see part 2". Fade to an empty frame.

Deviations from SHOW (see the scene report): the one-liner of beat 7 folds onto 5 rows, not 3
(65 characters a row); in beat 5 the book-order tag sits beside line 6 (line 5 is full width) and
the PermissionError card in the free rows at the bottom right (no room beside the ▶); the wc
command fills its row, so its `extra` tag sits in the title bar; the terminal clears before the wc
and the seam commands (a 12-row scroll would sweep over the tracker); in beat 8 the container strip
leaves so that the second terminal shows all five lines while the panel sits above it; the README
command is typed with Terminal.type, which keeps `--chunk_type char-split` on one row.
"""

import re

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Brace,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    TransformFromCopy,
    ValueTracker,
    VGroup,
    Write,
    linear,
    there_and_back,
)

from common import (
    CHAR_SPANS,
    COUNTS,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MINI_CENTER,
    NARRATION,
    P_CTR,
    P_REPO,
    STORY_START,
    STORY_TEXT,
    TOOL,
    TURN,
    Counter,
    MiniMap,
    Ribbon,
    beside,
    capture,
    card_rows,
    caption_extra,
    chunk_card,
    excerpt,
    extra_tag,
    illustration_tag,
    log_panel,
    lref,
    note,
    pin,
    ponder_card,
    readme_chip,
    resize,
    sans,
    second_terminal,
    strip_top,
    source_text,
    src_panel,
    term,
    tracker,
    type_cmd,
    under,
    your_turn,
    example_tag,
)
from explainer import style as S
from explainer.devops import (
    CAPTION,
    MONO,
    browser_window,
    chip,
    glyph_range,
    label,
    mono,
    mono_line,
    substring,
    tag,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ commands and real outputs
CHUNK = capture("10", "cli-container")
CHUNK_CMD = "python cli.py --chunk --chunk_type char-split"            # README.md line 103
assert CHUNK.cmd == CHUNK_CMD and CHUNK.exit == 0
CHUNK_OUT = CHUNK.at((2, 7), "…", (32, 34))
assert CHUNK.line(4) == "Number of files to process: 11", CHUNK.line(4)
assert CHUNK.line(32).endswith("Tolminc Cheese.txt") and CHUNK.line(33) == "Number of chunks: 24"
assert len(CHUNK_OUT) == 10

WC = capture("11", "cli-container")
WC_CMD = "wc -l outputs/chunks-char-split-*.jsonl"
assert WC.cmd == WC_CMD
WC_OUT = WC.at((2, 13))
assert WC.line(11).split()[0] == "24" and WC.line(11).endswith("Tolminc Cheese.jsonl")
assert WC.line(13).split() == ["8248", "total"]

SEAM = capture("12", "cli-container")
assert SEAM.cmd.startswith('python -c "import json;') and SEAM.exit == 0
SEAM_OUT = SEAM.at((2, 4))
assert SEAM.line(2) == "24"
END0 = SEAM.line(3)[1:-1]            # the last 40 characters of chunk 0 (repr quotes dropped)
START1 = SEAM.line(4)[1:-1]          # the first 40 characters of chunk 1
assert END0.endswith("things she intended to ac") and START1.startswith("s she intended to accomplish")
assert END0[-20:] == START1[:20]     # the shared 20 characters
ROW_A = "…" + END0[-25:]             # …things she intended to ac
ROW_B = START1[:28] + "…"            # s she intended to accomplish…
SHIFT_B = 6                          # row B's column 0 sits under row A's column 6 (the s of things)
a0, b0 = CHAR_SPANS[0]
assert STORY_TEXT[a0:b0].endswith(END0) and STORY_TEXT[CHAR_SPANS[1][0]:].startswith(START1)

LS = capture("16", "laptop")
LS_CMD = "ls -la outputs | head -5"
assert LS.cmd == LS_CMD
LS_OUT = LS.at((2, 6))
assert all("student student" in LS.line(n) for n in (3, 4, 5, 6))

TABLE = [CHUNK.line(8), CHUNK.line(9).replace("﻿", "")]   # the BOM is zero-width in a terminal
assert TABLE[1].startswith("0  The Project Gutenberg eBook of"), TABLE[1]
ROW0 = "The Project Gutenberg eBook of The Complete B..."
assert ROW0 in TABLE[1]

GITIGNORE = excerpt(".gitignore", 4, 4)
assert GITIGNORE == "/outputs"
README95 = source_text("README.md").split("\n")[94]
assert "check out this [visualization](https://ac215-llm-rag.dlops.io/chunkviz)" in README95
assert "Use Chrome browser" in source_text("README.md").split("\n")[97]
VIZ_URL = "ac215-llm-rag.dlops.io/chunkviz"

assert len(CHAR_SPANS) == COUNTS["tolminc_char"] == 24 and len(STORY_TEXT) == 7808
assert CHAR_SPANS[1] == (330, 680) and CHAR_SPANS[-1] == (7590, 7808)

PONDER_Q = ("The story is 7,808 characters long.\nWindows of 350 characters overlap by 20.\n"
            "How many chunks?")

# ------------------------------------------------------------------ layout
RIB_Y = 1.75          # beat 2: the ribbon (ruler labels above, the code panel below)
BAR_Y = 1.0           # beats 3-4: the whole story
PANEL_TOP = 0.85
COUNTER_AT = np.array([5.45, 2.45, 0])
BOOK_C = np.array([-4.4, 0.15, 0])        # beat 0: the book (x -6.2..-2.6)
ORIGIN_V = np.array([-4.4, -0.6, 0])      # where the topic arrows start
PROMPT_C = np.array([4.45, 0.45, 0])      # the prompt card


def deg(a: float) -> np.ndarray:
    r = np.radians(a)
    return np.array([np.cos(r), np.sin(r), 0])


def book_glyph(w: float = 3.6, h: float = 2.9, color: str = DATA) -> VGroup:
    """A GREEN book: cover with a spine line. .cover"""
    cover = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color,
                             stroke_width=3).set_fill(color, 0.08)
    spine = Line(cover.get_corner(UP + LEFT) + RIGHT * 0.24, cover.get_corner(DOWN + LEFT) + RIGHT * 0.24,
                 color=color, stroke_width=3)
    g = VGroup(cover, spine)
    g.cover = cover
    return g


def slab(w: float = 2.1, h: float = 0.22, color: str = DATA) -> VGroup:
    """One whole book, lying flat in the prompt card."""
    r = RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color=color,
                         stroke_width=2).set_fill(color, 0.35)
    sp = Line(r.get_corner(UP + LEFT) + RIGHT * 0.14, r.get_corner(DOWN + LEFT) + RIGHT * 0.14,
              color=color, stroke_width=2)
    return VGroup(r, sp)


def vec(origin, a: float, length: float, color: str = DATA, stroke: float = 5) -> Arrow:
    return Arrow(origin, origin + deg(a) * length, buff=0, color=color, stroke_width=stroke,
                 tip_length=0.18, max_tip_length_to_length_ratio=0.3)


def x_of_col(line, col: int) -> float:
    """x of the left edge of character column `col` of a mono_line (from its glyphs)."""
    from common import grid_x0
    from explainer.devops import cell_width
    return grid_x0(line) + col * cell_width(line.pt)


def place_col0(line, x: float, y: float):
    """Shift a mono_line so that its column 0 starts at x and its strut is centred on y."""
    line.shift(np.array([x - x_of_col(line, 0), y - line.strut.get_center()[1], 0]))
    return line


def underline(scene, line, glyphs, color: str = TURN):
    """A YELLOW underline under `glyphs` of terminal line `line`, drawn, then pinned to the line."""
    u = under(glyphs, color)
    pin(scene, line, u, anim=Create(u))
    return u


def row_tag(s: str, color: str = S.GREY, size: float = CAPTION, text_color: str | None = None,
            fill: float = 0.92, tint: bool = False, h: float = 0.36) -> VGroup:
    """A tag that fits inside one terminal row (the house tag is taller than a row). tint=True:
    a chip's faint tint of `color` instead of the opaque background. .box .text"""
    t = label(s, size, text_color or color)
    b = RoundedRectangle(width=t.width + 0.34, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2)
    b.set_fill(color if tint else S.BG, fill)
    bg = b.copy().set_stroke(width=0).set_fill(S.BG, 1)
    t.move_to(b)
    g = VGroup(bg, b, t)
    g.box, g.text = b, t
    return g


def bar_tag(t, mob):
    """Put `mob` at the right end of terminal t's title bar (not added)."""
    y = t.box.get_top()[1] - t.bar_h / 2
    return mob.move_to([t.box.get_right()[0] - 0.22 - mob.width / 2, y, 0])


def with_bg(m, pad: float = 0.08):
    """m on an opaque background patch (a label sitting on a line)."""
    bg = Rectangle(width=m.width + 2 * pad, height=m.height + 2 * pad, stroke_width=0).set_fill(S.BG, 1)
    bg.move_to(m)
    return VGroup(bg, m)


# ------------------------------------------------------------------ beat 1: the visualizer page
class ChunkViz(VGroup):
    """The schematic page of the chunk visualizer: a paragraph of GREY word blocks, GREEN chunk
    bands (two shades, alternating) with YELLOW where two windows overlap, and two sliders. The
    bands and knobs follow the ValueTrackers .size and .overlap (updaters: call .stop())."""

    S_RANGE = (40.0, 140.0)
    O_RANGE = (0.0, 30.0)

    def __init__(self, x0: float = -4.2, width: float = 8.4, top: float = 1.72, per_row: int = 60,
                 n_rows: int = 4, pitch: float = 0.46, size0: float = 100, ov0: float = 0,
                 slider_y=(-0.32, -0.9), **kw):
        super().__init__(**kw)
        self.u, self.x0 = width / per_row, x0
        text = STORY_TEXT[STORY_START:].replace("\n", " ")
        rows, words, rs, last = [], [], 0, 0
        for m in re.finditer(r"\S+", text):
            ws, we = m.start(), m.end()
            if we - rs > per_row:
                rows.append((rs, last))
                if len(rows) == n_rows:
                    break
                rs = ws
            words.append((len(rows), ws, we))
            last = we
        self.rows = rows
        self.ys = [top - r * pitch for r in range(n_rows)]
        self.total = rows[-1][1]
        blocks = VGroup()
        for r, ws, we in words:
            if r >= n_rows:
                continue
            rs_ = rows[r][0]
            xa, xb = x0 + (ws - rs_) * self.u, x0 + (we - rs_) * self.u
            blocks.add(Rectangle(width=max(0.02, xb - xa - 0.03), height=0.16, stroke_width=0)
                       .set_fill(S.GREY, 0.75).move_to([(xa + xb) / 2, self.ys[r], 0]))
        self.size = ValueTracker(size0)
        self.overlap = ValueTracker(ov0)
        self.bands = VGroup(*[Rectangle(width=0.01, height=0.34, stroke_width=0).set_fill(DATA, 0)
                              for _ in range(56)])
        self.bands.add_updater(lambda m: self._layout(m))
        self._layout(self.bands)
        sliders = VGroup()
        self.knobs = []
        for (name, vt, rng), y in zip((("chunk size", self.size, self.S_RANGE),
                                        ("overlap", self.overlap, self.O_RANGE)), slider_y):
            lab = label(name, CAPTION, INK).move_to([x0, y, 0], aligned_edge=LEFT)
            xa, xb = -1.2, 4.0
            track = Line([xa, y, 0], [xb, y, 0], color=S.GREY_DARK, stroke_width=5)
            knob = Dot([xa, y, 0], radius=0.12, color=INK)

            def follow(k, vt=vt, rng=rng, xa=xa, xb=xb, y=y):
                f = (vt.get_value() - rng[0]) / (rng[1] - rng[0])
                k.move_to([xa + f * (xb - xa), y, 0])
            knob.add_updater(follow)
            follow(knob)
            self.knobs.append(knob)
            sliders.add(VGroup(lab, track, knob))
        self.blocks, self.sliders = blocks, sliders
        self.add(self.bands, blocks, sliders)

    def _x(self, i: float, r: int) -> float:
        return self.x0 + (i - self.rows[r][0]) * self.u

    def _segments(self, a: float, b: float):
        out = []
        for r, (rs, re_) in enumerate(self.rows):
            lo, hi = max(a, rs), min(b, re_)
            if hi > lo:
                out.append((self._x(lo, r), self._x(hi, r), self.ys[r]))
        return out

    def _layout(self, m):
        s, o = self.size.get_value(), min(self.overlap.get_value(), self.size.get_value() - 5)
        wins, a = [], 0.0
        while True:
            wins.append((a, min(a + s, self.total)))
            if a + s >= self.total:
                break
            a += s - o
        segs = []
        for k, (a, b) in enumerate(wins):
            for x0, x1, y in self._segments(a, b):
                segs.append((x0, x1, y, DATA, 0.42 if k % 2 == 0 else 0.2))
        for k in range(len(wins) - 1):
            a1, b0_ = wins[k + 1][0], wins[k][1]
            if b0_ > a1:
                for x0, x1, y in self._segments(a1, b0_):
                    segs.append((x0, x1, y, TURN, 0.6))
        for i, r in enumerate(m.submobjects):
            if i < len(segs):
                x0, x1, y, c, op = segs[i]
                r.become(Rectangle(width=max(0.01, x1 - x0), height=0.34, stroke_width=0)
                         .set_fill(c, op).move_to([(x0 + x1) / 2, y, 0]))
            else:
                r.set_fill(opacity=0)

    def stop(self):
        self.bands.clear_updaters()
        for k in self.knobs:
            k.clear_updaters()


class CharSplit(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        tr = tracker("Chunk", 1)
        mm = MiniMap(MINI_CENTER)

        # ========================================================== 0 · why chunk at all
        lr = lref("A19–A22")
        bk = book_glyph().move_to(BOOK_C)
        topics = [("curd", 15), ("pasture", 42), ("grandfather", 150)]
        t_arrows = VGroup(*[vec(ORIGIN_V, a, 1.0) for _, a in topics])
        t_labels = VGroup()
        for (name, a), arr, side in zip(topics, t_arrows, (RIGHT, UP, UP)):
            lb = sans(name, CAPTION, INK).next_to(arr.get_end(), side, buff=0.12)
            t_labels.add(lb)
        t_labels[2].shift(RIGHT * 0.2)          # grandfather: clear of the spine
        mean = sum(deg(a) for _, a in topics) / 3
        avg_deg = float(np.degrees(np.arctan2(mean[1], mean[0])))
        avg = vec(ORIGIN_V, avg_deg, 0.95, stroke=7)
        avg_tip = avg.get_end()
        avg_lab = label("one vector, averaged", CAPTION, DATA)
        avg_lab.move_to([BOOK_C[0], ORIGIN_V[1] - 0.42, 0])
        ill = illustration_tag().move_to([-5.35, -3.2, 0])
        qs = ["how is curd made?", "where is the pasture?", "who is grandfather?"]
        q_cards = VGroup(*[chip(q, LOOKUP, size=CAPTION, fill_opacity=0.12) for q in qs])
        q_cards.arrange(DOWN, buff=0.55).move_to([0.05, 0.6, 0])
        q_arrows = VGroup(*[Arrow(c.get_left(), avg_tip + RIGHT * 0.05, buff=0.1, color=LOOKUP,
                                  stroke_width=4, tip_length=0.16) for c in q_cards])
        pframe = RoundedRectangle(width=2.6, height=2.3, corner_radius=0.14, stroke_color=DATA,
                                  stroke_width=3).set_fill(DATA, 0.05).move_to(PROMPT_C)
        plab = label("prompt", CAPTION, S.GREY).next_to(pframe, DOWN, buff=0.12)
        slabs = VGroup(*[slab() for _ in range(COUNTS["books"])])
        for i, s_ in enumerate(slabs):
            s_.move_to(pframe.get_bottom() + UP * (0.2 + 0.27 * i))
        n_books = label("11 books", CAPTION, DATA).move_to([PROMPT_C[0], 2.72, 0])
        bad = VGroup(tag("slow", ERR), tag("costly", ERR), tag("garbage", ERR)).arrange(RIGHT, buff=0.15)
        bad.next_to(plab, DOWN, buff=0.18)
        cards = VGroup()
        card_dirs = (25, 70, 140, 40, 160, 105)
        for k in range(6):
            c = chunk_card(1.45, 0.62, rows=2).move_to(
                [BOOK_C[0] + (-0.9 if k % 2 == 0 else 0.9), 0.95 - (k // 2) * 0.85, 0])
            ar = vec(c.get_right() + LEFT * 0.36 + DOWN * 0.16, card_dirs[k], 0.3, stroke=4)
            cards.add(VGroup(c, ar))
        hit = cards[3]                                            # the card about curd
        q_hit = Arrow(q_cards[0].get_left(), hit.get_right() + RIGHT * 0.05 + UP * 0.05, buff=0.1,
                      color=LOOKUP, stroke_width=4, tip_length=0.16)
        in_prompt = hit[0].copy().scale(1.4).move_to(PROMPT_C)
        rule = chip("a chunk = what you retrieve = what you paste", S.GREY, size=CAPTION)
        rule.move_to([-1.2, -2.45, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), FadeIn(lr), FadeIn(mm), run_time=0.6)
            self.play(mm.light("chunking"), FadeIn(bk), FadeIn(ill), run_time=0.6)
            self.play(LaggedStart(*[Create(a) for a in t_arrows], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(lb) for lb in t_labels], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("averages its topics")
            # the arrows merge (what became what); the three words make way for one caption
            # (a text-to-text morph between different words passes through an unreadable blob)
            self.play(ReplacementTransform(t_arrows, avg), FadeOut(t_labels, scale=0.8),
                      FadeIn(avg_lab, shift=UP * 0.1), run_time=1.3)
            vo.wait_until("so every question")
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in q_cards], lag_ratio=0.25),
                      run_time=0.8)
            self.play(LaggedStart(*[Create(a) for a in q_arrows], lag_ratio=0.2), run_time=0.8)
            self.play(FadeIn(pframe), FadeIn(plab), TransformFromCopy(bk, slabs[0]), run_time=0.8)
            vo.wait_until("Sending 11 books")
            self.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.3) for s_ in slabs[1:]], lag_ratio=0.15),
                      FadeIn(n_books), run_time=1.6)
            self.play(pframe.animate.set_stroke(ERR, 4), run_time=0.4)
            for t_ in bad:
                self.play(FadeIn(t_, shift=UP * 0.1), run_time=0.45)
            vo.wait_until("A chunk is small")
            self.play(FadeOut(VGroup(slabs, n_books, bad, q_arrows, avg, avg_lab)),
                      pframe.animate.set_stroke(DATA, 3), q_cards[1:].animate.set_opacity(0.3),
                      ReplacementTransform(bk, VGroup(*[c[0] for c in cards])), run_time=0.8)
            self.play(LaggedStart(*[Create(c[1]) for c in cards], lag_ratio=0.1), Create(q_hit),
                      run_time=0.6)
            self.play(hit[0].frame.animate(rate_func=there_and_back).set_stroke(LOOKUP, 6), run_time=0.5)
            self.play(TransformFromCopy(hit[0], in_prompt), FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(VGroup(cards, q_cards, q_hit, in_prompt, pframe, plab, rule, ill)), run_time=0.6)

        # ========================================================== 1 · step 1: the visualizer
        br = browser_window(VIZ_URL, width=9.6, height=4.3).move_to([0, 0.6, 0])
        viz = ChunkViz()
        bill = illustration_tag()          # on the bottom edge: the top edge is the address bar
        bill.move_to(br.frame.get_corner(DOWN + RIGHT) + np.array([-0.3 - bill.width / 2, 0, 0]))
        chip95 = readme_chip("README.md · line 95", "check out this visualization")
        chip95.move_to([-6.25 + chip95.width / 2, -2.3, 0])
        chrome = note("use Chrome").next_to(chip95, RIGHT, buff=0.35)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(br), FadeIn(viz), FadeIn(bill), run_time=0.7)
            self.play(FadeIn(chip95, shift=UP * 0.1), run_time=0.5)
            self.play(viz.size.animate.set_value(60), run_time=1.6)
            vo.wait_until("Open it in Chrome")
            self.play(FadeIn(chrome, shift=LEFT * 0.1), run_time=0.4)
            self.play(viz.overlap.animate.set_value(18), run_time=1.4)
            self.play(viz.size.animate.set_value(125), run_time=1.6)
            self.play(viz.overlap.animate.set_value(8), viz.size.animate.set_value(90), run_time=vo.remaining())
        viz.stop()
        self.play(FadeOut(VGroup(br, viz, bill, chip95, chrome)), run_time=0.6)

        # ========================================================== 2 · the ruler and cli.py 184-189
        rb = Ribbon()
        rb.shift(UP * RIB_Y)
        r0 = rb.ruler(*CHAR_SPANS[0])
        r1 = rb.ruler(*CHAR_SPANS[1])
        band = rb.band(CHAR_SPANS[1][0], CHAR_SPANS[0][1])
        lab350 = label("350 characters", CAPTION, TOOL).move_to([r0.frame.get_center()[0], 2.52, 0])
        lab20 = label("overlap 20", CAPTION, TURN).move_to([band.get_center()[0] + 0.25, 2.52, 0])
        cap_rb = VGroup(mono("Tolminc Cheese.txt", CAPTION, S.GREY),
                        label("· first 1,000 characters", CAPTION, S.GREY))
        cap_rb.arrange(RIGHT, buff=0.12)
        cap_rb.move_to([6.2 - cap_rb.width / 2, RIB_Y - 0.48, 0])
        y_step = RIB_Y - 0.5
        step_ln = Arrow([rb.x_of(0), y_step, 0], [rb.x_of(330), y_step, 0], buff=0, color=TOOL,
                        stroke_width=3, tip_length=0.14)
        step_lab = with_bg(label("step 330", CAPTION, TOOL)).move_to(step_ln.get_center())
        cnt = Counter("chunks", 1)
        # the number (TeX digits) renders smaller than its serif label: match the digit heights
        # (idempotent: k is 1 once common.Counter matches them itself)
        k_num = label("1", 26, INK).height / cnt.num.height
        if abs(k_num - 1) > 0.04:
            cnt.num.scale(k_num, about_edge=LEFT + DOWN)
        cnt.move_to(COUNTER_AT)
        panel = src_panel("cli.py", 184, 189, wrap=True)
        panel.shift(np.array([-panel.get_center()[0], PANEL_TOP - panel.get_top()[1], 0]))
        bar185, bar186 = panel.bar(185, TURN, 0.22), panel.bar(186, TURN, 0.22)
        # lines 185-186 as ONE bar (two line bars overlap and leave a bright seam between them)
        bars56 = Rectangle(width=bar185.width, height=bar185.get_top()[1] - bar186.get_bottom()[1],
                           stroke_width=0).set_fill(TURN, 0.22)
        bars56.move_to([bar185.get_center()[0], (bar185.get_top()[1] + bar186.get_bottom()[1]) / 2, 0])
        span350, span20 = panel.span(185, "350"), panel.span(186, "20")
        sep = panel.span(189, "separator=''")
        sep_box = RoundedRectangle(width=sep.width + 0.16, height=sep.height + 0.16, corner_radius=0.06,
                                   stroke_color=TURN, stroke_width=3).move_to(sep)

        with self.voiceover(SAY[2]) as vo:
            self.play(LaggedStart(*[FadeIn(b) for b in rb.blocks], lag_ratio=0.002), FadeIn(cap_rb),
                      run_time=1.0)
            self.add(rb)
            self.play(FadeIn(r0, shift=DOWN * 0.3), FadeIn(lab350), FadeIn(cnt), run_time=0.7)
            vo.wait_until("Lines 185 and 186")
            self.play(FadeOut(mm), FadeIn(panel, shift=UP * 0.3), run_time=0.7)
            self.play(FadeIn(bar185), run_time=0.5)
            # "...set windows of 350 characters": the 350 of line 185 and the ruler, together. The
            # spoken numbers before it make an interpolated anchor early, so time it back from the
            # next clause instead.
            lead = vo.time_until("overlapping by 20") - 1.4
            if lead > 0.05:
                self.wait(lead)
            self.play(Indicate(span350, color=TOOL, scale_factor=1.3), Indicate(lab350, color=TOOL),
                      r0.frame.animate(rate_func=there_and_back).set_stroke(width=7), run_time=1.0)
            vo.wait_until("overlapping by 20")
            self.play(Transform(bar185, bars56), Indicate(span20, color=TURN, scale_factor=1.3),
                      run_time=0.7)
            vo.wait_until("The separator is empty")
            self.play(Create(sep_box), run_time=0.6)
            vo.wait_until("so it counts")          # counting characters: a ripple along the ticks
            self.play(LaggedStart(*[Indicate(tk, color=TURN, scale_factor=1.8) for tk in r0.ticks],
                                  lag_ratio=0.25), run_time=1.3)
            vo.wait_until("stepping 330")
            self.play(TransformFromCopy(r0, r1), r0.animate.set_stroke(opacity=0.5), Create(step_ln),
                      FadeIn(step_lab), cnt.count_to(2, 0.9), run_time=0.9)
            r1.set_stroke(opacity=1)
            self.play(FadeIn(band), FadeIn(lab20), run_time=0.4)
            self.play(band.animate(rate_func=there_and_back).set_fill(opacity=0.9), run_time=0.8)

        # ========================================================== 3 · zoom out; ponder
        whole = Ribbon(view=(0, len(STORY_TEXT)), blocks=False)
        whole.shift(UP * BAR_Y)
        k = whole.unit / rb.unit
        px = rb.x_of(STORY_START) + STORY_START * whole.unit / (1 - k)    # the fixed point of the zoom
        about = np.array([px, RIB_Y, 0])
        measure_y = BAR_Y + 0.72
        m_line = VGroup(Line([-6.2, measure_y, 0], [6.2, measure_y, 0], color=S.GREY, stroke_width=2),
                        Line([-6.2, measure_y - 0.1, 0], [-6.2, measure_y + 0.1, 0], color=S.GREY, stroke_width=2),
                        Line([6.2, measure_y - 0.1, 0], [6.2, measure_y + 0.1, 0], color=S.GREY, stroke_width=2))
        m_lab = with_bg(label("7,808 characters · the whole story", CAPTION, S.GREY)).move_to([0, measure_y, 0])
        moving = VGroup(rb.blocks, r0, r1, band)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(panel, bar185, bar186, sep_box), shift=DOWN * 0.3),
                      FadeOut(VGroup(lab350, lab20, step_ln, step_lab, cap_rb)), run_time=0.6)
            self.play(moving.animate.stretch(k, 0, about_point=about).shift(DOWN * (RIB_Y - BAR_Y)),
                      run_time=1.2)
            self.add(whole)
            self.bring_to_back(whole)
            self.play(GrowFromEdge(whole, LEFT), run_time=1.0)
            self.remove(moving, rb, rb.blocks)          # the stretched blocks: the bar covers them now
            self.add(r0, r1, band)
            self.play(Create(m_line), FadeIn(m_lab), FadeIn(mm), run_time=0.7)
            vo.wait_until("Windows of 350")
            # at this scale the windows are small: the pulses scale, not only thicken
            self.play(Indicate(r0, color=TOOL, scale_factor=1.5), run_time=0.7)
            self.play(Indicate(r1, color=TOOL, scale_factor=1.5),
                      Indicate(band, color=TURN, scale_factor=1.8), run_time=0.8)
        card = ponder_card(PONDER_Q, width=9.2)
        card[0].set_fill(S.BG, 1)
        card.move_to([-1.55, -1.95, 0])
        if card.get_bottom()[1] < -3.55:
            card.shift(UP * (-3.55 - card.get_bottom()[1]))
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        tbar = card[3]
        self.play(tbar.animate(rate_func=linear).become(tbar.copy().scale(0.001, about_point=tbar.get_start())),
                  run_time=8)

        # ========================================================== 4 · the answer: 24
        new1 = whole.band(CHAR_SPANS[0][1], CHAR_SPANS[1][1], color=TOOL, opacity=0.45)
        l350 = label("350", CAPTION, TOOL).move_to([r0.frame.get_center()[0], BAR_Y - 0.5, 0])
        l330 = label("+330", CAPTION, TOOL).move_to([new1.get_center()[0] + 0.2, BAR_Y - 0.5, 0])
        if l330.get_left()[0] < l350.get_right()[0] + 0.15:
            l330.shift(RIGHT * (l350.get_right()[0] + 0.15 - l330.get_left()[0]))
        eq = VGroup(label("1 +", 32, INK), label("⌈", 32, INK), label("(7,808 − 350)", 32, INK),
                    label("/ 330", 32, INK), label("⌉", 32, INK), label("= 24", 32, INK))
        eq.arrange(RIGHT, buff=0.14).move_to([-0.6, -0.35, 0])
        br_up = Brace(eq[2], UP, buff=0.08, color=S.GREY)
        l7458 = label("7,458", CAPTION, S.GREY).next_to(br_up, UP, buff=0.08)
        br_dn = Brace(VGroup(eq[1], eq[4]), DOWN, buff=0.08, color=S.GREY)
        l23 = label("23 more windows", CAPTION, S.GREY).next_to(br_dn, DOWN, buff=0.08)
        trail = VGroup()
        run = r1

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            self.play(Indicate(r0.frame, color=TOOL, scale_factor=1.25), FadeIn(l350, shift=UP * 0.1),
                      run_time=0.7)
            vo.wait_until("and each one after it")
            self.play(FadeIn(new1), FadeIn(l330, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("7,458 more characters")
            self.play(FadeOut(new1), Write(eq[:5]), run_time=1.0)
            self.play(Create(br_up), FadeIn(l7458), run_time=0.5)
            vo.wait_until("need 23 more windows")
            ghost0 = r0.frame.copy().set_stroke(TOOL, 2, opacity=0.55)
            ghost1 = r1.frame.copy().set_stroke(TOOL, 2, opacity=0.55)
            self.play(FadeOut(r0), FadeIn(ghost0), FadeIn(ghost1), FadeOut(band), run_time=0.3)
            trail.add(ghost0, ghost1)
            for i in range(2, len(CHAR_SPANS)):
                nxt = whole.ruler(*CHAR_SPANS[i])
                g = nxt.frame.copy().set_stroke(TOOL, 2, opacity=0.55)
                self.play(Transform(run, nxt), FadeIn(g), cnt.count_to(i + 1, 0.12), run_time=0.12,
                          rate_func=linear)
                trail.add(g)
            self.play(Create(br_dn), FadeIn(l23), run_time=0.5)
            vo.wait_until("24 chunks")
            self.play(FadeIn(eq[5]), run_time=0.4)
            self.play(eq[5].animate.set_color(TURN), Indicate(cnt, color=TURN, scale_factor=1.15),
                      run_time=0.7)
        cnt.freeze()

        # ========================================================== 5 · step 2: char-split, for real
        t = term(P_CTR, rows=13, container=True)
        p_lines = None
        no_google = row_tag("no Google call in char-split's branch", text_color=INK, fill=0.16, tint=True)
        perm = card_rows(["Linux · PermissionError … 'outputs'?",
                          VGroup(label("on the laptop:", CAPTION, INK),
                                 mono("mkdir outputs && chmod a+w outputs", CAPTION, INK)).arrange(RIGHT, buff=0.15)],
                         buff=0.12)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(whole, run, trail, l350, l330, eq, br_up, l7458, br_dn, l23, cnt,
                                     m_line, m_lab, mm, lr)), tr.goto(2), run_time=0.7)
            self.play(FadeIn(t), run_time=0.4)
            cmd = t.type(self, CHUNK_CMD)
            p_lines = t.print(self, CHUNK_OUT, run_time=0.6)
            ln4, ln6, ln33 = p_lines[2], p_lines[4], p_lines[8]
            vo.wait_until("It reads 11 books")
            g11 = substring(ln4, "11")
            self.play(g11.animate.set_color(TURN), run_time=0.3)
            underline(self, ln4, g11)
            order = row_tag("your book order may differ")
            beside(order, t, ln6, buff=0.5)
            pin(self, ln6, order)
            vo.wait_until("the story gets 24")
            g24 = substring(ln33, "24")
            self.play(g24.animate.set_color(TURN), run_time=0.3)
            underline(self, ln33, g24)
            vo.wait_until("No key needed")
            beside(no_google, t, p_lines[1], buff=0.6)
            self.play(FadeIn(no_google, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Pause and run it")
            yt = your_turn()
            beside(yt, t, cmd, buff=0.4)
            pin(self, cmd, yt, anim=FadeIn(yt, scale=1.2))
            perm.move_to([t.box.get_right()[0] - 0.15 - perm.width / 2, -2.78, 0])
            self.play(FadeIn(perm, shift=UP * 0.1), run_time=0.5)
        self.wait(2)                                   # ▶ beat: hold the frame

        # ========================================================== 6 · extra: wc -l
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(no_google, perm)), caption_extra(tr, True), run_time=0.5)
            t.clear(self)
            wl = type_cmd(self, t, WC_CMD)
            assert len(wl.text) + 8 > t.max_chars          # no room beside it: the tag goes in the bar
            x_wc = bar_tag(t, row_tag("extra"))
            self.play(FadeIn(x_wc), run_time=0.3)
            w_lines = t.print(self, WC_OUT, run_time=0.6)
            l24, ltot = w_lines[9], w_lines[11]
            vo.wait_until("24 for the story")
            g = substring(l24, "24")
            self.play(g.animate.set_color(TURN), run_time=0.3)
            underline(self, l24, g)
            vo.wait_until("8,248 in total")
            g = substring(ltot, "8248 total")
            self.play(g.animate.set_color(TURN), run_time=0.3)
            underline(self, ltot, g)

        # ========================================================== 7 · extra: the seam (B14-B15)
        lr2 = lref("B14–B15")
        row_a = mono_line(ROW_A, 24, INK)
        row_b = mono_line(ROW_B, 24, INK)
        ya, yb = 1.95, 1.05
        xa0 = -2.6
        place_col0(row_a, xa0, ya)
        place_col0(row_b, x_of_col(row_a, SHIFT_B), yb)
        cut_x = x_of_col(row_a, len(ROW_A))
        band_x0 = x_of_col(row_a, SHIFT_B)
        h_row = row_a.strut.height
        pad_cut = 0.1           # the window edges at the cut clear the glyphs ("ac", the lone "s")
        a_left, a_right = x_of_col(row_a, 0) - 0.15, cut_x + pad_cut
        win_a = Rectangle(width=a_right - a_left, height=h_row + 0.3,
                          stroke_color=TOOL, stroke_width=3).set_fill(TOOL, 0.06)
        win_a.move_to([(a_left + a_right) / 2, ya, 0])
        b_left, b_right = band_x0 - pad_cut, x_of_col(row_b, len(ROW_B)) + 0.15
        win_b = Rectangle(width=b_right - b_left, height=h_row + 0.3, stroke_color=TOOL,
                          stroke_width=3).set_fill(TOOL, 0.06)
        win_b.move_to([(b_right + b_left) / 2, yb, 0])
        seam_band = Rectangle(width=cut_x - band_x0, height=ya - yb + h_row + 0.3, stroke_width=0)
        seam_band.set_fill(TURN, 0.22).move_to([(cut_x + band_x0) / 2, (ya + yb) / 2, 0])
        lab_a = label("end of chunk 0", CAPTION, S.GREY)
        lab_a.move_to([win_a.get_left()[0] - 0.25 - lab_a.width / 2, ya, 0])
        lab_b = label("start of chunk 1", CAPTION, S.GREY)
        lab_b.move_to([win_b.get_left()[0] - 0.25 - lab_b.width / 2, yb, 0])
        lab_same = label("the same 20 characters", CAPTION, TURN).move_to([(cut_x + band_x0) / 2, ya + 0.55, 0])
        u_ac = under(substring(row_a, "ac"), TURN, buff=0.06)
        u_s = under(glyph_range(row_b, 0, 1), TURN, buff=0.06)
        acc = substring(row_b, "accomplish")
        lec1 = chip("…artificial intelli", S.GREY, size=22, font=MONO)
        lec2 = chip("gence…", S.GREY, size=22, font=MONO)
        # one string cut in two: put both texts on one baseline (the g's descender centres
        # "gence…" higher in its chip); glyph 1 is an x-height letter in both ('a', 'e')
        lec2.text.shift(UP * (lec1.text[1].get_bottom()[1] - lec1.get_center()[1]
                              - (lec2.text[1].get_bottom()[1] - lec2.get_center()[1])))
        lec_y = -0.35
        lec1.move_to([cut_x - lec1.width / 2, lec_y, 0])
        lec2.move_to([cut_x + lec2.width / 2, lec_y, 0])
        lec_tag = example_tag().next_to(lec1, LEFT, buff=0.3)
        lec_note = note("end to end · no overlap").next_to(VGroup(lec1, lec2), DOWN, buff=0.15)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeIn(lr2), FadeOut(x_wc), run_time=0.4)
            t.clear(self, run_time=0.25)
            sl = type_cmd(self, t, SEAM.cmd, type_time=1.4)
            pin(self, sl, beside(extra_tag(), t, sl, buff=0.4))
            s_lines = t.print(self, SEAM_OUT, run_time=0.4)
            resize(self, t, 3, run_time=0.6)
            vo.wait_until("Chunk 0 stops")
            tgt_a = VGroup(*glyph_range(row_a, 1))
            self.play(TransformFromCopy(substring(s_lines[1], ROW_A[1:]), tgt_a),
                      FadeIn(glyph_range(row_a, 0, 1)), FadeIn(win_a), FadeIn(lab_a), run_time=0.9)
            self.remove(tgt_a, *row_a.glyphs)
            self.add(row_a)
            self.play(Create(u_ac), Indicate(substring(row_a, "ac"), color=TURN, scale_factor=1.3),
                      run_time=0.6)
            vo.wait_until("Chunk 1 backs up")
            tgt_b = VGroup(*glyph_range(row_b, 0, len(ROW_B) - 1))
            self.play(TransformFromCopy(substring(s_lines[2], ROW_B[:-1]), tgt_b),
                      FadeIn(glyph_range(row_b, len(ROW_B) - 1)), FadeIn(win_b), FadeIn(lab_b), run_time=0.9)
            self.remove(tgt_b, *row_b.glyphs)
            self.add(seam_band, row_a, row_b)
            self.play(FadeIn(seam_band), FadeIn(lab_same), run_time=0.6)
            vo.wait_until("to the last letter of things")
            self.play(Create(u_s), Indicate(glyph_range(row_b, 0, 1), color=TURN, scale_factor=1.5),
                      run_time=0.6)
            vo.wait_until("so accomplish is whole")
            self.play(Indicate(acc, color=DATA, scale_factor=1.12), run_time=0.8)
            vo.wait_until("The lecture's pieces")
            self.play(FadeIn(lec1, shift=RIGHT * 0.15), FadeIn(lec2, shift=LEFT * 0.15), run_time=0.6)
            self.play(FadeIn(lec_tag), FadeIn(lec_note), run_time=0.5)

        # ========================================================== 8 · on your laptop; row 0
        g_chip = VGroup(mono(".gitignore", CAPTION, S.GREY), label("· line 4", CAPTION, S.GREY),
                        chip(GITIGNORE, S.GREY, size=CAPTION, font=MONO)).arrange(RIGHT, buff=0.15)
        g_chip.move_to([6.45 - g_chip.width / 2, 3.28, 0])
        panel2 = log_panel(TABLE, "python cli.py --chunk … · the first book's table")
        panel2.shift(UP * (1.0 - panel2.frame.get_bottom()[1]))      # above the 6-row second terminal
        row0 = substring(panel2.rows[1], ROW0)
        row0_box = RoundedRectangle(width=row0.width + 0.2, height=panel2.rows[1].strut.height + 0.1,
                                    corner_radius=0.06, stroke_color=ERR, stroke_width=3)
        row0_box.move_to([row0.get_center()[0], panel2.rows[1].strut.get_center()[1], 0])
        err = tag("erratum · header and license, chunked like the rest · see part 2", ERR)
        err.next_to(panel2.frame, DOWN, buff=0.3).align_to(panel2.frame, LEFT).shift(RIGHT * 0.2)

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(row_a, row_b, win_a, win_b, seam_band, lab_a, lab_b, lab_same, u_ac,
                                     u_s, lec1, lec2, lec_tag, lec_note, lr2, t)), run_time=0.5)
            t2 = second_terminal(self, P_REPO, rows=6, top=strip_top(6))
            ll = type_cmd(self, t2, LS_CMD, type_time=0.9)
            pin(self, ll, beside(extra_tag(), t2, ll, buff=0.4))
            l_lines = t2.print(self, LS_OUT, run_time=0.4)
            own = VGroup(*[substring(l_lines[i], "student student") for i in range(1, 5)])
            own_box = RoundedRectangle(width=own.width + 0.1, height=own.height + 0.16, corner_radius=0.06,
                                       stroke_color=TURN, stroke_width=3).move_to(own)
            self.play(Create(own_box), own.animate.set_color(TURN), FadeIn(g_chip, shift=DOWN * 0.1),
                      run_time=0.5)
            vo.wait_until("Row 0")
            self.play(FadeIn(panel2, shift=DOWN * 0.2), run_time=0.6)
            self.play(Create(row0_box), row0.animate.set_color(ERR), run_time=0.6)
            vo.wait_until("these books start")
            self.play(row0_box.animate(rate_func=there_and_back).set_stroke(width=6), run_time=0.8)
            vo.wait_until("both chunked like the rest")
            self.play(FadeIn(err, shift=UP * 0.1), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(VGroup(tr, t2, own_box, panel2, row0_box, err, g_chip)), run_time=0.8)
        self.wait(0.3)
