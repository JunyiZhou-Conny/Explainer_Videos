"""S14 · The harness: only a human says yes (Colab · Travel Planner; lecture slides 20–22, then 36–37).

Beats (script.md "## S14", one voiceover block each):
0. TRACKER TP 1 → 3. The BLUE Colab frame "Travel Planner" (tag illustration). LECTURE 20–22: the
   GREY trip-request card of the hook (our words, slide 20) writes in at the bottom. "Copy it, add
   your key": GREY menu path File › Save a copy in Drive, the GOLD key and `OPENAI_API_KEY` (cell 10
   line 4). CODE(cell-08: 2) `%pip install -q "openai-agents==0.3.2"`, the pinned package boxed
   GREEN with the tag "pinned". "Paris shrinks": the request card becomes a small GREY box "mock
   catalog" (3 cities · 6 hotels · prices in cents / 5 search tools + finalize, counted from cells
   12, 14 and 21:28–34; no code chips), its rows written as named; a GREY excerpt chip of
   RECORDED(c27: 5) "Nothing has been booked."
1. TRACKER TP 4 → 6; the lecture tag leaves. Tags on the frame: recorded · the staff's last saved
   run, and GOLD "paid · every turn". One turn card at a time; each earlier card compacts into a
   chip "Turn k · <its Kind line>": Turn 1 RECORDED(c24: 3, 4 cut after "Los Angeles?", wrapped);
   Turn 2 the five `[tool]` lines (c25: 3, 31, 59, 73, 87; header "(folded)") counted 1–5 by YELLOW
   badges, then line 109 `Kind: options`; Turn 3 RECORDED(c26: 3–5, line 5 wrapped): the `[tool]
   finalize_plan` line underlined, "reply with 'yes' to approve it" YELLOW.
2. V8. The frame and chips leave; Turn 3's card becomes the GREEN plan card (c26: 7–9 + "…", the
   exact proposal, folded); the BLUE model pushes it to the YELLOW gate FINAL; the bar stops it and
   stamps it YELLOW PENDING. CODE(cell-15: 36–42) (subtitle "Finalize Plan Tool", 8 rows): line 36
   YELLOW, line 37 (the pending proposal) YELLOW, "needs_confirmation" boxed. The model pushes
   again: the same stamp.
3. The turnstile shrinks to the top right (BLUE model glyph, the GREEN card glyph with its PENDING
   stamp, the gate), the GREY human (person_icon) under it. CODE(cell-18: 55, 59–61) folded
   (subtitle "Business Logic", 8 rows, 20 pt): `prompt` PINK; `"yes"` flashes; line 61 GREEN, tag
   "pending → approved". PONDER (8 s): just before the card comes up the panel folds to lines 55
   and 61 (5 rows), so the card in the lower third covers none of it (8 rows and the card don't
   both fit under the tracker).
4. CODE(cell-18: 105–109): line 106 YELLOW with its `prompt` PINK, line 109 GREY, a GREY arrow
   "runs first". On the turnstile the model pushes twice; the PENDING stamp flashes each time.
5. TRACKER TP 7. CODE(cell-27: 2) with the GREY human beside it: `"yes"` types in. The turnstile
   moves to the middle; the stamp flips GREEN APPROVED; the bar swings up and the card passes.
   V8's calculator (BudgetTape, c27's costs_usd) builds 880 + 1,000 + 600 + 150 + 60 = 2,690 of
   6,000 row by row; RECORDED(c27: 32) `"total_usd": 2690.0` GREEN beside it. The gate leaves; the
   chip CODE(cell-27: 6) "the notebook's own test", its 2690.0 GREEN.
6. RECORDED(c27: 4–6) above the tape (the reply Python rendered): "checked" and "computed by
   Python" underlined GREEN. Then CODE(cell-18: 129–135) (11 rows): 129–131 RED "hard guardrail:
   raise"; 133–135 YELLOW "soft guardrail: warn".
7. LECTURE 36–37. Two GREY cards (our words): "instructions" with a sticky note "success criteria"
   (slide 36), "decision maker" with "guardrails" (slide 37); GREEN copies "Python's budget",
   "checked render", "approval gate" drop into a row "in code:"; the gate sits on the action tool
   `finalize_itinerary`. Cards and tag fade; TRACKER TP 8; ▶ your turn on a static GREY card, its
   last line GOLD "OpenAI calls · every turn". Hold 2 s. Empty frame.
"""

import re

import numpy as np
from common import (
    BUDGET_TOTAL,
    CLOUD,
    COST,
    DATA,
    ERR,
    INK,
    LAPTOP,
    LOOKUP,
    NARRATION,
    TURN,
    BudgetTape,
    Gate,
    _with_header,
    _wrap_line,
    capture,
    card_rows,
    colab_frame,
    cost_tag,
    excerpt,
    excerpt_chip,
    fix_chip,
    json_card,
    key_glyph,
    lref,
    menu_path,
    model_box,
    note,
    output_box,
    ponder_at,
    saved_run_tag,
    source_text,
    src_panel,
    stamp,
    sticky_note,
    tracker,
    under,
    your_turn,
)
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Create,
    CurvedArrow,
    FadeIn,
    FadeOut,
    FadeTransform,
    Group,
    Indicate,
    LaggedStart,
    ReplacementTransform,
    RoundedRectangle,
    SurroundingRectangle,
    Transform,
    Rectangle,
    VGroup,
)

