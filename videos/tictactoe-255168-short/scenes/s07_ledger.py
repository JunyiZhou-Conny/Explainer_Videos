"""S07 · 255,168, explained 255,168 是怎么来的 — ★3, the ledger: the rings unroll into bars by end move, the bars
join into one line of 255,168, each segment drops a copy stretched by its ghost factor, and the copies join into
one line of 9! = 362,880. Then the games regroup by result: X, O, draws.

Bars 70-80 (2:45.6-3:12.0) of script.md; scene time 0 is the downbeat of bar 70 (a segue from S06). As in S01
(the reference scene) the picture is a pure function of the scene time, and the notes come from the same numbers
(Sounds). All 255,168 games are splatted into one light image per frame (common.Splatter): each point is one game
from 72.1 on, so the ledger's lengths ARE the counts, on one scale for the whole scene: 1 unit = 30,240 games or
orders (9! = 12 units), one screen unit each (UNIT_S).

    70-71  the galaxy, restored (S06's last frame); tiny labels "第 5 步 · MOVE 5" ... "第 9 步 · MOVE 9" land one
           per beat at the 12 o'clock end of rings 5-9 (70.1 ... 71.1); 71.2-71.4 the rings ease apart and the
           turn comes to rest                                                                  (c21, five notes)
    72-74  72.1-72.3 the circle is cut at 12 o'clock and every ring unrolls into a row 12 units long, move 5 on
           top, every game at its slot (the ghost gaps show); 72.3-73.1 the games slide left and close the gaps:
           bars of 1,440 · 5,328 · 47,952 · 72,576 · 127,872 games (the move-9 bar cyan, then grey); the labels
           land one per beat (73.1-74.1); 74.2-74.4 the bars slide end to end into one line, 8.44 units long;
           74.4 "Σ = 255,168" lands at its end                                              (bell, glass, wood)
    75-76  the ghosts come back as multipliers, one per beat: × 24, × 6, × 2, × 1, × 1 (75.1-76.1); each segment
           drops a copy to a second line, stretched by its factor (dashed grey ghost slots open between its games)
           and docked end to end; its label rolls to 34,560 · 31,968 · 95,904 · 72,576 · 127,872; 76.2-76.4
           hairlines join each segment to its stretched partner: five fans                (ghost grains, fifths)
    77-78  77.1 HIT: the bottom line locks at exactly 12 units, "= 362,880", and "9! · 9 的阶乘 · NINE FACTORIAL"
           docks under it: 255,168 games over 362,880 orders (c22); bar 78: a light runs along the top line, down
           the hairlines and along the bottom line
    79-80  79.1-79.2 the bottom line fades; 79.1-79.4 the top line's games regroup by colour, in place: X's
           wins | O's | the draws, on the same scale, with half of all games marked (X's bar runs just past it);
           80.1-80.3 "X 赢 131,184 · X WINS", "O 赢 77,904 · O WINS", "平局 46,080 · DRAWS" under them (c23: just
           over half); the half mark and Σ = 255,168 stay up with c23 (S08 fades them with the labels, 81.3)

Every length is exact and asserted: 1,440 + 5,328 + 47,952 + 72,576 + 127,872 = 255,168 games = 8.438 units; the
same rows x 24, 6, 2, 1, 1 = 34,560 + 31,968 + 95,904 + 72,576 + 127,872 = 362,880 = 12 units; 131,184 (4.34) +
77,904 (2.58) + 46,080 (1.52) = 255,168; 131,184 > 255,168 / 2.

Hand-over from S06 (a segue at 70.1): s06_turn.HANDOVER_S07 and S06's own drawing functions (galaxy_families,
render_light, show_plate, the edges), so the first frame here is S06's last.
Hand-over to S08 (a segue at 81.1). s08_bigger.S07Stage subclasses Ledger: it runs Ledger.build on a stand-in and
draws this scene's own objects with Ledger.update_state (and its light with update_light until 81.3) at S07 times
past END, so S08's first frame is S07's last whatever it holds; it also reads ledger_points(END) (every game's
screen place, weight W_GAME and colour family), SH_PH and the shimmer 1 + 0.12 sin(SH_PH + 2.3 t) (the games'
flight from 81.3), HANDOVER_S08 ("unit", "w_game", "rho_cut", and the layout keys) and ROOT_S / Z (where the galaxy
was cut). So keep build, update_state and update_light working without a renderer and for t > END. The last
frame: X's wins | O's | the draws side by side on the top line (HANDOVER_S08 x0, line_y, gap; a game at x0 + its
place / 30,240 screen units), their labels under them, the half mark over X's bar, Σ = 255,168 at the line's end,
the HUD §4 and the readout "Σ 255,168". The camera is S06's CAM_1, unchanged.
"""

from __future__ import annotations

import math

import numpy as np
from manim import Line, Mobject, Rectangle, Text, VGroup, VMobject, config

from explainer.short import (FONT_MONO, FONT_OLDSTYLE, BeatScene, INK, INK_DIM, RED, WHITE, RollingCounter,
                             cjk, hero_number, stroke_px, tracked)

from common import (GALAXY_COLOURS, GALAXY_LOOK, HUD_LINES_Y, HUD_RIGHT, NINE_FACT, OC, PEN_HALO, PITCH, XC, Cam, FastCamera,
                    FrameImage, HudLine, Pen, ProgramPlate, Shot, Sounds, Splatter, TREE_ROOT, W, bi_label, box,
                    clamp01, counter_glyphs, cull, ease_in_out_cubic, ease_in_out_sine, ease_out_cubic,
                    ease_out_quad, galaxy_tree, gaussian_sprite, lerp, pulse, rgb, ring_radius, section_hud, seg,
                    show_sprite, uncull)
from common import LeanInk as Ink
from common import LeanText as InkText
from s02_fill import Glyphs
from s04_by_hand import ZH_SIZE, MiniBoard, en, hex_of, line_affine, maths
from s06_turn import CAM_1, CAM_STILL, EDGES, HANDOVER_S07, PLATE_DIM, ROT_RATE, THIN, edge_ends, galaxy_families, \
    render_light, show_plate
from s06_turn import END as S06_END
from s06_turn import rho as s06_rho

# ---------------------------------------------------------------- the plan's clock
BEAT, BAR = 0.6, 2.4
FIRST = 70


def bb(bar: int, beat: float = 1.0) -> float:
    """Scene time of script.md's "bar.beat" (global bar numbers): bb(74, 2.5) is "74.2+"."""
    return (bar - FIRST) * BAR + (beat - 1) * BEAT


END = bb(81)                                      # 26.4 s: 11 bars

# ---------------------------------------------------------------- the games, and the ledger's numbers (asserted)
_T = galaxy_tree()
L_SLOT, L_K, L_RES, L_LAST = _T.l_slot, _T.l_k.astype(int), _T.l_res.astype(int), _T.l_last
L_CENTRE, L_JIT, L_WEIGHT, L_FAM = _T.l_centre, _T.l_jit, _T.l_weight, _T.l_fam
N_DEPTH, N_CENTRE, D_IDX = _T.n_depth, _T.n_centre, _T.dust
N = len(L_SLOT)
FACT = [math.factorial(9 - k) for k in range(10)]
KS = (5, 6, 7, 8, 9)
COUNT = {k: int((L_K == k).sum()) for k in KS}
assert COUNT == {5: 1_440, 6: 5_328, 7: 47_952, 8: 72_576, 9: 127_872} and sum(COUNT.values()) == 255_168 == N
STRETCHED = {k: COUNT[k] * FACT[k] for k in KS}
assert STRETCHED == {5: 34_560, 6: 31_968, 7: 95_904, 8: 72_576, 9: 127_872}
assert sum(STRETCHED.values()) == NINE_FACT == 362_880
X9, D9 = int(((L_K == 9) & (L_RES == 1)).sum()), int(((L_K == 9) & (L_RES == 3)).sum())
assert (X9, D9) == (81_792, 46_080)
RESULT = {1: int((L_RES == 1).sum()), 2: int((L_RES == 2).sum()), 3: int((L_RES == 3).sum())}
assert RESULT == {1: 131_184, 2: 77_904, 3: 46_080} and 2 * RESULT[1] > N      # X: just over half (51.4 %)
assert all(int((L_RES[L_K == k] == (1 if k % 2 else 2)).sum()) == COUNT[k] for k in (5, 6, 7, 8))  # odd: X, even: O

