"""S03 · Games stop early 对局会提前结束 — Act II: game A stops on move 5; 9! counts it 24 times.

Bars 21-32 (0:48.0-1:16.8) of script.md; scene time 0 is the downbeat of bar 21. The picture is a pure
function of the scene time (State.update), as in s01_open; the notes come from the same numbers (Sounds).

    21-22  the 24 dim points of S02 gather into board A's grid (from rest: frame 0 is S02's last frame);
           game A replays, one mark per beat (the motif);
           22.2 the top-row win line; 22.3 the game stops: a stop bar drops after slot 5 of a move timeline,
           "第 5 步 · X 赢 · MOVE 5 · X WINS" (c07)
    23-25  but 9! kept going: four dashed ghost marks, O6 X5 O8 X7 (moves 6-9, never glowing); 24.1-25.3 the
           ghosts run through all 24 orders of the four empty squares, one per sixteenth (adjacent swaps, so
           moves 6 and 8 stay O, 7 and 9 X), the readout counts 1 -> 24; 25.3 "4 × 3 × 2 × 1 = 24" beside
           the timeline's ghost slots (lining figures: s02_fill.maths), clear of the captions
    26-28  the 24 ghost endings fly out from behind the board as a spread deck: 24 small copies in two fanned
           wings of 12 (no overlaps), each with the same five bright real moves and its own dashed ending
           (c08); 27.4 "幽灵对局 · GHOST GAMES" (c09); the copies sway
    29     the fan folds back; the board shrinks onto the left end of the move timeline, which rises and widens
           (X's slots cyan, O's amber); X's slots 1, 3, 5 light with a small X above each (X's 1st, 2nd, 3rd
           mark), "第 3 个 X：第 5 步 · X'S 3RD MARK: MOVE 5" under slot 5 (c10; it leaves with c10, at 31.1+)
    30-31  one tiny real board per end move rises above slots 5-9, trailing its ghost endings as a dashed
           fan: ×24 ×6 ×2 ×1 ×1, one per beat (c11)
    32     the move-5 board glides to the centre and grows; the rest fades; 32.4 three panel frames draw

Hand-over from S02 (a cut): the 24 dim points at s02_fill.ORDER_SCREEN, drawn the same way (order_dots).
Hand-over to S04 (a cut, 33.1): camera home (0, 0, full width); game A's final board XXXOO.... with its
glowing top-row win line, centred at HANDOVER["board"] with cell HANDOVER["cell"] (no move numbers), drawn
as S01 draws board A (mark_ink, S01's win line), every stroke x sqrt(0.6 / 1.4) as the board shrank;
three hairline panel frames HANDOVER["panels"] (centre x, centre y, width, height) above it; the HUD
section label common.section_hud("§2 · 对局会提前结束 · GAMES STOP EARLY") stays.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from manim import DashedVMobject, Line, Mobject, Rectangle, VGroup

from explainer.short import BG, BeatScene, FONT_MONO, INK, INK_DIM, INK_FAINT, WHITE, RollingCounter

from common import (GAME_A, OC, PITCH, XC, Cam, Ink, InkText, Shot, Sounds, W, H, bi_label, box,
                    clamp01, ease_in_cubic, ease_in_out_cubic, ease_in_out_sine, ease_out_cubic, ease_out_quad,
                    grid_lines, lerp, mark_ink, move_digit, o_template, player, pulse,
                    section_hud, seg, square_centre, tag, win_template, x_template)
from s02_fill import ORDER_DOTS, ORDER_SCREEN, Glyphs, Hairlines, maths, order_dots, stacked_label

# ---------------------------------------------------------------- the plan's clock (bar 21 = scene time 0)
BEAT, BAR = 0.6, 2.4
FIRST_BAR = 21


def bb(bar: int, beat: float = 1.0) -> float:
    """Musicians' count, as script.md writes it: bb(22, 2.5) is "22.2+" (scene time)."""
    return (bar - FIRST_BAR) * BAR + (beat - 1) * BEAT


END = bb(33)                                       # 28.8 s: 12 bars

# ---------------------------------------------------------------- the game and its ghosts (asserted)
WIN_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def replay(moves):
    """(cells, winner, winning line) after the moves, X first; asserts nobody had won before the last."""
    cells = ["."] * 9
    for k, s in enumerate(moves):
        assert cells[s] == "." and _won(cells) is None, (moves, k)
        cells[s] = player(k)
    w = _won(cells)
    return "".join(cells), (w[0] if w else None), (w[1] if w else None)


def _won(cells):
    for a, b, c in WIN_LINES:
        if cells[a] != "." and cells[a] == cells[b] == cells[c]:
            return cells[a], (a, c)
    return None


CELLS_A, WIN_A_SYM, WIN_A_LINE = replay(GAME_A)
assert CELLS_A == "XXXOO...." and WIN_A_SYM == "X" and WIN_A_LINE == (0, 2)
GHOST_SQ = tuple(s for s in range(9) if CELLS_A[s] == ".")
assert GHOST_SQ == (5, 6, 7, 8)
FIRST_GHOSTS = (6, 5, 8, 7)                        # moves 6-9 drawn first: O on 6, X on 5, O on 8, X on 7


def _sjt(n: int):
    """All n! orders of n items by adjacent swaps (Steinhaus-Johnson-Trotter), from the identity."""
    perm, dirs, out = list(range(n)), [-1] * n, []
    out.append(perm[:])
    while True:
        mob, mi = -1, -1
        for i, v in enumerate(perm):
            j = i + dirs[v]
            if 0 <= j < n and perm[j] < v and v > mob:
                mob, mi = v, i
        if mob < 0:
            return out
        j = mi + dirs[mob]
        perm[mi], perm[j] = perm[j], perm[mi]
        for v in range(mob + 1, n):
            dirs[v] = -dirs[v]
        out.append(perm[:])


ORDERS = [tuple(FIRST_GHOSTS[p] for p in perm) for perm in _sjt(4)]   # squares of moves 6, 7, 8, 9
assert len(ORDERS) == 24 == math.factorial(4) and len(set(ORDERS)) == 24
assert set(ORDERS) == set(itertools.permutations(GHOST_SQ)) and ORDERS[0] == FIRST_GHOSTS
assert all(sum(a != b for a, b in zip(p, q)) == 2 for p, q in zip(ORDERS, ORDERS[1:]))   # one swap a step
_b = list(CELLS_A)
for _k, _s in enumerate(FIRST_GHOSTS, 6):
    _b[_s] = "X" if _k % 2 else "O"
assert [l for l in WIN_LINES if _b[l[0]] != "." and _b[l[0]] == _b[l[1]] == _b[l[2]]] == [(0, 1, 2)]   # no 2nd line
assert sum(1 for p in itertools.permutations(range(9)) if p[:5] == GAME_A) == 24       # 9! counts game A 24 times


def ghost_sym(move: int) -> str:
    """Moves 6 and 8 are O's, 7 and 9 X's (1-based move numbers)."""
    return "X" if move % 2 else "O"


