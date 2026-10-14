"""speciesOT E4 · scGen as arithmetic, behind one adapter — Swiss scenes.

Narration and budgets come from the plan (script.json). Josh's code on screen comes from
videos/speciesot-series/excerpts.py (real line numbers; a long line may be elided with "…",
never rewritten). Repo paths and line numbers shown on screen were checked against the
speciesOT repo at 109bf12. The latent space is a 2-D cartoon of a 50-D code and says so.
Diagrams here: a cell as a stripe bar, the autoencoder squeeze, latent mean crosses and the
δ arrow, held-out cells shifted, one arrow failing a second cell type, three things called
scgen, and the package boundary with one door.
"""
import sys
from pathlib import Path

import numpy as np

SERIES = Path(__file__).resolve().parent.parent / "speciesot-series"
sys.path.insert(0, str(SERIES))

from manim import *  # noqa: E402,F401,F403
from speciesot_kit import *  # noqa: E402,F401,F403
from excerpts import CORE, CONFIG, rows  # noqa: E402

CORE_PATH = "src/speciesot/speciesot_core.py"
CONFIG_PATH = "Tests/config.yaml"
SKETCH = "2-D sketch · really 50-D"


class Ep(EpisodeScene):
    episode = "E4"
    total = "07"


# ---------------------------------------------------------------- episode parts

RNG = np.random.default_rng(4)
N_GENES = 14
MOUSE_MEAN = np.clip(RNG.uniform(.12, .85, N_GENES), .05, .95)
HUMAN_MEAN = np.clip(MOUSE_MEAN + RNG.choice([-.38, .38, .0, .3, -.3], N_GENES), .06, .94)
NOISE = RNG.normal(0, .07, N_GENES)
MOUSE_CELL = np.clip(MOUSE_MEAN + NOISE, .05, .95)
PRED_CELL = np.clip(HUMAN_MEAN + NOISE, .05, .95)


def gene_bar(x, y, values, w=.46, h=2.3, color=INK, outline=INK, stroke=2):
    """A cell as a vertical bar of genes: each stripe is one flat shade (= expression)."""
    n = len(values)
    sh = h / n
    stripes = VGroup(*[Rectangle(width=w, height=sh, stroke_width=0, fill_color=color,
                                 fill_opacity=float(v))
                       .move_to([x, y + h / 2 - sh * (i + .5), 0]) for i, v in enumerate(values)])
    frame = Rectangle(width=w, height=h, stroke_color=outline, stroke_width=stroke)\
        .move_to([x, y, 0])
    g = VGroup(stripes, frame)
    g.stripes, g.frame = stripes, frame
    return g


def restripe(bar, values, color=None):
    """Animations that change a bar's stripe shades (and optionally colour) in place."""
    return [s.animate.set_fill(color or s.get_fill_color(), opacity=float(v))
            for s, v in zip(bar.stripes, values)]


def op(s, x, y, size=44, color=INK):
    return Text(s, font=LATIN, font_size=size, color=color).move_to([x, y, 0])


def trapezoid(x0, x1, h0, h1, y=0, color=INK, dashed=False):
    """Encoder (h0 > h1) or decoder (h0 < h1): a flat four-sided funnel."""
    p = Polygon([x0, y + h0 / 2, 0], [x1, y + h1 / 2, 0], [x1, y - h1 / 2, 0],
                [x0, y - h0 / 2, 0], stroke_color=color, stroke_width=2, fill_color=PAPER,
                fill_opacity=1)
    return DashedVMobject(p, num_dashes=40) if dashed else p


def code_column(x, y, n=5, w=.34, h=1.0, color=INK, values=None):
    values = values if values is not None else [.25, .7, .45, .85, .35][:n]
    sh = h / n
    cells = VGroup(*[Rectangle(width=w, height=sh, stroke_color=color, stroke_width=1.5,
                               fill_color=color, fill_opacity=float(v))
                     .move_to([x, y + h / 2 - sh * (i + .5), 0]) for i, v in enumerate(values)])
    return cells


def mini_ae(x, y, scale=1.0, color=INK, dashed=False):
    """A small autoencoder icon: funnel in, code, funnel out."""
    s = scale
    enc = trapezoid(x - .95 * s, x - .2 * s, .9 * s, .34 * s, y, color, dashed)
    code = Rectangle(width=.22 * s, height=.34 * s, stroke_color=color, stroke_width=2,
                     fill_color=color, fill_opacity=0 if dashed else .55).move_to([x, y, 0])
    if dashed:
        code = DashedVMobject(code, num_dashes=8)
    dec = trapezoid(x + .2 * s, x + .95 * s, .34 * s, .9 * s, y, color, dashed)
    return VGroup(enc, code, dec)


