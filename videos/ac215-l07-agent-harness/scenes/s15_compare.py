"""S15 · Evaluation: one change, k runs, a diff (README "6 · Evaluation", steps 3 and 4).
Lecture: 40–42.

Beats (script.md "## S15", one voiceover block each):
 0  The tracker "README › 6 · Evaluation › Step 3" (no step lit yet). On "compares two configurations"
    two GREY cards batch A ⟷ batch B, "one change between them". On "The lecture warns" they leave and
    LECTURE 40–42 arrives with slide 40's table, one row, redrawn: headers "layer · what a change here
    typically breaks · what catches it", cells Context · "a prompt edit fixes one case, breaks three
    others" · GREEN "outcome" (the catching column lit). On "a prompt edit" the middle cell flashes and
    four GREY case cards arrive; on "fix one case" case 1 turns GREEN (a check), on "and break three"
    cases 2–4 turn RED (crosses); on "so compare per case" the YELLOW caption "compare per case".
 1  The row leaves. V8's cycle (slide 42 as a closed loop): each box lights YELLOW as the SAY names
    it; on "capture a test case" step 2's chip `data/agent_evaluation_cases.json` "golden cases"
    arrives under the cycle (it does not fit inside), a dashed GREEN line runs up to the pile of
    GREEN test-case cards beside step 2, which flashes. After "merge or iterate" the pile grows one
    card (lap 1); a second, quick lap grows it again.
 2  TRACKER Eval3 1. The cycle, its chip and the lecture tag leave. The container terminal (12 rows,
    title-bar tags `no key` and GOLD `live · billed per token`) and the YELLOW top-band chip "step 4
    · run k times". It types batch A (3 rows); `--context enriched`, the two `--case` flags and
    `--repeats 2` flash as named; on "4 live runs" a GOLD chip "4 runs" beside the last row.
    container/80: 2, …, 36, 38. On "0 of 4" `0/4` turns RED; on "with 3 errors" line 38 turns RED;
    on "If one fails" a GREY chip "README.md · line 721 a failed batch uses up its label · rerun with
    new labels" on the empty rows under it.
 3  TRACKER Eval3 2. The chip leaves, the live tag leaves the title bar, the top chip becomes "step
    3 · change one layer". `cp prompts/shop_assistant.md prompts/shop_assistant_v2.md` → the prompt
    returns. On "and edit the copy": TRACKER Eval3 3, the terminal shrinks to the strip, a GREY editor
    window (tag `illustration` above it) on the laptop opens `prompts/shop_assistant_v2.md`
    (schematic GREY lines). On "one deliberate change" a YELLOW line is added with a YELLOW pencil
    and the chip README.md · line 737 (excerpt) "Make one deliberate change"; on "keeping the" the
    second chip "Preserve the confirmed-constraint instructions." and the old lines flash GREEN.
 4  The editor leaves; TRACKER Eval3 3 · extra; the extra card "an extra · in the study guide" /
    “appends one line with printf” above the strip. On "asking for a price" the card leaves, the
    terminal grows back and types `diff -u prompts/shop_assistant.md prompts/shop_assistant_v2.md`
    (tag extra) → container/83: 2–4, …, 8, 9 folded to `+Keep … "Price:" … and "Action status:" …`
    (wrap; 8–9 GREEN). On "diff shows" line 9 flashes and the GREY caption "diff exits 1 when the
    files differ" arrives on the command's row (line 9 has no room); the frame holds 1 s to read it.
 5  TRACKER Eval3 4; the top chip "step 4 · run k times"; the live tag returns to the title bar. It
    types batch B (4 rows); on "with dash dash prompt file" `--prompt-file
    prompts/shop_assistant_v2.md` turns YELLOW with the YELLOW note "the only difference" →
    container/84: 2, …, 36, 38.
 6  TRACKER Eval3 5. The top chip leaves, the terminal grows to 13 rows, the top chip "step 5 ·
    compare" (tall form); the title bar's GOLD tag becomes GREEN `offline · free`. It types the
    compare (2 rows) → container/85: 5–9, …, 14, …, 436 folded to `"interpretation": "… Prompt/skill
    edits can be compared; code, data, model or settings changes are confounders. …` (wrap, 2 rows),
    438. On "Changed configuration" lines 5–7 GREEN; on "Confounding changes" line 8 GREEN; on
    "Change code" line 436's confounder phrase YELLOW; on "checked in code" lines 5–8 get a GREEN
    outline flash; then `"outcome": "unchanged"` gets a YELLOW box and the GREY tag "an error
    before and after".
 7  The top chip leaves as the terminal shrinks to the strip (the compare command and line 14).
    Above it, at once: the excerpt chip `formaggio/evaluation/evaluation.py · line 153 (excerpt)`:
    `"improved" if new["passed"] else "regressed"`; a balance (tag `illustration`) with the cards
    batch A and batch B on its pans and the GREEN note "only the prompt changed"; the four case
    cards of the opening as rows of before dots (tag `illustration`). On "only when pass or fail
    flips" the after dots and outcomes arrive: case 1 RED → GREEN "improved" (GREEN), cases 2–4
    GREEN → RED "regressed" (RED), while the excerpt's "improved" turns GREEN and "regressed" RED.
    On "every run errored" every illustrative part leaves (the excerpt back to ink), then this run's
    rows arrive (tag "this run · enriched · context-live-a → context-live-b"): standard #1,
    standard #2, missing-details #1 error → error (RED dots), GREY "unchanged"; missing-details #2
    GREY dashed, "missing"; the balance wobbles and settles level; 0.8 s of silence to read them.
 8  TRACKER Eval3 5 · extra. The picture leaves, and with it the YELLOW box and tag on the live
    compare's line 14; the extra card “a second scripted batch, context-fixture-2, with the v2
    prompt file” above the strip; then the terminal grows and types `python cli.py --compare
    context-fixture-1 context-fixture-2` (extra, the tag on the prompt's row) → container/87: 5–9,
    …, 14 (the … as at the live compare). On "reports all four" line 14's "unchanged" flashes and
    the GREY tag "the same for all 4 runs" (lines 14, 305, 596, 887) pins beside it; on "because
    fixtures" the top-band chip README.md · line 765 "Scripted fixture success does not establish
    live response quality" (expected).
 9  TRACKER Eval4 1 (the section switches while the terminal is still up). The terminal fades.
    QUOTE(README.md: 755–763) as one card: the first sentence, line 757, the five review questions
    with YELLOW checkboxes. On "They check properties" "cart validity", on "approval order"
    "approval ordering" are underlined GREEN; on "the prose needs" a YELLOW outline runs round the
    five questions; on "five questions" the boxes tick one by one.
10  The card leaves. Slide 41's three judges (mirrored: human YELLOW left, LLM judge GREY dashed
    middle, deterministic checks GREEN right), each on its word ("code" with LECTURE 41, "a model",
    "a human"). On "This tutorial uses two" the LLM judge gets `concept · lecture only` and the
    excerpt chip `formaggio/evaluation/context_evidence.py · line 1 (excerpt)` "no model judge"; on
    "code" the checks pulse, on "and you" the human pulses and the report row `human.prose_quality |
    not_applicable | Instructor review` (container/89 line 38) arrives under it. On "Lean toward
    code" a GREEN arrow grows rightwards with the caption "as far toward code as the task allows —
    same rule as the harness", and the V1 mini-map arrives; on "as in the harness" its GREEN column
    flashes.
11  The judges leave. The chip README.md · line 769 "one observed difference … the evidence … a
    limitation" centred, its three parts lit as said. On "And keep your cases" it moves up to the top
    band and the cycle returns centre with LECTURE 42 and its chips attached at once (`--repeats 2`
    inside, over step 4; "one prompt line" under step 3's box and `--compare` under step 5's: side
    by side inside the loop they touched); its pile glows; on "the eval set" the caption "the eval
    set is the most valuable artifact". On "Pause and run" everything leaves and the static GREY
    "your turn" card arrives (header "evaluation step 3 · with your key", the four commands of step 3
    folded with " \\", "then edit the copy" beside cp, GREY "a batch failed? new labels for both",
    GOLD "8 live runs · billed per token"). Hold 2 s, then an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Circle,
    Circumscribe,
    Create,
    DashedLine,
    DashedVMobject,
    Dot,
    DoubleArrow,
    GrowFromCenter,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    RoundedRectangle,
    Square,
    Succession,
    SurroundingRectangle,
    VGroup,
)

from common import *  # noqa: F401,F403
from common import _header_text, _md_text, _save_op, _set_op
from explainer import style as S
from explainer.devops import PANEL, box, cell_width, check_mark, chip, cross_mark, label, mono, substring
from explainer.scene import VoiceScene

SAY = NARRATION["S15"]

# ------------------------------------------------------------------ the real captures (file line numbers)
LIVE_A = capture("container/80")
CP = capture("container/81")
DIFF = capture("container/83")
LIVE_B = capture("container/84")
CMP = capture("container/85")
CMP_FIX = capture("container/87")
CARD = capture("container/89")
CMD_A = ("python cli.py --act 2 --evaluate core --context enriched --case standard --case missing-details "
         "--repeats 2 --label context-live-a")
CMD_B = ("python cli.py --act 2 --evaluate core --context enriched --case standard --case missing-details "
         "--repeats 2 --label context-live-b --prompt-file prompts/shop_assistant_v2.md")
CMD_CP = "cp prompts/shop_assistant.md prompts/shop_assistant_v2.md"
CMD_CMP = "python cli.py --compare context-live-a context-live-b --json-output outputs/context-comparison.json"
CMD_DIFF = "diff -u prompts/shop_assistant.md prompts/shop_assistant_v2.md"
CMD_FIX = "python cli.py --compare context-fixture-1 context-fixture-2"
assert LIVE_A.cmd == CMD_A and LIVE_B.cmd == CMD_B and CP.cmd == CMD_CP and CMP.cmd == CMD_CMP, LIVE_A.cmd
assert DIFF.cmd == CMD_DIFF and CMP_FIX.cmd == CMD_FIX
assert CP.lines == [] and CP.exit == 0 and DIFF.exit == 1
# the README spells the four commands of step 3 exactly so (README.md lines 728, 734, 742, 748)
for _n, _c in ((728, CMD_A), (734, CMD_CP), (742, CMD_B), (748, CMD_CMP)):
    assert source_line("README.md", _n).strip() == _c, (_n, source_line("README.md", _n))
# batch A / B summaries
assert LIVE_A.line(2) == "LIVE evaluation: 2 cases × 2 repeats = 4 runs."
assert LIVE_A.line(36) == "LIVE EVALUATION context-live-a: 0/4 scheduled runs passed"
assert LIVE_B.line(36) == "LIVE EVALUATION context-live-b: 0/4 scheduled runs passed"
assert LIVE_A.line(38) == LIVE_B.line(38) == "Failures: 0; errors: 3; missing: 1."
# the diff
L9 = DIFF.fold(9, 9, '+Keep the customer message under 120 words. Start it with two labeled lines: "Price:" … '
                     'and "Action status:" …')
assert DIFF.line(8) == "+" and DIFF.line(4) == "@@ -55,3 +55,5 @@"
# the comparison
assert CMP.line(5).strip() == '"changed_configuration": [' and CMP.line(6).strip() == '"prompt"'
assert CMP.line(7).strip() == "]," and CMP.line(8).strip() == '"confounding_changes": [],'
assert CMP.line(14).strip() == '"outcome": "unchanged",'
CONF = "code, data, model or settings changes are confounders."
L436 = CMP.fold(436, 436, '  "interpretation": "… Prompt/skill edits can be compared; ' + CONF + " …")
assert CMP.line(438) == "JSON saved: outputs/context-comparison.json"
assert [CMP_FIX.line(n) for n in range(5, 10)] == [CMP.line(n) for n in range(5, 10)]
assert CMP_FIX.line(14).strip() == '"outcome": "unchanged",'
# the scripted A/B lists four runs (container/87 lines 14, 305, 596, 887), all "unchanged": the tag
# "the same for all 4 runs" beside line 14 says so
_FIX_OUT = []
for _n in range(1, len(CMP_FIX.lines) + 2):
    try:
        if CMP_FIX.line(_n).startswith('      "outcome": '):
            _FIX_OUT.append((_n, CMP_FIX.line(_n).strip()))
    except IndexError:
        continue
assert _FIX_OUT == [(n, '"outcome": "unchanged",') for n in (14, 305, 596, 887)], _FIX_OUT
# the real per-run pairs of this A/B (container/85): three matched runs, error before and after; the
# fourth scheduled run (missing-details #2) is missing in both batches, so compare does not list it
PAIRS = []
for _n in range(1, len(CMP.lines) + 1):
    try:
        _ln = CMP.line(_n)
    except IndexError:
        continue
    if _ln.startswith('      "case_id": '):
        PAIRS.append((_ln.split('"')[3], int(CMP.line(_n + 1).split(":")[1].strip(" ,")),
                      CMP.line(_n + 2).split('"')[3]))
assert PAIRS == [("missing-details:enriched", 1, "unchanged"), ("standard:enriched", 1, "unchanged"),
                 ("standard:enriched", 2, "unchanged")], PAIRS
REAL_ROWS = ("standard #1", "standard #2", "missing-details #1", "missing-details #2")
# sources (exact sub-strings, checked)
EVAL_PY = "formaggio/evaluation/evaluation.py"
FLIP = '"improved" if new["passed"] else "regressed"'
assert FLIP in source_line(EVAL_PY, 153)
assert 'elif old["passed"] == new["passed"]:' in source_line(EVAL_PY, 150)
CTX_PY = "formaggio/evaluation/context_evidence.py"
NO_JUDGE = "no model judge"
assert NO_JUDGE in source_line(CTX_PY, 1)
REPORT_ROW = "human.prose_quality | not_applicable | Instructor review"
assert CARD.line(38).startswith(REPORT_ROW)
R721 = source_line("README.md", 721)
assert "Labels are unique and cannot be overwritten" in R721 and "choose a new label" in R721
R737_1, R737_2 = "Make one deliberate change", "Preserve the confirmed-constraint instructions."
assert R737_1 in source_line("README.md", 737) and R737_2 in source_line("README.md", 737)
R765 = "Scripted fixture success does not establish live response quality"
assert R765 in source_line("README.md", 765)
R769 = "one observed difference … the evidence … a limitation"
for _f in ("one observed difference", "the evidence", "a limitation"):
    assert _f in source_line("README.md", 769)
# the README's step 4 (lines 755-763): the first sentence, line 757, the five review questions
_R755 = source_line("README.md", 755)
S1A = "Automated evaluation checks application properties such as cart validity,"
S1B = "action counts, approval ordering, and required skill/resource usage."
assert _R755.startswith(S1A + " " + S1B), _R755[:150]
Q757 = "Final prose needs separate review. Ask whether the response:"
assert source_line("README.md", 757) == Q757
QUESTIONS = [source_line("README.md", n)[2:] for n in range(759, 764)]
assert all(source_line("README.md", n).startswith("- ") for n in range(759, 764))

# ------------------------------------------------------------------ layout
SAFE = 6.45
TITLE = 24


# ------------------------------------------------------------------ small helpers (S14's idiom)
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


def outline_flash(m, color: str = TURN, buff: float = 0.07):
    """A stroke-only flash round m (Circumscribe): nothing filled covers it."""
    return Circumscribe(m, color=color, buff=buff, fade_out=True, stroke_width=4)


def pulse(frame, color: str | None = None, width: float = 8.0):
    """A frame pulses: a thick outline (no fill) over it fades in and out."""
    ol = frame.copy().set_fill(opacity=0).set_stroke(color or frame.get_stroke_color(), width)
    return Succession(FadeIn(ol, run_time=0.3), FadeOut(ol, run_time=0.45))


def apart(a, b, gap: float = 0.06):
    """Assert that the bounding boxes of a and b are at least `gap` apart (no overlap)."""
    ok = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
          or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    assert ok, (a.get_corner(DOWN + LEFT), a.get_corner(UP + RIGHT), b.get_corner(DOWN + LEFT), b.get_corner(UP + RIGHT))


def inside(m, x0: float = -6.56, x1: float = 6.56, y0: float = -3.56, y1: float = 3.56):
    assert m.get_left()[0] >= x0 and m.get_right()[0] <= x1 and m.get_bottom()[1] >= y0 and m.get_top()[1] <= y1, \
        (m.get_corner(DOWN + LEFT), m.get_corner(UP + RIGHT))


def bar_y(t, rows: int) -> float:
    """The title bar's centre y of the house terminal `t` at `rows` rows (bottom edge fixed)."""
    return strip_top(rows) - t.bar_h / 2


