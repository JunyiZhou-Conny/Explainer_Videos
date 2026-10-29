"""S06 · Act 2: same agent, different context (README "2 · Context", steps 1-7; the lecture's
context-engineering slides 12-18).
Lecture: 12–18.

Beats (script.md "## S06", one voiceover block each):
 0  LECTURE 12–18 (with the picture). TRACKER Context (section shown, no step lit). Slide 16
    rebuilt from Act 1's real blocks (V4 ContextStack): the BLUE "LLM" and "response" first ("what
    the model sees"); the GREY chip "the invisible layer" (slide 12) over the empty column on
    "invisible layer"; on "one model call" the GREY "user prompt" chip and the arrows into and out
    of the column, the LLM pulses; the six GREEN-outlined blocks
    write in top to bottom as the SAY names them (system prompt · prompts/shop_assistant.md +
    policies; user message · the confirmed request (JSON); structured output · AgentReply; tool
    definitions · 5 tools); blocks 5-6 as GREY dashed empty slots "retrieved data" and "memory ·
    saved preferences", each pulsing as it is named.
 1  The ends and details leave; the column becomes the compact "basic · act 1", then a copy slides
    right: "enriched". Three GREY chips across the top "same prompt", "same model", "same tools";
    the V1 mini-map bottom right (Act 1's bars), Context & memory row YELLOW. Basic: the first four
    blocks light YELLOW in turn, its slots pulse GREY (empty); enriched: the two slots fill GREEN.
    Caption (slide 18, our words) "every block your code adds is a decision"; 1 s hold.
 2  TRACKER Context 1. Picture, chips, mini-map and lecture tag leave. Container terminal (11
    rows, TEAL), title-bar tag `no key`; it types `python cli.py --act 2 --compare`, the GOLD
    `live · billed per token` joins the title bar, a GOLD row chip "2 runs" beside the command.
    TERM(container/20: 2, 4–5 wrap, 7 wrap, 8, 9 as 401). Line 7 turns YELLOW on "saved taste" and
    the GREY chip from RECORDED(expected/colab-c16-customers: 4) fades in above the terminal:
    ‹customer 2› [mild cheeses, nonalcoholic pairings] (ID and preferences only); its preferences
    pulse on "mild cheeses". Line 8 gets the GREY row tag "enriched never starts".
 3  The terminal shrinks to the 3-row strip (the command, line 8, the 401's first row). Above it,
    left: QUOTE(README.md: 851–856) "prints both answers and a side-by-side table … The verdict
    reports improvement, a tie, / or a regression; it does not assume / enriched will win." (four
    rows, `expected`); right: a GREY dashed empty table outline (`illustration`, header
    acts/act2_context.py · lines 151–168): Measure | BASIC | ENRICHED; Cart check · Mild-cheese
    match · Model calls · Input tokens (all calls); no values. The verdict rows are underlined
    YELLOW on "and a verdict" and pulse on "a tie or a regression".
 4  TRACKER Context 2, then 3. The card and table leave; the terminal grows back (11 rows); the
    top-band chip README.md · line 271 (excerpt) "Individual runs, if you want to inspect each
    tool call". It types the basic run (folds) -> TERM(container/21: 10, 12 as 401s), then the
    enriched run -> TERM(container/22: 10, 12 as 401s). "Input: 1 conversation messages." gets a
    YELLOW box and the row tag "basic" on "basic sends 1"; "Input: 2 …" a YELLOW box and "enriched"
    on "enriched sends 2", then the strip (21:10 and 22:10). On "the extra one" the two compact
    columns return above it (lecture tag back), with what each sends on the right: basic ·
    1 message [request]; enriched · 2 messages [ ┄ ] [request]; a copy of enriched's two filled
    slots' frames folds into one GREEN card's frame as it slides into the empty message spot, then
    the words "context packet" appear (no filled box over its own label) and the card pulses.
 5  TRACKER Context 4. The columns, cards and lecture tag leave; the strip's rows go with them
    and the terminal grows back empty. It types the override run -> TERM(container/23: 10, 12
    as 401s). Top-band chips one at a time: container/23 · line 7 (excerpt) "at least one with a
    funk rating of 4 or higher" on "asks for funk", then README.md · lines 277–278 (excerpt)
    "must take priority over the saved mild preference" on "today's request must win".
 6  TRACKER Context 4 · extra. Top band: README.md · line 278 "Each Act 2 command also prints a
    separate PA/NY counterexample", under it on "A small slip" the GREY tag `erratum ·
    --compare doesn't`. On "This extra call does" the chips and the GOLD live tag leave, the
    terminal grows to 13 rows and types `python -c 'from acts.act2_context import
    print_shipping_demo; print_shipping_demo()'` (extra tag; folds onto 3 rows) ->
    TERM(container/29: 3–7 wrap, while the command is still on screen): `PA: REJECTED` RED (pulses
    on "fails for Pennsylvania"), `NY: PASS` GREEN; then 8–9 (wrap, the command scrolls off to its
    last row); NY pulses on "passes for New York", line 9's "FICTIONAL classroom PA rule" row
    YELLOW on "under a fictional rule". Then the terminal shrinks to the strip (PA, NY, that row);
    above it V4's toggle (`illustration`): the fixed cart (Comté 350 g · Bûcheron 350 g · Époisses
    300 g, GREY: a given cart, not a model's) on the GREEN validator, stamp RED "PA: REJECTED".
    A silent coda after the words (~3 s): the switch flips to NY, the stamp turns GREEN "NY:
    PASS" (NY row pulses); the GREY tag "a fictional classroom rule · not a law (container/29 ·
    line 9)" (FICTIONAL row pulses); the switch flips back to PA (PA row pulses); 0.5 s hold.
 7  TRACKER Context 5 (extra off). The toggle leaves; the terminal grows back (11 rows), the GOLD
    live tag returns and the two-row card below arrives in the top band. It types `python cli.py
    --act 3 --scenario pa-shipping` (folds) ->
    TERM(container/24: 5, 6 wrap, 9 folded to "Could you help me order cheese … My starting cart
    is 350 g of Comté, 350 g of Bûcheron, and 300 g of Époisses. …" wrap, 13, 15, 16 as 401s): 13
    BLUE, 15 YELLOW (pulses at the end). The GREY card: "the README puts this act 3 command here
    (README.md · line 286)" / "a customer's own cart, checked, and the model asked to fix it ·
    part 2 explains it" (its second row pulses on "part 2 explains it"); 0.6 s hold.
 8  TRACKER Context 6, then 7. The card leaves; the terminal grows to 12 rows. It types the
    evaluation command (folds onto 3 rows), a GOLD row chip "12 runs" beside it ->
    TERM(container/25: 2, …, 36, 38): "4 cases × 3 repeats = 12 runs" boxed YELLOW with the GREY
    tag "2 cases × 2 modes × 3" under it (on the "…" row); line 38 RED with the GREY caption
    "stops after 3 errors · exit 1". It types `python cli.py --view-report act2-context-live-1` ->
    TERM(container/26: 2–3 wrap): the report path PINK, caption "the report writes anyway ·
    evaluation explains it". On "the label is used up" the GREY top-band chip "the label is now
    taken · rerun with a new --label (README.md · line 721)".
 9  The terminal and its tags leave. README.md · line 301 "See Tutorial questions and evidence",
    under it the GREY two-row tag `erratum · docs/TUTORIAL_SCENARIOS.md was never published` /
    `use the README's checkpoints`; beside them S02's GREY dashed ghost `docs/` "not in the repo"
    returns on "the docs folder"; the erratum's second row pulses on "so use the README". On
    "Pause here" the chips leave and the static GREY "your turn" card enters ("with your key:", the
    seven commands of steps 1-7, folded at a space with " \\" before an option, GOLD "about 18 live
    runs · billed per token"), ▶ your turn. Hold 2 s, then everything fades to an empty frame.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    ReplacementTransform,
    RoundedRectangle,
    TransformFromCopy,
    VGroup,
    VMobject,
    Write,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.devops import box, cell_width, chip, label, mono
from explainer.scene import VoiceScene

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ the real captures (file line numbers)
CMP = capture("container/20")
assert CMP.cmd == "python cli.py --act 2 --compare", CMP.cmd
assert CMP.line(8) == "Starting basic context with gpt-5.6-luna", CMP.line(8)
assert CMP.line(7).startswith("Two fresh live runs: basic receives no saved profile;"), CMP.line(7)
E401_CMP = CMP.as401(9)                                               # "Run stopped: (… 401 …", 2 rows

BASIC = capture("container/21")
ENR = capture("container/22")
OVR = capture("container/23")
assert BASIC.cmd == "python cli.py --act 2 --scenario personalized --context basic", BASIC.cmd
assert ENR.cmd == "python cli.py --act 2 --scenario personalized --context enriched", ENR.cmd
assert OVR.cmd == "python cli.py --act 2 --scenario preference-override --context enriched", OVR.cmd
IN1, IN2 = "Input: 1 conversation messages.", "Input: 2 conversation messages."
assert IN1 in BASIC.line(10) and IN2 in ENR.line(10) and IN2 in OVR.line(10)
FUNK = "at least one with a funk rating of 4 or higher"
assert FUNK in OVR.line(7), OVR.line(7)

SHIP = capture("container/29")
assert SHIP.cmd == "python -c 'from acts.act2_context import print_shipping_demo; print_shipping_demo()'", SHIP.cmd
assert SHIP.line(5).strip() == "PA: REJECTED" and SHIP.line(7).strip() == "NY: PASS"
assert "FICTIONAL classroom PA rule" in SHIP.line(9)

PA3 = capture("container/24")
assert PA3.cmd == "python cli.py --act 3 --scenario pa-shipping", PA3.cmd
ASK9 = PA3.fold(9, 9, "Could you help me order cheese … My starting cart is 350 g of Comté, 350 g of Bûcheron, "
                      "and 300 g of Époisses. …")
assert PA3.line(13) == "Model call 1 · Cart proposer · gpt-5.6-luna", PA3.line(13)
assert PA3.line(15).strip() == "Available tools: none (structured proposal only)", PA3.line(15)

EVAL = capture("container/25")
assert EVAL.cmd == ("python cli.py --act 2 --evaluate core --case personalized --case preference-override "
                    "--repeats 3 --label act2-context-live-1"), EVAL.cmd
RUNS12 = "4 cases × 3 repeats = 12 runs"
assert RUNS12 in EVAL.line(2) and EVAL.line(38) == "Failures: 0; errors: 3; missing: 9."
assert EVAL.exit == 1
VIEW = capture("container/26")
assert VIEW.cmd == "python cli.py --view-report act2-context-live-1", VIEW.cmd
REPORT = "/app/outputs/reports/act2-context-live-1.html"
assert REPORT in VIEW.line(2)

C16 = capture("expected/colab-c16-customers")          # the staff's saved Colab run, cell 16
PREFS = "[mild cheeses, nonalcoholic pairings]"
assert MASK2 in C16.line(4) and C16.line(4).rstrip().endswith(PREFS), C16.line(4)

# README phrases (exact sub-strings, checked) and the lines the chips name
R271 = "Individual runs, if you want to inspect each tool call"
assert R271 in source_line("README.md", 271)
R277 = "must take priority over the saved mild preference"
assert R277 in " ".join(s.strip() for s in readme(277, 278)), readme(277, 278)
R278 = "Each Act 2 command also prints a separate PA/NY counterexample"
assert R278 in source_line("README.md", 278)
assert source_line("README.md", 286) == PA3.cmd
R301 = "See Tutorial questions and evidence"
assert R301 in source_line("README.md", 301).replace("[", "").replace("]", "")
assert "docs/TUTORIAL_SCENARIOS.md" in source_line("README.md", 301)
assert "choose a new label" in source_line("README.md", 721)
QUOTE = ["prints both answers and a side-by-side table …",       # README rows 852, 854-855
         "The verdict reports improvement, a tie,",
         "or a regression; it does not assume",
         "enriched will win."]
# the table's rows: four of the measures in acts/act2_context.py (metrics list, lines 151–161)
MEASURES = ("Cart check", "Mild-cheese match", "Model calls", "Input tokens (all calls)")
_act2 = excerpt("acts/act2_context.py", 151, 168)
assert all(f'("{m}"' in _act2 for m in MEASURES)

# the "your turn" card: steps 1-7 as typed, folded at a space (" \")
CARD_CMDS = (CMP.cmd, BASIC.cmd, ENR.cmd, OVR.cmd, PA3.cmd, EVAL.cmd, VIEW.cmd)
CARD_FOLD = 66

# ------------------------------------------------------------------ layout
T_ROWS = 11                       # the walkthrough terminal (top 1.79: a two-row band above it)
STACK_Y = -0.35                   # beat 0: the full stack's centre
COLS_Y, BX, EX = 0.2, -2.9, 1.5   # beat 1: the two compact columns
SAME_X = (BX + EX) / 2            # beat 1: the three "same …" chips, centred over both columns
COL_K = 0.85                      # beat 4: the columns return small (shapes; text keeps its size)
C2Y, B2X, E2X = 0.72, -4.9, -1.5  # beat 4: their centres
REQ_X = 4.75                      # beat 4: the request cards (centre x)
ROW_A_Y = 1.55                    # beat 4: basic's message row
TOG_Y = 0.95                      # beat 6: the toggle's centre (above the strip)
BAND_RIGHT = 6.5                  # right edge of the chips in the band above an 11-row terminal
BAND_TOP = 2.86                   # their top (the tracker's bottom is 2.93)


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


def flash(mob, color: str = TURN, k: float = 1.15):
    return Indicate(mob, color=color, scale_factor=k)


def row_tag(text: str, color: str = S.GREY, text_color: str | None = None) -> VGroup:
    """A tag that fits inside one terminal row (the house tag is taller than a 22 pt row)."""
    t = label(text, CAPTION, text_color or color)
    h = 0.37
    b = RoundedRectangle(width=t.width + 0.36, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return keep_size(g)


def runs_chip(text: str) -> VGroup:
    """The GOLD "n runs" chip, row-sized (white text, GOLD border): it rides on its command's row."""
    return row_tag(text, COST, INK)


