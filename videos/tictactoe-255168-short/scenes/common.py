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
        return Ink(x_template(size), XC.core, 3.2, XC.glow, 16, layers=6, glow_opacity=0.55 * bright)
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