# one example game per end move (script.md bars 30-31), each checked: who wins, on which move, on which line
END_GAMES = {5: GAME_A, 6: (0, 3, 1, 4, 6, 5), 7: (0, 1, 2, 3, 4, 5, 6), 8: (0, 4, 8, 2, 6, 3, 1, 5),
             9: (0, 1, 2, 3, 4, 5, 7, 6, 8)}
END_BOARDS = {}
for _m, _mv in END_GAMES.items():
    _c, _w, _l = replay(_mv)
    END_BOARDS[_m] = (_c, _w, _l)
assert [END_BOARDS[m][0] for m in range(5, 10)] == ["XXXOO....", "XX.OOOX..", "XOXOXOX..", "XXOOOOX.X", "XOXOXOOXX"]
assert [END_BOARDS[m][1] for m in range(5, 10)] == ["X", "O", "X", "O", "X"]
GHOST_ENDINGS = {m: math.factorial(9 - m) for m in range(5, 10)}
assert [GHOST_ENDINGS[m] for m in range(5, 10)] == [24, 6, 2, 1, 1]
assert [END_BOARDS[m][0].count(".") for m in range(5, 10)] == [4, 3, 2, 1, 0]
assert 4 * 3 * 2 * 1 == 24

# ---------------------------------------------------------------- places (world units; the camera is home)
CELL = 1.4                                         # board A at its opening size (S01)
BC = np.array([0.0, 1.0])                          # its centre: the board and its timeline sit in the picture
NUM_OFF = np.array([0.36, -0.36])                  # a move number in its square's lower-right corner (x cell)
TL_NARROW = dict(x0=-2.0, dx=0.5, y=-1.55)         # the move timeline under the board (slots 1-9)
TL_WIDE = dict(x0=-4.6, dx=1.2, y=-0.55)           # ... and wide, from bar 29 (higher: the slot-5 tag clears the captions)
TINY_CELL = 0.3                                    # the tiny boards of bars 29-31
LEFT_END = np.array([-6.0, -0.55])                 # board A shrunk onto the left end of the timeline
TINY_Y = 1.07                                      # the tiny boards above slots 5-9
MULT_Y = 2.05                                      # their multipliers
CARD = 4.4                                         # the card behind each board of the deck
# the spread deck (bars 26-28): the 24 copies fly out from behind the board into two fanned wings of 12
# (3 rows x 4 columns each side, tilted outwards like a hand of cards), small enough not to overlap, so each
# copy reads as a board: the same five bright real moves, its own dashed ending (an overlapping ±40° or ±60°
# fan behind the opaque board showed only a tangle of tilted lines at its edges)
DECK_SCALE = 0.22                                  # a copy is 0.22 x the board (a card 0.97 wide)
WING_X = (3.25, 4.33, 5.41, 6.49)                  # card centres, |x|, from the board outwards
WING_Y = (2.42, 1.34, 0.26)                        # rows, top to bottom
WING_DROP = 0.10                                   # each column further out sits a little lower (an arc) ...
WING_TILT = (5.0, 8.0, 11.0, 14.0)                 # ... and tilts a little more (degrees)


def deck_slot(i: int):
    """Where copy i lands: (centre, tilt in radians). Copies 0-11 on the left (left to right, top to bottom
    in each column), 12-23 on the right, so the deck's grains pan left to right as the copies fly out."""
    side, j = (-1, i) if i < 12 else (1, i - 12)
    col, row = divmod(j, 3)
    k = 3 - col if side < 0 else col                # 0: the column next to the board
    x = side * WING_X[k]
    y = WING_Y[row] - WING_DROP * k * k
    return np.array([x, y]), -side * math.radians(WING_TILT[k])
HANDOVER = {"board": np.array([0.0, -0.95]), "cell": 0.6,
            "panels": [(-4.1, 1.65, 3.8, 2.6), (0.0, 1.65, 3.8, 2.6), (4.1, 1.65, 3.8, 2.6)]}

# ---------------------------------------------------------------- times
GATHER = (0.0, 0.30)                               # the 24 points fly to their places on the four grid lines
GROW = (0.10, 0.42)                                # ... and the lines grow out of them
MOVES = [bb(21, 1), bb(21, 2), bb(21, 3), bb(21, 4), bb(22, 1)]
WIN = bb(22, 2)
STOP = bb(22, 3)                                   # the game stops: the timeline, its stop bar, the tag
GHOSTS = [bb(23, k) for k in (1, 2, 3, 4)]        # ghost moves 6-9
SHUFFLE = [bb(24, 1) + 0.15 * k for k in range(24)]   # orders 1-24 on sixteenths
LAND = bb(25, 3)                                   # lands on 24: "4 × 3 × 2 × 1 = 24"
FAN = bb(26, 1)                                    # the spread deck, staggered over one beat
FAN_LABEL = bb(27, 4)
PULSE5 = bb(28, 1)                                 # the five real moves pulse once
FOLD = (bb(29, 1), bb(29, 1) + 0.38)               # the deck folds back
SHRINK = (bb(29, 1) + 0.1, bb(29, 2) + 0.15)       # the board shrinks onto the left end; the timeline widens
X_SLOTS = [bb(29, 2), bb(29, 3), bb(29, 4)]        # X's slots 1, 3, 5 light
SLOT_LABEL = bb(29, 4)
SLOT_LABEL_OUT = (bb(31, 1.5), bb(31, 2.5))       # ... gone with c10, before c11 (31.2+)
RISE = [bb(30, 1), bb(30, 2), bb(30, 3), bb(30, 4), bb(31, 1)]   # end moves 5-9: boards rise, ×24 ... ×1
GLIDE = (bb(32, 1), bb(32, 3))                     # the move-5 board glides to the centre and grows
PANELS = bb(32, 4)
CAM_BACK = (FAN, FAN + 0.6)                        # the camera eases back to hold the deck ...
CAM_HOME = (bb(29, 1), bb(29, 2))                  # ... and home again for the timeline


def cam_path(t: float):
    """(centre x, centre y, frame width): home, eased back while the deck is open."""
    a = ease_in_out_cubic(seg(t, *CAM_BACK)) * (1 - ease_in_out_cubic(seg(t, *CAM_HOME)))
    push = ease_in_out_sine(seg(t, 0.0, FAN)) * (1 - ease_in_out_cubic(seg(t, *CAM_HOME)))   # a slow push-in
    drift = 0.12 * math.sin(2 * math.pi * seg(t, CAM_BACK[1], CAM_HOME[0])) * a      # the deck drifts by
    late = math.sin(math.pi * seg(t, CAM_HOME[1], GLIDE[0]))                          # bars 29-31, home again
    return drift + 0.10 * late, 0.40 * a + 0.05 * push + 0.04 * late, \
        W * (1 + 0.13 * a) * (1 - 0.018 * push) * (1 - 0.015 * late)


CAM = Cam(cam_path)


def tl_slot(k: int, t: float) -> np.ndarray:
    """Slot k (1-9) of the move timeline at time t: narrow under the board, wide from bar 29."""
    e = ease_in_out_cubic(seg(t, *SHRINK))
    a, b = TL_NARROW, TL_WIDE
    return np.array([lerp(a["x0"] + a["dx"] * (k - 1), b["x0"] + b["dx"] * (k - 1), e), lerp(a["y"], b["y"], e)])