UNIT = 30_240                                     # games (or orders) per unit: 9! = 12 units
assert NINE_FACT == 12 * UNIT
UNIT_S = 1.0                                      # screen units per unit (the plan's: 9! = 12 units; S08 asserts it)
PG = UNIT_S / UNIT                                # screen units per game (or per slot)
RES_GAP = 0.08                                    # 79.4-: X | O | draws on the top line, this far apart
assert round(N / UNIT, 2) == 8.44 and [round(RESULT[r] / UNIT, 2) for r in (1, 2, 3)] == [4.34, 2.58, 1.52]
ROW_LEN = 12 * UNIT_S                             # 12: a ring unrolled (all 9! slots)
CUM_TOP = {}
CUM_BOT = {}
_a = _b = 0.0
for _k in KS:
    CUM_TOP[_k], CUM_BOT[_k] = _a, _b
    _a += COUNT[_k] * PG
    _b += STRETCHED[_k] * PG
TOP_LEN, BOT_LEN = _a, _b
assert abs(BOT_LEN - ROW_LEN) < 1e-9

# every game's place in each arrangement: rank in its row (the move-9 row: X wins first, then draws), the top
# line, the stretched copy, its result bar
_order = np.lexsort((L_SLOT, np.where(L_RES == 1, 0, 1), L_K))
RANK = np.empty(N, np.int64)
for _k in KS:
    _idx = _order[L_K[_order] == _k]
    RANK[_idx] = np.arange(len(_idx))
K_TOP = np.array([CUM_TOP.get(k, 0.0) for k in range(10)])
K_BOT = np.array([CUM_BOT.get(k, 0.0) for k in range(10)])
F_K = np.array(FACT, dtype=float)
TOP_OFF = K_TOP[L_K] + (RANK + 0.5) * PG          # along the top line (from its left end)
BOT_OFF = K_BOT[L_K] + (RANK * F_K[L_K] + 0.5) * PG
RRANK = np.empty(N, np.int64)
for _r in (1, 2, 3):
    _idx = np.flatnonzero(L_RES == _r)
    _idx = _idx[np.argsort(TOP_OFF[_idx], kind="stable")]
    RRANK[_idx] = np.arange(len(_idx))
RES_OFF = (RRANK + 0.5) * PG + np.array([0.0, 0.0, RESULT[1] * PG + RES_GAP,
                                        (RESULT[1] + RESULT[2]) * PG + 2 * RES_GAP])[L_RES]
PHI = 2 * np.pi * L_CENTRE / NINE_FACT            # clockwise from the seam (slot 0)
SH_PH = np.random.default_rng(70).uniform(0, 2 * np.pi, N)    # the shimmer's phase per game
FAMILY_OF = {1: 0, 2: 1, 3: 2}

# ---------------------------------------------------------------- places (screen units; the camera is S06's CAM_1)
CAM = CAM_STILL
CX, CY, CW = CAM_1
Z = W / CW                                        # 1.0
ROOT_S = CAM.to_screen(TREE_ROOT, 0.0)            # (-0.95, 0.24)
ROW_X = -5.4                                      # 72.3-74.1: the rows' left ends (labelled just above) ...
ROW_Y = {5: 2.05, 6: 1.45, 7: 0.85, 8: 0.25, 9: -0.35}  # ... move 5 on top
LINE_X = -5.4                                     # 74.4-: both lines (and the result bars) start here
Y_TOP, Y_BOT = 2.05, -0.6
LABEL_DY = -0.52                                  # ... their labels (S08's stacked zh / en) centred under them
ROW_LAB_DY = 0.29                                 # a row's label sits above its left end
RES_BARS = {r: (float(LINE_X + (RES_OFF[L_RES == r] - 0.5 * PG).min()),
                float(LINE_X + (RES_OFF[L_RES == r] + 0.5 * PG).max())) for r in (1, 2, 3)}
HALF_X = LINE_X + N * PG / 2                       # half of all games: X's bar ends just past it
assert RES_BARS[1][1] > HALF_X
COL_R = -4.0                                      # 70-71: the ring labels' right edge (outside ring 9)
COL_Y = {9: 2.73, 8: 2.39, 7: 2.05, 6: 1.71, 5: 1.37}
APART_K = 0.25                                    # 71.2-71.4: the rings move apart about ring 7
W_GAME = 0.055                                    # one game's light in the ledger (per 1080p pixel)
J_SCALE = 1.6                                     # the bars' thickness: the rings' radial jitter, upright, x 1.6

# ---------------------------------------------------------------- times
RING_LAB_T = {5: bb(70, 1), 6: bb(70, 2), 7: bb(70, 3), 8: bb(70, 4), 9: bb(71, 1)}
APART = (bb(71, 2), bb(72, 1))
UNROLL = (bb(72, 1), bb(72, 3))
CLOSE = (bb(72, 3), bb(73, 1))
COUNT_T = {5: bb(73, 1), 6: bb(73, 2), 7: bb(73, 3), 8: bb(73, 4), 9: bb(74, 1)}
JOIN = (bb(74, 2), bb(74, 4))
SIGMA_T = bb(74, 4)
MULT_T = {5: bb(75, 1), 6: bb(75, 2), 7: bb(75, 3), 8: bb(75, 4), 9: bb(76, 1)}
DROP = 0.5
FAN_T = {k: bb(76, 2) + 0.3 * j for j, k in enumerate(KS)}
FAN_DRAW = 0.35
HIT = bb(77, 1)
RUN_TOP = (bb(78, 1), bb(78, 2))
RUN_DOWN = 0.45
RUN_BOT = (bb(78, 3), bb(79, 1))
FADE_BOT = (bb(79, 1), bb(79, 2))
REGROUP = (bb(79, 1), bb(79, 4))
RES_LAB_T = {1: bb(80, 1), 2: bb(80, 2), 3: bb(80, 3)}
HUD_X = (0.0, BEAT / 2)                           # 70.1: §3 -> §4, GAMES COUNTED -> Σ
PLATE_OUT = (0.0, 0.3)

# ---------------------------------------------------------------- the galaxy's last turn (S06's, then at rest)
RHO_END6 = float(HANDOVER_S07["rho_end"])
assert abs(RHO_END6 - s06_rho(S06_END)) < 1e-12


def _speed(t: float) -> float:
    if t < APART[0]:
        return 1.0
    return 1.0 - ease_in_out_sine(seg(t, *APART))


_RT = np.linspace(0.0, UNROLL[0], 2001)
_RS = np.array([_speed(t) for t in _RT])
_RHO = RHO_END6 + ROT_RATE * np.concatenate([[0.0], np.cumsum(0.5 * (_RS[1:] + _RS[:-1]) * np.diff(_RT))])


def rho(t: float) -> float:
    return float(np.interp(t, _RT, _RHO))


RHO_CUT = rho(UNROLL[0])                          # where slot 0 (the seam) is when the circle is cut


def apart(t: float) -> float:
    return ease_in_out_sine(seg(t, *APART))


def ring_r(k, t: float):
    """World radius of ring k as the rings ease apart (rings 5-9 only)."""
    r = 2.9 * (np.asarray(k, dtype=float) / 9.0) ** 0.75
    return r + (r - ring_radius(7)) * APART_K * apart(t)


def seam_point(k: int, t: float) -> np.ndarray:
    """Screen point where ring k starts (slot 0, clockwise from 12 o'clock by the turn)."""
    a = rho(t)
    return ROOT_S + Z * float(ring_r(k, t)) * np.array([math.sin(a), math.cos(a)])


