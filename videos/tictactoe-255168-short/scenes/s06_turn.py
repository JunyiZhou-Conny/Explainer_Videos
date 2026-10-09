"""S06 · Delete one check 删掉“判断输赢” — ★2, the turn: the winner check is struck out, the search runs again,
and every ghost game comes back: ring 9 fills to all 362,880 slots and takes S02's look.

Bars 62-69 (2:26.4-2:45.6) of script.md; scene time 0 is the downbeat of bar 62. As in S01 (the reference
scene), the picture is a pure function of the scene time (`update_state`), and the notes are computed from the
same numbers (Sounds), each with its own tag ("ghost@D4": a ghost glass at its square's pitch). Every point of
the galaxy is splatted with numpy into one light image per frame (common.Splatter, FrameImage), never drawn as
mobjects.

    62     62.1 the plate glides to the centre-left and grows 1.6x, the galaxy dims to 40 %; the winner check
           (lines 24-25) lights, tagged "判断输赢 · WINNER CHECK"; 62.2 a RED strike draws across both lines (c19)
    63     the program starts again: the galaxy's light drains into the root (a spiral, as the turn slows to a
           halt with the tape stop); the HUD counter rolls back to 000,000 on 63.4
    64     near-black, digital silence: only the struck check, faint, and the still pen on the empty root
    65-66  65.1 HIT: the re-run, one turn of the arm in two bars. Every game that ended on moves 5-8 lights as
           the arm passes, then its light streams outwards as pale streaks and splits into its (9 - k)! ghost
           games: unglowing grey points on ring 9, inside its own wedge (24, 6, 2, 1). The move-9 games keep
           their colours. The inner rings empty out; ring 9 fills in completely. The counter races; as it passes
           255,168 (66.2+) that value flashes RED in the HUD and is left behind
    67     67.1 the counter lands on 362,880 (the right third, where S05 landed 255,168; neutral halo); the
           whole tree takes S02's look and repeats S02's 18.1 flare frame (s02_fill's own point sets, weights,
           envelopes and tone map); 67.2 S02's label "9 × 8 × … × 1 = 9! = 362,880" and "9 的阶乘 · NINE
           FACTORIAL" fly in from the left and dock under the number                                    (c20)
    68-69  68.1 the strike pulses; 69.1 it erases, the winner check is back: the ghost points stream back
           inwards along their streaks into their games, which light again in their colours; the number rolls
           back to 255,168 as it docks into the HUD (69.1-69.3); 70.1 the five-ring galaxy of S05, restored

Every number is exact and asserted below: the 127,296 games that end before move 9 own exactly the 235,008 ghost
slots (1,440 x 24 + 5,328 x 6 + 47,952 x 2 + 72,576 x 1), which with the 127,872 move-9 games tile all 9! slots;
the re-run counts the slots the arm has passed, so it passes 255,168 at 66.2+ and lands on 362,880 at 67.1.

Hand-over from S05 (a segue at 62.1): s05_search.HANDOVER_S06, imported (the camera CAM(END), the galaxy turned
by rot(END), still turning at 0.35°/s; the plate at PLATE_TL at PLATE_DIM; the three HUD readouts; the pen on
the root at 90 %). S05 does not draw the two ring 1-2 edges of the walk (X0 and X0 O1) after bar 50; the first
frames here match that exactly, and the re-run (65-66) draws all 81.
Camera: S05's last frame until 65.1; during the re-run it eases (two bars) to CAM_1, S02's zoom 1.0 with the
root on screen at (-0.95, 0.24), so the number column on the right third clears ring 9; still from 67.1 (S02's
look is cached as intensity fields for that one camera and one turn, RHO_F: the galaxy's turn halts with the
tape stop and starts again at 69.1).
Hand-over to S07 (a segue at 70.1): HANDOVER_S07 below. The camera CAM_1; the galaxy is S05's look
(`galaxy_families`), turned by rho(END) and turning at ROT_RATE again; all 81 ring 1-2 edges at 38 %; the root
board and the pen (90 %); the plate at PLATE_TL, PLATE_DIM, scale PLATE_BACK, no strike; the HUD: §3 and one readout,
"对局计数 · GAMES COUNTED 255,168" (CALLS and UNDOS are gone since 63.1).
"""

from __future__ import annotations

import math
from math import factorial

import numpy as np
from manim import Group, Line, Mobject, Rectangle, VGroup, config

from explainer.short import FONT_MONO, BeatScene, INK, INK_DIM, RED, WHITE, _tone_lut, oldstyle, stroke_px

from common import (FILL_COLOR, FILL_SPLAT, FILL_WEIGHT, GALAXY_COLOURS, GALAXY_DUST_W, GALAXY_LOOK, GALAXY_SLOT_W,
                    H, HUD_LINES_Y, HUD_RIGHT, NINE_FACT, OC, PEN_HALO, PITCH, PLATE_TL, TREE_ROOT, XC, Cam,
                    FastCamera, FrameImage, HudLine, Pen, ProgramPlate, Shot, Sounds, Splatter, W, _LUT_SCALE,
                    _galaxy_lut, bi_label, box, clamp01, counter_glyphs, cull, ease_in_cubic, ease_in_out_cubic,
                    ease_in_out_sine, ease_out_cubic, ease_out_quad, fill_flare, fill_ring, galaxy_point,
                    galaxy_tree, gaussian_sprite, lerp, pulse, rgb, ring_radius, section_hud, seg, show_sprite,
                    uncull)
from common import LeanInk as Ink
from common import LeanText as InkText
from s02_fill import (A_SLOTS, FLIGHT as S02_FLIGHT, HIT as S02_HIT, INNER_GAIN, RING_SUB, RING_T as S02_RING_T,
                      SPARSE, SPARSE_WEIGHT, SWEEP as S02_SWEEP)
from s04_by_hand import MiniBoard, hex_of, line_affine, maths
from s05_search import CAM as S05_CAM
from s05_search import END as S05_END
from s05_search import HANDOVER_S06, HERO_C, HERO_SIZE, PLATE_DIM, ROT_RATE
from s05_search import rot as s05_rot

# ---------------------------------------------------------------- the plan's clock
BEAT, BAR = 0.6, 2.4
FIRST = 62


def bb(bar: int, beat: float = 1.0) -> float:
    """Scene time of script.md's "bar.beat" (global bar numbers): bb(66, 2.5) is "66.2+"."""
    return (bar - FIRST) * BAR + (beat - 1) * BEAT


END = bb(70)                                      # 19.2 s: 8 bars
T63, T64, T65, T67, T68, T69 = bb(63), bb(64), bb(65), bb(67), bb(68), bb(69)

# ---------------------------------------------------------------- the tree and its ghosts (numbers asserted)
FACT = [factorial(9 - k) for k in range(10)]      # slots owned by a game that ends after k moves
ROOT = np.asarray(TREE_ROOT, dtype=float)
_T = galaxy_tree()
L_SLOT, L_K, L_RES, L_LAST = _T.l_slot, _T.l_k, _T.l_res, _T.l_last
L_CENTRE, L_JIT, L_WEIGHT, L_FAM = _T.l_centre, _T.l_jit, _T.l_weight, _T.l_fam
N_SLOT, N_DEPTH, N_CENTRE = _T.n_slot, _T.n_depth, _T.n_centre
D_IDX, D_W = _T.dust, _T.dust_w
N_GAMES = len(L_SLOT)
assert N_GAMES == 255_168 and NINE_FACT == 362_880
assert np.all(np.diff(L_SLOT) > 0)                # the program's order is the clockwise order
BY_K = {k: int((L_K == k).sum()) for k in range(5, 10)}
assert BY_K == {5: 1_440, 6: 5_328, 7: 47_952, 8: 72_576, 9: 127_872}

EARLY = np.flatnonzero(L_K < 9)                   # the 127,296 games that end before move 9 ...
G_PER = np.array(FACT, dtype=np.int64)[L_K[EARLY]]
G_LEAF = np.repeat(EARLY, G_PER)                  # ... and their ghost games, one per slot they own
_first = np.repeat(np.cumsum(G_PER) - G_PER, G_PER)
G_SLOT = np.repeat(L_SLOT[EARLY], G_PER) + (np.arange(len(G_LEAF)) - _first)
N_GHOSTS = len(G_SLOT)
assert N_GHOSTS == 1_440 * 24 + 5_328 * 6 + 47_952 * 2 + 72_576 * 1 == 235_008
L9 = np.flatnonzero(L_K == 9)                     # the 127,872 games that fill the board (81,792 X wins, 46,080 draws)
assert len(L9) == 127_872 and int((L_RES[L9] == 1).sum()) == 81_792 and int((L_RES[L9] == 3).sum()) == 46_080
assert np.array_equal(np.sort(np.concatenate([G_SLOT, L_SLOT[L9]])), np.arange(NINE_FACT))   # all 9! slots, once
assert np.all(np.diff(G_SLOT) > 0)
WEDGE_GAMES = 255_168

# ring 9 exactly as S02 lays it out (s02_fill.FillOrders.build: fill_ring(9), game A's 24 on the ring itself)
_A9, R9 = fill_ring(9)
R9 = R9.copy()
R9[A_SLOTS] = ring_radius(9)
G_R9 = R9[G_SLOT]
G_DELAY = np.random.default_rng(62).uniform(0.0, 0.14, N_GHOSTS)    # 65-66: the streak's spread
G_BACK = np.random.default_rng(69).uniform(0.0, 0.8, N_GHOSTS)      # 69.1: the stream back