def hollow(n, cx, cy, spread=.22, color=INK, seed=0, radius=.06):
    """A held-out cell type: hollow dots."""
    rng = np.random.default_rng(seed)
    pts = rng.normal(0, spread, size=(n, 2))
    return VGroup(*[Circle(radius=radius, stroke_color=color, stroke_width=2)
                    .move_to([cx + px, cy + py, 0]) for px, py in pts])


def squares(n, cx, cy, spread=.2, color=GRAY, seed=0, side=.1):
    """A second cell type: small hollow squares."""
    rng = np.random.default_rng(seed)
    pts = rng.normal(0, spread, size=(n, 2))
    return VGroup(*[Square(side_length=side, stroke_color=color, stroke_width=2)
                    .move_to([cx + px, cy + py, 0]) for px, py in pts])


def cross(x, y, color=INK, r=.17, stroke=4):
    return VGroup(Line([x - r, y - r, 0], [x + r, y + r, 0], color=color, stroke_width=stroke),
                  Line([x - r, y + r, 0], [x + r, y - r, 0], color=color, stroke_width=stroke))


def delta_arrow(a, b, color=RED, stroke=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=stroke,
                 max_tip_length_to_length_ratio=.14, max_stroke_width_to_length_ratio=12)


def badge(n, x, y, color=RED):
    c = Circle(radius=.2, stroke_width=0, fill_color=color, fill_opacity=1).move_to([x, y, 0])
    return VGroup(c, Text(str(n), font=LATIN, font_size=20, color=PAPER, weight=BOLD)
                  .move_to(c.get_center()))


def dashed_box(x, y, w, h, color=INK, n=70, stroke=2):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=stroke).move_to([x, y, 0])
    return DashedVMobject(r, num_dashes=n)


def path_folder(x0, y, w, h, dashed=False, color=INK):
    """A folder outline (tab + body), left edge at x0, centred on y."""
    body = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2)\
        .move_to([x0 + w / 2, y, 0])
    tab = Rectangle(width=min(1.2, w * .3), height=.14, stroke_color=color, stroke_width=2)
    tab.move_to([x0 + tab.width / 2, y + h / 2 + .07, 0])
    if dashed:
        return VGroup(DashedVMobject(tab, num_dashes=12), DashedVMobject(body, num_dashes=80))
    return VGroup(tab, body)


# ---------------------------------------------------------------- scenes