def box_at(line, sub: str, color: str = TURN):
    """A box over the first `sub` in a terminal row (a mono_line); it becomes part of the row."""
    a = line.text.find(sub)
    assert a >= 0, (sub, line.text)
    b = col_box(line, a, a + len(sub), color)
    return b


def unhide(m):
    """Give a hidden Piece part (opacity 0, its own opacities saved in _hop) its opacities back,
    so a FadeIn of it fades in to them (a slot's hidden solid frame stays hidden)."""
    for f in m.get_family():
        op = getattr(f, "_hop", None)
        if isinstance(f, VMobject) and op is not None:
            f.set_fill(opacity=op[0], family=False)
            f.set_stroke(opacity=op[1], family=False)
    return m


def filled(cs):
    """Put a compact ContextStack's two slots in their filled state at once (fill_slots' end state)."""
    for b in cs.blocks_list[4:]:
        b.dashed.set_stroke(opacity=0)
        b.solid.set_stroke(HARNESS, 2.5, opacity=1).set_fill(HARNESS, 0.3)
        b.title.set_color(INK)
    return cs


def two_row_card(rows, color: str = S.GREY, text_color: str = S.GREY, buff: float = 0.07) -> VGroup:
    """A compact GREY card of serif rows (fits the band above an 11-row terminal). .frame .rows"""
    txt = VGroup(*[label(r, CAPTION, text_color) for r in rows]).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    fr = box(txt.width + 0.4, txt.height + 0.26, color, fill=S.BG, fill_opacity=0.94, radius=0.12, stroke=2)
    txt.move_to(fr)
    g = VGroup(fr, txt)
    g.frame, g.rows = fr, txt
    return keep_size(g)


