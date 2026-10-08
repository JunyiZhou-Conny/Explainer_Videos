"""S01 · How many games? 有多少种对局？ — the cold open (a silent puzzle) and the title.

Bars 1-11 (0:00.0-0:26.4) of script.md. The picture is a pure function of the scene time (State.update):
every object is placed from a template each frame, so a play's length only says what the event log
records. The notes are computed from the same numbers (Sounds) and logged as count marks with one
sound tag each ("X@C#5"), so explainer.music puts each one on the frame that shows it.

    1      the light pen draws a hairline grid, one line per beat (four low plucks)
    2-3    game A, one mark per beat: X0 O3 X1 O4 X2 (the motif C#5 G#4 D5 A4 E5); the top-row win line
    4      the camera eases right; the pen draws a second grid (c01, the question)
    5      game B on eighth notes, X2 O4 X0 O3 X1: the same final board (c02)
    6      "=?" between the boards; a light runs through both orders at once; "=?" -> "≠"
    7      B dissolves; a copy of A slides into its place and turns a quarter turn: "=?" (c03)
    8      "≠"; the turned copy flips over (game A mirrored); "≠"; everything falls into a point
    9      a slot counter scrambles, ticking faster; half a beat of darkness (the breath)
    10     TITLE HIT: one flash; the digits land left to right on 255,168 (cool left, warm right)
    11     the number dissolves into ~3,000 particles that swirl into the root of the tree

Hand-over to S02 (the join at 12.1 is a segue): the last frame has the camera frame 0.45 x 14.22 units
wide, centred on the root at (-2.0, +0.3); the root is an empty mini-board 0.42 units wide (hairlines
2 px on screen), with the light pen (screen-space, 4.5 px core) on its centre square.
"""

from __future__ import annotations

import math

import numpy as np
from manim import LIGHT, Group, Line, Mobject, Rectangle, Text, VGroup, config

from explainer.short import (BeatScene, FONT_TRACKED, INK, INK_DIM, WHITE, brackets, cjk, sample_points,
                             stroke_px, tracked)

from common import (GAME_A, GAME_B, OC, PEN_HALO, PITCH, WIN_TOP, XC, Cam, Ink, InkText, Pen, ScreenField, Shot, Sounds,
                    W, box, clamp01, ease_in_cubic, ease_in_expo, ease_in_out_cubic, ease_in_out_sine,
                    ease_out_cubic, ease_out_quad, final_glyphs, gaussian_sprite, grid_lines, lerp, mark_ink,
                    mirror_lr, move_digit, player, pulse, rgb, rot_cw, seg, square_centre, tag, title_counter,
                    win_template)

# ---------------------------------------------------------------- the plan's clock (script.md: bar n starts at (n-1) x 2.4 s)
BEAT, BAR = 0.6, 2.4


def bb(bar: int, beat: float = 1.0) -> float:
    """Musicians' count, as script.md writes it: bb(5, 2.5) is "5.2+" (the eighth after bar 5 beat 2)."""
    return (bar - 1) * BAR + (beat - 1) * BEAT


END = bb(12)                                      # 26.4 s: 11 bars

# ---------------------------------------------------------------- places (world units)
CELL = 1.4                                        # board 4.2 wide, cells 1.4
CA = np.array([0.0, 0.3])                         # board A (left third once the camera moves)
CB = np.array([6.6, 0.3])                         # board B / the copy (right third)
SIGN = np.array([3.3, 0.3])                       # "=?" between them
CAM_X = 3.3                                       # where the camera eases to in bar 4
FALL = np.array([3.3, 0.55])                      # bar 8.4: everything falls into this point ...
NUM_C = np.array([0.0, 0.55])                     # ... where the counter appears (camera home)
ROOT = np.array([-2.0, 0.3])                      # the root of the tree (S02's geometry)
NUM_OFF = np.array([0.36, -0.36]) * CELL          # a move number sits in its square's lower-right corner
LINE_S = 0.45                                     # the pen draws a grid line in 0.45 s (on a 0.6 s beat)

TURNED = tuple(rot_cw(s) for s in GAME_A)         # X2 O1 X5 O4 X8
FLIPPED = tuple(mirror_lr(s) for s in TURNED)     # X0 O1 X3 O4 X6 (game A mirrored in its diagonal)

# ---------------------------------------------------------------- times
GRID_A = [bb(1, k) for k in (1, 2, 3, 4)]
MOVES_A = [bb(2, 1), bb(2, 2), bb(2, 3), bb(2, 4), bb(3, 1)]
WIN_A = bb(3, 2)
GRID_B = [bb(4, k) for k in (1, 2, 3, 4)]
MOVES_B = [bb(5, 1), bb(5, 1.5), bb(5, 2), bb(5, 2.5), bb(5, 3)]
WIN_B = bb(5, 4)
SIGN_IN = bb(6, 1)
RUN_AB = [bb(6, 1 + 0.5 * k) for k in range(5)]   # 6.1, 6.1+, 6.2, 6.2+, 6.3: both orders at once
NE_1 = bb(6, 4)                                   # "=?" -> "≠"
DISSOLVE_B = bb(7, 1)                             # B to dust; the copy lifts and slides (one beat)
TURN = (bb(7, 2), bb(8, 1))                       # the quarter turn, 7.2-7.4
TURN_PLUCKS = [bb(7, 2 + 0.5 * k) for k in range(6)]
NE_2 = bb(8, 1)
RUN_T = [bb(8, 1 + 0.25 * k) for k in range(5)]   # the turned game on sixteenths, falling
FLIP = (bb(8, 2), bb(8, 3))                       # the card flip, one beat
RUN_F = [bb(8, 2.5 + 0.25 * k) for k in range(5)] # the flipped game, once its face shows
NE_3 = bb(8, 3)
FALL_T = (bb(8, 4), bb(9, 1))                     # everything falls into a point (ease-in-expo)
TICKS = [bb(9, 1), bb(9, 1.5), bb(9, 2), bb(9, 2.5), bb(9, 3), bb(9, 3.25), bb(9, 3.5), bb(9, 3.75), bb(9, 4),
         bb(9, 4.25)]                             # the scramble ticks, eighths then sixteenths
