"""S05 · Act 1: wrap it in a harness (README "1 · Agent and tools" steps 3-4). Lecture: 20–24.

Beats (script.md "## S05", one voiceover block each):
 0  LECTURE 20–24. A GREY dashed card (tag "illustration · our drawing") holds one line,
    `while True: model(); dispatch()`, inside a looping track with arrowheads; `model()` and
    `dispatch()` light as named and the BLUE agent core `build_agent` appears under the card. The
    GREY chip (slide 24, our words) "who does harness engineering? / anyone who wrote this loop"
    slides in beside it; at "has no stop" a dot runs round the track twice and the RED tag
    "no stop" lands under it.
 1  TRACKER Agent 3. The card leaves; the core slides to the bottom edge. CODE(README.md: 209,
    215–224) (folded; the gap row reads "… 4 more imports (lines 210–213)"); GREY chip "notebook
    cell: Colab or your own Jupyter" in the top band; `Harness(build_agent)` and the core light
    together; lines 217–220 get YELLOW bars one by one as the SAY names Trace, Budget, Context and
    Cart Check. At "The CLI builds exactly this" the panel is swapped (old out, then new in) for
    CODE(acts/act1_agent.py: 26–33), whose lines 29–32 get the same bars.
 2  V3 (tag illustration). The panel stays a moment, then everything but lines 29–32 fades; each
    of those four lines is swapped in place (old out, new in) for its ring's label (`Trace()`,
    `Budget(8, 20, 120 s)`, `Context("basic")`, `CartCheck()`), and the four labels slide left into
    a column while the core rises to the centre. The padlocked GREEN inner ring "admission · tool
    audit · shop rules" appears around the core (padlock pulses at "never comes off"). Then each
    label lifts straight up its column (over no text: the rows above it have left) and slides
    right into its ring's band as that ring slides on, inside out.
 3  The rings shrink left (texts out, shapes shrink, "agent" in). Along the bottom CODE(formaggio/
    agents/execution.py: 66, 69–70, 73–76) (folded, 20 pt); right of the rings a GREEN turnstile
    with a counter (tag illustration); the Budget ring glows, its README caption a quote card
    `README.md · line 230 (excerpt)`: "`Budget(...)` / Exact model/tool admission limits / and a
    run timeout". Eight BLUE "call" tokens pass, the counter ticks 1/8 … 8/8 and line 76's GREEN
    bar flashes on each tick; a ninth token: lines 73–74 RED, the turnstile locks RED and the RED
    label `Maximum of 8 model calls reached.` appears; a GREEN "tool" token bounces off the lock:
    lines 69–70 RED (the bar stops after the code) with the caption "the failure sticks" beside it.
    (Neighbouring line bars are drawn on one row grid, row_bar(): no bright seam between them.)
 4  The Budget ring lifts off; the turnstile, tokens, card and label leave; a GREY dashed fence
    draws round the rings, labelled "SDK fallback · 40 iterations · no call limits · no overall
    time budget", while the panel is swapped for CODE(execution.py: 56–58) (lines 57–58 joined
    and wrapped); the three values light as named. At the end the Budget ring slides back on,
    the fence and the panel leave.
 5  LECTURE 21. The CartCheck ring glows; excerpt chip `README.md · line 232 (excerpt)`
    "Independent assessment of the final proposal"; slide 21's strip at the bottom with "Verify"
    lit GREEN (the slide-21 tag arrives with it). "Back to the hook": answer card B (`… within
    your 1,5000¢ budget. …`, RED ring) at left, the GREEN check box RECORDED(c23: 63–68) at right
    (tag recorded); GREEN arrows point at the three item lines; a GREY dashed arrow to card B,
    "not read"; the garbled number pulses RED while "Cart satisfies the shop rules." flashes
    GREEN. "It reports, and never repairs":
    the strip leaves, then the four statuses of README.md · line 236 and the tag "reports · never
    repairs" (three groups on screen).
 6  LECTURE 22. V1 builds full screen: the rest leaves; card B and the check box lose their text
    and stretch into the BLUE and GREEN columns, the headers "the model proposes" / "the harness
    decides" write in, the PINK "who decides?" arrow; each column splits into five cells; the
    five GREY concern pills arrive at "five concerns", the BLUE texts at "the model's part", the
    GREEN cells pulse at "the harness's".
 7  Act 1 fills three GREEN cells (Control flow "Budget · admission", Tools "@tool schemas ·
    counted, audited calls", Verification "CartCheck"), each row lit YELLOW as it fills; then Move
    LEFT (BLUE) and Move RIGHT (GREEN); the GREEN arrow pulses at "Move right".
 8  The table and the lecture tag leave. Two onions (tag illustration, top right): `harness`
    (four rings) and `lite = harness.without("trace")` (three); a YELLOW "?" on lite's inner
    ring, another on the original's Trace ring, as asked. PONDER (8 s).
 9  The card leaves. "Yes, and yes": lite's inner ring glows GREEN, excerpt chip `README.md · line
    229 (excerpt)` "call counts and required tool admission/audit records remain". Then
    CODE(formaggio/agents/harness.py: 62–68) (20 pt) along the bottom, under the onions, with
    lines 63 and 68 lit; the original's Trace ring glows, GREEN tag "unchanged" after its name;
    lite gets the GREY caption "a separate configuration" after its name; quote card `README.md ·
    line 234 (excerpt)` "`.add(...)` also returns a new configuration."
10  TRACKER Agent 4. Container terminal (12 rows, TEAL), title-bar tags `no key` and GOLD `live ·
    billed per token`: `python cli.py --act 1 --scenario missing-details` -> container/12 lines
    4, 6 cut after "everyone's allergies." (wrapped), 8–10 (wrapped), 11 as the short 401. The two
    "I still need to …" sentences turn YELLOW; top-band chips, one after the other: QUOTE(README.md:
    248) "Look for clarification instead of invented details" (tag expected), then README.md · line
    252 (excerpt) "why calling preview_order does not authorize or place an order". At "Pause"
    the terminal leaves and the static GREY your-turn card holds 2 s; then an empty frame.

Every output line comes from capture("container/12") / capture("expected/colab-c23-agent-harness")
(exact sub-strings, checked below); README words from source_line("README.md", n).
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    DashedLine,
    Dot,
    DoubleArrow,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    Rectangle,
    RoundedRectangle,
    Succession,
    Transform,
    Triangle,
    VGroup,
    Write,
    linear,
    rush_into,
    there_and_back,
)

from common import *  # noqa: F401,F403
from common import _Reveal, _in_late, _out_early, _save_op, _set_op
from explainer.components import ponder_card
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real sources
C12 = capture("container/12")                              # python cli.py --act 1 --scenario missing-details
assert C12.cmd == "python cli.py --act 1 --scenario missing-details", C12.cmd
ASK_CUT = "everyone's allergies."
ASK_LIT = "I still need to confirm the destination. I still need to check everyone's allergies."
assert ASK_LIT in C12.line(6), C12.line(6)
REC = capture("expected/colab-c23-agent-harness")         # the staff's saved run of cell 23
B_ROW = "… within your 1,5000¢ budget. …"
assert "within your 1,5000¢ budget." in REC.line(61), REC.line(61)
L63 = REC.line(63)
_cut = L63.index(" (no automatic")
CHECK_ROWS = ([(L63[:_cut], REC.color(63)), ("  " + L63[_cut + 1:], REC.color(63))] + REC.out((64, 68)))
assert CHECK_ROWS[0][0] == "Independent cart check" and CHECK_ROWS[2][0] == "  1200 g; cheese subtotal $64.00"
assert [r[0].strip() for r in CHECK_ROWS[3:6]] == ["bucheron: 400 g", "epoisses: 400 g", "mimolette: 400 g"]
assert CHECK_ROWS[6] == ("  Cart satisfies the shop rules.", HARNESS), CHECK_ROWS[6]

# README words (exact sub-strings of the README lines)
R230 = source_line("README.md", 230)
assert "`Budget(...)`" in R230 and "Exact model/tool admission limits and a run timeout" in R230
R232 = "Independent assessment of the final proposal"
R229 = "call counts and required tool admission/audit records remain"
R234 = "`.add(...)` also returns a new configuration."
assert R234 in source_line("README.md", 234)
R236 = source_line("README.md", 236)
STATUSES = ("passed", "failed", "no_cart", "not_run")
assert "`passed`, `failed`, `no_cart`, or `not_run`" in R236 and "never repairs it" in R236
R248 = "Look for clarification instead of invented details"
assert R248 in source_line("README.md", 248)
R252 = "why calling preview_order does not authorize or place an order"
assert R252 in source_line("README.md", 252).replace("`", "")
assert source_line("README.md", 216).strip() == "Harness(build_agent)"
MORE = "4 more imports (lines 210–213)"
assert all(source_line("README.md", n).startswith("from ") for n in range(210, 214))

# act1_agent.py lines 29-32 -> the ring labels (their constructor spans)
SPANS = {29: ("trace", "Trace()"), 30: ("budget", "Budget(model_calls=8, tool_calls=20, seconds=120)"),
         31: ("context", "Context(mode)"), 32: ("cartcheck", "CartCheck()")}
RINGS4 = ("trace", "budget", "context", "cartcheck")
LOOP_TXT = "while True: model(); dispatch()"
MSG8 = "Maximum of 8 model calls reached."
PONDER = ("lite = harness.without(\"trace\")\nlite.run(...): is a tool call still counted and audited?\n"
          "Does harness itself still trace?")

# ------------------------------------------------------------------ layout
SAFE_X = 6.5
Y_C = -0.35                     # beat 2: the full rings' centre (top 2.4, bottom -3.1)
CORE_Y0, CORE_Y1 = -1.75, -2.95  # beat 0 / beat 1: the core under the card / under the README panel
PANEL_TOP = 2.78                # beat 1: README / act1 panels' top (header) under the tracker
STACK_X = -6.4                  # beat 2: the column the four labels wait in (left edges)
CR_POS = np.array([-4.4, 1.5, 0])  # beats 3-5: the compact rings (fence fits: x -6.4..-2.4, y 0.15..2.85)
HUB = np.array([-0.62, 1.72, 0])   # beat 3: the turnstile's hub (tokens pass at this height)
ONION_A, ONION_B = np.array([-4.85, 1.16, 0]), np.array([0.7, 1.16, 0])   # beats 8-9: harness and lite


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


def flash(mob, color: str = TURN, k: float = 1.15):
    return Indicate(mob, color=color, scale_factor=k)


def pulse(m, color: str = TURN, k: float = 1.06, run_time: float = 0.7, width: float | None = None):
    a = m.animate(rate_func=there_and_back, run_time=run_time).scale(k)
    return a.set_stroke(color, width) if width else a.set_stroke(color)


def hide(m, attr: str = "_x"):
    """m at opacity 0 (its opacities saved under attr) for a later _Reveal(m, attr=attr)."""
    _save_op(m, attr)
    _set_op(m, 0, attr)
    return m


def shown_copy(m):
    """A copy of a hidden Piece part at its saved (shown) opacities."""
    c = m.copy()
    _set_op(c)
    return c


def bar_flash(bar, k: float = 0.55, run_time: float = 0.3):
    return bar.animate(rate_func=there_and_back, run_time=run_time).set_fill(opacity=k)


def track_tip(point, direction) -> VGroup:
    """A small GREY arrowhead on the loop's track, pointing along `direction` (RIGHT / LEFT)."""
    t = Triangle(stroke_width=0).set_fill(S.GREY, 1).scale(0.11)
    t.rotate(-PI / 2 if direction[0] > 0 else PI / 2)
    return t.move_to(point)