def two_row_tag(rows, color: str = S.GREY) -> VGroup:
    """A house tag with two rows of text (an erratum note too long for one row). .box .text"""
    txt = VGroup(*[label(r, CAPTION, color) for r in rows]).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    b = RoundedRectangle(width=txt.width + 0.44, height=txt.height + 0.22, corner_radius=0.2,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    txt.move_to(b)
    g = VGroup(b, txt)
    g.box, g.text = b, txt
    return keep_size(g)


def bar_y(t, rows: int) -> float:
    """The title bar's centre y of the house terminal `t` at `rows` rows (bottom edge fixed)."""
    return strip_top(rows) - t.bar_h / 2


def fit(scene, t, rows: int, keep=None, tags=(), parked=(), extra=(), run_time: float = 0.8):
    """resize(), with the title-bar tags (`tags`, on screen) and the title riding along on the bar:
    frame_tags moved the title left next to the window dots, and resize() alone would centre it
    again under the tags (so the title is lent out of t while resize() runs). `parked` tags (off
    screen) are moved at once."""
    y = bar_y(t, rows)
    for m in parked:
        m.set_y(y)
    title, t.title = t.title, None
    try:
        resize(scene, t, rows, keep=keep, run_time=run_time,
               extra=[title.animate.set_y(y), *[m.animate.set_y(y) for m in tags], *extra])
    finally:
        t.title = title


def table_outline() -> VGroup:
    """The --compare table as a GREY dashed outline with no values (four of its measures; the column
    titles as cli.py prints them). .frame .head .rows"""
    heads = [label("Measure", CAPTION, S.GREY), mono("BASIC", CAPTION, S.GREY), mono("ENRICHED", CAPTION, S.GREY)]
    names = [label(m, CAPTION, INK) for m in MEASURES]
    col_w = [max(n.width for n in names) + 0.4, 1.3, 1.75]
    row_h = 0.46
    n = len(names) + 1
    w, h = sum(col_w), n * row_h
    fr = box(w + 0.1, h + 0.1, S.GREY, dashed=True, radius=0.1, stroke=2)
    x0, y0 = -w / 2, h / 2
    lines = VGroup()
    for i in range(1, n):
        y = y0 - i * row_h
        lines.add(DashedLine([x0, y, 0], [x0 + w, y, 0], color=S.GREY_DARK, stroke_width=2, dash_length=0.08))
    for c in (1, 2):
        x = x0 + sum(col_w[:c])
        lines.add(DashedLine([x, y0, 0], [x, y0 - h, 0], color=S.GREY_DARK, stroke_width=2, dash_length=0.08))
    for c, hd in enumerate(heads):
        hd.move_to([x0 + sum(col_w[:c]) + 0.22, y0 - row_h / 2, 0], aligned_edge=LEFT)
    for r, nm in enumerate(names, start=1):
        nm.move_to([x0 + 0.22, y0 - (r + 0.5) * row_h, 0], aligned_edge=LEFT)
    g = VGroup(fr, lines, *heads, *names)
    g.frame, g.head, g.rows = fr, VGroup(*heads), VGroup(*names)
    return g


def card_lines(cmd: str, limit: int = CARD_FOLD) -> str:
    """A command for the turn card, folded at a space with " \\" and a 4-space indent (preferring a
    break before an option, so an option keeps its value), rows joined by "\\n"."""
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


class ContextModes(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0 · slide 16 from Act 1's blocks
        tr = tracker("Context")
        lr = lref("12–18")
        cs = ContextStack(show=())
        cs.move_to([0, STACK_Y, 0])
        blocks = cs.blocks_list
        inv = keep_size(chip("the invisible layer", S.GREY, size=CAPTION))
        place(inv, cx=cs.parts["blocks"].get_center()[0], bottom=cs.parts["blocks"].get_top()[1] + 0.14)
        mem = blocks[5]
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(lr), run_time=0.5)
            self.add(cs)
            cs.reveal(self, "llm", "a_out", "response", run_time=0.6)        # what the model sees: its input
            vo.wait_until("the lecture's invisible layer")
            self.play(FadeIn(inv, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Here is one model call")
            cs.reveal(self, "prompt", "a_in", "a_mid", run_time=0.6)
            self.play(flash(cs.parts["llm"], CLOUD, 1.1), run_time=0.5)
            for i, anchor in enumerate(("system prompt and shop", "the request", "the reply format", "five tools")):
                vo.wait_until(anchor)
                self.play(FadeIn(unhide(blocks[i]), shift=RIGHT * 0.15), run_time=0.45)
            vo.wait_until("and two slots")
            unhide(blocks[4])
            unhide(mem)
            mem.detail.set_opacity(1).set_color(S.GREY)          # "memory · saved preferences", empty
            self.play(LaggedStart(FadeIn(blocks[4]), FadeIn(mem), lag_ratio=0.4), run_time=0.7)
            cs._flag(cs.parts["blocks"], False)
            vo.wait_until("for retrieved data")
            self.play(flash(blocks[4].dashed, S.GREY, 1.04), run_time=0.6)
            vo.wait_until("and saved preferences")
            self.play(flash(mem.dashed, S.GREY, 1.04), run_time=0.6)

        # ========================================================== 1 · basic and enriched
        bs = ContextStack(compact=True, title="basic · act 1")
        es = ContextStack(compact=True, title="enriched")
        bs.move_to([BX, COLS_Y, 0])
        es.move_to([EX, COLS_Y, 0])
        same = VGroup(*[keep_size(chip(s, S.GREY, size=CAPTION)) for s in ("same prompt", "same model", "same tools")])
        same.arrange(RIGHT, buff=0.3).move_to([SAME_X, TOPCHIP_Y, 0])
        dec = label("every block your code adds is a decision", CAPTION, INK)
        place(dec, cx=-0.75, cy=-2.45)
        mm = BoundaryMini(upto=1)
        ends = ("prompt", "a_in", "a_mid", "llm", "a_out", "response")
        details = [b.detail for b in blocks if b.detail is not None]
        with self.voiceover(SAY[1]) as vo:
            self.play(*cs.parts_out(*ends), *[d.animate.set_opacity(0) for d in details], FadeOut(inv),
                      run_time=0.4)
            # the column becomes "basic" (the same blocks, smaller), then a copy slides right: "enriched"
            moves = []
            for i, fb in enumerate(blocks):
                src = VGroup(fb.solid, fb.title) if fb.dashed is None else VGroup(fb.solid, fb.dashed, fb.title)
                bb = bs.block(i)
                dst_b = VGroup(bb.solid, bb.title) if bb.dashed is None else VGroup(bb.solid, bb.dashed, bb.title)
                moves.append(ReplacementTransform(src, dst_b))
            self.play(*moves, FadeIn(bs.parts["title"]), run_time=0.7)
            # the transforms left the parts on the scene one by one: swap them for the piece
            self.remove(*[m for m in self.mobjects if m not in (tr, lr)])
            self.add(bs)
            self.play(TransformFromCopy(bs.parts["blocks"], es.parts["blocks"]), FadeIn(es.parts["title"]),
                      run_time=0.7)
            self.remove(*[m for m in self.mobjects if m not in (tr, lr, bs)])
            self.add(es)
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in same], lag_ratio=0.25),
                      FadeIn(mm), run_time=0.6)
            self.play(mm.light("context"), run_time=0.4)
            vo.wait_until("sends the first four")
            self.play(LaggedStart(*[bs.light(i) for i in range(4)], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("and leaves the slots")
            self.play(flash(VGroup(*[b.dashed for b in bs.blocks_list[4:]]), S.GREY, 1.04), run_time=0.6)
            vo.wait_until("enriched fills them")
            self.play(*es.fill_slots(), run_time=0.7)
            self.play(Write(dec), run_time=0.8)
        self.wait(1.0)                                         # the caption reads before the picture goes

        # ========================================================== 2 · step 1: --compare
        t = term(container=True, rows=T_ROWS)
        ft = frame_tags(t, nokey_tag(), live_tag())
        nk, lv = ft[0], ft[1]
        c16_box = VGroup(mono(MASK2, CAPTION, S.GREY), mono(PREFS, CAPTION, INK)).arrange(RIGHT, buff=0.35)
        c16_fr = box(c16_box.width + 0.48, mono("|", CAPTION).height + 0.24, S.GREY, fill=S.BG,
                     fill_opacity=0.94, radius=0.1)
        c16_fr.move_to(c16_box)
        c16_head = note("recorded · the staff's saved Colab run · cell 16 (excerpt)")
        c16 = VGroup(c16_fr, c16_box)
        c16_head.next_to(c16_fr, UP, buff=0.08).align_to(c16_fr, LEFT).shift(RIGHT * 0.08)
        c16_all = VGroup(c16, c16_head)
        place(c16_all, right=BAND_RIGHT, top=BAND_TOP)
        assert c16_all.get_bottom()[1] > t.box.get_top()[1] + 0.05
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(bs, es, same, dec, mm)), FadeOut(lr), tr.goto(1), run_time=0.5)
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(nk, shift=DOWN * 0.1), run_time=0.5)
            cmd = type_cmd(self, t, CMP.cmd, 1.2)
            self.play(FadeIn(lv, shift=DOWN * 0.1), run_time=0.4)
            pin(self, cmd, beside(runs_chip("2 runs"), t, cmd), run_time=0.4)
            vo.wait_until("uses the personalized")
            show(self, t, CMP, 2, 4, 5, wrap=True, run_time=0.6)
            vo.wait_until("where today's request")
            r7 = show(self, t, CMP, 7, wrap=True, run_time=0.4)
            vo.wait_until("the second customer's saved")
            self.play(*[r.glyphs.animate.set_color(TURN) for r in r7], FadeIn(c16_all, shift=DOWN * 0.1),
                      run_time=0.6)
            vo.wait_until("mild cheeses and")
            self.play(flash(c16_box[1], TURN, 1.08), run_time=0.8)
            vo.wait_until("The basic run starts")
            l8 = show(self, t, CMP, 8, run_time=0.4)[0]
            vo.wait_until("and stops at the 401")
            r9 = show(self, t, CMP, E401_CMP, wrap=True, run_time=0.5)
            vo.wait_until("so enriched never starts")
            pin(self, l8, beside(row_tag("enriched never starts"), t, l8), run_time=0.5)

        # ========================================================== 3 · what a key gets you
        qc = quote_card(851, 856, lines=QUOTE, wrap=47)
        tb = table_outline()
        tb_head = note("acts/act2_context.py · lines 151–168")
        tb_head.next_to(tb.frame, UP, buff=0.1).align_to(tb.frame, LEFT).shift(RIGHT * 0.1)
        tb_tag = illustration_tag()
        tb_tag.next_to(tb.frame, DOWN, buff=0.12).align_to(tb.frame, RIGHT)
        tbl = VGroup(tb, tb_head, tb_tag)
        place(qc, left=-6.45, cy=0.7)
        place(tbl, right=6.45, cy=0.7)
        assert qc.get_right()[0] < tbl.get_left()[0] - 0.2, (qc.get_right()[0], tbl.get_left()[0])
        assert len(qc.rows) == 4 and "verdict" in qc.rows[1].text, [r.text for r in qc.rows]
        verdict = qc.rows[1:]
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(c16_all), run_time=0.3)
            fit(self, t, 3, keep=[cmd, l8, r9[0]], tags=(nk, lv))
            self.play(FadeIn(qc, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a side-by-side table")
            self.play(FadeIn(tbl, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and a verdict")
            uls = VGroup(*[under(r, TURN, 3) for r in verdict])
            self.play(LaggedStart(*[Create(u) for u in uls], lag_ratio=0.3), run_time=0.7)
            vo.wait_until("a tie or a regression")
            self.play(flash(verdict, TURN, 1.04), run_time=0.7)

        # ========================================================== 4 · steps 2-3: two single runs
        c271 = top_chip(R271, where="README.md · line 271 (excerpt)", color=S.GREY)
        place(c271, right=BAND_RIGHT, top=BAND_TOP - 0.15)
        bs2 = ContextStack(compact=True, title="basic · act 1")
        es2 = filled(ContextStack(compact=True, title="enriched"))
        for c, x in ((bs2, B2X), (es2, E2X)):
            c.rescale(COL_K)
            c.move_to([x, C2Y, 0])
        slots = es2.slots()
        req_a = json_card(["request"], HARNESS).move_to([REQ_X, ROW_A_Y, 0])
        req_b = json_card(["request"], HARNESS)
        pk = json_card(["context packet"], HARNESS)
        row_b_y = slots.get_center()[1]
        req_b.move_to([REQ_X, row_b_y, 0])
        pk.move_to([req_b.get_left()[0] - 0.2 - pk.width / 2, row_b_y, 0])
        ghost = box(pk.width, pk.frame.height, S.GREY, dashed=True, radius=0.12).move_to(pk)
        lab_a = label("basic · 1 message", CAPTION, S.GREY)
        place(lab_a, right=req_a.get_right()[0], bottom=req_a.get_top()[1] + 0.12)
        lab_b = label("enriched · 2 messages", CAPTION, S.GREY)
        place(lab_b, right=req_b.get_right()[0], bottom=req_b.get_top()[1] + 0.12)
        assert pk.get_left()[0] > es2.get_right()[0] + 0.3, (pk.get_left()[0], es2.get_right()[0])
        assert lab_b.get_bottom()[1] > pk.get_top()[1] + 0.05
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(qc, tbl, uls)), run_time=0.4)
            fit(self, t, T_ROWS, tags=(nk, lv))
            self.play(tr.goto(2), FadeIn(c271, shift=DOWN * 0.1), run_time=0.5)
            type_cmd(self, t, BASIC.cmd, 1.1)
            rb = show(self, t, BASIC, 10, BASIC.as401(12, short=True), run_time=0.4)
            self.play(tr.goto(3), run_time=0.4)
            type_cmd(self, t, ENR.cmd, 1.1)
            re = show(self, t, ENR, 10, ENR.as401(12, short=True), run_time=0.4)
            in1, in2 = rb[0], re[0]
            vo.wait_until("basic sends 1")
            b1 = box_at(in1, IN1)
            self.play(Create(b1), run_time=0.4)
            in1.add(b1)
            pin(self, in1, beside(row_tag("basic"), t, in1), run_time=0.35)
            vo.wait_until("enriched sends 2")
            b2 = box_at(in2, IN2)
            self.play(Create(b2), run_time=0.4)
            in2.add(b2)
            pin(self, in2, beside(row_tag("enriched"), t, in2), run_time=0.35)
            # the strip at once (its two rows are the ones just named), so the packet folds on its words
            fit(self, t, 3, keep=[in1, in2], tags=(nk, lv), extra=[FadeOut(c271)], run_time=0.7)
            vo.wait_until("the extra one")
            lr = lref("12–18")
            self.play(FadeIn(bs2), FadeIn(es2), FadeIn(lr), FadeIn(VGroup(req_a, lab_a, req_b, lab_b)),
                      Create(ghost), run_time=0.6)
            fold = VGroup(*[b.solid.copy() for b in es2.blocks_list[4:]])
            pk_frame = VGroup(pk.frame, pk[1])                       # the frame and its tint
            self.play(ReplacementTransform(fold, pk_frame), run_time=0.9)
            self.play(FadeIn(pk.rows), FadeOut(ghost), run_time=0.4)
            self.remove(pk_frame, pk.rows)
            self.add(pk)
            self.play(flash(pk, HARNESS, 1.06), run_time=0.6)

        # ========================================================== 5 · step 4: the override run
        c7 = top_chip(FUNK, where="container/23 · line 7 (excerpt)", color=S.GREY)
        place(c7, right=BAND_RIGHT, top=BAND_TOP - 0.15)
        c277 = top_chip(R277, where="README.md · lines 277–278 (excerpt)", color=S.GREY)
        place(c277, right=BAND_RIGHT, top=BAND_TOP - 0.15)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(bs2, es2, req_a, lab_a, req_b, lab_b, pk)), FadeOut(lr), run_time=0.4)
            # the strip's two boxed rows go with the picture: no YELLOW left over from the last idea
            fit(self, t, T_ROWS, keep=[], tags=(nk, lv), extra=[tr.goto(4)], run_time=0.7)
            type_cmd(self, t, OVR.cmd, 1.0)
            show(self, t, OVR, 10, OVR.as401(12, short=True), run_time=0.4)
            vo.wait_until("asks for funk")
            self.play(FadeIn(c7, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("and today's request")
            self.play(FadeOut(c7), run_time=0.3)
            self.play(FadeIn(c277, shift=DOWN * 0.1), run_time=0.4)

        # ========================================================== 6 · the PA/NY block, as an extra
        c278 = top_chip(R278, where="README.md · line 278", color=S.GREY)
        place(c278, right=BAND_RIGHT, top=BAND_TOP + 0.03)
        err = row_tag("erratum · --compare doesn't")
        place(err, right=c278.get_right()[0], top=c278.get_bottom()[1] - 0.07)
        assert err.get_bottom()[1] > t.box.get_top()[1] + 0.03, (err.get_bottom()[1], t.box.get_top()[1])
        tg = ShipToggle()
        cart = tg.parts["cart"]
        cart.glyph.set_color(S.GREY)
        cart.glyph[0].set_fill(S.GREY, 0.3)
        for c in cart.items:
            c.box.set_stroke(S.GREY).set_fill(S.GREY, 0.16)
        tg.move_to([0, TOG_Y, 0])
        fict = grey_tag("a fictional classroom rule · not a law (container/29 · line 9)")
        place(fict, cx=0, top=tg.get_bottom()[1] - 0.25)
        tg_il = illustration_tag()
        place(tg_il, right=6.3, top=tg.get_top()[1] + 0.35)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(c277), caption_extra(tr, True), run_time=0.4)
            self.play(FadeIn(c278, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("A small slip")
            self.play(FadeIn(err, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("dash dash compare doesn't")
            self.play(flash(err.text, S.GREY, 1.08), run_time=0.6)
            vo.wait_until("This extra call does")
            self.play(FadeOut(VGroup(c278, err)), FadeOut(lv), run_time=0.35)
            fit(self, t, 13, tags=(nk,), parked=(lv,), run_time=0.6)
            sc = type_cmd(self, t, SHIP.cmd, 1.1)
            pin(self, sc, beside(extra_tag(), t, sc), run_time=0.3)
            # PA and NY first, so the command is still on screen when they are named
            rs = show(self, t, SHIP, 3, 4, (SHIP.line(5), ERR), 6, (SHIP.line(7), HARNESS), wrap=True,
                      run_time=0.6)
            pa, ny = item_rows(rs, 2)[0], item_rows(rs, 4)[0]
            vo.wait_until("fails for Pennsylvania")
            self.play(flash(pa.glyphs, ERR, 1.1), run_time=0.5)
            rs2 = show(self, t, SHIP, 8, 9, wrap=True, run_time=0.5)
            l9 = next(r for r in item_rows(rs2, 1) if "FICTIONAL" in r.text)   # the row the tag cites
            # each phrase lights its own row while the whole output is up (the command's last row too)
            vo.wait_until("passes for New York")
            self.play(flash(ny.glyphs, HARNESS, 1.1), run_time=0.5)
            vo.wait_until("under a fictional rule")
            self.play(flash(l9.glyphs, TURN, 1.04), run_time=0.6)
            # V4's toggle: the strip keeps the three rows it restates
            fit(self, t, 3, keep=[pa, ny, l9], tags=(nk,), parked=(lv,), run_time=0.7)
            self.play(FadeIn(tg, shift=UP * 0.1), FadeIn(tg_il), run_time=0.45)
        # a short silent coda: the same cart flips PA -> NY -> PA, the strip's rows answering
        self.wait(0.3)                                         # the PA state reads before it flips
        self.play(*tg.flip(), flash(ny.glyphs, HARNESS, 1.1), run_time=0.8)
        self.play(FadeIn(fict, shift=UP * 0.1), flash(l9.glyphs, TURN, 1.04), run_time=0.6)
        self.play(*tg.flip(), flash(pa.glyphs, ERR, 1.1), run_time=0.8)
        self.wait(0.5)

        # ========================================================== 7 · step 5: the act 3 command
        a3 = two_row_card(["the README puts this act 3 command here (README.md · line 286)",
                           "a customer's own cart, checked, and the model asked to fix it · part 2 explains it"])
        place(a3, right=BAND_RIGHT, top=BAND_TOP)
        assert a3.get_bottom()[1] > strip_top(T_ROWS) + 0.03, a3.get_bottom()[1]
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(tg, tg_il, fict)), tr.goto(5), run_time=0.4)
            fit(self, t, T_ROWS, tags=(nk,), parked=(lv,), extra=[FadeIn(lv), FadeIn(a3, shift=DOWN * 0.1)],
                run_time=0.6)
            type_cmd(self, t, PA3.cmd, 0.9)
            r24 = show(self, t, PA3, 5, 6, ASK9, 13, (PA3.line(15), TURN), PA3.as401(16, short=True), wrap=True,
                       run_time=0.7)
            vo.wait_until("part 2 explains it")
            self.play(flash(a3.rows[1], S.GREY, 1.05), run_time=0.6)
            self.play(flash(item_rows(r24, 4)[0].glyphs, TURN, 1.06), run_time=0.6)
        self.wait(0.6)                                         # the card and the output read before they go

        # ========================================================== 8 · steps 6-7: twelve live runs, a report
        lab_chip = top_chip("the label is now taken · rerun with a new --label (README.md · line 721)", color=S.GREY)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(a3), tr.goto(6), run_time=0.4)
            fit(self, t, 12, tags=(nk, lv), run_time=0.5)
            ec = type_cmd(self, t, EVAL.cmd, 1.6)
            pin(self, ec, beside(runs_chip("12 runs"), t, ec), run_time=0.4)
            vo.wait_until("12 live runs")
            r2 = show(self, t, EVAL, 2, "…", run_time=0.5)
            bx = box_at(r2[0], RUNS12)
            self.play(Create(bx), run_time=0.4)
            r2[0].add(bx)
            mult = row_tag("2 cases × 2 modes × 3")
            place(mult, cx=bx.get_center()[0], cy=r2[1].strut.get_center()[1])
            pin(self, r2[1], mult, run_time=0.4)
            vo.wait_until("Without a key")
            r38 = show(self, t, EVAL, 36, (EVAL.line(38), ERR), run_time=0.5)
            stops = row_tag("stops after 3 errors · exit 1")
            pin(self, r38[1], beside(stops, t, r38[1]), run_time=0.4)
            vo.wait_until("but the report still writes")
            self.play(tr.goto(7), run_time=0.4)
            type_cmd(self, t, VIEW.cmd, 0.9)
            rv = show(self, t, VIEW, 2, 3, wrap=True, run_time=0.5)
            path = wrapped_glyphs(item_rows(rv, 0), REPORT)
            self.play(path.animate.set_color(LOOKUP), run_time=0.4)
            last = item_rows(rv, 1)[-1]
            pin(self, last, beside(row_tag("the report writes anyway · evaluation explains it"), t, last),
                run_time=0.4)
            vo.wait_until("and the label is used up")
            self.play(FadeIn(lab_chip, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 9 · a missing page; your turn
        c301 = readme_chip("README.md · line 301", R301)
        e301 = two_row_tag(["erratum · docs/TUTORIAL_SCENARIOS.md was never published",
                            "use the README's checkpoints"])
        ghost_d = ghost_file("docs/")
        gnote = note("not in the repo")
        gg = VGroup(ghost_d, gnote).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        grp = VGroup(c301, e301).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        place(grp, left=-5.6, cy=0.35)
        place(gg, left=grp.get_right()[0] + 0.7, cy=c301.get_center()[1] - 0.1)
        assert gg.get_right()[0] < 6.4, gg.get_right()[0]
        rows = [Prose("with your key:")] + [card_lines(c) for c in CARD_CMDS] + \
               [(Prose("about 18 live runs · billed per token"), COST)]
        tc = turn_card(rows)
        cw = cell_width(CAPTION)
        widest = max(r.get_right()[0] for item in tc.rows for r in (item if isinstance(item, VGroup) else [item]))
        for item, src in zip(tc.rows, rows):
            if isinstance(src, str) and "\n" in src:
                for r in item[1:]:
                    r.shift(RIGHT * 4 * cw)                       # Text drops leading spaces: put them back
        assert max(r.get_right()[0] for item in tc.rows for r in (item if isinstance(item, VGroup) else [item])) \
            <= widest + 1e-6
        place(tc, cx=0, top=2.62)
        assert tc.get_bottom()[1] > -3.55 and tc.width < 12.9, (tc.get_bottom()[1], tc.width)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(t, nk, lv, lab_chip)), run_time=0.5)
            self.play(FadeIn(c301, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(e301, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("the docs folder")
            self.play(FadeIn(gg, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("so use the README")
            self.play(flash(e301.text[1], S.GREY, 1.08), run_time=0.6)
            vo.wait_until("Pause here")
            self.play(FadeOut(VGroup(c301, e301, gg)), run_time=0.4)
            self.play(FadeIn(tc, scale=0.97), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(VGroup(tc, tr)), run_time=0.8)
        self.wait(0.3)
