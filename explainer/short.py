"""The short format: music-led, caption-led films on a beat grid (see docs/SHORTS.md).

    from explainer.short import *

    class ColdOpen(BeatScene):                 # MovingCameraScene + beat grid + event log + captions
        def construct(self):
            self.fig(1, "HOW MANY GAMES", "多少局")             # HUD label, fixed when the camera moves
            board = hairline(Square(3))
            self.play(Create(board), bars=1)                      # starts on the next bar, lasts one bar
            self.caption("games")                                 # captions.yaml line, shown now
            self.count(marks, every="eighth", sound="X")          # one mark (and one bell) per eighth note
            self.play(self.zoom_to(board, width=6), beats=4, rate_func=ease_in_expo)
            self.mark("hit"); self.play(FadeIn(glowing(title)), beats=1)
            self.wait_bars(2)                                     # the scene ends on a bar line anyway

Palette (one accent family per video, with a meaning): pure black BG, hairline INK line art, INK_DIM
for secondary lines, ACCENTS["cool"] / ACCENTS["warm"] (core -> mid -> glow -> halo), RED only for
"wrong / deleted / fails". Typography: FONT_CJK_SERIF (Song/Ming) for Chinese, FONT_TRACKED
(Montserrat) for wide-tracked title words, FONT_HEAVY (Inter Black) for one hero number per scene,
FONT_OLDSTYLE (EB Garamond italic) for small formula labels, FONT_MONO for the HUD.

Timing: every grid point is a whole number of frames (100 BPM: 36 frames a beat at 60 fps), so cuts
and reveals land exactly on beats and bars across the stitched video; the music composer
(explainer.music) reads the same grid from the event log.
"""

from __future__ import annotations

import inspect
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
from manim import (BOLD, DOWN, HEAVY, ITALIC, LEFT, NORMAL, ORIGIN, RIGHT, UL, UP, UR, Animation, FadeIn, Group,
                   ImageMobject, LaggedStart, Line, MarkupText, MovingCamera, MovingCameraScene, Rectangle, Text,
                   ValueTracker, VGroup, VMobject, config, linear, logger, rate_functions)

from . import captions as cap
from . import style
from .events import EventLog
from .grid import Grid, frames, hold_time, play_time

# ---------------------------------------------------------------- palette (short profile)
BG = "#050505"
INK = "#C8CCCC"            # hairline line art and text
INK_DIM = "#7D8484"        # secondary lines, HUD
INK_FAINT = "#3A3F3F"      # construction lines
GRID_LINE = "#151515"      # a faint background grid
RED = "#FC6255"            # the only extra hue: wrong / deleted / fails
WHITE = "#ECEDEB"


@dataclass(frozen=True)
class Accent:
    """One glowing accent family, from the hot core to the faint halo."""
    core: str
    mid: str
    glow: str
    halo: str


ACCENTS = {
    "cool": Accent("#DDFFFF", "#A3EBEF", "#5AA9B4", "#1B3438"),
    "warm": Accent("#F6C965", "#CFA463", "#784C2E", "#442100"),
}

FONT_CJK_SERIF = style.FONT_CJK_SERIF
FONT_TRACKED = style.FONT_TRACKED
FONT_HEAVY = style.FONT_HEAVY
FONT_OLDSTYLE = style.FONT_OLDSTYLE
FONT_MONO = style.FONT_MONO

PX = 1080 / 8.0            # pixels per Manim unit at 1080p (the default 8-unit-high frame)


def px(n: float) -> float:
    """Manim units of `n` pixels at 1080p."""
    return n / PX


def stroke_px(n: float) -> float:
    """The stroke_width that draws an `n`-pixel line at 1080p (Manim: width 1 = 0.01 units)."""
    return n / (PX * 0.01)


# ---------------------------------------------------------------- project settings

@lru_cache(maxsize=4)
def _spec_for(project: str | None) -> dict:
    if not project:
        return {}
    p = Path(project) / "video.yaml"
    if not p.exists():
        return {}
    import yaml
    return yaml.safe_load(p.read_text()) or {}


def project_spec() -> dict:
    """The video.yaml of the project being rendered (EXPLAINER_PROJECT, or the working directory)."""
    from .i18n import project_dir
    d = project_dir()
    return _spec_for(str(d) if d else None)


def _project() -> Path | None:
    from .i18n import project_dir
    return project_dir()


# ---------------------------------------------------------------- typography

def letter_spacing_units(spacing_em: float, font_size: float) -> int:
    """Pango letter_spacing for `spacing_em` (fraction of the em) at `font_size` (measured on
    ManimPango 0.7: 1000 Pango units add 0.0488 Manim units per gap at any font size)."""
    return int(round(spacing_em * font_size / 72 / 0.048828125 * 1000))


def _markup_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tracked(s: str, size: float = 20, spacing: float = 0.3, font: str = FONT_MONO, color: str = INK_DIM,
            weight=NORMAL, upper: bool = True, **kw) -> MarkupText:
    """Letter-spaced text (HUD labels, title words): `spacing` in em."""
    s = s.upper() if upper else s
    ls = letter_spacing_units(spacing, size)
    return MarkupText(f'<span letter_spacing="{ls}">{_markup_escape(s)}</span>', font=font, font_size=size,
                      color=color, weight=weight, **kw)


def cjk(s: str, size: float = 40, color: str = INK, weight=NORMAL, **kw) -> Text:
    """Chinese text in the Song/Ming serif."""
    return Text(s, font=f"{FONT_CJK_SERIF}", font_size=size, color=color, weight=weight, **kw)


def hero_number(s: str, size: float = 120, color: str = WHITE, **kw) -> Text:
    """The one heavy number of a scene (Inter Black)."""
    return Text(s, font=FONT_HEAVY, weight=HEAVY, font_size=size, color=color, **kw)


def oldstyle(s: str, size: float = 30, color: str = INK, italic: bool = True, **kw) -> Text:
    """A small formula label in an old-style italic (EB Garamond): `oldstyle("S = k log W")`."""
    return Text(s, font=FONT_OLDSTYLE, slant=ITALIC if italic else "NORMAL", font_size=size, color=color, **kw)