from explainer import style as S
from explainer.components import person_icon
from explainer.devops import box, chip, label, mono, step_badge, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S14"]
TP = "colab/travel-planner/"

# ------------------------------------------------------------------ the real sources
C24 = capture("expected/colab-travel-planner-c24-turn1.txt")
C25 = capture("expected/colab-travel-planner-c25-turn2.txt")
C26 = capture("expected/colab-travel-planner-c26-turn3.txt")
C27 = capture("expected/colab-travel-planner-c27-turn4-yes.txt")

PIP = excerpt(TP + "cell-08.py", 2, 2)
assert PIP == '%pip install -q "openai-agents==0.3.2"', PIP
KEY_NAME = "OPENAI_API_KEY"
assert f"userdata.get('{KEY_NAME}')" in excerpt(TP + "cell-10.py", 4, 4)

# the mock catalog, counted from the cells (script: cell-12 6–18, cell-14, cell-21 28–34)
_C12 = excerpt(TP + "cell-12.py", 6, 18)
N_CITIES = len(re.findall(r'^\s+"[A-Z][\w ]+": \{"airport"', _C12, re.M))
N_HOTELS = len(re.findall(r'^\s+"[A-Z]+-[A-Z]+": \(', _C12, re.M))
assert (N_CITIES, N_HOTELS) == (3, 6), (N_CITIES, N_HOTELS)
assert '"SFO-BAY": ("San Francisco", "Bay Area Suite", 25000, True)' in _C12      # prices in cents
N_SEARCH = len(re.findall(r"^def \w+_search\(", source_text(TP + "cell-14.py"), re.M))
_C21 = excerpt(TP + "cell-21.py", 28, 34)
assert N_SEARCH == 5 and _C21.count("function_tool(") == N_SEARCH and "finalize_itinerary" in _C21
CATALOG = [f"{N_CITIES} cities", f"{N_HOTELS} hotels", "prices in cents", f"{N_SEARCH} search tools + finalize"]

BOOKED = "Nothing has been booked."
assert BOOKED in C27.line(5)

# the staff's saved run: turns 1-3
T1_KIND = C24.line(3)
T1_Q = C24.cut(4, "Los Angeles?")
assert T1_KIND == "Kind: clarification" and T1_Q.startswith("Which supported California city")
T1_ROWS = [T1_KIND] + _wrap_line(T1_Q + " …", ["or Los Angeles?"])
T2_LINES = (3, 31, 59, 73, 87)
T2_TOOLS = [C25.line(n) for n in T2_LINES]
assert all(s.startswith("  [tool] ") for s in T2_TOOLS), T2_TOOLS
assert sum(1 for s in C25.lines if s.startswith("  [tool] ")) == 5
T2_KIND = C25.line(109)
assert T2_KIND == "Kind: options"
T3_TOOL, T3_KIND = C26.line(3), C26.line(4)
assert T3_TOOL.startswith("  [tool] finalize_plan:") and T3_KIND == "Kind: clarification"
T3_ASK = "reply with 'yes' to approve it"
T3_ROWS = [T3_TOOL, T3_KIND] + _wrap_line(C26.line(5), ["and reply", "Food is", "local transport"])
assert T3_ASK in T3_ROWS[3], T3_ROWS
PLAN_ROWS = [C26.line(7), C26.line(8), C26.line(9), "  …"]
assert C26.line(6) == "{" and C26.line(19) == "}" and '"outbound_id"' in PLAN_ROWS[0]
PLAN_HEAD = "the exact proposal · cell 26 · lines 6–19 (folded)"

# turn 4
T4_ROWS = [C27.line(4)] + _wrap_line(C27.line(5), ["2 traveler(s)", "Bay Art Museum.", "Nothing has"]) + [C27.line(6)]
assert C27.line(4) == "Kind: itinerary" and "computed by Python" in C27.line(6)
TOTAL_ROW = C27.line(32)
assert TOTAL_ROW.strip() == f'"total_usd": {BUDGET_TOTAL:.1f},', TOTAL_ROW
TEST = excerpt(TP + "cell-27.py", 6, 6)
assert TEST == 'assert context.checked_plan["total_usd"] == 2690.0', TEST
assert excerpt(TP + "cell-27.py", 2, 2) == 'reply = await run_turn(agent, "yes", session, context, invoke_agent)'

# the code panels (script.md S14)
assert "if proposal != travel_context.approved_proposal:" in excerpt(TP + "cell-15.py", 36, 36)
assert '"status": "needs_confirmation",' in excerpt(TP + "cell-15.py", 39, 39)
assert excerpt(TP + "cell-18.py", 106, 106).strip() == "apply_confirmation(prompt, context)"
assert excerpt(TP + "cell-18.py", 109, 109).strip().startswith("reply = await invoke_agent(")
assert "Hard Guardrail" in excerpt(TP + "cell-18.py", 130, 130)
assert "Soft Guardrail" in excerpt(TP + "cell-18.py", 133, 133)

PONDER_Q = ("In turn 3 the model got needs_confirmation.\n"
            "Why can't it just call finalize_itinerary again\n"
            "to approve its own plan?")

# our words for slide 20 (the same request card as the hook) and slides 36-37
REQUEST = ["5 days in Paris", "flights and hotels within budget", "activities you'd enjoy",
           "replan if it rains or a flight is late"]
TURN_ROWS = ["Travel Planner: every cell in order,", "Install OpenAI Agents SDK to Turn 4",
             "the last cell, Start an interactive conversation,"]
