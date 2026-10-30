"""S14 · Evaluation: the trace is the evidence (README "6 · Evaluation", steps 1 and 2).
Lecture: 39–40 (and 37).

Beats (script.md "## S14", one voiceover block each):
 0  The tracker "README › 6 · Evaluation › Step 1" (no step lit yet). Slide 39 redrawn, the LECTURE
    37, 39–40 tag arriving with it: a BLUE box "LLM · the provider's" (on "the provider's model"), a
    GREY box "Product · users, tasks, rules, cost" (on "and the product"), between them a GREY dashed box "the layers we
    build" with GREY arrows (on "is ours"); its four GREEN tiles Context · Harness · Tools · Skills
    pop in as named. On "So all of it must be tested" the RED banner "every layer we change must be
    tested" and the GREY chip (slide 37, our words) "in this class you wear every hat".
 1  The picture leaves. V8's three GREEN pills (slide 40) draw at once, empty (on "three things");
    each name writes in on its word: Outcome "did it get the right result?", Trajectory "did it get
    there sensibly?", Cost "tokens, turns, latency". On "the outcome and process checks" the check
    names of container/89 lines 39–44 slide in along their rows (from inside the band's right end):
    `outcome.proposal` into Outcome; `process.check_before_action`, `process.manager_authority`,
    `process.no_duplicate_orders` into Trajectory; on "plus calls and tokens" "model calls · input
    tokens" (line 25's column names) into Cost.
 2  TRACKER Eval1 1. The pills and the lecture tag leave. A GREEN cylinder (illustration), its PINK
    path `outputs/observability.sqlite` under it; every run of the video so far drops in as a small
    card (32, in list order: RED = the failed live runs, BLUE dashed = the scripted runs) while a
    counter climbs to 32 (tag your numbers will differ); on "including the failed live ones" the
    RED cards pulse. Then the container terminal (12 rows, GREEN title-bar tag offline · free) rises
    over it and types `python cli.py --list-runs` -> container/70 lines 2–9, …, 227; on "with status
    error" `"status": "error"` turns RED and `"mode": "live"` BLUE; GREY tag "32 runs here · your
    numbers will differ" on the closing bracket.
 3  TRACKER Eval1 2. `python cli.py --inspect-run RUN_ID` (as written) -> container/72 line 20 RED on
    "it fails"; GREY tag "a template" beside the error (the command's row is too full for it) on
    "because it's a template"; on "Paste a
    real one" the GREY caption "paste a run ID from --list-runs" beside the error. On "we use the
    manager approval run" the terminal shrinks to the 3-row strip (the error row stays), the
    cylinder returns above it (left), the manager-approval run's card (BLUE dashed, 16th) gets a
    YELLOW outline, and the real ID is pasted in the strip: `python cli.py --inspect-run
    7409b343679a457490c94fb7512faa31` (tag your numbers will differ on the prompt's row; the command
    fills the row under it).
 4  The YELLOW outline on the run's card pulses and the typed ID flashes PINK; a PINK arrow
    "7409b343…" runs from the cylinder to V8's event chain, whose five cards rise in dim; each
    lights to full as the SAY names it: approval.requested GREEN (on "with the fingerprint" the
    PINK hash chip beside it), approval.decided · human YELLOW, policy.decision · allow,
    order.placed, run.finished · completed GREEN. On "The evidence for order placed" order.placed
    pulses; the picture leaves, the terminal grows back (12 rows) and the trace prints the first
    event (container/71: …, 33 cut after the fingerprint; wrap): approval.requested GREEN, the
    fingerprint PINK and underlined, GREY tag "0245… · numbered across the whole database" on the
    `…` above it. On "not the prose" the top-band chip README.md · line 686 "Do not infer permission
    from the agent's prose". Then the trace confirms the rest of the chain line by line (…, 46, …,
    53 cut after "outcome": "allow", …, 58 cut after the ticket ID, …, 67), each event name lit as
    it prints (approval.decided and "source": "human" YELLOW, the fingerprint in 46 PINK and
    underlined, policy.decision and "allow", order.placed, run.finished and "completed" GREEN).
 5  TRACKER Eval1 2 · extra. The chip leaves. `python cli.py --inspect-run 536c6c4812c049c495a9988ed754ee49`
    (extra; your numbers will differ) -> container/73 lines 2, 5 cut after "call_number": 1, 7 folded
    to `0006 model.failed {"call_number": 1, "error": "(… Error code: 401 …` (RED; 67 characters, so
    it wraps at its JSON comma onto a hanging row: a word-boundary wrap left a lone '…' row that read
    as an elision), 10 folded to `0009 run.finished {"error": "(… Error code: 401 …`. Line 7's
    model.failed flashes on "model failed", its "Error code: 401" on "with the 401" (both YELLOW: the
    rows are RED already); on "A failure is evidence too" a YELLOW bracket in the left margin spans
    the run's events (a box round these tightly spaced rows read as an underline of the run ID).
 6  TRACKER Eval2 1 (the section switches). It types `python cli.py --act 2 --evaluate core --fixture
    --case standard --repeats 2 --label context-fixture-1` (three rows); the flags flash YELLOW as
    named (the act 2 evaluation, scripted + the GREY tag scripted, two repeats, the label) ->
    container/74 lines 2, …, 86 (GREEN), 88, 91–94. On "All 4 runs pass" line 86 flashes; on "but
    scripted runs" the top-band chip README.md · line 694 "they do not measure the model's
    context-engineering performance" (expected).
 7  TRACKER Eval2 2, 3, 4. `python cli.py --report context-fixture-1` -> container/75 lines 3
    (GREEN), 5; `python cli.py --view-report context-fixture-1` -> 76 lines 2–3, the default path
    `/app/outputs/reports/context-fixture-1.html` PINK on "to its default path"; on "or one you
    choose" `python cli.py --view-report context-fixture-1 --html-output outputs/my-report.html` ->
    77 line 2, `/app/outputs/my-report.html` PINK; then the terminal shrinks to the strip (the last
    command and its output line), so the browser can open on the next line's first words.
 8  Above the strip a GREY
    browser window (address `~/AC215/agent-harness/outputs/my-report.html`, tag illustration, no
    logo) opens on "Open it" and the page draws the scorecard from container/89 lines 13–22: the
    banner `SCRIPTED RESPONSES · These results test the evaluation machinery. …`, the tiles 4/4
    Passed / scheduled, 0 Runs with failed checks, 0 Run errors, 0 Missing runs, and the rows
    `standard:basic | 2/2 | 100% (2/2) …`, `standard:enriched | 2/2 | 100% (2/2) …`. On "from the
    outputs folder" the container box `/app/outputs/` appears under it and the address's `outputs/`
    turns PINK; on "on your laptop" the PINK bind-mount route grows to the laptop's
    `~/AC215/agent-harness/outputs/`. It holds to be read.
 9  TRACKER Eval2 5. The browser leaves, the terminal grows back; `python cli.py --view-report
    COLAB_LABEL --db outputs/colab.sqlite` (as written; tag a template) -> container/78 line 20 RED
    (wrap) with the caption "copy colab.sqlite from your Colab run into outputs/ first". TRACKER Eval2
    5 · extra: the act 2 evaluation again (extra) -> container/88 line 2 RED (wrap), caption "labels
    are immutable · choose a new one" (or "· use a new one" when that does not fit beside the
    row: it does not, at 20 pt). On "evaluation steps 1 and 2" (the error stays readable through
    "Pause and run") the terminal leaves and the static GREY
    "your turn" card arrives (the six commands of steps 1 and 2, long ones folded before an option
    with " \\" and a 4-space indent; GREEN "offline · free" last). Hold 2 s, then an empty frame.
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
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    UpdateFromAlphaFunc,
    VGroup,
    VMobject,
    Wait,
)

from common import *  # noqa: F401,F403
from common import _header_text, _save_op, _set_op, _src_find
from explainer import style as S
from explainer.devops import box, chip, glyph_range, label, line_pitch, mono, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S14"]

# ------------------------------------------------------------------ the real captures (file line numbers)
LIST = capture("container/70")
TPL = capture("container/72")
MGR = capture("container/71")
FAIL = capture("container/73")
FIX = capture("container/74")
REP = capture("container/75")
VIEW = capture("container/76")
HTML = capture("container/77")
COLAB = capture("container/78")
AGAIN = capture("container/88")
CARD = capture("container/89")
assert LIST.cmd == "python cli.py --list-runs", LIST.cmd
assert TPL.cmd == "python cli.py --inspect-run RUN_ID", TPL.cmd
assert MGR.cmd == f"python cli.py --inspect-run {RUN_MANAGER}", MGR.cmd
assert FAIL.cmd == f"python cli.py --inspect-run {RUN_FAILED}", FAIL.cmd
EVAL_CMD = "python cli.py --act 2 --evaluate core --fixture --case standard --repeats 2 --label context-fixture-1"
assert FIX.cmd == EVAL_CMD and AGAIN.cmd == EVAL_CMD, FIX.cmd
assert REP.cmd == "python cli.py --report context-fixture-1"
assert VIEW.cmd == "python cli.py --view-report context-fixture-1"
assert HTML.cmd == "python cli.py --view-report context-fixture-1 --html-output outputs/my-report.html"
assert COLAB.cmd == "python cli.py --view-report COLAB_LABEL --db outputs/colab.sqlite"
# list-runs: 32 runs, the live ones failed (status error), the scripted ones completed
RUN_IDS = [ln.split('"')[3] for ln in LIST.lines if '"run_id"' in ln]
MODES = [ln.split('"')[3] for ln in LIST.lines if '"mode"' in ln]
STATUSES = [ln.split('"')[3] for ln in LIST.lines if '"status"' in ln]
assert len(RUN_IDS) == len(MODES) == len(STATUSES) == 32
assert all((m == "live") == (s == "error") for m, s in zip(MODES, STATUSES))
K_FAILED, K_MANAGER = RUN_IDS.index(RUN_FAILED), RUN_IDS.index(RUN_MANAGER)
assert K_FAILED == 0 and MODES[K_MANAGER] == "fixture"
assert LIST.line(7).strip() == '"status": "error",' and LIST.line(8).strip() == '"mode": "live"'
assert LIST.line(227) == "]"
# the manager-approval run's entry in --list-runs: how the viewer finds their own run ID
CASE_MGR = '"case_id": "manager-approval"'
assert LIST.line(109).strip() == f'"run_id": "{RUN_MANAGER}",' and LIST.line(110).strip() == CASE_MGR + ","
ERR_RUNID = "cli.py: error: Unknown run ID"
assert TPL.line(20) == ERR_RUNID
# inspect-run (manager approval): the five events of the chain
FP = "e8caf06b29df9c585b778e2999c022c93be0896bb26bd8c5967e6fdbdb43399c"
assert FP.startswith(FINGERPRINT16)
L33 = MGR.cut(33, f'"fingerprint": "{FP}"')
assert MGR.line(33).startswith("0245 approval.requested ")
assert MGR.line(46).startswith("0258 approval.decided ") and '"source": "human"' in MGR.line(46)
assert MGR.line(46).count(FP) == 1
L53 = MGR.cut(53, '"outcome": "allow"')
assert L53.startswith("0265 policy.decision ")
L58 = MGR.cut(58, '"approval_ticket_id": "c48487091d824bd5a2575417247c17a1"')
assert L58.startswith("0270 order.placed ")
assert MGR.line(67) == '0279 run.finished {"error": null, "status": "completed"}'
# inspect-run (the first failed live run)
F5 = FAIL.cut(5, '"call_number": 1,')
F7 = FAIL.fold(7, 7, '0006 model.failed {"call_number": 1, "error": "(… Error code: 401 …')
F10 = FAIL.fold(10, 10, '0009 run.finished {"error": "(… Error code: 401 …')
_k = F7.index(' "error"')
F7A, F7B = F7[:_k], " " * WRAP_HANG + F7[_k + 1:]          # two rows of the one folded line
assert len(F7A) <= 65 and len(F7B) <= 65 and F7A.endswith('"call_number": 1,'), (F7A, F7B)
assert FAIL.line(2) == '0001 run.started {"act": 1, "mode": "live"}'
# step 2
L86 = "FIXTURE EVALUATION context-fixture-1: 4/4 scheduled runs passed"
assert FIX.line(86) == L86 and REP.line(3) == L86
for _n in (91, 92, 93, 94):
    assert FIX.line(_n).startswith("PASS standard:")
P_DEFAULT = "/app/outputs/reports/context-fixture-1.html"
P_MINE = "/app/outputs/my-report.html"
assert VIEW.line(2) == f"Saved evaluation report: {P_DEFAULT}"
assert HTML.line(2) == f"Saved evaluation report: {P_MINE}"
assert COLAB.line(20) == "cli.py: error: Recorded database not found: /app/outputs/colab.sqlite"
assert AGAIN.line(2).startswith("Evaluation stopped: Experiment label already exists.")
# the pills' check names (the evaluation report's checks) and the effort columns
CHECKS = ((0, "outcome.proposal", 39), (1, "process.check_before_action", 40),
          (1, "process.manager_authority", 42), (1, "process.no_duplicate_orders", 43))
for _i, _s, _n in CHECKS:
    assert CARD.line(_n).startswith(_s + " | pass"), (_n, CARD.line(_n))
assert "Mean model calls" in CARD.line(25) and "Mean input tokens" in CARD.line(25)
COST_CHIP = "model calls · input tokens"
# the scorecard (container/89 lines 13-22)
BANNER = CARD.cut(13, "evaluation machinery.")
assert BANNER.startswith("SCRIPTED RESPONSES · ")
TILES = (("4/4", "Passed / scheduled", 15), ("0", "Runs with failed checks", 16),
         ("0", "Run errors", 17), ("0", "Missing runs", 18))
for _num, _lbl, _n in TILES:
    assert CARD.line(_n) == _num + _lbl, (_n, CARD.line(_n))
ROWS = [CARD.cut(n, "100% (2/2)") for n in (21, 22)]
assert ROWS[0].startswith("standard:basic | 2/2 | ") and ROWS[1].startswith("standard:enriched | 2/2 | ")

# ------------------------------------------------------------------ sources (exact sub-strings, checked)
RD = "README.md"
R686 = "Do not infer permission from the agent's prose"
assert R686 in source_line(RD, 686) and source_line(RD, 686).startswith("**Checkpoint:**")
R694 = "do not measure the model's context-engineering performance"     # (13.0 wide with the tag)
assert R694 in source_line(RD, 694)
for _n, _c in ((675, LIST.cmd), (681, TPL.cmd), (691, EVAL_CMD), (699, REP.cmd), (705, VIEW.cmd),
               (713, HTML.cmd), (714, COLAB.cmd)):
    assert source_line(RD, _n).strip() == _c, (_n, source_line(RD, _n))
HOST_OUT = "~/AC215/agent-harness/outputs/"

# ------------------------------------------------------------------ layout
SAFE = 6.45
TITLE = 24


# ------------------------------------------------------------------ small helpers (S13's idiom)
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


def glow(glyphs, color: str = TURN, grow: float = 0.06, cap: float = 1.12):
    """Indicate one span of terminal text about its own centre, growing at most `grow` per side,
    so it never closes the space to its neighbours or runs past the text margin (a long span
    flashes mostly by colour)."""
    k = min(cap, 1 + 2 * grow / max(glyphs.width, 0.1))
    return Indicate(glyphs, color=color, scale_factor=k)


def margin_bracket(rows, color: str = TURN, gap: float = 0.16, tick: float = 0.08) -> VMobject:
    """A thin bracket in the terminal's left margin spanning `rows` (stroke only: it never reads as
    an underline of the row above, as a box round tightly spaced rows does)."""
    g = VGroup(*rows)
    top, bot = g.get_top()[1] + 0.02, g.get_bottom()[1] - 0.02
    x = g.get_left()[0] - gap
    ln = VMobject(stroke_color=color, stroke_width=4)
    ln.set_points_as_corners([[x + tick, top, 0], [x, top, 0], [x, bot, 0], [x + tick, bot, 0]])
    return ln


def pulse(frame, color: str | None = None, width: float = 8.0):
    """A frame pulses: a thick outline (no fill) over it fades in and out."""
    ol = frame.copy().set_fill(opacity=0).set_stroke(color or frame.get_stroke_color(), width)
    return Succession(FadeIn(ol, run_time=0.3), FadeOut(ol, run_time=0.45))


def apart(a, b, gap: float = 0.06):
    """Assert that the bounding boxes of a and b are at least `gap` apart (no overlap)."""
    ok = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
          or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    assert ok, (a.get_corner(DOWN + LEFT), a.get_corner(UP + RIGHT), b.get_corner(DOWN + LEFT), b.get_corner(UP + RIGHT))


def inside(m, x0: float = -6.55, x1: float = 6.55, y0: float = -3.55, y1: float = 3.55):
    assert m.get_left()[0] >= x0 and m.get_right()[0] <= x1 and m.get_bottom()[1] >= y0 and m.get_top()[1] <= y1, \
        (m.get_corner(DOWN + LEFT), m.get_corner(UP + RIGHT))


def bar_y(t, rows: int) -> float:
    """The title bar's centre y of the house terminal `t` at `rows` rows (bottom edge fixed)."""
    return strip_top(rows) - t.bar_h / 2


