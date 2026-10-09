"""S04 · Counting by hand 手算 — three panels count the games X wins on move 5, then the hand count of
move 6, then the tangle.

Bars 33-40 (1:16.8-1:36.0) of script.md. As in S01 (the reference scene), the picture is a pure function of
the scene time (`update_state`): every object is placed from a template each frame, and the notes are
computed from the same numbers (Sounds) and logged as count marks with one tag each ("X@C#5").

    33     panel 1: the 8 winning lines flash on a mini-board, one per eighth note        (8 bells, rising)
    34     panel 2: X's three marks on the top row take all 6 move orders, one per eighth  (bell + glass pairs)
           34.1 "8 条获胜线 · 8 LINES"; 34.4 "3 × 2 × 1 = 6 种顺序 · 6 ORDERS"
    35     panel 3: O's first mark hops through the 6 other squares on sixteenths, O's second steps
           through the 5 left on eighths; 36.1 "6 × 5 = 30 种放法 · 30 PLACES FOR O"
    36     the odometer: the panels tick as one counter (panel 3 every game, panel 2 every 30, panel 1
           every 180) while the centre board flickers through the 1,440 games, accelerating into a blur;
           the counter rolls 0 -> 1,440, "8 × 6 × 30 = 1,440" under it              (32nd ticks, glass, bells)
    37     37.1 the counter lands on 1,440 (hero number, cyan halo), the panels dim; 37.2 the note
           "第 5 步之前，谁都凑不齐三个棋子 · NOBODY HAS 3 MARKS BEFORE MOVE 5"              (c12)
    38     38.1-38.2 the 1,440 and the panels slide to the left third (the centre board, game A again,
           shrinks to the middle); 38.3 the silent annotation of move 6: XX.OOOX.., O's middle row
           amber, "O 连成一线：8 × 6 × (6 × 5 × 4) = 5,760 · O COMPLETES A LINE"           (one glass note)
    39     39.1 game A's board, O's would-be third mark dashed on square 5, is stamped RED
           "X 已经赢了 · X ALREADY WON", "12 × 6 × 6 = 432"; 39.2 "5,760 − 432 = 5,328"; 39.3 three
           placeholders "第 7 步 ? · MOVE 7 ?" ... and hairline arrows start to cross          (c13 at 39.4)
    40     the arrows knot into one dense tangle at the centre that keeps tightening; everything else
           fades into it                                       (the nine square notes swell into 41.1)

Every number is exact and asserted below: the odometer enumerates exactly the 1,440 games that end on
move 5 (each a real game: X completes its line on move 5, nobody had three marks before), the move-6
boards replay as script.md says, 8 × 6 × (6 × 5 × 4) = 5,760, 12 × 6 × 6 = 432, 5,760 − 432 = 5,328.

Hand-over from S03 (the join at 33.1 is a cut in the music, not in the picture): this scene starts from
s03_ghosts.HANDOVER (imported, so the two stay in step): the camera home; game A's final board XXXOO....,
no move numbers, centred at HANDOVER["board"] with cell HANDOVER["cell"], drawn as S03's BoardRig draws
it (common.mark_ink strokes on the 1.4-unit opening board, scaled, widths sqrt(scale), X glow 1.2 plus
S03's breathing, in phase across the join); the three hairline panel frames HANDOVER["panels"]
(INK_DIM, 1.5 px, 90 %); the HUD label common.section_hud("§2 · ...") top left.
Hand-over to S05 (a cut, with a flash frame at 41.1): at 41.1 only the knot is left, centred on screen at
(0, 0.3); `knot_screen(END)` gives its threads in screen units, and S05 snaps them.

Shared with S05 (imported from here): MiniBoard, Label / zh_en, Thread, knot_screen. From common: the lean
Ink / InkText (hidden strokes drop their points, so Cairo skips them), cull / uncull for the counters'
hidden glyphs, show_sprite, hud_label, section_hud.
"""

from __future__ import annotations

import math
from itertools import permutations

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Circle, DashedVMobject, Group, Line, MarkupText, Mobject, Rectangle,
                   VGroup, VMobject, config)

from explainer.short import (BeatScene, FONT_OLDSTYLE, INK, INK_DIM, RED, WHITE, cjk, stroke_px, tracked)

from common import LeanInk as Ink
from common import LeanText as InkText
from common import (counter_glyphs, cull, hud_label, mark_ink, section_hud, show_sprite, uncull, win_template)
from common import (GAME_A, OC, PEN_HALO, PITCH, XC, Shot, Sounds, W, box, clamp01, ease_in_cubic,
                    ease_in_out_cubic, ease_in_out_sine, ease_out_cubic, ease_out_quad, gaussian_sprite, grid_lines,
                    lerp, move_digit, o_template, player, pulse, rgb, seg, square_centre, tag, x_template)

# ---------------------------------------------------------------- the plan's clock (script.md: bar n starts at (n-1) x 2.4 s)
BEAT, BAR = 0.6, 2.4
FIRST = 33


def bb(bar: int, beat: float = 1.0) -> float:
    """Scene time of script.md's "bar.beat" (global bar numbers): bb(35, 2.5) is "35.2+"."""
    return (bar - FIRST) * BAR + (beat - 1) * BEAT


END = bb(41)                                      # 19.2 s: 8 bars

WIN_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
ORDERS = ((1, 3, 5), (1, 5, 3), (3, 1, 5), (3, 5, 1), (5, 1, 3), (5, 3, 1))   # move numbers of X's line squares


def winner(cells) -> str | None:
    for a, b, c in WIN_LINES:
        if cells[a] != "." and cells[a] == cells[b] == cells[c]:
            return cells[a]
    return None


def replay(moves) -> tuple[str, str | None]:
    """Play squares in order (X first), asserting every move is legal; (cells, winner)."""
    cells = ["."] * 9
    for k, s in enumerate(moves):
        assert cells[s] == "." and winner(cells) is None, (moves, k)
        cells[s] = player(k)
    return "".join(cells), winner(cells)


# ---------------------------------------------------------------- the odometer's 1,440 games
def o_places(line) -> list[tuple[int, int]]:
    """O's two marks (move 2, move 4) on the 6 squares off X's line: 6 × 5 = 30 ordered pairs."""
    rest = [s for s in range(9) if s not in line]
    return [(a, b) for a in rest for b in rest if b != a]


def odometer_game(g: int) -> tuple[int, int, int, tuple[int, ...]]:
    """Game g (0..1439) of the odometer: (line, order, O place, the five moves). Panel 3 turns every
    game, panel 2 every 30, panel 1 every 180; g = 0 (and 1,440) is game A."""
    g %= 1440
    li, k, p = g // 180, (g // 30) % 6, g % 30
    line = WIN_LINES[li]
    nums = ORDERS[k]
    x_by_move = {n: sq for n, sq in zip(nums, line)}
    o1, o2 = o_places(line)[p]
    return li, k, p, (x_by_move[1], o1, x_by_move[3], o2, x_by_move[5])


ODO_GAMES = [odometer_game(g)[3] for g in range(1440)]
assert ODO_GAMES[0] == GAME_A
assert len(set(ODO_GAMES)) == 1440                                    # 8 × 6 × 30, all different
for _m in ODO_GAMES:                                                  # each a real game won by X on move 5
    _c, _w = replay(_m)
    assert _w == "X" and all(replay(_m[:k])[1] is None for k in range(5))
assert len(o_places(WIN_LINES[0])) == 30 and 8 * 6 * 30 == 1440


def _all_move5_games() -> set:
    out, cells = set(), ["."] * 9

    def walk(seq):
        if winner(cells) is not None or len(seq) == 9:
            if len(seq) == 5:
                out.add(tuple(seq))
            return
        if len(seq) == 5:
            return
        for s in range(9):
            if cells[s] == ".":
                cells[s] = player(len(seq))
                walk(seq + [s])
                cells[s] = "."
    walk([])
    return out


assert set(ODO_GAMES) == _all_move5_games()                         # exactly the games that end on move 5

# the move-6 annotation (script.md bars 38-39)
MOVE6 = (0, 3, 1, 4, 6, 5)                                           # X0 O3 X1 O4 X6 O5: XX.OOOX.., O's middle row
assert replay(MOVE6) == ("XX.OOOX..", "O")
assert replay(GAME_A) == ("XXXOO....", "X")                          # ... and game A: X already won at move 5
_o_lines = [(ln, xs) for ln in WIN_LINES for xs in permutations([s for s in range(9) if s not in ln], 3)]
assert 8 * 6 * len(_o_lines) // 8 == 5760 and len(_o_lines) * 6 == 5760
_x_already = [(ln, xs) for ln, xs in _o_lines if any(set(xs) == set(l2) for l2 in WIN_LINES)]
assert len(_x_already) * 6 == 432 == 12 * 6 * 6 and 5760 - 432 == 5328

