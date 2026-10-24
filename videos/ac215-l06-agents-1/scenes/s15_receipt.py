"""S15 · The harness: success is a receipt (Colab · Cheese Newsletter; lecture slides 36–37, then 10–12).

Beats (script.md "## S15", one voiceover block each):
0. TRACKER NL 1 → 3. The BLUE Colab frame "Cheese Newsletter · Harness" (tag illustration). For
   step 1 (as S14): GREY menu path File › Save a copy in Drive, the GOLD key and `OPENAI_API_KEY` in
   Colab Secrets (cell 10 line 4); with the menu path, the GREY two-line caption "first open it:
   course site · Lecture 6 · Tutorial 3, / or the Cheese Newsletter link in the study guide" under
   the cell-8 chip's place (no room beside the menu path), until "In the users cell". CODE(cell-08: 3)
   `"agent-framework-core==1.18.0" \\` (subtitle "Install Microsoft Agent Framework"), the pinned
   package boxed GREEN with the tag "pinned". CODE(cell-16.redacted: 6–12) (20 pt, line 6
   wrapped before "Email is"): lines 8–9 YELLOW, tag "you and a friend"; lines 10–11 GREY, note
   "commented out"; line 6's "Email is preview-only" GREEN, underlined at "nothing is sent".
1. TRACKER NL 4. CODE(cell-25: 5, 8, 12–16, 25) folded (subtitle "Orchestrator Agent", 11 rows):
   `gpt-5.6-luna` BLUE; lines 13–15 GREEN one by one as the SAY names them (line 13 with a BLUE
   "web search" tag and the GOLD cost tag); `"max_iterations": 16` PURPLE; line 25 PURPLE bar, tag
   "one at a time" under the panel, below that bar.
2. TRACKER NL 5, tag recorded · the staff's last saved run. RECORDED(c27: 4–9) in an output box: the
   four `[tool] editor_agent` rows bracketed YELLOW "×4". CODE(cell-16.redacted: 114–116) under it
   (20 pt, wrapped): 114 GREEN bar and tag "every draft is validated", 116 YELLOW bar, GREY tag
   "errors go back as the tool's result". The chip leaves, the box grows: c27 10, 11 folded to
   `Saved HTML: … (8005 bytes). No email sent.` ("Saved HTML" underlined GREEN), then "…" and line
   30, GREY tag "saved run: 4 readers · today's list: 2".
3. LECTURE 36–37. V8: the BLUE orchestrator, a BLUE "newsletter draft" card and a YELLOW gate
   SUCCESS with a receipt slot. The orchestrator says "done!", the draft is pushed against the gate:
   it stays shut. "Python ignores its words": the picture moves up, the bubble dims, CODE(cell-18:
   118–120, 123–124) folded (subtitle "Business Logic", 9 rows, 20 pt) comes in; `reply` and
   `{reply}` boxed GREY, note "the model's words appear only inside the error" after line 120.
   Badges 1, 2 after the conditions on lines 119 and 123, which get YELLOW outlines as the SAY asks
   (the receipt token "receipt · send_email", then the file glyph "on disk?", come in at the top
   right); the raises on 120 and 124 underlined RED, tags "no receipt → error", "file missing →
   error" (outlines and underlines, not bars: the 20 pt rows leave no room for the note between
   bars). The GREEN receipt token (c27 line 35's path, folded) drops into the slot, the file glyph
   turns GREEN "on disk ✓", the gate turns GREEN and opens, the draft passes.
4. TRACKER NL 6. The editor's GREY prompt card left of the open gate. CODE(cell-22: 16) (subtitle
   "Editor Agent", plain text: it is prose in a string): GREY bar, "embedded URLs" YELLOW, flashes
   as a GREY sticky note "no embedded URLs" fades in on the prompt. At "The saved preview": RECORDED(c30: 26
   folded to `…Promotion URL: https://…`), the URL RED; at "because no code checks for it" the note
   drifts through the gate, unchecked, then the tag erratum · a rule that matters belongs in
   validate_newsletter; caption "a note is not a check".
5. LECTURE 10–12. Two GREY dashed concept boxes (tag concept · lecture only): "Self-RAG: relevant?
   supported? useful?", "Corrective RAG: grade the documents"; caption "don't trust: check"; a GREY
   dashed chip "Lecture 7: the harness". They fade; ▶ your turn on a static GREY card, its last line
   GOLD "web search · billed per call". Hold 2 s. Empty frame.
"""

import re

import numpy as np
from common import (
    CLOUD,
    COST,
    DATA,
    ERR,
    INK,
    NARRATION,
    TOOL,
    TURN,
    Gate,
    _with_header,
    capture,
    card_rows,
    cell_title,
    colab_frame,
    concept_box,
    concept_tag,
    cost_tag,
    erratum_tag,
    excerpt,
    grey_tag,
    key_glyph,
    lref,
    menu_path,
    model_box,
    note,
    output_box,
    receipt_token,
    saved_run_tag,
    src_panel,
    sticky_note,
    tracker,
    under,
    your_turn,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    Group,
    Indicate,
    LaggedStart,
    Polygon,
    ReplacementTransform,
    RoundedRectangle,
    SurroundingRectangle,
    VGroup,
    VMobject,
    smooth,
    squish_rate_func,
    there_and_back,
)

