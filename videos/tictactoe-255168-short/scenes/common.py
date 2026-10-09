"""Shared look, geometry and timing helpers of the tic-tac-toe short (script.md, "Conventions").

Every scene of the short draws its boards, marks, the light pen and the title number with these
helpers, so the same object always looks (and sounds) the same:

- Colours mean something: X is the cool family, O the warm one (a step darker), the light pen is
  white-hot with a neutral halo, line art is hairline INK on near-black, RED only means wrong.
- Sounds mean something: an X mark is a bell at its square's pitch, an O a glass tone
  (video.yaml music.square_pitches), so a game is heard as a melody. `Sounds` collects the notes
  of a scene and logs them as count marks with one tag per note ("X@C#5"), at the exact times the
  picture uses: explainer.music plays each one as tagged.
- The scenes are written as pure functions of the scene time t (`State`): every object is placed
  from a template each frame, so the picture at any moment does not depend on how the plays were
  cut, and the sound times come from the same numbers as the picture.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from manim import (Animation, Circle, Group, ImageMobject, Line, Mobject, Rectangle, Text, VGroup, VMobject,
                   config)

from explainer.short import (ACCENTS, BG, FONT_HEAVY, FONT_MONO, INK, INK_DIM, RED, WHITE, ParticleField,
                             RollingCounter, project_spec, stroke_px)

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent

W = config.frame_width            # 14.22 units: the full frame
H = config.frame_height           # 8 units

# ---------------------------------------------------------------- colours (script.md "Colour means something")
XC = ACCENTS["cool"]              # X: core #DDFFFF, mid #A3EBEF, glow #5AA9B4, halo #1B3438
OC = ACCENTS["warm"]              # O: core #F6C965, mid #CFA463, glow #784C2E, halo #442100
PEN = "#FFFFFF"                   # the light pen: white-hot core
PEN_HALO = "#DCE6E6"              # ... with a neutral halo
DRAW = INK                        # draws: grey-white, no hue

# ---------------------------------------------------------------- the game
GAME_A = (0, 3, 1, 4, 2)          # the cold-open game (X wins the top row on move 5): the motif
GAME_B = (2, 4, 0, 3, 1)          # same final board, another order
WIN_TOP = (0, 2)                  # game A's (and B's) win line: the top row

_DEFAULT_PITCHES = ["C#5", "D5", "E5", "G#4", "A4", "B4", "D4", "E4", "F#4"]


def square_pitches() -> list[str]:
    """Squares 0-8 -> note names (video.yaml music.square_pitches: a game is a melody)."""
    p = (project_spec().get("music") or {}).get("square_pitches")
    return list(p) if p and len(p) == 9 else list(_DEFAULT_PITCHES)


PITCH = square_pitches()


def rot_cw(i: int) -> int:
    """Square i after a quarter turn clockwise."""
    r, c = divmod(i, 3)
    return c * 3 + (2 - r)


def mirror_lr(i: int) -> int:
    """Square i after a flip about the vertical axis."""
    r, c = divmod(i, 3)
    return r * 3 + (2 - c)


def player(k: int) -> str:
    """Who plays move k (0-based): X on even moves."""
    return "X" if k % 2 == 0 else "O"


def tag(sym: str, square: int) -> str:
    """The sound tag of a mark: its player's timbre at its square's pitch ("X@C#5")."""
    return f"{sym}@{PITCH[square]}"


# ---------------------------------------------------------------- easing (arrivals ease out; no elastic)
def clamp01(x: float) -> float:
    return 0.0 if x <= 0 else 1.0 if x >= 1 else float(x)


def seg(t: float, a: float, b: float) -> float:
    """Progress 0..1 of t through [a, b]."""
    return clamp01((t - a) / (b - a)) if b > a else float(t >= a)


def ease_out_cubic(u: float) -> float:
    u = clamp01(u)
    return 1 - (1 - u) ** 3


def ease_out_quad(u: float) -> float:
    u = clamp01(u)
    return 1 - (1 - u) ** 2


def ease_in_out_sine(u: float) -> float:
    u = clamp01(u)
    return 0.5 - 0.5 * math.cos(math.pi * u)


def ease_in_out_cubic(u: float) -> float:
    u = clamp01(u)
    return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2


def ease_in_expo(u: float) -> float:
    u = clamp01(u)
    return 0.0 if u <= 0 else (2 ** (10 * u - 10) - 2 ** -10) / (1 - 2 ** -10)


def ease_in_cubic(u: float) -> float:
    u = clamp01(u)
    return u ** 3


def pulse(t: float, t0: float, decay: float = 0.3, attack: float = 0.03) -> float:
    """A flare at t0: rises in `attack` s, decays exponentially (0 before t0)."""
    if t < t0:
        return 0.0
    dt = t - t0
    return min(1.0, dt / attack) * math.exp(-max(0.0, dt - attack) / decay)


def lerp(a, b, u):
    return a + (b - a) * u


def mix_hex(c1: str, c2: str, u: float) -> np.ndarray:
    from manim import ManimColor
    a = np.array(ManimColor(c1).to_rgb())
    b = np.array(ManimColor(c2).to_rgb())
    return a + (b - a) * clamp01(u)


def rgb(c: str) -> np.ndarray:
    from manim import ManimColor
    return np.array(ManimColor(c).to_rgb(), dtype=float)


# ---------------------------------------------------------------- affine placement of templates
def affine(scale: float = 1.0, theta: float = 0.0, flip: float = 1.0) -> np.ndarray:
    """2x2 map: x-flip (1 .. -1, a card flip), then rotation by theta (radians, CCW), then scale."""
    c, s = math.cos(theta), math.sin(theta)
    return scale * np.array([[c, -s], [s, c]]) @ np.array([[flip, 0.0], [0.0, 1.0]])


def collapse(A: np.ndarray, b: np.ndarray, P, k: float) -> tuple[np.ndarray, np.ndarray]:
    """Compose a placement with a fall towards point P (k = 1: unchanged, 0: all at P)."""
    P = np.asarray(P, dtype=float)[:2]
    return A * k, P + (np.asarray(b, dtype=float)[:2] - P) * k


def _path_len(m: VMobject, samples: int = 16) -> float:
    pts = np.array([m.point_from_proportion(u) for u in np.linspace(0, 1, samples)])
    return float(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum())


class Ink(VGroup):
    """Stroke art (lines, circles) with a hot core over a stacked glow, re-placed every frame from a
    template in local coordinates. `show(f, A, b, ...)` reveals the parts in order (by length: an X
    is drawn as two strokes) up to fraction f and maps local -> world by x -> A x + b.

    Hidden ink gets stroke width 0, so Cairo skips it."""

    def __init__(self, tmpl: VMobject, color: str, width_px: float = 2.0, glow_color: str | None = None,
                 glow_px: float = 0.0, layers: int = 6, glow_opacity: float = 0.5, splits=None):
        super().__init__()
        self.parts = [p for p in tmpl.family_members_with_points()]
        if splits is None:
            ln = np.array([max(1e-6, _path_len(p)) for p in self.parts])
            self.cum = np.concatenate([[0.0], np.cumsum(ln)]) / ln.sum()
        else:
            self.cum = np.asarray(splits, dtype=float)
        self.layers = []           # (copies per part, width, opacity, is_core)
        if glow_color and glow_px > 0:
            for k in range(layers, 0, -1):
                w = stroke_px(2 * glow_px) * k / layers
                op = glow_opacity * (1 - k / (layers + 1)) ** 2
                cps = [p.copy().set_fill(opacity=0).set_stroke(glow_color, width=w, opacity=op) for p in self.parts]
                self.layers.append((cps, w, op, False))
        core_w = stroke_px(width_px)
        cps = [p.copy().set_fill(opacity=0).set_stroke(color, width=core_w, opacity=1.0) for p in self.parts]
        self.layers.append((cps, core_w, 1.0, True))
        for cps, _, _, _ in self.layers:
            self.add(*cps)
        self._scratch = [p.copy() for p in self.parts]
        self.color = color
        self.hide()

    def hide(self):
        for cps, _, _, _ in self.layers:
            for c in cps:
                c.set_stroke(width=0, opacity=0)
        return self

    def set_core_color(self, color):
        for c in self.layers[-1][0]:
            c.set_stroke(color=color)

    def show(self, f: float = 1.0, A=None, b=(0.0, 0.0), vis: float = 1.0, glow: float = 1.0,
             width: float = 1.0, core: float = 1.0, glow_width: float = 1.0):
        A = np.eye(2) if A is None else A
        b = np.asarray(b, dtype=float)[:2]
        if vis <= 1e-3 or f <= 1e-4:
            return self.hide()
        for i, p in enumerate(self.parts):
            a0, a1 = self.cum[i], self.cum[i + 1]
            fi = clamp01((f - a0) / max(1e-9, a1 - a0))
            if fi <= 2e-3:
                for cps, _, _, _ in self.layers:
                    cps[i].set_stroke(width=0, opacity=0)
                continue
            if fi >= 1 - 1e-6:
                src = p.points
            else:
                self._scratch[i].pointwise_become_partial(p, 0, fi)
                src = self._scratch[i].points
            q = src.copy()
            q[:, :2] = src[:, :2] @ A.T + b
            for cps, w, op, is_core in self.layers:
                c = cps[i]
                c.points = q.copy()
                if is_core:
                    c.set_stroke(width=w * width, opacity=clamp01(core * vis))
                else:
                    c.set_stroke(width=w * width * glow_width, opacity=clamp01(op * glow * vis))
        return self


class InkText(VGroup):
    """Filled glyphs (move numbers, a "?") placed from a template each frame without rotation (they
    stay upright): `show(centre, scale, sx, vis, color)`; sx squeezes the width (a card flip)."""

    def __init__(self, tmpl: VMobject, color: str = INK_DIM):
        super().__init__()
        self.tmpl = tmpl.copy().move_to([0, 0, 0])
        self.body = self.tmpl.copy()
        self.add(self.body)
        self._tf = [x for x in self.tmpl.get_family() if len(x.points)]
        self._bf = [x for x in self.body.get_family() if len(x.points)]
        self.color = color
        self.hide()

    def hide(self):
        for x in self._bf:
            x.set_fill(opacity=0).set_stroke(width=0, opacity=0)
        return self

    def show(self, centre, scale: float = 1.0, sx: float = 1.0, vis: float = 1.0, color=None):
        if vis <= 1e-3 or scale <= 1e-4 or abs(sx) <= 1e-3:
            return self.hide()
        c = np.asarray(centre, dtype=float)[:2]
        A = np.array([[scale * sx, 0.0], [0.0, scale]])
        col = color if color is not None else self.color
        for t, x in zip(self._tf, self._bf):
            q = t.points.copy()
            q[:, :2] = t.points[:, :2] @ A.T + c
            x.points = q
            x.set_fill(col, opacity=clamp01(vis)).set_stroke(width=0, opacity=0)
        return self


# ---------------------------------------------------------------- boards and marks (local coordinates)
def square_centre(i: int, cell: float) -> np.ndarray:
    r, c = divmod(i, 3)
    return np.array([(c - 1) * cell, (1 - r) * cell])


def grid_lines(cell: float, order: str = "pen") -> list[tuple[np.ndarray, np.ndarray]]:
    """The four grid lines of a board, as the pen draws them (boustrophedon: left vertical down, right
    vertical up, top horizontal right-to-left, bottom left-to-right)."""
    h, s = cell / 2, 1.5 * cell
    return [(np.array([-h, s]), np.array([-h, -s])), (np.array([h, -s]), np.array([h, s])),
            (np.array([s, h]), np.array([-s, h])), (np.array([-s, -h]), np.array([s, -h]))]


def x_template(size: float) -> VGroup:
    """An X as two strokes (top-left to bottom-right first), `size` wide, centred at the origin."""
    h = size / 2
    return VGroup(Line([-h, h, 0], [h, -h, 0]), Line([h, h, 0], [-h, -h, 0]))


def o_template(size: float) -> VMobject:
    """An O as one stroke, from 12 o'clock anticlockwise."""
    return Circle(radius=size / 2, num_components=12).rotate(math.pi / 2)


