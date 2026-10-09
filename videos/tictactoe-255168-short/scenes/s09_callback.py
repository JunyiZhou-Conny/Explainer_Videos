"""S09 · One tree 同一棵树 — the coda (bars 99-106).

Bars 99-106 (3:55.2-4:14.4) of script.md; scene time 0 is the downbeat of bar 99. As in S01 and S08, the
picture is a pure function of the scene time (`update_state`), drawn in screen space (the Manim camera stays
home), and the notes come from the same numbers (Sounds), each with its own tag.

    99     the camera rushes back (ease-in-expo, streaked outlines) into box 1 of the tic-tac-toe strip, and
           through it into the galaxy that box holds
    100    a zoom-through towards game A's leaf on ring 5 (10.12°); 100.4 the leaf blooms, the bloom breaks
           into 24 points that fly onto the four lines of game A's empty grid (as at 20.4 -> 21.1); in the
           same beat the camera pulls back: the grid on the left third at the opening size, the galaxy at 0.6
           on the right (root at (+2.6, +0.3))
    101-102  the opening image: game A replays one mark per beat (the motif, now over the tonic) while the
           light pen retraces its path in the galaxy, root to leaf, one segment per move; 102.2 the top-row
           win line sweeps and the leaf flares cyan                                            (c29)
    103    all 255,168 paths shimmer once: a wave of light from the root outwards; the board breathes
    104    the board and the galaxy dim to 30 %; the title re-forms over them, its particles gathering into
           the glyphs (the reverse of bar 11): 255,168, "TIC-TAC-TOE", "井字棋 · 不同的对局 · DIFFERENT GAMES"
    105-106  105.1 the end line (video.yaml end_card); bar 106 everything fades to black; the last frame is black

Hand-over from S08 (a cut at 99.1): the first frame redraws S08's last frame with S08's own rigs
(s08_bigger.StripsRig, its labels, the pen, the §6 label) from s08_bigger.strip_view(S08 END), then the rush
moves all of it through one screen similarity about box 1 (s08_bigger.xf_apply).
"""

from __future__ import annotations

import math

import numpy as np
from manim import LIGHT, Line, Mobject, Rectangle, VGroup

from explainer.short import BeatScene, FONT_TRACKED, INK, INK_DIM, WHITE, cjk, sample_points, stroke_px, tracked

from common import (GALAXY_COLOURS, GALAXY_LOOK, GAME_A, OC, PEN_HALO, PITCH, XC, FastCamera, FrameImage, Ink,
                    InkText, Pen, Shot, Sounds, Splatter, W, box, clamp01, ease_in_expo, ease_in_out_sine,
                    ease_out_cubic, ease_out_quad, final_glyphs, gaussian_sprite, grid_lines, player, pulse, rgb,
                    section_hud, seg, show_sprite, square_centre, tag, title_counter)
import s08_bigger as s08
from s08_bigger import (BOX_FILL, D_BASE, D_IDX, GA_R, GA_TH, GAL_IN_BOX, L_FAM, L_R, L_TH, L_WEIGHT, N_DEPTH,
                        N_R, N_TH, EDGE_CHILD, EDGE_PARENT, P_BOX, StripsRig, gal_screen, grain_points,
                        hex_of, pen_x, strip_view, xf_apply, zfac)
from s01_open import NUM_C, BoardRig, ColdOpen
from s02_fill import Hairlines
from s04_by_hand import MiniBoard, line_affine

# ---------------------------------------------------------------- the plan's clock (bar 99 = scene time 0)
BEAT, BAR = 0.6, 2.4
FIRST = 99


def bb(bar: int, beat: float = 1.0) -> float:
    """Scene time of script.md's "bar.beat" (global bar numbers): bb(102, 2.5) is "102.2+"."""
    return (bar - FIRST) * BAR + (beat - 1) * BEAT


END = bb(107)                                     # 19.2 s: 8 bars

# ---------------------------------------------------------------- times
RUSH = (0.0, bb(99, 4))                           # into box 1 and through it (ease-in-expo) ...
SETTLE = (bb(99, 4), bb(100))                     # ... easing into the whole galaxy
DIVE = (bb(100), bb(100, 4))                      # the zoom-through towards game A's leaf
BLOOM = bb(100, 4)                                # the leaf blooms; the camera pulls back (one beat)
PULL = (bb(100, 4), bb(101))
GATHER = (bb(100, 4), bb(100, 4) + 0.3)           # 24 points fly onto the grid's lines ...
GROW = (bb(100, 4) + 0.18, bb(101))               # ... which grow out of them
MOVES = [bb(101, 1), bb(101, 2), bb(101, 3), bb(101, 4), bb(102, 1)]
WIN = bb(102, 2)
SHIMMER = (bb(103), bb(103, 4) + 0.6)
TITLE = bb(104)
FORM = (bb(104), bb(104, 3))                      # the particles gather into the glyphs
END_LINE = bb(105)
FADE = (bb(106), bb(106, 4))                      # to black; black from 106.4 to the end