def slot_order(slot: int) -> tuple:
    """The fill order (all 9 squares) at slot `slot` of ring 9 (lexicographic = clockwise)."""
    left, out = list(range(9)), []
    for d in range(9):
        k = (int(slot) // FACT[d + 1]) % (9 - d)
        out.append(left.pop(k))
    return tuple(out)


assert slot_order(10_200)[:5] == (0, 3, 1, 4, 2)   # game A's first fill order (S02 bar 20)

# ---------------------------------------------------------------- the re-run (65.1-67.1): one turn of the arm
RUN = (T65, T67)


def sweep(t: float) -> float:
    """Slots the re-run has passed (no winner check: every slot is a full board, so this is the count)."""
    return NINE_FACT * clamp01((t - RUN[0]) / (RUN[1] - RUN[0]))


def pass_time(slot) -> np.ndarray:
    return RUN[0] + (RUN[1] - RUN[0]) * np.asarray(slot, dtype=float) / NINE_FACT


T_CROSS = float(pass_time(WEDGE_GAMES))           # the counter passes 255,168 ...
assert bb(66, 2.5) <= T_CROSS < bb(66, 3), T_CROSS     # ... at 66.2+ (script.md, check_short.py)
G_PASS = pass_time(L_SLOT[G_LEAF])                # when the arm reaches each ghost's game
G_LAUNCH = G_PASS + 0.08 + G_DELAY
G_FLY = 0.30
L9_PASS = pass_time(L_SLOT[L9])
D_PASS = pass_time(N_SLOT[D_IDX])

# ---------------------------------------------------------------- the camera (S05's last frame) and the turn
CAM_C = tuple(float(v) for v in S05_CAM(S05_END - 1e-6))
assert np.allclose(CAM_C, HANDOVER_S06["cam"])
Z0 = W / CAM_C[2]                                 # 1.045: S05's last frame (the root on screen at (-0.42, 0.26))
Z1 = 1.0                                          # 67.1: S02's zoom, the root further left, so the number
ROOT_SCREEN_1 = np.array([-0.95, 0.24])           # column on the right third clears ring 9
CAM_1 = (float(TREE_ROOT[0] - ROOT_SCREEN_1[0] / Z1), float(TREE_ROOT[1] - ROOT_SCREEN_1[1] / Z1), W / Z1)


def cam_path(t: float):
    """S05's camera until the re-run; during it (65.1-67.1) a slow ease towards S02's framing; then still
    (S02's look is cached for one camera)."""
    if t < T65:
        return CAM_C
    e = ease_in_out_sine(seg(t, T65, T67))
    w = CAM_C[2] * (CAM_1[2] / CAM_C[2]) ** e
    z = W / w
    r0 = (np.asarray(TREE_ROOT) - np.array(CAM_C[:2])) * Z0
    r = r0 + (ROOT_SCREEN_1 - r0) * e
    return float(TREE_ROOT[0] - r[0] / z), float(TREE_ROOT[1] - r[1] / z), w


CAM = Cam(cam_path)
CAM_STILL = Cam(lambda t: CAM_1)
RHO0 = float(s05_rot(S05_END))                    # 7.2°


def _speed(t: float) -> float:
    """The galaxy's turn (x ROT_RATE): S05's 0.35°/s, halted by the tape stop (bar 63), still for the turn
    and the S02 look (S02's fields are cached at one angle), turning again as the galaxy comes back."""
    if t < T63:
        return 1.0
    if t < T64:
        return 1.0 - ease_in_out_sine(seg(t, T63, T64))
    if t < T69:
        return 0.0
    return ease_in_out_sine(seg(t, T69, END))


_RT = np.linspace(0.0, END, 4001)
_RS = np.array([_speed(t) for t in _RT])
_RHO = RHO0 + ROT_RATE * np.concatenate([[0.0], np.cumsum(0.5 * (_RS[1:] + _RS[:-1]) * np.diff(_RT))])


def rho(t: float) -> float:
    """How far the galaxy has turned clockwise about the root (radians)."""
    if t >= END:
        return float(_RHO[-1] + ROT_RATE * (t - END))
    return float(np.interp(t, _RT, _RHO))


RHO_F = rho(T64)                                  # the angle it holds from 64.1 to 69.1
assert abs(rho(T67) - RHO_F) < 1e-12

# ---------------------------------------------------------------- places (screen units) and times
BIG_SCALE = 1.6
BIG_TL = np.array([-6.2, 2.25])                   # 62.1: the plate, centre-left, 1.6x
GLIDE_IN = (0.0, BEAT)                            # 62.1-62.2
GLIDE_OUT = (T65, T65 + BEAT)                     # 65.1-65.2: back to the left edge ...
PLATE_BACK = 0.88                                 # ... a little smaller than in S05: from 65.1 the camera puts ring 9
                                                  # 0.3 left of S05's, through line 33 and the frame at 1.0
HL_ON = (0.25, 0.55)                              # the winner check lights as the plate arrives
TAG_IN = (0.3, 0.7)                               # 62.1+
STRIKE = [(bb(62, 2), bb(62, 2) + 0.28), (bb(62, 2) + 0.1, bb(62, 2) + 0.38)]   # 62.2: lines 24, 25
DIM_T = (0.0, BEAT)                               # the galaxy dims to 40 %
DRAIN = (T63, T63 + 2.05)                         # bar 63: the light drains into the root
RESET = (bb(63, 4), bb(63, 4.5))                  # 63.4: the counter rolls back to 000,000
STRIKE_PULSE = T68                                # 68.1
ERASE = (T69, T69 + 0.35)                         # 69.1: the strike erases
LANDS = [T67 + 0.04 + 0.09 * i for i in range(6)] # 67.1: the digits lock left to right
LABEL_IN = (bb(67, 2), bb(67, 3))                 # 67.2: S02's label flies in from the left
LABEL_OUT = (T69, T69 + 0.4)
DOCK = (T69, bb(69, 3))                           # 69.1-69.3: 362,880 rolls back to 255,168 into the HUD
BACK_FLY = 0.6                                    # 69.1-69.4: each ghost's flight home
S02_SWITCH = 0.2                                  # 67.1: the re-run's picture gives way to S02's look
PEN_PULSES = [bb(62, b) for b in (1, 2, 3, 4)] + [bb(63, b) for b in (1, 2, 3, 4)]
PEN_AMP = [1.0] * 4 + [0.8, 0.6, 0.4, 0.2]        # the pulse dies with the tape stop; none in bar 64
HERO_NUM_C = np.array([HERO_C[0] - 0.15, 0.62])   # 362,880 where S05 landed 255,168 (the label docks under it)
MATHS_Y, TAG_Y = -0.16, -0.62
HERO_VALUE = NINE_FACT
DIM_GALAXY = 0.40
RERUN_DUST = 0.4                                  # 65-66: the inner rings empty out (their nodes stay, faint)
SHIMMER = 0.2                                     # 67.2-70.1: the ring's shimmer, +-20 % of its light (7 % did not
                                                  # show through the tone map: the hold 67.3-69.1 read as still)
FEATHER, TAG_FEATHER = 0.35, 0.14                 # the backings' soft edges (screen units, at the plate's 1.6x)
THIN = "\u2009"                                   # a thin space: "9 !" in EB Garamond italic, so the "!" clears the 9


# ---------------------------------------------------------------- light: S05's galaxy look, with an unglowing layer
def render_light(splat: Splatter, glow_fams, flat_fams=(), glow_px: float = 7.0, glow_amount: float = 0.55,
                 gain: float = 1.0, gamma: float = 0.75) -> np.ndarray:
    """common.Splatter.render with a second set of families that get no glow (ghost games never glow): both are
    summed in light and tone-mapped together, with headroom."""
    from scipy.ndimage import gaussian_filter
    h, w = splat.h, splat.w
    h2, w2 = h // 2, w // 2
    acc = np.zeros((3, h, w), np.float32)
    for img, col in glow_fams:
        if img is None:
            continue
        for c in range(3):
            if col[c] > 0:
                acc[c] += np.float32(col[c]) * img
    dens = np.float32(splat.scale * splat.scale)
    small = acc[:, :h2 * 2, :w2 * 2].reshape(3, h2, 2, w2, 2).sum(axis=(2, 4))
    sig = max(0.5, glow_px * splat.scale / 2)
    glow = gaussian_filter(small, (0, sig, sig), truncate=2.5)
    acc *= dens
    acc[:, :h2 * 2, :w2 * 2] += np.repeat(np.repeat(glow, 2, axis=1), 2, axis=2) * np.float32(glow_amount * dens / 4)
    for img, col in flat_fams:
        if img is None:
            continue
        for c in range(3):
            if col[c] > 0:
                acc[c] += np.float32(col[c]) * img * dens
    lut = _galaxy_lut(round(gain, 4), round(gamma, 4))
    idx = np.minimum(acc * np.float32(_LUT_SCALE), np.float32(len(lut) - 1)).astype(np.int32)
    return np.ascontiguousarray(lut[idx].transpose(1, 2, 0))


def galaxy_families(splat: Splatter, t: float, cam: Cam, rh: float, leaf_w=1.0, dust_w=1.0, leaves=None,
                    dust_depth_min: int = 0):
    """S05's galaxy as splat families: every game at its slot (weight (9 - k)! slots x GALAXY_SLOT_W x zoom^2,
    in its result's colour) and the internal nodes as faint dust. leaf_w / dust_w: multipliers (scalars or per
    point); `leaves`: an index subset."""
    z = cam.zoom(t)
    zf = z * z
    idx = np.arange(N_GAMES) if leaves is None else leaves
    P = galaxy_point(L_CENTRE[idx], L_K[idx], 0.0, 1.0, rh, L_JIT[idx])
    S = cam.to_screen(P, t)
    wts = L_WEIGHT[idx] * zf * (leaf_w if np.ndim(leaf_w) == 0 else np.asarray(leaf_w)[idx])
    fam = L_FAM[idx]
    out = []
    for f in range(3):
        sel = fam == f
        out.append((splat.accumulate(S[sel], wts[sel]), GALAXY_COLOURS[f]))
    dsel = N_DEPTH[D_IDX] >= dust_depth_min
    di = D_IDX[dsel]
    DP = galaxy_point(N_CENTRE[di], N_DEPTH[di], 0.0, 1.0, rh)
    dw = D_W[dsel] * GALAXY_DUST_W[N_DEPTH[di]] * zf * (dust_w if np.ndim(dust_w) == 0 else dust_w[dsel])
    out.append((splat.accumulate(cam.to_screen(DP, t), dw), GALAXY_COLOURS[3]))
    return out


# ---------------------------------------------------------------- S02's look of the tree of fill orders
class FillLook:
    """S02's tree of fill orders, drawn as s02_fill draws it at 18.1 (DotSplat.draw_layers with FILL_SPLAT for
    rings 5-9 and SPARSE for rings 2-4, FILL_WEIGHT x envelope x INNER_GAIN x subsampling, the same jitter, the
    same tone map), at this scene's camera and turn. Points that do not move are cached as intensity fields once;
    `image(...)` adds the moving ones, tone-maps and returns the light (premultiplied RGB on black, what S02's
    image shows). Ring 9 is split into the slots of the move-9 games and the ghost slots."""

    def __init__(self, cam: Cam, rh: float):
        self.q = config.pixel_height / 1080.0
        ppu = config.pixel_height / H * 0.5
        self.res = (max(8, int(round(W * ppu))), max(8, int(round(H * ppu))))
        self.cam, self.rh = cam, rh
        self.tree = dict(size_px=FILL_SPLAT["size_px"], glow_px=FILL_SPLAT["glow_px"],
                         glow_amount=FILL_SPLAT["glow_amount"])
        self.sparse = dict(size_px=SPARSE["size_px"], glow_px=SPARSE["glow_px"], glow_amount=SPARSE["glow_amount"])
        self.gain = FILL_SPLAT["gain"]
        assert SPARSE["gain"] == self.gain
        self.lut = _tone_lut(tuple(np.round(np.asarray(FILL_COLOR, dtype=float), 4)))
        self.fields = {}
        w_, h_ = self.res
        xs = (np.arange(w_) + 0.5) / w_ * W - W / 2
        ys = H / 2 - (np.arange(h_) + 0.5) / h_ * H
        rs = cam.to_screen(ROOT, 0.0)
        self.theta = np.arctan2(xs[None, :] - rs[0], ys[:, None] - rs[1]).astype(np.float32)   # for the shimmer

    def screen(self, ang, rad) -> np.ndarray:
        return self.cam.to_screen(np.stack([ROOT[0] + rad * np.sin(ang + self.rh), ROOT[1] + rad * np.cos(ang + self.rh)],
                                           axis=-1), 0.0)

    def field(self, pts, weights, look) -> np.ndarray:
        """explainer.short.splat up to its intensity (bilinear splat, gaussian core + glow), one channel."""
        from scipy.ndimage import gaussian_filter
        w_, h_ = self.res
        acc = np.zeros(h_ * w_, np.float64)
        u = (pts[:, 0] + W / 2) / W * w_ - 0.5
        v = (H / 2 - pts[:, 1]) / H * h_ - 0.5
        keep = (u > -2) & (u < w_ + 1) & (v > -2) & (v < h_ + 1)
        u, v = u[keep], v[keep]
        base = np.broadcast_to(np.asarray(weights, dtype=float), (len(keep),))[keep] * self.q
        iu, iv = np.floor(u).astype(int), np.floor(v).astype(int)
        fu, fv = u - iu, v - iv
        for du, dv, wt in ((0, 0, (1 - fu) * (1 - fv)), (1, 0, fu * (1 - fv)), (0, 1, (1 - fu) * fv), (1, 1, fu * fv)):
            x, y = iu + du, iv + dv
            ok = (x >= 0) & (x < w_) & (y >= 0) & (y < h_)
            acc += np.bincount((y * w_ + x)[ok], (wt * base)[ok], h_ * w_)
        a = acc.reshape(h_, w_).astype(np.float32)
        s, g = look["size_px"] * self.q, look["glow_px"] * self.q
        core = gaussian_filter(a, s, truncate=3.0) * np.float32((2 * np.pi * s ** 2) ** 0.5)
        soft = gaussian_filter(a, g, truncate=3.0) * np.float32((2 * np.pi * g ** 2) ** 0.5)
        return core + np.float32(look["glow_amount"]) * soft

    def build(self):
        """The static fields (unit weight per point): ring 9's move-9 slots and ghost slots, rings 5-8 (S02's
        subsampling), the sparse rings 2-4."""
        if self.fields:
            return
        a9 = 2 * np.pi * (np.arange(NINE_FACT) + 0.5) / NINE_FACT
        real = L_SLOT[L9]
        self.fields["9 real"] = self.field(self.screen(a9[real], R9[real]), 1.0, self.tree)
        self.fields["9 ghost"] = self.field(self.screen(a9[G_SLOT], R9[G_SLOT]), 1.0, self.tree)
        for d in range(2, 9):
            ang, rad = fill_ring(d)
            sub = RING_SUB.get(d, 1)
            idx = np.arange(0, len(ang), sub)
            self.fields[d] = self.field(self.screen(ang[idx], rad[idx]), 1.0, self.tree if d >= 5 else self.sparse)

    @staticmethod
    def envelopes(t2: float) -> dict:
        """S02's weights per point at S02 time t2 (s02_fill.FillOrders.ring_points / update_tree, after the
        rings have landed): ring 9 with its flare, rings 5-8 settling to a fainter dust, rings 2-4 sparse."""
        def landed(d):
            return 1.0 + 1.3 * pulse(t2, S02_RING_T[d] + S02_SWEEP[d] * 0.5 + S02_FLIGHT[d], 0.45)
        dim = 1.0 - 0.25 * ease_in_out_sine(seg(t2, S02_HIT, S02_HIT + 1.2))
        out = {9: FILL_WEIGHT[9] * landed(9) * fill_flare(t2 - S02_HIT) * INNER_GAIN[9] * RING_SUB.get(9, 1)}
        for d in range(5, 9):
            out[d] = FILL_WEIGHT[d] * landed(d) * dim * INNER_GAIN[d] * RING_SUB.get(d, 1)
        out[2] = dim * SPARSE_WEIGHT[2]
        for d in (3, 4):
            out[d] = landed(d) * dim * SPARSE_WEIGHT[d]
        return out

    def image(self, t2: float, real: float = 1.0, ghost: float = 1.0, inner: float = 1.0, moving=None,
              shimmer: float = 0.0, t: float = 0.0) -> np.ndarray:
        self.build()
        env = self.envelopes(t2)
        ring9 = self.fields["9 real"] * np.float32(env[9] * real)
        if ghost > 1e-4:
            ring9 = ring9 + self.fields["9 ghost"] * np.float32(env[9] * ghost)
        if shimmer > 0:
            th = self.theta
            # bright patches drifting round the ring (two waves turning opposite ways): the hold's ALIVE
            ring9 = ring9 * (1 + np.float32(shimmer) * np.sin(23 * th - 2.6 * t) * np.sin(9 * th + 1.5 * t))
        inten = ring9
        if inner > 1e-4:
            for d in range(2, 9):
                inten = inten + self.fields[d] * np.float32(env[d] * inner)
        if moving is not None:
            pts, wts = moving
            if len(pts):
                inten = inten + self.field(pts, wts * env[9], self.tree)
        v = 1.0 - np.exp(np.float32(-self.gain) * inten)
        rgba = self.lut[np.clip((v * 1023).astype(np.int32), 0, 1023)]
        return (rgba[..., :3].astype(np.uint16) * rgba[..., 3:4] // 255).astype(np.uint8)


# ---------------------------------------------------------------- the hero counter (S05's landing, neutral)
class HeroCounter:
    """The six-digit Inter Black odometer of S05's landing (common.title_counter's setting at HERO_SIZE), white
    core, with a stacked glow per glyph and a halo sprite in one colour (neutral for 362,880)."""

    def __init__(self, value: int, centre, size: float, glow_color: str = INK, halo_color: str = PEN_HALO):
        from explainer.short import RollingCounter
        self.value = int(value)
        self.c0 = np.asarray(centre, dtype=float)
        self.cnt = RollingCounter(self.value, digits=6, size=size, color=WHITE, leading_zeros=True)
        self.cnt.clear_updaters()
        self.cnt.move_to([*self.c0, 0])
        self.cnt.layout()
        self.w0 = self.cnt.ref.width
        glyphs = []
        for col in self.cnt.columns:
            glyphs.append([g for g in col if g.get_fill_opacity() > 0.99][0].copy())
        for _, sep in self.cnt.separators:
            glyphs.append(sep.copy())
        self.offs = [g.get_center()[:2] - self.c0 for g in glyphs]
        self.glow = []
        for g in glyphs:
            layers = []
            for k in range(7, 0, -1):
                c = g.copy().set_fill(opacity=0).set_stroke(glow_color, width=0, opacity=0)
                layers.append((c, 0.62 * (1 - k / 8) ** 2, stroke_px(2 * 22 * size / 178) * k / 7, c.height))
            self.glow.append(layers)
        self.glow_group = VGroup(*[c for lay in self.glow for c, _, _, _ in lay])
        self.halo = gaussian_sprite(halo_color, 96, 0.34, aspect=3.0)
        self.halo_w0, self.halo_h0 = 12.8 * size / 178, 4.3 * size / 178
        self.halo.stretch_to_fit_width(self.halo_w0).stretch_to_fit_height(self.halo_h0)
        self.digits = [int(ch) for ch in f"{self.value:06d}"]

    def hide(self):
        gl = counter_glyphs(self.cnt)
        uncull(gl)
        for col in self.cnt.columns:
            for g in col:
                g.set_opacity(0)
        for _, sep in self.cnt.separators:
            sep.set_opacity(0)
        cull(gl)
        for lay in self.glow:
            for c, _, _, _ in lay:
                uncull([c])
                c.set_stroke(width=0, opacity=0)
                cull([c])
        show_sprite(self.halo, opacity=0)

    def show(self, centre, scale: float, vis: float, positions=None, value=None, glow: float = 1.0,
             glow_each=None, halo: float = 0.5, color=WHITE):
        cnt = self.cnt
        gl = counter_glyphs(cnt)
        uncull(gl)
        cur = cnt.ref.width / self.w0
        if abs(scale / cur - 1) > 1e-6:
            cnt.scale(scale / cur)
        cnt.ref.move_to([centre[0], centre[1], 0])
        if positions is not None:
            cnt.manual = list(positions)
            cnt.manual_top = 999_999
        else:
            cnt.manual = None
            cnt.value.set_value(float(self.value if value is None else value))
        cnt.layout()
        for col in cnt.columns:
            for g in col:
                g.set_fill(color, opacity=g.get_fill_opacity() * vis)
        for _, sep in cnt.separators:
            sep.set_fill(color, opacity=vis)
        cull(gl)
        for i, lay in enumerate(self.glow):
            v = glow * (1.0 if glow_each is None else glow_each[i]) * vis
            for c, base, wk, h0 in lay:
                uncull([c])
                if v <= 1e-3:
                    c.set_stroke(width=0, opacity=0)
                    cull([c])
                    continue
                kk = h0 * scale / max(1e-6, c.height)
                if abs(kk - 1) > 1e-6:
                    c.scale(kk)
                c.move_to([*(np.asarray(centre) + self.offs[i] * scale), 0])
                c.set_stroke(width=wk * scale, opacity=clamp01(base * v))
        show_sprite(self.halo, centre, self.halo_w0 * scale, self.halo_h0 * scale, halo * vis)


def show_plate(plate: ProgramPlate, frame_vis: float, row_vis, hl=None, tl=None, scale: float = 1.0,
               tag_vis: float | None = None):
    """common.ProgramPlate.show with the frame and tag faded apart from the lines (bar 64 keeps only the struck
    check)."""
    hl = hl or {}
    tl = plate.tl if tl is None else np.asarray(tl, dtype=float)
    k = scale
    c = tl + k * np.array([plate.width / 2, -plate.height / 2])
    plate.frame.show(1.0, np.eye(2) * k, c, vis=0.6 * frame_vis)
    base = rgb(INK_DIM)
    for j, (num, lnum, txt, lw, tw, y, ind) in enumerate(plate.rows):
        lv = row_vis[j]
        amt, col = hl.get(num, (0.0, WHITE))
        tc = base * (1 - amt) + rgb(col if col != WHITE else "#F2F4F4") * amt
        tc = hex_of(tc)
        yy = tl[1] + k * y
        if lv <= 1e-3:
            lnum.hide()
            txt.hide()
        else:
            lnum.show([tl[0] + k * (0.1 + lw / 2), yy], scale=k, vis=lv * 0.8, color=INK_DIM)
            txt.show([tl[0] + k * (0.5 + ind + (tw - ind) / 2), yy], scale=k, vis=lv, color=tc)
        if num in plate.bars:
            b = plate.bars[num]
            b.stretch_to_fit_width((plate.width - 0.12) * k).stretch_to_fit_height(plate.pitch * 0.92 * k)
            b.move_to([c[0], yy, 0])
            b.set_fill(col, opacity=clamp01(0.13 * amt * lv))
    tv = frame_vis if tag_vis is None else tag_vis
    if tv <= 1e-3:
        plate.tag_zh.hide()
        plate.tag_en.hide()
    else:
        plate.tag_zh.show(tl + k * np.array([0.18, 0.17]), scale=k, vis=tv, color=INK_DIM)
        plate.tag_en.show(tl + k * np.array([0.42 + plate.tag_en.tmpl.width / 2, 0.17]), scale=k, vis=tv,
                          color=INK_DIM)


def soft_panel(w: float, h: float, feather: float, ppu: float = 40.0):
    """A dark backing (black, RGBA) w x h screen units whose alpha falls off smoothly over `feather` units at its
    edges, so it dims what is behind it without cutting a hard-edged rectangle into the galaxy."""
    from manim import ImageMobject
    wp, hp = max(8, int(round(w * ppu))), max(8, int(round(h * ppu)))
    x = (np.arange(wp) + 0.5) / ppu
    y = (np.arange(hp) + 0.5) / ppu
    ax = np.clip(np.minimum(x, w - x) / feather, 0, 1)
    ay = np.clip(np.minimum(y, h - y) / feather, 0, 1)
    a = np.outer(ay * ay * (3 - 2 * ay), ax * ax * (3 - 2 * ax))
    img = np.zeros((hp, wp, 4), np.uint8)
    img[..., 3] = np.clip(255 * a, 0, 255).astype(np.uint8)
    im = ImageMobject(img)
    im.set_resampling_algorithm(2)
    return im


def ring_edge_paths():
    """The 81 nodes of rings 1-2 as (slot centre, depth, parent slot centre, parent depth)."""
    out = []
    for i in np.flatnonzero((N_DEPTH >= 1) & (N_DEPTH <= 2)):
        d = int(N_DEPTH[i])
        par = N_SLOT[i] - N_SLOT[i] % FACT[d - 1] if d > 1 else 0
        out.append((float(N_CENTRE[i]), d, float(par + FACT[d - 1] / 2) if d > 1 else 0.0, d - 1, int(N_SLOT[i])))
    assert len(out) == 81
    return out


EDGES = ring_edge_paths()
S05_SKIPS = {0, 1}                                # S05's last frame lacks the walk's two edges: X0 (ring 1), X0 O1
assert EDGES[0][4] == 0 and EDGES[0][1] == 1 and EDGES[1][4] == 0 and EDGES[1][1] == 2
NO_LEAVES = np.zeros(0, np.int64)
RING1_DUST = (N_DEPTH[D_IDX] == 1).astype(float)


def edge_ends(e, rh: float):
    c, d, pc, pd, _ = e
    a = galaxy_point(c, d, 0.0, 1.0, rh)
    b = ROOT.copy() if pd == 0 else galaxy_point(pc, pd, 0.0, 1.0, rh)
    return b, a


HANDOVER_S07 = {"cam": CAM_1, "rho_end": rho(END), "rot_rate": ROT_RATE, "plate_dim": PLATE_DIM,
                "plate_scale": PLATE_BACK, "games": WEDGE_GAMES, "pen_vis": 0.9, "edge_vis": 0.38}


# ---------------------------------------------------------------- the scene
class DeleteCheck(BeatScene):

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
        self.fill = FillLook(CAM_STILL, RHO_F)
        self.root = MiniBoard(0.14, 0, 0, nums=0)
        self.edges = [Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK_DIM, 1.2) for _ in EDGES]
        self.arm = Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), INK, 1.4, PEN_HALO, 10, layers=4, glow_opacity=0.35)
        self.streak = Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), "#FFFFFF", 2.6, PEN_HALO, 16, layers=5, glow_opacity=0.6)
        # screen space: the backing, the plate (and two motion-blur copies), the strike, the tag, the pen, HUD
        self.plate = ProgramPlate()
        bw, bh = self.plate.width * BIG_SCALE + 0.3, self.plate.height * BIG_SCALE + 0.55
        self.backing = soft_panel(bw + 2 * FEATHER, bh + 2 * FEATHER, FEATHER)      # (feathered: no hard edges)
        self.backing_pad = (2 * FEATHER / bw, 2 * FEATHER / bh)
        show_sprite(self.backing, opacity=0)
        self.blur = [ProgramPlate() for _ in range(2)]
        self.strikes = [Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), RED, 2.6, RED, 9, layers=4, glow_opacity=0.5)
                        for _ in range(2)]
        tag = bi_label("判断输赢", "WINNER CHECK", zh_size=20, en_size=16.5, color=INK)
        tag[2].set_color(INK_DIM)
        self.tag_w, self.tag_h = tag.width, tag.height
        self.tag_backing = soft_panel(self.tag_w + 0.3 + 2 * TAG_FEATHER, self.tag_h + 0.24 + 2 * TAG_FEATHER,
                                      TAG_FEATHER)
        show_sprite(self.tag_backing, opacity=0)
        self.tag_parts = [InkText(tag[0], INK), InkText(tag[1], INK_DIM), InkText(tag[2], INK_DIM)]
        self.tag_offs = [p.get_center()[:2] - tag.get_center()[:2] for p in tag]
        self.bracket = Ink(VGroup(Line([0, 0.5, 0], [0.5, 0.5, 0]), Line([0.5, 0.5, 0], [0.5, -0.5, 0]),
                                  Line([0.5, -0.5, 0], [0, -0.5, 0])), INK_DIM, 1.3)
        self.pen = Pen()
        self.sec = section_hud("§3 · 探索每一局 · PLAY EVERY GAME")
        self.hud_games = HudLine("对局计数", "GAMES COUNTED", HUD_LINES_Y[0])
        self.hud_calls = HudLine("调用次数", "CALLS", HUD_LINES_Y[1])
        self.hud_undos = HudLine("撤销次数", "UNDOS", HUD_LINES_Y[2])
        from explainer.short import RollingCounter
        self.red_mark = RollingCounter(WEDGE_GAMES, digits=6, size=12, color=RED, font=FONT_MONO, weight="NORMAL",
                                       leading_zeros=True)
        self.red_mark.clear_updaters()
        hc = self.hud_games.counter
        self.red_c = np.array([hc.ref.get_center()[0], HUD_LINES_Y[1]])
        self.red_mark.move_to([*self.red_c, 0])
        self.red_mark.layout()
        self.red_halo = gaussian_sprite(RED, 64, 0.3, aspect=2.6)
        # 67.1: the hero and S02's label
        self.hero = HeroCounter(HERO_VALUE, HERO_NUM_C, HERO_SIZE)
        # (lining figures: a 1 is not an I; a thin space keeps the italic "!" off the 9's tail, where "9!" reads "9/")
        m = maths(f"9 × 8 × … × 1 = 9{THIN}! = 362,880", size=28, color=INK)
        lab = bi_label("9 的阶乘", "NINE FACTORIAL", zh_size=20, en_size=16.5, color=INK_DIM)
        self.maths = [InkText(m, INK) for _ in range(3)]
        self.lab9 = [InkText(lab, INK_DIM) for _ in range(3)]
        self.maths_glow = gaussian_sprite(PEN_HALO, 64, 0.3, aspect=4.0)
        assert m.width < 2 * (W / 2 - 0.45 - HERO_NUM_C[0]) + 0.6 and lab.width < 2 * (W / 2 - 0.45 - HERO_NUM_C[0]) + 0.2

        self.clock_mob = Mobject()
        self.clock_mob.add_updater(lambda mob: self.update_state(self.clock()))
        self.add(self.clock_mob, self.camera.frame)
        self.add(self.galaxy, *self.edges, self.arm, self.root.group, self.streak)
        self.fix(self.backing, *[b.group for b in self.blur], self.plate.group, *self.strikes, self.bracket,
                 self.tag_backing, *self.tag_parts, self.pen, self.sec, self.hud_games.group, self.hud_calls.group,
                 self.hud_undos.group, self.red_halo, self.red_mark, self.hero.halo, self.hero.glow_group,
                 self.hero.cnt, self.maths_glow, *self.maths, *self.lab9)
        self.update_state(0.0)

    # ------------------------------------------------------------- the picture at time t
    def update_state(self, t: float):
        cx, cy, w = CAM(t)
        self.camera.frame.set(width=w)
        self.camera.frame.move_to([cx, cy, 0])
        self.galaxy.move_to([cx, cy, 0])
        rh = rho(t)
        self.update_galaxy(t, rh)
        self.update_edges(t, rh)
        self.update_arm(t, rh)
        self.update_root(t)
        self.update_plate(t)
        self.update_pen(t)
        self.update_hud(t)
        self.update_hero(t)
        self.update_label(t)

    # --- the galaxy's light, phase by phase
    def update_galaxy(self, t: float, rh: float):
        sp = self.splat
        if t < T64:                                              # S05's galaxy, dimmed, then drained (bar 63)
            dim = 1 - (1 - DIM_GALAXY) * ease_in_out_sine(seg(t, *DIM_T))
            if t < DRAIN[0]:
                self.galaxy.light = render_light(sp, galaxy_families(sp, t, CAM, rh, leaf_w=dim, dust_w=dim),
                                                 **GALAXY_LOOK)
                return
            self.galaxy.light = self.drain_light(t, rh, dim)
            return
        if t < T65:                                              # bar 64: nothing
            self.galaxy.light = None
            return
        if t < T67 + S02_SWITCH:                                 # the re-run
            light = self.rerun_light(t, rh)
            if t >= T67:                                         # ... gives way to S02's look under its flare
                a = 1 - seg(t, T67, T67 + S02_SWITCH)
                fill = self.fill_light(t, rh)
                light = np.maximum((light.astype(np.float32) * a).astype(np.uint8), fill)
            self.galaxy.light = light
            return
        self.galaxy.light = self.fill_light(t, rh)

    def drain_light(self, t: float, rh: float, dim: float) -> np.ndarray:
        """Bar 63: every point spirals into the root, accelerating, and fades (the tape stop)."""
        sp = self.splat
        z = CAM.zoom(t)
        zf = z * z
        r = 2.9 * (L_K / 9.0) ** 0.75 + L_JIT
        dr = 2.9 * (N_DEPTH[D_IDX] / 9.0) ** 0.75
        e_now = ease_in_cubic(seg(t, *DRAIN))
        fams = [[None, GALAXY_COLOURS[f]] for f in range(4)]
        for lag, lw in ((0.0, 1.0), (0.05, 0.45), (0.1, 0.2)):         # the frame and two blur copies
            if lag and e_now < 0.05:
                continue
            e = ease_in_cubic(seg(t - lag, *DRAIN))
            k = 1 - e
            spin = 1.6 * e * e                                        # radians, clockwise
            th = 2 * np.pi * L_CENTRE / NINE_FACT + rh + spin * (1.2 - 0.35 * L_K / 9.0)
            P = np.stack([ROOT[0] + r * k * np.sin(th), ROOT[1] + r * k * np.cos(th)], axis=-1)
            S = CAM.to_screen(P, t)
            wl = L_WEIGHT * zf * dim * (1 - e_now) ** 1.5 * lw
            for f in range(3):
                sel = L_FAM == f
                img = sp.accumulate(S[sel], wl[sel])
                fams[f][0] = img if fams[f][0] is None else fams[f][0] + img
            dth = 2 * np.pi * N_CENTRE[D_IDX] / NINE_FACT + rh + spin * 1.2
            DP = np.stack([ROOT[0] + dr * k * np.sin(dth), ROOT[1] + dr * k * np.cos(dth)], axis=-1)
            dw = D_W * GALAXY_DUST_W[N_DEPTH[D_IDX]] * zf * dim * (1 - e_now) ** 1.5 * lw
            img = sp.accumulate(CAM.to_screen(DP, t), dw)
            fams[3][0] = img if fams[3][0] is None else fams[3][0] + img
        return render_light(sp, [tuple(f) for f in fams], **GALAXY_LOOK)

    def rerun_light(self, t: float, rh: float) -> np.ndarray:
        """65.1-67.1: the arm passes every slot; games that end before move 9 stream into their ghosts."""
        sp = self.splat
        zf = CAM.zoom(t) ** 2
        fams_glow, fams_flat = [], []
        # the move-9 games: as in S05 (appear, flare)
        n9 = int(np.searchsorted(L9_PASS, t, side="right"))
        if n9:
            idx = L9[:n9]
            age = t - L9_PASS[:n9]
            wl = L_WEIGHT[idx] * zf * np.clip(age / 0.08, 0, 1) * (1 + 2.6 * np.exp(-np.maximum(age, 0) / 0.28))
            P = galaxy_point(L_CENTRE[idx], 9, 0.0, 1.0, rh, L_JIT[idx])
            S = CAM.to_screen(P, t)
            fam = L_FAM[idx]
            for f in (0, 2):
                sel = fam == f
                fams_glow.append((sp.accumulate(S[sel], wl[sel]), GALAXY_COLOURS[f]))
        # the ghosts of the games that end earlier: at their game until launch, in flight (a pale streak), landed
        ng = int(np.searchsorted(G_PASS, t, side="right"))
        if ng:
            gl = G_LEAF[:ng]
            age = t - G_PASS[:ng]
            fl = np.clip(age / 0.08, 0, 1) * (1 + 2.6 * np.exp(-np.maximum(age, 0) / 0.28))
            w0 = GALAXY_SLOT_W * zf
            landed = t >= G_LAUNCH[:ng] + G_FLY
            # landed: grey, unglowing, on S02's ring 9 positions
            li = np.flatnonzero(landed)
            if len(li):
                a9 = 2 * np.pi * (G_SLOT[li] + 0.5) / NINE_FACT + rh
                P = np.stack([ROOT[0] + G_R9[li] * np.sin(a9), ROOT[1] + G_R9[li] * np.cos(a9)], axis=-1)
                fams_flat.append((sp.accumulate(CAM.to_screen(P, t), np.full(len(li), w0)), GALAXY_COLOURS[3]))
            fi = np.flatnonzero(~landed)
            if len(fi):
                lf = gl[fi]
                r0 = 2.9 * (L_K[lf] / 9.0) ** 0.75 + L_JIT[lf]
                a0 = 2 * np.pi * L_CENTRE[lf] / NINE_FACT
                a1 = 2 * np.pi * (G_SLOT[fi] + 0.5) / NINE_FACT
                r1 = G_R9[fi]
                for lag, lw in ((0.0, 1.0), (0.03, 0.45), (0.06, 0.22)):
                    u = np.clip((t - lag - G_LAUNCH[fi]) / G_FLY, 0, 1)
                    e = u * u * (3 - 2 * u)
                    if lag > 0:
                        moving = (e > 0.02) & (e < 0.98)
                        if not moving.any():
                            continue
                    else:
                        moving = np.ones(len(fi), bool)
                    rr = r0 + (r1 - r0) * e
                    aa = a0 + (a1 - a0) * e + rh
                    P = np.stack([ROOT[0] + rr * np.sin(aa), ROOT[1] + rr * np.cos(aa)], axis=-1)[moving]
                    S = CAM.to_screen(P, t)
                    ww = (w0 * fl[fi] * lw)[moving]
                    em = e[moving]
                    fam = L_FAM[lf][moving]
                    for f in range(2):                               # the game's colour fades as it streams ...
                        sel = fam == f
                        if sel.any():
                            fams_glow.append((sp.accumulate(S[sel], (ww * (1 - em))[sel]), GALAXY_COLOURS[f]))
                    pale = ww * 2.2 * em * (1 - em)                  # ... a pale streak ...
                    fams_glow.append((sp.accumulate(S, pale), GALAXY_COLOURS[2]))
                    if lag == 0:                                     # ... and lands as a grey ghost
                        fams_flat.append((sp.accumulate(S, ww * em), GALAXY_COLOURS[3]))
        # the internal nodes, as the arm passes (S05's dust)
        nd = D_PASS <= t
        if nd.any():
            di = D_IDX[nd]
            age = t - D_PASS[nd]
            DP = galaxy_point(N_CENTRE[di], N_DEPTH[di], 0.0, 1.0, rh)
            dw = D_W[nd] * GALAXY_DUST_W[N_DEPTH[di]] * zf * (1 + 1.2 * np.exp(-np.maximum(age, 0) / 0.3))
            dw = dw * np.where(N_DEPTH[di] >= 5, RERUN_DUST, 1.0)
            fams_glow.append((sp.accumulate(CAM.to_screen(DP, t), dw), GALAXY_COLOURS[3]))
        return render_light(sp, fams_glow, fams_flat, **GALAXY_LOOK)

    def fill_light(self, t: float, rh: float) -> np.ndarray:
        """67.1-69.4: S02's look (its 18.1 flare at 67.1); from 69.1 the ghosts stream home and S05's galaxy
        comes back in its colours."""
        t2 = S02_HIT + (t - T67)
        shimmer = SHIMMER * ease_in_out_sine(seg(t, T67 + 0.3, T67 + 1.2))
        if t < T69:
            fill = self.fill.image(t2, shimmer=shimmer, t=t)
            fams = galaxy_families(self.splat, t, CAM, rh, leaves=NO_LEAVES, dust_w=RING1_DUST)
            return np.maximum(fill, render_light(self.splat, fams, **GALAXY_LOOK))
        # 69.1-70.1: the stream home
        real = 1 - ease_in_out_sine(seg(t, T69 + 0.15, T69 + 1.1))
        inner = 1 - ease_in_out_sine(seg(t, T69 + 0.3, T69 + 1.5))
        u = np.clip((t - T69 - G_BACK) / BACK_FLY, 0, 1)
        e = u * u * (3 - 2 * u)
        moving = None
        flying = np.flatnonzero(e < 1)
        if len(flying):
            pts, wts = [], []
            for lag, lw in ((0.0, 1.0), (0.035, 0.4), (0.07, 0.18)):
                ul = np.clip((t - lag - T69 - G_BACK[flying]) / BACK_FLY, 0, 1)
                el = ul * ul * (3 - 2 * ul)
                if lag > 0:
                    keep = (el > 0.02) & (el < 0.98)
                    if not keep.any():
                        continue
                else:
                    keep = np.ones(len(flying), bool)
                fi = flying[keep]
                el = el[keep]
                lf = G_LEAF[fi]
                r0 = G_R9[fi]
                r1 = 2.9 * (L_K[lf] / 9.0) ** 0.75 + L_JIT[lf]
                a0 = 2 * np.pi * (G_SLOT[fi] + 0.5) / NINE_FACT
                a1 = 2 * np.pi * L_CENTRE[lf] / NINE_FACT
                rr = r0 + (r1 - r0) * el
                aa = a0 + (a1 - a0) * el + rh
                P = np.stack([ROOT[0] + rr * np.sin(aa), ROOT[1] + rr * np.cos(aa)], axis=-1)
                pts.append(CAM.to_screen(P, t))
                wts.append(lw * (1 - el) ** 1.5)
            moving = (np.concatenate(pts), np.concatenate(wts))
        if real > 1e-4 or inner > 1e-4 or moving is not None:
            fill = self.fill.image(t2, real=real, ghost=0.0, inner=inner, moving=moving, shimmer=shimmer, t=t)
        else:
            fill = None
        # S05's galaxy: the early games light as their ghosts arrive, the move-9 games take their colours back
        home = np.bincount(G_LEAF, e, minlength=N_GAMES)
        lw = np.ones(N_GAMES)
        lw[EARLY] = home[EARLY] / np.array(FACT, dtype=float)[L_K[EARLY]]
        lw[L9] = 1 - real
        dw = np.where(N_DEPTH[D_IDX] == 1, 1.0, 1 - inner)
        fams = galaxy_families(self.splat, t, CAM, rh, leaf_w=lw, dust_w=dw)
        light = render_light(self.splat, fams, **GALAXY_LOOK)
        return light if fill is None else np.maximum(fill, light)

    # --- the ring 1-2 edges: S05's (79 of them) until the drain, all 81 as the re-run passes them
    def update_edges(self, t: float, rh: float):
        width = 1.0 / CAM.zoom(t)
        for i, (e, ink) in enumerate(zip(EDGES, self.edges)):
            if t < T63:
                vis = 0.0 if i in S05_SKIPS else 0.38
                vis *= 1 - (1 - DIM_GALAXY) * ease_in_out_sine(seg(t, *DIM_T))
                g = 1.0
            elif t < T65:
                vis = (0.0 if i in S05_SKIPS else 0.38 * DIM_GALAXY) * (1 - seg(t, T63, T63 + 1.0))
                g = 1.0
            else:
                tv = float(pass_time(e[4]))
                vis = 0.38 if t >= tv else 0.0
                g = ease_out_cubic(seg(t, tv, tv + 0.2))
            if vis <= 1e-3:
                ink.hide()
                continue
            p, q = edge_ends(e, rh)
            A, c = line_affine(p, q)
            ink.show(g, A, c, vis=vis, width=width)

    def update_arm(self, t: float, rh: float):
        av = 0.0
        if RUN[0] <= t < RUN[1] + 0.3:
            av = seg(t, RUN[0], RUN[0] + 0.12) * (1 - seg(t, RUN[1], RUN[1] + 0.3))
        if av <= 1e-3:
            self.arm.hide()
            self.streak.hide()
            return
        th = 2 * np.pi * sweep(t) / NINE_FACT + rh
        d = np.array([math.sin(th), math.cos(th)])
        width = 1.0 / CAM.zoom(t)
        A, c = line_affine(ROOT + d * 0.05, ROOT + d * 3.12)
        self.arm.show(1.0, A, c, vis=0.3 * av, glow=0.8, width=width)
        A, c = line_affine(ROOT + d * (ring_radius(5) - 0.06), ROOT + d * (ring_radius(9) + 0.06))
        flick = 0.85 + 0.15 * math.sin(97 * t) * math.sin(61 * t)
        self.streak.show(1.0, A, c, vis=0.7 * av * flick, glow=1.0, width=width * 0.8)

    def update_root(self, t: float):
        self.root.place(ROOT, 1.0)
        self.root.draw_grid(1.0, vis=1.0, width=1.0 / CAM.zoom(t))

    # --- the plate: 62.1 it glides in and grows; 62.2 the strike; bar 64 only the check; 65.1 back; 69.1 erased
    def plate_place(self, t: float):
        if t < GLIDE_OUT[0]:
            e = ease_in_out_cubic(seg(t, *GLIDE_IN))
            return PLATE_TL + (BIG_TL - PLATE_TL) * e, 1 + (BIG_SCALE - 1) * e, e
        e = 1 - ease_in_out_cubic(seg(t, *GLIDE_OUT))
        return PLATE_TL + (BIG_TL - PLATE_TL) * e, PLATE_BACK + (BIG_SCALE - PLATE_BACK) * e, e

    def update_plate(self, t: float):
        P = self.plate
        tl, k, e = self.plate_place(t)
        n = len(P.rows)
        check = [j for j, r in enumerate(P.rows) if r[0] in (24, 25)]
        # how visible: S05's 55 %, full while big; bar 63 everything but the check fades; back at 65.1
        base = PLATE_DIM + (1 - PLATE_DIM) * e
        if t < GLIDE_OUT[0]:
            fade = ease_in_out_sine(seg(t, T63 + 0.3, T64))
            others, check_v = 1.0 - fade, base * lerp(1.0, 0.55, fade)
        else:
            g = ease_in_out_sine(seg(t, *GLIDE_OUT))
            others, check_v = g, lerp(0.55, PLATE_DIM, g)
        row_vis = [check_v if j in check else base * others for j in range(n)]
        frame_vis = base * others
        # the check: lit as the plate arrives, RED-tinted once struck, white again when it comes back (69.1)
        hl = {}
        lit = ease_out_cubic(seg(t, *HL_ON))
        struck = ease_out_cubic(seg(t, STRIKE[0][0], STRIKE[1][1]))
        erased = ease_out_cubic(seg(t, *ERASE))
        for num in (24, 25):
            if t < STRIKE[0][0]:
                hl[num] = (lit, WHITE)
            elif t < ERASE[0]:
                hl[num] = (lerp(1.0, 0.5, struck) + 0.35 * pulse(t, STRIKE_PULSE, 0.4), RED)
            else:
                back = pulse(t, ERASE[0] + 0.15, 0.4)
                hl[num] = (max(0.5 * (1 - erased), 0.9 * back), RED if erased < 0.5 else WHITE)
        show_plate(P, frame_vis, row_vis, hl, tl, k)
        # the backing behind the big plate (the galaxy is behind it)
        bo = 0.72 * e * (frame_vis if t >= T63 else 1.0)
        bw, bh = P.width * k + 0.3, P.height * k + 0.55
        show_sprite(self.backing, [tl[0] + P.width * k / 2, tl[1] - P.height * k / 2 + 0.12],
                    bw * (1 + self.backing_pad[0]), bh * (1 + self.backing_pad[1]), bo)
        # motion blur: the plate a few frames back, during the two glides
        for gi, bp in enumerate(self.blur):
            moving = GLIDE_IN[0] < t < GLIDE_IN[1] or GLIDE_OUT[0] < t < GLIDE_OUT[1]
            sp = abs(math.sin(math.pi * seg(t, *(GLIDE_IN if t < GLIDE_OUT[0] else GLIDE_OUT))))
            if not moving or sp < 0.08:
                show_plate(bp, 0.0, [0.0] * n)
                continue
            tlg, kg, _ = self.plate_place(t - 0.035 * (gi + 1))
            op = (0.3, 0.14)[gi] * sp
            show_plate(bp, frame_vis * op, [v * op for v in row_vis], {}, tlg, kg, tag_vis=0.0)
        # the strike: 62.2, across both lines; it pulses on 68.1 and erases (right to left) on 69.1
        glow = 1.0 + 1.6 * pulse(t, STRIKE[0][0] + 0.1, 0.35) + 2.2 * pulse(t, STRIKE_PULSE, 0.45) \
            + 1.5 * pulse(t, ERASE[0], 0.3)
        sv = (1.0 if t < T63 + 0.3 else lerp(1.0, 0.5, seg(t, T63 + 0.3, T64))) if t < GLIDE_OUT[0] else \
            lerp(0.5, 0.85, seg(t, *GLIDE_OUT))
        for (a, b), num, ink in zip(STRIKE, (24, 25), self.strikes):
            f = ease_out_quad(seg(t, a, b)) * (1 - ease_in_out_sine(seg(t, *ERASE)))
            if f <= 1e-3:
                ink.hide()
                continue
            ind = next(r[6] for r in P.rows if r[0] == num)
            y = P.row_y(num, tl, k)
            x0 = tl[0] + k * (0.5 + ind - 0.06)
            x1 = P.row_right(num, tl, k) + 0.06 * k
            A, c = line_affine(np.array([x0, y]), np.array([x1, y]))
            ink.show(f, A, c, vis=sv, glow=glow, width=max(0.6, k ** 0.5), glow_width=max(0.6, k ** 0.5))
        # the tag "判断输赢 · WINNER CHECK", beside the check, while the plate is big
        tv = ease_out_cubic(seg(t, *TAG_IN)) * (1 - ease_in_out_sine(seg(t, T63 + 0.3, T63 + 1.0)))
        if tv <= 1e-3:
            for p in self.tag_parts:
                p.hide()
            self.bracket.hide()
            show_sprite(self.tag_backing, opacity=0)
            return
        y24, y25 = P.row_y(24, tl, k), P.row_y(25, tl, k)
        xb = P.row_right(24, tl, k) + 0.14
        hb = abs(y24 - y25) + 0.16
        self.bracket.show(1.0, np.array([[0.16, 0.0], [0.0, hb]]), np.array([xb, (y24 + y25) / 2]), vis=0.8 * tv)
        cen = np.array([xb + 0.32 + self.tag_w / 2 + 0.06 * (1 - tv), (y24 + y25) / 2])
        show_sprite(self.tag_backing, cen, self.tag_w + 0.3 + 2 * TAG_FEATHER, self.tag_h + 0.24 + 2 * TAG_FEATHER,
                    0.7 * tv)
        for p, off, col in zip(self.tag_parts, self.tag_offs, (INK, INK_DIM, INK_DIM)):
            p.show(cen + off, vis=tv, color=col)

    def update_pen(self, t: float):
        p = CAM.to_screen(ROOT, t)
        g = max([a * pulse(t, tp, 0.25) for tp, a in zip(PEN_PULSES, PEN_AMP) if tp <= t + 1e-6] + [0.0])
        g = max(g, pulse(t, -BEAT, 0.25))                         # (S05's last pulse, 61.4, still fading)
        vis = 0.9
        if RUN[0] <= t < RUN[1] + 0.4:                            # 65-66: the pen is the arm's streak
            vis = 0.9 * (1 - seg(t, RUN[0], RUN[0] + 0.1)) if t < RUN[1] else 0.9 * seg(t, RUN[1], RUN[1] + 0.3)
        self.pen.place(p, vis, glow=1.0 + 0.8 * g)

    # --- the HUD: the counter resets (63.4), races (65-66), passes 255,168 in RED, becomes the hero (67.1)
    def games_value(self, t: float) -> float:
        if t < RESET[0]:
            return float(WEDGE_GAMES)
        if t < RUN[0]:
            return WEDGE_GAMES * (1 - ease_in_out_sine(seg(t, *RESET)))
        if t < RUN[1]:
            return float(int(sweep(t)))
        if t < DOCK[0]:
            return float(NINE_FACT)
        return float(WEDGE_GAMES)

    def update_hud(self, t: float):
        sv = 1 - 0.55 * ease_in_out_sine(seg(t, RESET[1], T64)) * (1 - seg(t, RUN[0], RUN[0] + 0.3))
        if abs(sv - getattr(self, "_sec_v", 1.0)) > 1e-4:          # bar 64: near-black, the HUD label dims too
            for p in self.sec.get_family():
                if len(p.points):
                    p.set_fill(opacity=sv)
            self._sec_v = sv
        v = self.games_value(t)
        vis = 1.0
        if T63 <= t < RUN[0]:
            vis = 1 - 0.6 * ease_in_out_sine(seg(t, RESET[1], T64))
        if t >= RUN[0]:
            vis = lerp(0.4, 1.0, seg(t, RUN[0], RUN[0] + 0.3))
        if T67 <= t:                                              # the hero has it in between (as in S05)
            vis = 0.0 if t < DOCK[1] - 0.25 else seg(t, DOCK[1] - 0.25, DOCK[1])
        red = pulse(t, T_CROSS, 0.35) if t >= T_CROSS else 0.0
        col = hex_of(rgb(INK_DIM) * (1 - red) + rgb(RED) * red)
        self.hud_games.show(v, vis, color=col)
        cu = 1 - seg(t, T63, T63 + 0.6)
        self.hud_calls.show(HANDOVER_S06["calls"], cu)
        self.hud_undos.show(HANDOVER_S06["undos"], cu)
        # the value it overran: left behind in RED under the readout, fading
        rv = (ease_out_cubic(seg(t, T_CROSS, T_CROSS + 0.08)) * (1 - seg(t, T_CROSS + 0.6, T_CROSS + 1.8))
              if t >= T_CROSS else 0.0)
        gl = counter_glyphs(self.red_mark)
        uncull(gl)
        c = self.red_mark
        dy = -0.05 * ease_out_cubic(seg(t, T_CROSS, T_CROSS + 1.8))
        c.ref.move_to([self.red_c[0], self.red_c[1] + dy, 0])
        c.value.set_value(WEDGE_GAMES)
        c.layout()
        for colm in c.columns:
            for g in colm:
                g.set_fill(RED, opacity=g.get_fill_opacity() * rv)
        for _, sep in c.separators:
            sep.set_fill(RED, opacity=rv)
        cull(gl)
        hv = rv * (0.35 + 0.9 * pulse(t, T_CROSS, 0.4)) if t >= T_CROSS else 0.0
        show_sprite(self.red_halo, self.red_c + np.array([0.0, dy]), 1.7, 0.42, hv)

    def update_hero(self, t: float):
        Hc = self.hero
        if not (T67 <= t < DOCK[1]):
            Hc.hide()
            return
        dock = ease_in_out_cubic(seg(t, *DOCK))
        hud = self.hud_games.counter
        k = 1 + (hud.ref.width / Hc.w0 - 1) * dock
        c = HERO_NUM_C + (hud.ref.get_center()[:2] - HERO_NUM_C) * dock
        vis = 1 - seg(t, DOCK[1] - 0.2, DOCK[1])
        if t < DOCK[0]:
            pos = []
            for i, L in enumerate(LANDS):
                u = ease_out_cubic(seg(t, T67, L + 0.12))
                pos.append(Hc.digits[i] + 10 * (1 - u) * (1 + (i % 2)))
            breathe = 1 + 0.14 * math.sin(2 * math.pi * (t - T67) / BAR)
            each = [ease_out_cubic(seg(t, L, L + 0.3)) * breathe + 1.2 * pulse(t, L, 0.25) for L in LANDS + [T67]]
            hv = ease_out_cubic(seg(t, T67, T67 + 0.5)) * (0.42 + 0.06 * math.sin(2 * math.pi * (t - T67) / BAR))
            Hc.show(c, k, vis, positions=pos, glow=1.0, glow_each=each, halo=hv)
            return
        value = HERO_VALUE + (WEDGE_GAMES - HERO_VALUE) * dock    # 362,880 rolls back to 255,168 as it docks
        Hc.show(c, k, vis, value=value, glow=1 - dock, halo=0.42 * (1 - dock))

    def update_label(self, t: float):
        """67.2: "9 × 8 × … × 1 = 9! = 362,880" and "9 的阶乘 · NINE FACTORIAL" fly in from the left (one beat,
        ease-out, two blur copies) and dock under the number; they leave as the ghosts go home (69.1)."""
        v = seg(t, LABEL_IN[0], LABEL_IN[0] + 0.12) * (1 - seg(t, *LABEL_OUT))
        if v <= 1e-3:
            for m in self.maths + self.lab9:
                m.hide()
            show_sprite(self.maths_glow, opacity=0)
            return
        u = ease_out_cubic(seg(t, *LABEL_IN))
        for j in range(3):
            lag = 0.04 * j
            uj = ease_out_cubic(seg(t - lag, *LABEL_IN))
            dx = -2.6 * (1 - uj)
            op = (1.0, 0.32, 0.14)[j] * (abs(math.sin(math.pi * u)) if j else 1.0)
            if j and (u >= 0.999 or op < 0.02):
                self.maths[j].hide()
                self.lab9[j].hide()
                continue
            self.maths[j].show([HERO_NUM_C[0] + dx, MATHS_Y], vis=v * op, color=INK)
            self.lab9[j].show([HERO_NUM_C[0] + dx * 0.8, TAG_Y], vis=v * op * 0.95, color=INK_DIM)
        gl = 0.18 + 0.5 * pulse(t, LABEL_IN[1] - 0.2, 0.5)
        show_sprite(self.maths_glow, [HERO_NUM_C[0], MATHS_Y], 4.6, 0.7, gl * v * u)

    # ------------------------------------------------------------- the sounds (from the same numbers)
    def score(self):
        S = self.sounds
        sx = lambda p, t: float(CAM.to_screen(p, t)[0])
        rx = sx(ROOT, 0.0)
        # bar 62: the pen's pulse goes on (S05's quarter notes). Bar 63 is the tape stop: the composer slows
        # what is already sounding and plays nothing that starts inside it (the drain, the pen's last pulses
        # and the counter's roll back are picture only); bar 64 is digital silence
        S.phrase("pen", [(tp, "pen@D5", rx) for tp in PEN_PULSES[:4]], gain=0.6)
        # 62.1: the tag for the winner check; 62.2: the strike (RED: a reverse whoosh)
        S.phrase("tag", [(TAG_IN[0], "pluck@F#3", -1.0)], gain=0.45)
        S.phrase("strike", [(STRIKE[0][0], "undo", -3.2)], gain=0.9)
        # 65.1-67.1: the swarm: each grain the slot under the arm, a ghost (most of them) or a real full board.
        # It starts one 32nd after the hit: a cue that starts on the silence's last instant is not played
        for bar, step, gain in ((65, BEAT / 8, 0.34), (66, BEAT / 16, 0.42)):
            notes = []
            for j in range(1 if bar == 65 else 0, int(round(BAR / step))):
                tt = bb(bar) + j * step
                s = int(min(NINE_FACT - 1, sweep(tt + 1e-6)))
                g = int(np.searchsorted(L_SLOT, s, side="right")) - 1
                th = 2 * np.pi * s / NINE_FACT + RHO_F
                x = sx(ROOT + ring_radius(9) * np.array([math.sin(th), math.cos(th)]), tt)
                if L_K[g] == 9:
                    res, sq = int(L_RES[g]), int(L_LAST[g])
                    name = "X" if res == 1 else "draw"
                    notes.append((tt, f"{name}@{PITCH[sq]}", x))
                else:
                    sq = slot_order(s)[-1]
                    notes.append((tt, f"ghost@{PITCH[sq]}", x))
            S.phrase(f"swarm {bar}", notes, gain=gain)
        S.phrase("overrun", [(T_CROSS, "undo", 5.5)], gain=0.7)
        # 67.1: S02's bloom chord returns with its flare (s02_fill: all seven notes of D Lydian, rolled)
        bloom = ["D5", "E5", "F#5", "G#5", "A5", "B5", "C#6"]
        S.phrase("bloom", [(T67 + 0.05 * i, f"bell@{n}", 4.0 - 0.3 * i) for i, n in enumerate(bloom)], gain=0.55)
        S.phrase("label", [(LABEL_IN[0], "pluck@A4", 4.6), (LABEL_IN[0] + 0.15, "pluck@E4", 4.6)], gain=0.45)
        # 68.1: the strike pulses; 69.1 it erases and the check is back; the swarm in reverse, dying away
        S.phrase("strike pulse", [(STRIKE_PULSE, "undo", -5.5)], gain=0.5)
        S.phrase("erase", [(ERASE[0], "undo", -5.5)], gain=0.6)
        S.phrase("check back", [(ERASE[0] + 0.15, "glass@A5", -5.0)], gain=0.4)
        back = []
        rng = np.random.default_rng(691)
        for j in range(24):
            tt = T69 + 0.075 * j
            gi = int(rng.integers(N_GHOSTS))
            sq = slot_order(int(G_SLOT[gi]))[-1]
            back.append((tt, f"ghost@{PITCH[sq]}", float(rng.uniform(-3, 3))))
        S.phrase("swarm back", back, gain=0.3)
        S.phrase("dock", [(DOCK[1], "glass@A5", 5.5)], gain=0.45)
        S.log(self)
        self.mark("particles", at=RUN[0] + BEAT / 8, n=N_GHOSTS, sound="ghost", x=round(rx, 2))

    # ------------------------------------------------------------- the logged events and the clock
    def log_events(self):
        ev = self.shots

        def add(t, dur, x, y, w, h):
            ev.append((float(t), float(dur), (x, y, w, h)))
        add(GLIDE_IN[0], BEAT, -3.6, 0.6, 5.0, 3.8)                         # the plate glides in and grows
        add(STRIKE[0][0], 0.4, -4.0, 1.5, 3.8, 0.4)
        add(TAG_IN[0], BEAT, 0.6, 1.4, 3.8, 0.5)
        for k in range(4):                                                  # bar 63: the drain
            add(T63 + k * BEAT, BEAT, -0.42, 0.26, 6.0, 6.0)
        add(RESET[0], 0.3, 5.5, 3.55, 1.0, 0.2)
        add(GLIDE_OUT[0], BEAT, -5.0, 1.8, 3.2, 2.4)
        for k in range(8):                                                  # 65-66: the re-run
            add(RUN[0] + k * BEAT, BEAT, -0.42, 0.26, 6.0, 6.0)
        add(T_CROSS, 0.3, 5.5, 3.3, 1.0, 0.2)
        add(T67, BEAT, *HERO_NUM_C, 4.2, 0.9)
        add(T67, BEAT, -0.42, 0.26, 6.0, 6.0)
        add(LABEL_IN[0], BEAT, HERO_NUM_C[0], -0.4, 4.0, 0.9)
        for k in range(1, 4):
            add(T67 + k * BEAT, BEAT, -0.42, 0.26, 6.0, 6.0)                # the ring shimmers
        for k in range(4):
            add(T68 + k * BEAT, BEAT, -0.42, 0.26, 6.0, 6.0)
        add(STRIKE_PULSE, 0.4, -5.2, 2.3, 2.5, 0.3)
        add(ERASE[0], 0.4, -5.2, 2.3, 2.5, 0.3)
        for k in range(4):                                                  # 69: the stream home, the dock
            add(T69 + k * BEAT, BEAT, -0.42, 0.26, 6.0, 6.0)
        add(DOCK[0], DOCK[1] - DOCK[0], 5.0, 1.8, 4.5, 3.0)

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
