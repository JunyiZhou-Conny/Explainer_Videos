"""S05 · Play every game 探索每一局 — ★1, the search lights all 255,168 games (the galaxy).

Bars 41-61 (1:36.0-2:26.4) of script.md. As in S01 (the reference scene), the picture is a pure function of
the scene time (`update_state`), and the notes are computed from the same numbers (Sounds), each with its
own tag ("X@C#5": an X bell at its square's pitch). The galaxy is all 255,168 leaves and 294,778 internal
nodes of the real game tree, splatted with numpy into one image per frame (`Splatter`), never as mobjects.

    41     41.1 the knot from S04 snaps (one flash frame); its threads straighten and vanish, leaving the
           root at (-2.0, +0.3); 41.2-41.4 the program plate fades in at the left edge          (c14)
    42     the light pen appears on the root and pulses on the beats; the camera pushes in
    43-44  the pen walks the program's first game, one move per beat, X0 O1 X2 O3 X4 O5 X6, an edge
           behind it, the inset board beside it; 44.3 X's 2-4-6 diagonal, leaf 1 lights cyan on ring 7;
           44.4 a dashed ghost stub tries to go on and is cut off by a stop bar          (the motif of the walk)
    45-46  RED undo, X7 O6 X8 -> leaf 2 (ring 9); undo, undo, O8 X6 -> leaf 3                  (c15)
    47-48  twice as fast: leaf 4 (move 7), leaf 5 (move 9), leaf 6: the first draw, grey-white  (c16)
    49-50  the walk accelerates through the first wedge (games 7 ... 27,732): sixteenths, then faster
           than the eye; the camera pulls out (49.1-53.1); 50.3-50.4 the plate's tags: 递归 / RECURSION,
           回溯 / BACKTRACKING; 51.1 the counter crosses 27,732 on the downbeat
    51-53  the sweep: a faint arm turns clockwise one first-move wedge (40°) per bar; the counter on the
           downbeats 57,324 · 85,056 · 114,648                                                   (c17)
    54-58  12 s without words: wedges 5-9; CALLS and UNDOS run live; a slow rotation; 58.4+ half a beat
           of darkness as the arm reaches 12 o'clock
    59     59.1 LANDING: one flash frame, the galaxy flares; 255,168 on the right third, set like the
           title (cool left, warm right); CALLS 549,946, UNDOS 549,945                           (c18)
    60-61  the galaxy turns, the camera eases in towards the inner rings; 61.1-61.3 the number docks back
           into the HUD readout

Geometry (script.md "The tree"): root (-2.0, +0.3); ring d at r_d = 2.9 (d/9)^0.75; every node splits its
wedge equally among its children, clockwise in square order from 12 o'clock, so a game that ends after k
moves owns (9 - k)! of the 9! slots, and the program's depth-first order is the clockwise order. The
first six games are walked in a local magnifier (`LENS`): their tiny subtree (8 of the 362,880 slots) is
spread out sideways so it reads as a tree, and the magnifier relaxes into the true geometry as the
camera pulls out (49.1-50.2). The counter is the number of leaves whose slot the sweep has passed, so it
passes exactly through the running totals at the wedge boundaries.

Hand-over from S04 (a cut at 41.1, with the flash): S04 ends on the knot alone, centred on screen at
(0, 0.3); this scene's camera starts centred on (-2.0, 0.0), frame 14.22 wide, so the root lands where
the knot was.
Hand-over to S06 (a segue at 62.1). At 62.1 (this scene's END):
  - camera: CAM(END) = (centre x, centre y, width), see `cam_path` (root on screen at about (-1.0, 0.27),
    zoom 1.10);
  - the galaxy: all 255,168 leaves lit (`Splatter` weights below, tone-mapped with headroom), turned
    clockwise about the root by ROT(END) (0.35°/s since 53.1, about 6.5°), dust on rings 0-8, edges of
    rings 1-2; the pen on the root, pulsing on the beats;
  - the plate at the left edge (screen space, `ProgramPlate`), dimmed to PLATE_DIM;
  - HUD: §3 top left; top right "对局计数 · GAMES COUNTED 255,168", "调用次数 · CALLS 549,946",
    "撤销次数 · UNDOS 549,945".
"""

from __future__ import annotations

import math
from math import factorial

import numpy as np
from manim import RIGHT, Dot, Line, Mobject, Rectangle, Text, VGroup, VMobject, config

from explainer.short import BeatScene, FONT_MONO, INK, INK_DIM, RED, WHITE, cjk, stroke_px

from common import (GALAXY_COLOURS, GALAXY_DUST_W, GALAXY_LOOK, GALAXY_SLOT_W, HUD_LINES_Y, FastCamera,
                    FrameImage, HudLine, ProgramPlate, PLATE_TL, Splatter, TREE_ROOT, counter_glyphs, cull,
                    galaxy_point, galaxy_tree, hud_label, section_hud, show_sprite, uncull)
from common import (OC, PEN, PEN_HALO, PITCH, XC, Cam, Pen, Shot, Sounds, W, box, clamp01,
                    ease_in_cubic, ease_in_out_cubic, ease_in_out_sine, ease_out_cubic, ease_out_quad,
                    final_glyphs, gaussian_sprite, grid_lines, lerp, o_template, player, pulse, rgb, seg,
                    square_centre, tag, title_counter, x_template)
from s04_by_hand import (EN_SIZE, ZH_SIZE, Ink, InkText, Label, MiniBoard, Thread, en, hex_of, line_affine,
                         line_ink, win_ends, zh_en)
from s04_by_hand import END as S04_END
from s04_by_hand import knot_screen

# ---------------------------------------------------------------- the plan's clock
BEAT, BAR = 0.6, 2.4
FIRST = 41


def bb(bar: int, beat: float = 1.0) -> float:
    """Scene time of script.md's "bar.beat" (global bar numbers): bb(47, 2.5) is "47.2+"."""
    return (bar - FIRST) * BAR + (beat - 1) * BEAT


END = bb(62)                                      # 50.4 s: 21 bars

# ---------------------------------------------------------------- the game tree (the program's real search)
WIN_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
FACT = [factorial(9 - k) for k in range(10)]      # slots owned by a node after k moves
N_SLOTS = factorial(9)
ROOT = np.asarray(TREE_ROOT, dtype=float)
RING = np.array([2.9 * (d / 9) ** 0.75 for d in range(10)])


_T = galaxy_tree()                                # common.GalaxyTree: the program's search, in its order
L_SLOT, L_MOVES, L_RES, N_SLOT, N_DEPTH = _T.l_slot, _T.l_moves, _T.l_res, _T.n_slot, _T.n_depth
L_K, L_LAST = _T.l_k, _T.l_last
N_GAMES = len(L_SLOT)
ALL_STARTS = _T.all_starts                        # every explore() call, by where it starts
assert np.allclose(ROOT, TREE_ROOT)
WEDGE_END = [int((L_SLOT < (k + 1) * FACT[1]).sum()) for k in range(9)]
assert N_GAMES == 255_168 and len(ALL_STARTS) == 549_946
assert WEDGE_END == [27_732, 57_324, 85_056, 114_648, 140_520, 170_112, 197_844, 227_436, 255_168]
assert [int((L_K == k).sum()) for k in range(5, 10)] == [1_440, 5_328, 47_952, 72_576, 127_872]
assert int((L_RES == 1).sum()) == 131_184 and int((L_RES == 2).sum()) == 77_904 and int((L_RES == 3).sum()) == 46_080
assert sum(FACT[k] * int((L_K == k).sum()) for k in range(5, 10)) == N_SLOTS     # the leaves tile the circle
_ga = np.flatnonzero((L_MOVES[:, :5] == (0, 3, 1, 4, 2)).all(axis=1) & (L_K == 5))[0]
assert _ga + 1 == 7_317 and L_SLOT[_ga] == 10_200 and abs(L_SLOT[_ga] / N_SLOTS * 360 - 10.119) < 1e-3  # game A
FIRST_SIX = [tuple(int(x) for x in L_MOVES[i, :L_K[i]]) for i in range(6)]
assert FIRST_SIX == [(0, 1, 2, 3, 4, 5, 6), (0, 1, 2, 3, 4, 5, 7, 6, 8), (0, 1, 2, 3, 4, 5, 7, 8, 6),
                     (0, 1, 2, 3, 4, 5, 8), (0, 1, 2, 3, 4, 6, 5, 7, 8), (0, 1, 2, 3, 4, 6, 5, 8, 7)]
