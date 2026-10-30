"""S08 · Act 3: rails, not suggestions (README "3 · Harness › Act 3", steps 1-3, and two extras).
Start of part 2. Lecture: 22–23, then 36.

Beats (script.md "## S08", one voiceover block each):
 0  A TEAL 3-row strip at the bottom with the bare container prompt, its title bar tagged "still
    running from part 1"; on "if you closed it" the GREY card "closed it? on the laptop: `bash
    docker-shell.sh`, then your key" (README.md · lines 101, 113–115) above it. On "Remember the
    move-right arrow" the card leaves and V1's table arrives small (as of act 2; its rows are
    bars) with LECTURE 22–23; Move LEFT dims, the GREEN Move RIGHT arrow lights and its four
    reasons write in as named (high stakes · irreversible · predictable · audit); on "give control
    to code" slide 23's frame is redrawn as a GREEN dashed border round the table, its banner "the
    harness keeps authority" on the bottom edge.
 1  On "Act 3 does exactly that" the banner and the Move RIGHT arrow pulse; on "The order route is
    a graph" the table, its frame, the lecture tag (it leaves with its picture) and the strip leave. V5: the
    U-shaped rail (tag "illustration · README.md · lines 349–356": the README's diagram redrawn),
    GREEN stations, edges and switch, the one BLUE station "propose cart", the revise loop with
    "revisions ≤ 2"; under it CODE(acts/act3_workflow.py: 27–32) (20 pt, only line 29 wrapped). On
    "and Python owns its edges" every edge flashes. As the SAY names each move, its edge lights
    (thicker, a GREEN flash) and its code line gets a GREEN bar; on "and back to propose" the loop
    and line 29 turn YELLOW, on "only if the report fails" its condition turns YELLOW and the
    switch pulses; on "at most twice" the RECORDED chip `Revisions allowed  2` (Agent Harness ·
    cell 14 · saved output, tag recorded) arrives right of the counter, which pulses. On "Only one
    node" the BLUE station pulses and "no tools · structured proposal" writes in under it.
 2  LECTURE 36. The panel, chips and tags leave; the rail's texts fade, then its shapes shrink
    onto slide 36 redrawn: a PINK double arrow with four stops (rule-based · structured output ·
    hybrid · full agent autonomy) and a small graph above each (code nodes GREEN, model nodes BLUE;
    dashed BLUE edges = paths the model picks). The GREY card "README: under Agent Harness
    (README.md · line 17) / lecture: under Agent Systems (slide 36) · same graph" on top. On "near
    structured output" that stop lights and the rail's BLUE station pulses; on "a fixed graph" the
    caption "a fixed graph · one model step" writes in above it.
 3  TRACKER Act3 1. The spectrum leaves. Container terminal (12 rows, TEAL), title-bar tags `no
    key` + GOLD `live · billed per token` (the typed line fills its row). `python cli.py --act 3
    --scenario standard` -> container/30 lines 2–3 (wrap), 5, 9–10, 12–14, 15 as 401s (12 rows).
    On "the model proposes quantities" line 12 (Cart proposer) pulses BLUE and line 14's
    "Available tools: none (structured proposal only)" turns YELLOW; on "transitions" the two
    `Step:` lines turn GREEN; on "Success is a receipt" the top-band chip README.md · line 367 "A
    successful order has an application receipt" (expected).
 4  TRACKER Act3 2: `python cli.py --act 3` -> container/31 lines 5, 6 (wrap), 16 as 401s; the
    scenario turns YELLOW, and "the harness checks it and stops". The terminal shrinks to the strip
    (step 2's command and its scenario line; the tags ride on the bar) and, on "Comté", the rail
    returns above it (tag illustration inside the U), a BLUE "model" chip on "propose cart", the
    customer's cart: a GREY token left of "confirm" and the GREY item chips Comté · Bûcheron ·
    Époisses inside the U, the GREY tag "customer input · data/shipping_customer_cart.json" in the
    top band (the chips flash; on "to Pennsylvania" the strip's `pa-shipping` flashes). On "Before":
    the tag leaves, a RED bar closes the loop, "review only"; the token runs through confirm and
    propose (it leaves propose BLUE: the model records the cart) and stops at validate, RED (Comté
    RED), under the README's QUOTE(382–383) (excerpt, `expected`; in the top band from "Before" on).
    On "After": TRACKER Act3 3 as the quote leaves and the bar lifts; the strip types `python cli.py
    --act 3 --scenario pa-shipping` -> container/32 line 5 (its scenario YELLOW; the strip holds the
    prompt, the folded command and that line) while
    the counter "revisions ≤ 2" pulses, and the token rides the loop back into propose; on "may fix
    it" the model chip pulses.
 5  TRACKER Act3 3 · extra. The strip's tags swap to `scripted` + GREEN `offline · free`; it types
    `python cli.py --act 3 --fixture --scenario pa-shipping` (tag extra). On "a script in the
    model's seat" the model chip slides out and the BLUE dashed `scripted` seat comes in. A BLUE
    dashed token runs the rail while the strip prints container/36 in turn: 11–13 as it leaves
    propose (the cart chips arrive BLUE; its first row flashes on "Attempt 1 has", "RAW MILK" turns
    RED on "raw-milk"), 14–15 as it enters
    validate, 16 (wrapped: the whole reason) with the RED stamp `shipping: comte`, token and Comté
    RED; 17, and it rides the revise loop (counter 1/2); 19–21 as it leaves propose again, 22 (the
    whole attempt-2 cart), 23–25 while the Comté chip swaps for Taleggio (old out, then new in) and
    the GREY chip "README.md · lines 384–385 quote the start of the line: `Removed: Comté 18 mois
    (comte) — 350 g`" (expected) arrives; on "valid, 50 dollars" it enters validate: a GREEN stamp
    `valid; $50.10` (the capture's words), token and chips GREEN, then 26–27 ("valid; $50.10"
    GREEN); 28 as it runs pairings, review, revalidate and
    place (it waits out of the U, GREEN), and 33–35 (`your numbers will differ` on the receipt).
 6  TRACKER Act3 3 · extra. `python cli.py --act 3 --fixture --scenario pa-shipping-blocked`
    (extra) -> a new BLUE dashed token: rejected at validate, back along the loop (counter 1/2),
    container/37 lines 19–24 print and the caption "No changes; the same cart was proposed again."
    (the capture's line 24) appears; rejected again (2/2); the third proposal fails (36–37) and the
    token runs into a RED buffer "UNRESOLVED" (38–39) beside validate (`your numbers will differ` on
    the blank row 38, over the run ID's end: its own row is full); on "not blocked" a GREY
    dashed buffer "BLOCKED · live run only" under it; on "so in Colab" the GREY card "Colab: keep
    `USE_FIXTURES = False` for this lesson (Agent Harness · cell 11 · line 6)" top right. On "Pause
    and run" everything but the tracker leaves (its caption drops " · extra": the card is the README's
    steps 1-3 plus the extra) and the static "your turn" card shows the three live
    commands ("with your key:"), the fixture command (extra; GREEN "no key: offline · free") and
    the GOLD "live proposals · billed per token". Hold 2 s, then fade to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Polygon,
    Rectangle,
    RoundedRectangle,
    ShowPassingFlash,
    Succession,
    Text,
    UpdateFromAlphaFunc,
    VGroup,
    VMobject,
    linear,
    smooth,
    squish_rate_func,
)

from common import *  # noqa: F401,F403
from common import _header_text, _mixed_row, _swap_text
from explainer import style as S
from explainer.devops import box, chip, label, mono, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S08"]

# ------------------------------------------------------------------ the real captures (file line numbers)
STD = capture("container/30")
BLK = capture("container/31")
PAS = capture("container/32")
FIX = capture("container/36")
FXB = capture("container/37")
assert STD.cmd == "python cli.py --act 3 --scenario standard", STD.cmd
assert BLK.cmd == "python cli.py --act 3", BLK.cmd
assert PAS.cmd == "python cli.py --act 3 --scenario pa-shipping", PAS.cmd
assert FIX.cmd == "python cli.py --act 3 --fixture --scenario pa-shipping", FIX.cmd
assert FXB.cmd == "python cli.py --act 3 --fixture --scenario pa-shipping-blocked", FXB.cmd
assert len(P_CTR) + 1 + len(STD.cmd) <= 65 < len(P_CTR) + 1 + len(STD.cmd) + 3   # no room for a tag beside it
assert STD.line(9) == "Step: confirm_request" and STD.line(10) == "Step: propose_cart"
assert "Cart proposer" in STD.line(12)
TOOLS14 = "Available tools: none (structured proposal only)"
assert STD.line(14).strip() == TOOLS14, STD.line(14)
SC31 = "pa-shipping-blocked · LIVE proposals"
SC32 = "pa-shipping · LIVE proposals"
assert BLK.line(5) == f"Scenario: {SC31}" and PAS.line(5) == f"Scenario: {SC32}"
STOPS31 = "the harness checks it and stops"
assert STOPS31 in BLK.line(6)
RAW = "RAW MILK"
assert FIX.line(12).strip() == "Comté 18 mois (comte) — 350 g · RAW MILK"
assert FIX.line(16).startswith("Cart attempt 1: shipping: comte")
REMOVED = "Removed: Comté 18 mois (comte) — 350 g"
assert FIX.line(24).strip() == REMOVED and FIX.line(25).strip() == "Added: Taleggio (taleggio) — 350 g"
VALID = "valid; $50.10"
assert FIX.line(27) == f"Cart attempt 2: {VALID}"
assert FIX.line(33).startswith("--- WORKFLOW PLACED") and FIX.line(34) == "Order placed."
assert FIX.line(35).startswith("Receipt: ")
NOCHG = "No changes; the same cart was proposed again."
assert FXB.line(24).strip() == NOCHG
assert FXB.line(36).startswith("Cart attempt 3: shipping: comte")
assert FXB.line(37).strip() == "Revision limit reached; no order will be placed."
assert FXB.line(39).startswith("--- WORKFLOW UNRESOLVED")
for _c, _n in ((STD, 15), (BLK, 16), (PAS, 16)):
    _c.as401(_n, short=True)

C14 = capture("expected/colab-c14-policies")
REV = C14.squeeze(8)                       # whitespace only: the saved table's padding
assert REV == "Revisions allowed  2", REV

# sources (exact sub-strings, checked)
R367 = "A successful order has an application receipt"
assert R367 in source_line("README.md", 367)
assert "Act 3: a controlled workflow" in source_line("README.md", 17) and "3. Agent Harness" in source_line("README.md", 17)
assert source_line("README.md", 101).strip() == "bash docker-shell.sh"
assert source_line("README.md", 113).startswith("read -rsp")
assert "Confirm request" in source_line("README.md", 349) and "Revalidate and place" in source_line("README.md", 356)
Q383 = "It should show Comté marked `RAW MILK`, a shipping violation, `WORKFLOW BLOCKED`, and no receipt."
assert "`Removed:" in source_line("README.md", 384) and source_line("README.md", 385).startswith("Comté`")
COLAB6 = "USE_FIXTURES = False"
assert source_line("colab/cell-11.py", 6).startswith(COLAB6)
EDGE_LINES = (27, 28, 29, 30, 31, 32)          # acts/act3_workflow.py: RAIL_EDGES order
for _n, (_a, _b) in zip(EDGE_LINES, (("confirm", "propose"), ("propose", "validate"), ("validate", "propose"),
                                       ("validate", "pair"), ("pair", "approve"), ("approve", "place"))):
    assert source_line("acts/act3_workflow.py", _n).strip().startswith(f".add_edge({_a}, {_b}"), _n
COND29 = "condition=lambda state: not state.report.ok)"
assert source_line("acts/act3_workflow.py", 29).rstrip().endswith(COND29)

# ------------------------------------------------------------------ layout
SAFE = 6.45
RAIL_K = 0.8            # the rail at 0.8 (Piece.rescale: shapes shrink, every text keeps 20 pt)
TOP_BAND = 1.97         # beats 4-6: a card above the rail starts here (the rail's counter tops out under it)


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


def flash(mob, color: str = TURN, k: float = 1.12):
    return Indicate(mob, color=color, scale_factor=k)


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
    """resize(), with the title-bar tags riding along on the bar; the title, which frame_tags may
    have moved left, is lent out of t while resize() runs, so it stays where it is (S07's idiom)."""
    y = bar_y(t, rows)
    title, t.title = t.title, None
    try:
        resize(scene, t, rows, keep=keep, run_time=run_time,
               extra=[title.animate.set_y(y), *[m.animate.set_y(y) for m in tags]])
    finally:
        t.title = title


def texts_of(mob) -> list:
    """Every text in mob's family (Text, or a mono_line with .pt)."""
    return [m for m in mob.get_family() if isinstance(m, Text) or hasattr(m, "pt")]


def path_of(pts) -> VMobject:
    p = VMobject()
    p.set_points_as_corners([np.array(q, dtype=float) for q in pts])
    return p


def ride(m, path, run_time: float, rate=smooth):
    """One animation: m's centre runs along `path` (a VMobject) with one smooth ease."""
    def upd(mob, a):
        mob.move_to(path.point_from_proportion(min(1.0, max(0.0, rate(a)))))
    return UpdateFromAlphaFunc(m, upd, run_time=run_time, rate_func=linear)


def tint(tok, color: str, rate=smooth) -> list:
    """Animations: a cart_token glyph (solid or dashed) turns `color`: strokes, the basket's
    tint and the wheels."""
    out = []
    for m in tok.glyph.family_members_with_points():
        if isinstance(m, Dot):
            out.append(m.animate(rate_func=rate).set_fill(color, 1).set_stroke(color))
        else:
            out.append(m.animate(rate_func=rate).set_stroke(color).set_fill(color, m.get_fill_opacity()))
    return out


def sq(a: float, b: float):
    """rate_func: smooth, squeezed into [a, b] of the play."""
    return squish_rate_func(smooth, a, b)


def item_chip(name: str, color: str = S.GREY) -> VGroup:
    """A cart item chip (cart_token's item look): the cheese's name on a tinted chip."""
    return chip(name, color, size=CAPTION, pad_x=0.14, pad_y=0.06)


def recolor_chip(c, color: str, rate=smooth):
    return c.box.animate(rate_func=rate).set_stroke(color).set_fill(color, 0.16)


def cart_chips(names, color: str) -> VGroup:
    """The cart's contents inside the U: a GREY "cart" and one chip per item. .items .lbl"""
    items = VGroup(*[item_chip(n, color) for n in names]).arrange(RIGHT, buff=0.08)
    lbl = label("cart", CAPTION, S.GREY)
    row = VGroup(lbl, items).arrange(RIGHT, buff=0.18)
    row.items, row.lbl = items, lbl
    return row


def pulse(frame, color: str | None = None, width: float = 8.0):
    """A station's frame pulses: a thick outline (no fill) over it fades in and out. The frame
    itself is not animated, so it never comes forward over its own label."""
    ol = frame.copy().set_fill(opacity=0).set_stroke(color or frame.get_stroke_color(), width)
    return Succession(FadeIn(ol, run_time=0.3), FadeOut(ol, run_time=0.45))


def feed(t, items, wrap: bool = False):
    """(rows, anims, done): print `items` ((text, colour) pairs, at most t.rows rows in all, each
    cut at the row like Terminal.print, or folded at a word boundary with wrap=True, as
    wrap_output does for t.print) into terminal `t` as ANIMATIONS, so a token can move in the same
    play: rows that scroll off fade in place (first 30%), the staying rows shift up (30-65%), the
    new rows fade in after (staggered; when no row stays, right after the old ones are gone, so
    the strip is never blank for long). Call done() after the play."""
    texts = []
    for s_, col in items:
        if wrap and len(s_) > t.max_chars:
            texts += [(row, col) for row, _a, _b, _ind in wrap_output(s_, t.max_chars)]
        else:
            texts.append((t._cut(s_), col))
    assert 0 < len(texts) <= t.rows, len(texts)
    overflow = max(0, len(t.lines) + len(texts) - t.rows)
    gone = list(t.lines.submobjects[:overflow])
    stay = list(t.lines.submobjects[overflow:])
    anims = [FadeOut(r, rate_func=squish_rate_func(smooth, 0.0, 0.3)) for r in gone]
    if overflow and stay:
        anims += [r.animate(rate_func=squish_rate_func(smooth, 0.3, 0.65)).shift(UP * t.pitch * overflow)
                  for r in stay]
    new = VGroup()
    for j, (s_, col) in enumerate(texts):
        ln = mono_line(s_, t.size, col)
        t._place(ln, len(stay) + j)
        new.add(ln)
    for ln in new:
        t.lines.add(ln)
    t0 =(0.6 if stay else 0.32) if overflow else 0.0
    n = len(new)
    for j, ln in enumerate(new):
        a = t0 + (1 - t0) * 0.4 * (j / (n - 1) if n > 1 else 0)
        anims.append(FadeIn(ln, rate_func=squish_rate_func(smooth, a, min(1.0, a + (1 - t0) * 0.6))))

    def done():
        for r in gone:
            if r in t.lines.submobjects:
                t.lines.remove(r)
    return new, anims, done


def new_rail(show=None):
    """V5 at 0.8 (its boxes built 2.95 wide, so "validate and price" keeps a margin at 0.8)."""
    rl = Rail(box_w=2.95, show=show)
    rl.rescale(RAIL_K)
    return rl


def band_card(rows, frame_color: str = S.GREY) -> VGroup:
    """A GREY card of rows (mobjects), left-aligned, opaque. .frame .rows"""
    rws = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    fr = box(rws.width + 0.5, rws.height + 0.4, frame_color, fill=S.BG, fill_opacity=0.95, radius=0.12)
    rws.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    g = VGroup(fr, rws)
    g.frame, g.rows = fr, rws
    return g


def mini_node(color: str, w: float = 0.42, h: float = 0.26) -> RoundedRectangle:
    return RoundedRectangle(width=w, height=h, corner_radius=0.07, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.3)


def mini_arrow(a, b, color: str = HARNESS) -> Arrow:
    return Arrow(a, b, buff=0.04, color=color, stroke_width=2.5, tip_length=0.1,
                 max_tip_length_to_length_ratio=0.4)


def rule_graph() -> VGroup:
    """Rule-based: a fixed if/else graph, every node code (GREEN)."""
    n0, n3 = mini_node(HARNESS).move_to([0, 0, 0]), mini_node(HARNESS).move_to([2.2, 0, 0])
    d = Polygon([0.6, 0, 0], [0.82, 0.16, 0], [1.04, 0, 0], [0.82, -0.16, 0], stroke_color=HARNESS,
                stroke_width=2.5).set_fill(HARNESS, 0.3)
    n1, n2 = mini_node(HARNESS).move_to([1.55, 0.36, 0]), mini_node(HARNESS).move_to([1.55, -0.36, 0])
    ar = VGroup(mini_arrow(n0.get_right(), d.get_left()), mini_arrow(d.get_top(), n1.get_left()),
                mini_arrow(d.get_bottom(), n2.get_left()), mini_arrow(n1.get_right(), n3.get_left()),
                mini_arrow(n2.get_right(), n3.get_left()))
    return VGroup(ar, n0, d, n1, n2, n3)


def hybrid_graph() -> VGroup:
    """Hybrid: a fixed graph with several model steps embedded (BLUE)."""
    cols = (HARNESS, CLOUD, HARNESS, CLOUD, HARNESS)
    pts = ((0, 0), (0.55, 0.32), (1.1, 0), (1.65, 0.32), (2.2, 0))
    ns = [mini_node(c).move_to([x, y, 0]) for c, (x, y) in zip(cols, pts)]
    ar = VGroup(*[mini_arrow(a.get_right(), b.get_left()) for a, b in zip(ns, ns[1:])])
    extra = mini_node(CLOUD).move_to([1.1, -0.42, 0])
    ar.add(mini_arrow(ns[1].get_bottom(), extra.get_left()), mini_arrow(extra.get_right(), ns[3].get_bottom()))
    return VGroup(ar, *ns, extra)


def agent_graph() -> VGroup:
    """Full agent autonomy: a model node picks its own paths (dashed BLUE) at run time."""
    a = mini_node(CLOUD).move_to([0.2, 0, 0])
    b = mini_node(CLOUD).move_to([1.2, 0, 0])
    others = [mini_node(S.GREY).move_to(p) for p in ([1.2, 0.42, 0], [1.2, -0.42, 0], [2.2, 0.24, 0], [2.2, -0.24, 0])]
    ed = VGroup(*[DashedLine(p, q, dash_length=0.06).set_stroke(CLOUD, 2.5) for p, q in (
        (a.get_right(), b.get_left()), (a.get_right(), others[0].get_left()), (a.get_right(), others[1].get_left()),
        (b.get_right(), others[2].get_left()), (b.get_right(), others[3].get_left()))])
    return VGroup(ed, a, b, *others)


class RailGeo:
    """Where things are on a placed (rescaled) Rail: the two rows, the three columns and the
    points a token passes. Tokens tunnel: z_index -1 under the opaque station boxes, so a token
    goes INTO a station and comes out the other side (it never crosses a label)."""

    def __init__(self, rl):
        f = {n: rl.station(n).frame for n in RAIL_STATIONS}
        self.f = f
        self.yt, self.yb = f["confirm"].get_center()[1], f["place"].get_center()[1]
        self.xl, self.xm, self.xr = (f[n].get_center()[0] for n in ("confirm", "propose", "validate"))
        self.bw, self.bh = f["confirm"].width, f["confirm"].height
        self.start = np.array([self.xl - self.bw / 2 - 0.5, self.yt, 0])
        self.end = np.array([self.xl - self.bw / 2 - 0.5, self.yb, 0])
        self.gap_cp = np.array([(self.xl + self.xm) / 2, self.yt, 0])
        self.gap_pv = np.array([(self.xm + self.xr) / 2, self.yt, 0])
        self.c = {n: f[n].get_center() for n in RAIL_STATIONS}
        self.arc = rl.loop.arc
        self.top_top = f["confirm"].get_top()[1]             # top of the top row's boxes
        self.bot_top = f["place"].get_top()[1]
        self.bot_bottom = f["place"].get_bottom()[1]

    def loop_path(self) -> VMobject:
        """From inside validate, out of its top along the revise arc, into propose."""
        p = path_of([self.c["validate"], self.arc.get_start()])
        p.append_vectorized_mobject(self.arc.copy())
        p.add_line_to(self.c["propose"])
        return p

    def to_place_path(self) -> VMobject:
        """From inside validate down the right side, along the bottom row, out of place."""
        return path_of([self.c["validate"], self.c["pairings"], self.c["review"], self.c["place"], self.end])


def new_token(dashed: bool = False, color: str = CLOUD):
    t = cart_token(dashed=dashed, color=color)
    t.set_z_index(-1)                    # under the station boxes: it tunnels through them
    return t


class Rails(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · part 2: the prompt; Move RIGHT
        strip = term(container=True, rows=3)
        still = frame_tags(strip, grey_tag("still running from part 1"))
        closed = card_rows([_mixed_row(["closed it? on the laptop:", "`bash docker-shell.sh`", ", then your key"]),
                            ("README.md · lines 101, 113–115", S.GREY)])
        place(closed, left=-6.45, bottom=STRIP_TOP + 0.3)
        ab = ActionBoundary(width=8.6, row_h=0.42, texts=(), moves=True).prefill(2)
        ml, mr = ab.parts["moves_left"], ab.parts["moves_right"]
        mr.remove(mr.reasons)                       # the reasons write in one by one (below)
        r1 = VGroup(label("high stakes", CAPTION, INK), label("· irreversible", CAPTION, INK)).arrange(RIGHT, buff=0.12)
        r2 = VGroup(label("predictable", CAPTION, INK), label("· audit", CAPTION, INK)).arrange(RIGHT, buff=0.12)
        reasons = VGroup(r1, r2).arrange(DOWN, buff=0.08)
        reasons.next_to(mr.arrow, DOWN, buff=0.1)
        items = [r1[0], r1[1], r2[0], r2[1]]
        tbl = VGroup(ab, reasons)
        fr23 = box(tbl.width + 0.36, tbl.height + 0.55, HARNESS, dashed=True, stroke=3)   # room for the banner
        ban_t = label("the harness keeps authority", CAPTION, HARNESS)
        ban = VGroup(Rectangle(width=ban_t.width + 0.4, height=ban_t.height + 0.16, stroke_width=0)
                     .set_fill(S.BG, 1), ban_t)
        whole = VGroup(tbl, fr23)
        fr23.move_to(tbl).shift(DOWN * 0.125)
        ban.move_to(fr23.get_bottom())
        apart(ban, reasons)
        lr = lref("22–23")
        place(VGroup(whole, ban), right=lr.get_left()[0] - 0.15, bottom=STRIP_TOP + 0.14)
        assert fr23.get_top()[1] < lr.get_bottom()[1] - 0.06 or fr23.get_right()[0] < lr.get_left()[0]
        inside(fr23)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(strip, shift=UP * 0.2), run_time=0.6)
            bare_prompt(self, strip)
            self.play(FadeIn(still, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("if you closed it")
            self.play(FadeIn(closed, shift=UP * 0.1), run_time=0.5)
            self.play(flash(closed.rows[0], TURN, 1.04), run_time=0.7)
            vo.wait_until("Remember the move-right")
            self.play(FadeOut(closed), run_time=0.4)
            self.play(FadeIn(ab), FadeIn(lr), run_time=0.6)
            self.play(ml.animate.set_opacity(0.3), mr.arrow.animate.set_stroke(width=8), run_time=0.5)
            self.play(flash(mr.title, HARNESS, 1.2), run_time=0.6)
            for it, anchor in zip(items, ("when stakes are high", "be undone", "the task is predictable",
                                          "or you need an audit")):
                vo.wait_until(anchor)
                self.play(FadeIn(it, shift=UP * 0.08), run_time=0.4)
            vo.wait_until("give control to code")
            self.play(Create(fr23), run_time=0.8)
            self.play(FadeIn(ban, shift=UP * 0.05), run_time=0.4)

        # ========================================================== 1 · V5: the graph; Python owns its edges
        rl = new_rail(show=("stations", "edges", "loop", "counter", "switch"))
        p = src_panel("acts/act3_workflow.py", 27, 32, wrap={29: ["condition="]}, size=20)
        place(p, cx=0, bottom=-3.5)
        g0 = RailGeo(rl)
        # the band above the rail: illustration tag (left), RECORDED chip right of the counter
        ill = illustration_tag("README.md · lines 349–356")
        rec_t = mono(REV, CAPTION, OUTPUT)
        rec_fr = box(rec_t.width + 0.4, rec_t.height + 0.24, S.GREY, fill=TERM_BG, fill_opacity=1, radius=0.08)
        rec_t.move_to(rec_fr)
        rec = VGroup(rec_fr, rec_t)
        rec_h = _header_text("Agent Harness · cell 14 · saved output")
        rec_tag = recorded_tag()
        # stack: rail, then (relative to it) the band rows
        rl.shift(UP * (p.get_top()[1] + 0.14 - (rl.get_bottom()[1])) + LEFT * 0.25)   # room for the chip
        g0 = RailGeo(rl)
        row_a = g0.top_top + 0.08 + 0.235          # band row A (illustration tag, the chip)
        row_b = max(row_a + 0.53, rl.counter.get_top()[1] + 0.06 + 0.235)   # row B (its header and tag): over the counter
        lift = max(0.0, row_b + 0.235 - 3.52)
        assert lift < 0.01, f"beat 1 is {lift:.2f} too tall"
        place(ill, left=-6.45, cy=row_a)
        place(rec, right=SAFE, cy=row_a)
        place(rec_h, right=SAFE - 0.05, cy=row_b)
        place(rec_tag, right=rec_h.get_left()[0] - 0.2, cy=row_b)
        cnt = rl.counter
        for a_, b_ in ((ill, cnt), (rec, cnt), (rec_h, cnt), (rec_tag, cnt), (ill, rl.loop), (rec, rl.loop),
                       (ill, rec_tag), (rl, p)):
            apart(a_, b_)
        for m in (ill, rec, rec_h, rec_tag, rl, p):
            inside(m)
        bars = {n: p.bar(n, TURN if n == 29 else HARNESS, 0.2) for n in EDGE_LINES}
        cond = p.span(29, COND29.rstrip(")"))
        edges = [rl.edge(i) for i in range(6)]
        with self.voiceover(SAY[1]) as vo:
            self.play(flash(ban_t, HARNESS, 1.06), mr.arrow.animate.set_stroke(width=10), run_time=0.8)
            vo.wait_until("The order route is a graph")
            self.play(FadeOut(VGroup(ab, reasons, fr23, ban)), FadeOut(lr), FadeOut(VGroup(strip, still)),
                      run_time=0.5)
            self.play(FadeIn(rl), FadeIn(ill, shift=DOWN * 0.08), run_time=0.7)
            vo.wait_until("and Python owns its edges")
            self.play(FadeIn(p, shift=UP * 0.1), run_time=0.6)
            self.play(LaggedStart(*[ShowPassingFlash(e.copy().set_stroke(HARNESS, 9), time_width=0.6)
                                    for e in edges if e is not rl.loop],
                                  ShowPassingFlash(rl.loop.arc.copy().set_stroke(HARNESS, 9), time_width=0.6),
                                  lag_ratio=0.15), run_time=1.2)
            steps = (("Confirm, propose", 0), ("propose, validate", 1), ("and back to propose", 2),
                     ("then pairings", 3), ("manager review when", 4), ("revalidate and place", 5))
            for anchor, i in steps:
                vo.wait_until(anchor)
                n = EDGE_LINES[i]
                if i == 2:
                    self.play(rl.loop.animate.set_color(TURN).set_stroke(width=6), FadeIn(bars[n]), run_time=0.5)
                    self.play(ShowPassingFlash(rl.loop.arc.copy().set_stroke(TURN, 10), time_width=0.6), run_time=0.8)
                    vo.wait_until("only if the report fails")
                    self.play(cond.animate.set_color(TURN), flash(rl.switch, TURN, 1.5), run_time=0.6)
                    vo.wait_until("at most twice")
                    self.play(FadeIn(rec, shift=LEFT * 0.1), FadeIn(rec_h), FadeIn(rec_tag), run_time=0.6)
                    self.play(flash(cnt, HARNESS, 1.2), flash(rec_t, HARNESS, 1.08), run_time=0.8)
                    continue
                e = edges[i]
                self.play(e.animate.set_stroke(width=6), FadeIn(bars[n]), run_time=0.4)
                self.play(ShowPassingFlash(e.copy().set_stroke(HARNESS, 10), time_width=0.7), run_time=0.6)
            vo.wait_until("Only one node")
            self.play(pulse(rl.station("propose").frame, CLOUD, 9), run_time=0.75)
            self.play(*rl.parts_in("caption"), run_time=0.5)
            vo.wait_until("with no tools")
            self.play(flash(rl.parts["caption"], CLOUD, 1.08), run_time=0.7)


        # ========================================================== 2 · slide 36: the autonomy spectrum
        sp = Spectrum(width=12.2)
        sp.move_to([0, -1.55, 0])
        PIC_H = 1.35                                   # pictures sit this far above their stops
        pics = {0: rule_graph(), 2: hybrid_graph(), 3: agent_graph()}
        for i, pic in pics.items():
            pic.scale(0.95).move_to(sp.above(i, PIC_H))           # (glyphs only: no text in them)
        k_mini = 2.5 / (g0.f["validate"].get_right()[0] - g0.f["confirm"].get_left()[0])
        filing = band_card([
            VGroup(label("README: under Agent Harness", CAPTION, INK),
                   _header_text("(README.md · line 17)")).arrange(RIGHT, buff=0.15),
            VGroup(label("lecture: under Agent Systems", CAPTION, INK), label("(slide 36)", CAPTION, S.GREY),
                   label("· same graph", CAPTION, INK)).arrange(RIGHT, buff=0.15),
        ])
        place(filing, cx=0, top=2.55)
        lr36 = lref("36")
        apart(filing, lr36)
        cap36 = label("a fixed graph · one model step", CAPTION, INK)
        with self.voiceover(SAY[2]) as vo:
            olds = [p, *bars.values(), rec, rec_h, rec_tag, ill]
            self.play(FadeOut(VGroup(*olds)), *[m.animate.set_opacity(0) for m in texts_of(rl)],
                      rl.loop.animate.set_color(HARNESS).set_stroke(width=4),
                      *[e.animate.set_stroke(width=4) for e in edges if e is not rl.loop], run_time=0.6)
            mini = rl.glyph_only()                     # the texts have left: shapes only from here
            self.remove(*rl.get_family())             # (a part revealed by FadeIn sits on the scene on its own)
            self.add(mini)
            self.play(mini.animate.scale(k_mini).move_to(sp.above(1, PIC_H)), FadeIn(filing, shift=DOWN * 0.1),
                      run_time=1.0)
            place(cap36, cx=mini.get_center()[0], bottom=mini.get_top()[1] + 0.2)
            apart(cap36, filing)
            for pic in pics.values():
                apart(pic, cap36)
                apart(pic, mini, 0.45)
            apart(pics[0], pics[2], 0.45)
            apart(pics[2], pics[3], 0.45)
            vo.wait_until("on the lecture's autonomy spectrum")
            self.play(FadeIn(lr36), Create(sp.arrow),
                      LaggedStart(*[FadeIn(VGroup(d, tx)) for d, tx in zip(sp.dots, sp.labels)], lag_ratio=0.2),
                      run_time=1.0)
            self.play(LaggedStart(*[FadeIn(pics[i], shift=UP * 0.1) for i in (0, 2, 3)], lag_ratio=0.25),
                      run_time=0.9)
            vo.wait_until("it sits near structured output")
            self.play(sp.light(1), run_time=0.5)
            self.play(pulse(mini.st["propose"].frame, CLOUD, 7), run_time=0.75)
            vo.wait_until("a fixed graph")
            self.play(FadeIn(cap36, shift=UP * 0.08), run_time=0.5)

        # ========================================================== 3 · step 1: the standard order, live (401)
        tr = tracker("Act3", 1)
        t = term(container=True, rows=12)
        ft = frame_tags(t, nokey_tag(), live_tag())
        c367 = top_chip(R367, where="README.md · line 367", expected=True)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(sp, *pics.values(), mini, cap36, filing)), FadeOut(lr36), run_time=0.5)
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t, shift=UP * 0.2), FadeIn(ft[0], shift=DOWN * 0.1),
                      run_time=0.5)
            type_cmd(self, t, STD.cmd, 1.1)
            self.play(FadeIn(ft[1], shift=DOWN * 0.1), run_time=0.3)
            out = show(self, t, STD, (2, 3), 5, (9, 10), (12, 14), STD.as401(15, short=True), wrap=True,
                       run_time=0.9)
            assert len(t.lines) <= 12
            r9, r10 = item_rows(out, 3)[0], item_rows(out, 4)[0]
            r12, r14 = item_rows(out, 5)[0], item_rows(out, 7)[0]
            vo.wait_until("the model proposes quantities")
            self.play(flash(r12.glyphs, CLOUD, 1.06), run_time=0.6)
            self.play(substring(r14, TOOLS14).animate.set_color(TURN), run_time=0.4)
            vo.wait_until("transitions")
            self.play(r9.glyphs.animate.set_color(HARNESS), r10.glyphs.animate.set_color(HARNESS), run_time=0.5)
            vo.wait_until("Success is a receipt")
            self.play(FadeIn(c367, shift=DOWN * 0.1), run_time=0.5)
            self.play(flash(c367.phrase, TURN, 1.05), run_time=0.6)

        # ========================================================== 4 · steps 2-3: the shipping lesson, before / after
        rl4 = new_rail()
        rl4.shift(UP * (STRIP_TOP + 0.12 - rl4.get_bottom()[1]) + LEFT * 0.3)
        g = RailGeo(rl4)
        inside(rl4)
        assert rl4.get_top()[1] < TOP_BAND - 0.06, rl4.get_top()
        ill4 = illustration_tag()
        cap_prop = rl4.parts["caption"]
        cart_row = cart_chips(("Comté", "Bûcheron", "Époisses"), S.GREY)
        cart_items = cart_row.items
        mid_y = (g.top_top - g.bh + g.bot_top) / 2           # the U's inside, between the rows
        place(cart_row, cx=g.xm - 0.2, cy=mid_y - 0.12)
        place(ill4, left=g.f["confirm"].get_left()[0], cy=cart_row.get_center()[1])
        for a_, b_ in ((cart_row, cap_prop), (cart_row, g.f["review"]), (cart_row, g.f["propose"]),
                       (ill4, cart_row), (ill4, g.f["place"]), (ill4, g.f["confirm"])):
            apart(a_, b_)
        seat = chip("model", CLOUD, size=CAPTION)
        seat.next_to(g.f["propose"], UP, buff=0.08).align_to(g.f["propose"], LEFT)
        apart(seat, rl4.loop)
        tok = new_token(color=S.GREY)                      # the customer's cart: input data, not a proposal
        tok.move_to(g.start)
        inside(tok)
        cust = grey_tag("customer input · data/shipping_customer_cart.json")
        place(cust, left=-6.45, bottom=TOP_BAND + 0.12)
        assert cust.get_top()[1] < 2.9
        bl = rl4.block_loop("review only")
        # at 0.8 the bar reaches the counter and its label the corner of "propose cart": a shorter
        # bar (top clear of the counter) and the label right under it
        mid = rl4.loop.arc.point_from_proportion(0.5)
        top_lim = min(mid[1] + 0.22, rl4.counter.get_bottom()[1] - 0.08)
        bl.bar.put_start_and_end_on(mid + DOWN * 0.16, np.array([mid[0], top_lim, 0]))
        bl.label.next_to(bl.bar, DOWN, buff=0.04)
        apart(bl, rl4.counter)
        apart(bl.label, g.f["propose"], 0.03)
        apart(bl.label, g.f["validate"], 0.03)
        quote = quote_card(382, 383, lines=[Q383], wrap=50, header="README.md · lines 382–383 (excerpt)")
        place(quote, left=-1.35, bottom=TOP_BAND)
        inside(quote)
        for m in (cust, quote):
            apart(m, tr)
        nudge = np.array([g.f["validate"].get_left()[0] + 0.15 - tok.width / 2, g.yt, 0])
        with self.voiceover(SAY[4]) as vo:
            # step 2 (Before) owns the strip until "After": its command and scenario stay under the
            # Before story; step 3's command is typed as the revise loop opens
            self.play(FadeOut(c367), tr.goto(2), run_time=0.4)
            c1 = type_cmd(self, t, BLK.cmd, 0.5)
            o1 = show(self, t, BLK, 5, 6, BLK.as401(16, short=True), wrap=True, run_time=0.4)
            sc31 = item_rows(o1, 0)[0]
            self.play(substring(sc31, SC31).animate.set_color(TURN),
                      wrapped_glyphs(item_rows(o1, 1), STOPS31).animate.set_color(TURN), run_time=0.4)
            self.wait(0.9)
            keep = [*c1.rows, sc31] if hasattr(c1, "rows") else [c1, sc31]
            fit(self, t, 3, keep=keep, tags=list(ft), run_time=0.5)
            strip = t
            vo.wait_until("Comté")
            self.play(FadeIn(rl4), FadeIn(ill4), FadeIn(seat, shift=DOWN * 0.08), FadeIn(tok, shift=RIGHT * 0.2),
                      FadeIn(cart_row, shift=UP * 0.08), FadeIn(cust, shift=DOWN * 0.08), run_time=0.6)
            self.play(LaggedStart(*[flash(c, S.GREY, 1.12) for c in cart_items], lag_ratio=0.25), run_time=0.8)
            vo.wait_until("to Pennsylvania")
            self.play(flash(substring(sc31, "pa-shipping"), TURN, 1.1), run_time=0.6)
            vo.wait_until("Before, the model")
            self.play(FadeIn(bl, shift=DOWN * 0.1), FadeOut(cust), run_time=0.4)
            self.play(FadeIn(quote, shift=DOWN * 0.1), run_time=0.4)        # (where the tag was: after it)
            self.play(ride(tok, path_of([g.start, g.gap_cp]), 0.7), run_time=0.7)
            self.play(ride(tok, path_of([g.gap_cp, g.gap_pv]), 0.8), *tint(tok, CLOUD, sq(0.35, 0.6)),
                      *[recolor_chip(c, CLOUD, sq(0.5, 0.8)) for c in cart_items], run_time=0.8)
            vo.wait_until("the harness checks it and stops")
            self.play(ride(tok, path_of([g.gap_pv, nudge]), 0.35), run_time=0.35)
            self.play(*tint(tok, ERR), recolor_chip(cart_items[0], ERR), run_time=0.3)
            self.play(ride(tok, path_of([nudge, g.gap_pv]), 0.35), run_time=0.35)
            vo.wait_until("After, the revise loop")
            self.play(tr.goto(3), FadeOut(bl, shift=UP * 0.3), FadeOut(quote), run_time=0.45)
            type_cmd(self, t, PAS.cmd, 0.5)
            # (the command folds under the prompt: prompt, command and its scenario fill the strip;
            # the 401 that follows is the same as step 2's)
            o2 = show(self, t, PAS, 5, run_time=0.3)
            self.play(substring(o2[0], SC32).animate.set_color(TURN), flash(rl4.counter, HARNESS, 1.2),
                      ride(tok, path_of([g.gap_pv, g.c["validate"]]), 0.6), run_time=0.6)
            self.play(ride(tok, g.loop_path(), 1.3), run_time=1.3)
            vo.wait_until("may fix it")
            self.play(flash(seat, CLOUD, 1.2), pulse(rl4.station("propose").frame, CLOUD, 8), run_time=0.75)
        self.remove(tok)                         # inside propose (hidden): the before / after runs are over

        # ========================================================== 5 · extra: the same path offline, scripted
        ft5 = frame_tags(strip, scripted_tag(), offline_tag())
        stamp_c = stamp("shipping: comte", ERR)
        place(stamp_c, left=rl4.loop.get_right()[0] + 0.12, bottom=g.top_top + 0.12)
        apart(stamp_c, rl4.counter)
        apart(stamp_c, rl4.loop)
        inside(stamp_c)
        stamp_ok = stamp(VALID, HARNESS)                 # attempt 2 passes: the capture's own words
        place(stamp_ok, left=stamp_c.get_left()[0], bottom=stamp_c.get_bottom()[1])
        apart(stamp_ok, rl4.counter)
        apart(stamp_ok, rl4.loop)
        inside(stamp_ok)
        exp = excerpt_chip(REMOVED, "README.md · lines 384–385 quote the start of the line:", line=FIX.line(24))
        etag = expected_tag()
        place(exp, left=-2.6, bottom=TOP_BAND + 0.04)
        place(etag, left=exp.chip.get_right()[0] + 0.25, cy=exp.chip.get_center()[1])
        assert exp.get_top()[1] < 2.93 and etag.get_right()[0] < SAFE
        apart(VGroup(exp, etag), tr)
        com5 = cart_items[0]
        tal = item_chip("Taleggio", CLOUD)
        tal.move_to(com5).align_to(com5, LEFT)
        grow = tal.width - com5.width
        assert cart_row.get_right()[0] + grow < g.xr - 0.3
        tok5 = new_token(dashed=True)
        tok5.move_to(g.start)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(cart_row), FadeOut(VGroup(*ft)), run_time=0.4)
            self.play(caption_extra(tr, True), FadeIn(ft5), run_time=0.4)
            c3 = type_cmd(self, strip, FIX.cmd, 0.9)
            ex = extra_tag()
            beside(ex, strip, c3)
            pin(self, c3, ex, run_time=0.3)
            for c in cart_items:                  # attempt 1 is the scripted proposer's (same three cheeses)
                c.box.set_stroke(CLOUD).set_fill(CLOUD, 0.16)
            self.play(FadeIn(tok5, shift=RIGHT * 0.2), run_time=0.3)
            self.play(ride(tok5, path_of([g.start, g.gap_cp]), 0.6), run_time=0.6)
            vo.wait_until("with a script in the model's seat")
            self.play(FadeOut(seat, shift=LEFT * 0.3), run_time=0.35)
            self.play(*rl4.scripted_seat(), run_time=0.55)
            rows, an, done = feed(strip, FIX.out(11, 12, 13))
            self.play(ride(tok5, path_of([g.gap_cp, g.gap_pv]), 0.8), FadeIn(cart_row, rate_func=sq(0.45, 1.0)),
                      *an, run_time=0.8)
            done()
            att1 = rows[0]
            vo.wait_until("Attempt 1 has")
            self.play(flash(att1.glyphs, TURN, 1.04), run_time=0.5)
            # "raw-milk Comté": the RAW MILK line stays on the strip until it is said
            vo.wait_until("raw-milk")
            self.play(substring(rows[1], RAW).animate.set_color(ERR), flash(com5, ERR, 1.15), run_time=0.6)
            rows, an, done = feed(strip, FIX.out(14, 15))
            self.play(ride(tok5, path_of([g.gap_pv, g.c["validate"]]), 0.5), *an, run_time=0.5)
            done()
            rows, an, done = feed(strip, FIX.out(16), wrap=True)          # the whole reason, 2 rows
            assert len(rows) == 2, len(rows)
            self.play(FadeIn(stamp_c, scale=1.2), *tint(tok5, ERR), recolor_chip(com5, ERR), *an, run_time=0.5)
            done()
            vo.wait_until("and the rail sends it back")
            rows, an, done = feed(strip, FIX.out(17))
            self.play(ride(tok5, g.loop_path(), 1.1), FadeOut(stamp_c, rate_func=sq(0.5, 1.0)), *an, run_time=1.1)
            done()
            self.play(*rl4.count(1), run_time=0.4)
            vo.wait_until("attempt 2 swaps in Taleggio")
            rows, an, done = feed(strip, FIX.out(19, 20, 21))
            self.play(ride(tok5, path_of([g.c["propose"], g.gap_pv]), 0.6), *tint(tok5, CLOUD, sq(0.0, 0.3)),
                      *an, run_time=0.6)
            done()
            rows, an, done = feed(strip, FIX.out(22))           # attempt 2's whole cart on the strip
            self.play(*an, run_time=0.35)
            done()
            others = list(cart_items[1:3])                     # (before the swap stages Taleggio in)
            rows, an, done = feed(strip, FIX.out(23, 24, 25))   # Changes · Removed · Added
            self.play(*an, *_swap_text(cart_items, com5, tal),
                      *[c.animate(rate_func=sq(0.4, 0.6)).shift(RIGHT * grow) for c in others],
                      FadeIn(exp, shift=DOWN * 0.08, rate_func=sq(0.5, 1.0)), FadeIn(etag, rate_func=sq(0.5, 1.0)),
                      run_time=1.0)
            done()
            vo.wait_until("valid, 50 dollars")
            self.play(ride(tok5, path_of([g.gap_pv, g.c["validate"]]), 0.45), run_time=0.45)
            # the stamp and the capture's own line arrive together (Changes · Removed · Added stayed up till now)
            rows, an, done = feed(strip, FIX.out(26, 27))
            self.play(FadeIn(stamp_ok, scale=1.2), *tint(tok5, HARNESS),
                      *[recolor_chip(c, HARNESS) for c in cart_items], *an, run_time=0.5)
            done()
            self.play(substring(rows[1], VALID).animate.set_color(HARNESS), run_time=0.3)
            rows, an, done = feed(strip, FIX.out(28))
            self.play(ride(tok5, g.to_place_path(), 1.6), *an, run_time=1.6)
            done()
            rows, an, done = feed(strip, FIX.out(33, 34, 35))
            self.play(*an, run_time=0.5)
            done()
            dt = differ_tag()
            beside(dt, strip, rows[2])
            pin(self, rows[2], dt, run_time=0.3)

        # ========================================================== 6 · trap: blocked + fixtures = UNRESOLVED
        unres = buffer_stop("UNRESOLVED")
        unres.shift(np.array([0, g.yt, 0]) - unres.bar.get_center())
        place(unres, right=6.5)
        blocked = buffer_stop("BLOCKED", S.GREY, dashed=True)
        only = label("live run only", CAPTION, S.GREY)
        only.next_to(blocked.label, DOWN, buff=0.06)
        blocked.add(only)
        place(blocked, cx=unres.get_center()[0], top=unres.get_bottom()[1] - 0.2)
        inside(unres)
        inside(blocked)
        assert blocked.get_bottom()[1] > STRIP_TOP + 0.05
        apart(blocked, g.f["pairings"])
        apart(unres, g.f["validate"], 0.02)
        stop_at = np.array([unres.bar.get_left()[0] - 0.08 - tok5.width / 2, g.yt, 0])
        nochg = band_card([mono(NOCHG, CAPTION, OUTPUT)])
        place(nochg, cx=g.xm, bottom=TOP_BAND + 0.08)
        colab = band_card([_mixed_row(["Colab: keep", f"`{COLAB6}`", "for this lesson"], CAPTION),
                           _header_text("(Agent Harness · cell 11 · line 6)")])
        place(colab, right=SAFE, bottom=TOP_BAND + 0.04)
        for m in (nochg, colab):
            inside(m)
            apart(m, tr)
            apart(m, rl4.counter)
        cart6 = cart_chips(("Comté", "Bûcheron", "Époisses"), CLOUD)
        cart6.move_to(cart_row).align_to(cart_row, LEFT)
        com6 = cart6.items[0]
        tok6 = new_token(dashed=True)
        tok6.move_to(g.start)
        tc = turn_card([Prose("with your key:"), STD.cmd, BLK.cmd, PAS.cmd,
                        (Prose("no key: offline · free"), HARNESS), (FIX.cmd, "extra"),
                        (Prose("live proposals · billed per token"), COST)])
        place(tc, cx=0, cy=-0.35)
        inside(tc)
        assert tc.get_top()[1] < tr.get_bottom()[1] - 0.1
        with self.voiceover(SAY[6]) as vo:
            newc = label("revisions ≤ 2", CAPTION, HARNESS).move_to(rl4.counter)
            reset = _swap_text(rl4, rl4.counter, newc)
            rl4.counter = rl4.parts["counter"] = newc
            self.play(FadeOut(VGroup(exp, etag, tok5, cart_row, stamp_ok)), *reset, run_time=0.4)
            c4 = type_cmd(self, strip, FXB.cmd, 0.7)
            ex6 = extra_tag()
            beside(ex6, strip, c4)
            pin(self, c4, ex6, run_time=0.25)
            self.play(FadeIn(tok6, rate_func=sq(0.0, 0.2)), ride(tok6, path_of([g.start, g.gap_pv]), 0.7),
                      FadeIn(cart6, rate_func=sq(0.6, 1.0)), run_time=0.7)
            self.play(ride(tok6, path_of([g.gap_pv, g.c["validate"]]), 0.4), *tint(tok6, ERR, sq(0.6, 1.0)),
                      recolor_chip(com6, ERR, sq(0.6, 1.0)), run_time=0.4)
            rows, an, done = feed(strip, FXB.out(19, 20, 21))
            self.play(ride(tok6, g.loop_path(), 0.8), *rl4.count(1), *an, run_time=0.8)
            done()
            vo.wait_until("proposes the same cart three times")
            rows, an, done = feed(strip, FXB.out(22, 23, 24))
            self.play(ride(tok6, path_of([g.c["propose"], g.c["validate"]]), 0.7), *tint(tok6, CLOUD, sq(0.0, 0.2)),
                      recolor_chip(com6, CLOUD, sq(0.0, 0.3)), FadeIn(nochg, shift=DOWN * 0.08, rate_func=sq(0.4, 1.0)),
                      *an, run_time=0.7)
            done()
            self.play(*tint(tok6, ERR), recolor_chip(com6, ERR), run_time=0.25)
            self.play(ride(tok6, g.loop_path(), 0.7), *rl4.count(2), run_time=0.7)
            rows, an, done = feed(strip, FXB.out(36, 37))
            self.play(ride(tok6, path_of([g.c["propose"], g.c["validate"]]), 0.6), *tint(tok6, CLOUD, sq(0.0, 0.2)),
                      recolor_chip(com6, CLOUD, sq(0.0, 0.3)), *an, FadeIn(unres, rate_func=sq(0.5, 1.0)),
                      run_time=0.6)
            done()
            self.play(*tint(tok6, ERR), recolor_chip(com6, ERR), run_time=0.25)
            vo.wait_until("and ends unresolved")
            rows, an, done = feed(strip, FXB.out(38, 39))
            self.play(ride(tok6, path_of([g.c["validate"], stop_at]), 0.5), *an, run_time=0.5)
            done()
            # the run ID's row is full: its `your numbers will differ` sits on the blank row 38 right
            # above the ID's end (it rides with that row)
            # (the house tag is 0.47 tall and a row 0.40: this one is the same tag at 20 pt in a
            # slimmer pill, so it clears the rows above and below)
            assert not rows[0].text.strip(), rows[0].text
            dt6 = tag("your numbers will differ", S.GREY, size=CAPTION)
            dt6.box.stretch_to_fit_height(strip.pitch - 0.04)
            dt6.move_to([strip.box.get_right()[0] - 0.12 - dt6.width / 2, rows[0].strut.get_center()[1], 0])
            r37 = strip.lines[0]
            assert FXB.line(37).strip() in r37.text, r37.text
            for r_ in (r37, rows[1]):
                assert not covers_text(dt6, r_)
            assert dt6.get_bottom()[1] > rows[1].glyphs.get_top()[1] + 0.02
            pin(self, rows[0], dt6, run_time=0.6,
                anim=AnimationGroup(FadeIn(dt6, shift=LEFT * 0.1), flash(unres, ERR, 1.15)))
            vo.wait_until("not blocked")
            self.play(FadeIn(blocked, shift=UP * 0.08), run_time=0.5)
            vo.wait_until("so in Colab")
            self.play(FadeOut(nochg), run_time=0.3)
            self.play(FadeIn(colab, shift=DOWN * 0.08), run_time=0.4)
            self.play(flash(colab.rows[0], TURN, 1.04), run_time=0.7)
            vo.wait_until("Pause and run")
            self.play(FadeOut(VGroup(rl4, ill4, cart6, tok6, unres, blocked, colab, strip, ft5)),
                      caption_extra(tr, False), run_time=0.5)
            self.play(FadeIn(tc, scale=0.97), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tc, tr)), run_time=0.8)
        self.wait(0.3)