def gather_ease(u: float) -> float:
    """The 24 points' flight into the grid: an ease-out arrival whose first frames start from rest (an
    ease-out from frame 0 would jump 40-120 px on the first frame after S02's last one, which shows them
    exactly where S02 left them)."""
    u = clamp01(u)
    v = clamp01(u / 0.25)
    return ease_out_cubic(u) * v * v * (3 - 2 * v)


def _dashed(tmpl, n: int):
    """A dashed copy of a mark template (a ghost)."""
    parts = [p for p in tmpl.family_members_with_points()]
    return VGroup(*[DashedVMobject(p, num_dashes=n, dashed_ratio=0.55) for p in parts])


def _seg_poly(poly: np.ndarray):
    return poly[:-1], poly[1:]


def _circle(c, r, n=28, a0=math.pi / 2):
    a = a0 + np.linspace(0, 2 * np.pi, n + 1)
    return np.asarray(c) + r * np.stack([np.cos(a), np.sin(a)], axis=1)


# ---------------------------------------------------------------- a board drawn from its moves
class BoardRig:
    """A board: grid, real marks (with move numbers), win line, and the four ghost squares (dashed X or O
    and a ghost move number each), placed each frame by centre b and scale s (cell = CELL * s)."""

    def __init__(self, moves, win, ghosts: bool = True, cell: float = CELL, nums: bool = True):
        self.cell = cell
        self.moves = list(moves)
        self.grid = Hairlines(INK, 2.0)
        self.marks = [mark_ink(player(k), 0.62 * cell) for k in range(len(self.moves))]
        a, c = win
        col = XC if player(len(self.moves) - 1) == "X" else OC
        self.win = Ink(win_template(a, c, cell), col.mid, 3.2, col.glow, 18, layers=7, glow_opacity=0.55)
        self.nums = [InkText(move_digit(k + 1)) for k in range(len(self.moves))] if nums else []
        self.ghost_x, self.ghost_o, self.ghost_n = {}, {}, {}
        if ghosts:
            for s in GHOST_SQ:
                self.ghost_x[s] = Ink(_dashed(x_template(0.62 * cell), 5), INK_DIM, 2.0)
                self.ghost_o[s] = Ink(_dashed(o_template(0.62 * cell), 12), INK_DIM, 2.0)
            for m in (6, 7, 8, 9):
                self.ghost_n[m] = InkText(move_digit(m), INK_DIM)
        self.group = VGroup(self.grid, *self.marks, self.win, *self.nums, *self.ghost_x.values(),
                            *self.ghost_o.values(), *self.ghost_n.values())
        self.place(np.zeros(2))

    def place(self, b, s: float = 1.0):
        self.b, self.s = np.asarray(b, dtype=float), float(s)
        self.A = np.eye(2) * s
        return self

    def square(self, i: int) -> np.ndarray:
        return self.A @ square_centre(i, self.cell) + self.b

    def hide(self):
        self.grid.set_segments([], [])
        for x in self.marks + [self.win] + list(self.ghost_x.values()) + list(self.ghost_o.values()):
            x.hide()
        for n in self.nums + list(self.ghost_n.values()):
            n.hide()

    def draw_grid(self, f: float = 1.0, vis: float = 1.0, width: float | None = None):
        P, Q = [], []
        for p, q in grid_lines(self.cell):
            P.append(self.A @ p + self.b)
            Q.append(self.A @ (p + (q - p) * f) + self.b)
        if width is None:                                                # hairlines thin as the board shrinks
            width = max(0.4, (self.s * self.cell / CELL) ** 0.5)
        self.grid.set_segments(P, Q, width=width, opacity=vis)

    def draw_marks(self, mark_f, glow, num_v, vis: float = 1.0, win_f: float = 0.0, win_glow: float = 1.0):
        w = max(0.4, (self.s * self.cell / CELL) ** 0.5)               # hairlines thin as the board shrinks
        for k, m in enumerate(self.marks):
            m.show(mark_f[k], self.A, self.square(self.moves[k]), vis=vis, glow=glow[k], width=w, glow_width=w)
        self.win.show(win_f, self.A, self.b, vis=vis, glow=win_glow, width=w, glow_width=w)
        for k, n in enumerate(self.nums):
            at = self.square(self.moves[k]) + self.s * self.cell * NUM_OFF + np.array([0, 0.06 * (1 - num_v[k])])
            n.show(at, scale=self.s, vis=num_v[k] * vis)

    def draw_ghosts(self, order, f, vis, num_vis=None):
        """order: squares of moves 6-9 (or None); f[i], vis[i]: how drawn / visible the ghost of move 6 + i."""
        shown = set()
        for i, s in enumerate(order or ()):
            m = 6 + i
            ink, other = (self.ghost_x[s], self.ghost_o[s]) if ghost_sym(m) == "X" else (self.ghost_o[s], self.ghost_x[s])
            ink.show(f[i], self.A, self.square(s), vis=vis[i], width=max(0.5, (self.s * self.cell / CELL) ** 0.5))
            other.hide()
            shown.add(s)
            nv = vis[i] if num_vis is None else num_vis[i]
            self.ghost_n[m].show(self.square(s) + self.s * self.cell * NUM_OFF, scale=self.s, vis=nv)
        for s in GHOST_SQ:
            if s not in shown:
                self.ghost_x[s].hide()
                self.ghost_o[s].hide()
        if not order:
            for n in self.ghost_n.values():
                n.hide()