class S01(Ep):
    def construct(self):
        self.header()
        y0 = .45
        xs = [-3.6, -1.2, 1.2, 3.6]
        mouse = gene_bar(xs[0], y0, MOUSE_CELL, color=GRAY, outline=GRAY)
        m_mean = gene_bar(xs[1], y0, MOUSE_MEAN, color=GRAY, outline=GRAY)
        h_mean = gene_bar(xs[2], y0, HUMAN_MEAN, color=INK)
        slot = dashed_box(xs[3], y0, .46, 2.3, RED, 40)
        qmark = op("?", xs[3], y0, 40, RED)
        top = y0 - 1.3
        labs = [label("mouse cell", 22, GRAY), label("mouse mean", 22, GRAY),
                label("human mean", 22, INK), label("predicted human", 22, RED)]
        for lb, x in zip(labs, xs):
            lb.move_to([x, 0, 0]).align_to([0, top, 0], UP)
        minus, plus, eq = op("−", -2.4, y0, 54, RED), op("+", 0, y0, 54, RED), op("=", 2.4, y0)
        genes = left("one stripe = one gene", xs[0] - .25, y0 + 1.42, 20, GRAY)
        with self.say(0) as vo:
            self.cue(vo, .02, FadeIn(mouse, shift=RIGHT * .1), FadeIn(labs[0]), FadeIn(genes),
                     Create(slot), FadeIn(qmark), FadeIn(labs[3]), run_time=.7)
            vo.wait_until("one subtraction")
            self.play(FadeIn(minus, scale=1.3), FadeIn(m_mean, shift=LEFT * .1), FadeIn(labs[1]),
                      run_time=.5)
            vo.wait_until("one addition")
            self.play(FadeIn(plus, scale=1.3), FadeIn(h_mean, shift=LEFT * .1), FadeIn(labs[2]),
                      minus.animate.set_color(INK), run_time=.5)
            # the arithmetic itself: the mouse cell slides into the slot and re-shades
            moving = mouse.copy()
            self.play(FadeIn(eq), plus.animate.set_color(INK), FadeOut(qmark),
                      moving.animate.move_to([xs[3], y0, 0]), run_time=.7)
            self.play(*restripe(moving, PRED_CELL, INK), moving.frame.animate.set_color(RED),
                      FadeOut(slot), run_time=.9)
            vo.wait_until("the bet scGen")
            bet = left("scGen's bet: one subtraction, one addition", -4.4, -1.72, 26, RED,
                       bold=True)
            self.play(FadeIn(bet, shift=UP * .1), run_time=.5)
            note = left("(done on a learned code, not raw genes — next)", -4.4, -2.2, 19, GRAY)
            self.play(FadeIn(note), run_time=.4)
            vo.wait_until("your package")
            pkg = chip("scGenModel", 4.6, -2.2, INK, 20)
            self.play(FadeIn(pkg, shift=LEFT * .1), run_time=.4)
        eqn = VGroup(mouse, m_mean, h_mean, moving, minus, plus, eq, *labs, genes)
        c1 = Rectangle(width=7.6, height=3.6, stroke_color=INK, stroke_width=2)\
            .move_to([-2.5, .2, 0])
        c2 = Rectangle(width=4.7, height=3.6, stroke_color=INK, stroke_width=2)\
            .move_to([3.95, .2, 0])
        t1 = left("the idea · one picture", -6.05, -1.22, 26, INK, bold=True)
        t2 = left("which library code?", 1.85, -1.22, 26, INK, bold=True)
        chips = VGroup(*[VGroup(chip("scgen", 3.55, y, INK, 22), op("?", 4.65, y, 34, RED))
                         for y in (1.4, .7, 0)])
        with self.say(1) as vo:
            self.cue(vo, .02, FadeOut(bet), FadeOut(note), FadeOut(pkg),
                     eqn.animate.scale(.85).move_to([-2.5, .58, 0]), run_time=.8)
            vo.wait_until("two things")
            self.play(Create(c1), Create(c2), run_time=.6)
            vo.wait_until("the idea")
            self.play(FadeIn(t1), c1.animate.set_color(RED), run_time=.45)
            vo.wait_until("which library")
            self.play(FadeIn(t2), c2.animate.set_color(RED), c1.animate.set_color(INK),
                      LaggedStart(*[FadeIn(c, shift=LEFT * .15) for c in chips], lag_ratio=.3),
                      run_time=1.0)
        self.finish()


GENES_20 = np.clip(np.random.default_rng(7).uniform(.1, .9, 20), .05, .95)
ROUGH_20 = np.clip(GENES_20 + np.random.default_rng(8).normal(0, .28, 20), .05, .95)
MOUSE_20 = np.clip(GENES_20 + np.random.default_rng(9).normal(0, .12, 20), .05, .95)
HUMAN_20 = np.clip(GENES_20[::-1] + np.random.default_rng(10).normal(0, .12, 20), .05, .95)
# cell types in the 2-D sketch of the code space: (name, mouse centre, label position)
TYPES = [("T cells", (2.45, .6), (2.75, .08)),
         ("B cells", (4.75, .95), (5.05, .43)),
         ("macrophages", (4.0, -.75), (4.3, -1.3))]
OFFSET = np.array([.55, .3, 0])