def title_glyph(glyph: str, height: float = 3.6, color: str = WHITE) -> Text:
    """One huge bold Song/Ming character (about 45 % of the frame height by default)."""
    t = Text(glyph, font=FONT_CJK_SERIF, weight=BOLD, font_size=200, color=color)
    return t.scale_to_fit_height(height)


def title_card(glyph: str, word: str, sub: str | None = None, color: str = WHITE,
               word_color: str = INK, height: float = 3.4) -> VGroup:
    """Title: a huge glyph (or number) over a wide-tracked word over a tiny mono line."""
    g = title_glyph(glyph, height, color) if len(glyph) <= 2 else hero_number(glyph, 160, color)
    w = tracked(word, size=26, spacing=0.9, font=FONT_TRACKED, color=word_color)
    parts = [g, w]
    if sub:
        parts.append(tracked(sub, size=14, spacing=0.4, color=INK_DIM))
    out = VGroup(*parts).arrange(DOWN, buff=0.45)
    if sub:
        out[2].shift(UP * 0.15)
    return out


# ---------------------------------------------------------------- line art and ornaments

def hairline(m: VMobject, color: str = INK, width_px: float = 2.0, opacity: float = 1.0) -> VMobject:
    """Restyle as hairline line art: no fill, a `width_px` stroke at 1080p."""
    m.set_fill(opacity=0).set_stroke(color, width=stroke_px(width_px), opacity=opacity)
    return m


def brackets(m, size: float = 0.25, buff: float = 0.15, color: str = INK_DIM, width_px: float = 1.5) -> VGroup:
    """Four drafting corner brackets around a mobject."""
    x0, y0 = m.get_left()[0] - buff, m.get_bottom()[1] - buff
    x1, y1 = m.get_right()[0] + buff, m.get_top()[1] + buff
    g = VGroup()
    for (x, y, sx, sy) in ((x0, y1, 1, -1), (x1, y1, -1, -1), (x0, y0, 1, 1), (x1, y0, -1, 1)):
        p = np.array([x, y, 0])
        g.add(Line(p + RIGHT * sx * size, p), Line(p, p + UP * sy * size))
    return g.set_stroke(color, width=stroke_px(width_px))


def crosshair(point=ORIGIN, size: float = 0.18, color: str = INK_DIM, width_px: float = 1.2) -> VGroup:
    p = np.array(point, dtype=float)
    g = VGroup(Line(p + LEFT * size, p + RIGHT * size), Line(p + DOWN * size, p + UP * size))
    return g.set_stroke(color, width=stroke_px(width_px))


def faint_grid(spacing: float = 0.5, color: str = GRID_LINE, width: float | None = None,
               height: float | None = None) -> VGroup:
    """A faint square grid over the frame (a technical-drawing ground)."""
    w = width or config.frame_width + 2
    h = height or config.frame_height + 2
    g = VGroup()
    for x in np.arange(-w / 2, w / 2 + 1e-6, spacing):
        g.add(Line([x, -h / 2, 0], [x, h / 2, 0]))
    for y in np.arange(-h / 2, h / 2 + 1e-6, spacing):
        g.add(Line([-w / 2, y, 0], [w / 2, y, 0]))
    return g.set_stroke(color, width=stroke_px(1.0))


# ---------------------------------------------------------------- glow

def glow(m: VMobject, color: str | None = None, layers: int = 7, radius_px: float = 18, opacity: float = 0.5
         ) -> VGroup:
    """Stacked-stroke glow: `layers` copies of `m`'s outline, wider and fainter, to put under it.
    `radius_px` is how far the glow reaches at 1080p."""
    color = color or (m.get_stroke_color() if m.get_stroke_width() else m.get_fill_color())
    g = VGroup()
    full = stroke_px(2 * radius_px)
    for k in range(layers, 0, -1):
        c = m.copy().clear_updaters()
        c.set_fill(opacity=0).set_stroke(color, width=full * k / layers,
                                          opacity=opacity * (1 - k / (layers + 1)) ** 2)
        g.add(c)
    return g


def glowing(m: VMobject, color: str | None = None, **kw) -> VGroup:
    """VGroup(glow, m): animate the group so the glow follows the object."""
    return VGroup(glow(m, color, **kw), m)


def _rgb(color) -> np.ndarray:
    from manim import ManimColor
    return np.array(ManimColor(color).to_rgb(), dtype=float)


def halo(radius: float = 1.0, color: str = ACCENTS["cool"].mid, opacity: float = 0.6, sigma: float = 0.35,
         pixels: int = 160) -> ImageMobject:
    """A soft radial-gaussian light (an RGBA sprite) of `radius` units; put it under a glowing object."""
    y, x = np.mgrid[-1:1:pixels * 1j, -1:1:pixels * 1j]
    a = np.exp(-(x * x + y * y) / (2 * sigma ** 2))
    a[x * x + y * y > 1] = 0
    img = np.zeros((pixels, pixels, 4), np.uint8)
    img[..., :3] = (np.clip(_rgb(color), 0, 1) * 255).astype(np.uint8)
    img[..., 3] = (255 * a * opacity).astype(np.uint8)
    im = ImageMobject(img)
    im.set_resampling_algorithm(2)   # bilinear
    return im.scale_to_fit_width(2 * radius)


def light_dot(color: str = ACCENTS["cool"].core, radius: float = 0.05, halo_radius: float = 0.45,
              halo_color: str | None = None) -> Group:
    """A hot dot with a halo: a photon, a light pen's head."""
    from manim import Dot
    d = Dot(radius=radius, color=color)
    return Group(halo(halo_radius, halo_color or color, opacity=0.7, sigma=0.3), d)


class PenWrite(Animation):
    """Draw stroke art part by part (each part's share of the time is its share of the length) with a
    light dot riding the pen tip. The animated mobject is Group(m, pen): fade the pen out afterwards
    (`self.play(FadeOut(anim.pen))`); `m` stays."""

    def __init__(self, m: VMobject, pen: Group | None = None, **kw):
        self.pen = pen or light_dot()
        self.target = m
        kw.setdefault("rate_func", rate_functions.smooth)
        super().__init__(Group(m, self.pen), **kw)

    def begin(self):
        self.parts = self.target.family_members_with_points()
        lengths = np.array([max(1e-6, _path_length(p)) for p in self.parts])
        self.cum = np.concatenate([[0], np.cumsum(lengths)]) / lengths.sum()
        self.starts = [p.copy() for p in self.parts]
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        u = float(self.rate_func(alpha))
        tip = None
        for i, (part, start) in enumerate(zip(self.parts, self.starts)):
            a, b = self.cum[i], self.cum[i + 1]
            local = float(np.clip((u - a) / max(1e-9, b - a), 0, 1))
            part.pointwise_become_partial(start, 0, local)
            if a <= u <= b or (tip is None and i == len(self.parts) - 1):
                tip = start.point_from_proportion(local)
        if tip is not None:
            self.pen.move_to(tip)