def mark_ink(sym: str, size: float, bright: float = 1.0) -> Ink:
    if sym == "X":
        return Ink(x_template(size), XC.core, 2.8, XC.glow, 12, layers=6, glow_opacity=0.42 * bright)
    return Ink(o_template(size), OC.core, 3.0, OC.glow, 15, layers=6, glow_opacity=0.5 * bright)


def win_template(a: int, b: int, cell: float, ext: float = 0.42) -> Line:
    p, q = square_centre(a, cell), square_centre(b, cell)
    d = (q - p) / np.linalg.norm(q - p)
    p, q = p - d * cell * ext, q + d * cell * ext
    return Line([p[0], p[1], 0], [q[0], q[1], 0])


def move_digit(n: int, size: float = 23) -> Text:
    return Text(str(n), font=FONT_MONO, font_size=size, color=INK_DIM)


# ---------------------------------------------------------------- light
def gaussian_sprite(color, px: int = 128, sigma: float = 0.32, opacity: float = 1.0, gradient=None,
                    aspect: float = 1.0) -> ImageMobject:
    """A soft radial light (RGBA). `gradient` = (left colour, right colour) for a halo that changes hue
    across its width (the title: cool on the left, warm on the right); `aspect` = width / height."""
    w, h = int(px * aspect), px
    y, x = np.mgrid[-1:1:h * 1j, -1:1:w * 1j]
    a = np.exp(-(x * x + y * y) / (2 * sigma ** 2))
    a[x * x + y * y > 1] = 0
    img = np.zeros((h, w, 4), np.uint8)
    if gradient is not None:
        u = (x + 1) / 2
        c0, c1 = rgb(gradient[0]), rgb(gradient[1])
        col = c0[None, None, :] * (1 - u[..., None]) + c1[None, None, :] * u[..., None]
    else:
        col = np.broadcast_to(rgb(color), (h, w, 3))
    img[..., :3] = np.clip(col * 255, 0, 255).astype(np.uint8)
    img[..., 3] = np.clip(255 * a * opacity, 0, 255).astype(np.uint8)
    im = ImageMobject(img)
    im.set_resampling_algorithm(2)
    return im