# ---------------------------------------------------------------- places (screen units)
S08_END = s08.END - 1e-6
V0 = strip_view(S08_END)                          # S08's last frame
PIVOT0 = np.array([float(s08.box_x(0, V0["z"])), V0["rows"]["ttt"]])      # box 1 of the tic-tac-toe strip
G_IN_BOX = GAL_IN_BOX * BOX_FILL * P_BOX * V0["z"] / (2 * 2.9)              # the galaxy's scale inside it
FULL = (-0.6, 0.28, 1.0)                          # the whole galaxy (S05's full view)
K_RUSH = 0.82 / G_IN_BOX                          # the zoom at 99.4 (the galaxy at 82 %) ...
K_FULL = 1.0 / G_IN_BOX                           # ... and at 100.1
G_DIVE = 26.0                                     # the galaxy's scale at 100.4 (at the leaf)
LEAF_SCREEN = np.array([0.0, 0.3])                # where the leaf is brought by the dive
SMALL = (2.6, 0.3, 0.6)                           # the galaxy on the right, scaled to 0.6 (101.1 on)
CAM_Z = 1 / 0.97                                  # S01's camera at bar 4: the opening image's scale
BOARD_C = np.array([-3.3 * CAM_Z, 0.3 * CAM_Z])   # board A on the left third, exactly as in S01 bar 4
BOARD_S = CAM_Z
ROT_RATE = math.radians(0.35)


def rho(t: float) -> float:
    """The galaxy's slow clockwise turn (ALIVE)."""
    return ROT_RATE * t


def leaf_offset(t: float) -> np.ndarray:
    """Game A's leaf relative to the root, at scale 1 (galaxy units)."""
    a = GA_TH[5] + rho(t)
    return np.array([GA_R[5] * math.sin(a), GA_R[5] * math.cos(a)])


def k_rush(t: float) -> float:
    """The rush's zoom (1 = S08's last frame) during 99.1-100.1."""
    if t < RUSH[1]:
        return math.exp(math.log(K_RUSH) * ease_in_expo(seg(t, *RUSH)))
    return math.exp(math.log(K_RUSH) + (math.log(K_FULL) - math.log(K_RUSH)) * ease_out_cubic(seg(t, *SETTLE)))


def rush_xf(t: float):
    """The similarity that carries S08's last frame through the rush: box 1's centre moves to the galaxy's
    full-view root as the zoom grows."""
    k = k_rush(t)
    u = math.log(k) / math.log(K_FULL)
    c = PIVOT0 + (np.array(FULL[:2]) - PIVOT0) * (u * u * (3 - 2 * u))
    return (PIVOT0, c, k)


def gcam(t: float):
    """(root x, root y, scale) of the galaxy on screen."""
    if t < DIVE[0]:
        p0, c, k = rush_xf(t)
        return (float(c[0]), float(c[1]), G_IN_BOX * k)
    if t < BLOOM:
        e = ease_in_expo(seg(t, *DIVE))
        g = math.exp(math.log(G_DIVE) * e)
        q0 = np.array(FULL[:2]) + leaf_offset(DIVE[0])            # the leaf where it is at 100.1 ...
        q = q0 + (LEAF_SCREEN - q0) * (1 - (1 - e) ** 2)          # ... brought to the centre
        r = q - g * leaf_offset(t)
        return (float(r[0]), float(r[1]), g)
    e = ease_out_cubic(seg(t, *PULL))
    g = math.exp(math.log(G_DIVE) + (math.log(SMALL[2]) - math.log(G_DIVE)) * e)
    q = LEAF_SCREEN + (np.array(SMALL[:2]) + SMALL[2] * leaf_offset(t) - LEAF_SCREEN) * e
    r = q - g * leaf_offset(t)
    if t >= PULL[1]:
        e2 = ease_in_out_sine(seg(t, PULL[1], END))                 # then a slow push (ALIVE)
        return (SMALL[0], SMALL[1], SMALL[2] * (1 + 0.03 * e2))
    return (float(r[0]), float(r[1]), g)