def _path_length(m: VMobject, samples: int = 24) -> float:
    pts = np.array([m.point_from_proportion(t) for t in np.linspace(0, 1, samples)])
    return float(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum())


# ---------------------------------------------------------------- particles

class ParticleField(ImageMobject):
    """Thousands of glowing points, rendered as one image per frame: positions from a NumPy simulation
    (a function of time, or a precomputed array), splatted with an additive gaussian (core + glow)
    into an RGBA image. 20k particles cost a few tens of ms per frame.

        field = ParticleField(gas(2000, box=(-4, -2.5, 4, 2.5), start="left"), color=ACCENTS["cool"].core)
        self.add_field(field)               # (BeatScene) driven by the scene clock: smooth across plays
        self.wait_bars(4)
        field.set_speed(-1)                 # rewind: the simulation runs backwards from here

    positions: f(t) -> (N, 2 or 3) array in scene units, or an array (K, N, 2|3) sampled at `data_fps`.
    weights: per-particle brightness (N,), or f(t) -> (N,). colors: one colour or (N, 3) RGB in [0, 1].
    region: (x0, y0, x1, y1) covered by the image (default: the whole frame). resolution: image pixels
    per output pixel (0.5 is plenty: the glow is soft).
    """

    def __init__(self, positions, *, color=INK, colors=None, weights=None, size_px: float = 1.4,
                 glow_px: float = 6.0, glow_amount: float = 0.7, gain: float = 1.6, region=None,
                 resolution: float = 0.5, data_fps: float = 60.0, **kw):
        x0, y0, x1, y1 = region or (-config.frame_width / 2, -config.frame_height / 2,
                                    config.frame_width / 2, config.frame_height / 2)
        self.region = (float(x0), float(y0), float(x1), float(y1))
        ppu = config.pixel_height / config.frame_height * resolution
        self.res = (max(8, int(round((x1 - x0) * ppu))), max(8, int(round((y1 - y0) * ppu))))
        self.ppu = ppu
        self.positions = positions
        self.data_fps = data_fps
        self.weights = weights
        self.colors = None if colors is None else np.asarray(colors, dtype=float)
        self.color_rgb = _rgb(color)
        self.size_px = size_px * resolution * config.pixel_height / 1080
        self.glow_px = glow_px * resolution * config.pixel_height / 1080
        self.glow_amount = glow_amount
        self.gain = gain
        self.brightness = 1.0
        self._t_sim = 0.0          # simulation time at the last speed change
        self._t_clock = None       # clock time at the last speed change
        self.speed = 1.0
        self.clock = None
        w, h = self.res
        super().__init__(np.zeros((h, w, 4), np.uint8), **kw)
        self.set_resampling_algorithm(2)
        self.stretch_to_fit_width(x1 - x0)
        self.stretch_to_fit_height(y1 - y0)
        self.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        self.render_at(0.0)

    # --- time
    def follow(self, clock) -> "ParticleField":
        """Drive the simulation from `clock()` (scene seconds); BeatScene.add_field does this."""
        self.clock = clock
        self._t_clock = clock()
        self.add_updater(lambda m: m.render_at(m.sim_time()))
        return self

    def sim_time(self) -> float:
        if self.clock is None:
            return self._t_sim
        return self._t_sim + self.speed * (self.clock() - self._t_clock)

    def set_speed(self, speed: float) -> "ParticleField":
        """Change how fast simulated time runs (1 = real time, -1 = rewind, 0 = freeze), from now on."""
        if self.clock is not None:
            self._t_sim = self.sim_time()
            self._t_clock = self.clock()
        self.speed = float(speed)
        return self

    def jump_to(self, t_sim: float) -> "ParticleField":
        self._t_sim = float(t_sim)
        if self.clock is not None:
            self._t_clock = self.clock()
        return self

    # --- rendering
    def points_at(self, t: float) -> np.ndarray:
        p = self.positions
        if callable(p):
            return np.asarray(p(t), dtype=float)
        k = float(np.clip(t * self.data_fps, 0, len(p) - 1))
        i = int(math.floor(k))
        j = min(i + 1, len(p) - 1)
        f = k - i
        return np.asarray(p[i], dtype=float) * (1 - f) + np.asarray(p[j], dtype=float) * f

    def render_at(self, t: float) -> None:
        pts = self.points_at(t)
        wts = self.weights(t) if callable(self.weights) else self.weights
        self.pixel_array = splat(pts, self.region, self.res, weights=wts, colors=self.colors,
                                 color=self.color_rgb, size_px=self.size_px, glow_px=self.glow_px,
                                 glow_amount=self.glow_amount, gain=self.gain * self.brightness)