assert list(L_RES[:6]) == [1, 1, 1, 1, 1, 3]                    # game 6 is the first draw

# ---------------------------------------------------------------- the walk (bars 43-48): every move and undo
WALK_TIMES = ([bb(43, b) for b in (1, 2, 3, 4)] + [bb(44, b) for b in (1, 2, 3)]                 # game 1
              + [bb(45, b) for b in (1, 2, 3, 4)]                                                # game 2
              + [bb(46, b) for b in (1, 2, 3, 4)]                                                # game 3
              + [bb(47, b) for b in (1, 1.5, 2, 2.5)]                                            # game 4
              + [bb(47, b) for b in (3, 3.5, 4, 4.5)] + [bb(48, b) for b in (1, 1.5)]            # game 5
              + [bb(48, b) for b in (2, 2.5, 3, 3.5)])                                           # game 6


def walk_events():
    """(time, kind, path after the event) for every move and undo of the first six games: a move adds
    one square, an undo erases the last one (the RED eraser)."""
    ev, path = [], ()
    times = iter(WALK_TIMES)
    for leaf in FIRST_SIX:
        k = 0
        while k < min(len(path), len(leaf)) and path[k] == leaf[k]:
            k += 1
        while len(path) > k:
            path = path[:-1]
            ev.append((next(times), "undo", path))
        while len(path) < len(leaf):
            path = path + (leaf[len(path)],)
            ev.append((next(times), "move", path))
    assert next(times, None) is None
    return ev


WALK = walk_events()
assert [k for _, k, _ in WALK].count("undo") == 1 + 2 + 3 + 2 + 2
LEAF_T = [t for t, k, p in WALK if k == "move" and p in FIRST_SIX]                    # when each leaf lights
assert [round(t, 2) for t in LEAF_T] == [round(x, 2) for x in (bb(44, 3), bb(45, 4), bb(46, 4), bb(47, 2.5),
                                                                bb(48, 1.5), bb(48, 3.5))]
STUB_T = bb(44, 4)

# the lens: the first six games' subtree drawn as a tidy tree, leaves 1-6 spread sideways (world units of
# arc), each internal node above the mean of its leaves; nodes the walk does not visit inherit the offset
# of their deepest visited ancestor. Only nodes under X0 O1 X2 O3 X4 (slots 0-23) move.
LENS_K = 0.5
LENS = {}
for _r, _leaf in enumerate(FIRST_SIX):
    for _d in range(len(_leaf) + 1):
        LENS.setdefault(_leaf[:_d], []).append(LENS_K * (_r + 1 - 3.5) / 2)
LENS = {p: (float(np.mean(v)) if len(p) >= 5 else 0.0) for p, v in LENS.items()}


def lens_dx(moves) -> float:
    m = tuple(int(x) for x in moves if x >= 0)
    for d in range(len(m), -1, -1):
        if m[:d] in LENS:
            return LENS[m[:d]]
    return 0.0


