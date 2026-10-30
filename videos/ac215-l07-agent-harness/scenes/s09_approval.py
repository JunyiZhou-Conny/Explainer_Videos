"""S09 · Act 3: approve this exact cart (README "3 · Harness › Act 3", steps 4-6, and one extra).
Lecture: 22–23.

Beats (script.md "## S09", one voiceover block each):
 0  TRACKER Act3 4. LECTURE 22–23 with slide 23's banner, redrawn as a GREEN dashed strip in the
    top band: "set boundaries carefully — permissions · sandboxing · budgets · checks". The
    container terminal (12 rows, TEAL; title-bar tags `scripted` + GREEN `offline · free`, which
    flash on "is scripted") types `python cli.py --act 3 --fixture --scenario manager-approval` ->
    container/33 lines 11–14, 16; on "60 guests in New York" the GREY tag "the ask (line 8): 60 guests ·
    NY · $300 budget" pins beside row 11; then 20, 23–26. On "a valid cart" line 16 turns GREEN and the
    review's "$220.80" lights; on "above the 200 dollar threshold" the banner and its lecture tag
    leave and the top-band chip README.md · line 359 "Manager approval is required for a cheese
    subtotal greater than $200" arrives.
 1  The chip leaves; line 28 prints cut after "decline: " (the prompt row scrolls away) and the
    terminal shrinks to the strip (lines 26 and 28). V5 as a mini rail (glyph-only, tag
    illustration) top right: the token waits at "manager review", which freezes amber with the
    PURPLE tag `request_info` above it; "you · the manager" (a YELLOW person and hand) arrives left
    of it. On "the host answers" CODE(formaggio/agents/workflow_steps.py: 129–130) arrives above
    the strip and line 129's comment gets a YELLOW bar. On "Type approve" the strip types
    `approve` in YELLOW and the rail thaws.
 2  The strip, rail, person and panel leave together, then (old out, new in) the approval ticket
    (V5's Ticket, laid out as three rows of slots in reading order) builds top left and
    CODE(formaggio/shop/checkout.py: 31–36) arrives at the bottom. As the SAY names request,
    items, subtotal, policy and product attributes, lines 31–35 get GREEN bars and each field's
    chip writes into its slot (the faint slot outline goes); the PINK hash `e8caf06b29df9c58 …`
    (container/71 line 46) prints with the GREY note "same cart, same data · your run prints this
    hash too". On "Stock is left out on purpose" `exclude={"stock_g"}` gets a YELLOW box and the
    `stock_g` chip appears crossed out right of the ticket; on "it's rechecked" the excerpt chip
    formaggio/shop/checkout.py · line 29 "Inventory is rechecked, not approved." arrives above it.
 3  The chips and panel leave; the rail returns top right and the cart token rolls onto
    "revalidate & place" (it stays visible there); a PINK re-hash comes out under the station
    and slides down, then along under the ticket (never across it) to sit under the ticket's
    hash. CODE(formaggio/shop/checkout.py: 84–87) arrives at the bottom; the three conditions
    get YELLOW outlines and GREEN checks as the SAY names them (decision == "approve";
    checkout_key, with the GREY caption "this checkout (the order's own key)" above the header and a
    GREY elbow pointer down the free column to the right-hand checkout_key; fingerprint: both
    hashes flash and the re-hash gets a GREEN check). On "Change one line" the panel leaves, then
    the what-if row (tag `illustration · what if`): a YELLOW `items` chip with a pencil -> a different
    hash; on "and the hashes differ" a RED ≠ and "not approved"; it holds 1 s, leaves, and the
    real run goes on: the strip returns and prints container/33 lines 30, 32–34 (tag `your
    numbers will differ` on the receipt row), and the token becomes the GREEN receipt card.
 4  A stopwatch "active time" (tag illustration) and the chip README.md · line 444 (excerpt)
    "excluding manager wait time" arrive; the stopwatch runs, the YELLOW hand moves over the
    ticket and the stopwatch stops (grey); the hand taps, "approve", and it runs again.
 5  The stopwatch, hand, chip, receipt and re-hash leave. TRACKER Act3 4 · extra. The strip types
    the same command again (tag extra on its prompt row) -> container/34 line 28 cut after
    "decline: ", `decline` typed YELLOW, lines 31 (RED) and 32.
 6  The declined lines stay a moment, then the strip leaves. A what-if: the approved cart waits
    before "revalidate & place" (the ticket's hash row gets a GREEN check); the rail's tag becomes
    `illustration · what if` (old out, then new in); a GREEN shelf with two bars, Mimolette and
    Taleggio (no numbers), and a second BLUE cart token rolls in from off-screen right along the
    Mimolette row and stops right of its bar with a "?". The station outline flashes on "What does checkout do". PONDER (8 s); the picture never
    shows the answer.
 7  The card leaves. The second token drains the Mimolette bar and leaves; the approved cart rolls
    onto "revalidate & place" (the hash check pulses: still matching); on "finds a stock
    violation" the 1,600 g it needs shows as a RED dashed outline past the bar and a RED stamp
    "stock violation"; on "and blocks" the token and station turn RED, RED "blocked" beside it,
    and the excerpt chip formaggio/agents/workflow_steps.py · lines 155–158. On "Stock isn't in
    the fingerprint" the ticket's hash and check pulse and the excerpt chip of line 29 arrives;
    then the caption "an approval authorizes a decision · it doesn't reserve stock"; on "it doesn't
    reserve anything" a RED outline flash round the Mimolette bar; on "Act 6" the GREY chip "act 6
    runs this for real".
 8  TRACKER Act3 5. Everything else leaves. Container terminal (12 rows; `scripted`, `offline ·
    free`) types `python cli.py --act 3 --fixture --scenario out-of-stock` -> container/35 lines
    11–14, 16 (RED, on "so attempt 1 fails"), 25–26 (YELLOW, on "One bounded revision"), 28 (GREEN,
    on "and the order places", then 35 "Order placed." GREEN: valid, then placed), 45 with the GREY
    tag "scripted: no model" (on "with zero model calls").
 9  TRACKER Act3 6. The terminal leaves. CODE(README.md: 423–430), line 427 YELLOW. Under it the
    README's layer table (lines 439–440) as two GREEN rings around a mini rail (tag illustration):
    `WorkflowBudget(model_calls=8, seconds=120)` and `WorkflowTrace()`, each with its
    `.without(...)` chip; inside them the padlocked ring "validation · authorization · approval ·
    final revalidation". On "can come off" the chips flash and both rings lift off; on
    "validation, approval" the padlocked ring flashes; on "are graph and checkout rules" the
    excerpt chip README.md · line 444 "graph/checkout rules, so neither layer can remove them".
10  The panel and rings leave. The checkpoint chip README.md · line 448; the V1 mini-map with
    LECTURE 22 (it leaves with the map): Control flow lights YELLOW, its GREEN cell gains a bar,
    caption "Control flow ← the workflow graph"; on "and checkout revalidates" Verification, its
    bar and "Verification ← validate · revalidate" (both captions stay, each beside its own row).
    On "Pause and run" everything but the tracker
    leaves and the static "your turn" card arrives (manager-approval: approve, then again with
    decline · out-of-stock · notebook cell: Colab or Jupyter · GREEN "offline · free"). Hold 2 s,
    then fade to an empty frame.
"""