# ---------------------------------------------------------------- layout (world units; the camera is home)
from s03_ghosts import HANDOVER                   # where S03 leaves the board and the panel frames (33.1)
PANEL_C = [np.array([x, y]) for x, y, _, _ in HANDOVER["panels"]]
PANEL_W, PANEL_H = HANDOVER["panels"][0][2], HANDOVER["panels"][0][3]
PANEL_BOARD_DY = 0.42                             # mini-board centre above the panel centre
PANEL_LABEL_DY = -0.76                            # label centre below the panel centre
CELL_P = 0.46                                     # the panels' mini-boards
CENTRE_C = np.asarray(HANDOVER["board"], dtype=float)   # the centre board: game A, as S03 leaves it
CELL_C = float(HANDOVER["cell"])
CELL_T = 1.4                                      # ... drawn as S01/S03 draw it: the opening board, scaled
COUNT_C = np.array([PANEL_C[2][0], -0.8])         # the counter, right third
FORMULA_C = np.array([PANEL_C[2][0], -1.72])
NOTE_C = np.array([PANEL_C[0][0], -0.95])         # the note (37.2), left third
SLIDE_CTRL = np.array([0.6, 2.4])                 # the counter arcs over the board as it slides left
# after the slide (38.1-38.2): the 1,440 group on the left third
LEFT_SCALE = 0.34
LEFT_PANEL_C = [np.array([-6.05 + 1.39 * k, 2.58]) for k in range(3)]
LEFT_COUNT_C = np.array([-4.66, 1.2])
LEFT_FORMULA_C = np.array([-4.66, 0.5])
COUNT_SCALE_L = 0.66
# the move-6 annotation (middle), the stamp, the result and the placeholders (right)
ROW_A = np.array([-1.25, 1.9])                    # XX.OOOX..
ROW_B = np.array([-1.25, -0.05])                  # game A + O's dashed 6th mark (the centre board, shrunk)
CELL_ROW = 0.36
TEXT_X = -0.38                                    # left edge of the annotation text
ROW_C = np.array([-0.38, -1.42])                  # 5,760 − 432 = 5,328 (left aligned)
HOLD_C = [np.array([5.45, 1.85]), np.array([5.45, 0.45]), np.array([5.45, -0.95])]
KNOT_C = np.array([0.0, 0.3])                     # the knot, on screen (S05's root lands here)
NUM_OFF = np.array([0.36, -0.36])                 # a move number sits in its square's lower-right corner

# ---------------------------------------------------------------- times
P1_FLASH = [bb(33, 1 + 0.5 * k) for k in range(8)]
P1_LABEL = bb(34)
P2_IN = bb(34)
P2_ORDERS = [bb(34, 1 + 0.5 * k) for k in range(6)]
P2_LABEL = bb(34, 4)
P3_IN = bb(35)
O1_HOPS = [bb(35) + 0.15 * k for k in range(6)]
O1_SQ = [4, 5, 6, 7, 8, 3]                        # through the 6 other squares, ending on game A's 3
O2_STEPS = [bb(35, 2.5), bb(35, 3), bb(35, 3.5), bb(35, 4), bb(35, 4.5)]
O2_SQ = [5, 6, 7, 8, 4]                           # through the 5 left, ending on game A's 4
P3_LABEL = bb(36)
ODO = (bb(36), bb(37))
LAND = bb(37)
NOTE_IN = bb(37, 2)
SLIDE = (bb(38), bb(38, 2))
ANNOT = bb(38, 3)
STAMP = bb(39)
RESULT = bb(39, 2)
HOLDS = [bb(39, 3), bb(39, 3.5), bb(39, 4)]
THREADS_IN = bb(39, 3)
KNOT_T = (bb(40), bb(40, 3))                      # the arrows knot into one tangle ...
FADE_T = (bb(40), bb(40, 4))                      # ... and everything else fades into it
ODO_P = 2.4                                       # g(u) = 1440 u^p: the odometer accelerates
GRID_IN = [0.0, bb(33, 4), bb(34, 4)]             # each panel's mini-board draws itself before its bar


def odo_count(t: float) -> float:
    """Games counted by the odometer at time t (0 before bar 36, 1,440 from 37.1)."""
    u = seg(t, *ODO)
    return 1440.0 * u ** ODO_P


def odo_time(g: float) -> float:
    return ODO[0] + BAR * (g / 1440.0) ** (1 / ODO_P)


def cam_path(t: float):
    """(centre x, centre y, frame width): home; bar 40 pushes in on the knot (it stays at (0, 0.3) on screen)."""
    e = ease_in_out_sine(seg(t, bb(40), END))
    w = W * (1 - 0.04 * e)
    z = W / w
    return 0.0, KNOT_C[1] * (1 - 1 / z), w


# ---------------------------------------------------------------- type
def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def maths(s: str, size: float = 30, color: str = INK) -> MarkupText:
    """A small formula in EB Garamond italic with lining figures (old-style 1 reads as I)."""
    return MarkupText(f'<span font_features="lnum 1">{_esc(s)}</span>', font=FONT_OLDSTYLE, slant="ITALIC",
                      font_size=size, color=color)


EN_SIZE = 16.5                                    # tracked mono caps 22 px tall at 1080p (content labels)
ZH_SIZE = 20                                      # Song/Ming, about 34 px


def en(s: str, size: float = EN_SIZE, color: str = INK_DIM, spacing: float = 0.12, upper: bool = True):
    return tracked(s, size=size, spacing=spacing, color=color, upper=upper)


class Label:
    """Lines of text (each an InkText with its own colour), stacked and aligned, shown together:
    show(anchor, scale, vis, dy). align: "c" centres the lines on the anchor, "l" puts their left edges
    on it. Lines are given as (mobject, colour)."""

    def __init__(self, lines, gap: float = 0.1, align: str = "c"):
        self.items = []
        y = 0.0
        heights = [m.height for m, _ in lines]
        total = sum(heights) + gap * (len(lines) - 1)
        y = total / 2
        for (m, col), h in zip(lines, heights):
            cy = y - h / 2
            it = InkText(m, col)
            dx = 0.0 if align == "c" else m.width / 2
            self.items.append((it, np.array([dx, cy]), col))
            y -= h + gap
        self.width = max(m.width for m, _ in lines)
        self.height = total
        self.group = VGroup(*[it for it, _, _ in self.items])

    def show(self, anchor, scale: float = 1.0, vis: float = 1.0, colors=None):
        a = np.asarray(anchor, dtype=float)
        for j, (it, off, col) in enumerate(self.items):
            c = col if colors is None else colors[j]
            it.show(a + off * scale, scale=scale, vis=vis, color=c)

    def hide(self):
        for it, _, _ in self.items:
            it.hide()


def zh_en(zh, en_text: str, zh_color=INK, en_color=INK_DIM, gap: float = 0.1, align: str = "c") -> Label:
    """A bilingual content label: the Chinese line (a mobject or a string), the tracked English under it."""
    z = cjk(zh, size=ZH_SIZE, color=zh_color) if isinstance(zh, str) else zh
    return Label([(z, zh_color), (en(en_text, color=en_color), en_color)], gap=gap, align=align)


def hex_of(c) -> str:
    c = np.clip(np.asarray(c, dtype=float), 0, 1)
    return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in c)


# ---------------------------------------------------------------- boards
def line_ink(color_core=XC.mid, glow=XC.glow, px: float = 3.0, glow_px: float = 14, layers: int = 6,
             glow_opacity: float = 0.55) -> Ink:
    """A unit segment (-0.5, 0) .. (0.5, 0) that `place_line` maps onto any line of a board."""
    return Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), color_core, px, glow, glow_px, layers=layers,
               glow_opacity=glow_opacity)


def line_affine(p, q):
    d = np.asarray(q, dtype=float) - np.asarray(p, dtype=float)
    return np.array([[d[0], -d[1]], [d[1], d[0]]]), (np.asarray(p) + np.asarray(q)) / 2


def win_ends(line, cell: float, ext: float = 0.42):
    a, b = square_centre(line[0], cell), square_centre(line[2], cell)
    d = (b - a) / np.linalg.norm(b - a)
    return a - d * cell * ext, b + d * cell * ext