def fit(scene, t, rows: int, keep=None, tags=(), run_time: float = 0.8, more=()):
    """resize(), with the title-bar tags riding along on the bar (S08's / S14's idiom); `more`:
    animations that play with the resize (a top chip leaving)."""
    y = bar_y(t, rows)
    title, t.title = t.title, None
    try:
        resize(scene, t, rows, keep=keep, run_time=run_time,
               extra=[title.animate.set_y(y), *[m.animate.set_y(y) for m in tags], *more])
    finally:
        t.title = title


def arrow(a, b, color: str = S.GREY, stroke: float = 3, buff: float = 0.06):
    return Arrow(a, b, buff=buff, color=color, stroke_width=stroke, tip_length=0.18,
                 max_tip_length_to_length_ratio=0.3)


def rows_of(cmd_line) -> list:
    """The rows of a typed command (one row, or a folded VGroup with .rows)."""
    return list(cmd_line.rows) if hasattr(cmd_line, "rows") else [cmd_line]


def typed_glyphs(cmd_line, *subs: str) -> VGroup:
    """The glyphs of each of `subs` in a typed (possibly folded) command, each found on the row
    that holds it (a flag and its value may sit on two rows: pass them as two subs)."""
    out = VGroup()
    for sub in subs:
        for r in rows_of(cmd_line):
            if sub in r.text:
                out.add(*substring(r, sub))
                break
        else:
            raise ValueError(f"{sub!r} is not on one typed row: {[r.text for r in rows_of(cmd_line)]}")
    return out


