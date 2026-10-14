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
            legend = VGroup(Dot([2.0, -1.5, 0], radius=.06, color=GRAY),
                            left("mouse", 2.15, -1.5, 18, GRAY),
                            Dot([2.0, -1.5 - .34, 0], radius=.06, color=INK),
                            left("human", 2.15, -1.5 - .34, 18, INK))
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
        saved = self.content()   # dim_rest() regroups these, so keep the list
        for m in saved:
            m.save_state()
        with self.say(2) as vo:
            card = ponder("要让同一个箭头对每种细胞类型都管用，必须满足什么？",
                          "What must be true for one arrow to work for every cell type?",
                          y=-.6)
            self.cue(vo, .08, self.dim_rest(), run_time=.5)
            self.play(FadeIn(card, shift=UP * .1), run_time=.5)
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
            self.cue(vo, .01, FadeOut(card), *[Restore(m) for m in saved], run_time=.45)
            a_l = left("mouse type A (held-out)", -6.0, -2.15, 18, GRAY)
            self.play(*[FadeOut(m) for m in (mouse, human, ml, hl, xm, xh, ta, r1, r2, r3,
                                             shift_l, tb, *steps, out_bar, out_l, link, al)],
                      darrow.animate.set_opacity(.25), dlab.animate.set_opacity(.25),
                      d2.animate.set_color(GRAY), FadeIn(a_l),
                      FadeIn(lc), FadeIn(l1), FadeIn(typeb), FadeIn(bl), run_time=.6)
            d3 = darrow.copy().set_opacity(1).shift(B_C - M_C)
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
            self.play(FadeIn(true_b), Create(own), run_time=.6)
            self.play(Create(gap), FadeIn(miss), run_time=.5)
            vo.wait_until("the gap CellOT")
            self.play(FadeIn(cellot, shift=UP * .08), FadeIn(cellot2, shift=UP * .08),
                      run_time=.5)
        self.finish()


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
        xs = [-2.85, -.35, 1.85, 4.6]

        def under(t, x, k, color=GRAY):
            return at(t, x, ly[k] - .56, 18, color)

        # setup lane
        ae0 = mini_ae(xs[1], ly["setup"], .75, GRAY, dashed=True)
        a_set = arrow(chips["setup"].get_right(), [xs[1] - .8, ly["setup"], 0], INK)
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
        tr_arrows = [arrow([a, ty, 0], [b, ty, 0], INK) for a, b in
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
        p_arrows = [arrow([a, py, 0], [b, py, 0], INK) for a, b in
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