# ---------------------------------------------------------------- the spread deck: 24 faint copies
class DeckCard:
    """One card of the spread deck: the board with game A's five real moves and one dashed ending, as a
    few Hairlines (one Cairo path each), placed by centre, scale and tilt."""

    def __init__(self, order):
        c = CELL
        self.card = Hairlines(INK_FAINT, 1.4)
        self.grid = Hairlines(INK, 1.4)
        self.xs = Hairlines(XC.mid, 1.5)
        self.os = Hairlines(OC.mid, 1.5)
        self.gh = Hairlines(INK_DIM, 1.8)
        h = 0.31 * c
        segs = {"card": [], "grid": [], "xs": [], "os": [], "gh": []}
        r, n = 0.12, 5
        q = CARD / 2 - r
        corners = [(q, q, 0), (-q, q, 1), (-q, -q, 2), (q, -q, 3)]
        pts = []
        for cx, cy, k in corners:                                        # a rounded square
            a = np.linspace(k * math.pi / 2, (k + 1) * math.pi / 2, n)
            pts += list(np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], axis=1))
        pts.append(pts[0])
        P, Q = _seg_poly(np.array(pts))
        segs["card"] += list(zip(P, Q))
        segs["grid"] += [(p, q_) for p, q_ in grid_lines(c)]
        for k, s in enumerate(GAME_A):
            z = square_centre(s, c)
            if player(k) == "X":
                segs["xs"] += [(z + np.array([-h, h]), z + np.array([h, -h])), (z + np.array([h, h]), z + np.array([-h, -h]))]
            else:
                P, Q = _seg_poly(_circle(z, h, 24))
                segs["os"] += list(zip(P, Q))
        for i, s in enumerate(order):
            z = square_centre(s, c)
            if ghost_sym(6 + i) == "X":
                for d0, d1 in ((np.array([-h, h]), np.array([h, -h])), (np.array([h, h]), np.array([-h, -h]))):
                    for j in range(5):
                        u0, u1 = j / 5, (j + 0.55) / 5
                        segs["gh"].append((z + d0 + (d1 - d0) * u0, z + d0 + (d1 - d0) * u1))
            else:
                for j in range(12):
                    a0 = math.pi / 2 + 2 * math.pi * j / 12
                    a = np.linspace(a0, a0 + 2 * math.pi * 0.55 / 12, 3)
                    poly = z + h * np.stack([np.cos(a), np.sin(a)], axis=1)
                    P, Q = _seg_poly(poly)
                    segs["gh"] += list(zip(P, Q))
        self.segs = {k: (np.array([a for a, _ in v]), np.array([b for _, b in v])) for k, v in segs.items()}
        self.back = VGroup()                                             # the card's body: opaque black
        self.body = np.array(pts)
        from manim import VMobject
        self.back_m = VMobject().set_stroke(width=0).set_fill(BG, opacity=0)
        self.back_m.set_points_as_corners([[*p, 0] for p in self.body])
        self.back_tp = self.back_m.points.copy()
        self.group = VGroup(self.back_m, self.card, self.grid, self.os, self.xs, self.gh)

    def show(self, centre, scale: float, theta: float, vis: float, real: float = 1.0):
        if vis <= 1e-3:
            for m in (self.card, self.grid, self.xs, self.os, self.gh):
                m.set_segments([], [])
            self.back_m.set_fill(BG, opacity=0)
            return
        c, s = math.cos(theta), math.sin(theta)
        R = scale * np.array([[c, -s], [s, c]])
        off = np.asarray(centre, dtype=float)
        w = max(0.6, scale ** 0.35)                                      # hairlines thin a little with the size

        def tr(p):
            return p @ R.T + off
        q = self.back_tp.copy()
        q[:, :2] = tr(self.back_tp[:, :2])
        self.back_m.points = q
        self.back_m.set_fill(BG, opacity=clamp01(DECK_BODY * vis))
        for key, mob, op in (("card", self.card, 0.40), ("grid", self.grid, 0.42), ("xs", self.xs, 0.80 * real),
                             ("os", self.os, 0.75 * real), ("gh", self.gh, 0.62)):
            P, Q = self.segs[key]
            mob.set_segments(tr(P), tr(Q), width=w, opacity=clamp01(op * vis))


