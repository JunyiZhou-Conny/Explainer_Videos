"""S04 · A script that is code.

Beats: a small BLUE pen (the agent) writes the pipeline, one GREY file at a time, as each is
named: paper.pdf -> catalog.yaml -> digest.md -> script.md -> scenes/*.py -> output/ (each icon
carries a hint of what is inside: script.md's lines alternate GREY "show" and ORANGE "say"); the
real motto of docs/WORKFLOW.md (A13) types in above, and the chain shows it: it stops at the
script (a pause mark), a faded-BLUE reviewer looks, and it resumes -> the row rises; two catches
pop off the first files: a cataloging sub-agent reads a PDF, not just its name (the file card
flips: redrawn, tagged "reconstruction"), the real filename and arXiv ids in RED, and the
library's 36 PDFs in file order, the 4 wrong ones RED (A41); the real page 270 of the privacy
paper slides in (A14, cropped to the line), the line is underlined in WHITE, and a GREEN sticky
note out of digest.md quotes the digest's erratum -> script.md opens into the real tic-tac-toe
script (A15): its colour line first, then the S03 block, the show line with a GREY bar "the
picture", the say line with an ORANGE bar "spoken word for word", an arrow to the real line of
code that reads it (A16, `SAY = NARRATION["S03"]`, the "S03" lit in both), then the convention
line turns ORANGE and "9!" becomes "nine factorial" -> the page folds back into script.md; two
faded-BLUE reviewers stop the chain there, two GREY clocks (a tick for a sentence, many turns for
a re-render) -> the false start on a UTC time lane (A43): the review lane runs from 15:47; at
16:07 the pen writes the guide's real heading (A13, docs/WORKFLOW.md at 41eca34); at 16:12-16:13
six faded-BLUE builders start while the review is still running; at 16:24 all six turn RED and
fade; the review carries on to 16:30.

Every number on screen is checked in _check() (runs on import): the 36 PDFs and the 4 wrong ones,
the A41 strings, the run times of the false start and their "minutes later" / "eleven minutes",
and that every quoted excerpt is in its asset.

Helpers defined here (not in common.py): doc_icon(), pipe_item(), tip_of(), find_glyphs(),
wrap_to(), flip_faces(), pdf_grid(), sticky_note(), script_panel(), clock_label().
"""

import datetime as dt

import numpy as np
from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AUDIO, BUG, CAPTION, EXCERPTS, INK, MEASURED, NARRATION, PANEL, SUB_AGENT, SUB_AGENT_TEXT,
                    TOOL, asset_text, box, bug_tag, caption, clock, code_block, code_span, dim, emphasize,
                    exhibit, fade_out_all, file_icon, gather, label, mono, pause_icon, pen, person_icon,
                    pin_to_corner, pulse, recon_tag, role_icon, source_caption, strike, time_axis, undim)

SAY = NARRATION["S04"]

A13, A14, A15, A16, A41, A43 = (EXCERPTS[k] for k in ("A13", "A14", "A15", "A16", "A41", "A43"))

# ------------------------------------------------------------------ the real material
# A41: the library's 36 PDFs as first uploaded (commit b035291, literature/pdfs/NN_*.pdf; 19 and
# 33 were never there), in file order. Four were the wrong paper (commit 41eca34 and the catalog
# run record): 18 Cellpose, 20 DCAN, 24 TopoLoss (Hu 2019), 36 MILD-Net.
LIBRARY = [*range(1, 19), *range(20, 33), *range(34, 39)]
MISFILED = {18, 20, 24, 36}
FILENAME = A41["filename"]                       # 20_chen2016dcan_1604.02678.pdf
FILENAME_SHOWN = FILENAME.replace("dcan_", "dcan_\n", 1)     # wrapped on the card, not changed
INSIDE = "inside: a math paper\non topological pressure"      # A41 `inside`: "Topological Pressure of Proper Map"
WRONG_ID, LIKELY_ID = "1604.02678", A41["likely"].split()[-1]  # "most likely arXiv 1604.02677"

# A14: page 270 of the privacy paper (1195 x 1834), cropped to its last two lines of the
# paragraph that defines Lap(λ); the target line "mean 0, and standard deviation λ." spans
# x 117-531 px, baseline at about 1254 px (measured on the png).
PAGE, PAGE_CROP = "dp_paper_p270.png", (100, 1194, 724, 1262)
LINE_X = (117, 531)

# A15: the tic-tac-toe script.md at bb3fc1e (lines 12-22 and 74-84), shown with "…" for cuts.
TTT_SCRIPT = asset_text("ttt_script_excerpt.md")
SCRIPT_PATH = "videos/tictactoe-255168/script.md"
READS = asset_text("code/ttt_s03_stop_28.py")    # A16: SAY = NARRATION["S03"] (s03_stop.py line 28)
NINE = A15["convention"]                         # say "nine factorial", never "9!"

# A43: the false start, Oct 4 (UTC), from the run records and git.
DAY = "2026-10-04"
REVIEW = (f"{DAY} {A43['review_lane']['start']}", f"{DAY} {A43['review_lane']['end']}")
GUIDE_AT = f"{DAY} {A43['guide_committed']}"
STARTS = [f"{DAY} {t}" for t in A43["builders"]["started"]]
KILLED = f"{DAY} {A43['builders']['killed']}"
LANE_T0, LANE_T1 = f"{DAY} 15:40", f"{DAY} 16:35"


def _t(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s)