class Pen(Group):
    """The light pen: a white-hot dot with a neutral halo, drawn in screen space (a fixed mobject),
    so it is the same size on screen whatever the camera does. `place(screen_xy, vis)`."""

    def __init__(self, radius_px: float = 4.5, halo_px: float = 46):
        from manim import Dot
        self.halo_img = gaussian_sprite(PEN_HALO, 96, 0.28)
        self.halo_w = 2 * halo_px / 135.0
        self.halo_img.scale_to_fit_width(self.halo_w)
        self.core = Dot(radius=radius_px / 135.0, color=PEN)
        super().__init__(self.halo_img, self.core)
        self.place((0, 0), 0)

    def place(self, xy, vis: float = 1.0, glow: float = 1.0):
        p = np.array([xy[0], xy[1], 0.0])
        self.halo_img.move_to(p)
        self.core.move_to(p)
        self.halo_img.set_opacity(clamp01(0.85 * vis * glow))
        self.core.set_fill(PEN, opacity=clamp01(vis))
        return self


# ---------------------------------------------------------------- the camera as a function of time
class Cam:
    """A camera path: cam(t) -> (centre x, centre y, frame width). world <-> screen helpers."""

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, t):
        return self.fn(t)

    def to_screen(self, p, t):
        cx, cy, w = self.fn(t)
        k = W / w
        p = np.asarray(p, dtype=float)
        if p.ndim == 1:
            return np.array([(p[0] - cx) * k, (p[1] - cy) * k])
        out = np.empty((len(p), 2))
        out[:, 0] = (p[:, 0] - cx) * k
        out[:, 1] = (p[:, 1] - cy) * k
        return out

    def zoom(self, t) -> float:
        return W / self.fn(t)[2]


class ScreenField(ParticleField):
    """A particle field drawn in screen space (fix it in the scene): world positions(t) go through the
    camera path, so the splat stays sharp however far the camera zooms."""

    def __init__(self, world_positions, cam: Cam, weights=None, colors=None, **kw):
        self.world_positions = world_positions
        self.cam = cam
        self.world_weights = weights
        super().__init__(lambda t: self.cam.to_screen(self.world_positions(t), t),
                         weights=weights, colors=colors, **kw)


# ---------------------------------------------------------------- the title number (S01 bar 10, S05 59.1, S09)
TITLE_VALUE = 255_168
TITLE_SIZE = 178                  # Inter Black: digits about 1.85 units (23 % of the frame height), 10 wide


def title_counter(centre=(0.0, 0.55), size: float = TITLE_SIZE) -> RollingCounter:
    """The six-digit odometer that lands on 255,168: the same object, and so the same setting, every time
    the number is the hero (the title, the S05 landing, the coda)."""
    c = RollingCounter(TITLE_VALUE, digits=6, size=size, color=WHITE, leading_zeros=True)
    c.clear_updaters()            # driven by the scene's State
    c.move_to([centre[0], centre[1], 0])
    c.layout()
    return c


def final_glyphs(counter: RollingCounter) -> VGroup:
    """Static copies of what the counter shows at 255,168 (one glyph per digit, then the comma), placed
    exactly where the counter draws them."""
    counter.manual = None
    counter.value.set_value(TITLE_VALUE)
    counter.layout()
    out = []
    for col in counter.columns:
        vis = [g for g in col if g.get_fill_opacity() > 0.99]
        out.append(vis[0].copy())
    for _, sep in counter.separators:
        out.append(sep.copy())
    return VGroup(*out)


