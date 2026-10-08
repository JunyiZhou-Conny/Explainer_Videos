"""S03 · Who did what.

Beats: the team builds column by column. PINK the user (where S02 left them), BLUE the agent (one
long session), a grid of 183 faded-BLUE dots filling in with its count (183 sub-agents in 46
workflow runs, before this video), a GREY "workflow script" card that comes out of the agent and
launches three of the dots (copies fly out and become sub-agents, each with a job tag), and the GREY
tools with a gloss each (the two voices and the recognizer are pointed at as they are named) ->
the other columns step aside, the user moves to the corner and the PINK column expands into a
checklist (30 pt, mid-frame) that ticks as each item is named; on "supplied the program" it shrinks
to the top band (24 pt) as the real program slides up under it (A09, lines 31-38 of the extracted
file, which are lines 43-50 of the request; text as pasted, indent removed, the user's comments
verbatim and unhighlighted; 20 pt, the largest size its 76-character line allows);
it runs and prints a GREEN 255168 (A24); the "0" on the one highlighted line becomes a BLUE "O" in a
diff chip ("0" (zero) -> "O" (the letter O): the two glyphs look alike in a code font), held by a
small agent icon -> that icon becomes the BLUE column in the corner: eight GREY chips of what it
made, then the commit ribbon (A11, git up to bb3fc1e, UTC, on S02's date axis): one tick per
commit, PINK for the user's two, a gloss for "commit", the Oct 6 burst, WIP dots, GREY usage-limit
bands (A12) and the user's two PINK nudges -> the ribbon rises; two speed bars on the same time
axis (a PINK request dot, a BLUE bar to the final cut) -> the cost card (LIVE value, always with
LIVE's label) counts up under the dimmed ribbon; "the whole session" circles the ribbon, and the
four PINK request pins of S02 light up on "all four requests".

Every number on screen is checked in _check() (runs on import): the commit counts, the stops, the
two durations, the request times, the user's program really printing 255168, and the agent's
one-character change on the highlighted line.

Helpers defined here (not in common.py): tools_glyph(), name_chip(), check_item(), items_top_y(),
dot_grid(), diff_chip(), Ribbon / ribbon(), speed_bar(), request_pin().
"""

import contextlib
import csv
import datetime as dt
import io
import textwrap

import numpy as np
from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AGENT, INK, LIVE, MEASURED, NARRATION, PANEL, QUOTES, SUB_AGENT, SUB_AGENT_TEXT, TOOL,
                    USER, asset, asset_text, box, caption, check_mark, chip, code_panel, code_span,
                    cost_card, dim, emphasize, fade_out_all, file_icon, gather, label, line_bar, mono,
                    pulse, role_icon, source_caption, tag, terminal, time_axis)

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ the numbers on screen (real data)
ORIGINAL = asset_text("user_original_program.py")      # A09: the user's program, as pasted
CLEANED = asset_text("play_all_games.py")              # A09: the agent's cleaned copy
PROGRAM_OUT = asset_text("play_all_games.out")         # A24: "255168"
EXCERPT_FIRST, EXCERPT_LAST = 31, 38                   # total = 0 ... return total (1-based)
EXCERPT = textwrap.dedent("\n".join(ORIGINAL.splitlines()[EXCERPT_FIRST - 1:EXCERPT_LAST]))
NEXT_LINE = 4                                          # next_player = "0" ... (0-based, in EXCERPT)
# The line numbers count lines of the extracted file (A09 starts it at WIN_LINES); in the request
# itself the program opens with two docstrings, so the same lines are 43-50 there. The caption
# therefore names the file the numbers belong to.
PANEL_PATH = "the user's program, as pasted in the request: user_original_program.py"


def _commits():
    """A11: (utc, role, wip) per commit, oldest first (no names: roles only)."""
    with asset("commits.csv").open() as f:
        return [(dt.datetime.fromisoformat(r["utc"]), r["role"], r["wip"] == "True") for r in csv.DictReader(f)]


def _stops():
    """A12: (stop, end, user_restart) per usage-limit stop; end = resumed, else reset, else None."""
    out = []
    with asset("usage_limits.csv").open() as f:
        for r in csv.DictReader(f):
            end = r["resumed"] or r["reset"]
            out.append((dt.datetime.fromisoformat(r["stop"]), dt.datetime.fromisoformat(end) if end else None,
                        bool(r["resumed"])))
    return out