def splat(pts: np.ndarray, region, res, weights=None, colors=None, color=(1, 1, 1), size_px: float = 0.7,
          glow_px: float = 3.0, glow_amount: float = 0.7, gain: float = 1.6) -> np.ndarray:
    """Points -> RGBA uint8 image (h, w, 4): bilinear splat, gaussian core + glow, soft tone map."""
    from scipy.ndimage import gaussian_filter
    x0, y0, x1, y1 = region
    w, h = res
    out = np.zeros((h, w, 4), np.uint8)
    if pts is None or len(pts) == 0:
        return out
    u = (pts[:, 0] - x0) / (x1 - x0) * w - 0.5
    v = (y1 - pts[:, 1]) / (y1 - y0) * h - 0.5
    keep = (u > -2) & (u < w + 1) & (v > -2) & (v < h + 1)
    if weights is not None:
        weights = np.broadcast_to(np.asarray(weights, dtype=float), (len(pts),))[keep]
    if colors is not None:
        colors = np.asarray(colors, dtype=float)[keep]
    u, v = u[keep], v[keep]
    iu, iv = np.floor(u).astype(int), np.floor(v).astype(int)
    fu, fv = u - iu, v - iv
    base = np.ones(len(u)) if weights is None else weights
    chans = 1 if colors is None else 3
    acc = np.zeros((chans, h * w))
    for du, dv, wt in ((0, 0, (1 - fu) * (1 - fv)), (1, 0, fu * (1 - fv)), (0, 1, (1 - fu) * fv), (1, 1, fu * fv)):
        x, y = iu + du, iv + dv
        ok = (x >= 0) & (x < w) & (y >= 0) & (y < h)
        idx = (y * w + x)[ok]
        ww = (wt * base)[ok]
        if colors is None:
            acc[0] += np.bincount(idx, ww, h * w)
        else:
            for c in range(3):
                acc[c] += np.bincount(idx, ww * colors[ok, c], h * w)
    acc = acc.reshape(chans, h, w).astype(np.float32)
    core = np.stack([gaussian_filter(a, size_px, truncate=3.0) for a in acc]) * np.float32(
        (2 * np.pi * size_px ** 2) ** 0.5)
    soft = np.stack([gaussian_filter(a, glow_px, truncate=3.0) for a in acc]) * np.float32(
        (2 * np.pi * glow_px ** 2) ** 0.5)
    inten = core + np.float32(glow_amount) * soft
    if colors is None:                   # one colour: tone map through a lookup table (fast)
        v = 1.0 - np.exp(np.float32(-gain) * inten[0])
        return _tone_lut(tuple(np.round(np.asarray(color, dtype=float), 4)))[(v * 1023).astype(np.int32)]
    rgb = np.moveaxis(inten, 0, -1)                     # (h, w, 3) float32
    np.multiply(rgb, np.float32(-gain), out=rgb)
    np.exp(rgb, out=rgb)
    np.subtract(np.float32(1.0), rgb, out=rgb)
    alpha = rgb.max(axis=2)
    np.multiply(rgb, np.float32(255.0) / np.maximum(alpha, np.float32(1e-4))[..., None], out=rgb)
    out[..., :3] = np.minimum(rgb, 255).astype(np.uint8)
    out[..., 3] = (alpha * 255).astype(np.uint8)
    return out


@lru_cache(maxsize=32)
def _tone_lut(color: tuple) -> np.ndarray:
    """RGBA for each level v = 1 - exp(-gain * I) of one colour: channel c saturates as 1 - (1 - v) ** c,
    so bright cores turn white-hot while the faint glow keeps the hue."""
    v = np.linspace(0, 1, 1024)[:, None]
    c = np.clip(np.asarray(color, dtype=float), 1e-3, 1)[None, :]
    rgb = 1.0 - (1.0 - v) ** c             # = 1 - exp(-gain * I * c): the same curve as the colour path
    alpha = rgb.max(axis=1)
    lut = np.zeros((1024, 4), np.uint8)
    lut[:, :3] = np.clip(rgb / np.maximum(alpha[:, None], 1e-4) * 255, 0, 255).astype(np.uint8)
    lut[:, 3] = np.clip(alpha * 255, 0, 255).astype(np.uint8)
    return lut


# --- simulations: each returns positions(t) -> (N, 2), closed form, so any t (and rewinds) is exact

def _reflect(x, lo, hi):
    span = hi - lo
    y = np.mod(x - lo, 2 * span)
    return lo + np.where(y > span, 2 * span - y, y)


def gas(n: int, box=(-4.0, -2.5, 4.0, 2.5), seed: int = 0, speed: float = 1.2, start=None):
    """An ideal gas in a box: free flight with elastic walls. `start`: "left" bunches every particle
    in the left half at t = 0 (the reference's ordered state), or a (x0, y0, x1, y1) box."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    if start == "left":
        sx0, sy0, sx1, sy1 = x0, y0, (x0 + x1) / 2, y1
    elif start is None:
        sx0, sy0, sx1, sy1 = box
    else:
        sx0, sy0, sx1, sy1 = start
    p0 = np.column_stack([rng.uniform(sx0, sx1, n), rng.uniform(sy0, sy1, n)])
    ang = rng.uniform(0, 2 * np.pi, n)
    sp = speed * np.sqrt(rng.chisquare(2, n) / 2)
    vel = np.column_stack([np.cos(ang), np.sin(ang)]) * sp[:, None]

    def positions(t):
        p = p0 + vel * t
        return np.column_stack([_reflect(p[:, 0], x0, x1), _reflect(p[:, 1], y0, y1)])
    return positions


def drift(n: int, region=None, seed: int = 0, speed: float = 0.06, wobble: float = 0.15):
    """Slow ambient dust: each point drifts and wobbles, wrapping around the region."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = region or (-config.frame_width / 2 - 0.5, -config.frame_height / 2 - 0.5,
                                config.frame_width / 2 + 0.5, config.frame_height / 2 + 0.5)
    p0 = np.column_stack([rng.uniform(x0, x1, n), rng.uniform(y0, y1, n)])
    v = rng.normal(0, speed, (n, 2))
    f = rng.uniform(0.05, 0.25, (n, 2))
    ph = rng.uniform(0, 2 * np.pi, (n, 2))

    def positions(t):
        p = p0 + v * t + wobble * np.sin(2 * np.pi * f * t + ph)
        return np.column_stack([x0 + np.mod(p[:, 0] - x0, x1 - x0), y0 + np.mod(p[:, 1] - y0, y1 - y0)])
    return positions


def dissolve(points: np.ndarray, seed: int = 0, spread: float = 1.2, power: float = 1.5, jitter: float = 0.02):
    """Points that start on a shape (sample_points) and diffuse outward: a glyph turning to dust."""
    rng = np.random.default_rng(seed)
    p0 = np.asarray(points, dtype=float)[:, :2] + rng.normal(0, jitter, (len(points), 2))
    vel = rng.normal(0, 1, (len(points), 2)) * spread

    def positions(t):
        return p0 + vel * max(0.0, t) ** power
    return positions