# ---------------------------------------------------------------- where every game is, at time t
def ribbon(phi, jit, R: float, P, A, a0: float, e: float):
    """The unrolling: a ring of radius R (screen) cut at P (heading clockwise, at angle a0 from 12 o'clock)
    straightens into a row from A, ROW_LEN long, as e goes 0 -> 1 (constant curvature (1 - e) / R, the cut end
    moving from P to A). phi: each point's angle from the cut; jit: its radial offset (screen)."""
    S = np.asarray(P, dtype=float) + (np.asarray(A, dtype=float) - np.asarray(P, dtype=float)) * e
    beta = -a0 * (1 - e)
    kap = (1 - e) / R
    L = 2 * np.pi * R + (ROW_LEN - 2 * np.pi * R) * e
    s = L * phi / (2 * np.pi)
    h = beta - kap * s
    if kap > 1e-6:
        x = S[0] + (math.sin(beta) - np.sin(h)) / kap
        y = S[1] + (np.cos(h) - math.cos(beta)) / kap
    else:
        x = S[0] + s * math.cos(beta)
        y = S[1] + s * math.sin(beta)
    return np.stack([x - jit * np.sin(h), y + jit * np.cos(h)], axis=-1), L


def ledger_points(t: float):
    """(screen xy (N, 2), weight (N,), colour family (N,)) of the 255,168 games from 72.1 on: the rows, the bars,
    the top line, the result bars (the copies are drawn apart)."""
    xy = np.empty((N, 2))
    w = np.full(N, W_GAME)
    fam = L_FAM.astype(np.int64).copy()
    jy = L_JIT * Z * J_SCALE
    if t < CLOSE[0]:                                 # the unroll
        e = ease_in_out_cubic(seg(t, *UNROLL))
        for k in KS:
            m = L_K == k
            R = Z * float(ring_r(k, UNROLL[0]))
            P = seam_point(k, UNROLL[0])
            pts, L = ribbon(PHI[m], L_JIT[m] * Z, R, P, (ROW_X, ROW_Y[k]), RHO_CUT, e)
            xy[m] = pts
            w[m] = L_WEIGHT[m] * Z * Z * (2 * np.pi * R / L)
        return xy, w, fam
    if t < JOIN[0]:                                  # the gaps close: solid bars
        e = ease_in_out_cubic(seg(t, *CLOSE))
        jy = L_JIT * Z * (1 + (J_SCALE - 1) * e)
        x_slot = ROW_X + ROW_LEN * PHI / (2 * np.pi)
        x_bar = ROW_X + (RANK + 0.5) * PG
        xy[:, 0] = x_slot + (x_bar - x_slot) * e
        xy[:, 1] = np.array([ROW_Y.get(k, 0.0) for k in range(10)])[L_K] + jy
        R = np.array([Z * float(ring_r(k, UNROLL[0])) if k >= 5 else 1.0 for k in range(10)])[L_K]
        w0 = L_WEIGHT * Z * Z * (2 * np.pi * R / ROW_LEN)
        w = w0 + (W_GAME - w0) * e
        return xy, w, fam
    row_y = np.array([ROW_Y.get(k, 0.0) for k in range(10)])[L_K]
    if t < REGROUP[0]:                               # the bars join into the top line
        e = ease_in_out_cubic(seg(t, *JOIN))
        xy[:, 0] = (ROW_X + (RANK + 0.5) * PG) + (LINE_X + TOP_OFF - ROW_X - (RANK + 0.5) * PG) * e
        xy[:, 1] = row_y + (Y_TOP - row_y) * e + jy
        return xy, w, fam
    # 79.1-79.4: they regroup by result, the left end first
    lag = 0.25 * TOP_OFF / TOP_LEN
    u = np.clip((t - REGROUP[0] - lag) / (REGROUP[1] - REGROUP[0] - 0.25), 0, 1)
    e = u * u * (3 - 2 * u)
    lift = 0.32 * np.sin(np.pi * e) * np.where(L_RES == 1, 1.0, np.where(L_RES == 2, -1.0, 0.6))
    xy[:, 0] = LINE_X + TOP_OFF + (RES_OFF - TOP_OFF) * e
    xy[:, 1] = Y_TOP + lift + jy                     # (the colours pass over and under each other)
    return xy, w, fam


def copy_points(k: int, t: float):
    """The stretched copy of segment k (75.1-): its games' screen xy and its progress e (0 at the top line)."""
    m = np.flatnonzero(L_K == k)
    e = ease_in_out_cubic(seg(t, MULT_T[k] + 0.05, MULT_T[k] + 0.05 + DROP))
    x = LINE_X + TOP_OFF[m] + (BOT_OFF[m] - TOP_OFF[m]) * e
    y = Y_TOP + (Y_BOT - Y_TOP) * e + L_JIT[m] * Z * J_SCALE
    return m, np.stack([x, y], axis=-1), e


def seg_ends(k: int, line: str):
    if line == "top":
        return LINE_X + CUM_TOP[k], LINE_X + CUM_TOP[k] + COUNT[k] * PG
    return LINE_X + CUM_BOT[k], LINE_X + CUM_BOT[k] + STRETCHED[k] * PG


# label places (screen): the counts above the top line (two tiers for the tiny segments, with leaders), the
# multipliers between the lines (inside each fan), the stretched counts under the bottom line
TIER1, TIER2 = Y_TOP + 0.42, Y_TOP + 0.77
TOP_LAB = {}                                      # filled in below: 5 and 6 left of the line, 7-9 over their segments
MULT_F = 0.705                                    # the multipliers sit this far down their fans
BOT_LAB_Y = Y_BOT - 0.36
N362_DY = -0.86                                   # = 362,880 under the bottom line's right end


def _top_labels():
    w = {k: (0.73 if k < 7 else 0.88) for k in (5, 6, 7, 8)}
    out = {5: (LINE_X - 0.1 - w[5] / 2, TIER1), 6: (LINE_X - 0.1 - w[6] / 2, TIER2)}
    for k in (7, 8, 9):
        a0, a1 = seg_ends(k, "top")
        out[k] = ((a0 + a1) / 2, TIER1)
    return out


def fan_point(k: int, f: float) -> np.ndarray:
    a0, a1 = seg_ends(k, "top")
    b0, b1 = seg_ends(k, "bot")
    return np.array([lerp((a0 + a1) / 2, (b0 + b1) / 2, f), lerp(Y_TOP, Y_BOT, f)])


TOP_LAB.update(_top_labels())
# what S08 reads (see the module docstring): the result bars X | O | draws on one line, each game at x0 + its place
# / unit (+ gap between bars), y line_y + its radial jitter x thick, weight bar_w (= w_game); the labels centred
# label_dy under each bar; the HUD: §4 and the readout "Σ 255,168"
HANDOVER_S08 = {"line_y": Y_TOP, "x0": LINE_X, "gap": RES_GAP, "unit": UNIT, "thick": J_SCALE * Z, "bar_w": W_GAME,
                "labels": ((f"X 赢 {RESULT[1]:,}", "X WINS"), (f"O 赢 {RESULT[2]:,}", "O WINS"),
                           (f"平局 {RESULT[3]:,}", "DRAWS")),
                "label_dy": LABEL_DY, "hud": "§4 · 255,168 是怎么来的 · 255,168, EXPLAINED", "readout": "Σ 255,168",
                "cam": CAM_1, "rho_cut": None, "bars": RES_BARS, "w_game": W_GAME}
assert UNIT_S == 1.0                              # (S08 places the games at x0 + place / 30,240 screen units)