COMMITS = _commits()
STOPS = _stops()
# the two restarts that came from the user's own messages (A12, checked against the transcript):
# "… Please continue from where you left off." (cut, so "…" marks it, as in S02) and "Try again" (whole)
NUDGES = [(dt.datetime(2026, 10, 7, 2, 12), "Please continue …"), (dt.datetime(2026, 10, 7, 20, 9), "Try again")]
# request -> final cut (git + the request log; fact sheet 2a)
PRIVACY = (dt.datetime(2026, 10, 4, 15, 28), dt.datetime(2026, 10, 4, 21, 29))
TICTACTOE = (dt.datetime(2026, 10, 5, 21, 53), dt.datetime(2026, 10, 6, 1, 0))
REQUESTS = [(r["n"], dt.datetime.fromisoformat(f"{r['date']} {r['utc']}")) for r in QUOTES["requests"]]
T0, T1 = "2026-10-04 00:00", "2026-10-08 00:00"         # the axis of S02 (UTC)

TOOLS = [("Manim", "animation"),
         ("Kokoro", "text-to-speech,\nEnglish, local"),
         ("edge-tts", "online text-to-speech via\nMicrosoft Edge (Chinese)"),
         ("faster-whisper", "speech recognizer"),
         ("FFmpeg", "video"),
         ("jieba", "Chinese word breaks"),
         ("LaTeX", "math")]
JOBS = ["build one scene", "review", "translate"]
MADE = ["toolkit", "scripts", "scenes", "translations", "voices", "subtitles", "reviews", "renders"]
CHECKLIST = ["chose the topics and the audiences", "uploaded 36 PDFs", "gave the tic-tac-toe counts",
             "supplied the program"]
# The footer follows the narration's wording (script.md live values: "about a hundred" switches to
# "over a hundred" above about 110 commits), so the two can't drift apart. The ribbon itself stays
# frozen at bb3fc1e (98 commits), as its source caption says.
if "about a hundred" in SAY[2]:
    FOOTER = "about 100 commits · 2 by the user"
elif "over a hundred" in SAY[2]:
    FOOTER = "over 100 commits · 2 by the user"
else:
    raise AssertionError("S03 say line 3 changed its commit wording: update FOOTER to match")


def _check():
    # A11: 98 commits up to bb3fc1e, the first two (and only those) by the user, 28 WIP, 50 on Oct 6
    assert len(COMMITS) == 98
    assert [r for _, r, _ in COMMITS[:2]] == ["user", "user"] and sum(r == "user" for _, r, _ in COMMITS) == 2
    assert sum(w for *_, w in COMMITS) == 28
    assert sum(t.date() == dt.date(2026, 10, 6) for t, *_ in COMMITS) == 50
    assert all(dt.datetime.fromisoformat(T0) <= t < dt.datetime.fromisoformat(T1) for t, *_ in COMMITS)
    # A12: at least 6 stops; the two user restarts are the two known "resumed" times
    assert len(STOPS) == 6
    assert [e for _, e, by_user in STOPS if by_user] == [t for t, _ in NUDGES]
    # "about 6 hours" (6 h 01 min) and "about 3 hours" / "just over three" (3 h 07 min)
    assert round((PRIVACY[1] - PRIVACY[0]).total_seconds() / 3600) == 6
    assert 3 < (TICTACTOE[1] - TICTACTOE[0]).total_seconds() / 3600 < 3.25
    assert [n for n, _ in REQUESTS] == [1, 2, 3, 4]
    assert REQUESTS[0][1] == PRIVACY[0] and REQUESTS[1][1] == TICTACTOE[0]
    # A09/A24: the user's program, exactly as pasted, already printed the answer
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(ORIGINAL, "user_original_program.py", "exec"), {"__name__": "user_program"})
    assert out.getvalue().strip() == PROGRAM_OUT.strip() == "255168"
    # ... and on the highlighted line, the agent's only change is the digit 0 -> the letter O
    a = [s.strip() for s in ORIGINAL.splitlines() if s.strip().startswith("next_player")]
    b = [s.strip() for s in CLEANED.splitlines() if s.strip().startswith("next_player")]
    assert a == ['next_player = "0" if player == "X" else "X"'] and b == [a[0].replace('"0"', '"O"')]
    assert EXCERPT.splitlines()[NEXT_LINE].strip() == a[0]
    assert len(EXCERPT.splitlines()) == EXCERPT_LAST - EXCERPT_FIRST + 1      # the caption's "lines 31–38"
    assert "#" in EXCERPT                              # the user's own comments are in the excerpt


_check()

# ------------------------------------------------------------------ layout
HEAD_Y = 2.75                    # the column heads; S02 leaves the user at (-5.75, 2.75), height 1.25
ICON_H = 1.25
X_USER, X_AGENT, X_SUBS, X_TOOLS = -5.75, -3.45, -0.75, 3.7
LABEL_TOP = 1.92                 # top of the labels under the column heads
TOOL_X = 0.98                    # left edge of the tool rows
ROW_X = -4.75                    # left edge of the checklist / chip rows next to the corner icon
ROW_Y = (3.05, 2.4)
CORNER = np.array([-5.8, 3.05, 0])   # the role in focus (beats 2 and 3): a smaller icon in the corner
CORNER_H = 0.95
AXIS_Y = -0.3                    # the ribbon's axis in S03's third beat; it rises in the fourth
RISE = 1.6


