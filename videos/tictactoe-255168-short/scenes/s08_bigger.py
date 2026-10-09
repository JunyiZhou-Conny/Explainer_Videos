"""S08 · Perfect play, and chess 双方都不失误，还有国际象棋 — the climax (bars 81-98).

Bars 81-98 (3:12.0-3:55.2) of script.md; scene time 0 is the downbeat of bar 81. As in S01 (the reference
scene), the picture is a pure function of the scene time (`update_state`), and the notes are computed from
the same numbers (Sounds), each with its own tag ("X@C#5": an X bell at its square's pitch). The galaxy is
all 255,168 leaves and the internal nodes of the real game tree, splatted with numpy into one light image per
frame (common.Splatter), never as mobjects. Everything is drawn in screen space: the Manim camera stays home,
and the "camera" is the galaxy's own placement (`gcam`) and the strips' zoom (`zs`).

    81-82  the three result bars of S07 hold, shimmering; 81.3-82.1 their 255,168 points fly back into the
           galaxy (2 beats); 82.1 the internal nodes brighten and the root glows white          (c24)
    83-86  the minimax wave: the colours climb the tree, one ring per half bar (ring 8 on 83.1 ... ring 1 on
           86.3), each internal node taking the best result for the player to move; a label rides the wave
           front ("轮到 X 时：挑对 X 最好的 · BEST FOR X" / "... O ..."); ring 2 ends 48 cyan, 24 grey, ring 1
           all 9 grey; the camera pushes in towards the inner rings
    87     87.1 the root turns grey with a soft flare (perfect play is a draw)                  (c25)
    88-89  88.1 game A's leaf is ringed and its path lights back to the root (its notes backwards);
           88.3 the inset: game A after move 2, X0 cyan, O3 in RED "O 的失误 · O'S MISTAKE", the path's
           second step turns RED; 88.4 the centre glows grey "只有下中心才能保住平局 · ONLY THE CENTRE KEEPS THE
           DRAW"; 89.1-89.3 the inset plays on faintly, X1 O4 X2, to X's top row
    90-92  §6. 90.1-90.3 the galaxy shrinks into one small glowing box: box 1 of the strip "2 5 5 1 6 8"
           (6 boxes, "井字棋 · 6 位数 · TIC-TAC-TOE · 6 DIGITS"); 90.4 the chess strip starts below it, "1" and
           then zeros, one box per sixteenth and then faster; the camera pulls back as it runs, from close on
           the 55 px boxes (zoom Z0 = 2, so the digits read) to frame 2.6 on the 121st box             (c26)
    93     93.1 THE CLIMAX: the 121st box lands (one flash frame); the chess label (至少 ... 估计), "121 位数 ·
           121 DIGITS"; the tic-tac-toe strip glows, "全部下完 · ALL PLAYED OUT"                   (c27)
    94-95  the atoms strip runs between the two, 81 boxes (94.1-95.1), its label and "81 位数"   (c28)
    96-98  96.1 "每多一个格子，就大 10 倍 · EACH EXTRA BOX: 10 TIMES BIGGER"; the light pen comes back and
           sweeps the chess strip (a faint arm, its grain), one box per beat from 96.3, and stalls on box 6
           (97.4); bar 98 it pulses there while the 115 dark boxes fade into grain; the camera drifts back

Hand-over from S07 (a segue at 81.1): drawn by S07 itself. S07Stage runs s07_ledger.Ledger.build on a stand-in
and draws S07's objects with S07's own update_state at S07's times (and S07's own light until 81.3), so the first
frame here is S07's last whatever S07 ends on; they fade as the games leave (81.3-81.4). Every game flies from
where s07_ledger.ledger_points(END) leaves it to its slot in the galaxy as S07 cut it (S06's camera: the root on
screen at s07_ledger.ROOT_S, the turn s07_ledger.RHO_CUT).
Hand-over to S09 (a cut at 99.1): S09 draws this scene's last frame with the same rigs (StripsRig, the labels,
the pen, pen_glow) through `strip_view(END)`, then rushes back into box 1 of the tic-tac-toe strip.
"""

from __future__ import annotations

import math
from math import factorial
from types import SimpleNamespace

import numpy as np
from manim import Circle, Dot, ImageMobject, Line, Mobject, Rectangle, VGroup, VMobject

from explainer.short import BeatScene, FONT_MONO, INK, INK_DIM, RED, WHITE, cjk, stroke_px

from common import (GALAXY_COLOURS, GALAXY_DUST_W, GALAXY_LOOK, GAME_A, HUD_LINES_Y, NINE_FACT, OC,
                    PEN_HALO, PITCH, XC, FastCamera, FrameImage, Ink, InkText, LeanText, Pen, Shot,
                    Sounds, Splatter, W, H, bi_label, box, clamp01, ease_in_out_cubic, ease_in_out_sine,
                    ease_out_cubic, ease_out_quad, galaxy_tree, gaussian_sprite, o_template, order_slot, player,
                    pulse, rgb, ring_radius, section_hud, seg, show_sprite, tag)
from s02_fill import Hairlines
from s04_by_hand import EN_SIZE, ZH_SIZE, MiniBoard, en, hex_of, line_affine
import s07_ledger as s07

# ---------------------------------------------------------------- the plan's clock (bar 81 = scene time 0)
BEAT, BAR = 0.6, 2.4
FIRST = 81


def bb(bar: int, beat: float = 1.0) -> float:
    """Scene time of script.md's "bar.beat" (global bar numbers): bb(88, 3.5) is "88.3+"."""
    return (bar - FIRST) * BAR + (beat - 1) * BEAT


END = bb(99)                                      # 43.2 s: 18 bars

# ---------------------------------------------------------------- the game tree and its perfect-play values
_T = galaxy_tree()
FACT = [factorial(9 - k) for k in range(10)]
N_GAMES = len(_T.l_slot)
L_K, L_RES, L_FAM, L_WEIGHT, L_JIT = _T.l_k, _T.l_res, _T.l_fam, _T.l_weight, _T.l_jit
L_SLOT, L_MOVES = _T.l_slot, _T.l_moves
L_TH = 2 * np.pi * _T.l_centre / NINE_FACT        # clockwise from 12 o'clock
L_R = 2.9 * (L_K / 9.0) ** 0.75 + L_JIT
N_SLOT, N_DEPTH = _T.n_slot, _T.n_depth
N_TH = 2 * np.pi * _T.n_centre / NINE_FACT
N_R = 2.9 * (N_DEPTH / 9.0) ** 0.75
WIN_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
assert N_GAMES == 255_168 and len(N_SLOT) == 294_778


def minimax_values() -> np.ndarray:
    """The perfect-play result of every internal node (1 X wins, 2 O wins, 3 draw), in the program's order
    (common.GalaxyTree.n_slot: the same depth-first walk): each node takes the best of its children for the
    player to move (X: X > draw > O; O: O > draw > X)."""
    b = [0] * 9
    vals: list[int] = []
    prefer = {1: (1, 3, 2), 2: (2, 3, 1)}

    def win():
        for a, c, d in WIN_LINES:
            if b[a] and b[a] == b[c] == b[d]:
                return b[a]
        return 0

    def walk(p: int, d: int) -> int:
        w = win()
        if w or d == 9:
            return w if w else 3
        i = len(vals)
        vals.append(0)
        res = []
        for sq in range(9):
            if b[sq] == 0:
                b[sq] = p
                res.append(walk(3 - p, d + 1))
                b[sq] = 0
        vals[i] = min(res, key=prefer[p].index)
        return vals[i]
    walk(1, 0)
    return np.array(vals, np.int8)


N_VAL = minimax_values()
assert len(N_VAL) == len(N_SLOT)


def ring_counts(d: int) -> dict:
    m = N_DEPTH == d
    return {"X": int((N_VAL[m] == 1).sum()), "O": int((N_VAL[m] == 2).sum()), "D": int((N_VAL[m] == 3).sum())}


assert N_VAL[0] == 3                                                  # the root: perfect play is a draw
assert ring_counts(1) == {"X": 0, "O": 0, "D": 9}                     # ring 1: all 9 grey
assert ring_counts(2) == {"X": 48, "O": 0, "D": 24}                   # ring 2: 48 cyan, 24 grey


def node_index(path) -> int:
    """Index (in N_SLOT order) of the internal node reached by these moves."""
    i = np.flatnonzero((N_SLOT == order_slot(path)) & (N_DEPTH == len(path)))
    assert len(i) == 1, path
    return int(i[0])


# game A's path: root, X0, X0 O3, X0 O3 X1, X0 O3 X1 O4, and its leaf (the 7,317th game the program finds)
GA_PATH = [tuple(GAME_A[:d]) for d in range(6)]
GA_LEAF = int(np.flatnonzero((L_MOVES[:, :5] == GAME_A).all(axis=1) & (L_K == 5))[0])
assert GA_LEAF + 1 == 7_317 and L_SLOT[GA_LEAF] == 10_200 and L_RES[GA_LEAF] == 1
GA_NODES = [node_index(p) for p in GA_PATH[:5]]
GA_VALS = [int(N_VAL[i]) for i in GA_NODES] + [1]
assert GA_VALS == [3, 3, 1, 1, 1, 1]                  # grey, grey, then cyan from O's second move on: O3 lost it
REPLIES = {s: int(N_VAL[node_index((0, s))]) for s in range(1, 9)}
assert [s for s, v in REPLIES.items() if v == 3] == [4]           # after X0, only the centre keeps the draw
GA_TH = [2 * np.pi * (order_slot(p) + FACT[len(p)] / 2) / NINE_FACT for p in GA_PATH[:5]] + [float(L_TH[GA_LEAF])]
GA_R = [ring_radius(len(p)) for p in GA_PATH[:5]] + [float(L_R[GA_LEAF])]
GA_R[0] = 0.0

