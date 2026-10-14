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


def base(s, x, y, size=22, color=INK, bold=False):
    """A centred label whose baseline (not its ink box) sits at a fixed height, so a row of
    labels lines up whatever their ascenders and descenders."""
    t = label("|" + s, size, color, bold=bold)
    strut = t[0]
    t.shift([0, y - strut.get_center()[1], 0])
    t.remove(strut)
    t.set_x(x)
    return t


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
    tw, top = min(1.2, w * .3), y + h / 2
    tab = VMobject(stroke_color=color, stroke_width=2).set_points_as_corners(
        [[x0, top, 0], [x0, top + .14, 0], [x0 + tw, top + .14, 0], [x0 + tw, top, 0]])
    if dashed:
        return VGroup(DashedVMobject(tab, num_dashes=8), DashedVMobject(body, num_dashes=80))
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
        ly = y0 - 1.48
        labs = [base(t, x, ly, 22, c) for t, x, c in zip(
            ("mouse cell", "mouse mean", "human mean", "predicted human"), xs,
            (GRAY, GRAY, INK, RED))]
        minus, plus, eq = op("−", -2.4, y0, 54, RED), op("+", 0, y0, 54, RED), op("=", 2.4, y0)
        genes = left("one stripe = one gene", xs[0] - .25, y0 + 1.42, 22, GRAY)
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
        c1 = Rectangle(width=7.9, height=3.6, stroke_color=INK, stroke_width=2)\
            .move_to([-2.35, .2, 0])
        c2 = Rectangle(width=4.45, height=3.6, stroke_color=INK, stroke_width=2)\
            .move_to([4.075, .2, 0])
        t1 = left("the idea · one picture", -6.05, -1.22, 26, INK, bold=True)
        t2 = left("which library code?", 2.1, -1.22, 26, INK, bold=True)
        chips = VGroup(*[VGroup(chip("scgen", 3.65, y, INK, 22), op("?", 4.75, y, 34, RED))
                         for y in (1.4, .7, 0)])
        with self.say(1) as vo:
            self.cue(vo, .02, FadeOut(bet), FadeOut(note), FadeOut(pkg),
                     eqn.animate.scale(.8).move_to([-2.35, .6, 0]), run_time=.8)
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
                cx, cy, _z = np.array([mx, my, 0]) + OFFSET * sp
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
                self.play(*restripe(inp, vals, col), *restripe(out, vals, col),
                          inp.frame.animate.set_color(col), out.frame.animate.set_color(col),
                          FadeIn(sp_l), FadeIn(pulse), run_time=.35)
                self.play(pulse.animate.move_to([-2.55, y, 0]), run_time=.35)
                d0 = dots[first * 8]
                self.play(pulse.animate.move_to(d0.get_center()).set_color(col)
                          .scale(.5), run_time=.4)
                self.remove(pulse)
                self.add(d0)
                self.play(FadeOut(sp_l), run_time=.15)
            rest = [d for i, d in enumerate(dots) if i not in (0, 8)]
            self.play(LaggedStart(*[FadeIn(d, scale=.5) for d in rest], lag_ratio=.03),
                      run_time=.9)
            vo.wait_until("both species land")
            legend = VGroup(Dot([2.0, -1.1, 0], radius=.06, color=GRAY),
                            left("mouse", 2.15, -1.1, 18, GRAY),
                            Dot([2.0, -1.1 - .34, 0], radius=.06, color=INK),
                            left("human", 2.15, -1.1 - .34, 18, INK))
            self.play(FadeIn(box_t), FadeIn(sketch), FadeIn(legend), box.animate.set_color(RED),
                      run_time=.5)
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


M_C = np.array([-4.6, -.1, 0])            # mouse training mean (2-D sketch)
H_C = np.array([-1.8, .75, 0])            # human training mean
DELTA = H_C - M_C
A_C = np.array([-4.3, -1.45, 0])          # held-out mouse type A
B_C = np.array([-5.1, .3, 0])             # a second mouse type B (s03 L3)
B_TRUE = np.array([-3.3, -.35, 0])        # where B's human cells really are


def plane(self_label=True):
    frame = Rectangle(width=7.85, height=4.0, stroke_color=INK, stroke_width=2)\
        .move_to([-2.275, -.4, 0])
    lab = left(f"code space · {SKETCH}", -6.2, 1.85, 18, GRAY)
    return frame, lab