# ------------------------------------------------------------------ helpers (this scene only)
def tools_glyph(height: float = 0.9) -> VGroup:
    """A GREY terminal window ('tools': programs the agent runs), drawn from primitives."""
    w = height * 1.4
    win = RoundedRectangle(width=w, height=height, corner_radius=0.1, stroke_color=TOOL, stroke_width=3)
    win.set_fill(PANEL, 1)
    top = height * 0.24
    bar = Line(win.get_corner(UL) + DOWN * top, win.get_corner(UR) + DOWN * top, color=TOOL, stroke_width=2.5)
    dots = VGroup(*[Dot(radius=0.035, color=TOOL) for _ in range(3)]).arrange(RIGHT, buff=0.06)
    dots.move_to(win.get_corner(UL) + np.array([0.22, -top / 2, 0]))
    prompt = mono(">_", 26, TOOL).move_to(win.get_center() + DOWN * top / 2)
    return VGroup(win, bar, dots, prompt)


def name_chip(s: str, width: float, size: float = 22) -> VGroup:
    """A GREY tool chip of a fixed width (the tool rows line up), text centred."""
    t = label(s, size, INK)
    h = 0.5
    b = box(width, h, TOOL, fill_opacity=0.16, radius=h / 2.6)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def check_item(s: str, size: float = 30) -> VGroup:
    """A PINK checklist item: an empty box and the text; .tick is the PINK check mark to Create
    (positioned, not in the group). Sizes scale with `size` (30 pt here, shrunk to 24 pt later)."""
    k = size / 24
    b = RoundedRectangle(width=0.36 * k, height=0.36 * k, corner_radius=0.07 * k, stroke_color=USER,
                         stroke_width=2.5)
    b.set_fill(USER, 0.1)
    t = label(s, size, INK)
    g = VGroup(b, t).arrange(RIGHT, buff=0.18 * k)
    g.box, g.text = b, t
    g.tick = check_mark(0.34 * k, USER, 5)
    return g


def items_top_y(grid: VGroup) -> float:
    """Centre y of the first checklist row of a (possibly scaled) checklist grid."""
    return grid[0].get_center()[1]