def _paragraphs(md: str) -> list[str]:
    """The excerpt's paragraphs: a heading, a bullet or a SHOW/SAY line, with its continuation lines."""
    out, blank = [], True
    for ln in md.splitlines():
        starts = ln.startswith(("- ", "SHOW:", "SAY:", "#", "Conventions"))
        if ln.strip() and out and not blank and not starts:
            out[-1] += " " + ln.strip()
        elif ln.strip():
            out.append(ln.strip())
        blank = not ln.strip()
    return out


PARAS = _paragraphs(TTT_SCRIPT)


def _para(start: str) -> str:
    return next(p for p in PARAS if p.startswith(start))


def _pick(p: str, *pieces: str) -> str:
    """Pieces of paragraph p, in order, joined by "…" (a cut); a final "…" if p goes on."""
    i = 0
    for x in pieces:
        i = p.index(x, i) + len(x)
    return " … ".join(pieces) + ("" if i == len(p) else " …")


DOC = [  # (role, text): the script.md excerpt as shown, in file order
    ("head", _para("Conventions")),
    ("conv", _pick(_para("- `SAY:` lines are spoken verbatim"), "- `SAY:` lines are spoken verbatim", NINE + ".")),
    ("gap", "…"),
    ("colour", _pick(_para("- Semantic colours"), "- Semantic colours (fixed for the whole video): **X** = BLUE · **O** = ORANGE ·")),
    ("gap", "…"),
    ("s03", _para("## S03")),
    ("show", _pick(_para("SHOW: A game plays"), "SHOW: A game plays move by move with move numbers in the squares",
                   "X wins on move 5 (YELLOW top row).")),
    ("say", _para("SAY: Here's the catch.")),
]


def _check():
    # A41: 36 PDFs, 4 of them the wrong paper; the DCAN file is one of them
    assert len(LIBRARY) == 36 and len(MISFILED) == 4 and MISFILED <= set(LIBRARY)
    assert FILENAME == "20_chen2016dcan_1604.02678.pdf" and int(FILENAME[:2]) in MISFILED
    assert A41["tally"] == "4 of 36 PDFs: the wrong paper"
    assert WRONG_ID in FILENAME and LIKELY_ID == "1604.02677"
    assert FILENAME_SHOWN.replace("\n", "") == FILENAME
    # A14 / A15 / A16: the excerpts shown are in their assets
    assert A14["page_line"] == "mean 0, and standard deviation λ."
    assert NINE in DOC[1][1] and "S03" in READS and READS == A16["scene_reads"]
    flat = " ".join(TTT_SCRIPT.split())
    for role, text in DOC:
        for piece in text.split(" … "):
            assert piece.removesuffix(" …") in flat or piece == "…", piece[:40]
    # A43: 3 runs x 2 agents, started 16:12:55-16:13:15, killed 16:24:19; guide at 16:07
    b = A43["builders"]
    assert b["runs"] * b["agents_per_run"] == 6 and len(STARTS) == b["runs"]
    assert _t(REVIEW[0]) < _t(GUIDE_AT) < min(map(_t, STARTS)) < _t(KILLED) < _t(REVIEW[1])
    assert 5 <= (min(map(_t, STARTS)) - _t(GUIDE_AT)).total_seconds() / 60 <= 7      # "Minutes later"
    for s in STARTS:                                                                  # "Eleven minutes"
        assert round((_t(KILLED) - _t(s)).total_seconds() / 60) == 11
    assert _t(LANE_T0) < _t(REVIEW[0]) and _t(REVIEW[1]) < _t(LANE_T1)


_check()

# ------------------------------------------------------------------ layout
ROW_X = [-5.5, -3.3, -1.1, 1.1, 3.3, 5.5]
ICON_H = 0.95
ROW_Y0 = 0.1                     # the row while it is written (beat 1)
ROW_Y1 = 2.75                    # the row at the top (beats 2 and 4)
NAME_SIZE = 22
FILES = [("paper.pdf", None, "pdf"), ("catalog.yaml", None, "yaml"),
         ("digest.md", "page numbers + errata", "md"), ("script.md", None, "script"),
         ("scenes/*.py", None, "py"), ("output/", "mp4, subtitles,\nchapters", "out")]
PHRASES = ["a paper", "a catalog entry", "a digest", "a script,", "animation code", "and the video"]
DOC_SIZE = 22
PANEL_L, PANEL_R = -6.5, 1.75    # the script.md page (beat 3)
PANEL_TOP = 3.45