class S03(Ep):
    def construct(self):
        self.header()
        frame, plab = plane()
        mouse = cloud(34, *M_C[:2], .3, GRAY, seed=21, radius=.05)
        human = cloud(34, *H_C[:2], .3, INK, seed=22, radius=.05)
        ml = left("mouse · training", -6.05, .82, 18, GRAY)
        hl = left("human · training", -.95, .75, 18, INK)
        xm, xh = cross(*M_C[:2], INK), cross(*H_C[:2], INK)
        x0 = 2.05
        ta = left("train · average, subtract", x0, 1.75, 20, GRAY, bold=True)
        r1 = VGroup(cross(x0 + .12, 1.3, INK, .09, 3), left("mouse mean", x0 + .4, 1.3, 20))
        r2 = VGroup(cross(x0 + .12, .9, INK, .09, 3), left("human mean", x0 + .4, .9, 20))
        r3 = left("δ = human mean − mouse mean", x0, .45, 19, RED, bold=True)
        darrow = delta_arrow(M_C, H_C)
        dlab = at("δ", -3.4, .62, 30, RED, bold=True)
        with self.say(0) as vo:
            self.cue(vo, .02, Create(frame), FadeIn(plab), FadeIn(mouse), FadeIn(ml),
                     run_time=.6)
            vo.wait_until("average their codes")
            self.play(FadeIn(ta), FadeIn(r1), ReplacementTransform(mouse.copy(), xm),
                      run_time=.8)
            vo.wait_until("Do the same")
            self.play(FadeIn(human), FadeIn(hl), run_time=.45)
            self.play(FadeIn(r2), ReplacementTransform(human.copy(), xh), run_time=.8)
            vo.wait_until("The difference")
            self.play(GrowArrow(darrow), FadeIn(dlab), FadeIn(r3), run_time=.7)
            vo.wait_until("the species shift")
            shift_l = left("the species shift", x0, .08, 20, RED)
            self.play(FadeIn(shift_l), Indicate(darrow, color=RED, scale_factor=1.06),
                      run_time=.6)
        heldout = hollow(14, *A_C[:2], .18, GRAY, seed=23)
        start = heldout.copy().shift(LEFT * 2.4).set_opacity(0)
        al = left("held-out mouse type (never trained on)", -6.0, -2.15, 18, GRAY)
        tb = left("predict · held-out cells", x0, -.5, 20, GRAY, bold=True)
        steps = [left(t, x0, y_, 20, INK) for t, y_ in
                 (("1  encode", -.93), ("2  add δ", -1.33), ("3  decode", -1.73))]
        out_bar = gene_bar(5.2, -1.33, PRED_CELL, w=.3, h=1.05, color=INK, outline=RED)
        out_l = left("predicted human cells", x0, -2.2, 20, RED, bold=True)
        with self.say(1) as vo:
            self.cue(vo, .02, FadeIn(tb), shift_l.animate.set_color(GRAY),
                     r3.animate.set_color(INK), run_time=.4)
            vo.wait_until("held-out mouse")
            self.play(FadeIn(al), run_time=.4)
            vo.wait_until("Encode them")
            steps[0].set_color(RED)
            self.play(FadeIn(steps[0]),
                      Transform(start, heldout), run_time=.6)
            self.remove(start)
            self.add(heldout)
            vo.wait_until("add delta")
            moved = heldout.copy()
            d2 = darrow.copy()
            steps[1].set_color(RED)
            self.play(FadeIn(steps[1]), steps[0].animate.set_color(INK),
                      d2.animate.shift(A_C - M_C), run_time=.5)
            self.play(moved.animate.shift(DELTA).set_stroke(RED), run_time=.9)
            vo.wait_until("decode.")
            link = arrow([steps[2].get_right()[0] + .15, -1.73, 0],
                         out_bar.get_left() + LEFT * .05 + DOWN * .25, RED)
            steps[2].set_color(RED)
            self.play(FadeIn(steps[2]), steps[1].animate.set_color(INK), Create(link),
                      FadeIn(out_bar), run_time=.6)
            vo.wait_until("Out come")
            self.play(FadeIn(out_l, shift=UP * .08), steps[2].animate.set_color(INK),
                      run_time=.45)
        with self.say(2) as vo:
            card = ponder("要让同一个箭头对每种细胞类型都管用，必须满足什么？",
                          "What must be true for one arrow to work for every cell type?",
                          y=-.6)
            self.cue(vo, .08, self.veil(), run_time=.5)
            self.play(FadeIn(card, shift=UP * .1), run_time=.5)
        self.hold(2)
        typeb = squares(10, *B_C[:2], .15, GRAY, seed=24)
        bl = at("mouse type B", B_C[0] + .05, B_C[1] + .55, 18, GRAY)
        true_a = cloud(12, *(A_C + DELTA)[:2], .16, INK, seed=25, radius=.045)
        true_b = cloud(12, *B_TRUE[:2], .16, INK, seed=26, radius=.045)
        lc = left("assumption · 假设", x0, 1.75, 22, INK, bold=True)
        l1 = left("one δ, the same for every type", x0, 1.3, 20, INK)
        fits = left("type A:  fits", x0, .55, 20, INK)
        miss = left("type B:  misses", x0, .15, 20, RED, bold=True)
        cellot = left("CellOT: a map,", x0, -.85, 26, RED, bold=True)
        cellot2 = left("not one arrow", x0, -1.3, 26, RED, bold=True)
        with self.say(3) as vo:
            self.cue(vo, .01, FadeOut(card), self.unveil(), run_time=.45)
            a_l = left("mouse type A (held-out)", -6.0, -2.15, 18, GRAY)
            self.play(*[FadeOut(m) for m in (mouse, human, ml, hl, xm, xh, ta, r1, r2, r3,
                                             shift_l, tb, *steps, out_bar, out_l, link, al)],
                      FadeOut(darrow), FadeOut(dlab),
                      d2.animate.set_color(GRAY), FadeIn(a_l),
                      FadeIn(lc), FadeIn(l1), FadeIn(typeb), FadeIn(bl), run_time=.6)
            d3 = delta_arrow(B_C, B_C + DELTA)
            moved_b = typeb.copy()
            self.play(FadeIn(d3), run_time=.35)
            self.play(moved_b.animate.shift(DELTA).set_stroke(RED), run_time=.9)
            vo.wait_until("If species")
            self.play(FadeIn(true_a), FadeIn(fits), run_time=.5)
            vo.wait_until("one arrow can't")
            own = DashedLine(B_C + RIGHT * .2, B_TRUE + LEFT * .25, color=GRAY, stroke_width=3,
                             dash_length=.1).add_tip(tip_length=.16)
            gap = DashedLine(B_C + DELTA + DOWN * .2, B_TRUE + UP * .25, color=RED,
                             stroke_width=3, dash_length=.08)
            real_b = left("real human B", 0, -.6, 17, INK)
            real_b.move_to([-3.75 - real_b.width / 2, -.6, 0])
            self.play(FadeIn(true_b), FadeIn(real_b), Create(own), run_time=.6)
            self.play(Create(gap), FadeIn(miss), run_time=.5)
            vo.wait_until("the gap CellOT")
            self.play(FadeIn(cellot, shift=UP * .08), FadeIn(cellot2, shift=UP * .08),
                      run_time=.5)
        self.finish()


def planned_tag(x, y):
    """Grey provenance chip for behaviour that does not exist in the code yet."""
    t = source_tag("PLANNED")
    t[0].set_stroke(GRAY)
    t[1].set_color(GRAY)
    return t.move_to([x, y, 0])


def lane_arrow(a, b, color=INK):
    """A thin flow arrow with a fixed small tip (long and short arrows look alike)."""
    return Arrow(a, b, buff=.08, color=color, stroke_width=3, tip_length=.16,
                 max_tip_length_to_length_ratio=1, max_stroke_width_to_length_ratio=20)