assert excerpt(TP + "cell-08.py", 1, 1) == "# @title Install OpenAI Agents SDK"
assert excerpt(TP + "cell-27.py", 1, 1).startswith("# Turn 4:")
assert excerpt(TP + "cell-28.py", 1, 1) == "# @title Start an interactive conversation"

TOP = 2.88            # under the tracker band (its bottom is 2.97)
RIGHT_EDGE = 6.45


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


def obox(rows, header):
    """A notebook output box (RECORDED) whose wrap marks ↪ are GREY."""
    ob = output_box(rows, header=header)
    for r in ob.rows:
        if "↪" in r.text:
            substring(r, "↪").set_color(S.GREY)
    return ob


def row_of(p, n: int, k: int = 0):
    """The k-th code row of file line n in a src_panel."""
    return p.code.code_lines[p.rows_of(n)[k]]


def span_bar(p, a: int, b: int, color: str = TURN, opacity: float = 0.18):
    """One translucent bar over every code row of file lines a..b."""
    bars = VGroup(*[p.bar(n, color, opacity) for n in range(a, b + 1)])
    r = Rectangle(width=bars.width, height=bars.height, stroke_width=0).set_fill(color, opacity)
    return r.move_to(bars)


def mixed_chip(parts, color: str = S.GREY, size: float = 20) -> VGroup:
    """A chip whose text mixes serif (GREY) and mono (white): parts = ["serif", "`mono`", …]."""
    mobs = [mono(p[1:-1], size, INK) if p.startswith("`") else label(p, size, S.GREY) for p in parts]
    row = VGroup(*mobs).arrange(RIGHT, buff=0.14)
    h = mono("|", size).height + 0.24
    b = box(row.width + 0.5, h, color, fill=S.BG, fill_opacity=0.95, radius=h / 2.6)
    row.move_to(b)
    g = VGroup(b, row)
    g.box, g.text = b, row
    return g