# ---------------------------------------------------------------- logging: plays and sounds
class Shot(Animation):
    """A logged visual event: no drawing of its own (the State draws everything), but the event log
    records its time, length, place and size, so the composer's brightness follows the motion."""

    def __init__(self, box: Mobject, **kw):
        kw.setdefault("rate_func", lambda u: u * u * (3 - 2 * u))
        super().__init__(box, **kw)

    def interpolate_mobject(self, alpha: float) -> None:
        pass


def box(x: float, y: float, w: float, h: float) -> Rectangle:
    """An invisible rectangle standing for a visual event's place and size (world units)."""
    return Rectangle(width=max(0.05, w), height=max(0.05, h)).move_to([x, y, 0]).set_stroke(width=0).set_fill(
        opacity=0)


class Sounds:
    """The notes of a scene, collected while it is built and logged as count marks (one per phrase) at
    the exact times the picture uses. Each note is (time, sound tag, screen x): "X@C#5" a bell at
    C#5, "O@G#4" glass, "grid@D3" a pluck (video.yaml music.sounds), "tick", or an effect name."""

    def __init__(self):
        self.phrases: list[tuple[str, list[tuple[float, str, float]], bool]] = []
        self.fx: list[tuple[float, str, float, float]] = []

    def phrase(self, name: str, notes, rise: bool = False, gain: float = 1.0):
        """One count mark: its notes get one crescendo (the composer's count velocity); `rise`: ticks
        and other unpitched items climb; `gain`: this phrase softer or louder."""
        notes = sorted((float(t), str(tg), float(x)) for t, tg, x in notes)
        if notes:
            self.phrases.append((name, notes, rise, float(gain)))

    def effect(self, t: float, sound: str, dur: float = 0.6, x: float = 0.0):
        self.fx.append((float(t), sound, float(dur), float(x)))

    def log(self, scene) -> None:
        for name, notes, rise, gain in self.phrases:
            extra = {} if gain == 1.0 else {"gain": round(gain, 3)}
            scene.mark("count", at=notes[0][0], n=len(notes), every=0.0, pitch="rise" if rise else "flat",
                       phrase=name, times=[round(t, 4) for t, _, _ in notes], sounds=[tg for _, tg, _ in notes],
                       xs=[round(x, 2) for _, _, x in notes], **extra)
        for t, sound, dur, x in self.fx:
            scene.mark("fx", at=t, dur=dur, sound=sound, x=round(x, 2))

    def table(self) -> list[tuple[float, str, str]]:
        rows = [(t, tg, name) for name, notes, _, _ in self.phrases for t, tg, _ in notes]
        rows += [(t, s, "fx") for t, s, _, _ in self.fx]
        return sorted(rows)


__all__ = [n for n in dir() if not n.startswith("_")]


# ================================================================ added for S02-S03 (used again by S04-S09)
# ---------------------------------------------------------------- the tree (script.md "The tree"), one geometry in
# S02 (the tree of fill orders) and S05-S09 (the galaxy): root at (-2.0, +0.3), ring d at radius 2.9 (d/9)^0.75,
# every node splits its wedge equally among its children, clockwise in square order 0 -> 8 from 12 o'clock.
import math as _math

TREE_ROOT = np.array([-2.0, 0.3])
NINE_FACT = _math.factorial(9)                     # 362,880 slots on the circle


def ring_radius(d: float) -> float:
    """Radius of ring d (after d moves): 0.56, 0.94, 1.27, 1.58, 1.87, 2.14, 2.40, 2.65, 2.90."""
    return 2.9 * (d / 9.0) ** 0.75


def ring_size(d: int) -> int:
    """Nodes on ring d of the tree of fill orders: 9!/(9-d)! (9, 72, 504, 3,024, ..., 362,880)."""
    return NINE_FACT // _math.factorial(9 - d)


def slot_angle(slot, n: int = NINE_FACT):
    """Angle (radians, clockwise from 12 o'clock) of the centre of slot `slot` of n equal slots."""
    return 2 * np.pi * (np.asarray(slot, dtype=float) + 0.5) / n


def tree_point(angle, r, phi: float = 0.0, root=TREE_ROOT) -> np.ndarray:
    """World point(s) at clockwise angle `angle` (+ a turn phi of the whole tree) and radius r."""
    a = np.asarray(angle, dtype=float) + phi
    r = np.asarray(r, dtype=float)
    return np.stack([root[0] + r * np.sin(a), root[1] + r * np.cos(a)], axis=-1)


def order_slot(moves) -> int:
    """The first of the (9 - k)! fill orders (lexicographic = clockwise) that begin with these k moves:
    its slot on ring 9. Game A (0, 3, 1, 4, 2) -> 10,200, at 10.12 degrees."""
    left, slot = list(range(9)), 0
    for i, m in enumerate(moves):
        slot += left.index(m) * _math.factorial(8 - i)
        left.remove(m)
    return slot


# S02's look of the tree of fill orders: neutral white-grey points, additive splats, ring 9 the luminous circle
# (S06 at 67.1 repeats S02's 18.1 flare frame with these numbers: FILL_WEIGHT[9] * fill_flare(t - hit)).
FILL_COLOR = (0.80, 0.82, 0.82)                    # INK, as an RGB triple for explainer.short.splat
FILL_SPLAT = dict(size_px=0.55, glow_px=3.2, glow_amount=0.8, gain=1.5)   # at resolution 0.5 (1080p px / 2)
FILL_JITTER = {2: 0.0, 3: 0.004, 4: 0.006, 5: 0.008, 6: 0.010, 7: 0.012, 8: 0.014, 9: 0.016}   # radial sigma
FILL_WEIGHT = {2: 1.0, 3: 0.45, 4: 0.09, 5: 0.012, 6: 0.0035, 7: 0.0012, 8: 0.0007, 9: 0.0034}  # per point