BREATH = bb(9, 4.5)                               # 9.4+: half a beat of darkness (video.yaml silence cue)
HIT = bb(10, 1)                                   # 10.1: the title
LANDS = [HIT + 0.04 + 0.09 * i for i in range(6)] # each digit lands with a note of the title's rolled chord
DISSOLVE = bb(11, 1)
SWIRL = (bb(11, 3), bb(11, 4))                    # 11.3-11.4: the particles swirl into the root
DIVE = (bb(11, 3), bb(11, 4.75))                  # the camera dives to the root (frame 0.45)
ROOT_IN = bb(11, 4)


def cam_path(t: float):
    """(centre x, centre y, frame width) at scene time t."""
    if t < GRID_B[0]:                                     # bars 1-3: a slow push-in, 1.00 -> 0.97
        return 0.0, 0.0, W * (1 - 0.03 * ease_in_out_sine(t / GRID_B[0]))
    if t < GRID_B[1]:                                     # 4.1: eases right, one beat
        return CAM_X * ease_out_cubic(seg(t, GRID_B[0], GRID_B[1])), 0.0, W * 0.97
    if t < FALL_T[1]:                                     # a slow drift while the puzzle plays
        e = ease_in_out_sine(seg(t, GRID_B[1], FALL_T[0]))
        return CAM_X, 0.02 * e, W * (0.97 - 0.012 * e)
    if t < HIT:                                           # home (the frame is black at the jump)
        return 0.0, 0.0, W * (1 - 0.012 * seg(t, FALL_T[1], HIT))
    if t < DISSOLVE:                                      # bar 10: push-in 0.99 -> 0.96
        return 0.0, 0.0, W * (0.988 - 0.028 * ease_out_quad(seg(t, HIT, DISSOLVE)))
    if t < DIVE[0]:
        return 0.0, 0.0, W * (0.96 - 0.005 * seg(t, DISSOLVE, DIVE[0]))
    e = ease_in_out_cubic(seg(t, *DIVE))                  # 11.3: the dive to the root, frame 0.45
    w0, w1 = 0.955 * W, 0.45 * W
    return ROOT[0] * e, ROOT[1] * e, w0 * (w1 / w0) ** e


CAM = Cam(cam_path)


def rot(theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]])


# ---------------------------------------------------------------- a board and what is on it
class BoardRig:
    """A board (grid, marks of a game, move numbers, win line), placed each frame by
    centre b, scale s, rotation theta, a card flip fx (x -> fx x, applied in world orientation after
    the rotation) and an optional fall towards a point. Move numbers stay upright, in the lower-right
    corner of their square."""

    def __init__(self, moves, cell: float = CELL, ghosts: int = 0):
        self.cell = cell
        self.moves = list(moves)
        self.lines = [Ink(Line([*p, 0], [*q, 0]), INK, 2.0) for p, q in grid_lines(cell)]
        self.marks = [mark_ink(player(k), 0.62 * cell) for k in range(len(self.moves))]
        self.win = Ink(win_template(*WIN_TOP, cell), XC.mid, 3.4, XC.glow, 22, layers=7, glow_opacity=0.7)
        self.nums = [InkText(move_digit(k + 1)) for k in range(len(self.moves))]
        self.num_halos = [gaussian_sprite(PEN_HALO, 64, 0.3).scale_to_fit_width(0.62) for _ in self.moves]
        for hlo in self.num_halos:
            hlo.set_opacity(0)
        self.ghosts = []                     # motion-blur copies (core strokes only) for the quarter turn
        for _ in range(ghosts):
            g = [Ink(Line([*p, 0], [*q, 0]), INK, 2.0) for p, q in grid_lines(cell)]
            g += [Ink(_mark_tmpl(player(k), 0.62 * cell), XC.core if player(k) == "X" else OC.core, 2.5)
                  for k in range(len(self.moves))]
            g.append(Ink(win_template(*WIN_TOP, cell), XC.mid, 2.5))
            self.ghosts.append(g)
        self.group = Group(*[i for g in self.ghosts for i in g], *self.lines, *self.marks, self.win,
                           *self.num_halos, *self.nums)
        self.place(np.zeros(2))

    def place(self, b, s: float = 1.0, theta: float = 0.0, fx: float = 1.0, fall=None):
        A = s * np.array([[fx, 0.0], [0.0, 1.0]]) @ rot(theta)
        b = np.asarray(b, dtype=float)
        k = 1.0
        if fall is not None:
            P, k = np.asarray(fall[0], dtype=float), float(fall[1])
            A, b = A * k, P + (b - P) * k
        self.A, self.b, self.s, self.fx, self.k = A, b, s * k, fx, k
        return self

    def square(self, i: int) -> np.ndarray:
        return self.A @ square_centre(i, self.cell) + self.b

    def number_at(self, k: int) -> np.ndarray:
        return self.square(self.moves[k]) + self.s * NUM_OFF

    def hide(self):
        for x in self.lines + self.marks + [self.win]:
            x.hide()
        for n in self.nums:
            n.hide()
        for hlo in self.num_halos:
            hlo.set_opacity(0)
        for g in self.ghosts:
            for x in g:
                x.hide()

    def draw(self, line_f, mark_f, num_v, win_f, glow, hl, vis: float = 1.0, glow_w: float = 1.0,
             sx: float = 1.0):
        """line_f[4], mark_f[k], num_v[k], win_f: drawn fractions; glow[k]: mark glow levels; hl[k]:
        how lit each move number is (0..1)."""
        width = max(0.35, self.k ** 0.5)
        for ln, f in zip(self.lines, line_f):
            ln.show(f, self.A, self.b, vis=vis, width=width)
        for k, m in enumerate(self.marks):
            Ak = self.A
            bk = self.square(self.moves[k])
            m.show(mark_f[k], Ak, bk, vis=vis, glow=glow[k], width=width, glow_width=glow_w * width)
        self.win.show(win_f, self.A, self.b, vis=vis, glow=glow[-1] if len(glow) > len(self.marks) else 1.0,
                      width=width, glow_width=glow_w * width)
        for k, n in enumerate(self.nums):
            h = hl[k]
            col = rgb(INK_DIM) * (1 - h) + rgb(WHITE) * h
            settle = (1 - num_v[k]) * 0.06
            at = self.number_at(k) + np.array([0.0, settle * self.s])
            n.show(at, scale=self.s * (1 + 0.55 * h), sx=sx, vis=num_v[k] * vis, color=_hex(col))
            hlo = self.num_halos[k]
            hlo.move_to([at[0], at[1], 0])
            hlo.set_opacity(clamp01(0.8 * h * vis))