def text_span(t, sub: str):
    """The glyphs of `sub` inside a one-line Text (spaces have no glyphs)."""
    s = t.original_text if hasattr(t, "original_text") else t.text
    i = s.find(sub)
    if i < 0:
        raise ValueError(f"{sub!r} not in {s!r}")
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def request_card() -> VGroup:
    """The hook's trip request (slide 20, our words), GREY, rows with dots. .frame .rows .dots"""
    rows = VGroup(*[label(s, 22, INK) for s in REQUEST]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    dots = VGroup(*[RoundedRectangle(width=0.1, height=0.1, corner_radius=0.05, stroke_width=0)
                    .set_fill(S.GREY, 1).next_to(r, LEFT, buff=0.2) for r in rows])
    body = VGroup(dots, rows)
    fr = box(body.width + 0.7, body.height + 0.45, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    body.move_to(fr)
    head = note("a trip request · in our words").next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
    g = VGroup(fr, body, head)
    g.frame, g.rows, g.dots, g.header = fr, rows, dots, head
    return g


def catalog_box() -> VGroup:
    """The small GREY "mock catalog" box: two rows, the first one in three parts. .frame .parts"""
    r1 = VGroup(label(CATALOG[0], 22, INK), label("·", 22, S.GREY), label(CATALOG[1], 22, INK),
                label("·", 22, S.GREY), label(CATALOG[2], 22, INK)).arrange(RIGHT, buff=0.14)
    r2 = label(CATALOG[3], 22, INK)
    rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    fr = box(rows.width + 0.6, rows.height + 0.45, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.12)
    rows.move_to(fr)
    head = note("mock catalog").next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
    g = VGroup(fr, head, rows)
    g.frame, g.header, g.parts = fr, head, [r1[0], VGroup(r1[1], r1[2], r1[3], r1[4]), r2]
    return g


def card_glyph(w: float = 2.25, h: float = 0.72) -> VGroup:
    """The plan card as a glyph (V8's mini turnstile): a GREEN card, its stamp on its face."""
    fr = box(w, h, DATA, fill=S.BG, fill_opacity=0.95, radius=0.1, stroke=2.5)
    tint = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_width=0).set_fill(DATA, 0.1)
    return VGroup(fr, tint.move_to(fr))


def model_glyph(s: float = 0.42) -> VGroup:
    return VGroup(box(s, s, CLOUD, fill_opacity=0.3, radius=0.08, stroke=3))


def gate_target(gate: Gate, k: float, center) -> Gate:
    """A copy of `gate` with its shapes scaled by k and its label kept at its own size, centred
    (posts) at `center`."""
    t = gate.copy()
    t.scale(k)
    t.caption.scale(1 / k)
    posts = VGroup(t.lpost, t.rpost)
    t.shift(np.array(center) - posts.get_center())
    t.caption.move_to([posts.get_center()[0], posts.get_top()[1] + 0.1 + t.caption.height / 2, 0])
    return t


def your_card(rows) -> VGroup:
    """turn_card's look for rows that mix serif and mono (card_rows + the YELLOW ▶ tag on the
    top-right corner), as in S02."""
    c = card_rows(rows, buff=0.14)
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


def recolor(glyphs, color: str) -> list:
    """Animations recolouring each glyph of a span on its own: animating the span group itself
    would make Manim add it to the scene and split the panel that holds the glyphs."""
    return [g.animate.set_color(color) for g in glyphs]


def flash(glyphs, color: str = INK, k: float = 1.25) -> list:
    """Indicate each glyph of a span on its own (see recolor)."""
    return [Indicate(g, color=color, scale_factor=k) for g in glyphs]


def bump(scene, mobs, back: float = 0.45, run_time: float = 0.55):
    """The pushed card backs off and hits the gate's left post again (each mobject moved on its
    own: a wrapper group would be left on the scene)."""
    scene.play(*[m.animate.shift(LEFT * back) for m in mobs], run_time=run_time * 0.45)
    scene.play(*[m.animate.shift(RIGHT * back) for m in mobs], run_time=run_time * 0.55)


class ApprovalGate(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)

        # ============================================================ 0 · the notebook; Paris shrinks
        tr = tracker("TP")
        cf = colab_frame("Travel Planner")
        lr = lref("20–22")
        req = request_card()
        place(req, left=-6.0, bottom=-3.2)
        mp = menu_path(["File", "Save a copy in Drive"])
        place(mp, left=-6.0, cy=1.95)
        keyrow = VGroup(key_glyph(0.3), mono(KEY_NAME, 22, INK), note("in Colab Secrets", size=22))
        keyrow.arrange(RIGHT, buff=0.2)
        place(keyrow, left=mp.get_right()[0] + 0.7, cy=1.95)
        p08 = src_panel(TP + "cell-08.py", 2, subtitle=True)
        place(p08, left=-6.0, top=mp.get_bottom()[1] - 0.35)
        pin_box = SurroundingRectangle(p08.span(2, '"openai-agents==0.3.2"'), color=DATA, buff=0.06,
                                       stroke_width=3)
        pinned = tag("pinned", DATA)
        place(pinned, left=p08.get_right()[0] + 0.3, cy=row_of(p08, 2).get_center()[1])
        cat = catalog_box()
        place(cat, left=-6.0, bottom=-2.9)
        booked = excerpt_chip(BOOKED, "Travel Planner · cell 27 · saved output (excerpt)", line=C27.line(5))
        place(booked, left=cat.get_right()[0] + 0.6, cy=cat.frame.get_center()[1])
        inside(req, mp, keyrow, p08, pinned, cat, booked)
        apart(keyrow, mp, 0.3)
        apart(p08, req, 0.3)
        apart(cat, booked, 0.3)
        assert keyrow.get_right()[0] < RIGHT_EDGE and booked.get_right()[0] < RIGHT_EDGE
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(cf), run_time=0.8)
            self.play(FadeIn(lr), FadeIn(req.frame), FadeIn(req.header), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(VGroup(d, r), shift=RIGHT * 0.15)
                                    for d, r in zip(req.dots, req.rows)], lag_ratio=0.4), run_time=1.4)
            vo.wait_until("Copy it")
            self.play(tr.goto(1), FadeIn(mp, shift=DOWN * 0.1), run_time=0.6)
            self.play(mp.light(1), run_time=0.4)
            vo.wait_until("add your key")
            self.play(FadeIn(keyrow, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and install its pinned agents package")
            self.play(tr.goto(2), FadeIn(p08, shift=UP * 0.15), run_time=0.6)
            self.play(Create(pin_box), FadeIn(pinned, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Paris shrinks")
            self.play(ReplacementTransform(req.frame, cat.frame), FadeOut(req.rows), FadeOut(req.dots),
                      ReplacementTransform(req.header, cat.header), run_time=1.0)
            vo.wait_until("3 cities")
            self.play(FadeIn(cat.parts[0], shift=UP * 0.1), run_time=0.4)
            vo.wait_until("6 hotels")
            self.play(FadeIn(cat.parts[1], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("5 search tools")
            self.play(tr.goto(3), FadeIn(cat.parts[2], shift=UP * 0.1), run_time=0.6)
            vo.wait_until("booking nothing")
            self.play(FadeIn(booked, shift=LEFT * 0.15), run_time=0.6)

        # ============================================================ 1 · the staff's saved run: turns 1-3
        saved = saved_run_tag()
        saved.move_to([cf.tag.get_left()[0] - 0.3 - saved.width / 2, cf.frame.get_top()[1], 0])
        paid = cost_tag("paid · every turn")
        place(paid, right=6.15, cy=2.1)
        t1 = obox(T1_ROWS, "Turn 1 · cell 24 · output")
        place(t1, left=-6.1, cy=-0.6)
        t2 = obox(T2_TOOLS + [T2_KIND], "Turn 2 · cell 25 · output (folded)")
        place(t2, left=-6.1, cy=-0.6)
        badges = VGroup(*[step_badge(i + 1, TURN, size=20, radius=0.17) for i in range(5)])
        for b, r in zip(badges, t2.rows[:5]):
            b.move_to([t2.frame.get_right()[0] + 0.35, r.strut.get_center()[1], 0])
        t3 = obox(T3_ROWS, "Turn 3 · cell 26 · output")
        place(t3, left=-6.1, cy=-0.6)
        chip1 = mixed_chip(["Turn 1 ·", f"`{T1_KIND}`"])
        place(chip1, left=-6.1, cy=2.1)
        chip2 = mixed_chip(["Turn 2 ·", f"`{T2_KIND}`"])
        place(chip2, left=chip1.get_right()[0] + 0.3, cy=2.1)
        tool_ul = under(substring(t3.rows[0], "[tool] finalize_plan"), TURN, stroke=3)
        ask = substring(t3.rows[3], T3_ASK)
        inside(saved, paid, t1, t2, badges, t3, chip1, chip2)
        apart(chip2, paid, 0.2)
        assert t3.get_bottom()[1] > cf.frame.get_bottom()[1] + 0.2
        assert badges.get_right()[0] < cf.frame.get_right()[0] - 0.1
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in (lr, mp, keyrow, p08, pin_box, pinned, cat, booked)],
                      tr.goto(4), run_time=0.6)
            self.play(FadeIn(saved), FadeIn(paid), FadeIn(t1, shift=UP * 0.15), run_time=0.7)
            self.play(Indicate(t1.rows[1], color=INK, scale_factor=1.03), run_time=0.8)
            vo.wait_until("Turn 2 runs five searches")
            self.play(tr.goto(5), ReplacementTransform(t1, chip1), run_time=0.7)
            self.play(FadeIn(t2.frame), FadeIn(t2.rule), FadeIn(t2.header), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(VGroup(t2.rows[i], badges[i]), shift=RIGHT * 0.1)
                                    for i in range(5)], lag_ratio=0.45), run_time=1.8)
            vo.wait_until("and offers options")
            self.play(FadeIn(t2.rows[5], shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("In turn 3 the user picks")
            self.play(tr.goto(6), ReplacementTransform(VGroup(t2, badges), chip2), run_time=0.7)
            self.play(FadeIn(t3, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the model calls finalize")
            self.play(Create(tool_ul), run_time=0.5)
            vo.wait_until("and the reply shows the exact plan")
            self.play(*recolor(ask, TURN), run_time=0.6)

        # ============================================================ 2 · V8: the gate stamps PENDING
        plan = json_card(PLAN_ROWS, DATA, header=PLAN_HEAD)
        gate = Gate("FINAL", TURN, gate_w=1.5, gate_h=2.0)
        gate.move_to([4.75, 0, 0])
        model = model_box("model", w=1.2, h=0.8)
        place(plan, top=TOP - 0.05)
        post_x = gate.lpost.get_center()[0]
        plan_y = plan.frame.get_center()[1]
        gate.shift(UP * (plan_y - VGroup(gate.lpost, gate.rpost).get_center()[1]))
        stop_x = post_x - 0.1 - plan.frame.width / 2           # the card's centre when it hits the post
        plan.shift(RIGHT * (stop_x - plan.frame.get_center()[0]))
        model.move_to([plan.frame.get_left()[0] - 0.12 - model.width / 2, plan_y, 0])
        walk = 1.8
        model.shift(LEFT * walk)
        plan.shift(LEFT * walk)
        inside(model, plan, gate)
        p15 = src_panel(TP + "cell-15.py", 36, 42, wrap=True, subtitle=True)
        _with_header(p15, "Travel Planner · cell 15 · lines 36–42", subtitle="Finalize Plan Tool")
        place(p15, left=-6.3, top=min(plan.frame.get_bottom()[1], gate.get_bottom()[1]) - 0.35)
        inside(p15)
        assert p15.get_bottom()[1] > -3.5, p15.get_bottom()
        bar36 = p15.bar(36, TURN, 0.18)
        bar37 = p15.bar(37, TURN, 0.18)
        nbox = SurroundingRectangle(p15.span(39, '"needs_confirmation"'), color=TURN, buff=0.06, stroke_width=3)
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in (cf, saved, paid, chip1, chip2, tool_ul)],
                      FadeTransform(t3, plan), run_time=0.9)
            self.play(FadeIn(gate), FadeIn(model, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("A finalize call from the model")
            self.play(model.animate.shift(RIGHT * walk), plan.animate.shift(RIGHT * walk), run_time=1.0)
            pend = stamp("PENDING", TURN)                      # bottom right: clear of the header and rows
            pend.move_to(plan.frame.get_corner(DOWN + RIGHT) + np.array([-pend.width / 2 - 0.25, 0, 0]))
            self.play(Indicate(gate.bar, color=TURN, scale_factor=1.05),
                      FadeIn(pend, scale=1.6), run_time=0.5)
            self.play(FadeIn(p15, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("if the plan isn't the approved one")
            self.play(FadeIn(bar36), run_time=0.5)
            vo.wait_until("the code stores it as pending")
            self.play(FadeIn(bar37), Indicate(pend, color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("and returns needs confirmation")
            self.play(Create(nbox), run_time=0.5)
            bump(self, [model, plan, pend])
            self.play(Indicate(pend, color=TURN, scale_factor=1.15), run_time=0.5)

        # ============================================================ 3 · apply_confirmation; PONDER
        p18 = src_panel(TP + "cell-18.py", [55, (59, 61)], size=20,
                        wrap={55: ["context:"], 60: ['"yes, confirm"'], 61: ["context.pending"]})
        _with_header(p18, "Travel Planner · cell 18 · lines 55–61 (folded)", subtitle="Business Logic")
        place(p18, left=-6.45, top=TOP)
        zone = p18.get_right()[0] + 0.25                     # the turnstile's zone: zone .. RIGHT_EDGE
        g_k = 0.45
        g_t = gate_target(gate, g_k, [RIGHT_EDGE - 0.42, 2.05, 0])
        bar_y = g_t.bar.get_center()[1]
        cg = card_glyph(1.8, 0.66)
        cg.move_to([g_t.lpost.get_center()[0] - 0.1 - cg.width / 2, bar_y + 0.1, 0])
        mg = model_glyph(0.38)
        mg.move_to([cg.get_left()[0] - 0.08 - mg.width / 2, cg.get_center()[1], 0])
        pend_t = stamp("PENDING", TURN, size=20).move_to(cg)
        mini = VGroup(mg, cg, pend_t, g_t)
        assert mg.get_left()[0] > zone, (mg.get_left(), zone)
        assert g_t.get_right()[0] < 6.55, g_t.get_right()
        assert g_t.caption.get_top()[1] < 3.08, g_t.caption.get_top()
        human = person_icon(LAPTOP, height=0.55)
        human.move_to([g_t.get_center()[0], 0.95, 0])
        h_lab = note("the human", size=22)
        place(h_lab, right=human.get_left()[0] - 0.2, cy=human.get_center()[1])
        apart(VGroup(human, h_lab), mini, 0.1)
        assert h_lab.get_left()[0] > p18.get_right()[0] + 0.2
        prompt55 = p18.span(55, "prompt")
        yes60 = p18.span(60, '"yes"')
        bar61 = p18.bar(61, DATA, 0.2)
        tag61 = tag("pending → approved", DATA, size=20)
        place(tag61, right=p18.code.get_right()[0] - 0.08, cy=row_of(p18, 61).get_center()[1])
        assert tag61.get_left()[0] > row_of(p18, 61).get_right()[0] + 0.2
        inside(p18, mini, human, h_lab, tag61)
        # the panel the ponder card leaves room for: lines 55 and 61 only (5 rows)
        p18b = src_panel(TP + "cell-18.py", [55, 61], size=20,
                         wrap={55: ["context:"], 61: ["context.pending"]})
        _with_header(p18b, "Travel Planner · cell 18 · lines 55–61 (folded)", subtitle="Business Logic")
        place(p18b, left=-6.45, top=TOP)
        p18b.span(55, "prompt").set_color(LOOKUP)
        bar61b = p18b.bar(61, DATA, 0.2)
        tag61b = tag61.copy()
        place(tag61b, left=row_of(p18b, 61).get_right()[0] + 0.25, cy=row_of(p18b, 61).get_center()[1])
        apart(tag61b, mini, 0.2)
        apart(tag61b, VGroup(human, h_lab), 0.2)
        assert p18b.get_bottom()[1] > 0.0, p18b.get_bottom()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(p15), FadeOut(bar36), FadeOut(bar37), FadeOut(nbox),
                      FadeTransform(plan, cg), FadeTransform(model, mg),
                      Transform(gate, g_t), Transform(pend, pend_t), run_time=1.0)
            self.add(pend)                                     # the stamp on top of the card glyph
            pend_mini = pend
            self.play(FadeIn(p18, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("apply confirmation")
            self.play(*recolor(prompt55, LOOKUP), FadeIn(human, shift=UP * 0.1), FadeIn(h_lab),
                      run_time=0.6)
            vo.wait_until("only an explicit yes")
            self.play(*flash(yes60), run_time=0.7)
            self.play(FadeIn(bar61), FadeIn(tag61, shift=LEFT * 0.1), run_time=0.6)
        self.play(ReplacementTransform(p18, p18b), ReplacementTransform(bar61, bar61b),
                  ReplacementTransform(tag61, tag61b), run_time=0.6)
        self.add(bar61b, tag61b)
        card = ponder_at(self, PONDER_Q, 8)

        # ============================================================ 4 · it runs first; every retry: PENDING
        p105 = src_panel(TP + "cell-18.py", 105, 109, wrap={109: ["session="]})
        _with_header(p105, "Travel Planner · cell 18 · lines 105–109")
        place(p105, left=-6.35, top=TOP)
        bar106 = p105.bar(106, TURN, 0.18)
        bar109 = p105.bar(109, S.GREY, 0.22)
        prompt106 = p105.span(106, "prompt")
        x_arrow = p105.get_right()[0] + 0.15
        y106 = row_of(p105, 106).get_center()[1]
        y109 = row_of(p105, 109).get_center()[1]
        arrow = CurvedArrow([x_arrow, y106, 0], [x_arrow, y109, 0], angle=-PI / 2, color=S.GREY,
                            stroke_width=3, tip_length=0.18)
        runs = note("runs first", size=22)
        place(runs, left=arrow.get_right()[0] + 0.15, cy=(y106 + y109) / 2)
        inside(p105, arrow, runs)
        apart(runs, mini, 0.1)
        apart(runs, VGroup(human, h_lab), 0.1)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card), ReplacementTransform(p18b, p105), FadeOut(bar61b), FadeOut(tag61b),
                      run_time=0.8)
            self.play(FadeIn(bar106), *recolor(prompt106, LOOKUP), run_time=0.5)
            vo.wait_until("before the agent starts")
            self.play(FadeIn(bar109), Create(arrow), run_time=0.7)
            self.play(FadeIn(runs, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("Inside turn 3")
            self.play(Indicate(gate.caption, color=TURN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("so every retry gets the same stamp")
            for _ in range(2):
                bump(self, [mg, cg, pend_mini], back=0.35, run_time=0.5)
                self.play(Indicate(pend_mini, color=TURN, scale_factor=1.15), run_time=0.45)

        # ============================================================ 5 · turn 4: yes, APPROVED, Python's budget
        p27 = src_panel(TP + "cell-27.py", 2, wrap={2: ["session"]})
        _with_header(p27, "Travel Planner · cell 27 · line 2")
        place(p27, left=-6.35, top=TOP)
        yes = p27.span(2, '"yes"')
        for gl in yes:
            gl.set_opacity(0)
        h_to = np.array([p27.get_right()[0] + 0.6, row_of(p27, 2).get_center()[1], 0])
        h_lab_to = h_lab.copy()
        place(h_lab_to, left=h_to[0] + 0.45, cy=h_to[1])
        # the turnstile in the middle row, with room for the card to pass
        row_b = 0.05                                          # the card's centre line
        x_g = -1.6                                            # the gate's centre (between its posts)
        posts = VGroup(gate.lpost, gate.rpost)
        g_shift = np.array([x_g - posts.get_center()[0], row_b - cg.get_center()[1], 0])   # keeps bar vs card
        half_g = posts.width / 2
        cg_b = card_glyph(2.15, 0.66).move_to([x_g - half_g - 0.1 - 2.15 / 2, row_b, 0])
        mg_b = mg.copy().move_to([cg_b.get_left()[0] - 0.08 - mg.width / 2, row_b, 0])
        pass_dx = (x_g + half_g + 0.25 + 2.15 / 2) - cg_b.get_center()[0]
        assert cg_b.get_right()[0] + pass_dx < 1.5 and mg_b.get_left()[0] > -6.3
        tape = BudgetTape()
        place(tape, left=-6.35, bottom=-3.45)
        tot = obox([TOTAL_ROW], "cell 27 · saved output")
        place(tot, left=tape.get_right()[0] + 0.6, bottom=-3.45)
        tot_num = substring(tot.rows[0], '"total_usd": 2690.0')
        test = excerpt_chip(TEST, "Travel Planner · cell 27 · line 6", line=TEST)
        place(test, left=-6.35, cy=row_b - 0.1)
        own = note("the notebook's own test", size=22)
        place(own, left=test.get_right()[0] + 0.3, cy=test.chip.get_center()[1])
        test_num = text_span(test.text, "2690.0")
        inside(p27, tape, tot, test, own)
        apart(tot, tape, 0.3)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(p105), FadeOut(bar106), FadeOut(bar109), FadeOut(arrow), FadeOut(runs),
                      tr.goto(7), gate.animate.shift(g_shift), Transform(cg, cg_b), Transform(mg, mg_b),
                      pend_mini.animate.move_to(cg_b), human.animate.move_to(h_to),
                      h_lab.animate.move_to(h_lab_to), run_time=0.9)
            inside(VGroup(mg, cg, gate), human, h_lab)
            apart(gate, p27, 0.15)
            self.play(FadeIn(p27, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the human types yes")
            self.play(LaggedStart(*[gl.animate.set_opacity(1) for gl in yes], lag_ratio=0.7), run_time=0.9)
            self.play(Indicate(human, color=INK, scale_factor=1.12), run_time=0.5)
            vo.wait_until("The stamp flips to approved")
            appr = stamp("APPROVED", DATA, size=20).move_to(cg)
            self.play(ReplacementTransform(pend_mini, appr), run_time=0.6)
            vo.wait_until("finalize runs")
            self.play(gate.open(run_time=0.5))
            self.play(cg.animate.shift(RIGHT * pass_dx), appr.animate.shift(RIGHT * pass_dx), run_time=0.8)
            vo.wait_until("and Python builds the budget line by line")
            self.play(*tape.parts_in("glyph"), run_time=0.4)
            rows = tape.row_anims()
            for a in rows[:-1]:
                self.play(a, run_time=0.45)
            vo.wait_until("2,690 dollars out of 6,000")
            self.play(rows[-1], run_time=0.5)
            self.play(FadeIn(tot, shift=LEFT * 0.1), run_time=0.5)
            self.play(*recolor(tot_num, DATA), run_time=0.4)
            vo.wait_until("The notebook's own test")
            self.play(FadeOut(VGroup(mg, cg, appr, gate)), FadeIn(test, shift=UP * 0.1),
                      FadeIn(own, shift=LEFT * 0.1), run_time=0.6)
            self.play(*recolor(test_num, DATA), *flash(tot_num, DATA, 1.12),
                      Indicate(tape.total, color=DATA, scale_factor=1.08), run_time=0.8)

        # ============================================================ 6 · checked state; hard and soft guardrails
        t4 = obox(T4_ROWS, "Turn 4 · cell 27 · saved output")
        place(t4, left=-6.35, top=TOP)
        assert t4.get_bottom()[1] > tape.get_top()[1] + 0.3, (t4.get_bottom(), tape.get_top())
        ul_checked = under(substring(t4.rows[1], "checked"), DATA, stroke=3)
        ul_python = under(substring(t4.rows[-1], "computed by Python"), DATA, stroke=3)
        p129 = src_panel(TP + "cell-18.py", 129, 135, wrap=True)
        _with_header(p129, "Travel Planner · cell 18 · lines 129–135")
        place(p129, left=-6.35, top=TOP)
        inside(t4, p129)
        hard = span_bar(p129, 129, 131, ERR, 0.2)
        soft = span_bar(p129, 133, 135, TURN, 0.18)
        hard_tag = tag("hard guardrail: raise", ERR, size=20)       # on line 129's short row, clear of 130
        place(hard_tag, right=p129.code.get_right()[0] - 0.2, cy=row_of(p129, 129).get_center()[1] + 0.03)
        soft_tag = tag("soft guardrail: warn", TURN, size=20)       # on 133's short second row, clear of 134
        place(soft_tag, right=p129.code.get_right()[0] - 0.2, cy=row_of(p129, 133, 1).get_center()[1] - 0.05)
        assert hard_tag.get_left()[0] > row_of(p129, 129).get_right()[0] + 0.2
        assert hard_tag.get_bottom()[1] > row_of(p129, 130).get_top()[1] - 0.005
        assert soft_tag.get_top()[1] < row_of(p129, 133).get_bottom()[1] + 0.005
        assert soft_tag.get_left()[0] > max(row_of(p129, 133, 1).get_right()[0],
                                            row_of(p129, 134).get_right()[0]) + 0.2
        with self.voiceover(SAY[6]) as vo:
            self.play(*[FadeOut(m) for m in (p27, human, h_lab, test, own)], run_time=0.5)
            self.play(FadeIn(t4, shift=DOWN * 0.15), run_time=0.6)
            self.play(Create(ul_checked), run_time=0.5)
            self.play(Create(ul_python), run_time=0.5)
            vo.wait_until("An itinerary that skipped the check")
            self.play(*[FadeOut(m) for m in (t4, ul_checked, ul_python, tape, tot)], run_time=0.5)
            self.play(FadeIn(p129, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("a hard guardrail")
            self.play(FadeIn(hard), FadeIn(hard_tag, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("a dollar amount in the model's prose")
            self.play(FadeIn(soft), run_time=0.5)
            vo.wait_until("a soft one")
            self.play(FadeIn(soft_tag, shift=LEFT * 0.1), run_time=0.5)

        # ============================================================ 7 · slides 36-37: the same ideas, in code; ▶
        def lecture_card(title: str, sub: str) -> VGroup:
            t = label(title, 28, INK)
            s_ = note(sub, size=20)
            body = VGroup(t, s_).arrange(DOWN, buff=0.12)
            fr = box(5.2, 1.75, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
            body.move_to(fr).shift(UP * 0.28)
            g = VGroup(fr, body)
            g.frame, g.title, g.sub = fr, t, s_
            return g

        card_a = lecture_card("instructions", "your prompt · slide 36")
        card_b = lecture_card("decision maker", "what the LLM core becomes · slide 37")
        card_a.move_to([-3.25, 1.55, 0])
        card_b.move_to([3.25, 1.55, 0])
        note_a = sticky_note("success criteria")
        note_b = sticky_note("guardrails")
        note_a.move_to(card_a.frame.get_corner(DOWN + RIGHT) + np.array([-0.75, -0.02, 0]))
        note_b.move_to(card_b.frame.get_corner(DOWN + RIGHT) + np.array([-0.75, -0.02, 0]))
        assert note_a.get_top()[1] < card_a.sub.get_bottom()[1] - 0.05
        assert note_b.get_top()[1] < card_b.sub.get_bottom()[1] - 0.05
        in_code = label("in code:", 24, S.GREY)
        c_budget = fix_chip("Python's budget")
        c_render = fix_chip("checked render")
        c_gate = fix_chip("approval gate")
        code_row = VGroup(in_code, c_budget, c_render, c_gate).arrange(RIGHT, buff=0.35)
        code_row.move_to([0, -0.6, 0])
        tool = chip("finalize_itinerary", DATA, size=22, font="DejaVu Sans Mono")
        act = note("action tool", size=22)
        tool_grp = VGroup(act, tool).arrange(RIGHT, buff=0.3)
        tool_grp.shift(np.array([c_gate.get_center()[0] - tool.get_center()[0], -2.75 - tool.get_center()[1], 0]))
        g_small = Gate("FINAL", TURN, gate_w=0.8, gate_h=0.9)
        g_small.shift(np.array([tool.get_center()[0] - g_small.get_center()[0],
                                tool.get_top()[1] + 0.02 - g_small.lpost.get_bottom()[1], 0]))
        lr2 = lref("36–37")
        inside(card_a, card_b, note_a, note_b, code_row, tool_grp, g_small)
        apart(card_a, card_b, 0.3)
        apart(g_small, code_row, 0.15)
        apart(note_a, code_row, 0.3)
        your = your_card([
            TURN_ROWS[0], TURN_ROWS[1], TURN_ROWS[2],
            VGroup(label("is optional: type", 20, INK), mono("exit", 20, INK), label("to leave", 20, INK))
            .arrange(RIGHT, buff=0.14),
            ("OpenAI calls · every turn", COST),
        ])
        your.move_to([0, 0.2, 0])
        inside(your)
        with self.voiceover(SAY[7]) as vo:
            self.play(*[FadeOut(m) for m in (p129, hard, soft, hard_tag, soft_tag)], FadeIn(lr2), run_time=0.6)
            self.play(FadeIn(card_a, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(note_a, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("and guardrails in the decision maker")
            self.play(FadeIn(card_b, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(note_b, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("This notebook keeps both in code")
            self.play(FadeIn(in_code), run_time=0.3)
            self.play(LaggedStart(
                FadeIn(c_budget, target_position=note_a.get_center(), scale=0.6),
                FadeIn(c_render, target_position=note_a.get_center(), scale=0.6),
                FadeIn(c_gate, target_position=note_b.get_center(), scale=0.6), lag_ratio=0.4), run_time=1.4)
            self.play(FadeIn(tool_grp, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(g_small, target_position=c_gate.get_center(), scale=0.7), run_time=0.7)
            vo.wait_until("on the action tool")
            self.play(Indicate(tool, color=DATA, scale_factor=1.08), Indicate(g_small.bar, color=TURN),
                      run_time=0.8)
            vo.wait_until("Every turn is paid")
            self.play(*[FadeOut(m) for m in (card_a, card_b, note_a, note_b, code_row, tool_grp, g_small, lr2)],
                      tr.goto(8), run_time=0.6)
            vo.wait_until("pause, and run the four turns")
            self.play(FadeIn(your, shift=UP * 0.15), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
