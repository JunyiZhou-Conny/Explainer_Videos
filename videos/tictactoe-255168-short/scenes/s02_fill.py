"""S02 · Fill the board 填满棋盘 — Act I: the tree of fill orders, 9 × 8 × … × 1 = 9! = 362,880 > 255,168.

Bars 12-20 (0:26.4-0:48.0) of script.md; scene time 0 is the downbeat of bar 12. The picture is a pure
function of the scene time (State.update), as in s01_open: every object is placed from a template each
frame, and the notes are computed from the same numbers (Sounds) and logged with one sound tag each.

    12     the root (S01's hand-over) breathes, the pen pulses on beats 1 and 3; a dashed guide for ring 1
           draws clockwise from 12 o'clock (c04, the question)
    13-14  ring 1: the pen sends nine child boards, one per eighth note, X on squares 0 ... 8 clockwise (the
           nine square notes); 14.1 "9" on the right third, the readout 9. Ring 2: the 8 O replies under
           X0 appear one per eighth in a lens and each runs along the lens's leader onto ring 2
    15-17  15.1 the bundle of 8 is copied under the other 8 first moves ("× 8", 72); then one factor per
           half bar (× 7 ring 3, × 6 ring 4, × 5 ring 5) and one per beat (× 4 … × 1, rings 6-9): each
           ring sprays out of its parents, clockwise. The camera pulls out 0.45 -> 1.0 (15.1-17.4)
    18     HIT: ring 9 flares (FILL_WEIGHT / fill_flare in common.py: S06 repeats this frame at 67.1);
           362,880 lands (Inter Black, neutral halo), "= 9! = 362,880" (the 9! upright in Inter), with a
           leader from the 9! to "9! 读作“9 的阶乘” / 9! = NINE FACTORIAL" under it, "所有顺序的树 · THE TREE
           OF ORDERS" (c05); the tree turns 0.5°/s; the frame sits a little low, so ring 9 clears the captions
    19     255,168 drifts in under it (the title's halo, cool left, warm right); 19.2 a RED ">" (c06)
    20     the camera dives (ease-in-expo) into ring 9 at 10.12° (its sideways travel from 20.2): the rings
           streak past (motion blur) and fade to nothing as they reach the caption band, the boards round the
           root fade out before they get there; the numbers stay pinned in frame (c06 asks about them, and the
           streaks fade out behind them: num_mask) and fade over 20.3-20.4 (the tree's tag leaves as the dive
           starts); 20.4 the frame fills with one
           glowing point (sigma capped and floored above the band, so the corners and the captions stay
           dark), which resolves into the 24 dim points of the 24 fill orders that begin with game A's five
           moves (slots 10,200-10,223)

Maths labels use lining figures (maths(): an old-style 1 reads as I), as S04, S06 and S07 do.

Hand-over from S01 (a segue): camera (-2.0, +0.3) at 0.45 of the frame width, the root an empty board
0.42 units wide (2 px hairlines), the pen on its centre. Hand-over to S03 (a cut): the 24 dim points at
ORDER_SCREEN (screen units, a line through (0, 1.0) tilted along the ring), drawn by DotSplat with
ORDER_DOTS; nothing else but the HUD.
"""

from __future__ import annotations

import math

import numpy as np
from manim import LEFT, RIGHT, ImageMobject, Line, MarkupText, Mobject, Text, VGroup, VMobject, config

from explainer.short import (BeatScene, FONT_HEAVY, FONT_MONO, FONT_OLDSTYLE, INK, INK_DIM, RED, WHITE, RollingCounter, cjk,
                             hero_number, splat, stroke_px, tracked)

from common import (FILL_COLOR, FILL_SPLAT, FILL_WEIGHT, GAME_A, H, NINE_FACT, OC, PEN_HALO, TREE_ROOT, XC,
                    Cam, Ink, Pen, Shot, Sounds, W, bi_label, box, clamp01, ease_in_cubic, ease_in_expo,
                    ease_in_out_cubic, ease_in_out_sine, ease_out_cubic, ease_out_quad, fill_flare, fill_ring,
                    gaussian_sprite, grid_lines, lerp, o_template, order_slot, pulse, rgb, ring_radius,
                    section_hud, seg, slot_angle, square_centre, tag, tree_point, x_template)

# ---------------------------------------------------------------- the plan's clock (bar 12 = scene time 0)
BEAT, BAR = 0.6, 2.4
FIRST_BAR = 12


def bb(bar: int, beat: float = 1.0) -> float:
    """Musicians' count, as script.md writes it: bb(14, 1.5) is "14.1+" (scene time)."""
    return (bar - FIRST_BAR) * BAR + (beat - 1) * BEAT


END = bb(21)                                        # 21.6 s: 9 bars