def two_row_chip(top: str, bottom: str, color: str = S.GREY) -> VGroup:
    """A GREY chip with a GREY question row and a white answer row (slide 24, our words)."""
    a = label(top, 22, S.GREY)
    b = label(bottom, 22, INK)
    rows = VGroup(a, b).arrange(DOWN, buff=0.14)
    fr = box(rows.width + 0.6, rows.height + 0.4, color, fill_opacity=0.08, radius=0.18).move_to(rows)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


def pointer(frame, parts, x_left: float, color: str = TURN) -> VGroup:
    """A YELLOW leader from the right edge of a ring frame to a short label whose left edge is at
    x_left, right of the onion ("`Trace()` ?"): .leader .text. Placed, not added."""
    t = VGroup(*[mono(p[1:-1], CAPTION, c) if p.startswith("`") else label(p, 22, c) for p, c in parts])
    t.arrange(RIGHT, buff=0.14)
    a = frame.get_right() + RIGHT * 0.03
    t.move_to(a)
    t.shift(RIGHT * (x_left - t.get_left()[0]))
    ln = Line(a, t.get_left() + LEFT * 0.12, color=color, stroke_width=3)
    g = VGroup(ln, t)
    g.leader, g.text = ln, t
    return g


def code_row(panel, n: int):
    """The (first) code row of file line n in a src_panel."""
    return panel.code.code_lines[panel.rows_of(n)[0]]