class S02(Ep):
    def construct(self):
        self.header()
        y = .35
        inp = gene_bar(-5.6, y, GENES_20, w=.42, h=2.6)
        enc = trapezoid(-5.15, -2.95, 2.6, .9, y)
        dec = trapezoid(-2.15, .05, .9, 2.6, y)
        code = code_column(-2.55, y, 5, .34, .9)
        out = gene_bar(.5, y, ROUGH_20, w=.42, h=2.6)
        enc_l = at("encoder", -4.05, 1.62, 22, RED, bold=True)
        dec_l = at("decoder", -1.05, 1.62, 22, RED, bold=True)
        g_l = left("~1000 gene values", -6.25, -1.25, 20, INK)
        g_m = mono_left("x_dimension: 1000", -6.25, -1.62, 17, GRAY)
        c_l = at("50 numbers", -2.55, -.62, 22, RED, bold=True)
        c_m = at("z_dimension: 50", -2.55, -.98, 17, GRAY).become(mono("z_dimension: 50", 17, GRAY)
                                                                  .move_to([-2.55, -.98, 0]))
        o_l = at("rebuilt", .5, -1.25, 20, INK)
        with self.say(0) as vo:
            self.cue(vo, .02, FadeIn(inp, shift=RIGHT * .1), run_time=.5)
            vo.wait_until("An encoder")
            self.play(Create(enc), FadeIn(enc_l), run_time=.6)
            vo.wait_until("about a thousand")
            self.play(FadeIn(g_l), FadeIn(g_m), run_time=.45)
            vo.wait_until("into a short code")
            self.play(ReplacementTransform(inp.stripes.copy(), code), run_time=1.0)
            vo.wait_until("fifty numbers")
            self.play(FadeIn(c_l, shift=UP * .08), FadeIn(c_m), enc_l.animate.set_color(INK),
                      run_time=.45)
            vo.wait_until("A decoder")
            self.play(Create(dec), FadeIn(dec_l), c_l.animate.set_color(INK), run_time=.6)
            self.play(ReplacementTransform(code.copy(), out.stripes), FadeIn(out.frame),
                      FadeIn(o_l), run_time=1.0)
        box = Rectangle(width=4.4, height=3.7, stroke_color=INK, stroke_width=2)\
            .move_to([3.9, .1, 0])
        box_t = left("one shared code space", 1.9, 1.7, 20, INK, bold=True)
        sketch = left(SKETCH, 1.7, -2.1, 18, GRAY)
        rng = np.random.default_rng(11)
        dots, homes = VGroup(), []
        for name, (mx, my), _ in TYPES:
            for sp, col in ((0, GRAY), (1, INK)):
                cx, cy = np.array([mx, my, 0]) + OFFSET * sp
                for _ in range(8):
                    homes.append([cx + rng.normal(0, .13), cy + rng.normal(0, .13), 0])
                    dots.add(Dot([rng.uniform(2.0, 5.8), rng.uniform(-1.5, 1.4), 0],
                                 radius=.055, color=col))
        good = at("rebuilt ≈ input", .5, -1.62, 20, RED)
        with self.say(1) as vo:
            self.cue(vo, .02, FadeIn(good), dec_l.animate.set_color(INK), run_time=.4)
            self.play(*restripe(out, GENES_20), run_time=1.2)
            vo.wait_until("Mouse and human")
            self.play(FadeIn(box), FadeOut(good), run_time=.4)
            for col, vals, first in ((GRAY, MOUSE_20, 0), (INK, HUMAN_20, 1)):
                pulse = Dot([-5.6, y, 0], radius=.11, color=RED)
                sp_l = at("mouse" if first == 0 else "human", -5.6, 1.92, 20, col, bold=True)
                self.play(*restripe(inp, vals, col), inp.frame.animate.set_color(col),
                          FadeIn(sp_l), FadeIn(pulse), run_time=.35)
                self.play(pulse.animate.move_to([-2.55, y, 0]), run_time=.45)
                d0 = dots[first * 8]
                self.play(pulse.animate.move_to(d0.get_center()).set_color(col)
                          .scale(.5), run_time=.5)
                self.remove(pulse)
                self.add(d0)
                self.play(FadeOut(sp_l), run_time=.2)
            rest = [d for i, d in enumerate(dots) if i not in (0, 8)]
            self.play(LaggedStart(*[FadeIn(d, scale=.5) for d in rest], lag_ratio=.03),
                      run_time=.9)
            vo.wait_until("both species land")
            self.play(FadeIn(box_t), FadeIn(sketch), box.animate.set_color(RED), run_time=.5)
        labs = VGroup(*[at(n, lx, ly, 18, GRAY) for n, _, (lx, ly) in TYPES])
        with self.say(2) as vo:
            self.cue(vo, .02, box.animate.set_color(INK),
                     *[d.animate.move_to(h) for d, h in zip(dots, homes)], run_time=1.3)
            vo.wait_until("close together")
            self.play(FadeIn(labs), run_time=.4)
            vo.wait_until("next step")
            hints = VGroup(*[Arrow([mx, my, 0], np.array([mx, my, 0]) + OFFSET, buff=.02,
                                   color=RED, stroke_width=3,
                                   max_tip_length_to_length_ratio=.3)
                             for _, (mx, my), _ in TYPES])
            self.play(LaggedStart(*[GrowArrow(h) for h in hints], lag_ratio=.2), run_time=.8)
        self.finish()