import hashlib

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Circumscribe,
    FadeTransform,
    GrowArrow,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    Mobject,
    Rectangle,
    RoundedRectangle,
    SurroundingRectangle,
    Text,
    Transform,
    UpdateFromAlphaFunc,
    VGroup,
    VMobject,
    linear,
    smooth,
)

from common import *  # noqa: F401,F403
from common import _set_op
from explainer import style as S
from explainer.devops import MONO, box, check_mark, chip, label, mono, substring
from explainer.scene import VoiceScene

SAY = NARRATION["S09"]

# ------------------------------------------------------------------ the real captures (file line numbers)
MGR = capture("container/33")
DEC = capture("container/34")
OOS = capture("container/35")
C71 = capture("container/71")
assert MGR.cmd == DEC.cmd == "python cli.py --act 3 --fixture --scenario manager-approval", MGR.cmd
assert OOS.cmd == "python cli.py --act 3 --fixture --scenario out-of-stock", OOS.cmd
assert len(P_CTR) + 1 + len(MGR.cmd) > 65          # the command folds: prompt row + command row
assert MGR.line(16) == "Cart attempt 1: valid; $220.80"
assert MGR.line(20).startswith("MANAGER REVIEW — ticket c48487091d824bd5a2575417247c17a1")
SUB23 = "$220.80"
assert MGR.line(23).strip() == f"4800 g; cheese subtotal {SUB23}"
ASK = "decline: "
ASK8 = "the ask (line 8): 60 guests · NY · $300 budget"
assert "for 60 guests in NY on a $300.00 budget" in MGR.line(8)
assert MGR.line(28).endswith(ASK + "approve") and DEC.line(28).endswith(ASK + "decline")
assert MGR.line(30) == "Step: revalidate_and_place"
assert MGR.line(32).startswith("--- WORKFLOW PLACED — run " + RUN_MANAGER)
assert MGR.line(33) == "Order placed."
RECEIPT = MGR.line(34).split()[-1]
assert MGR.line(34) == f"Receipt: {RECEIPT}"
assert DEC.line(31).startswith("--- WORKFLOW DECLINED — run ")
assert DEC.line(32) == "Manager declined this cart. No order placed."
assert OOS.line(16) == "Cart attempt 1: stock: munster — Requested 300 g; available 0 g."
assert OOS.line(25).strip() == "Removed: Munster (munster) — 300 g"
assert OOS.line(26).strip() == "Added: Époisses (epoisses) — 300 g"
assert OOS.line(28) == "Cart attempt 2: valid; $50.10"
assert OOS.line(35) == "Order placed."
assert OOS.line(45) == "Proposal attempts: 2. Model calls: 0."
# the hash: the first 16 characters of this run's fingerprint (container/71 inspects run RUN_MANAGER)
assert "approval.decided" in C71.line(46) and f'"fingerprint": "{FINGERPRINT16}' in C71.line(46)
assert "c48487091d824bd5a2575417247c17a1" in C71.line(46)

# ------------------------------------------------------------------ sources (exact sub-strings, checked)
WS = "formaggio/agents/workflow_steps.py"
CO = "formaggio/shop/checkout.py"
R359 = "Manager approval is required for a cheese subtotal greater than $200"
assert R359 in source_line("README.md", 359).replace("**", "")
C129 = "The external host supplies the response; the agent cannot."
assert C129 in source_line(WS, 129) and "ctx.request_info(" in source_line(WS, 130)
INV29 = "Inventory is rechecked, not approved."
assert INV29 in source_line(CO, 29)
FIELD_KEYS = ('"request"', '"items"', '"subtotal_cents"', '"policy"', '"products"')
for _n, _k in zip(range(31, 36), FIELD_KEYS):
    assert source_line(CO, _n).strip().startswith(("payload = {" + _k) if _n == 31 else _k), _n
EXC35 = 'exclude={"stock_g"}'
assert EXC35 in source_line(CO, 35)
COND85 = 'ticket.decision == "approve"'
COND86A = "ticket.checkout_key == checkout_key"
COND86B = "ticket.fingerprint == fingerprint"
assert COND85 in source_line(CO, 85) and COND86A in source_line(CO, 86) and COND86B in source_line(CO, 86)
BLOCK158 = "Final checkout blocked: {exc} No order placed."
assert "except PolicyBlocked" in source_line(WS, 155) and BLOCK158 in source_line(WS, 158)
R444A = "excluding manager wait time"
R444B = "graph/checkout rules, so neither layer can remove them"
assert R444A in source_line("README.md", 444) and R444B in source_line("README.md", 444)
R448 = "what an approval is bound to and why checkout must revalidate"
assert R448 in source_line("README.md", 448)
R427 = 'lesson = build_act3(fixture=True, scenario="out-of-stock")'
assert source_line("README.md", 427) == R427
TRACE439, BUDGET440 = "WorkflowTrace()", "WorkflowBudget(model_calls=8, seconds=120)"
WO_TRACE, WO_BUDGET = '.without("trace")', '.without("budget")'
assert f"`{TRACE439}`" in source_line("README.md", 439) and f"lesson{WO_TRACE}" in source_line("README.md", 439)
assert f"`{BUDGET440}`" in source_line("README.md", 440) and f"lesson{WO_BUDGET}" in source_line("README.md", 440)
assert source_line("README.md", 448).startswith("**Checkpoint:**")

# the what-if hash (an illustration: any one-line change gives an unrelated SHA-256)
WHATIF16 = hashlib.sha256(b"illustration: one cart line changed").hexdigest()[:16]
assert WHATIF16[:4] != FINGERPRINT16[:4]

PONDER = ("The manager approves. Before checkout runs, another order takes most of the Mimolette.\n"
          "What does checkout do —\nand why doesn't the approval protect this order?")