class Marks:
    """A pool of X and O marks (each its own Ink) that can stand on any square of a board. style "s01":
    exactly common.mark_ink's strokes (the opening board's look)."""

    def __init__(self, n_x: int, n_o: int, size: float, glow_px_x: float = 10, glow_px_o: float = 12,
                 layers: int = 5, core_x: float = 2.6, core_o: float = 2.8, bright: float = 1.0, style: str = ""):
        if style == "s01":
            core_x, glow_px_x, core_o, glow_px_o = 2.8, 12, 3.0, 15
            layers = max(layers, 6) if layers > 2 else layers
        self.x = [Ink(x_template(size), XC.core, core_x, XC.glow, glow_px_x, layers=layers,
                      glow_opacity=0.42 * bright) for _ in range(n_x)]
        self.o = [Ink(o_template(size), OC.core, core_o, OC.glow, glow_px_o, layers=layers,
                      glow_opacity=0.5 * bright) for _ in range(n_o)]
        self.group = VGroup(*self.x, *self.o)

    def hide(self):
        for m in self.x + self.o:
            m.hide()


class MiniBoard:
    """A board with its grid, a pool of marks, move numbers 1-9 (each placed on its move's square), a
    win line and its own placement (centre, scale)."""

    def __init__(self, cell: float, n_x: int = 3, n_o: int = 2, num_size: float = 23, grid_px: float = 2.0,
                 glow_x: float = 10, glow_o: float = 12, layers: int = 5, win_color=(XC.mid, XC.glow),
                 nums: int = 9, mark_scale: float = 0.62, style: str = ""):
        self.cell = cell
        self.lines = [Ink(Line([*p, 0], [*q, 0]), INK, grid_px) for p, q in grid_lines(cell)]
        self.marks = Marks(n_x, n_o, mark_scale * cell, glow_x, glow_o, layers, style=style)
        if style == "s01":                                # S01/S03's win line: 3.2 px, glow 18, 7 layers
            self.win = line_ink(win_color[0], win_color[1], 3.2, 18, layers=7 if layers > 2 else layers)
        else:
            self.win = line_ink(win_color[0], win_color[1], 3.0, 14, layers=6)
        self.nums = [InkText(move_digit(k + 1, num_size)) for k in range(nums)]
        self.group = Group(*self.lines, *self.marks.group, self.win, *self.nums)
        self.c, self.s = np.zeros(2), 1.0

    def place(self, c, s: float = 1.0):
        self.c, self.s = np.asarray(c, dtype=float), float(s)
        return self

    def sq(self, i: int) -> np.ndarray:
        return self.c + self.s * square_centre(i, self.cell)

    def hide(self):
        for x in self.lines:
            x.hide()
        self.marks.hide()
        self.win.hide()
        for n in self.nums:
            n.hide()

    def draw_grid(self, f=1.0, vis: float = 1.0, width: float = 1.0):
        fs = f if isinstance(f, (list, tuple)) else [f] * 4
        for ln, fi in zip(self.lines, fs):
            ln.show(fi, np.eye(2) * self.s, self.c, vis=vis, width=width)

    def draw_win(self, line, f: float, vis: float = 1.0, glow: float = 1.0, width: float = 1.0):
        if line is None or f <= 0:
            self.win.hide()
            return
        p, q = win_ends(line, self.cell)
        A, b = line_affine(p * self.s, q * self.s)
        self.win.show(f, A, b + self.c, vis=vis, glow=glow, width=width)

    def draw_marks(self, xs, os, vis_x=1.0, vis_o=1.0, glow_x=1.0, glow_o=1.0, width: float = 1.0,
                   f_x=None, f_o=None):
        """xs, os: squares (None hides); vis/glow/f per mark or one value."""
        def per(v, n):
            return list(v) if isinstance(v, (list, tuple)) else [v] * n
        vx, vo = per(vis_x, len(self.marks.x)), per(vis_o, len(self.marks.o))
        gx, go = per(glow_x, len(self.marks.x)), per(glow_o, len(self.marks.o))
        fx = per(1.0 if f_x is None else f_x, len(self.marks.x))
        fo = per(1.0 if f_o is None else f_o, len(self.marks.o))
        A = np.eye(2) * self.s
        for j, m in enumerate(self.marks.x):
            sq = xs[j] if j < len(xs) else None
            if sq is None:
                m.hide()
            else:
                m.show(fx[j], A, self.sq(sq), vis=vx[j], glow=gx[j], width=width, glow_width=width)
        for j, m in enumerate(self.marks.o):
            sq = os[j] if j < len(os) else None
            if sq is None:
                m.hide()
            else:
                m.show(fo[j], A, self.sq(sq), vis=vo[j], glow=go[j], width=width, glow_width=width)

    def draw_numbers(self, moves, vis=1.0, colors=None, scale: float = 1.0, at=None):
        """Number k+1 on the square of move k (or at `at[k]`, world)."""
        for k, n in enumerate(self.nums):
            if k >= len(moves) or moves[k] is None:
                n.hide()
                continue
            v = vis[k] if isinstance(vis, (list, tuple)) else vis
            p = at[k] if at is not None else self.sq(moves[k]) + self.s * NUM_OFF * self.cell
            col = colors[k] if colors is not None else INK_DIM
            n.show(p, scale=self.s * scale, vis=v, color=col)


# ---------------------------------------------------------------- the tangle (a pure function of the time)
N_THREADS = 26
_rng = np.random.default_rng(3305)
_ANCHOR_HOLD = [c + np.array([-0.95, 0.1]) for c in HOLD_C]        # the placeholders' left edges
_ANCHOR_BOARD = [ROW_A + np.array([0.7, 0.0]), ROW_B + np.array([0.7, 0.0]), ROW_A + np.array([0.0, -0.62]),
                 ROW_B + np.array([0.0, 0.62]), ROW_C + np.array([1.6, 0.25]), LEFT_COUNT_C + np.array([1.1, 0.0]),
                 ROW_B + np.array([-0.62, 0.0]), ROW_A + np.array([-0.62, 0.0])]
THREADS = []
for _i in range(N_THREADS):
    _a = _ANCHOR_HOLD[_i % 3] + _rng.normal(0, 0.12, 2)
    _b = _ANCHOR_BOARD[int(_rng.integers(len(_ANCHOR_BOARD)))] + _rng.normal(0, 0.1, 2)
    if _i % 4 == 3:                                   # some point the other way: the cases feed back
        _a, _b = _b, _a
    _d = _b - _a
    _n = np.array([-_d[1], _d[0]]) / (np.linalg.norm(_d) + 1e-9)
    _bulge = _rng.uniform(-1.4, 1.4)
    THREADS.append({
        "a": _a, "b": _b,
        "c1": _a + _d * 0.3 + _n * _bulge * 1.6, "c2": _a + _d * 0.7 - _n * _bulge * 1.1,
        "t0": THREADS_IN + 0.9 * (_i / N_THREADS) ** 0.8,          # they come faster and faster
        "turns": _rng.choice([1.5, 2.0, 2.5, 3.0]), "phase": _rng.uniform(0, 2 * np.pi),
        "lobes": int(_rng.choice([2, 3, 4])), "w": _rng.uniform(0.25, 0.55), "spin": _rng.uniform(-2.2, 2.2),
        "tilt": _rng.uniform(0, np.pi), "ecc": _rng.uniform(0.55, 1.0), "k0": KNOT_T[0] + 0.035 * _i,
    })
N_PTS = 72
_S = np.linspace(0, 1, N_PTS)