def stick(scene, pairs) -> None:
    """After their play: make each mob part of its terminal row (as pin() does), so it scrolls,
    moves and fades with the row."""
    for row, mob in pairs:
        scene.remove(mob)
        row.add(mob)
        scene.add(row)


def pin_tag(scene, t, line, tag_, run_time: float = 0.35):
    """beside() + pin(): a tag right after a line's text (its last row when folded)."""
    beside(tag_, t, line)
    return pin(scene, line, tag_, run_time=run_time)


def hide_all(m) -> None:
    _save_op(m)
    _set_op(m, 0)


def card_lines(cmd: str, limit: int = 66) -> str:
    """A command for the turn card (S06's / S14's idiom), folded at a space with " \\" and a
    4-space indent, preferring a break before an option (an option keeps its value)."""
    rows, cur = [], cmd
    while len(cur) > limit:
        room = limit - 2
        spaces = [i for i, ch in enumerate(cur) if ch == " " and (4 if rows else 0) < i <= room]
        opt = [i for i in spaces if cur[i + 1] == "-"]
        cut = opt[-1] if opt and opt[-1] >= room * 0.5 else spaces[-1]
        rows.append(cur[:cut] + " \\")
        cur = "    " + cur[cut + 1:]
    rows.append(cur)
    assert " ".join(r.rstrip(" \\").strip() for r in rows) == cmd, rows
    return "\n".join(rows)


def text_glyphs(t, sub: str, src: str | None = None) -> VGroup:
    """The glyphs of `sub` in a Text. A normal Text has one glyph per non-space character (and
    .text may come without its spaces); one built with disable_ligatures=True has one submobject
    per character of `src`, spaces included."""
    full = src if src is not None else t.text
    n = len(t.submobjects)
    if n == len(full) and src is not None:
        a = full.find(sub)
        if a < 0:
            raise ValueError(f"{sub!r} not in {full!r}")
        return VGroup(*t.submobjects[a:a + len(sub)])
    s = "".join(full.split())
    key = "".join(sub.split())
    a = s.find(key)
    if a < 0:
        raise ValueError(f"{sub!r} not in {full!r}")
    assert n == len(s), (n, len(s))
    return VGroup(*t.submobjects[a:a + len(key)])


def note_chip(where: str, text: str, quoted: bool = False, width: float | None = None) -> VGroup:
    """A GREY chip: GREY `where` (README.md · line N …) above, the text inside (in quotes when it is
    the README's own words; our paraphrase otherwise). .frame .text .header"""
    t = mtext(f"“{text}”" if quoted else text, CAPTION, INK, font=S.FONT)
    fr = box(max(width or 0, t.width + 0.44), t.height + 0.3, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    t.move_to(fr)
    if width:
        t.align_to(fr, LEFT).shift(RIGHT * 0.22)
    hd = _header_text(where).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.08)
    g = VGroup(fr, t, hd)
    g.frame, g.text, g.header = fr, t, hd
    return keep_size(g)