# ------------------------------------------------------------------ helpers (this scene only)
def doc_icon(kind: str, height: float = ICON_H) -> VGroup:
    """A GREY file with a hint of its contents drawn inside (no text): 'pdf' text lines, 'yaml'
    key/value rows, 'md' notes, 'script' alternating GREY show / ORANGE say lines, 'py' indented
    code, 'out' a frame with a subtitle. .page .fold .marks"""
    w, h, f = height * 0.78, height, height * 0.26
    page = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - f, 0], [w / 2 - f, h / 2, 0],
                   [-w / 2, h / 2, 0], stroke_color=TOOL, stroke_width=2.5).set_fill(PANEL, 1)
    fold = Polygon([w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0], [w / 2, h / 2 - f, 0],
                   stroke_color=TOOL, stroke_width=2).set_fill(TOOL, 0.5)
    left, sw = -w * 0.32, 2.2
    ys = [h * 0.2 - k * h * 0.15 for k in range(5)]
    marks = VGroup()

    def seg(x0, x1, y, col=TOOL, width=sw):
        return Line([x0, y, 0], [x1, y, 0], stroke_width=width, color=col)

    if kind == "pdf":
        marks.add(seg(left, left + w * 0.38, ys[0] + 0.03, width=3.2))
        marks.add(*[seg(left, left + w * fr, y) for fr, y in zip((0.64, 0.64, 0.52, 0.64), ys[1:])])
    elif kind == "yaml":
        for k, y in enumerate(ys[:4]):
            marks.add(seg(left, left + w * 0.18, y), seg(left + w * 0.26, left + w * (0.62 - 0.08 * (k % 2)), y))
    elif kind == "md":
        marks.add(seg(left, left + w * 0.3, ys[0] + 0.03, width=3.2))
        marks.add(*[seg(left + (0.06 if k % 2 else 0), left + w * fr, y)
                    for k, (fr, y) in enumerate(zip((0.64, 0.56, 0.64, 0.46), ys[1:]))])
    elif kind == "script":
        for k, y in enumerate(ys[:4]):
            col = TOOL if k % 2 == 0 else AUDIO
            marks.add(seg(left, left + w * (0.64 if k % 2 == 0 else 0.56), y, col, 2.6))
    elif kind == "py":
        for ind, fr, y in zip((0, 0.1, 0.2, 0.2, 0.1), (0.5, 0.46, 0.34, 0.42, 0.36), ys):
            marks.add(seg(left + w * ind, left + w * (ind + fr), y))
    elif kind == "out":
        scr = Rectangle(width=w * 0.62, height=w * 0.35, stroke_color=TOOL, stroke_width=2)
        scr.set_fill(TOOL, 0.25).move_to([left + w * 0.31, ys[0] - 0.04, 0])
        tri = Triangle(stroke_width=0).set_fill(TOOL, 0.9).rotate(-PI / 2).scale_to_fit_height(w * 0.16)
        tri.move_to(scr)
        marks.add(scr, tri, seg(left + w * 0.06, left + w * 0.56, ys[3]), seg(left + w * 0.12, left + w * 0.5, ys[4]))
    g = VGroup(page, fold, marks)
    g.page, g.fold, g.marks = page, fold, marks
    return g


class PipeItem(VGroup):
    """pipe_item(): .icon .name .note (or None)."""


def pipe_item(name: str, note: str | None, kind: str) -> PipeItem:
    ic = doc_icon(kind)
    nm = mono(name, NAME_SIZE, INK).next_to(ic, DOWN, buff=0.18)
    g = PipeItem(ic, nm)
    g.icon, g.name, g.note = ic, nm, None
    if note:
        n = caption(note, CAPTION, line_spacing=0.85).next_to(nm, DOWN, buff=0.1)
        g.add(n)
        g.note = n
    return g


def tip_of(p: VGroup) -> np.ndarray:
    """The writing tip of common.pen(): the lowest vertex of its nib."""
    v = p[1].get_vertices()
    return v[np.argmin(v[:, 1])]