def fill_ring(d: int, seed: int = 362_880) -> tuple[np.ndarray, np.ndarray]:
    """Ring d of the tree of fill orders as (angles, radii): node i (lexicographic) at the centre of its
    wedge, its radius jittered (gaussian, clipped at 2.2 sigma; the same numbers in every scene)."""
    n = ring_size(d)
    rng = np.random.default_rng(seed + d)
    s = FILL_JITTER.get(d, 0.0)
    jit = np.clip(rng.normal(0.0, s, n), -2.2 * s, 2.2 * s) if s > 0 else np.zeros(n)
    return slot_angle(np.arange(n), n), ring_radius(d) + jit


def fill_flare(dt: float) -> float:
    """Ring 9's brightness multiplier around its flare (S02 18.1, again at S06 67.1): dt = t - hit."""
    if dt < 0:
        return 1.0
    return 1.0 + 2.6 * min(1.0, dt / 0.03) * _math.exp(-max(0.0, dt - 0.03) / 0.5)


# ---------------------------------------------------------------- bilingual labels and the section HUD
def bi_label(zh: str, en: str, zh_size: float = 22, en_size: float = 20, color: str = INK,
             en_color: str | None = None, spacing: float = 0.22, gap: float = 0.16) -> VGroup:
    """A one-line bilingual label, Chinese first: "8 条获胜线 · 8 LINES" (Noto Serif CJK SC, then tracked
    Noto Sans Mono caps; en_size 20 is 27 px caps at 1080p). Parts: [0] zh, [1] the dot, [2] en."""
    from explainer.short import cjk, tracked
    a = cjk(zh, size=zh_size, color=color)
    dot = cjk("·", size=zh_size, color=en_color or color)
    b = tracked(en, size=en_size, spacing=spacing, color=en_color or color)
    g = VGroup(a, dot, b).arrange(buff=gap)
    b.align_to(a, direction=np.array([0, -1, 0])).shift(np.array([0, 0.012 * zh_size / 19, 0]))
    return g


def section_hud(text: str, zh_size: float = 15, en_size: float = 12.5, color: str = INK_DIM) -> VGroup:
    """The section label, top left, fixed in the frame: "§2 · 对局会提前结束 · GAMES STOP EARLY" (video.yaml
    sections), as BeatScene.hud places a corner label (buff 0.55). The same object across scene cuts."""
    from explainer.short import cjk, tracked
    num, zh, en = [p.strip() for p in text.split("·", 2)]
    parts = [tracked(num, size=en_size, spacing=0.2, color=color, upper=False), cjk("·", size=zh_size, color=color),
             cjk(zh, size=zh_size, color=color), cjk("·", size=zh_size, color=color),
             tracked(en, size=en_size, spacing=0.25, color=color)]
    g = VGroup(*parts).arrange(buff=0.12)
    for p in (parts[0], parts[4]):
        p.align_to(parts[2], direction=np.array([0, -1, 0])).shift(np.array([0, 0.01, 0]))
    g.move_to(np.array([-W / 2 + 0.55 + g.width / 2, H / 2 - 0.55 - g.height / 2, 0]))
    return g


# ================================================================ added for S04-S05 (used again by S06-S09)
# The galaxy (the program's game tree: 255,168 leaves and 294,778 internal nodes, splatted into one light
# image per frame), the explore() plate and the HUD readout lines. S06 continues all three from S05's last
# frame (the segue at 62.1), S07-S09 draw the same galaxy: same points, same weights, same tone map.
from functools import lru_cache as _lru_cache

_EMPTY_PTS = np.zeros((0, 3))


class LeanInk(Ink):
    """Ink whose hidden strokes drop their points, so Cairo skips them (pools of marks, mostly hidden)."""

    def hide(self):
        super().hide()
        for cps, _, _, _ in self.layers:
            for c in cps:
                c.points = _EMPTY_PTS
        return self

    def show(self, *a, **kw):
        out = super().show(*a, **kw)
        for cps, _, _, _ in self.layers:
            for c in cps:
                if c.stroke_width == 0 or (len(c.points) and c.get_stroke_opacity() <= 1e-3):
                    c.points = _EMPTY_PTS
        return out


class LeanText(InkText):
    """InkText whose hidden glyphs drop their points (show() places them again)."""

    def hide(self):
        for x in self._bf:
            x.points = _EMPTY_PTS
            x.set_fill(opacity=0).set_stroke(width=0, opacity=0)
        return self


def cull(mobs) -> None:
    """Drop the points of invisible glyphs (a rolling counter's other digits); `uncull` brings them back
    before the counter lays itself out again."""
    for g in mobs:
        if g.get_fill_opacity() <= 1e-3 and len(g.points):
            g._stash = g.points
            g.points = _EMPTY_PTS


def uncull(mobs) -> None:
    for g in mobs:
        st = g.__dict__.pop("_stash", None)
        if st is not None:
            g.points = st


def counter_glyphs(c) -> list:
    return [g for col in c.columns for g in col] + [sep for _, sep in c.separators]


def show_sprite(img, centre=None, width=None, height=None, opacity: float = 1.0) -> None:
    """Place a light sprite (an ImageMobject); a hidden one drops its corner points, so the camera skips
    its (costly) image transform."""
    if opacity <= 1e-3:
        if len(img.points):
            img._stash = img.points
            img.points = _EMPTY_PTS
        return
    st = img.__dict__.pop("_stash", None)
    if st is not None:
        img.points = st
    if width is not None:
        img.stretch_to_fit_width(width)
    if height is not None:
        img.stretch_to_fit_height(height)
    if centre is not None:
        img.move_to([centre[0], centre[1], 0])
    img.set_opacity(clamp01(opacity))


# ---------------------------------------------------------------- the HUD readouts, top right (S04-S07)
def hud_label(zh: str, en: str, size: float = 12) -> VGroup:
    """A readout label "中文 · ENGLISH" in the HUD style (tiny, 50 % grey)."""
    from explainer.short import cjk, tracked
    g = VGroup(cjk(zh, size=size, color=INK_DIM), cjk("·", size=size, color=INK_DIM),
               tracked(en, size=size, spacing=0.25, color=INK_DIM)).arrange(buff=0.12)
    g[2].align_to(g[0], direction=np.array([0, -1, 0]))
    return g