def gather(points: np.ndarray, duration: float, seed: int = 0, spread: float = 1.2, power: float = 1.5):
    """The reverse of dissolve: scattered points that land on the shape at t = duration."""
    d = dissolve(points, seed, spread, power)

    def positions(t):
        return d(max(0.0, duration - t))
    return positions


def sample_points(m, n: int, seed: int = 0) -> np.ndarray:
    """`n` points spread along the outlines of a mobject (by path length), as an (n, 3) array."""
    rng = np.random.default_rng(seed)
    parts = [p for p in m.family_members_with_points() if len(p.points)]
    lengths = np.array([max(1e-6, _path_length(p)) for p in parts])
    which = rng.choice(len(parts), size=n, p=lengths / lengths.sum())
    ts = rng.random(n)
    return np.array([parts[i].point_from_proportion(float(t)) for i, t in zip(which, ts)])


# ---------------------------------------------------------------- rolling-digit counters

class RollingCounter(VGroup):
    """An odometer number: each digit is a column of glyphs that rolls (soft fade above and below, no
    occluders), so a count reads as motion. Laid out for `digits` columns (leading zeros hidden).

        n = RollingCounter(0, digits=6).to_edge(RIGHT)
        self.play(FadeIn(n))
        self.play(n.roll_to(255168), bars=4)     # every digit rolls like an odometer
        self.play(n.land(362880), beats=4)       # scramble, then settle left to right
    """

    def __init__(self, value: float = 0, digits: int = 6, group: str = ",", font: str = FONT_HEAVY,
                 weight=HEAVY, size: float = 96, color: str = WHITE, leading_zeros: bool = False, **kw):
        super().__init__(**kw)
        self.leading_zeros = leading_zeros
        templates = [Text(str(d), font=font, weight=weight, font_size=size, color=color) for d in range(10)]
        self.cell_w = max(t.width for t in templates) * 1.04
        self.cell_h = max(t.height for t in templates) * 1.35
        self.columns: list[VGroup] = []
        self.separators: list[tuple[int, VMobject]] = []
        x = 0.0
        items = []
        for k in reversed(range(digits)):           # k = power of ten, leftmost first
            col = VGroup(*[t.copy() for t in templates], templates[0].copy())   # 0..9 and a wrap-around 0
            col.x, col.k = x + self.cell_w / 2, k
            self.columns.append(col)
            items.append(col)
            x += self.cell_w
            if group and k > 0 and k % 3 == 0:
                sep = Text(group, font=font, weight=weight, font_size=size, color=color)
                sep.x = x + self.cell_w * 0.12
                self.separators.append((k, sep))
                items.append(sep)
                x += self.cell_w * 0.4
        self.total_w = x
        self.ref = Rectangle(width=x, height=self.cell_h * 0.8).set_stroke(width=0).set_fill(opacity=0)
        self.add(self.ref, *items)
        self.value = ValueTracker(value)
        self.manual: list[float] | None = None       # per-column positions while landing
        self.manual_top = 0.0                         # the largest value shown while landing
        self.layout()
        self.add_updater(lambda m: m.layout())

    def digit_positions(self, v: float) -> list[float]:
        """Roll position of each column: 3.0 shows "3", 3.5 is half way to "4" (odometer carries)."""
        v = max(0.0, float(v))
        out = []
        for col in self.columns:
            k = col.k
            if k == 0:
                p = v % 10.0
            else:
                r = v % (10.0 ** k)
                p = math.floor(v / 10.0 ** k) % 10 + max(0.0, r - (10.0 ** k - 1))
            out.append(p)
        return out

    def layout(self) -> None:
        v = self.value.get_value()
        ps = self.manual if self.manual is not None else self.digit_positions(v)
        s = self.ref.width / self.total_w
        left, cy = self.ref.get_left()[0], self.ref.get_center()[1]
        top = max(1.0, v if self.manual is None else self.manual_top)
        for col, p in zip(self.columns, ps):
            show = self.leading_zeros or col.k == 0 or top >= 10 ** col.k
            q = p % 10.0
            for j, g in enumerate(col):
                dy = (j - q) * self.cell_h             # glyph 10 is the "0" that follows 9
                vis = max(0.0, 1.0 - abs(dy) / (self.cell_h * 0.75)) ** 2 if show else 0.0
                g.move_to([left + col.x * s, cy - (dy if vis > 0 else 0.0) * s, 0])
                g.set_opacity(vis)
        for k, sep in self.separators:
            sep.move_to([left + sep.x * s, cy - self.cell_h * 0.3 * s, 0])
            sep.set_opacity(1.0 if (self.leading_zeros or top >= 10 ** k) else 0.0)

    def __deepcopy__(self, memo):
        """Copies are static (also inside a copied group): animations copy their mobject (FadeOut's
        target), and a copy that kept the layout updater would undo the fade every frame."""
        c = super().__deepcopy__(memo)
        c.updaters = []
        return c

    def roll_to(self, value: float, **kw) -> Animation:
        return CounterRoll(self, value, **kw)

    def land(self, value: int, spins: int = 2, lag: float = 0.12, **kw) -> Animation:
        return CounterLand(self, value, spins=spins, lag=lag, **kw)


class CounterRoll(Animation):
    """Roll a RollingCounter to a value (all digits move like an odometer)."""

    def __init__(self, counter: RollingCounter, value: float, rate_func=rate_functions.ease_in_out_cubic, **kw):
        self.counter, self.target, self.start = counter, float(value), None
        super().__init__(counter, rate_func=rate_func, **kw)

    def begin(self):
        self.start = self.counter.value.get_value()
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        self.counter.value.set_value(self.start + (self.target - self.start) * alpha)
        self.counter.layout()

    def event_info(self) -> dict:
        return {"from": self.start, "to": self.target}


