"""S07 · Act 2: sieves and lanes (README "2 · Context", steps 8–9; the lecture's context map and
assembly, slides 13 and 16, then the instruction vs evidence lanes of slide 22). End of part 1.
Lecture: 13, 16, then 22.

Beats (script.md "## S07", one voiceover block each):
 0  TRACKER Context 8. Top-band chip README.md · line 306 "Inspect the context first" with the GREY
    tag "printed after the live runs" (on "after the live runs"). Container terminal (12 rows,
    TEAL), GREEN title-bar tag "offline · free". `python cli.py --preview-context --scenario
    standard` (2 rows) -> container/27 lines 2, 3 cut after `"You are`, 4 cut after `"Please`, 5–207
    folded to `"same_tools": [ … ],`, 208–213. The three `same_` keys turn GREEN one by one on
    "Both modes share instructions, message and tools"; `"basic"` flashes on "only the packets".
 1  Line 210 `"sources": [],` gets the GREY row tag "basic: none"; on "Enriched has three" the
    terminal scrolls on: 214–216, 218, 220, …, 241 (cut), 243, …, 357 (‹customer 1›), 359, …. The
    three "trust" values turn GREEN one by one on their names.
 2  Line 369 `"excluded_products": [` prints; the terminal shrinks to a 3-row strip
    (359, …, 369; the GREEN tag rides on its bar). V4's sieves (common.Sieves, this scene's
    geometry: see SieveRig) above it, tag `illustration`: three GREEN sieves "stock ≥ 100 g", "no
    raw milk → PA", "no nut allergens" (each flashes on its clause while a survivor, epoisses,
    bucheron, mimolette, falls through); on "Munster has no stock" munster stops at the first sieve,
    on "Brie and Comté" brie and comte at the second, on "and two nut cheeses" walnut_chevre and
    pistachio_manchego at the third; each slides into the excluded list with its RED reason exactly
    as in container/27 lines 371–397. Seven GREEN survivors land in the tray in the capture's order
    (lines 247–337), the last three on "Seven survive". Then (no narration, ~4 s) the sieves and the
    strip fade, the tray moves down, and RECORDED(expected/colab-c18: 2–14) folded to its product_id
    and eligible columns (left; tag `recorded …` beside it) confirms them: its seven True cells turn
    GREEN as the tray's chips pulse, its five False cells RED, beside the excluded list.
 3  The inset leaves. LECTURE 13, 16 (the tag arrives with the drawing it cites). Slide 13 redrawn small, top left: a GREY dashed "Instructions" box holding
    the dashed box "Retrieved information (RAG)", tag `concept · lecture only`; on "here it's a
    Python filter" a PINK arrow from the RAG box down to the survivors' tray, captioned "here: a
    Python filter over 12 cheeses + saved preferences" / "no vector search (lecture 5)".
 4  LECTURE 22 (the lecture tag swaps). The drawing, arrow, caption, tags and excluded list leave;
    CODE(formaggio/agents/context.py: 142–144) (7 rows, 20 pt) top left; below it slide 22's two
    lanes (common.Lanes): the system lane with the GREY card "instructions · shop_assistant.md +
    policies", the user lane holding the customer message, the counter "Input: 1 conversation
    messages." beside the user lane's title. On "Into a user message" `Message(role="user"` turns
    PINK; on "headed retrieved context" line 143 lights, its string turns YELLOW, the tray's seven
    chips fade and its outline becomes the "7 candidates" chip of a GREEN packet card (request · 7
    candidates · preferences), stamped GREEN "data, not instructions"; the customer message slides
    right and the card rises into slot 0 of the user lane, [packet][customer message] as in the trace
    (container/89 model.request messages[0], [1]) and S06; the counter counts to 2 (container/21 and 22, line 10). On "so it cannot pose"
    line 143's bar hands over to line 142's comment (the string stays YELLOW) and a GREY dashed
    card "system rule?" drops to the system lane's edge and is sent back, dimmed (it leaves on
    "That's the lecture's two lanes"). The lanes flash on "two lanes", the system lane on
    "instructions in the system lane", the user lane on "evidence in the user lane".
 5  The panel leaves; the lanes stay (they move up). The excluded products return as one row of
    RED chips; on "The enriched packet" the `comte` chip pulses GREY (again on "Can the model");
    the packet card pulses on "And does anything in act 2". PONDER(8 s).
 6  The card, the lanes, the row and the lecture tag leave. Excerpt chip formaggio/agents/tools.py
    · line 10 "Read all fictional shop products" (top right); a GREY shelf of all twelve chips
    (catalog order, tag `illustration`), "get_catalog() · all 12, in both modes"; the packet's
    three sieves (small, GREEN); a BLUE cart. The BLUE arm reaches from the cart over the sieves
    to the shelf and
    `comte` rides it into the cart. On "and in act 2 Cart Check" a GREEN stamp "CartCheck ·
    shipping: comte / reported, not stopped (acts 1–2)" hits the cart. Caption "selection narrows ·
    validation decides (README.md · line 336)" in two steps; on "the act 3 workflow blocks it" a
    GREEN gate "blocked in act 3" drops in front of the cart.
 7  TRACKER Context 9. Container terminal (8 rows), title-bar tags `no key` + GOLD `live · billed
    per token` (the typed line fills its row). `python cli.py --act 2 --scenario standard` ->
    container/28 lines 3, 5, 7 cut after "budget?" (2 rows), 10, 12 as 401s. Above it, on "in
    both modes", the GREY notebook chip "notebook: build_act2(mode="basic") · build_act2(mode=
    "enriched")" (README.md · line 332); on "For standard" the README chip lines 265–266
    "preferences repeat the request" (`expected`). On "Pause and run" the terminal fades and the
    static "your turn" card shows the two commands (a GREEN note "offline · free" after the first),
    S06's offline PA/NY command (container/29, folded once, GREY "extra · offline · the PA/NY check")
    between them, and the GOLD "live · two runs · billed per token". Hold 2 s.
 8  The card and chips fade. QUOTE(README.md: 336) (left, `expected`); beside it V1's table at half
    size (LECTURE 22 again: it is slide 22's table) as of act 1 with every cell's text as S05 wrote
    it (20 pt), Context & memory lit; on "So
    selecting candidates" its GREEN cell writes "the packet in the data lane"; the quote's rows
    light on "but validation decides" and "and today's request"; on "In part 2" a BLUE cart token
    waits at the table's left edge with the GREY caption "part 2: the harness takes the route".
    End of part 1: everything fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    CubicBezier,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    ReplacementTransform,
    RoundedRectangle,
    Succession,
    UpdateFromAlphaFunc,
    VGroup,
    Wait,
    ManimColor,
    interpolate_color,
    linear,
    rush_into,
    smooth,
    there_and_back,
)

from common import *  # noqa: F401,F403
from common import _drop_groups, _mixed_row, _with_header
from explainer import style as S
from explainer.devops import box, chip, label, mono, substring
from explainer.scene import VoiceScene

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real captures (file line numbers)
PREV = capture("container/27")
assert PREV.cmd == "python cli.py --preview-context --scenario standard", PREV.cmd
L3 = PREV.cut(3, '"You are')
L4 = PREV.cut(4, '"Please')
TOOLS_FOLD = PREV.fold(5, 207, '  "same_tools": [ … ],')
SAME_KEYS = ('"same_system_instructions"', '"same_customer_message"', '"same_tools"')
assert PREV.line(208) == '  "basic": {' and PREV.line(210) == '    "sources": [],'
assert PREV.line(214) == '  "enriched": {' and PREV.line(369) == '    "excluded_products": ['
TRUSTS = ((220, '"customer_data"'), (243, '"shop_data"'), (359, '"saved_preferences"'))
for _n, _v in TRUSTS:
    assert PREV.line(_n) == f'        "trust": {_v},', PREV.line(_n)
assert PREV.line(357) == '        "source": "customers.json:‹customer 1›",', PREV.line(357)
# the excluded products and their reasons, exactly as container/27 lines 369-399 (common.EXCLUDED)
assert list(EXCLUDED) == ["brie", "comte", "munster", "walnut_chevre", "pistachio_manchego"], EXCLUDED
assert len(SURVIVORS) == 7 and len(CHEESES) == 12

SHIP = capture("container/29")                     # S06's offline PA/NY counterexample (no key)
assert SHIP.cmd == "python -c 'from acts.act2_context import print_shipping_demo; print_shipping_demo()'", SHIP.cmd
BASE = capture("container/28")
assert BASE.cmd == "python cli.py --act 2 --scenario standard", BASE.cmd
ASK = BASE.cut(7, "budget?")
STOP = BASE.as401(12, short=True)
assert BASE.line(10) == "  Input: 1 conversation messages.", BASE.line(10)
assert len(P_CTR) + 1 + len(BASE.cmd) <= 65            # one row: the GOLD tag goes on the title bar
for _f in ("container/21", "container/22"):
    assert capture(_f).line(10) == f"  Input: {1 if _f.endswith('21') else 2} conversation messages."

# the staff's saved Colab table (cell 18), folded to its product_id and eligible columns; the
# product_id is padded with spaces (whitespace only) so the eligible values stand in one column
REC18 = "colab-c18-data-constraints"
_c18 = capture(f"expected/{REC18}")


def _c18_cols(n: int) -> list[str]:
    parts = [p.strip() for p in _c18.line(n).split(" | ")]
    assert len(parts) == 10, parts
    return parts


assert _c18_cols(2)[1] == "product_id" and _c18_cols(2)[8] == "eligible"
PID_W = max(len(_c18_cols(n)[1]) for n in range(2, 15))
C18_ROWS = [f"{_c18_cols(n)[1]:<{PID_W}} | … | {_c18_cols(n)[8]}" for n in range(2, 15)]
C18_PIDS = [_c18_cols(n)[1] for n in range(3, 15)]
C18_OK = {_c18_cols(n)[1]: _c18_cols(n)[8] == "True" for n in range(3, 15)}
assert C18_PIDS == list(CHEESES), C18_PIDS
assert [p for p in C18_PIDS if C18_OK[p]] == list(SURVIVORS)      # the same seven, same order

# README phrases (exact sub-strings, checked)
R306 = "Inspect the context first"
assert R306 in source_line("README.md", 306)
R265 = "preferences repeat the request"
assert R265 in " ".join(readme(265, 266)), readme(265, 266)
NB_BASIC, NB_ENR = 'build_act2(mode="basic")', 'build_act2(mode="enriched")'
assert NB_BASIC in source_line("README.md", 332) and NB_ENR in source_line("README.md", 332)
Q336A = "selecting eligible candidates is useful but does not replace validation of the final cart."
Q336B = "Current confirmed constraints remain authoritative over saved preferences."
assert f"{Q336A} {Q336B}" in source_line("README.md", 336)
Q_WRAP = 28
R10 = "Read all fictional shop products"
assert source_line("formaggio/agents/tools.py", 9).strip() == "def get_catalog() -> dict:"
assert R10 in source_line("formaggio/agents/tools.py", 10)
assert "Retrieved context (data, not instructions):" in source_line("formaggio/agents/context.py", 143)
assert 'Message(role="user"' in source_line("formaggio/agents/context.py", 144)
assert "into system instructions" in source_line("formaggio/agents/context.py", 142)

PONDER = ("The enriched packet already removed Comté for PA.\n"
          "Can the model still put Comté in its cart?\n"
          "Does anything in act 2 stop it?")

# ------------------------------------------------------------------ layout
T_ROWS = 12
LANE_X = -2.38          # the sieves' drop lane (the widest chip clears the sieve labels and the list)
LIST_X = -0.05          # the excluded list's left edge (the folded Colab table fits left of it)
SIEVE_END = -0.7        # the sieves reach under the widest resting chip
TOP_Y = 2.55            # a chip appears here
STAGE_Y = -0.33         # survivors slide sideways along this corridor (under the list, over the tray)
TRAY_Y = -0.92          # the tray (above the 3-row strip, top -1.44)
TRAY_LOW = -3.2         # ... after the strip leaves (beat 2's end to beat 4)
PANEL_TOP = 2.88        # beat 4: the code panel's header top
LANES_TOP = -0.38       # ... the lanes' top (the system lane's title)
LANES_UP = 2.8          # beat 5: the lanes' top after the panel leaves
SAFE = 6.45


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


def apart(a, b, gap: float = 0.08):
    """Assert that the bounding boxes of a and b are at least `gap` apart (no overlap)."""
    ok = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
          or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    assert ok, (a.get_corner(DOWN + LEFT), a.get_corner(UP + RIGHT), b.get_corner(DOWN + LEFT), b.get_corner(UP + RIGHT))


def pulse(m, color: str, k: float = 1.12, run_time: float = 0.7, frame=None, width: float = 5.0):
    """Indicate's swell without its fill: m grows and shrinks back while its frame's border glows
    `color`; the fill never changes, so a filled chip or card keeps its label readable."""
    fr = frame
    for name in ("box", "frame"):
        if fr is None:
            fr = getattr(m, name, None)
    c0, w0 = fr.get_stroke_color(), fr.get_stroke_width()
    col = ManimColor(color)
    state = {"s": 1.0}

    def upd(mob, a):
        b = there_and_back(a)
        s_ = 1 + (k - 1) * b
        mob.scale(s_ / state["s"])
        state["s"] = s_
        fr.set_stroke(interpolate_color(c0, col, b), width=w0 + (width - w0) * b)

    return UpdateFromAlphaFunc(m, upd, run_time=run_time, rate_func=linear)


def wrap_words(s: str, limit: int) -> list[str]:
    """quote_card's row breaking (at spaces, rows of at most `limit` characters)."""
    rows, cur = [], ""
    for w in s.split(" "):
        if cur and len(cur) + 1 + len(w) > limit:
            rows.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    rows.append(cur)
    return rows