from explainer import style as S
from explainer.devops import box, check_mark, file_glyph, label, mono, step_badge, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S15"]
NL = "colab/cheese-newsletter/"

# ------------------------------------------------------------------ the real sources
C27 = capture("expected/colab-cheese-newsletter-c27-run-demo.txt")
C30 = capture("expected/colab-cheese-newsletter-c30-preview-1.txt")

assert excerpt(NL + "cell-08.py", 3, 3).strip() == '"agent-framework-core==1.18.0" \\'
KEY_NAME = "OPENAI_API_KEY"
assert f"userdata.get('{KEY_NAME}')" in excerpt(NL + "cell-10.py", 4, 4)
assert cell_title(NL + "cell-08.py") == "Install Microsoft Agent Framework"

_USERS = excerpt(NL + "cell-16.redacted.py", 6, 12)
assert "Email is preview-only." in excerpt(NL + "cell-16.redacted.py", 6, 6)
assert len(re.findall(r'^    \{"name": "<reader\d>"', _USERS, re.M)) == 2          # two readers kept
assert len(re.findall(r'^    # \{"name": "<reader\d>"', _USERS, re.M)) == 2        # two commented out
assert "validate_newsletter(draft" in excerpt(NL + "cell-16.redacted.py", 114, 114)
assert '{"status": "error"' in excerpt(NL + "cell-16.redacted.py", 116, 116)

assert '"gpt-5.6-luna"' in excerpt(NL + "cell-25.py", 5, 5)
assert '"max_iterations": 16' in excerpt(NL + "cell-25.py", 8, 8)
assert [s.strip() for s in excerpt(NL + "cell-25.py", 13, 15).split("\n")] == \
    ["researcher_agent,", "editor_agent,", "send_email,"]
assert '"allow_multiple_tool_calls": False' in excerpt(NL + "cell-25.py", 25, 25)

assert excerpt(NL + "cell-18.py", 119, 119).strip() == "if context.receipt is None:"
assert "{reply}" in excerpt(NL + "cell-18.py", 120, 120)
assert excerpt(NL + "cell-18.py", 123, 123).strip() == 'if not Path(receipt["path"]).is_file():'
assert "points to a file that does not exist" in excerpt(NL + "cell-18.py", 124, 124)
_REPLY_USES = [n for n in range(108, 127) if "reply" in excerpt(NL + "cell-18.py", n, n)]
assert _REPLY_USES == [118, 120], _REPLY_USES          # the reply is used only inside the error

RULE = excerpt(NL + "cell-22.py", 16, 16)
assert RULE == "Write plain text in all fields: no HTML, Markdown formatting, or embedded URLs."

# the staff's saved run (cell 27)
RUN_A = C27.at((4, 9))                                   # the first city: researcher, editor x4
assert RUN_A[1] == "  [tool] researcher_agent" and RUN_A[2:] == ["  [tool] editor_agent"] * 4
SEND = C27.line(10)
assert SEND.startswith("  [tool] send_email")
SAVED = C27.fold(11, 11, "Saved HTML: … (8005 bytes). No email sent.")
CREATED = C27.line(30)
assert CREATED == "Created 4 mock emails. No email was sent."
assert sum(1 for s in C27.lines if s.startswith("Generating newsletter for ")) == 4
RECEIPT = C27.fold(35, 35, "…/<reader1>-…html")          # the receipt's 'path' (first reader)
assert "'path': '/content/newsletter_output/<reader1>-" in C27.line(35)

# the saved preview (cell 30)
URL_ROW = C30.fold(26, 26, "…Promotion URL: https://…")

TURN_ROWS = ["Newsletter: every cell in order", "Run Demo · the two previews"]
assert excerpt(NL + "cell-27.py", 1, 1) == "# @title Run Demo"

Y_PIC = 1.4           # V8's picture row once the code panel is under it
DY_BIG = -1.4         # the picture starts lower and centred (alone on screen), then moves up
DX_BIG = 2.4


# ------------------------------------------------------------------ helpers
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