def row_bar(panel, first: int, last: int | None = None, color: str = TURN, opacity: float = 0.2,
            right: float | None = None) -> Rectangle:
    """One translucent bar over file lines first..last of a src_panel, on a uniform row grid, so
    bars of neighbouring lines abut without the brighter seam two overlapping .bar()s leave.
    right: the bar's right edge (default: the panel's, as .bar())."""
    bg = panel.code.background
    pts = [(i, r.get_center()[1]) for i, r in enumerate(panel.code.code_lines) if r.width > 0.05]
    (i0, ya), (i1, yb) = pts[0], pts[-1]                          # (empty rows have no centre)
    pitch = (ya - yb) / (i1 - i0)
    y0 = sum(y + i * pitch for i, y in pts) / len(pts)            # row 0's centre on the grid
    ks = [k for n in range(first, (last or first) + 1) for k in panel.rows_of(n)]
    top = y0 - min(ks) * pitch + pitch / 2
    bot = y0 - max(ks) * pitch - pitch / 2
    x0 = bg.get_left()[0] + 0.06
    x1 = bg.get_right()[0] - 0.06 if right is None else right
    r = Rectangle(width=x1 - x0, height=top - bot, stroke_width=0).set_fill(color, opacity)
    return r.move_to([(x0 + x1) / 2, (top + bot) / 2, 0])


def answer_b() -> VGroup:
    """S01's answer card B, cut to the phrase the hook circled: BLUE frame, header "answer B", one
    mono row; a RED ring round the garbled "1,5000¢" (still on it from the hook)."""
    row = mono_line(B_ROW, CAPTION, INK)
    grey_masks(row)
    fr = box(row.glyphs.width + 0.6, row.glyphs.height + 0.5, CLOUD, fill=S.BG, fill_opacity=1.0, stroke=3,
             radius=0.12)
    row.shift(fr.get_center() - row.glyphs.get_center())
    hd = sans("answer B", 22, CLOUD, weight="BOLD").next_to(fr, UP, buff=0.1).align_to(fr, LEFT).shift(RIGHT * 0.1)
    bad = substring(row, "1,5000¢")
    bad.set_color(ERR)
    rr = ring(bad, ERR, buff=0.07, stroke=4)
    g = VGroup(fr, row, hd, rr)
    g.frame, g.row, g.header, g.ring, g.bad = fr, row, hd, rr, bad
    return g


def check_box() -> VGroup:
    """RECORDED(c23: 63–68) as S01's GREEN-bordered output box (line 63 folded at a space)."""
    chk = output_box(CHECK_ROWS)
    chk.frame.set_stroke(HARNESS, 3)
    return chk


