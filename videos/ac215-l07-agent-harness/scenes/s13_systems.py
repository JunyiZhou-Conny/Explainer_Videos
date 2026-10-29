"""S13 · Act 6: an agent that calls a workflow (README "5 · Agent systems", steps 1-3).
Lecture: 31–33, then 21, 36 and 22.

Beats (script.md "## S13", one voiceover block each):
 0  LECTURE 31–33; the tracker "README › 5 · Agent systems" (no step lit yet). Left: "single
    agent", one BLUE agent node whose three GREEN "tool" chips pop in one by one, "grows by adding
    tools". On "with a graph of agents": "graph of agents" in two patterns. On "a manager calling
    agents as tools": "manager", a BLUE node with GREY edges to three BLUE specialist nodes, "tool
    call". On "or peers handing off": "peers", three GREY dashed nodes with "handoff" arrows and a
    baton passed along, the GREY dashed `concept · lecture only` and "not in this tutorial".
 1  The single agent, the heading and two of the specialists leave. The manager node moves left
    and becomes "customer assistant / harness"; the middle specialist grows into a GREEN box
    holding V5's mini rail (its one BLUE proposer station), "act 3 ordering workflow"; its edge
    turns PINK and "tool call" becomes `start_order(request_id)` (old out, then new in). The
    README's diagram completes (tag illustration · README.md · lines 605–611): a GREEN return
    "pending review or final outcome", then, in a column under the assistant, "tasting-planning
    skill" → "customer-facing explanation". On "with a model inside one node" the BLUE station
    pulses; on "No handoffs" the peers fade.
 2  TRACKER Systems 1. The picture and its lecture tag leave. CODE(README.md: 619–624), line 622
    YELLOW (`build_act6(fixture=True)`). Under it composition_layers.py lines 22–26 as five GREEN
    chips (header "formaggio/agents/composition_layers.py · lines 22–26"); as the SAY names them,
    model_calls ("outer model calls"), tool_calls, workflow_model_calls ("per workflow") and
    seconds ("one shared clock · nested workflows included") flash and get their GREY notes.
 3  CODE(acts/act6_composition.py: 15, 17–19, 23–24) (folded; line 18 wrapped): line 15 gets a
    YELLOW bar, line 18 a GREEN bar with both "manager-approval" GREEN. On "the model only picks an
    ID" line 24 gets a PINK bar, `request_id` turns PINK and the PINK handle chip `request-1`
    arrives beside it. On "Its tools are narrow" the header "acts/act6_composition.py · lines 24,
    29, 34" with the GREY tag "narrow tools" beside it; the three GREEN tool chips arrive under
    them as they are named.
 4  TRACKER Systems 2. Container terminal (10 rows; title-bar tags `no key` + GOLD `live · billed
    per token`: the typed line fills its row) types `python cli.py --act 6 --scenario standard` ->
    container/60 lines 2–3 (wrap; line 3 GREEN), 5, 7, 9 (wrap), 10 as 401s. On "tell outer model
    calls apart" line 7 pulses BLUE, start_order and get_order_status turn PINK and the top-band
    chip README.md · line 637 (expected) arrives, centred between the tracker and the terminal;
    on "the outer agent cannot approve" line 3's "host manager review when required" turns YELLOW.
 5  TRACKER Systems 3. The chip leaves; the terminal shrinks to the strip (its tags swap, old out
    then new in, to `scripted` + GREEN `offline · free`). Above it (tag illustration, right of the
    tracker) a BLUE "customer assistant" node and two glyph-only rails, request-1 above request-2 (PINK
    arrows and handles), each with three stations named once between them: validate · manager
    review · revalidate & place; the right side stays free. The strip types the two-orders
    command (folds; `--manager-decision approve` in a YELLOW outline, tag TEST decision) and
    prints container/61 lines 5 ("approve" YELLOW), 23–24, 35, 38, 46–47, 58, 61 in turn, while
    each BLUE dashed (scripted) token enters its rail, turns GREEN through validate (`$220.80` by
    the station), then waits ON the amber "manager review" station (its GREEN ticket, the
    harness's, as S09's; the track into it amber). On "and the test decision approves both" a
    YELLOW check (the human decision) lands beside each ticket.
 6  The shared GREEN shelf (StockShelf) at right: Mimolette 3,000 g, Taleggio 3,000 g, Comté
    6,000 g, under it a RECORDED box (Agent Harness · cell 18 · saved output: lines 2, 4, 7, 9
    folded to the product and stock_g columns). On "Request 1 is placed" ticket 1's check pulses,
    request-1 thaws and rides on to "revalidate & place", the strip prints line 80 GREEN; on
    "leaving 1,400" the bars drain by 1,600 g (Mimolette and Taleggio 1,400 g, Comté 4,400 g). On
    "Request 2 reaches revalidation" the RECORDED box leaves, ticket 2's check pulses and request-2
    rides onto its "revalidate & place"; on "needing 1,600" RED dashed outlines of 1,600 g on the
    two short bars (Comté gets a GREEN check); on "blocked" token and station turn RED, the two RED
    labels (container/61 lines 190–191) arrive right of request-2's ticket and the strip prints
    line 92 RED.
    On "That's the ponder" the YELLOW chip "the act 3 ponder · for real"; on "approval is not
    placement" both checks pulse beside one placed and one blocked order.
 7  The picture leaves; the terminal grows to 12 rows. On "the lecture's response step" slide 21's
    six steps (chips slimmed to fit above the terminal) arrive with LECTURE 21, "Response" lit GREEN.
    On "the app checks the model's plan" it prints container/61 152, 158–160
    (cut after "1600 g"); on "and fills in quantities" the three "1600 g" turn GREEN; on "and the
    status, placed" 170 GREEN, on "from the receipt" its GREY tag "filled in by the app from the
    receipt". On "The blocked order" 175, 183, 184 (wrapped, RED) with the GREY chip "one
    message for both cases · formaggio/operations/governance.py · line 75"; on "the stock lines
    below" 190–191 (YELLOW box, GREY tag "the reason") and 193.
 8  LECTURE 36, 22. The terminal and the six steps leave. Slide 36's spectrum returns (four stops,
    small graphs: a rule graph, act 3's rail, act 6, an agent graph); act 6 sits at "hybrid": a
    BLUE agent node outside, a PINK call into the fixed rail; on "it's a hybrid" that stop lights
    and "hybrid · inside out" writes in. The V1 mini-map: Sub agents YELLOW, its GREEN cell gains a
    bar, caption "Sub agents ← narrow tools · separate counters · one clock"; the checkpoint chip
    README.md · line 662. On "Pause and run" everything but the tracker leaves and the static
    "your turn" card arrives (with your key: the standard run; the two-orders run, GREEN offline ·
    free; GOLD "act 6 live · billed per token"). Hold 2 s, then an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Circumscribe,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Mobject,
    Polygon,
    RoundedRectangle,
    ShowPassingFlash,
    Succession,
    Transform,
    UpdateFromAlphaFunc,
    VGroup,
    VMobject,
    linear,
    smooth,
    squish_rate_func,
)

from common import *  # noqa: F401,F403
from common import _header_text, _set_op
from explainer import style as S
from explainer.devops import box, cell_width, check_mark, chip, code_span, label, mono, mono_line, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S13"]

# ------------------------------------------------------------------ the real captures (file line numbers)
STD = capture("container/60")
TWO = capture("container/61")
C18 = capture("expected/colab-c18-data-constraints")
assert STD.cmd == "python cli.py --act 6 --scenario standard", STD.cmd
assert TWO.cmd == "python cli.py --act 6 --fixture --scenario two-orders --manager-decision approve", TWO.cmd
assert len(P_CTR) + 1 + len(STD.cmd) == 64          # fills its row: the GOLD tag goes on the title bar
assert STD.line(3).startswith("Harness → ordering workflow → host manager review when required")
assert STD.line(7) == "Model call 1 · Customer assistant · gpt-5.6-luna"
assert "start_order, get_order_status, assess_event" in STD.line(9)
HOST = "host manager review when required"
assert TWO.line(5) == "TEST manager response configured: approve"
assert TWO.line(23).strip() == "Tool call 2: start_order" and TWO.line(24).strip() == "Arguments: request id: request-1"
assert TWO.line(46).strip() == "Tool call 3: start_order" and TWO.line(47).strip() == "Arguments: request id: request-2"
SUB = "$220.80"
assert TWO.line(35) == TWO.line(58) == f"Cart attempt 1: valid; {SUB}"
assert TWO.line(38) == "Order request-1: pending_approval" and TWO.line(61) == "Order request-2: pending_approval"
assert TWO.line(80) == "Order request-1: placed" and TWO.line(92) == "Order request-2: blocked"
assert TWO.line(152) == "## Host tasting plan — request-1"
PLAN_CUT = "1600 g"
for _n in (158, 159, 160):
    assert PLAN_CUT in TWO.line(_n), _n
assert TWO.line(170) == "Authoritative status: placed."
assert TWO.line(175) == "request-1: placed" and TWO.line(183) == "request-2: blocked"
STOCK_MSG = "stock: Requested 1600 g; available 1400 g."
assert TWO.line(190).strip() == TWO.line(191).strip() == STOCK_MSG
assert TWO.line(193) == "Outer model calls: 10; workflow model calls: 0."
# the shelf's numbers: the saved Colab table (cell 18), stock_g column
for _n, _pid, _g in ((4, "comte", 6000), (7, "mimolette", 3000), (9, "taleggio", 3000)):
    _cols = [c.strip() for c in C18.line(_n).split("|")]
    assert _cols[1] == _pid and _cols[4] == str(_g), C18.line(_n)
assert [c.strip() for c in C18.line(2).split("|")][4] == "stock_g"
NEED, LEFT_AFTER = 1600, 1400                         # each order takes 1,600 g of each cheese (61:74-76)

# ------------------------------------------------------------------ sources (exact sub-strings, checked)
RD = "README.md"
R605 = ("Customer assistant / harness", "start_order(request_id)", "Act 3 ordering workflow",
        "pending review or final outcome", "tasting-planning skill", "customer-facing explanation")
for _n, _s in zip((605, 606, 607, 609, 610, 611), R605):
    assert _s in source_line(RD, _n), (_n, _s)
R622 = "build_act6(fixture=True)"
assert R622 in source_line(RD, 622)
R637 = "Separate outer-model calls from workflow-model calls"
assert R637 in source_line(RD, 637)
R662 = "why two approvals do not guarantee two successful orders"
assert R662 in source_line(RD, 662) and source_line(RD, 662).startswith("**Checkpoint:**")
CL = "formaggio/agents/composition_layers.py"
BUDGET = ((22, "model_calls: int = 16", "outer model calls"),
          (23, "tool_calls: int = 20", None),
          (24, "seconds: float = 180", "one shared clock · nested workflows included"),
          (25, "workflow_model_calls: int = 8", "per workflow"),
          (26, "proposal_seconds: float = 120", None))
for _n, _s, _ in BUDGET:
    assert source_line(CL, _n).strip() == _s, (_n, source_line(CL, _n))
A6 = "acts/act6_composition.py"
C15 = "The host confirms requests; the model can only select their IDs."
assert C15 in source_line(A6, 15)
MA = '"manager-approval"'
assert source_line(A6, 18).count(MA) == 2
assert source_line(A6, 24).strip() == "async def start_order(request_id: str) -> dict:"
TOOLS = (("start_order", 24), ("get_order_status", 29), ("assess_event", 34))
for _t, _n in TOOLS:
    assert f"def {_t}(request_id: str)" in source_line(A6, _n), (_t, _n)
GOV = "formaggio/operations/governance.py"
MSG75 = "Invalid or unauthorized order."
assert MSG75 in source_line(GOV, 75) and TWO.line(184) == f"Final checkout blocked: {MSG75} No order placed."
TWO_ROWS = ("python cli.py --act 6 --fixture \\", "    --scenario two-orders --manager-decision approve")
assert " ".join(r.rstrip(" \\").strip() for r in TWO_ROWS) == TWO.cmd

# ------------------------------------------------------------------ layout
SAFE = 6.45
TOP = 2.6               # content top under the tracker
TITLE = 24              # the beat-0 headings
# beats 5-6: two glyph-only rails above the strip, a shared shelf at right
Y1, Y2 = 1.85, 0.35     # the rails' rows (request-1 above request-2)
XV = -3.3               # the "validate" stations' x
BAND = 0.62             # a rail's annotations sit this far above (request-1) / below (request-2) it
SHELF_RIGHT = SAFE


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
    """Indicate on a chip's or tag's TEXT (its .text), never on its filled backing: a flash never
    hides its own label."""
    txt = getattr(mob, "text", None)
    return Indicate(txt if isinstance(txt, Mobject) else mob, color=color, scale_factor=k)


def outline_flash(m, color: str = TURN, buff: float = 0.07):
    """A stroke-only flash round m (Circumscribe): nothing filled covers it."""
    return Circumscribe(m, color=color, buff=buff, fade_out=True, stroke_width=4)


def pulse(frame, color: str | None = None, width: float = 8.0):
    """A frame pulses: a thick outline (no fill) over it fades in and out; the frame itself is not
    animated, so it never comes forward over its own label."""
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
    """resize(), with the title-bar tags riding along on the bar; the title, which frame_tags may
    have moved left, is lent out of t while resize() runs, so it stays where it is (S08's idiom)."""
    y = bar_y(t, rows)
    title, t.title = t.title, None
    try:
        resize(scene, t, rows, keep=keep, run_time=run_time,
               extra=[title.animate.set_y(y), *[m.animate.set_y(y) for m in tags]])
    finally:
        t.title = title


def path_of(pts) -> VMobject:
    p = VMobject()
    p.set_points_as_corners([np.array(q, dtype=float) for q in pts])
    return p


def ride(m, path, run_time: float, rate=smooth):
    """One animation: m's centre runs along `path` (a VMobject) with one smooth ease."""
    def upd(mob, a):
        mob.move_to(path.point_from_proportion(min(1.0, max(0.0, rate(a)))))
    return UpdateFromAlphaFunc(m, upd, run_time=run_time, rate_func=linear)


def tint(tok, color: str) -> list:
    """Animations: a cart_token glyph (solid or dashed) turns `color`: strokes, the basket's tint,
    the wheels."""
    out = []
    for m in tok.glyph.family_members_with_points():
        if type(m).__name__ == "Dot":
            out.append(m.animate.set_fill(color, 1).set_stroke(color))
        else:
            out.append(m.animate.set_stroke(color).set_fill(color, m.get_fill_opacity()))
    return out


def feed(t, items):
    """(rows, anims, done): print `items` ((text, colour) pairs, at most t.rows rows, each cut at the
    row like Terminal.print) into terminal `t` as ANIMATIONS, so a token can move in the same play
    (S08's feed): rows that scroll off fade in place (first 30%), the staying rows shift up
    (30-65%), the new rows fade in after. Call done() after the play."""
    texts = [(t._cut(s_), col) for s_, col in items]
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
    t0 = (0.6 if stay else 0.32) if overflow else 0.0
    n = len(new)
    for j, ln in enumerate(new):
        a = t0 + (1 - t0) * 0.4 * (j / (n - 1) if n > 1 else 0)
        anims.append(FadeIn(ln, rate_func=squish_rate_func(smooth, a, min(1.0, a + (1 - t0) * 0.6))))

    def done():
        for r in gone:
            if r in t.lines.submobjects:
                t.lines.remove(r)
    return new, anims, done


def node(text: str, color: str = CLOUD, w: float | None = None, h: float | None = None,
         dashed: bool = False, size: float = CAPTION) -> VGroup:
    """A labelled node: a rounded box in `color` ("\\n" splits the label into rows; dashed: GREY
    text, an outline only). .frame .text"""
    rows = VGroup(*[label(r, size, S.GREY if dashed else INK) for r in text.split("\n")]).arrange(DOWN, buff=0.06)
    fr = box(max(w or 0, rows.width + 0.4), max(h or 0, rows.height + 0.3), color,
             fill_opacity=0.14, stroke=3, radius=0.12, dashed=dashed)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.text = fr, rows
    return g


def arrow(a, b, color: str = S.GREY, stroke: float = 3, buff: float = 0.06, dashed: bool = False):
    ar = Arrow(a, b, buff=buff, color=color, stroke_width=stroke, tip_length=0.16,
               max_tip_length_to_length_ratio=0.3)
    if dashed:
        from manim import DashedVMobject
        body = DashedVMobject(Line(ar.get_start(), ar.tip.get_start()), num_dashes=6).set_stroke(color, stroke)
        return VGroup(body, ar.tip)
    return ar


def ShowFlash(m, color: str | None = None):
    """A bright pass along an edge (an arrow or a line), the edge itself untouched."""
    src = Line(m.get_start(), m.get_end()) if isinstance(m, Arrow) else m.copy()
    col = color or m.get_color()
    return ShowPassingFlash(src.set_stroke(col, 9), time_width=0.6, run_time=0.7)


def slim_tag(s: str, color: str = S.GREY, size: float = CAPTION, pad_y: float = 0.05) -> VGroup:
    """tag() with less vertical padding: a 20-pt tag() is 0.44 tall and the 22-pt terminal row pitch is
    0.40, so a box drawn round the next rows would touch it; this one stays inside its row's pitch."""
    t_ = label(s, size, color)
    h = mono("|", size).height + 2 * pad_y
    b = RoundedRectangle(width=t_.width + 0.4, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t_.move_to(b)
    g = VGroup(b, t_)
    g.box, g.text = b, t_
    return g


def rows_box(rows, color: str = TURN, pad_x: float = 0.07, pad_y: float = 0.025) -> RoundedRectangle:
    """An outline round terminal rows: their glyphs' width, their struts' height (tight, so a tag
    pinned on the row above stays clear). Not added."""
    gl = VGroup(*[r.glyphs for r in rows])
    top = max(r.strut.get_top()[1] for r in rows) + pad_y
    bot = min(r.strut.get_bottom()[1] for r in rows) - pad_y
    b = RoundedRectangle(width=gl.width + 2 * pad_x, height=top - bot, corner_radius=0.05,
                         stroke_color=color, stroke_width=3).set_fill(opacity=0)
    b.move_to([gl.get_center()[0], (top + bot) / 2, 0])
    return b


def new_token():
    """A scripted cart (BLUE dashed: real program output, scripted proposal), under the stations:
    it tunnels through them."""
    t = cart_token(dashed=True, scale=0.8)
    t.set_z_index(-1)
    return t


def mini_node(color: str, w: float = 0.42, h: float = 0.26, dashed: bool = False) -> VMobject:
    r = RoundedRectangle(width=w, height=h, corner_radius=0.07, stroke_color=color,
                         stroke_width=2.5).set_fill(color, 0.3)
    if dashed:
        from manim import DashedVMobject
        r = DashedVMobject(r.set_fill(opacity=0), num_dashes=10).set_stroke(color, 2.5)
    return r


def mini_arrow(a, b, color: str = HARNESS) -> Arrow:
    return Arrow(a, b, buff=0.04, color=color, stroke_width=2.5, tip_length=0.1,
                 max_tip_length_to_length_ratio=0.4)


def rule_graph() -> VGroup:
    """Rule-based: a fixed if/else graph, every node code (GREEN) (as in act 3's spectrum)."""
    n0, n3 = mini_node(HARNESS).move_to([0, 0, 0]), mini_node(HARNESS).move_to([2.2, 0, 0])
    d = Polygon([0.6, 0, 0], [0.82, 0.16, 0], [1.04, 0, 0], [0.82, -0.16, 0], stroke_color=HARNESS,
                stroke_width=2.5).set_fill(HARNESS, 0.3)
    n1, n2 = mini_node(HARNESS).move_to([1.55, 0.36, 0]), mini_node(HARNESS).move_to([1.55, -0.36, 0])
    ar = VGroup(mini_arrow(n0.get_right(), d.get_left()), mini_arrow(d.get_top(), n1.get_left()),
                mini_arrow(d.get_bottom(), n2.get_left()), mini_arrow(n1.get_right(), n3.get_left()),
                mini_arrow(n2.get_right(), n3.get_left()))
    return VGroup(ar, n0, d, n1, n2, n3)


def agent_graph() -> VGroup:
    """Full agent autonomy: a model node picks its own paths (dashed BLUE) at run time."""
    a = mini_node(CLOUD).move_to([0.2, 0, 0])
    b = mini_node(CLOUD).move_to([1.2, 0, 0])
    others = [mini_node(S.GREY).move_to(p) for p in ([1.2, 0.42, 0], [1.2, -0.42, 0], [2.2, 0.24, 0], [2.2, -0.24, 0])]
    ed = VGroup(*[DashedLine(p, q, dash_length=0.06).set_stroke(CLOUD, 2.5) for p, q in (
        (a.get_right(), b.get_left()), (a.get_right(), others[0].get_left()), (a.get_right(), others[1].get_left()),
        (b.get_right(), others[2].get_left()), (b.get_right(), others[3].get_left()))])
    return VGroup(ed, a, b, *others)


def act3_rail(width: float = 2.2) -> VGroup:
    """Act 3's fixed graph, glyph-only (V5's mini rail scaled down)."""
    rl = Rail(mini=True)
    g = rl.glyph_only()
    g.scale(width / g.width)
    return g


def act6_graph() -> VGroup:
    """Act 6 inside out: a BLUE agent node outside, a PINK call into the fixed rail (its tool).
    .agent .call .rail"""
    rl = act3_rail(1.75)
    a = mini_node(CLOUD, w=0.5, h=0.32)
    a.next_to(rl, LEFT, buff=0.55)
    call = Arrow(a.get_right(), rl.get_left() + RIGHT * 0.02, buff=0.04, color=LOOKUP, stroke_width=3,
                 tip_length=0.12, max_tip_length_to_length_ratio=0.4)
    g = VGroup(call, a, rl)
    g.agent, g.call, g.rail = a, call, rl
    return g


# ------------------------------------------------------------------ the scene
class AgentSystem(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0 · one agent, or a graph of agents
        tr = tracker("Systems")
        lr = lref("31–33")
        LX = -4.55
        ttl1 = label("single agent", TITLE, INK)
        a_node = node("agent", CLOUD, w=1.6)
        a_node.move_to([LX, 0.45, 0])
        place(ttl1, cx=LX, bottom=a_node.get_top()[1] + 0.3)
        tools = VGroup(*[chip("tool", HARNESS, size=CAPTION) for _ in range(3)]).arrange(RIGHT, buff=0.3)
        tools.move_to([LX, -0.8, 0])
        links = VGroup(*[Line(a_node.frame.get_bottom(), c.get_top(), buff=0.05, color=HARNESS, stroke_width=2.5)
                         for c in tools])
        grow = label("grows by adding tools", CAPTION, S.GREY)
        place(grow, cx=LX, top=tools.get_bottom()[1] - 0.22)
        single = VGroup(ttl1, a_node, links, tools, grow)
        # the manager pattern (top right)
        MX, SX = -0.4, 3.9
        ttl2 = label("graph of agents", TITLE, INK)
        m_node = node("agent", CLOUD, w=1.5)
        m_node.move_to([MX, 1.3, 0])
        m_lbl = label("manager", CAPTION, INK)
        place(m_lbl, cx=MX, bottom=m_node.get_top()[1] + 0.14)
        specs = [node("agent", CLOUD, w=1.4).move_to([SX, y, 0]) for y in (2.2, 1.3, 0.4)]
        edges = [arrow(m_node.frame.get_right(), sp.frame.get_left(), S.GREY) for sp in specs]
        tcall = label("tool call", CAPTION, S.GREY)
        e_mid = edges[1]
        place(tcall, cx=(e_mid.get_start()[0] + e_mid.get_end()[0]) / 2 + 0.6, bottom=e_mid.get_center()[1] + 0.1)
        place(ttl2, cx=(MX + SX) / 2, top=2.98)
        # the peers pattern (bottom right): GREY dashed, lecture only
        PY = -1.95
        peers = [node("agent", S.GREY, w=1.15, dashed=True).move_to([x, PY, 0]) for x in (0.45, 3.0, 5.55)]
        p_ar = [arrow(a.frame.get_right(), b.frame.get_left(), S.GREY, dashed=True) for a, b in zip(peers, peers[1:])]
        p_hand = [label("handoff", CAPTION, S.GREY).next_to(ar, UP, buff=0.12) for ar in p_ar]
        for hd, a, b in zip(p_hand, peers, peers[1:]):
            assert hd.get_left()[0] > a.get_right()[0] + 0.12 and hd.get_right()[0] < b.get_left()[0] - 0.12
        p_lbl = label("peers", CAPTION, INK)
        place(p_lbl, cx=peers[0].get_center()[0], bottom=peers[0].get_top()[1] + 0.14)
        baton = RoundedRectangle(width=0.42, height=0.14, corner_radius=0.06, stroke_color=S.GREY,
                                 stroke_width=2).set_fill(S.GREY, 0.6)
        b_y = peers[0].get_bottom()[1] - 0.22
        baton.move_to([peers[0].get_center()[0], b_y, 0])
        ctag = concept_tag()
        nt = label("not in this tutorial", CAPTION, S.GREY)
        foot = VGroup(ctag, nt).arrange(RIGHT, buff=0.3)
        place(foot, cx=peers[1].get_center()[0], top=b_y - 0.3)
        peer_g = VGroup(p_lbl, *peers, *p_ar, *p_hand, baton, foot)
        for m in (single, ttl2, m_lbl, m_node, *specs, tcall, peer_g):
            inside(m)
        apart(ttl2, lr, 0.1)
        apart(ttl2, specs[0], 0.08)
        apart(single, m_node, 0.3)
        apart(single, peer_g, 0.2)
        apart(specs[2], peer_g, 0.2)
        apart(ttl1, tr, 0.1)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), run_time=0.5)
            self.play(FadeIn(ttl1, shift=DOWN * 0.1), FadeIn(a_node, scale=0.9), FadeIn(lr), run_time=0.5)
            for lk, c in zip(links, tools):
                self.play(Create(lk), FadeIn(c, shift=DOWN * 0.1), run_time=0.35)
            self.play(FadeIn(grow, shift=UP * 0.08), run_time=0.4)
            vo.wait_until("The lecture contrasts one agent")
            self.play(pulse(a_node.frame, CLOUD), run_time=0.75)
            vo.wait_until("with a graph of agents")
            self.play(FadeIn(ttl2, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("a manager calling agents as tools")
            self.play(FadeIn(m_lbl), FadeIn(m_node, scale=0.9), run_time=0.4)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(e), FadeIn(sp, shift=RIGHT * 0.15))
                                    for e, sp in zip(edges, specs)], lag_ratio=0.25), run_time=0.9)
            self.play(FadeIn(tcall, shift=UP * 0.08), run_time=0.35)
            vo.wait_until("or peers handing off")
            self.play(FadeIn(p_lbl), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in peers], lag_ratio=0.2),
                      FadeIn(VGroup(*p_ar, *p_hand)), FadeIn(baton), run_time=0.7)
            for p in peers[1:]:
                self.play(baton.animate.set_x(p.get_center()[0]), run_time=0.45)
            self.play(FadeIn(foot, shift=UP * 0.08), run_time=0.4)

        # ========================================================== 1 · the manager pattern, a workflow for a tool
        mgr = node("customer assistant /\nharness", CLOUD)
        mgr.move_to([-4.95, 1.3, 0])
        wf = RoundedRectangle(width=5.5, height=2.5, corner_radius=0.18, stroke_color=HARNESS,
                              stroke_width=2.5).set_fill(HARNESS, 0.05)
        wf.move_to([3.65, 1.3, 0])
        rail = Rail(mini=True)
        rail.move_to(wf)
        wf_cap = label("act 3 ordering workflow", CAPTION, HARNESS)
        place(wf_cap, cx=wf.get_center()[0], bottom=wf.get_top()[1] + 0.12)
        ya, yb = 1.55, 1.0
        go = arrow([mgr.frame.get_right()[0], ya, 0], [wf.get_left()[0], ya, 0], LOOKUP, stroke=4, buff=0.08)
        go_t = mono(R605[1], CAPTION, LOOKUP)
        place(go_t, cx=go.get_center()[0], bottom=ya + 0.12)
        back = arrow([wf.get_left()[0], yb, 0], [mgr.frame.get_right()[0], yb, 0], HARNESS, stroke=4, buff=0.08)
        back_t = label(R605[3], CAPTION, HARNESS)
        place(back_t, cx=back.get_center()[0], top=yb - 0.12)
        skill = node("tasting-planning skill", HARNESS)
        place(skill, cx=mgr.get_center()[0], top=mgr.get_bottom()[1] - 0.6)
        expl = node("customer-facing\nexplanation", S.GREY)
        place(expl, cx=mgr.get_center()[0], top=skill.get_bottom()[1] - 0.6)
        down = arrow(mgr.frame.get_bottom(), skill.frame.get_top(), S.GREY)
        side = arrow(skill.frame.get_bottom(), expl.frame.get_top(), S.GREY)
        ill1 = illustration_tag("README.md · lines 605–611")
        place(ill1, left=-SAFE, cy=2.55)
        prop = rail.station("propose").frame
        diagram = VGroup(mgr, wf, rail, wf_cap, go, go_t, back, back_t, skill, expl, down, side, ill1)
        for m in diagram:
            inside(m)
        apart(go_t, mgr, 0.1)
        apart(go_t, wf, 0.1)
        apart(back_t, mgr, 0.1)
        apart(back_t, wf, 0.1)
        apart(wf_cap, lr, 0.1)
        apart(ill1, tr, 0.05)
        apart(ill1, go_t, 0.1)
        apart(VGroup(skill, expl), peer_g, 0.2)
        apart(expl, back_t, 0.15)
        apart(VGroup(skill, expl), VGroup(go, back, back_t), 0.2)
        # the morph: the manager node's frame becomes the assistant's, the middle specialist's the
        # workflow box, the middle edge the PINK call; their texts swap in place (old out, then new in)
        sp = specs[1]
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(single), FadeOut(ttl2), FadeOut(m_lbl),
                      FadeOut(VGroup(specs[0], specs[2], edges[0], edges[2])), run_time=0.5)
            self.play(pulse(m_node.frame, CLOUD), ShowFlash(e_mid), run_time=0.75)
            vo.wait_until("except the tool it calls")
            self.play(FadeOut(m_node.text), FadeOut(sp.text), FadeOut(tcall), run_time=0.3)
            self.play(Transform(m_node.frame, mgr.frame), Transform(sp.frame, wf), Transform(e_mid, go),
                      run_time=0.9)
            self.play(FadeIn(mgr.text), FadeIn(go_t, shift=UP * 0.08), FadeIn(ill1), run_time=0.4)
            vo.wait_until("the one from act 3")
            self.play(FadeIn(rail), FadeIn(wf_cap, shift=DOWN * 0.08), run_time=0.6)
            self.play(GrowArrow(back), FadeIn(back_t, shift=UP * 0.08), run_time=0.5)
            vo.wait_until("with a model inside one node")
            self.play(pulse(prop, CLOUD, 9), run_time=0.75)
            self.play(GrowArrow(down), FadeIn(skill, shift=DOWN * 0.1), run_time=0.45)
            self.play(GrowArrow(side), FadeIn(expl, shift=DOWN * 0.1), run_time=0.45)
            vo.wait_until("No handoffs")
            self.play(FadeOut(peer_g), run_time=0.6)
        # (the morphed mobjects stand for their targets from here on)
        pic1 = VGroup(m_node.frame, mgr.text, sp.frame, e_mid, go_t, rail, wf_cap, back, back_t, down, skill,
                      side, expl, ill1)

        # ========================================================== 2 · step 1: the notebook cell builds it; the budget
        p619 = src_panel(RD, 619, 624, size=20, language="python")
        place(p619, left=-6.35, top=TOP)
        b622 = p619.bar(622, TURN, 0.2)
        s622 = p619.span(622, R622)
        hdr = _header_text(f"{CL} · lines 22–26")
        chips = [chip(s, HARNESS, size=CAPTION, font=MONO, pad_y=0.06) for _, s, _ in BUDGET]
        col = VGroup(*chips).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        place(hdr, left=-6.25, top=p619.get_bottom()[1] - 0.3)
        place(col, left=-6.35, top=hdr.get_bottom()[1] - 0.12)
        nx = col.get_right()[0] + 0.4
        notes = {}
        for (n, _, txt), c in zip(BUDGET, chips):
            if txt:
                notes[n] = place(label(txt, CAPTION, S.GREY), left=nx, cy=c.get_center()[1])
        for m in (p619, hdr, col, *notes.values()):
            inside(m)
        apart(p619, tr, 0.05)
        ch = dict(zip((n for n, _, _ in BUDGET), chips))
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(pic1), FadeOut(lr), run_time=0.5)
            self.play(tr.goto(1), run_time=0.5)
            self.play(FadeIn(p619, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("builds it")
            self.play(FadeIn(b622), s622.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("The budget")
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in chips], lag_ratio=0.12),
                      run_time=0.8)
            for anchor, n in (("16 outer model calls", 22), ("20 tool calls", 23), ("8 proposer calls", 25),
                              ("and one shared 180-second clock", 24)):
                vo.wait_until(anchor)
                anims = [flash(ch[n], HARNESS, 1.08)]
                if n in notes:
                    anims.append(FadeIn(notes[n], shift=LEFT * 0.1))
                self.play(*anims, run_time=0.5)
        pic2 = VGroup(p619, b622, hdr, col, *notes.values())

        # ========================================================== 3 · the host confirms; the model picks an ID; narrow tools
        p15 = src_panel(A6, [15, (17, 19), (23, 24)], wrap={18: ['"request-2"']}, size=20)
        place(p15, left=-6.35, top=TOP)
        b15 = p15.bar(15, TURN, 0.2)
        b18 = p15.bar(18, HARNESS, 0.18)
        r18 = p15.rows_of(18)
        ma = VGroup(code_span(p15.code, r18[0], MA), code_span(p15.code, r18[1], MA))
        b24 = p15.bar(24, LOOKUP, 0.2)
        rid = p15.span(24, "request_id")
        row24 = p15.code.code_lines[p15.rows_of(24)[0]]
        handle = chip("request-1", LOOKUP, size=CAPTION, font=MONO)
        place(handle, left=row24.get_right()[0] + 0.45, cy=row24.get_center()[1])
        assert handle.get_right()[0] < p15.get_right()[0] - 0.1, (handle.get_right(), p15.get_right())
        thdr = _header_text(f"{A6} · lines 24, 29, 34")
        tchips = [chip(t_, HARNESS, size=CAPTION, font=MONO) for t_, _ in TOOLS]
        trow = VGroup(*tchips).arrange(RIGHT, buff=0.3)
        narrow = grey_tag("narrow tools")
        place(thdr, left=-6.25, top=p15.get_bottom()[1] - 0.3)
        place(trow, left=-6.35, top=thdr.get_bottom()[1] - 0.26)       # (room for the tag beside the header)
        place(narrow, left=thdr.get_right()[0] + 0.35, cy=thdr.get_center()[1])
        for m in (p15, handle, thdr, trow, narrow):
            inside(m)
        apart(narrow, trow, 0.12)
        apart(p15, tr, 0.05)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(pic2), run_time=0.4)
            self.play(FadeIn(p15, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(b15), p15.span(15, C15).animate.set_color(TURN), run_time=0.5)
            self.play(FadeIn(b18), ma.animate.set_color(HARNESS), run_time=0.5)
            vo.wait_until("the model only picks an ID")
            self.play(FadeIn(b24), rid.animate.set_color(LOOKUP), run_time=0.4)
            self.play(FadeIn(handle, shift=RIGHT * 0.1), run_time=0.45)
            vo.wait_until("Its tools are narrow")
            self.play(FadeIn(thdr), FadeIn(narrow, shift=LEFT * 0.1), run_time=0.4)
            for (t_, _), c, anchor in zip(TOOLS, tchips, ("start order", "get order status", "assess event")):
                vo.wait_until(anchor)
                self.play(FadeIn(c, shift=UP * 0.1), run_time=0.35)
        pic3 = VGroup(p15, b15, b18, b24, handle, thdr, trow, narrow)

        # ========================================================== 4 · step 2: act 6, standard (live: a 401 here)
        t = term(container=True, rows=10)
        ft = frame_tags(t, nokey_tag(), live_tag())
        c637 = top_chip(R637, where="README.md · line 637", expected=True)
        c637.set_y((tr.get_bottom()[1] + ft.get_top()[1]) / 2)          # mid-gap over a 10-row terminal
        apart(c637, tr, 0.3)
        apart(c637, ft, 0.3)
        assert c637.get_bottom()[1] > t.box.get_top()[1] + 0.05
        s5, c5 = STD.out(5)[0]
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(pic3), run_time=0.4)
            self.play(tr.goto(2), FadeIn(t, shift=UP * 0.2), FadeIn(ft[0], shift=DOWN * 0.1), run_time=0.5)
            type_cmd(self, t, STD.cmd, 1.2)
            self.play(FadeIn(ft[1], shift=DOWN * 0.1), run_time=0.3)
            # line 3 prints GREEN; line 5 is cut at the row (not wrapped), the rest fold
            o23 = show(self, t, STD, 2, (STD.line(3), HARNESS), wrap=True, run_time=0.4)
            o5 = show(self, t, STD, (t._cut(s5), c5), 7, 9, STD.as401(10, short=True), wrap=True, run_time=0.5)
            assert len(t.lines) == 10, len(t.lines)
            r3 = item_rows(o23, 1)
            vo.wait_until("tell outer model calls apart")
            r7 = item_rows(o5, 1)[0]
            assert r7.text == STD.line(7), r7.text
            self.play(flash(r7.glyphs, CLOUD, 1.05), run_time=0.6)
            r9 = item_rows(o5, 2)[0]
            self.play(substring(r9, "start_order").animate.set_color(LOOKUP),
                      substring(r9, "get_order_status").animate.set_color(LOOKUP), run_time=0.4)
            self.play(FadeIn(c637, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("the outer agent cannot approve")
            host = wrapped_glyphs(r3, HOST)
            self.play(host.animate.set_color(TURN), run_time=0.4)
            self.play(flash(host, TURN, 1.04), run_time=0.6)

        # ========================================================== 5 · step 3: two orders, one shop (scripted, offline)
        # the picture above the strip: a concierge, two rails, a free shelf space at right
        r1 = Rail(mini=True, layout="line", names=("validate", "review", "place"))
        r2 = Rail(mini=True, layout="line", names=("validate", "review", "place"))
        for rl, y in ((r1, Y1), (r2, Y2)):
            rl.shift(np.array([XV - rl.station("validate").frame.get_center()[0], y - rl.get_center()[1], 0]))
        # Rail(layout="line") draws only the edges of RAIL_EDGES; validate -> review is not one of them
        e_vr = {}
        for rl in (r1, r2):
            a_, b_ = rl.station("validate").frame, rl.station("review").frame
            e_vr[id(rl)] = Arrow(a_.get_right(), b_.get_left(), buff=0.04, color=HARNESS, stroke_width=4,
                                 tip_length=0.16, max_tip_length_to_length_ratio=0.25)
        conc = node("customer\nassistant", CLOUD)
        conc.move_to([-SAFE + conc.width / 2, (Y1 + Y2) / 2, 0])
        starts = [rl.start() for rl in (r1, r2)]
        calls = [arrow(conc.frame.get_right(), rl.station("validate").frame.get_left(), LOOKUP, stroke=3, buff=0.06)
                 for rl in (r1, r2)]
        mid_y = (Y1 + Y2) / 2
        st_names = VGroup()
        for name, txt in (("validate", "validate"), ("review", "manager\nreview"), ("place", "revalidate\n& place")):
            nm = VGroup(*[label(s, CAPTION, INK) for s in txt.split("\n")]).arrange(DOWN, buff=0.04)
            nm.move_to([r1.station(name).frame.get_center()[0], mid_y, 0])
            st_names.add(nm)
        yb1, yb2 = Y1 + BAND, Y2 - BAND
        reqs = [mono("request-1", CAPTION, LOOKUP), mono("request-2", CAPTION, LOOKUP)]
        for rq, yb in zip(reqs, (yb1, yb2)):
            place(rq, right=XV - 0.95, cy=yb)
        amts = [mono(SUB, CAPTION, HARNESS).move_to([XV, yb, 0]) for yb in (yb1, yb2)]
        # the approval ticket is the harness's (GREEN, as S09's); the check beside it is the human's (YELLOW)
        tks = [chip("ticket", HARNESS, size=CAPTION).move_to([r1.station("review").frame.get_center()[0], yb, 0])
               for yb in (yb1, yb2)]
        cks = [check_mark(0.28, TURN).next_to(tk, RIGHT, buff=0.18) for tk in tks]
        ill5 = illustration_tag()
        place(ill5, left=-2.25, cy=3.27)            # the top band right of the tracker (the shelf takes the right)
        rails_g = VGroup(r1, r2, *e_vr.values(), conc, *calls, st_names, *reqs)
        for m in (rails_g, *amts, *tks, *cks, ill5):
            inside(m)
        for a_, b_ in ((reqs[0], amts[0]), (amts[0], tks[0]), (reqs[1], amts[1]), (amts[1], tks[1]),
                       (st_names, r1), (st_names, r2), (st_names, conc), (reqs[0], tr), (tks[0], tr)):
            apart(a_, b_, 0.08)
        assert max(m.get_bottom()[1] for m in (*amts, *tks, *reqs)) > STRIP_TOP + 0.15
        toks = [new_token(), new_token()]
        for tk_, s in zip(toks, starts):
            tk_.move_to(s)
        ft5 = None
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(c637), FadeOut(ft), tr.goto(3), run_time=0.4)
            fit(self, t, 3, keep=0, run_time=0.6)
            strip = t
            ft5 = frame_tags(strip, scripted_tag(), offline_tag())
            self.play(FadeIn(ft5, shift=DOWN * 0.1), FadeIn(rails_g), FadeIn(ill5), run_time=0.5)
            vo.wait_until("two orders sharing one shop")
            c5 = type_cmd(self, strip, TWO.cmd, 1.0)
            assert [r.text for r in c5.rows][1] == TWO_ROWS[1], [r.text for r in c5.rows]
            row2 = c5.rows[1]
            k = row2.text.index("--manager-decision approve")
            ol = col_box(row2, k, k + len("--manager-decision approve"), TURN)
            tt = beside(test_tag(), strip, row2)
            pin(self, row2, ol, run_time=0.3, anim=Create(ol))
            pin(self, row2, tt, run_time=0.3)
            self.wait(0.3)
            # the strip prints the run in turn; each request's token runs its rail with it
            new, an, done = feed(strip, TWO.out(5))
            self.play(*an, run_time=0.4)
            done()
            self.play(substring(new[0], "approve").animate.set_color(TURN), run_time=0.25)
            for i, (rl, tok, (la, lb), lv, lp) in enumerate(zip(
                    (r1, r2), toks, ((23, 24), (46, 47)), (35, 58), (38, 61))):
                new, an, done = feed(strip, TWO.out(la, lb))
                self.play(*an, ShowFlash(calls[i], LOOKUP), FadeIn(tok, shift=RIGHT * 0.3), run_time=0.5)
                done()
                new, an, done = feed(strip, [(TWO.line(lv), HARNESS)])
                gap = rl.spot("validate")
                self.play(*an, ride(tok, path_of([tok.get_center(), gap]), 0.6), run_time=0.6)
                done()
                self.play(*tint(tok, HARNESS), FadeIn(amts[i], shift=UP * 0.08 if i == 0 else DOWN * 0.08),
                          run_time=0.3)
                new, an, done = feed(strip, TWO.out(lp))
                tok.set_z_index(2)                       # it waits ON "manager review", off the amber track
                rv = rl.station("review").frame.get_center()
                self.play(*an, *rl.freeze("review"), e_vr[id(rl)].animate.set_color(AMBER),
                          ride(tok, path_of([tok.get_center(), rv]), 0.5),
                          FadeIn(tks[i], shift=DOWN * 0.08 if i == 0 else UP * 0.08), run_time=0.5)
                done()
            vo.wait_until("and the test decision approves both")
            self.play(LaggedStart(*[FadeIn(c, scale=1.3) for c in cks], lag_ratio=0.3), run_time=0.6)

        # ========================================================== 6 · one shelf: request-1 placed, request-2 blocked
        shelf = StockShelf((("Mimolette", 3000), ("Taleggio", 3000), ("Comté", 6000)), cap=6000, bar_w=2.6)
        place(shelf, right=SHELF_RIGHT, top=3.3)
        rec_rows = [C18.fold(2, 2, "… product_id | … | stock_g …"),
                    C18.fold(4, 4, "… comte | … | 6000 …"),
                    C18.fold(7, 7, "… mimolette | … | 3000 …"),
                    C18.fold(9, 9, "… taleggio | … | 3000 …")]
        rec = recorded_box("colab-c18-data-constraints", *rec_rows)
        place(rec, right=SHELF_RIGHT, top=shelf.get_bottom()[1] - 0.25)
        need = [shelf.need(n, NEED) for n in ("Mimolette", "Taleggio")]
        ok_c = check_mark(0.26, HARNESS)
        c_name = shelf.rows[2][0]
        place(ok_c, right=c_name.get_left()[0] - 0.15, cy=shelf.frames["Comté"].get_center()[1])
        reds = VGroup(*[mono(TWO.line(n).strip(), CAPTION, ERR) for n in (190, 191)]).arrange(DOWN, buff=0.12,
                                                                                         aligned_edge=LEFT)
        place(reds, right=SAFE, bottom=STRIP_TOP + 0.19)
        ponder = chip("the act 3 ponder · for real", TURN, size=CAPTION)
        place(ponder, right=SAFE, bottom=reds.get_top()[1] + 0.25)
        for m in (shelf, rec, reds, ponder, ok_c):
            inside(m)
        for a_, b_ in ((shelf, rails_g), (shelf, rec), (shelf, ill5), (reds, r2), (reds, reqs[1]), (reds, amts[1]),
                       (reds, tks[1]), (ponder, rails_g), (ponder, shelf), (ok_c, ill5)):
            apart(a_, b_, 0.08)
        apart(reds, cks[1], 0.15)                           # (request-2's check, right above the RED lines)
        for part in (rec.frame, rec.header, rec.tag):       # (the box's bounding box is an L: check its parts)
            for b_ in (r1, r2, st_names, *calls):
                apart(part, b_, 0.08)
        places = [rl.station("place").frame for rl in (r1, r2)]
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(shelf, shift=LEFT * 0.15), run_time=0.6)
            self.play(FadeIn(rec, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("at 3,000 grams each")
            self.play(flash(shelf.value("Mimolette"), HARNESS, 1.15), flash(shelf.value("Taleggio"), HARNESS, 1.15),
                      run_time=0.6)
            # request-1: approved, revalidated, placed
            vo.wait_until("Request 1 is placed")
            self.play(flash(cks[0], TURN, 1.4), *r1.unfreeze("review"), e_vr[id(r1)].animate.set_color(HARNESS),
                      run_time=0.45)
            # from "manager review" it rides ON to "revalidate & place": seen at checkout
            self.play(ride(toks[0], path_of([toks[0].get_center(), places[0].get_center()]), 0.6), run_time=0.6)
            new, an, done = feed(strip, [(TWO.line(80), HARNESS)])
            self.play(pulse(places[0], HARNESS), *an, run_time=0.6)
            done()
            vo.wait_until("leaving 1,400")
            self.play(*shelf.set("Mimolette", LEFT_AFTER), *shelf.set("Taleggio", LEFT_AFTER),
                      *shelf.set("Comté", 6000 - NEED), run_time=0.9)
            # request-2: approved, revalidated, blocked by stock
            vo.wait_until("Request 2 reaches revalidation")
            self.play(FadeOut(rec), run_time=0.3)
            self.play(flash(cks[1], TURN, 1.4), *r2.unfreeze("review"), e_vr[id(r2)].animate.set_color(HARNESS),
                      run_time=0.45)
            self.play(ride(toks[1], path_of([toks[1].get_center(), places[1].get_center()]), 0.7), run_time=0.7)
            vo.wait_until("needing 1,600")
            self.play(*[Create(nd) for nd in need], FadeIn(ok_c, scale=1.2), run_time=0.6)
            vo.wait_until("blocked")
            self.play(*tint(toks[1], ERR), places[1].animate.set_stroke(ERR, 4), run_time=0.4)
            new, an, done = feed(strip, [(TWO.line(92), ERR)])
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in reds], lag_ratio=0.3), *an, run_time=0.5)
            done()
            vo.wait_until("That's the ponder from act 3")
            self.play(FadeIn(ponder, shift=LEFT * 0.1), run_time=0.45)
            vo.wait_until("approval is not placement")
            self.play(*[flash(c, TURN, 1.4) for c in cks], run_time=0.6)
            self.play(pulse(places[0], HARNESS), pulse(places[1], ERR), run_time=0.75)

        # ========================================================== 7 · slide 21's Response: the app renders the answer
        lr21 = lref("21")
        ss = SixSteps()
        # slimmer chips (text unchanged) and the seam cut to them: the 12-row terminal's top edge and
        # its title-bar tags are right under the strip
        for c in ss.chips.values():
            c.box.stretch_to_fit_height(0.4)
        chips6 = VGroup(*ss.chips.values())
        sx = ss.seam_x()
        ss.remove(ss.seam)
        ss.seam = DashedLine([sx, chips6.get_top()[1], 0], [sx, chips6.get_bottom()[1], 0],
                             color=LOOKUP, stroke_width=4, dash_length=0.08)
        ss.add(ss.seam)
        t12_top = strip_top(12)
        tags_up = ft5.get_top()[1] - strip.box.get_top()[1]          # the tags straddle the top edge
        place(ss, cx=0.0, bottom=t12_top + tags_up + 0.15)
        inside(ss)
        apart(ss, tr, 0.04)
        apart(ss, lr21, 0.04)
        pic5 = VGroup(rails_g, *amts, *tks, *cks, *toks, ill5, shelf, *need, ok_c, reds, ponder)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(pic5), run_time=0.5)
            fit(self, strip, 12, tags=list(ft5), run_time=0.8)
            t = strip
            vo.wait_until("the lecture's response step")
            self.play(FadeIn(ss, shift=DOWN * 0.1), FadeIn(lr21), run_time=0.5)    # the tag comes with its picture
            self.play(ss.light("Response", HARNESS), run_time=0.4)
            vo.wait_until("the app checks the model's plan")
            plan = show(self, t, TWO, 152, *[TWO.cut(n, PLAN_CUT) for n in (158, 159, 160)], run_time=0.6)
            vo.wait_until("and fills in quantities")           # the quantities came from the receipt
            qty = VGroup(*[substring(r, PLAN_CUT) for r in plan[1:]])
            self.play(qty.animate.set_color(HARNESS), run_time=0.5)
            vo.wait_until("and the status, placed")
            r170 = show(self, t, TWO, (TWO.line(170), HARNESS), run_time=0.35)[0]
            vo.wait_until("from the receipt")
            tg170 = beside(grey_tag("filled in by the app from the receipt"), t, r170)
            pin(self, r170, tg170, run_time=0.4)
            vo.wait_until("The blocked order says")
            o184 = show(self, t, TWO, 175, 183, (TWO.line(184), ERR), wrap=True, run_time=0.5)
            r184 = item_rows(o184, 2)
            # slim, and a hair above its row's centre: the YELLOW box round the next two rows stays clear
            # (the row above has no descenders)
            gchip = slim_tag(f"one message for both cases ({GOV} · line 75)", pad_y=0.025)
            beside(gchip, t, r184[-1])
            gchip.shift(UP * 0.02)
            pin(self, r184[-1], gchip, run_time=0.45)
            vo.wait_until("the stock lines below give the reason")
            o190 = show(self, t, TWO, 190, 191, run_time=0.4)
            yb = rows_box(o190[:2])
            apart(yb, gchip, 0.07)
            rs = grey_tag("the reason")
            place(rs, left=yb.get_right()[0] + 0.3, cy=yb.get_center()[1])
            assert rs.get_right()[0] < t.box.get_right()[0] - 0.12
            pin(self, o190[1], yb, run_time=0.4, anim=Create(yb))
            pin(self, o190[1], rs, run_time=0.35)
            show(self, t, TWO, 193, run_time=0.3)
            assert len(t.lines) == 12 and t.lines[0].text == TWO.line(152), [r.text for r in t.lines]

        # ========================================================== 8 · slide 36: a hybrid, inside out; the map; your turn
        lr36 = lref("36, 22")
        sp = Spectrum(width=12.2)
        sp.move_to([0, -0.3, 0])
        PIC_H = 1.25
        pics = {0: rule_graph(), 1: act3_rail(2.0), 2: act6_graph(), 3: agent_graph()}
        for i, pic in pics.items():
            pic.move_to(sp.above(i, PIC_H))
        pics[1].set_opacity(0.45)                       # act 3's own place (S08), dimmed
        a6 = pics[2]
        hyb = label("hybrid · inside out", CAPTION, INK)
        place(hyb, cx=a6.get_center()[0], bottom=a6.get_top()[1] + 0.18)
        c662 = top_chip(R662, where="README.md · line 662")
        c662.shift(DOWN * 0.14)                         # (its left end runs under the tracker's caption)
        mm = BoundaryMini(MINI_CENTER, upto=5)
        mcap = label("Sub agents ← narrow tools · separate counters · one clock", CAPTION, HARNESS)
        mcap.move_to([mm.frame.get_left()[0] - 0.2 - mcap.width / 2, mm.rows["sub"][0].get_center()[1], 0])
        for m in (sp, *pics.values(), hyb, c662, mcap):
            inside(m)
        inside(mm, -6.6, 6.6, -3.6, 3.6)              # (the map's own home touches the safe frame)
        apart(hyb, c662, 0.15)
        apart(sp, mm, 0.1)
        apart(sp, mcap, 0.1)
        apart(c662, lr36, 0.02)
        apart(c662, tr, 0.12)
        for i in range(3):
            apart(pics[i], pics[i + 1], 0.3)
        wk = label("with your key", CAPTION, COST)
        off = label("offline · free", CAPTION, HARNESS)
        tc_w = max(mono(STD.cmd, CAPTION).width + 0.35 + wk.width,
                   mono(TWO_ROWS[1].strip(), CAPTION).width + 4 * cell_width(CAPTION) + 0.35 + off.width) + 0.6 + 0.3
        tc = turn_card([
            STD.cmd,
            "\n".join(TWO_ROWS),
            (Prose("act 6 live · billed per token"), COST),
        ], width=tc_w)
        place(wk, left=tc.rows[0].get_right()[0] + 0.35, cy=tc.rows[0].get_center()[1])
        r2nd = tc.rows[1][1]
        r2nd.shift(RIGHT * 4 * cell_width(CAPTION))     # the continuation row's indent, as typed
        place(off, left=r2nd.get_right()[0] + 0.35, cy=r2nd.get_center()[1])
        tc.add(wk, off)
        place(tc, cx=0, cy=-0.2)
        inside(tc)
        assert off.get_right()[0] < tc.frame.get_right()[0] - 0.1 and wk.get_right()[0] < tc.frame.get_right()[0] - 0.1
        apart(wk, tc.tag, 0.04)
        apart(tc, tr, 0.05)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(t, ft5, ss)), FadeOut(lr21), run_time=0.6)
            self.play(FadeIn(sp), LaggedStart(*[FadeIn(pics[i], shift=UP * 0.1) for i in range(4)], lag_ratio=0.2),
                      FadeIn(mm), FadeIn(lr36), run_time=1.0)
            vo.wait_until("it's a hybrid")
            self.play(sp.light(2), FadeIn(hyb, shift=UP * 0.08), run_time=0.5)
            vo.wait_until("inside out")
            self.play(FadeIn(c662, shift=DOWN * 0.1), mm.light("sub"), run_time=0.45)
            self.play(mm.add_bar("sub"), FadeIn(mcap, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("the agent outside")
            self.play(pulse(a6.agent, CLOUD, 7), run_time=0.75)
            vo.wait_until("the fixed graph as its tool")
            self.play(ShowFlash(a6.call), outline_flash(a6.rail, HARNESS, 0.08), run_time=0.7)
            vo.wait_until("Pause and run")
            self.play(FadeOut(VGroup(sp, *pics.values(), hyb, c662, mm, mcap)), FadeOut(lr36), run_time=0.5)
            self.play(FadeIn(tc, scale=0.97), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tc, tr)), run_time=0.8)
        self.wait(0.3)