# game A's path in the galaxy (root, X0, X0 O3, X0 O3 X1, X0 O3 X1 O4, the leaf)
def path_points(t: float) -> np.ndarray:
    return gal_screen(np.array(GA_TH), np.array(GA_R), gcam(t), rho(t))


# ---------------------------------------------------------------- the title (S01 bar 10's layout, re-formed)
class TitleRig:
    """255,168 as the title shows it (S01 bar 10): Inter Black digits with a stacked glow, cool on the left
    and warm on the right, a halo, the tracked TIC-TAC-TOE and the subline; all at S01's scale on screen."""

    def __init__(self):
        cnt = title_counter(NUM_C)
        self.glyphs = final_glyphs(cnt).scale(CAM_Z, about_point=np.zeros(3))
        xs = np.array([g.get_center()[0] for g in self.glyphs])
        lo, hi = xs.min(), xs.max()
        self.glow, self.core = [], []
        for g, x in zip(self.glyphs, xs):
            u = clamp01((x - lo) / (hi - lo))
            col = hex_of(rgb(XC.glow) * (1 - u) + rgb(OC.mid) * u)
            layers = []
            for k in range(7, 0, -1):
                wk = stroke_px(2 * 22) * k / 7
                c = g.copy().set_fill(opacity=0).set_stroke(col, width=0, opacity=0)
                layers.append((c, 0.62 * (1 - k / 8) ** 2, wk))
            self.glow.append(layers)
            self.core.append(g.copy().set_fill(WHITE, opacity=0).set_stroke(width=0))
        self.halo = gaussian_sprite(None, 96, 0.34, gradient=(XC.glow, OC.mid), aspect=3.0)
        self.halo_c = NUM_C * CAM_Z
        self.halo_wh = (12.8 * CAM_Z, 4.3 * CAM_Z)
        word = tracked("TIC-TAC-TOE", size=26, spacing=0.9, font=FONT_TRACKED, color=INK, weight=LIGHT)
        self.word = InkText(word, INK)
        zh = cjk("井字棋 · 不同的对局", size=19, color=INK_DIM)
        en = tracked("DIFFERENT GAMES", size=16.5, spacing=0.3, color=INK_DIM)
        dot = cjk("·", size=19, color=INK_DIM)
        line = VGroup(zh, dot, en).arrange(buff=0.18)
        en.align_to(zh, direction=np.array([0, -1, 0])).shift(np.array([0, 0.012, 0]))
        self.sub = InkText(line, INK_DIM)
        self.word_c = np.array([NUM_C[0], NUM_C[1] - 1.42]) * CAM_Z
        self.sub_c = np.array([NUM_C[0], NUM_C[1] - 2.0]) * CAM_Z
        self.group = VGroup(*[c for lay in self.glow for c, _, _ in lay], *self.core, self.word, self.sub)
        self.targets = sample_points(self.glyphs, 3000, seed=104)[:, :2]

    def show(self, core: float, glow: float, halo: float, word: float, sub: float, scale_word: float = 1.0):
        for g, c in zip(self.glyphs, self.core):
            c.set_fill(WHITE, opacity=clamp01(core))
        for lay in self.glow:
            for c, base, wk in lay:
                if glow <= 1e-3:
                    c.set_stroke(width=0, opacity=0)
                else:
                    c.set_stroke(width=wk, opacity=clamp01(base * glow))
        show_sprite(self.halo, self.halo_c, *self.halo_wh, clamp01(halo))
        self.word.show(self.word_c + np.array([0, -0.1 * (1 - word)]), scale=CAM_Z, vis=word, color=INK)
        self.sub.show(self.sub_c + np.array([0, -0.08 * (1 - sub)]), scale=CAM_Z, vis=sub, color=INK_DIM)