HUD_RIGHT = W / 2 - 0.45                           # the readouts' right edge
HUD_LINES_Y = [3.55, 3.31, 3.07]                   # line 1, 2, 3 (S05: games counted, calls, undos)


class HudLine:
    """One readout line "中文 · ENGLISH  000,000" (a six-digit mono odometer), right-aligned at the HUD's
    right edge, fixed in the frame: `show(value, vis)`; nothing is redone while nothing changes."""

    def __init__(self, zh: str, en: str, y: float, digits: int = 6, leading_zeros: bool = True):
        self.label = hud_label(zh, en)
        self.counter = RollingCounter(0, digits=digits, size=12, color=INK_DIM, font=FONT_MONO, weight="NORMAL",
                                      leading_zeros=leading_zeros)
        self.counter.clear_updaters()
        self.counter.move_to([HUD_RIGHT - self.counter.ref.width / 2, y, 0])
        self.counter.layout()
        self.label.next_to(self.counter.ref, np.array([-1, 0, 0]), buff=0.22)
        self.label.align_to(self.counter.columns[0][0], np.array([0, -1, 0]))
        self.lab_t = LeanText(self.label, INK_DIM)
        self.lab_c = self.label.get_center()[:2]
        self.group = Group(self.lab_t, self.counter)
        self.y = y
        self._last = None

    def show(self, value: float, vis: float, color=INK_DIM):
        key = (round(float(value), 3), round(vis, 4), color)
        if key == self._last:
            return
        self._last = key
        self.lab_t.show(self.lab_c, vis=vis, color=INK_DIM)
        c = self.counter
        gl = counter_glyphs(c)
        uncull(gl)
        c.value.set_value(max(0.0, float(value)))
        c.layout()
        for col in c.columns:
            for g in col:
                g.set_fill(color, opacity=g.get_fill_opacity() * vis)
        for _, sep in c.separators:
            sep.set_fill(color, opacity=vis)
        cull(gl)


# ---------------------------------------------------------------- the galaxy: every explore() call of the program
GALAXY_SEED = 255_168


class GalaxyTree:
    """The program's search, in its order (= clockwise), as arrays. Leaves (games): slot start, moves
    (padded with -1), result (1 X wins, 2 O wins, 3 draw), length k, last square, slot centre, radial jitter,
    weight, colour family. Internal nodes: slot start, depth, slot centre; `dust` is the subset S05 draws
    as faint dust (all of rings 0-5, a third of rings 6-8 at three times the weight)."""

    def __init__(self):
        fact = [_math.factorial(9 - k) for k in range(10)]
        lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        l_slot, l_moves, l_res, n_slot, n_depth = [], [], [], [], []
        b, seq = [0] * 9, []

        def win():
            for a, c, d in lines:
                if b[a] and b[a] == b[c] == b[d]:
                    return b[a]
            return 0

        def walk(p, s0):
            w, d = win(), len(seq)
            if w or d == 9:
                l_slot.append(s0)
                l_moves.append(tuple(seq))
                l_res.append(w if w else 3)
                return
            n_slot.append(s0)
            n_depth.append(d)
            k = 0
            for sq in range(9):
                if b[sq] == 0:
                    b[sq] = p
                    seq.append(sq)
                    walk(3 - p, s0 + k * fact[d + 1])
                    seq.pop()
                    b[sq] = 0
                    k += 1
        walk(1, 0)
        self.fact = fact
        self.l_slot = np.array(l_slot, np.int64)
        self.l_moves = np.full((len(l_moves), 9), -1, np.int8)
        for i, m in enumerate(l_moves):
            self.l_moves[i, :len(m)] = m
        self.l_res = np.array(l_res, np.int8)
        self.l_k = (self.l_moves >= 0).sum(axis=1).astype(np.int8)
        self.l_last = self.l_moves[np.arange(len(self.l_k)), self.l_k - 1]
        self.l_centre = self.l_slot + np.array(fact, dtype=float)[self.l_k] / 2
        self.n_slot = np.array(n_slot, np.int64)
        self.n_depth = np.array(n_depth, np.int8)
        self.n_centre = self.n_slot + np.array(fact, dtype=float)[self.n_depth] / 2
        rng = np.random.default_rng(GALAXY_SEED)
        self.l_jit = rng.uniform(-0.03, 0.03, len(self.l_slot))           # radial jitter <= 0.03
        keep = (self.n_depth <= 5) | (rng.random(len(self.n_slot)) < 1 / 3)
        self.dust = np.flatnonzero(keep)
        self.dust_w = np.where(self.n_depth[self.dust] <= 5, 1.0, 3.0)
        self.l_weight = GALAXY_SLOT_W * np.array(fact, dtype=float)[self.l_k]
        self.l_fam = np.where(self.l_res == 1, 0, np.where(self.l_res == 2, 1, 2)).astype(np.int8)
        self.all_starts = np.sort(np.concatenate([self.n_slot, self.l_slot]))   # every explore() call


@_lru_cache(maxsize=1)
def galaxy_tree() -> GalaxyTree:
    """The tree, built once per process (about 1.5 s)."""
    return GalaxyTree()


def galaxy_point(slot_centre, depth, dx=0.0, m: float = 1.0, rho: float = 0.0, dr=0.0) -> np.ndarray:
    """World position(s) of a node: ring `depth` (+ dr), at its slot's angle clockwise from 12 o'clock, plus
    an arc offset dx * m (S05's magnifier), the whole tree turned clockwise by rho (radians)."""
    r = 2.9 * (np.asarray(depth, dtype=float) / 9.0) ** 0.75 + dr
    th = 2 * np.pi * np.asarray(slot_centre, dtype=float) / NINE_FACT + rho
    with np.errstate(divide="ignore", invalid="ignore"):
        th = th + np.where(r > 0, m * np.asarray(dx) / np.maximum(r, 1e-6), 0.0)
    return np.stack([TREE_ROOT[0] + r * np.sin(th), TREE_ROOT[1] + r * np.cos(th)], axis=-1)