# ------------------------------------------------------------------ layout
SAFE = 6.45
TOP = 2.86              # content top under the tracker (its bottom is 2.97)
RAIL_RIGHT = 6.35       # the mini rail's home: top right
BAND_Y = TOPCHIP_Y      # the one-line band above a 12-row terminal (top 2.19)
STOCK = {"Mimolette": 3000, "Taleggio": 3000}    # c18 stock_g 3000 (as in act 6, container/61)
NEED, LEFT_AFTER = 1600, 1400                     # this cart's 1,600 g; what another order leaves
SHELF_CAP = 3200                                  # the bars' scale (no numbers on screen): 3,000 g nearly full


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
    txt = getattr(mob, "text", None)                 # (a Text's own .text is its string)
    return Indicate(txt if isinstance(txt, Mobject) else mob, color=color, scale_factor=k)


def outline_flash(m, color: str = TURN, buff: float = 0.07):
    """A stroke-only flash round m (Circumscribe): nothing filled covers it."""
    return Circumscribe(m, color=color, buff=buff, fade_out=True, stroke_width=4)


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
    """Animations: a cart_token glyph turns `color` (strokes, the basket's tint, the wheels)."""
    out = []
    for m in tok.glyph.family_members_with_points():
        if type(m).__name__ == "Dot":
            out.append(m.animate.set_fill(color, 1).set_stroke(color))
        else:
            out.append(m.animate.set_stroke(color).set_fill(color, m.get_fill_opacity()))
    return out


def new_token(color: str = CLOUD):
    t = cart_token(color=color, scale=0.8)
    t.set_z_index(-1)                    # under the station boxes: it tunnels through them
    return t


def reveal(m, **kw):
    """FadeIn of a piece member kept at opacity 0 (its saved opacities come back first)."""
    _set_op(m)
    return FadeIn(m, **kw)


def home_rail() -> Rail:
    """V5 as a glyph-only mini rail at its home, top right (stations named by my own labels)."""
    rl = Rail(mini=True)
    rl.shift(RIGHT * (RAIL_RIGHT - rl.get_right()[0]) + UP * (TOP - rl.get_top()[1]))
    return rl


def st_label(rl, name: str) -> Text:
    """The station's name under it (RAIL_SHORT), 20 pt."""
    return label(RAIL_SHORT[name], CAPTION, INK).next_to(rl.station(name).frame, DOWN, buff=0.1)


def unfreeze_now(rl, name: str):
    """rl.unfreeze(name), applied at once (the rail is off screen)."""
    g = rl.station(name)
    g.frame.set_stroke(HARNESS, 3)
    g.tint.set_fill(HARNESS, 0.12)
    for e in rl.edges:
        if e is not None and e is not rl.loop:
            e.set_color(HARNESS)


def code_box(p, n: int, sub: str, color: str = TURN):
    """A YELLOW outline round a sub-string of code line n (an outline hides nothing)."""
    return SurroundingRectangle(p.span(n, sub), color=color, buff=0.04, stroke_width=2.5, corner_radius=0.04)


def two_row_note(rows, color: str = S.GREY) -> VGroup:
    """A GREY tag in two rows (a one-row tag would be 7.4 wide). .box .rows"""
    t = VGroup(*[label(r, CAPTION, color) for r in rows]).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    b = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.22, corner_radius=0.16,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.rows = b, t
    return g


def neq(color: str = ERR) -> VGroup:
    """A RED ≠ drawn (the serif font's ≠ is thin at 20 pt)."""
    a = Line([-0.16, 0.07, 0], [0.16, 0.07, 0])
    b = Line([-0.16, -0.07, 0], [0.16, -0.07, 0])
    s = Line([0.09, 0.2, 0], [-0.09, -0.2, 0])
    return VGroup(a, b, s).set_stroke(color, 4)


class FlatTicket(Ticket):
    """V5's approval ticket (common.Ticket: the same parts, slot chips and animations), laid out
    for this scene: the five slots in three rows, in reading order (request · items /
    subtotal_cents · policy / products), under the title and the SHA-256 row under them, about
    5.85 x 3.0 instead of 5.2 x 3.6 wide-and-tall, so the ticket and a code panel fit one above the
    other and a 6.6-wide excerpt chip fits beside it. The `stock_g` chip (part "excluded") sits
    right of the card at the products row; its "rechecked, not approved" note is dropped (the
    excerpt chip of checkout.py line 29 says it). .sha .row_y"""

    ROWS = ((0, 1), (2, 3), (4,))

    def __init__(self):
        super().__init__()
        fr = self.frame
        self.shift(-fr.get_center())
        tint_, ttl = self.parts["card"][1], self.parts["card"][2]
        pad, gap, sh, cap_gap = 0.22, 0.1, 0.42, 0.12
        hgap = 0.2                                          # between two slots in a row
        ws = [chip(f, HARNESS, size=CAPTION, font=MONO, pad_y=0.04).width + 0.06 for f in TICKET_FIELDS]
        row_w = [sum(ws[i] for i in r) + hgap * (len(r) - 1) for r in self.ROWS]
        hrow = self.parts["hash"]
        hl, hc = hrow[0], hrow[1]
        width = max(max(row_w), hrow.width + 0.7, ttl.width) + 2 * pad
        n = len(self.ROWS)
        height = pad + ttl.height + cap_gap + n * sh + (n - 1) * gap + cap_gap + hrow.height + pad
        fr.become(box(width, height, HARNESS, fill=S.BG, fill_opacity=1.0, stroke=3))
        tint_.become(RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_width=0)
                     .set_fill(HARNESS, 0.06))
        top, left = height / 2, -width / 2
        ttl.move_to([left + pad + ttl.width / 2, top - pad - ttl.height / 2, 0])
        y = top - pad - ttl.height - cap_gap - sh / 2
        self.row_y = []
        for r in self.ROWS:
            x = left + pad
            for i in r:
                # a fresh slot in the old one's place, shaped like the chip that fills it: a faint
                # solid GREY outline (a short dashed pill draws ragged dashes, and GREY dashed reads
                # "lecture only" in this series)
                nb = RoundedRectangle(width=ws[i], height=sh, corner_radius=sh / 2.6, stroke_color=S.GREY,
                                      stroke_width=1.5, stroke_opacity=0.6).set_fill(opacity=0)
                nb.move_to([x + ws[i] / 2, y, 0])
                slots = self.parts["slots"]
                slots.submobjects[slots.submobjects.index(self.slot_frames[i])] = nb
                self.slot_frames[i] = nb
                x += ws[i] + hgap
            self.row_y.append(y)
            y -= sh + gap
        hrow.move_to([left + pad + hrow.width / 2, -height / 2 + pad + hrow.height / 2, 0])
        exg = self.parts["excluded"]
        exg.remove(exg[2])                                  # the note: an excerpt chip says it
        exg.move_to([width / 2 + 0.3 + exg.width / 2, self.row_y[-1], 0])
        self.sha = hl