def _mark_tmpl(sym: str, size: float):
    from common import o_template, x_template
    return x_template(size) if sym == "X" else o_template(size)


def _hex(c) -> str:
    c = np.clip(np.asarray(c), 0, 1)
    return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in c)


class SignRig:
    """The hairline "=?" (a question mark over an equals sign) that becomes "≠" (a slash through it)."""

    def __init__(self):
        eq = VGroup(Line([-0.3, 0.08, 0], [0.3, 0.08, 0]), Line([-0.3, -0.08, 0], [0.3, -0.08, 0]))
        self.eq = Ink(eq, INK, 2.2, INK, 9, layers=4, glow_opacity=0.55, splits=[0, 0.5, 1.0])
        self.slash = Ink(Line([-0.15, -0.3, 0], [0.15, 0.3, 0]), INK, 2.2, INK, 9, layers=4, glow_opacity=0.55)
        self.q = InkText(Text("?", font=FONT_TRACKED, weight=LIGHT, font_size=40, color=INK), INK)
        self.group = VGroup(self.eq, self.slash, self.q)

    def hide(self):
        self.eq.hide()
        self.slash.hide()
        self.q.hide()


# ---------------------------------------------------------------- the scene
class ColdOpen(BeatScene):

    def construct(self):
        self.sounds = Sounds()
        self.shots: list[tuple[float, float, tuple]] = []       # logged visual events (t, dur, box)
        self.build()
        self.score()
        self.run()

    # ------------------------------------------------------------- objects
    def build(self):
        self.A = BoardRig(GAME_A)
        self.B = BoardRig(GAME_B)
        self.C = BoardRig(GAME_A, ghosts=3)          # the copy of A that turns and flips
        self.sign = SignRig()
        # the slot counter and the title (bars 9-11)
        self.counter = title_counter(NUM_C)
        self.glyphs = final_glyphs(self.counter)     # where the digits land (static)
        xs = np.array([g.get_center()[0] for g in self.glyphs])
        lo, hi = xs.min(), xs.max()
        self.title_glow = []
        for g, x in zip(self.glyphs, xs):            # halo colour: cool on the left, warm on the right
            u = clamp01((x - lo) / (hi - lo))
            col = _hex(rgb(XC.glow) * (1 - u) + rgb(OC.mid) * u)
            layers = []
            for k in range(7, 0, -1):
                wk = stroke_px(2 * 22) * k / 7
                c = g.copy().set_fill(opacity=0).set_stroke(col, width=0, opacity=0)
                layers.append((c, 0.62 * (1 - k / 8) ** 2, wk))
            self.title_glow.append(layers)
        self.title_glow_group = VGroup(*[c for lay in self.title_glow for c, _, _ in lay])
        self.halo = gaussian_sprite(None, 96, 0.34, gradient=(XC.glow, OC.mid), aspect=3.0)
        self.halo.stretch_to_fit_width(12.8).stretch_to_fit_height(4.3).move_to([*NUM_C, 0])
        word = tracked("TIC-TAC-TOE", size=26, spacing=0.9, font=FONT_TRACKED, color=INK, weight=LIGHT)
        self.word = InkText(word, INK)
        zh = cjk("井字棋 · 不同的对局", size=19, color=INK_DIM)
        en = tracked("DIFFERENT GAMES", size=16.5, spacing=0.3, color=INK_DIM)
        dot = cjk("·", size=19, color=INK_DIM)
        line = VGroup(zh, dot, en).arrange(buff=0.18)
        en.align_to(zh, direction=np.array([0, -1, 0])).shift(np.array([0, 0.012, 0]))
        self.subline = InkText(line, INK_DIM)
        self.word_y, self.sub_y = NUM_C[1] - 1.42, NUM_C[1] - 2.0
        bx = Rectangle(width=self.counter.ref.width + 0.2, height=self.counter.cell_h * 0.62)
        self.frame_marks = Ink(brackets(bx.move_to([0, 0, 0]), size=0.32, buff=0.32), INK_DIM, 1.6)
        # the root of the tree (bar 11), and the light pen
        self.root = BoardRig([], cell=0.14)
        self.pen = Pen()
        # full-frame overlays (screen space): the breath and the flash
        self.dark = Rectangle(width=W + 0.2, height=8.2).set_stroke(width=0).set_fill("#000000", opacity=0)
        self.flash = Rectangle(width=W + 0.2, height=8.2).set_stroke(width=0).set_fill("#FFFFFF", opacity=0)
        # particle fields (screen space): board B's dust, the title's dissolve
        self.dust_b = self.make_dust_b()
        self.dust_t = self.make_dust_title()

        self.clock_mob = Mobject()
        self.clock_mob.add_updater(lambda m: self.update_state(self.clock()))
        self.add(self.clock_mob, self.camera.frame)
        self.add(self.halo, self.A.group, self.B.group, self.C.group, self.sign.group, self.title_glow_group,
                 self.counter, self.frame_marks, self.word, self.subline, self.root.group)
        self.fix(self.pen, self.dark, self.flash)
        self.halo.set_opacity(0)
        self.rng = np.random.default_rng(255168)
        self.counter_plan()
        self.update_state(0.0)

    def make_dust_b(self) -> ScreenField:
        """Board B as it stands at 7.1, sampled into points that drift apart and fade."""
        rng = np.random.default_rng(7)
        parts, cols = [], []
        for p, q in grid_lines(CELL):
            parts.append((Line([*(p + CB), 0], [*(q + CB), 0]), INK, 160))
        for k, sq in enumerate(GAME_B):
            c = square_centre(sq, CELL) + CB
            m = _mark_tmpl(player(k), 0.62 * CELL).move_to([*c, 0])
            parts.append((m, XC.core if player(k) == "X" else OC.core, 150))
        wl = win_template(*WIN_TOP, CELL).shift([*CB, 0])
        parts.append((wl, XC.mid, 160))
        pts = []
        for m, col, n in parts:
            p = sample_points(m, n, seed=int(rng.integers(1 << 30)))[:, :2]
            pts.append(p)
            cols.append(np.repeat(rgb(col)[None, :], n, axis=0))
        p0 = np.concatenate(pts)
        colors = np.concatenate(cols)
        v = rng.normal(0, 0.5, p0.shape) + (p0 - CB) * 0.45 + np.array([0.9, 0.35])
        t0, d = DISSOLVE_B, 1.1

        def pos(t):
            u = max(0.0, (t - t0) / d)
            return p0 + v * (1 - (1 - min(u, 1.0)) ** 2) * 1.3

        def wts(t):
            u = clamp01((t - t0) / d)
            return np.full(len(p0), 0.9 * (1 - u) ** 2)
        return ScreenField(pos, CAM, weights=wts, colors=colors, size_px=1.5, glow_px=5, gain=1.8)

    def make_dust_title(self) -> ScreenField:
        """The title's glyph outlines as ~3,000 points: they drift apart (11.1-11.2), then swirl
        clockwise into the root (11.3-11.4) and fade into it."""
        rng = np.random.default_rng(11)
        p0 = sample_points(self.glyphs, 3000, seed=3)[:, :2]
        xs = p0[:, 0]
        u = np.clip((xs - xs.min()) / (xs.max() - xs.min()), 0, 1)
        w = np.clip((u - 0.38) / 0.24, 0, 1)[:, None]            # cool left, warm right, blended between
        colors = rgb(XC.mid)[None, :] * (1 - w) + rgb(OC.core)[None, :] * w
        out = (p0 - NUM_C) * np.array([0.12, 0.35])
        v = rng.normal(0, 0.32, p0.shape) + out
        q1 = p0 + v                                             # where the drift ends (11.3)
        spin = rng.uniform(1.6, 2.6, len(p0))                    # clockwise turns on the way in (radians)
        t0, t1 = DISSOLVE, SWIRL[0]

        def pos(t):
            if t <= t1:
                return p0 + v * seg(t, t0, t1) ** 1.7          # holds the glyphs' shape, then drifts apart
            e = ease_in_cubic(seg(t, *SWIRL))
            r = (q1 - ROOT) * (1 - e)
            ang = -spin * e
            c, s = np.cos(ang), np.sin(ang)
            return ROOT + np.column_stack([c * r[:, 0] - s * r[:, 1], s * r[:, 0] + c * r[:, 1]])

        def wts(t):
            fade_in = seg(t, t0 - 0.02, t0 + 0.12)
            fade_out = 1 - seg(t, SWIRL[1], SWIRL[1] + 0.4)
            return np.full(len(p0), 0.6 * fade_in * fade_out)
        return ScreenField(pos, CAM, weights=wts, colors=colors, size_px=1.25, glow_px=6, gain=1.6)

    # ------------------------------------------------------------- the counter's plan (bars 9-10)
    def counter_plan(self):
        rng = np.random.default_rng(9)
        n = 6
        self.c_p0 = rng.integers(0, 10, n).astype(float)
        steps = np.zeros((n, len(TICKS)))
        for j in range(len(TICKS)):                       # faster ticks, bigger jumps: it accelerates
            steps[:, j] = 1 + (j >= 4) + (j >= 7) + rng.integers(0, 2, n)
        self.c_steps = steps
        last = self.c_p0 + steps.sum(axis=1)
        target = np.array([2, 5, 5, 1, 6, 8], dtype=float)
        m = np.ceil((last + 4 - target) / 10.0)          # roll forward at least 4 digits into place
        self.c_last, self.c_target = last, target + 10 * m

    def counter_positions(self, t: float) -> np.ndarray:
        if t < HIT:
            p = self.c_p0.copy()
            for j, tj in enumerate(TICKS):
                p += self.c_steps[:, j] * ease_out_cubic(seg(t, tj, tj + 0.1))
            return p
        return np.array([lerp(a, b, ease_out_cubic(seg(t, HIT, L)))
                         for a, b, L in zip(self.c_last, self.c_target, LANDS)])

    # ------------------------------------------------------------- the picture at time t
    def update_state(self, t: float):
        cx, cy, w = CAM(t)
        frame = self.camera.frame
        frame.set(width=w)
        frame.move_to([cx, cy, 0])
        self.update_boards(t)
        self.update_sign(t)
        self.update_title(t)
        self.update_root(t)
        self.update_pen(t)
        dark = 0.88 * seg(t, BREATH, BREATH + 0.05) if BREATH <= t < HIT else 0.0
        self.dark.set_fill(opacity=dark)
        fl = 0.85 * math.exp(-(t - HIT) / 0.022) if HIT <= t < HIT + 0.07 else 0.0
        self.flash.set_fill(opacity=fl)
        for f, (a, b) in ((self.dust_b, (DISSOLVE_B, DISSOLVE_B + 1.2)), (self.dust_t, (DISSOLVE, END))):
            if f in self.mobjects and a - 1e-6 <= t <= b + 1e-6:
                f.render_at(t)

    def fall(self, t):
        """Bar 8.4: everything falls into one point (ease-in-expo)."""
        if t < FALL_T[0]:
            return None
        return FALL, 1 - ease_in_expo(seg(t, *FALL_T))

    def update_boards(self, t: float):
        A, B, C = self.A, self.B, self.C
        fall = self.fall(t)
        gone = t >= FALL_T[1]
        # ---- board A
        if gone:
            A.hide()
        else:
            A.place(CA, fall=fall)
            lf = [ease_in_out_sine(seg(t, a, a + LINE_S)) for a in GRID_A]
            mf = [_smooth(seg(t, a, a + 0.25)) for a in MOVES_A]
            nv = [ease_out_cubic(seg(t, a + 0.12, a + 0.42)) for a in MOVES_A]
            wf, passes = self.win_progress(t, WIN_A)
            glow, hl = self.mark_levels(t, MOVES_A, passes, WIN_A, RUN_AB, GAME_A)
            A.draw(lf, mf, nv, wf, glow, hl)
        # ---- board B: drawn in bars 4-5, dust at 7.1
        if t >= DISSOLVE_B + 0.15:
            B.hide()
        else:
            vis = 1 - seg(t, DISSOLVE_B, DISSOLVE_B + 0.15)
            B.place(CB)
            lf = [ease_in_out_sine(seg(t, a, a + LINE_S)) for a in GRID_B]
            mf = [_smooth(seg(t, a, a + 0.2)) for a in MOVES_B]
            nv = [ease_out_cubic(seg(t, a + 0.1, a + 0.36)) for a in MOVES_B]
            wf, passes = self.win_progress(t, WIN_B)
            glow, hl = self.mark_levels(t, MOVES_B, passes, WIN_B, RUN_AB, GAME_B)
            B.draw(lf, mf, nv, wf, glow, hl, vis=vis)
        # ---- the copy of A: lifts and slides (7.1), turns (7.2-7.4), flips (8.2), falls (8.4)
        if t < DISSOLVE_B or gone:
            C.hide()
            return
        u = ease_in_out_sine(seg(t, DISSOLVE_B, TURN[0]))
        lift = math.sin(math.pi * u)
        centre = CA + (CB - CA) * u + np.array([0.0, 0.4 * lift])      # lifts over the gap as it slides
        e = ease_in_out_cubic(seg(t, *TURN))
        theta = -0.5 * math.pi * e
        fu = ease_in_out_sine(seg(t, *FLIP))
        fx = math.cos(math.pi * fu)
        C.place(centre, s=1 + 0.04 * lift, theta=theta, fx=fx, fall=fall)
        _, passes = self.win_progress(t, WIN_A)
        hl = [max(pulse(t, RUN_T[k], 0.3), pulse(t, RUN_F[k], 0.3)) for k in range(5)]
        base = 1.35 + 0.15 * math.sin(2 * math.pi * (t - WIN_A) / BAR)
        glow = [(base if player(k) == "X" else 1.1) + 0.9 * hl[k] + 0.6 * lift for k in range(5)] + [1.0 + 0.5 * lift]
        C.draw([1] * 4, [1] * 5, [1] * 5, 1.0, glow, hl, sx=abs(fx) if abs(fx) > 0.02 else 0.0)
        # motion-blur ghosts of the turn: the board a few frames back, fading with the turn's speed
        speed = abs(math.sin(math.pi * seg(t, *TURN)))
        for gi, ghost in enumerate(C.ghosts):
            if speed < 0.05 or not (TURN[0] < t < TURN[1]):
                for x in ghost:
                    x.hide()
                continue
            lag = 0.035 * (gi + 1)
            th = -0.5 * math.pi * ease_in_out_cubic(seg(t - lag, *TURN))
            Ag = (1 + 0.04 * lift) * rot(th)
            op = (0.3, 0.17, 0.08)[gi] * speed
            for x in ghost[:4]:
                x.show(1.0, Ag, centre, vis=op)
            for k, x in enumerate(ghost[4:9]):
                x.show(1.0, Ag, Ag @ square_centre(GAME_A[k], CELL) + centre, vis=op)
            ghost[9].show(1.0, Ag, centre, vis=op)

    def win_progress(self, t: float, t0: float):
        """The win line sweeps the top row in one beat (ease-out); when its head passes each X."""
        f = ease_out_quad(seg(t, t0, t0 + BEAT))
        return f, self.pass_times(t0)

    @staticmethod
    def pass_times(t0: float) -> list[float]:
        # the head is at fraction f = 1 - (1 - u)^2 of the line; square centres at f = 0.148, 0.5, 0.852
        L = 2 * CELL + 2 * 0.42 * CELL
        out = []
        for x in (-CELL, 0.0, CELL):
            f = (x + L / 2) / L
            out.append(t0 + BEAT * (1 - math.sqrt(1 - f)))
        return out

    def mark_levels(self, t, move_t, passes, win_t, run, moves):
        """Glow level of each mark (and of the win line, last) and how lit each move number is."""
        top = {0: passes[0], 1: passes[1], 2: passes[2]}        # squares on the top row: flare as the line passes
        glow = []
        for k, sq in enumerate(moves):
            g = 1.0 + 0.8 * pulse(t, move_t[k], 0.35)           # each mark lands with a little flare
            if player(k) == "X" and sq in top:
                g += 1.1 * pulse(t, top[sq], 0.45)
                if t >= top[sq]:                                # ... and stays brighter, breathing
                    g += 0.35 + 0.15 * math.sin(2 * math.pi * (t - win_t) / BAR)
            else:
                g += 0.06 * math.sin(2 * math.pi * (t - win_t) / BAR + 1.0) * (t >= win_t)
            glow.append(g)
        hl = [pulse(t, run[k], 0.32) for k in range(len(moves))]
        glow = [g + 0.9 * h for g, h in zip(glow, hl)]
        glow.append(1.0 + 0.12 * math.sin(2 * math.pi * (t - win_t) / BAR) * (t >= win_t + BEAT))
        return glow, hl

    def update_sign(self, t: float):
        S = self.sign
        if t < SIGN_IN or t >= FALL_T[1]:
            S.hide()
            return
        fall = self.fall(t)
        k = 1.0 if fall is None else fall[1]
        appear = ease_out_cubic(seg(t, SIGN_IN, SIGN_IN + 0.3))
        if DISSOLVE_B <= t:                       # out of the way while the copy slides over, back as "=?"
            appear = min(1 - seg(t, DISSOLVE_B, DISSOLVE_B + 0.15), 1.0) if t < TURN[0] else \
                ease_out_cubic(seg(t, TURN[0], TURN[0] + 0.3))
        c = SIGN + np.array([0.0, 0.14 * (1 - appear)])
        if fall is not None:
            c = fall[0] + (c - fall[0]) * k
        A = np.eye(2) * k
        glow = 0.6 + 2.2 * max(pulse(t, NE_1, 0.4), pulse(t, NE_2, 0.4), pulse(t, NE_3, 0.35))
        S.eq.show(1.0, A, c, vis=appear, glow=glow, width=max(0.35, k ** 0.5))
        # the slash: drawn at 6.4, gone at 7.1, drawn again at 8.1
        if t < NE_1:
            sf, sv = 0.0, 0.0
        elif t < DISSOLVE_B:
            sf, sv = ease_out_cubic(seg(t, NE_1, NE_1 + 0.2)), 1.0
        elif t < NE_2:
            sf, sv = 1.0, 1.0 if t < DISSOLVE_B + 0.15 else 0.0
        else:
            sf, sv = ease_out_cubic(seg(t, NE_2, NE_2 + 0.2)), 1.0
        S.slash.show(sf, A, c, vis=sv * appear, glow=glow, width=max(0.35, k ** 0.5))
        # the question mark: up until 6.4, back at 7.1, gone at 8.1
        if t < NE_1:
            qv = appear
        elif t < DISSOLVE_B:
            qv = 1 - seg(t, NE_1, NE_1 + 0.15)
        elif t < NE_2:
            qv = 1.0 if t >= TURN[0] else 0.0
        else:
            qv = 1 - seg(t, NE_2, NE_2 + 0.15)
        S.q.show(c + np.array([0.0, 0.42]) * k, scale=k * (0.9 + 0.1 * qv), vis=qv, color=INK)

    def update_title(self, t: float):
        cnt = self.counter
        on = FALL_T[1] <= t < DISSOLVE + 0.25
        if not on:
            for col in cnt.columns:
                for g in col:
                    g.set_opacity(0)
            for _, sep in cnt.separators:
                sep.set_opacity(0)
            self.frame_marks.hide()
        else:
            cnt.manual = list(self.counter_positions(t))
            cnt.manual_top = 999_999
            cnt.layout()
            bright = 0.62 if t < HIT else 1.0
            vis = seg(t, FALL_T[1], FALL_T[1] + 0.2) * (1 - seg(t, DISSOLVE, DISSOLVE + 0.2))
            col = INK if t < HIT else WHITE
            for c in cnt.columns:
                for g in c:
                    op = g.get_fill_opacity()
                    g.set_fill(col, opacity=op * vis * bright)
            for _, sep in cnt.separators:
                sep.set_fill(col, opacity=vis * (bright if t < HIT else 1.0))
            # the brackets: open out of the point (9.1), fly outwards and fade at the hit
            if t < HIT:
                k = 0.06 + 0.94 * ease_out_cubic(seg(t, FALL_T[1], FALL_T[1] + 0.3))
                self.frame_marks.show(1.0, np.eye(2) * k, NUM_C, vis=0.9)
            else:
                k = 1 + 0.35 * ease_out_cubic(seg(t, HIT, HIT + 0.6))
                self.frame_marks.show(1.0, np.eye(2) * k, NUM_C, vis=0.9 * (1 - seg(t, HIT, HIT + 0.6)))
        # glow per digit after it lands; the comma's at the hit; breathing; gone as the number dissolves
        breathe = 1 + 0.14 * math.sin(2 * math.pi * (t - HIT) / BAR)
        out = 1 - seg(t, DISSOLVE, DISSOLVE + 0.2)
        lands = LANDS + [HIT]
        for i, lay in enumerate(self.title_glow):
            v = ease_out_cubic(seg(t, lands[i], lands[i] + 0.3)) * breathe * out if t >= HIT else 0.0
            v += 1.2 * pulse(t, lands[i], 0.25) * out if t >= HIT else 0.0
            for c, base, wk in lay:
                if v <= 1e-3:
                    c.set_stroke(width=0, opacity=0)
                else:
                    c.set_stroke(width=wk, opacity=clamp01(base * v))
        hv = ease_out_cubic(seg(t, HIT, HIT + 0.5)) * (0.5 + 0.08 * math.sin(2 * math.pi * (t - HIT) / BAR))
        hv *= 1 - seg(t, DISSOLVE, DISSOLVE + 1.0)
        self.halo.set_opacity(hv if t >= HIT else 0.0)
        wv = ease_out_cubic(seg(t, HIT + 0.15, HIT + 0.75)) * (1 - seg(t, DISSOLVE, DISSOLVE + 0.8))
        self.word.show([NUM_C[0], self.word_y - 0.1 * (1 - wv)], vis=wv, color=INK)
        sv = ease_out_cubic(seg(t, HIT + 0.4, HIT + 1.0)) * (1 - seg(t, DISSOLVE, DISSOLVE + 0.8))
        self.subline.show([NUM_C[0], self.sub_y - 0.08 * (1 - sv)], vis=sv, color=INK_DIM)

    def update_root(self, t: float):
        R = self.root
        if t < ROOT_IN:
            R.hide()
            return
        s = 0.05 + 0.95 * ease_out_cubic(seg(t, ROOT_IN, ROOT_IN + 0.4))
        R.place(ROOT, s=s)
        width = 1.0 / CAM.zoom(t)                 # 2 px on screen whatever the zoom
        for ln in R.lines:
            ln.show(1.0, R.A, R.b, vis=seg(t, ROOT_IN, ROOT_IN + 0.15), width=width)

    def update_pen(self, t: float):
        p, vis = self.pen_world(t)
        if vis <= 1e-3:
            self.pen.place((0, 0), 0)
            return
        self.pen.place(CAM.to_screen(p, t), vis)

    def pen_world(self, t: float):
        """Where the light pen is (world) and how visible: it draws the grids (bars 1 and 4) and sits
        on the root at the end."""
        for starts, c in ((GRID_A, CA), (GRID_B, CB)):
            a, z = starts[0], starts[-1] + LINE_S
            if a - 0.001 <= t <= z + 0.45:
                lines = [(p + c, q + c) for p, q in grid_lines(CELL)]
                vis = seg(t, a, a + 0.05)
                if t > z:                                   # drifts off and fades after the last line
                    u = seg(t, z, z + 0.45)
                    end = lines[-1][1]
                    return end + np.array([0.25, -0.12]) * ease_out_quad(u), vis * (1 - u) ** 1.5
                for k, s0 in enumerate(starts):
                    if t <= s0 + LINE_S:
                        f = ease_in_out_sine(seg(t, s0, s0 + LINE_S))
                        p, q = lines[k]
                        return p + (q - p) * f, vis
                    if k + 1 < len(starts) and t < starts[k + 1]:
                        u = ease_in_out_sine(seg(t, s0 + LINE_S, starts[k + 1]))
                        a0, b0 = lines[k][1], lines[k + 1][0]
                        return a0 + (b0 - a0) * u, vis * (0.55 + 0.45 * abs(2 * u - 1))
        if t >= ROOT_IN + 0.1:
            return ROOT, ease_out_cubic(seg(t, ROOT_IN + 0.1, ROOT_IN + 0.4))
        return np.zeros(2), 0.0

    # ------------------------------------------------------------- the sounds (from the same numbers)
    def score(self):
        S = self.sounds
        sx = lambda p, t: float(CAM.to_screen(p, t)[0])
        A = BoardRig(GAME_A).place(CA)
        B = BoardRig(GAME_B).place(CB)
        # bar 1: four low plucks, one per grid line (Dmaj9)
        mids_a = [CA + (p + q) / 2 for p, q in grid_lines(CELL)]
        S.phrase("grid A", [(t, f"grid@{n}", sx(m, t)) for t, n, m in zip(GRID_A, ("D3", "A3", "E4", "A4"), mids_a)])
        # bars 2-3: game A, the motif (X bell / O glass at each square's pitch)
        S.phrase("game A", [(t, tag(player(k), sq), sx(A.square(sq), t)) for k, (t, sq) in enumerate(zip(MOVES_A, GAME_A))])
        S.phrase("win A", [(t, f"X@{n}", sx(A.square(sq), t))
                           for t, n, sq in zip(self.pass_times(WIN_A), ("C#6", "D6", "E6"), (0, 1, 2))])
        S.effect(WIN_A, "whoosh_up", BEAT, sx(A.square(1), WIN_A))
        # bar 4: the second grid (E9), panned right
        mids_b = [CB + (p + q) / 2 for p, q in grid_lines(CELL)]
        S.phrase("grid B", [(t, f"grid@{n}", sx(m, t)) for t, n, m in zip(GRID_B, ("E3", "B3", "F#4", "G#4"), mids_b)])
        # bar 5: game B, the same five notes in another order
        S.phrase("game B", [(t, tag(player(k), sq), sx(B.square(sq), t)) for k, (t, sq) in enumerate(zip(MOVES_B, GAME_B))])
        S.phrase("win B", [(t, f"X@{n}", sx(B.square(sq), t))
                           for t, n, sq in zip(self.pass_times(WIN_B), ("C#6", "D6", "E6"), (0, 1, 2))])
        S.effect(WIN_B, "whoosh_up", BEAT, sx(B.square(1), WIN_B))
        # bar 6: "=?" (a suspended tone), both orders in counterpoint, "≠" (a soft thump)
        S.phrase("=?", [(SIGN_IN, "bell@E4", 0.0)])
        S.phrase("both orders", [(t, tag(player(k), GAME_A[k]), sx(A.square(GAME_A[k]), t)) for k, t in enumerate(RUN_AB)]
                 + [(t, tag(player(k), GAME_B[k]), sx(B.square(GAME_B[k]), t)) for k, t in enumerate(RUN_AB)])
        S.effect(NE_1, "thump", 0.6, 0.0)
        # bar 7: B to dust (a shimmer), six plucks across the quarter turn (F#m9), left to right
        S.effect(DISSOLVE_B, "shimmer", 1.8, sx(CB, DISSOLVE_B))
        S.phrase("turn", [(t, f"pluck@{n}", lerp(1.3, 5.3, k / 5))
                          for k, (t, n) in enumerate(zip(TURN_PLUCKS, ("F#3", "C#4", "E4", "G#4", "A4", "C#5")))])
        # bar 8: the turned game falling on sixteenths; the flip (an air whoosh) and the flipped game
        T = BoardRig(GAME_A).place(CB, theta=-math.pi / 2)
        S.phrase("turned", [(t, tag(player(k), sq), sx(T.square(GAME_A[k]), t))
                            for k, (t, sq) in enumerate(zip(RUN_T, TURNED))])
        S.effect(FLIP[0], "whoosh_up", BEAT, sx(CB, FLIP[0]))
        F = BoardRig(GAME_A).place(CB, theta=-math.pi / 2, fx=-1.0)
        S.phrase("flipped", [(t, tag(player(k), sq), sx(F.square(GAME_A[k]), t))
                             for k, (t, sq) in enumerate(zip(RUN_F, FLIPPED))])
        # bar 9: the scramble, ticks that climb and speed up; 9.4+ the breath; 10.1 the title
        S.phrase("scramble", [(t, "tick", 0.0) for t in TICKS], rise=True)
        # bar 11: the dissolve's shimmer; grains that fall as the particles converge; the root's plucks
        S.effect(DISSOLVE, "shimmer", 1.6, 0.0)
        S.phrase("drift", [(DISSOLVE + 0.15 + 0.3 * k, f"glass@{n}", x)
                           for k, (n, x) in enumerate(zip(("F#6", "D6", "C#6", "B5"), (-2.5, 2.2, -1.2, 1.0)))])
        S.phrase("converge", [(SWIRL[0] + 0.15 * k, f"glass@{n}", lerp(-0.6, -0.15, k / 4))
                              for k, n in enumerate(("A5", "F#5", "D5", "C#5", "B4"))])
        S.phrase("root", [(ROOT_IN, "grid@B2", -0.2), (ROOT_IN + 0.15, "grid@F#3", -0.1),
                          (ROOT_IN + 0.3, "pen@B5", 0.0)])
        S.log(self)
        self.mark("silence", at=BREATH, dur=HIT - BREATH, hit=False)
        self.mark("title", at=HIT)

    # ------------------------------------------------------------- the logged events and the clock
    def log_events(self):
        ev = self.shots

        def add(t, dur, x, y, w, h):
            ev.append((float(t), float(dur), (x, y, w, h)))
        for k, t in enumerate(GRID_A):
            add(t, BEAT, *CA, 4.2, 4.2)
        for t, sq in zip(MOVES_A, GAME_A):
            add(t, 0.42, *(CA + square_centre(sq, CELL)), 0.9, 0.9)
        add(WIN_A, BEAT, CA[0], CA[1] + CELL, 4.2, 0.2)
        add(GRID_B[0], BEAT, CAM_X, 0.0, 14.0, 8.0)                     # the camera eases right
        for t in GRID_B:
            add(t, BEAT, *CB, 4.2, 4.2)
        for t, sq in zip(MOVES_B, GAME_B):
            add(t, 0.3, *(CB + square_centre(sq, CELL)), 0.9, 0.9)
        add(WIN_B, BEAT, CB[0], CB[1] + CELL, 4.2, 0.2)
        add(SIGN_IN, 0.3, *SIGN, 0.6, 0.9)
        for t in RUN_AB:
            add(t, 0.3, CAM_X, 0.3, 11.0, 4.2)
        add(NE_1, BEAT, *SIGN, 0.6, 0.9)
        add(DISSOLVE_B, BEAT, 3.3, 0.3, 11.0, 4.6)
        add(TURN[0], TURN[1] - TURN[0], *CB, 4.2, 4.2)
        for t in RUN_T:
            add(t, 0.15, *CB, 4.2, 4.2)
        add(FLIP[0], BEAT, *CB, 4.2, 4.2)
        for t in RUN_F:
            add(t, 0.15, *CB, 4.2, 4.2)
        add(NE_3, BEAT, *SIGN, 0.6, 0.9)
        add(FALL_T[0], BEAT, CAM_X, 0.3, 11.0, 4.6)
        for j, t in enumerate(TICKS):
            add(t, 0.15 if j >= 4 else 0.3, *NUM_C, 10.4, 2.4)
        add(HIT, BEAT, *NUM_C, 12.0, 4.0)
        add(HIT + BEAT, BEAT, NUM_C[0], self.word_y, 6.0, 0.6)
        add(DISSOLVE, BAR / 2, *NUM_C, 12.0, 4.0)
        add(SWIRL[0], BEAT, -1.0, 0.4, 8.0, 3.0)
        add(SWIRL[1], BEAT, *ROOT, 0.5, 0.5)

    def run(self):
        """Play the logged events in time order (each a Shot; overlapping ones share a play), and add
        the particle fields while they are needed."""
        self.log_events()
        fields = [(self.dust_b, DISSOLVE_B, DISSOLVE_B + 1.2), (self.dust_t, DISSOLVE, END)]
        steps = sorted({round(t, 4) for t, _, _ in self.shots} | {round(a, 4) for _, a, _ in fields}
                       | {round(b, 4) for _, _, b in fields if b < END})
        for i, t in enumerate(steps):
            nxt = steps[i + 1] if i + 1 < len(steps) else END
            self.until(f"{t:.4f}s")
            for f, a, b in fields:
                if abs(t - a) < 1e-6:
                    self.fix(f)
                    self.add(self.pen, self.dark, self.flash)       # (keep the pen and overlays on top)
                if abs(t - b) < 1e-6:
                    self.unfix(f)
                    self.remove(f)
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


def _smooth(u: float) -> float:
    u = clamp01(u)
    return u * u * (3 - 2 * u)