# ---------------------------------------------------------------- numbers (assert what is cheap to assert)
RUNNING = [NINE_FACT // math.factorial(9 - k) for k in range(1, 10)]          # 9, 72, ..., 362,880, 362,880
assert RUNNING == [9, 72, 504, 3_024, 15_120, 60_480, 181_440, 362_880, 362_880]
assert math.prod(range(1, 10)) == NINE_FACT == 362_880
TITLE = 255_168
assert NINE_FACT > TITLE                            # compared, never subtracted (must-get-right item 2)
A_SLOT = order_slot(GAME_A)                         # the 24 fill orders that begin with game A ...
assert A_SLOT == 10_200 and math.factorial(9 - len(GAME_A)) == 24      # ... are slots 10,200-10,223
A_SLOTS = np.arange(A_SLOT, A_SLOT + 24)
assert abs(math.degrees(float(slot_angle(A_SLOT - 0.5))) - 10.119) < 1e-3  # 10.12° clockwise from 12

# ---------------------------------------------------------------- places (world units) and look
ROOT = TREE_ROOT
ROOT_CELL = 0.14                                    # S01's root: an empty board 0.42 wide
KID_CELL = 0.087                                    # ring-1 boards, 0.26 wide
KID_R = ring_radius(1)
R2 = ring_radius(2)
CLOSE = 0.45                                        # the camera's frame width at the start (S01's hand-over)
COL_X = 4.55                                        # the number column on the right third (screen units)
LENS_C = tree_point(math.radians(285), 1.80)        # the lens, left of the root, beside the branch
LENS_R = 0.70
LENS_CELL = 0.090                                   # lens boards, 0.27 wide (larger than ring 1's)
ORDER_Y = 1.0                                       # S03's board centre: the 24 dim points line up through it
ORDER_SPACING = 0.36                                # screen units between the 24 points at the end
DELTA = 2 * math.pi * ring_radius(9) / NINE_FACT    # world distance between neighbouring slots on ring 9

# ---------------------------------------------------------------- times
GUIDE = (bb(12, 1), bb(12, 4))                      # the dashed guide circle for ring 1 draws clockwise
KIDS = [bb(13, 1) + 0.3 * k for k in range(9)]      # 13.1, 13.1+, ..., 14.1: the nine first moves
KID_FLIGHT = 0.3
NINE = bb(14, 1)                                    # "9" lands, readout 9
REPLY_SQ = [s for s in range(9) if s != 0]          # O's 8 replies to X0: squares 1 ... 8
REPLIES = [bb(14, 1) + 0.3 * (j + 1) for j in range(8)]   # 14.1+ ... 15.1
REPLY_RUN = 0.3                                     # each reply's point runs along the leader onto ring 2
LENS_IN = (bb(14, 1), bb(14, 1) + 0.35)
LENS_OUT = (bb(15, 1), bb(15, 1) + 0.4)
BUNDLE = bb(15, 1)                                  # copies of the bundle of 8 drop under the other 8 kids
FACTOR_T = [NINE, BUNDLE, bb(15, 3), bb(16, 1), bb(16, 3), bb(17, 1), bb(17, 2), bb(17, 3), bb(17, 4)]
RING_T = {d: FACTOR_T[d - 1] for d in range(3, 10)}            # ring d sprays on factor d (× 7 ... × 1)
SWEEP = {3: 0.55, 4: 0.55, 5: 0.55, 6: 0.3, 7: 0.3, 8: 0.3, 9: 0.28}     # clockwise launch sweep
FLIGHT = {3: 0.4, 4: 0.4, 5: 0.4, 6: 0.28, 7: 0.28, 8: 0.28, 9: 0.26}
PULL = (bb(15, 1), bb(17, 4))                       # the camera pulls out 0.45 -> 1.0
HIT = bb(18, 1)                                     # ring 9 flares; 362,880
ROW_B_T = HIT + 0.15
TAG9_T = bb(18, 2)
TREE_TAG_T = bb(18, 3)
ROT_RATE = math.radians(0.5)                        # the tree turns 0.5°/s from the hit ...
ROT_STOP = (bb(19, 3), bb(20, 1))                   # ... and comes to rest for the dive
DRIFT_IN = (bb(19, 1), bb(19, 2))                   # 255,168 drifts in under 362,880
GT_T = bb(19, 2)                                    # the RED ">"
DIVE = (bb(20, 1), bb(20, 4))                       # ease-in-expo into ring 9 at 10.12°
RESOLVE = (bb(20, 4), END)                          # the glowing point resolves into 24 dim points
TEXT_OUT = (bb(20, 1), bb(20, 1) + 0.5)             # the HUD readout fades as the dive starts
TRAVEL = (bb(20, 2), bb(20, 4))                     # the dive's sideways travel starts at 20.2 (c06 is read first)
NUM_OUT = (bb(20, 3), bb(20, 4))                    # the right third's numbers stay pinned in frame, then fade
GLOW_SIG_MAX = 2.6                                  # the glowing point at its largest (screen units)
BAND_TOP, BAND_RAMP = -2.72, 0.4                    # the captions' band (Chinese glyph tops at 87 % - 38 px)
BAND_FADE = (BAND_TOP - 0.05, BAND_TOP + 0.45)      # the dive: the tree fades to nothing as it reaches the band
PULSES = ([bb(b, k) for b in (12, 13, 14) for k in (1, 3)] + [bb(15, k) for k in (1, 2, 3, 4)]
          + [bb(16, 1 + 0.5 * k) for k in range(8)] + [bb(17, 1 + 0.25 * k) for k in range(16)])

# ---------------------------------------------------------------- the 24 dim points (S02 -> S03 hand-over)
ORDER_DOTS = dict(size_px=1.3, glow_px=5.5, glow_amount=0.9, gain=1.6, weight=1.25)   # 1080p, resolution 0.5
SPARSE = dict(size_px=0.7, glow_px=1.8, glow_amount=0.55, gain=1.5)   # rings 2-4: discrete points, little glow
TREE_LOOK = dict(color=FILL_COLOR, **FILL_SPLAT)
SPARSE_LOOK = dict(color=FILL_COLOR, **SPARSE)
DOTS_LOOK = dict(color=FILL_COLOR, size_px=ORDER_DOTS["size_px"], glow_px=ORDER_DOTS["glow_px"],
                 glow_amount=ORDER_DOTS["glow_amount"], gain=ORDER_DOTS["gain"])
GRAINS = {3: 6, 4: 8, 5: 10, 6: 6, 7: 6, 8: 6, 9: 6}                 # each ring's spray (sound), denser ...
GRAIN_GAIN = {3: 0.32, 4: 0.36, 5: 0.40, 6: 0.30, 7: 0.32, 8: 0.34, 9: 0.36}   # ... but bar 17 is no louder than 18.1
RING_SUB = {7: 2, 8: 3}                                            # dust rings drawn from every 2nd / 3rd point
SPARSE_WEIGHT = {2: 1.5, 3: 0.85, 4: 0.13}
INNER_GAIN = {5: 0.7, 6: 0.6, 7: 0.55, 8: 0.55, 9: 1.0}            # rings 5-8: fainter dust under ring 9


def _phi_table():
    ts = np.linspace(0.0, END, 4001)
    sp = np.array([ROT_RATE * ease_in_out_sine(seg(t, HIT, HIT + 0.6)) * (1 - ease_in_out_sine(seg(t, *ROT_STOP)))
                   for t in ts])
    ph = np.concatenate([[0.0], np.cumsum(0.5 * (sp[1:] + sp[:-1]) * np.diff(ts))])
    return ts, ph


_PHI_T, _PHI = _phi_table()


def phi(t: float) -> float:
    """How far the whole tree has turned (radians, clockwise) at scene time t."""
    return float(np.interp(t, _PHI_T, _PHI))


PHI_END = phi(DIVE[0])
TARGET_ANGLE = float(2 * np.pi * (A_SLOT + 12) / NINE_FACT)       # the mean of the 24 slot centres
TARGET = tree_point(TARGET_ANGLE, ring_radius(9), PHI_END)     # the centre of the 24 slots, after the turn
K_GLOW = 125.0                                      # zoom when the glowing point fills the frame (20.4)
K_FINAL = ORDER_SPACING / DELTA                     # zoom at the end: neighbouring slots 0.36 apart
S_END = np.array([0.0, ORDER_Y])                    # where TARGET sits on screen at the end


# ---------------------------------------------------------------- the camera
def _cam_before_dive(t: float):
    if t < PULL[0]:                                 # close on the root; a faint push-in keeps it alive
        e = ease_in_out_sine(seg(t, 0.0, PULL[0]))
        return ROOT[0], ROOT[1], W * (CLOSE - 0.012 * e)
    w_close = W * (CLOSE - 0.012)
    if t < PULL[1]:                                 # 15.1-17.4: pull out so the ring of 9 fits
        e = ease_in_out_cubic(seg(t, *PULL))
        return ROOT[0] * (1 - e), ROOT[1] * (1 - e), w_close * (W / w_close) ** e
    if t < HIT:
        return 0.0, 0.0, W
    e = ease_in_out_sine(seg(t, HIT, DIVE[0]))      # bars 18-19: a slow push towards the tree, the frame a
    return -0.12 * e, -0.06 * e, W * (1 - 0.025 * e)   # little low, so ring 9 clears c05/c06 (and the HUD)


C_DIVE0 = _cam_before_dive(DIVE[0])
K_DIVE0 = W / C_DIVE0[2]
S_DIVE0 = (TARGET - np.array(C_DIVE0[:2])) * K_DIVE0


def cam_path(t: float):
    """(centre x, centre y, frame width) at scene time t."""
    if t < DIVE[0]:
        return _cam_before_dive(t)
    if t < DIVE[1]:                                 # the dive: TARGET glides to S_END while the zoom accelerates
        u = seg(t, *DIVE)
        k = K_DIVE0 * (K_GLOW / K_DIVE0) ** ease_in_expo(u)
        s = S_DIVE0 + (S_END - S_DIVE0) * ease_in_out_cubic(seg(t, *TRAVEL))
    else:                                           # the resolve: the zoom carries on and settles
        u = seg(t, *RESOLVE)
        k = K_GLOW * (K_FINAL / K_GLOW) ** ease_out_cubic(u)
        s = S_END
    c = TARGET - s / k
    return float(c[0]), float(c[1]), W / k


CAM = Cam(cam_path)


def order_world() -> np.ndarray:
    """World positions of the 24 fill orders that begin with game A (ring 9, no jitter), after the turn."""
    return tree_point(slot_angle(A_SLOTS), ring_radius(9), PHI_END)


def order_screen(t: float = END) -> np.ndarray:
    """Their screen positions at time t (at END: where S03 picks them up)."""
    return CAM.to_screen(order_world(), t)


ORDER_SCREEN = order_screen(END)                    # (24, 2): a line of points through (0, 1.0), S03's board centre


# ---------------------------------------------------------------- drawing helpers
def _rot(a: float) -> np.ndarray:
    """2x2 matrix of a clockwise turn by a (radians) in world coordinates."""
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, s], [-s, c]])


class Hairlines(VMobject):
    """Many straight hairline segments in one VMobject (one Cairo path): set(P, Q) each frame."""

    def __init__(self, color: str = INK, width_px: float = 1.5, opacity: float = 1.0):
        super().__init__()
        self.base = stroke_px(width_px)
        self.set_fill(opacity=0).set_stroke(color, width=self.base, opacity=opacity)
        self.points = np.zeros((0, 3))

    def set_segments(self, P, Q, width: float = 1.0, opacity: float = 1.0):
        P, Q = np.asarray(P, dtype=float).reshape(-1, 2), np.asarray(Q, dtype=float).reshape(-1, 2)
        if len(P) == 0 or opacity <= 1e-3:
            self.points = np.zeros((0, 3))
            self.set_stroke(width=0, opacity=0)
            return self
        n = len(P)
        pts = np.zeros((4 * n, 3))
        d = Q - P
        pts[0::4, :2] = P
        pts[1::4, :2] = P + d / 3
        pts[2::4, :2] = P + 2 * d / 3
        pts[3::4, :2] = Q
        self.points = pts
        self.set_stroke(width=self.base * width, opacity=clamp01(opacity))
        return self