def row_tag(text: str, color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """A tag that fits inside one terminal row (the house tag is taller than a 22 pt row)."""
    t = label(text, size, color)
    h = 0.37
    b = RoundedRectangle(width=t.width + 0.36, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def bar_y(t, rows: int) -> float:
    """The title bar's centre y of the house terminal `t` at `rows` rows (bottom edge fixed)."""
    return strip_top(rows) - t.bar_h / 2


def fit(scene, t, rows: int, keep=None, tags=(), run_time: float = 0.8):
    """resize(), with the title-bar tags (on screen) riding along on the bar; the title, which
    frame_tags may have moved left, is lent out of t while resize() runs, so it stays put."""
    y = bar_y(t, rows)
    title, t.title = t.title, None
    try:
        resize(scene, t, rows, keep=keep, run_time=run_time,
               extra=[title.animate.set_y(y), *[m.animate.set_y(y) for m in tags]])
    finally:
        t.title = title


def two_row_stamp(rows, color: str, size: float = CAPTION) -> VGroup:
    """A stamp with two bold rows (stamp()'s look: outlined, opaque dark fill). .frame .text"""
    txt = VGroup(*[S.text(r, size, color, weight="BOLD") for r in rows]).arrange(DOWN, buff=0.06)
    fr = RoundedRectangle(width=txt.width + 0.34, height=txt.height + 0.24, corner_radius=0.06,
                          stroke_color=color, stroke_width=3).set_fill(S.BG, 0.9)
    txt.move_to(fr)
    g = VGroup(fr, txt)
    g.frame, g.text = fr, txt
    return keep_size(g)


def card(text: str, color: str = S.GREY, size: float = CAPTION, h: float = 0.56) -> VGroup:
    """A one-line message card (serif text on an opaque card). .frame .text"""
    t = label(text, size, INK)
    fr = box(t.width + 0.5, h, color, fill=S.BG, fill_opacity=0.95, stroke=2.5, radius=0.12)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def packet_card() -> VGroup:
    """The context packet as ONE user message: a GREEN card holding its three sources (the
    confirmed request, the selected candidates, the saved preferences). .frame .chips"""
    chips = VGroup(*[chip(n, HARNESS, size=CAPTION) for n in ("request", "7 candidates", "preferences")])
    chips.arrange(RIGHT, buff=0.12)
    fr = box(chips.width + 0.3, chips.height + 0.16, HARNESS, fill=S.BG, fill_opacity=0.95, stroke=3,
             radius=0.12)
    chips.move_to(fr)
    g = VGroup(fr, chips)
    g.frame, g.chips = fr, chips
    return g


def travel(m, pts, run_time: float, end_color=None, color_from: float = 0.6):
    """One animation: m's centre runs along the polyline `pts` (one smooth ease over the whole
    length); its chip border turns `end_color` over the last part of the run."""
    pts = [np.array(p, dtype=float) for p in pts]
    seg = [float(np.linalg.norm(b - a)) for a, b in zip(pts, pts[1:])]
    total = sum(seg) or 1.0
    start = m.box.get_stroke_color()
    end = ManimColor(end_color) if end_color is not None else None

    def at(d):
        for p, q, ln in zip(pts, pts[1:], seg):
            if d <= ln:
                return p + (q - p) * (d / ln if ln else 0.0)
            d -= ln
        return pts[-1]

    def upd(mob, a):
        mob.move_to(at(smooth(a) * total))
        if end_color is not None:
            k = min(1.0, max(0.0, (a - color_from) / (1 - color_from)))
            mob.box.set_stroke(interpolate_color(start, end, k))

    return UpdateFromAlphaFunc(m, upd, run_time=run_time, rate_func=linear)


def ride(m, path, run_time: float, end_color=None):
    """One animation: m's centre runs along the curve `path` (smooth); its chip border turns
    `end_color` over the first fifth of the run (one animation, so nothing fights the move)."""
    start = m.box.get_stroke_color()
    end = ManimColor(end_color) if end_color is not None else None

    def upd(mob, a):
        mob.move_to(path.point_from_proportion(smooth(a)))
        if end is not None:
            mob.box.set_stroke(interpolate_color(start, end, min(1.0, a * 5)))

    return UpdateFromAlphaFunc(m, upd, run_time=run_time, rate_func=linear)


def curve_top(path, n: int = 60) -> float:
    """The highest point the curve itself reaches (a Bezier's bounding box holds its handles)."""
    return max(path.point_from_proportion(k / n)[1] for k in range(n + 1))


class SieveRig(Sieves):
    """common.Sieves (V4, S07) with this scene's geometry and chip paths. Two fixes over the shared
    piece (requests in the report): (1) the drop lane sat so far left that pistachio_manchego
    (3.2 wide) crossed the end of the "no raw milk → PA" label and its resting place reached past
    the sieve's end; here the lane, the sieves' length and the list's x leave room for the widest
    chip; (2) survivors came down the lane into the tray row and then slid sideways through the
    chips already there; here they slide along an empty corridor ABOVE the tray and drop straight
    into an empty slot, so any order works (the tray fills left to right in the capture's order).
    .fall(pid) -> (chip, animation) so several survivors can fall in one LaggedStart; .settle()
    after the play makes the chips members. .dissolve(scene) hands the shown mobjects to the
    scene (for the later beats, which move, fade and transform them one by one)."""

    def __init__(self, size: float = CAPTION, **kw):
        Piece.__init__(self, **kw)
        self.size = size
        sv = VGroup()
        self.sieve_lines, self.sieve_labels = [], []
        for (txt, _), y in zip(SIEVES, SIEVE_Y):
            ln = DashedLine([-6.4, y, 0], [SIEVE_END, y, 0], color=HARNESS, stroke_width=5, dash_length=0.12,
                            dashed_ratio=0.7)
            t = label(txt, size, HARNESS).next_to(ln, UP, buff=0.06).align_to(ln, LEFT)
            sv.add(ln, t)
            self.sieve_lines.append(ln)
            self.sieve_labels.append(t)
        self.part("sieves", sv, shown=False)
        lh = mono("excluded_products", size, S.GREY).move_to([LIST_X, 2.55, 0], aligned_edge=LEFT)
        self.part("list_head", lh, shown=False)
        tray = box(12.8, 0.62, HARNESS, dashed=True, stroke=2).move_to([0, TRAY_Y, 0])
        self.part("tray", tray, shown=False)
        self.rows_y = {}
        k_by_sieve: dict[int, int] = {}
        for pid, reason in EXCLUDED.items():
            si = [r for _, r in SIEVES].index(reason)
            k = k_by_sieve.get(si, 0)
            k_by_sieve[si] = k + 1
            n_here = sum(1 for r in EXCLUDED.values() if r == reason)
            off = 0.0 if n_here == 1 else (0.22 if k == 0 else -0.22)
            self.rows_y[pid] = SIEVE_Y[si] + off
        self.chips, self.reasons, self.rejects, self.tray_chips = {}, {}, [], {}
        widths = [cheese_chip(p).width for p in SURVIVORS]
        gap = 0.2
        x = -(sum(widths) + gap * (len(widths) - 1)) / 2
        self._tray_layout = {}
        for p, w in zip(SURVIVORS, widths):
            self._tray_layout[p] = x + w / 2
            x += w + gap
        self._pending = []
        # the widest chip in the lane clears the labels on its left and the list on its right
        wmax = max(cheese_chip(p).width for p in CHEESES)
        assert LANE_X - wmax / 2 > max(t.get_right()[0] for t in self.sieve_labels) + 0.1
        assert LANE_X + wmax / 2 < LIST_X - 0.15

    def fall(self, pid: str, run_time: float = 1.0):
        """(chip, animation): one chip's whole way, as one animation."""
        c = cheese_chip(pid)
        c.move_to([LANE_X, TOP_Y, 0])
        self.chips[pid] = c
        h = c.height
        if pid in EXCLUDED:
            si = [r for _, r in SIEVES].index(EXCLUDED[pid])
            rest = [LANE_X, SIEVE_Y[si] + h / 2 + 0.03, 0]
            y = self.rows_y[pid]
            dest = [LIST_X + c.width / 2, y, 0]
            r = mono(EXCLUDED[pid], self.size, ERR)
            r.move_to([LIST_X + c.width + 0.15 + r.width / 2, y, 0])
            assert r.get_right()[0] < 6.58, pid
            self.reasons[pid] = r
            anim = Succession(FadeIn(c, shift=DOWN * 0.15, run_time=run_time * 0.15),
                              travel(c, [c.get_center(), rest], run_time * 0.3),
                              Wait(run_time=run_time * 0.12),
                              travel(c, [rest, dest], run_time * 0.28, ERR, 0.0),
                              FadeIn(r, shift=LEFT * 0.1, run_time=run_time * 0.15))
            self._pending.append((pid, c, r))
        else:
            sx = self._tray_layout[pid]
            pts = [c.get_center(), [LANE_X, STAGE_Y, 0], [sx, STAGE_Y, 0], [sx, TRAY_Y, 0]]
            anim = Succession(FadeIn(c, shift=DOWN * 0.15, run_time=run_time * 0.15),
                              travel(c, pts, run_time * 0.85, HARNESS, 0.75))
            self._pending.append((pid, c, None))
        return c, anim

    def settle(self, scene, anims=()):
        """After the play: the fallen chips (and reasons) become members of the piece."""
        _drop_groups(scene, list(anims))
        for pid, c, r in self._pending:
            mobs = [m for m in (c, r) if m is not None]
            for m in mobs:
                if m in scene.mobjects:
                    scene.remove(m)
            self.add(*mobs)
            if r is not None:
                self.rejects.append(pid)
            else:
                self.tray_chips[pid] = c
        self._pending = []
        self._ensure(scene)

    def drop_some(self, scene, pids, each: float = 0.9, lag: float = 0.45):
        """Play the falls of `pids` (survivors may overlap in time: lag; a reject falls alone)."""
        anims = [self.fall(p, each)[1] for p in pids]
        if len(anims) == 1:
            scene.play(anims[0])
        else:
            scene.play(LaggedStart(*anims, lag_ratio=lag))
        self.settle(scene, anims)

    def dissolve(self, scene) -> dict:
        """The piece leaves the scene and its shown parts and chips become scene mobjects
        (later beats move, fade and transform them one by one). Returns them by name."""
        out = {"list_head": self.parts["list_head"], "tray": self.parts["tray"]}
        scene.remove(self)
        shown = [out["list_head"], out["tray"], *self.chips.values(), *self.reasons.values()]
        scene.add(*shown)
        return out


def shelf():
    """Beat 6: a GREY shelf holding all twelve products (catalog order, two per row: `comte`
    top right, where the arm reaches it from above). .frame .chips .label"""
    chips = {p: cheese_chip(p) for p in CHEESES}
    pairs = [CHEESES[i:i + 2] for i in range(0, 12, 2)]
    w0 = max(chips[a].width for a, _ in pairs)
    x0, x1 = -6.15, -6.15 + w0 + 0.3
    for r, (a, b) in enumerate(pairs):
        y = 1.2 - r * 0.5
        place(chips[a], left=x0, cy=y)
        place(chips[b], left=x1, cy=y)
    allc = VGroup(*chips.values())
    fr = box(allc.width + 0.5, allc.height + 0.42, S.GREY, fill_opacity=0.05, stroke=2.5)
    fr.move_to(allc)
    lb = _mixed_row(["`get_catalog()`", "· all 12, in both modes"], CAPTION, S.GREY)
    place(lb, left=fr.get_left()[0] + 0.05, top=fr.get_bottom()[1] - 0.12)
    g = VGroup(fr, allc, lb)
    g.frame, g.chips, g.label = fr, chips, lb
    return g


def mini_sieves(center) -> VGroup:
    """Beat 6: the packet's three sieves, small (shapes only) with one GREEN label under them."""
    lines = VGroup(*[DashedLine([-0.75, 0, 0], [0.75, 0, 0], color=HARNESS, stroke_width=5, dash_length=0.12,
                                dashed_ratio=0.7).shift(UP * (0.36 - 0.36 * k)) for k in range(3)])
    lb = label("the packet's sieves", CAPTION, HARNESS).next_to(lines, DOWN, buff=0.16)
    g = VGroup(lines, lb).move_to(center)
    g.lines, g.label = lines, lb
    return g


def slide13() -> VGroup:
    """Slide 13 redrawn small (our drawing): a GREY dashed "Instructions" box holding the dashed
    box "Retrieved information (RAG)". .outer .title .rag .rag_box"""
    outer = box(5.3, 2.0, S.GREY, dashed=True, stroke=2.5)
    ttl = label("Instructions", CAPTION, S.GREY)
    place(ttl, left=outer.get_left()[0] + 0.25, top=outer.get_top()[1] - 0.14)
    rt = label("Retrieved information (RAG)", CAPTION, INK)
    rb = box(rt.width + 0.5, 0.62, S.GREY, dashed=True, stroke=2.5)
    rag = VGroup(rb, rt)
    rt.move_to(rb)
    rag.move_to(outer.get_center() + DOWN * 0.22)
    g = VGroup(outer, ttl, rag)
    g.outer, g.title, g.rag, g.rag_box = outer, ttl, rag, rb
    return g


class ContextPacket(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0 · step 8: --preview-context, offline
        tr = tracker("Context", 8)
        c306 = readme_chip("README.md · line 306", R306)
        after = grey_tag("printed after the live runs")
        top = VGroup(c306, after).arrange(RIGHT, buff=0.2)
        top.move_to([CHIP_RIGHT - top.width / 2, TOPCHIP_Y, 0])
        assert top.get_top()[1] < tr.get_bottom()[1] - 0.02 or top.get_left()[0] > tr.get_right()[0] + 0.1
        t = term(container=True, rows=T_ROWS)
        ft = frame_tags(t, offline_tag())
        off = ft[0]
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), run_time=0.5)
            self.play(FadeIn(c306, shift=DOWN * 0.1), run_time=0.5)
            self.play(flash(c306.phrase, TURN, 1.06), run_time=0.7)
            vo.wait_until("after the live runs")
            self.play(FadeIn(after, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Without a key")
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            type_cmd(self, t, PREV.cmd, 1.3)
            out = show(self, t, PREV, 2, L3, L4, TOOLS_FOLD, (208, 213), run_time=0.8)
            vo.wait_until("offline")                    # the output is up before "Both modes share"
            self.play(FadeIn(off, shift=DOWN * 0.1), run_time=0.4)
            self.play(flash(off.text, HARNESS, 1.15), run_time=0.5)
            vo.wait_until("Both modes share")
            keys = [substring(out[i], k) for i, k in zip((1, 2, 3), SAME_KEYS)]
            self.play(keys[0].animate.set_color(HARNESS), run_time=0.4)
            vo.wait_until("message and tools")
            self.play(keys[1].animate.set_color(HARNESS), run_time=0.4)
            self.play(keys[2].animate.set_color(HARNESS), run_time=0.4)
            vo.wait_until("only the packets differ")
            self.play(flash(substring(out[4], '"basic"'), TURN, 1.2), run_time=0.7)

        # ========================================================== 1 · basic: none; enriched: three sources
        with self.voiceover(SAY[1]) as vo:
            r210 = out[6]
            bt = row_tag("basic: none")
            beside(bt, t, r210, buff=0.45)
            pin(self, r210, bt, run_time=0.4)
            self.play(flash(r210.glyphs, S.GREY, 1.08), run_time=0.6)
            vo.wait_until("Enriched has three")
            en = show(self, t, PREV, (214, 216), 218, 220, "…", 241, 243, "…", 357, 359, "…", run_time=0.9)
            trust_rows = {220: en[4], 243: en[7], 359: en[10]}
            for anchor, (n, val) in zip(("the confirmed request", "shop data", "and saved preferences"), TRUSTS):
                vo.wait_until(anchor)
                v = substring(trust_rows[n], val)
                self.play(v.animate.set_color(HARNESS), run_time=0.35)
                self.play(flash(v, HARNESS, 1.12), run_time=0.5)

        # ========================================================== 2 · V4: twelve cheeses, three sieves
        sv = SieveRig()
        ill = illustration_tag()
        place(ill, right=SAFE - 0.15, cy=2.55)
        lr = lref("13, 16")
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(top), run_time=0.3)
            r369 = show(self, t, PREV, 369, run_time=0.3)[0]
            fit(self, t, 3, keep=[en[10], en[11], r369], tags=[off], run_time=0.6)
            sv.reveal(self, "sieves", "tray", extra=[FadeIn(ill)], run_time=0.5)
            for i, anchor in enumerate(("enough stock", "no raw milk", "no nut allergens")):
                vo.wait_until(anchor)                   # each sieve lights on its clause (they come ~1 s apart)
                fall = sv.fall(("epoisses", "bucheron", "mimolette")[i], 0.8)[1]   # ... as a survivor falls
                self.play(Indicate(sv.sieve_labels[i], color=HARNESS, scale_factor=1.12, run_time=0.8),
                          sv.sieve_lines[i].animate(run_time=0.8, rate_func=there_and_back).set_stroke(width=7), fall)
                sv.settle(self, [fall])
            vo.wait_until("Munster has no stock")
            self.play(*sv.parts_in("list_head"), run_time=0.3)
            sv.drop_some(self, ["munster"], 1.0)
            vo.wait_until("Brie and Comté")
            sv.drop_some(self, ["brie"], 0.9)
            sv.drop_some(self, ["comte"], 0.9)
            vo.wait_until("and two nut cheeses")
            sv.drop_some(self, ["walnut_chevre"], 0.9)
            sv.drop_some(self, ["pistachio_manchego"], 0.9)
            sv.drop_some(self, ["taleggio"], 0.8)
            vo.wait_until("Seven survive")
            sv.drop_some(self, ["manchego", "gouda", "halloumi"], 0.75, lag=0.3)
            tray_chips = [sv.tray_chips[p] for p in SURVIVORS]

        # the recorded check: the staff's saved table (cell 18), folded
        inset = recorded_box(REC18, *C18_ROWS, header="Agent Harness · cell 18 · saved output (folded)",
                             tag_=False)
        place(inset, left=-6.45, top=2.78)
        rtag = recorded_tag()
        rows18 = inset.rows
        parts = {"list_head": sv.parts["list_head"], "tray": sv.parts["tray"]}
        tray = parts["tray"]
        self.play(*sv.parts_out("sieves"), FadeOut(VGroup(t, off)), run_time=0.5)
        sv.dissolve(self)
        self.play(*[m.animate.shift(UP * (TRAY_LOW - TRAY_Y)) for m in (tray, *tray_chips)], run_time=0.6)
        place(rtag, left=inset.frame.get_right()[0] + 0.25, bottom=inset.frame.get_bottom()[1])
        assert inset.frame.get_right()[0] < LIST_X - 0.15 and inset.get_bottom()[1] > tray.get_top()[1] + 0.1
        self.play(FadeIn(inset, shift=UP * 0.1), FadeIn(rtag, shift=LEFT * 0.1), run_time=0.5)
        oks = [substring(rows18[k + 1], "True" if C18_OK[p] else "False") for k, p in enumerate(C18_PIDS)]
        self.play(LaggedStart(*[o.animate.set_color(HARNESS) for o, p in zip(oks, C18_PIDS) if C18_OK[p]],
                              lag_ratio=0.15),
                  LaggedStart(*[pulse(c, HARNESS) for c in tray_chips], lag_ratio=0.15), run_time=1.1)
        self.play(LaggedStart(*[o.animate.set_color(ERR) for o, p in zip(oks, C18_PIDS) if not C18_OK[p]],
                              lag_ratio=0.15), run_time=0.5)
        self.wait(0.5)

        # ========================================================== 3 · slide 13: "retrieved information" here
        s13 = slide13()
        place(s13, left=-6.4, top=2.8)
        ctag = concept_tag()
        place(ctag, right=s13.outer.get_right()[0], top=s13.outer.get_bottom()[1] - 0.1)
        rag_b = s13.rag_box
        ax = rag_b.get_left()[0] + 0.55                 # left of the concept tag, which sits under the box
        arr = Arrow([ax, rag_b.get_bottom()[1] - 0.02, 0], [ax, tray.get_top()[1] + 0.02, 0], buff=0.05,
                    color=LOOKUP, stroke_width=5, max_tip_length_to_length_ratio=0.08)
        assert ctag.get_left()[0] > ax + 0.2
        cap1 = label("here: a Python filter over 12 cheeses + saved preferences", CAPTION, INK)
        cap2 = label("no vector search (lecture 5)", CAPTION, S.GREY)
        caps = VGroup(cap1, cap2).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        place(caps, left=arr.get_right()[0] + 0.35, cy=-1.55)
        assert caps.get_right()[0] < SAFE and caps.get_top()[1] < -0.2
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(inset, rtag)), run_time=0.4)
            self.play(FadeIn(s13.outer), FadeIn(s13.title), FadeIn(lr), run_time=0.5)   # the tag cites this drawing
            self.play(FadeIn(s13.rag, shift=UP * 0.1), FadeIn(ctag, shift=UP * 0.08), run_time=0.5)
            self.play(flash(s13.rag[1], S.GREY, 1.08), run_time=0.6)
            vo.wait_until("here it's a Python filter")
            self.play(GrowArrow(arr), run_time=0.6)
            self.play(FadeIn(cap1, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("not the vector search")
            self.play(FadeIn(cap2, shift=RIGHT * 0.1), run_time=0.5)

        # ========================================================== 4 · slide 22: the packet goes in the user lane
        p = src_panel("formaggio/agents/context.py", 142, 144, wrap=True, size=20)
        _with_header(p, "formaggio/agents/context.py · lines 142–144 · wrapped")
        place(p, left=-6.45, top=PANEL_TOP)
        ln = Lanes(lane_h=0.8)
        m1 = card("customer message")
        m1.move_to(ln.slot("user", 0, m1.width))
        ln.filled["user"].append(m1)
        ln.parts["user"].add(m1)
        ufr = ln.lanes["user"].frame
        ln.counter.move_to([ufr.get_right()[0] - 0.12 - ln.counter.width / 2, ln.lanes["user"].title.get_center()[1], 0])
        place(ln, cx=0, top=LANES_TOP)
        assert ln.get_top()[1] < p.get_bottom()[1] - 0.05, (ln.get_top(), p.get_bottom())
        env = packet_card()
        dest = ln.slot("user", 0, env.width)            # the trace: messages[0] is the context packet,
        env.move_to([dest[0], TRAY_LOW, 0])             # messages[1] the customer's request (S06 too)
        m1_dest = [dest[0] + env.width / 2 + 0.2 + m1.width / 2, m1.get_center()[1], 0]
        assert m1_dest[0] + m1.width / 2 < ufr.get_right()[0] - 0.1
        st = stamp("data, not instructions", HARNESS, size=CAPTION, angle=0.0)
        place(st, left=env.get_right()[0] + 0.3, cy=TRAY_LOW)
        assert st.get_right()[0] < SAFE + 0.1 and env.get_top()[1] < ufr.get_bottom()[1] - 0.05
        rule = concept_box("system rule?")
        sfr = ln.lanes["system"].frame
        place(rule, cx=4.6, cy=1.0)
        assert rule.get_left()[0] > p.code.get_right()[0] + 0.15
        b143 = p.bar(143)
        b142 = p.bar(142)
        s143 = VGroup(p.span(143, '"Retrieved context (data, not'), p.span(143, 'instructions):\\n"'))
        s144 = p.span(144, 'Message(role="user"')
        lr22 = lref("22")
        with self.voiceover(SAY[4]) as vo:
            olds = [s13, ctag, arr, caps, parts["list_head"], ill,
                    *[sv.chips[x] for x in sv.rejects], *[sv.reasons[x] for x in sv.rejects]]
            self.play(*[FadeOut(m) for m in olds], FadeOut(lr), run_time=0.5)
            self.play(FadeIn(p, shift=UP * 0.1), FadeIn(ln), FadeIn(lr22), run_time=0.6)
            lr = lr22
            vo.wait_until("Into a user message")
            self.play(s144.animate.set_color(LOOKUP), run_time=0.4)
            self.play(flash(ln.lanes["user"].title, HARNESS, 1.1), run_time=0.5)
            vo.wait_until("headed retrieved context")
            self.play(FadeIn(b143), s143.animate.set_color(TURN), run_time=0.4)
            mid = env.chips[1]
            gone = LaggedStart(*[FadeOut(c, scale=0.6) for c in tray_chips], lag_ratio=0.06)
            self.play(gone, run_time=0.45)
            _drop_groups(self, [gone])
            self.remove(*tray_chips)
            self.play(ReplacementTransform(tray, mid.box), FadeIn(mid.text, scale=0.8), run_time=0.6)
            self.play(FadeIn(env.chips[0], shift=RIGHT * 0.1), FadeIn(env.chips[2], shift=LEFT * 0.1), run_time=0.4)
            self.play(Create(env.frame), run_time=0.35)
            self.add(env)
            self.play(FadeIn(st, scale=1.15), run_time=0.35)
            # the customer message makes room first, then the packet rises into slot 0 (nothing crosses)
            self.play(m1.animate.move_to(m1_dest), FadeOut(st), run_time=0.45)
            self.play(env.animate.move_to(dest), run_time=0.6)
            ln.filled["user"] = [env, m1]
            self.remove(env)
            ln.add(env)
            self.play(*ln.count_to(2), run_time=0.6)
            vo.wait_until("so it cannot pose")
            self.play(FadeOut(b143), run_time=0.2)          # the bars overlap: one at a time (143's string stays YELLOW)
            self.play(FadeIn(b142), FadeIn(rule, shift=DOWN * 0.1), run_time=0.4)
            # the card drops to the system lane's top edge and is sent back, dimmed. (Not Lanes.turn_back:
            # its two .animate builders in one Succession share the card's .target, so the card only
            # dimmed in place; see the report.) Two plays, one builder each.
            near = [rule.get_center()[0], sfr.get_top()[1] + rule.height / 2 + 0.06, 0]
            home = rule.get_center().copy()
            self.play(rule.animate(rate_func=rush_into).move_to(near), run_time=0.5)
            self.play(rule.animate.move_to(home).set_opacity(0.4), run_time=0.6)
            vo.wait_until("That's the lecture's two lanes")
            self.play(FadeOut(rule), run_time=0.3)      # the turned-back ghost leaves before the lanes speak
            self.play(flash(ln.lanes["system"].frame, S.GREY, 1.02), flash(ln.lanes["user"].frame, HARNESS, 1.02),
                      run_time=0.7)
            vo.wait_until("instructions in the system lane")
            self.play(flash(ln.lanes["system"].title, TURN, 1.1), pulse(ln.inst_card, TURN, 1.05), run_time=0.7)
            vo.wait_until("evidence in the user lane")
            self.play(flash(ln.lanes["user"].title, HARNESS, 1.1), pulse(env, HARNESS, 1.06), run_time=0.7)

        # ========================================================== 5 · ponder: can the model still pick Comté?
        row_chips = VGroup(*[cheese_chip(x, ERR) for x in EXCLUDED])
        row_chips.arrange(RIGHT, buff=0.1)
        row_head = mono("excluded_products", CAPTION, S.GREY)
        exc = VGroup(row_head, row_chips).arrange(RIGHT, buff=0.2)
        comte = row_chips[list(EXCLUDED).index("comte")]
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(p, b142)), run_time=0.5)
            self.play(ln.animate.shift(UP * (LANES_UP - ln.get_top()[1])), run_time=0.7)
            place(exc, cx=0, top=ln.get_bottom()[1] - 0.32)
            assert exc.get_right()[0] < SAFE + 0.1 and exc.get_left()[0] > -SAFE - 0.1
            vo.wait_until("The enriched packet")
            self.play(FadeIn(exc, shift=DOWN * 0.1), run_time=0.5)
            self.play(pulse(comte, S.GREY, 1.25), run_time=0.8)
            vo.wait_until("Can the model")
            self.play(pulse(comte, S.GREY, 1.25), run_time=0.8)
            vo.wait_until("And does anything")
            self.play(pulse(env, HARNESS, 1.05), run_time=0.8)
        pcard = ponder_at(self, PONDER, seconds=8.0)
        assert pcard.get_top()[1] < exc.get_bottom()[1] - 0.05

        # ========================================================== 6 · yes: get_catalog returns all twelve
        exc10 = excerpt_chip(R10, "formaggio/agents/tools.py · line 10 (excerpt)",
                             line=source_line("formaggio/agents/tools.py", 10))
        place(exc10, right=SAFE, top=2.88)
        sh = shelf()
        ill6 = illustration_tag()
        place(ill6, left=sh.frame.get_left()[0], bottom=sh.frame.get_top()[1] + 0.15)
        sv6 = mini_sieves([1.3, 0.25, 0])
        cart = cart_token()
        cart.move_to([3.4, -0.3, 0])
        ct = sh.chips["comte"]
        arm = CubicBezier(cart.get_top() + UP * 0.05, [3.4, 2.05, 0], [ct.get_center()[0], 2.05, 0],
                          ct.get_top() + UP * 0.04)
        arm.set_stroke(CLOUD, 5)
        ride_path = CubicBezier(ct.get_center(), [ct.get_center()[0], 2.0, 0], [3.4, 2.0, 0], [3.4, -0.78, 0])
        stc = two_row_stamp(["CartCheck · shipping: comte", "reported, not stopped (acts 1–2)"], HARNESS)
        place(stc, cx=3.4, top=-1.15)
        gate = Gate(text="blocked in act 3", color=HARNESS, gate_w=0.9, gate_h=1.2)
        gate.move_to([5.35, -0.15, 0])
        capA = label("selection narrows", 24, INK)
        capB = label("· validation decides", 24, INK)
        capS = label("(README.md · line 336)", CAPTION, S.GREY)
        capg = VGroup(capA, capB, capS).arrange(RIGHT, buff=0.18)
        place(capg, cx=0, bottom=-3.4)
        assert gate.get_right()[0] < SAFE + 0.1 and stc.get_right()[0] < SAFE + 0.1
        assert sh.frame.get_right()[0] < sv6.get_left()[0] - 0.15
        assert curve_top(arm) < exc10.get_bottom()[1] - 0.15
        assert ill6.get_top()[1] < tr.get_bottom()[1] - 0.1 and ill6.get_right()[0] < ct.get_left()[0] - 0.3
        assert curve_top(ride_path) + ct.height / 2 < exc10.get_bottom()[1] - 0.1
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(pcard), FadeOut(VGroup(ln, exc)), FadeOut(lr), run_time=0.5)
            vo.wait_until("the get catalog tool")
            self.play(FadeIn(sh.frame), LaggedStart(*[FadeIn(c) for c in sh.chips.values()], lag_ratio=0.06),
                      FadeIn(exc10, shift=DOWN * 0.1), run_time=0.9)
            self.play(FadeIn(sh.label, shift=UP * 0.05), FadeIn(sv6), FadeIn(cart), FadeIn(ill6), run_time=0.5)
            self.play(Create(arm), run_time=0.7)
            self.play(ride(ct, ride_path, 1.1, CLOUD), arm.animate.set_stroke(opacity=0.35), run_time=1.1)
            vo.wait_until("and in act 2 Cart Check")
            self.play(FadeIn(stc, scale=1.2), run_time=0.4)
            self.play(flash(stc.text[1], HARNESS, 1.06), run_time=0.6)
            vo.wait_until("Selection narrows")
            self.play(FadeIn(capA, shift=UP * 0.1), flash(sv6.lines, HARNESS, 1.1), run_time=0.6)
            vo.wait_until("but validation decides")
            self.play(FadeIn(capB, shift=UP * 0.1), FadeIn(capS), run_time=0.5)
            vo.wait_until("the act 3 workflow blocks it")
            self.play(FadeIn(gate, shift=DOWN * 0.4), run_time=0.5)
            self.play(gate.slam(HARNESS), run_time=0.4)

        # ========================================================== 7 · step 9: the optional baseline; your turn
        t2 = term(container=True, rows=8)
        ft2 = frame_tags(t2, nokey_tag(), live_tag())
        nk2, lv2 = ft2[0], ft2[1]
        c265 = top_chip(R265, where="README.md · lines 265–266", expected=True)
        nb_row = _mixed_row(["notebook:", f"`{NB_BASIC}`", "·", f"`{NB_ENR}`"], CAPTION, INK)
        nb = card_rows([nb_row, ("(README.md · line 332)", S.GREY)])
        place(nb, left=-6.45, top=c265.get_bottom()[1] - 0.25)
        assert nb.get_bottom()[1] > t2.box.get_top()[1] + 0.08
        # S06's command, folded once after the `;` (" \\" + 4-space indent, as the terminals fold): inside
        # the quotes the backslash is Python's line continuation, so the two rows paste and run as typed
        ship_rows = ["python -c 'from acts.act2_context import print_shipping_demo; \\", "    print_shipping_demo()'"]
        assert ship_rows[0][:-2] + " " + ship_rows[1].strip() == SHIP.cmd, ship_rows
        tc = turn_card([PREV.cmd, ("\n".join(ship_rows), "extra · offline · the PA/NY check"), BASE.cmd,
                        (Prose("live · two runs · billed per token"), COST)], width=11.6)
        ship = tc.rows[1]                               # its continuation row keeps its 4-space indent
        cw = mono("x" * 40, CAPTION, INK).width / 40
        VGroup(ship[1], ship[2]).shift(RIGHT * 4 * cw)
        off2 = label("offline · free", CAPTION, HARNESS)  # a GREEN note: a boxed tag would touch the ▶ tag above it
        place(off2, left=tc.rows[0].get_right()[0] + 0.35, cy=tc.rows[0].get_center()[1])
        tc.add(off2)
        place(tc, cx=0, top=nb.get_bottom()[1] - 0.2)
        assert tc.get_bottom()[1] > -3.55, tc.get_bottom()
        assert off2.get_right()[0] < tc.frame.get_right()[0] - 0.1
        assert ship.get_right()[0] < tc.frame.get_right()[0] - 0.2, (ship.get_right(), tc.frame.get_right())
        apart(off2, tc.tag, 0.04)
        assert tc.get_top()[1] < nb.get_bottom()[1] - 0.05
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(sh, ill6, sv6, cart, arm, ct, stc, gate, capg, exc10)), tr.goto(9), run_time=0.5)
            self.play(FadeIn(t2, shift=UP * 0.2), FadeIn(nk2, shift=DOWN * 0.1), run_time=0.4)
            type_cmd(self, t2, BASE.cmd, 0.85)
            self.play(FadeIn(lv2, shift=DOWN * 0.1), run_time=0.3)
            show(self, t2, BASE, 3, 5, ASK, 10, STOP, wrap=True, run_time=0.6)
            vo.wait_until("in both modes")
            self.play(FadeIn(nb, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("For standard")
            self.play(FadeIn(c265, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("so little may change")
            self.play(flash(c265.phrase, TURN, 1.05), run_time=0.7)
            vo.wait_until("Pause and run")
            self.play(FadeOut(VGroup(t2, ft2)), run_time=0.4)
            self.play(FadeIn(tc, scale=0.97), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame

        # ========================================================== 8 · checkpoint; end of part 1
        q = quote_card(336, lines=[Q336A, Q336B], wrap=Q_WRAP, header="README.md · line 336 (excerpt)",
                       expected=False)
        place(q, left=-6.45, top=2.8)
        etag = expected_tag()
        place(etag, left=q.frame.get_left()[0], top=q.frame.get_bottom()[1] - 0.12)
        half = ActionBoundary(width=8.6, row_h=0.55, moves=False).prefill(1)   # every row's text, as S05 wrote them
        seen = VGroup(*[half.parts[n] for n in ("heads", "who", "pills", "blue", "green")])
        half.shift(RIGHT * (SAFE + 0.05 - seen.get_right()[0]) + UP * (-0.1 - seen.get_center()[1]))
        assert q.get_right()[0] < seen.get_left()[0] - 0.15, (q.get_right(), seen.get_left())
        lr8 = lref("22")
        cart8 = cart_token()
        place(cart8, right=seen.get_left()[0] - 0.35, cy=half.cell("sub", "blue").get_center()[1])
        cap8 = VGroup(label("part 2:", CAPTION, S.GREY), label("the harness takes the route", CAPTION, S.GREY))
        cap8.arrange(DOWN, buff=0.06, aligned_edge=RIGHT)
        place(cap8, right=cart8.get_right()[0] + 0.1, top=cart8.get_bottom()[1] - 0.2)
        assert cap8.get_left()[0] > -SAFE - 0.1
        for a_, b_ in ((cart8, q), (cart8, etag), (cap8, etag), (cap8, seen), (etag, seen), (cart8, seen)):
            apart(a_, b_)
        n_first = len(wrap_words(Q336A, Q_WRAP))
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(tc, nb, c265)), run_time=0.5)
            self.play(FadeIn(q, shift=UP * 0.1), FadeIn(etag), FadeIn(half), FadeIn(lr8), run_time=0.6)
            self.play(half.light("context"), run_time=0.35)
            m, an = half.fill("context", "the packet in the data lane")
            self.play(*an, run_time=0.6)
            vo.wait_until("but validation decides")
            self.play(flash(VGroup(*q.rows[:n_first]), TURN, 1.03), run_time=0.8)
            vo.wait_until("and today's request")
            self.play(flash(VGroup(*q.rows[n_first:]), TURN, 1.03), run_time=0.8)
            vo.wait_until("In part 2")
            self.play(FadeIn(cart8, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(cap8, shift=UP * 0.08), run_time=0.5)
            self.play(cart8.animate.shift(RIGHT * 0.12), run_time=0.4)
        self.wait(0.6)
        self.play(FadeOut(VGroup(q, etag, half, lr8, cart8, cap8, tr)), run_time=0.8)
        self.wait(0.3)