# ------------------------------------------------------------------ the scene
class ExactCart(VoiceScene):
    def construct(self):
        assert len(SAY) == 11, len(SAY)

        # ========================================================== 0 · step 4: a valid cart above $200
        tr = tracker("Act3", 4)
        lr = lref("22–23")
        ban_t = label("set boundaries carefully — permissions · sandboxing · budgets · checks", CAPTION, INK,
                      t2c={"set boundaries carefully": HARNESS})
        ban_fr = box(ban_t.width + 0.5, ban_t.height + 0.26, HARNESS, dashed=True, stroke=2)
        ban_t.move_to(ban_fr)
        banner = VGroup(ban_fr, ban_t)
        place(banner, cx=0.0, cy=BAND_Y)
        t = term(container=True, rows=12)
        ft = frame_tags(t, scripted_tag(), offline_tag())
        c359 = top_chip(R359, where="README.md · line 359")
        for m in (banner, c359):
            assert m.get_bottom()[1] > t.box.get_top()[1] + 0.05 and m.get_top()[1] < tr.get_bottom()[1] - 0.03
            inside(m)
        apart(banner, lr)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(lr), FadeIn(banner, shift=DOWN * 0.1), run_time=0.6)
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(ft, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("is scripted")
            self.play(flash(ft[0], S.GREY, 1.15), flash(ft[1], HARNESS, 1.1), run_time=0.6)
            type_cmd(self, t, MGR.cmd, 1.0)
            o1 = show(self, t, MGR, (11, 14), 16, run_time=0.6)
            vo.wait_until("60 guests in New York")
            # the ask itself is capture line 8 (the 12 rows are full): a GREY tag on row 11's free right
            ask8 = grey_tag(ASK8)
            pin(self, o1[0], beside(ask8, t, o1[0], buff=0.35), run_time=0.4)
            o2 = show(self, t, MGR, 20, (23, 26), run_time=0.6)
            vo.wait_until("a valid cart")
            self.play(o1[4].glyphs.animate.set_color(HARNESS), run_time=0.4)
            self.play(flash(o1[4].glyphs, HARNESS, 1.06), substring(o2[1], SUB23).animate.set_color(TURN), run_time=0.6)
            vo.wait_until("above the 200 dollar threshold")
            self.play(FadeOut(banner), FadeOut(lr), run_time=0.4)
            self.play(FadeIn(c359, shift=DOWN * 0.1), run_time=0.5)
            self.play(flash(c359.phrase, TURN, 1.04), run_time=0.6)
        r26 = o2[4]

        # ========================================================== 1 · the pause: you are the manager
        rl = home_rail()
        tok = new_token()
        tok.move_to(rl.spot("pairings"))
        lab_rev = st_label(rl, "review")
        ill = illustration_tag()
        place(ill, right=RAIL_RIGHT, cy=3.27)
        rq = chip("request_info", TOOL, size=CAPTION, font=MONO)
        top_row_bottom = rl.station("propose").frame.get_bottom()[1]
        bot_row_top = rl.station("review").frame.get_top()[1]
        rq.move_to([rl.station("review").frame.get_center()[0], (top_row_bottom + bot_row_top) / 2, 0])
        assert rq.get_top()[1] < top_row_bottom - 0.04 and rq.get_bottom()[1] > bot_row_top + 0.04
        pers = person_icon(TURN, height=0.8)
        hnd = hand(TURN, h=0.55)
        you = label("you · the manager", CAPTION, TURN)
        place(pers, cx=0.15, top=2.55)
        hnd.next_to(pers, RIGHT, buff=0.12).align_to(pers, DOWN)
        place(you, cx=VGroup(pers, hnd).get_center()[0], top=pers.get_bottom()[1] - 0.15)
        p129 = src_panel(WS, 129, 130, wrap={129: ["the agent"]}, size=20)
        place(p129, left=-SAFE, top=lab_rev.get_bottom()[1] - 0.12)
        assert p129.get_bottom()[1] > STRIP_TOP + 0.05, p129.get_bottom()
        b129 = p129.bar(129, TURN, 0.2)
        host = VGroup(p129.span(129, "The external host supplies the response;"), p129.span(129, "the agent cannot."))
        for a_, b_ in ((VGroup(pers, hnd, you), rl), (ill, tr), (you, p129), (lab_rev, p129)):
            apart(a_, b_)
        for m in (rl, ill, pers, you, p129):
            inside(m)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(c359), run_time=0.25)
            r28 = show(self, t, MGR, MGR.cut(28, ASK, ellipsis=False), run_time=0.35)[0]
            fit(self, t, 3, keep=[r26, r28], tags=list(ft), run_time=0.6)
            strip = t
            self.play(FadeIn(rl), FadeIn(tok), FadeIn(ill, shift=DOWN * 0.1), FadeIn(lab_rev), run_time=0.4)
            self.play(*rl.freeze("review"), FadeIn(rq, scale=0.9), run_time=0.4)
            vo.wait_until("and you are the manager")
            self.play(FadeIn(pers, shift=RIGHT * 0.15), FadeIn(hnd, shift=RIGHT * 0.15), FadeIn(you), run_time=0.5)
            vo.wait_until("the host answers")
            self.play(FadeIn(p129, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(b129), host.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("Type approve")
            type_after(self, strip, r28, "approve", pause=0.2, type_time=0.5)
            self.play(*rl.unfreeze("review"), FadeOut(rq), flash(hnd, TURN, 1.2), run_time=0.5)

        # ========================================================== 2 · the ticket: a fingerprint, not stock
        tk = FlatTicket()
        tk.shift(np.array([-SAFE + tk.frame.width / 2, TOP - tk.frame.height / 2, 0]) - tk.frame.get_center())
        p31 = src_panel(CO, 31, 36, wrap={35: [".model_dump"]}, size=20)
        place(p31, left=-SAFE, bottom=-3.5)
        assert p31.get_top()[1] < tk.frame.get_bottom()[1] - 0.12, (p31.get_top(), tk.frame.get_bottom())
        bars31 = [p31.bar(n, HARNESS, 0.18) for n in range(31, 36)]
        keys = [p31.span(n, k) for n, k in zip(range(31, 36), FIELD_KEYS)]
        exc_box = code_box(p31, 35, EXC35)
        exg = tk.parts["excluded"]
        same = two_row_note(["same cart, same data ·", "your run prints this hash too"])
        place(same, left=exg.get_left()[0], top=exg.get_bottom()[1] - 0.12)
        ex29 = excerpt_chip(INV29, f"{CO} · line 29 (excerpt)", line=source_line(CO, 29))
        place(ex29, left=exg.get_left()[0], bottom=exg.get_top()[1] + 0.22)
        assert ex29.get_bottom()[1] > exg.get_top()[1] + 0.08, (ex29.get_bottom(), exg.get_top())
        assert exg.get_bottom()[1] > same.get_top()[1] + 0.06, (exg.get_bottom(), same.get_top())
        assert same.get_bottom()[1] > p31.get_top()[1] + 0.12, (same.get_bottom(), p31.get_top())
        for m in (tk, same, ex29, p31):
            inside(m)
        apart(ex29, tk.frame)
        apart(same, ex29)
        anchors = ("taken over the request", "the items", "the subtotal", "the policy", "and the product attributes")
        with self.voiceover(SAY[2]) as vo:
            # everything out, then the ticket in (old out, then new in: the panel and ticket share space)
            self.play(FadeOut(VGroup(strip, ft)), FadeOut(VGroup(pers, hnd, you)), FadeOut(VGroup(rl, tok, lab_rev, ill)),
                      FadeOut(VGroup(p129, b129)), run_time=0.5)
            self.play(FadeIn(tk, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("A fingerprint")
            self.play(FadeIn(p31, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the SHA-256 hash")
            self.play(reveal(tk.sha, shift=UP * 0.05), run_time=0.4)
            for i, anchor in enumerate(anchors):
                vo.wait_until(anchor)
                self.play(FadeIn(bars31[i]), keys[i].animate.set_color(HARNESS), tk.fill(i, run_time=0.5),
                          tk.slot(i).animate.set_stroke(opacity=0), run_time=0.5)
            self.play(reveal(tk.hash_mob, scale=1.1), run_time=0.5)
            self.play(FadeIn(same, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("Stock is left out on purpose")
            self.play(Create(exc_box), run_time=0.4)
            self.play(*tk.show_excluded(), run_time=0.5)
            vo.wait_until("it's rechecked")
            self.play(FadeIn(ex29, shift=DOWN * 0.1), run_time=0.5)
            self.play(flash(ex29.text, TURN, 1.04), run_time=0.6)

        # ========================================================== 3 · at checkout: the same hash, this checkout
        tok3 = new_token()
        tok3.set_z_index(2)                  # it stops ON "revalidate & place": seen at checkout
        tok3.move_to(rl.spot("review"))
        lab_pl = st_label(rl, "place")
        unfreeze_now(rl, "review")
        p84 = src_panel(CO, 84, 87, wrap={86: ["and ticket.fingerprint"]}, size=20)
        place(p84, left=-SAFE, bottom=-3.5)
        rh = hash_chip()
        place(rh, cx=lab_pl.get_center()[0], top=lab_pl.get_bottom()[1] - 0.1)
        cmp_at = np.array([tk.hash_mob.get_center()[0], tk.frame.get_bottom()[1] - 0.1 - rh.height / 2, 0])
        assert rh.get_bottom()[1] > p84.get_top()[1] + 0.05
        boxes = [code_box(p84, 85, COND85), code_box(p84, 86, COND86A), code_box(p84, 86, COND86B)]
        checks = []
        for bx in boxes:                    # a column of checks right of the conditions' rows
            c = check_mark(0.26, HARNESS)
            c.move_to([p84.get_right()[0] - 0.45, bx.get_center()[1], 0])
            assert c.get_left()[0] > bx.get_right()[0] + 0.25
            checks.append(c)
        cap86 = label("this checkout (the order's own key)", CAPTION, S.GREY)
        match = check_mark(0.3, HARNESS)
        match.move_to([cmp_at[0] + rh.width / 2 + 0.2 + match.width / 2, cmp_at[1], 0])
        # the caption sits above the panel's header; a GREY elbow pointer runs down the free column
        # right of lines 85-86 and points left at the right-hand checkout_key (this checkout's own
        # key), so the caption is tied to it without crossing any code
        x_el = boxes[1].get_right()[0] + 0.42
        place(cap86, right=x_el + 0.35, bottom=p84.get_top()[1] + 0.12)
        k86 = p84.span(86, "checkout_key", 1)
        y86 = k86.get_center()[1]
        ptr = VGroup(Line([x_el, cap86.get_bottom()[1] - 0.06, 0], [x_el, y86, 0], stroke_width=2.5, color=S.GREY),
                     Arrow([x_el + 0.0125, y86, 0], [boxes[1].get_right()[0] + 0.05, y86, 0], buff=0, color=S.GREY,
                           stroke_width=2.5, tip_length=0.13, max_tip_length_to_length_ratio=0.5))
        assert x_el > p84.header.get_right()[0] + 0.25, (x_el, p84.header.get_right())
        assert x_el > boxes[0].get_right()[0] + 0.25 and x_el < checks[0].get_left()[0] - 0.4
        rh_end = rh.copy().move_to(cmp_at)
        apart(cap86, match, 0.15)
        apart(cap86, rh_end, 0.15)
        apart(rh_end, p84, 0.1)
        inside(cap86)
        rcpt = receipt_token(RECEIPT[:8] + "…")
        place(rcpt, right=rl.station("confirm").frame.get_left()[0] - 0.15, cy=1.62)
        apart(rcpt, tk.frame, 0.1)
        apart(rcpt, rl.station("confirm").frame, 0.1)
        apart(rcpt, lab_pl, 0.1)
        # the what-if row: an edited items chip, a different hash, RED ≠, not approved
        wi_tag = illustration_tag("what if")
        wi_items = chip("items", TURN, size=CAPTION, font=MONO, pad_y=0.04)
        wi_pen = pencil(0.4, TURN)
        wi_hash = hash_chip(WHATIF16)
        wi_ne = neq()
        wi_no = label("not approved", CAPTION, ERR)
        wi_mid = VGroup(wi_items, wi_pen).arrange(RIGHT, buff=0.1)
        wi_ar = Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=S.GREY, stroke_width=3, tip_length=0.14,
                      max_tip_length_to_length_ratio=0.4)
        wi = VGroup(wi_tag, wi_mid, wi_ar, wi_hash, wi_ne, wi_no).arrange(RIGHT, buff=0.22)
        place(wi, left=-SAFE + 0.05, top=cmp_at[1] - rh.height / 2 - 0.12)
        inside(wi)
        assert wi.get_bottom()[1] > STRIP_TOP + 0.05
        place_c = rl.station("place").frame.get_center()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p31, *bars31, exc_box)), FadeOut(VGroup(same, ex29)), *tk.parts_out("excluded"),
                      run_time=0.5)
            self.play(FadeIn(rl), FadeIn(tok3), FadeIn(lab_pl), FadeIn(ill), run_time=0.5)
            self.play(ride(tok3, path_of([tok3.get_center(), place_c]), 0.7), run_time=0.7)
            self.play(outline_flash(rl.station("place").frame, HARNESS), FadeIn(rh, shift=DOWN * 0.15), run_time=0.6)
            # the re-hash goes under the ticket's hash: down, then along under the ticket, never across it
            self.play(ride(rh, path_of([rh.get_center(), [rh.get_center()[0], cmp_at[1], 0], cmp_at]), 0.9),
                      run_time=0.9)
            vo.wait_until("The approval counts")
            self.play(FadeIn(p84, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("only if the decision is approve")
            self.play(Create(boxes[0]), run_time=0.35)
            self.play(FadeIn(checks[0], scale=1.3), run_time=0.25)
            vo.wait_until("and the ticket matches this checkout")
            self.play(Create(boxes[1]), FadeIn(cap86, shift=UP * 0.08), Create(ptr), run_time=0.45)
            self.play(FadeIn(checks[1], scale=1.3), run_time=0.25)
            vo.wait_until("and this fingerprint")
            self.play(Create(boxes[2]), flash(tk.hash_mob, HARNESS, 1.06), flash(rh, HARNESS, 1.06), run_time=0.4)
            self.play(FadeIn(checks[2], scale=1.3), FadeIn(match, scale=1.3), run_time=0.3)
            # a what-if aside: one cart line changes, the re-hash differs, no approval. The panel
            # with its three checks stays until then; old out, then new in (the row takes its place)
            vo.wait_until("Change one line")
            self.play(FadeOut(VGroup(p84, *boxes, *checks, cap86, ptr)), run_time=0.25)
            self.play(FadeIn(wi_tag), FadeIn(wi_mid, shift=DOWN * 0.1), run_time=0.3)
            self.play(GrowArrow(wi_ar), FadeIn(wi_hash, shift=RIGHT * 0.1), run_time=0.35)
            vo.wait_until("and the hashes differ")
            self.play(FadeIn(wi_ne, scale=1.3), FadeIn(wi_no), run_time=0.35)
            self.wait(1.0)                                   # the aside is read before the real run goes on
            # back to the real run: the aside leaves, the strip returns, the order is placed
            self.play(FadeOut(wi), run_time=0.3)
            self.play(FadeIn(VGroup(strip, ft)), ride(tok3, path_of([tok3.get_center(), rl.spot("place")]), 0.35),
                      run_time=0.35)
            show(self, strip, MGR, 30, run_time=0.2)         # (one line at a time: the strip scrolls)
            pl = show(self, strip, MGR, (32, 34), run_time=0.35)
            dt = beside(differ_tag(), strip, pl[-1])
            pin(self, pl[-1], dt, run_time=0.4,
                anim=AnimationGroup(FadeIn(dt, shift=LEFT * 0.1), FadeTransform(tok3, rcpt)))
        receipt = rcpt

        # ========================================================== 4 · the stopwatch: your thinking time
        sw = Stopwatch()
        place(sw, left=match.get_right()[0] + 0.65, bottom=STRIP_TOP + 0.32)   # clear of the strip's bar tags
        sw_tag = illustration_tag()
        place(sw_tag, left=sw.get_right()[0] + 0.25, top=sw.get_top()[1])
        ex444 = excerpt_chip(R444A, "README.md · line 444 (excerpt)", line=source_line("README.md", 444))
        place(ex444, left=sw.get_right()[0] + 0.25, bottom=sw.get_bottom()[1])
        apart(sw_tag, ex444)
        hnd4 = hand(TURN, h=0.55)
        hover = tk.frame.get_corner(UP + RIGHT) + np.array([-0.55, -0.42, 0])
        hnd4.move_to(hover + LEFT * 0.8)
        tap = label("approve", CAPTION, TURN)
        tap.next_to(hnd4.copy().move_to(hover), LEFT, buff=0.12)
        for m in (sw, sw_tag, ex444):
            inside(m)
            assert m.get_bottom()[1] > STRIP_TOP + 0.05
        apart(sw_tag, match)
        apart(ex444, receipt)
        apart(sw_tag, lab_pl, 0.1)
        assert tap.get_left()[0] > tk.frame.get_left()[0] + 2.6   # right of the title and the slot chips
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeIn(sw), FadeIn(sw_tag), FadeIn(ex444, shift=LEFT * 0.1), run_time=0.45)
            self.play(sw.run(0.3, 0.7), FadeIn(hnd4, shift=RIGHT * 0.2), run_time=0.7)
            self.play(hnd4.animate.move_to(hover), sw.pause_look(True), run_time=0.5)
            self.play(hnd4.animate.shift(UP * 0.1), run_time=0.3)
            self.play(hnd4.animate.shift(DOWN * 0.1), run_time=0.3)
            self.play(FadeIn(tap, scale=1.2), flash(hnd4, TURN, 1.2), sw.pause_look(False), run_time=0.45)
            self.play(sw.run(0.35, 0.9), run_time=0.9)
        sw.freeze()

        # ========================================================== 5 · extra: decline
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(sw, sw_tag, ex444, hnd4, tap)), FadeOut(VGroup(receipt, rh, match)),
                      caption_extra(tr, True), run_time=0.45)
            c5 = type_cmd(self, strip, DEC.cmd, 0.6)
            ex5 = extra_tag()
            beside(ex5, strip, c5.rows[0])
            pin(self, c5.rows[0], ex5, run_time=0.3)
            r28d = show(self, strip, DEC, DEC.cut(28, ASK, ellipsis=False), run_time=0.35)[0]
            vo.wait_until("type decline instead")
            type_after(self, strip, r28d, "decline", pause=0.2, type_time=0.5)
            vo.wait_until("the workflow ends")
            show(self, strip, DEC, (DEC.line(31), ERR), (DEC.line(32), INK), run_time=0.45)

        # ========================================================== 6 · ponder: another order takes the Mimolette
        tok6 = new_token()
        tok6.set_z_index(2)                  # it stops ON "revalidate & place" (seen there, blocked there)
        tok6.move_to(rl.spot("review"))
        chk6 = check_mark(0.26, HARNESS)
        chk6.next_to(tk.hash_mob, RIGHT, buff=0.2)
        assert chk6.get_right()[0] < tk.frame.get_right()[0] - 0.05
        shelf = StockShelf(tuple(STOCK.items()), cap=SHELF_CAP, bar_w=2.6, numbers=False)
        mim = shelf.frames["Mimolette"]
        place(shelf, left=tk.frame.get_right()[0] + 0.35, top=lab_pl.get_bottom()[1] - 0.2)
        sh_tag = illustration_tag("what if")             # the rail's tag becomes the what-if's (sequential swap)
        place(sh_tag, right=ill.get_right()[0], cy=ill.get_center()[1])
        tok2 = new_token()
        tok2.set_z_index(0)
        stop2 = np.array([mim.get_right()[0] + 0.3 + tok2.width / 2, mim.get_center()[1], 0])
        tok2.move_to(stop2)
        qm = label("?", 26, CLOUD)
        qm.next_to(tok2, RIGHT, buff=0.1)
        tok2_q = VGroup(tok2, qm)
        inside(tok2_q)
        pcard = ponder_card(PONDER, width=12.4)
        card_top = -3.55 + pcard.height
        assert shelf.get_bottom()[1] > card_top + 0.1, (shelf.get_bottom(), card_top)
        apart(shelf, tk.frame, 0.1)
        apart(tok2_q, rl, 0.1)
        apart(sh_tag, tr, 0.1)
        with self.voiceover(SAY[6]) as vo:
            self.wait(0.8)                               # the declined run stays readable a moment
            self.play(FadeOut(VGroup(strip, ft)), caption_extra(tr, False), run_time=0.45)
            vo.wait_until("The manager approves")
            self.play(FadeIn(tok6, shift=RIGHT * 0.15), FadeIn(chk6, scale=1.2), run_time=0.5)
            self.play(flash(tok6, TURN, 1.2), flash(chk6, HARNESS, 1.3), run_time=0.5)
            vo.wait_until("Before checkout runs")
            self.play(FadeOut(ill), run_time=0.3)
            self.play(FadeIn(shelf), FadeIn(sh_tag), run_time=0.6)
            vo.wait_until("another order takes")
            # the second cart rolls in from off-screen right along the empty Mimolette row
            q_home = tok2_q.get_center()
            tok2_q.shift(RIGHT * (7.4 - tok2_q.get_left()[0]))
            self.add(tok2_q)
            self.play(tok2_q.animate.move_to(q_home), run_time=1.0)
            vo.wait_until("What does checkout do")
            self.play(outline_flash(rl.station("place").frame, TURN), run_time=0.7)
        card = ponder_at(self, PONDER, seconds=8.0, width=12.4)
        assert abs(card.get_top()[1] - card_top) < 0.3

        # ========================================================== 7 · checkout revalidates: blocked
        need = shelf.need("Mimolette", NEED)
        viol = stamp("stock violation", ERR)
        place(viol, left=mim.get_right()[0] + 0.3, cy=mim.get_center()[1])
        blk = stamp("blocked", ERR)
        place(blk, right=rl.station("place").frame.get_left()[0] - 0.2, cy=rl.station("place").frame.get_center()[1])
        apart(blk, tk.frame, 0.08)
        ex158 = excerpt_chip(BLOCK158, f"{WS} · lines 155–158 (excerpt)", line=source_line(WS, 158))
        place(ex158, left=-SAFE, top=min(shelf.get_bottom()[1], tk.frame.get_bottom()[1]) - 0.25)
        act6 = grey_tag("act 6 runs this for real")
        place(act6, right=SAFE, cy=ex158.chip.get_center()[1])
        ex29b = excerpt_chip(INV29, f"{CO} · line 29 (excerpt)", line=source_line(CO, 29))
        place(ex29b, left=-SAFE, top=ex158.get_bottom()[1] - 0.18)
        cap7 = label("an approval authorizes a decision · it doesn't reserve stock", CAPTION, INK)
        place(cap7, left=-SAFE + 0.05, top=ex29b.get_bottom()[1] - 0.18)
        for m in (ex158, act6, ex29b, cap7, viol, blk):
            inside(m)
        apart(ex158, act6, 0.15)
        apart(viol, mim, 0.15)
        mbar = shelf.bar("Mimolette")
        w_left = shelf.bar_w * LEFT_AFTER / shelf.cap
        drained = Rectangle(width=w_left, height=mbar.height, stroke_width=0).set_fill(HARNESS, 0.7)
        drained.move_to([mim.get_left()[0] + w_left / 2, mim.get_center()[1], 0])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(card), run_time=0.3)
            self.play(Transform(mbar, drained), tok2_q.animate.shift(LEFT * 0.25), run_time=0.7)
            self.play(FadeOut(tok2_q, shift=RIGHT * 0.6),
                      ride(tok6, path_of([tok6.get_center(), rl.station("place").frame.get_center()]), 0.6), run_time=0.6)
            self.play(flash(chk6, HARNESS, 1.3), run_time=0.35)
            vo.wait_until("finds a stock violation")
            self.play(Create(need), run_time=0.5)
            self.play(FadeIn(viol, scale=1.2), run_time=0.4)
            vo.wait_until("and blocks")
            self.play(*tint(tok6, ERR), FadeIn(blk, scale=1.2), rl.station("place").frame.animate.set_stroke(ERR, 4),
                      run_time=0.45)
            self.play(FadeIn(ex158, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Stock isn't in the fingerprint")
            self.play(flash(tk.hash_mob, HARNESS, 1.05), flash(chk6, HARNESS, 1.3), run_time=0.6)
            self.play(FadeIn(ex29b, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("an approval authorizes a decision")
            self.play(FadeIn(cap7, shift=UP * 0.08), run_time=0.5)
            vo.wait_until("it doesn't reserve anything")
            self.play(outline_flash(mim, ERR, 0.08), run_time=0.7)    # the stock nobody reserved
            vo.wait_until("Act 6 shows this for real")
            self.play(FadeIn(act6, shift=LEFT * 0.1), run_time=0.4)

        # ========================================================== 8 · step 5: out of stock, one revision
        t8 = term(container=True, rows=12)
        ft8 = frame_tags(t8, scripted_tag(), offline_tag())
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(tk, chk6, rl, tok6, lab_pl, blk, shelf, sh_tag, need, viol, ex158, act6,
                                     ex29b, cap7)), tr.goto(5), run_time=0.6)
            self.play(FadeIn(t8, shift=UP * 0.2), FadeIn(ft8, shift=DOWN * 0.1), run_time=0.5)
            type_cmd(self, t8, OOS.cmd, 1.0)
            show(self, t8, OOS, (11, 14), run_time=0.5)
            vo.wait_until("so attempt 1 fails")
            show(self, t8, OOS, (OOS.line(16), ERR), run_time=0.4)
            vo.wait_until("One bounded revision")
            show(self, t8, OOS, (OOS.line(25), TURN), (OOS.line(26), TURN), run_time=0.5)
            vo.wait_until("and the order places")
            show(self, t8, OOS, (OOS.line(28), HARNESS), run_time=0.4)
            show(self, t8, OOS, (OOS.line(35), HARNESS), run_time=0.4)      # valid, and then placed
            vo.wait_until("with zero model calls")
            r45 = show(self, t8, OOS, 45, run_time=0.4)[0]
            pin(self, r45, beside(grey_tag("scripted: no model"), t8, r45), run_time=0.4)

        # ========================================================== 9 · step 6: the notebook cell; the layers
        p423 = src_panel("README.md", 423, 430, size=20)
        place(p423, left=-SAFE, top=TOP)
        b427 = p423.bar(427, TURN, 0.2)
        ill9 = illustration_tag()
        place(ill9, right=SAFE, top=TOP - 0.1)
        apart(ill9, p423, 0.1)
        rings, lifts, chips9, inner, lock9, in_lab = self.layer_rings(p423)
        ex444b = excerpt_chip(R444B, "README.md · line 444 (excerpt)", line=source_line("README.md", 444))
        place(ex444b, cx=0.0, cy=(p423.get_bottom()[1] + in_lab.get_top()[1]) / 2)
        assert ex444b.get_bottom()[1] > in_lab.get_top()[1] + 0.08, (ex444b.get_bottom(), in_lab.get_top())
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(t8, ft8)), tr.goto(6), run_time=0.5)
            self.play(FadeIn(p423, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the notebook cell")
            self.play(FadeIn(b427), run_time=0.4)
            self.play(FadeIn(rings), FadeIn(ill9), run_time=0.7)
            vo.wait_until("Its trace and budget layers")
            self.play(*[flash(c, TURN, 1.1) for c in chips9], run_time=0.6)
            self.play(*[m.animate.shift(UP * 0.35).set_opacity(0) for m in lifts], run_time=0.8)
            self.remove(*lifts)
            vo.wait_until("validation, approval and revalidation")
            self.play(flash(inner, HARNESS, 1.04), flash(lock9, HARNESS, 1.4), run_time=0.7)
            vo.wait_until("are graph and checkout rules")
            self.play(FadeIn(ex444b, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("so they stay")
            self.play(flash(in_lab, HARNESS, 1.05), run_time=0.6)

        # ========================================================== 10 · checkpoint; the map; your turn
        c448 = top_chip(R448, where="README.md · line 448")
        lr10 = lref("22")
        apart(c448, lr10)
        mm = BoundaryMini(upto=2)
        tc = turn_card([MGR.cmd, (Prose("    type approve, then run it again and type decline"), S.GREY), OOS.cmd,
                        (Prose("notebook cell: Colab or Jupyter"), S.GREY), (Prose("offline · free"), HARNESS)])
        place(tc, cx=0, cy=-0.3)
        inside(tc)
        assert tc.get_top()[1] < tr.get_bottom()[1] - 0.1
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(p423, b427, ill9, ex444b, *[m for m in rings if m not in lifts])), run_time=0.4)
            self.play(FadeIn(c448, shift=DOWN * 0.1), FadeIn(mm), FadeIn(lr10), run_time=0.5)
            self.play(mm.light("control"), run_time=0.25)
            cap_c = mm.caption("Control flow ← the workflow graph")
            self.play(mm.add_bar("control"), FadeIn(cap_c, shift=LEFT * 0.1), run_time=0.45)
            # each caption stays beside its own row until the beat ends (the rows are 3 apart)
            vo.wait_until("and checkout revalidates")
            self.play(mm.light("verify"), run_time=0.3)
            cap_v = mm.caption("Verification ← validate · revalidate")
            apart(cap_c, cap_v, 0.1)
            self.play(mm.add_bar("verify"), FadeIn(cap_v, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Pause and run")
            self.play(FadeOut(VGroup(c448, mm, cap_c, cap_v)), FadeOut(lr10), run_time=0.5)
            self.play(FadeIn(tc, scale=0.97), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tc, tr)), run_time=0.8)
        self.wait(0.3)

    # ------------------------------------------------------------------ beat 9's picture
    def layer_rings(self, panel):
        """The README's layer table (lines 439-440) as rings round a mini rail (illustration):
        the outer GREEN ring WorkflowBudget(...), the next WorkflowTrace(), each with its
        .without(...) chip on its top edge; inside them the padlocked ring of the graph/checkout
        rules. Returns (all, the parts that lift off, the two chips, the inner ring, its padlock,
        its label)."""
        top = panel.get_bottom()[1] - 0.4
        bottom = -3.5
        step = 0.46
        rings = VGroup()

        def ring(w, top_y, bot_y, stroke):
            r = RoundedRectangle(width=w, height=top_y - bot_y, corner_radius=0.3, stroke_color=HARNESS,
                                 stroke_width=stroke).set_fill(opacity=0)
            return r.move_to([0, (top_y + bot_y) / 2, 0])

        def edge_label(mob, r, x_left):
            bg = Rectangle(width=mob.width + 0.24, height=mob.height + 0.1, stroke_width=0).set_fill(S.BG, 1)
            g = VGroup(bg, mob)
            g.text = mob                   # flash() lights the words, never the opaque backing
            mob.move_to(bg)
            return place(g, left=x_left, cy=r.get_top()[1])

        rb = ring(12.6, top, bottom, 3)
        rt = ring(10.4, top - step, bottom + 0.12, 3)
        ri = ring(8.2, top - 2 * step, bottom + 0.24, 6)
        lb = edge_label(mono(BUDGET440, CAPTION, HARNESS), rb, -5.9)
        cb = chip(WO_BUDGET, TURN, size=CAPTION, font=MONO, pad_y=0.06)
        place(cb, right=5.95, cy=rb.get_top()[1])
        lt = edge_label(mono(TRACE439, CAPTION, HARNESS), rt, -4.8)
        ct = chip(WO_TRACE, TURN, size=CAPTION, font=MONO, pad_y=0.06)
        place(ct, right=cb.get_left()[0] - 0.25, cy=rt.get_top()[1])     # never under the budget chip
        lock = padlock(0.42, HARNESS)
        li = edge_label(label("validation · authorization · approval · final revalidation", CAPTION, HARNESS), ri, -3.2)
        place(lock, right=li.get_left()[0] - 0.08, cy=ri.get_top()[1])
        mini = Rail(mini=True)
        mini.scale(0.55)
        place(mini, cx=0.0, cy=(li.get_bottom()[1] + ri.get_bottom()[1]) / 2)
        assert mini.get_top()[1] < li.get_bottom()[1] - 0.06 and mini.get_bottom()[1] > ri.get_bottom()[1] + 0.06
        assert lock.get_left()[0] > ri.get_left()[0] + 0.1
        apart(cb, ct, 0.15)
        apart(ct, lt, 0.3)
        rings.add(rb, rt, ri, mini, lb, cb, lt, ct, li, lock)
        inside(rings)
        return rings, [rb, rt, lb, cb, lt, ct], [cb, ct], ri, lock, li