class Glyphs(VGroup):
    """Filled glyphs (a Text) with a stacked-stroke glow, placed each frame by centre and scale (screen
    space): show(centre, scale, vis, glow). `glow_colors`: one colour per glyph (255,168: cool -> warm)."""

    def __init__(self, tmpl: VMobject, color: str = WHITE, glow_color: str = INK, glow_px: float = 0.0,
                 layers: int = 6, glow_opacity: float = 0.5, glow_colors=None):
        super().__init__()
        t = tmpl.copy()
        t.shift(-t.get_center())
        self.w, self.h = float(t.width), float(t.height)
        self.parts = [p for p in t.family_members_with_points()]
        self.tp = [p.points.copy() for p in self.parts]
        self.color = color
        self.glow = []
        if glow_px > 0:
            for k in range(layers, 0, -1):
                w = stroke_px(2 * glow_px) * k / layers
                op = glow_opacity * (1 - k / (layers + 1)) ** 2
                cps = []
                for i, p in enumerate(self.parts):
                    col = glow_colors[min(i, len(glow_colors) - 1)] if glow_colors else glow_color
                    cps.append(p.copy().set_fill(opacity=0).set_stroke(col, width=0, opacity=0))
                self.glow.append((cps, w, op))
                self.add(*cps)
        self.core = [p.copy().set_fill(color, opacity=0).set_stroke(width=0, opacity=0) for p in self.parts]
        self.add(*self.core)
        self.hide()

    def hide(self):
        for c in self.core:
            c.set_fill(opacity=0)
        for cps, _, _ in self.glow:
            for c in cps:
                c.set_stroke(width=0, opacity=0)
        return self

    def show(self, centre, scale: float = 1.0, vis: float = 1.0, glow: float = 1.0, color=None):
        if vis <= 1e-3 or scale <= 1e-4:
            return self.hide()
        c = np.asarray(centre, dtype=float)[:2]
        for i, tp in enumerate(self.tp):
            q = tp.copy()
            q[:, :2] = tp[:, :2] * scale + c
            self.core[i].points = q
            self.core[i].set_fill(color or self.color, opacity=clamp01(vis))
            for cps, w, op in self.glow:
                cps[i].points = q.copy()
                o = clamp01(op * glow * vis)
                cps[i].set_stroke(width=w * scale if o > 1e-3 else 0, opacity=o)
        return self


class DotSplat(ImageMobject):
    """A full-frame image of additive splats in screen space (fix it in the scene): draw(points, weights)."""

    def __init__(self, color=FILL_COLOR, size_px: float = 0.55, glow_px: float = 3.2, glow_amount: float = 0.8,
                 gain: float = 1.5):
        q = config.pixel_height / 1080.0
        ppu = config.pixel_height / H * 0.5
        self.res = (max(8, int(round(W * ppu))), max(8, int(round(H * ppu))))
        self.region = (-W / 2, -H / 2, W / 2, H / 2)
        self.q = q
        self.look = dict(color=tuple(color), size_px=size_px * q, glow_px=glow_px * q, glow_amount=glow_amount,
                         gain=gain)
        super().__init__(np.zeros((self.res[1], self.res[0], 4), np.uint8))
        self.set_resampling_algorithm(2)
        self.stretch_to_fit_width(W).stretch_to_fit_height(H).move_to([0, 0, 0])

    def draw_layers(self, layers, glow=None, floor=None):
        """Several splat layers (pts, weights, look) and an optional soft glow composited (over, bottom to top)
        into this one image: one resample per frame instead of one per layer. `floor` = (y0, y1) screen units:
        the glow fades out below y1 and is gone at y0 (the caption band stays dark)."""
        h, w_ = self.res[1], self.res[0]
        acc_rgb = np.zeros((h, w_, 3), np.float32)
        acc_a = np.zeros((h, w_, 1), np.float32)
        if glow is not None and glow[3] > 1e-3:
            cx, cy, sig, op, col = glow
            xs = ((np.arange(w_) + 0.5) / w_ * W - W / 2).astype(np.float32)
            ys = (H / 2 - (np.arange(h) + 0.5) / h * H).astype(np.float32)
            g = np.float32(op) * np.exp(-((xs[None, :] - cx) ** 2 + (ys[:, None] - cy) ** 2) / np.float32(2 * sig * sig))
            if floor is not None:
                u = np.clip((ys - floor[0]) / (floor[1] - floor[0]), 0, 1)
                g = g * (u * u * (3 - 2 * u))[:, None].astype(np.float32)
            acc_a = g[..., None]
            acc_rgb = acc_a * np.asarray(col, np.float32)[None, None, :]
        for pts, weights, look in layers:
            if pts is None or len(pts) == 0:
                continue
            lk = dict(look)
            col = tuple(lk.pop("color", FILL_COLOR))
            lk = {k: v * self.q if k in ("size_px", "glow_px") else v for k, v in lk.items()}
            img = splat(np.asarray(pts, dtype=float), self.region, self.res,
                        weights=np.asarray(weights, dtype=float) * self.q, color=col, **lk)
            a = img[..., 3:4].astype(np.float32) / 255.0
            acc_rgb = img[..., :3].astype(np.float32) / 255.0 * a + acc_rgb * (1 - a)
            acc_a = a + acc_a * (1 - a)
        rgb = acc_rgb / np.maximum(acc_a, 1e-4)
        out = np.empty((h, w_, 4), np.uint8)
        out[..., :3] = np.clip(rgb * 255, 0, 255)
        out[..., 3:] = np.clip(acc_a * 255, 0, 255)
        self.pixel_array = out

    def draw(self, pts, weights, glow=None):
        """Splat the points; `glow` = (centre x, centre y, sigma, opacity, rgb): a soft light under them, in
        screen units (cheaper than a huge sprite, and it lies in the same image)."""
        h, w_ = self.res[1], self.res[0]
        if pts is None or len(pts) == 0:
            img = np.zeros((h, w_, 4), np.uint8)
        else:
            w = np.asarray(weights, dtype=float) * self.q   # the same look at any render quality
            img = splat(np.asarray(pts, dtype=float), self.region, self.res, weights=w, **self.look)
        if glow is not None and glow[3] > 1e-3:
            cx, cy, sig, op, col = glow
            xs = (np.arange(w_) + 0.5) / w_ * W - W / 2
            ys = H / 2 - (np.arange(h) + 0.5) / h * H
            g = op * np.exp(-((xs[None, :] - cx) ** 2 + (ys[:, None] - cy) ** 2) / (2 * sig * sig))
            a1 = img[..., 3:4] / 255.0
            a2 = g[..., None]
            a = a1 + a2 * (1 - a1)
            rgb = (img[..., :3] / 255.0 * a1 + np.asarray(col)[None, None, :] * a2 * (1 - a1)) / np.maximum(a, 1e-4)
            img = np.concatenate([np.clip(rgb * 255, 0, 255), np.clip(a * 255, 0, 255)], axis=2).astype(np.uint8)
        self.pixel_array = img


def order_dots() -> DotSplat:
    """The splat that draws the 24 dim points (S02's last beat, S03's first)."""
    d = ORDER_DOTS
    return DotSplat(FILL_COLOR, d["size_px"], d["glow_px"], d["glow_amount"], d["gain"])


def arc_track(a0: float, a1: float, r: float, n: int = 40, phi_: float = 0.0) -> np.ndarray:
    """Points of an arc round the root (clockwise angles a0 -> a1)."""
    return tree_point(np.linspace(a0, a1, n), r, phi_)


def _poly_at(poly: np.ndarray, u: float) -> np.ndarray:
    """The point a fraction u along a polyline (by length)."""
    d = np.linalg.norm(np.diff(poly, axis=0), axis=1)
    cum = np.concatenate([[0.0], np.cumsum(d)])
    s = clamp01(u) * cum[-1]
    i = int(np.clip(np.searchsorted(cum, s) - 1, 0, len(d) - 1))
    f = (s - cum[i]) / max(1e-9, d[i])
    return poly[i] + (poly[i + 1] - poly[i]) * f


def _poly_part(poly: np.ndarray, u: float) -> np.ndarray:
    """The polyline up to fraction u."""
    if u >= 1:
        return poly
    d = np.linalg.norm(np.diff(poly, axis=0), axis=1)
    cum = np.concatenate([[0.0], np.cumsum(d)])
    s = clamp01(u) * cum[-1]
    k = int(np.searchsorted(cum, s))
    return np.vstack([poly[:max(1, k)], _poly_at(poly, u)[None, :]])


def _park(img) -> None:
    """Hide an image sprite cheaply: Cairo/PIL resample every ImageMobject at its on-screen size, also at
    opacity 0, so an invisible sprite is shrunk to nothing."""
    img.set_opacity(0)
    if img.width > 0.02:
        img.set(width=0.01)
    img.move_to([0, 0, 0])


def _hex(c) -> str:
    c = np.clip(np.asarray(c), 0, 1)
    return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in c)


BAND_GLOW = (BAND_TOP - 0.05, BAND_TOP + 1.3)       # the dive's glowing point: a soft floor above the band


def band_mask(y, on: float = 1.0) -> np.ndarray:
    """Weights of points at screen heights y during the dive: 0 in the caption band, 1 above BAND_FADE."""
    u = np.clip((np.asarray(y, dtype=float) - BAND_FADE[0]) / (BAND_FADE[1] - BAND_FADE[0]), 0.0, 1.0)
    return 1.0 - on * (1.0 - u * u * (3 - 2 * u))