def quote_chip(where: str, phrase: str) -> VGroup:
    """readme_chip's look (GREY `where`, the phrase in quotes, one row), its phrase drawn without
    ligatures so text_glyphs() can find words in it. .frame .where .phrase"""
    w = _header_text(where)
    ph = S.text(f"“{phrase}”", CAPTION, INK, font=S.FONT, disable_ligatures=True)
    row = VGroup(w, ph).arrange(RIGHT, buff=0.25)
    fr = box(row.width + 0.4, row.height + 0.24, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    fr.move_to(row)
    g = VGroup(fr, row)
    g.frame, g.where, g.phrase, g.src = fr, w, ph, f"“{phrase}”"
    return keep_size(g)


def row_chip(where: str, text: str) -> VGroup:
    """A one-row GREY chip: GREY `where`, then our words (not a quote). .frame .text"""
    hd = _header_text(where)
    t = label(text, CAPTION, INK)
    row = VGroup(hd, t).arrange(RIGHT, buff=0.3)
    fr = box(row.width + 0.44, row.height + 0.26, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.1)
    row.move_to(fr)
    g = VGroup(fr, row)
    g.frame, g.text = fr, t
    return keep_size(g)


# ------------------------------------------------------------------ pictures
def slide40_row() -> VGroup:
    """Slide 40's table, one row, redrawn: headers, then Context · the break · GREEN outcome (the
    catching column lit). Each cell is sized to its text; the row is centred."""
    heads = VGroup(*[note(s) for s in ("layer", "what a change here typically breaks", "what catches it")])
    cells = VGroup()
    for i, s in enumerate(("Context", "a prompt edit fixes one case, breaks three others", "outcome")):
        col = HARNESS if i == 2 else S.GREY
        tx = sans(s, TITLE, INK, weight="BOLD") if i == 0 else label(s, TITLE, INK)
        w = max(tx.width + 0.6, heads[i].width + 0.3)
        fr = box(w, 0.78, col, fill_opacity=0.14 if i == 2 else 0.08, stroke=3 if i == 2 else 2.5, radius=0.12)
        tx.move_to(fr)
        g = VGroup(fr, tx)
        g.frame, g.text = fr, tx
        cells.add(g)
    cells.arrange(RIGHT, buff=0.25).move_to(ORIGIN)
    for h, c in zip(heads, cells):
        h.move_to([c.get_center()[0], 0.66, 0])
    out = VGroup(heads, cells)
    out.heads, out.cells = heads, cells
    return out


def case_card(k: int) -> VGroup:
    """A GREY test-case card "case k" with room for a mark. .frame .text .k"""
    fr = box(2.5, 1.0, S.GREY, fill_opacity=0.08, stroke=2.5, radius=0.14)
    t = mono(f"case {k}", 22, INK)
    t.move_to(fr).shift(LEFT * 0.35)
    g = VGroup(fr, t)
    g.frame, g.text, g.k = fr, t, k
    return g


def editor_window(path: str, w: float, h: float) -> VGroup:
    """A schematic editor window on the laptop (GREY, no logo): a title bar with the file path,
    schematic GREY lines for the file's text. .frame .title .lines .slot (where a new line goes)"""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=S.GREY,
                          stroke_width=2.5).set_fill(PANEL, 1)
    bar_h = 0.5
    bar = Line(fr.get_corner(UP + LEFT) + DOWN * bar_h, fr.get_corner(UP + RIGHT) + DOWN * bar_h,
               color=S.GREY_DARK, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.055, color=S.GREY_DARK) for _ in range(3)]).arrange(RIGHT, buff=0.1)
    dots.move_to(fr.get_corner(UP + LEFT) + np.array([0.35, -bar_h / 2, 0]))
    title = mono(path, CAPTION, S.GREY)
    title.next_to(dots, RIGHT, buff=0.3)
    x0 = fr.get_left()[0] + 0.45
    y0 = fr.get_top()[1] - bar_h - 0.32
    fracs = (0.86, 0.92, 0.7, 0.0, 0.9, 0.82, 0.55)
    lines = VGroup()
    pitch = 0.3
    full = w - 0.9
    for i, f in enumerate(fracs):
        if f <= 0:
            continue
        ln = Rectangle(width=full * f, height=0.11, stroke_width=0).set_fill(S.GREY, 0.55)
        ln.move_to([x0 + full * f / 2, y0 - i * pitch, 0])
        lines.add(ln)
    slot = Dot([x0, y0 - (len(fracs) + 0.2) * pitch, 0], radius=0.01).set_opacity(0)
    g = VGroup(fr, bar, dots, title, lines, slot)
    g.frame, g.title, g.lines, g.slot, g.full = fr, title, lines, slot, full
    return g