class CounterLand(Animation):
    """Scramble every digit, then settle them left to right on `value` (a slot machine)."""

    def __init__(self, counter: RollingCounter, value: int, spins: int = 2, lag: float = 0.12, **kw):
        self.counter, self.target, self.spins, self.lag = counter, int(value), spins, lag
        kw.setdefault("rate_func", linear)
        super().__init__(counter, **kw)

    def begin(self):
        self.p0 = self.counter.digit_positions(self.counter.value.get_value())
        self.p1 = self.counter.digit_positions(self.target)
        self.counter.manual_top = max(self.counter.value.get_value(), self.target)
        self.counter.manual = list(self.p0)
        self.lag_ = min(self.lag, 0.6 / max(1, len(self.p0) - 1))
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        n = len(self.p0)
        span = max(1e-6, 1 - self.lag_ * (n - 1))
        ps = []
        for i, (a, b) in enumerate(zip(self.p0, self.p1)):
            u = float(np.clip((alpha - self.lag_ * i) / span, 0, 1))
            u = 1 - (1 - u) ** 3                      # ease out: fast spin, long settle
            end = b + 10 * (self.spins + i % 2) + (10 if b < a else 0)
            ps.append(a + (end - a) * u)
        self.counter.manual = ps
        self.counter.layout()

    def finish(self):
        super().finish()
        self.counter.manual = None
        self.counter.value.set_value(self.target)
        self.counter.layout()

    def event_info(self) -> dict:
        """When each digit settles, as fractions of the run time (left to right): one note each."""
        n = len(getattr(self, "p0", [])) or 1
        lag = getattr(self, "lag_", self.lag)
        span = max(1e-6, 1 - lag * (n - 1))
        # ease-out cubic reaches 95 % of its travel at u = 1 - 0.05 ** (1 / 3) ~ 0.63
        lands = [min(1.0, lag * i + span * 0.63) for i in range(n)]
        if self.rate_func is not linear:
            from .events import _alpha_at
            lands = [_alpha_at(self.rate_func, u) for u in lands]
        return {"to": self.target, "lands": lands}


# ---------------------------------------------------------------- camera that keeps a HUD still

def sound_tag(m) -> str | None:
    """The sound tag of a mobject (`m.sound = "X"` or "X@C#5"), or of the first part of it that has one."""
    for x in m.get_family():
        snd = x.__dict__.get("sound")
        if snd is not None:
            return str(snd)
    return None


class HUDCamera(MovingCamera):
    """A MovingCamera that draws `fixed_mobjects` in screen space, on top: HUD labels, figure numbers
    and counters stay put while the camera pans and zooms. (Fixed mobjects must be top-level scene
    mobjects: BeatScene.fix adds them.)"""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.fixed_mobjects: list = []
        self._screen = Rectangle(width=config.frame_width, height=config.frame_height).set_stroke(width=0)

    def capture_mobjects(self, mobjects, **kwargs):
        if not self.fixed_mobjects:
            return super().capture_mobjects(mobjects, **kwargs)
        fixed = {id(x) for m in self.fixed_mobjects for x in m.get_family()}
        mobjects = list(mobjects)
        moving = [m for m in mobjects if id(m) not in fixed]
        still = [m for m in mobjects if id(m) in fixed]
        super().capture_mobjects(moving, **kwargs)
        if still:
            frame, self.frame = self.frame, self._screen
            try:
                super().capture_mobjects(still, **kwargs)
            finally:
                self.frame = frame


# ---------------------------------------------------------------- the scene