def slot_path(slot: int, depth: int) -> tuple:
    """The moves that lead to the node at (slot start, depth): the inverse of node_slot."""
    out, left = [], list(range(9))
    for d in range(depth):
        k = (int(slot) // FACT[d + 1]) % (9 - d)
        out.append(left.pop(k))
    return tuple(out)


def node_slot(path) -> int:
    """Slot start of the node reached by `path` (each child owns FACT[depth] slots)."""
    s, b = 0, set()
    for d, sq in enumerate(path):
        k = sum(1 for q in range(sq) if q not in b)
        s += k * FACT[d + 1]
        b.add(sq)
    return s


# ---------------------------------------------------------------- the frontier: how far the search is at time t
T49, T51, T59 = bb(49), bb(51), bb(59)
SWEEP_RATE = FACT[1] / BAR                        # one first-move wedge (40 320 slots) per bar
DISCRETE = [T49 + 0.15 * j for j in range(4)]     # games 7-10 on sixteenths (49.1 ...)


def _profile():
    """The acceleration of bars 49-50 as a table (t, s): the log of the speed rises smoothly from about
    one game per sixteenth to a peak, then settles on the sweep's speed exactly at 51.1, having covered
    exactly the first wedge."""
    t0, t1 = DISCRETE[-1] + 0.15, T51
    s0 = float(L_SLOT[10])                        # game 11
    r0 = (float(L_SLOT[11]) - s0) / 0.15
    u = np.linspace(0, 1, 6001)

    def rates(lp):
        a = np.where(u < 0.78, math.log(r0) + (lp - math.log(r0)) * _ss(u / 0.78),
                     lp + (math.log(SWEEP_RATE) - lp) * _ss((u - 0.78) / 0.22))
        return np.exp(a)

    def cover(lp):
        r = rates(lp)
        return float(np.sum((r[1:] + r[:-1]) / 2) * (t1 - t0) / (len(u) - 1))
    lo, hi = math.log(SWEEP_RATE), math.log(SWEEP_RATE) + 6
    for _ in range(80):
        mid = (lo + hi) / 2
        if cover(mid) < FACT[1] - s0:
            lo = mid
        else:
            hi = mid
    r = rates((lo + hi) / 2)
    s = s0 + np.concatenate([[0.0], np.cumsum((r[1:] + r[:-1]) / 2) * (t1 - t0) / (len(u) - 1)])
    s *= 1.0
    s[-1] = FACT[1]
    return t0 + u * (t1 - t0), s


def _ss(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


PROF_T, PROF_S = _profile()
assert np.all(np.diff(PROF_S) >= 0)


def frontier(t: float) -> float:
    """Slots the search has covered at time t (leaves with a slot start below it are found)."""
    if t < T49:
        return float(L_SLOT[6]) - 0.5 if t >= LEAF_T[-1] else -1.0
    if t < PROF_T[0]:
        j = min(3, int((t - T49) / 0.15 + 1e-9))
        return float(L_SLOT[6 + j]) + 0.5
    if t < T51:
        return float(np.interp(t, PROF_T, PROF_S))
    if t < T59:
        return FACT[1] + SWEEP_RATE * (t - T51)
    return float(N_SLOTS)


def found_time(slots: np.ndarray) -> np.ndarray:
    """When the search passes each slot start (the inverse of `frontier`), for slots from game 7 on."""
    out = np.full(len(slots), np.inf)
    s = slots.astype(float)
    disc = [float(L_SLOT[6 + j]) for j in range(4)]
    for j in range(4):
        hi = disc[j + 1] if j < 3 else float(PROF_S[0])
        m = (s >= disc[j]) & (s < hi)
        out[m] = DISCRETE[j]
    m = (s >= PROF_S[0]) & (s < FACT[1])
    out[m] = np.interp(s[m], PROF_S, PROF_T)
    m = s >= FACT[1]
    out[m] = T51 + (s[m] - FACT[1]) / SWEEP_RATE
    return out


L_T = found_time(L_SLOT)
L_T[:6] = LEAF_T
assert abs(L_T[WEDGE_END[0]] - T51) < 1e-6 and np.all(np.diff(L_T) >= -1e-9)
WALK_NODE_T = {}                                  # when the pen first reaches each node of the walk
for _t, _k, _p in WALK:
    if _k == "move":
        WALK_NODE_T.setdefault(_p, _t)
WALK_NODE_T[()] = bb(42)


def games_at(t: float) -> int:
    """Games counted at time t (a leaf counts from the frame after the search passes its slot, so on a
    wedge line's downbeat the counter shows that wedge's running total exactly)."""
    return int(np.searchsorted(L_T, t - 1e-6, side="right"))


for _w in range(9):                               # 51.1 27,732 · 52.1 57,324 · ... · 59.1 255,168
    assert games_at(bb(51 + _w)) == WEDGE_END[_w], (_w, games_at(bb(51 + _w)))


def calls_undos(t: float) -> tuple[int, int]:
    """explore() calls made and marks erased by time t."""
    if t < T49:
        moves = sum(1 for tt, k, _ in WALK if k == "move" and tt <= t)
        undos = sum(1 for tt, k, _ in WALK if k == "undo" and tt <= t)
        return (1 + moves if t >= bb(43) else (1 if t >= bb(42) else 0)), undos
    if t >= T59:
        return len(ALL_STARTS), len(ALL_STARTS) - 1
    s = frontier(t)
    calls = int(np.searchsorted(ALL_STARTS, s, side="left"))
    g = max(0, int(np.searchsorted(L_SLOT, s, side="left")) - 1)
    return calls, calls - 1 - int(L_K[g])


assert calls_undos(T49 - 1e-6) == (calls_undos(T49 - 1e-6)[0], 10)

# ---------------------------------------------------------------- the camera, the galaxy's turn and the lens
LENS_T = (T49, bb(50, 1.5))                       # the magnifier relaxes into the true geometry
CAM_START = (-2.0, 0.0, W)                        # 41.1: the root where the knot was
CAM_WALK0 = (-1.95, 1.0, 0.35 * W)                # 43.1: close on the first wedge
CAM_WALK = (-1.97, 2.55, 0.35 * W)                # 44.4-48.4: the walked subtree (rings 4-9)
FULL_Z = 1.0                                      # the full galaxy: ring 9 fills the picture's height
ROOT_SCREEN_FULL = np.array([-0.62, 0.28])
CAM_FULL = (ROOT[0] - ROOT_SCREEN_FULL[0] / FULL_Z, ROOT[1] - ROOT_SCREEN_FULL[1] / FULL_Z, W / FULL_Z)
END_Z = 1.045                                     # 60-61: easing in towards the inner rings
ROOT_SCREEN_END = np.array([-0.42, 0.26])
CAM_END = (ROOT[0] - ROOT_SCREEN_END[0] / END_Z, ROOT[1] - ROOT_SCREEN_END[1] / END_Z, W / END_Z)
ROT_RATE = math.radians(0.35)                     # the galaxy turns clockwise from 53.1


def _mix_cam(a, b, e):
    w = a[2] * (b[2] / a[2]) ** e
    return a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e, w


def cam_path(t: float):
    if t < bb(42):
        e = seg(t, 0, bb(42))
        return CAM_START[0], CAM_START[1], CAM_START[2] * (1 - 0.01 * e)
    if t < bb(43):
        e = ease_in_out_cubic(seg(t, bb(42), bb(43)))
        a = (CAM_START[0], CAM_START[1], CAM_START[2] * 0.99)
        return _mix_cam(a, CAM_WALK0, e)
    if t < bb(44, 4):
        e = ease_in_out_sine(seg(t, bb(43), bb(44, 4)))
        return _mix_cam(CAM_WALK0, CAM_WALK, e)
    if t < T49:
        e = seg(t, bb(44, 4), T49)
        return CAM_WALK[0], CAM_WALK[1] + 0.03 * e, CAM_WALK[2] * (1 - 0.02 * e)
    walk_end = (CAM_WALK[0], CAM_WALK[1] + 0.03, CAM_WALK[2] * 0.98)
    if t < bb(53):
        e = ease_in_out_cubic(seg(t, T49, bb(53)))
        return _mix_cam(walk_end, CAM_FULL, e)
    if t < T59:
        e = ease_in_out_sine(seg(t, bb(53), T59))                    # a slow drift
        return CAM_FULL[0] + 0.05 * e, CAM_FULL[1] - 0.02 * e, CAM_FULL[2] * (1 + 0.008 * e)
    held = (CAM_FULL[0] + 0.05, CAM_FULL[1] - 0.02, CAM_FULL[2] * 1.008)
    e = ease_in_out_sine(seg(t, T59, END))
    return _mix_cam(held, CAM_END, e)


CAM = Cam(cam_path)


def rot(t: float) -> float:
    """How far the galaxy has turned clockwise about the root (radians): eased in from 53.1."""
    t0 = bb(53)
    if t <= t0:
        return 0.0
    ramp = 2.0
    dt = t - t0
    return ROT_RATE * (dt * dt / (2 * ramp) if dt < ramp else dt - ramp / 2)


def lens_m(t: float) -> float:
    return 1.0 - ease_in_out_cubic(seg(t, *LENS_T))


def polar(slot_centre, depth, dx=0.0, m=1.0, rho=0.0, dr=0.0):
    """World position of a node (common.galaxy_point): ring `depth`, its slot's angle, the lens offset."""
    return galaxy_point(slot_centre, depth, dx, m, rho, dr)


def path_pos(path, t: float) -> np.ndarray:
    d = len(path)
    if d == 0:
        return ROOT.copy()
    return polar(node_slot(path) + FACT[d] / 2, d, LENS.get(path, lens_dx(path)), lens_m(t), rot(t))


# ---------------------------------------------------------------- the galaxy's points
L_CENTRE, L_JIT, L_WEIGHT, L_FAM = _T.l_centre, _T.l_jit, _T.l_weight, _T.l_fam
L_DX = np.zeros(N_GAMES)
for _i in np.flatnonzero(L_SLOT < 24):
    L_DX[_i] = lens_dx(L_MOVES[_i])
N_CENTRE = _T.n_centre
D_IDX, D_W = _T.dust, _T.dust_w                   # dust: rings 0-5, a third of rings 6-8 (three times the weight)
D_DX = np.zeros(len(D_IDX))
D_T = found_time(N_SLOT[D_IDX])
for _j in np.flatnonzero(N_SLOT[D_IDX] < 24):     # the walk's nodes: their walk times and lens offsets
    _p = slot_path(N_SLOT[D_IDX[_j]], int(N_DEPTH[D_IDX[_j]]))
    D_DX[_j] = lens_dx(_p)
    if _p in WALK_NODE_T:
        D_T[_j] = WALK_NODE_T[_p]
D_T[N_DEPTH[D_IDX] == 0] = bb(41, 1.25)
assert all(slot_path(node_slot(p), len(p)) == p for p in WALK_NODE_T)
FAM_COL = GALAXY_COLOURS
DUST_W = GALAXY_DUST_W


PLATE_DIM = 0.55                                  # the plate during the hero shot (54-61)
HUD_Y = HUD_LINES_Y


# ---------------------------------------------------------------- times
SNAP = (0.0, 0.42)                                # 41.1: the knot snaps
ROOT_IN = 0.12
PLATE_IN = (bb(41, 2), bb(41, 4))
PEN_IN = bb(42)
PEN_PULSES = [bb(42, b) for b in (1, 2, 3, 4)]
TAGS_IN = [bb(50, 3), bb(50, 4)]
TAGS_OUT = (bb(53, 3), bb(54))
INSET_OUT = (bb(50, 3), bb(51, 1.5))
ARM_IN = (bb(50, 1), T51)
DARK = bb(58, 4.5)                                # 58.4+: half a beat of darkness (video.yaml cue)
LANDS = [T59 + 0.04 + 0.09 * i for i in range(6)]
DOCK = (bb(61), bb(61, 3))                        # 61.1-61.3: the number docks into the HUD
END_PULSES = [bb(60, b) for b in (1, 2, 3, 4)] + [bb(61, b) for b in (1, 2, 3, 4)]
HERO_C = np.array([4.75, 0.38])                   # 255,168 on the right third (screen)
HERO_SIZE = 74


def octave_up(note: str) -> str:
    return note[:-1] + str(int(note[-1]) + 1)


# ---------------------------------------------------------------- the scene
class EveryGame(BeatScene):

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
        # the knot from S04, in this scene's world (S04's screen + this camera's centre)
        cx, cy, w = CAM_START
        self.knot = [p / (W / w) + np.array([cx, cy]) for p in knot_screen(S04_END)]
        self.threads = [Thread() for _ in self.knot]
        # the root, the walk's edges and nodes, its leaves (glowing dots), stop bars and the ghost stub
        self.root = MiniBoard(0.14, 0, 0, nums=0)
        self.walk_paths = sorted({p for _, k, p in WALK if k == "move"}, key=lambda p: (len(p), p))
        self.edges = {p: Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.6) for p in self.walk_paths}
        self.node_dots = {p: Dot(radius=0.012, color=INK_DIM) for p in self.walk_paths}
        self.leaf_core = [Dot(radius=0.022, color=XC.core) for _ in range(6)]
        self.leaf_halo = [gaussian_sprite(XC.glow if L_RES[i] == 1 else "#C8CCCC", 64, 0.3) for i in range(6)]
        self.stops = [Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK, 1.8) for _ in range(6)]
        self.stub = Ink(VGroup(*[Line([0, 0.25 * j / 5, 0], [0, 0.25 * (j + 0.55) / 5, 0]) for j in range(5)]),
                        INK_DIM, 1.6)
        # the rings 1-2 edges (81 hairlines), drawn as their nodes are visited
        self.ring_edges = []
        for i in np.flatnonzero((N_DEPTH >= 1) & (N_DEPTH <= 2)):
            p = slot_path(N_SLOT[i], int(N_DEPTH[i]))
            if p in WALK_NODE_T:
                continue                                 # the walk draws its own edges
            tv = float(found_time(np.array([N_SLOT[i]]))[0])
            self.ring_edges.append((p, tv, Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.2)))
        # the frontier: the arm and the pen's streak
        self.arm = Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK, 1.4, PEN_HALO, 10, layers=4, glow_opacity=0.35)
        self.streak = Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), PEN, 2.6, PEN_HALO, 16, layers=5, glow_opacity=0.6)
        self.path_line = VMobject().set_stroke(INK, width=stroke_px(1.4), opacity=0).set_fill(opacity=0)
        self.path_line.set_points_as_corners([[0, 0, 0], [0.01, 0, 0]])
        # screen space: the plate and its tags, the inset board, the pen, the HUD, the hero number
        self.plate = ProgramPlate()
        self.tag1 = Label([(VGroup(cjk("递归：", size=ZH_SIZE), Text("explore", font=FONT_MONO, font_size=17),
                                   cjk("调用自己", size=ZH_SIZE)).arrange(RIGHT, buff=0.08), INK),
                           (en("RECURSION: explore CALLS ITSELF", upper=False).set_color(INK_DIM), INK_DIM)],
                          gap=0.1, align="l")
        self.tag2 = Label([(cjk("回溯：撤销，退回来再试", size=ZH_SIZE), INK),
                           (en("BACKTRACKING: UNDO,"), INK_DIM), (en("STEP BACK, TRY AGAIN"), INK_DIM)],
                          gap=0.08, align="l")
        self.leaders = [Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.2) for _ in range(2)]
        self.inset = MiniBoard(0.55, 5, 4, nums=0, glow_x=9, glow_o=11, layers=5)
        self.inset_blur = [MiniBoard(0.55, 5, 4, nums=0, glow_x=0, glow_o=0, layers=1) for _ in range(2)]
        self.eraser = Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), RED, 3.0, RED, 10, layers=4, glow_opacity=0.5)
        self.inset_c = np.array([4.55, 0.35])
        self.pen = Pen()
        self.pen_trail = [Dot(radius=0.03, color=PEN) for _ in range(6)]
        self.sec = section_hud("§3 · 探索每一局 · PLAY EVERY GAME")
        self.hud_games = HudLine("对局计数", "GAMES COUNTED", HUD_Y[0])
        self.hud_calls = HudLine("调用次数", "CALLS", HUD_Y[1])
        self.hud_undos = HudLine("撤销次数", "UNDOS", HUD_Y[2])
        self.hero = title_counter(HERO_C, HERO_SIZE)
        self.glyphs = final_glyphs(self.hero)
        xs = np.array([g.get_center()[0] for g in self.glyphs])
        lo, hi = xs.min(), xs.max()
        self.hero_glow = []
        for g, x in zip(self.glyphs, xs):            # halo colour: cool on the left, warm on the right
            u = clamp01((x - lo) / (hi - lo))
            col = hex_of(rgb(XC.glow) * (1 - u) + rgb(OC.mid) * u)
            layers = []
            for k in range(7, 0, -1):
                c = g.copy().set_fill(opacity=0).set_stroke(col, width=0, opacity=0)
                layers.append((c, 0.62 * (1 - k / 8) ** 2, stroke_px(2 * 22 * HERO_SIZE / 178) * k / 7))
            self.hero_glow.append(layers)
        self.hero_glow_group = VGroup(*[c for lay in self.hero_glow for c, _, _ in lay])
        self.hero_halo = gaussian_sprite(None, 96, 0.34, gradient=(XC.glow, OC.mid), aspect=3.0)
        self.hero_halo.stretch_to_fit_width(12.8 * HERO_SIZE / 178).stretch_to_fit_height(4.3 * HERO_SIZE / 178)
        self.hero_halo.move_to([*HERO_C, 0])
        self.halo_w0, self.halo_h0 = self.hero_halo.width, self.hero_halo.height
        self.dark = Rectangle(width=W + 0.2, height=8.2).set_stroke(width=0).set_fill("#000000", opacity=0)
        self.flash = Rectangle(width=W + 0.2, height=8.2).set_stroke(width=0).set_fill("#FFFFFF", opacity=0)

        self.clock_mob = Mobject()
        self.clock_mob.add_updater(lambda m: self.update_state(self.clock()))
        self.add(self.clock_mob, self.camera.frame)
        self.add(self.galaxy, *[e for _, _, e in self.ring_edges], *self.edges.values(), self.path_line,
                 *self.node_dots.values(), self.arm, self.root.group, *self.stops, self.stub, *self.leaf_halo,
                 *self.leaf_core, self.streak, *self.threads)
        self.fix(self.plate.group, self.tag1.group, self.tag2.group, *self.leaders,
                 *[b.group for b in self.inset_blur], self.inset.group, self.eraser, *self.pen_trail, self.pen,
                 self.sec, self.hud_games.group, self.hud_calls.group, self.hud_undos.group, self.hero_halo,
                 self.hero_glow_group, self.hero, self.dark, self.flash)
        self.update_state(0.0)

    # ------------------------------------------------------------- the picture at time t
    def update_state(self, t: float):
        cx, cy, w = CAM(t)
        self.camera.frame.set(width=w)
        self.camera.frame.move_to([cx, cy, 0])
        self.galaxy.move_to([cx, cy, 0])
        self.update_knot(t)
        self.update_root(t)
        self.update_walk(t)
        self.update_galaxy(t)
        self.update_frontier(t)
        self.update_plate(t)
        self.update_inset(t)
        self.update_pen(t)
        self.update_hud(t)
        self.update_hero(t)
        dark = 0.88 * seg(t, DARK, DARK + 0.05) if DARK <= t < T59 else 0.0
        self.dark.set_fill(opacity=dark)
        fl = 0.0
        for t0 in (0.0, T59):
            if t0 <= t < t0 + 0.07:
                fl = max(fl, 0.85 * math.exp(-(t - t0) / 0.022))
        self.flash.set_fill(opacity=fl)

    def px_width(self, t: float, px: float = 1.0) -> float:
        """An Ink width factor that draws `px` pixels on screen whatever the zoom."""
        return px / CAM.zoom(t)

    # --- 41.1: the knot snaps; its threads straighten and vanish
    def update_knot(self, t: float):
        if t >= SNAP[1]:
            for th in self.threads:
                th.hide()
            return
        e = ease_out_cubic(seg(t, *SNAP))
        vis = 1 - seg(t, 0.1, SNAP[1])
        n = len(self.threads)
        for i, (th, pts) in enumerate(zip(self.threads, self.knot)):
            a = 2 * math.pi * (i * 0.618034 % 1.0) + 0.3      # spread evenly round the knot
            d = np.array([math.cos(a), math.sin(a)])
            s = np.linspace(0, 1, len(pts))[:, None]
            reach = 0.35 + (2.2 + 1.2 * ((i * 0.37) % 1.0)) * e   # the threads fly out as straight rays
            straight = ROOT + d * (reach + (s - 0.5) * (0.6 + 1.4 * e))
            p = pts * (1 - e) + straight * e
            th.show(p, 1.0, vis * (0.9 + 0.6 * (1 - e)), head=0.0, width=self.px_width(t))

    def update_root(self, t: float):
        R = self.root
        if t < ROOT_IN:
            R.hide()
            return
        s = 0.3 + 0.7 * ease_out_cubic(seg(t, ROOT_IN, ROOT_IN + 0.35))
        R.place(ROOT, s)
        R.draw_grid(1.0, vis=seg(t, ROOT_IN, ROOT_IN + 0.12), width=self.px_width(t, 1.0))

    # --- bars 43-48: the walk (vector objects in the lens); they hand over to the splat in bar 49
    def walk_state(self, t: float):
        """The pen's path now, and the event in progress: (path, kind, t0, previous path)."""
        prev, cur, kind, t0 = (), (), None, -1.0
        for tt, k, p in WALK:
            if tt <= t:
                prev, cur, kind, t0 = cur, p, k, tt
        return cur, kind, t0, prev

    def update_walk(self, t: float):
        hand = 1 - ease_in_out_sine(seg(t, T49 + 0.3, bb(50, 2)))      # the vectors give way to the splat
        width = self.px_width(t)
        visited = {p: tt for p, tt in WALK_NODE_T.items() if tt <= t}
        cur, kind, t0, prev = self.walk_state(t)
        on_path = {cur[:d] for d in range(len(cur) + 1)} if t < T49 else set()
        for p, ink in self.edges.items():
            if p not in visited or hand <= 1e-3:
                ink.hide()
                continue
            a, b = path_pos(p[:-1], t), path_pos(p, t)
            g = ease_out_cubic(seg(t, visited[p], visited[p] + 0.25 if visited[p] < bb(47) else visited[p] + 0.16))
            A, c = line_affine(a, a + (b - a) * 1.0)
            lit = p in on_path
            ink.show(g, A, c, vis=(0.95 if lit else 0.42) * hand, width=width * (1.25 if lit else 1.0))
        for p, d in self.node_dots.items():
            if p not in visited or hand <= 1e-3:
                d.set_fill(opacity=0)
                continue
            q = path_pos(p, t)
            d.move_to([*q, 0])
            d.set(width=0.024 / CAM.zoom(t) * 2.86)
            d.set_fill(INK_DIM, opacity=0.7 * hand)
        # the six leaves: a glowing dot each (cyan X wins, grey-white the draw), with a stop bar
        for i in range(6):
            core, halo, stop = self.leaf_core[i], self.leaf_halo[i], self.stops[i]
            if t < LEAF_T[i] or hand <= 1e-3:
                core.set_fill(opacity=0)
                show_sprite(halo, opacity=0)
                stop.hide()
                continue
            q = path_pos(FIRST_SIX[i], t)
            fl = pulse(t, LEAF_T[i], 0.45)
            z = CAM.zoom(t)
            core.move_to([*q, 0])
            core.set(width=(0.052 + 0.03 * fl) * 2.86 / z)
            core.set_fill(XC.core if L_RES[i] == 1 else "#E8ECEC", opacity=hand)
            hw = (0.42 + 0.35 * fl) * 2.86 / z
            show_sprite(halo, q, hw, hw, (0.75 + 0.6 * fl) * hand)
            k = len(FIRST_SIX[i])
            # the stop bar, just outside the leaf, across the radius
            st = LEAF_T[i] + (BEAT if i == 0 else 0.12)
            sv = ease_out_cubic(seg(t, st, st + 0.15)) * hand
            dirv = q - ROOT
            dirv = dirv / np.linalg.norm(dirv)
            nrm = np.array([-dirv[1], dirv[0]])
            cen = q + dirv * (0.085 if i else 0.2)
            A, c = line_affine(cen - nrm * 0.055, cen + nrm * 0.055)
            stop.show(sv, A, c, vis=sv, width=width * 1.2)
        # 44.4: the ghost stub tries to continue past leaf 1, and stops at the bar
        q = path_pos(FIRST_SIX[0], t)
        dirv = (q - ROOT) / np.linalg.norm(q - ROOT)
        if STUB_T <= t and hand > 1e-3:
            f = ease_out_quad(seg(t, STUB_T, STUB_T + 0.3))
            nrm = np.array([-dirv[1], dirv[0]])
            A = np.column_stack([nrm, dirv]) * 0.7
            self.stub.show(f, A, q + dirv * 0.04, vis=0.55 * hand * (1 - 0.5 * seg(t, STUB_T + 0.6, STUB_T + 1.2)),
                           width=width)
        else:
            self.stub.hide()

    # --- the galaxy: every leaf found so far, the dust, the flare at the landing
    def update_galaxy(self, t: float):
        n = games_at(t) if t >= T49 else 0
        if n == 0:
            self.galaxy.light = None
            return
        m, rho = lens_m(t), rot(t)
        z = CAM.zoom(t)
        cam = CAM
        idx = slice(0, n)
        P = polar(L_CENTRE[idx], L_K[idx], L_DX[idx], m, rho, L_JIT[idx])
        S = cam.to_screen(P, t)
        age = t - L_T[idx]
        appear = np.clip(age / 0.08, 0, 1)
        flare = 1 + 2.6 * np.exp(-np.maximum(age, 0) / 0.28)
        zf = z * z                                       # the same surface brightness at any zoom
        land = 1 + 1.6 * pulse(t, T59, 0.7) if t >= T59 else 1.0
        breathe = 1 + 0.05 * math.sin(2 * math.pi * (t - T59) / (2 * BAR)) if t >= T59 else 1.0
        wts = L_WEIGHT[idx] * appear * flare * zf * land * breathe
        fam = L_FAM[idx]
        families = []
        for f in range(3):
            sel = fam == f
            families.append((self.splat.accumulate(S[sel], wts[sel]), FAM_COL[f]))
        # dust: internal nodes visited so far
        dmask = D_T <= t
        di = D_IDX[dmask]
        if len(di):
            DP = polar(N_CENTRE[di], N_DEPTH[di], D_DX[dmask], m, rho)
            DS = cam.to_screen(DP, t)
            dw = D_W[dmask] * DUST_W[N_DEPTH[di]] * zf * (1 + 1.2 * np.exp(-np.maximum(t - D_T[dmask], 0) / 0.3))
            families.append((self.splat.accumulate(DS, dw), FAM_COL[3]))
        # tiny RED sparks at the tips: the undos, a few per frame while the walk is fast
        if T49 + 0.6 <= t < T59:
            recent = np.flatnonzero((age >= 0) & (age < 0.09))
            if len(recent):
                pick = recent[(recent * 7919) % 6 == 0][:400]
                if len(pick):
                    out = (P[pick] - ROOT)
                    out /= np.maximum(np.linalg.norm(out, axis=1, keepdims=True), 1e-6)
                    sp = cam.to_screen(P[pick] + out * (0.03 + 0.25 * age[pick][:, None]), t)
                    families.append((self.splat.accumulate(sp, np.full(len(pick), 1.2 * zf) * (1 - age[pick] / 0.09)),
                                     FAM_COL[4]))
        self.galaxy.light = self.splat.render(families, **GALAXY_LOOK)

    # --- the frontier: the arm (from 50.1), the pen's streak, the current path; the ring 1-2 edges
    def update_frontier(self, t: float):
        width = self.px_width(t)
        s = frontier(t) if t >= T49 else -1
        rho = rot(t)
        for p, tv, ink in self.ring_edges:
            if t < tv:
                ink.hide()
                continue
            g = ease_out_cubic(seg(t, tv, tv + 0.2))
            A, c = line_affine(path_pos(p[:-1], t), path_pos(p, t))
            ink.show(g, A, c, vis=0.38, width=width)
        # the arm
        av = ease_in_out_sine(seg(t, *ARM_IN)) * (1 - seg(t, T59 - 0.02, T59)) if t < T59 else 0.0
        if av > 1e-3:
            th = 2 * np.pi * s / N_SLOTS + rho
            d = np.array([math.sin(th), math.cos(th)])
            p0, p1 = ROOT + d * 0.05, ROOT + d * 3.12
            A, c = line_affine(p0, p1)
            self.arm.show(1.0, A, c, vis=0.26 * av, glow=0.7, width=width)
            q0, q1 = ROOT + d * (RING[5] - 0.06), ROOT + d * (RING[9] + 0.06)
            A, c = line_affine(q0, q1)
            flick = 0.85 + 0.15 * math.sin(97 * t) * math.sin(61 * t)
            self.streak.show(1.0, A, c, vis=0.6 * av * flick, glow=0.9, width=width * 0.8)
        else:
            self.arm.hide()
            self.streak.hide()
        # the current path (root to the frontier leaf), faint, while the walk is fast
        pv = (1 - ease_in_out_sine(seg(t, ARM_IN[0], ARM_IN[1]))) if T49 <= t < T51 else 0.0
        if pv > 1e-3:
            g = max(6, games_at(t) - 1)
            mv = [int(x) for x in L_MOVES[g, :L_K[g]]]
            pts = [path_pos(tuple(mv[:d]), t) for d in range(len(mv) + 1)]
            self.path_line.set_points_as_corners([[*p, 0] for p in pts])
            self.path_line.set_stroke(INK, width=stroke_px(1.4) * width, opacity=0.6 * pv)
        else:
            self.path_line.set_stroke(width=0, opacity=0)

    # --- the plate: fades in (41.2-41.4), highlights the line being run, tags (50.3-50.4)
    def update_plate(self, t: float):
        n = len(PLATE_LINES)
        lv = [ease_out_cubic(seg(t, PLATE_IN[0] + 0.07 * j, PLATE_IN[0] + 0.07 * j + 0.3)) for j in range(n)]
        dim = 1 - (1 - PLATE_DIM) * ease_in_out_sine(seg(t, bb(53, 3), bb(54, 2)))
        hl = {}

        def add(num, amt, col=WHITE):
            a0, _ = hl.get(num, (0.0, col))
            if amt > a0:
                hl[num] = (amt, col)
        for tt, k, p in WALK:
            if t < tt - 0.01 or t > tt + 0.9:
                continue
            step = 0.3 if tt >= bb(47) else 0.6
            if k == "move":
                add(31, 1 - seg(t, tt + 0.5 * step, tt + 0.7 * step) if t >= tt else 0)
                add(33, seg(t, tt + 0.35 * step, tt + 0.5 * step) * (1 - seg(t, tt + step, tt + step + 0.1)))
                if p in FIRST_SIX:
                    res = L_RES[FIRST_SIX.index(p)]
                    lines = (24, 25) if res != 3 else (26, 27)
                    for num in lines:
                        add(num, seg(t, tt + 0.2, tt + 0.3) * (1 - seg(t, tt + 0.75, tt + 0.9)))
            else:
                add(34, pulse(t, tt, 0.35) if t >= tt else 0, RED)
        if T49 <= t < T59:                               # the fast walk: every line flickers, then glows
            fast = seg(t, T49, T49 + 1.2)
            for j, num in enumerate((24, 25, 26, 27, 31, 33, 34)):
                fl = 0.5 + 0.5 * math.sin(41 * t + 2.1 * j) * math.sin(23 * t + j)
                add(num, (0.25 + 0.45 * fl) * fast * (1 - 0.6 * seg(t, bb(53), bb(54))), RED if num == 34 else WHITE)
        self.plate.show(dim * ease_out_cubic(seg(t, PLATE_IN[0] - 0.1, PLATE_IN[0] + 0.25)), hl, line_vis=lv)
        # the tags on the recursive call and the undo line (50.3, 50.4), gone before the 12 wordless seconds
        out = 1 - seg(t, *TAGS_OUT)
        for j, (lab, ld, num) in enumerate(((self.tag1, self.leaders[0], 33), (self.tag2, self.leaders[1], 34))):
            v = ease_out_cubic(seg(t, TAGS_IN[j], TAGS_IN[j] + 0.35)) * out
            if v <= 1e-3:
                lab.hide()
                ld.hide()
                continue
            y = self.plate.row_y(num)
            x0 = self.plate.row_right(num) + 0.08
            anchor = np.array([PLATE_TL[0] + 0.05, -0.55 - 1.05 * j])
            lab.show(anchor + np.array([0.0, -0.05 * (1 - v)]), vis=v)
            A, c = line_affine(np.array([x0, y]), np.array([PLATE_TL[0] + self.plate.width + 0.15, y]))
            ld.show(v, A, c, vis=0.6 * v)

    # --- the inset board: the position the pen is at (bars 43-50)
    def inset_moves(self, t: float):
        if t < T49:
            cur, kind, t0, prev = self.walk_state(t)
            return cur, kind, t0, prev
        g = max(6, games_at(t) - 1)
        return tuple(int(x) for x in L_MOVES[g, :L_K[g]]), "fast", L_T[g], ()

    def update_inset(self, t: float):
        B = self.inset.place(self.inset_c, 1.0)
        vis = ease_out_cubic(seg(t, bb(43) - 0.3, bb(43))) * (1 - seg(t, *INSET_OUT))
        for bl in self.inset_blur:
            bl.hide()
        if vis <= 1e-3:
            B.hide()
            self.eraser.hide()
            return
        B.draw_grid(1.0, vis=vis)
        cur, kind, t0, prev = self.inset_moves(t)
        xs = [cur[i] for i in range(0, len(cur), 2)]
        os = [cur[i] for i in range(1, len(cur), 2)]
        fx = [1.0] * 5
        fo = [1.0] * 4
        vx, vo = [vis] * 5, [vis] * 4
        if kind == "move" and len(cur):
            k = len(cur) - 1
            f = ease_out_cubic(seg(t, t0, t0 + 0.22))
            if k % 2 == 0:
                fx[k // 2] = f
            else:
                fo[k // 2] = f
        # undo: the erased mark is swiped off by a RED eraser
        self.eraser.hide()
        if kind == "undo" and t < t0 + 0.4:
            sq = prev[-1]
            k = len(prev) - 1
            u = seg(t, t0, t0 + 0.18)
            fade = 1 - seg(t, t0 + 0.08, t0 + 0.3)
            if k % 2 == 0:
                xs = xs + [sq]
                vx[len(xs) - 1] = vis * fade
            else:
                os = os + [sq]
                vo[len(os) - 1] = vis * fade
            c = B.sq(sq)
            p0, p1 = c + np.array([-0.32, 0.18]), c + np.array([0.32, -0.18])
            A, cc = line_affine(p0, p1)
            self.eraser.show(ease_out_quad(u), A, cc, vis=vis * (1 - seg(t, t0 + 0.2, t0 + 0.4)), glow=1.4)
        B.draw_marks(xs, os, vis_x=vx, vis_o=vo, f_x=fx, f_o=fo, glow_x=1.0, glow_o=1.0)
        # the win line at a leaf (or nothing: the draw)
        g = None
        if kind == "move" and cur in FIRST_SIX:
            g = FIRST_SIX.index(cur)
        elif kind == "fast":
            g = max(6, games_at(t) - 1)
        line = None
        if g is not None and L_RES[g] != 3:
            cells = ["."] * 9
            for i_, sq in enumerate(cur):
                cells[sq] = "XO"[i_ % 2]
            line = next((ln for ln in WIN_LINES if cells[ln[0]] != "." and cells[ln[0]] == cells[ln[1]] == cells[ln[2]]), None)
        if line is not None:
            wv = ease_out_quad(seg(t, t0, t0 + 0.3)) if kind == "move" else 1.0
            col = (XC.mid, XC.glow) if L_RES[g] == 1 else (OC.mid, OC.glow)
            B.win.set_core_color(col[0])
            B.draw_win(line, wv, vis=vis, glow=1.2)
        else:
            B.win.hide()
        # fast: the games just found, as fading copies (a blur)
        if kind == "fast":
            n = games_at(t)
            n_prev = games_at(t - 1 / 30)
            if n - n_prev > 1:
                for j, bl in enumerate(self.inset_blur):
                    gj = max(6, n - 1 - (j + 1) * max(1, (n - n_prev) // 3))
                    mv = [int(x) for x in L_MOVES[gj, :L_K[gj]]]
                    bl.place(self.inset_c, 1.0)
                    bl.draw_marks(mv[0::2], mv[1::2], vis_x=0.35 * vis / (j + 1), vis_o=0.35 * vis / (j + 1),
                                  glow_x=0.0, glow_o=0.0)

    # --- the pen: on the root (bar 42), walking (43-48), racing (49-50), then the frontier's streak
    def update_pen(self, t: float):
        for d in self.pen_trail:
            d.set_fill(opacity=0)
        if t < PEN_IN:
            self.pen.place((0, 0), 0)
            return
        if t >= T59:                                     # the search is over: back on the root
            p = CAM.to_screen(ROOT, t)
            beat = max([pulse(t, tp, 0.25) for tp in END_PULSES if t >= tp] + [0.0])
            self.pen.place(p, 0.9 * seg(t, T59, T59 + 0.1), glow=1.0 + 0.8 * beat)
            return
        if t < bb(43):
            beat = max([pulse(t, tp, 0.25) for tp in PEN_PULSES if t >= tp] + [0.0])
            self.pen.place(CAM.to_screen(ROOT, t), ease_out_cubic(seg(t, PEN_IN, PEN_IN + 0.25)), glow=1.0 + 0.9 * beat)
            return
        if t < T49:
            cur, kind, t0, prev = self.walk_state(t)
            dur = 0.3 if t0 >= bb(47) else 0.45
            u = ease_out_cubic(seg(t, t0, t0 + dur))
            a, b = path_pos(prev, t), path_pos(cur, t)
            q = a + (b - a) * u
            self.pen.place(CAM.to_screen(q, t), 1.0, glow=1.0 + 0.5 * pulse(t, t0, 0.2))
            return
        # bars 49-58: the pen races along the frontier; its trail of the games just found; as the arm
        # takes over, it becomes the arm's hot streak
        fade = 1 - ease_in_out_sine(seg(t, ARM_IN[0] + 0.6, ARM_IN[1]))
        g = max(5, games_at(t) - 1)
        q = path_pos(tuple(int(x) for x in L_MOVES[g, :L_K[g]]), t) if g < 24 else polar(L_CENTRE[g], L_K[g], L_DX[g], lens_m(t), rot(t))
        self.pen.place(CAM.to_screen(q, t), fade, glow=1.0)
        for j, d in enumerate(self.pen_trail):
            gj = g - (j + 1) * max(1, (games_at(t) - games_at(t - 0.05)) // 6)
            if gj < 0 or fade <= 1e-3:
                continue
            qj = polar(L_CENTRE[gj], L_K[gj], L_DX[gj], lens_m(t), rot(t))
            sp = CAM.to_screen(qj, t)
            d.move_to([*sp, 0])
            d.set_fill(PEN, opacity=0.5 * fade * (1 - j / 6))

    # --- the HUD (games, calls, undos) and the landing (59.1)
    def update_hud(self, t: float):
        on = ease_out_cubic(seg(t, PLATE_IN[0], PLATE_IN[1]))
        games = games_at(t) if t >= bb(43) else 0
        calls, undos = calls_undos(t)
        if t >= T59:
            games = N_GAMES
        hv = ease_out_cubic(seg(t, PLATE_IN[0], PLATE_IN[1]))
        back = 1.0 if t < T59 else seg(t, DOCK[1] - 0.25, DOCK[1])         # the hero has it in between
        self.hud_games.show(games, hv * back)
        cu = ease_out_cubic(seg(t, bb(54), bb(54, 2)))
        self.hud_calls.show(calls, cu)
        self.hud_undos.show(undos, cu)

    def update_hero(self, t: float):
        cnt = self.hero
        gl_all = counter_glyphs(cnt)
        uncull(gl_all)
        on = T59 <= t < DOCK[1]
        if not on:
            for col in cnt.columns:
                for g in col:
                    g.set_opacity(0)
            for _, sep in cnt.separators:
                sep.set_opacity(0)
            for lay in self.hero_glow:
                for c, _, _ in lay:
                    uncull([c])
                    c.set_stroke(width=0, opacity=0)
                    cull([c])
            show_sprite(self.hero_halo, opacity=0)
            cull(gl_all)
            return
        dock = ease_in_out_cubic(seg(t, *DOCK))
        # the digits lock left to right (a short roll into place, like the title)
        pos = []
        target = [2, 5, 5, 1, 6, 8]
        for i, L in enumerate(LANDS):
            u = ease_out_cubic(seg(t, T59, L + 0.12))
            pos.append(target[i] + 10 * (1 - u) * (1 + (i % 2)))
        cnt.manual = pos
        cnt.manual_top = 999_999
        # docking: shrink towards the HUD readout's digits
        hud = self.hud_games.counter
        k = 1 + (hud.ref.width / self.hero_w0 - 1) * dock
        cur = cnt.ref.width / self.hero_w0
        if abs(k / cur - 1) > 1e-6:
            cnt.scale(k / cur)
        c = HERO_C + (hud.ref.get_center()[:2] - HERO_C) * dock
        cnt.ref.move_to([*c, 0])
        cnt.layout()
        vis = (1 - seg(t, DOCK[1] - 0.2, DOCK[1]))
        if T59 <= t < T59 + 0.6 / config.frame_rate:
            vis = 0.0                                    # the flash frame is clean white
        for colm in cnt.columns:
            for g in colm:
                g.set_fill(WHITE, opacity=g.get_fill_opacity() * vis)
        for _, sep in cnt.separators:
            sep.set_fill(WHITE, opacity=vis)
        cull(gl_all)
        breathe = 1 + 0.14 * math.sin(2 * math.pi * (t - T59) / BAR)
        lands = LANDS + [T59]
        s = cnt.ref.width / self.hero_w0
        for i, lay in enumerate(self.hero_glow):
            gl = self.glyphs[i]
            p0 = gl.get_center()[:2] - HERO_C
            v = ease_out_cubic(seg(t, lands[i], lands[i] + 0.3)) * breathe + 1.2 * pulse(t, lands[i], 0.25)
            v *= 1 - dock
            for cp, base, wk in lay:
                uncull([cp])
                if v <= 1e-3:
                    cp.set_stroke(width=0, opacity=0)
                    cull([cp])
                    continue
                kk = gl.height * s / max(1e-6, cp.height)
                if abs(kk - 1) > 1e-6:
                    cp.scale(kk)
                cp.move_to([*(c + p0 * s), 0])
                cp.set_stroke(width=wk * s, opacity=clamp01(base * v))
        hv = ease_out_cubic(seg(t, T59, T59 + 0.5)) * (0.5 + 0.08 * math.sin(2 * math.pi * (t - T59) / BAR)) * (1 - dock)
        k = cnt.ref.width / self.hero_w0
        show_sprite(self.hero_halo, c, self.halo_w0 * k, self.halo_h0 * k, hv)

    # ------------------------------------------------------------- the sounds (from the same numbers)
    def score(self):
        S = self.sounds
        sx = lambda p, t: float(CAM.to_screen(p, t)[0])
        S.effect(0.0, "shimmer", 1.2, 0.0)                                     # the knot's threads fly apart
        S.phrase("plate", [(PLATE_IN[0], "pluck@A3", float(PLATE_TL[0] + 1.5))], gain=0.4)
        S.phrase("pen", [(tp, "pen@A4", 0.0) for tp in PEN_PULSES], gain=0.7)
        # the walk: every move its square's note (X bell, O glass); undos RED whooshes; leaves a ping in
        # the winner's timbre and a tick; the stop bars muted plucks
        moves, undos, pings, ticks, stops = [], [], [], [], []
        for tt, k, p in WALK:
            x = sx(path_pos(p, tt), tt)
            if k == "move":
                sq = p[-1]
                moves.append((tt, tag(player(len(p) - 1), sq), x))
                if p in FIRST_SIX:
                    i = FIRST_SIX.index(p)
                    if L_RES[i] == 3:
                        pings.append((tt, f"draw@{PITCH[sq]}", x))
                    else:
                        pings.append((tt + 0.01, f"X@{octave_up(PITCH[sq])}", x))
                    ticks.append((tt + 0.02, "tick", x))
                    stops.append((LEAF_T[i] + (BEAT if i == 0 else 0.12), "pluck@D3", x))
            else:
                undos.append((tt, "undo", x))
        S.phrase("walk", moves)
        S.phrase("leaves", pings, gain=0.8)
        S.phrase("leaf ticks", ticks, gain=0.6)
        S.phrase("stops", stops, gain=0.45)
        S.phrase("undos", undos, gain=0.8)
        # bars 49-58: the leaf pings thicken into grains, in the proportions being lit (bells for X, glass
        # for O, wood for draws), each at its game's last square: sixteenths in bar 49, then 32nd notes,
        # doubled in 57-58
        for bar in range(49, 59):
            step = BEAT / 4 if bar == 49 else (BEAT / 8 if bar < 57 else BEAT / 16)
            notes = []
            for j in range(int(round(BAR / step))):
                tt = bb(bar) + j * step
                g = max(6, games_at(tt + 1e-6) - 1)
                res = int(L_RES[g])
                sq = int(L_LAST[g])
                name = "X" if res == 1 else "O" if res == 2 else "draw"
                th = 2 * np.pi * L_CENTRE[g] / N_SLOTS + rot(tt)
                x = sx(ROOT + RING[L_K[g]] * np.array([math.sin(th), math.cos(th)]), tt)
                notes.append((tt, f"{name}@{octave_up(PITCH[sq]) if res == 1 else PITCH[sq]}", x))
            S.phrase(f"grains {bar}", notes, gain=0.32 + 0.025 * (bar - 49))
        # 59.1: the digits lock (a rolled Dmaj9, rising); the pen's pulse on quarter notes (60-61); the dock
        S.phrase("lock", [(L, f"bell@{n}", float(HERO_C[0]) - 1.5 + 0.6 * i)
                          for i, (L, n) in enumerate(zip(LANDS, ("D5", "F#5", "A5", "C#6", "E6", "F#6")))], gain=0.7)
        S.phrase("settle", [(T59 + 0.3, "tick", 5.5), (T59 + 0.42, "tick", 5.5)], gain=0.5)
        S.phrase("pen again", [(tp, "pen@D5", sx(ROOT, tp)) for tp in END_PULSES], gain=0.6)
        S.phrase("dock", [(DOCK[1], "glass@A5", 5.5)], gain=0.45)
        S.log(self)
        self.mark("particles", at=T49, n=N_GAMES, x=round(sx(ROOT, T49), 2))
        self.mark("riser", at=bb(57), dur=2 * BAR)

    # ------------------------------------------------------------- the logged events and the clock
    def log_events(self):
        ev = self.shots

        def add(t, dur, x, y, w, h):
            ev.append((float(t), float(dur), (x, y, w, h)))
        add(0.0, BEAT, *ROOT, 3.0, 3.0)
        add(PLATE_IN[0], PLATE_IN[1] - PLATE_IN[0], -5.4, 2.0, 3.2, 2.2)
        for tp in PEN_PULSES:
            add(tp, 0.3, *ROOT, 0.4, 0.4)
        add(bb(42), BAR, -2.0, 0.6, 6.0, 4.0)                              # the push-in
        for tt, k, p in WALK:
            q = path_pos(p, tt)
            add(tt, 0.3, *q, 0.5, 0.5)
        add(STUB_T, 0.3, *path_pos(FIRST_SIX[0], STUB_T), 0.3, 0.3)
        for k in range(int(round((T59 - T49) / BEAT))):                     # the search: the whole picture
            add(T49 + k * BEAT, BEAT, -1.3, 0.3, 6.5, 6.5)
        for t in TAGS_IN:
            add(t, BEAT, -4.5, -1.0, 5.0, 1.0)
        add(T59, BEAT, *HERO_C, 4.5, 1.2)
        for k in range(1, 12):                                             # 59-61: a slow turn, the zoom
            add(T59 + k * BEAT, BEAT, -1.3, 0.3, 6.5, 6.5)
        add(DOCK[0], DOCK[1] - DOCK[0], 5.0, 1.8, 4.5, 3.0)
        for k in range(int(round((END - DOCK[1]) / BEAT))):
            add(DOCK[1] + k * BEAT, BEAT, -1.3, 0.3, 6.5, 6.5)

    def run(self):
        self.hero_w0 = self.hero.ref.width
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