def check_card() -> VGroup:
    """QUOTE(README.md: 755–763): the first sentence (two rows), line 757, the five review questions
    with YELLOW checkboxes. .frame .s1 (two Texts) .q757 .boxes .qs .header .tag"""
    s1 = VGroup(_md_text(S1A), _md_text(S1B + " …")).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    q = _md_text(Q757)
    boxes, qs, items = VGroup(), VGroup(), VGroup()
    for s in QUESTIONS:
        b = Square(0.26, color=TURN, stroke_width=3).set_fill(S.BG, 0)
        t = _md_text(s)
        it = VGroup(b, t).arrange(RIGHT, buff=0.22)
        boxes.add(b)
        qs.add(t)
        items.add(it)
    items.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    body = VGroup(s1, q, items).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    items.shift(RIGHT * 0.15)
    fr = box(body.width + 0.7, body.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    head = _header_text("README.md · lines 755–763").next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    tg = expected_tag().next_to(head, RIGHT, buff=0.25)
    g = VGroup(fr, body, head, tg)
    g.frame, g.s1, g.q757, g.boxes, g.qs, g.items, g.header, g.tag = fr, s1, q, boxes, qs, items, head, tg
    return g


def pair_row(k: int, before: str, after: str, outcome: str, ocol: str, chip_w: float) -> VGroup:
    """One row of beat 7: the case chip, the before dot → the after dot, the outcome word.
    .card .label .before .after .arr .word"""
    fr = box(chip_w, 0.44, S.GREY, fill_opacity=0.08, stroke=2.5, radius=0.12)
    t = mono(f"case {k}", CAPTION, INK)
    t.move_to(fr)
    card = VGroup(fr, t)
    card.frame, card.text = fr, t
    d0 = Dot(radius=0.13, color=before)
    d1 = Dot(radius=0.13, color=after)
    ar = arrow(np.array([0, 0, 0]), np.array([0.55, 0, 0]), S.GREY, stroke=3, buff=0.0)
    w = label(outcome, CAPTION, ocol)
    d0.next_to(card, RIGHT, buff=0.35)
    ar.next_to(d0, RIGHT, buff=0.12)
    d1.next_to(ar, RIGHT, buff=0.12)
    w.next_to(d1, RIGHT, buff=0.3)
    g = VGroup(card, d0, ar, d1, w)
    g.card, g.label, g.before, g.arr, g.after, g.word = card, t, d0, ar, d1, w
    return g


def hollow(dot) -> VGroup:
    """A GREY dashed hollow circle where `dot` is (a missing run)."""
    c = Circle(radius=0.13).set_stroke(S.GREY, 2.5)
    d = DashedVMobject(c, num_dashes=8, dashed_ratio=0.6).set_stroke(S.GREY, 2.5)
    return VGroup(d).move_to(dot)


# ------------------------------------------------------------------ the scene
class FairComparison(VoiceScene):
    def construct(self):
        assert len(SAY) == 12, len(SAY)

        # ========================================================== 0 · slide 40: a prompt edit fixes one, breaks three
        tr = tracker("Eval3")
        lr = lref("40–42")
        row40 = slide40_row()
        place(row40, cy=1.15)
        row40.shift(UP * (1.15 - row40.cells.get_center()[1]))
        cards = VGroup(*[case_card(k) for k in range(1, 5)]).arrange(RIGHT, buff=0.55)
        place(cards, cx=0, cy=-0.75)
        marks = []
        for c in cards:
            m = check_mark(0.34, HARNESS) if c.k == 1 else cross_mark(0.3, ERR)
            m.move_to(c.frame.get_right() + LEFT * 0.5)
            marks.append(m)
        cap0 = sans("compare per case", 26, TURN, weight="BOLD")
        place(cap0, cx=0, top=cards.get_bottom()[1] - 0.45)
        pic0 = VGroup(row40, cards, cap0)
        bA0, bB0 = json_card(["batch A"], S.GREY), json_card(["batch B"], S.GREY)
        ab = VGroup(bA0, bB0).arrange(RIGHT, buff=2.4).move_to([0, 0.4, 0])
        ab_ar = DoubleArrow(bA0.get_right() + RIGHT * 0.15, bB0.get_left() + LEFT * 0.15, color=S.GREY, buff=0,
                            stroke_width=3, tip_length=0.16)
        ab_t = note("one change between them")
        place(ab_t, cx=0, top=ab.get_bottom()[1] - 0.25)
        pic_ab = VGroup(ab, ab_ar, ab_t)
        for m in (row40, cards, cap0, pic_ab):
            inside(m)
        apart(row40, tr, 0.1)
        apart(row40, lr, 0.1)
        apart(row40, cards, 0.3)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), run_time=0.6)
            vo.wait_until("compares two configurations")
            self.play(FadeIn(bA0, shift=RIGHT * 0.15), FadeIn(bB0, shift=LEFT * 0.15), run_time=0.5)
            self.play(GrowFromCenter(ab_ar), FadeIn(ab_t, shift=UP * 0.08), run_time=0.5)
            vo.wait_until("The lecture warns")
            self.play(FadeOut(pic_ab), run_time=0.35)
            self.play(FadeIn(lr), LaggedStart(*[FadeIn(VGroup(h, c), shift=UP * 0.1) for h, c in zip(row40.heads, row40.cells)],
                                  lag_ratio=0.3), run_time=1.0)
            vo.wait_until("a prompt edit")
            self.play(Indicate(row40.cells[1].text, color=TURN, scale_factor=1.06),
                      LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.15), run_time=0.8)
            vo.wait_until("fix one case")
            c1 = cards[0]
            self.play(c1.frame.animate.set_stroke(HARNESS, 3.5).set_fill(HARNESS, 0.18), Create(marks[0]),
                      run_time=0.45)
            vo.wait_until("and break three")
            self.play(LaggedStart(*[AnimationGroup(c.frame.animate.set_stroke(ERR, 3.5).set_fill(ERR, 0.16),
                                                   Create(m)) for c, m in zip(cards[1:], marks[1:])],
                                  lag_ratio=0.25), run_time=0.8)
            vo.wait_until("so compare per case")
            self.play(FadeIn(cap0, shift=UP * 0.1), pulse(row40.cells[2].frame, HARNESS, 7), run_time=0.75)
        pic0.add(*marks)

        # ========================================================== 1 · slide 42: the improvement loop
        cy = Cycle()
        cy.move_to([0, 0.3, 0])
        data_chip = keep_size(chip("data/agent_evaluation_cases.json", HARNESS, size=CAPTION, font=MONO))
        gold = note("golden cases")
        dgrp = VGroup(gold, data_chip).arrange(RIGHT, buff=0.25)
        place(dgrp, right=SAFE - 0.2, top=cy.get_bottom()[1] - 0.25)
        px = cy.pile.get_center()[0] + 0.05
        link = DashedLine(np.array([px, data_chip.get_top()[1] + 0.06, 0]),
                          np.array([px, cy.pile.get_bottom()[1] - 0.08, 0]), color=HARNESS, stroke_width=3,
                          dash_length=0.1)
        for m in (cy, dgrp):
            inside(m)
        apart(cy, tr, 0.05)
        apart(cy, lr, 0.05)
        assert link.get_left()[0] > cy.box(2).frame.get_right()[0] + 0.15, "the link crosses step 3"
        apart(dgrp, cy.boxes[3], 0.15)
        names = ("see a failure", "capture a test case", "change one layer", "run the suite k times",
                 "compare with the baseline", "then merge or iterate")
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(pic0), run_time=0.5)
            self.play(FadeIn(cy, scale=0.97), run_time=0.7)
            for i, ph in enumerate(names):
                vo.wait_until(ph)
                self.play(cy.light(i), run_time=0.3)
                if i == 1:
                    self.play(FadeIn(dgrp, shift=UP * 0.1), Create(link), run_time=0.5)
                    self.play(Indicate(cy.pile, color=HARNESS, scale_factor=1.15), run_time=0.5)
            self.play(cy.unlight(), cy.grow_pile(), run_time=0.45)
            cy.lap(self, 2.4)                       # a second lap: the suite grows again

        # ========================================================== 2 · step 3: live batch A (4 runs, 401s here)
        t = term(container=True, rows=12)
        nk, lv = frame_tags(t, nokey_tag(), live_tag())
        lv_right = lv.get_right()[0]
        bar_tags = [nk, lv]
        chip4 = top_chip("step 4 · run k times")
        apart(chip4, tr, 0.01)
        assert chip4.get_bottom()[1] > t.box.get_top()[1] + 0.05
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(cy, dgrp, link)), FadeOut(lr), tr.goto(1), run_time=0.5)
            self.play(FadeIn(t, shift=UP * 0.3), FadeIn(nk, shift=UP * 0.3), FadeIn(lv, shift=UP * 0.3),
                      FadeIn(chip4, shift=DOWN * 0.1), run_time=0.5)
            ca = type_cmd(self, t, CMD_A, 1.1)
            assert len(rows_of(ca)) == 3, [r.text for r in rows_of(ca)]
            vo.wait_until("enriched mode")
            self.play(Indicate(typed_glyphs(ca, "--context enriched"), color=TURN, scale_factor=1.08), run_time=0.45)
            vo.wait_until("on two cases")
            self.play(Indicate(typed_glyphs(ca, "--case standard --case missing-details"), color=TURN,
                               scale_factor=1.06), run_time=0.45)
            vo.wait_until("twice")
            self.play(Indicate(typed_glyphs(ca, "--repeats 2"), color=TURN, scale_factor=1.1), run_time=0.45)
            vo.wait_until("4 live runs")
            pin_tag(self, t, ca, cost_chip("4 runs"), run_time=0.4)
            vo.wait_until("Without a key")
            oa = show(self, t, LIVE_A, 2, "…", 36, 38, run_time=0.5)
            r36, r38 = oa[2], oa[3]
            assert r36.text == LIVE_A.line(36) and r38.text == LIVE_A.line(38)
            vo.wait_until("0 of 4")
            self.play(substring(r36, "0/4").animate.set_color(ERR), run_time=0.4)
            vo.wait_until("with 3 errors")
            self.play(r38.glyphs.animate.set_color(ERR), run_time=0.45)
            vo.wait_until("If one fails")
            rule = row_chip("README.md · line 721", "a failed batch uses up its label · rerun with new labels")
            place(rule, left=t.box.get_left()[0] + 0.2, top=r38.strut.get_bottom()[1] - 0.25)
            assert rule.get_right()[0] < t.box.get_right()[0] - 0.15
            assert rule.get_bottom()[1] > t.box.get_bottom()[1] + 0.15
            self.play(FadeIn(rule, shift=UP * 0.08), run_time=0.45)

        # ========================================================== 3 · copy the prompt, edit the copy on the laptop
        chip3 = top_chip("step 3 · change one layer")
        ed = editor_window("prompts/shop_assistant_v2.md", 6.0, 3.45)
        place(ed, left=-SAFE + 0.05, bottom=STRIP_TOP + 0.2)
        ill3 = illustration_tag()                  # above the frame (the title bar holds the path)
        place(ill3, right=ed.frame.get_right()[0] - 0.1, bottom=ed.frame.get_top()[1] + 0.1)
        new_ln = Rectangle(width=ed.full * 0.8, height=0.11, stroke_width=0).set_fill(TURN, 0.9)
        new_ln.move_to(ed.slot.get_center() + RIGHT * new_ln.width / 2)
        pen = pencil(0.5, TURN)
        pen.next_to(new_ln, RIGHT, buff=0.1).shift(UP * 0.15)
        n1 = note_chip("README.md · line 737 (excerpt)", R737_1, quoted=True)
        n2 = note_chip("README.md · line 737 (excerpt)", R737_2, quoted=True)
        nw = max(n1.frame.width, n2.frame.width)
        n1 = note_chip("README.md · line 737 (excerpt)", R737_1, quoted=True, width=nw)
        n2 = note_chip("README.md · line 737 (excerpt)", R737_2, quoted=True, width=nw)
        place(n1, left=ed.frame.get_right()[0] + 0.3, top=ed.frame.get_top()[1] - 0.15)
        place(n2, left=n1.get_left()[0], top=n1.get_bottom()[1] - 0.35)
        pic3 = VGroup(ed, ill3, new_ln, pen, n1, n2)
        for m in pic3:
            inside(m)
        apart(ed, tr, 0.1)
        apart(n1, chip3, 0.05)
        assert new_ln.get_bottom()[1] > ed.frame.get_bottom()[1] + 0.1 and pen.get_top()[1] < ed.frame.get_top()[1] - 0.6
        assert pen.get_right()[0] < ed.frame.get_right()[0] - 0.1
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(rule), FadeOut(lv), tr.goto(2), run_time=0.4)
            bar_tags = [nk]
            self.play(Succession(FadeOut(chip4), FadeIn(chip3)), run_time=0.5)
            ccp = type_cmd(self, t, CMD_CP, 0.8)
            bp = bare_prompt(self, t)
            vo.wait_until("and edit the copy")
            self.play(tr.goto(3), run_time=0.4)
            fit(self, t, 3, keep=rows_of(ccp) + [bp], tags=bar_tags, run_time=0.7)
            self.play(FadeIn(ed, shift=UP * 0.15), FadeIn(ill3), run_time=0.5)
            vo.wait_until("one deliberate change")
            self.play(FadeIn(new_ln, shift=RIGHT * 0.2), FadeIn(pen, shift=LEFT * 0.15), FadeIn(n1, shift=LEFT * 0.1),
                      run_time=0.55)
            vo.wait_until("keeping the")
            self.play(FadeIn(n2, shift=LEFT * 0.1), Indicate(ed.lines, color=HARNESS, scale_factor=1.02), run_time=0.6)

        # ========================================================== 4 · extra: the appended line, and the diff
        xc4 = extra_card("appends one line with printf", title="an extra · in the study guide")
        place(xc4, cx=0, cy=0.65)
        inside(xc4)
        apart(xc4, tr, 0.1)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(pic3), caption_extra(tr, True), run_time=0.45)
            self.play(FadeIn(xc4, shift=UP * 0.1), run_time=0.45)
            vo.wait_until("asking for a price")
            self.play(FadeOut(xc4), run_time=0.35)
            fit(self, t, 12, tags=bar_tags, run_time=0.6)
            cdf = type_cmd(self, t, CMD_DIFF, 0.8)
            xt4 = pin_tag(self, t, cdf, extra_tag(), run_time=0.3)
            vo.wait_until("diff shows")
            od = show(self, t, DIFF, 2, 3, 4, "…", (DIFF.line(8), HARNESS), (L9, HARNESS), wrap=True, run_time=0.5)
            r9 = item_rows(od, 5)
            cap4 = note("diff exits 1 when the files differ")       # on the command's row (line 9 is full)
            place(cap4, left=xt4.get_right()[0] + 0.25, cy=xt4.get_center()[1])
            assert cap4.get_right()[0] < t.box.get_right()[0] - 0.12, cap4.get_right()
            pin(self, cdf, cap4, run_time=0.6,
                anim=AnimationGroup(FadeIn(cap4, shift=LEFT * 0.1),
                                    Indicate(VGroup(*[r.glyphs for r in r9]), color=HARNESS, scale_factor=1.04)))
            self.wait(1.0)                              # the caption scrolls away with batch B: read it now

        # ========================================================== 5 · live batch B: only the prompt file differs
        with self.voiceover(SAY[5]) as vo:
            lv2 = live_tag()
            lv2.move_to([lv_right - lv2.width / 2, nk.get_center()[1], 0])
            self.play(caption_extra(tr, False), tr.goto(4), FadeIn(lv2), run_time=0.45)
            bar_tags = [nk, lv2]
            self.play(Succession(FadeOut(chip3), FadeIn(chip4)), run_time=0.5)
            cb = type_cmd(self, t, CMD_B, 1.3)
            assert len(rows_of(cb)) == 4, [r.text for r in rows_of(cb)]
            vo.wait_until("with dash dash prompt file")
            pf = typed_glyphs(cb, "--prompt-file", "prompts/shop_assistant_v2.md")
            self.play(pf.animate.set_color(TURN), run_time=0.4)
            only = note("the only difference", TURN)
            pin_tag(self, t, cb, only, run_time=0.35)
            show(self, t, LIVE_B, 2, "…", 36, 38, run_time=0.5)

        # ========================================================== 6 · compare, offline: one change, no confounders
        chip5 = top_chip("step 5 · compare", tall=True)
        apart(chip5, tr, 0.05)
        off = offline_tag()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(chip4), tr.goto(5), run_time=0.4)
            fit(self, t, 13, tags=bar_tags, run_time=0.6)
            assert chip5.get_bottom()[1] > t.box.get_top()[1], (chip5.get_bottom(), t.box.get_top())
            off.move_to([lv_right - off.width / 2, nk.get_center()[1], 0])
            self.play(FadeIn(chip5, shift=DOWN * 0.1), Succession(FadeOut(lv2), FadeIn(off)), run_time=0.5)
            bar_tags = [nk, off]
            cc = type_cmd(self, t, CMD_CMP, 0.9)
            oc = show(self, t, CMP, (5, 9), "…", 14, "…", L436, 438, wrap=True, run_time=0.6)
            assert len(t.lines) == 13 and rows_of(cc)[0] in t.lines, [ln.text for ln in t.lines]
            r5_7, r8, r14 = [oc[0], oc[1], oc[2]], oc[3], oc[6]
            assert r14.text == CMP.line(14)
            r436 = item_rows(oc, 8)
            vo.wait_until("Changed configuration")
            self.play(*[r.glyphs.animate.set_color(HARNESS) for r in r5_7], run_time=0.45)
            vo.wait_until("Confounding changes")
            self.play(r8.glyphs.animate.set_color(HARNESS), run_time=0.45)
            vo.wait_until("Change code")
            self.play(wrapped_glyphs(r436, CONF).animate.set_color(TURN), run_time=0.5)
            vo.wait_until("checked in code")
            self.play(outline_flash(VGroup(*[r.glyphs for r in r5_7 + [r8]]), HARNESS, 0.08), run_time=0.8)
            k = r14.text.index('"outcome"')
            hb = col_box(r14, k, k + len('"outcome": "unchanged"'), TURN)
            self.play(Create(hb), run_time=0.35)
            stick(self, [(r14, hb)])
            et6 = pin_tag(self, t, r14, grey_tag("an error before and after"), run_time=0.35)

        # ========================================================== 7 · compare flags a flip; here: error → error
        ex7 = excerpt_chip(FLIP, f"{EVAL_PY} · line 153 (excerpt)", line=source_line(EVAL_PY, 153))
        place(ex7, left=-SAFE + 0.05, top=2.7)
        chip_w = mono("missing-details #2", CAPTION).width + 0.5
        spec = ((1, ERR, HARNESS, "improved", HARNESS), (2, HARNESS, ERR, "regressed", ERR),
                (3, HARNESS, ERR, "regressed", ERR), (4, HARNESS, ERR, "regressed", ERR))
        prow = VGroup(*[pair_row(k, b, a, w, c, chip_w) for k, b, a, w, c in spec])
        prow.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        ptag = illustration_tag()
        place(ptag, left=-SAFE + 0.1, top=ex7.get_bottom()[1] - 0.16)
        place(prow, left=-SAFE + 0.1, top=ptag.get_bottom()[1] - 0.14)
        ptag2 = grey_tag("this run · enriched · context-live-a → context-live-b")
        place(ptag2, left=ptag.get_left()[0], cy=ptag.get_center()[1])
        bal = Balance(width=4.2)
        cA = json_card(["batch A"], S.GREY)
        cB = json_card(["batch B"], S.GREY)
        bal.move_to([4.15, 0.0, 0])
        place(bal, bottom=-0.75)
        for c_, pan in ((cA, bal.beam_g[1][0]), (cB, bal.beam_g[1][1])):
            c_.move_to(pan.get_center() + UP * (c_.height / 2 + 0.04))     # on the pans (load()'s spot)
        bal.load(cA, cB)                     # members of the beam: they tilt with it (already in place)
        btag = illustration_tag()
        place(btag, right=SAFE, bottom=max(cA.get_top()[1], cB.get_top()[1]) + 0.2)
        bnote = label("only the prompt changed", CAPTION, HARNESS)
        place(bnote, cx=bal.get_center()[0], top=bal.get_bottom()[1] - 0.12)
        for m in (ex7, prow, ptag, ptag2, bal, bnote, btag):
            inside(m)
        assert bnote.get_bottom()[1] > STRIP_TOP + 0.1, bnote.get_bottom()
        assert prow.get_bottom()[1] > STRIP_TOP + 0.15, prow.get_bottom()
        apart(ex7, tr, 0.05)
        apart(prow, bal, 0.3)
        apart(ptag2, bal, 0.2)
        apart(ex7, bal, 0.1)
        apart(btag, ex7, 0.05)
        # the excerpt's two outcome words light with the flips they name (colour only, nothing filled)
        flip_up, flip_dn = text_glyphs(ex7.text, '"improved"'), text_glyphs(ex7.text, '"regressed"')
        with self.voiceover(SAY[7]) as vo:
            # the 5.9 s line carries two pictures: the set-up rides on the shrink, so the flips can
            # be read before "here every run errored" turns them into this run's pairs
            fit(self, t, 3, keep=rows_of(cc) + [r14], tags=bar_tags, run_time=0.7, more=[FadeOut(chip5)])
            for r in prow:
                for m in (r.after, r.word):
                    hide_all(m)
            self.play(FadeIn(ex7, shift=DOWN * 0.1), FadeIn(bal, shift=DOWN * 0.1), FadeIn(btag), FadeIn(bnote),
                      FadeIn(ptag), LaggedStart(*[FadeIn(VGroup(r.card, r.before, r.arr), shift=RIGHT * 0.1)
                                                 for r in prow], lag_ratio=0.12), run_time=0.7)
            vo.wait_until("only when pass or fail flips")
            for r in prow:
                _set_op(r.after)
                _set_op(r.word)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r.after, scale=1.4), FadeIn(r.word, shift=LEFT * 0.1))
                                    for r in prow], lag_ratio=0.25),
                      flip_up.animate.set_color(HARNESS), flip_dn.animate.set_color(ERR), run_time=0.9)
            vo.wait_until("every run errored")
            # the real runs of this A/B: every illustrative part leaves first (tag, labels, outcomes,
            # row 4's dots), then the real ones arrive together and the dots turn RED (errors)
            new_labels = [mono(s, CAPTION, INK).move_to(r.card.frame) for r, s in zip(prow, REAL_ROWS)]
            words = []
            for i, r in enumerate(prow):
                w = label("unchanged" if i < 3 else "missing", CAPTION, S.GREY)
                w.move_to(r.word, aligned_edge=LEFT)
                words.append(w)
            holes = (hollow(prow[3].before), hollow(prow[3].after))
            self.play(FadeOut(ptag), *[FadeOut(r.label) for r in prow], *[FadeOut(r.word) for r in prow],
                      FadeOut(prow[3].before), FadeOut(prow[3].after),
                      flip_up.animate.set_color(INK), flip_dn.animate.set_color(INK), run_time=0.35)
            self.play(FadeIn(ptag2), *[FadeIn(nl) for nl in new_labels], *[FadeIn(w, shift=LEFT * 0.08) for w in words],
                      *[d.animate.set_color(ERR) for r in prow[:3] for d in (r.before, r.after)],
                      FadeIn(holes[0]), FadeIn(holes[1]), prow[3].card.frame.animate.set_stroke(S.GREY_DARK),
                      run_time=0.5)
            for r, nl in zip(prow, new_labels):
                r.card.remove(r.label)
                r.card.add(nl)
                r.label = nl
            pic7_rest = VGroup(*words, *holes)
            # the balance weighs A against B and settles level: nothing flipped
            self.play(Succession(bal.tilt(0.05, run_time=0.25), bal.tilt(-0.1, run_time=0.35),
                                 bal.tilt(0.05, run_time=0.25)), run_time=0.85)
        self.wait(0.8)                                  # read this run's pairs before the extra
        pic7 = VGroup(ex7, ptag2, *[VGroup(r.card, r.arr) for r in prow], *[r.before for r in prow[:3]],
                      *[r.after for r in prow[:3]], pic7_rest, bal, btag, bnote)

        # ========================================================== 8 · extra: two scripted batches compare unchanged
        xc8 = extra_card("a second scripted batch, context-fixture-2, with the v2 prompt file",
                         title="an extra · in the study guide")
        place(xc8, cx=0, cy=0.65)
        inside(xc8)
        apart(xc8, tr, 0.1)
        c765 = top_chip(R765, where="README.md · line 765", expected=True)
        apart(c765, tr, 0.01)
        with self.voiceover(SAY[8]) as vo:
            # the live compare's YELLOW box and its tag leave with the picture: the look-here-now
            # mark must not stay on an old row while the scripted compare is typed under it
            for m in (hb, et6):
                r14.remove(m)
                self.add(m)
            self.play(FadeOut(pic7), FadeOut(hb), FadeOut(et6), caption_extra(tr, True), run_time=0.5)
            self.play(FadeIn(xc8, shift=UP * 0.1), run_time=0.45)
            vo.wait_until("comparing two scripted batches")
            self.wait(0.6)
            self.play(FadeOut(xc8), run_time=0.35)
            fit(self, t, 12, tags=bar_tags, run_time=0.6)
            assert c765.get_bottom()[1] > t.box.get_top()[1] + 0.05
            cf = type_cmd(self, t, CMD_FIX, 0.7)
            # the command starts under the prompt and fills its row: the tag goes on the prompt's row
            pin_tag(self, t, rows_of(cf)[0], extra_tag(), run_time=0.3)
            # a … for lines 10-13 ("results": [ {, case_id, repetition), as at the live compare
            of = show(self, t, CMP_FIX, (5, 9), "…", 14, run_time=0.5)
            f14 = of[6]
            assert f14.text == CMP_FIX.line(14)
            vo.wait_until("reports all four")
            all4 = beside(grey_tag("the same for all 4 runs"), t, f14)
            pin(self, f14, all4, run_time=0.6,
                anim=AnimationGroup(Indicate(substring(f14, '"unchanged"'), color=TURN, scale_factor=1.2),
                                    FadeIn(all4, shift=LEFT * 0.1)))
            vo.wait_until("because fixtures")
            self.play(FadeIn(c765, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 9 · step 4: what the checks establish
        cc9 = check_card()
        place(cc9, cx=0, cy=-0.35)
        inside(cc9)
        apart(cc9, tr, 0.1)
        u1 = under(text_glyphs(cc9.s1[0], "cart validity"), HARNESS, stroke=4, buff=0.06)
        u2 = under(text_glyphs(cc9.s1[1], "approval ordering"), HARNESS, stroke=4, buff=0.06)
        ticks = [check_mark(0.26, TURN, 5).move_to(b).shift(UP * 0.03 + RIGHT * 0.03) for b in cc9.boxes]
        with self.voiceover(SAY[9]) as vo:
            tr = switch_section(self, tr, "Eval4", 1, run_time=0.8)
            self.play(FadeOut(t), FadeOut(nk), FadeOut(off), FadeOut(c765), run_time=0.45)
            self.play(FadeIn(cc9, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("They check properties")
            self.play(Create(u1), run_time=0.4)
            vo.wait_until("approval order")
            self.play(Create(u2), run_time=0.4)
            vo.wait_until("the prose needs")
            self.play(outline_flash(cc9.items, TURN, 0.12), run_time=0.9)
            # the ticks run under "with the README's five questions" (on "five questions" the fifth
            # landed as the card left)
            vo.wait_until("with the README")
            for tk in ticks:
                self.play(Create(tk), run_time=0.25)
        pic9 = VGroup(cc9, u1, u2, *ticks)

        # ========================================================== 10 · slide 41: three judges, two used here
        lr41 = lref("41")
        jd = Judges()
        place(jd, cx=0, cy=1.55)
        hum, llm, chk = jd.judge(0), jd.judge(1), jd.judge(2)
        ctag = concept_tag()
        place(ctag, cx=llm.frame.get_center()[0], bottom=llm.frame.get_top()[1] + 0.12)
        nj = excerpt_chip(NO_JUDGE, f"{CTX_PY} · line 1 (excerpt)", line=source_line(CTX_PY, 1))
        place(nj, cx=llm.frame.get_center()[0], top=llm.frame.get_bottom()[1] - 0.3)
        rep = excerpt_chip(REPORT_ROW, "outputs/reports/context-fixture-1.html · a report row (excerpt)",
                           line=CARD.line(38), frame=TURN)
        place(rep, left=hum.frame.get_left()[0], top=nj.get_bottom()[1] - 0.3)
        mini = BoundaryMini(upto=6)
        ay = rep.get_bottom()[1] - 0.45
        lean = arrow(np.array([hum.frame.get_left()[0] + 0.2, ay, 0]),
                     np.array([mini.get_left()[0] - 0.35, ay, 0]), HARNESS, stroke=6, buff=0.0)
        lcap = label("as far toward code as the task allows — same rule as the harness", CAPTION, HARNESS)
        place(lcap, left=lean.get_left()[0], top=ay - 0.2)
        for m in (jd, ctag, nj, rep, lean, lcap, mini):
            inside(m)
        apart(jd, tr, 0.1)
        apart(ctag, lr41, 0.1)
        apart(ctag, tr, 0.1)
        apart(nj, rep, 0.1)
        apart(lcap, mini, 0.15)
        apart(lean, mini, 0.1)
        assert lcap.get_right()[0] < mini.get_left()[0] - 0.15, lcap.get_right()
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(pic9), run_time=0.5)
            for j, ph in ((chk, "code"), (llm, "a model"), (hum, "a human")):
                vo.wait_until(ph)
                self.play(FadeIn(j, shift=DOWN * 0.1), *([FadeIn(lr41)] if j is chk else []), run_time=0.4)
            vo.wait_until("This tutorial uses two")
            self.play(FadeIn(ctag, shift=DOWN * 0.08), FadeIn(nj, shift=UP * 0.08), run_time=0.5)
            vo.wait_until("code, and you")
            self.play(pulse(chk.frame, HARNESS, 8), run_time=0.6)
            vo.wait_until("and you")
            self.play(pulse(hum.frame, TURN, 8), FadeIn(rep, shift=UP * 0.08), run_time=0.6)
            vo.wait_until("Lean toward code")
            self.play(GrowArrow(lean), FadeIn(lcap, shift=RIGHT * 0.1), FadeIn(mini), run_time=0.7)
            vo.wait_until("as in the harness")
            self.play(mini.flash_green(), run_time=0.8)
        pic10 = VGroup(jd, ctag, nj, rep, lean, lcap, mini)

        # ========================================================== 11 · checkpoint; keep your cases; your turn
        c769_top = top_chip(R769, where="README.md · line 769")
        apart(c769_top, tr, 0.01)
        c769 = quote_chip("README.md · line 769", R769)
        assert abs(c769.width - c769_top.width) < 0.05, (c769.width, c769_top.width)
        c769.move_to([0, 0.4, 0])
        parts769 = [text_glyphs(c769.phrase, f, c769.src) for f in ("one observed difference", "the evidence",
                                                                      "a limitation")]
        lr42 = lref("42")
        # `--repeats 2` sits in step 4's slot inside the loop; "one prompt line" (step 3) and `--compare`
        # (step 5) would share one row of the 4.3-wide inside and touch, reading as one phrase: each
        # hangs under its own box instead (members of the cycle, clear of the arrows to step 4)
        cy.attach(3, keep_size(chip("--repeats 2", S.GREY, size=CAPTION, font=MONO)))
        hung = []
        for i, s, mono_ in ((2, "one prompt line", False), (4, "--compare", True)):
            c_ = keep_size(chip(s, S.GREY, size=CAPTION, font=MONO if mono_ else None))
            place(c_, cx=cy.box(i).frame.get_center()[0], top=cy.box(i).frame.get_bottom()[1] - 0.12)
            assert c_.get_bottom()[1] > cy.box(3).frame.get_bottom()[1], "a hung chip leaves the cycle"
            cy.add(c_)
            hung.append(c_)
        for c_, a_ in ((hung[0], cy.parts["arrows"][2]), (hung[1], cy.parts["arrows"][3])):
            apart(c_, a_, 0.2)
            apart(c_, cy.box(3), 0.3)
        cy.move_to([0, -0.05, 0])
        apart(cy, c769_top, 0.05)
        apart(cy, lr42, 0.05)
        ev = sans("the eval set is the most valuable artifact", 26, HARNESS, weight="BOLD")
        place(ev, cx=0, top=cy.get_bottom()[1] - 0.25)
        inside(ev)
        inside(cy)
        for c_ in hung:
            apart(c_, ev, 0.3)
        glow =SurroundingRectangle(cy.pile, color=HARNESS, buff=0.1, stroke_width=4, corner_radius=0.08)
        rows11 = [card_lines(CMD_A), (CMD_CP, "then edit the copy"), card_lines(CMD_B), card_lines(CMD_CMP),
                  (Prose("a batch failed? new labels for both"), S.GREY),
                  (Prose("8 live runs · billed per token"), COST)]
        # the tracker shows Step 4 by now: the header names the step these commands belong to
        tc = turn_card(rows11, width=12.6, header="evaluation step 3 · with your key")
        for k in (0, 2, 3):                          # the folded commands' continuation rows: indented 4
            for row in tc.rows[k][1:]:
                row.shift(RIGHT * 4 * cell_width(CAPTION))
        place(tc, cx=0, top=2.7)
        inside(tc)
        apart(tc, tr, 0.05)
        for k in (0, 2, 3):
            assert tc.rows[k][-1].get_right()[0] < tc.frame.get_right()[0] - 0.2, tc.rows[k][-1].get_right()
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(pic10), FadeOut(lr41), run_time=0.5)
            self.play(FadeIn(c769, shift=UP * 0.1), run_time=0.45)
            for part, ph in zip(parts769, ("one difference", "its evidence", "and one limit")):
                vo.wait_until(ph)
                self.play(Indicate(part, color=TURN, scale_factor=1.06), run_time=0.45)
            vo.wait_until("And keep your cases")
            self.play(c769.animate.move_to(c769_top), run_time=0.5)
            self.play(FadeIn(cy, scale=0.97), FadeIn(lr42), run_time=0.6)
            self.play(Create(glow), Indicate(cy.pile, color=HARNESS, scale_factor=1.2), run_time=0.6)
            vo.wait_until("the eval set")
            self.play(FadeIn(ev, shift=UP * 0.1), FadeOut(glow), run_time=0.5)
            vo.wait_until("Pause and run")
            self.play(FadeOut(VGroup(cy, ev, c769, lr42)), run_time=0.5)
            self.play(FadeIn(tc, scale=0.97), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tc, tr)), run_time=0.8)
        self.wait(0.3)