# the galaxy's light: a leaf shines in proportion to the slots it owns, (9 - k)! of the 9!, so a lit band has
# the same surface brightness on every ring and its coverage is the ring's share of 9! (9.5 / 8.8 / 26.4 /
# 20.0 / 35.2 %). A ghost game (S06) owns one slot and gets GALAXY_SLOT_W, so a leaf's light can stream into
# its (9 - k)! ghosts unchanged in total, and the full ring 9 is brighter than S05's 35 % one only by the
# slots lit. Weights are multiplied by zoom^2 (the same surface brightness at any zoom).
GALAXY_SLOT_W = 0.065
GALAXY_DUST_W = np.array([0.0, 2.4, 1.2, 0.6, 0.3, 0.16, 0.09, 0.06, 0.05, 0.0])   # internal nodes, by ring
GALAXY_COLOURS = [rgb(XC.mid), rgb(OC.mid), rgb("#C8CCCC"), rgb(INK_DIM), rgb("#FC6255"), rgb("#FFFFFF")]
GALAXY_LOOK = dict(glow_px=7.0, glow_amount=0.55, gain=1.0, gamma=0.75)              # Splatter.render
_LUT_SCALE = 1024.0                                # lookup-table steps per unit of intensity (up to 8)


@_lru_cache(maxsize=8)
def _galaxy_lut(gain: float, gamma: float) -> np.ndarray:
    i = np.arange(int(8 * _LUT_SCALE)) / _LUT_SCALE
    return np.clip(255 * (1 - np.exp(-gain * i ** gamma)), 0, 255).astype(np.uint8)


class Splatter:
    """Points -> one RGB light image per frame (light on black): bilinear splats per colour family plus a
    wide gaussian glow (on a half-size grid), summed in light and tone-mapped per channel with headroom,
    1 - exp(-gain I^gamma), through a lookup table. Intensity is weight per 1080p pixel, so the picture
    does not depend on the render resolution. Show it with a FrameImage (and FastCamera)."""

    def __init__(self, res: float = 0.5):
        self.w = max(16, int(round(config.pixel_width * res)))
        self.h = max(16, int(round(config.pixel_height * res)))
        self.scale = res * config.pixel_height / 1080          # pixels of this image per 1080p pixel
        self.ppu = self.h / H                                   # image pixels per screen unit

    def accumulate(self, xy, w) -> np.ndarray:
        """xy: (n, 2) screen units; w: (n,) -> (h, w) float32 weights per image pixel."""
        W_, H_ = self.w, self.h
        u = (xy[:, 0] + W / 2) * self.ppu - 0.5
        v = (H / 2 - xy[:, 1]) * self.ppu - 0.5
        w = np.asarray(w, dtype=float)
        keep = (u > -2) & (u < W_ + 1) & (v > -2) & (v < H_ + 1) & (w > 0)
        u, v, w = u[keep], v[keep], w[keep]
        acc = np.zeros(H_ * W_, np.float64)
        if len(u):
            iu, iv = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
            fu, fv = u - iu, v - iv
            for du, dv, ww in ((0, 0, (1 - fu) * (1 - fv)), (1, 0, fu * (1 - fv)), (0, 1, (1 - fu) * fv),
                               (1, 1, fu * fv)):
                x, y = iu + du, iv + dv
                ok = (x >= 0) & (x < W_) & (y >= 0) & (y < H_)
                acc += np.bincount((y * W_ + x)[ok], (ww * w)[ok], H_ * W_)
        return acc.reshape(H_, W_).astype(np.float32)

    def render(self, families, glow_px: float = 7.0, glow_amount: float = 0.55, gain: float = 1.0,
               gamma: float = 0.75) -> np.ndarray:
        """families: [(accumulate(...) image, rgb colour)] -> RGB uint8 light (h, w, 3)."""
        from scipy.ndimage import gaussian_filter
        h, w = self.h, self.w
        h2, w2 = h // 2, w // 2
        acc = np.zeros((3, h, w), np.float32)
        for img, col in families:
            if img is None:
                continue
            for c in range(3):
                if col[c] > 0:
                    acc[c] += np.float32(col[c]) * img
        dens = np.float32(self.scale * self.scale)
        small = acc[:, :h2 * 2, :w2 * 2].reshape(3, h2, 2, w2, 2).sum(axis=(2, 4))
        sig = max(0.5, glow_px * self.scale / 2)
        glow = gaussian_filter(small, (0, sig, sig), truncate=2.5)
        acc *= dens
        acc[:, :h2 * 2, :w2 * 2] += np.repeat(np.repeat(glow, 2, axis=1), 2, axis=2) * np.float32(glow_amount * dens / 4)
        lut = _galaxy_lut(round(gain, 4), round(gamma, 4))
        idx = np.minimum(acc * np.float32(_LUT_SCALE), np.float32(len(lut) - 1)).astype(np.int32)
        return np.ascontiguousarray(lut[idx].transpose(1, 2, 0))


class FrameImage(ImageMobject):
    """A full-frame light layer: `light` is an RGB uint8 image (light on black, any size) that FastCamera
    scales to the frame and blends on with "lighten" (Manim's general image path costs ~120 ms a frame at
    1080p). Add it before everything it should sit under; `light = None` shows nothing."""
    fullframe = True

    def __init__(self):
        super().__init__(np.zeros((8, 8, 4), np.uint8))
        self.stretch_to_fit_width(W)
        self.stretch_to_fit_height(H)
        self.light = None


def _fast_camera_class():
    from PIL import Image as _Image
    from explainer.short import HUDCamera

    class FastCamera(HUDCamera):
        """HUDCamera that draws FrameImage layers straight onto the frame (pass camera_class=FastCamera)."""

        def display_image_mobject(self, image_mobject, pixel_array):
            if getattr(image_mobject, "fullframe", False):
                light = image_mobject.light
                if light is None:
                    return
                img = _Image.fromarray(light, "RGB")
                if img.size != (self.pixel_width, self.pixel_height):
                    img = img.resize((self.pixel_width, self.pixel_height), _Image.BILINEAR)
                np.maximum(pixel_array[..., :3], np.asarray(img), out=pixel_array[..., :3])
                return
            super().display_image_mobject(image_mobject, pixel_array)
    return FastCamera