def dot_grid(n: int = 183, cols: int = 23, step: float = 0.13, radius: float = 0.045) -> VGroup:
    """n faded-BLUE dots, row by row (183 = 8 rows of 23, less one)."""
    dots = VGroup(*[Dot([(k % cols) * step, -(k // cols) * step, 0], radius=radius, color=SUB_AGENT)
                    for k in range(n)])
    rows = -(-n // cols)
    frame = Rectangle(width=(cols - 1) * step, height=(rows - 1) * step).move_to(
        [(cols - 1) * step / 2, -(rows - 1) * step / 2, 0])
    dots.shift(-frame.get_center())        # centred on the full 23 x 8 block, not on the 183 dots
    return dots


def diff_chip(size: float = 24):
    """The agent's edit: '"0" (zero) -> "O" (the letter O)', the O in BLUE (the two glyphs look
    alike in a code font, so each gets its name), then a second line 'comments rewritten'.
    Returns (chip, box_short): the full chip and the box that frames only the first line."""
    z0 = mono('"0"', size, INK)
    n0 = caption("(zero)", 20)
    arrow = mono("→", size, INK)
    z1 = mono('"O"', size, AGENT)
    n1 = caption("(the letter O)", 20)
    first = VGroup(z0, n0, arrow, z1, n1).arrange(RIGHT, buff=0.12)
    for n in (n0, n1):
        n.align_to(z0, DOWN)
    arrow.shift(RIGHT * 0.06)
    z1.shift(RIGHT * 0.12)
    n1.shift(RIGHT * 0.12)
    rest = label("comments rewritten", size, INK)
    body = VGroup(first, rest).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    full = box(body.width + 0.52, body.height + 0.34, AGENT, fill_opacity=0.12, radius=0.2)
    body.move_to(full)
    short = box(full.width, first.height + 0.34, AGENT, fill_opacity=0.12, radius=0.2)
    short.align_to(full, UP).align_to(full, LEFT)
    g = VGroup(full, body)                  # the first line sits centred in the short box too
    g.box, g.zero, g.oh, g.first, g.rest = full, z0, z1, first, rest
    g.names = VGroup(n0, n1)
    return g, short


class Ribbon(VGroup):
    """ribbon(): .axis (a common.TimeAxis), .days, .ticks, .user_ticks, .wip, .bands, .x_of(t)."""


def ribbon(axis_y: float = AXIS_Y, tick_h: float = 0.62) -> Ribbon:
    """The commit ribbon (A11, A12) on S02's date axis: midnight ticks, day names, one tick per
    commit (PINK = the user, BLUE = the agent), a GREY dot over each WIP commit, GREY usage-limit
    bands (a plain GREY tick where the end is unknown), behind the ticks."""
    axis = time_axis(T0, T1, width=12.0)
    axis.move_to([0, axis_y, 0])
    x_of = axis.x_of
    days = VGroup()
    for d in range(4, 9):                       # as in S02: midnight ticks, day names mid-day
        x = x_of(f"2026-10-{d:02d} 00:00")
        days.add(Line([x, axis_y - 0.12, 0], [x, axis_y + 0.12, 0], color=TOOL, stroke_width=2))
        if d < 8:
            days.add(caption(f"Oct {d}", 20).move_to([x_of(f"2026-10-{d:02d} 12:00"), axis_y - 0.32, 0]))
    ticks, user_ticks, wip = VGroup(), VGroup(), VGroup()
    for t, role, is_wip in COMMITS:
        x = x_of(t)
        ln = Line([x, axis_y + 0.06, 0], [x, axis_y + 0.06 + tick_h, 0], stroke_width=2.4,
                  color=USER if role == "user" else AGENT)
        ticks.add(ln)
        if role == "user":
            user_ticks.add(ln)
        if is_wip:
            wip.add(Dot([x, axis_y + tick_h + 0.17, 0], radius=0.034, color=TOOL))
    bands = VGroup()
    top = tick_h + 0.32
    for stop, end, _ in STOPS:
        x0 = x_of(stop)
        if end is None:
            m = Line([x0, axis_y, 0], [x0, axis_y + top, 0], color=TOOL, stroke_width=3.5)
        else:
            x1 = x_of(end)
            m = Rectangle(width=x1 - x0, height=top, stroke_width=0).set_fill(TOOL, 0.3)
            m.move_to([(x0 + x1) / 2, axis_y + top / 2, 0])
        bands.add(m.set_z_index(-1))
    g = Ribbon(axis.line, days, bands, ticks, wip)
    g.axis, g.days, g.ticks, g.user_ticks, g.wip, g.bands, g.x_of = axis, days, ticks, user_ticks, wip, bands, x_of
    g.tick_top = axis_y + 0.06 + tick_h
    return g


def speed_bar(x_of, axis_y: float, span, y: float, head: str, hours: str, rest: str) -> VGroup:
    """Request -> final cut on the ribbon's own time axis: a PINK dot (the user's request), a BLUE
    bar (the agent's work), a WHITE cap (final cut), dashed GREY drops from the axis, and the label.
    .dot .bar .cap .drops .text"""
    x0, x1 = x_of(span[0]), x_of(span[1])
    bar = Rectangle(width=x1 - x0, height=0.26, stroke_width=0).set_fill(AGENT, 0.9).move_to([(x0 + x1) / 2, y, 0])
    dot = Dot([x0, y, 0], radius=0.075, color=USER).set_z_index(2)   # over the bar that grows from it
    cap = Line([x1, y - 0.22, 0], [x1, y + 0.22, 0], color=INK, stroke_width=4)
    drops = VGroup(*[DashedLine([x, axis_y - 0.02, 0], [x, y + 0.13, 0], dash_length=0.06, stroke_width=1.6,
                                color=TOOL) for x in (x0, x1)])
    line2 = VGroup(label(hours, 22, INK), caption(rest, 20)).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    text = VGroup(label(head, 22, INK), line2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    text.next_to(cap, RIGHT, buff=0.22)
    mask = BackgroundRectangle(text, color=S.BG, fill_opacity=1, buff=0.08).set_z_index(1)
    text.set_z_index(2)
    text.add_to_back(mask)                  # later drop lines pass behind the label
    g = VGroup(drops, bar, dot, cap, text)
    g.dot, g.bar, g.cap, g.drops, g.text, g.hours = dot, bar, cap, drops, text, line2[0]
    return g


def request_pin(x_of, axis_y: float, n: int, t, height: float = 1.12) -> VGroup:
    """A request of S02 on the ribbon: a PINK dot on the axis (as in S02), a PINK hairline up
    through the ribbon and the request's number above it."""
    x = x_of(t)
    dot = Dot([x, axis_y, 0], radius=0.07, color=USER)
    line = Line([x, axis_y, 0], [x, axis_y + height, 0], color=USER, stroke_width=2.5)
    num = label(str(n), 26, USER, weight="BOLD").move_to([x, axis_y + height + 0.2, 0])
    return VGroup(line, dot, num)




# ------------------------------------------------------------------ the scene
class Team(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- the team, column by column
        user = role_icon("user", ICON_H).move_to([X_USER, HEAD_Y, 0])
        user_l = label("the user", 26, USER).next_to(user, DOWN, buff=0.25)
        agent = role_icon("agent", ICON_H).move_to([X_AGENT, HEAD_Y, 0])
        agent_l = VGroup(label("the agent:\nClaude Code", 26, AGENT, line_spacing=0.85),
                         caption("one long session", 22)).arrange(DOWN, buff=0.12)
        agent_l.move_to([X_AGENT, 0, 0]).align_to([0, LABEL_TOP, 0], UP)
        user_l.align_to(agent_l, UP)

        dots = dot_grid().move_to([X_SUBS, HEAD_Y, 0])
        count = Integer(0, font_size=30, color=SUB_AGENT_TEXT)
        sub_word = label("sub-agents", 26, SUB_AGENT_TEXT)
        runs = caption("46 workflow runs", 22)
        before = caption("before this video", 22)
        probe = label("183", 26)                               # layout probe only, never shown
        count_line = VGroup(probe, sub_word).arrange(RIGHT, buff=0.12)
        VGroup(count_line, runs, before).arrange(DOWN, buff=0.1).move_to([X_SUBS, 0, 0]) \
            .align_to([0, LABEL_TOP, 0], UP)

        def keep_count(m):
            m.next_to(sub_word, LEFT, buff=0.12).align_to(probe, DOWN)
        count.add_updater(keep_count)
        keep_count(count)

        glyph = tools_glyph().move_to([X_TOOLS, HEAD_Y, 0])
        tools_l = label("tools", 26, TOOL).move_to([X_TOOLS, 0, 0]).align_to([0, LABEL_TOP, 0], UP)
        name_w = max(label(n, 22).width for n, _ in TOOLS) + 0.44
        rows = VGroup()
        y = tools_l.get_bottom()[1] - 0.22
        for name, gl in TOOLS:
            r = VGroup(name_chip(name, name_w), caption(gl, 20, line_spacing=0.85)).arrange(RIGHT, buff=0.18)
            r.align_to([TOOL_X, 0, 0], LEFT).align_to([0, y, 0], UP)
            rows.add(r)
            y = r.get_bottom()[1] - 0.1

        # the workflow: a script the agent writes, launching three of the dots, one job each
        card_body = VGroup(file_icon(0.46), label("workflow script", 24, INK)).arrange(RIGHT, buff=0.18)
        card_box = box(card_body.width + 0.5, card_body.height + 0.34, TOOL, fill=PANEL, fill_opacity=1)
        card_body.move_to(card_box)
        wf_card = VGroup(card_box, card_body).move_to([-2.6, -0.3, 0])
        picks = [dots[k] for k in (30, 101, 150)]
        kids = [role_icon("sub", 0.62).person.move_to([x, -1.55, 0]) for x in (-4.55, -2.6, -0.7)]
        jobs = [tag(j, SUB_AGENT_TEXT, size=22).next_to(kd, DOWN, buff=0.16) for j, kd in zip(JOBS, kids)]
        arrows = [Arrow(wf_card.get_bottom(), kd.get_top(), buff=0.12, color=TOOL, stroke_width=3,
                        tip_length=0.16, max_tip_length_to_length_ratio=0.25) for kd in kids]
        src0 = source_caption("source: the session's workflow run records")

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(user, shift=UP * 0.2), FadeIn(user_l), run_time=0.7)
            vo.wait_until("One AI agent")
            self.play(FadeIn(agent, shift=UP * 0.2), FadeIn(agent_l, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("Under it")
            self.add(count)
            self.play(LaggedStart(*[FadeIn(d, scale=0.2) for d in dots], lag_ratio=0.03),
                      ChangeDecimalToValue(count, 183, rate_func=linear),
                      FadeIn(sub_word), FadeIn(src0), run_time=2.6)
            count.clear_updaters()
            vo.wait_until("in 46 workflow")
            self.play(FadeIn(runs, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("before this video")
            self.play(FadeIn(before, shift=UP * 0.1), run_time=0.5)

            vo.wait_until("A workflow is a script")
            self.play(FadeIn(wf_card, target_position=agent.get_bottom(), scale=0.3), run_time=0.9)
            vo.wait_until("to launch sub-agents")
            movers = [d.copy() for d in picks]
            self.play(*[d.animate.set_color(SUB_AGENT_TEXT).scale(1.6) for d in picks], run_time=0.4)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
                      LaggedStart(*[ReplacementTransform(m, kd, path_arc=PI / 5) for m, kd in zip(movers, kids)],
                                  lag_ratio=0.15), run_time=1.1)
            vo.wait_until("each with one job")
            self.play(LaggedStart(*[FadeIn(j, shift=DOWN * 0.1) for j in jobs], lag_ratio=0.25), run_time=0.9)

            vo.wait_until("And tools")
            self.play(FadeIn(glyph, shift=UP * 0.2), FadeIn(tools_l),
                      LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.1), run_time=1.1)
            vo.wait_until("like a synthetic voice")
            self.play(emphasize(rows[1], run_time=0.8), emphasize(rows[2], run_time=0.8))
            vo.wait_until("and a speech recognizer")
            self.play(emphasize(rows[3], run_time=0.8))

        # ---------------------------------------------------------- what the user did
        # the checklist builds large in the middle (30 pt), then shrinks to the top band (24 pt)
        # when the program slides up under it
        items = [check_item(s) for s in CHECKLIST]
        col2 = max(items[0].width, items[2].width) + 0.75
        for k, it in enumerate(items):
            it.move_to([0, (0.95, 0.1)[k // 2], 0]).align_to([(k % 2) * col2, 0, 0], LEFT)
        grid = VGroup(*items)
        grid.move_to([0.45, 0.55, 0])
        for it in items:
            it.tick.move_to(it.box.get_center() + np.array([0.05, 0.04, 0]))
        grid.add(*[it.tick for it in items])
        shrunk = grid.copy().scale(0.8)
        shrunk.shift(np.array([ROW_X, ROW_Y[0], 0]) - np.array([shrunk.get_left()[0], items_top_y(shrunk), 0]))
        # the real line is 76 characters long: 20 pt (the minimum) is the largest size that fits
        panel = code_panel(EXCERPT, PANEL_PATH, EXCERPT_FIRST, font_size=20)
        panel.move_to([0, 0, 0]).align_to([0, ROW_Y[1] - 0.4, 0], UP)
        code = panel.code
        bar = line_bar(code, NEXT_LINE)
        zero = code_span(code, NEXT_LINE, '"0"')
        term = terminal([("$ python user_original_program.py", TOOL), ("255168", MEASURED)], size=20)
        term.next_to(panel, DOWN, buff=0.3).align_to(panel, LEFT)
        term_head = VGroup(term.box, term[1], term[2], term.lines[0])
        diff, diff_short = diff_chip()
        helper = role_icon("agent", 0.8)
        helper.next_to(diff, LEFT, buff=0.22).align_to(diff, UP)
        cleaned = caption("the cleaned file is the code on screen\nin the tic-tac-toe video", 20)
        cleaned.next_to(diff, DOWN, buff=0.14).align_to(diff, LEFT)
        diff_group = VGroup(helper, diff, diff_short, cleaned)
        diff_group.align_to(panel, RIGHT).align_to(term, UP)
        shown = [VGroup(it.box, it.text) for it in items]
        assert abs(shrunk[0].text.font_size - 24) < 0.1

        corner_user = role_icon("user", CORNER_H).move_to(CORNER)
        corner_user_l = label("the user", 26, USER).next_to(corner_user, DOWN, buff=0.12)

        with self.voiceover(SAY[1]) as vo:
            team = gather(self, agent, agent_l, dots, count, sub_word, runs, before, wf_card, *kids, *jobs, *arrows,
                          glyph, tools_l, rows, src0)
            self.play(FadeOut(team, shift=RIGHT * 0.5), ReplacementTransform(user, corner_user),
                      ReplacementTransform(user_l, corner_user_l), run_time=0.8)
            for k, (it, sh, phrase) in enumerate(zip(items, shown, ("The user decided", "They uploaded",
                                                                     "gave the tic-tac-toe", "and supplied the program"))):
                vo.wait_until(phrase)
                self.play(FadeIn(sh, shift=RIGHT * 0.2), run_time=0.5)
                if k == 0:
                    vo.wait_until("and for whom")
                self.play(Create(it.tick), run_time=0.35)
            grid = gather(self, *shown, *[it.tick for it in items])
            # the checklist clears the middle before the program slides up into it (no crossing)
            self.play(LaggedStart(grid.animate.scale(0.8).move_to(shrunk), FadeIn(panel, shift=UP * 0.6),
                                  lag_ratio=0.6), run_time=1.3)
            vo.wait_until("It already worked")
            self.play(FadeIn(term_head, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(term.lines[1], shift=RIGHT * 0.1), run_time=0.4)
            self.play(emphasize(term.lines[1], run_time=0.6))
            vo.wait_until("The agent only changed")
            self.play(FadeIn(bar), run_time=0.4)
            self.play(Circumscribe(zero, color=S.WHITE, buff=0.06, run_time=0.8))
            vo.wait_until("into the letter O")
            self.play(FadeIn(helper, shift=UP * 0.15), FadeIn(diff_short),
                      LaggedStart(TransformFromCopy(zero, diff.zero),
                                  FadeIn(VGroup(diff.names[0], diff.first[2], diff.oh, diff.names[1]),
                                         shift=RIGHT * 0.15), lag_ratio=0.45), run_time=1.0)
            vo.wait_until("and rewrote the comments")
            self.play(ReplacementTransform(diff_short, diff.box), FadeIn(diff.rest, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(cleaned, shift=UP * 0.1), run_time=0.5)

        # ---------------------------------------------------------- what the agent did
        head = role_icon("agent", CORNER_H)
        head.shift(CORNER - head.person.get_center())       # the person on the corner spot, badge aside
        head_l = label("the agent", 26, AGENT).next_to(head.person, DOWN, buff=0.12).align_to(corner_user_l, UP)
        made = VGroup(*[chip(s, TOOL, size=24) for s in MADE])
        for r in range(2):
            VGroup(*made[4 * r:4 * r + 4]).arrange(RIGHT, buff=0.25).move_to([0, ROW_Y[r], 0]) \
                .align_to([ROW_X, 0, 0], LEFT)
        rib = ribbon(AXIS_Y)
        x_of = rib.x_of
        first_agent = [ln for ln in rib.ticks if ln not in rib.user_ticks][0]
        commit_gloss = label("commit = a saved version of the project", 24, TOOL)
        commit_gloss.move_to([0, AXIS_Y + 1.5, 0]).align_to([-6.4, 0, 0], LEFT)
        gloss_arrow = Arrow([first_agent.get_x(), commit_gloss.get_bottom()[1], 0],
                            [first_agent.get_x(), rib.tick_top + 0.27, 0], buff=0.06, color=TOOL, stroke_width=3,
                            tip_length=0.15, max_tip_length_to_length_ratio=0.4)
        oct6 = Line([x_of("2026-10-06 00:00"), rib.tick_top + 0.32, 0], [x_of("2026-10-07 00:00"), rib.tick_top + 0.32, 0])
        burst = Brace(oct6, UP, buff=0.02, color=TOOL)
        burst_l = label("50 commits that day", 24, INK).next_to(burst, UP, buff=0.08)
        wip_key = VGroup(Dot(radius=0.05, color=TOOL), caption("WIP checkpoint (work in progress)", 22))
        # both marks the ribbon uses for a stop: a band (its end is known) and a plain tick (it isn't)
        stop_swatch = VGroup(Rectangle(width=0.36, height=0.26, stroke_width=0).set_fill(TOOL, 0.3),
                             Line(DOWN * 0.15, UP * 0.15, color=TOOL, stroke_width=3.5)).arrange(RIGHT, buff=0.1)
        stop_key = VGroup(stop_swatch, label("usage-limit stops: at least 6", 22, INK))
        for kk in (wip_key, stop_key):
            kk.arrange(RIGHT, buff=0.16)
        VGroup(wip_key, stop_key).arrange(DOWN, aligned_edge=LEFT, buff=0.16) \
            .move_to([0, AXIS_Y - 1.15, 0]).align_to([-6.4, 0, 0], LEFT)
        nudges = VGroup()
        for t, words in NUDGES:
            x = x_of(t)
            d = Dot([x, AXIS_Y - 0.5, 0], radius=0.06, color=USER)
            ln = Line([x, AXIS_Y, 0], d.get_center(), color=USER, stroke_width=3.5)
            txt = label(f"the user:\n“{words}”", 22, USER, line_spacing=0.85).next_to(d, DOWN, buff=0.1)
            nudges.add(VGroup(ln, d, txt))
        # the two quotes sit 18 h apart on the axis: keep a clear gap so they never read as one line
        gap = nudges[1][2].get_left()[0] - nudges[0][2].get_right()[0]
        if gap < 0.5:
            nudges[0][2].shift(LEFT * (0.5 - gap))
        footer = label(FOOTER, 26, INK, t2c={"2 by the user": USER})
        footer.move_to([0, AXIS_Y - 2.05, 0])
        src2 = source_caption("git log up to commit bb3fc1e · usage-limit stops from the session transcript · UTC")
        # the first commit after each stop: work picked up where it left off
        resumed = VGroup(*[next(ln for (t, _, _), ln in zip(COMMITS, rib.ticks) if t >= (end or stop))
                           for stop, end, _ in STOPS])

        with self.voiceover(SAY[2]) as vo:
            gone = gather(self, corner_user, corner_user_l, grid, panel, bar, term_head,
                          term.lines[1], diff.box, diff.zero, diff.names, diff.first[2], diff.oh, diff.rest, cleaned)
            self.play(FadeOut(gone, shift=LEFT * 0.4), ReplacementTransform(helper, head), run_time=0.9)
            self.play(FadeIn(head_l, shift=UP * 0.1),
                      LaggedStart(*[FadeIn(c, target_position=head.get_center(), scale=0.4) for c in made],
                                  lag_ratio=0.08), run_time=1.1)
            vo.wait_until("It wrote the toolkit")
            self.play(emphasize(made[0], run_time=0.7), Create(rib.axis.line), FadeIn(rib.days), FadeIn(src2),
                      run_time=0.9)
            vo.wait_until("and made all but two")
            self.play(LaggedStart(*[Create(t) for t in rib.ticks], lag_ratio=0.04), run_time=2.0)
            self.play(Circumscribe(rib.user_ticks, color=S.WHITE, buff=0.12, run_time=0.8))
            vo.wait_until("the project's saved versions")
            self.play(FadeIn(commit_gloss, shift=DOWN * 0.1), GrowArrow(gloss_arrow), run_time=0.7)
            self.play(GrowFromCenter(burst), FadeIn(burst_l, shift=DOWN * 0.1),
                      LaggedStart(*[FadeIn(w, scale=0.3) for w in rib.wip], lag_ratio=0.05),
                      FadeIn(wip_key), run_time=0.9)
            vo.wait_until("Over four days")
            self.play(LaggedStart(*[FadeIn(b) for b in rib.bands], lag_ratio=0.3), run_time=1.8)
            self.play(FadeIn(stop_key, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and each time picked up")
            self.play(LaggedStart(*[Indicate(m, color=S.WHITE, scale_factor=1.6) for m in resumed], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(n, shift=UP * 0.15) for n in nudges], lag_ratio=0.4), run_time=1.4)
            self.play(FadeIn(footer, shift=UP * 0.1), run_time=0.6)

        # ---------------------------------------------------------- how long, and what it cost
        up_y = AXIS_Y + RISE
        privacy = speed_bar(x_of, up_y, PRIVACY, up_y - 1.25, "privacy video: request 15:28 → final cut 21:29",
                            "about 6 hours", "(24 min of video, plus the paper library and the toolkit)")
        ttt = speed_bar(x_of, up_y, TICTACTOE, up_y - 2.35, "tic-tac-toe: request 21:53 → final cut 01:00",
                        "about 3 hours", "(12 min 37 s of video)")
        src3 = source_caption("times: git and the request log (UTC) · lengths: ffprobe")
        src4 = source_caption("cost: the session's own cost counter")
        card = cost_card()
        card.move_to([0, -1.95, 0])
        card.number.set_value(0)
        pins = VGroup(*[request_pin(x_of, up_y, n, t) for n, t in REQUESTS])
        pins_l = label("requests", 22, USER).next_to(pins[0][2], LEFT, buff=0.3)

        with self.voiceover(SAY[3]) as vo:
            done = gather(self, head, head_l, made, commit_gloss, gloss_arrow, burst, burst_l, wip_key, stop_key,
                          nudges, footer, src2)
            rib = gather(self, rib)
            # the labels leave first, so the rising ribbon never runs through them
            self.play(LaggedStart(FadeOut(done), rib.animate.shift(UP * RISE), lag_ratio=0.45), run_time=1.3)
            for sb, phrase in ((privacy, "the privacy video took"), (ttt, "and tic-tac-toe just")):
                vo.wait_until(phrase)
                self.play(Create(sb.drops), FadeIn(sb.dot, scale=0.5), run_time=0.4)
                self.play(GrowFromEdge(sb.bar, LEFT), FadeIn(sb.cap), FadeIn(sb.text, shift=LEFT * 0.15),
                          *([FadeIn(src3)] if sb is privacy else []), run_time=0.8)
                self.play(emphasize(sb.hours, run_time=0.6))
            vo.wait_until("And the cost on screen")
            bars = gather(self, privacy, ttt)
            self.play(FadeOut(bars), *dim(rib, opacity=0.4), FadeTransform(src3, src4), run_time=0.6)
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.6)
            self.play(ChangeDecimalToValue(card.number, LIVE["cost_usd"]), run_time=1.7, rate_func=smooth)
            vo.wait_until("is for the whole session")
            self.play(Circumscribe(rib, color=S.WHITE, buff=0.12, run_time=1.0),
                      emphasize(card.label[0], run_time=1.0))
            vo.wait_until("all four requests")
            self.play(LaggedStart(FadeIn(pins_l, shift=RIGHT * 0.15), *[FadeIn(p, shift=DOWN * 0.15) for p in pins],
                                  lag_ratio=0.2),
                      emphasize(card.label[1], run_time=1.2), run_time=1.2)
            vo.wait_until("not one video")
            self.play(pulse(card, 1.03, run_time=0.6))
        card.number.clear_updaters()
        self.wait(0.6)
        fade_out_all(self)