def fit(scene, t, rows: int, keep=None, tags=(), run_time: float = 0.8):
    """resize(), with the title-bar tags riding along on the bar (S08's / S13's idiom)."""
    y = bar_y(t, rows)
    title, t.title = t.title, None
    try:
        resize(scene, t, rows, keep=keep, run_time=run_time,
               extra=[title.animate.set_y(y), *[m.animate.set_y(y) for m in tags]])
    finally:
        t.title = title


def arrow(a, b, color: str = S.GREY, stroke: float = 3, buff: float = 0.06):
    return Arrow(a, b, buff=buff, color=color, stroke_width=stroke, tip_length=0.16,
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


def per_row(rows, sub: str) -> list:
    """[(row, glyphs)] of `sub` in ONE printed (wrapped) line, one entry per row it spans."""
    i, j = _src_find(rows, sub)
    out = []
    for r in rows:
        a, b = r.src_span
        lo, hi = max(i, a), min(j, b)
        if lo < hi:
            out.append((r, glyph_range(r, lo - a + r.src_indent, hi - a + r.src_indent)))
    return out


def stick(scene, pairs) -> None:
    """After their play: make each mob part of its terminal row (as pin() does), so it scrolls and
    fades with the row."""
    for row, mob in pairs:
        scene.remove(mob)
        row.add(mob)
        scene.add(row)


def pin_tag(scene, t, line, tag_, run_time: float = 0.35):
    """beside() + pin(): a tag right after a line's text (its last row when folded)."""
    beside(tag_, t, line)
    return pin(scene, line, tag_, run_time=run_time)


def row_tag(s: str, color: str = S.GREY) -> VGroup:
    """A tag beside a terminal row whose pill is lower than the row pitch, so the tags of two
    neighbouring rows never touch (S16's row_tag; the shared tag() pill is taller than the pitch).
    .box .text"""
    g = tag(s, color, size=CAPTION)
    h = line_pitch(TERM_PT) - 0.08
    if g.box.height > h:
        b = RoundedRectangle(width=g.box.width, height=h, corner_radius=h / 2, stroke_color=color,
                             stroke_width=2).set_fill(S.BG, 0.92).move_to(g.box)
        g.submobjects[g.submobjects.index(g.box)] = b
        g.box = b
        g.text.move_to(b)
    return keep_size(g)


def hide_all(m) -> None:
    _save_op(m)
    _set_op(m, 0)


def run_card(live: bool) -> VGroup:
    """A run as a small card: RED (a live run that failed at the 401) or BLUE dashed (scripted)."""
    r = RoundedRectangle(width=0.28, height=0.18, corner_radius=0.04)
    if live:
        r.set_stroke(ERR, 2.5).set_fill(ERR, 0.4)
        return VGroup(r)
    r.set_fill(opacity=0)
    d = DashedVMobject(r, num_dashes=8, dashed_ratio=0.6).set_stroke(CLOUD, 2.5)
    return VGroup(d)


def tile_box(text: str, color: str, w: float, h: float) -> VGroup:
    fr = box(w, h, color, fill_opacity=0.14, stroke=3, radius=0.12)
    t = sans(text, TITLE, INK)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def two_line_box(head: str, sub_rows, color: str, w: float, h: float, sub_color: str = INK) -> VGroup:
    fr = box(w, h, color, fill_opacity=0.14, stroke=3, radius=0.14)
    rows = VGroup(sans(head, TITLE, INK, weight="BOLD"),
                  *[label(s, CAPTION, sub_color) for s in sub_rows]).arrange(DOWN, buff=0.08)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.text = fr, rows
    return g


# ------------------------------------------------------------------ the scene
class TraceEvidence(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0 · slide 39: what we build must be tested
        tr = tracker("Eval1")
        lr = lref("37, 39–40")
        Y0 = 1.0
        llm = two_line_box("LLM", ["the provider's"], CLOUD, 2.5, 1.5)
        llm.move_to([-5.0, Y0, 0])
        prod = two_line_box("Product", ["users, tasks,", "rules, cost"], S.GREY, 2.5, 1.5)
        prod.move_to([5.0, Y0, 0])
        mid = box(5.7, 3.0, S.GREY, dashed=True, radius=0.2)
        mid.move_to([0, Y0, 0])
        mid_t = note("the layers we build")
        place(mid_t, cx=0, top=mid.get_top()[1] - 0.18)
        tiles = [tile_box(s, HARNESS, 2.4, 0.72) for s in ("Context", "Harness", "Tools", "Skills")]
        grid = VGroup(*tiles).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.26))
        place(grid, cx=0, top=mid_t.get_bottom()[1] - 0.22)
        a1 = arrow(llm.frame.get_right(), mid.get_left(), S.GREY, stroke=4)
        a2 = arrow(mid.get_right(), prod.frame.get_left(), S.GREY, stroke=4)
        ban_t = label("every layer we change must be tested", TITLE, ERR)
        ban_f = RoundedRectangle(width=ban_t.width + 0.6, height=ban_t.height + 0.32, corner_radius=0.12,
                                 stroke_color=ERR, stroke_width=3).set_fill(ERR, 0.08)
        ban_t.move_to(ban_f)
        banner = VGroup(ban_f, ban_t)
        place(banner, cx=0, top=mid.get_bottom()[1] - 0.35)
        hats = chip("in this class you wear every hat", S.GREY, size=CAPTION)
        place(hats, cx=0, top=banner.get_bottom()[1] - 0.3)
        pic0 = VGroup(llm, prod, mid, mid_t, grid, a1, a2, banner, hats)
        for m in pic0:
            inside(m)
        apart(mid, tr, 0.1)
        apart(prod, lr, 0.1)
        apart(llm, mid, 0.3)
        apart(mid, prod, 0.3)
        assert grid.get_bottom()[1] > mid.get_bottom()[1] + 0.1
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), run_time=0.5)
            vo.wait_until("the provider's model")
            # the lecture tag arrives with the picture it cites (and leaves with slide 40's pills)
            self.play(FadeIn(llm, shift=RIGHT * 0.15), FadeIn(lr), run_time=0.5)
            vo.wait_until("and the product")
            self.play(FadeIn(prod, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("is ours")
            self.play(Create(mid), FadeIn(mid_t), GrowArrow(a1), GrowArrow(a2), run_time=0.6)
            for tl, word in zip(tiles, ("context", "harness", "tools", "skills")):
                vo.wait_until(word)
                self.play(FadeIn(tl, scale=0.9), run_time=0.3)
            vo.wait_until("So all of it must be tested")
            self.play(FadeIn(banner, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(hats, shift=UP * 0.08), run_time=0.4)

        # ========================================================== 1 · slide 40: outcome, trajectory, cost
        tp = ThreePills()
        tp.move_to([0, -0.05, 0])           # centred in the frame under the top band
        for b in tp.bands:
            hide_all(b)
        chips = []
        # (pad_y 0.07: three chips stack in the Trajectory band with a visible gap; at the default
        # 0.12 they touched at ThreePills' 0.52 row pitch)
        for i, s, _ in CHECKS:
            c = keep_size(chip(s, HARNESS, size=CAPTION, font=MONO, pad_y=0.07))
            chips.append((i, c))
        chips.append((2, keep_size(chip(COST_CHIP, HARNESS, size=CAPTION, pad_y=0.07))))
        assert all(c.height < 0.44 for _, c in chips), [round(c.height, 2) for _, c in chips]
        inside(tp)
        apart(tp, tr, 0.1)
        apart(tp, lr, 0.1)

        def drop(i, c):
            tp.start(i, c)
            # start inside the band (its right edge clear of the border), then slide left along the row
            c.shift(LEFT * max(0.0, c.get_right()[0] - (tp.bands[i].frame.get_right()[0] - 0.2)))
            tp.bands[i].add(c)          # a member before it shows: drawn once, moves with the band
            self.play(FadeIn(c, shift=LEFT * 0.2), run_time=0.25)
            self.play(tp.drop(i, c, run_time=0.45))

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(pic0), run_time=0.5)
            self.add(tp)
            # "three things": the three empty GREEN pills at once (no empty frame); each name on its word
            for b in tp.bands:
                _set_op(b.frame)
            self.play(LaggedStart(*[FadeIn(b.frame, shift=DOWN * 0.1) for b in tp.bands], lag_ratio=0.25),
                      run_time=0.8)
            for i, word in enumerate(("outcome", "trajectory", "and cost")):
                vo.wait_until(word)
                _set_op(tp.bands[i].title)
                self.play(FadeIn(tp.bands[i].title, shift=RIGHT * 0.12), run_time=0.4)
            vo.wait_until("the outcome and process checks")
            drop(*chips[0])
            for i, c in chips[1:4]:
                drop(i, c)
            vo.wait_until("plus calls and tokens")
            drop(*chips[4])

        # ========================================================== 2 · step 1: every run, one database; --list-runs
        cyl = cylinder(3.0, 2.0)
        cyl.remove(cyl[3])          # the two disk arcs: behind a full pile they read as threads through the cards
        cards = [run_card(m == "live") for m in MODES]
        CW, CH, GX, GY = 0.28, 0.18, 0.07, 0.1
        for k, c in enumerate(cards):
            col, row = k % 8, k // 8                    # the first runs at the bottom: a growing pile
            c.move_to([(col - 3.5) * (CW + GX), (row - 1.5) * (CH + GY), 0])
        pile = VGroup(*cards)
        # centred in the cylinder's visible body (under the lid's front edge), not in its bounding box
        pile.shift(DOWN * 0.42)
        cyl_g = VGroup(cyl, pile)
        for c in cards:
            hide_all(c)
        CX, CY = -1.4, 0.55
        cyl_g.move_to([CX, CY, 0])
        lbl1 = mono("outputs/observability.sqlite", CAPTION, LOOKUP)
        place(lbl1, cx=CX, top=cyl.get_bottom()[1] - 0.15)
        cnt = Counter("runs", 0, size=26)
        place(cnt, left=cyl.get_right()[0] + 0.6, cy=CY + 0.25)
        dif = differ_tag()
        place(dif, left=cnt.get_left()[0], top=cnt.get_bottom()[1] - 0.2)
        ill = illustration_tag()
        place(ill, left=cnt.get_left()[0], bottom=cyl.get_top()[1] - 0.05)
        pic2 = VGroup(cyl_g, lbl1, cnt, dif, ill)
        for m in pic2:
            inside(m)
        apart(cyl_g, tr, 0.1)
        apart(ill, tr, 0.1)
        t = term(container=True, rows=12)
        ft = frame_tags(t, offline_tag())
        reds = VGroup(*[c for c, m in zip(cards, MODES) if m == "live"])
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(tp), FadeOut(lr), tr.goto(1), run_time=0.5)
            self.play(FadeIn(cyl_g), FadeIn(lbl1, shift=UP * 0.08), FadeIn(cnt), FadeIn(ill), run_time=0.5)
            for c in cards:
                _set_op(c)
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.6) for c in cards], lag_ratio=0.15),
                      cnt.count_to(32, run_time=2.6), run_time=2.6)
            self.play(FadeIn(dif, shift=UP * 0.08), run_time=0.35)
            vo.wait_until("in one SQLite database")
            self.play(pulse(cyl.top, HARNESS), run_time=0.75)
            vo.wait_until("including the failed live ones")
            # each RED card pulses about its own centre (a group Indicate would spread them over the BLUE ones)
            self.play(LaggedStart(*[Indicate(c, color=ERR, scale_factor=1.3) for c in reds], lag_ratio=0.02),
                      run_time=0.7)
            cnt.freeze()
            self.play(FadeOut(pic2), FadeIn(t, shift=UP * 0.3), FadeIn(ft, shift=UP * 0.3), run_time=0.6)
            type_cmd(self, t, LIST.cmd, 0.8)
            o70 = show(self, t, LIST, (2, 9), "…", 227, run_time=0.5)
            vo.wait_until("with status error")
            r7, r8 = o70[5], o70[6]
            assert r7.text == LIST.line(7) and r8.text == LIST.line(8)
            self.play(substring(r7, '"status": "error"').animate.set_color(ERR),
                      substring(r8, '"mode": "live"').animate.set_color(CLOUD), run_time=0.4)
            r227 = o70[-1]
            pin_tag(self, t, r227, grey_tag("32 runs here · your numbers will differ"))

        # ========================================================== 3 · RUN_ID is a template; we use the manager run
        lbl2 = VGroup(mono("outputs/", CAPTION, LOOKUP), mono("observability.sqlite", CAPTION, LOOKUP))
        lbl2.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        hl = SurroundingRectangle(cards[K_MANAGER], color=TURN, buff=0.05, stroke_width=3, corner_radius=0.04)
        with self.voiceover(SAY[3]) as vo:
            self.play(tr.goto(2), run_time=0.4)
            c3 = type_cmd(self, t, TPL.cmd, 0.9)
            vo.wait_until("it fails")
            e20 = show(self, t, TPL, (TPL.line(20), ERR), run_time=0.4)[0]
            vo.wait_until("because it's a template")
            tt3 = pin_tag(self, t, e20, row_tag("a template"))          # the command's row is too full for it
            vo.wait_until("Paste a real one")
            cap3 = note("paste a run ID from --list-runs")
            place(cap3, left=tt3.get_right()[0] + 0.25, cy=tt3.get_center()[1])
            assert cap3.get_right()[0] < t.box.get_right()[0] - 0.12, cap3.get_right()
            pin(self, e20, cap3, run_time=0.4)
            vo.wait_until("we use the manager approval run")
            fit(self, t, 3, keep=[e20], tags=list(ft), run_time=0.7)
            # the cylinder returns above the strip, at the left (shapes only: no text is scaled)
            cyl_g.scale(0.85)
            cyl_g.move_to([-4.85, 0.75, 0])
            place(lbl2, left=cyl.get_left()[0] - 0.25, top=cyl.get_bottom()[1] - 0.12)
            hl.move_to(cards[K_MANAGER])
            ill4 = illustration_tag()
            place(ill4, left=cyl.get_left()[0] - 0.25, bottom=cyl.get_top()[1] + 0.12)
            # how to find it: its --list-runs entry names the case (container/70 line 110), so the
            # viewer looks up their own manager-approval run the same way
            case3 = grey_tag(f"its --list-runs entry: {CASE_MGR}")
            place(case3, left=cyl.get_right()[0] + 0.35, cy=hl.get_center()[1])
            for m in (cyl_g, lbl2, ill4, case3):
                inside(m)
            assert lbl2.get_bottom()[1] > STRIP_TOP + 0.12, lbl2.get_bottom()
            assert case3.get_bottom()[1] > STRIP_TOP + 0.3, case3.get_bottom()
            apart(ill4, tr, 0.05)
            apart(case3, cyl_g, 0.2)
            self.play(FadeIn(cyl_g), FadeIn(lbl2), FadeIn(ill4), run_time=0.5)
            self.play(Create(hl), FadeIn(case3, shift=LEFT * 0.1), run_time=0.4)
            # ... and its real ID is pasted in the strip (the command fills its row: it starts under the
            # prompt, so the tag goes on the prompt's row)
            c4 = type_cmd(self, t, MGR.cmd, 0.9)
            assert len(t.lines) == 3 and t.lines[0] is e20, [ln.text for ln in t.lines]
            pin_tag(self, t, rows_of(c4)[0], row_tag("your numbers will differ"), run_time=0.3)

        # ========================================================== 4 · the run's events, then the trace confirms them
        ec = EventChain()
        place(ec, cx=0.75, top=3.0)         # 4.3 tall: the top band is free (the lecture tag left)
        c0, c2 = ec.card(0), ec.card(2)
        fpc = hash_chip(FINGERPRINT16)
        place(fpc, left=c0.get_right()[0] + 0.25, cy=c0.get_center()[1])
        # the run is looked up by its ID: a PINK arrow from the database to the chain's middle
        ay = c2.get_center()[1]
        start = np.array([cyl.get_right()[0] + 0.12, ay, 0])
        end = np.array([c2.get_left()[0] - 0.08, ay, 0])
        look = arrow(start, end, LOOKUP, stroke=4, buff=0.0)
        rid = mono(RUN_MANAGER[:8] + "…", CAPTION, LOOKUP)
        place(rid, cx=(start[0] + end[0]) / 2, bottom=ay + 0.14)
        for m in (ec, fpc, look, rid):
            inside(m)
        assert ec.get_bottom()[1] > STRIP_TOP + 0.12, ec.get_bottom()
        apart(ec, lbl2, 0.1)
        apart(ec, cyl_g, 0.3)
        apart(rid, cyl_g, 0.05)
        apart(rid, ec, 0.08)
        apart(ec, tr, 0.1)
        assert look.get_length() > 1.2, look.get_length()
        apart(fpc, ec.card(1), 0.05)
        c686 = top_chip(R686, where="README.md · line 686")
        pic4 = VGroup(cyl_g, hl, lbl2, ill4, look, rid, ec, fpc)
        # the run's five events arrive dim with the lookup (the arrow has a target), then each lights
        # to full as the SAY reads it (opacity scaled from the parts' saved values: no fill jumps)
        DIM = 0.22
        ev = [[ec.parts[f"c{i}"]] + ([ec.parts[f"a{i - 1}"]] if i else []) for i in range(5)]

        def brighten(i):
            return [UpdateFromAlphaFunc(m, lambda mob, a: _set_op(mob, DIM + (1 - DIM) * a)) for m in ev[i]]

        id_glyphs = typed_glyphs(c4, RUN_MANAGER)
        with self.voiceover(SAY[4]) as vo:
            self.add(ec)
            # this run: the manager-approval one, the ID just pasted
            self.play(pulse(hl, TURN, 6), glow(id_glyphs, LOOKUP), run_time=0.7)
            self.play(FadeOut(case3), run_time=0.3)       # it sits where the chain rises: gone first
            for grp in ev:
                for m in grp:
                    _set_op(m, DIM)
            self.play(GrowArrow(look), FadeIn(rid, shift=RIGHT * 0.1),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.12) for grp in ev for m in grp], lag_ratio=0.08),
                      run_time=0.8)
            names = ("approval requested", "approval decided by a human", "policy decision allow",
                     "order placed", "run finished")
            for i, word in enumerate(names):
                vo.wait_until(word)
                self.play(*brighten(i), run_time=0.4)
                if i == 0:
                    vo.wait_until("with the fingerprint")
                    self.play(FadeIn(fpc, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("The evidence for order placed")
            self.play(pulse(ec.card(3).frame, HARNESS, 9), run_time=0.7)
            self.play(FadeOut(pic4), run_time=0.3)
            fit(self, t, 12, tags=list(ft), run_time=0.55)
            # "is an event": the trace prints the chain's first event (the command was typed in beat 3)
            o33 = show(self, t, MGR, "…", L33, wrap=True, run_time=0.35)
            r33 = item_rows(o33, 1)
            fp33 = per_row(r33, FP)
            u33 = [(r, under(g, LOOKUP, stroke=3, buff=0.04)) for r, g in fp33]
            numtag = grey_tag("0245… · numbered across the whole database")
            beside(numtag, t, o33[0])
            assert not covers_text(numtag, o33[0])
            self.play(substring(r33[0], "approval.requested").animate.set_color(HARNESS),
                      *[g.animate.set_color(LOOKUP) for _, g in fp33], *[Create(u) for _, u in u33],
                      FadeIn(numtag, shift=LEFT * 0.1), run_time=0.4)
            stick(self, u33 + [(o33[0], numtag)])
            vo.wait_until("not the prose")
            self.play(FadeIn(c686, shift=DOWN * 0.1), run_time=0.45)
            # then the rest of the chain, line by line (the end runs past the SAY: kept brisk)
            o46 = show(self, t, MGR, "…", 46, wrap=True, run_time=0.35)
            r46 = item_rows(o46, 1)
            fp46 = per_row(r46, FP)
            u46 = [(r, under(g, LOOKUP, stroke=3, buff=0.04)) for r, g in fp46]
            self.play(substring(r46[0], "approval.decided").animate.set_color(TURN),
                      wrapped_glyphs(r46, '"source": "human"').animate.set_color(TURN),
                      *[g.animate.set_color(LOOKUP) for _, g in fp46], *[Create(u) for _, u in u46],
                      run_time=0.35)
            stick(self, u46)
            # the last three events print in one go (staggered, in order), then light together
            o = show(self, t, MGR, "…", L53, "…", L58, "…", 67, wrap=True, run_time=0.7)
            lit = []
            for k, subs in ((1, ("policy.decision", '"outcome": "allow"')), (3, ("order.placed",)),
                            (5, ("run.finished", '"status": "completed"'))):
                rr = item_rows(o, k)
                lit += [wrapped_glyphs(rr, s).animate.set_color(HARNESS) for s in subs]
            self.play(*lit, run_time=0.4)
            assert len(t.lines) == 12

        # ========================================================== 5 · extra: a failed live run is evidence too
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(c686), caption_extra(tr, True), run_time=0.4)
            c5 = type_cmd(self, t, FAIL.cmd, 1.0)
            last5 = rows_of(c5)[0]          # the prompt's row: the command fills the row under it
            et = extra_tag()
            beside(et, t, last5)
            dt = differ_tag()
            place(dt, left=et.get_right()[0] + 0.15, cy=et.get_center()[1])
            assert dt.get_right()[0] < t.box.get_right()[0] - 0.12
            pin(self, last5, et, run_time=0.3)
            pin(self, last5, dt, run_time=0.3)
            # F7 (67 characters) wraps at its JSON comma, as wrap_output would with a hanging indent of
            # 2: the word-boundary wrap would leave its closing '…' alone on a row (read as an elision)
            o73 = show(self, t, FAIL, 2, F5, (F7A, ERR), (F7B, ERR), F10, run_time=0.5)
            r7 = [o73[2], o73[3]]
            assert len(o73) == 5 and r7[1].text.strip().endswith("Error code: 401 …"), [r.text for r in o73]
            vo.wait_until("model failed")
            # (the rows are RED already: the event name and then the 401 flash YELLOW, "look here")
            self.play(glow(substring(r7[0], "model.failed")), run_time=0.6)
            vo.wait_until("with the 401")
            self.play(glow(substring(r7[1], "Error code: 401"), grow=0.08), run_time=0.6)
            vo.wait_until("A failure is evidence too")
            # the failed run's whole trace: a YELLOW bracket in the margin (a box round these tightly
            # spaced rows drew its top edge as an underline of the run ID above)
            brk = margin_bracket([r.glyphs for r in o73])
            assert brk.get_left()[0] > t.box.get_left()[0] + 0.1, brk.get_left()
            self.play(Create(brk), run_time=0.45)
            self.play(Succession(Wait(0.8), FadeOut(brk, run_time=0.35)))

        # ========================================================== 6 · step 2: a scripted batch (offline)
        with self.voiceover(SAY[6]) as vo:
            tr = switch_section(self, tr, "Eval2", 1, run_time=0.8)
            c6 = type_cmd(self, t, EVAL_CMD, 1.6)
            assert len(rows_of(c6)) == 3, [r.text for r in rows_of(c6)]
            vo.wait_until("the act 2 evaluation")
            self.play(glow(typed_glyphs(c6, "--act 2 --evaluate core")), run_time=0.6)
            vo.wait_until("scripted")
            self.play(glow(typed_glyphs(c6, "--fixture")), run_time=0.6)
            pin_tag(self, t, c6, scripted_tag(), run_time=0.3)
            vo.wait_until("two repeats")
            self.play(glow(typed_glyphs(c6, "--repeats 2")), run_time=0.6)
            vo.wait_until("labeled context fixture 1")
            # (the flag and its value sit on two rows: each flashes about its own centre)
            self.play(glow(typed_glyphs(c6, "--label")), glow(typed_glyphs(c6, "context-fixture-1")),
                      run_time=0.6)
            o74 = show(self, t, FIX, 2, "…", (L86, HARNESS), 88, (91, 94), run_time=0.6)
            assert len(t.lines) == 12
            vo.wait_until("All 4 runs pass")
            self.play(glow(substring(o74[2], "4/4 scheduled runs passed")), run_time=0.6)
            vo.wait_until("but scripted runs")
            c694 = top_chip(R694, where="README.md · line 694", expected=True)
            # this chip runs left under the tracker's caption: centre it in the band between the
            # caption and the terminal's top (with its title-bar tag) instead of 0.03 under the caption
            lo = max(t.box.get_top()[1], ft.get_top()[1])
            c694.set_y((tr.get_bottom()[1] + lo) / 2)
            apart(c694, tr, 0.08)
            apart(c694, VGroup(t.box, ft), 0.08)
            self.play(FadeIn(c694, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 7 · read the report back; export the HTML scorecard
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(c694), tr.goto(2), run_time=0.4)
            type_cmd(self, t, REP.cmd, 0.7)
            show(self, t, REP, (L86, HARNESS), 5, run_time=0.4)
            vo.wait_until("and export the HTML scorecard")
            self.play(tr.goto(3), run_time=0.35)
            type_cmd(self, t, VIEW.cmd, 0.7)
            o76 = show(self, t, VIEW, (2, 3), wrap=True, run_time=0.4)      # line 2 is 68 characters
            vo.wait_until("to its default path")
            self.play(wrapped_glyphs(item_rows(o76, 0), P_DEFAULT).animate.set_color(LOOKUP), run_time=0.4)
            # "or one you choose": the --html-output command types through the clause, its path lights
            self.play(tr.goto(4), run_time=0.35)
            c7 = type_cmd(self, t, HTML.cmd, 0.9)
            o77 = show(self, t, HTML, 2, run_time=0.35)
            vo.wait_until("or one you choose")
            self.play(substring(o77[0], P_MINE).animate.set_color(LOOKUP), run_time=0.4)
            # make room for the page now, so the browser opens on "Open it" (the strip keeps the last
            # command and its saved path)
            fit(self, t, 3, keep=rows_of(c7) + [o77[0]], tags=list(ft), run_time=0.6)

        # ========================================================== 8 · open it from the laptop's outputs folder
        BW, BTOP, BBOT = 12.6, 2.85, -0.3
        br = browser_window(HOST_OUT + "my-report.html", width=BW, height=BTOP - BBOT)
        br.move_to([0, (BTOP + BBOT) / 2, 0])
        page = br.content
        x0 = page.get_left()[0] + 0.25
        ban_rows = VGroup(sans("SCRIPTED RESPONSES", CAPTION, INK, weight="BOLD"),
                          label(BANNER[len("SCRIPTED RESPONSES"):].lstrip(), CAPTION, INK))
        ban_rows.arrange(RIGHT, buff=0.14, aligned_edge=DOWN)     # (Text drops the leading space)
        sban = box(ban_rows.width + 0.4, ban_rows.height + 0.24, S.GREY, fill_opacity=0.1, radius=0.08)
        ban_rows.move_to(sban)
        sbanner = VGroup(sban, ban_rows)
        place(sbanner, left=x0, top=page.get_top()[1] - 0.08)
        ill8 = illustration_tag()
        place(ill8, right=page.get_right()[0] - 0.2, cy=sbanner.get_center()[1])
        th = 0.84
        tiles8 = VGroup()
        for num, lab, _ in TILES:
            n = sans(num, 24, HARNESS, weight="BOLD")
            lb = label(lab, CAPTION, INK)
            fr = box(max(2.4, lb.width + 0.5), th, HARNESS, fill_opacity=0.1, stroke=2.5, radius=0.1)
            col = VGroup(n, lb).arrange(DOWN, buff=0.05)
            col.move_to(fr)
            tiles8.add(VGroup(fr, col))
        gap = max(0.22, (page.width - 0.5 - sum(tl.width for tl in tiles8)) / 3)   # the row spans the page
        tiles8.arrange(RIGHT, buff=gap)
        place(tiles8, left=x0, top=sbanner.get_bottom()[1] - 0.15)
        trows = VGroup(*[mtext(r, CAPTION, INK) for r in ROWS]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        place(trows, left=x0 + 0.1, top=tiles8.get_bottom()[1] - 0.15)
        assert trows.get_bottom()[1] > br.frame.get_bottom()[1] + 0.08, trows.get_bottom()
        assert tiles8.get_right()[0] < br.frame.get_right()[0] - 0.1, tiles8.get_right()
        apart(sbanner, ill8, 0.15)
        # the bind mount: container /app/outputs/ -> laptop ~/AC215/agent-harness/outputs/
        RY = -1.0
        ctr_c = VGroup(label("container", CAPTION, CTR), mono("/app/outputs/", CAPTION, LOOKUP)).arrange(RIGHT, buff=0.15)
        ctr_f = box(ctr_c.width + 0.4, ctr_c.height + 0.22, CTR, fill_opacity=0.08, radius=0.1)
        ctr_c.move_to(ctr_f)
        ctr_g = VGroup(ctr_f, ctr_c)
        lap_c = VGroup(label("laptop", CAPTION, S.GREY), mono(HOST_OUT, CAPTION, LOOKUP)).arrange(RIGHT, buff=0.15)
        lap_f = box(lap_c.width + 0.4, lap_c.height + 0.22, S.GREY, fill_opacity=0.08, radius=0.1)
        lap_c.move_to(lap_f)
        lap_g = VGroup(lap_f, lap_c)
        place(ctr_g, right=SAFE - 0.05, cy=RY)
        place(lap_g, left=-SAFE + 0.05, cy=RY)
        mount = arrow(ctr_g.get_left() + LEFT * 0.05, lap_g.get_right() + RIGHT * 0.05, LOOKUP, stroke=4, buff=0.0)
        bm = note("bind mount")
        place(bm, cx=mount.get_center()[0], bottom=RY + 0.12)
        route = VGroup(ctr_g, lap_g, mount, bm)
        for m in (br, route, ill8):
            inside(m)
        apart(br, tr, 0.04)
        apart(bm, br, 0.08)
        apart(route, VGroup(br.frame), 0.1)
        assert route.get_bottom()[1] > STRIP_TOP + 0.1, route.get_bottom()
        assert mount.get_length() > 0.6, mount.get_length()
        addr = br.address
        a_out = glyph_range_text(addr, "outputs/")
        with self.voiceover(SAY[8]) as vo:
            # "Open it": the browser opens with the scorecard drawing in
            self.play(FadeIn(br), FadeIn(sbanner), FadeIn(ill8),
                      LaggedStart(*[FadeIn(tl, shift=UP * 0.08) for tl in tiles8], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(r) for r in trows], lag_ratio=0.3), run_time=0.9)
            # "from the outputs folder": the address's outputs/ turns PINK (a path under outputs/), and
            # it is the container's /app/outputs/ ... (colour only: the address glyphs have no spaces
            # between them, so a scaled flash would run into its neighbours)
            vo.wait_until("from the outputs folder")
            self.play(FadeIn(ctr_g), a_out.animate.set_color(LOOKUP), run_time=0.5)
            # ... "on your laptop": through the bind mount
            vo.wait_until("on your laptop")
            self.play(GrowArrow(mount), FadeIn(bm), FadeIn(lap_g, shift=LEFT * 0.1), run_time=0.6)
            self.wait(1.6)                              # time to read the scorecard (on top of the pad)
        pic8 = VGroup(br, sbanner, ill8, tiles8, trows, route)

        # ========================================================== 9 · two templates and an immutable label; your turn
        tc_rows = [LIST.cmd, (TPL.cmd, "paste a run ID"), card_lines(EVAL_CMD), REP.cmd, VIEW.cmd,
                   card_lines(HTML.cmd), (Prose("offline · free"), HARNESS)]
        tc = turn_card(tc_rows, width=12.4)
        for k in (2, 5):                               # the folded commands' continuation rows,
            assert len(tc.rows[k]) == 2                # indented 4 as typed (Text drops leading spaces)
            tc.rows[k][1].shift(RIGHT * 4 * cell_width(CAPTION))
        assert tc.rows[5][1].get_right()[0] < tc.frame.get_right()[0] - 0.2, tc.rows[5][1].get_right()
        place(tc, cx=0, cy=-0.35)
        inside(tc)
        apart(tc, tr, 0.05)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(pic8), tr.goto(5), run_time=0.5)
            fit(self, t, 12, tags=list(ft), run_time=0.7)
            c9 = type_cmd(self, t, COLAB.cmd, 1.0)
            pin_tag(self, t, c9, row_tag("a template"), run_time=0.3)
            vo.wait_until("it fails")
            o78 = show(self, t, COLAB, (COLAB.line(20), ERR), wrap=True, run_time=0.4)
            cap9 = note("copy colab.sqlite from your Colab run into outputs/ first")
            pin_tag(self, t, o78[-1], cap9, run_time=0.4)
            vo.wait_until("Labels are immutable")
            self.play(caption_extra(tr, True), run_time=0.4)
            c9b = type_cmd(self, t, EVAL_CMD, 1.1)
            pin_tag(self, t, c9b, extra_tag(), run_time=0.3)
            vo.wait_until("and the batch stops")
            o88 = show(self, t, AGAIN, (AGAIN.line(2), ERR), wrap=True, run_time=0.4)
            for txt in ("labels are immutable · choose a new one", "labels are immutable · use a new one"):
                cap9b = note(txt)                       # the SHOW's words if they fit beside the row
                beside(cap9b, t, o88[-1])
                if cap9b.get_right()[0] <= t.box.get_right()[0] - 0.12 and not covers_text(cap9b, o88[-1]):
                    break
            else:
                raise ValueError("the immutable-label caption does not fit beside its row")
            pin(self, o88[-1], cap9b, run_time=0.4)
            # (the error and its caption stay readable into "Pause and run"; the card comes on the steps)
            vo.wait_until("evaluation steps 1 and 2")
            self.play(FadeOut(t), FadeOut(ft), caption_extra(tr, False), run_time=0.5)
            self.play(FadeIn(tc, scale=0.97), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tc, tr)), run_time=0.8)
        self.wait(0.3)


def card_lines(cmd: str, limit: int = 66) -> str:
    """A command for the turn card (S06's idiom), folded at a space with " \\" and a 4-space indent,
    preferring a break before an option (an option keeps its value), rows joined by "\\n"."""
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


def glyph_range_text(t, sub: str) -> VGroup:
    """The glyphs of `sub` in a plain mono Text (spaces have no glyphs)."""
    s = t.text
    i = s.find(sub)
    if i < 0:
        raise ValueError(f"{sub!r} not in {s!r}")
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])