# ---------------------------------------------------------------- the scene
class SameTree(BeatScene):

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
        # S08's last frame: the strips, their labels, the pen and its arm, the §6 label
        self.strips = StripsRig()
        self.pen = Pen()
        self.arm = Ink(Line([0, -0.5, 0], [0, 0.5, 0]), INK, 1.4, PEN_HALO, 10, layers=4, glow_opacity=0.35)
        g6 = section_hud("§6 · 更复杂的棋 · BIGGER GAMES")
        self.sec6, self.sec6_c = InkText(g6, INK_DIM), g6.get_center()[:2]
        # the galaxy's structure: the ring 1-2 edges, the root board, game A's path, the leaf's bloom
        self.edges = Hairlines(INK_DIM, 1.2)
        self.root_board = MiniBoard(0.14, 0, 0, nums=0)
        self.path = [Ink(Line([-0.5, 0, 0], [0.5, 0, 0]), WHITE, 2.0, PEN_HALO, 10, layers=5, glow_opacity=0.5)
                     for _ in range(5)]
        self.leaf_halo = gaussian_sprite(XC.mid, 96, 0.3)
        self.leaf_core = gaussian_sprite(XC.core, 64, 0.22)
        self.bloom = gaussian_sprite(XC.mid, 96, 0.3)              # 100.4: the leaf's bloom, at the frame's centre
        # game A's board (S01's BoardRig: the same grid, marks, numbers and win line)
        self.board = BoardRig(GAME_A)
        self.board.place(BOARD_C, BOARD_S)
        spots = []
        for p, q in grid_lines(1.4):
            for i in range(6):
                u = (i + 0.5) / 6
                spots.append(BOARD_C + BOARD_S * (p + (q - p) * u))
        self.spots = np.array(spots)
        rng = np.random.default_rng(100)
        self.spot_spread = rng.normal(0, 0.06, (24, 2))
        self.spot_segs = [(BOARD_C + BOARD_S * p, BOARD_C + BOARD_S * q, (i + 0.5) / 6)
                          for p, q in grid_lines(1.4) for i in range(6)]
        self.grow = Hairlines(INK, 2.0)
        # the title and the end line
        self.title = TitleRig()
        self.end_line = s08.stacked([("完整版、程序和练习：见视频简介", INK_DIM, "zh"),
                                     ("FULL VERSION, PROGRAM AND EXERCISES: SEE THE DESCRIPTION", INK_DIM, "en")],
                                    align="c")
        self.title_src = None
        self.dark = Rectangle(width=W + 0.2, height=8.2).set_stroke(width=0).set_fill("#000000", opacity=0)

        self.clock_mob = Mobject()
        self.clock_mob.add_updater(lambda m: self.update_state(self.clock()))
        self.add(self.clock_mob, self.camera.frame)
        self.add(self.light)
        self.fix(self.edges, self.root_board.group, *self.path, self.leaf_halo, self.leaf_core, self.bloom, self.board.group,
                 self.grow,
                 *self.strips.sprites, self.strips.group, self.arm, self.pen, self.sec6, self.title.halo,
                 self.title.group, self.end_line.group, self.dark)
        self.title_sources()
        self.update_state(0.0)

    def title_sources(self):
        """Where the title's particles come from at 104.1: leaves of the small galaxy, and the board's lines."""
        rng = np.random.default_rng(1041)
        pick = rng.choice(len(L_TH), 2000, replace=False)
        g = gal_screen(L_TH[pick], L_R[pick], gcam(TITLE), rho(TITLE))
        lines = []
        for p, q in grid_lines(1.4):
            u = rng.random(250)[:, None]
            lines.append(BOARD_C + BOARD_S * (p + (q - p) * u))
        src = np.concatenate([g, *lines])
        tgt = self.title.targets
        order = np.argsort(src[:, 0])                     # left sources go to left glyphs (no crossing streams)
        src = src[order]
        tgt = tgt[np.argsort(tgt[:, 0])]
        self.title_src, self.title_tgt = src, tgt
        u = np.clip((tgt[:, 0] - tgt[:, 0].min()) / np.ptp(tgt[:, 0]), 0, 1)
        w = np.clip((u - 0.38) / 0.24, 0, 1)[:, None]
        self.title_col = (rgb(XC.mid)[None, :] * (1 - w) + rgb(OC.core)[None, :] * w)
        self.title_cool = (w[:, 0] < 0.5)
        self.title_delay = rng.uniform(0, 0.25, len(src))
        self.title_spin = rng.uniform(-0.6, 0.6, len(src))

    # ------------------------------------------------------------- the picture at time t
    def update_state(self, t: float):
        self.update_strips(t)
        self.update_light(t)
        self.update_tree(t)
        self.update_board(t)
        self.update_title(t)
        dark = ease_in_out_sine(seg(t, *FADE))
        self.dark.set_fill(opacity=dark)

    def dim(self, t: float) -> float:
        """The board and the galaxy dim to 30 % under the title (104.1)."""
        return 1 - 0.7 * ease_in_out_sine(seg(t, TITLE, TITLE + 0.6))

    # --- 99: S08's last frame, carried through the rush
    def update_strips(self, t: float):
        S = self.strips
        if t >= SETTLE[0] + 0.2:
            S.hide_all()
            self.pen.place((0, 0), 0)
            self.arm.hide()
            self.sec6.hide()
            return
        xf = rush_xf(t)
        k = xf[2]
        ghosts = []
        for lag, op in ((0.035, 0.4), (0.07, 0.2)):
            g = rush_xf(max(0.0, t - lag))
            if k / g[2] > 1.04:
                ghosts.append((g, op * min(1.0, (k / g[2] - 1.04) * 4)))
        vis = 1 - seg(t, RUSH[1] - 0.35, SETTLE[0] + 0.2)
        dig = 1 - seg(t, 0.5, 1.1)                       # the digits go before they get huge
        L = S.draw(S08_END, V0["z"], V0["rows"], xf=xf, vis=vis, ghosts=ghosts, lit=V0["lit"], grain=V0["grain"],
                   glow=1.0 - seg(t, 0.4, 1.2), breathe=V0["breathe"])
        for gl in S.digits.values():
            gl.mob.set_fill(opacity=gl.mob.get_fill_opacity() * dig)
        S.lit_digits.mob.set_fill(opacity=S.lit_digits.mob.get_fill_opacity() * dig)
        S.draw_labels(S08_END, L, V0["rows"], xf=None, vis=1 - seg(t, 0.0, 0.4))
        pv = 1 - seg(t, 0.0, 0.35)
        x, y = xf_apply(np.array([pen_x(S08_END, V0["z"]), V0["rows"]["chess"]]), xf)
        self.pen.place((x, y), pv, glow=s08.pen_glow(S08_END))
        self.arm.show(1.0, np.diag([1.0, 0.56]), (x, y), vis=0.3 * 0.4 * pv, glow=0.7) if pv > 1e-3 else self.arm.hide()
        self.sec6.show(self.sec6_c, vis=1 - seg(t, 0.0, 0.45))

    # --- the light layer: the galaxy (with its shimmer), the grain, the bloom's 24 points, the title's particles
    def update_light(self, t: float):
        fams = [[[], []] for _ in range(6)]

        def put(f, p, w):
            fams[f][0].append(p)
            fams[f][1].append(w)
        G, rh = gcam(t), rho(t)
        on = seg(t, 0.25, 0.9)                             # the galaxy takes over from box 1's glow
        fade = 1 - ease_in_out_sine(seg(t, *FADE))
        dim = self.dim(t) * fade
        if on > 1e-3 and fade > 1e-3:
            zf = zfac(min(G[2], 2.6)) * on * dim
            shim = self.shimmer(t)
            P = gal_screen(L_TH, L_R, G, rh)
            w = L_WEIGHT * zf * (1 if shim is None else shim(L_R))
            trails = self.trails(t)
            for f in range(3):
                sel = L_FAM == f
                put(f, P[sel], w[sel])
            for lag, k in trails:                          # motion blur while the camera dives or pulls back
                G2 = gcam(t - lag)
                P2 = gal_screen(L_TH, L_R, G2, rho(t - lag))
                for f in range(3):
                    sel = L_FAM == f
                    put(f, P2[sel], w[sel] * k)
            DP = gal_screen(N_TH[D_IDX], N_R[D_IDX], G, rh)
            dw = D_BASE * zf * (1 if shim is None else shim(N_R[D_IDX]))
            put(3, DP, dw)
        if t < SETTLE[0]:                                  # S08's grain, carried by the rush
            xf = rush_xf(t)
            p, w = grain_points(S08_END, V0["z"], V0["rows"], V0["grain"], xf)
            if p is not None:
                put(3, p, w * (1 - seg(t, 0.6, 1.4)))
        # 100.4: the bloom breaks into 24 points that fly onto the grid's lines
        if GATHER[0] <= t < GROW[1] + 0.1:
            e = ease_out_cubic(seg(t, *GATHER))
            src = LEAF_SCREEN + self.spot_spread
            pts = src + (self.spots - src) * e
            wv = 7.0 * (1 - seg(t, GROW[0] + 0.15, GROW[1] + 0.1))
            put(2, pts, np.full(24, wv))
            if e < 0.97:
                e2 = ease_out_cubic(seg(t - 0.03, *GATHER))
                put(2, src + (self.spots - src) * e2, np.full(24, 0.5 * wv))
        # 104.1: the title's particles
        if FORM[0] <= t < FORM[1] + 0.6:
            u = np.clip((t - FORM[0] - self.title_delay) / (FORM[1] - FORM[0] - 0.25), 0, 1)
            e = np.where(u < 0.5, 4 * u ** 3, 1 - (-2 * u + 2) ** 3 / 2)
            d = self.title_tgt - self.title_src
            nrm = np.column_stack([-d[:, 1], d[:, 0]])
            pts = self.title_src + d * e[:, None] + nrm * (self.title_spin * np.sin(np.pi * e))[:, None] * 0.25
            wv = 4.0 * (0.45 + 0.55 * np.sin(np.pi * np.clip(e * 1.15, 0, 1))) * (1 - seg(t, FORM[1] - 0.1, FORM[1] + 0.45))
            put(0, pts[self.title_cool], wv[self.title_cool])
            put(1, pts[~self.title_cool], wv[~self.title_cool])
        families = []
        for f, (ps, ws) in enumerate(fams):
            if ps:
                families.append((self.splat.accumulate(np.concatenate(ps), np.concatenate(ws)), GALAXY_COLOURS[f]))
        self.light.light = self.splat.render(families, **GALAXY_LOOK) if families else None

    def trails(self, t: float):
        if DIVE[0] + 0.6 <= t < PULL[1]:
            k = clamp01(1 - abs(t - BLOOM) / 0.6)
            return [(0.02, 0.5 * k), (0.04, 0.25 * k)]
        return []

    def shimmer(self, t: float):
        """103: a wave of light from the root outwards through every path (None outside it)."""
        if not (SHIMMER[0] <= t < SHIMMER[1] + 0.4):
            return None
        R = 3.2 * ease_in_out_sine(seg(t, *SHIMMER)) - 0.2
        return lambda r: 1 + 1.5 * np.exp(-((np.asarray(r) - R) / 0.28) ** 2)

    # --- the tree's structure: edges, root, game A's path, the leaf and its bloom, the pen
    def update_tree(self, t: float):
        G, rh = gcam(t), rho(t)
        fade = 1 - ease_in_out_sine(seg(t, *FADE))
        dim = self.dim(t) * fade
        ev = ease_in_out_sine(seg(t, SETTLE[0], DIVE[0] + 0.3)) * (1 - seg(t, DIVE[0] + 0.6, BLOOM)) + \
            ease_in_out_sine(seg(t, PULL[1] - 0.3, PULL[1] + 0.3))
        shim = self.shimmer(t)
        if ev > 1e-3 and dim > 1e-3 and G[2] < 4:
            pc = gal_screen(N_TH[EDGE_CHILD], N_R[EDGE_CHILD], G, rh)
            pp = gal_screen(N_TH[EDGE_PARENT], N_R[EDGE_PARENT], G, rh)
            pp[N_DEPTH[EDGE_CHILD] == 1] = [G[0], G[1]]
            boost = 1.0 if shim is None else float(shim(0.75))
            self.edges.set_segments(pp, pc, opacity=0.34 * ev * dim * boost)
        else:
            self.edges.set_segments([], [])
        rv = ev * dim
        if rv > 1e-3 and G[2] < 4:
            B = self.root_board.place((G[0], G[1]), G[2])
            B.draw_grid(1.0, vis=0.8 * rv, width=0.8)
        else:
            self.root_board.hide()
        # game A's path: the pen walks it, root to leaf, one segment per move (101.1-102.1)
        P = path_points(t)
        for j in range(5):
            f = ease_out_cubic(seg(t, MOVES[j], MOVES[j] + 0.4))
            if f <= 1e-3 or dim <= 1e-3:
                self.path[j].hide()
                continue
            A, c = line_affine(P[j], P[j] + (P[j + 1] - P[j]) * f)
            self.path[j].show(1.0, A, c, vis=0.85 * dim, glow=1.0 + 0.8 * pulse(t, MOVES[j], 0.3), width=0.9)
        # the pen: on the root from 100.4+, along the path in step with the marks, then on the leaf
        pv = ease_out_cubic(seg(t, PULL[1] - 0.25, PULL[1])) * dim
        if pv > 1e-3:
            k = sum(1 for m in MOVES if t >= m)
            if k == 0:
                q = P[0]
            else:
                f = ease_out_cubic(seg(t, MOVES[k - 1], MOVES[k - 1] + 0.4))
                q = P[k - 1] + (P[k] - P[k - 1]) * f
            out = 1 - ease_in_out_sine(seg(t, WIN + 0.6, WIN + 1.6))
            self.pen.place(q, pv * out, glow=1.0 + 0.7 * max([pulse(t, m, 0.25) for m in MOVES if t >= m] + [0]))
        elif t >= SETTLE[0] + 0.2:
            self.pen.place((0, 0), 0)
        # the leaf: a soft cyan point that swells as the camera dives at it; at 100.4 it blooms (the bloom stays
        # at the frame's centre and breaks into the grid's 24 points) while the leaf goes back with the galaxy;
        # it lights when the pen reaches it (102.1) and flares with the win line (102.2)
        lp = P[5]
        lv = ease_in_expo(seg(t, DIVE[0], BLOOM)) if DIVE[0] <= t < BLOOM else 0.0
        flare = pulse(t, WIN, 0.6) if t >= WIN else 0.0
        steady = ease_out_cubic(seg(t, MOVES[4], MOVES[4] + 0.3)) * 0.55 * dim
        size = min(0.05 * G[2], 1.2) * (1 + 1.5 * lv) + 0.25 * flare
        show_sprite(self.leaf_halo, lp, size * 3.2, size * 3.2, clamp01((lv + steady + 0.8 * flare) * fade))
        show_sprite(self.leaf_core, lp, size * 1.1, size * 1.1, clamp01((lv + steady + flare) * fade))
        if BLOOM <= t < BLOOM + 0.6:
            b = math.exp(-(t - BLOOM) / 0.16)
            bs = 3.0 * (1.2 + 0.6 * (1 - b)) * (0.35 + 0.65 * b)
            show_sprite(self.bloom, LEAF_SCREEN, bs * 2.6, bs * 2.6, clamp01(1.1 * b))
        else:
            show_sprite(self.bloom, opacity=0)

    # --- game A's board: it grows out of the bloom, then the game replays (S01's look and timing)
    def update_board(self, t: float):
        Bd = self.board
        if t < GROW[0]:
            Bd.hide()
            self.grow.set_segments([], [])
            return
        fade = 1 - ease_in_out_sine(seg(t, *FADE))
        vis = self.dim(t) * fade
        if vis <= 1e-3:
            Bd.hide()
            self.grow.set_segments([], [])
            return
        Bd.place(BOARD_C, BOARD_S)
        g = ease_out_quad(seg(t, *GROW))
        if g < 1:                                        # the lines grow out of the 24 spots (as S03 21.1)
            P, Q = [], []
            half = g / 12
            for (p, q, u) in self.spot_segs:
                P.append(p + (q - p) * max(0.0, u - half))
                Q.append(p + (q - p) * min(1.0, u + half))
            self.grow.set_segments(P, Q, opacity=(0.4 + 0.6 * g) * vis)
        else:
            self.grow.set_segments([], [])
        lf = [1.0 if g >= 1 else 0.0] * 4
        mf = [ease_out_cubic(seg(t, a, a + 0.25)) for a in MOVES]
        nv = [ease_out_cubic(seg(t, a + 0.12, a + 0.42)) for a in MOVES]
        wf = ease_out_quad(seg(t, WIN, WIN + BEAT))
        passes = ColdOpen.pass_times(WIN)
        glow, hl = ColdOpen.mark_levels(None, t, MOVES, passes, WIN, [-1e9] * 5, GAME_A)
        br = 0.12 * math.sin(2 * math.pi * (t - SHIMMER[0]) / BAR) if t >= SHIMMER[0] else 0.0
        glow = [g * (1 + br) for g in glow]
        Bd.draw(lf, mf, nv, wf, glow, hl, vis=vis)

    # --- 104: the title re-forms over the dimmed board and galaxy; 105.1 the end line
    def update_title(self, t: float):
        T = self.title
        fade = 1 - ease_in_out_sine(seg(t, *FADE))
        if t < FORM[0] + 0.2:
            T.show(0, 0, 0, 0, 0)
            self.end_line.hide()
            return
        core = ease_out_cubic(seg(t, FORM[1] - 0.35, FORM[1] + 0.25)) * fade
        breathe = 1 + 0.14 * math.sin(2 * math.pi * (t - FORM[1]) / BAR)
        glow = (ease_out_cubic(seg(t, FORM[1] - 0.2, FORM[1] + 0.4)) * breathe + 1.0 * pulse(t, FORM[1], 0.4)) * fade
        halo = ease_out_cubic(seg(t, FORM[1] - 0.2, FORM[1] + 0.5)) * (0.5 + 0.08 * math.sin(2 * math.pi * (t - FORM[1]) / BAR)) * fade
        word = ease_out_cubic(seg(t, FORM[1], FORM[1] + 0.6)) * fade
        sub = ease_out_cubic(seg(t, FORM[1] + 0.25, FORM[1] + 0.85)) * fade
        T.show(core, glow, halo, word, sub)
        ev = ease_out_cubic(seg(t, END_LINE, END_LINE + 0.8)) * fade
        self.end_line.show([0.0, -2.3 - 0.05 * (1 - ev)], "c", ev)

    # ------------------------------------------------------------- the sounds (from the same numbers)
    def score(self):
        S = self.sounds
        # 99.1: a reverse noise swell under the rush, an air whoosh as it accelerates through the box (video.yaml's
        # section cue brings the thump and Asus4; its act brings D back)
        S.effect(0.0, "swell", RUSH[1] - RUSH[0] + 0.3, x=float(PIVOT0[0]))
        S.effect(RUSH[1] - 0.6, "whoosh_up", 0.9, x=-0.6)
        # 100.4: the bloom (a shimmer) and the grid: four low plucks, as S01 drew it (bar 1)
        S.effect(BLOOM, "shimmer", 1.4, x=0.0)
        mids = [BOARD_C + BOARD_S * (p + q) / 2 for p, q in grid_lines(1.4)]
        S.phrase("grid", [(BLOOM + 0.15 * k, f"grid@{n}", float(m[0]))
                          for k, (n, m) in enumerate(zip(("D3", "A3", "E4", "A4"), mids))], gain=0.6)
        # 101-102: the motif, X bell / O glass at each square's pitch (now over the tonic), then the win run
        sq = lambda s_: BOARD_C + BOARD_S * square_centre(s_, 1.4)
        S.phrase("game A", [(t, tag(player(k), s_), float(sq(s_)[0])) for k, (t, s_) in enumerate(zip(MOVES, GAME_A))])
        S.phrase("win", [(t, f"X@{n}", float(sq(s_)[0]))
                         for t, n, s_ in zip(ColdOpen.pass_times(WIN), ("C#6", "D6", "E6"), (0, 1, 2))])
        S.effect(WIN, "whoosh_up", BEAT, float(sq(1)[0]))
        # 103: every game, once: a soft upward sweep of grains through Dmaj9
        tones = ("D4", "E4", "F#4", "A4", "C#5", "D5", "E5", "F#5", "A5", "C#6", "D6", "E6", "F#6", "A6", "C#7", "D7")
        gx = lambda k: float(SMALL[0] + SMALL[2] * 2.9 * (k / 15) * math.sin(2.4 * k))
        S.phrase("every game", [(SHIMMER[0] + 0.15 * k, f"glass@{tones[k]}", gx(k)) for k in range(16)], gain=0.3)
        # 104.1: the title gathers (a shimmer) and the motif's last note, E5, on the bell
        S.effect(TITLE, "shimmer", 2.0, x=0.0)
        S.phrase("last note", [(TITLE, f"X@{PITCH[2]}", 0.0)], gain=0.8)
        S.log(self)
        self.mark("riser", at=bb(100), dur=BAR)                   # the resolve's riser into 101.1
        self.mark("end", at=END_LINE)

    # ------------------------------------------------------------- the logged events and the clock
    def log_events(self):
        ev = self.shots

        def add(t, dur, x, y, w, h):
            ev.append((float(t), float(dur), (float(x), float(y), float(w), float(h))))
        for k in range(4):                                         # 99: the rush
            add(k * BEAT, BEAT, 0.0, 0.5, 13.0, 7.0)
        add(SETTLE[0], BEAT, *FULL[:2], 5.8, 5.8)
        for k in range(4):                                         # 100: the dive
            add(DIVE[0] + k * BEAT, BEAT, 0.0, 0.3, 13.0, 7.0)
        add(BLOOM, BEAT, -1.5, 0.3, 13.0, 7.0)                     # the bloom, the grid, the pull-back
        for t_, s_ in zip(MOVES, GAME_A):
            add(t_, 0.42, *(BOARD_C + BOARD_S * square_centre(s_, 1.4)), 0.9, 0.9)
            add(t_, 0.4, *SMALL[:2], 1.5, 1.5)                     # the pen's segment
        add(WIN, BEAT, BOARD_C[0], BOARD_C[1] + 1.44, 4.3, 0.2)
        add(WIN + BEAT, 2 * BEAT, -0.4, 0.3, 12.0, 4.5)
        for k in range(4):                                         # 103: the shimmer
            add(SHIMMER[0] + k * BEAT, BEAT, *SMALL[:2], 3.5, 3.5)
        add(TITLE, FORM[1] - FORM[0], 0.0, 0.3, 12.0, 4.5)         # 104: the title re-forms
        add(FORM[1], BEAT, 0.0, -0.9, 6.0, 0.6)
        add(FORM[1] + BEAT, BEAT, 0.0, 0.6, 10.0, 2.5)
        add(END_LINE, 2 * BEAT, 0.0, -2.3, 9.2, 0.6)
        add(END_LINE + 2 * BEAT, 2 * BEAT, 0.0, 0.3, 10.0, 3.0)
        add(FADE[0], FADE[1] - FADE[0], 0.0, 0.0, 14.0, 8.0)       # 106: to black

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