class BeatScene(EventLog, MovingCameraScene):
    """A short-format scene: a MovingCameraScene on a beat grid that logs its events and captions.

    Grid (video.yaml `tempo:`, default 100 BPM; bar = 4 beats):
        self.play(anim, beats=2)        start on the next beat, last 2 beats
        self.play(anim, bars=1)         start on the next bar line, last 1 bar
        self.play(anim, run_time=0.9)   start now; any run time (whole frames)
        self.on_bar() / self.on_beat()  wait to the next bar line / beat (nothing if already on one)
        self.wait_beats(n), self.wait_bars(n), self.until("3:2")
        self.count(mobs, every="eighth", anim=FadeIn)   one item per subdivision, logged as a count
        self.now, self.beat, self.bar, self.grid.label(self.now) -> "3:2"
    Captions (captions.yaml, see explainer.captions): self.caption("id") / self.caption(zh=..., en=...)
    Marks for the music: self.mark("hit"), self.play(..., kind="reveal", sound="glass")
    HUD: self.fig(3, "TIME DILATION", "时间变慢"), self.hud(text, corner=UR), self.fix(mobject)
    Camera: self.zoom_to(target, width=...), self.camera_home(), self.drift(velocity), self.stop_drift()
    Particles: self.add_field(ParticleField(...))

    The scene ends on a bar line: tear_down pads with a (moving) hold to the next bar.
    """

    bpm: float | None = None           # None: video.yaml `tempo` (or music.bpm), else 100
    beats_per_bar: int = 4
    background: str = BG
    end_on_bar: bool = True
    captions_key: str | None = None    # captions.yaml key; default: the scene file stem, then class name

    def __init__(self, **kwargs):
        config.background_color = self.background
        kwargs.setdefault("camera_class", HUDCamera)
        super().__init__(**kwargs)

    # ------------------------------------------------------------- setup
    def setup(self):
        super().setup()
        spec = project_spec()
        bpm = (self.bpm or spec.get("tempo") or (spec.get("grid") or {}).get("bpm")
               or (spec.get("music") or {}).get("bpm") or 100)
        self.grid = Grid(float(bpm), int(self.beats_per_bar))
        self._drift = None
        self._caps: list[cap.Caption] = []
        self._pool: list[cap.Caption] = []
        try:
            stem = Path(inspect.getfile(type(self))).stem
        except (TypeError, OSError):          # a module loaded without sys.modules (explainer.check)
            stem = type(self).__module__.rsplit(".", 1)[-1] or None
        self.scene_stem = stem
        project = _project()
        if project is not None:
            table = cap.load(cap.project_file(project, spec))
            self._pool = cap.for_scene(table, *(k for k in (self.captions_key, stem, type(self).__name__) if k))
        for c in self._pool:
            if c.at is not None:
                c.t = self.grid.time(c.at)
                c.dur = cap.duration(c, self.grid)
                c.placed = "yaml"
                self._caps.append(c)

    # ------------------------------------------------------------- clock and grid
    @property
    def fps(self) -> float:
        return float(self.camera.frame_rate)

    @property
    def frame_index(self) -> int:
        return int(round(self.renderer.time * self.fps))

    @property
    def now(self) -> float:
        """Scene time, exact to the frame."""
        return self.frame_index / self.fps

    def clock(self) -> float:
        """The time of the frame being drawn (use in updaters; smooth across play() calls)."""
        return float(self.renderer.time)

    @property
    def beat(self) -> float:
        return self.grid.beat

    @property
    def bar(self) -> float:
        return self.grid.bar

    def event_grid(self) -> dict:
        return {"bpm": self.grid.bpm, "beat": self.grid.beat, "beats_per_bar": self.grid.beats_per_bar,
                "bar": self.grid.bar, "offset": 0.0}

    def event_extras(self) -> dict:
        return {"format": "short", "scene_file": self.scene_stem,
                "captions": [c.as_dict() for c in sorted(self._caps, key=lambda c: c.t or 0.0)]}

    # ------------------------------------------------------------- play and wait on the grid
    def play(self, *animations, beats: float | None = None, bars: float | None = None, on: str | None = None,
             **kwargs):
        if on is None and (beats is not None or bars is not None):
            on = "bar" if (bars is not None and beats is None) else "beat"
        if on:
            self.wait_to(on)
        length = None
        if beats is not None or bars is not None:
            length = (bars or 0) * self.grid.bar + (beats or 0) * self.grid.beat
        elif kwargs.get("run_time") is not None:
            length = float(kwargs["run_time"])
        if length is not None:
            kwargs["run_time"] = play_time(max(1, frames(length, self.fps)), self.fps)
        return super().play(*animations, **kwargs)

    def get_moving_and_static_mobjects(self, animations):
        """Fixed (HUD) mobjects are redrawn every frame, so they stay on top of moving content."""
        moving, static = super().get_moving_and_static_mobjects(animations)
        fixed = getattr(self.camera, "fixed_mobjects", None)
        if fixed:
            ids = {id(x) for m in fixed for x in m.get_family()}
            lift = [m for m in static if id(m) in ids]
            if lift:
                static = [m for m in static if id(m) not in ids]
                moving = list(moving) + lift
        return moving, static

    def _moving(self) -> bool:
        return bool(self.always_update_mobjects or self.updaters or any(
            m.updaters for m in self.get_mobject_family_members()))

    def wait(self, duration: float | None = None, stop_condition=None, frozen_frame=None, *,
             beats: float | None = None, bars: float | None = None):
        """Wait `duration` seconds (default: one beat), or `beats` / `bars`; whole frames, and the
        picture keeps moving if anything has an updater."""
        if beats is not None or bars is not None:
            duration = (bars or 0) * self.grid.bar + (beats or 0) * self.grid.beat
        if duration is None:
            duration = self.grid.beat
        if stop_condition is not None:
            return super().wait(duration, stop_condition=stop_condition, frozen_frame=frozen_frame)
        n = frames(duration, self.fps)
        if n <= 0:
            return None
        frozen = (not self._moving()) if frozen_frame is None else bool(frozen_frame)
        d = hold_time(n, self.fps) if frozen else play_time(n, self.fps)
        return super().wait(d, frozen_frame=frozen)

    def wait_to(self, unit: str = "bar") -> None:
        """Wait to the next grid point of `unit` ("bar", "beat", "eighth", "sixteenth", ...: note names,
        a beat being a quarter note); no-op if on one."""
        t = self.now
        target = self.grid.snap(t, unit, "up", tol=0.5 / self.fps)
        if target - t > 0.5 / self.fps:
            self.wait(target - t)

    def on_bar(self) -> None:
        self.wait_to("bar")

    def on_beat(self) -> None:
        self.wait_to("beat")

    def wait_beats(self, n: float = 1) -> None:
        self.wait(n * self.grid.beat)

    def wait_bars(self, n: float = 1) -> None:
        self.wait(n * self.grid.bar)

    def until(self, pos) -> None:
        """Wait until a grid position of this scene ("3:2" = bar 3, beat 2, from 0; or "7.2s")."""
        target = self.grid.time(pos)
        if target < self.now - 0.5 / self.fps:
            logger.warning(f"{type(self).__name__}: until({pos!r}) is {self.now - target:.2f}s in the past")
            return
        if target - self.now > 0.5 / self.fps:
            self.wait(target - self.now)

    def count(self, mobjects, every="eighth", each: float | None = None, anim=FadeIn, on: str | None = "beat",
              kind: str = "count", sound: str | None = None, pitch: str = "rise", **anim_kw):
        """Reveal `mobjects` one per subdivision (`every`: a grid unit such as "eighth" or "sixteenth", or
        seconds), logged as a count so the music gives each one its own note:
        self.count(cards, every="eighth").

        Each item sounds as its own `.sound` tag says (`m.sound = "X"`, or `"X@C#5"` for a fixed note,
        or `"@C#5"` for the count's instrument at that note); `sound=` is the tag of items that have
        none; else video.yaml music.sounds/palette `count`, else the palette's count instrument. Notes
        without a fixed pitch climb through the chord (`pitch="flat"`: they repeat one note)."""
        mobjects = list(mobjects)
        if not mobjects:
            return
        step = self.grid.unit(every) if isinstance(every, str) else float(every)
        each = each if each is not None else max(0.3, 2 * step)
        if on:
            self.wait_to(on)
        n = len(mobjects)
        total = (n - 1) * step + each
        t0 = self.now
        data = {"n": n, "every": step, "pitch": pitch, "times": [round(t0 + i * step, 4) for i in range(n)],
                "xs": [round(float(m.get_center()[0]), 2) for m in mobjects]}
        tags = [sound_tag(m) for m in mobjects]
        if any(t is not None for t in tags):
            data["sounds"] = tags
        if sound:
            data["sound"] = sound
        self.mark(kind, **data)
        anims = [anim(m, run_time=each, **anim_kw) for m in mobjects]
        group = LaggedStart(*anims, lag_ratio=step / each if each > 0 else 1.0)
        self.play(group, run_time=total, sound=sound)

    # ------------------------------------------------------------- captions
    def caption(self, id: str | None = None, *, zh: str | None = None, en: str | None = None,
                beats: float | None = None, dur: float | None = None, at=None) -> cap.Caption:
        """Show a caption now (or at grid position `at`): a captions.yaml line by id, the next line not
        yet shown (no id), or inline text. Captions are drawn into the picture at stitch time."""
        c = None
        if zh is None and en is None:
            pool = [x for x in self._pool if x.placed != "yaml" and x not in self._caps]
            if id is not None:
                c = next((x for x in self._pool if x.id == id), None)
                if c is None:
                    raise KeyError(f"no caption {id!r} for scene {self.scene_stem or type(self).__name__} "
                                   f"in captions.yaml")
                if c in self._caps:
                    self._caps.remove(c)
            elif pool:
                c = pool[0]
            else:
                raise KeyError(f"{type(self).__name__}: no captions left in captions.yaml to place")
        else:
            c = cap.Caption(zh=zh or "", en=en or "", id=id, scene=self.scene_stem)
        c.t = self.grid.time(at) if at is not None else self.now
        if beats is not None:
            c.beats, c.dur, c.fixed = beats, None, True
        if dur is not None:
            c.dur, c.fixed = dur, True
        if not c.fixed:
            c.dur = None
        c.dur = cap.duration(c, self.grid)
        c.placed = "code"
        self._caps.append(c)
        self.events.append({"type": "caption", "t": round(c.t, 4), "dur": round(c.dur, 4),
                            **({"id": c.id} if c.id else {})})
        return c

    # ------------------------------------------------------------- HUD (screen space)
    def fix(self, *mobjects):
        """Pin mobjects to the screen: they ignore camera moves (HUD, figure labels, counters)."""
        for m in mobjects:
            if m not in self.camera.fixed_mobjects:
                self.camera.fixed_mobjects.append(m)
        self.add(*mobjects)
        return mobjects[0] if len(mobjects) == 1 else mobjects

    def unfix(self, *mobjects):
        for m in mobjects:
            if m in self.camera.fixed_mobjects:
                self.camera.fixed_mobjects.remove(m)

    def hud(self, text: str, corner=UR, size: float = 12, color: str = INK_DIM, add: bool = True,
            buff: float = 0.55) -> MarkupText:
        """A tiny letter-spaced readout in a corner ("TICK 007", "β = 0.30"), fixed in the frame. Returns
        the mobject without adding it when add=False (to animate it in, then self.fix it)."""
        t = tracked(text, size=size, spacing=0.25, color=color, font=FONT_MONO, upper=False)   # (CJK: fallback)
        t.to_corner(corner, buff=buff)
        if add:
            self.fix(t)
        return t

    def fig(self, n: int | str, en: str, zh: str | None = None, add: bool = True) -> MarkupText:
        """The section label of the reference style, top left: "FIG. 03  GHOST GAMES · 幽灵对局"."""
        num = f"{int(n):02d}" if isinstance(n, int) or str(n).isdigit() else str(n)
        s = f"FIG. {num}   {en.upper()}" + (f"  ·  {zh}" if zh else "")
        return self.hud(s, corner=UL, add=add)

    # ------------------------------------------------------------- camera
    @property
    def frame(self):
        return self.camera.frame

    def zoom_to(self, target=None, width: float | None = None, scale: float | None = None):
        """An animation of the camera frame: `self.play(self.zoom_to(cup, width=1), beats=4,
        rate_func=rate_functions.ease_in_expo)` (zoom-through), `self.zoom_to(scale=3)` (pull out)."""
        a = self.camera.frame.animate
        if scale is not None:
            a = a.scale(scale)
        if width is not None:
            a = a.set(width=width)
        if target is not None:
            a = a.move_to(target.get_center() if hasattr(target, "get_center") else target)
        return a

    def camera_home(self):
        """An animation back to the default frame (centre, full width)."""
        return self.camera.frame.animate.set(width=config.frame_width).move_to(ORIGIN)

    def drift(self, velocity=(0.04, 0.0), zoom: float = 0.0):
        """A slow camera drift (units/s, and a zoom rate: 0.01 = 1 %/s wider), from now until
        stop_drift(): keeps a hold alive."""
        self.stop_drift()
        frame = self.camera.frame
        c0, w0, t0 = frame.get_center().copy(), frame.width, self.clock()
        v = np.array([velocity[0], velocity[1], 0.0])

        def upd(m):
            dt = self.clock() - t0
            m.set(width=w0 * math.exp(zoom * dt))
            m.move_to(c0 + v * dt)
        self._drift = upd
        frame.add_updater(upd)
        if frame not in self.mobjects:
            self.add(frame)

    def stop_drift(self):
        if self._drift is not None:
            self.camera.frame.remove_updater(self._drift)
            self._drift = None

    # ------------------------------------------------------------- particles
    def add_field(self, field: ParticleField, front: bool = False) -> ParticleField:
        """Add a particle field driven by the scene clock (smooth across plays and waits)."""
        field.follow(self.clock)
        pts = field.points_at(field.sim_time())
        self.mark("particles", n=int(len(pts)), x=round(float(np.mean(pts[:, 0])), 2) if len(pts) else 0.0)
        if front:
            self.add(field)
        else:
            self.add(field)
            self.bring_to_back(field)
        return field

    # ------------------------------------------------------------- end on a bar line
    def tear_down(self):
        if self.end_on_bar:
            t = self.now
            target = self.grid.snap(t, "bar", "up", tol=0.5 / self.fps)
            if target - t > 0.5 / self.fps:
                self.mark("pad")
                self.wait(target - t)
        left = [c for c in self._pool if c not in self._caps]
        for c in left:
            logger.warning(f"{type(self).__name__}: caption never shown: {c.id or c.zh[:20]!r}")
        super().tear_down()


__all__ = [
    # palette and type
    "BG", "INK", "INK_DIM", "INK_FAINT", "GRID_LINE", "RED", "WHITE", "Accent", "ACCENTS", "FONT_CJK_SERIF",
    "FONT_TRACKED", "FONT_HEAVY", "FONT_OLDSTYLE", "FONT_MONO", "px", "stroke_px", "tracked", "cjk",
    "hero_number", "oldstyle", "title_glyph", "title_card", "letter_spacing_units",
    # line art, glow, light
    "hairline", "brackets", "crosshair", "faint_grid", "glow", "glowing", "halo", "light_dot", "PenWrite",
    # particles
    "ParticleField", "splat", "gas", "drift", "dissolve", "gather", "sample_points",
    # counters
    "RollingCounter", "CounterRoll", "CounterLand",
    # the scene
    "BeatScene", "HUDCamera", "Grid", "project_spec", "np",
]