def tint(ch, color):
    """Recolour a chip's outline and text (not its paper fill)."""
    return [ch[0].animate.set_stroke(color), ch[1].animate.set_color(color)]


def mini_table(x, y, color, n=3, w=.8, rh=.13, gap=.05):
    """A tiny table: n rows of cells (flat fills)."""
    return VGroup(*[Rectangle(width=w, height=rh, stroke_width=0, fill_color=color,
                              fill_opacity=.8).move_to([x, y - i * (rh + gap), 0])
                    for i in range(n)])


class S04(Ep):
    def construct(self):
        self.header()
        ly = {"setup": 1.35, "train": .05, "predict": -1.4}
        names = {"setup": "setup()", "train": "train()", "predict": "predict()"}
        chips = {k: chip(names[k], -5.15, ly[k], INK, 22) for k in ly}
        cls = mono_left("class scGenModel(AbstractModel)", -6.2, 1.88, 17, GRAY)
        plan = planned_tag(0, 1.88)
        plan.move_to([cls.get_right()[0] + .25 + plan.width / 2, 1.88, 0])
        plan_l = left("what each method should do · not in the code yet",
                      plan.get_right()[0] + .2, 1.88, 17, GRAY)
        cls = VGroup(cls, plan, plan_l)
        xs = [-2.85, -.35, 1.85, 4.6]

        def under(t, x, k, color=GRAY):
            return at(t, x, ly[k] - .56, 18, color)

        # setup lane
        ae0 = mini_ae(xs[1], ly["setup"], .75, GRAY, dashed=True)
        a_set = lane_arrow(chips["setup"].get_right(), [xs[1] - .8, ly["setup"], 0])
        u_set = under("untrained network", xs[1], "setup", RED)
        # train lane
        ty = ly["train"]
        mouse_t = mini_table(-3.35, ty + .32, GRAY)
        human_t = mini_table(-2.35, ty + .32, INK)
        merged_m = mini_table(-2.75, ty + .4, GRAY, rh=.11, gap=.04)
        merged_h = mini_table(-2.75, ty + .4 - 3 * .15, INK, rh=.11, gap=.04)
        species = VGroup(*[Square(side_length=.11, stroke_width=0, fill_color=c, fill_opacity=1)
                           .move_to([-3.32, ty + .4 - i * .15, 0])
                           for i, c in enumerate([GRAY] * 3 + [INK] * 3)])
        u_join = under("one table + species label", xs[0], "train", RED)
        u_join.shift(DOWN * .18)
        ae1 = mini_ae(xs[1], ty, .75, INK)
        u_fit = under("fit the network", xs[1], "train", RED)
        d_small = delta_arrow([xs[2] - .5, ty - .15, 0], [xs[2] + .5, ty + .2, 0], RED, 5)
        u_delta = under("compute δ", xs[2], "train", RED)
        store = chip("self.delta", xs[3], ty, RED, 22)
        u_store = under("kept on the object", xs[3], "train", RED)
        tr_arrows = [lane_arrow([a, ty, 0], [b, ty, 0]) for a, b in
                     ((-4.0, -3.5), (-2.05, -1.15), (.45, 1.25), (2.45, 3.55))]
        with self.say(0) as vo:
            self.cue(vo, .02, FadeIn(cls), run_time=.4)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * .1) for c in chips.values()],
                                  lag_ratio=.25), run_time=.8)
            vo.wait_until("Setup builds")
            self.play(*tint(chips["setup"], RED), GrowArrow(a_set), Create(ae0),
                      FadeIn(u_set), run_time=.7)
            vo.wait_until("Train joins")
            self.play(*tint(chips["setup"], INK), u_set.animate.set_color(GRAY),
                      *tint(chips["train"], RED), GrowArrow(tr_arrows[0]),
                      FadeIn(mouse_t), FadeIn(human_t), run_time=.5)
            self.play(ReplacementTransform(mouse_t, merged_m),
                      ReplacementTransform(human_t, merged_h), run_time=.8)
            self.play(FadeIn(species, shift=RIGHT * .1), FadeIn(u_join), run_time=.4)
            vo.wait_until("fits the network")
            fit = ae0.copy()
            self.play(GrowArrow(tr_arrows[1]), u_join.animate.set_color(GRAY),
                      fit.animate.move_to(ae1), run_time=.45)
            self.play(ReplacementTransform(fit, ae1), FadeIn(u_fit), run_time=.5)
            vo.wait_until("computes delta")
            self.play(GrowArrow(tr_arrows[2]), GrowArrow(d_small), FadeIn(u_delta),
                      u_fit.animate.set_color(GRAY), run_time=.5)
            vo.wait_until("keeps it on")
            self.play(GrowArrow(tr_arrows[3]), FadeIn(store, shift=RIGHT * .1),
                      FadeIn(u_store), u_delta.animate.set_color(GRAY), run_time=.5)
        py = ly["predict"]
        px = [-3.1, 0.0, 2.3, 4.6]
        test = cloud(10, px[0], py, .12, GRAY, seed=31, radius=.045)
        enc = trapezoid(px[0] + .35, px[0] + .95, .62, .26, py, INK)
        u_enc = under("encode test mouse", px[0] + .5, "predict", RED)
        add = chip("+ self.delta", px[1], py, RED, 20)
        u_add = under("add the stored δ", px[1], "predict", RED)
        dec = trapezoid(px[2] - .3, px[2] + .3, .26, .62, py, INK)
        u_dec = under("decode", px[2], "predict", RED)
        ann = chip("AnnData", px[3], py, INK, 22)
        u_ann = under("every metric can read it", px[3], "predict", RED)
        p_arrows = [lane_arrow([a, py, 0], [b, py, 0]) for a, b in
                    ((-4.0, -3.45), (px[0] + 1.0, add.get_left()[0] - .02),
                     (add.get_right()[0] + .02, px[2] - .32),
                     (px[2] + .35, ann.get_left()[0] - .02))]
        with self.say(1) as vo:
            self.cue(vo, .02, *tint(chips["train"], INK),
                     u_store.animate.set_color(GRAY), *tint(chips["predict"], RED),
                     GrowArrow(p_arrows[0]), FadeIn(test), run_time=.45)
            vo.wait_until("encodes")
            self.play(Create(enc), FadeIn(u_enc), run_time=.45)
            token = Dot([px[0] + .65, py, 0], radius=.1, color=GRAY)
            self.play(FadeIn(token), run_time=.2)
            vo.wait_until("adds the stored")
            fly = store.copy()
            self.play(GrowArrow(p_arrows[1]), u_enc.animate.set_color(GRAY),
                      ReplacementTransform(fly, add), FadeIn(u_add),
                      token.animate.move_to([px[1], py + .45, 0]), run_time=.7)
            self.play(token.animate.set_color(RED), run_time=.25)
            vo.wait_until("decodes")
            self.play(GrowArrow(p_arrows[2]), Create(dec), FadeIn(u_dec),
                      u_add.animate.set_color(GRAY), token.animate.move_to([px[2], py, 0]),
                      run_time=.5)
            vo.wait_until("returns an AnnData")
            self.play(GrowArrow(p_arrows[3]), u_dec.animate.set_color(GRAY),
                      ReplacementTransform(token, ann), run_time=.5)
            vo.wait_until("every metric")
            self.play(FadeIn(u_ann), run_time=.4)
        tr_rows = rows(CORE, 277, 285)
        pr_rows = [(n, t.replace(".astype(np.float64)", "…")) for n, t in rows(CORE, 287, 294)]
        tp = code_panel(tr_rows, CORE_PATH, -3.2, .42, width=6.2, size=17)
        pp = code_panel(pr_rows, CORE_PATH, 3.2, .56, width=6.2, size=17)
        n1 = left("282 · δ is a local: gone when train returns", -6.25, -1.62, 19, INK)
        n2 = left("284–285 · the fit is commented out, then pass", -6.25, -2.05, 19, INK)
        n3 = left("292 · hands back the mouse cells, untouched", .15, -1.62, 19, INK)
        with self.say(2) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()], run_time=.4)
            self.play(FadeIn(tp, shift=UP * .1), FadeIn(pp, shift=UP * .1), run_time=.5)
            vo.wait_until("Train computes delta")
            m282 = highlight(self, tp, 282, run_time=.3)
            dy = tp.row_y(282)
            dd = delta_arrow([-1.05, dy - .08, 0], [-.35, dy + .08, 0], RED, 4).set_z_index(3)
            self.play(GrowArrow(dd), run_time=.3)
            vo.wait_until("never fits")
            m284 = tp.mark(284, 285)
            self.play(FadeIn(m284), FadeIn(n2), run_time=.4)
            vo.wait_until("vanishes")
            self.play(FadeIn(n1), dd.animate.scale(.05).set_opacity(0), run_time=.7)
            vo.wait_until("Predict ends")
            m292 = highlight(self, pp, 292, run_time=.3)
            gy = pp.row_y(292)
            out = cloud(8, 5.8, pp.row_y(288), .07, GRAY, seed=32, radius=.04).set_z_index(3)
            self.play(FadeIn(out), run_time=.3)
            self.play(FadeIn(n3), out.animate.move_to([5.8, gy, 0]), run_time=.6)
            vo.wait_until("your blanks")
            boxes = VGroup(*[SurroundingRectangle(VGroup(*[p.row(n) for n in ns]), color=RED,
                                                  buff=.06, stroke_width=2.5)
                             for p, ns in ((tp, (282,)), (tp, (284, 285)), (pp, (292,)))])
            self.play(Create(boxes), *[n.animate.set_color(RED) for n in (n1, n2, n3)],
                      run_time=.6)
        self.finish()