# the pinned numbers' block on the right third (screen units: left edge, bottom, top) and the mask's feather: while
# the numbers are up during the dive, ring 9's streak fades out behind them (it would sweep through "9! 读作 …" and
# "> 255,168" at 20.3+), and it comes back as they fade (NUM_OUT)
NUM_BOX = (2.45, -2.3, 2.05)                        # (down to the band fade: no sliver of ring between)
NUM_FEATHER = 0.45


def num_mask(xy, on: float = 1.0) -> np.ndarray:
    """Weights of points at screen positions xy during the dive: 1 - on inside NUM_BOX, 1 outside its feather."""
    xy = np.asarray(xy, dtype=float).reshape(-1, 2)
    x0, y0, y1 = NUM_BOX
    f = NUM_FEATHER
    ux = np.clip((xy[:, 0] - (x0 - f)) / f, 0.0, 1.0)
    uy = np.clip(np.minimum(xy[:, 1] - (y0 - f), (y1 + f) - xy[:, 1]) / f, 0.0, 1.0)
    m = (ux * ux * (3 - 2 * ux)) * (uy * uy * (3 - 2 * uy))
    return 1.0 - on * m


def maths(s: str, size: float = 30, color: str = INK) -> MarkupText:
    """A small formula in EB Garamond italic with lining figures: an old-style 1 reads as I ("× I"). The same
    setting as S04's maths(), which S06 and S07 use (S06 repeats this scene's "9 × 8 × … × 1 = 9! = 362,880")."""
    esc = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return MarkupText(f'<span font_features="lnum 1">{esc}</span>', font=FONT_OLDSTYLE, slant="ITALIC",
                      font_size=size, color=color)


def stacked_label(zh: str, en: str, zh_size: float = 21, en_size: float = 20, color: str = INK_DIM,
                  buff: float = 0.1) -> VGroup:
    """A bilingual tag on two lines, left-aligned: Chinese, then tracked English caps (27 px at 1080p)."""
    a = cjk(zh, size=zh_size, color=color)
    b = tracked(en, size=en_size, spacing=0.22, color=color)
    return VGroup(a, b).arrange(direction=np.array([0, -1, 0]), buff=buff, aligned_edge=LEFT)