# ---------------------------------------------------------------- the scene
class GhostGames(BeatScene):

    def construct(self):
        self.sounds = Sounds()
        self.shots: list[tuple[float, float, tuple]] = []
        self.build()
        self.score()
        self.run()

    # ------------------------------------------------------------- objects
    def build(self):
        self.dots = order_dots()
        self.gather_plan()
        self.grow = Hairlines(INK, 2.0)
        self.backing = Rectangle(width=CARD, height=CARD).set_stroke(width=0).set_fill(BG, opacity=0)
        self.backing.move_to([*BC, 0])
        self.front_card = Hairlines(INK_FAINT, 1.4)
        self.deck = [DeckCard(o) for o in ORDERS]
        self.A = BoardRig(GAME_A, WIN_A_LINE)
        self.tiny = {m: BoardRig(END_GAMES[m], END_BOARDS[m][2], ghosts=False, cell=TINY_CELL, nums=False)
                     for m in range(6, 10)}
        # the move timeline
        self.tl_base = Hairlines(INK_DIM, 1.2)
        self.tl_ticks = [Ink(Line([0, -0.09, 0], [0, 0.09, 0]), (XC if k % 2 else OC).mid, 2.6,
                             (XC if k % 2 else OC).glow, 9, layers=4, glow_opacity=0.55) for k in range(1, 10)]
        self.tl_ghost = Hairlines(INK_DIM, 2.0)
        self.tl_nums = [InkText(move_digit(k, 20), INK_DIM) for k in range(1, 10)]
        self.stop_bar = Ink(Line([0, -0.28, 0], [0, 0.28, 0]), INK, 2.2, INK, 6, layers=3, glow_opacity=0.35)
        self.slot_x = [mark_ink("X", 0.34, bright=0.8) for _ in range(3)]    # X's 1st, 2nd, 3rd mark (bar 29)
        lbl = stacked_label("第 5 步 · X 赢", "MOVE 5 · X WINS", color=INK_DIM)
        self.stop_tag, self.stop_tag_w = Glyphs(lbl, INK_DIM), lbl.width
        self.slot_tag = Glyphs(stacked_label("第 3 个 X：第 5 步", "X'S 3RD MARK: MOVE 5", color=INK), INK)
        self.formula = Glyphs(maths("4 × 3 × 2 × 1 = 24", size=28, color=INK), INK, INK, 7, layers=4,
                              glow_opacity=0.45)
        self.fan_tag = Glyphs(bi_label("幽灵对局", "GHOST GAMES", zh_size=22, en_size=20, color=INK_DIM), INK_DIM)
        self.fans = {m: Hairlines(INK_DIM, 1.2) for m in range(5, 10)}
        self.mults = {m: Glyphs(maths(f"×{GHOST_ENDINGS[m]}", size=40, color=WHITE), WHITE, INK, 9, layers=5,
                                glow_opacity=0.45) for m in range(5, 10)}
        self.panels = Hairlines(INK_DIM, 1.5)
        # HUD
        self.section = section_hud("§2 · 对局会提前结束 · GAMES STOP EARLY")
        self.readout_label = bi_label("已列出的顺序", "ORDERS SHOWN", zh_size=15, en_size=12.5, color=INK_DIM)
        self.readout = RollingCounter(0, digits=2, font=FONT_MONO, weight="NORMAL", size=24, color=INK)
        self.readout.clear_updaters()
        rx = W / 2 - 0.55
        self.readout.move_to([rx - self.readout.ref.width / 2, H / 2 - 0.55 - 0.42, 0])
        self.readout.layout()
        self.readout_label.move_to([rx - self.readout_label.width / 2, H / 2 - 0.55 - 0.1, 0])
        self.readout_group = VGroup(self.readout_label, self.readout)

        self.clock_mob = Mobject()
        self.clock_mob.add_updater(lambda m: self.update_state(self.clock()))
        self.add(self.clock_mob, self.camera.frame)
        order = sorted(range(24), key=lambda i: -abs(i - 11.5))          # outer cards first, inner ones on top
        self.add(*[self.deck[i].group for i in order], self.backing, self.front_card, self.grow, self.A.group,
                 *[b.group for b in self.tiny.values()], *self.fans.values(), self.tl_base, self.tl_ghost,
                 *self.tl_ticks, *self.tl_nums, self.stop_bar, *self.slot_x, self.stop_tag, self.slot_tag, self.formula,
                 self.fan_tag, *self.mults.values(), self.panels)
        self.fix(self.dots, self.section, self.readout_group)
        self.update_state(0.0)

    def gather_plan(self):
        """The 24 points of S02 each fly to one of 24 spots, six on each grid line (shortest total path, so
        no two paths cross); each line then grows out of its six spots."""
        from scipy.optimize import linear_sum_assignment
        spots, segs = [], []
        for p, q in grid_lines(CELL):
            for i in range(6):
                u = (i + 0.5) / 6
                spots.append(BC + p + (q - p) * u)
                segs.append((BC + p, BC + q, u))
        spots = np.array(spots)
        cost = np.linalg.norm(ORDER_SCREEN[:, None, :] - spots[None, :, :], axis=2)
        r, c = linear_sum_assignment(cost)
        self.dot_target = spots[c[np.argsort(r)]]
        self.spots, self.spot_segs = spots, segs

    # ------------------------------------------------------------- the picture at time t
    def update_state(self, t: float):
        cx, cy, w = CAM(t)
        frame = self.camera.frame
        frame.set(width=w)
        frame.move_to([cx, cy, 0])
        self.update_gather(t)
        self.update_board(t)
        self.update_deck(t)
        self.update_timeline(t)
        self.update_tiny(t)
        self.update_labels(t)
        self.update_hud(t)

    # --- 21.1: the 24 points gather into board A's grid
    def update_gather(self, t: float):
        e = gather_ease(seg(t, *GATHER))
        fade = 1 - ease_in_out_sine(seg(t, GROW[0] + 0.05, GROW[1]))
        if fade > 1e-3:
            pts = ORDER_SCREEN + (self.dot_target - ORDER_SCREEN) * e
            trail = [pts]
            wts = [np.full(24, ORDER_DOTS["weight"] * fade)]
            for lag, wt in ((0.03, 0.4),):                              # a short motion-blur trail
                e2 = gather_ease(seg(t - lag, *GATHER))
                if 0 < e2 < 0.98:
                    trail.append(ORDER_SCREEN + (self.dot_target - ORDER_SCREEN) * e2)
                    wts.append(np.full(24, ORDER_DOTS["weight"] * fade * wt))
            self.dots.draw(CAM.to_screen(np.concatenate(trail), t), np.concatenate(wts))
        else:
            self.dots.draw(None, None)
        g = ease_out_quad(seg(t, *GROW))
        if 0 < g < 1:
            P, Q = [], []
            half = g / 12
            for (p, q, u) in self.spot_segs:
                P.append(p + (q - p) * max(0.0, u - half))
                Q.append(p + (q - p) * min(1.0, u + half))
            self.grow.set_segments(P, Q, opacity=0.4 + 0.6 * g)
        else:
            self.grow.set_segments([], [])

    # --- board A: the game, its stop, its ghosts and their shuffle; later the tiny board of move 5
    def board_place(self, t: float):
        """Board A's centre and scale: the opening size until bar 29, then on the timeline's left end, above
        slot 5 (bar 30), and centred for S04 (bar 32)."""
        if t < SHRINK[0]:
            return BC, 1.0
        tiny = TINY_CELL / CELL
        if t < RISE[0]:
            e = ease_in_out_cubic(seg(t, *SHRINK))
            return BC + (LEFT_END - BC) * e, lerp(1.0, tiny, e)
        if t < GLIDE[0]:
            e = ease_in_out_cubic(seg(t, RISE[0], RISE[0] + 0.5))
            p0, p1 = LEFT_END, np.array([tl_slot(5, t)[0], TINY_Y])
            arc = np.array([0.0, 0.9 * math.sin(math.pi * e)])
            return p0 + (p1 - p0) * e + arc, tiny
        e = ease_in_out_cubic(seg(t, *GLIDE))
        p0 = np.array([tl_slot(5, t)[0], TINY_Y])
        return p0 + (HANDOVER["board"] - p0) * e, lerp(tiny, HANDOVER["cell"] / CELL, e)

    def update_board(self, t: float):
        A = self.A
        b, s = self.board_place(t)
        A.place(b, s)
        grid_on = t >= GROW[1]
        if grid_on:
            A.draw_grid(1.0, vis=1.0)
        else:
            A.grid.set_segments([], [])
        mf = [ease_out_cubic(seg(t, m, m + (GROW[1] if k == 0 else 0.25))) for k, m in enumerate(MOVES)]
        breathe = 0.12 * math.sin(2 * math.pi * (t - WIN) / BAR) * (t >= WIN)
        passes = self.pass_times(WIN)
        glow = []
        for k, sq in enumerate(GAME_A):
            g = 1.0 + 0.8 * pulse(t, MOVES[k], 0.35) + 1.1 * pulse(t, PULSE5 + 0.06 * k, 0.45)
            if player(k) == "X":
                g += 0.9 * pulse(t, passes[sq], 0.45) + (0.2 + breathe) * (t >= passes[sq])
            glow.append(g)
        num_out = 1 - seg(t, SHRINK[0], SHRINK[0] + 0.25)               # the numbers leave as it shrinks
        nv = [ease_out_cubic(seg(t, m + 0.12, m + 0.42)) * num_out for m in MOVES]
        wf = ease_out_quad(seg(t, WIN, WIN + BEAT))
        wg = 1.0 + 0.12 * math.sin(2 * math.pi * (t - WIN) / BAR) * (t >= WIN + BEAT) + 0.6 * pulse(t, PULSE5, 0.5)
        A.draw_marks(mf, glow, nv, vis=1.0, win_f=wf, win_glow=wg)
        # the ghosts: drawn one per beat in bar 23, shuffled 24.1-25.3, shimmering, gone as the board shrinks
        if t < GHOSTS[0] or t >= SHRINK[0] + 0.25:
            A.draw_ghosts(None, [], [])
            return
        k = sum(1 for ts in SHUFFLE if ts <= t + 1e-6)                  # orders shown so far
        order = ORDERS[max(0, k - 1)]
        prev = ORDERS[max(0, k - 2)]
        since = t - SHUFFLE[k - 1] if k >= 1 else 9.0
        out = 1 - seg(t, SHRINK[0], SHRINK[0] + 0.25)
        f, vis, nvis = [], [], []
        for i in range(4):
            fi = ease_out_cubic(seg(t, GHOSTS[i], GHOSTS[i] + 0.3))
            if t < GHOSTS[i]:
                fi = 0.0
            changed = order[i] != prev[i] and k >= 2
            flick = clamp01(since / 0.07) if changed else 1.0          # the new square fades in fast
            shimmer = 1 + 0.10 * math.sin(2 * math.pi * 1.7 * t + 1.9 * i) * (t >= LAND)
            v = GHOST_VIS * flick * shimmer * out
            f.append(fi if k == 0 else 1.0)
            vis.append(v if fi > 0 else 0.0)
            nvis.append(0.75 * v / GHOST_VIS * GHOST_NUM_VIS if fi > 0 else 0.0)
        A.draw_ghosts(order, f, vis, nvis)

    @staticmethod
    def pass_times(t0: float) -> dict:
        """When the win line's head passes the centres of squares 0, 1, 2 (ease-out over one beat)."""
        L = 2 * CELL + 2 * 0.42 * CELL
        out = {}
        for sq, x in zip((0, 1, 2), (-CELL, 0.0, CELL)):
            f = (x + L / 2) / L
            out[sq] = t0 + BEAT * (1 - math.sqrt(1 - f))
        return out

    # --- the spread deck (bars 26-28) and the front card it sits behind
    def deck_place(self, t: float, i: int):
        """Copy i: (centre, scale, tilt). It flies out from behind the board (26.1, staggered over one beat,
        ease-out), sways gently while the deck is open (ALIVE) and flies back in as the deck folds (29.1)."""
        slot, tilt = deck_slot(i)
        t0 = FAN + 0.6 * i / 24
        e = ease_out_cubic(seg(t, t0, t0 + 0.45)) * (1 - ease_in_cubic(seg(t, *FOLD)))
        on = seg(t, FAN + 0.6, FAN + 1.8) * (1 - seg(t, FOLD[0], FOLD[0] + 0.1))
        ph = 2 * math.pi * (t - FAN) / (2 * BAR) + 0.61 * i
        sway = math.radians(2.0) * math.sin(ph) * on
        bob = np.array([0.03 * math.sin(ph + 1.3), 0.04 * math.sin(ph)]) * on
        arc = np.array([0.0, 0.35 * math.sin(math.pi * e)])               # a small lift on the way out and back
        centre = BC + (slot - BC) * e + arc * (1 - e) + bob
        scale = lerp(0.9, DECK_SCALE, ease_out_cubic(clamp01(e * 1.15)))
        return centre, scale, tilt * e + sway

    def update_deck(self, t: float):
        on = FAN <= t < FOLD[1]
        presence = ease_out_cubic(seg(t, FAN, FAN + 0.3)) * (1 - seg(t, FOLD[0] + 0.2, FOLD[1]))
        self.backing.set_fill(BG, opacity=clamp01(BACKING * presence) if on else 0.0)
        if on:
            a = np.linspace(0, 1, 2)
            q = CARD / 2
            pts = np.array([[q, q], [-q, q], [-q, -q], [q, -q], [q, q]]) + BC
            self.front_card.set_segments(pts[:-1], pts[1:], opacity=0.55 * presence)
            del a
        else:
            self.front_card.set_segments([], [])
        for i, card in enumerate(self.deck):
            if not on:
                card.show(BC, 1.0, 0.0, 0.0)
                continue
            t0 = FAN + 0.6 * i / 24
            vis = ease_out_cubic(seg(t, t0, t0 + 0.2)) * (1 - seg(t, FOLD[0] + 0.15, FOLD[1]))
            real = 1.0 + 0.4 * pulse(t, PULSE5 + 0.06 * 2, 0.5)
            card.show(*self.deck_place(t, i), vis, real)

    # --- the move timeline
    def update_timeline(self, t: float):
        if t < STOP or t >= GLIDE[1]:
            self.tl_base.set_segments([], [])
            self.tl_ghost.set_segments([], [])
            for x in self.tl_ticks + [self.stop_bar]:
                x.hide()
            for n in self.tl_nums:
                n.hide()
            return
        v = ease_out_cubic(seg(t, STOP, STOP + 0.35)) * (1 - ease_in_out_sine(seg(t, GLIDE[0], GLIDE[0] + 1.0)))
        wide = ease_in_out_cubic(seg(t, *SHRINK))
        p1, p9 = tl_slot(1, t), tl_slot(9, t)
        pad = lerp(0.3, 0.5, wide)
        self.tl_base.set_segments([p1 - np.array([pad, 0])], [p9 + np.array([pad, 0])], opacity=0.45 * v)
        P, Q = [], []
        for k in range(1, 10):
            p = tl_slot(k, t)
            self.tl_nums[k - 1].show(p + np.array([0, -0.30]), scale=1.0, vis=0.9 * v)
            tick = self.tl_ticks[k - 1]
            if k <= 5:                                                   # game A's real moves
                lit = 1.0
            else:                                                        # ghost moves 6-9: dashed, until bar 29
                lit = wide
                if t >= GHOSTS[k - 6] and wide < 1:
                    for j in range(2):
                        y0, y1 = -0.09 + 0.1 * j, -0.09 + 0.1 * j + 0.06
                        P.append(p + np.array([0, y0]))
                        Q.append(p + np.array([0, y1]))
            glow = 0.6 + 1.6 * max([pulse(t, ts, 0.6) for ts, kk in zip(X_SLOTS, (1, 3, 5)) if kk == k] or [0.0])
            if k in (1, 3, 5):
                glow += 0.9 * (t >= X_SLOTS[(k - 1) // 2]) * (1 - seg(t, RISE[0], RISE[0] + 1.0))
            tick.show(1.0, np.eye(2) * lerp(1.0, 1.25, wide), p, vis=v * lit, glow=glow)
        self.tl_ghost.set_segments(P, Q, opacity=0.6 * v * (1 - wide))
        # bar 29: X's marks 1, 2, 3 light above slots 1, 3, 5 with the bells (move 5 is X's 3rd mark)
        for j, (ts, k) in enumerate(zip(X_SLOTS, (1, 3, 5))):
            xv = ease_out_cubic(seg(t, ts, ts + 0.25)) * (1 - ease_in_out_sine(seg(t, RISE[0], RISE[0] + 0.35))) * v
            if xv > 1e-3:
                p = tl_slot(k, t) + np.array([0, 0.48 + 0.06 * (1 - xv)])
                self.slot_x[j].show(clamp01(xv * 1.2), np.eye(2), p, vis=xv, glow=1.0 + 1.4 * pulse(t, ts, 0.5),
                                    width=0.75, glow_width=0.6)
            else:
                self.slot_x[j].hide()
        # the stop bar drops after slot 5; it lifts away as the timeline widens
        sv = ease_out_cubic(seg(t, STOP, STOP + 0.3)) * (1 - seg(t, SHRINK[0], SHRINK[0] + 0.3))
        if sv > 1e-3:
            x = (tl_slot(5, t)[0] + tl_slot(6, t)[0]) / 2
            self.stop_bar.show(1.0, np.eye(2), np.array([x, tl_slot(5, t)[1] + 0.25 * (1 - sv)]), vis=sv,
                               glow=1.0 + 1.5 * pulse(t, STOP, 0.4))
        else:
            self.stop_bar.hide()

    # --- bars 30-31: one tiny real board per end move, its trailing fan of ghost endings, its multiplier
    def update_tiny(self, t: float):
        fade = 1 - ease_in_out_sine(seg(t, GLIDE[0], GLIDE[0] + 0.9))
        for i, m in enumerate(range(5, 10)):
            t0 = RISE[i]
            e = ease_out_cubic(seg(t, t0, t0 + 0.5))
            if m == 5:
                b, s = self.board_place(t)
                top = np.array([b[0], b[1] - 1.5 * TINY_CELL - 0.06])
                rise_v = 1.0 if t >= t0 else 0.0
            else:
                rig = self.tiny[m]
                if t < t0 or fade <= 1e-3:
                    rig.hide()
                    self.fans[m].set_segments([], [])
                    self.mults[m].hide()
                    continue
                slot = tl_slot(m, t)
                b = slot + (np.array([slot[0], TINY_Y]) - slot) * e
                rig.place(b, lerp(0.35, 1.0, e))
                rig.draw_grid(1.0, vis=fade)
                n = len(END_GAMES[m])
                mf = [clamp01((e - 0.15) * 1.6)] * n
                gl = [1.0 + 0.8 * pulse(t, t0, 0.4)] * n
                rig.draw_marks(mf, gl, [0] * n, vis=fade, win_f=ease_out_quad(seg(t, t0 + 0.15, t0 + 0.45)),
                               win_glow=1.0 + 0.6 * pulse(t, t0 + 0.2, 0.5))
                top = np.array([b[0], b[1] - 1.5 * TINY_CELL * rig.s - 0.06])
                rise_v = e
            # the trailing fan: one dashed ray per ghost ending (24, 6, 2, 1 and none)
            n_rays = GHOST_ENDINGS[m] if m < 9 else 0
            fan = self.fans[m]
            if n_rays and t >= t0 and fade > 1e-3:
                spread = {24: 36, 6: 22, 2: 10, 1: 0}[n_rays]
                breathe = 1 + 0.12 * math.sin(2 * math.pi * (t - RISE[-1]) / BAR + i) * seg(t, RISE[-1] + 0.3, RISE[-1] + BEAT)
                L = 0.78 * ease_out_cubic(seg(t, t0 + 0.05, t0 + 0.55))
                P, Q = [], []
                for r in range(n_rays):
                    a = math.radians(spread * breathe * (2 * r / (n_rays - 1) - 1) if n_rays > 1 else 0.0)
                    d = np.array([math.sin(a), -math.cos(a)])
                    ph = RAY_PHASE[r % len(RAY_PHASE)]
                    for j in range(7):
                        u0 = min(1.0, (j + ph) / 7)
                        u1 = min(1.0, (j + ph + 0.45) / 7)
                        if u1 > u0:
                            P.append(top + d * L * u0)
                            Q.append(top + d * L * u1)
                fan.set_segments(P, Q, opacity=0.5 * fade * rise_v)
            else:
                fan.set_segments([], [])
            # the multiplier lands on its beat
            mv = ease_out_cubic(seg(t, t0, t0 + 0.25)) * fade
            if mv > 1e-3:
                x = tl_slot(m, t)[0]
                self.mults[m].show(np.array([x, MULT_Y - 0.1 * (1 - mv)]), vis=mv, glow=0.5 + 2.0 * pulse(t, t0, 0.45))
            else:
                self.mults[m].hide()

    # --- labels: the stop tag, the formula, the deck's name, the slot-5 tag, the panels for S04
    def update_labels(self, t: float):
        v = ease_out_cubic(seg(t, STOP, STOP + 0.4)) * (1 - seg(t, GHOSTS[0], GHOSTS[0] + 0.5))
        if v > 1e-3:
            self.stop_tag.show(BC + np.array([CELL * 1.5 + 0.35 + self.stop_tag_w / 2, CELL - 0.05 * (1 - v)]), vis=v)
        else:
            self.stop_tag.hide()
        v = ease_out_cubic(seg(t, LAND, LAND + 0.35)) * (1 - seg(t, SHRINK[0], SHRINK[0] + 0.3))
        if v > 1e-3:                                                     # beside the ghost slots 6-9 it counts
            x = tl_slot(9, t)[0] + FORMULA_GAP + self.formula.w / 2
            self.formula.show(np.array([x, TL_NARROW["y"] - 0.17 + 0.05 * (1 - v)]), vis=v,
                              glow=0.3 + 1.8 * pulse(t, LAND, 0.5))
        else:
            self.formula.hide()
        v = ease_out_cubic(seg(t, FAN_LABEL, FAN_LABEL + 0.4)) * (1 - seg(t, FOLD[0], FOLD[0] + 0.3))
        if v > 1e-3:
            self.fan_tag.show(np.array([0.0, FAN_TAG_Y + 0.06 * (1 - v)]), vis=0.95 * v)
        else:
            self.fan_tag.hide()
        v = ease_out_cubic(seg(t, SLOT_LABEL, SLOT_LABEL + 0.4)) * (1 - ease_in_out_sine(seg(t, *SLOT_LABEL_OUT)))
        if v > 1e-3:
            self.slot_tag.show(tl_slot(5, t) + np.array([0, -0.84 + 0.05 * (1 - v)]), vis=v)
        else:
            self.slot_tag.hide()
        # 32.4: three hairline panel frames draw above the centre board (S04's panels), clockwise from top left
        P, Q = [], []
        for j, (x, y, w, h) in enumerate(HANDOVER["panels"]):
            f = ease_out_cubic(seg(t, PANELS + 0.06 * j, PANELS + 0.06 * j + 0.45))
            if f <= 0:
                continue
            corners = np.array([[x - w / 2, y + h / 2], [x + w / 2, y + h / 2], [x + w / 2, y - h / 2],
                                [x - w / 2, y - h / 2], [x - w / 2, y + h / 2]])
            lens = np.linalg.norm(np.diff(corners, axis=0), axis=1)
            cum = np.concatenate([[0], np.cumsum(lens)]) / lens.sum()
            for i in range(4):
                if f <= cum[i]:
                    break
                u = clamp01((f - cum[i]) / (cum[i + 1] - cum[i]))
                P.append(corners[i])
                Q.append(corners[i] + (corners[i + 1] - corners[i]) * u)
        self.panels.set_segments(P, Q, opacity=0.9)

    def update_hud(self, t: float):
        for p in self.section.get_family():
            if len(p.points):
                p.set_fill(opacity=1.0)
        lv = seg(t, SHUFFLE[0] - 0.25, SHUFFLE[0]) * (1 - seg(t, SHRINK[0], SHRINK[0] + 0.4))
        for p in self.readout_label.get_family():
            if len(p.points):
                p.set_fill(opacity=lv)
        k = sum(1 for ts in SHUFFLE if ts <= t + 1e-6)
        self.readout.value.set_value(float(k))
        self.readout.layout()
        hot = pulse(t, LAND, 0.5)
        col = WHITE if hot > 0.05 else INK
        for c in self.readout.columns:
            for g in c:
                g.set_fill(col, opacity=g.get_fill_opacity() * lv)

    # ------------------------------------------------------------- the sounds (from the same numbers)
    def score(self):
        S = self.sounds
        sx = lambda p, t: float(CAM.to_screen(np.asarray(p, dtype=float), t)[0])
        board = BoardRig(GAME_A, WIN_A_LINE, ghosts=False).place(BC)
        S.phrase("game A", [(t, tag(player(k), sq), sx(board.square(sq), t)) for k, (t, sq) in enumerate(zip(MOVES, GAME_A))])
        passes = self.pass_times(WIN)
        S.phrase("win A", [(passes[sq], f"X@{n}", sx(board.square(sq), passes[sq]))
                           for sq, n in zip((0, 1, 2), ("C#6", "D6", "E6"))])
        S.effect(WIN, "whoosh_up", BEAT, sx(board.square(1), WIN))
        S.phrase("stop", [(STOP, "pluck@D3", sx(tl_slot(5, STOP), STOP))], gain=0.6)   # a muted pluck
        S.phrase("ghosts", [(t, f"ghost@{PITCH[s]}", sx(board.square(s), t)) for t, s in zip(GHOSTS, FIRST_GHOSTS)],
                 gain=0.75)
        S.phrase("shuffle", [(t, f"ghost@{n}", sx(BC, t) + 2.0 * math.sin(k))
                             for k, (t, n) in enumerate(zip(SHUFFLE, rising(24, TONES_BM9)))], gain=0.5)
        S.effect(LAND, "thump", 0.6, 0.0)
        S.phrase("deck", [(FAN + 0.6 * i / 24, f"ghost@{n}", 3.2 * (2 * i / 23 - 1))
                          for i, n in enumerate(rising(24, TONES_FSM9))], gain=0.45)
        S.phrase("name", [(FAN_LABEL + 0.04 * i, f"glass@{n}", 0.0) for i, n in enumerate(("F#4", "A4", "C#5", "E5"))],
                 gain=0.5)
        S.effect(PULSE5, "shimmer", 1.2, 0.0)
        S.effect(FOLD[0], "whoosh_down", 0.5, 0.0)
        S.phrase("X's slots", [(t, f"X@{n}", sx(tl_slot(k, X_SLOTS[-1] + 0.5), t))
                               for t, n, k in zip(X_SLOTS, ("G#4", "B4", "E5"), (1, 3, 5))], gain=0.8)
        S.phrase("slot tag", [(SLOT_LABEL + 0.05, "pluck@B4", sx(tl_slot(5, SLOT_LABEL), SLOT_LABEL))], gain=0.4)
        steps = [("X", "E5"), ("O", "D5"), ("X", "C#5"), ("O", "B4"), ("X", "A4")]    # five notes stepping down
        S.phrase("end moves", [(t, f"{w}@{n}", sx(tl_slot(m, t), t)) for t, (w, n), m in zip(RISE, steps, range(5, 10))])
        for t0, m in zip(RISE, range(5, 10)):
            n = GHOST_ENDINGS[m] if m < 9 else 0
            if n:
                S.phrase(f"ghosts of move {m}", [(t0 + 0.1 + 0.4 * j / max(1, n), f"ghost@{q}", sx(tl_slot(m, t0), t0))
                                                 for j, q in enumerate(rising(n, TONES_E9))], gain=0.4)
        S.effect(GLIDE[0], "whoosh_up", 1.2, 0.0)
        S.phrase("panels", [(PANELS + 0.06 * j, f"grid@{n}", x) for j, (n, x) in
                            enumerate(zip(("E3", "B3", "E4"), (-4.1, 0.0, 4.1)))], gain=0.55)
        S.log(self)

    # ------------------------------------------------------------- the logged events and the clock
    def log_events(self):
        ev = self.shots

        def add(t, dur, x, y, w, h):
            ev.append((float(t), float(dur), (x, y, w, h)))

        add(GATHER[0], GROW[1], *BC, 8.0, 4.2)
        for t, sq in zip(MOVES, GAME_A):
            add(t, 0.42, *(BC + square_centre(sq, CELL)), 0.9, 0.9)
        add(WIN, BEAT, BC[0], BC[1] + CELL, 4.2, 0.2)
        add(STOP, BEAT, 0.0, TL_NARROW["y"], 4.6, 0.6)
        for t, sq in zip(GHOSTS, FIRST_GHOSTS):
            add(t, 0.3, *(BC + square_centre(sq, CELL)), 0.9, 0.9)
        for t in SHUFFLE:
            add(t, 0.15, BC[0] + 0.7, BC[1] - 0.7, 2.8, 2.8)
        add(LAND, BEAT, 0.0, TL_NARROW["y"] - 0.72, 3.0, 0.4)
        add(FAN, 1.0, *BC, 8.0, 5.0)
        add(FAN_LABEL, BEAT, 0.0, FAN_TAG_Y, 3.5, 0.4)
        add(PULSE5, BEAT, *BC, 4.2, 4.2)
        add(FOLD[0], BEAT, *BC, 8.0, 5.0)
        for t in X_SLOTS:
            add(t, BEAT, 0.0, TL_WIDE["y"], 0.3, 0.3)
        for t, m in zip(RISE, range(5, 10)):
            add(t, BEAT, TL_WIDE["x0"] + TL_WIDE["dx"] * (m - 1), TINY_Y, 1.0, 1.6)
        add(GLIDE[0], GLIDE[1] - GLIDE[0], 0.0, -0.3, 11.0, 2.0)
        add(PANELS, BEAT, 0.0, 1.65, 12.0, 2.6)

    def run(self):
        """Play the logged events in time order (each a Shot; overlapping ones share a play)."""
        self.log_events()
        steps = sorted({round(t, 4) for t, _, _ in self.shots})
        for i, t in enumerate(steps):
            nxt = steps[i + 1] if i + 1 < len(steps) else END
            self.until(f"{t:.4f}s")
            active = [(a, d, bx) for a, d, bx in self.shots if a <= t + 1e-6 and a + d > t + 1e-6]
            if not active:
                continue
            end = min(nxt, max(a + d for a, d, _ in active))
            if end - t < 0.5 / self.fps:
                continue
            shots = [Shot(box(*bx)) for _, _, bx in active]
            self.play(*shots, run_time=end - t)
            self.remove(*[s.mobject for s in shots])
        self.until(f"{END:.4f}s")


GHOST_VIS = 0.55                                   # ghost marks: dashed #7D8484, dim, never glowing
RAY_PHASE = list(np.random.default_rng(31).uniform(0.0, 1.0, 24))   # each ghost ray's dots start apart
GHOST_NUM_VIS = 0.8
DECK_BODY = 0.0                                    # the deck's cards are faint, transparent copies
BACKING = 1.0                                      # the main board's backing hides the copies until they clear it
FAN_TAG_Y = 3.62                                   # the deck's name, above the fan (the camera is eased back)
FORMULA_GAP = 0.62                                 # 25.3: "4 × 3 × 2 × 1 = 24" starts this far right of slot 9

# the ghost counts' notes: they climb through the bar's chord (video.yaml music.chords) to D6 at most, each
# count spread over its own length (the composer's unpitched rise clamps at its top note, D7 / C#7: the last
# 10-12 ghosts of a 24-count would repeat one shrill reversed-glass note)
TONES_BM9 = ["D4", "F#4", "A4", "B4", "C#5", "D5", "F#5", "A5", "B5", "C#6", "D6"]    # bars 23-25: Bm9/D
TONES_FSM9 = ["E4", "F#4", "G#4", "A4", "C#5", "E5", "F#5", "G#5", "A5", "C#6"]       # bars 26-27: F#m9
TONES_E9 = ["E4", "F#4", "G#4", "B4", "D5", "E5", "F#5", "G#5", "B5", "D6"]           # bar 30: E9


def rising(n: int, tones) -> list[str]:
    """n notes climbing through `tones`: a few items take the lowest tones in turn; 24 step up the whole set."""
    if n <= len(tones):
        return list(tones[:n]) if n < 4 else [tones[round(i * (len(tones) - 1) / (n - 1))] for i in range(n)]
    return [tones[round(i * (len(tones) - 1) / (n - 1))] for i in range(n)]