# the ring 1-2 edges (81 hairlines): every depth-1 and depth-2 node and its parent
EDGE_CHILD = np.flatnonzero((N_DEPTH >= 1) & (N_DEPTH <= 2))
_RING1 = {int(N_SLOT[i]): int(i) for i in np.flatnonzero(N_DEPTH == 1)}
EDGE_PARENT = np.array([0 if N_DEPTH[i] == 1 else _RING1[int(N_SLOT[i]) // FACT[1] * FACT[1]]   # the root, or the
                        for i in EDGE_CHILD])                                                    # ring-1 node over it
assert len(EDGE_CHILD) == 81 and (N_DEPTH[EDGE_PARENT] == N_DEPTH[EDGE_CHILD] - 1).all()

# the dust that the wave colours: common's dust subset (rings 0-5, a third of 6-8), without the root
D_IDX = _T.dust[N_DEPTH[_T.dust] > 0]
D_W = np.where(N_DEPTH[D_IDX] <= 5, 1.0, 3.0)
D_RING = N_DEPTH[D_IDX]
D_VAL = N_VAL[D_IDX]
D_BASE = D_W * GALAXY_DUST_W[D_RING]
# the wave's colours on the dust, by ring: strong where nodes are few (rings 1-4 read as single nodes), below
# the leaves' light where they are many (rings 6-8), so the leaves keep their colours
RING_BOOST = np.array([0.0, 1.5, 1.5, 1.9, 1.5, 1.0, 0.6, 0.5, 0.45, 0.0])
VAL_HEX = {1: XC.mid, 2: OC.mid, 3: "#C8CCCC"}            # a perfect-play value's colour (X, O, draw)

# ---------------------------------------------------------------- times
FLY = (bb(81, 3), bb(82))                         # the result bars fly back into the galaxy (2 beats)
FLY_SPREAD, FLY_JIT, FLY_DUR = 0.25, 0.04, 0.9
LABELS_OUT = (bb(81, 3), bb(81, 3) + 0.3)        # S07's labels, ruler and sums fade as the games leave
S07_GONE = LABELS_OUT[1] + 0.05                   # ... and S07's objects leave the scene
SEC_SWAP = (0.0, 0.5)                             # §4 -> §5 (the segue: out, then in) ...
SEC6 = bb(90)                                     # ... and §5 -> §6
READY = bb(82)                                    # dust brightens, the root glows white
WAVE_T = {8: bb(83), 7: bb(83, 3), 6: bb(84), 5: bb(84, 3), 4: bb(85), 3: bb(85, 3), 2: bb(86), 1: bb(86, 3)}
WAVE_START = bb(82, 3)                            # the front leaves ring 9 ...
ROOT_GREY = bb(87)                                # ... and reaches the root: grey
RING_A = bb(88)                                   # game A's leaf is ringed
PATH_T = [bb(88) + 0.15 * j for j in range(5)]    # its path lights back to the root, one edge per sixteenth
INSET_IN = bb(88, 3)                              # the inset; O3 RED; the mistake edge RED
CENTRE_IN = bb(88, 4)                             # the centre glows grey
PLAY_ON = [bb(89, 1), bb(89, 2), bb(89, 3)]        # X1 O4 X2, faint
WIN_IN = bb(89, 3.5)
COLLAPSE = (bb(90), bb(90, 3))                    # the galaxy shrinks into one small glowing box
TTT_T = [bb(90, 3) + 0.075 * k for k in range(6)] # its six boxes, on 32nd notes
CHESS0 = bb(90, 4)                                # the chess strip: "1" ...
HIT = bb(93)                                      # ... and its 121st box: the climax
SWEEP = (HIT, HIT + 0.5)                          # 93.1: a light runs the whole chess strip and blooms in box 121
ATOMS = (bb(94), bb(95))
CHESS_DIM = (bb(94), bb(94, 2))                   # the long labels step back to 55 % once read (c27, c28 say it)
ATOMS_DIM = (bb(95, 2), bb(95, 3))
NOTE_IN = bb(96)
LABELS_OFF = (bb(96), bb(96, 2))                  # ... and go as the camera moves in
ZOOM_IN = (bb(96, 2), bb(96, 4))                  # in on the strips' left ends: the six boxes the pen lights read
PEN_IN = bb(96)
ARM_IN = (bb(96), bb(96, 3))
LIT_T = [bb(96, 3), bb(96, 4), bb(97, 1), bb(97, 2), bb(97, 3), bb(97, 4)]
STALL = bb(98)
ZOOM_OUT = (bb(98), bb(98, 4))                    # back out: the 115 dark boxes ahead
ENDS_BACK = (bb(98, 3), bb(98, 4))                # "121 位数", "81 位数" come back with them
GRAIN = (bb(98), bb(98, 4.5))                     # the 115 dark boxes dim into grain


def chess_times() -> list[float]:
    """The 121 boxes: the "1" on 90.4, four zeros on sixteenths (the 5th box on 91.1), then faster and faster
    (an exponential rate, about one per frame at the end), the 121st exactly on 93.1."""
    t = [CHESS0 + 0.15 * i for i in range(5)]
    n, T0, T1 = 116, t[-1], HIT
    r0 = 1 / 0.15
    lo, hi = 0.01, 3.0
    for _ in range(100):                          # rate r0 e^(b u): 116 more boxes in T1 - T0
        b = (lo + hi) / 2
        if r0 * (math.exp(b * (T1 - T0)) - 1) / b < n:
            lo = b
        else:
            hi = b
    b = (lo + hi) / 2
    for k in range(1, n + 1):                     # box k of the run lands when the count reaches k
        t.append(T0 + math.log(1 + k * b / r0) / b)
    t[-1] = HIT
    return t


CHESS_T = chess_times()
ATOMS_T = [ATOMS[0] + (ATOMS[1] - ATOMS[0]) * (1 - math.sqrt(1 - i / 80)) for i in range(81)]
assert len(CHESS_T) == 121 and len(ATOMS_T) == 81 and abs(CHESS_T[-1] - HIT) < 1e-9 and abs(ATOMS_T[-1] - ATOMS[1]) < 1e-9
assert all(b > a for a, b in zip(CHESS_T, CHESS_T[1:]))

# ---------------------------------------------------------------- the hand-over from S07 (a segue at 81.1)
S07_END = s07.END                                 # S08's t = 0 is S07's t = S07_END
UNIT = 30_240                                     # games per unit of length (S07's scale: 9! = 12 units)
assert s07.UNIT == UNIT
assert UNIT == 30_240 and [round(n / UNIT, 2) for n in (131_184, 77_904, 46_080)] == [4.34, 2.58, 1.52]
BAR_XY, BAR_W, _fam07 = s07.ledger_points(S07_END)  # every game in S07's result bars (screen), with its light
assert (_fam07 == L_FAM).all() and len(BAR_XY) == N_GAMES
SHIMMER_PH = s07.SH_PH                            # S07's shimmer of the games, continued
RHO0 = float(s07.RHO_CUT)                         # the galaxy's turn when S07 cut it: every game flies to its slot
_rng = np.random.default_rng(81)
_u = (BAR_XY[:, 0] - BAR_XY[:, 0].min()) / np.ptp(BAR_XY[:, 0])
FLY_T0 = FLY[0] + FLY_SPREAD * _u + _rng.uniform(0, FLY_JIT, N_GAMES)      # each point leaves from its place
assert FLY_T0.max() + FLY_DUR <= FLY[1] + 1e-9

# ---------------------------------------------------------------- the galaxy's placement ("the camera")
ROT_RATE = math.radians(0.35)                     # the slow clockwise turn (ALIVE), from 82.1
G_FULL = (float(s07.ROOT_S[0]), float(s07.ROOT_S[1]), float(s07.Z))   # the galaxy where S06 / S07 drew it
G_WAVE = (-2.45, -0.35, 1.40)                     # pushed in on the inner rings (87.1)
G_HOLD = (-2.49, -0.40, 1.46)                     # ... drifting until 90.1

# the strips (screen units): one box per digit, every strip to the same scale
P_BOX = 0.25                                      # box pitch at zoom 1 (121 boxes fit the frame at zoom 1/2.6)
BOX_FILL = 0.82                                   # a box's width as a share of the pitch
XL = -5.7                                         # the strips' left end
Z0 = 2.0                                          # the zoom when the strips appear (90.3): boxes 55 px, digits
                                                  # 29 px at 1080p, so "2 5 5 1 6 8" reads; the camera then pulls
                                                  # back 5.2x along the chess run, to frame 2.6 on its 121st box
BOX_H0 = BOX_FILL * P_BOX * Z0                    # a box's height at Z0 (square, 55 px); pulled back the boxes stay
                                                  # tall (h ~ z^0.1: 47 px at frame 2.6): a band of bright cells,
                                                  # not a hairline
# rows: the tic-tac-toe strip right above the chess strip's first six boxes (6 against 121, one scale), the atoms
# strip under the chess strip's label; each long label under its strip
ROWS0 = {"ttt": 1.15, "chess": 0.60, "atoms": -0.85}    # rows at zoom Z0
ROWS1 = {"ttt": 1.35, "chess": 0.80, "atoms": -0.75}    # rows once pulled back (frame 2.6 and wider)
ZS1, ZS_DRIFT = 1 / 2.6, 1 / 2.8                  # the zoom at 93.1 (frame 2.6), drifting back to frame 2.8 (96.2)
Z_IN = 1.0                                        # 96.4-98.1: the first boxes at 34 px, their digits 26 px
ZS_END = 1 / 2.9                                  # the end of the scene (the 115 dark boxes ahead)
PULL_P = 3.0                                      # the knee of the pull-back (a soft minimum, see zs)
PULL_C = 121.5 * (ZS1 ** -PULL_P - Z0 ** -PULL_P) ** (-1 / PULL_P)   # ... so that the 121st box stands at ZS1
DIGITS = {"ttt": "255168", "chess": "1" + "0" * 120, "atoms": "1" + "0" * 80}
assert DIGITS["ttt"] == f"{N_GAMES}" and int(DIGITS["chess"]) == 10 ** 120 and int(DIGITS["atoms"]) == 10 ** 80
assert len(DIGITS["ttt"]) == 6 and len(DIGITS["chess"]) == 121 and len(DIGITS["atoms"]) == 81
GAL_IN_BOX = 0.35                                 # the shrunken galaxy's diameter as a share of box 1's width
BOX1_C0 = np.array([XL + 0.5 * P_BOX * Z0, ROWS0["ttt"]])
S_BOX = GAL_IN_BOX * BOX_FILL * P_BOX * Z0 / (2 * 2.9)


def _mix(a, b, e):
    return (a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e, a[2] * (b[2] / a[2]) ** e)


def gcam(t: float):
    """(root x, root y, scale) of the galaxy on screen at time t."""
    if t < READY:
        return G_FULL
    a = (G_FULL[0], G_FULL[1], 1.02)
    if t < bb(83):
        return _mix(G_FULL, a, ease_in_out_sine(seg(t, READY, bb(83))))
    if t < ROOT_GREY:
        return _mix(a, G_WAVE, ease_in_out_sine(seg(t, bb(83), ROOT_GREY)))
    if t < COLLAPSE[0]:
        return _mix(G_WAVE, G_HOLD, ease_in_out_sine(seg(t, ROOT_GREY, COLLAPSE[0])))
    return _mix(G_HOLD, (BOX1_C0[0], BOX1_C0[1], S_BOX), ease_in_out_cubic(seg(t, *COLLAPSE)))


def rho(t: float) -> float:
    """How far the galaxy has turned clockwise (radians): S07's turn at the cut, then a slow turn eased in from
    82.1."""
    dt = t - READY
    if dt <= 0:
        return RHO0
    ramp = 2.0
    return RHO0 + ROT_RATE * (dt * dt / (2 * ramp) if dt < ramp else dt - ramp / 2)


def zfac(s: float) -> float:
    """Leaf weights x zfac: the same surface brightness at any zoom (s^2); shrinking below full size the light
    concentrates (s^1.15), so the galaxy ends as one bright point, not a dim smudge."""
    return s * s if s >= 1 else s ** 1.15


def gal_screen(th, r, G, rh: float):
    """Screen positions of tree points (clockwise angle th, radius r) for the placement G and turn rh."""
    a = np.asarray(th) + rh
    r = np.asarray(r)
    return np.column_stack([G[0] + G[2] * r * np.sin(a), G[1] + G[2] * r * np.cos(a)])


def front_radius(t: float) -> float:
    """The minimax wave front (galaxy units): ring 9 at 82.3, ring d at WAVE_T[d], the root at 87.1."""
    keys = [(WAVE_START, ring_radius(9))] + [(WAVE_T[d], ring_radius(d)) for d in range(8, 0, -1)] + [(ROOT_GREY, 0.0)]
    if t <= keys[0][0]:
        return keys[0][1]
    for (ta, ra), (tb, rb) in zip(keys, keys[1:]):
        if t <= tb:
            return ra + (rb - ra) * ease_in_out_sine(seg(t, ta, tb))
    return 0.0


# ---------------------------------------------------------------- the strips' camera
def _chess_count(t: float) -> float:
    """Chess boxes standing at time t, continuous (for the camera, so it never jerks)."""
    if t < CHESS_T[0]:
        return 0.0
    if t >= CHESS_T[-1]:
        return 121.0
    k = int(np.searchsorted(CHESS_T, t, side="right"))
    a, b = CHESS_T[k - 1], CHESS_T[k]
    return k + (t - a) / (b - a)


def _run_zoom(n: float) -> float:
    """The strips' zoom once n chess boxes stand: Z0 while the run is short, then pulled back so the run's front
    keeps to the frame (a soft minimum of Z0 and PULL_C / (n + 0.5); the front x = XL + P_BOX (n + 0.5) z rises
    monotonically), exactly ZS1 at the 121st box."""
    return (Z0 ** -PULL_P + (PULL_C / (n + 0.5)) ** -PULL_P) ** (-1 / PULL_P)


def _pull(n: float) -> float:
    """0 .. 1: how far the camera has pulled back once n chess boxes stand (log zoom, 1 at the 121st)."""
    return clamp01(math.log(Z0 / _run_zoom(n)) / math.log(Z0 / ZS1))


def _lerp_log(a: float, b: float, e: float) -> float:
    return math.exp(math.log(a) + (math.log(b) - math.log(a)) * e)


def zs(t: float) -> float:
    """The strips' zoom (1 = box pitch P_BOX on screen; 1/2.6 = the frame 2.6 times wider): pulled back along the
    run (90.4-93.1), a slow drift back (93.1-96.2), in on the left ends while the pen lights its six boxes
    (96.2-96.4, then a slow drift), back out over bar 98, still drifting at the cut."""
    if t < HIT:
        return _run_zoom(_chess_count(t))
    if t < ZOOM_IN[0]:
        return _lerp_log(ZS1, ZS_DRIFT, ease_in_out_sine(seg(t, HIT, ZOOM_IN[0])))
    z_in = Z_IN * (1 - 0.05 * ease_in_out_sine(seg(t, ZOOM_IN[1], STALL)))
    if t < STALL:
        return _lerp_log(ZS_DRIFT, z_in, ease_in_out_cubic(seg(t, *ZOOM_IN)))
    z_out = ZS_END * (1.02 - 0.02 * seg(t, ZOOM_OUT[1], END))
    return _lerp_log(z_in, z_out, ease_in_out_cubic(seg(t, *ZOOM_OUT)))


assert abs(_run_zoom(121.0) - ZS1) < 1e-9 and abs(_run_zoom(0.0) / Z0 - 1) < 1e-4


def rows_z(z: float) -> dict:
    """The strips' rows at zoom z (they move apart a little as the camera pulls back)."""
    lam = clamp01(math.log(Z0 / z) / math.log(Z0 / ZS1))
    return {k: ROWS0[k] + (ROWS1[k] - ROWS0[k]) * lam for k in ROWS0}


def rows(t: float) -> dict:
    return rows_z(zs(t))


def box_x(i, z: float):
    """Screen x of box i's centre at zoom z (the left end stays put: the camera pulls back along the strip)."""
    return XL + (np.asarray(i, dtype=float) + 0.5) * P_BOX * z


def box_size(z: float) -> tuple[float, float]:
    """(width, height) of a box: square close up (Z0); pulled back the height shrinks only slowly, so far out the
    boxes read as tall bright cells (11 x 47 px at frame 2.6)."""
    return BOX_FILL * P_BOX * z, BOX_H0 * (min(z, Z0) / Z0) ** 0.1


_fronts = [box_x(_chess_count(t), zs(t)) for t in np.linspace(CHESS0, HIT, 400)]
assert max(_fronts) < 6.25 and all(b >= a - 1e-6 for a, b in zip(_fronts, _fronts[1:])), max(_fronts)


# ---------------------------------------------------------------- small drawing helpers
class BiText:
    """A label made of several text parts (a common.bi_label, or zh over en lines), each an InkText with its
    own colour, placed together: show(anchor, align "l" / "c" / "r", vis)."""

    def __init__(self, group: VGroup, colors):
        c = group.get_center()[:2]
        self.parts = [(LeanText(p, col), p.get_center()[:2] - c, col) for p, col in zip(group, colors)]
        self.width, self.height = group.width, group.height
        self.group = VGroup(*[it for it, _, _ in self.parts])
        self.hide()

    def hide(self):
        for it, _, _ in self.parts:
            it.hide()

    def show(self, anchor, align: str = "c", vis: float = 1.0, colors=None, scale: float = 1.0):
        if vis <= 1e-3:
            return self.hide()
        a = np.asarray(anchor, dtype=float)[:2].copy()
        if align == "l":
            a[0] += self.width * scale / 2
        elif align == "r":
            a[0] -= self.width * scale / 2
        for j, (it, off, col) in enumerate(self.parts):
            it.show(a + off * scale, scale=scale, vis=vis, color=colors[j] if colors else col)


EN_C = 20.5                                      # content labels' English: 28 px caps at 1080p, in the line colour
                                                  # (the 50 % grey is the HUD's)


def bi(zh: str, en_text: str, zh_color=INK, en_color=INK, en_size: float = EN_C) -> BiText:
    """One line: 中文 · ENGLISH (content size: the English 28 px caps at 1080p)."""
    g = bi_label(zh, en_text, zh_size=ZH_SIZE, en_size=en_size)
    return BiText(g, [zh_color, en_color, en_color])


def stacked(lines, align: str = "l", gap: float = 0.09, en_size: float = EN_C) -> BiText:
    """Lines (text, colour, "zh" / "en") stacked top to bottom, aligned left or centred."""
    mobs = [cjk(s, size=ZH_SIZE, color=c) if k == "zh" else en(s, size=en_size, color=c) for s, c, k in lines]
    g = VGroup(*mobs).arrange(np.array([0, -1, 0]), buff=gap,
                              aligned_edge=np.array([-1, 0, 0]) if align == "l" else np.array([0, 0, 0]))
    return BiText(g, [c for _, c, _ in lines])


class Glyphs1:
    """Digit glyphs (Noto Sans Mono) of many boxes drawn as ONE filled VMobject: set(centres, digits, height,
    opacity)."""

    def __init__(self, color=INK_DIM):
        from manim import Text
        self.tmpl = {}
        for d in "0123456789":
            t = Text(d, font=FONT_MONO, font_size=48)
            h = Text("0", font=FONT_MONO, font_size=48).height
            c = t.get_center()
            parts = [p.points.copy() for p in t.family_members_with_points()]
            self.tmpl[d] = [(q - c) / h for q in parts]
        self.mob = VMobject().set_fill(color, opacity=0).set_stroke(width=0, opacity=0)
        self.mob.points = np.zeros((0, 3))
        self.color = color

    def set(self, centres, digits, height: float, opacity: float = 1.0, color=None):
        if len(centres) == 0 or opacity <= 1e-3 or height <= 1e-4:
            self.mob.points = np.zeros((0, 3))
            self.mob.set_fill(opacity=0)
            return
        out = []
        for (x, y), d in zip(centres, digits):
            for q in self.tmpl[d]:
                p = q * height
                p[:, 0] += x
                p[:, 1] += y
                out.append(p)
        self.mob.points = np.concatenate(out)
        self.mob.set_fill(color or self.color, opacity=clamp01(opacity)).set_stroke(width=0, opacity=0)


def rect_segments(c, w, h):
    """The four sides of each box (centres c (n, 2), width w, height h) as segment end points."""
    c = np.asarray(c, dtype=float).reshape(-1, 2)
    if len(c) == 0:
        return np.zeros((0, 2)), np.zeros((0, 2))
    w = np.broadcast_to(np.asarray(w, dtype=float), (len(c),))[:, None] / 2
    h = np.broadcast_to(np.asarray(h, dtype=float), (len(c),))[:, None] / 2
    tl = c + np.hstack([-w, h])
    tr = c + np.hstack([w, h])
    br = c + np.hstack([w, -h])
    bl = c + np.hstack([-w, -h])
    P = np.concatenate([tl, tr, br, bl])
    Q = np.concatenate([tr, br, bl, tl])
    return P, Q


def xf_apply(p, xf):
    """A similarity on screen points: xf = (pivot0, pivot1, K): p -> pivot1 + K (p - pivot0)."""
    if xf is None:
        return np.asarray(p, dtype=float)
    p0, p1, k = xf
    return np.asarray(p1) + k * (np.asarray(p, dtype=float) - np.asarray(p0))


# ---------------------------------------------------------------- the three digit strips (S08 bars 90-98, S09 bar 99)
class BoxFill(VMobject):
    """Many filled rectangles as one VMobject (one Cairo path, one colour): set(centres, w, h, opacity)."""

    def __init__(self, color=INK):
        super().__init__()
        self.base_color = color
        self.set_fill(color, opacity=0).set_stroke(width=0, opacity=0)
        self.points = np.zeros((0, 3))

    def set(self, c, w, h, opacity: float, color=None):
        c = np.asarray(c, dtype=float).reshape(-1, 2)
        if len(c) == 0 or opacity <= 1e-3:
            self.points = np.zeros((0, 3))
            self.set_fill(opacity=0)
            return self
        n = len(c)
        P, Q = rect_segments(c, w, h)                 # the four sides of all boxes, side by side ...
        idx = np.stack([np.arange(n) + k * n for k in range(4)], axis=1).reshape(-1)   # ... box by box
        P, Q = P[idx], Q[idx]
        d = Q - P
        pts = np.zeros((4 * len(P), 3))
        pts[0::4, :2] = P
        pts[1::4, :2] = P + d / 3
        pts[2::4, :2] = P + 2 * d / 3
        pts[3::4, :2] = Q
        self.points = pts
        self.set_fill(color or self.base_color, opacity=clamp01(opacity)).set_stroke(width=0, opacity=0)
        return self


def lit_count(t: float) -> int:
    """How many chess boxes the light pen has lit by time t (0-6)."""
    return sum(1 for tt in LIT_T if t >= tt)


def ends_vis(t: float) -> float:
    """The strips' end labels ("121 位数", "81 位数"): they go as the camera moves in on the left ends and come
    back as it pulls out."""
    if t < STALL:
        return 1 - seg(t, ZOOM_IN[0], ZOOM_IN[0] + 0.3)
    return seg(t, *ENDS_BACK)


def atoms_vis(t: float) -> float:
    """The atoms strip steps back while the pen works on the chess strip (96.2-98.1)."""
    if t < STALL:
        return 1 - 0.55 * ease_in_out_sine(seg(t, *ZOOM_IN))
    return 0.45 + 0.15 * ease_in_out_sine(seg(t, *ZOOM_OUT))


class StripsRig:
    """The tic-tac-toe strip (6 glowing boxes "2 5 5 1 6 8"), the chess strip (121 bright cells, "1" and 120
    zeros), the atoms strip (81 cells), and the light they carry: the sweep and the glowing 121st box at the climax,
    the boxes the pen lights (in the tic-tac-toe strip's colours, so the six match the six above them) and their
    bracket. `draw(t, view, xf, vis, ghosts)` draws them as they stand at S08 time t (view = strip_view(t)), through
    an optional screen similarity xf (S09's rush back) with motion-blur ghost copies; `draw_labels` the labels."""

    def __init__(self):
        self.out = {"ttt": Hairlines(INK_DIM, 1.3), "chess": Hairlines(INK, 1.4), "atoms": Hairlines(INK_DIM, 1.3)}
        self.dim_out = Hairlines(INK_DIM, 1.3)        # chess boxes 7-121 as they dim (bar 98)
        self.ghost_out = [Hairlines(INK_DIM, 1.3) for _ in range(2)]
        self.fill = {"chess": BoxFill(INK), "atoms": BoxFill(INK)}
        self.dim_fill = BoxFill(INK)
        self.digits = {k: Glyphs1(WHITE if k == "ttt" else INK) for k in DIGITS}
        self.dim_digits = Glyphs1(INK)
        self.ttt_cols = [hex_of(rgb(XC.mid) * (1 - u) + rgb(OC.mid) * u) for u in np.linspace(0, 1, 6)]
        self.ttt_glow_cols = [hex_of(rgb(XC.glow) * (1 - u) + rgb(OC.glow) * u) for u in np.linspace(0, 1, 6)]
        self.ttt_box = [Ink(Rectangle(width=1, height=1), c, 1.6, g, 8, layers=4, glow_opacity=0.6)
                        for c, g in zip(self.ttt_cols, self.ttt_glow_cols)]
        self.ttt_fill = [Rectangle(width=1, height=1).set_stroke(width=0).set_fill(c, opacity=0) for c in self.ttt_cols]
        self.ttt_halo = gaussian_sprite(None, 96, 0.34, gradient=(XC.glow, OC.mid), aspect=3.0)
        self.box1_glow = gaussian_sprite(XC.mid, 64, 0.3)
        self.lit_box = [Ink(Rectangle(width=1, height=1), c, 1.8, g, 10, layers=4, glow_opacity=0.65)
                        for c, g in zip(self.ttt_cols, self.ttt_glow_cols)]
        self.lit_fill = [Rectangle(width=1, height=1).set_stroke(width=0).set_fill(c, opacity=0) for c in self.ttt_cols]
        self.lit_digits = Glyphs1(WHITE)
        self.flash_out = Hairlines(WHITE, 1.8)
        self.end_box = Ink(Rectangle(width=1, height=1), WHITE, 2.0, PEN_HALO, 12, layers=5, glow_opacity=0.6)
        self.end_halo = gaussian_sprite(PEN_HALO, 64, 0.3)
        self.bracket = Ink(VGroup(Line([-0.5, 0.5, 0], [-0.5, 0, 0]), Line([-0.5, 0, 0], [0.5, 0, 0]),
                                  Line([0.5, 0, 0], [0.5, 0.5, 0])), INK, 1.5, PEN_HALO, 6, layers=3,
                           glow_opacity=0.3)
        # labels: the English of content labels at 28 px in the line colour
        self.lab_ttt = bi("井字棋：6 位数", "TIC-TAC-TOE: 6 DIGITS")
        self.tag_ttt = bi("全部下完", "ALL PLAYED OUT")
        self.lab_chess = stacked([("国际象棋：至少 1 后面跟着 120 个零（香农，1950 年，估计）", INK, "zh"),
                                  ("CHESS: AT LEAST 1 FOLLOWED BY 120 ZEROS", INK, "en"),
                                  ("(SHANNON 1950, ESTIMATE)", INK, "en")])
        self.end_chess = bi("121 位数", "121 DIGITS")
        self.lab_atoms = stacked([("可观测宇宙中的原子：大约 1 后面跟着 80 个零（估计）", INK, "zh"),
                                  ("ATOMS IN THE OBSERVABLE UNIVERSE: ABOUT 1", INK, "en"),
                                  ("FOLLOWED BY 80 ZEROS (ESTIMATE)", INK, "en")])
        self.end_atoms = bi("81 位数", "81 DIGITS")
        self.note = bi("每多一个格子，就大 10 倍", "EACH EXTRA BOX: 10 TIMES BIGGER")
        self.lit_lab = [bi(f"{n} 格", f"{n} BOX" + ("ES" if n > 1 else "")) for n in range(1, 7)]
        assert self.lab_atoms.width < 12.4 and self.lab_chess.width < 12.4 and self.note.width < 12.0
        assert self.lab_ttt.width + 0.35 + self.tag_ttt.width < 12.3, (self.lab_ttt.width, self.tag_ttt.width)
        self.labels = [self.lab_ttt, self.tag_ttt, self.lab_chess, self.end_chess, self.lab_atoms, self.end_atoms,
                       self.note, *self.lit_lab]
        self.group = VGroup(*self.fill.values(), self.dim_fill, *self.out.values(), self.dim_out, *self.ghost_out,
                            *self.ttt_fill, *self.lit_fill, *self.ttt_box, *self.lit_box, self.flash_out,
                            self.end_box, self.bracket, *[g.mob for g in self.digits.values()], self.dim_digits.mob,
                            self.lit_digits.mob, *[lb.group for lb in self.labels])
        self.sprites = [self.ttt_halo, self.box1_glow, self.end_halo]
        self.hide_all()

    # --- which boxes stand at S08 time t, and how far each has landed
    @staticmethod
    def landed(times, t: float) -> tuple[int, np.ndarray]:
        n = int(np.searchsorted(times, t + 1e-9, side="right"))
        age = t - np.asarray(times[:n])
        return n, age

    def hide_all(self):
        for h in [*self.out.values(), self.dim_out, *self.ghost_out, self.flash_out]:
            h.set_segments([], [])
        for f in [*self.fill.values(), self.dim_fill]:
            f.set([], 0, 0, 0)
        for g in [*self.digits.values(), self.dim_digits, self.lit_digits]:
            g.set([], [], 0)
        for x in self.ttt_box + self.lit_box + [self.end_box, self.bracket]:
            x.hide()
        for r in self.ttt_fill + self.lit_fill:
            r.set_fill(opacity=0)
        for s in self.sprites:
            show_sprite(s, opacity=0)
        for lb in self.labels:
            lb.hide()

    def layout(self, t: float, z: float, ry: dict) -> dict:
        """Box centres, sizes and landing ages of each strip at S08 time t (zoom z, rows ry), before xf."""
        out = {}
        for key, times in (("ttt", TTT_T), ("chess", CHESS_T), ("atoms", ATOMS_T)):
            n, age = self.landed(times, t)
            i = np.arange(n)
            w, h = box_size(z)
            land = np.clip(age / 0.12, 0, 1)
            k = 0.55 + 0.45 * (1 - (1 - land) ** 3)                # each box lands with a short ease-out
            c = np.column_stack([box_x(i, z), np.full(n, ry[key]) + 0.06 * h * (1 - land)])
            out[key] = dict(n=n, c=c, w=w * k, h=h * k, land=land, w0=w, h0=h)
        return out

    def draw(self, t: float, view: dict, xf=None, vis: float = 1.0, ghosts=(), glow: float = 1.0) -> dict:
        """The strips at S08 time t as `view` (strip_view) frames them; ghosts: [(xf, opacity)] earlier placements
        drawn as faint outlines (S09's motion blur)."""
        z, ry, grain = view["z"], view["rows"], view["grain"]
        L = self.layout(t, z, ry)
        K = 1.0 if xf is None else xf[2]
        dim = 1 - 0.62 * grain                                    # bar 98: the 115 boxes ahead dim
        # the chess and atoms strips: bright cells (a faint fill, outlines in the line colour), their digits
        for key in ("chess", "atoms"):
            s = L[key]
            if s["n"] == 0 or vis <= 1e-3:
                self.out[key].set_segments([], [])
                self.fill[key].set([], 0, 0, 0)
                self.digits[key].set([], [], 0)
                if key == "chess":
                    self.dim_out.set_segments([], [])
                    self.dim_fill.set([], 0, 0, 0)
                    self.dim_digits.set([], [], 0)
                continue
            n = s["n"]
            c = xf_apply(s["c"], xf)
            w, hh = s["w"] * K, s["h"] * K
            sv = vis * (view["atoms"] if key == "atoms" else 1.0)
            land = float(np.mean(s["land"] ** 0.5))
            keep = np.ones(n, bool)
            if key == "chess" and grain > 0:
                keep[6:] = False
            P, Q = rect_segments(c[keep], w[keep], hh[keep])
            self.out[key].set_segments(P, Q, opacity=(0.85 if key == "chess" else 0.7) * sv * land)
            self.fill[key].set(c[keep], w[keep], hh[keep], (0.12 if key == "chess" else 0.06) * sv * land)
            dh = min(0.5 * float(np.min(s["h0"])) * K, 1.2 * float(np.min(s["w0"])) * K)
            show = s["land"] >= 0.5                                  # a digit appears once its box has landed
            dig = DIGITS[key][:n]
            self.digits[key].set(c[show & keep], "".join(d for d, k_ in zip(dig, show & keep) if k_), dh,
                                 (0.85 if key == "chess" else 0.6) * sv)
            if key == "chess":
                if (~keep).any():
                    P2, Q2 = rect_segments(c[~keep], w[~keep], hh[~keep])
                    self.dim_out.set_segments(P2, Q2, opacity=0.85 * sv * dim)
                    self.dim_fill.set(c[~keep], w[~keep], hh[~keep], 0.12 * sv * dim)
                    self.dim_digits.set(c[~keep & show], "".join(d for d, k_ in zip(dig, ~keep & show) if k_), dh,
                                        0.85 * sv * (1 - 0.8 * grain))
                else:
                    self.dim_out.set_segments([], [])
                    self.dim_fill.set([], 0, 0, 0)
                    self.dim_digits.set([], [], 0)
        # the tic-tac-toe boxes: glowing outlines (cool -> warm), a faint fill, a halo behind them, white digits
        s = L["ttt"]
        if s["n"] and vis > 1e-3:
            c = xf_apply(s["c"], xf)
            dh = min(0.5 * s["h0"] * K, 1.2 * s["w0"] * K)
            show = s["land"] >= 0.5
            self.digits["ttt"].set(c[show], "".join(d for d, k_ in zip(DIGITS["ttt"], show) if k_), dh, vis)
        else:
            self.digits["ttt"].set([], [], 0)
        self.out["ttt"].set_segments([], [])
        for j in range(6):
            if j >= s["n"] or vis <= 1e-3:
                self.ttt_box[j].hide()
                self.ttt_fill[j].set_fill(opacity=0)
                continue
            cj = xf_apply(s["c"][j], xf)
            wj, hj = s["w"][j] * K, s["h"][j] * K
            g = glow * (1 + 0.3 * view["breathe"])
            self.ttt_box[j].show(1.0, np.diag([wj, hj]), cj, vis=vis * min(1.0, s["land"][j] * 1.5), glow=g)
            self.ttt_fill[j].stretch_to_fit_width(max(1e-3, wj)).stretch_to_fit_height(max(1e-3, hj)).move_to([*cj, 0])
            self.ttt_fill[j].set_fill(self.ttt_cols[j], opacity=clamp01(0.2 * vis * s["land"][j] * g))
        if s["n"] and vis > 1e-3:
            c0, c1 = xf_apply(s["c"][0], xf), xf_apply(s["c"][s["n"] - 1], xf)
            hw = (c1[0] - c0[0]) + s["w0"] * K * 2.6
            show_sprite(self.ttt_halo, (c0 + c1) / 2, max(hw, s["h0"] * K * 2.2), s["h0"] * K * 3.0,
                        0.5 * vis * glow * (1 + 0.3 * view["breathe"]))
            bw = s["w0"] * K
            g1 = 0.25 + 0.75 * math.exp(-max(0.0, t - TTT_T[0]) / 0.4)   # the galaxy's last light, settling
            show_sprite(self.box1_glow, c0, bw * 1.1, bw * 1.1, 0.7 * vis * glow * g1)
        else:
            show_sprite(self.ttt_halo, opacity=0)
            show_sprite(self.box1_glow, opacity=0)
        # the boxes the pen has lit (chess strip): the tic-tac-toe strip's colours, glowing, white digits
        s = L["chess"]
        cs, ds = [], []
        for j in range(6):
            amt = next((a for b, a in view["lit"] if b == j), 0.0)
            if j >= s["n"] or amt <= 1e-3 or vis <= 1e-3:
                self.lit_box[j].hide()
                self.lit_fill[j].set_fill(opacity=0)
                continue
            cj = xf_apply(s["c"][j], xf)
            wj, hj = s["w0"] * K, s["h0"] * K
            self.lit_box[j].show(1.0, np.diag([wj, hj]), cj, vis=vis * min(1.0, amt), glow=glow * (1.0 + 0.8 * max(0.0, amt - 1)))
            self.lit_fill[j].stretch_to_fit_width(max(1e-3, wj)).stretch_to_fit_height(max(1e-3, hj)).move_to([*cj, 0])
            self.lit_fill[j].set_fill(self.ttt_cols[j], opacity=clamp01(0.3 * vis * min(1.3, amt)))
            cs.append(cj)
            ds.append(DIGITS["chess"][j])
        dh = min(0.5 * s["h0"] * K, 1.2 * s["w0"] * K) if s["n"] else 0
        self.lit_digits.set(cs, ds, dh, vis)
        # the bracket under the lit boxes (the count is its label, draw_labels)
        nl, bv = view["bracket"]
        if nl and s["n"] >= nl and bv > 1e-3 and vis > 1e-3:
            a = xf_apply(s["c"][0], xf)
            b = xf_apply(s["c"][nl - 1], xf)
            x0, x1 = a[0] - s["w0"] * K / 2, b[0] + s["w0"] * K / 2
            y = a[1] - s["h0"] * K / 2 - 0.09 * K
            self.bracket.show(1.0, np.diag([x1 - x0, 0.16 * K]), np.array([(x0 + x1) / 2, y]), vis=vis * bv,
                              glow=1.0 + 1.2 * view["bracket_flash"])
        else:
            self.bracket.hide()
        # the climax: every chess outline flares once; the 121st box keeps a glow
        if view["flash"] > 1e-3 and s["n"] and vis > 1e-3:
            c = xf_apply(s["c"], xf)
            P, Q = rect_segments(c, s["w0"] * K, s["h0"] * K)
            self.flash_out.set_segments(P, Q, opacity=clamp01(view["flash"]) * vis, width=1.0 + 0.8 * view["flash"])
        else:
            self.flash_out.set_segments([], [])
        ev = view["end_glow"] * vis
        if s["n"] == 121 and ev > 1e-3:
            ce = xf_apply(s["c"][120], xf)
            self.end_box.show(1.0, np.diag([s["w0"] * K, s["h0"] * K]), ce, vis=clamp01(ev), glow=0.8 + 0.8 * ev)
            hs = s["h0"] * K * (2.4 + 1.6 * view["bloom"])
            show_sprite(self.end_halo, ce, hs, hs, clamp01(0.55 * ev + 0.6 * view["bloom"] * vis))
        else:
            self.end_box.hide()
            show_sprite(self.end_halo, opacity=0)
        # motion-blur ghosts (S09's rush): earlier placements, outlines only
        for gi, gh in enumerate(self.ghost_out):
            if gi >= len(ghosts):
                gh.set_segments([], [])
                continue
            gxf, op = ghosts[gi]
            Pa, Qa = [], []
            for key in ("ttt", "chess", "atoms"):
                ss = L[key]
                if ss["n"] == 0:
                    continue
                c = xf_apply(ss["c"], gxf)
                P, Q = rect_segments(c, ss["w0"] * gxf[2], ss["h0"] * gxf[2])
                Pa.append(P)
                Qa.append(Q)
            if Pa:
                gh.set_segments(np.concatenate(Pa), np.concatenate(Qa), opacity=op * vis)
            else:
                gh.set_segments([], [])
        return L

    def draw_labels(self, t: float, L: dict, view: dict, xf=None, vis: float = 1.0):
        """The labels at S08 time t (screen; they fade, they do not zoom): each strip's long label under it, the
        counts at the strips' ends, the tic-tac-toe label over its boxes, the lit boxes' count under the bracket."""
        K = 1.0 if xf is None else xf[2]
        s = L["ttt"]
        if s["n"]:
            c0 = xf_apply(s["c"][0], xf)
            a = ease_out_cubic(seg(t, TTT_T[0], TTT_T[0] + 0.35))
            x0 = c0[0] - s["w0"] * K / 2
            y = c0[1] + s["h0"] * K / 2 + 0.27
            self.lab_ttt.show([x0, y + 0.05 * (1 - a)], "l", vis * a)
            a = ease_out_cubic(seg(t, HIT, HIT + 0.4))
            self.tag_ttt.show([x0 + self.lab_ttt.width + 0.35 + 0.1 * (1 - a), y], "l", vis * a)
        else:
            self.lab_ttt.hide()
            self.tag_ttt.hide()
        off = 1 - ease_in_out_sine(seg(t, *LABELS_OFF))
        s = L["chess"]
        if s["n"]:
            c0 = xf_apply(s["c"][0], xf)
            a = ease_out_cubic(seg(t, HIT, HIT + 0.45)) * (1 - 0.45 * ease_in_out_sine(seg(t, *CHESS_DIM))) * off
            top = c0[1] - s["h0"] * K / 2 - 0.14
            self.lab_chess.show([c0[0] - s["w0"] * K / 2, top - self.lab_chess.height / 2 - 0.05 * (1 - a)], "l",
                                vis * a)
            e = xf_apply(s["c"][-1], xf)
            a = ease_out_cubic(seg(t, HIT + 0.15, HIT + 0.55)) * ends_vis(t)
            self.end_chess.show([e[0] + s["w0"] * K / 2, e[1] + s["h0"] * K / 2 + 0.24], "r", vis * a)
            nl, bv = view["bracket"]
            for n, lb in enumerate(self.lit_lab, start=1):
                if n == nl and bv > 1e-3:
                    self.lit_lab[n - 1].show([c0[0] - s["w0"] * K / 2, c0[1] - s["h0"] * K / 2 - 0.4], "l", vis * bv)
                else:
                    lb.hide()
        else:
            self.lab_chess.hide()
            self.end_chess.hide()
            for lb in self.lit_lab:
                lb.hide()
        s = L["atoms"]
        if s["n"]:
            c0 = xf_apply(s["c"][0], xf)
            a = ease_out_cubic(seg(t, ATOMS[0], ATOMS[0] + 0.45)) * (1 - 0.45 * ease_in_out_sine(seg(t, *ATOMS_DIM))) * off
            top = c0[1] - s["h0"] * K / 2 - 0.14
            self.lab_atoms.show([c0[0] - s["w0"] * K / 2, top - self.lab_atoms.height / 2 - 0.05 * (1 - a)], "l",
                                vis * a)
            e = xf_apply(s["c"][-1], xf)
            a = ease_out_cubic(seg(t, ATOMS[1], ATOMS[1] + 0.4)) * ends_vis(t) * view["atoms"]
            self.end_atoms.show([e[0] + s["w0"] * K / 2 + 0.3 + 0.1 * (1 - a), e[1]], "l", vis * a)
        else:
            self.lab_atoms.hide()
            self.end_atoms.hide()
        a = ease_out_cubic(seg(t, NOTE_IN, NOTE_IN + 0.5))
        y = xf_apply(np.array([0.0, NOTE_Y]), xf)[1] if xf is not None else NOTE_Y
        self.note.show([0.0, y - 0.05 * (1 - a)], "c", vis * a)


NOTE_Y = -2.2                                     # "每多一个格子，就大 10 倍", under everything (above the captions)


def pen_x(t: float, z: float) -> float:
    """Where the light pen is on the chess strip (screen x): from the strip's left end (96.1) to box 1's centre
    (96.3), then one box per beat (ease-out), and stalled on box 6 from 97.4."""
    keys = [(PEN_IN, XL)] + [(tt, float(box_x(j, z))) for j, tt in enumerate(LIT_T)]
    if t <= keys[0][0]:
        return XL
    for (ta, xa), (tb, xb) in zip(keys, keys[1:]):
        if t <= tb:
            u = seg(t, ta, tb)
            return xa + (xb - xa) * (ease_in_out_sine(u) if ta == PEN_IN else ease_out_cubic(u / 0.6 if u < 0.6 else 1))
    return float(box_x(5, z))


def pen_glow(t: float) -> float:
    """The light pen's glow on the chess strip: a flare on each box it lights, a pulse on the beats of bar 98."""
    beat = max([pulse(t, bb(98, b), 0.28) for b in (1, 2, 3, 4) if t >= bb(98, b)] + [0.0])
    return 1.0 + 1.3 * beat + 0.6 * max([pulse(t, tt, 0.25) for tt in LIT_T if t >= tt] + [0.0])


def strip_view(t: float) -> dict:
    """How the strips stand at S08 time t: zoom, rows, lit boxes, grain, the climax's sweep and glows (S09 starts
    from strip_view(END))."""
    z = zs(t)
    lit = []
    for j, tt in enumerate(LIT_T):
        if t >= tt:
            amt = 1.0 + 1.2 * pulse(t, tt, 0.35)
            if t >= STALL and j == 5:
                amt += 0.6 * max([pulse(t, bb(98, b), 0.3) for b in (1, 2, 3, 4) if t >= bb(98, b)] + [0.0])
            lit.append((j, amt))
    nl = lit_count(t)
    bv = ease_out_cubic(seg(t, LIT_T[0], LIT_T[0] + 0.3)) if nl else 0.0
    bflash = max([pulse(t, tt, 0.3) for tt in LIT_T if t >= tt] + [0.0])
    head = 120 * (t - SWEEP[0]) / (SWEEP[1] - SWEEP[0]) if SWEEP[0] <= t < SWEEP[1] + 0.3 else None
    end_glow = ease_out_cubic(seg(t, SWEEP[1] - 0.08, SWEEP[1] + 0.25)) * (1 - 0.6 * ease_in_out_sine(seg(t, *GRAIN)))
    breathe = math.sin(2 * math.pi * (t - HIT) / BAR) if t >= HIT else 0.0
    end_glow *= 1 + 0.2 * breathe
    return {"z": z, "rows": rows_z(z), "lit": lit, "grain": ease_in_out_sine(seg(t, *GRAIN)),
            "flash": 0.55 * pulse(t, HIT, 0.3) if t >= HIT else 0.0, "breathe": breathe, "head": head,
            "end_glow": end_glow, "bloom": pulse(t, SWEEP[1], 0.45) if t >= SWEEP[1] else 0.0,
            "atoms": atoms_vis(t), "bracket": (nl, bv), "bracket_flash": bflash}


# ---------------------------------------------------------------- the grain of the dark boxes (bar 98) and the pen's sparks
_g_rng = np.random.default_rng(98)
GRAIN_BOX = np.repeat(np.arange(6, 121), 14)                       # 14 grains on the outline of each dark box
GRAIN_UV = _g_rng.uniform(-0.5, 0.5, (len(GRAIN_BOX), 2))
_side = _g_rng.integers(0, 4, len(GRAIN_BOX))                      # snap each grain onto one side of its box
GRAIN_UV[_side == 0, 1] = 0.5
GRAIN_UV[_side == 1, 1] = -0.5
GRAIN_UV[_side == 2, 0] = 0.5
GRAIN_UV[_side == 3, 0] = -0.5
GRAIN_PH = _g_rng.uniform(0, 2 * np.pi, (len(GRAIN_BOX), 2))
GRAIN_F = _g_rng.uniform(0.6, 1.6, (len(GRAIN_BOX), 2))
GRAIN_W = _g_rng.uniform(0.5, 1.0, len(GRAIN_BOX))
SPARK_T = np.arange(PEN_IN, END + 1.0, 0.04)                       # the pen's grain texture: a spark every 40 ms
SPARK_V = _g_rng.normal(0, 1, (len(SPARK_T), 2)) * np.array([0.10, 0.16]) + np.array([-0.18, 0.0])
SPARK_O = _g_rng.normal(0, 1, (len(SPARK_T), 2)) * 0.03


def grain_points(t: float, z: float, ry: dict, grain: float, xf=None):
    """The dark chess boxes as grain: points on their outlines that drift and dim (screen, weights)."""
    if grain <= 1e-3:
        return None, None
    w, h = box_size(z)
    cx = box_x(GRAIN_BOX, z)
    p = np.column_stack([cx + GRAIN_UV[:, 0] * w, ry["chess"] + GRAIN_UV[:, 1] * h])
    amp = 0.012 + 0.03 * grain
    p = p + amp * np.column_stack([np.sin(GRAIN_F[:, 0] * 3.1 * t + GRAIN_PH[:, 0]),
                                   np.cos(GRAIN_F[:, 1] * 2.7 * t + GRAIN_PH[:, 1])])
    p = xf_apply(p, xf)
    wts = GRAIN_W * 0.9 * math.sin(math.pi * min(1.0, grain * 1.15)) ** 0.6 * (0.35 + 0.65 * (1 - grain)) + \
        GRAIN_W * 0.25 * grain
    return p, wts


def spark_points(t: float, px: float, py: float, moving_until: float):
    """Sparks the pen leaves behind while it sweeps (fewer once it stalls), drifting back and fading."""
    births = SPARK_T[(SPARK_T <= t) & (SPARK_T > t - 0.7)]
    if len(births) == 0:
        return None, None
    j = np.searchsorted(SPARK_T, births)
    age = t - births
    keep = (births <= moving_until) | (j % 5 == 0)
    j, age = j[keep], age[keep]
    p = np.column_stack([np.full(len(j), px), np.full(len(j), py)]) + SPARK_O[j] + SPARK_V[j] * age[:, None]
    return p, 1.6 * (1 - age / 0.7) ** 2


def strip_lights(t: float, view: dict, xf=None):
    """Light under the strips (white, splatted): the chess strip's band of cells (each box a soft glow, the 115
    ahead dimming in bar 98), the atoms strip fainter; a spark on each box as it lands (the run's front); at 93.1
    a light that runs the whole chess strip and blooms in its 121st box; a burst on each box the pen lights."""
    z, ry = view["z"], view["rows"]
    w, h = box_size(z)
    ps, ws = [], []
    tri = np.array([-0.3, 0.0, 0.3])
    for key, times, base, k in (("chess", CHESS_T, 0.42, 1.0), ("atoms", ATOMS_T, 0.2, 0.6), ("ttt", TTT_T, 0.0, 1.0)):
        n = int(np.searchsorted(times, t + 1e-9, side="right"))
        if n == 0:
            continue
        i = np.arange(n)
        age = t - np.asarray(times[:n])
        wt = base * np.clip(age / 0.12, 0, 1) + 2.4 * k * np.where(age < 0.45, np.exp(-age / 0.1), 0.0)
        if key == "atoms":
            wt = wt * view["atoms"]
        if key == "chess":
            if view["grain"] > 0:
                wt[6:] *= 1 - 0.7 * view["grain"]
            if view["head"] is not None:                       # the climax's sweep, then the bloom in box 121
                wt = wt + 6.0 * np.exp(-((i - view["head"]) / 3.0) ** 2) * (view["head"] <= 125)
            wt[min(n, 121) - 1] += (6.0 * view["bloom"] + 1.4 * view["end_glow"]) if n == 121 else 0.0
            for j, tt in enumerate(LIT_T):                     # the pen lights a box: a burst
                if t >= tt and j < n:
                    wt[j] += 6.0 * math.exp(-(t - tt) / 0.15) + 0.5
        sel = wt > 1e-3
        if not sel.any():
            continue
        x = np.repeat(box_x(i[sel], z), 3)
        y = ry[key] + np.tile(tri, int(sel.sum())) * h
        ps.append(np.column_stack([x, y]))
        ws.append(np.repeat(wt[sel], 3) / 3)
    if not ps:
        return None, None
    return xf_apply(np.concatenate(ps), xf), np.concatenate(ws)


# ---------------------------------------------------------------- S07's last frame (81.1-81.6), drawn by S07 itself
class S07Stage(s07.Ledger):
    """S07's scene without a scene: s07_ledger.Ledger.build runs on this stand-in (no renderer, no camera), which
    records what S07 adds and fixes, so S08 shows S07's own objects drawn by S07's own update_state at S07's
    times: the first frame here is S07's last, whatever S07 ends on. S08 then fades them (`draw`) as the games
    fly home and drops them (`mobjects`) once they are gone."""

    HUD_Y = 3.15                                  # what sits above this (screen) is S07's HUD: it goes with §4

    def __init__(self):                           # (deliberately not Scene.__init__: nothing here renders)
        self._cam = SimpleNamespace(frame=Mobject())
        self.added, self.fixed = [], []
        self.build()
        self.update_state(S07_END)
        self.base = []                            # (mobject, fill opacity, stroke opacity or image alpha, is hud)
        for m in self.fixed:
            for x in m.get_family():
                hud = len(x.points) > 0 and x.get_center()[1] > self.HUD_Y
                if isinstance(x, ImageMobject):
                    self.base.append((x, None, float(getattr(x, "stroke_opacity", 1.0)), hud))
                elif isinstance(x, VMobject):
                    self.base.append((x, x.get_fill_opacity(), x.get_stroke_opacity(), hud))

    @property
    def camera(self):
        return self._cam

    def add(self, *mobs):
        self.added.extend(mobs)
        return self

    def fix(self, *mobs):
        self.fixed.extend(mobs)
        return mobs[0] if len(mobs) == 1 else mobs

    def remove(self, *mobs):
        return self

    def clock(self) -> float:
        return S07_END

    @property
    def mobjects_to_show(self) -> list:
        return list(self.fixed)

    def light_at(self, t07: float):
        """S07's own light image (its games in the result bars) at S07 time t07."""
        type(self).update_light(self, t07)
        return self.galaxy.light

    def draw(self, t07: float, vis: float, vis_hud: float):
        """S07's last frame at S07 time t07 (its breathing goes on), faded by vis (the HUD by vis_hud)."""
        for x, f, a, _ in self.base:                          # back to S07's last frame, then S07 draws on it
            if f is None:
                if len(x.points):
                    x.set_opacity(a)
            else:
                x.set_fill(opacity=f)
                x.set_stroke(opacity=a)
        self.update_light = lambda t: None                    # (its light is drawn by S08)
        try:
            self.update_state(t07)
        finally:
            del self.update_light
        for x, f, a, hud in self.base:
            k = vis_hud if hud else vis
            if k >= 1 - 1e-6:
                continue
            if f is None:
                if len(x.points):
                    x.set_opacity(clamp01(getattr(x, "stroke_opacity", a) * k))
            else:
                x.set_fill(opacity=x.get_fill_opacity() * k)
                x.set_stroke(opacity=x.get_stroke_opacity() * k)


# ---------------------------------------------------------------- the scene
class BiggerGames(BeatScene):

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
        self.light = FrameImage()
        # S07's last frame: the HUD (§4 and its readout) and the bars' labels
        self.secs = []
        for text in ("§5 · 双方都不失误 · PERFECT PLAY", "§6 · 更复杂的棋 · BIGGER GAMES"):
            g = section_hud(text)
            self.secs.append((InkText(g, INK_DIM), g.get_center()[:2]))
        self.sec5, self.sec6 = [s for s, _ in self.secs]
        self.s07 = S07Stage()
        # the tree's inner structure: the ring 1-2 edges, the root, the wave front and its label
        self.edges = Hairlines(INK_DIM, 1.2)
        # rings 1-2 (81 nodes) as small dots, so their perfect-play colours read one by one (48 cyan, 24 grey; 9 grey)
        self.node_glow = [Dot(radius=0.05, color=INK_DIM).set_fill(opacity=0) for _ in EDGE_CHILD]
        self.node_core = [Dot(radius=0.017, color=INK_DIM).set_fill(opacity=0) for _ in EDGE_CHILD]
        self.root_halo = gaussian_sprite(WHITE, 64, 0.3)
        self.root_board = MiniBoard(0.14, 0, 0, nums=0)            # the root, as S05 draws it: a tiny empty board
        self.front = Ink(Circle(radius=1.0, num_components=64).rotate(math.pi / 2), INK, 1.3, PEN_HALO, 10, layers=4,
                         glow_opacity=0.32)
        self.wave_lab = [bi("轮到 X 时：挑对 X 最好的", "BEST FOR X"), bi("轮到 O 时：挑对 O 最好的", "BEST FOR O")]
        self.wave_leader = Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.1)
        # game A: the ring round its leaf, its path, the inset
        self.leaf_ring = Ink(Circle(radius=1.0, num_components=32).rotate(math.pi / 2), XC.mid, 1.8, XC.glow, 10, layers=5,
                             glow_opacity=0.55)
        self.path = [Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), WHITE, 2.0, PEN_HALO, 10, layers=5, glow_opacity=0.5)
                     for _ in range(5)]
        self.path_red = Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), RED, 2.4, RED, 11, layers=5, glow_opacity=0.55)
        self.path_dots = [gaussian_sprite(VAL_HEX[v], 48, 0.3) for v in GA_VALS]
        self.inset = MiniBoard(0.52, 3, 1, nums=0, glow_x=9, glow_o=11, layers=5)
        self.inset_c = np.array([4.35, 0.95])
        self.red_o = Ink(o_template(0.62 * 0.52), RED, 3.0, RED, 12, layers=5, glow_opacity=0.5)
        self.centre_glow = gaussian_sprite("#C8CCCC", 64, 0.32)
        self.lab_mistake = bi("O 的失误", "O'S MISTAKE", zh_color=RED, en_color=RED)
        self.lab_centre = stacked([("只有下中心才能保住平局", INK, "zh"), ("ONLY THE CENTRE", INK_DIM, "en"),
                                   ("KEEPS THE DRAW", INK_DIM, "en")], align="c")
        self.inset_leader = Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.1)
        # the strips, the pen and its arm, the flash
        self.strips = StripsRig()
        self.pen = Pen()
        self.arm = Ink(Line([0, -0.5, 0], [0, 0.5, 0]), INK, 1.4, PEN_HALO, 10, layers=4, glow_opacity=0.35)
        self.flash = Rectangle(width=W + 0.2, height=8.2).set_stroke(width=0).set_fill("#FFFFFF", opacity=0)

        self.clock_mob = Mobject()
        self.clock_mob.add_updater(lambda m: self.update_state(self.clock()))
        self.add(self.clock_mob, self.camera.frame)
        self.add(self.light)
        self.s07_on = True
        self.fix(self.edges, *self.node_glow, *self.node_core, self.front, self.wave_leader, self.root_halo, self.root_board.group, *self.path, self.path_red,
                 *self.path_dots, self.leaf_ring, self.inset_leader, self.centre_glow, self.inset.group, self.red_o,
                 *[lb.group for lb in self.wave_lab], self.lab_mistake.group,
                 self.lab_centre.group, *self.strips.sprites, self.strips.group, self.arm, self.pen,
                 self.sec5, self.sec6, *self.s07.mobjects_to_show, self.flash)
        self.update_state(0.0)

    # ------------------------------------------------------------- the picture at time t
    def update_state(self, t: float):
        self.update_light(t)
        self.update_tree(t)
        self.update_game_a(t)
        self.update_strips(t)
        self.update_hud(t)
        fl = 0.85 * math.exp(-(t - HIT) / 0.022) if HIT <= t < HIT + 0.07 else 0.0
        self.flash.set_fill(opacity=fl)

    # --- the light layer: the bars' points, the galaxy, the grain and the sparks
    def galaxy_on(self, t: float) -> float:
        """How much of the galaxy's light is drawn (it hands over to box 1's glow at 90.3)."""
        return 1 - seg(t, COLLAPSE[1] - 0.05, COLLAPSE[1] + 0.12)

    def update_light(self, t: float):
        fams = [[[], []] for _ in range(6)]                   # X, O, draws, dust, RED, white: (points, weights)

        def put(f, p, w):
            fams[f][0].append(p)
            fams[f][1].append(w)
        if t < FLY[0] - 1e-6:                                  # S07's own light (its games, shimmering)
            self.light.light = self.s07.light_at(S07_END + t)
            return
        if self.galaxy_on(t) > 1e-3:
            self.galaxy_families(t, put)
        v = strip_view(t)
        z, ry = v["z"], v["rows"]
        if t >= TTT_T[0]:
            p, w = strip_lights(t, v)
            if p is not None:
                put(5, p, w)
        if t >= PEN_IN:
            g = ease_in_out_sine(seg(t, *GRAIN))
            p, w = grain_points(t, z, ry, g)
            if p is not None:
                put(3, p, w)
            p, w = spark_points(t, pen_x(t, z), ry["chess"], LIT_T[-1])
            if p is not None:
                put(5, p, w)
        families = []
        for f, (ps, ws) in enumerate(fams):
            if ps:
                families.append((self.splat.accumulate(np.concatenate(ps), np.concatenate(ws)), GALAXY_COLOURS[f]))
        if not families:
            self.light.light = None
            return
        img = self.splat.render(families, **GALAXY_LOOK)
        G = gcam(t)
        k = clamp01((G[2] - 1.08) / 0.3) if t < COLLAPSE[0] + 0.3 else 0.0
        if k > 0:                                              # keep the caption band and the HUD band dark
            img = (img * self.band_mask(k)[:, None, None]).astype(np.uint8)
        self.light.light = img

    def band_mask(self, k: float) -> np.ndarray:
        h = self.splat.h
        y = H / 2 - (np.arange(h) + 0.5) / h * H
        bottom = np.clip((y + 2.62) / 0.5, 0, 1)                 # the caption band (y < -2.8) dims ...
        top = np.clip((3.3 - y) / 0.35, 0, 1)                    # ... and the HUD band (y > 3.36)
        return (1 - k * (1 - 0.42 * (1 - bottom) - bottom)) * (1 - k * (1 - 0.5 * (1 - top) - top))

    def galaxy_families(self, t: float, put):
        G, rh = gcam(t), rho(t)
        on = self.galaxy_on(t)
        zf = zfac(G[2]) * on
        dim = 1 - 0.45 * ease_in_out_sine(seg(t, RING_A, RING_A + 0.5)) * (1 - ease_in_out_sine(seg(t, *COLLAPSE)))
        # the leaves: in S07's bars, flying, or in the galaxy
        gal = gal_screen(L_TH, L_R, G, rh)
        if t < FLY[1]:
            e = np.clip((t - FLY_T0) / FLY_DUR, 0, 1)
            e = np.where(e < 0.5, 4 * e ** 3, 1 - (-2 * e + 2) ** 3 / 2)
            shim = 1 + 0.12 * np.sin(SHIMMER_PH + 2.3 * (S07_END + t))
            w = (BAR_W * shim * (1 - e) + L_WEIGHT * zf * e)
            P = self.flight(e)
            for f in range(3):
                sel = L_FAM == f
                put(f, P[sel], w[sel])
            moving = (e > 0.02) & (e < 0.98)
            if moving.any():                                   # a short motion-blur trail
                for lag, k in ((0.03, 0.45), (0.06, 0.2)):
                    e2 = np.clip((t - lag - FLY_T0[moving]) / FLY_DUR, 0, 1)
                    e2 = np.where(e2 < 0.5, 4 * e2 ** 3, 1 - (-2 * e2 + 2) ** 3 / 2)
                    P2 = self.flight(e2, moving)
                    w2 = w[moving] * k
                    for f in range(3):
                        sel = L_FAM[moving] == f
                        put(f, P2[sel], w2[sel])
        else:
            w = L_WEIGHT * zf * dim
            flare = 1 + 0.35 * pulse(t, READY, 0.5) if t >= READY else 1.0
            for f in range(3):
                sel = L_FAM == f
                put(f, gal[sel], w[sel] * flare)
        # the dust (internal nodes): grey until the wave reaches its ring, then the best result's colour
        dust_in = ease_in_out_sine(seg(t, FLY[0] + 0.5, FLY[1] + 0.1))
        if dust_in > 1e-3:
            bright = 1 + 0.3 * ease_out_cubic(seg(t, READY, READY + 0.4))
            P = gal_screen(N_TH[D_IDX], N_R[D_IDX], G, rh)
            tcol = np.array([WAVE_T.get(int(d), 1e9) for d in range(10)])[D_RING]
            col = t >= tcol
            fl = np.where(col, 1 + 2.0 * np.exp(-np.maximum(t - tcol, 0) / 0.35), 1.0)
            w = D_BASE * zf * dust_in * bright * np.where(col, RING_BOOST[D_RING], 1.0) * fl * dim
            put(3, P[~col], w[~col])
            for v, f in ((1, 0), (2, 1), (3, 2)):
                sel = col & (D_VAL == v)
                if sel.any():
                    put(f, P[sel], w[sel])

    def flight(self, e: np.ndarray, sel=None) -> np.ndarray:
        """The points on their way from S07's bars to their leaves (an arc, the same sense for all)."""
        a = BAR_XY if sel is None else BAR_XY[sel]
        b = gal_screen(L_TH if sel is None else L_TH[sel], L_R if sel is None else L_R[sel], G_FULL, RHO0)
        d = b - a
        nrm = np.column_stack([d[:, 1], -d[:, 0]])
        return a + d * e[:, None] + nrm * (0.16 * np.sin(np.pi * e))[:, None]

    # --- the tree's inner structure: edges, root, the wave front and its label
    def update_tree(self, t: float):
        G, rh = gcam(t), rho(t)
        on = self.galaxy_on(t)
        out = 1 - seg(t, COLLAPSE[0], COLLAPSE[0] + 0.5)
        ev = ease_in_out_sine(seg(t, READY - 0.2, READY + 0.4)) * out
        if ev > 1e-3:
            pc = gal_screen(N_TH[EDGE_CHILD], N_R[EDGE_CHILD], G, rh)
            pp = gal_screen(N_TH[EDGE_PARENT], N_R[EDGE_PARENT], G, rh)
            pp[N_DEPTH[EDGE_CHILD] == 1] = [G[0], G[1]]
            dim = 1 - 0.4 * ease_in_out_sine(seg(t, RING_A, RING_A + 0.5))
            self.edges.set_segments(pp, pc, opacity=0.36 * ev * dim)
            k = min(G[2], 1.5)
            for j, i in enumerate(EDGE_CHILD):
                d = int(N_DEPTH[i])
                t0 = WAVE_T[d]
                done = t >= t0
                col = VAL_HEX[int(N_VAL[i])] if done else INK_DIM
                fl = pulse(t, t0, 0.35) if done else 0.0
                self.node_core[j].move_to([*pc[j], 0]).set(width=2 * 0.017 * k * (1 + 0.6 * fl))
                self.node_core[j].set_fill(col, opacity=clamp01(ev * dim * (0.55 + 0.45 * done + 0.3 * fl)))
                self.node_glow[j].move_to([*pc[j], 0]).set(width=2 * 0.05 * k * (1 + 0.8 * fl))
                self.node_glow[j].set_fill(col, opacity=clamp01(ev * dim * (0.18 * done + 0.35 * fl)))
        else:
            self.edges.set_segments([], [])
            for d in self.node_core + self.node_glow:
                d.set_fill(opacity=0)
        # the root: white at 82.1, grey at 87.1 (a soft flare), breathing
        rv = ease_out_cubic(seg(t, READY - 0.15, READY + 0.2)) * out
        if rv > 1e-3:
            grey = ease_in_out_sine(seg(t, ROOT_GREY, ROOT_GREY + 0.35))
            col = hex_of(rgb(WHITE) * (1 - grey) + rgb("#C8CCCC") * grey)
            fl = (pulse(t, READY, 0.5) if t >= READY else 0) + (0.9 * pulse(t, ROOT_GREY, 0.6) if t >= ROOT_GREY else 0)
            br = 1 + 0.12 * math.sin(2 * math.pi * (t - READY) / BAR)
            k = min(G[2], 1.5)
            hw = (0.5 + 0.3 * fl) * k * br
            show_sprite(self.root_halo, (G[0], G[1]), hw, hw, clamp01((0.75 - 0.25 * grey + 0.5 * fl) * rv))
            B = self.root_board.place((G[0], G[1]), min(G[2], 1.0))
            for ln in B.lines:
                ln.set_core_color(col)
            B.draw_grid(1.0, vis=rv * (0.95 - 0.25 * grey), width=0.8)
        else:
            show_sprite(self.root_halo, opacity=0)
            self.root_board.hide()
        # the wave front and its label (83.1-86.4)
        fv = ease_in_out_sine(seg(t, WAVE_START - 0.3, WAVE_START + 0.3)) * (1 - seg(t, WAVE_T[1] + 0.2, ROOT_GREY))
        if fv > 1e-3:
            R = front_radius(t) * G[2]
            self.front.show(1.0, np.eye(2) * R, (G[0], G[1]), vis=0.5 * fv, glow=0.9)
        else:
            self.front.hide()
        lv = ease_in_out_sine(seg(t, WAVE_T[8] - 0.3, WAVE_T[8] + 0.1)) * (1 - seg(t, WAVE_T[1] + 0.4, ROOT_GREY))
        if lv > 1e-3:
            reached = [d for d, tt in WAVE_T.items() if t >= tt]
            ring = min(reached) if reached else 8                  # the ring the front is on
            which = 0 if ring % 2 == 0 else 1                      # X to move on even rings
            t_in = WAVE_T[ring] if ring != 8 else -1.0
            t_next = WAVE_T.get(ring - 1, 1e9)
            a_in = ease_out_cubic(seg(t, t_in, t_in + 0.16))       # the next label comes in just after its ring's
            a_out = 1 - seg(t, t_next - 0.16, t_next - 0.02)       # time, once the last one has gone
            anchor = np.array([6.42, 2.62])
            for j, lb in enumerate(self.wave_lab):
                if j == which:
                    lb.show(anchor + np.array([0.0, -0.05 * (1 - a_in)]), "r", lv * a_in * a_out)
                else:
                    lb.hide()
            th = math.radians(42) + rh
            R = front_radius(t) * G[2]
            p = np.array([G[0] + R * math.sin(th), G[1] + R * math.cos(th)])
            q = anchor - np.array([self.wave_lab[which].width + 0.12, 0.08])
            A, c = line_affine(q, p)
            self.wave_leader.show(1.0, A, c, vis=0.55 * lv)
        else:
            for lb in self.wave_lab:
                lb.hide()
            self.wave_leader.hide()

    # --- game A: its leaf ringed, its path lit back to the root, the inset (bars 88-89)
    def update_game_a(self, t: float):
        G, rh = gcam(t), rho(t)
        out = 1 - ease_in_out_sine(seg(t, COLLAPSE[0], COLLAPSE[0] + 0.45))
        pts = gal_screen(np.array(GA_TH), np.array(GA_R), G, rh)
        lv = ease_out_cubic(seg(t, RING_A, RING_A + 0.35)) * out
        if lv > 1e-3:
            br = 1 + 0.15 * math.sin(2 * math.pi * (t - RING_A) / BAR)
            self.leaf_ring.show(ease_out_cubic(seg(t, RING_A, RING_A + 0.35)), np.eye(2) * 0.085 * G[2], pts[5],
                                vis=lv, glow=br + 0.8 * pulse(t, RING_A, 0.4))
        else:
            self.leaf_ring.hide()
        for j in range(5):                                     # edge j joins node j and node j+1; lit leaf-first
            ink = self.path[j]
            t0 = PATH_T[4 - j]
            f = ease_out_cubic(seg(t, t0, t0 + 0.22))
            if f <= 1e-3 or out <= 1e-3:
                ink.hide()
                continue
            A, c = line_affine(pts[j + 1], pts[j + 1] + (pts[j] - pts[j + 1]) * f)
            red = j == 1 and t >= INSET_IN
            ink.show(1.0, A, c, vis=out * (0.0 if red else 0.9), glow=1.0 + 0.8 * pulse(t, t0, 0.3))
            if j == 1:
                rv = ease_out_cubic(seg(t, INSET_IN, INSET_IN + 0.25)) * out
                if rv > 1e-3:
                    A, c = line_affine(pts[2], pts[1])
                    self.path_red.show(1.0, A, c, vis=rv, glow=1.0 + 0.8 * pulse(t, INSET_IN, 0.4))
                else:
                    self.path_red.hide()
        if t < PATH_T[3] or out <= 1e-3:
            self.path_red.hide()
        for j, sp in enumerate(self.path_dots):                # the path's nodes, in their perfect-play colours
            t0 = PATH_T[4 - min(j, 4)] if j < 5 else RING_A
            v = ease_out_cubic(seg(t, t0, t0 + 0.2)) * out
            fl = pulse(t, t0, 0.35) if t >= t0 else 0.0
            show_sprite(sp, pts[j], (0.16 + 0.1 * fl) * G[2], (0.16 + 0.1 * fl) * G[2], clamp01((0.7 + 0.6 * fl) * v))
        # the inset
        iv = ease_out_cubic(seg(t, INSET_IN, INSET_IN + 0.3)) * out
        B = self.inset.place(self.inset_c + np.array([0.0, -0.06 * (1 - iv)]), 1.0)
        if iv <= 1e-3:
            B.hide()
            self.red_o.hide()
            show_sprite(self.centre_glow, opacity=0)
            self.lab_mistake.hide()
            self.lab_centre.hide()
            self.inset_leader.hide()
            return
        B.draw_grid(1.0, vis=iv)
        xs = [0] + [s for s, tt in ((1, PLAY_ON[0]), (2, PLAY_ON[2])) if t >= tt]
        fx = [1.0] + [ease_out_cubic(seg(t, tt, tt + 0.25)) for s, tt in ((1, PLAY_ON[0]), (2, PLAY_ON[2])) if t >= tt]
        vx = [iv] + [0.5 * iv] * (len(xs) - 1)
        os_ = [4] if t >= PLAY_ON[1] else []
        B.draw_marks(xs, os_, vis_x=vx, vis_o=0.5 * iv, f_x=fx, f_o=[ease_out_cubic(seg(t, PLAY_ON[1], PLAY_ON[1] + 0.25))],
                     glow_x=[1.0 + 0.6 * pulse(t, INSET_IN, 0.4)] + [0.5] * (len(xs) - 1), glow_o=0.5)
        self.red_o.show(ease_out_cubic(seg(t, INSET_IN, INSET_IN + 0.25)), np.eye(2), B.sq(3), vis=iv,
                        glow=1.0 + 0.9 * pulse(t, INSET_IN, 0.45))
        if t >= WIN_IN:
            B.win.set_core_color(XC.mid)
            B.draw_win((0, 1, 2), ease_out_quad(seg(t, WIN_IN, WIN_IN + 0.5)), vis=0.5 * iv, glow=0.7)
        else:
            B.win.hide()
        cv = ease_out_cubic(seg(t, CENTRE_IN, CENTRE_IN + 0.3)) * iv * (1 - 0.7 * seg(t, PLAY_ON[1], PLAY_ON[1] + 0.3))
        br = 1 + 0.15 * math.sin(2 * math.pi * (t - CENTRE_IN) / BAR)
        show_sprite(self.centre_glow, B.sq(4), 0.62 * br, 0.62 * br, clamp01(0.55 * cv * br))
        top = self.inset_c[1] + 1.5 * 0.52 + 0.36
        self.lab_mistake.show([self.inset_c[0], top - 0.05 * (1 - iv)], "c", iv)
        lc = ease_out_cubic(seg(t, CENTRE_IN, CENTRE_IN + 0.35)) * out
        self.lab_centre.show([self.inset_c[0], self.inset_c[1] - 1.5 * 0.52 - 0.58 - 0.05 * (1 - lc)], "c", lc)
        m = (pts[1] + pts[2]) / 2
        q = self.inset_c + np.array([-1.5 * 0.52 - 0.18, 0.0])
        A, c = line_affine(m + (q - m) * 0.06, q)
        self.inset_leader.show(ease_out_cubic(seg(t, INSET_IN, INSET_IN + 0.35)), A, c, vis=0.5 * iv)

    # --- the strips, the pen and its arm (bars 90-98)
    def update_strips(self, t: float):
        S = self.strips
        if t < TTT_T[0] - 0.3:
            S.hide_all()
            self.pen.place((0, 0), 0)
            self.arm.hide()
            return
        v = strip_view(t)
        L = S.draw(t, v, glow=1.0 + 0.6 * pulse(t, HIT, 0.6) if t >= HIT else 1.0)
        S.draw_labels(t, L, v)
        if t >= PEN_IN:
            pv = ease_out_cubic(seg(t, PEN_IN, PEN_IN + 0.3))
            x, y = pen_x(t, v["z"]), v["rows"]["chess"]
            self.pen.place((x, y), pv, glow=pen_glow(t))
            av = ease_in_out_sine(seg(t, *ARM_IN)) * (1 - 0.6 * ease_in_out_sine(seg(t, LIT_T[-1], STALL)))
            A = np.diag([1.0, 0.56])
            self.arm.show(1.0, A, (x, y), vis=0.3 * av, glow=0.7)
        else:
            self.pen.place((0, 0), 0)
            self.arm.hide()

    # --- the HUD: §4 (S07) -> §5 at the segue, §5 -> §6 at 90.1; S07's readout fades
    def update_hud(self, t: float):
        m = (SEC_SWAP[0] + SEC_SWAP[1]) / 2
        out4 = 1 - ease_in_out_sine(seg(t, SEC_SWAP[0], m))
        in5 = ease_in_out_sine(seg(t, m, SEC_SWAP[1]))
        out5 = 1 - ease_in_out_sine(seg(t, SEC6, SEC6 + 0.25))
        in6 = ease_in_out_sine(seg(t, SEC6 + 0.25, SEC6 + 0.5))
        for (sec, c), v in zip(self.secs, (in5 * out5, in6)):
            sec.show(c, vis=v)
        if self.s07_on:                                         # (faded to nothing from S07_GONE, then removed)
            self.s07.draw(S07_END + min(t, S07_GONE), 1 - ease_in_out_sine(seg(t, *LABELS_OUT)), out4)

    # ------------------------------------------------------------- the sounds (from the same numbers)
    def score(self):
        S = self.sounds
        rx = lambda t: float(gcam(t)[0])
        # 81.3-82.1: the flight back into the galaxy (a soft granular sweep); 82.1 a single held bell: the root
        S.effect(FLY[0], "shimmer", FLY[1] - FLY[0] + 0.8, x=-1.0)
        S.phrase("root", [(READY, "bell@D5", rx(READY))], gain=0.7)
        # 83-86: the wave, one note per ring, falling: a bell on X's turns, glass on O's, each a chord tone
        # (83 E9 · 84 F#m9 · 85 Bm9 · 86 Asus4)
        notes = {8: "B5", 7: "G#5", 6: "E5", 5: "C#5", 4: "A4", 3: "F#4", 2: "E4", 1: "D4"}
        th = math.radians(42)
        S.phrase("wave", [(WAVE_T[d], f"{'X' if d % 2 == 0 else 'O'}@{notes[d]}",
                           float(gcam(WAVE_T[d])[0] + ring_radius(d) * gcam(WAVE_T[d])[2] * math.sin(th + rho(WAVE_T[d]))))
                          for d in range(8, 0, -1)], gain=0.8)
        # 87.1: the grey root, a draw (a wooden pluck; video.yaml's section cue brings the open fifth and the thump)
        S.phrase("grey root", [(ROOT_GREY, "draw@D4", rx(ROOT_GREY))], gain=0.75)
        # 88.1: game A's leaf is ringed and its path lights back to the root: its five notes backwards, on sixteenths
        pts = lambda t: gal_screen(np.array(GA_TH), np.array(GA_R), gcam(t), rho(t))
        S.phrase("path back", [(PATH_T[4 - j], tag(player(j), GAME_A[j]), float((pts(PATH_T[4 - j])[j] +
                                                                                 pts(PATH_T[4 - j])[j + 1])[0] / 2))
                               for j in range(5)], gain=0.55)
        # 88.3: the RED tag: a short reverse whoosh and a rub (F natural against Bm9's F#) that resolves up;
        # 88.4: the centre glows, a draw's pluck at the centre square's pitch
        ix = float(self.inset_c[0])
        S.effect(INSET_IN, "whoosh_rev", 0.4, ix)
        S.phrase("mistake", [(INSET_IN, "glass@F5", ix), (INSET_IN + 0.3, "glass@F#5", ix)], gain=0.6)
        S.phrase("centre", [(CENTRE_IN, f"draw@{PITCH[4]}", ix)], gain=0.6)
        # 89.1-89.3: the inset plays on, faintly: the motif's last three notes, then X's top row (a faint win run)
        S.phrase("play on", [(tt, tag(player(k), GAME_A[k]), ix) for k, tt in zip((2, 3, 4), PLAY_ON)], gain=0.45)
        S.phrase("faint win", [(WIN_IN + 0.15 * j, f"X@{n}", ix) for j, n in enumerate(("C#6", "D6", "E6"))], gain=0.3)
        # 90.1: the galaxy shrinks into a box (a pull-out); its six boxes, then every chess box a tick, accelerating
        S.effect(COLLAPSE[0], "whoosh_down", COLLAPSE[1] - COLLAPSE[0], x=-3.0)
        S.phrase("ttt strip", [(tt, "tick", float(box_x(j, zs(tt)))) for j, tt in enumerate(TTT_T)], rise=True, gain=0.8)
        S.phrase("chess strip", [(tt, "tick", float(box_x(j, zs(tt)))) for j, tt in enumerate(CHESS_T)], rise=True)
        # 94: the atoms' run, softer; 95.1 a low bell
        S.phrase("atoms strip", [(tt, "tick", float(box_x(j, zs(tt)))) for j, tt in enumerate(ATOMS_T)], rise=True,
                 gain=0.55)
        S.phrase("atoms bell", [(ATOMS[1], "bell@B3", float(box_x(80, zs(ATOMS[1]))))], gain=0.8)
        # 96-98: the note (a soft pluck); the pen's soft pulse; a ping per box it lights (F#9's tones, rising); its
        # thin grain; the stall: the pen pulses on the beats of bar 98
        # (bars 96-97 are F#9: F# A# C# E G#, so the pluck and the pen's first pulses sit on its tones; bar 98 is
        # Emaj9, where the stalled pen pulses on its fifth, B4)
        S.phrase("note", [(NOTE_IN, "pluck@F#3", 0.0)], gain=0.35)
        S.phrase("pen", [(bb(96, b), "pen@C#5", XL) for b in (1, 2)]
                 + [(bb(98, b), "pen@B4", float(box_x(5, zs(bb(98, b))))) for b in (1, 2, 3, 4)], gain=0.6)
        S.phrase("lit", [(tt, f"pen@{n}", float(box_x(j, zs(tt))))
                         for j, (tt, n) in enumerate(zip(LIT_T, ("F#5", "G#5", "A#5", "C#6", "E6", "F#6")))], gain=0.75)
        tones = ("C#6", "E6", "F#6", "G#6", "A#6")
        grains = []
        for k in range(int((LIT_T[-1] + 0.3 - PEN_IN) / 0.15)):
            tt = PEN_IN + 0.15 * k
            grains.append((tt, f"glass@{tones[(k * 3 + k // 5) % 5]}", pen_x(tt, zs(tt))))
        S.phrase("pen grain", grains, gain=0.18)
        S.log(self)

    # ------------------------------------------------------------- the logged events and the clock
    def log_events(self):
        ev = self.shots

        def add(t, dur, x, y, w, h):
            ev.append((float(t), float(dur), (float(x), float(y), float(w), float(h))))
        add(0.0, 2 * BEAT, -4.0, 0.66, 3.5, 1.6)                                 # S07's bars shimmer
        add(LABELS_OUT[0], 0.3, -1.0, 1.0, 9.6, 2.6)                             # its labels, the ruler, Σ fade
        add(FLY[0], FLY[1] - FLY[0], -1.0, 0.8, 9.0, 6.0)                        # the flight
        add(READY, BEAT, *G_FULL[:2], 1.2, 1.2)                                  # the root lights
        add(READY + BEAT, 3 * BEAT, *G_FULL[:2], 5.8, 5.8)                       # a slow drift, the dust
        for k in range(16):                                                      # 83-86: the wave and the push-in
            t = bb(83) + k * BEAT
            g = gcam(t)
            add(t, BEAT, g[0], g[1], 5.8 * g[2], 5.8 * g[2])
        for d, tt in WAVE_T.items():
            g = gcam(tt)
            add(tt, 0.4, g[0], g[1], 2 * ring_radius(d) * g[2], 2 * ring_radius(d) * g[2])
        add(ROOT_GREY, BEAT, *gcam(ROOT_GREY)[:2], 0.8, 0.8)
        for k in range(1, 4):
            add(ROOT_GREY + k * BEAT, BEAT, *gcam(ROOT_GREY)[:2], 4.0, 4.0)      # the grey root breathes; slow turn
        P = gal_screen(np.array(GA_TH), np.array(GA_R), gcam(RING_A), rho(RING_A))
        add(RING_A, 0.35, *P[5], 0.3, 0.3)
        for j in range(5):
            add(PATH_T[4 - j], 0.22, *((P[j] + P[j + 1]) / 2), 0.6, 0.6)
        add(INSET_IN, 0.3, *self.inset_c, 2.2, 2.6)
        add(CENTRE_IN, 0.35, *self.inset_c, 2.2, 1.6)
        for tt in PLAY_ON:
            add(tt, 0.3, *self.inset_c, 0.6, 0.6)
        add(WIN_IN, 0.5, *self.inset_c, 1.6, 0.3)
        add(bb(89, 4), BEAT, -1.0, 0.0, 6.0, 6.0)
        add(COLLAPSE[0], COLLAPSE[1] - COLLAPSE[0], -3.0, 0.3, 8.0, 7.0)         # the galaxy shrinks into a box
        for tt in TTT_T:
            add(tt, 0.075, *BOX1_C0, 0.3, 0.3)
        for k in range(int(round((HIT - CHESS0) / BEAT))):                        # the chess strip runs
            t = CHESS0 + k * BEAT
            add(t, BEAT, 0.0, -0.3, 12.0, 2.0)
        add(HIT, BEAT, 0.0, 0.5, 13.0, 4.5)                                       # the climax, the labels
        add(HIT + BEAT, 3 * BEAT, 0.0, 0.5, 12.0, 4.0)                            # a slow drift
        for k in range(4):
            add(ATOMS[0] + k * BEAT, BEAT, -2.0, 0.7, 8.0, 1.2)                   # the atoms strip runs
        add(ATOMS[1], BEAT, 1.0, 0.9, 10.0, 1.4)
        add(ATOMS[1] + BEAT, 3 * BEAT, 0.0, 0.5, 12.0, 4.0)
        add(NOTE_IN, 2 * BEAT, 0.0, -1.85, 9.3, 0.3)
        for tt in LIT_T:
            add(tt, 0.35, float(box_x(LIT_T.index(tt), zs(tt))), -0.85, 0.4, 0.8)
        for b in (1, 2, 3, 4):
            add(bb(98, b), 0.3, float(box_x(5, zs(bb(98, b)))), -0.85, 0.4, 0.8)
        add(GRAIN[0], GRAIN[1] - GRAIN[0], 1.0, -0.85, 10.5, 0.5)

    def run(self):
        self.log_events()
        self.shots = [(a, min(d, END - a), bx) for a, d, bx in self.shots if a < END - 1e-6]
        steps = sorted({round(t, 4) for t, _, _ in self.shots})
        steps = sorted(set(steps) | {round(S07_GONE, 4)})
        for i, t in enumerate(steps):
            nxt = steps[i + 1] if i + 1 < len(steps) else END
            self.until(f"{t:.4f}s")
            if self.s07_on and t >= S07_GONE - 1e-6:          # S07's objects have faded: out of the scene
                self.s07_on = False
                gone = self.s07.mobjects_to_show
                self.unfix(*gone)
                self.remove(*gone)
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