def _bezier(th, s):
    a, c1, c2, b = th["a"], th["c1"], th["c2"], th["b"]
    u = s[:, None]
    return (1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * c1 + 3 * (1 - u) * u ** 2 * c2 + u ** 3 * b


def knot_radius(t: float) -> float:
    """The knot tightens: fast while it forms, then slowly (it keeps tightening into 41.1)."""
    return 1.25 - 0.5 * ease_in_out_cubic(seg(t, KNOT_T[0], KNOT_T[1])) - 0.12 * seg(t, KNOT_T[1], END)


def _knot(th, s, t):
    R = knot_radius(t)
    ang = 2 * np.pi * th["turns"] * s + th["phase"] + th["spin"] * (t - KNOT_T[0])
    rho = R * (1 - th["w"] + th["w"] * np.sin(th["lobes"] * ang + 1.7 * t + th["phase"]))
    x, y = rho * np.cos(ang), th["ecc"] * rho * np.sin(ang)
    c, sn = math.cos(th["tilt"] + 0.4 * t), math.sin(th["tilt"] + 0.4 * t)
    return KNOT_C + np.column_stack([c * x - sn * y, sn * x + c * y])


def thread_points(i: int, t: float) -> tuple[np.ndarray, float, float]:
    """Thread i at time t (world = screen in S04): its points, how much of it is drawn, how knotted."""
    th = THREADS[i]
    grow = ease_out_cubic(seg(t, th["t0"], th["t0"] + 0.45))
    k = ease_in_out_sine(seg(t, th["k0"], th["k0"] + 1.0))
    p = _bezier(th, _S)
    if k > 0:
        edge = np.abs(2 * _S - 1)                        # the middle is pulled in first, the ends follow
        kk = np.clip(k * (1 + 0.8 * (1 - edge)) - 0.3 * edge * (1 - k), 0, 1)[:, None]
        p = p * (1 - kk) + _knot(th, _S, t) * kk
    return p, grow, k


def knot_screen(t: float = END) -> list[np.ndarray]:
    """The threads as they stand on screen at time t (S05 starts from knot_screen(END))."""
    cx, cy, w = cam_path(min(t, END - 1e-6))
    z = W / w
    return [(thread_points(i, t)[0] - np.array([cx, cy])) * z for i in range(N_THREADS)]


class Thread(VGroup):
    """A hairline arrow: a polyline (core + a faint glow) with a small arrowhead at its end."""

    def __init__(self):
        super().__init__()
        self.glow = VMobject().set_stroke(INK, width=stroke_px(6), opacity=0.0).set_fill(opacity=0)
        self.core = VMobject().set_stroke(INK, width=stroke_px(1.5), opacity=0.0).set_fill(opacity=0)
        self.head = VMobject().set_stroke(INK, width=stroke_px(1.5), opacity=0.0).set_fill(opacity=0)
        self.add(self.glow, self.core, self.head)
        for m in (self.glow, self.core, self.head):
            m.set_points_as_corners([[0, 0, 0], [0.01, 0, 0]])

    def hide(self):
        for m in (self.glow, self.core, self.head):
            m.set_stroke(width=0, opacity=0)
            m.points = np.zeros((0, 3))

    def show(self, pts: np.ndarray, f: float, vis: float, head: float, color=INK, width: float = 1.0):
        if f <= 1e-3 or vis <= 1e-3:
            return self.hide()
        n = max(2, int(round(f * len(pts))))
        q = pts[:n]
        p3 = np.column_stack([q, np.zeros(len(q))])
        self.core.set_points_as_corners(p3)
        self.glow.set_points_as_corners(p3)
        self.core.set_stroke(color, width=stroke_px(1.5) * width, opacity=clamp01(0.85 * vis))
        self.glow.set_stroke(color, width=stroke_px(6) * width, opacity=clamp01(0.08 * vis))
        if head > 1e-3 and n >= 3:
            tip = q[-1]
            d = q[-1] - q[-3]
            d = d / (np.linalg.norm(d) + 1e-9)
            nrm = np.array([-d[1], d[0]])
            L = 0.12
            hp = [tip - d * L + nrm * L * 0.55, tip, tip - d * L - nrm * L * 0.55]
            self.head.set_points_as_corners([[*p, 0] for p in hp])
            self.head.set_stroke(color, width=stroke_px(1.5) * width, opacity=clamp01(0.85 * vis * head))
        else:
            self.head.set_stroke(width=0, opacity=0)
        return self


# ---------------------------------------------------------------- the scene
class ByHand(BeatScene):

    def construct(self):
        self.sounds = Sounds()
        self.shots: list[tuple[float, float, tuple]] = []
        self.build()
        self.score()
        self.run()

    # ------------------------------------------------------------- objects
    def build(self):
        self.frames = [Ink(Rectangle(width=PANEL_W, height=PANEL_H), INK_DIM, 1.5) for _ in range(3)]
        # panel 1: the 8 lines on a mini-board
        self.p1 = MiniBoard(CELL_P, 0, 0, nums=0)
        self.p1_lines = [line_ink(XC.mid, XC.glow, 2.6, 10, layers=5) for _ in range(8)]
        # panel 2: X's three marks and their move numbers (1, 3, 5)
        self.p2 = MiniBoard(CELL_P, 3, 0, num_size=18, nums=5, glow_x=8, layers=4)
        # panel 3: X's line (dim), O's two marks (moves 2 and 4) and their hop trails
        self.p3 = MiniBoard(CELL_P, 3, 2, num_size=18, nums=5, glow_x=6, glow_o=9, layers=4)
        self.p3_trail = [Ink(o_template(0.62 * CELL_P), OC.core, 2.0) for _ in range(4)]
        # labels
        self.lab1 = zh_en("8 条获胜线", "8 LINES")
        self.lab2 = zh_en(VGroup(maths("3 × 2 × 1 = 6", 30), cjk("种顺序", size=ZH_SIZE)).arrange(RIGHT, buff=0.12),
                          "6 ORDERS")
        self.lab3 = zh_en(VGroup(maths("6 × 5 = 30", 30), cjk("种放法", size=ZH_SIZE)).arrange(RIGHT, buff=0.12),
                          "30 PLACES FOR O")
        # the centre board: the game being counted, with up to 3 fading copies (the odometer's blur)
        self.centre = [MiniBoard(CELL_T, 3, 2, num_size=23, nums=5 if k == 0 else 0, layers=6 if k == 0 else 2,
                                 style="s01") for k in range(4)]
        self.ghost_o = Ink(DashedVMobject(o_template(0.62 * CELL_T), num_dashes=12, dashed_ratio=0.55), INK_DIM, 2.4)
        self.ghost_num = InkText(move_digit(6, 23), INK_DIM)
        # the counter: an odometer with the hero's glow and halo
        from explainer.short import RollingCounter
        self.counter = RollingCounter(0, digits=4, size=88, color=WHITE)
        self.counter.clear_updaters()
        self.counter.move_to([*COUNT_C, 0])
        self.counter.layout()
        self.count_w0 = self.counter.ref.width
        self.hero = self.final_glyphs(1440)
        self.hero_glow = []
        for g in self.hero:
            layers = []
            for k in range(6, 0, -1):
                c = g.copy().set_fill(opacity=0).set_stroke(XC.glow, width=0, opacity=0)
                layers.append((c, 0.6 * (1 - k / 7) ** 2, stroke_px(2 * 18) * k / 6))
            self.hero_glow.append(layers)
        self.hero_glow_group = VGroup(*[c for lay in self.hero_glow for c, _, _ in lay])
        self.halo = gaussian_sprite(XC.glow, 96, 0.33, aspect=2.4)
        self.halo.stretch_to_fit_width(6.2).stretch_to_fit_height(2.6)
        self.formula = InkText(maths("8 × 6 × 30 = 1,440", 30), INK)
        self.note = zh_en("第 5 步之前，谁都凑不齐三个棋子", "NOBODY HAS 3 MARKS BEFORE MOVE 5", gap=0.12)
        # the move-6 annotation, the stamp, the result
        self.row_a = MiniBoard(CELL_ROW, 3, 3, num_size=16, nums=6, glow_x=7, glow_o=9, layers=4,
                               win_color=(OC.mid, OC.glow))
        self.lab_a = Label([(cjk("O 连成一线", size=ZH_SIZE, color=INK), INK),
                            (en("O COMPLETES A LINE"), INK_DIM),
                            (maths("8 × 6 × (6 × 5 × 4) = 5,760", 30), INK)], gap=0.11, align="l")
        self.lab_b = Label([(cjk("X 已经赢了", size=ZH_SIZE, color=RED), RED),
                            (en("X ALREADY WON", color=RED), RED),
                            (maths("12 × 6 × 6 = 432", 30), INK)], gap=0.11, align="l")
        self.stamp = Ink(Rectangle(width=1.5, height=1.5), RED, 2.6, RED, 10, layers=4, glow_opacity=0.5)
        self.result = InkText(maths("5,760 − 432 = 5,328", 36), INK)
        self.result_glow = gaussian_sprite(OC.glow, 64, 0.3, aspect=3.0)
        self.result_glow.stretch_to_fit_width(3.6).stretch_to_fit_height(0.9)
        self.holds = [zh_en(f"第 {k} 步 ?", f"MOVE {k} ?", gap=0.1) for k in (7, 8, 9)]
        self.hold_frames = [Ink(DashedVMobject(Rectangle(width=1.85, height=0.95), num_dashes=28, dashed_ratio=0.5),
                                INK_DIM, 1.4) for _ in range(3)]
        self.threads = [Thread() for _ in range(N_THREADS)]
        # HUD (screen space)
        self.sec = section_hud("§2 · 对局会提前结束 · GAMES STOP EARLY")
        self.hud5 = hud_label("第 5 步", "MOVE 5")
        self.hud6 = hud_label("第 6 步", "MOVE 6")
        self.hud_count = RollingCounter(0, digits=4, size=12, color=INK_DIM, font="Noto Sans Mono", weight="NORMAL")
        self.hud_count.clear_updaters()
        for h in (self.hud5, self.hud6):
            h.to_corner(np.array([1, 1, 0]), buff=0.45).shift(LEFT * 0.95)
        self.hud_count.next_to(self.hud5, RIGHT, buff=0.22)
        self.hud_count.align_to(self.hud5, DOWN)
        self.hud_count.layout()
        self.hud5_t = InkText(self.hud5, INK_DIM)
        self.hud6_t = InkText(self.hud6, INK_DIM)
        self.hud5_c = self.hud5.get_center()[:2]

        self.clock_mob = Mobject()
        self.clock_mob.add_updater(lambda m: self.update_state(self.clock()))
        self.add(self.clock_mob, self.camera.frame)
        self.add(self.halo, self.result_glow, *self.frames, self.p1.group, *self.p1_lines, self.p2.group,
                 *self.p3_trail, self.p3.group, self.lab1.group, self.lab2.group, self.lab3.group,
                 *[b.group for b in reversed(self.centre)], self.ghost_o, self.ghost_num, self.hero_glow_group,
                 self.counter, self.formula, self.note.group, self.row_a.group, self.lab_a.group, self.lab_b.group,
                 self.stamp, self.result, *[h.group for h in self.holds], *self.hold_frames, *self.threads)
        self.fix(self.sec, self.hud5_t, self.hud6_t, self.hud_count)
        self.update_state(0.0)

    def final_glyphs(self, value: int) -> VGroup:
        c = self.counter
        c.manual = None
        c.value.set_value(value)
        c.layout()
        out = []
        for col in c.columns:
            vis = [g for g in col if g.get_fill_opacity() > 0.99]
            if vis:
                out.append(vis[0].copy())
        for k, sep in c.separators:
            if sep.get_fill_opacity() > 0.99:
                out.append(sep.copy())
        c.value.set_value(0)
        c.layout()
        return VGroup(*out)

    # ------------------------------------------------------------- the picture at time t
    def update_state(self, t: float):
        cx, cy, w = cam_path(t)
        self.camera.frame.set(width=w)
        self.camera.frame.move_to([cx, cy, 0])
        fade = 1 - ease_in_cubic(seg(t, *FADE_T))           # bar 40: everything but the knot fades into it
        self.update_panels(t, fade)
        self.update_centre(t, fade)
        self.update_counter(t, fade)
        self.update_annotation(t, fade)
        self.update_threads(t)
        self.update_hud(t)

    # --- the slide to the left third (38.1-38.2)
    @staticmethod
    def slide(t: float) -> float:
        return ease_in_out_cubic(seg(t, *SLIDE))

    def panel_place(self, k: int, t: float):
        """(centre, scale) of panel k: in place, then (38.1-38.2) small on the left third. The panels
        go first (they clear the top before the counter arcs over the board)."""
        e = ease_out_cubic(seg(t, SLIDE[0], SLIDE[0] + 0.45))
        return PANEL_C[k] + (LEFT_PANEL_C[k] - PANEL_C[k]) * e, 1 + (LEFT_SCALE - 1) * e

    def odo_state(self, t: float):
        """The odometer's game index during bar 36 (0 before: game A's choices; 1,440 after)."""
        if t < ODO[0]:
            return 0
        return int(math.floor(odo_count(t) + 1e-9))

    def update_panels(self, t: float, fade: float):
        dim = 1 - 0.55 * ease_out_cubic(seg(t, LAND, LAND + 0.6))      # 37.1: the panels dim
        g = self.odo_state(t)
        o_li, o_k, o_p, _ = odometer_game(g)
        odo_on = ODO[0] <= t < ODO[1]
        breathe = 1 + 0.08 * math.sin(2 * math.pi * t / BAR)
        for j, fr in enumerate(self.frames):
            c, s = self.panel_place(j, t)
            fr.show(1.0, np.eye(2) * s, c, vis=0.9 * fade * (0.6 + 0.4 * dim))
        # ---- panel 1: 8 lines flash (bar 33), the top row stays; in bar 36 the lit line steps every 180
        c1, s1 = self.panel_place(0, t)
        bc = c1 + np.array([0, PANEL_BOARD_DY]) * s1
        B = self.p1.place(bc, s1)
        B.draw_grid(self.grid_f(0, t), vis=fade * dim)
        cur = 0 if not odo_on else o_li
        for j, ink in enumerate(self.p1_lines):
            t0 = P1_FLASH[j]
            if t < t0:
                ink.hide()
                continue
            f = ease_out_quad(seg(t, t0, t0 + 0.14))
            flash = pulse(t, t0, 0.22)
            lit = 1.0 if j == cur else 0.0
            if t >= P1_LABEL and j == cur:
                lv = 1.0
            else:
                lv = 0.16 + 0.84 * flash
            if odo_on:
                lv = 1.0 if j == cur else 0.14
            if t >= ODO[1]:
                lv = 1.0 if j == 0 else 0.14
            p, q = win_ends(WIN_LINES[j], CELL_P, 0.3)
            A, b = line_affine(p * s1, q * s1)
            ink.show(f, A, b + bc, vis=lv * fade * dim, glow=0.6 + 1.2 * flash + 0.3 * lit * breathe,
                     width=max(0.5, s1 ** 0.5))
        self.lab1.show(c1 + np.array([0, PANEL_LABEL_DY]) * s1 + np.array([0, -0.06 * (1 - seg(t, P1_LABEL, P1_LABEL + 0.3))]),
                       scale=s1, vis=ease_out_cubic(seg(t, P1_LABEL, P1_LABEL + 0.3)) * fade * dim
                       * (1 - seg(t, SLIDE[0], SLIDE[0] + 0.25)))
        # ---- panel 2: X's three marks take the 6 orders (bar 34); in bar 36 they follow panel 1's line
        c2, s2 = self.panel_place(1, t)
        bc2 = c2 + np.array([0, PANEL_BOARD_DY]) * s2
        B2 = self.p2.place(bc2, s2)
        B2.draw_grid(self.grid_f(1, t), vis=fade * dim)
        if t < P2_IN:
            B2.marks.hide()
            B2.draw_numbers([])
        else:
            line = WIN_LINES[o_li] if odo_on else WIN_LINES[0]
            kk = o_k if odo_on else (0 if t >= ODO[1] else self.order_at(t))
            fx = ease_out_cubic(seg(t, P2_IN, P2_IN + 0.25))
            B2.draw_marks(list(line), [], vis_x=fade * dim, glow_x=1.0 + 0.5 * self.order_flash(t),
                          f_x=fx, width=max(0.5, s2 ** 0.5))
            # the move numbers ride to their squares at each new order
            nums = ORDERS[kk]
            prev = ORDERS[max(0, kk - 1)] if not odo_on else nums
            u = ease_out_cubic(seg(t, self.order_time(kk), self.order_time(kk) + 0.2)) if not odo_on else 1.0
            at = []
            moves = [None] * 5
            for n in (1, 3, 5):
                sq_new = line[nums.index(n)]
                sq_old = line[prev.index(n)]
                pa = B2.sq(sq_old) + s2 * NUM_OFF * CELL_P
                pb = B2.sq(sq_new) + s2 * NUM_OFF * CELL_P
                arc = np.array([0.0, 0.12 * math.sin(math.pi * u)]) * s2
                moves[n - 1] = sq_new
                at.append((n - 1, pa + (pb - pa) * u + arc))
            pos = [None] * 5
            for i, p_ in at:
                pos[i] = p_
            nv = ease_out_cubic(seg(t, P2_IN + 0.1, P2_IN + 0.35)) * fade * dim
            fl = self.order_flash(t)
            col = hex_of(rgb(INK) * (1 - fl) + rgb(WHITE) * fl)
            B2.draw_numbers(moves, vis=nv, colors=[col] * 5, scale=1.0, at=[pos[i] if pos[i] is not None else
                                                                               np.zeros(2) for i in range(5)])
        self.lab2.show(c2 + np.array([0, PANEL_LABEL_DY]) * s2 + np.array([0, -0.06 * (1 - seg(t, P2_LABEL, P2_LABEL + 0.3))]),
                       scale=s2, vis=ease_out_cubic(seg(t, P2_LABEL, P2_LABEL + 0.3)) * fade * dim
                       * (1 - seg(t, SLIDE[0], SLIDE[0] + 0.25)))
        # ---- panel 3: X's line (dim), O's first mark hops 6 squares, the second steps 5 (bar 35)
        c3, s3 = self.panel_place(2, t)
        bc3 = c3 + np.array([0, PANEL_BOARD_DY]) * s3
        B3 = self.p3.place(bc3, s3)
        B3.draw_grid(self.grid_f(2, t), vis=fade * dim)
        for tr in self.p3_trail:
            tr.hide()
        if t < P3_IN:
            B3.marks.hide()
            B3.draw_numbers([])
        else:
            line = WIN_LINES[o_li] if odo_on else WIN_LINES[0]
            xv = 0.42 * ease_out_cubic(seg(t, P3_IN, P3_IN + 0.2)) * fade * dim
            if odo_on or t >= ODO[1]:
                o1, o2 = o_places(line)[o_p] if odo_on else (3, 4)
                o1p, o2p = B3.sq(o1), B3.sq(o2)
                v1 = v2 = 1.0
                f2 = 1.0
            else:
                o1p, v1, o1_moving = self.hop_pos(B3, t, O1_HOPS, O1_SQ)
                o2p, v2, _ = self.hop_pos(B3, t, O2_STEPS, O2_SQ)
                f2 = ease_out_cubic(seg(t, O2_STEPS[0], O2_STEPS[0] + 0.15))
                # a short trail behind the hopping marks (motion blur)
                for j, (times, sqs) in enumerate(((O1_HOPS, O1_SQ), (O2_STEPS, O2_SQ))):
                    for gi in range(2):
                        q, vq, mv = self.hop_pos(B3, t - 0.03 * (gi + 1), times, sqs)
                        if mv > 0.05 and vq > 0:
                            self.p3_trail[2 * j + gi].show(1.0, np.eye(2) * s3, q,
                                                          vis=(0.3, 0.14)[gi] * mv * fade * dim)
            B3.draw_marks(list(line), [], vis_x=xv, glow_x=0.4, width=max(0.5, s3 ** 0.5))
            # O marks are drawn through the pool at arbitrary points (hops between squares)
            A = np.eye(2) * s3
            om = B3.marks.o
            if v1 > 0:
                om[0].show(1.0, A, o1p, vis=v1 * fade * dim, glow=1.0 + 0.6 * self.hop_flash(t, O1_HOPS),
                           width=max(0.5, s3 ** 0.5), glow_width=max(0.5, s3 ** 0.5))
            else:
                om[0].hide()
            if v2 > 0:
                om[1].show(f2, A, o2p, vis=v2 * fade * dim, glow=1.0 + 0.6 * self.hop_flash(t, O2_STEPS),
                           width=max(0.5, s3 ** 0.5), glow_width=max(0.5, s3 ** 0.5))
            else:
                om[1].hide()
            nv = fade * dim
            at = [None, o1p + s3 * NUM_OFF * CELL_P, None, o2p + s3 * NUM_OFF * CELL_P, None]
            B3.draw_numbers([None, 0 if v1 > 0 else None, None, 0 if v2 > 0 else None, None],
                            vis=[0, v1 * nv, 0, v2 * nv, 0], colors=[INK] * 5, scale=1.0,
                            at=[a if a is not None else np.zeros(2) for a in at])
        self.lab3.show(c3 + np.array([0, PANEL_LABEL_DY]) * s3 + np.array([0, -0.06 * (1 - seg(t, P3_LABEL, P3_LABEL + 0.3))]),
                       scale=s3, vis=ease_out_cubic(seg(t, P3_LABEL, P3_LABEL + 0.3)) * fade * dim
                       * (1 - seg(t, SLIDE[0], SLIDE[0] + 0.25)))

    @staticmethod
    def grid_f(k: int, t: float) -> list:
        return [ease_out_quad(seg(t, GRID_IN[k] + 0.07 * i, GRID_IN[k] + 0.07 * i + 0.22)) for i in range(4)]

    @staticmethod
    def order_at(t: float) -> int:
        k = 0
        for j, tj in enumerate(P2_ORDERS):
            if t >= tj:
                k = j
        return k

    @staticmethod
    def order_time(k: int) -> float:
        return P2_ORDERS[k]

    @staticmethod
    def order_flash(t: float) -> float:
        return max(pulse(t, tj, 0.25) for tj in P2_ORDERS) if t >= P2_ORDERS[0] and t < ODO[0] else 0.0

    @staticmethod
    def hop_flash(t, times) -> float:
        return max(pulse(t, tj, 0.18) for tj in times) if t < ODO[0] else 0.0

    @staticmethod
    def hop_pos(B: MiniBoard, t: float, times, sqs):
        """Where a hopping O is: it lands on each square at its time (an eased hop with a small arc);
        how visible (0 before its first hop) and how fast it is moving (0..1)."""
        if t < times[0]:
            return B.sq(sqs[0]), 0.0, 0.0
        j = max(i for i, tj in enumerate(times) if t >= tj)
        dur = 0.12
        u = seg(t, times[j], times[j] + dur)
        if j == 0:
            return B.sq(sqs[0]), ease_out_cubic(seg(t, times[0], times[0] + 0.08)), 0.0
        a, b = B.sq(sqs[j - 1]), B.sq(sqs[j])
        e = ease_out_cubic(u)
        arc = np.array([0.0, 0.16 * B.s * math.sin(math.pi * e)])
        moving = math.sin(math.pi * u) if u < 1 else 0.0
        return a + (b - a) * e + arc, 1.0, moving

    # --- the centre board: game A, then the odometer's games (bar 36), then game A again
    def centre_place(self, t: float):
        """The centre board's centre and scale (of the 1.4 template): S03's hand-over, then (38.1-38.2)
        small in row B."""
        e = self.slide(t)
        return CENTRE_C + (ROW_B - CENTRE_C) * e, (CELL_C + (CELL_ROW - CELL_C) * e) / CELL_T

    def update_centre(self, t: float, fade: float):
        c, s = self.centre_place(t)
        width = max(0.4, s ** 0.5)                       # strokes thin as the board shrinks (as in S03)
        boards = self.centre
        for B in boards:
            B.place(c, s)
        boards[0].draw_grid(1.0, vis=fade, width=width)
        for B in boards[1:]:
            for ln in B.lines:
                ln.hide()
        breathe = -0.12 * math.cos(2 * math.pi * t / BAR)   # S03's breathing, in phase across the join
        if ODO[0] <= t < ODO[1]:
            # the odometer: the current game, and fading copies of the games just shown (a blur)
            gf = odo_count(t)
            rate = 1440 * ODO_P * (seg(t, *ODO) ** (ODO_P - 1)) / BAR       # games per second
            per_frame = rate / 60.0
            step = max(1.0, per_frame / 2.5)
            for j, B in enumerate(boards):
                gj = int(math.floor(gf - j * step))
                if j > 0 and (per_frame < 1.2 or gj < 0):
                    B.marks.hide()
                    B.win.hide()
                    continue
                _, _, _, game = odometer_game(gj)
                li = odometer_game(gj)[0]
                vis = (1.0, 0.45, 0.28, 0.16)[j] * fade
                land = pulse(t, odo_time(gj), 0.12) if per_frame < 1 else 0.0
                B.draw_marks([game[0], game[2], game[4]], [game[1], game[3]], vis_x=vis, vis_o=vis,
                             glow_x=1.0 + 0.5 * land, glow_o=1.0 + 0.5 * land, width=width)
                B.draw_win(WIN_LINES[li], 1.0, vis=vis * 0.9, glow=0.9, width=width)
                if j == 0:
                    nv = (1.0 if per_frame < 3 else 0.55) * fade
                    B.draw_numbers(list(game), vis=nv, colors=[INK] * 5)
            return
        for B in boards[1:]:
            B.marks.hide()
            B.win.hide()
        B = boards[0]
        glow = 1.2 + breathe + 0.8 * pulse(t, LAND, 0.4)
        B.draw_marks([0, 1, 2], [3, 4], vis_x=fade, vis_o=fade, glow_x=glow, glow_o=1.0, width=width)
        B.draw_win(WIN_LINES[0], 1.0, vis=fade, glow=1.0 + breathe + 0.6 * pulse(t, LAND, 0.4), width=width)
        nv = (ease_out_cubic(seg(t, ODO[0], ODO[0] + 0.3)) if t < ODO[1] else 1.0) * fade
        nv *= 1 - seg(t, SLIDE[0], SLIDE[0] + 0.25)          # too small to read once the board shrinks
        B.draw_numbers(list(GAME_A), vis=nv, colors=[INK] * 5)
        # 39.1: O's would-be third mark, dashed on square 5 (a ghost move: never glows)
        gv = ease_out_cubic(seg(t, STAMP, STAMP + 0.25)) * fade
        if gv > 0:
            self.ghost_o.show(1.0, np.eye(2) * s, B.sq(5), vis=0.55 * gv, width=width)
            self.ghost_num.hide()
        else:
            self.ghost_o.hide()
            self.ghost_num.hide()

    # --- the counter and the hero 1,440
    def counter_place(self, t: float):
        e = ease_in_out_cubic(seg(t, SLIDE[0] + 0.05, SLIDE[1]))
        p = (1 - e) ** 2 * COUNT_C + 2 * (1 - e) * e * SLIDE_CTRL + e ** 2 * LEFT_COUNT_C
        return p, 1 + (COUNT_SCALE_L - 1) * e

    def update_counter(self, t: float, fade: float):
        cnt = self.counter
        uncull(counter_glyphs(cnt))
        c, s = self.counter_place(t)
        vis = ease_out_cubic(seg(t, ODO[0], ODO[0] + 0.25)) * fade
        g = min(1440.0, odo_count(t)) if t >= ODO[0] else 0.0
        if t >= LAND:
            g = 1440.0
        cnt.value.set_value(math.floor(g))           # whole games: every frame shows an exact count
        cnt.manual = None
        k = s * self.count_w0 / cnt.ref.width        # scale the whole counter about its centre
        if abs(k - 1) > 1e-6:
            cnt.scale(k)
        cnt.ref.move_to([*c, 0])
        cnt.layout()
        col = WHITE if t >= LAND else INK
        for colm in cnt.columns:
            for gl in colm:
                gl.set_fill(col, opacity=gl.get_fill_opacity() * vis)
        for _, sep in cnt.separators:
            sep.set_fill(col, opacity=sep.get_fill_opacity() * vis)
        cull(counter_glyphs(cnt))
        # the hero glow (per glyph) and the halo: cyan, X's colour (these are X's wins)
        breathe = 1 + 0.12 * math.sin(2 * math.pi * (t - LAND) / BAR)
        hv = 0.0
        if t >= LAND:
            hv = (ease_out_cubic(seg(t, LAND, LAND + 0.35)) * breathe + 1.1 * pulse(t, LAND, 0.3)) * fade
        for g_, lay in zip(self.hero, self.hero_glow):
            target = c + (g_.get_center()[:2] - COUNT_C) * s
            for cpy, base, wk in lay:
                uncull([cpy])
                if hv <= 1e-3:
                    cpy.set_stroke(width=0, opacity=0)
                    cpy.set_fill(opacity=0)
                    cull([cpy])
                    continue
                kk = g_.height * s / max(1e-6, cpy.height)
                if abs(kk - 1) > 1e-6:
                    cpy.scale(kk)
                cpy.move_to([*target, 0])
                cpy.set_stroke(XC.glow, width=wk * s, opacity=clamp01(base * hv))
        halo_v = 0.0
        if t >= LAND:
            halo_v = 0.42 * ease_out_cubic(seg(t, LAND, LAND + 0.5)) * (1 + 0.1 * math.sin(2 * math.pi * (t - LAND) / BAR))
        show_sprite(self.halo, c, 6.2 * s, 2.6 * s, halo_v * fade * (1 - 0.35 * self.slide(t)))
        # the formula under it (bar 36 on), and the note (37.2)
        fv = ease_out_cubic(seg(t, ODO[0] + 0.15, ODO[0] + 0.45)) * fade
        fv *= 1 - seg(t, SLIDE[0], SLIDE[0] + 0.12) * (1 - seg(t, SLIDE[1] - 0.12, SLIDE[1]))   # out of the way
        e = ease_in_out_cubic(seg(t, SLIDE[0] + 0.05, SLIDE[1]))
        fc = c + (FORMULA_C - COUNT_C) * (1 - e) + (LEFT_FORMULA_C - LEFT_COUNT_C) * e
        self.formula.show(fc, scale=1 + (0.85 - 1) * e, vis=fv, color=INK)
        nv = ease_out_cubic(seg(t, NOTE_IN, NOTE_IN + 0.4)) * (1 - seg(t, SLIDE[0], SLIDE[0] + 0.25)) * fade
        self.note.show(NOTE_C + np.array([0, -0.05 * (1 - seg(t, NOTE_IN, NOTE_IN + 0.4))]), vis=nv,
                       colors=[INK, INK_DIM])

    # --- the move-6 annotation, the stamp, the result, the placeholders
    def update_annotation(self, t: float, fade: float):
        a = ease_out_cubic(seg(t, ANNOT, ANNOT + 0.35)) * fade
        B = self.row_a.place(ROW_A + np.array([0.0, -0.08 * (1 - a)]), 1.0)
        if a <= 1e-3:
            B.hide()
            self.lab_a.hide()
        else:
            B.draw_grid(1.0, vis=a)
            xs = [MOVE6[0], MOVE6[2], MOVE6[4]]
            os = [MOVE6[1], MOVE6[3], MOVE6[5]]
            gl = 1.0 + 0.7 * pulse(t, ANNOT, 0.4) + 0.12 * math.sin(2 * math.pi * t / BAR)
            B.draw_marks(xs, os, vis_x=a, vis_o=a, glow_x=0.8, glow_o=[1.0, 1.0, gl])
            B.draw_win(WIN_LINES[1], ease_out_quad(seg(t, ANNOT + 0.1, ANNOT + 0.45)), vis=a, glow=gl)
            B.draw_numbers(list(MOVE6), vis=a, colors=[INK_DIM] * 6)
            self.lab_a.show(np.array([TEXT_X, ROW_A[1] + 0.02]) + np.array([0, -0.06 * (1 - a)]), vis=a)
        # 39.1 the stamp on game A's board: "X 已经赢了 · X ALREADY WON", 12 × 6 × 6 = 432
        sv = ease_out_cubic(seg(t, STAMP, STAMP + 0.2)) * fade
        if sv <= 1e-3:
            self.stamp.hide()
            self.lab_b.hide()
        else:
            k = 1.18 - 0.18 * ease_out_cubic(seg(t, STAMP, STAMP + 0.18))       # pressed down onto the board
            th = math.radians(-7)
            A = k * np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
            self.stamp.show(1.0, A, ROW_B, vis=0.9 * sv, glow=0.6 + 1.4 * pulse(t, STAMP, 0.3))
            self.lab_b.show(np.array([TEXT_X, ROW_B[1] + 0.02]), vis=sv,
                            colors=[RED, RED, INK])
        rv = ease_out_cubic(seg(t, RESULT, RESULT + 0.35)) * fade
        w = self.result.tmpl.width
        self.result.show(ROW_C + np.array([w / 2, -0.06 * (1 - rv)]), vis=rv, color=INK)
        show_sprite(self.result_glow, (ROW_C[0] + w * 0.86, ROW_C[1]), None, None,
                    0.35 * rv * (1 + 0.15 * math.sin(2 * math.pi * t / BAR)) + 0.5 * pulse(t, RESULT, 0.4) * fade)
        for j, (lab, fr) in enumerate(zip(self.holds, self.hold_frames)):
            hv = ease_out_cubic(seg(t, HOLDS[j], HOLDS[j] + 0.3)) * fade
            if hv <= 1e-3:
                lab.hide()
                fr.hide()
                continue
            wob = np.array([0.0, 0.025 * math.sin(2 * math.pi * (t - HOLDS[j]) / 1.2 + j)])
            lab.show(HOLD_C[j] + wob + np.array([0.0, -0.06 * (1 - hv)]), vis=hv * 0.9, colors=[INK, INK_DIM])
            fr.show(1.0, np.eye(2), HOLD_C[j] + wob, vis=0.7 * hv)

    def update_threads(self, t: float):
        cx, cy, w = cam_path(t)
        z = W / w
        for i, th in enumerate(self.threads):
            pts, grow, k = thread_points(i, t)
            if grow <= 1e-3:
                th.hide()
                continue
            bright = 0.75 + 0.25 * k
            th.show(pts, grow, bright, head=(1 - seg(k, 0.0, 0.35)) * grow, width=1.0 / z)

    def update_hud(self, t: float):
        to6 = ease_in_out_sine(seg(t, ANNOT, ANNOT + 0.3))
        hv = (1 - ease_in_cubic(seg(t, FADE_T[0], FADE_T[1]))) * ease_out_cubic(seg(t, 0.0, 0.35))
        self.hud5_t.show(self.hud5_c + np.array([0, 0.05 * to6]), vis=(1 - to6) * hv, color=INK_DIM)
        self.hud6_t.show(self.hud5_c + np.array([0, -0.05 * (1 - to6)]), vis=to6 * hv, color=INK_DIM)
        hc = self.hud_count
        uncull(counter_glyphs(hc))
        if t < ODO[0]:
            v, cv = 0.0, 0.0
        elif t < ANNOT:
            v, cv = min(1440.0, odo_count(t)), 1.0 - to6
        elif t < RESULT:
            v, cv = 0.0, 0.0
        else:
            u = ease_out_cubic(seg(t, RESULT, RESULT + 0.45))
            v, cv = 5328.0 * u, 1.0
        hc.value.set_value(math.floor(v))
        hc.layout()
        on = ease_out_cubic(seg(t, ODO[0], ODO[0] + 0.25)) if t < ANNOT else ease_out_cubic(seg(t, RESULT, RESULT + 0.2))
        for colm in hc.columns:
            for gl in colm:
                gl.set_fill(INK_DIM, opacity=gl.get_fill_opacity() * cv * on * hv)
        for _, sep in hc.separators:
            sep.set_fill(INK_DIM, opacity=sep.get_fill_opacity() * cv * on * hv)
        cull(counter_glyphs(hc))

    # ------------------------------------------------------------- the sounds (from the same numbers)
    def score(self):
        S = self.sounds
        # bar 33: the 8 lines, 8 bells rising through the chord (E9)
        S.phrase("8 lines", [(t, "X", float(PANEL_C[0][0] + 0.25 * (j - 3.5) / 3.5)) for j, t in enumerate(P1_FLASH)],
                 rise=True, gain=0.8)
        S.phrase("8 LINES", [(P1_LABEL, "bell@B5", float(PANEL_C[0][0]))], gain=0.7)
        # bar 34: the 6 orders, a bell (the square of move 1) and a glass (the square of move 5) each
        pairs = []
        for k, t in enumerate(P2_ORDERS):
            nums = ORDERS[k]
            sq1, sq5 = WIN_LINES[0][nums.index(1)], WIN_LINES[0][nums.index(5)]
            pairs += [(t, tag("X", sq1), float(PANEL_C[1][0] - 0.3)), (t + 0.02, f"glass@{PITCH[sq5]}", float(PANEL_C[1][0] + 0.3))]
        S.phrase("6 orders", pairs, gain=0.8)
        S.phrase("6 ORDERS", [(P2_LABEL, "bell@G#5", float(PANEL_C[1][0]))], gain=0.7)
        # bar 35: O's first mark on sixteenths (6 squares), the second on eighths (5 squares)
        S.phrase("O first", [(t, tag("O", sq), float(PANEL_C[2][0])) for t, sq in zip(O1_HOPS, O1_SQ)], gain=0.75)
        S.phrase("O second", [(t, tag("O", sq), float(PANEL_C[2][0])) for t, sq in zip(O2_STEPS, O2_SQ)], gain=0.85)
        S.phrase("30 PLACES", [(P3_LABEL, "bell@C#6", float(PANEL_C[2][0]))], gain=0.7)
        # bar 36: the odometer, three layered streams: a tick per game (they blur), a glass note each
        # time the order changes (every 30), a bell each time the line changes (every 180)
        S.phrase("odometer", [(odo_time(g), "tick", float(COUNT_C[0])) for g in range(1, 1441)], rise=True, gain=0.8)
        fm9 = ["F#4", "A4", "C#5", "E5", "G#5", "A5"]
        S.phrase("orders", [(odo_time(30 * j), f"glass@{fm9[(j % 6)]}", float(PANEL_C[1][0])) for j in range(1, 49)],
                 gain=0.5)
        bells = ["F#5", "A5", "C#6", "E6", "F#6", "G#6", "A6", "C#7"]
        S.phrase("lines", [(odo_time(180 * j), f"bell@{bells[j - 1]}", float(PANEL_C[0][0])) for j in range(1, 9)],
                 gain=0.7)
        # 37.1: the hit is video.yaml's; the counter lands with one bell; 37.2 the note (a pluck)
        S.phrase("1,440", [(LAND, "bell@A5", float(COUNT_C[0]))], gain=0.8)
        S.phrase("note", [(NOTE_IN, "pluck@E5", float(NOTE_C[0]))], gain=0.5)
        # 38.3: one glass note (O's count): O's middle square
        S.phrase("O line", [(ANNOT, tag("O", 4), float(ROW_A[0]))])
        # 39.1: the RED stamp: a short reverse whoosh and a low thud; 39.2 the result; 39.3 the placeholders
        S.effect(STAMP - 0.35, "whoosh_rev", 0.35, float(ROW_B[0]))
        S.effect(STAMP, "thump", 0.6, float(ROW_B[0]))
        S.phrase("5,328", [(RESULT, tag("O", 5), float(ROW_C[0] + 1.5))], gain=0.7)
        S.phrase("placeholders", [(t, "pluck@" + n, float(HOLD_C[j][0])) for j, (t, n) in
                                  enumerate(zip(HOLDS, ("B3", "D4", "F#4")))], gain=0.55)
        # 39.3 -> 41.1: the nine square notes at once, struck again and again as the knot tightens, then
        # nine reversed glass notes that swell into 41.1 and stop dead there (the cut)
        strikes = [HOLDS[0], bb(40), bb(40, 2), bb(40, 3), bb(40, 3.5), bb(40, 4)]
        for j, ts in enumerate(strikes):
            S.phrase(f"cluster {j}", [(ts + 0.012 * q, f"glass@{PITCH[q]}", -1.5 + 0.375 * q) for q in range(9)],
                     gain=0.28 + 0.07 * j)
        S.phrase("cluster swell", [(END - 1.405, f"glass_rev@{PITCH[q]}", -1.5 + 0.375 * q) for q in range(9)], gain=0.6)
        S.log(self)
        self.mark("riser", at=HOLDS[0], dur=END - HOLDS[0])

    # ------------------------------------------------------------- the logged events and the clock
    def log_events(self):
        ev = self.shots

        def add(t, dur, x, y, w, h):
            ev.append((float(t), float(dur), (x, y, w, h)))
        for t in P1_FLASH:
            add(t, 0.3, *(PANEL_C[0] + [0, PANEL_BOARD_DY]), 1.2, 1.2)
        add(P1_LABEL, BEAT, PANEL_C[0][0], PANEL_C[0][1] - 0.5, 2.0, 0.6)
        for t in P2_ORDERS:
            add(t, 0.3, *(PANEL_C[1] + [0, PANEL_BOARD_DY]), 1.2, 1.2)
        add(P2_LABEL, BEAT, PANEL_C[1][0], PANEL_C[1][1] - 0.5, 2.6, 0.6)
        for t in O1_HOPS:
            add(t, 0.15, *(PANEL_C[2] + [0, PANEL_BOARD_DY]), 1.2, 1.2)
        for t in O2_STEPS:
            add(t, 0.3, *(PANEL_C[2] + [0, PANEL_BOARD_DY]), 1.2, 1.2)
        add(P3_LABEL, BEAT, PANEL_C[2][0], PANEL_C[2][1] - 0.5, 2.6, 0.6)
        for k in range(16):                                   # the odometer: the whole picture moves
            add(ODO[0] + k * BAR / 16, BAR / 16, 0.0, 0.5, 13.0, 6.0)
        add(LAND, BEAT, *COUNT_C, 4.0, 1.5)
        add(NOTE_IN, BEAT, *NOTE_C, 5.2, 0.7)
        add(SLIDE[0], SLIDE[1] - SLIDE[0], 0.0, 0.5, 13.0, 6.0)
        add(ANNOT, BEAT, ROW_A[0] + 1.6, ROW_A[1], 4.6, 1.2)
        add(STAMP, BEAT, ROW_B[0] + 1.6, ROW_B[1], 4.6, 1.5)
        add(RESULT, BEAT, ROW_C[0] + 1.7, ROW_C[1], 3.6, 0.5)
        for t, c in zip(HOLDS, HOLD_C):
            add(t, 0.3, *c, 1.9, 1.0)
        for k in range(6):                                    # the threads and the knot
            add(HOLDS[0] + k * BEAT, BEAT, 0.5, 0.3, 11.0, 5.0)

    def run(self):
        """Play the logged events in time order (each a Shot; overlapping ones share a play)."""
        self.log_events()
        self.shots = [(a, min(d, END - a), bx) for a, d, bx in self.shots if a < END - 1e-6]
        steps = sorted({round(t, 4) for t, _, _ in self.shots})
        for i, t in enumerate(steps):
            nxt = steps[i + 1] if i + 1 < len(steps) else END
            self.until(f"{t:.4f}s")
            active = [(a, d, bx) for a, d, bx in self.shots if a <= t + 1e-6 and a + d > t + 1e-6]
            if not active:
                continue
            end = min(nxt, max(a + d for a, d, _ in active))
            n = int(math.floor(end * self.fps + 1e-6)) - self.frame_index
            if n < 1:
                continue
            shots = [Shot(box(*bx)) for _, _, bx in active]
            self.play(*shots, run_time=n / self.fps)
            self.remove(*[s.mobject for s in shots])
        self.until(f"{END:.4f}s")