def find_glyphs(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` inside Text t (empty if it isn't there, e.g. in another language).
    Works with disable_ligatures=True (one glyph per character, spaces included) and with the
    usual layout (no glyphs for spaces)."""
    s = getattr(t, "original_text", None) or getattr(t, "text", "")
    i = s.find(sub)
    if i < 0:
        return VGroup()
    if len(t.submobjects) == len(s):
        return VGroup(*t.submobjects[i:i + len(sub)])
    if len(t.submobjects) == len("".join(s.split())):
        a = len("".join(s[:i].split()))
        return VGroup(*t.submobjects[a:a + len("".join(sub.split()))])
    return VGroup()


def wrap_to(s: str, size: float, max_w: float, indent: str = "", keep: str | None = None) -> list[str]:
    """s word-wrapped to max_w (measured in the house font), continuation lines prefixed by
    `indent`; no break is put inside the phrase `keep`, nor before a "…"."""
    glue = "\u0000"
    s2 = s.replace(keep, keep.replace(" ", glue)) if keep and keep in s else s
    s2 = s2.replace(" …", glue + "…")          # a cut mark stays with the word before it
    lines, cur = [], ""
    for w in s2.split(" "):
        t = f"{cur} {w}" if cur else w
        if cur and label(((indent if lines else "") + t).replace(glue, " "), size).width > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    out = [(indent if k else "") + ln.replace(glue, " ") for k, ln in enumerate(lines)]
    assert " ".join(x.strip() for x in out) == " ".join(s.split())
    return out


def flip_faces(width: float = 4.75, height: float = 1.35):
    """The catalog moment, redrawn: a file card (PDF icon + the real filename), and its back
    (what the agent found inside). Returns (front, back); back.tag is the 'reconstruction' tag."""
    fb = box(width, height, TOOL, fill=PANEL, fill_opacity=1, radius=0.14)
    ic = doc_icon("pdf", 0.75)
    nm = mono(FILENAME_SHOWN, 24, INK, line_spacing=0.9)
    body = VGroup(ic, nm).arrange(RIGHT, buff=0.22).move_to(fb)
    front = VGroup(fb, body)
    bb = box(width, height, TOOL, fill=PANEL, fill_opacity=1, radius=0.14)
    txt = label(INSIDE, 26, INK, line_spacing=0.9).move_to(bb).shift(DOWN * 0.1)
    back = VGroup(bb, txt)
    t = recon_tag()
    t.move_to(bb.get_corner(UR) + np.array([-t.width / 2 - 0.15, 0, 0]))     # straddles the top edge
    back.add(t)
    back.tag = t
    return front, back


def pdf_grid(cols: int = 6, h: float = 0.3) -> VGroup:
    """The library's 36 PDFs in file order (small GREY files); .wrong = the 4 misfiled ones."""
    tiles = VGroup(*[file_icon(h, TOOL) for _ in LIBRARY]).arrange_in_grid(cols=cols, buff=(0.12, 0.1))
    tiles.wrong = VGroup(*[t for t, n in zip(tiles, LIBRARY) if n in MISFILED])
    return tiles


def turn_red(tile: VGroup) -> VGroup:
    """A copy of a small file icon in RED (the wrong paper)."""
    t = tile.copy()
    t[0].set_stroke(BUG).set_fill(BUG, 0.3)
    t[1].set_stroke(BUG).set_fill(BUG, 0.6)
    t[2].set_stroke(BUG)
    return t


def sticky_note(text: str, width: float | None = None) -> VGroup:
    """A GREEN sticky note (a measured check): the digest's own words, exact. .box .text"""
    t = label(text, 26, INK, line_spacing=0.95)
    w = width or t.width + 0.6
    b = box(w, t.height + 0.5, MEASURED, fill_opacity=0.16, radius=0.08)
    corner = Polygon(b.get_corner(DR) + LEFT * 0.32, b.get_corner(DR) + UP * 0.32, b.get_corner(DR),
                     stroke_width=0).set_fill(S.BG, 1)
    fold = Polygon(b.get_corner(DR) + LEFT * 0.32, b.get_corner(DR) + UP * 0.32,
                   b.get_corner(DR) + np.array([-0.32, 0.32, 0]), stroke_color=MEASURED, stroke_width=2)
    fold.set_fill(MEASURED, 0.45)
    t.move_to(b)
    g = VGroup(b, corner, fold, t)
    g.box, g.text = b, t
    return g


class ScriptPanel(VGroup):
    """script_panel(): .frame .bar .title .rows (one Text per line) and .parts[role] -> VGroup of
    the lines of that paragraph."""


def script_panel() -> ScriptPanel:
    """The real tic-tac-toe script.md, as a page: a GREY frame with its path in a title bar, the
    excerpt's lines in the house font (one Text per line, ligatures off so phrases can be found)."""
    max_w = PANEL_R - PANEL_L - 0.55
    rows, parts = VGroup(), {}
    y = PANEL_TOP - 0.82
    step = 0.355
    for role, text in DOC:
        indent = "  " if text.startswith("- ") else ""
        keep = NINE if role == "conv" else None
        lines = [text] if role in ("head", "gap") else wrap_to(text, DOC_SIZE, max_w, indent, keep)
        grp = VGroup()
        if role in ("s03", "show", "colour") or (role == "head" and rows):
            y -= 0.1
        for ln in lines:
            t = label(ln, DOC_SIZE, INK, disable_ligatures=True)
            t.move_to([0, y, 0]).align_to([PANEL_L + 0.3, 0, 0], LEFT)
            grp.add(t)
            rows.add(t)
            y -= step
        parts.setdefault(role, VGroup()).add(*grp)
    bottom = y + step - 0.3
    frame = box(PANEL_R - PANEL_L, PANEL_TOP - bottom, TOOL, fill=PANEL, fill_opacity=1, radius=0.16)
    frame.move_to([(PANEL_L + PANEL_R) / 2, (PANEL_TOP + bottom) / 2, 0])
    ttl = VGroup(file_icon(0.36), mono(SCRIPT_PATH, 20, INK)).arrange(RIGHT, buff=0.16)
    ttl.move_to([0, PANEL_TOP - 0.3, 0]).align_to(frame, LEFT).shift(RIGHT * 0.25)
    bar = Line([PANEL_L + 0.05, PANEL_TOP - 0.58, 0], [PANEL_R - 0.05, PANEL_TOP - 0.58, 0],
               color=S.GREY_DARK, stroke_width=2)
    g = ScriptPanel(frame, bar, ttl, rows)
    g.frame, g.bar, g.title, g.rows, g.parts = frame, bar, ttl, rows, parts
    return g


def side_bar(lines: VGroup, color: str, x: float, stroke: float = 7) -> Line:
    """A vertical bar beside some lines of the page (outside its right edge)."""
    return Line([x, lines.get_top()[1] + 0.02, 0], [x, lines.get_bottom()[1] - 0.02, 0], color=color,
                stroke_width=stroke)


def clock_label(top: str, bottom: str) -> VGroup:
    """Two-line GREY-ish caption under a clock: the case, then its cost (WHITE)."""
    return VGroup(label(top, 24, TOOL), label(bottom, 26, INK)).arrange(DOWN, buff=0.1)


# ------------------------------------------------------------------ the scene
class ScriptIsCode(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- the pipeline is a chain of files
        items = [pipe_item(n, note, kind) for n, note, kind in FILES]
        for it, x in zip(items, ROW_X):
            it.shift(np.array([x, ROW_Y0, 0]) - it.icon.get_center())
        arrows = [Arrow(a.icon.get_right() + RIGHT * 0.12, b.icon.get_left() + LEFT * 0.12, buff=0, color=TOOL,
                        stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.25)
                  for a, b in zip(items, items[1:])]
        track = DashedLine([ROW_X[0] - 0.75, ROW_Y0, 0], [ROW_X[-1] + 0.75, ROW_Y0, 0], dash_length=0.09,
                           dashed_ratio=0.45, color=TOOL, stroke_width=2).set_opacity(0.55)
        quill = pen(0.62, S.BLUE)
        quill.shift(track.get_start() + UP * 0.5 - tip_of(quill))
        motto = label("“" + A13["motto"] + "”", 30, INK).move_to([0, 2.05, 0])
        src0 = source_caption("motto: " + A13["src"])
        pause = VGroup(Rectangle(width=0.42, height=0.42, stroke_width=0).set_fill(S.BG, 1), pause_icon(0.28, INK))
        pause.move_to(arrows[3].get_center())
        reviewer = role_icon("sub", 0.75)
        reviewer.move_to([ROW_X[3], ROW_Y0 - 1.75, 0])
        downstream = VGroup(arrows[3], arrows[4], items[4], items[5])

        def pen_to(it, dx=0.0):
            spot = it.icon.get_center() + np.array([0.12 + dx, -0.02, 0])
            return quill.animate.shift(spot - tip_of(quill))

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(quill, shift=RIGHT * 0.4), run_time=0.5)
            self.play(Create(track), quill.animate(rate_func=there_and_back).shift(UP * 0.35 + RIGHT * 0.25),
                      run_time=vo.until("a paper") - 0.45)
            for k, (it, phrase) in enumerate(zip(items, PHRASES)):
                vo.wait_until(phrase)
                self.play(pen_to(it, -0.18), *([GrowArrow(arrows[k - 1])] if k else []), run_time=0.3)
                extra = [FadeIn(it.note, shift=UP * 0.08)] if it.note is not None else []
                self.play(Create(it.icon.page), FadeIn(it.icon.fold),
                          LaggedStart(*[Create(m) for m in it.icon.marks], lag_ratio=0.15),
                          pen_to(it, 0.2), FadeIn(it.name, shift=UP * 0.08), *extra,
                          run_time=0.45, rate_func=smooth)
            vo.wait_until("Every step leaves")
            self.play(FadeOut(quill, shift=UP * 0.3), FadeOut(track), run_time=0.4)
            self.play(AddTextLetterByLetter(motto, time_per_char=0.03), FadeIn(src0), run_time=1.6)
            vo.wait_until("so you can stop")
            self.play(FadeIn(pause, scale=0.5), *dim(downstream, opacity=0.35), run_time=0.45)
            vo.wait_until("review,")
            self.play(FadeIn(reviewer, shift=UP * 0.25), run_time=0.45)
            vo.wait_until("and resume")
            self.play(FadeOut(pause, scale=0.5), *undim(downstream), run_time=0.45)
            self.play(ShowPassingFlash(VGroup(arrows[3].copy(), arrows[4].copy()).set_color(S.WHITE).set_stroke(width=5),
                                       time_width=0.6), run_time=0.6)

        # ---------------------------------------------------------- each file gets checked
        row = gather(self, *items, *arrows)
        lift = UP * (ROW_Y1 - ROW_Y0)

        # catch 1: the catalog agents read the PDFs
        reader = role_icon("sub", 0.95).move_to([-5.95, 0.3, 0])
        front, back = flip_faces()
        VGroup(front, back).move_to([-2.85, 0.3, 0])
        red_line = VGroup(mono(WRONG_ID, 22, BUG), label("· DCAN is most likely", 22, BUG),
                          mono(LIKELY_ID, 22, BUG)).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        red_line.move_to([0, -0.72, 0]).align_to([-6.45, 0, 0], LEFT)
        grid = pdf_grid(cols=9, h=0.36).move_to([0, -2.12, 0]).align_to([-6.3, 0, 0], LEFT)
        tally = bug_tag("4 of 36 PDFs:\nthe wrong paper", size=26).next_to(grid, RIGHT, buff=0.4)
        src1 = source_caption("file names: the library as uploaded · finding: the catalog run record")

        # catch 2: the digest lists the paper's own mistakes
        page = exhibit(PAGE, width=5.9, crop=PAGE_CROP).move_to([0, 0.45, 0]).align_to([6.45, 0, 0], RIGHT)
        under = Line(page.px(LINE_X[0], PAGE_CROP[3]) + DOWN * 0.08, page.px(LINE_X[1], PAGE_CROP[3]) + DOWN * 0.08,
                     color=S.WHITE, stroke_width=5)
        page_cap = caption("real page · the privacy paper, p. 270").next_to(under, DOWN, buff=0.14)
        page_cap.align_to(page, LEFT)
        note = sticky_note(A14["digest_note"].replace(" — ", "\n— ", 1)).rotate(1.5 * DEGREES)
        note.move_to([page.get_x(), -1.55, 0])
        note_cap = caption("the privacy video's digest.md · lines 29–30").next_to(note, DOWN, buff=0.16)
        note_cap.align_to(note, RIGHT)

        with self.voiceover(SAY[1], pad=1.4) as vo:
            self.play(FadeOut(motto), FadeOut(src0), FadeOut(reviewer), row.animate.shift(lift), run_time=0.9)
            self.play(LaggedStart(*[AnimationGroup(pulse(it.icon, 1.12, run_time=0.5),
                                                   it.icon.page.animate(rate_func=there_and_back, run_time=0.5)
                                                   .set_stroke(S.WHITE, 4)) for it in items],
                                  lag_ratio=0.15), run_time=1.0)
            vo.wait_until("Agents cataloging")
            self.play(*dim(items[3], items[4], items[5], *arrows[2:], opacity=0.35),
                      FadeIn(front, target_position=items[0].icon.get_center(), scale=0.3),
                      FadeIn(reader, target_position=items[1].icon.get_center(), scale=0.5), run_time=0.8)
            self.play(Circumscribe(front, color=S.WHITE, buff=0.06, run_time=0.8))
            vo.wait_until("read them")
            back.save_state()
            back.stretch(0.02, 0)
            self.play(front.animate(rate_func=rush_into).stretch(0.02, 0), run_time=0.3)
            self.remove(front)
            self.add(back)
            self.play(Restore(back, rate_func=rush_from), run_time=0.3)
            vo.wait_until("and found that")
            self.play(FadeIn(red_line, shift=UP * 0.1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in grid], lag_ratio=0.02), FadeIn(src1), run_time=0.9)
            vo.wait_until("were the wrong papers")
            self.play(*[Transform(t, turn_red(t)) for t in grid.wrong], FadeIn(tally, shift=LEFT * 0.15), run_time=0.6)
            self.play(LaggedStart(*[Indicate(t, color=S.WHITE, scale_factor=1.35) for t in grid.wrong], lag_ratio=0.15),
                      run_time=0.8)

            vo.wait_until("And the privacy digest")
            self.play(*dim(reader, back, red_line, grid, tally, src1, opacity=0.55),
                      FadeIn(page, shift=LEFT * 0.6), FadeIn(page_cap), run_time=0.7)
            self.play(Create(under), run_time=0.45)
            vo.wait_until("lists the paper's")
            self.play(TransformFromCopy(items[2].icon, note, path_arc=-PI / 6), run_time=0.8)
            self.play(FadeIn(note_cap, shift=UP * 0.08), emphasize(note.text, run_time=0.8))

        # ---------------------------------------------------------- the script: show lines and say lines
        panel = script_panel()
        conv, colour, s03, show, say = (panel.parts[k] for k in ("conv", "colour", "s03", "show", "say"))
        rest = VGroup(*[r for r in panel.rows if r not in colour])
        bar_x = PANEL_R + 0.16
        show_bar, say_bar = side_bar(show, TOOL, bar_x), side_bar(say, AUDIO, bar_x)
        show_l = label("the picture", 26, TOOL).next_to(show_bar, RIGHT, buff=0.2)
        say_l = label("spoken word\nfor word", 26, AUDIO, line_spacing=0.9).next_to(say_bar, RIGHT, buff=0.2)
        chip = code_block(READS, font_size=20)
        chip.move_to([0, s03.get_y() + 0.42, 0]).align_to([6.45, 0, 0], RIGHT)
        chip_cap = caption("s03_stop.py · line 28").next_to(chip, DOWN, buff=0.1).align_to(chip, LEFT)
        reads_l = label("the scene reads this file", 24, TOOL).next_to(chip, UP, buff=0.14).align_to(chip, LEFT)
        reads_arrow = CurvedArrow(say_l.get_right() + RIGHT * 0.15, chip.get_corner(DR) + np.array([-0.45, -0.06, 0]),
                                  angle=PI / 2, color=AUDIO, stroke_width=3, tip_length=0.16)
        src2 = source_caption("real file · the tic-tac-toe video's script.md (commit bb3fc1e); “…” marks a cut")
        nine_line = next(r for r in conv if NINE in (getattr(r, "original_text", "") or ""))
        nine = find_glyphs(nine_line, NINE)
        sym = mono("9!", 32, INK)
        words = label("nine factorial", 30, AUDIO)
        swap = VGroup(sym, Arrow(LEFT * 0.35, RIGHT * 0.35, buff=0, color=TOOL, stroke_width=3, tip_length=0.15),
                      words).arrange(RIGHT, buff=0.18)
        swap.move_to([0, nine_line.get_y(), 0]).align_to([6.45, 0, 0], RIGHT)
        sym_strike = strike(sym, stroke=5, pad=0.06)
        s03_glyphs = find_glyphs(s03[0], "S03")
        chip_s03 = code_span(chip, 0, "S03")
        script_item = items[3]
        others = [it for it in items if it is not script_item]

        with self.voiceover(SAY[2]) as vo:
            gone = gather(self, reader, back, red_line, grid, tally, src1, page, page_cap, under, note, note_cap)
            self.play(FadeOut(gone), *[FadeOut(m) for m in (*others, *arrows)],
                      ReplacementTransform(script_item.icon, panel.frame),
                      ReplacementTransform(script_item.name, panel.title), FadeIn(panel.bar), run_time=1.0)
            rest.set_opacity(0.3)
            self.play(FadeIn(panel.rows), FadeIn(src2), run_time=0.6)
            self.play(Circumscribe(colour, color=S.WHITE, buff=0.08, run_time=0.8))
            vo.wait_until("a show line")
            self.play(colour.animate.set_opacity(0.3), VGroup(s03, show, say).animate.set_opacity(1), run_time=0.5)
            self.play(Create(show_bar), run_time=0.35)
            vo.wait_until("the picture")
            self.play(FadeIn(show_l, shift=LEFT * 0.15), run_time=0.45)
            vo.wait_until("with a say line")
            self.play(Create(say_bar), run_time=0.35)
            self.play(FadeIn(say_l, shift=LEFT * 0.15), run_time=0.45)
            vo.wait_until("the exact words")
            self.play(say.animate.set_color(AUDIO), run_time=0.8)
            vo.wait_until("The animation code")
            self.play(Create(reads_arrow), FadeIn(reads_l, shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(chip, shift=UP * 0.2), FadeIn(chip_cap), run_time=0.6)
            vo.wait_until("straight from this file")
            self.play(Indicate(s03_glyphs, color=S.WHITE, scale_factor=1.3),
                      Indicate(chip_s03, color=S.WHITE, scale_factor=1.3), run_time=0.9)
            vo.wait_until("It's written for the ear")
            self.play(conv.animate.set_opacity(1), VGroup(show, say, s03).animate.set_opacity(0.45), run_time=0.5)
            self.play(nine.animate.set_color(AUDIO), run_time=0.4)
            self.play(Circumscribe(nine, color=S.WHITE, buff=0.06, run_time=0.8))
            vo.wait_until("nine factorial is")
            self.play(TransformFromCopy(nine[-3:-1], sym), run_time=0.6)
            self.play(Create(sym_strike), GrowArrow(swap[1]), run_time=0.4)
            self.play(TransformFromCopy(nine[5:19], words, path_arc=-PI / 3), run_time=0.8)

        # ---------------------------------------------------------- review the script before any animation
        new_icon = doc_icon("script").move_to([ROW_X[3], ROW_Y1, 0])
        new_name = mono("script.md", NAME_SIZE, INK).next_to(new_icon, DOWN, buff=0.18)
        reviewers = VGroup(role_icon("sub", 0.75), role_icon("sub", 0.75)).arrange(RIGHT, buff=0.35)
        reviewers.move_to([ROW_X[3], 1.1, 0])
        gate = VGroup(Rectangle(width=0.42, height=0.42, stroke_width=0).set_fill(S.BG, 1), pause_icon(0.28, INK))
        gate.move_to(arrows[3].get_center())
        downstream = VGroup(arrows[3], arrows[4], items[4], items[5])
        c1, c2 = clock(0.72), clock(0.72)
        c1.move_to([ROW_X[3] - 0.3, -0.75, 0])
        c2.move_to([ROW_X[5] - 0.75, -0.75, 0])
        l1 = clock_label("fix a sentence in script.md:", "seconds").next_to(c1, DOWN, buff=0.3)
        l2 = clock_label("fix it after animation:", "a re-render").next_to(c2, DOWN, buff=0.3)

        # the false start, on a time lane (Oct 4, UTC)
        axis = time_axis(LANE_T0, LANE_T1, width=9.6,
                         ticks=[(f"{h}:{m:02d}", f"{DAY} {h}:{m:02d}") for h, m in
                                ((15, 50), (16, 0), (16, 20), (16, 30))])
        axis.move_to([1.5, -2.65, 0])
        x_of = axis.x_of
        ax_y = axis.line.get_y()
        small_ticks = VGroup(*[Line([x_of(f"{DAY} {t}"), ax_y - 0.08, 0], [x_of(f"{DAY} {t}"), ax_y + 0.08, 0],
                                    color=TOOL, stroke_width=2) for t in ("15:40", "16:10")])
        day = label("day one · Oct 4", 30, INK).move_to([0, 2.95, 0]).align_to([-6.4, 0, 0], LEFT)
        utc = caption("UTC", 22).next_to(axis.line, LEFT, buff=0.25)
        REV_Y, LANE_Y0, LANE_DY = 1.2, -0.25, 0.37
        lane_ys = [LANE_Y0 - k * LANE_DY for k in range(6)]
        rev_icons_at = VGroup(*[m.copy() for m in reviewers]).arrange(RIGHT, buff=0.12)
        rev_icons_at.move_to([0, REV_Y, 0]).align_to([-6.4, 0, 0], LEFT)
        rev_l = label("script review", 26, SUB_AGENT_TEXT).next_to(rev_icons_at, RIGHT, buff=0.2)
        rev_times = caption("15:47 → 16:30", 22).move_to([0, REV_Y + 0.36, 0]).align_to([x_of(REVIEW[0]), 0, 0], LEFT)
        now = ValueTracker(_t(REVIEW[0]).timestamp())

        def x_now():
            return x_of(dt.datetime.fromtimestamp(now.get_value()))

        def lane_bar(t0: str, t_end: str, y: float, h: float, color: str = SUB_AGENT, opacity: float = 1.0):
            x0, x1 = x_of(t0), x_of(t_end)

            def draw():
                x = min(max(x_now(), x0), x1)
                return Rectangle(width=max(x - x0, 0.001), height=h, stroke_width=0) \
                    .set_fill(color, opacity if x > x0 + 0.002 else 0).move_to([(x0 + x) / 2, y, 0])
            return always_redraw(draw)

        cursor = always_redraw(lambda: Line([x_now(), ax_y, 0], [x_now(), REV_Y + 0.3, 0], color=TOOL,
                                            stroke_width=2.5))
        review_bar = lane_bar(REVIEW[0], REVIEW[1], REV_Y, 0.32)
        starts = [s for s in STARTS for _ in range(2)]          # 3 runs x 2 agents
        builder_bars = [lane_bar(s, KILLED, y, 0.2) for s, y in zip(starts, lane_ys)]
        builders = VGroup(*[person_icon(SUB_AGENT, 0.34).move_to([x_of(s) - 0.24, y, 0])
                            for s, y in zip(starts, lane_ys)])
        b_label = VGroup(label("6 sub-agents\nbuilding scenes", 26, SUB_AGENT_TEXT, line_spacing=0.9),
                         caption("3 runs × 2 agents", 22)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        b_label.move_to([0, (lane_ys[0] + lane_ys[-1]) / 2, 0]).align_to([-6.45, 0, 0], LEFT)
        b_time = caption("16:12–16:13", 20, SUB_AGENT_TEXT).move_to([x_of(STARTS[1]), ax_y - 0.62, 0])
        b_tick = Line([x_of(STARTS[1]), ax_y - 0.08, 0], [x_of(STARTS[1]), ax_y + 0.08, 0], color=SUB_AGENT_TEXT,
                      stroke_width=3)

        guide_text = label(A13["heading"].replace("script ", "script\n", 1), 26, INK, line_spacing=0.9)
        guide_path = VGroup(mono("docs/WORKFLOW.md", 20, TOOL), caption("· commit 41eca34", 20)) \
            .arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        guide_body = VGroup(guide_path, guide_text).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        guide_ic = file_icon(0.55)
        guide_inner = VGroup(guide_ic, guide_body).arrange(RIGHT, buff=0.22)
        guide_box = box(guide_inner.width + 0.5, guide_inner.height + 0.36, TOOL, fill=PANEL, fill_opacity=1)
        guide_inner.move_to(guide_box)
        guide = VGroup(guide_box, guide_inner).move_to([x_of(GUIDE_AT) + 0.6, 2.62, 0])
        guide_drop = DashedLine([x_of(GUIDE_AT), guide.get_bottom()[1], 0], [x_of(GUIDE_AT), ax_y, 0],
                                dash_length=0.08, color=TOOL, stroke_width=2)
        guide_time = caption("16:07", 20).move_to([x_of(GUIDE_AT), ax_y - 0.32, 0])
        quill2 = pen(0.62, S.BLUE)
        src3 = source_caption("times: the session's workflow run records and git (UTC)")
        stop_line = Line([x_of(KILLED), lane_ys[0] + 0.25, 0], [x_of(KILLED), ax_y, 0], color=BUG, stroke_width=4)
        stop_tag = bug_tag("stopped at 16:24,\nbefore the review was done", size=24)
        stop_tag.move_to([x_of(KILLED), (REV_Y + lane_ys[0]) / 2 - 0.02, 0])

        for m in (items[4], items[5], *arrows[2:]):          # dimmed in beat 2, faded out in beat 3
            m.restore()

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(panel.rows, panel.bar, show_bar, say_bar, show_l, say_l, reads_arrow, reads_l,
                                     chip, chip_cap, swap, sym_strike, src2)),
                      ReplacementTransform(panel.frame, new_icon), ReplacementTransform(panel.title, new_name),
                      *[FadeIn(m) for m in (*others, *arrows)], run_time=1.0)
            vo.wait_until("review the script")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.25) for r in reviewers], lag_ratio=0.3), run_time=0.7)
            vo.wait_until("before any animation")
            self.play(FadeIn(gate, scale=0.5), *dim(downstream, opacity=0.35), run_time=0.5)
            vo.wait_until("a sentence costs")
            self.play(FadeIn(c1, scale=0.6), FadeIn(l1, shift=UP * 0.1), run_time=0.5)
            self.play(Rotate(c1.minute, -TAU / 60, about_point=c1.face.get_center()), run_time=0.4)
            vo.wait_until("an animation costs")
            self.play(FadeIn(c2, scale=0.6), FadeIn(l2, shift=UP * 0.1), run_time=0.5)
            self.play(Rotate(c2.minute, -TAU * 3, about_point=c2.face.get_center()),
                      Rotate(c2.hour, -TAU / 4, about_point=c2.face.get_center()), run_time=1.5, rate_func=smooth)

            # the rule, and how it was broken the same day
            vo.wait_until("The agent wrote")
            stage = gather(self, *others, new_icon, new_name, *arrows, gate, c1, c2, l1, l2)
            self.play(FadeOut(stage), ReplacementTransform(reviewers, rev_icons_at), run_time=0.8)
            self.play(Create(axis.line), FadeIn(axis.marks), FadeIn(small_ticks), FadeIn(day), FadeIn(utc), FadeIn(rev_l),
                      FadeIn(rev_times), FadeIn(src3), run_time=0.6)
            self.add(review_bar, cursor)
            quill2.shift(guide_text.get_left() + LEFT * 0.1 - tip_of(quill2))
            self.play(now.animate.set_value(_t(GUIDE_AT).timestamp()), FadeIn(guide_box), FadeIn(guide_ic),
                      FadeIn(guide_path), FadeIn(quill2, shift=DOWN * 0.2), run_time=0.9, rate_func=linear)
            self.play(Write(guide_text), quill2.animate.shift(RIGHT * guide_text.width), run_time=1.1)
            self.play(FadeOut(quill2, shift=UP * 0.2), Create(guide_drop), FadeIn(guide_time), run_time=0.5)
            vo.wait_until("on day one")
            self.play(emphasize(day, run_time=0.7))

            vo.wait_until("Minutes later")
            self.play(now.animate.set_value(_t(STARTS[0]).timestamp()), run_time=vo.until("it started six"),
                      rate_func=linear)
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in builders], lag_ratio=0.12),
                      FadeIn(b_label, shift=RIGHT * 0.15), FadeIn(b_time), FadeIn(b_tick), run_time=0.9)
            self.add(*builder_bars)
            t_still = vo.time_until("while the review")
            t_stop = vo.time_until("all six were stopped")
            self.play(now.animate(rate_func=linear).set_value(_t(KILLED).timestamp()),
                      Succession(Wait(max(0.05, t_still)), emphasize(rev_l, run_time=0.9)),
                      run_time=max(t_stop, t_still + 1.0))
            for b in builder_bars:
                b.clear_updaters()
            self.play(Create(stop_line), *[m.animate.set_fill(BUG, 1) for m in builder_bars],
                      builders.animate.set_color(BUG), run_time=0.5)
            self.play(FadeIn(stop_tag, scale=0.9), *[m.animate.set_fill(BUG, 0.25) for m in builder_bars],
                      builders.animate.set_opacity(0.3), run_time=0.7)
        self.play(now.animate.set_value(_t(REVIEW[1]).timestamp()), run_time=0.9, rate_func=linear)
        review_bar.clear_updaters()
        cursor.clear_updaters()
        self.play(FadeOut(cursor), emphasize(axis.marks[-1][1], run_time=0.8), emphasize(rev_times, run_time=0.8))
        self.wait(0.5)
        fade_out_all(self)