# specs/m1_modern.yaml lines 33-37 in the speciesOT repo (109bf12), verbatim
M1_ROWS = [(33, "scgen_hidden_units:"), (34, "- 256"), (35, "- 256"),
           (36, "scgen_latent_dim: 50"), (37, "scgen_lr: 0.001")]


def qchip(x, y, size=22):
    """'scgen' with a red question mark."""
    c = chip("scgen", x, y, INK, size)
    q = op("?", c.get_right()[0] + .22, y + .12, 30, RED)
    return VGroup(c, q)


class S05(Ep):
    def construct(self):
        self.header()
        fx0, fx1, fy0, fy1 = -6.3, 2.35, -2.42, 1.6
        frame = Rectangle(width=fx1 - fx0, height=fy1 - fy0, stroke_color=INK, stroke_width=2)\
            .move_to([(fx0 + fx1) / 2, (fy0 + fy1) / 2, 0])
        flab = left("your speciesOT project", fx0, 1.85, 20, INK, bold=True)
        repo = mono_left("repo @109bf12", flab.get_right()[0] + .25, 1.85, 16, GRAY)
        ftag = source_tag("READ IN CODE")
        ftag.move_to([repo.get_right()[0] + .3 + ftag.width / 2, 1.85, 0])
        flab = VGroup(flab, repo, ftag)
        one = qchip(-2.4, .3)
        spots = [(-2.4, .75), (4.45, .3), (-2.4, -1.45)]
        with self.say(0) as vo:
            self.cue(vo, .02, Create(frame), FadeIn(flab), run_time=.6)
            vo.wait_until("trace back")
            self.play(FadeIn(one, scale=1.2), run_time=.5)
            vo.wait_until("three different")
            q3 = [one.copy() for _ in range(3)]
            self.remove(one)
            self.play(*[c.animate.move_to([x, y, 0]) for c, (x, y) in zip(q3, spots)],
                      run_time=.9)
        # (1) the TensorFlow scgen: a git-ignored nested clone, its own env
        h1 = VGroup(badge(1, -5.95, 1.3),
                    left("TensorFlow scgen (VAEArith) · atlas scripts", -5.6, 1.3, 20, INK,
                         bold=True))
        f1 = path_folder(-5.6, .7, 7.45, .46, dashed=True)
        p1 = mono_left("scgen-cellot-ablation/scgen-reproducibility/code", -5.45, .7, 16, INK)
        ign = chip("git-ignored", 1.25, 1.3, GRAY, 17, font=LATIN, pad=.14)
        env = chip("scgen_tf1 · TF 1.15", -4.3, .17, INK, 18)
        env.move_to([-5.6 + env.width / 2, .17, 0])
        helpers = left("Josh's helpers ≡ these lines:", -2.1, .17, 18, RED)
        hpath = mono_left("atlas-paper-vae/scripts/02_eval_metrics.py:151–171", -5.95, -.25,
                          16, INK)
        with self.say(1) as vo:
            self.cue(vo, .02, ReplacementTransform(q3[0], h1), run_time=.6)
            vo.wait_until("separate clone")
            self.play(Create(f1), FadeIn(p1), run_time=.7)
            vo.wait_until("git-ignored")
            link1 = DashedLine(ign.get_bottom(), [ign.get_x(), .95, 0], color=GRAY,
                               stroke_width=2, dash_length=.05)
            self.play(FadeIn(ign, scale=1.1), Create(link1), run_time=.4)
            vo.wait_until("its own TensorFlow")
            env[0].set_stroke(RED)
            env[1].set_color(RED)
            self.play(FadeIn(env, shift=RIGHT * .1), run_time=.45)
            vo.wait_until("Josh's helper")
            self.play(*tint(env, INK), FadeIn(helpers), FadeIn(hpath, shift=UP * .08),
                      run_time=.5)
            vo.wait_until("line for line")
            self.play(Indicate(hpath, color=RED, scale_factor=1.03), run_time=.6)
        # (2) the pip package: outside the project
        bx, bw = 4.45, 3.7
        box2 = Rectangle(width=bw, height=2.6, stroke_color=INK, stroke_width=2)\
            .move_to([bx, .3, 0])
        b2 = VGroup(badge(2, 2.85, 1.86),
                    left("pip package", 3.15, 1.86, 20, INK, bold=True))
        hdr = mono_left("scgen 2.x (scvi-tools)", 2.8, 1.3, 17, INK)
        exp = left("exports:", 2.8, .9, 17, GRAY)
        names = [mono_left(n, 2.8, y_, 20, INK) for n, y_ in
                 (("SCGEN", .5), ("SCGENVAE", .1), ("VAEArith", -.32))]
        strike_v = strike(names[2])
        none_l = left("not in 2.x", 4.65, -.32, 17, RED)
        t2 = tag_at("READ IN PACKAGE", 3.55, -1.32)
        t2b = VGroup(tag_at("INFERRED", 5.45, -1.32), at("Josh's env?", 5.45, -1.7, 17, GRAY))
        core_p = code_panel([(10, "# … (~20s, pulls in scvi-tools/torch) …"), (248, CORE[248]),
                             (252, CORE[252])], CORE_PATH, -2.85, -1.45, width=6.6, size=16)
        with self.say(2) as vo:
            self.cue(vo, .02, FadeOut(q3[2]),
                     ReplacementTransform(q3[1], VGroup(box2, b2, hdr)), run_time=.6)
            vo.wait_until("import scgen")
            self.play(FadeIn(core_p, shift=UP * .1), run_time=.45)
            m248 = highlight(self, core_p, 248, run_time=.3)
            ry = core_p.row_y(248)
            go = arrow([core_p.frame.get_right()[0] + .05, ry, 0], [2.65, -.6, 0], RED)
            self.play(GrowArrow(go), FadeIn(exp), *[FadeIn(n) for n in names[:2]], run_time=.7)
            vo.wait_until("His comment")
            m10 = core_p.mark(10)
            self.play(ReplacementTransform(m248, m10), go.animate.set_color(INK), run_time=.4)
            vo.wait_until("no VAEArith")
            self.play(FadeIn(names[2]), run_time=.35)
            self.play(Create(strike_v), FadeIn(none_l), FadeIn(t2), run_time=.5)
            vo.wait_until("If that's what loads")
            self.play(FadeIn(t2b), run_time=.4)
            vo.wait_until("setup stops")
            m252 = core_p.mark(252)
            ey = core_p.row_y(252)
            stop = cross(core_p.row(252).get_right()[0] + .25, ey, RED, .11, 4).set_z_index(3)
            stop_l = left("stops here", core_p.frame.get_right()[0] + .14, ey, 19, RED,
                          bold=True)
            self.play(ReplacementTransform(m10, m252), Create(stop), run_time=.5)
            self.play(FadeIn(stop_l), run_time=.35)
        # (3) the vendored CellOT autoencoder
        h3 = VGroup(badge(3, -5.95, -.75),
                    left("PyTorch AutoEncoder · cellot folder", -5.6, -.75, 20, INK, bold=True))
        f3 = path_folder(-5.6, -1.27, 2.85, .44)
        p3 = mono_left("cellot/cellot_gpu", -5.45, -1.27, 18, INK)
        vend = left("vendored bunnech/cellot · BSD · your edits", -2.6, -1.27, 17, GRAY)
        ae = mono_left("AutoEncoder + compute_scgen_shift", -5.6, -1.75, 18, INK)
        aeloc = mono_left("models/ae.py:22, 175", -.5, -1.75, 16, GRAY)
        made = left("→ made your benchmark numbers", -5.6, -2.17, 20, RED, bold=True)
        with self.say(3) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in (core_p, m252, go, stop, stop_l)],
                     FadeIn(q3[2]), run_time=.4)
            self.play(ReplacementTransform(q3[2], h3), run_time=.6)
            vo.wait_until("CellOT's source")
            self.play(Create(f3), FadeIn(p3), run_time=.5)
            vo.wait_until("with your own edits")
            self.play(FadeIn(vend), run_time=.4)
            vo.wait_until("plain autoencoder")
            self.play(FadeIn(ae, shift=UP * .08), FadeIn(aeloc), run_time=.5)
            vo.wait_until("same mean shift")
            self.play(Indicate(ae, color=RED, scale_factor=1.04), run_time=.6)
            vo.wait_until("That one produced")
            self.play(FadeIn(made, shift=RIGHT * .1), f3.animate.set_color(RED),
                      run_time=.5)
        cfg = code_panel(rows(CONFIG, 32, 40), CONFIG_PATH, -3.6, -.25, width=5.3, size=20)
        m1 = code_panel(M1_ROWS, "specs/m1_modern.yaml", 3.75, .5, width=4.3, size=19)
        b3 = VGroup(badge(3, 1.85, 1.88),
                    left("cellot autoencoder", 2.15, 1.88, 20, INK, bold=True))
        spec = left("= the cellot autoencoder's spec", 1.6, -.95, 19, RED, bold=True)
        tf = chip("TF VAEArith: 2 × 800, fixed", 3.75, -1.55, INK, 19)
        b1 = badge(1, tf.get_left()[0] - .32, -1.55)
        tfloc = mono_left("atlas-paper-vae/configs/m2_v08.yaml:27", 1.2, -2.1, 16, GRAY)
        with self.say(4) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()], run_time=.45)
            self.play(FadeIn(cfg, shift=UP * .1), run_time=.45)
            ties = VGroup()
            marks = []
            for word, a, bs in (("two layers", 34, (33, 34, 35)), ("fifty latent", 38, (36,)),
                                ("learning rate", 35, (37,))):
                vo.wait_until(word)
                ma, mb = cfg.mark(a), m1.mark(*bs)
                tie = Line([cfg.frame.get_right()[0], cfg.row_y(a), 0],
                           [m1.frame.get_left()[0], m1.row_y(bs[len(bs) // 2]), 0],
                           color=RED, stroke_width=2.5)
                anims = [FadeIn(ma), FadeIn(mb), Create(tie)]
                if not marks:
                    anims += [FadeIn(m1, shift=LEFT * .1), FadeIn(b3)]
                self.play(*anims, run_time=.5)
                marks += [ma, mb]
                ties.add(tie)
            vo.wait_until("That's the cellot")
            self.play(FadeIn(spec, shift=UP * .08), run_time=.45)
            vo.wait_until("The TensorFlow model")
            self.play(FadeIn(tf), FadeIn(b1), FadeIn(tfloc), ties.animate.set_color(GRAY),
                      spec.animate.set_color(INK), run_time=.5)
            vo.wait_until("would go nowhere")
            na = np.array([cfg.frame.get_right()[0], cfg.row_y(34), 0])
            nb = np.array([b1.get_left()[0] - .05, -1.55, 0])
            nowhere = DashedLine(na, nb, color=RED, stroke_width=3, dash_length=.1)
            self.play(Create(nowhere), run_time=.45)
            mid = na + .75 * (nb - na)
            self.play(Create(strike(tf[1])), Create(cross(mid[0], mid[1], RED, .14, 4)),
                      run_time=.45)
        self.finish()


CELLOT = "cellot/cellot_gpu/cellot/"
CALLS = [  # (narration phrase, call, file:line in the speciesOT repo at 109bf12)
    ("build or load", "load_autoencoder_model", "models/ae.py:33"),
    ("train it", "train_auto_encoder", "train/train.py:173"),
    ("encode,", "model.encode", "models/ae.py:149"),
    ("decode,", "model.decode", "models/ae.py:152"),
    ("compute the shift", "compute_scgen_shift", "models/ae.py:175"),
]
# videos/speciesot-series/checks/error_trail.py, verbatim
FAKE_ROWS = [(32, "class FakeVAEArith:"), (33, "    def __init__(self, **kwargs):"),
             (34, "        self.kwargs = kwargs"), (35, ""), (36, ""),
             (37, "fake.VAEArith = FakeVAEArith"), (38, 'sys.modules["scgen"] = fake')]


def package(cx, cy, r, inside=True, size=18):
    """The package as a boundary, with its classes inside and scGenModel as the door."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=2.5).move_to([cx, cy, 0])
    parts = VGroup()
    if inside:
        for name, dx, dy in (("Experiment", -.1, 1.1), ("IdentityModel", -.35, .35),
                             ("R2 · MMD metrics", -.15, -.4)):
            parts.add(chip(name, cx + dx * r / 2.0, cy + dy * r / 2.0, INK, size,
                           font=MONO if " " not in name else LATIN))
    door = chip("scGenModel", cx + r, cy, RED, size + 2)
    return ring, parts, door


class S06(Ep):
    def construct(self):
        self.header()
        cx, cy, r = -3.75, -.3, 1.95
        ring, parts, door = package(cx, cy, r)
        plab = left("your speciesot package", -6.25, 1.9, 20, INK, bold=True)
        contract = at("setup · train · predict", cx - .1, cy - 1.0, 17, GRAY)
        dlab = left("adapter · the one door", door.get_left()[0] + 1.0, cy - .72, 18, RED,
                    bold=True)
        out_word = mono("scgen", 20, RED).move_to([door.get_right()[0] + .7, cy + .35, 0])
        out_arrow = arrow(door.get_right() + RIGHT * .05, [door.get_right()[0] + 1.35, cy, 0],
                          RED)
        with self.say(0) as vo:
            self.cue(vo, .02, Create(ring), FadeIn(plab), run_time=.6)
            self.play(LaggedStart(*[FadeIn(pp, scale=.9) for pp in parts], lag_ratio=.25),
                      run_time=.7)
            vo.wait_until("is an adapter")
            self.play(FadeIn(door, scale=1.15), run_time=.5)
            vo.wait_until("the only place")
            self.play(GrowArrow(out_arrow), FadeIn(out_word), FadeIn(dlab), run_time=.6)
            vo.wait_until("Everything else")
            tok = Dot(parts[0].get_right() + RIGHT * .1, radius=.08, color=INK)
            self.play(FadeIn(contract), FadeIn(tok), run_time=.4)
            self.play(tok.animate.move_to(door.get_left() + LEFT * .1), run_time=.8)
            self.play(FadeOut(tok), Indicate(door, color=RED, scale_factor=1.05), run_time=.5)
        libs = [("1", "TF VAEArith · git-ignored clone", 1.35),
                ("2", "scgen 2.x · pip (scvi-tools)", .2),
                ("3", "cellot AutoEncoder", -.95)]
        lib_g = []
        for n, text, y in libs:
            c = chip(text, 3.55, y, GRAY if n != "3" else INK, 18, font=LATIN)
            lib_g.append(VGroup(badge(n, c.get_left()[0] - .3, y, GRAY if n != "3" else RED),
                                c))
        wires = [DashedLine(door.get_right() + RIGHT * .05, g[0].get_left() + LEFT * .05,
                            color=GRAY, stroke_width=2.5, dash_length=.1) for g in lib_g]
        made = left("made your benchmark numbers", lib_g[2][1].get_left()[0], -1.5, 18, GRAY)
        josh = VGroup(tag_at("INFERRED", 0, -2.05), left("our pick · decide with Josh", 0, -2.05,
                                                           19, INK))
        josh[0].move_to([made.get_left()[0] + josh[0].width / 2, -2.05, 0])
        josh[1].next_to(josh[0], RIGHT, buff=.2)
        if josh.get_right()[0] > 6.2:
            josh.shift(LEFT * (josh.get_right()[0] - 6.2))
        with self.say(1) as vo:
            self.cue(vo, .02, FadeOut(out_arrow), FadeOut(out_word), run_time=.3)
            self.play(LaggedStart(*[FadeIn(g, shift=LEFT * .1) for g in lib_g], lag_ratio=.2),
                      *[Create(w) for w in wires], run_time=.9)
            vo.wait_until("exactly one")
            self.play(*[w.animate.set_opacity(.25) for w in wires[:2]], run_time=.4)
            vo.wait_until("wrap the cellot")
            solid = Line(door.get_right() + RIGHT * .05, lib_g[2][0].get_left() + LEFT * .05,
                         color=RED, stroke_width=4)
            self.play(ReplacementTransform(wires[2], solid), *tint(lib_g[2][1], RED),
                      run_time=.5)
            vo.wait_until("because it made")
            self.play(FadeIn(made), run_time=.4)
            vo.wait_until("Settle that")
            self.play(FadeIn(josh, shift=UP * .08), run_time=.45)
        # the few calls, with file and line (cellot/cellot_gpu/cellot, repo @109bf12)
        bx0, bx1, by0, by1 = -.35, 6.3, -1.85, 1.75
        box = Rectangle(width=bx1 - bx0, height=by1 - by0, stroke_color=INK, stroke_width=2)\
            .move_to([(bx0 + bx1) / 2, (by0 + by1) / 2, 0])
        bhead = VGroup(badge(3, bx0 + .2, 1.92),
                       left("cellot AutoEncoder", bx0 + .5, 1.92, 20, INK, bold=True),
                       mono_left(CELLOT, bx0 + .3, by1 - .32, 16, GRAY))
        rows_ = []
        for i, (_, call, loc) in enumerate(CALLS):
            yy = by1 - .95 - i * .5
            rows_.append(VGroup(mono_left(call, bx0 + .3, yy, 19, INK),
                                mono_left(loc, bx0 + 3.95, yy, 17, GRAY)))
        rtag = source_tag("READ IN CODE")
        rtag.move_to([bx1 - .15 - rtag.width / 2, by1 - .32, 0])
        nowhere = left("read the source here — nowhere else", bx0 + .3, by0 + .3, 19, RED)
        with self.say(2) as vo:
            self.cue(vo, .02, *[FadeOut(m) for m in (*lib_g[:2], *wires[:2], made, josh, dlab)],
                     ReplacementTransform(lib_g[2], bhead), FadeIn(box),
                     solid.animate.put_start_and_end_on(door.get_right() + RIGHT * .05,
                                                        [bx0 - .05, cy, 0]), run_time=.7)
            prev = None
            for (phrase, _, _), row in zip(CALLS, rows_):
                vo.wait_until(phrase)
                row[0].set_color(RED)
                anims = [FadeIn(row, shift=LEFT * .1)]
                if prev is not None:
                    anims.append(prev[0].animate.set_color(INK))
                self.play(*anims, run_time=.35)
                prev = row
            vo.wait_until("Read the library")
            self.play(prev[0].animate.set_color(INK), FadeIn(nowhere), FadeIn(rtag),
                      run_time=.45)
        fake = code_panel(FAKE_ROWS, "videos/speciesot-series/checks/error_trail.py", 3.0,
                          -.12, width=6.3, size=18)
        tests = DashedVMobject(Rectangle(width=6.75, height=4.4, stroke_color=GRAY,
                                         stroke_width=2).move_to([2.97, -.2, 0]), num_dashes=70)
        tlab = left("in tests: no scgen installed", -.2, 1.72, 19, GRAY, bold=True)
        mtag = tag_at("MEASURED", 0, -1.85)
        mlab = left("how we ran Josh's code for this series", 0, -1.85, 18, INK)
        mtag.move_to([-.2 + mtag.width / 2, -1.85, 0])
        mlab.next_to(mtag, RIGHT, buff=.2)
        with self.say(3) as vo:
            lib = VGroup(box, bhead, *rows_, rtag, nowhere)
            self.cue(vo, .02, lib.animate.shift(RIGHT * 7).set_opacity(0), run_time=.7)
            self.remove(lib)
            vo.wait_until("a few-line fake")
            self.play(FadeIn(fake, shift=LEFT * .6),
                      solid.animate.put_start_and_end_on(door.get_right() + RIGHT * .05,
                                                         [fake.frame.get_left()[0] - .05, cy,
                                                          0]), run_time=.7)
            m = highlight(self, fake, 32, 33, 34, run_time=.35)
            vo.wait_until("never need it")
            self.play(Create(tests), FadeIn(tlab), run_time=.6)
            vo.wait_until("That's exactly")
            self.play(FadeIn(mtag), FadeIn(mlab), FadeOut(m), run_time=.45)
        with self.say(4) as vo:
            card = ponder("以后换成另一种 scGen 实现，包里有几个文件要改？",
                          "Switch to another scGen implementation: how many files change?",
                          y=-.55)
            self.cue(vo, .06, self.veil(), run_time=.5)
            self.play(FadeIn(card, shift=UP * .1), run_time=.5)
        self.hold(4)
        self.finish()


COMMENTS = [(None, "def train(self, training_data):"),
            (None, "    # 1. join mouse + human (species)"),
            (None, "    # 2. fit the network"),
            (None, "    # 3. delta = mean(z_h) - mean(z_m)"),
            (None, "    # 4. keep it: self.delta = delta"),
            (None, "def predict(self, test_data):"),
            (None, "    # 1. encode the test mouse cells"),
            (None, "    # 2. add self.delta, then decode"),
            (None, "    # 3. return an AnnData")]


class S07(Ep):
    def construct(self):
        self.header()
        y = 1.15
        bar1 = gene_bar(-5.85, y, MOUSE_CELL, w=.3, h=1.4, color=GRAY, outline=GRAY)
        enc = trapezoid(-5.5, -4.45, 1.4, .5, y)
        lat = Rectangle(width=3.3, height=1.6, stroke_color=INK, stroke_width=2)\
            .move_to([-2.45, y, 0])
        sk = left(SKETCH, -4.05, y - 1.0, 16, GRAY)
        cells = cloud(12, -3.4, y - .25, .14, GRAY, seed=41, radius=.045)
        d = DELTA / np.linalg.norm(DELTA) * 1.75
        dar = delta_arrow([-3.3, y - .55, 0], [-3.3 + d[0], y - .55 + d[1], 0])
        dec = trapezoid(-.6, .45, .5, 1.4, y)
        bar2 = gene_bar(.8, y, PRED_CELL, w=.3, h=1.4, color=INK, outline=RED)
        meths = [("setup", "builds the network", 1.65), ("train", "learns network + δ", 1.05),
                 ("predict", "applies them", .45)]
        mrows = [VGroup(chip(m + "()", 2.85, yy, INK, 20),
                        left(t, 4.0, yy, 20, INK)) for m, t, yy in meths]
        for r_ in mrows:
            r_[0].move_to([1.75 + r_[0].width / 2, r_[0].get_y(), 0])
            r_[1].next_to(r_[0], RIGHT, buff=.2)
        with self.say(0) as vo:
            self.cue(vo, .03, FadeIn(bar1), run_time=.3)
            vo.wait_until("encodes")
            self.play(Create(enc), FadeIn(lat), FadeIn(cells), FadeIn(sk), run_time=.6)
            vo.wait_until("shifts every cell")
            self.play(GrowArrow(dar), run_time=.4)
            self.play(cells.animate.shift([d[0], d[1], 0]).set_color(RED), run_time=.9)
            vo.wait_until("and decodes")
            self.play(Create(dec), FadeIn(bar2, shift=RIGHT * .1), run_time=.5)
            for (m, _, _), r_ in zip(meths, mrows):
                vo.wait_until({"setup": "Setup builds", "train": "train learns",
                               "predict": "predict applies"}[m])
                self.play(FadeIn(r_, shift=LEFT * .1), run_time=.35)
        cx, cy, r = -4.75, -1.33, 1.05
        ring = Circle(radius=r, stroke_color=INK, stroke_width=2.5).move_to([cx, cy, 0])
        inner = at("your package", cx, cy + .55, 17, GRAY)
        door = chip("adapter", cx + r, cy, RED, 18)
        three = [VGroup(badge(n, -1.95, yy, RED if n == "3" else GRAY),
                        left(t, -1.65, yy, 18, INK if n == "3" else GRAY))
                 for n, t, yy in (("1", "TF VAEArith", -.65), ("2", "scgen 2.x", -1.3),
                                  ("3", "cellot AE", -1.95))]
        wire = Line(door.get_right() + RIGHT * .05, three[2][0].get_left() + LEFT * .05,
                    color=RED, stroke_width=4)
        ans = left("1 file changes", .9, -1.0, 30, RED, bold=True)
        ans2 = left("the adapter + its section of the config", .9, -1.55, 20, INK)
        with self.say(1) as vo:
            self.cue(vo, .02, *[r_.animate.set_opacity(.45) for r_ in mrows], run_time=.3)
            self.play(LaggedStart(*[FadeIn(t) for t in three], lag_ratio=.2), run_time=.6)
            vo.wait_until("Your adapter")
            self.play(Create(ring), FadeIn(inner), FadeIn(door), run_time=.6)
            self.play(Create(wire), run_time=.4)
            vo.wait_until("The answer")
            new = Line(door.get_right() + RIGHT * .05, three[1][0].get_left() + LEFT * .05,
                       color=RED, stroke_width=4)
            self.play(Transform(wire, new), Indicate(door, color=RED, scale_factor=1.15),
                      run_time=.8)
            vo.wait_until("one file changes")
            self.play(FadeIn(ans, shift=UP * .08), run_time=.45)
            vo.wait_until("plus its section")
            self.play(FadeIn(ans2), run_time=.4)
        ex = left("EXERCISE · 练习", -6.2, 1.85, 22, RED, bold=True)
        s1 = left("1 · find the calls, with file:line", -6.2, 1.3, 20, INK, bold=True)
        s1p = mono_left("in " + CELLOT, -6.2, .88, 16, GRAY)
        slots = []
        for i, (_, call, _) in enumerate(CALLS):
            yy = .38 - i * .5
            slot = DashedVMobject(Rectangle(width=1.25, height=.34, stroke_color=GRAY,
                                            stroke_width=2), num_dashes=16)\
                .move_to([-1.35, yy, 0])
            slots.append(VGroup(mono_left(call, -6.2, yy, 17, INK), slot,
                                at("?", -1.35, yy, 18, GRAY)))
        s2 = left("2 · train and predict as comments", .0, 1.3, 20, INK, bold=True)
        panel = code_panel(COMMENTS, "", 3.15, -.55, width=6.3, size=18, numbers=False)
        etag = tag_at("EXAMPLE", 5.6, 1.3)
        with self.say(2) as vo:
            self.cue(vo, .01, *[FadeOut(mm) for mm in self.content()], run_time=.4)
            self.play(FadeIn(ex), run_time=.3)
            vo.wait_until("in the cellot")
            self.play(FadeIn(s1), FadeIn(s1p), run_time=.4)
            self.play(LaggedStart(*[FadeIn(sl, shift=RIGHT * .1) for sl in slots],
                                  lag_ratio=.2), run_time=1.0)
            vo.wait_until("Then write")
            self.play(FadeIn(s2), FadeIn(etag), FadeIn(panel.frame), run_time=.4)
            lines = list(panel.texts)
            per = max(.2, (vo.remaining() - .8) / len(lines))
            for t in lines:
                self.play(FadeIn(t, shift=RIGHT * .08), run_time=min(.3, per))
                if per > .3:
                    self.wait(per - .3)
        self.finish()