# ---------------------------------------------------------------- the scene
class FillOrders(BeatScene):

    def construct(self):
        self.sounds = Sounds()
        self.shots: list[tuple[float, float, tuple]] = []
        self.build()
        self.score()
        self.run()

    # ------------------------------------------------------------- objects
    def build(self):
        self.rng = np.random.default_rng(12)
        # --- the root (S01's), the ring-1 guide, the ring-1 boards, edges
        self.root_lines = [Ink(Line([*p, 0], [*q, 0]), INK, 2.0) for p, q in grid_lines(ROOT_CELL)]
        n_dash = 44
        a = np.linspace(0, 2 * np.pi, n_dash + 1)[:-1]
        self.guide_a = np.stack([a, a + 0.55 * 2 * np.pi / n_dash], axis=1)
        self.guide = Hairlines(INK_DIM, 1.4)
        self.kid_angles = slot_angle(np.arange(9), 9)
        self.kid_lines = Hairlines(INK, 1.4)                              # 9 boards x 4 lines
        self.kid_x = [Ink(x_template(0.62 * KID_CELL), XC.core, 1.7, XC.glow, 5, layers=4, glow_opacity=0.55)
                      for _ in range(9)]
        self.edges1 = Hairlines(INK_DIM, 1.2)                             # root -> ring 1
        self.edges2 = Hairlines(INK_DIM, 1.0)                             # ring 1 -> ring 2
        # --- the lens of O's replies to X0
        self.lens_ring = Hairlines(INK_DIM, 1.3)
        self.lens_track = Hairlines(INK_DIM, 1.1)
        self.lens_lines = Hairlines(INK, 1.2)                             # 8 boards x 4 lines
        self.lens_x = [Ink(x_template(0.62 * LENS_CELL), XC.core, 1.5, XC.glow, 4, layers=3, glow_opacity=0.5)
                       for _ in range(8)]
        self.lens_o = [Ink(o_template(0.62 * LENS_CELL), OC.core, 1.6, OC.glow, 5, layers=3, glow_opacity=0.55)
                       for _ in range(8)]
        cols, rows = 4, 2
        self.lens_pos = [LENS_C + np.array([((j % cols) - 1.5) * 0.31, (0.5 - j // cols) * 0.34]) for j in range(8)]
        # the leader leaves the lens where it is nearest the root and runs clockwise round ring 2 to wedge 0
        exit_ = LENS_C + (ROOT - LENS_C) / np.linalg.norm(ROOT - LENS_C) * LENS_R
        r_exit = float(np.linalg.norm(exit_ - ROOT))
        a_exit = math.atan2(exit_[0] - ROOT[0], exit_[1] - ROOT[1]) % (2 * np.pi)
        self.reply_angles = slot_angle(np.arange(8), 72)                 # wedge 0 of ring 2: 2.5° ... 37.5°
        self.tracks = []
        for j in range(8):
            arc = arc_track(a_exit, 2 * np.pi + self.reply_angles[j], r_exit, 50)
            drop = tree_point(np.full(4, self.reply_angles[j]), np.linspace(r_exit, R2, 4))
            o = self.lens_pos[j] + square_centre(REPLY_SQ[j], LENS_CELL)
            self.tracks.append(np.vstack([o[None, :], arc, drop[1:]]))
        self.leader = np.vstack([arc_track(a_exit, 2 * np.pi + math.radians(20), r_exit, 50),
                                 tree_point(np.full(3, math.radians(20)), np.linspace(r_exit, 1.0, 3))[1:]])
        # --- the rings of the splat (rings 2-9), relative to the root, unturned
        self.rings = {}
        for d in range(2, 10):
            ang, rad = fill_ring(d)
            if d == 9:
                rad = rad.copy()
                rad[A_SLOTS] = ring_radius(9)                            # game A's 24 lie exactly on the ring
            sub = RING_SUB.get(d, 1)
            idx = np.arange(0, len(ang), sub)
            rel = np.stack([rad[idx] * np.sin(ang[idx]), rad[idx] * np.cos(ang[idx])], axis=1)
            ring = {"rel": rel, "n": len(idx), "sub": sub}
            if d >= 3:
                pa, pr = self.rings[d - 1]["ang"], self.rings[d - 1]["rad"]
                par = idx // (10 - d)
                ring["prel"] = np.stack([pr[par] * np.sin(pa[par]), pr[par] * np.cos(pa[par])], axis=1)
                ring["launch"] = RING_T[d] + SWEEP[d] * (idx + 0.5) / len(ang)
            ring["ang"], ring["rad"] = ang, rad
            self.rings[d] = ring
        self.canvas = DotSplat(FILL_COLOR, **FILL_SPLAT)                  # every splat layer, one image
        self._static_cache = {}
        self.glow = gaussian_sprite(PEN_HALO, 128, 0.3)
        self.glow.set_opacity(0)
        # --- the numbers on the right third (screen space)
        self.build_numbers()
        # --- HUD
        self.section = section_hud("§1 · 填满棋盘 · FILL THE BOARD")
        self.readout_label = bi_label("顺序", "ORDERS", zh_size=15, en_size=12.5, color=INK_DIM)
        self.readout = RollingCounter(0, digits=6, font=FONT_MONO, weight="NORMAL", size=24, color=INK)
        self.readout.clear_updaters()
        rx = W / 2 - 0.55
        self.readout.move_to([rx - self.readout.ref.width / 2, H / 2 - 0.55 - 0.42, 0])
        self.readout.layout()
        self.readout_label.move_to([rx - self.readout_label.width / 2, H / 2 - 0.55 - 0.1, 0])
        self.readout_group = VGroup(self.readout_label, self.readout)
        self.pen = Pen()

        self.clock_mob = Mobject()
        self.clock_mob.add_updater(lambda m: self.update_state(self.clock()))
        self.add(self.clock_mob, self.camera.frame)
        self.add(*self.root_lines, self.guide, self.edges1, self.edges2, self.kid_lines, *self.kid_x,
                 self.lens_ring, self.lens_track, self.lens_lines, *self.lens_x, *self.lens_o)
        self.fix(self.canvas, self.glow, self.halo_n, self.halo_t, *self.number_rigs, self.gt,
                 self.tree_tag_line, self.leader9_line, self.section, self.readout_group, self.pen)
        self.update_state(0.0)

    def build_numbers(self):
        row_a = maths("9 × 8 × 7 × 6 × 5 × 4 × 3 × 2 × 1", size=26, color=INK)
        glyphs = list(row_a)                                             # 17 glyphs: 9, ×, 8, ×, 7, ...
        assert len(glyphs) == 17
        groups = [VGroup(glyphs[0])] + [VGroup(glyphs[2 * k - 1], glyphs[2 * k]) for k in range(1, 9)]
        rc = row_a.get_center()
        self.row_a_y = 0.72
        self.factor_rigs = [Glyphs(g, INK, INK, 7, layers=4, glow_opacity=0.5) for g in groups]
        self.factor_off = [g.get_center()[:2] - rc[:2] for g in groups]
        # "= 9! = 362,880": the symbol 9! set upright in Inter, about 1.45 times the formula's figures (an
        # italic "!" reads as "9." or "9l" at phone size), with a leader to the tag that says how to read it
        eq = maths("=", size=26, color=INK)
        nine = Text("9!", font=FONT_HEAVY, weight="MEDIUM", font_size=34, color=INK)
        tail = maths("= 362,880", size=26, color=INK)
        row_b = VGroup(eq, nine, tail).arrange(RIGHT, buff=0.13)
        base = tail[1].get_bottom()[1]                                   # figures on one baseline
        nine.shift(np.array([0.0, base - nine[0].get_bottom()[1], 0.0]))
        eq.move_to(np.array([eq.get_center()[0], tail[0].get_center()[1], 0.0]))
        self.row_b = Glyphs(row_b, INK, INK, 6, layers=4, glow_opacity=0.4)
        self.row_b_y = 0.30
        self.row_b_x = COL_X - row_a.width / 2 + 0.3 + row_b.width / 2  # indented under row A (it continues it)
        rbc = row_b.get_center()[:2]
        self.nine_xy = np.array([self.row_b_x, self.row_b_y]) + (nine.get_center()[:2] - rbc)   # the 9! on screen
        self.nine_bottom = self.row_b_y + (nine.get_bottom()[1] - rbc[1])
        self.nine_x = self.nine_xy[0]
        tag9 = VGroup(cjk("9! 读作“9 的阶乘”", size=20, color=INK_DIM),
                      tracked("9! = NINE FACTORIAL", size=16.5, spacing=0.12, color=INK_DIM)).arrange(
            direction=np.array([0, -1, 0]), buff=0.12, aligned_edge=LEFT)
        self.tag9 = Glyphs(tag9, INK_DIM)
        self.tag9_w, self.tag9_h = tag9.width, tag9.height
        left = self.nine_x - nine.width / 2 - 0.03                       # the tag's small "9!" under the big one
        self.tag9_xy = np.array([left + tag9.width / 2, -0.50])
        small9 = cjk("9!", size=20)
        self.leader9 = (np.array([self.nine_x, self.nine_bottom - 0.05]),
                        np.array([left + small9.width / 2, self.tag9_xy[1] + self.tag9_h / 2 + 0.05]))
        self.leader9_line = Hairlines(INK_DIM, 1.2)
        hero = hero_number("362,880", size=66)
        self.hero = Glyphs(hero, WHITE, INK, 16, layers=6, glow_opacity=0.42)
        self.hero_xy = np.array([COL_X, 1.55])
        self.halo_n = gaussian_sprite(PEN_HALO, 96, 0.34, aspect=3.0)
        self.halo_n.stretch_to_fit_width(6.2).stretch_to_fit_height(2.0)
        self.halo_n.set_opacity(0)
        title = hero_number("255,168", size=46)
        xs = np.array([g.get_center()[0] for g in title])
        u = (xs - xs.min()) / (xs.max() - xs.min())
        gcols = [_hex(rgb(XC.glow) * (1 - v) + rgb(OC.mid) * v) for v in u]
        self.title = Glyphs(title, WHITE, INK, 12, layers=6, glow_opacity=0.55, glow_colors=gcols)
        self.title_xy = np.array([COL_X + 0.32, -1.32])
        self.title_w = title.width
        self.halo_t = gaussian_sprite(None, 96, 0.34, gradient=(XC.glow, OC.mid), aspect=3.0)
        self.halo_t.stretch_to_fit_width(4.6).stretch_to_fit_height(1.5)
        self.halo_t.set_opacity(0)
        h = 0.27                                                          # the RED ">": two hairline strokes
        gt = VGroup(Line([-h * 0.75, h, 0], [h * 0.75, 0, 0]), Line([h * 0.75, 0, 0], [-h * 0.75, -h, 0]))
        self.gt = Ink(gt, RED, 3.0, RED, 12, layers=5, glow_opacity=0.5)
        self.gt_xy = np.array([self.title_xy[0] - self.title_w / 2 - 0.42, self.title_xy[1]])
        tt = stacked_label("所有顺序的树", "THE TREE OF ORDERS", color=INK_DIM)
        self.tree_tag = Glyphs(tt, INK_DIM)
        self.tree_tag_w = tt.width
        self.tree_tag_xy = np.array([0.78 + tt.width / 2, -2.22])
        self.tree_tag_line = Hairlines(INK_DIM, 1.2)
        self.number_rigs = [*self.factor_rigs, self.row_b, self.tag9, self.hero, self.title,
                            self.tree_tag]

    # ------------------------------------------------------------- the picture at time t
    def update_state(self, t: float):
        cx, cy, w = CAM(t)
        frame = self.camera.frame
        frame.set(width=w)
        frame.move_to([cx, cy, 0])
        k = W / w
        ph = phi(t)
        self.M = k * _rot(ph)                                             # rel (unturned) -> screen
        self.off = (ROOT - np.array([cx, cy])) * k
        self.k = k
        # the dive (bar 20) must keep the caption band clear while c06 is read: the tree's splat fades to
        # nothing as it reaches the band (band_on), and the hairline boards, edges and the pen round the root
        # fade out as a block before their lowest point gets there (hair)
        self.band_on = ease_in_out_sine(seg(t, DIVE[0], DIVE[0] + 0.3))
        self.hair = 1.0 if t < DIVE[0] else clamp01((self.off[1] - 1.05 * k - (BAND_TOP + 0.15)) / 0.6)
        self.update_root(t)
        self.update_ring1(t)
        self.update_lens(t)
        self.update_tree(t)
        self.update_numbers(t)
        self.update_hud(t)
        self.update_pen(t)
        self.update_glow(t)

    def to_screen_rel(self, rel) -> np.ndarray:
        return np.asarray(rel) @ self.M.T + self.off

    def in_view(self, p, margin: float = 1.0) -> bool:
        s = self.to_screen_rel(np.asarray(p, dtype=float) - ROOT)
        return bool(np.all(np.abs(s) < np.array([W / 2 + margin, H / 2 + margin])))

    # --- the root and ring 1
    def update_root(self, t: float):
        ph = phi(t)
        A = _rot(ph)
        breathe = 1.0 - 0.22 * (0.5 - 0.5 * math.cos(2 * math.pi * t / BAR)) * (t < PULL[0])   # from S01's level
        vis = (1.0 if self.in_view(ROOT, 0.5) else 0.0) * self.hair
        for ln in self.root_lines:
            ln.show(1.0, A, ROOT, vis=vis * clamp01(breathe), width=1.0 / self.k)
        # the dashed guide for ring 1: drawn clockwise from 12 o'clock over 12.1-12.4, gone as ring 1 lands
        f = ease_out_quad(seg(t, *GUIDE))
        gv = 0.55 * seg(t, GUIDE[0], GUIDE[0] + 0.1) * (1 - seg(t, KIDS[-1], KIDS[-1] + 0.6))
        sel = self.guide_a[self.guide_a[:, 0] < f * 2 * np.pi]
        if len(sel) and gv > 1e-3:
            P = tree_point(sel[:, 0], KID_R, ph)
            Q = tree_point(np.minimum(sel[:, 1], f * 2 * np.pi), KID_R, ph)
            self.guide.set_segments(P, Q, width=1.0 / self.k, opacity=gv)
        else:
            self.guide.set_segments([], [])

    def kid_progress(self, t: float, k: int) -> float:
        return ease_out_cubic(seg(t, KIDS[k], KIDS[k] + KID_FLIGHT))

    def update_ring1(self, t: float):
        ph = phi(t)
        A = _rot(ph)
        P, Q, E1p, E1q = [], [], [], []
        far = self.k > 40.0 or self.hair <= 1e-3                         # deep in the dive: all far off
        hv = self.hair
        for k in range(9):
            e = self.kid_progress(t, k)
            if t < KIDS[k] or far:
                self.kid_x[k].hide()
                continue
            r = lerp(0.05, KID_R, e)
            c = tree_point(self.kid_angles[k], r, ph)
            s = lerp(0.35, 1.0, e)
            for p, q in grid_lines(KID_CELL):
                P.append(A @ (p * s) + c)
                Q.append(A @ (q * s) + c)
            xc = c + A @ (square_centre(k, KID_CELL) * s)
            g = 1.0 + 1.2 * pulse(t, KIDS[k], 0.35)
            self.kid_x[k].show(ease_out_cubic(seg(t, KIDS[k], KIDS[k] + 0.25)), A * s, xc, glow=g,
                               width=1.0 / self.k, glow_width=1.0, vis=hv)
            # the edge from the root trails the child out
            E1p.append(tree_point(self.kid_angles[k], 0.27, ph))
            E1q.append(tree_point(self.kid_angles[k], max(0.27, r - 0.15), ph))
        self.kid_lines.set_segments(P, Q, width=1.0 / self.k, opacity=0.9 * hv)
        self.edges1.set_segments(E1p, E1q, width=1.0 / self.k, opacity=0.65 * hv)
        # ring-2 edges: under X0 as each reply lands, then the bundle's copies swing round with their dots
        P2, Q2 = [], []
        if not far:
            for j in range(8):
                land = REPLIES[j] + REPLY_RUN
                f = ease_out_quad(seg(t, land - 0.05, land + 0.12))
                for kk in range(9):
                    rot = self.bundle_turn(t, kk)
                    if rot is None or (kk == 0 and f <= 0):
                        continue
                    a = self.reply_angles[j] + rot
                    fj = f if kk == 0 else 1.0
                    P2.append(tree_point(lerp(self.kid_angles[0] + rot, a, 0.25), KID_R + 0.15, ph))
                    Q2.append(tree_point(lerp(self.kid_angles[0] + rot, a, 0.25 + 0.75 * fj),
                                         KID_R + 0.15 + (R2 - 0.035 - KID_R - 0.15) * fj, ph))
        self.edges2.set_segments(P2, Q2, width=1.0 / self.k, opacity=0.5 * hv)

    def bundle_turn(self, t: float, kk: int):
        """How far bundle copy kk has swung clockwise from wedge 0 (None: not there yet)."""
        if kk == 0:
            return 0.0
        if t < BUNDLE:
            return None
        e = ease_out_cubic(seg(t, BUNDLE + 0.025 * kk, BUNDLE + 0.025 * kk + 0.36))
        return 2 * np.pi * kk / 9 * e

    # --- the lens of replies
    def update_lens(self, t: float):
        vis = ease_out_cubic(seg(t, *LENS_IN)) * (1 - ease_in_out_sine(seg(t, *LENS_OUT)))
        if vis <= 1e-3:
            for x in (self.lens_ring, self.lens_track, self.lens_lines):
                x.set_segments([], [])
            for m in self.lens_x + self.lens_o:
                m.hide()
            return
        a = np.linspace(0, 2 * np.pi, 73)
        circ = LENS_C + LENS_R * np.stack([np.cos(a), np.sin(a)], axis=1)
        s = lerp(0.6, 1.0, vis)
        circ = LENS_C + (circ - LENS_C) * s
        self.lens_ring.set_segments(circ[:-1], circ[1:], width=1.0 / self.k, opacity=0.8 * vis)
        tr = _poly_part(self.leader, ease_out_quad(seg(t, LENS_IN[0], LENS_IN[0] + 0.5)))
        self.lens_track.set_segments(tr[:-1], tr[1:], width=1.0 / self.k, opacity=0.55 * vis)
        P, Q = [], []
        for j in range(8):
            if t < REPLIES[j] - 0.12:
                self.lens_x[j].hide()
                self.lens_o[j].hide()
                continue
            e = ease_out_cubic(seg(t, REPLIES[j] - 0.12, REPLIES[j] + 0.08))
            c = LENS_C + (self.lens_pos[j] - LENS_C) * s
            bs = s * lerp(0.7, 1.0, e)
            for p, q in grid_lines(LENS_CELL):
                P.append(p * bs + c)
                Q.append(q * bs + c)
            v = vis * e
            self.lens_x[j].show(1.0, np.eye(2) * bs, c + square_centre(0, LENS_CELL) * bs, vis=v,
                                width=1.0 / self.k)
            g = 1.0 + 1.4 * pulse(t, REPLIES[j], 0.35)
            self.lens_o[j].show(ease_out_cubic(seg(t, REPLIES[j], REPLIES[j] + 0.22)), np.eye(2) * bs,
                                c + square_centre(REPLY_SQ[j], LENS_CELL) * bs, vis=vis, glow=g, width=1.0 / self.k)
        self.lens_lines.set_segments(P, Q, width=1.0 / self.k, opacity=0.85 * vis)

    # --- the splat: rings 2-9, the replies' running points, the 24 dim points
    def update_tree(self, t: float):
        """The splat layers: rings 5-9 (S02's look), rings 2-4 and the replies' running points (crisp
        points), the 24 dim points and the glowing point of the dive, all in one image."""
        fade_all = 1.0 - ease_in_out_sine(seg(t, RESOLVE[0], RESOLVE[0] + 0.4))
        blur = self.blur_offsets(t)
        sparse_p, sparse_w = [], []
        static, moving = [], []                                          # rings 5-9
        for d in range(2, 10) if fade_all > 1e-3 else ():
            pr, wr = self.ring_points(t, d)
            if pr is None:
                continue
            if d <= 4:
                wr = wr if len(wr) == len(pr) else np.full(len(pr), float(wr[0]))
                sparse_p.append(pr)
                sparse_w.append(wr * fade_all * SPARSE_WEIGHT[d] / FILL_WEIGHT[d])
                continue
            gain = fade_all * INNER_GAIN[d] * self.rings[d]["sub"]
            if pr is self.rings[d]["rel"]:
                static.append((d, float(wr[0]) * gain if np.ndim(wr) else wr * gain))
            else:
                moving.append((pr, wr * gain))
        for j in range(8):                                               # replies run along the leader onto ring 2
            u = seg(t, REPLIES[j] + 0.02, REPLIES[j] + REPLY_RUN)
            if not (0 < u < 1):
                continue
            for lag, wt in ((0.0, 1.0), (0.06, 0.55), (0.12, 0.3), (0.18, 0.15)):
                sparse_p.append((_poly_at(self.tracks[j], ease_in_out_sine(max(0.0, u - lag))) - ROOT)[None, :])
                sparse_w.append(np.array([2.6 * wt]))
        tree_p, tree_w = [], []
        if static:
            key = tuple(d for d, _ in static)
            if key not in self._static_cache:
                self._static_cache = {key: np.concatenate([self.rings[d]["rel"] for d in key])}
            tree_p.append(self._static_cache[key])
            tree_w.append(np.repeat(np.array([w for _, w in static]), [self.rings[d]["n"] for d, _ in static]))
        for pr, wr in moving:
            tree_p.append(pr)
            tree_w.append(wr)
        layers = []
        for pts, wts, look in ((tree_p, tree_w, TREE_LOOK), (sparse_p, sparse_w, SPARSE_LOOK)):
            if not pts:
                continue
            rel = pts[0] if len(pts) == 1 else np.concatenate(pts)
            wt = wts[0] if len(wts) == 1 else np.concatenate(wts)
            scr = rel @ self.M.T + self.off
            if blur:                                                     # only points near the frame streak
                near = (np.abs(scr[:, 0]) < W / 2 + 4) & (np.abs(scr[:, 1]) < H / 2 + 4)
                rel_n, wt_n = rel[near], wt[near]
                scr = np.concatenate([scr[near] if i == 0 else rel_n @ M.T + off for i, (M, off, _) in enumerate(blur)])
                wt = np.concatenate([wt_n * bw for _, _, bw in blur])
            keep = (np.abs(scr[:, 0]) < W / 2 + 0.2) & (np.abs(scr[:, 1]) < H / 2 + 0.2)
            scr, wt = scr[keep], wt[keep]
            if self.band_on > 1e-3:                                      # the dive: nothing bright in the band,
                wt = wt * band_mask(scr[:, 1], self.band_on)             # nor behind the pinned numbers
                num_on = self.band_on * (1 - ease_in_out_sine(seg(t, *NUM_OUT)))
                if num_on > 1e-3:
                    wt = wt * num_mask(scr, num_on)
            layers.append((scr, wt, look))
        # the 24 dim points of game A's fill orders come out of the glow (20.4 -> 21.1)
        dv = ease_in_out_sine(seg(t, RESOLVE[0] + 0.05, RESOLVE[0] + 0.5))
        if dv > 1e-3:
            layers.append((CAM.to_screen(order_world(), t), np.full(24, ORDER_DOTS["weight"] * dv), DOTS_LOOK))
        self.canvas.draw_layers(layers, glow=self.glow_spec(t), floor=BAND_GLOW if self.band_on > 1e-3 else None)

    def blur_offsets(self, t: float):
        """Motion blur for the dive: the camera a little earlier in the frame (screen maps and weights)."""
        if t < DIVE[0] or t >= RESOLVE[1]:
            return None
        out = []
        k_now, k_prev = W / CAM(t)[2], W / CAM(max(DIVE[0], t - 1 / 60))[2]
        rate = abs(math.log(k_now / k_prev))                             # zoom per frame
        if rate < 0.02:
            return None
        n = 3 if rate < 0.08 else 5
        for i in range(n):
            ts = t - i * 1.2 / 60.0 / (n - 1)
            cx, cy, w = CAM(max(DIVE[0], ts))
            k = W / w
            out.append((k * _rot(phi(ts)), (ROOT - np.array([cx, cy])) * k,
                        ((0.45, 0.33, 0.22) if n == 3 else (0.34, 0.25, 0.18, 0.13, 0.10))[i]))
        return out

    def ring_points(self, t: float, d: int):
        """Root-relative points (unturned) and weights of ring d at time t (None: not there yet)."""
        ring = self.rings[d]
        W0 = FILL_WEIGHT[d]
        if d == 2:
            pts, wts = [], []
            for kk in range(9):
                rot = self.bundle_turn(t, kk)
                if rot is None:
                    continue
                ang = self.reply_angles + rot
                if kk == 0:
                    landed = np.array([t >= REPLIES[j] + REPLY_RUN for j in range(8)])
                    if not landed.any():
                        continue
                    ang = ang[landed]
                    fl = np.array([1 + 1.5 * pulse(t, REPLIES[j] + REPLY_RUN, 0.3) for j in range(8)])[landed]
                else:
                    fl = np.full(8, 1.0 + 0.8 * pulse(t, BUNDLE + 0.025 * kk + 0.36, 0.3))
                pts.append(np.stack([R2 * np.sin(ang), R2 * np.cos(ang)], axis=1))
                wts.append(W0 * fl)
            if not pts:
                return None, None
            return np.concatenate(pts), np.concatenate(wts) * self.ring_dim(t, d)
        t0 = RING_T[d]
        if t < t0:
            return None, None
        t_done = t0 + SWEEP[d] + FLIGHT[d]
        env = 1.0 + 1.3 * pulse(t, t0 + SWEEP[d] * 0.5 + FLIGHT[d], 0.45)
        if d == 9:
            env *= fill_flare(t - HIT)
        env *= self.ring_dim(t, d)
        if t >= t_done:
            if d == 9 and t > DIVE[0]:
                return ring["rel"], np.array([min(0.9 / (INNER_GAIN[9] * ring["sub"]), W0 * env * max(1.0, self.k / K_DIVE0))])
            return ring["rel"], np.array([W0 * env])
        u = np.clip((t - ring["launch"]) / FLIGHT[d], 0.0, 1.0)
        live = t >= ring["launch"]
        e = 1 - (1 - u[live]) ** 3
        par, tgt = ring["prel"][live], ring["rel"][live]
        pos = par + (tgt - par) * e[:, None]
        w = W0 * env * (0.35 + 0.65 * e) * (1 + 1.2 * (1 - e))
        flying = e < 0.98
        if flying.any():                                                 # a short streak behind the flyers
            e2 = np.clip(1 - (1 - np.clip(u[live][flying] - 0.2, 0, 1)) ** 3, 0, 1)
            trail = par[flying] + (tgt[flying] - par[flying]) * e2[:, None]
            pos = np.concatenate([pos, trail])
            w = np.concatenate([w, w[flying] * 0.45])
        return pos, w

    def ring_dim(self, t: float, d: int) -> float:
        """Inner rings settle to a fainter dust once ring 9 is the luminous circle."""
        if d == 9:
            return 1.0
        return 1.0 - 0.25 * ease_in_out_sine(seg(t, HIT, HIT + 1.2))

    # --- the numbers (screen space: pinned in the frame like the HUD, also through the dive, while c06 asks about
    # them; they fade over 20.3-20.4 as the frame fills with the glowing point)
    def update_numbers(self, t: float):
        pin = 1 - ease_in_out_sine(seg(t, *NUM_OUT))
        gone = pin <= 1e-3
        rc = np.array([COL_X, self.row_a_y])
        for i, (rig, off) in enumerate(zip(self.factor_rigs, self.factor_off)):
            t0 = FACTOR_T[i]
            v = ease_out_cubic(seg(t, t0, t0 + 0.25))
            if v <= 0 or gone:
                rig.hide()
                continue
            lift = 0.08 * (1 - v)
            glow = 0.25 + 2.2 * pulse(t, t0, 0.4) + 0.6 * pulse(t, HIT, 0.6)
            rig.show(rc + off + np.array([0, -lift]), vis=v * pin, glow=glow)
        v = ease_out_cubic(seg(t, ROW_B_T, ROW_B_T + 0.35))
        if v > 0 and not gone:
            self.row_b.show(np.array([self.row_b_x, self.row_b_y - 0.06 * (1 - v)]), vis=v * pin,
                            glow=0.3 + 1.5 * pulse(t, ROW_B_T, 0.45))
        else:
            self.row_b.hide()
        # 18.2: the tag that says how to read 9!, and its leader from the upright 9!
        v = ease_out_cubic(seg(t, TAG9_T, TAG9_T + 0.4))
        if v > 0 and not gone:
            self.tag9.show(self.tag9_xy + np.array([0, -0.05 * (1 - v)]), vis=0.95 * v * pin)
            p0, p1 = self.leader9
            grow = ease_out_cubic(seg(t, TAG9_T, TAG9_T + 0.35))
            self.leader9_line.set_segments([p0], [p0 + (p1 - p0) * grow], width=1.0, opacity=0.7 * v * pin)
        else:
            self.tag9.hide()
            self.leader9_line.set_segments([], [])
        # the hero: 362,880 lands on the hit (a short rise, white core, neutral halo that breathes)
        v = ease_out_cubic(seg(t, HIT, HIT + 0.3))
        if v > 0 and not gone:
            breathe = 1 + 0.12 * math.sin(2 * math.pi * (t - HIT) / BAR)
            xy = self.hero_xy + np.array([0, -0.12 * (1 - v)])
            self.hero.show(xy, scale=1.04 - 0.04 * v, vis=v * pin, glow=(0.8 + 1.6 * pulse(t, HIT, 0.5)) * breathe)
            self.halo_n.move_to([xy[0], xy[1], 0])
            self.halo_n.set(width=6.2)
            self.halo_n.stretch_to_fit_height(2.0)
            self.halo_n.set_opacity(clamp01(v * pin * (0.32 + 0.05 * math.sin(2 * math.pi * (t - HIT) / BAR))))
        else:
            self.hero.hide()
            _park(self.halo_n)
        # bar 19: the title's 255,168 drifts in under it; 19.2 a RED ">"
        v = ease_out_cubic(seg(t, *DRIFT_IN))
        if v > 0 and not gone:
            xy = self.title_xy + np.array([-0.9 * (1 - v), -0.25 * (1 - v)])
            v *= pin
            br = 1 + 0.1 * math.sin(2 * math.pi * (t - DRIFT_IN[0]) / BAR)
            self.title.show(xy, vis=v, glow=(0.85 + 0.8 * pulse(t, DRIFT_IN[1], 0.5)) * br)
            self.halo_t.move_to([xy[0], xy[1], 0])
            self.halo_t.set(width=4.6)
            self.halo_t.stretch_to_fit_height(1.5)
            self.halo_t.set_opacity(clamp01(0.42 * v))
        else:
            self.title.hide()
            _park(self.halo_t)
        v = ease_out_cubic(seg(t, GT_T, GT_T + 0.2))
        if v > 0 and not gone:
            g = 0.7 + 2.0 * pulse(t, GT_T, 0.45)
            self.gt.show(1.0, np.eye(2) * lerp(1.25, 1.0, v), self.gt_xy, vis=v * pin, glow=g, width=1.0,
                         glow_width=1.0)
        else:
            self.gt.hide()
        # the tree's tag at the lower right of ring 9, with a hairline to the ring: it leaves as the dive starts
        # (its leader would have to follow the ring)
        v = ease_out_cubic(seg(t, TREE_TAG_T, TREE_TAG_T + 0.45)) * (1 - ease_in_out_sine(seg(t, DIVE[0], DIVE[0] + 0.4)))
        if v > 1e-3:
            xy = self.tree_tag_xy + np.array([0.1 * (1 - v) * (t < DIVE[0]), 0])
            self.tree_tag.show(xy, vis=0.95 * v)
            a = math.radians(137) + phi(t)
            p0 = CAM.to_screen(tree_point(a, ring_radius(9) + 0.06, 0.0), t)
            p1 = xy + np.array([-self.tree_tag_w / 2 - 0.1, 0.12])
            grow = ease_out_cubic(seg(t, TREE_TAG_T, TREE_TAG_T + 0.45))
            self.tree_tag_line.set_segments([p0], [p0 + (p1 - p0) * grow], width=1.0, opacity=0.6 * v)
        else:
            self.tree_tag.hide()
            self.tree_tag_line.set_segments([], [])

    # --- HUD, pen, glow
    def update_hud(self, t: float):
        sv = seg(t, 0.0, 0.5)
        for p in self.section.get_family():
            if len(p.points):
                p.set_fill(opacity=sv)
        out = 1 - seg(t, *TEXT_OUT)
        lv = seg(t, NINE - 0.3, NINE) * out
        for p in self.readout_label.get_family():
            if len(p.points):
                p.set_fill(opacity=lv)
        val = 0.0
        for i, t0 in enumerate(FACTOR_T):
            if t >= t0:
                prev = RUNNING[i - 1] if i else 0
                val = prev + (RUNNING[i] - prev) * ease_out_cubic(seg(t, t0, t0 + 0.3))
        self.readout.value.set_value(val)
        self.readout.layout()
        for col in self.readout.columns:
            for g in col:
                g.set_fill(INK, opacity=g.get_fill_opacity() * lv)
        for _, sep in self.readout.separators:
            sep.set_fill(INK, opacity=sep.get_fill_opacity() * lv)

    def update_pen(self, t: float):
        """The pen sits on the root: it pulses with the pulse (beats 1 and 3, then faster) and as it sends
        each first move; it dims a little once the tree is complete."""
        p = CAM.to_screen(ROOT, t)
        if np.any(np.abs(p) > np.array([W / 2 + 0.3, H / 2 + 0.3])):
            self.pen.place((0, 0), 0)
            return
        g = max([pulse(t, tp, 0.2) for tp in PULSES if tp <= t + 1e-6] or [0.0])
        g = max(g, max([pulse(t, tk, 0.22) for tk in KIDS if tk <= t + 1e-6] or [0.0]))
        vis = (1.0 if t < HIT else 1.0 - 0.3 * seg(t, HIT, HIT + 1.0)) * self.hair
        if vis <= 1e-3:
            self.pen.place((0, 0), 0)
            return
        self.pen.place(p, vis)
        self.pen.halo_img.set(width=self.pen.halo_w * (1 + 0.7 * g))
        self.pen.halo_img.move_to([p[0], p[1], 0])
        self.pen.core.set(width=2 * 4.5 / 135.0 * (1 + 0.35 * g))
        self.pen.core.move_to([p[0], p[1], 0])

    def update_glow(self, t: float):
        _park(self.glow)                                                 # (drawn into the dots' image)

    def glow_spec(self, t: float):
        """The glowing point at game A's 24 slots: it brightens as the dive starts, fills the frame at 20.4
        and fades as the 24 points come out of it (centre, sigma, opacity, colour in screen units)."""
        if t < DIVE[0] or t >= RESOLVE[1]:
            return None
        rise = ease_in_cubic(seg(t, DIVE[0], DIVE[1]))
        fall = 1 - ease_out_quad(seg(t, RESOLVE[0] + 0.02, RESOLVE[0] + 0.5))
        op = clamp01((0.3 + 0.52 * rise) * fall)
        if op < 2e-3:
            return None
        k = W / CAM(t)[2]
        p = CAM.to_screen(TARGET, t)
        sig = max(0.012, 0.018 * k)                                      # 0.018 world units: a point that grows
        # ... until it fills the frame (20.4) as one glowing point, never a flat grey: its sigma stops growing at
        # GLOW_SIG_MAX screen units, so the corners and the caption band stay dark (the captions stay readable)
        return (float(p[0]), float(p[1]), min(GLOW_SIG_MAX, sig), op, rgb(PEN_HALO))

    # ------------------------------------------------------------- the sounds (from the same numbers)
    def score(self):
        S = self.sounds
        sx = lambda p, t: float(CAM.to_screen(p, t)[0])
        # the pen's pulse: beats 1 and 3, then quarters, eighths (bar 16) and sixteenths (bar 17), the
        # sixteenths softer (bar 17 is a build: it must stay under the 18.1 hit)
        S.phrase("pen pulse", [(tp, "pen@A3", sx(ROOT, tp)) for tp in PULSES if tp < bb(17)], gain=0.5)
        S.phrase("pen pulse 17", [(tp, "pen@A3", sx(ROOT, tp)) for tp in PULSES if tp >= bb(17)], gain=0.36)
        S.phrase("ring 1", [(tk, tag("X", k), sx(tree_point(self.kid_angles[k], KID_R), tk)) for k, tk in enumerate(KIDS)])
        S.phrase("ring 2", [(tr, tag("O", REPLY_SQ[j]), sx(self.lens_pos[j], tr)) for j, tr in enumerate(REPLIES)])
        fifths = ["D3", "A3", "E4", "B4", "F#5", "C#6", "G#6", "D4", "A4"]   # one note per factor, in fifths
        S.phrase("factors", [(t0, f"bell@{n}", 3.5) for t0, n in zip(FACTOR_T, fifths)], gain=0.8)
        S.phrase("factor ticks", [(t0, "tick", 3.5) for t0 in FACTOR_T], rise=True)
        S.effect(BUNDLE, "shimmer", 1.0, sx(ROOT, BUNDLE))
        scale = ["C#6", "D6", "E6", "F#6", "G#6", "A6", "B6"]
        for d in range(3, 10):                                           # each ring's spray: a cloud of grains
            n = GRAINS[d]                                                # (bar 17: 24 grains in all, not 60)
            ts = RING_T[d] + SWEEP[d] * (np.arange(n) + self.rng.uniform(0.1, 0.9, n)) / n
            S.phrase(f"ring {d} grains", [(float(tt), f"glass@{scale[int(self.rng.integers(len(scale)))]}",
                                           float(np.sin(2 * np.pi * (tt - RING_T[d]) / SWEEP[d]) * 2.5))
                                          for tt in ts], gain=GRAIN_GAIN[d])
        bloom = ["D5", "E5", "F#5", "G#5", "A5", "B5", "C#6"]               # 18.1: all seven notes of D Lydian
        S.phrase("bloom", [(HIT + 0.05 * i, f"bell@{n}", 4.0 - 0.3 * i) for i, n in enumerate(bloom)], gain=0.55)
        S.phrase("tags", [(TAG9_T, "pluck@A4", 3.5), (TREE_TAG_T, "pluck@E4", 3.0)], gain=0.45)
        S.effect(DRIFT_IN[0], "shimmer", 1.2, 4.0)
        S.phrase("255,168", [(DRIFT_IN[0] + 0.1, "glass@B4", 4.5), (DRIFT_IN[0] + 0.25, "glass@F#5", 5.0)], gain=0.5)
        S.phrase("red >", [(GT_T, "glass@G4", 3.0)], gain=0.55)             # the rub: G natural against G#
        S.effect(RESOLVE[0], "shimmer", 1.6, 0.0)                           # the glowing point
        S.log(self)

    # ------------------------------------------------------------- the logged events and the clock
    def log_events(self):
        ev = self.shots

        def add(t, dur, x, y, w, h):
            ev.append((float(t), float(dur), (x, y, w, h)))

        add(GUIDE[0], GUIDE[1] - GUIDE[0], *ROOT, 1.2, 1.2)
        for k, tk in enumerate(KIDS):
            add(tk, KID_FLIGHT, *tree_point(self.kid_angles[k], KID_R), 0.3, 0.3)
        add(LENS_IN[0], 0.35, *LENS_C, 1.3, 1.3)
        for j, tr in enumerate(REPLIES):
            add(tr, REPLY_RUN, *self.lens_pos[j], 0.25, 0.25)
        add(BUNDLE, BEAT, *ROOT, 2.0, 2.0)
        add(PULL[0], PULL[1] - PULL[0], -1.0, 0.15, 10.0, 5.6)
        for d in range(3, 10):
            r = ring_radius(d)
            add(RING_T[d], SWEEP[d] + FLIGHT[d], *ROOT, 2 * r, 2 * r)
        add(HIT, BEAT, -2.0, 0.3, 5.8, 5.8)
        add(HIT, BEAT, COL_X, 1.55, 4.0, 0.8)
        add(TAG9_T, BEAT, *self.tag9_xy, self.tag9_w, self.tag9_h)
        add(TREE_TAG_T, BEAT, 3.5, -2.3, 5.8, 0.4)
        add(DRIFT_IN[0], BEAT, *self.title_xy, 3.0, 0.6)
        add(GT_T, BEAT, *self.gt_xy, 0.5, 0.6)
        add(DIVE[0], DIVE[1] - DIVE[0], *TARGET, 0.5, 0.5)
        add(NUM_OUT[0], NUM_OUT[1] - NUM_OUT[0], COL_X, 0.3, 4.4, 3.4)          # the pinned numbers fade
        add(RESOLVE[0], BEAT, *TARGET, 0.01, 0.01)

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