def inside(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= -6.6 and m.get_right()[0] <= 6.6, (m.get_left(), m.get_right())
        assert m.get_bottom()[1] >= -3.6 and m.get_top()[1] <= 3.6, (m.get_bottom(), m.get_top())


def apart(a, b, gap: float = 0.05):
    """Assert the bounding boxes of a and b do not overlap."""
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    assert sep, (a.get_corner(DOWN + LEFT), a.get_corner(UP + RIGHT), b.get_corner(DOWN + LEFT),
                 b.get_corner(UP + RIGHT))


def row_of(p, n: int, k: int = 0):
    """The k-th code row of file line n in a src_panel."""
    return p.code.code_lines[p.rows_of(n)[k]]


def widen(p, right: float):
    """Stretch a src_panel's background so its right edge is at `right` (room for tags inside)."""
    bg = p.code.background
    bg.stretch_to_fit_width(right - bg.get_left()[0], about_edge=LEFT)
    return p


def at_row_right(m, p, n: int, k: int = 0, pad: float = 0.22):
    """Put m at the right end of the panel, on the code row k of file line n; assert it clears the
    row's text."""
    r = row_of(p, n, k)
    place(m, right=p.code.background.get_right()[0] - pad, cy=r.get_center()[1])
    assert m.get_left()[0] > r.get_right()[0] + 0.2, (n, k, m.get_left(), r.get_right())
    return m


def row_outline(m, color: str, bx: float = 0.06, by: float = 0.014, stroke: float = 2.2):
    """An outline hugging one 20 pt code row: tight vertically, so it never touches the next row."""
    r = SurroundingRectangle(m, color=color, buff=bx, stroke_width=stroke)
    r.stretch_to_fit_height(m.height + 2 * by)
    return r.move_to(m)


def obox(rows, header, width=None):
    return output_box(rows, header=header, width=width)


def bubble(text: str = "done!", color: str = CLOUD) -> VGroup:
    """The orchestrator's BLUE speech bubble, its tail pointing down-left. .body .text"""
    t = S.text(text, 24, color, font=S.FONT_SANS, weight="BOLD")
    body = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.32, corner_radius=0.2,
                            stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    bl = body.get_corner(DOWN + LEFT)
    tail = Polygon(bl + np.array([0.25, 0.02, 0]), bl + np.array([0.55, 0.02, 0]),
                   bl + np.array([0.05, -0.3, 0]), stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    t.move_to(body)
    g = VGroup(tail, body, t)
    g.body, g.text = body, t
    return g


def draft_card(w: float = 2.2, h: float = 0.95) -> VGroup:
    """The newsletter draft (the editor model wrote it: BLUE), a title and two text bars."""
    fr = box(w, h, CLOUD, fill=S.BG, fill_opacity=0.95, radius=0.1, stroke=2.5)
    t = label("newsletter draft", 20, INK)
    bars = VGroup(*[RoundedRectangle(width=w * f, height=0.07, corner_radius=0.035, stroke_width=0)
                    .set_fill(S.GREY, 0.8) for f in (0.7, 0.5)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    body = VGroup(t, bars).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(fr)
    return VGroup(fr, body)


def prompt_card(w: float = 2.7, h: float = 1.15) -> VGroup:
    """The editor agent's instructions as a GREY card. .frame"""
    fr = box(w, h, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.12)
    t = label("editor prompt", 20, INK)
    bars = VGroup(*[RoundedRectangle(width=w * f, height=0.07, corner_radius=0.035, stroke_width=0)
                    .set_fill(S.GREY, 0.7) for f in (0.75, 0.6, 0.7)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    body = VGroup(t, bars).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(fr).align_to(fr, LEFT) \
        .shift(RIGHT * 0.25)
    g = VGroup(fr, body)
    g.frame = fr
    return g


def right_bracket(mobs, text: str, color: str = TURN, x: float | None = None) -> VGroup:
    """A bracket on the right of `mobs` with `text` after it. .line .text"""
    g = VGroup(*mobs)
    top, bot = g.get_top()[1] + 0.03, g.get_bottom()[1] - 0.03
    x = g.get_right()[0] + 0.25 if x is None else x
    ln = VMobject(stroke_color=color, stroke_width=4)
    ln.set_points_as_corners([[x - 0.1, top, 0], [x, top, 0], [x, bot, 0], [x - 0.1, bot, 0]])
    t = S.text(text, 24, color, font=S.FONT_SANS, weight="BOLD")
    t.next_to(ln, RIGHT, buff=0.15)
    out = VGroup(ln, t)
    out.line, out.text = ln, t
    return out


def mixed(parts, size: float = 20, color: str = INK) -> VGroup:
    """One card row mixing serif and mono: parts = ["serif", "`mono`", …]."""
    mobs = [mono(p[1:-1], size, color) if p.startswith("`") else label(p, size, color) for p in parts]
    return VGroup(*mobs).arrange(RIGHT, buff=0.12)


def your_card(rows) -> VGroup:
    """turn_card's look for rows that mix serif and mono (card_rows + the YELLOW ▶ tag on the
    top-right corner), as in S14."""
    c = card_rows(rows, buff=0.16)
    fr = c.frame
    tall = box(fr.width, fr.height + 0.14, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    tall.move_to(fr).align_to(fr, DOWN)
    c.remove(fr)
    c.add_to_back(tall)
    c.frame = tall
    tg = your_turn().move_to(c.frame.get_corner(UP + RIGHT)).shift(LEFT * 1.0)
    c.add(tg)
    c.tag = tg
    return c


class Receipt(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)

        # ============================================================ 0 · the notebook; the USERS cell
        tr = tracker("NL", 1)                 # step 1 lit from the start (an empty caption sits at ORIGIN)
        cf = colab_frame("Cheese Newsletter · Harness", top=2.55)   # the tab clears the tracker caption
        mp = menu_path(["File", "Save a copy in Drive"])          # step 1: copy it, add the key
        place(mp, left=-6.0, cy=1.9)
        keyrow = VGroup(key_glyph(0.3), mono(KEY_NAME, 22, INK), note("in Colab Secrets", size=22))
        keyrow.arrange(RIGHT, buff=0.2)
        place(keyrow, left=mp.get_right()[0] + 0.7, cy=1.9)
        p08 = src_panel(NL + "cell-08.py", 3, subtitle=True)
        place(p08, left=-6.0, top=mp.get_bottom()[1] - 0.15)
        pin_box = SurroundingRectangle(p08.span(3, '"agent-framework-core==1.18.0"'), color=DATA, buff=0.06,
                                       stroke_width=3)
        pinned = tag("pinned", DATA)
        place(pinned, left=p08.code.background.get_right()[0] + 0.3, cy=row_of(p08, 3).get_center()[1])
        # where the original notebook is, as S02 and S14 say it: the course site (Lecture 6 · Tutorial 3,
        # Colab link, tutorials_demo.md "Tutorial 3: Cheese Newsletter - Harness") and the study guide's
        # Cheese Newsletter checklist link the same Colab. Ed itself was never opened, so it is not named.
        # No room beside the menu path (the key row fills it): under the chip, where p16 goes later; it
        # leaves at "In the users cell", just before p16 comes in (a crossfade muddled the two).
        where = VGroup(label("first open it: course site · Lecture 6 · Tutorial 3,", 20, S.GREY),
                       label("or the Cheese Newsletter link in the study guide", 20, S.GREY))
        where.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        place(where, left=-6.0, top=p08.get_bottom()[1] - 0.3)
        p16 = src_panel(NL + "cell-16.redacted.py", 6, 12, size=20, wrap={6: ["Email is"]})
        _with_header(p16, "Cheese Newsletter · cell 16 · lines 6–12",
                     subtitle=cell_title(NL + "cell-16.redacted.py"))
        place(p16, left=-6.15, top=p08.get_bottom()[1] - 0.15)
        bars_you = VGroup(p16.bar(8, TURN, 0.2), p16.bar(9, TURN, 0.2))
        bars_off = VGroup(p16.bar(10, S.GREY, 0.22), p16.bar(11, S.GREY, 0.22))
        you = tag("you and a friend", TURN)
        at_row_right(you, p16, 7)
        you.shift(UP * 0.14)                   # clear of line 8's text and YELLOW bar below it
        off = note("commented out", size=22)
        at_row_right(off, p16, 12)
        preview = p16.span(6, "Email is preview-only")
        ul_preview = under(preview, DATA, stroke=3)
        inside(cf, mp, keyrow, p08, pinned, p16, where)
        apart(where, p08, 0.2)
        apart(where, pinned, 0.2)
        apart(where, mp, 0.2)
        assert keyrow.get_right()[0] < cf.frame.get_right()[0] - 0.3
        assert mp.get_top()[1] < cf.title.get_bottom()[1] - 0.1
        assert keyrow.get_top()[1] < cf.title.get_bottom()[1] - 0.1
        apart(tr, cf.title, 0.1)               # the caption's descenders stay off the tab's top border
        apart(you, row_of(p16, 8), 0.04)
        apart(you, bars_you[0], 0.02)          # the tag's border stays off line 8's bar
        apart(you, row_of(p16, 6, 1), 0.1)
        apart(off, row_of(p16, 11), 0.04)
        assert pinned.get_right()[0] < cf.tag.get_right()[0]
        assert p16.get_bottom()[1] > cf.frame.get_bottom()[1] + 0.15, p16.get_bottom()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(cf), run_time=0.8)
            self.play(FadeIn(mp, shift=DOWN * 0.1), FadeIn(where, shift=LEFT * 0.1), run_time=0.5)
            self.play(mp.light(1), FadeIn(keyrow, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("with Microsoft's Agent Framework")
            self.play(tr.goto(2), FadeIn(p08, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("pinned")
            self.play(Create(pin_box), FadeIn(pinned, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("In the users cell")
            self.play(tr.goto(3), FadeOut(where), run_time=0.4)   # gone before p16 takes its place
            self.play(FadeIn(p16, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("put in yourself and a friend")
            self.play(FadeIn(bars_you), FadeIn(you, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("and keep two entries")
            self.play(FadeIn(bars_off), FadeIn(off, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Email is preview only")
            self.play(preview.animate.set_color(DATA), run_time=0.5)
            vo.wait_until("nothing is sent")
            self.play(Create(ul_preview), run_time=0.5)

        # ============================================================ 1 · the orchestrator: three tools, 16 iterations
        p25 = src_panel(NL + "cell-25.py", [5, 8, (12, 16), 25], subtitle=True)
        place(p25, left=-6.0, top=2.15)
        model = p25.span(5, '"gpt-5.6-luna"')
        tool_bars = [p25.bar(n, DATA, 0.2) for n in (13, 14, 15)]
        web = tag("web search", CLOUD)
        place(web, left=row_of(p25, 13).get_right()[0] + 0.5, cy=row_of(p25, 13).get_center()[1])
        paid = cost_tag()
        place(paid, left=web.get_right()[0] + 0.3, cy=web.get_center()[1])
        iters = p25.span(8, '"max_iterations": 16')
        iters_box = SurroundingRectangle(iters, color=TOOL, buff=0.06, stroke_width=3)
        bar25 = p25.bar(25, TOOL, 0.2)
        one = tag("one at a time", TOOL)
        # under the panel, right below line 25's bar: the rows are too close for a tag between them
        # (on the '…' row it covered the top of line 25's "False")
        place(one, right=p25.code.background.get_right()[0] - 0.22, top=p25.code.background.get_bottom()[1] - 0.1)
        assert one.get_bottom()[1] > cf.frame.get_bottom()[1] + 0.2, one.get_bottom()
        inside(p25, web, paid, one)
        assert paid.get_right()[0] < p25.code.background.get_right()[0] - 0.1
        assert p25.get_bottom()[1] > cf.frame.get_bottom()[1] + 0.15, p25.get_bottom()
        assert p25.get_top()[1] < cf.title.get_bottom()[1] - 0.1, p25.get_top()
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in (mp, keyrow, p08, pin_box, pinned, p16, bars_you, bars_off, you,
                                             off, ul_preview)], tr.goto(4), run_time=0.6)
            self.play(FadeIn(p25, shift=UP * 0.15), run_time=0.6)
            self.play(model.animate.set_color(CLOUD), run_time=0.5)
            vo.wait_until("a researcher with web search")
            self.play(FadeIn(tool_bars[0]), FadeIn(web, shift=LEFT * 0.1), run_time=0.5)
            self.play(FadeIn(paid, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("an editor")
            self.play(FadeIn(tool_bars[1]), run_time=0.4)
            vo.wait_until("and send email")
            self.play(FadeIn(tool_bars[2]), run_time=0.4)
            vo.wait_until("At most 16 iterations")
            self.play(iters.animate.set_color(TOOL), Create(iters_box), run_time=0.6)
            vo.wait_until("one tool call at a time")
            self.play(FadeIn(bar25), FadeIn(one, shift=LEFT * 0.1), run_time=0.6)

        # ============================================================ 2 · the staff's saved run
        saved = saved_run_tag()
        saved.move_to([cf.tag.get_left()[0] - 0.3 - saved.width / 2, cf.frame.get_top()[1], 0])
        assert saved.get_left()[0] > cf.title.get_right()[0] + 0.3
        rows_c = RUN_A + [SEND, SAVED, "…", CREATED]
        head = "Run Demo · cell 27 · saved output (folded)"
        box_c = obox(rows_c, head)
        w_box = box_c.frame.width
        box_a = obox(RUN_A, head, width=w_box)
        box_b = obox(RUN_A + [SEND, SAVED], head, width=w_box)
        for b in (box_a, box_b, box_c):
            place(b, left=-6.0, top=2.18)
        for i in range(len(RUN_A)):
            assert np.allclose(box_a.rows[i].get_center(), box_c.rows[i].get_center(), atol=1e-3)
        x4 = right_bracket(box_a.rows[2:6], "×4", TURN)
        p16b = src_panel(NL + "cell-16.redacted.py", 114, 116, size=20, wrap=True)
        _with_header(p16b, "Cheese Newsletter · cell 16 · lines 114–116",
                     subtitle=cell_title(NL + "cell-16.redacted.py"))
        place(p16b, left=-6.0, top=box_a.get_bottom()[1] - 0.12)
        widen(p16b, 6.15)
        bar114 = p16b.bar(114, DATA, 0.2)
        bar116 = p16b.bar(116, TURN, 0.15)
        n114 = tag("every draft is validated", DATA)
        at_row_right(n114, p16b, 114, 1)
        n116 = tag("errors go back as the tool's result", S.GREY)
        at_row_right(n116, p16b, 116, 1)
        n116.shift(DOWN * 0.1)                 # off the bottoms of line 116's first row ("str(exc),")
        apart(n116, row_of(p16b, 116, 0), 0.04)
        assert n116.get_bottom()[1] > p16b.code.background.get_bottom()[1] + 0.06, n116.get_bottom()
        ul_saved = under(substring(box_b.rows[7], "Saved HTML:"), DATA, stroke=3)
        four = grey_tag("saved run: 4 readers · today's list: 2")
        place(four, left=box_c.frame.get_left()[0] + 0.2, top=box_c.frame.get_bottom()[1] - 0.2)
        inside(saved, box_c, x4, p16b, four)
        assert x4.get_right()[0] < box_a.frame.get_right()[0] - 0.1
        assert p16b.get_bottom()[1] > cf.frame.get_bottom()[1] + 0.1, p16b.get_bottom()
        assert box_c.get_bottom()[1] > cf.frame.get_bottom()[1] + 0.15
        assert box_c.get_top()[1] < cf.title.get_bottom()[1] - 0.1, box_c.get_top()
        assert four.get_right()[0] < cf.frame.get_right()[0] - 0.15
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in (p25, model, iters_box, bar25, one, web, paid, *tool_bars)],
                      tr.goto(5), run_time=0.6)
            self.play(FadeIn(saved), FadeIn(box_a.frame), FadeIn(box_a.rule), FadeIn(box_a.header),
                      FadeIn(box_a.rows[0]), FadeIn(box_a.rows[1]), run_time=0.7)
            vo.wait_until("the first city took four editor calls")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in box_a.rows[2:6]], lag_ratio=0.5),
                      run_time=1.3)
            self.play(Create(x4.line), FadeIn(x4.text, scale=1.3), run_time=0.5)
            vo.wait_until("the code validates every draft")
            self.play(FadeIn(p16b, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(bar114), FadeIn(n114, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("and hands any errors back")
            self.play(FadeIn(bar116), FadeIn(n116, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Then send email wrote the HTML")
            self.play(FadeOut(p16b), FadeOut(bar114), FadeOut(bar116), FadeOut(n114), FadeOut(n116),
                      run_time=0.4)
            self.play(ReplacementTransform(box_a.frame, box_b.frame), ReplacementTransform(box_a.rule, box_b.rule),
                      ReplacementTransform(box_a.header, box_b.header),
                      *[ReplacementTransform(box_a.rows[i], box_b.rows[i]) for i in range(6)], run_time=0.5)
            self.play(LaggedStart(FadeIn(box_b.rows[6], shift=RIGHT * 0.1), FadeIn(box_b.rows[7], shift=RIGHT * 0.1),
                                  lag_ratio=0.5), run_time=0.8)
            self.play(Create(ul_saved), run_time=0.4)
            vo.wait_until("That run had four readers")
            self.play(ReplacementTransform(box_b.frame, box_c.frame), ReplacementTransform(box_b.rule, box_c.rule),
                      ReplacementTransform(box_b.header, box_c.header),
                      *[ReplacementTransform(box_b.rows[i], box_c.rows[i]) for i in range(8)], run_time=0.5)
            self.play(FadeIn(box_c.rows[8]), FadeIn(box_c.rows[9], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("today's list makes two")
            self.play(FadeIn(four, shift=LEFT * 0.1), run_time=0.5)

        # ============================================================ 3 · V8: success is a receipt
        lr = lref("36–37")
        gate = Gate("SUCCESS", TURN, gate_w=1.3, gate_h=1.5, slot=True)
        posts = VGroup(gate.lpost, gate.rpost)
        gate.shift(np.array([-0.35, Y_PIC, 0]) - posts.get_center())
        orch = model_box("orchestrator", w=1.95, h=0.75)
        orch.move_to([-5.4, Y_PIC, 0])
        draft = draft_card()
        push = 0.85
        draft.move_to([gate.lpost.get_center()[0] - 0.1 - draft.width / 2 - push, Y_PIC, 0])
        bub = bubble("done!")
        place(bub, left=orch.frame.get_right()[0] - 0.55, bottom=orch.frame.get_top()[1] + 0.08)
        tok = receipt_token(RECEIPT)
        tok.move_to([2.45, Y_PIC, 0])
        tok_lab = note("receipt · send_email", size=22)
        place(tok_lab, left=tok.get_left()[0] + 0.1, bottom=tok.get_top()[1] + 0.08)
        fglyph = file_glyph(0.5, S.GREY)
        on_disk = label("on disk?", 22, S.GREY)
        fgrp = VGroup(fglyph, on_disk).arrange(RIGHT, buff=0.18)
        place(fgrp, right=6.05, cy=Y_PIC)
        on_disk_ok = label("on disk", 22, DATA).move_to(on_disk, aligned_edge=LEFT)
        tick = check_mark(0.32, DATA).next_to(on_disk_ok, RIGHT, buff=0.15)
        pic = VGroup(orch, draft, gate, bub)
        inside(pic, tok, tok_lab, fgrp, tick, on_disk_ok)
        apart(orch, draft, 0.2)
        apart(tok, fgrp, 0.2)
        apart(VGroup(tok, tok_lab), gate, 0.2)
        assert bub.get_top()[1] < 2.85 and gate.caption.get_top()[1] < 2.85
        apart(bub, tr, 0.1)
        # the code panel under the picture
        p18 = src_panel(NL + "cell-18.py", [(118, 120), (123, 124)], size=20, wrap=True)
        _with_header(p18, "Cheese Newsletter · cell 18 · lines 118–124 (folded)",
                     subtitle=cell_title(NL + "cell-18.py"))
        place(p18, left=-6.55, bottom=-3.45)
        widen(p18, 6.57)
        assert p18.get_top()[1] < min(m.get_bottom()[1] for m in (orch, draft, gate, tok, fgrp)) - 0.1
        reply = p18.span(120, "{reply}")
        reply_var = p18.span(118, "reply")
        reply_box = VGroup(SurroundingRectangle(reply_var, color=S.GREY, buff=0.05, stroke_width=2.5),
                           SurroundingRectangle(reply, color=S.GREY, buff=0.05, stroke_width=2.5))
        words = note("the model's words appear only inside the error", size=20)
        place(words, left=row_of(p18, 120, 1).get_right()[0] + 0.25, cy=row_of(p18, 120, 1).get_center()[1])
        assert words.get_right()[0] < p18.code.background.get_right()[0] - 0.08, words.get_right()
        apart(words, row_of(p18, 120, 0), 0.03)
        apart(words, row_of(p18, 123), 0.03)
        badges = VGroup()
        for k, n in enumerate((119, 123)):
            r = row_of(p18, n)
            b = step_badge(k + 1, TURN, size=20, radius=0.17)
            b.next_to(r, RIGHT, buff=0.3)              # right after the condition's colon
            badges.add(b)
        # outlines and underlines, not bars: the 20 pt rows leave no room for a note between bars
        bar119 = row_outline(row_of(p18, 119), TURN)
        bar123 = row_outline(row_of(p18, 123), TURN)
        for n, ol in ((119, bar119), (123, bar123)):     # the outline stays off the rows above and below
            k = p18.rows_of(n)[0]
            assert ol.get_bottom()[1] > p18.code.code_lines[k + 1].get_top()[1] + 0.01, n
            assert ol.get_top()[1] < p18.code.code_lines[k - 1].get_bottom()[1] - 0.01, n
        raise120 = under(p18.span(120, "raise RuntimeError"), ERR, stroke=3, buff=0.04)
        raise124 = under(p18.span(124, "raise RuntimeError"), ERR, stroke=3, buff=0.04)
        apart(words, bar123, 0.02)
        no_rec = tag("no receipt → error", ERR)
        at_row_right(no_rec, p18, 119)
        no_file = tag("file missing → error", ERR)
        at_row_right(no_file, p18, 123)
        inside(p18, words, no_rec, no_file)
        apart(badges[0], no_rec, 0.2)
        apart(badges[1], no_file, 0.2)
        apart(words, no_rec, 0.05)
        apart(words, no_file, 0.05)
        slot = gate.slot
        # after the gate opens, the draft passes: its left edge well clear of the slot on the right post
        pass_dx = (slot.get_right()[0] + 0.35) - (draft.get_left()[0] + push)
        assert draft.get_right()[0] + push + pass_dx < fgrp.get_left()[0] - 0.3
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in (cf, saved, box_c, ul_saved, x4, four)], FadeIn(lr), run_time=0.6)
            pic.shift(UP * DY_BIG + RIGHT * DX_BIG)
            self.play(FadeIn(orch, shift=RIGHT * 0.15), FadeIn(draft, shift=RIGHT * 0.15), FadeIn(gate),
                      run_time=0.7)
            vo.wait_until("When the orchestrator stops")
            self.play(FadeIn(bub, scale=0.6, target_position=orch.get_top()), run_time=0.4)
            self.play(draft.animate.shift(RIGHT * push), run_time=0.7)
            self.play(Indicate(gate.bar, color=TURN, scale_factor=1.06), run_time=0.5)
            vo.wait_until("Python ignores its words")
            self.play(VGroup(orch, draft, gate).animate.shift(DOWN * DY_BIG + LEFT * DX_BIG),
                      bub.animate.shift(DOWN * DY_BIG + LEFT * DX_BIG).set_opacity(0.35), run_time=0.7)
            self.play(FadeIn(p18, shift=UP * 0.15), run_time=0.5)
            self.play(Create(reply_box), FadeIn(words, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("and checks two things")
            self.play(LaggedStart(*[FadeIn(b, scale=1.4) for b in badges], lag_ratio=0.5), run_time=0.7)
            vo.wait_until("is there a receipt from send email")
            self.play(Create(bar119), FadeIn(tok, shift=LEFT * 0.2), FadeIn(tok_lab, shift=LEFT * 0.2),
                      run_time=0.6)
            vo.wait_until("and is that file on disk")
            self.play(Create(bar123), FadeIn(fgrp, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("If not, the run fails")
            self.play(Create(raise120), Create(raise124), FadeIn(no_rec, shift=LEFT * 0.1),
                      FadeIn(no_file, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("success is a receipt")
            self.play(FadeOut(tok_lab), tok.animate.move_to(slot).scale(0.12).set_opacity(0),
                      LaggedStart(slot.animate.set_stroke(DATA, 3).set_fill(DATA, 0.6),
                                  # "on disk?" out, then "on disk" and the tick in ("?" and the
                                  # tick shared a place; the squeezed cross-fade read both)
                                  AnimationGroup(fglyph.animate.set_color(DATA),
                                                 FadeOut(on_disk, rate_func=squish_rate_func(smooth, 0.0, 0.45)),
                                                 FadeIn(on_disk_ok, rate_func=squish_rate_func(smooth, 0.55, 1.0)),
                                                 Create(tick, rate_func=squish_rate_func(smooth, 0.55, 1.0))),
                                  lag_ratio=0.6), run_time=0.8)
            self.remove(tok)
            fgrp.remove(on_disk)            # replaced by on_disk_ok: never bring "on disk?" back in a fade
            gate.bar.set_color(DATA)
            self.play(gate.open(run_time=0.4), gate.caption.animate.set_color(DATA), run_time=0.4)
            self.play(draft.animate.shift(RIGHT * pass_dx), run_time=0.6)

        # ============================================================ 4 · a note is not a check
        pcard = prompt_card()
        pcard.move_to([-4.6, Y_PIC, 0])
        p22 = src_panel(NL + "cell-22.py", 16, wrap=True, subtitle=True, language="text")   # prose in a string
        _with_header(p22, "Cheese Newsletter · cell 22 · line 16", subtitle=cell_title(NL + "cell-22.py"))
        place(p22, left=-6.3, top=0.45)
        rule_bar = p22.bar(16, S.GREY, 0.2)
        urls = p22.span(16, "embedded URLs")
        sticky = sticky_note("no embedded URLs")
        sticky.rotate(-0.06)
        sticky.move_to(pcard.frame.get_corner(DOWN + RIGHT) + np.array([-0.35, 0.2, 0]))
        drift_to = np.array([2.6, Y_PIC + 0.05, 0])
        assert sticky.get_left()[0] + (drift_to[0] - sticky.get_center()[0]) > gate.rpost.get_center()[0] + 0.2
        prev = obox([URL_ROW], "Cheese Newsletter · cell 30 · saved preview (excerpt)")
        place(prev, left=-6.15, top=p22.get_bottom()[1] - 0.35)
        prev_tag = saved_run_tag()
        place(prev_tag, left=prev.header.get_right()[0] + 0.3, cy=prev.header.get_center()[1])
        url = substring(prev.rows[0], "https://")
        err = erratum_tag("a rule that matters belongs in validate_newsletter")
        place(err, left=prev.frame.get_left()[0], top=prev.frame.get_bottom()[1] - 0.25)
        cap = label("a note is not a check", 26, INK, t2c={"note": S.GREY, "check": DATA})
        place(cap, left=prev.frame.get_right()[0] + 0.6, cy=prev.frame.get_center()[1])
        inside(pcard, sticky, p22, prev, prev_tag, err, cap)
        apart(pcard, gate, 0.3)
        apart(prev_tag, p22, 0.05)
        apart(sticky, p22, 0.1)                # on the prompt card, clear of the panel header under it
        apart(cap, err, 0.1)
        assert p22.get_top()[1] < gate.get_bottom()[1] - 0.1, (p22.get_top(), gate.get_bottom())
        with self.voiceover(SAY[4]) as vo:
            self.play(*[FadeOut(m) for m in (p18, reply_box, words, badges, bar119, bar123, raise120, raise124,
                                             no_rec, no_file, orch, bub, draft, fgrp, on_disk_ok, tick)],
                      tr.goto(6), run_time=0.6)
            self.play(FadeIn(pcard, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("The editor is told")
            self.play(FadeIn(p22, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(rule_bar), run_time=0.4)
            vo.wait_until("no embedded URLs")
            self.play(urls.animate.set_color(TURN), run_time=0.4)
            # the rule flashes in the code and the note fades in on the prompt card (a flying copy
            # crossed the panel's header)
            self.play(Indicate(urls, color=TURN, scale_factor=1.1, rate_func=squish_rate_func(there_and_back, 0.0, 0.5)),
                      FadeIn(sticky, rate_func=squish_rate_func(smooth, 0.3, 1.0)), run_time=0.9)
            vo.wait_until("The saved preview has one anyway")
            self.play(FadeIn(prev, shift=UP * 0.1), FadeIn(prev_tag), run_time=0.5)
            self.play(url.animate.set_color(ERR), run_time=0.4)
            vo.wait_until("because no code checks for it")
            self.play(sticky.animate.move_to(drift_to).set_opacity(0.6), run_time=1.0)   # through, unchecked
            self.play(FadeIn(err, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("a note is not a check")
            self.play(FadeIn(cap, shift=LEFT * 0.1), run_time=0.5)

        # ============================================================ 5 · check, don't trust; ▶
        ctag = concept_tag()
        self_rag = concept_box("Self-RAG: relevant? supported? useful?", size=24)
        crag = concept_box("Corrective RAG: grade the documents", size=24)
        VGroup(self_rag, crag).arrange(DOWN, buff=0.45)
        place(ctag, cx=0, bottom=self_rag.get_top()[1] + 0.3)
        motto = label("don't trust: check", 30, INK, t2c={"check": DATA})
        place(motto, cx=0, top=crag.get_bottom()[1] - 0.5)
        l7 = concept_box("Lecture 7: the harness", size=24)
        place(l7, cx=0, top=motto.get_bottom()[1] - 0.55)
        VGroup(ctag, self_rag, crag, motto, l7).move_to([0, 0.1, 0])
        your = your_card([
            TURN_ROWS[0],
            mixed(["edit", "`USERS`", "(keep 2: the second preview shows reader 2)"]),
            TURN_ROWS[1],
            ("web search · billed per call", COST),
        ])
        your.move_to([0, -0.2, 0])
        inside(ctag, self_rag, crag, motto, l7, your)
        apart(ctag, tr, 0.1)
        with self.voiceover(SAY[5]) as vo:
            self.play(*[FadeOut(m) for m in (pcard, sticky, gate, p22, rule_bar, prev, prev_tag, err, cap, lr)],
                      run_time=0.6)
            lr2 = lref("10–12")
            self.play(FadeIn(lr2), FadeIn(ctag), run_time=0.4)
            vo.wait_until("Self-RAG")
            self.play(FadeIn(self_rag, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("and Corrective RAG")
            self.play(FadeIn(crag, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("grade their retrieval")
            self.play(Indicate(self_rag.text, color=INK, scale_factor=1.04),
                      Indicate(crag.text, color=INK, scale_factor=1.04), run_time=0.8)
            vo.wait_until("don't trust, check")
            self.play(FadeIn(motto, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Next lecture calls this outer layer")
            self.play(FadeIn(l7, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Web search is billed per call")
            self.play(*[FadeOut(m) for m in (ctag, self_rag, crag, motto, l7, lr2)], run_time=0.5)
            self.play(FadeIn(your, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("pause, and run the demo")
            self.play(your.tag.animate(rate_func=there_and_back).scale(1.15), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