FastCamera = _fast_camera_class()


# ---------------------------------------------------------------- the explore() plate (S05, S06), screen space
PLATE_LINES = [(23, "def explore(player):"), (24, "  if winner(board) is not None:"), (25, "    return 1"),
               (26, '  if "." not in board:'), (27, "    return 1"), (None, "      ⋯"),
               (31, "      board[square] = player"), (None, "      ⋯"),
               (33, "      total += explore(next_player)"), (34, '      board[square] = "."')]
PLATE_TL = np.array([-6.9, 2.98])                  # S05: the plate's top-left corner on screen
PLATE_SIZE = 8.8
PLATE_PITCH = 0.19


class ProgramPlate:
    """The explore() plate: file lines 23-27, ⋯, 31, ⋯, 33, 34 of the long video's play_all_games.py
    (comments removed, two spaces per level), mono and grey, with line numbers and the tag "程序 · THE
    PROGRAM"; any line can be highlighted. Screen space: `show(vis, hl, line_vis, tl, scale)` with
    hl = {file line: (amount 0-1, colour)} (white, or RED for the undo line)."""

    def __init__(self, tl=PLATE_TL, size: float = PLATE_SIZE, pitch: float = PLATE_PITCH):
        from explainer.short import cjk, tracked
        self.tl = np.asarray(tl, dtype=float)
        self.pitch = pitch
        self.char_w = Text("M" * 20, font=FONT_MONO, font_size=size).width / 20    # (Text drops leading blanks)
        self.rows = []
        y = -0.42
        for num, code in PLATE_LINES:
            ln = Text(f"{num:>2}" if num else "  ", font=FONT_MONO, font_size=size, color=INK_DIM)
            indent = (len(code) - len(code.lstrip(" "))) * self.char_w
            tx = Text(code.strip(), font=FONT_MONO, font_size=size, color=INK_DIM)
            self.rows.append((num, LeanText(ln, INK_DIM), LeanText(tx, INK_DIM), ln.width, tx.width + indent, y,
                              indent))
            y -= pitch
        self.width = max(r[4] for r in self.rows) + 0.62
        self.height = -y + 0.05
        self.frame = LeanInk(Rectangle(width=self.width, height=self.height), INK_DIM, 1.2)
        self.bars = {num: Rectangle(width=self.width - 0.12, height=pitch * 0.92).set_stroke(width=0)
                     .set_fill(WHITE, opacity=0) for num, *_ in self.rows if num}
        self.tag_zh = LeanText(cjk("程序", size=12, color=INK_DIM), INK_DIM)
        self.tag_en = LeanText(tracked("THE PROGRAM", size=12, spacing=0.25, color=INK_DIM), INK_DIM)
        self.group = Group(self.frame, *self.bars.values(), *[r[1] for r in self.rows], *[r[2] for r in self.rows],
                           self.tag_zh, self.tag_en)

    def row_y(self, num: int, tl=None, scale: float = 1.0) -> float:
        tl = self.tl if tl is None else np.asarray(tl, dtype=float)
        return tl[1] + scale * next(r[5] for r in self.rows if r[0] == num)

    def row_right(self, num: int, tl=None, scale: float = 1.0) -> float:
        tl = self.tl if tl is None else np.asarray(tl, dtype=float)
        return tl[0] + scale * (0.5 + next(r[4] for r in self.rows if r[0] == num))

    def show(self, vis: float, hl=None, line_vis=None, tl=None, scale: float = 1.0):
        hl = hl or {}
        tl = self.tl if tl is None else np.asarray(tl, dtype=float)
        k = scale
        c = tl + k * np.array([self.width / 2, -self.height / 2])
        self.frame.show(1.0, np.eye(2) * k, c, vis=0.6 * vis)
        base = rgb(INK_DIM)
        for j, (num, lnum, txt, lw, tw, y, ind) in enumerate(self.rows):
            lv = vis if line_vis is None else vis * line_vis[j]
            amt, col = hl.get(num, (0.0, WHITE))
            tc = base * (1 - amt) + rgb(col if col != WHITE else "#F2F4F4") * amt
            tc = "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in np.clip(tc, 0, 1))
            yy = tl[1] + k * y
            lnum.show([tl[0] + k * (0.1 + lw / 2), yy], scale=k, vis=lv * 0.8, color=INK_DIM)
            txt.show([tl[0] + k * (0.5 + ind + (tw - ind) / 2), yy], scale=k, vis=lv, color=tc)
            if num in self.bars:
                b = self.bars[num]
                b.stretch_to_fit_width((self.width - 0.12) * k).stretch_to_fit_height(self.pitch * 0.92 * k)
                b.move_to([c[0], yy, 0])
                b.set_fill(col, opacity=clamp01(0.13 * amt * lv))
        self.tag_zh.show(tl + k * np.array([0.18, 0.17]), scale=k, vis=vis, color=INK_DIM)
        self.tag_en.show(tl + k * np.array([0.42 + self.tag_en.tmpl.width / 2, 0.17]), scale=k, vis=vis,
                         color=INK_DIM)


__all__ += ["LeanInk", "LeanText", "cull", "uncull", "counter_glyphs", "show_sprite", "hud_label",
            "HUD_RIGHT", "HUD_LINES_Y", "HudLine", "GALAXY_SEED", "GalaxyTree", "galaxy_tree", "galaxy_point",
            "GALAXY_SLOT_W", "GALAXY_DUST_W", "GALAXY_COLOURS", "GALAXY_LOOK", "Splatter", "FrameImage",
            "FastCamera", "PLATE_LINES", "PLATE_TL", "PLATE_SIZE", "PLATE_PITCH", "ProgramPlate"]