# ---------------------------------------------------------------- the scene
class Ledger(BeatScene):

    def __init__(self, **kw):
        kw.setdefault("camera_class", FastCamera)
        super().__init__(**kw)

    def construct(self):
        self.sounds = Sounds()
        self.shots: list[tuple[float, float, tuple]] = []
        self.build()
        self.score()
        self.run()

    # ------------------------------------------------------------- objects
    def build(self):
        self.splat = Splatter(0.5)
        self.galaxy = FrameImage()
        self.root = MiniBoard(0.14, 0, 0, nums=0)
        self.edges = [Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.2) for _ in EDGES]
        # screen space
        self.plate = ProgramPlate()
        self.sec3 = section_hud("§3 · 探索每一局 · PLAY EVERY GAME")
        self.sec4 = section_hud("§4 · 255,168 是怎么来的 · 255,168, EXPLAINED")
        self.hud_games = HudLine("对局计数", "GAMES COUNTED", HUD_LINES_Y[0])
        # the readout "Σ 255,168" (S08's S07Stage draws it with this class, then fades it with §4)
        self.hud_sigma = HudLine("对局计数", "GAMES COUNTED", HUD_LINES_Y[0])
        sig = Text("Σ", font=FONT_OLDSTYLE, font_size=15, color=INK_DIM)
        sig.next_to(self.hud_sigma.counter.ref, np.array([-1, 0, 0]), buff=0.18)
        sig.align_to(self.hud_sigma.counter.columns[0][0], np.array([0, -1, 0]))
        self.hud_sigma.label = sig
        self.hud_sigma.lab_t = InkText(sig, INK_DIM)
        self.hud_sigma.lab_c = sig.get_center()[:2]
        self.hud_sigma.group.remove(self.hud_sigma.group[0])
        self.hud_sigma.group.add(self.hud_sigma.lab_t)
        self.pen = Pen()
        self.heads = [Pen(radius_px=3.5, halo_px=34) for _ in range(8)]
        # 70-71: the ring labels and their leaders
        self.ring_lab = {}
        for k in KS:
            lab = bi_label(f"第 {k} 步", f"MOVE {k}", zh_size=20, en_size=16.5, color=INK)
            lab[2].set_color(INK_DIM)
            parts = [InkText(p, col) for p, col in zip(lab, (INK, INK_DIM, INK_DIM))]
            offs = [p.get_center()[:2] - lab.get_center()[:2] for p in lab]
            self.ring_lab[k] = (parts, offs, lab.width, lab.height)
        self.leaders = {k: Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.0) for k in KS}
        # 73: the counts at the bars' ends; 74.2- above the top line, with leaders
        col = {5: XC.mid, 6: OC.mid, 7: XC.mid, 8: OC.mid}
        self.count_lab = {}
        for k in KS:
            if k < 9:
                m = Text(f"{COUNT[k]:,}", font=FONT_MONO, font_size=18, color=col[k])
                parts = [InkText(m, col[k])]
                offs = [np.zeros(2)]
                cols = [col[k]]
            else:
                a = Text(f"{X9:,}", font=FONT_MONO, font_size=18, color=XC.mid)
                p = Text("+", font=FONT_MONO, font_size=18, color=INK_DIM)
                b = Text(f"{D9:,}", font=FONT_MONO, font_size=18, color="#C8CCCC")
                g = VGroup(a, p, b).arrange(buff=0.14)
                parts = [InkText(x, c) for x, c in zip(g, (XC.mid, INK_DIM, "#C8CCCC"))]
                offs = [x.get_center()[:2] - g.get_center()[:2] for x in g]
                cols = [XC.mid, INK_DIM, "#C8CCCC"]
                m = g
            self.count_lab[k] = (parts, offs, cols, m.width, m.height)
        self.count_leaders = {k: Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.0) for k in KS}
        # 74.4: Σ = 255,168 (the title's halo: cool on the left, warm on the right)
        self.sigma_sym = InkText(Text("Σ", font=FONT_OLDSTYLE, font_size=34, color=INK), INK)
        self.sigma_eq = InkText(maths("=", size=34, color=INK), INK)
        t255 = hero_number("255,168", size=36)
        xs = np.array([g.get_center()[0] for g in t255])
        u = (xs - xs.min()) / (xs.max() - xs.min())
        self.n255 = Glyphs(t255, WHITE, INK, 10, layers=6, glow_opacity=0.55,
                           glow_colors=[hex_of(rgb(XC.glow) * (1 - v) + rgb(OC.mid) * v) for v in u])
        self.n255_w = t255.width
        self.halo255 = gaussian_sprite(None, 96, 0.34, gradient=(XC.glow, OC.mid), aspect=3.0)
        # 75-76: multipliers, the stretched counts, ghost dashes, the fans
        self.mult = {k: InkText(maths(f"× {FACT[k]}", size=28, color=INK), INK) for k in KS}
        self.bot_cnt = {}
        for k in KS:
            c = RollingCounter(COUNT[k], digits=6, size=17, font=FONT_MONO, weight="NORMAL",
                               color=col.get(k, XC.mid))
            c.clear_updaters()
            self.bot_cnt[k] = c
        self.dashes = {k: VMobject().set_stroke(INK_DIM, width=stroke_px(1.6), opacity=0).set_fill(opacity=0)
                       for k in (5, 6, 7)}
        for d in self.dashes.values():
            d.points = np.zeros((0, 3))
        self.fan_lines = [Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.2) for _ in range(6)]
        self.fan_fill = {k: VMobject().set_stroke(width=0).set_fill(XC.glow if k % 2 else OC.mid, opacity=0)
                         for k in KS}
        for f in self.fan_fill.values():
            f.set_points_as_corners([[0, 0, 0], [0.01, 0, 0], [0, 0.01, 0], [0, 0, 0]])
        self.end_ticks = [Ink(Line([0, -0.5, 0], [0, 0.5, 0]), INK, 1.4) for _ in range(4)]
        # 77.1: = 362,880 and 9! · 9 的阶乘 · NINE FACTORIAL
        self.eq362 = InkText(maths("=", size=34, color=INK), INK)
        t362 = hero_number("362,880", size=36)
        self.n362 = Glyphs(t362, WHITE, INK, 10, layers=6, glow_opacity=0.5)
        self.n362_w = t362.width
        self.halo362 = gaussian_sprite(PEN_HALO, 96, 0.34, aspect=3.0)
        nine = VGroup(maths(f"9{THIN}!", size=28, color=INK_DIM), cjk("·", size=20, color=INK_DIM),
                      bi_label("9 的阶乘", "NINE FACTORIAL", zh_size=20, en_size=16.5, color=INK_DIM)).arrange(buff=0.14)
        self.nine = InkText(nine, INK_DIM)
        self.nine_w = nine.width
        # 79-80: the half of all games marked on the line, the result labels (S08 draws them with this class, through
        # s08_bigger.S07Stage). (ruler and half_line are kept from an earlier interface; they are not drawn.)
        self.ruler = Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.3)
        self.ruler_ticks = [Ink(Line([0, -0.5, 0], [0, 0.5, 0]), INK_DIM, 1.3) for _ in range(3)]
        self.half_line = VMobject().set_stroke(INK_DIM, width=stroke_px(1.2), opacity=0).set_fill(opacity=0)
        self.half_line.points = np.zeros((0, 3))
        self.half_lab = InkText(maths("½", size=26, color=INK_DIM), INK_DIM)
        self.res_lab = {}
        for r, (zh, en_) in {1: (f"X 赢 {RESULT[1]:,}", "X WINS"), 2: (f"O 赢 {RESULT[2]:,}", "O WINS"),
                             3: (f"平局 {RESULT[3]:,}", "DRAWS")}.items():
            lab = bi_label(zh, en_, zh_size=20, en_size=16.5, color=INK)
            lab[2].set_color(INK_DIM)
            parts = [InkText(p, c) for p, c in zip(lab, (INK, INK_DIM, INK_DIM))]
            offs = [p.get_center()[:2] - lab.get_center()[:2] for p in lab]
            self.res_lab[r] = (parts, offs, lab.width)

        self.clock_mob = Mobject()
        self.clock_mob.add_updater(lambda mob: self.update_state(self.clock()))
        self.add(self.clock_mob, self.camera.frame)
        self.add(self.galaxy, *self.edges, self.root.group)
        fixed = [self.plate.group, *[p for k in KS for p in self.ring_lab[k][0]], *self.leaders.values(),
                 *self.fan_fill.values(), *self.fan_lines, *self.dashes.values(), *self.end_ticks,
                 self.ruler, *self.ruler_ticks, self.half_line, self.half_lab,
                 *[p for k in KS for p in self.count_lab[k][0]], *self.count_leaders.values(),
                 *self.mult.values(), *self.bot_cnt.values(), self.halo255, self.sigma_sym, self.sigma_eq,
                 self.n255, self.halo362, self.eq362, self.n362, self.nine,
                 *[p for r in (1, 2, 3) for p in self.res_lab[r][0]], self.pen, *self.heads, self.sec3, self.sec4,
                 self.hud_games.group, self.hud_sigma.group]
        self.fix(*fixed)
        self.update_state(0.0)

    # ------------------------------------------------------------- the picture at time t
    def update_state(self, t: float):
        self.camera.frame.set(width=CW)
        self.camera.frame.move_to([CX, CY, 0])
        self.galaxy.move_to([CX, CY, 0])
        self.update_light(t)
        self.update_tree_lines(t)
        self.update_plate_hud(t)
        self.update_ring_labels(t)
        self.update_counts(t)
        self.update_sigma(t)
        self.update_copies_ui(t)
        self.update_362(t)
        self.update_results(t)
        self.update_heads(t)

    # --- the light: the galaxy (70-72.1), then the ledger's points
    def update_light(self, t: float):
        sp = self.splat
        if t < UNROLL[0]:
            rh = rho(t)
            a = apart(t)
            if a <= 1e-6:
                self.galaxy.light = render_light(sp, galaxy_families(sp, t, CAM, rh), **GALAXY_LOOK)
                return
            self.galaxy.light = render_light(sp, self.galaxy_apart(t, rh), **GALAXY_LOOK)
            return
        fams = [[None, GALAXY_COLOURS[f]] for f in range(4)]

        def add(f, xy, w):
            img = sp.accumulate(xy, w)
            fams[f][0] = img if fams[f][0] is None else fams[f][0] + img
        xy, w, fam = ledger_points(t)
        shimmer = 1 + 0.12 * np.sin(SH_PH + 2.3 * t) * seg(t, CLOSE[0], CLOSE[1])
        w = w * shimmer
        w = w * self.run_glow(t, xy, "top")
        for f in range(3):
            sel = fam == f
            add(f, xy[sel], w[sel])
        # the dust and the inner rings fade as the circle is cut
        dv = 1 - ease_in_out_sine(seg(t, UNROLL[0], UNROLL[0] + 0.5))
        if dv > 1e-3:
            DP = self.dust_points(UNROLL[0])
            dw = _T.dust_w * self.dust_w0 * dv
            add(3, DP, dw)
        # the stretched copies (75.1-79.2)
        fade = 1 - ease_in_out_sine(seg(t, *FADE_BOT))
        lock = 1 + 1.4 * pulse(t, HIT, 0.5)
        for k in KS:
            if t < MULT_T[k] + 0.05 or fade <= 1e-3:
                continue
            m, cxy, e = copy_points(k, t)
            cw = np.full(len(m), W_GAME * fade * lock) * (1 + 0.12 * np.sin(SH_PH[m] + 2.3 * t))
            cw = cw * self.run_glow(t, cxy, "bot")
            f = int(L_FAM[m[0]]) if k < 9 else None
            if k < 9:
                add(f, cxy, cw)
            else:
                for ff in (0, 2):
                    sel = L_FAM[m] == ff
                    add(ff, cxy[sel], cw[sel])
            if 0.02 < e < 0.98:                          # a fast move: two blur copies
                for lag, lw in ((0.02, 0.3), (0.04, 0.12)):
                    _, bxy, _ = copy_points(k, t - lag)
                    if k < 9:
                        add(f, bxy, cw * lw)
                    else:
                        for ff in (0, 2):
                            sel = L_FAM[m] == ff
                            add(ff, bxy[sel], cw[sel] * lw)
        self.galaxy.light = render_light(sp, [tuple(f) for f in fams], **GALAXY_LOOK)

    def galaxy_apart(self, t: float, rh: float):
        """S05's galaxy with rings 5-9 eased apart about ring 7 (71.2-71.4)."""
        sp = self.splat
        out = []
        r = ring_r(L_K, t) + L_JIT
        th = PHI + rh
        P = np.stack([TREE_ROOT[0] + r * np.sin(th), TREE_ROOT[1] + r * np.cos(th)], axis=-1)
        S = CAM.to_screen(P, t)
        wts = L_WEIGHT * Z * Z
        for f in range(3):
            sel = L_FAM == f
            out.append((sp.accumulate(S[sel], wts[sel]), GALAXY_COLOURS[f]))
        out.append((sp.accumulate(self.dust_points(t), _T.dust_w * self.dust_w0), GALAXY_COLOURS[3]))
        return out

    @property
    def dust_w0(self):
        from common import GALAXY_DUST_W
        return GALAXY_DUST_W[N_DEPTH[D_IDX]] * Z * Z

    def dust_points(self, t: float) -> np.ndarray:
        d = N_DEPTH[D_IDX].astype(float)
        r = 2.9 * (d / 9.0) ** 0.75
        r = np.where(d >= 5, r + (r - ring_radius(7)) * APART_K * apart(t), r)
        th = 2 * np.pi * N_CENTRE[D_IDX] / NINE_FACT + rho(t)
        P = np.stack([TREE_ROOT[0] + r * np.sin(th), TREE_ROOT[1] + r * np.cos(th)], axis=-1)
        return CAM.to_screen(P, t)

    def run_glow(self, t: float, xy: np.ndarray, line: str) -> np.ndarray:
        """Bar 78: the light running along the top line, then the bottom line (a brightness bump at its head)."""
        if not (RUN_TOP[0] <= t < RUN_BOT[1] + 0.4):
            return 1.0
        if line == "top":
            u = seg(t, *RUN_TOP)
            hx = LINE_X + TOP_LEN * ease_in_out_sine(u)
            amp = 2.2 * (1 - seg(t, RUN_TOP[1], RUN_TOP[1] + 0.4)) * seg(t, RUN_TOP[0], RUN_TOP[0] + 0.1)
            near = np.abs(xy[:, 1] - Y_TOP) < 0.2
        else:
            u = seg(t, *RUN_BOT)
            hx = LINE_X + BOT_LEN * ease_in_out_sine(u)
            amp = 2.2 * seg(t, RUN_BOT[0], RUN_BOT[0] + 0.1) * (1 - seg(t, RUN_BOT[1], RUN_BOT[1] + 0.4))
            near = np.abs(xy[:, 1] - Y_BOT) < 0.2
        return 1 + amp * near * np.exp(-((xy[:, 0] - hx) / 0.35) ** 2)

    # --- the tree's lines (S06's edges, the root board), the pen; gone as the circle is cut
    def update_tree_lines(self, t: float):
        v = 1 - ease_in_out_sine(seg(t, UNROLL[0], UNROLL[0] + 0.4))
        rh = rho(t)
        for e, ink in zip(EDGES, self.edges):
            if v <= 1e-3:
                ink.hide()
                continue
            p, q = edge_ends(e, rh)
            A, c = line_affine(p, q)
            ink.show(1.0, A, c, vis=0.38 * v, width=1.0 / Z)
        self.root.place(TREE_ROOT, 1.0)
        if v <= 1e-3:
            self.root.hide()
        else:
            self.root.draw_grid(1.0, vis=v, width=1.0 / Z)
        self.pen.place(ROOT_S, 0.9 * v)

    def update_plate_hud(self, t: float):
        pv = PLATE_DIM * (1 - ease_in_out_sine(seg(t, *PLATE_OUT)))
        show_plate(self.plate, pv, [pv] * len(self.plate.rows), {}, None, HANDOVER_S07["plate_scale"])
        x = ease_in_out_sine(seg(t, *HUD_X))
        if abs(x - getattr(self, "_hx", -1)) > 1e-4:
            for p in self.sec3.get_family():
                if len(p.points):
                    p.set_fill(opacity=1 - x)
            for p in self.sec4.get_family():
                if len(p.points):
                    p.set_fill(opacity=x)
            self._hx = x
        self.hud_games.show(N, 1 - x)
        self.hud_sigma.show(N, x)

    # --- 70-74: the ring labels (at the seam, with leaders; then with their rows)
    def update_ring_labels(self, t: float):
        e = ease_in_out_cubic(seg(t, *UNROLL))
        out = 1 - ease_in_out_sine(seg(t, JOIN[0], JOIN[0] + 0.4))
        for k in KS:
            parts, offs, lw, lh = self.ring_lab[k]
            v = ease_out_cubic(seg(t, RING_LAB_T[k], RING_LAB_T[k] + 0.35)) * out
            ld = self.leaders[k]
            if v <= 1e-3:
                for p in parts:
                    p.hide()
                ld.hide()
                continue
            c0 = np.array([COL_R - lw / 2, COL_Y[k]])
            c1 = np.array([ROW_X + lw / 2, ROW_Y[k] + ROW_LAB_DY])
            c = c0 + (c1 - c0) * e + np.array([0.08 * (1 - ease_out_cubic(seg(t, RING_LAB_T[k], RING_LAB_T[k] + 0.35))), 0])
            v = v * abs(1 - 2 * e) ** 1.5                  # the labels cross as the rows re-stack: gone mid-way
            for p, off, col in zip(parts, offs, (INK, INK_DIM, INK_DIM)):
                p.show(c + off, vis=v, color=col)
            # the leader: from the label to its ring's seam (drawn as the label lands), shrinking into the row
            lv = v * (1 - ease_in_out_sine(seg(t, UNROLL[0], UNROLL[0] + 0.6)))
            if lv <= 1e-3:
                ld.hide()
                continue
            a = np.array([c[0] + lw / 2 + 0.08, c[1]])
            b = seam_point(k, min(t, UNROLL[0])) if t < UNROLL[0] else \
                np.asarray(seam_point(k, UNROLL[0])) + (np.array([ROW_X, ROW_Y[k]]) - seam_point(k, UNROLL[0])) * e
            A, cc = line_affine(a, b)
            ld.show(ease_out_cubic(seg(t, RING_LAB_T[k] + 0.1, RING_LAB_T[k] + 0.5)), A, cc, vis=0.55 * lv)

    # --- 73-79: the counts (at the bars' ends, then above the top line)
    def update_counts(self, t: float):
        out = 1 - ease_in_out_sine(seg(t, REGROUP[0], REGROUP[0] + 0.4))
        j = ease_in_out_cubic(seg(t, *JOIN))
        for k in KS:
            parts, offs, cols, lw, lh = self.count_lab[k]
            v = ease_out_cubic(seg(t, COUNT_T[k], COUNT_T[k] + 0.3)) * out
            ld = self.count_leaders[k]
            if v <= 1e-3:
                for p in parts:
                    p.hide()
                ld.hide()
                continue
            end = ROW_X + COUNT[k] * PG
            c0 = np.array([end + 0.14 + lw / 2, ROW_Y[k]]) + np.array([0.06 * (1 - v), 0])
            c1 = np.array(TOP_LAB[k])
            c = c0 + (c1 - c0) * j
            for p, off, col in zip(parts, offs, cols):
                p.show(c + off, vis=v, color=col)
            lv = v * j
            if lv <= 1e-3:
                ld.hide()
                continue
            a0, a1 = seg_ends(k, "top")
            if k in (5, 6):                               # from the label's right edge to its stub
                a = np.array([c[0] + lw / 2 + 0.06, c[1] - 0.02])
                b = np.array([(a0 + a1) / 2 + (0.0 if k == 5 else 0.02), Y_TOP + 0.07])
            else:
                a = np.array([c[0], c[1] - lh / 2 - 0.05])
                b = np.array([(a0 + a1) / 2, Y_TOP + 0.06])
            A, cc = line_affine(a, b)
            ld.show(1.0, A, cc, vis=0.5 * lv)

    def update_sigma(self, t: float):
        v = ease_out_cubic(seg(t, SIGMA_T, SIGMA_T + 0.3))
        if v <= 1e-3:
            for m in (self.sigma_sym, self.sigma_eq):
                m.hide()
            self.n255.hide()
            show_sprite(self.halo255, opacity=0)
            return
        x0 = LINE_X + TOP_LEN + 0.28 + 2 * RES_GAP * ease_in_out_cubic(seg(t, *REGROUP))
        y = Y_TOP
        breathe = 1 + 0.1 * math.sin(2 * math.pi * (t - SIGMA_T) / BAR)
        self.sigma_sym.show([x0 + 0.12, y + 0.02], vis=v, color=INK)
        self.sigma_eq.show([x0 + 0.48, y], vis=v, color=INK)
        nc = np.array([x0 + 0.72 + self.n255_w / 2, y - 0.04 * (1 - v)])
        self.n255.show(nc, vis=v, glow=(0.85 + 1.4 * pulse(t, SIGMA_T, 0.5)) * breathe)
        show_sprite(self.halo255, nc, 3.4, 1.15, 0.38 * v)

    # --- 75-79: multipliers, stretched counts, ghost dashes, fans, end ticks
    def update_copies_ui(self, t: float):
        fade = 1 - ease_in_out_sine(seg(t, *FADE_BOT))
        for k in KS:
            mt = MULT_T[k]
            v = ease_out_cubic(seg(t, mt, mt + 0.25)) * fade
            mm = self.mult[k]
            if v <= 1e-3:
                mm.hide()
            else:
                e = ease_in_out_cubic(seg(t, mt + 0.05, mt + 0.05 + DROP))
                c = fan_point(k, e) + np.array([0.0, lerp(-0.3, 0.34, ease_in_out_sine(e))])
                mm.show(c, vis=v, color=INK)
            # the stretched count under the bottom line, rolling as the copy stretches
            cnt = self.bot_cnt[k]
            gl = counter_glyphs(cnt)
            uncull(gl)
            e = ease_in_out_cubic(seg(t, mt + 0.05, mt + 0.05 + DROP))
            cv = ease_out_cubic(seg(t, mt + 0.2, mt + 0.45)) * fade
            b0, b1 = seg_ends(k, "bot")
            cnt.ref.move_to([(b0 + b1) / 2, BOT_LAB_Y, 0])
            cnt.value.set_value(COUNT[k] + (STRETCHED[k] - COUNT[k]) * e)
            cnt.layout()
            colk = XC.mid if (k % 2 or k == 9) else OC.mid
            for colm in cnt.columns:
                for g in colm:
                    g.set_fill(colk, opacity=g.get_fill_opacity() * cv)
            for _, sep in cnt.separators:
                sep.set_fill(colk, opacity=sep.get_fill_opacity() * cv)
            cull(gl)
            # the ghost slots of copies 5-7: dashes along the stretched copy
            if k in self.dashes:
                d = self.dashes[k]
                dv = 0.35 * e * fade * (1 - 1 / FACT[k]) / (1 - 1 / 24)
                if dv <= 1e-3 or t < mt:
                    d.points = np.zeros((0, 3))
                    d.set_stroke(opacity=0)
                else:
                    a0, a1 = seg_ends(k, "top")
                    x0 = lerp(a0, b0, e)
                    x1 = lerp(a1, b1, e)
                    y = lerp(Y_TOP, Y_BOT, e) - 0.075
                    n = max(1, int((x1 - x0) / 0.07))
                    xs = np.linspace(x0, x1, n + 1)
                    pts = []
                    for i in range(n):
                        p, q = np.array([xs[i], y, 0]), np.array([xs[i] + 0.55 * (xs[i + 1] - xs[i]), y, 0])
                        pts += [p, p + (q - p) / 3, p + 2 * (q - p) / 3, q]
                    d.points = np.array(pts)
                    d.set_stroke(INK_DIM, width=stroke_px(1.6), opacity=clamp01(dv))
        # the fans: hairlines from each top segment's ends to its partner's (76.2-76.4)
        bounds_top = [LINE_X + CUM_TOP[k] for k in KS] + [LINE_X + TOP_LEN]
        bounds_bot = [LINE_X + CUM_BOT[k] for k in KS] + [LINE_X + BOT_LEN]
        for j, ink in enumerate(self.fan_lines):
            t0 = FAN_T[KS[max(0, j - 1)]] if j > 0 else FAN_T[5]          # (boundary j closes fan j - 1)
            f = ease_out_quad(seg(t, t0, t0 + FAN_DRAW))
            if f <= 1e-3 or fade <= 1e-3:
                ink.hide()
                continue
            a = np.array([bounds_top[j], Y_TOP - 0.06])
            b = np.array([bounds_bot[j], Y_BOT + 0.06])
            A, c = line_affine(a, b)
            ink.show(f, A, c, vis=clamp01(0.6 * fade * (1 + 0.65 * self.down_glow(t, j))), width=1.0)
        for k in KS:
            ff = self.fan_fill[k]
            f = ease_in_out_sine(seg(t, FAN_T[k] + 0.2, FAN_T[k] + 0.7)) * fade
            if f <= 1e-3:
                ff.set_fill(opacity=0)
                continue
            a0, a1 = seg_ends(k, "top")
            b0, b1 = seg_ends(k, "bot")
            yt, yb = Y_TOP - 0.06, Y_BOT + 0.06
            ff.set_points_as_corners([[a0, yt, 0], [a1, yt, 0], [b1, yb, 0], [b0, yb, 0], [a0, yt, 0]])
            ff.set_fill(opacity=0.035 * f * (1 + 0.5 * pulse(t, HIT, 0.6)))
        # 77.1: the bottom line locks at exactly 12 units: ticks at both ends of both lines
        tv = ease_out_cubic(seg(t, HIT, HIT + 0.3)) * fade
        ends = [(LINE_X, Y_BOT), (LINE_X + BOT_LEN, Y_BOT), (LINE_X, Y_TOP), (LINE_X + TOP_LEN, Y_TOP)]
        for (x, y), ink in zip(ends, self.end_ticks):
            if tv <= 1e-3:
                ink.hide()
                continue
            ink.show(1.0, np.array([[1.0, 0.0], [0.0, 0.26]]), np.array([x + (-0.03 if x == LINE_X else 0.03), y]),
                     vis=0.8 * tv)

    def down_glow(self, t: float, j: int) -> float:
        """Bar 78: the light running down hairline j (from when the top run passes its top end)."""
        bounds_top = [LINE_X + CUM_TOP[k] for k in KS] + [LINE_X + TOP_LEN]
        u0 = (bounds_top[j] - LINE_X) / TOP_LEN
        t0 = RUN_TOP[0] + (RUN_TOP[1] - RUN_TOP[0]) * self._inv_ease(u0)
        if not (t0 <= t < t0 + RUN_DOWN + 0.3):
            return 0.0
        return math.sin(math.pi * seg(t, t0, t0 + RUN_DOWN + 0.3))

    @staticmethod
    def _inv_ease(u: float) -> float:
        """The time fraction at which ease_in_out_sine reaches u."""
        return math.acos(1 - 2 * clamp01(u)) / math.pi

    def update_362(self, t: float):
        fade = 1 - ease_in_out_sine(seg(t, *FADE_BOT))
        v = ease_out_cubic(seg(t, HIT, HIT + 0.3)) * fade
        if v <= 1e-3:
            self.eq362.hide()
            self.n362.hide()
            self.nine.hide()
            show_sprite(self.halo362, opacity=0)
            return
        right = LINE_X + BOT_LEN - 0.02                    # under the bottom line's right end (it fills the width)
        y = Y_BOT + N362_DY
        breathe = 1 + 0.1 * math.sin(2 * math.pi * (t - HIT) / BAR)
        nc = np.array([right - self.n362_w / 2, y - 0.04 * (1 - v)])
        self.eq362.show([nc[0] - self.n362_w / 2 - 0.26, y], vis=v, color=INK)
        self.n362.show(nc, vis=v, glow=(0.85 + 1.6 * pulse(t, HIT, 0.5)) * breathe)
        show_sprite(self.halo362, nc, 3.3, 1.1, 0.34 * v)
        nv = ease_out_cubic(seg(t, HIT + 0.15, HIT + 0.6)) * fade
        self.nine.show([right - self.nine_w / 2, y - 0.5 - 0.12 * (1 - nv)], vis=nv, color=INK_DIM)

    # --- 79-80: the half mark and the result labels
    def update_results(self, t: float):
        """79-80: half of all games marked on the line (X's bar runs just past it), the labels under the bars
        (80.1-80.3, zh over en). They stay up with c23 into S08, which draws them with this class (S07Stage)
        and fades them at 81.3."""
        hv = ease_in_out_sine(seg(t, REGROUP[1] - 0.3, REGROUP[1] + 0.3))
        tick = self.ruler_ticks[1]
        self.ruler.hide()
        for k in (self.ruler_ticks[0], self.ruler_ticks[2]):
            k.hide()
        self.half_line.points = np.zeros((0, 3))
        if hv <= 1e-3:
            tick.hide()
            self.half_lab.hide()
        else:
            g = 1 + 1.4 * pulse(t, RES_LAB_T[1], 0.5)
            tick.show(1.0, np.array([[1.0, 0.0], [0.0, 0.42]]), np.array([HALF_X, Y_TOP]), vis=clamp01(0.9 * hv * g),
                      width=1.2)
            self.half_lab.show([HALF_X, Y_TOP + 0.4], vis=hv, color=INK_DIM)
        for r in (1, 2, 3):
            parts, _, _ = self.res_lab[r]
            v = ease_out_cubic(seg(t, RES_LAB_T[r], RES_LAB_T[r] + 0.35))
            parts[1].hide()                                # (the bi_label's dot: the label is set on two lines)
            if v <= 1e-3:
                parts[0].hide()
                parts[2].hide()
                continue
            x0, x1 = RES_BARS[r]
            cx, y = (x0 + x1) / 2, Y_TOP + LABEL_DY - 0.06 * (1 - v)
            parts[0].show([cx, y + 0.14], vis=v, color=INK)
            parts[2].show([cx, y - 0.17], vis=v, color=INK_DIM)

    def update_heads(self, t: float):
        """Bar 78: the running light's heads (screen-space pens): along the top, down each hairline, along the
        bottom."""
        hs = self.heads
        for h in hs:
            h.place((0, 0), 0)
        if RUN_TOP[0] <= t < RUN_TOP[1] + 0.05:
            u = ease_in_out_sine(seg(t, *RUN_TOP))
            hs[0].place((LINE_X + TOP_LEN * u, Y_TOP), 0.9 * seg(t, RUN_TOP[0], RUN_TOP[0] + 0.08))
        bounds_top = [LINE_X + CUM_TOP[k] for k in KS] + [LINE_X + TOP_LEN]
        bounds_bot = [LINE_X + CUM_BOT[k] for k in KS] + [LINE_X + BOT_LEN]
        for j in range(6):
            u0 = (bounds_top[j] - LINE_X) / TOP_LEN
            t0 = RUN_TOP[0] + (RUN_TOP[1] - RUN_TOP[0]) * self._inv_ease(u0)
            if t0 <= t < t0 + RUN_DOWN:
                f = ease_in_out_sine(seg(t, t0, t0 + RUN_DOWN))
                p = np.array([lerp(bounds_top[j], bounds_bot[j], f), lerp(Y_TOP - 0.06, Y_BOT + 0.06, f)])
                hs[1 + j].place(p, 0.75 * math.sin(math.pi * min(1.0, f * 1.15 + 0.08)))
        if RUN_BOT[0] <= t < RUN_BOT[1] + 0.05:
            u = ease_in_out_sine(seg(t, *RUN_BOT))
            hs[7].place((LINE_X + BOT_LEN * u, Y_BOT), 0.9 * (1 - seg(t, RUN_BOT[1] - 0.1, RUN_BOT[1] + 0.05)))

    # ------------------------------------------------------------- the sounds (from the same numbers)
    def score(self):
        S = self.sounds
        # 70.1-71.1: five soft notes for the ring labels, rising (Asus4)
        S.phrase("ring labels", [(RING_LAB_T[k], f"glass@{n}", COL_R - 1.1)
                                 for k, n in zip(KS, ("A4", "B4", "D5", "E5", "A5"))], gain=0.42)
        # 72.1: the cut and the unroll (a shimmer); 72.3-73.1 the games slide left (falling grains)
        S.effect(UNROLL[0], "shimmer", 1.4, 0.0)
        S.phrase("close", [(CLOSE[0] + 0.15 * j, f"glass@{n}", lerp(4.0, -3.0, j / 7))
                           for j, n in enumerate(("B5", "A5", "F#5", "E5", "C#5", "B4", "A4", "F#4"))], gain=0.25)
        # 73.1-74.1: one note per label: X a bell, O glass, the draws a wooden pluck
        S.phrase("counts", [(COUNT_T[5], "X@C#5", ROW_X), (COUNT_T[6], "O@E5", ROW_X), (COUNT_T[7], "X@F#5", -2.6),
                            (COUNT_T[8], "O@A5", -1.9), (COUNT_T[9], "X@B5", 0.0)], gain=0.7)
        S.phrase("draws", [(COUNT_T[9] + 0.02, "draw@E5", 1.0)], gain=0.6)
        S.phrase("join", [(JOIN[0] + 0.3 * j, f"pluck@{n}", lerp(-4.0, 0.0, j / 3))
                          for j, n in enumerate(("G#3", "B3", "E4", "G#4"))], gain=0.35)
        S.phrase("sigma", [(SIGMA_T, "bell@E5", 2.2), (SIGMA_T + 0.06, "bell@B5", 3.2)], gain=0.55)
        # 75.1-76.1: each multiplier a flurry of N ghost grains (24, 6, 2, 1, 1) and one note of S02's fifths stack
        ghost_notes = ["D4", "E4", "F#4", "G#4", "A4", "B4", "C#5", "D5", "E5", "F#5", "G#5", "A5"]
        for k, n in zip(KS, ("D4", "A4", "E5", "B5", "F#6")):
            f = FACT[k]
            span = min(0.5, 0.02 * f) if f > 1 else 0.0
            x = float(fan_point(k, 0.0)[0])
            S.phrase(f"ghosts {k}", [(MULT_T[k] + (span * j / max(1, f - 1) if f > 1 else 0.0),
                                       f"ghost@{ghost_notes[(j * 5 + k) % len(ghost_notes)]}", x) for j in range(f)],
                     gain=0.32)
            S.phrase(f"fifth {k}", [(MULT_T[k], f"bell@{n}", x)], gain=0.5)
        S.phrase("fans", [(FAN_T[k], f"pluck@{n}", float(fan_point(k, 0.5)[0]))
                          for k, n in zip(KS, ("F#4", "A4", "B4", "D5", "F#5"))], gain=0.35)
        # 77.1: = 362,880 (a rolled Dmaj9 under the boom and the resolve); 9! docks
        S.phrase("lock", [(HIT + 0.05 + 0.08 * i, f"bell@{n}", 4.0 + 0.4 * i)
                          for i, n in enumerate(("D5", "F#5", "A5", "C#6", "E6"))], gain=0.5)
        S.phrase("nine", [(HIT + 0.15, "pluck@A4", 4.0)], gain=0.4)
        # bar 78: the light runs along, down and along (glass, rising then falling)
        run = [(RUN_TOP[0] + 0.15 * j, f"glass@{n}", lerp(LINE_X, LINE_X + TOP_LEN, j / 3))
               for j, n in enumerate(("D5", "E5", "F#5", "A5"))]
        run += [(RUN_TOP[1] + 0.05, "glass@C#6", -3.0)]
        run += [(RUN_BOT[0] + 0.3 * j, f"glass@{n}", lerp(LINE_X, LINE_X + BOT_LEN, j / 3))
                for j, n in enumerate(("A5", "F#5", "E5", "D5"))]
        S.phrase("run", run, gain=0.32)
        # 79.1: the regroup (a shimmer); 80.1-80.3: a bell, a glass tone and a wooden pluck for the results
        S.effect(REGROUP[0], "shimmer", 1.6, -2.0)
        S.phrase("results", [(RES_LAB_T[1], "X@B4", -1.0), (RES_LAB_T[2], "O@G#4", -2.4),
                             (RES_LAB_T[3], "draw@E4", -3.2)], gain=0.65)
        S.log(self)

    # ------------------------------------------------------------- the logged events and the clock
    def log_events(self):
        ev = self.shots

        def add(t, dur, x, y, w, h):
            ev.append((float(t), float(dur), (x, y, w, h)))
        for k in KS:
            add(RING_LAB_T[k], BEAT, COL_R - 1.1, COL_Y[k], 2.3, 0.3)
        for j in range(3):
            add(APART[0] + j * BEAT, BEAT, *ROOT_S, 6.0, 6.0)
        add(UNROLL[0], UNROLL[1] - UNROLL[0], 0.0, 0.8, 12.0, 6.0)
        add(CLOSE[0], CLOSE[1] - CLOSE[0], 0.0, 1.0, 9.6, 2.6)
        for k in KS:
            add(COUNT_T[k], BEAT, ROW_X + COUNT[k] * PG + 0.6, ROW_Y[k], 1.2, 0.3)
        add(JOIN[0], JOIN[1] - JOIN[0], -3.0, 1.2, 7.0, 2.6)
        add(SIGMA_T, BEAT, 2.6, Y_TOP, 3.4, 0.6)
        for k in KS:
            add(MULT_T[k], BEAT, *fan_point(k, 0.5), 1.5, 3.0)
        for k in KS:
            add(FAN_T[k], 0.3, *fan_point(k, 0.5), 1.5, 3.0)
        add(HIT, BEAT, 0.0, 0.5, 12.0, 3.4)
        add(HIT, BEAT, 5.0, Y_BOT, 3.0, 0.6)
        for j in range(3):
            add(HIT + (j + 1) * BEAT, BEAT, 0.0, 0.5, 12.0, 3.4)
        for j in range(4):
            add(RUN_TOP[0] + j * BEAT, BEAT, 0.0, 0.5, 12.0, 3.4)
        add(REGROUP[0], REGROUP[1] - REGROUP[0], -3.5, 1.0, 6.0, 2.4)
        for r in (1, 2, 3):
            add(RES_LAB_T[r], BEAT, (RES_BARS[r][0] + RES_BARS[r][1]) / 2, Y_TOP + LABEL_DY, 2.0, 0.6)
        for t0 in (bb(70, 2), bb(70, 3), bb(70, 4), bb(71, 2)):           # the galaxy turns (ALIVE)
            add(t0, BEAT, *ROOT_S, 6.0, 6.0)
        for t0 in [bb(73, 2) + j * BEAT for j in range(4)] + [bb(80, 4)] + [bb(80, 4) + j * BEAT for j in range(1, 2)]:
            add(t0, BEAT, 0.0, 1.0, 9.6, 2.6)                                  # the points shimmer

    def run(self):
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


GALAXY_FAMILY_HEX = [XC.mid, OC.mid, "#C8CCCC"]
HANDOVER_S08["rho_cut"] = RHO_CUT