class HarnessLayers(VoiceScene):
    def play(self, *anims, **kw):
        """Scene.play, then drop the wrapper groups an animation left on the scene (a LaggedStart's
        group, a substring's glyph group): their members are drawn by their owners, and a wrapper
        left behind would keep them on screen after their owner leaves (as in S01)."""
        super().play(*anims, **kw)
        self._prune()

    def _prune(self):
        for m in list(self.mobjects):
            others = set()
            for o in self.mobjects:
                if o is not m:
                    others.update(o.get_family())
            fam = [f for f in m.get_family() if f is not m and not f.submobjects]   # its drawn leaves
            if fam and all(f in others for f in fam):
                self.remove(m)

    def drop(self, *pieces):
        """Take pieces off the scene for good, with every top-level mobject holding any of their
        members (an animation can leave a piece split into its parts, or wrapped in a group)."""
        fam = set()
        for p in pieces:
            fam.update(p.get_family())
        for m in list(self.mobjects):
            if any(f in fam for f in m.get_family()):
                self.remove(m)

    def construct(self):
        assert len(SAY) == 11, len(SAY)

        # ========================================================== 0 · the bare loop has no stop
        lr = lref("20–24")
        loop_t = mono(LOOP_TXT, 22, INK)
        th = loop_t.height + 0.75
        track = RoundedRectangle(width=loop_t.width + 0.8, height=th, corner_radius=th / 2,
                                 stroke_color=S.GREY, stroke_width=3).move_to(loop_t)
        tips = VGroup(track_tip(track.get_top(), RIGHT), track_tip(track.get_bottom(), LEFT))
        card0 = box(track.width + 0.7, track.height + 0.7, S.GREY, dashed=True, stroke=2.5).move_to(loop_t)
        loop_g = VGroup(card0, track, tips, loop_t)
        place(loop_g, left=-6.4, cy=1.15)
        ill0 = illustration_tag("our drawing")
        place(ill0, left=card0.get_left()[0] + 0.1, top=card0.get_bottom()[1] - 0.15)
        nostop = tag("no stop", ERR)
        place(nostop, right=card0.get_right()[0] - 0.1, top=card0.get_bottom()[1] - 0.15)
        who = two_row_chip("who does harness engineering?", "anyone who wrote this loop")
        place(who, right=SAFE_X - 0.05, cy=card0.get_center()[1])
        apart(card0, who, 0.2)
        t_model = substring_text(loop_t, "model()")
        t_disp = substring_text(loop_t, "dispatch()")
        dot = Dot(radius=0.08, color=INK).move_to(track.get_top())
        lap = track.copy().set_stroke(opacity=0)
        hr = HarnessRings(show=())                    # V3, every part hidden; the core joins in beat 2
        hr.move_to([0, Y_C, 0])
        core = hr.parts["core"].copy()
        _set_op(core)                                  # (the copy carries the hidden opacities)
        core.move_to([0, CORE_Y0, 0])
        apart(core, ill0, 0.15)
        inside_frame(loop_g, ill0, nostop, who, core, lr)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(lr, shift=DOWN * 0.1), Create(card0), FadeIn(ill0), run_time=0.7)
            vo.wait_until("if you've written a loop")
            self.play(Write(loop_t), Create(track), run_time=1.0)
            self.play(FadeIn(tips, scale=0.5), run_time=0.3)
            vo.wait_until("that calls a model")
            self.play(t_model.animate.set_color(CLOUD), FadeIn(core, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("and runs its tool calls")
            self.play(t_disp.animate.set_color(HARNESS), run_time=0.3)
            self.play(flash(t_disp, HARNESS, 1.1), run_time=0.6)
            vo.wait_until("you're a harness engineer")
            self.play(FadeIn(who, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("And a bare loop has no stop")
            dot.move_to(lap.point_from_proportion(0))
            self.play(FadeIn(dot, scale=0.5), run_time=0.15)
            self.play(MoveAlongPath(dot, lap), rate_func=linear, run_time=0.9)
            self.play(MoveAlongPath(dot, lap), FadeIn(nostop, shift=UP * 0.1), rate_func=linear, run_time=0.9)

        # ========================================================== 1 · step 3: the notebook cell; the CLI builds it
        tr = tracker("Agent", 3)
        rp = src_panel("README.md", [209, (215, 224)])
        place(rp, cx=0, top=PANEL_TOP)
        gap_row = rp.code.code_lines[1]
        more = note(MORE).next_to(gap_row, RIGHT, buff=0.25)
        more.set_y(gap_row.get_center()[1])
        rp.add(more)
        nb = two_row_chip("notebook cell:", "Colab or your own Jupyter")
        bars_r = {n: row_bar(rp, n) for n in (217, 218, 219, 220)}
        hb = rp.span(216, "build_agent")
        ap = src_panel("acts/act1_agent.py", 26, 33, wrap=True)
        place(ap, cx=0, top=PANEL_TOP)
        bars_a = {n: row_bar(ap, n) for n in (29, 30, 31, 32)}
        core_b1 = core.copy().move_to([0, CORE_Y1, 0])
        place(nb, left=core_b1.get_right()[0] + 0.45, cy=CORE_Y1)
        apart(rp, core_b1, 0.12)
        apart(rp, nb, 0.08)
        inside_frame(rp, ap, nb, core_b1)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(card0, track, tips, loop_t, ill0, nostop, who, dot)),
                      core.animate.move_to(core_b1), FadeIn(tr, shift=DOWN * 0.2), run_time=0.7)
            self.play(FadeIn(rp, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("for Colab or Jupyter")
            self.play(FadeIn(nb, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("that wraps build agent")
            self.play(hb.animate.set_color(CLOUD), run_time=0.3)
            self.play(flash(hb, CLOUD, 1.15), pulse(core[0], CLOUD, 1.04, run_time=0.8, width=6), run_time=0.8)
            for n, a in zip((217, 218, 219, 220), ("It adds Trace", "Budget with 8 model calls",
                                                   "basic Context", "and Cart Check")):
                vo.wait_until(a)
                self.play(FadeIn(bars_r[n]), run_time=0.4)
            vo.wait_until("The CLI builds exactly this")
            self.play(FadeOut(VGroup(rp, *bars_r.values(), nb), shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(ap, shift=UP * 0.1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(bars_a[n]) for n in (29, 30, 31, 32)], lag_ratio=0.2), run_time=0.7)

        # ========================================================== 2 · V3: the inner ring, four layers slide on
        # the four lines -> the ring labels, swapped in place (old out, then new in), then a column
        rows = {n: code_row(ap, ln) for ln, (n, _) in SPANS.items()}
        home = {n: hr.label_of(n).get_center().copy() for n in RINGS4}
        start = {}
        for ln, (n, sub) in SPANS.items():
            lab = hr.label_of(n)
            x0 = ap.span(ln, sub).get_left()[0]
            lab.move_to([x0 + lab.width / 2, rows[n].get_center()[1], 0])
            start[n] = lab.get_center().copy()
        col = {n: np.array([STACK_X + hr.label_of(n).width / 2, start[n][1], 0]) for n in RINGS4}
        later = {"trace": "budget", "budget": "context", "context": "cartcheck"}
        for n, nxt in later.items():   # a waiting label never touches the ring that slides on before it
            lab_w = hr.label_of(nxt).width
            assert STACK_X + lab_w < hr.frames[n].get_left()[0] - 0.08, (n, nxt)
        ill2 = illustration_tag()
        place(ill2, right=SAFE_X, bottom=-3.45)
        apart(ill2, hr.frames["cartcheck"], 0.1)
        core_dst = hr.parts["core"].get_center()

        with self.voiceover(SAY[2]) as vo:
            for ln in SPANS:
                ap.code.code_lines.remove(rows[SPANS[ln][0]])
            self.add(*rows.values())
            self.add(hr)
            # (brisk: the inner ring must land while "never comes off" is still being said)
            self.play(FadeOut(VGroup(ap, *bars_a.values())), run_time=0.35)
            self.play(*[FadeOut(rows[n], rate_func=_out_early) for n in RINGS4],
                      *[_Reveal(hr.label_of(n), rate_func=_in_late) for n in RINGS4], run_time=0.6)
            self.play(*[hr.label_of(n).animate.move_to(col[n]) for n in RINGS4],
                      core.animate.move_to(core_dst), run_time=0.6)
            _set_op(hr.parts["core"])                  # the piece's own core takes the copy's place
            hr._flag(hr.parts["core"], False)
            self.remove(core)
            self.play(*hr.parts_in("inner"), FadeIn(ill2), run_time=0.45)
            vo.wait_until("never comes off")
            self.play(flash(hr.parts["inner"].lock, HARNESS, 1.6), run_time=0.5)
            vo.wait_until("call admission")
            self.play(flash(hr.label_of("inner"), HARNESS, 1.08), run_time=0.8)
            vo.wait_until("Four harness layers slide on")
            moves = []
            for n in RINGS4:
                lab = hr.label_of(n)
                up = np.array([col[n][0], home[n][1], 0])
                rise = lab.animate(run_time=0.4).move_to(up).build()      # built one at a time: a
                slide = lab.animate(run_time=0.45).move_to(home[n]).build()  # builder shares .target
                moves.append(Succession(rise, AnimationGroup(slide, _Reveal(hr.frames[n], shift=DOWN * 0.35,
                                                                            run_time=0.45))))
            self.play(LaggedStart(*moves, lag_ratio=0.75), run_time=2.9)
            for n in RINGS4:
                hr._flag(hr.parts[n], False)

        # ========================================================== 3 · Budget is a turnstile
        cr = HarnessRings(mode="compact").move_to(CR_POS)
        cr_texts = [cr.parts["core"][1], cr.parts["inner"].lock]
        for m in cr_texts:
            hide(m)
        ep = src_panel("formaggio/agents/execution.py", [66, (69, 70), (73, 76)], size=20)
        place(ep, cx=0, bottom=-3.5)
        apart(cr, ep, 0.08)
        ts = Turnstile()
        ts.shift(HUB - ts.hub.get_center())
        ill3 = illustration_tag()
        place(ill3, cx=ts.counter.get_center()[0], bottom=ts.counter.get_top()[1] + 0.12)
        apart(ill3, tr, 0.1)
        apart(ill3, lr, 0.1)
        q230 = quote_card(230, lines=["`Budget(...)`", "Exact model/tool admission limits", "and a run timeout"],
                          header="README.md · line 230 (excerpt)", expected=False)
        place(q230, right=SAFE_X, top=2.9)
        msg = mono(MSG8, CAPTION, ERR)
        place(msg, left=ts.base.get_right()[0] + 0.3, bottom=ep.get_top()[1] + 0.14)
        apart(msg, q230, 0.1)
        apart(ts, ep, 0.08)
        b76 = row_bar(ep, 76, color=HARNESS, opacity=0.16)
        b7374 = row_bar(ep, 73, 74, color=ERR)                   # one bar: no seam between the rows
        # lines 69-70: the bar stops after line 70's text, and the caption sits on the panel beside
        # it (GREY on a RED bar was hard to read)
        x_end = code_row(ep, 70).get_right()[0] + 0.3
        b6970 = row_bar(ep, 69, 70, color=ERR, right=x_end)
        sticks = note("the failure sticks")
        place(sticks, left=x_end + 0.4, cy=b6970.get_center()[1])
        assert sticks.get_right()[0] < ep.code.background.get_right()[0] - 0.2
        tok_probe = ts.token()
        assert tok_probe.get_left()[0] > cr.frames["cartcheck"].get_right()[0] + 0.1
        apart(ts.token(), q230, 0.1)
        inside_frame(cr, ep, ts, ill3, q230, msg)

        with self.voiceover(SAY[3]) as vo:
            # the rings shrink left: their texts leave first, then the shapes shrink
            texts = [hr.labels[n] for n in RINGS4] + [hr.labels["inner"], hr.parts["inner"].lock,
                                                       hr.parts["core"][1]]
            self.play(*[m.animate.set_opacity(0) for m in texts], FadeOut(ill2), run_time=0.3)
            self.play(*[Transform(hr.frames[n], cr.frames[n]) for n in ("inner",) + RINGS4],
                      Transform(hr.core, cr.core), run_time=0.7)
            self.drop(hr)
            self.add(cr)
            self.play(*[_Reveal(m, attr="_x") for m in cr_texts], FadeIn(ep, shift=UP * 0.15),
                      FadeIn(ts), FadeIn(ill3), run_time=0.5)
            self.play(cr.glow("budget"), FadeIn(q230, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("Each model call")
            self.play(FadeIn(b76), run_time=0.2)
            prev = None
            for k in range(8):
                tok = ts.token()
                self.play(FadeIn(tok, shift=RIGHT * 0.25), *([FadeOut(prev)] if prev else []), run_time=0.14)
                self.play(ts.admit(tok, 0.22), bar_flash(b76, 0.6, 0.22), run_time=0.22)
                prev = tok
            ninth = ts.token()
            self.play(FadeIn(ninth, shift=RIGHT * 0.25), FadeOut(prev), run_time=0.25)
            vo.wait_until("a ninth fails")
            self.play(ninth.animate.shift(RIGHT * 0.25), FadeIn(b7374), FadeOut(b76), run_time=0.35)
            self.play(*ts.lock(text=None), FadeIn(msg, shift=UP * 0.1), run_time=0.6)
            self.play(flash(ts.counter, ERR, 1.3), run_time=0.5)
            vo.wait_until("and the lock stays shut")
            tool = ts.token(HARNESS, "tool")
            self.play(FadeOut(ninth), FadeIn(tool, shift=RIGHT * 0.25), FadeOut(b7374), run_time=0.3)
            hit = ts.hub.get_center() + LEFT * (0.85 + tool.width / 2)     # the lock sticks: the tool
            back = tool.get_center().copy()                                 # token runs at it and back
            self.play(tool.animate(rate_func=rush_into).move_to(hit), FadeIn(b6970), run_time=0.4)
            self.play(tool.animate.move_to(back), FadeIn(sticks, shift=LEFT * 0.1), run_time=0.45)

        # ========================================================== 4 · without Budget: the SDK fallback
        fe = cr.fence()
        fe.remove(fe.label)
        # the fence, drawn here 0.2 less tall than .fence()'s (its top ran 0.08 under the tracker)
        outer = cr.frames["cartcheck"]
        fe.frame = box(outer.width + 0.6, outer.height + 0.3, S.GREY, dashed=True, stroke=3,
                       radius=0.45).move_to(outer)
        apart(fe.frame, tr, 0.15)
        fe_lab = fit_rows(FENCE_TEXT, 5.4, CAPTION, S.GREY, align=LEFT)
        place(fe_lab, left=fe.frame.get_right()[0] + 0.35, cy=cr.core.get_center()[1])
        e56 = src_panel("formaggio/agents/execution.py", 56, 58, join=[(57, 58)], size=20,
                        wrap={57: ['{"max_iterations"', '"max_duration_seconds"', '"allow_concurrent_invocation"']})
        place(e56, cx=0, bottom=-3.5)
        ill4 = illustration_tag()
        place(ill4, left=fe.frame.get_right()[0] + 0.35, top=fe.frame.get_top()[1])
        apart(fe.frame, tr, 0.02)
        apart(fe.frame, e56, 0.1)
        apart(fe_lab, e56, 0.1)
        apart(ill4, fe_lab, 0.1)
        sp40 = e56.span(57, '"max_iterations": 40')
        spfc = e56.span(57, '"max_function_calls": None')
        spdur = e56.span(57, '"max_duration_seconds": None')
        rings4 = {id(sp): ring(sp, TURN, buff=0.06, stroke=3) for sp in (sp40, spfc, spdur)}
        inside_frame(fe.frame, fe_lab, e56, ill4)

        with self.voiceover(SAY[4]) as vo:
            self.play(*cr.lift("budget"), FadeOut(VGroup(ts, tool, msg, q230, ill3)), run_time=0.6)
            self.play(FadeOut(VGroup(ep, b6970, sticks)), run_time=0.3)
            self.play(FadeIn(e56, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("only the framework's fallback")
            self.play(Create(fe.frame), FadeIn(ill4), run_time=0.8)
            self.play(FadeIn(fe_lab, shift=LEFT * 0.1), run_time=0.5)
            for sp, a in ((sp40, "40 loop iterations"), (spfc, "no call limits"), (spdur, "no overall time budget")):
                vo.wait_until(a)                       # (the strings are yellow already: ring them)
                self.play(Create(rings4[id(sp)]), run_time=0.5)
        cr.frames["budget"].set_stroke(width=3)        # (invisible while lifted: it comes back unlit)
        self.play(*cr.put("budget"), FadeOut(VGroup(fe.frame, fe_lab, ill4, e56, *rings4.values())), run_time=0.7)

        # ========================================================== 5 · Cart Check: the verify step; back to the hook
        ex232 = excerpt_chip(R232, "README.md · line 232 (excerpt)", line=source_line("README.md", 232))
        place(ex232, left=fe.frame.get_right()[0] + 0.15, top=2.86)
        ss = SixSteps()
        place(ss, cx=0, bottom=-3.48)
        cb = answer_b()
        place(cb, left=-6.3, top=cr.get_bottom()[1] - 0.3)
        chk = check_box()
        place(chk, right=SAFE_X, top=ex232.get_bottom()[1] - 0.2)
        rec = recorded_tag()
        place(rec, right=SAFE_X, top=chk.get_bottom()[1] - 0.1)
        # GREEN arrows: the check reads the three item lines (rows 3-5)
        items5 = [chk.rows[k] for k in (3, 4, 5)]
        x_bar = max(r.glyphs.get_right()[0] for r in items5) + 0.75
        spine = Line([x_bar, items5[0].get_center()[1], 0], [x_bar, items5[-1].get_center()[1], 0],
                     color=HARNESS, stroke_width=4)
        arrows = VGroup(*[Arrow([x_bar, r.get_center()[1], 0], [r.glyphs.get_right()[0] + 0.08, r.get_center()[1], 0],
                                buff=0, color=HARNESS, stroke_width=4, tip_length=0.16,
                                max_tip_length_to_length_ratio=0.5) for r in items5])
        items_g = VGroup(spine, arrows)
        assert x_bar < chk.frame.get_right()[0] - 0.1
        # the GREY dashed arrow to the prose, "not read"
        a_from = np.array([chk.frame.get_left()[0] - 0.1, chk.rows[0].get_center()[1], 0])
        a_to = np.array([cb.frame.get_right()[0] + 0.1, cb.frame.get_center()[1], 0])
        nr_line = DashedLine(a_from, a_to, color=S.GREY, stroke_width=3, dash_length=0.12)
        nr_tip = Arrow(a_from + (a_to - a_from) * 0.9, a_to, buff=0, color=S.GREY, stroke_width=3,
                       tip_length=0.18, max_tip_length_to_length_ratio=1.0)
        nr_t = note("not read")
        mid = (a_from + a_to) / 2
        nr_t.move_to(mid + np.array([-0.55, 0.3, 0]))
        notread = VGroup(nr_line, nr_tip, nr_t)
        # the four statuses (README.md line 236) and the tag
        st_head = VGroup(mono("README.md", CAPTION, S.GREY), note("· line 236")).arrange(RIGHT, buff=0.12)
        st_chips = VGroup(*[chip(s, c, size=CAPTION, font=MONO) for s, c in
                            zip(STATUSES, (HARNESS, ERR, S.GREY, S.GREY))]).arrange(RIGHT, buff=0.18)
        st_tag = grey_tag("reports · never repairs")
        st_top = VGroup(st_head, st_tag).arrange(RIGHT, buff=0.35)
        status = VGroup(st_top, st_chips).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        place(status, left=-6.3, bottom=ss.get_top()[1] + 0.22)
        lr21 = lref("21")
        verdict = chk.rows[6]
        for a, b in ((ex232, cr), (cb, cr), (chk, ex232), (cb, chk), (rec, status), (chk, status),
                     (status, ss), (ex232, lr21), (cb, status), (nr_t, cr), (nr_t, chk), (nr_t, cb), (nr_t, ex232)):
            apart(a, b, 0.06)
        inside_frame(ex232, ss, cb, chk, rec, status, notread)

        with self.voiceover(SAY[5]) as vo:
            self.play(cr.glow("cartcheck"), FadeIn(ex232, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("the lecture's verify step")
            # the slide-21 tag arrives with slide 21's strip (old tag out, then the new one in)
            self.play(Succession(FadeOut(lr), FadeIn(lr21)), FadeIn(ss, shift=UP * 0.15), run_time=0.6)
            lr = lr21
            self.play(ss.light("Verify", HARNESS), run_time=0.5)
            vo.wait_until("Back to the hook")
            self.play(FadeIn(cb, shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(chk, shift=LEFT * 0.15), FadeIn(rec), run_time=0.5)
            vo.wait_until("it checked the items")
            self.play(Create(spine), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.25), run_time=0.8)
            vo.wait_until("not the prose")
            self.play(Create(nr_line), FadeIn(nr_tip), run_time=0.6)
            self.play(FadeIn(nr_t, shift=DOWN * 0.08), run_time=0.4)
            vo.wait_until("so the garbled budget still passed")
            self.play(pulse(cb.ring, ERR, 1.25, run_time=0.8, width=6),
                      flash(verdict.glyphs, HARNESS, 1.08), run_time=0.8)
            vo.wait_until("It reports, and never repairs")
            # the strip has made its point: it leaves before the statuses come (three groups on screen)
            self.play(FadeOut(ss, shift=DOWN * 0.1), run_time=0.3)
            self.play(FadeIn(st_head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in st_chips], lag_ratio=0.25),
                      run_time=0.8)
            self.play(FadeIn(st_tag, shift=LEFT * 0.1), run_time=0.4)

        # ========================================================== 6 · V1: the action boundary
        ab = ActionBoundary(show=())
        ab.move_to([0, -0.05, 0])
        lr22 = lref("22")
        apart(ab, tr, 0.02)
        apart(ab, lr22, 0.05)
        inside_frame(ab)
        rows5 = ("control", "tools", "context", "verify", "sub")
        blue_frames = [ab.blues[n].frame for n in rows5]
        green_frames = [ab.greens[n].frame for n in rows5]

        def column(frames, color):
            top, bot = frames[0].get_top()[1], frames[-1].get_bottom()[1]
            r = RoundedRectangle(width=frames[0].width, height=top - bot, corner_radius=0.12,
                                 stroke_color=color, stroke_width=3).set_fill(color, 0.08)
            return r.move_to([frames[0].get_center()[0], (top + bot) / 2, 0])
        col_b, col_g = column(blue_frames, CLOUD), column(green_frames, HARNESS)

        with self.voiceover(SAY[6]) as vo:
            gone = [cr, ex232, rec, items_g, notread, status, cb.row, cb.header, cb.ring, chk.rows, chk.rule]
            self.play(*[FadeOut(m) for m in gone], run_time=0.5)
            lr = lref_swap(self, lr, "22")
            self.play(Transform(cb.frame, col_b), Transform(chk.frame, col_g), run_time=0.9)
            self.add(ab)
            self.play(*ab.parts_in("heads", "who"), run_time=0.6)
            # each column splits into five cells: five stacked copies whose fills add up to the
            # column's (0.08), each going to its cell at the cell's own (saved) opacities; a copy at
            # opacity 1 flashed two solid BLUE / GREEN blocks
            k = 1 - (1 - 0.08) ** (1 / len(rows5))
            pieces_b = [col_b.copy().set_fill(opacity=k) for _ in rows5]
            pieces_g = [col_g.copy().set_fill(opacity=k) for _ in rows5]
            self.remove(cb.frame, chk.frame)
            self.add(*pieces_b, *pieces_g)
            self.play(*[Transform(p, shown_copy(f)) for p, f in zip(pieces_b, blue_frames)],
                      *[Transform(p, shown_copy(f)) for p, f in zip(pieces_g, green_frames)], run_time=0.8)
            for n in rows5:
                _set_op(ab.blues[n].frame)
                _set_op(ab.greens[n].frame)
            self.remove(*pieces_b, *pieces_g)
            vo.wait_until("five concerns")
            ab._flag(ab.parts["pills"], False)
            self.play(LaggedStart(*[_Reveal(ab.pills[n], shift=UP * 0.1) for n in rows5], lag_ratio=0.2),
                      run_time=1.0)
            vo.wait_until("the model's part on the left")
            ab._flag(ab.parts["blue"], False)
            self.play(LaggedStart(*[_Reveal(ab.blue_texts[n]) for n in rows5], lag_ratio=0.15), run_time=0.9)
            vo.wait_until("the harness's on the right")
            ab._flag(ab.parts["green"], False)
            self.play(*[pulse(f, HARNESS, 1.0, run_time=0.8, width=5) for f in green_frames], run_time=0.8)

        # ========================================================== 7 · Act 1 fills three rows; move right
        fills = [("control", "Budget · admission"), ("tools", "@tool schemas · counted, audited calls"),
                 ("verify", "CartCheck")]
        ml, mr = ab.parts["moves_left"], ab.parts["moves_right"]

        with self.voiceover(SAY[7]) as vo:
            for n, text in fills:
                _, an = ab.fill(n, text, run_time=0.4)
                self.play(ab.light(n), *an, run_time=0.45)
            self.play(ab.unlight(), *ab.parts_in("moves_left", "moves_right"), run_time=0.5)
            vo.wait_until("Move right")
            self.play(Indicate(mr.arrow, color=HARNESS, scale_factor=1.2), flash(mr.title, HARNESS, 1.15),
                      run_time=0.8)
            self.play(Indicate(mr.arrow, color=HARNESS, scale_factor=1.2), run_time=0.7)

        # ========================================================== 8 · ponder: harness.without("trace")
        # compact onions: the picture must stay above the ponder card (its top at -0.3)
        oa = HarnessRings(mode="compact").move_to(ONION_A)
        ob = HarnessRings(mode="compact", without=("trace",)).move_to(ONION_B)
        ta = mono("harness", CAPTION, INK)
        place(ta, cx=oa.get_center()[0], bottom=oa.get_top()[1] + 0.19)   # (room for beat 9's tag beside it)
        tb = mono('lite = harness.without("trace")', CAPTION, INK)
        place(tb, cx=ob.get_center()[0], bottom=ob.get_top()[1] + 0.19)
        ill8 = illustration_tag()           # top right (no lecture tag now): beside tb sits beat 9's caption
        place(ill8, right=SAFE_X, top=3.55)
        q_trace = pointer(oa.frames["trace"], [("`Trace()`", TURN), ("?", TURN)], oa.get_right()[0] + 0.35)
        q_lite = pointer(ob.frames["inner"], [("counted · audited", TURN), ("?", TURN)], ob.get_right()[0] + 0.35)
        apart(ta, tr, 0.08)
        apart(oa, ob, 0.2)
        apart(q_trace, ob, 0.15)
        inside_frame(oa, ob, ta, tb, ill8, q_trace, q_lite)
        ponder_top = -3.55 + ponder_card(PONDER, width=10.2).height    # ponder_at keeps its bottom at -3.55
        assert oa.get_bottom()[1] > ponder_top + 0.1 and ob.get_bottom()[1] > ponder_top + 0.1, ponder_top

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(ab), FadeOut(lr), run_time=0.6)
            self.play(FadeIn(oa, shift=UP * 0.15), FadeIn(ta), FadeIn(ill8), run_time=0.6)
            vo.wait_until("Take harness without trace")
            self.play(FadeIn(ob, shift=UP * 0.15), FadeIn(tb), run_time=0.6)
            self.play(flash(tb, TURN, 1.06), run_time=0.6)
            vo.wait_until("Is a tool call still counted")
            self.play(ob.glow("inner", TURN), Create(q_lite.leader), run_time=0.4)
            self.play(FadeIn(q_lite.text, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("And does the original harness")
            self.play(oa.glow("trace", TURN), Create(q_trace.leader), run_time=0.4)
            self.play(FadeIn(q_trace.text, shift=LEFT * 0.1), run_time=0.4)
        card = ponder_at(self, PONDER, seconds=8.0)

        # ========================================================== 9 · yes, and yes: the inner ring; new configurations
        ex229 = excerpt_chip(R229, "README.md · line 229 (excerpt)", line=source_line("README.md", 229))
        place(ex229, cx=0, bottom=-3.45)
        apart(ex229, oa, 0.1)
        hp = src_panel("formaggio/agents/harness.py", 62, 68, wrap=True, size=20)
        place(hp, cx=0, bottom=-3.5)
        b63, b68 = row_bar(hp, 63), row_bar(hp, 68)
        # each onion's caption sits in its title row, after its name (between the onions, "unchanged"
        # sat closer to lite than to harness; under the illustration tag, the caption read as the
        # quote card's)
        unch = tag("unchanged", HARNESS)
        place(unch, left=ta.get_right()[0] + 0.3,                                  # level with ta, clear of oa
              cy=max(ta.get_center()[1], oa.get_top()[1] + 0.09 + unch.height / 2))
        sep = note("a separate configuration")
        place(sep, left=tb.get_right()[0] + 0.3, cy=tb.get_center()[1])
        assert sep.get_right()[0] <= SAFE_X, sep.get_right()
        q234 = quote_card(234, lines=["`.add(...)` also returns", "a new configuration."],
                          header="README.md · line 234 (excerpt)", expected=False)
        place(q234, right=SAFE_X, top=sep.get_bottom()[1] - 0.25)
        for a_, b_ in ((unch, ob), (unch, tb), (sep, tb), (q234, hp), (q234, ob), (sep, ob), (oa, hp), (ob, hp),
                       (unch, hp), (q234, ill8), (sep, ill8), (unch, oa)):
            apart(a_, b_, 0.08)
        apart(unch, tr, 0.08)
        inside_frame(hp, unch, sep, q234, ex229)

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(card), FadeOut(VGroup(q_lite, q_trace)), oa.unglow("trace"), ob.unglow("inner"),
                      run_time=0.5)
            vo.wait_until("Admission and the audit")
            self.play(ob.glow("inner", HARNESS), FadeIn(ex229, shift=UP * 0.1), run_time=0.6)
            self.play(flash(ob.parts["inner"].lock, HARNESS, 1.8), run_time=0.6)
            vo.wait_until("And the add and without methods")
            self.play(FadeOut(ex229), ob.unglow("inner"), run_time=0.4)   # (the onions keep their tag)
            self.play(FadeIn(hp, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("never change a harness")
            self.play(FadeIn(b63), FadeIn(b68), run_time=0.4)
            vo.wait_until("each returns a new configuration")
            self.play(flash(hp.span(63, "return replace("), TURN, 1.08),
                      flash(hp.span(68, "return replace("), TURN, 1.08), run_time=0.7)
            self.play(FadeIn(sep, shift=LEFT * 0.1), FadeIn(q234, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("so the original keeps all four layers")
            self.play(oa.glow("trace"), FadeIn(unch, shift=LEFT * 0.1), run_time=0.5)
            self.play(oa.unglow("trace"), run_time=0.4)

        # ========================================================== 10 · step 4: missing details; ▶ your turn
        t = term(container=True, rows=12)
        ft = frame_tags(t, nokey_tag(), live_tag())
        c248 = top_chip(R248, where="README.md · line 248", expected=True)
        c252 = top_chip(R252, where="README.md · line 252 (excerpt)")
        apart(c248, t, 0.02)
        apart(c252, t, 0.02)
        tc = turn_card([Prose("with your key:"), C12.cmd, Prose("look for: a question back · CartCheck: no_cart"),
                        (Prose("live · billed per token"), COST)])
        place(tc, cx=0, cy=-0.2)
        inside_frame(t, ft, c248, c252, tc)

        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(oa, ob, ta, tb, ill8, unch, sep, q234, hp, b63, b68)), run_time=0.5)
            self.play(tr.goto(4), FadeIn(t, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(ft, shift=DOWN * 0.1), run_time=0.3)
            type_cmd(self, t, C12.cmd, 0.9)
            out = show(self, t, C12, 4, C12.cut(6, ASK_CUT), (8, 10), C12.as401(11, short=True), wrap=True,
                       run_time=0.8)
            bare_prompt(self, t)
            ask_rows = item_rows(out, 1)
            lit = wrapped_glyphs(ask_rows, ASK_LIT)
            vo.wait_until("With a key, look for a question back")
            self.play(lit.animate.set_color(TURN), FadeIn(c248, shift=DOWN * 0.1), run_time=0.5)
            self.play(flash(c248.phrase, TURN, 1.03), run_time=0.6)
            vo.wait_until("Cart Check should report no cart")
            self.play(FadeOut(c248), run_time=0.3)
            self.play(FadeIn(c252, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Pause and run it")
            self.play(FadeOut(VGroup(t, ft)), run_time=0.4)
            self.play(FadeIn(tc, shift=UP * 0.1), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame (the checkpoint chip stays)
        self.play(FadeOut(VGroup(tr, tc, c252)), run_time=0.6)
        self.wait(0.3)


def substring_text(t, sub: str) -> VGroup:
    """The glyphs of `sub` in a one-line mono Text (spaces have no glyphs)."""
    s = t.text
    i = s.find(sub)
    assert i >= 0, (sub, s)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t[a:a + n])
