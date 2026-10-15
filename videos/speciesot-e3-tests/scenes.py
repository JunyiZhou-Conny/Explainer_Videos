"""speciesOT E3 · A test is a question with a known answer — Swiss scenes.

Narration and budgets come from the plan (script.json). Code on screen is Josh's real source
(videos/speciesot-series/excerpts.py, real line numbers; a long line may be elided with "…",
never rewritten). Code we wrote ourselves to illustrate a test carries the EXAMPLE tag; the
three sketches in S04 were run against Josh's R2Evaluation / MMDEvaluation (3 passed).

Data on screen is the measured data, regenerated here with the seeds of
checks/error_trail.py: the toy test sets (rng 0: MMD 0.326, the 5 vs 7 cells) and the
known-answer cloud (rng 1: 40 cells × 3 genes, MMD vs shift, R² perfect / shuffled).
Kernel values for Josh's three points are computed (exp(-0.5·d²)), never typed.
"""
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent.parent / "speciesot-series"
sys.path.insert(0, str(SERIES))

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F401,F403
from speciesot_kit import *  # noqa: E402,F401,F403
from excerpts import CORE, TEST_EVALUATION, TEST_MODEL, rows  # noqa: E402

CORE_PATH = "src/speciesot/speciesot_core.py"
TESTS = "src/speciesot/Tests"
TEST_EVAL_PATH = f"{TESTS}/test_evaluation.py"
TEST_MODEL_PATH = f"{TESTS}/test_model.py"


class Ep(EpisodeScene):
    episode = "E3"
    total = "07"

    def settle(self, *whole):
        """After a LaggedStart over the parts of an object, Scene.play leaves a plain Group
        holding those parts. Unwrap it and put the whole objects back as single top-level
        mobjects, so later fades, transforms and restores act on exactly what is on screen
        (a ReplacementTransform of the whole would otherwise leave the old parts behind)."""
        fam = {id(x) for w in whole for x in w.get_family()}

        def covered(m):            # one of the wholes, or a wrapper made only of them
            return id(m) in fam or (bool(m.submobjects) and all(covered(c) for c in m.submobjects))
        keep = []
        for m in self.mobjects:
            for part in ([m] if isinstance(m, VMobject) else m.submobjects):
                if not covered(part) and all(part is not k for k in keep):
                    keep.append(part)
        self.mobjects = keep
        self.add(*whole)


# ---------------------------------------------------------------- measured data

def toy_cells():
    """The toy test sets of checks/error_trail.py (seed 0, same draw order, float32)."""
    rng = np.random.default_rng(0)

    def draw(n, s=0.0):
        return rng.normal(s, 1.0, size=(n, 4)).astype(np.float32).astype(float)
    draw(6), draw(6, 1.0)                    # training sets (not shown)
    mouse, human = draw(5), draw(5, 1.0)     # test sets -> MMD 0.326
    human7 = draw(7, 1.0)                    # uneven human test set (5 vs 7 -> ValueError)
    return mouse, human, human7


def known_answer_cells():
    """stage known_answers: 40 cells x 3 genes (seed 1) and the shuffle permutation."""
    r = np.random.default_rng(1)
    base = r.normal(0, 1, size=(40, 3))
    return base, r.permutation(40)


def r2_score(p, t):
    """R2Evaluation.evaluate (speciesot_core.py 311-316) on plain arrays."""
    a, b = p - p.mean(0), t - t.mean(0)
    num, den = (a * b).sum(0), np.sqrt((a ** 2).sum(0) * (b ** 2).sum(0))
    ok = den > 1e-12
    return float(np.mean((num[ok] / den[ok]) ** 2))


def rbf(a, b, gamma):
    d2 = ((a[:, None, :] - b[None, :, :]) ** 2).sum(-1)
    return np.exp(-gamma * d2)


# ---------------------------------------------------------------- diagram parts

class Plot:
    """A square scatter box: data range [lo, hi] on both genes -> a box of side `side`."""

    def __init__(self, cx, cy, side, lo, hi):
        self.cx, self.cy, self.side = cx, cy, side
        self.sc = side / (hi - lo)
        self.mid = (lo + hi) / 2

    def p(self, g1, g2):
        return np.array([self.cx + (g1 - self.mid) * self.sc,
                         self.cy + (g2 - self.mid) * self.sc, 0])

    def box(self):
        return Rectangle(width=self.side, height=self.side, stroke_color=FAINT,
                         stroke_width=1.5).move_to([self.cx, self.cy, 0])

    def axes_labels(self, size=17):
        b = self.cy - self.side / 2
        lx = label("gene 1 →", size, GRAY)
        lx.move_to([self.cx + self.side / 2 - lx.width / 2, b - .2, 0])
        ly = label("gene 2 →", size, GRAY).rotate(PI / 2)
        ly.move_to([self.cx - self.side / 2 - .2, self.cy + self.side / 2 - ly.height / 2, 0])
        return VGroup(lx, ly)


def dots(plot, pts, color=INK, r=.055):
    return VGroup(*[Dot(plot.p(a, b), radius=r, color=color) for a, b in pts])


def rings(plot, pts, color=GRAY, r=.085, stroke=2.2):
    return VGroup(*[Circle(radius=r, color=color, stroke_width=stroke).move_to(plot.p(a, b))
                    for a, b in pts])


def shade(v, lo=-2.8, hi=2.8):
    return .05 + .8 * float(np.clip((v - lo) / (hi - lo), 0, 1))


def matrix(vals, x, top, cw=.36, ch=.25):
    """A cells x genes matrix: one row per cell, shaded by the real value."""
    nr, nc = vals.shape
    g = VGroup()
    g.cells = VGroup()
    for i in range(nr):
        row = VGroup(*[Rectangle(width=cw, height=ch, stroke_color=PAPER, stroke_width=1.5,
                                 fill_color=INK, fill_opacity=shade(vals[i, j]))
                       .move_to([x - (nc - 1) * cw / 2 + j * cw, top - ch / 2 - i * ch, 0])
                       for j in range(nc)])
        g.cells.add(row)
    g.frame = Rectangle(width=nc * cw, height=nr * ch, stroke_color=INK, stroke_width=2)\
        .move_to([x, top - nr * ch / 2, 0])
    g.add(g.cells, g.frame)
    g.cw, g.ch, g.top, g.x = cw, ch, top, x
    return g


def row_y(m, i):
    return m.top - m.ch / 2 - i * m.ch


def kgrid(K, x, y, cw=.96, ch=.44, size=18):
    """A 3x3 kernel matrix with its computed values (cells tinted by similarity)."""
    n = K.shape[0]
    g = VGroup()
    g.cells = VGroup()
    for i in range(n):
        for j in range(n):
            v = K[i, j]
            box = Rectangle(width=cw, height=ch, stroke_color=PAPER, stroke_width=2,
                            fill_color=INK, fill_opacity=.04 + .22 * v)\
                .move_to([x - (n - 1) * cw / 2 + j * cw, y + (n - 1) * ch / 2 - i * ch, 0])
            txt = mono("1" if abs(v - 1) < 1e-12 else f"{v:.3f}", size, INK)\
                .move_to(box.get_center())
            g.cells.add(VGroup(box, txt))
    g.texts = VGroup(*[c[1] for c in g.cells])
    g.frame = Rectangle(width=n * cw, height=n * ch, stroke_color=INK, stroke_width=2)\
        .move_to([x, y, 0])
    g.add(g.cells, g.frame)
    return g


def tick(x, y, size=30, color=INK):
    return mono("✓", size, color, bold=True).move_to([x, y, 0])


def cross(x, y, size=30, color=RED):
    return mono("✗", size, color, bold=True).move_to([x, y, 0])


def rack(x, y):
    g = VGroup()
    for i in range(3):
        yy = y + .38 - i * .38
        g.add(Rectangle(width=1.3, height=.32, stroke_color=INK, stroke_width=2,
                        fill_color=PAPER, fill_opacity=1).move_to([x, yy, 0]),
              Dot([x - .45, yy, 0], radius=.045, color=INK),
              Line([x - .2, yy, 0], [x + .48, yy, 0], color=GRAY, stroke_width=2))
    return g


def bigfile(x, y):
    w, h, f = .95, 1.15, .28
    body = Polygon([x - w / 2, y + h / 2, 0], [x + w / 2 - f, y + h / 2, 0],
                   [x + w / 2, y + h / 2 - f, 0], [x + w / 2, y - h / 2, 0],
                   [x - w / 2, y - h / 2, 0], stroke_color=INK, stroke_width=2,
                   fill_color=PAPER, fill_opacity=1)
    fold = VMobject(stroke_color=INK, stroke_width=2).set_points_as_corners(
        [[x + w / 2 - f, y + h / 2, 0], [x + w / 2 - f, y + h / 2 - f, 0],
         [x + w / 2, y + h / 2 - f, 0]])
    return VGroup(body, fold, label("GB", 26, INK, bold=True).move_to([x, y - .12, 0]))


def gpu_icon(x, y):
    body = Rectangle(width=1.3, height=.78, stroke_color=INK, stroke_width=2).move_to([x, y, 0])
    pins = VGroup(*[Line([x + dx, y + s * .39, 0], [x + dx, y + s * .55, 0], color=INK,
                         stroke_width=2) for dx in (-.45, -.22, 0, .22, .45) for s in (1, -1)])
    return VGroup(body, pins, label("GPU", 24, INK, bold=True).move_to([x, y, 0]))


def red_box(m, buff=.06):
    return SurroundingRectangle(m, color=RED, stroke_width=2.5, buff=buff)


def save(ms):
    for m in ms:
        m.save_state()
    return ms


# ---------------------------------------------------------------- S01

class S01(Ep):
    def construct(self):
        self.header()
        mouse, human, _ = toy_cells()
        both = np.vstack([mouse[:, :2], human[:, :2]])
        lo, hi = both.min() - .4, both.max() + .4
        ya, yb = 1.15, -1.45
        pa = Plot(-4.6, ya, 1.7, lo, hi)
        box_a = pa.box()
        m_a, h_a = rings(pa, mouse[:, :2]), dots(pa, human[:, :2])
        leg = VGroup(Circle(radius=.075, color=GRAY, stroke_width=2.2).move_to([-5.35, .03, 0]),
                     left("mouse", -5.18, .03, 17, GRAY),
                     Dot([-4.3, .03, 0], radius=.055, color=INK),
                     left("human", -4.15, .03, 17, INK))
        note = left("5 toy cells each · genes 1–2 of 4", -5.45, -.27, 17, GRAY)
        chip_a = chip("MMDEvaluation", -1.4, ya, INK, 22)
        arr1 = arrow([-3.6, ya, 0], chip_a.get_left(), INK)
        arr2 = arrow(chip_a.get_right(), [1.05, ya, 0], INK)
        num = at("0.326", 2.75, ya, 80, INK, bold=True)
        tag = tag_at("MEASURED", 2.75, ya - .78)
        with self.say(0) as vo:
            self.cue(vo, .02, FadeIn(box_a), FadeIn(m_a), FadeIn(h_a), FadeIn(leg),
                     FadeIn(note), run_time=.6)
            vo.wait_until("MMD metric")
            self.play(Create(arr1), FadeIn(chip_a, shift=RIGHT * .1), run_time=.5)
            vo.wait_until("zero point")
            self.play(Create(arr2), FadeIn(num, shift=RIGHT * .15), FadeIn(tag), run_time=.6)
            vo.wait_until("Is that right?")
            q = at("?", 4.85, ya, 84, RED, bold=True)
            self.play(FadeIn(q, scale=1.3), run_time=.4)

        # the number is a sum of kernel averages in 4 dimensions: no eye can check it
        g = .1
        terms = [rbf(mouse, mouse, g).mean(), rbf(human, human, g).mean(),
                 rbf(mouse, human, g).mean()]
        dec, dec_lab = VGroup(), VGroup()
        xx_ = 0.0
        for s_, lab_ in [("=", None), (f"{terms[0]:.3f}", "inside mouse"), ("+", None),
                         (f"{terms[1]:.3f}", "inside human"), ("− 2 ×", None),
                         (f"{terms[2]:.3f}", "across")]:
            t_ = mono(s_, 20, GRAY)
            l_ = label(lab_, 17, GRAY) if lab_ else None
            w_ = max(t_.width, l_.width if l_ else 0)
            t_.move_to([xx_ + w_ / 2, ya - 1.2, 0])
            dec.add(t_)
            if l_:
                dec_lab.add(l_.move_to([xx_ + w_ / 2, ya - 1.52, 0]))
            xx_ += w_ + .24
        VGroup(dec, dec_lab).shift(RIGHT * (2.75 - VGroup(dec, dec_lab).get_center()[0]))
        pb = Plot(-4.6, yb, 1.7, lo, hi)
        box_b = pb.box()
        m_b = rings(pb, mouse[:, :2])
        h_b = dots(pb, human[:, :2])
        h_same = dots(pb, mouse[:, :2])
        chip_b = chip("MMDEvaluation", -1.4, yb, INK, 22)
        arr3 = arrow([-3.6, yb, 0], chip_b.get_left(), INK)
        arr4 = arrow(chip_b.get_right(), [1.05, yb, 0], INK)
        must = at("must be 0", 2.75, yb, 44, RED, bold=True)
        known = at("known answer · 已知答案", 2.75, yb - .6, 21, GRAY)
        same_lab = left("identical clouds", -3.65, yb - .62, 17, GRAY)
        with self.say(1) as vo:
            vo.wait_until("Nobody can check")
            self.play(TransformFromCopy(num, dec), FadeIn(dec_lab, shift=UP * .05), run_time=.7)
            vo.wait_until("But you can check")
            self.play(q.animate.set_color(GRAY), TransformFromCopy(box_a, box_b),
                      TransformFromCopy(m_a, m_b), TransformFromCopy(h_a, h_b), run_time=.7)
            vo.wait_until("already know")
            self.play(Transform(h_b, h_same), FadeIn(same_lab), run_time=.8)
            self.play(Create(arr3), FadeIn(chip_b), Create(arr4), FadeIn(must, shift=RIGHT * .1),
                      FadeIn(known), run_time=.6)

        row_a = VGroup(box_a, m_a, h_a, leg, note, chip_a, arr1, arr2, num, tag, q, dec, dec_lab)
        row_b = VGroup(box_b, m_b, h_b, same_lab, chip_b, arr3, arr4, must, known)
        defin = left("a test = a question with a known answer", -6.1, -.55, 36, INK, bold=True)
        defzh = left("测试 = 一个答案已知的问题，由代码自己作答", -6.1, -1.12, 24, GRAY)
        got = mono("0.0 ✓", 30, RED, bold=True).move_to([5.45, ya, 0])
        with self.say(2) as vo:
            self.cue(vo, .01, FadeOut(row_a), row_b.animate.shift(UP * (ya - yb)), run_time=.7)
            vo.wait_until("a question")
            self.play(FadeIn(defin, shift=UP * .1), FadeIn(defzh), run_time=.5)
            vo.wait_until("which your code")
            tok = Dot([-3.6, ya, 0], radius=.08, color=RED)
            self.play(FadeIn(tok), must.animate.set_color(INK), run_time=.2)
            self.play(tok.animate.move_to(chip_b.get_left()), run_time=.3)
            self.play(chip_b[0].animate.set_stroke(RED), chip_b[1].animate.set_color(RED),
                      run_time=.25)
            self.play(tok.animate.move_to([1.05, ya, 0]), chip_b[0].animate.set_stroke(INK),
                      chip_b[1].animate.set_color(INK), run_time=.3)
            self.play(FadeOut(tok), FadeIn(got, shift=LEFT * .1), run_time=.3)
            vo.wait_until("every time")
            runs = VGroup()
            for k in range(3):
                runs.add(VGroup(left(f"run {k + 1}", -6.1 + k * 2.5, -1.95, 22, GRAY),
                                tick(-6.1 + k * 2.5 + 1.25, -1.95, 26, INK)))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * .1) for r in runs], lag_ratio=.45),
                      run_time=1.1)
            self.settle(runs)
        self.finish()


# ---------------------------------------------------------------- S02

class S02(Ep):
    def construct(self):
        self.header()
        x = np.array([[0., 0.], [1., 1.], [2., 2.]])        # test_evaluation.py line 15
        test = code_panel(rows(TEST_EVALUATION, 14, 22), TEST_EVAL_PATH, -2.25, .35,
                          width=8.1, size=17)
        # x as a table: rows = cells, columns = genes
        cols, rws = [4.45, 5.55], [1.2, .82, .44]
        head = VGroup(at("gene 1", cols[0], 1.58, 17, GRAY), at("gene 2", cols[1], 1.58, 17, GRAY))
        rlab = VGroup(*[at(f"cell {i + 1}", 3.25, y, 17, GRAY) for i, y in enumerate(rws)])
        vals = VGroup(*[mono(f"{x[i, j]:.0f}.", 20).move_to([cols[j], rws[i], 0])
                        for i in range(3) for j in range(2)])
        tframe = Rectangle(width=2.3, height=1.2, stroke_color=INK, stroke_width=2)\
            .move_to([5.0, .82, 0])
        table = VGroup(head, rlab, vals, tframe)
        tname = left("x: 3 cells × 2 genes", 2.75, 1.92, 17, GRAY)
        pl = Plot(4.45, -.82, 1.6, -.6, 2.6)
        pbox = pl.box()
        truth = dots(pl, x, INK, .07)
        pred = rings(pl, x, GRAY, .14, 2.5)
        leg = VGroup(Circle(radius=.075, color=GRAY, stroke_width=2.2).move_to([2.95, -1.85, 0]),
                     left("predicted", 3.12, -1.85, 17, GRAY),
                     Dot([4.6, -1.85, 0], radius=.055, color=INK),
                     left("truth", 4.75, -1.85, 17, INK))
        same = at("the same cloud", 4.45, -2.17, 19, RED, bold=True)
        with self.say(0) as vo:
            self.cue(vo, .02, FadeIn(test, shift=UP * .1), run_time=.6)
            vo.wait_until("Three cells")
            m = highlight(self, test, 15, run_time=.3)
            self.play(FadeIn(tname), FadeIn(head), FadeIn(rlab), Create(tframe),
                      TransformFromCopy(test.row(15), vals), run_time=.8)
            vo.wait_until("The prediction")
            m2 = test.mark(16, 17)
            self.play(ReplacementTransform(m, m2), FadeIn(pbox), FadeIn(leg), run_time=.4)
            self.play(*[TransformFromCopy(vals[2 * i], truth[i]) for i in range(3)],
                      *[TransformFromCopy(vals[2 * i + 1], pred[i]) for i in range(3)],
                      run_time=.9)
            self.settle(truth, pred)     # the dots arrived one by one: re-add them as two clouds
            self.play(FadeIn(same, shift=UP * .08), run_time=.4)

        # the kernel: similarity of every pair of points, exp(-gamma * d^2), gamma = 0.5 (line 19)
        K = rbf(x, x, .5)
        d2 = ((x[:, None, :] - x[None, :, :]) ** 2).sum(-1)
        gx, gy = [-4.2, 0, 4.2], .95
        names = [("xx", "inside predicted"), ("yy", "inside truth"), ("xy", "across")]
        grids = VGroup(*[kgrid(K, gxx, gy) for gxx in gx])
        titles = VGroup(*[VGroup(mono_left(n, gxx - 1.44, 1.86, 20, INK, bold=True),
                                 left(d, gxx - .97, 1.86, 18, GRAY))
                          for (n, d), gxx in zip(names, gx)])
        ops = VGroup(at("+", -2.1, gy, 34, INK), at("− 2 ×", 2.1, gy, 30, INK))
        means = VGroup(*[mono(f"mean {K.mean():.3f}", 18, INK).move_to([gxx, .02, 0])
                         for gxx in gx])
        mmdp = code_panel([(n, CORE[n]) for n in (327, 328, 329, 331)], CORE_PATH, 2.6, -1.45,
                          width=7.2, size=17)
        # the same three points, small, at the left: where 0.368 and 0.018 come from
        sp = Plot(-5.5, -1.55, 1.25, -.6, 2.6)
        sbox = sp.box()
        struth = dots(sp, x, INK, .06)
        spred = rings(sp, x, GRAY, .11, 2.2)
        snum = VGroup(*[mono(str(i + 1), 17, GRAY).move_to(sp.p(*x[i]) + np.array([.24, -.13, 0]))
                        for i in range(3)])
        kform = VGroup(mono_left("k = exp(−0.5 · d²)", -6.2, -.5, 18, INK),
                       left("γ = 0.5, test line 19", -3.2, -.5, 17, GRAY))
        pairs = [(0, 1), (0, 2)]
        # the points are collinear: draw the 1-3 pair as an arc so it doesn't hide the 1-2 pair
        plines = VGroup(Line(sp.p(*x[0]), sp.p(*x[1]), color=RED, stroke_width=4),
                        ArcBetweenPoints(sp.p(*x[0]), sp.p(*x[2]), angle=-PI / 2.2, color=RED,
                                         stroke_width=4))
        sup = {1: "¹", 2: "²", 4: "⁴"}
        plabs = VGroup(*[mono_left(f"d² = {d2[a, b]:.0f} → e⁻{sup[int(.5 * d2[a, b])]} = "
                                   f"{K[a, b]:.3f}", -4.6, y, 18, INK)
                         for (a, b), y in zip(pairs, (-1.2, -1.8))])

        def cells(g, a, b):            # the two entries (a, b) and (b, a) of a 3x3 grid
            return [g.texts[3 * a + b], g.texts[3 * b + a]]
        with self.say(1) as vo:
            keep = (pbox, truth, pred)
            self.cue(vo, .01, *[FadeOut(mm) for mm in self.content() if mm not in keep],
                     ReplacementTransform(pbox, sbox), ReplacementTransform(truth, struth),
                     ReplacementTransform(pred, spred),
                     run_time=.5)
            self.play(LaggedStart(*[FadeIn(c) for g_ in grids for c in g_.cells],
                                  lag_ratio=.03),
                      *[Create(g_.frame) for g_ in grids], FadeIn(titles), FadeIn(ops),
                      FadeIn(mmdp), FadeIn(kform), FadeIn(snum), run_time=1.0)
            self.settle(*grids)
            lit = []
            for k, (a, b) in enumerate(pairs):
                now = [t for g_ in grids for t in cells(g_, a, b)]
                anims = [Create(plines[k]), FadeIn(plabs[k], shift=RIGHT * .08),
                         *[t.animate.set_color(RED) for t in now]]
                if k:
                    anims += [plines[k - 1].animate.set_color(INK),
                              plabs[k - 1].animate.set_color(GRAY),
                              *[t.animate.set_color(INK) for t in lit]]
                self.play(*anims, run_time=.45)
                lit = now
            vo.wait_until("Add the average")
            hk = highlight(self, mmdp, 327, 329, run_time=.3)
            self.play(grids[0].frame.animate.set_color(RED), grids[1].frame.animate.set_color(RED),
                      ops[0].animate.set_color(RED), FadeIn(means[0]), FadeIn(means[1]),
                      plines[1].animate.set_color(INK), plabs[1].animate.set_color(GRAY),
                      *[t.animate.set_color(INK) for t in lit], run_time=.6)
            vo.wait_until("then subtract")
            hk2 = mmdp.mark(328, 331)
            self.play(ReplacementTransform(hk, hk2),
                      grids[0].frame.animate.set_color(INK), grids[1].frame.animate.set_color(INK),
                      ops[0].animate.set_color(INK), ops[1].animate.set_color(RED),
                      grids[2].frame.animate.set_color(RED), FadeIn(means[2]), run_time=.6)

        eq = mono(f"{K.mean():.3f} + {K.mean():.3f} − 2 × {K.mean():.3f}", 20, INK)\
            .move_to([3.75, -.85, 0])
        zero = at("= 0", 3.75, -1.6, 44, RED, bold=True)
        small = VGroup(sbox, struth, spred, snum, plines, plabs, kform)
        with self.say(2) as vo:
            self.cue(vo, .01, FadeOut(small), FadeOut(hk2), FadeOut(ops), FadeOut(titles),
                     grids[2].frame.animate.set_color(INK),
                     mmdp.animate.move_to([-2.6, -1.45, 0]), run_time=.5)
            vo.wait_until("all three averages")
            self.play(*[FadeOut(grids[i].texts) for i in (0, 2)],
                      *[FadeOut(means[i]) for i in (0, 2)], run_time=.25)
            self.play(*[grids[i].animate.move_to([0, gy, 0]) for i in (0, 2)], run_time=.8)
            same3 = at("all three grids are the same", 0, 1.86, 20, GRAY)
            self.play(FadeIn(same3), TransformFromCopy(means[1], eq), run_time=.5)
            vo.wait_until("must be zero")
            self.play(FadeIn(zero, shift=UP * .1), run_time=.4)

        tail = code_panel(rows(TEST_EVALUATION, 19, 22), TEST_EVAL_PATH, -.6, 1.07, width=7.8,
                          size=18)
        y22 = tail.row_y(22)
        line_end = tail.row(22).get_right()[0]
        zero_at = np.array([4.95, y22, 0])
        to_approx = arrow(zero_at + LEFT * .55, [line_end + .12, y22, 0], RED).set_z_index(3)
        fp = repr(0.1 + 0.2 - 0.3)
        approx = VGroup(at("approx: floating-point sums are rarely exactly 0", 0, -.62, 24, INK),
                        mono(f"0.1 + 0.2 − 0.3  =  {fp}", 20, GRAY).move_to([0, -1.22, 0]),
                        at("pytest.approx(0.0) means 0 ± 1e-12", 0, -1.75, 20, GRAY))
        ok = terminal(["$ pytest -q …/Tests/test_evaluation.py",
                       ".                       [100%]",
                       "1 passed in 1.45s"], -3.35, -1.05, width=5.7, size=17)
        bad = terminal(["F                       [100%]",
                        "E  assert 0.500905449162582 == 0.0 ± 1.0e-12",
                        "E    Obtained: 0.500905449162582",
                        "E    Expected: 0.0 ± 1.0e-12"], 3.05, -1.15, width=6.5, size=16)
        ok_lab = left("✓ passes, silently", -6.2, -.15, 22, INK, bold=True)
        ok_tag = source_tag("MEASURED").next_to(ok_lab, RIGHT, buff=.25)
        bad_lab = left("✗ fails, loudly", -.2, -.15, 22, RED, bold=True)
        bad_tag = source_tag("EXAMPLE").next_to(bad_lab, RIGHT, buff=.25)
        bad_note = VGroup(left("excerpt of real pytest output,", -.2, -2.09, 17, GRAY),
                          left("if speciesot_core.py:331 lost its “2 *”", -.2, -2.34, 17, GRAY))
        with self.say(3) as vo:
            self.cue(vo, .01, *[FadeOut(mm) for mm in self.content() if mm is not zero],
                     zero.animate.move_to(zero_at), FadeIn(tail, shift=UP * .1), run_time=.6)
            vo.wait_until("assert that")
            hl = highlight(self, tail, 22, run_time=.35)
            self.play(GrowArrow(to_approx), run_time=.5)
            vo.wait_until("Approximately, because")
            self.play(FadeIn(approx[0], shift=UP * .08), run_time=.45)
            self.play(FadeIn(approx[1]), run_time=.4)
            vo.wait_until("rarely exactly")
            self.play(FadeIn(approx[2]), run_time=.4)
            vo.wait_until("If it is")
            self.play(FadeOut(approx), FadeOut(to_approx), zero.animate.set_color(INK),
                      run_time=.3)
            self.play(FadeIn(ok, shift=UP * .1), FadeIn(ok_lab), FadeIn(ok_tag), run_time=.45)
            vo.wait_until("If not")
            self.play(FadeIn(bad, shift=UP * .1), FadeIn(bad_lab), FadeIn(bad_tag),
                      FadeIn(bad_note), run_time=.5)
            vo.wait_until("both numbers")
            self.play(Create(red_box(VGroup(bad.lines[2], bad.lines[3]), .08)), run_time=.35)
        self.finish()


# ---------------------------------------------------------------- S03

class S03(Ep):
    def construct(self):
        self.header()
        fname = "test_mmd_is_zero_for_identical_distributions"
        call = mono(fname + "()", 19, INK).move_to([0, -.95, 0])
        call_lab = at("you never call it yourself", 0, -.45, 19, GRAY)
        term = terminal(["$ pytest"], -5.0, 1.55, width=2.3, size=24)
        files = ["config.yaml", "e24_replica.ipynb", "test_evaluation.py", "test_model.py",
                 "toy_config.yaml"]
        tx, ty = -2.0, [1.47, 1.11, .75, .39, .03]
        root = mono_left("Tests/", tx - .3, 1.86, 20, INK, bold=True)
        tree = VGroup(*[mono_left(f, tx, y, 19, GRAY if f.endswith("ipynb") else INK)
                        for f, y in zip(files, ty)])
        pip = VGroup(left("package installed with", -6.2, .88, 17, GRAY),
                     mono_left("pip install -e .  (E2)", -6.2, .6, 17, GRAY))
        twig = VGroup(*[Line([tx - .22, y + .18, 0], [tx - .22, y, 0], color=FAINT,
                             stroke_width=1.5) for y in ty],
                      *[Line([tx - .22, y, 0], [tx - .08, y, 0], color=FAINT, stroke_width=1.5)
                        for y in ty])
        rule_f = chip("files:  test_*.py", 4.3, 1.42, INK, 20)
        rule_d = chip("functions:  test*", 4.3, .62, INK, 20)
        arr0 = arrow(term.get_right() + RIGHT * .05, [tx - .5, 1.86, 0], INK)
        with self.say(0) as vo:
            self.cue(vo, .02, FadeIn(call), FadeIn(call_lab), run_time=.5)
            st = strike(call)
            self.play(Create(st), run_time=.4)
            vo.wait_until("You type")
            self.play(FadeIn(term, shift=RIGHT * .1), FadeIn(pip), run_time=.4)
            vo.wait_until("It finds")
            self.play(Create(arr0), FadeIn(root), FadeIn(twig), FadeIn(tree), FadeIn(rule_f),
                      run_time=.6)
            scan = Rectangle(width=.08, height=.3, stroke_width=0, fill_color=RED,
                             fill_opacity=1).move_to([tx - .4, ty[0], 0])
            self.add(scan)
            for i, f in enumerate(files):
                hit = f.startswith("test_")
                self.play(scan.animate.move_to([tx - .4, ty[i], 0]),
                          tree[i].animate.set_color(RED if hit else FAINT), run_time=.28)
            self.play(FadeOut(scan), *[tree[i].animate.set_color(INK) for i in (2, 3)],
                      run_time=.25)
            defl = mono(f"def {fname}():", 19, INK).move_to([0, -.95, 0])
            defl[3:7].set_color(RED)
            vo.wait_until("runs every function")
            src = mono_left("in test_evaluation.py:", -3.8, -.45, 18, GRAY)
            self.play(FadeOut(call_lab), FadeOut(st), ReplacementTransform(call, defl),
                      FadeIn(src), FadeIn(rule_d),
                      tree[2].animate.set_color(RED), run_time=.6)
            vo.wait_until("reports")
            rep_arr = arrow([defl.get_right()[0] + .15, -.95, 0],
                            [defl.get_right()[0] + .85, -.95, 0], INK)
            dot_ = mono(".", 40, RED, bold=True).next_to(rep_arr, RIGHT, buff=.15)\
                .align_to(defl, DOWN)
            key = mono(".  passed      F  failed      E  error", 18, GRAY).move_to([0, -1.95, 0])
            self.play(Create(rep_arr), FadeIn(dot_, scale=1.5), FadeIn(key), run_time=.5)

        run1 = terminal(["$ pytest -q src/speciesot/Tests/test_evaluation.py",
                         ".                       [100%]",
                         "1 passed in 1.45s"], 0, 1.2, width=9.2, size=20)
        mtag = tag_at("MEASURED", 5.55, 1.75)
        x0, x1, y_bar = -5.2, 4.8, -.65
        sc = (x1 - x0) / 1.45
        axis = Line([x0, y_bar - .32, 0], [x1, y_bar - .32, 0], color=GRAY, stroke_width=1.5)
        ticks = VGroup(*[VGroup(Line([x0 + t * sc, y_bar - .38, 0], [x0 + t * sc, y_bar - .26, 0],
                                     color=GRAY, stroke_width=1.5),
                                mono(f"{t:g} s", 16, GRAY).move_to([x0 + t * sc, y_bar - .62, 0]))
                         for t in (0, .5, 1.0, 1.45)])
        imp = Rectangle(width=(1.45 - .02) * sc, height=.42, stroke_width=0, fill_color=FAINT,
                        fill_opacity=1).move_to([x0 + (1.43 * sc) / 2, y_bar, 0])
        body = Rectangle(width=.02 * sc, height=.42, stroke_width=0, fill_color=RED,
                         fill_opacity=1).move_to([x1 - .01 * sc, y_bar, 0])
        imp_lab = left("start-up + importing numpy, anndata, sklearn …", x0 + .15, y_bar, 19, INK)
        body_lab = at("the test itself: a few ms", x1 - 1.1, y_bar + .52, 19, RED)
        itag = tag_at("INFERRED", x1 - .55, -1.72)
        with self.say(1) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content() if m is not term],
                     ReplacementTransform(term, run1), run_time=.6)
            vo.wait_until("passes")
            self.play(FadeIn(mtag), Indicate(run1.lines[2], color=RED, scale_factor=1.05),
                      run_time=.6)
            vo.wait_until("most of that")
            self.play(FadeIn(axis), FadeIn(ticks), GrowFromEdge(imp, LEFT), run_time=.9)
            self.play(FadeIn(imp_lab), FadeIn(body), FadeIn(body_lab), FadeIn(itag), run_time=.5)
            vo.wait_until("Pause and predict")
            pcard = ponder("对整个 Tests 文件夹运行 pytest，会发生什么？",
                           "Run pytest on the whole Tests folder: what happens?", y=-1.25)
            self.play(self.veil(), run_time=.35)
            self.play(FadeIn(pcard, shift=UP * .1), run_time=.45)
        self.hold(1)                 # thinking time after the ponder question

        run2 = terminal(["$ pytest -q src/speciesot/Tests",
                         "ERROR src/speciesot/Tests/test_model.py - FileNotFoundError: "
                         "[Errno 2] No suc...",
                         "!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection "
                         "!!!!!!!!!!!!!!!!!!!!",
                         "1 error in 1.58s"], 0, 1.1, width=12.6, size=17)
        run2b = terminal(["$ pytest -q src/speciesot/Tests",
                          "ERROR src/speciesot/Tests/test_model.py - FileNotFoundError: "
                          "[Errno 2] No suc...",
                          "!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection "
                          "!!!!!!!!!!!!!!!!!!!!",
                          "1 error in 1.58s"], 0, -1.68, width=12.6, size=16)
        tm_rows = rows(TEST_MODEL, 1, 8)
        tm_rows[4] = (5, 'experiment_spec_path = "/n/…/Tests/config.yaml"')
        tm = code_panel(tm_rows, TEST_MODEL_PATH, -2.75, .68, width=7.1, size=16, gap=.255)
        rx = 1.1
        script_lab = left("no  def test_…  — a script", rx, 1.86, 21, RED, bold=True)
        on_import = left("runs the moment pytest imports it", rx, 1.5, 19, INK)
        off_h = left("off the cluster", rx, 1.08, 20, INK, bold=True)
        off_e = mono_left("FileNotFoundError", rx, .74, 19, RED)
        off_w = mono_left("line 6 → speciesot_core.py:81", rx, .45, 16, GRAY)
        off_t = source_tag("MEASURED").move_to([5.65, 1.08, 0])
        on_h = left("on the cluster", rx, .02, 20, INK, bold=True)
        on_t = source_tag("INFERRED").move_to([5.65, .02, 0])
        load_lab = left("loads the multi-GB atlas files", rx, -.3, 18, INK)
        load = Rectangle(width=.01, height=.14, stroke_width=0, fill_color=GRAY, fill_opacity=1)\
            .move_to([rx + .005, -.6, 0])
        crash = left("✗ crashes in setup()", rx + 2.75, -.6, 18, RED)
        with self.say(2) as vo:
            self.cue(vo, .01, FadeOut(pcard), self.unveil(),
                     *[FadeOut(m) for m in (mtag, axis, ticks, imp, body, imp_lab,
                                            body_lab, itag)],
                     ReplacementTransform(run1, run2), run_time=.5)
            vo.wait_until("stops early")
            stop = red_box(run2.lines[2], .05)
            self.play(Create(stop), run_time=.4)
            vo.wait_until("test_model.py isn't")
            self.play(FadeOut(stop), ReplacementTransform(run2, run2b), run_time=.6)
            self.play(FadeIn(tm, shift=UP * .1), FadeIn(script_lab), run_time=.5)
            vo.wait_until("Its code runs")
            mk = tm.mark(1)
            self.play(FadeIn(mk), FadeIn(on_import), run_time=.3)
            for n in (5, 6, 8):
                nm = tm.mark(n)
                self.play(ReplacementTransform(mk, nm), run_time=.3)
                mk = nm
            vo.wait_until("Off the cluster")
            nm = tm.mark(6)
            err_box = red_box(run2b.lines[1], .04)
            self.play(ReplacementTransform(mk, nm), FadeIn(off_h), FadeIn(off_t),
                      script_lab.animate.set_color(INK), run_time=.4)
            mk = nm
            self.play(FadeIn(off_e, shift=RIGHT * .1), FadeIn(off_w), Create(err_box),
                      run_time=.5)
            vo.wait_until("On the cluster")
            self.play(FadeOut(err_box), FadeIn(on_h), FadeIn(on_t),
                      off_e.animate.set_color(INK), run_time=.4)
            vo.wait_until("loads the multi")
            nm = tm.mark(8)
            self.play(ReplacementTransform(mk, nm), FadeIn(load_lab), run_time=.4)
            mk = nm
            self.play(load.animate.stretch_to_fit_width(2.55).move_to([rx + 1.275, -.6, 0]),
                      run_time=1.2)
            vo.wait_until("then crashes")
            self.play(FadeIn(crash), run_time=.4)
            vo.wait_until("before a single")
            int_box = red_box(run2b.lines[2], .04)
            self.play(Create(int_box), run_time=.5)

        icons = VGroup(rack(-4.0, .45), bigfile(0, .45), gpu_icon(4.0, .45))
        names = VGroup(at("a cluster", -4.0, -.5, 21, INK), at("gigabyte files", 0, -.5, 21, INK),
                       at("a GPU", 4.0, -.5, 21, INK))
        need = left("a good test runs on", -6.1, 1.72, 28, INK, bold=True)
        yours = VGroup(left("your code", need.get_right()[0] + .25, 1.72, 28, RED, bold=True))
        yours.add(left("alone", yours.get_right()[0] + .25, 1.72, 28, INK, bold=True))
        strikes = VGroup(*[Line(ic.get_corner(DL) + LEFT * .15 + DOWN * .1,
                                ic.get_corner(UR) + RIGHT * .15 + UP * .1, color=RED,
                                stroke_width=5) for ic in icons])
        ly = -1.95
        loop = VGroup(chip("edit", -3.0, ly, INK, 22), chip("pytest", -.6, ly, INK, 22),
                      chip("✓ green", 1.8, ly, INK, 22))
        la = VGroup(arrow(loop[0].get_right(), loop[1].get_left(), INK),
                    arrow(loop[1].get_right(), loop[2].get_left(), INK),
                    CurvedArrow(loop[2].get_top() + UP * .05, loop[0].get_top() + UP * .05,
                                angle=PI / 3.2, color=GRAY, stroke_width=2.5,
                                tip_length=.18))
        every = left("≈ 1.5 s · after every edit", 2.95, ly - .02, 20, RED)
        with self.say(3) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()], run_time=.4)
            self.play(FadeIn(need), FadeIn(yours), run_time=.4)
            self.play(LaggedStart(*[FadeIn(i, shift=UP * .1) for i in icons], lag_ratio=.2),
                      FadeIn(names), run_time=.7)
            self.settle(icons)
            for w, s in zip(["No cluster", "no gigabyte", "no GPU"], strikes):
                vo.wait_until(w)
                self.play(Create(s), run_time=.3)
            vo.wait_until("fast enough")
            self.play(*[n.animate.set_color(GRAY) for n in names],
                      FadeIn(loop), Create(la), run_time=.6)
            tok = Dot(loop[0].get_bottom() + DOWN * .14, radius=.08, color=RED)
            self.play(FadeIn(tok), FadeIn(every), run_time=.3)
            for k in (1, 2, 0):
                self.play(tok.animate.move_to(loop[k].get_bottom() + DOWN * .14), run_time=.4)
        self.finish()


# ---------------------------------------------------------------- S04

class S04(Ep):
    def construct(self):
        self.header()
        base, perm = known_answer_cells()
        xy = base[:, :2]
        pl = Plot(-3.55, -.15, 3.8, -2.95, 4.65)
        box = pl.box()
        pred = rings(pl, xy, GRAY, .075, 2)
        truth = dots(pl, xy, INK, .05)
        note = left("40 cells × 3 genes · genes 1–2 shown", -5.45, -2.3, 17, GRAY)
        leg = VGroup(Circle(radius=.07, color=GRAY, stroke_width=2).move_to([-5.32, 1.92, 0]),
                     left("predicted", -5.15, 1.92, 17, GRAY),
                     Dot([-3.7, 1.92, 0], radius=.05, color=INK),
                     left("truth = predicted + shift", -3.55, 1.92, 17, INK))
        # bar chart: MMD vs shift (MEASURED)
        shifts, mmd = ["0", "0.5", "1", "2"], [0.0, 0.0797, 0.2923, 0.8473]
        bx, base_y, hs = [1.55, 2.75, 3.95, 5.15], -1.65, 2.9
        axis = Line([.95, base_y, 0], [5.8, base_y, 0], color=INK, stroke_width=2)
        xl = VGroup(*[mono(s, 18, GRAY).move_to([b, base_y - .25, 0]) for s, b in zip(shifts, bx)])
        xt = at("shift added to every gene", 3.35, base_y - .6, 17, GRAY)
        yt = left("MMD", .95, 1.92, 20, INK, bold=True)
        ctag = source_tag("MEASURED").move_to([5.3, 1.92, 0])
        chart = VGroup(axis, xl, xt, yt, ctag)
        meaning = left("MMD = how far apart two clouds are", .95, 1.45, 19, GRAY)
        with self.say(0) as vo:
            self.cue(vo, .02, FadeIn(box), FadeIn(pred), FadeIn(truth),
                     FadeIn(note), FadeIn(leg), run_time=.6)
            vo.wait_until("From what")
            self.play(FadeIn(chart), FadeIn(meaning), run_time=.6)
            vo.wait_until("Pause and predict")
            pcard = ponder("把一团点推离另一团，MMD 应该怎么变？",
                          "Push one cloud away from the other: what should MMD do?", y=-1.25)
            self.play(self.veil(), run_time=.4)
            self.play(FadeIn(pcard, shift=UP * .1), run_time=.5)
        self.hold(0)                 # thinking time after the ponder question

        bars = VGroup()
        vlabs = VGroup()
        for b, v in zip(bx, mmd):
            h = max(v * hs, .02)
            bars.add(Rectangle(width=.72, height=h, stroke_width=0, fill_color=INK,
                               fill_opacity=1).move_to([b, base_y + h / 2, 0]))
            vlabs.add(mono("0" if v == 0 else f"{v:.3f}", 18, INK)
                      .move_to([b, base_y + h + .22, 0]))
        with self.say(1) as vo:
            self.cue(vo, .01, FadeOut(pcard), self.unveil(), run_time=.5)
            for k, w in enumerate(["nothing", "half", "one, then", "two, and"]):
                vo.wait_until(w)
                s = float(shifts[k])
                anims = [GrowFromEdge(bars[k], DOWN), FadeIn(vlabs[k])]
                if k:
                    ds = (s - float(shifts[k - 1])) * pl.sc
                    anims.append(truth.animate.shift(np.array([ds, ds, 0])))
                self.play(*anims, run_time=.45)
            prev = None
            for k, w in enumerate(["from zero", "point zero eight", "point two nine",
                                   "point eight five"]):
                vo.wait_until(w)
                anims = [bars[k].animate.set_fill(RED), vlabs[k].animate.set_color(RED)]
                if prev is not None:
                    anims += [bars[prev].animate.set_fill(INK), vlabs[prev].animate.set_color(INK)]
                self.play(*anims, run_time=.3)
                prev = k

        r2_box = VGroup()
        r2a = VGroup(left("R²", .95, 1.2, 30, INK, bold=True),
                     left("perfect prediction", 1.85, 1.2, 20, GRAY),
                     mono("1.0", 34, INK, bold=True).move_to([5.35, 1.2, 0]))
        r2b = VGroup(left("R²", .95, .35, 30, INK, bold=True),
                     left("cells shuffled", 1.85, .35, 20, GRAY),
                     mono("0.020", 34, RED, bold=True).move_to([5.2, .35, 0]))
        rtag = source_tag("MEASURED").move_to([5.3, 1.92, 0])
        r2t = left("R2Evaluation", .95, 1.92, 20, INK, bold=True)
        lines = VGroup(*[Line(pl.p(*xy[i]), pl.p(*xy[i]), color=GRAY, stroke_width=1.4)
                         for i in range(40)])
        lines_to = VGroup(*[Line(pl.p(*xy[i]), pl.p(*xy[perm[i]]), color=GRAY, stroke_width=1.4)
                            for i in range(40)])
        k = int(np.argmax(np.linalg.norm(xy - xy[perm], axis=1)))
        with self.say(2) as vo:
            self.cue(vo, .01, FadeOut(bars), FadeOut(vlabs), FadeOut(chart), FadeOut(meaning),
                     truth.animate.shift(np.array([-2, -2, 0]) * pl.sc),
                     Transform(leg[3], left("truth", -3.55, 1.92, 17, INK)), run_time=.7)
            self.play(FadeIn(r2t), FadeIn(rtag), FadeIn(r2a[:2]), run_time=.4)
            vo.wait_until("and it does")
            self.play(FadeIn(r2a[2], scale=1.2), run_time=.4)
            vo.wait_until("Shuffle")
            self.add(lines)
            self.play(*[pred[i].animate.move_to(pl.p(*xy[perm[i]])) for i in range(40)],
                      Transform(lines, lines_to), run_time=1.4)
            vo.wait_until("it drops")
            sh = base[perm]          # MMD of shuffled vs original cells (default gamma 0.1)
            mmd_same = rbf(sh, sh, .1).mean() + rbf(base, base, .1).mean() \
                - 2 * rbf(sh, base, .1).mean()
            assert abs(mmd_same) < 1e-9
            same_lab = left(f"same cloud · MMD still {abs(mmd_same):.0f} · R² 1.0 → 0.020", .95,
                            -1.75, 20, GRAY)
            self.play(FadeIn(r2b), FadeIn(same_lab, shift=UP * .05), run_time=.5)
            vo.wait_until("pairs cell one")
            pair = VGroup(Line(pl.p(*xy[k]), pl.p(*xy[perm[k]]), color=RED, stroke_width=4),
                          Dot(pl.p(*xy[k]), radius=.08, color=RED),
                          Circle(radius=.11, color=RED, stroke_width=3).move_to(pl.p(*xy[perm[k]])))
            pl_lab = VGroup(left("compares predicted cell i", .95, -.7, 21, RED),
                            left("with truth cell i, row by row", .95, -1.08, 21, RED))
            self.play(r2b[2].animate.set_color(INK), FadeIn(pair), FadeIn(pl_lab), run_time=.6)
            vo.wait_until("Remember")
            rem = red_box(pl_lab, .12)
            self.play(Create(rem), run_time=.5)

        imports = [(1, "import anndata as ad"), (2, "import numpy as np"), (3, "import pytest"),
                   (4, "from speciesot.speciesot_core import ("),
                   (5, "    MMDEvaluation, R2Evaluation)")]
        t_mmd = [(1, "def test_mmd_grows_with_shift():"),
                 (2, "    x = np.array([[0., 0.], [1., 1.]])"),
                 (3, "    mmd = MMDEvaluation.mmd_distance"),
                 (4, "    d = [mmd(x, x + s, 0.5) for s in (0, 1, 2)]"),
                 (5, "    assert d[0] < d[1] < d[2]")]
        t_one = [(1, "def test_r2_perfect_is_one():"),
                 (2, "    a = ad.AnnData(np.eye(10))"),
                 (3, "    r2 = R2Evaluation().evaluate(a, a)"),
                 (4, "    assert r2 == pytest.approx(1.0)")]
        t_shuf = [(1, "def test_r2_drops_when_cells_shuffled():"),
                  (2, "    a = ad.AnnData(np.eye(10))"),
                  (3, "    b = ad.AnnData(np.eye(10)[::-1])"),
                  (4, "    r2 = R2Evaluation().evaluate(b, a)"),
                  (5, "    assert r2 < 0.1")]
        wl, wr = 5.55, 6.85
        xl_, xr_ = -6.3 + wl / 2, 6.3 - wr / 2
        def ytop(n, top):          # panel centre so its frame top sits at `top`
            return top - (n * 16 * .0172 + .7) / 2
        p_imp = code_panel(imports, "EXAMPLE · Tests/test_known_answers.py", xl_,
                           ytop(5, 2.04), width=wl, size=16, numbers=False)
        p_mmd = code_panel(t_mmd, "shift ↑  →  MMD ↑", xr_, ytop(5, 2.04), width=wr, size=16,
                           numbers=False)
        p_one = code_panel(t_one, "perfect  →  R² = 1", xl_, ytop(4, -.18), width=wl, size=16,
                           numbers=False)
        p_shuf = code_panel(t_shuf, "shuffled  →  R² ≈ 0", xr_, ytop(5, -.18), width=wr,
                            size=16, numbers=False)
        panels = [p_imp, p_mmd, p_one, p_shuf]
        etags = VGroup(*[source_tag("EXAMPLE").scale(.8).move_to(
            [p.frame.get_right()[0] - .6, p.frame.get_top()[1] - .21, 0]) for p in panels[1:]])
        logic = VGroup(left("tiny arrays, built inside the test", -6.1, 1.6, 22, INK, bold=True),
                       left("no h5ad files · no cluster", -6.1, 1.1, 20, GRAY),
                       left("checks the logic, not the biology", -6.1, .55, 22, RED, bold=True))
        with self.say(3) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()], run_time=.45)
            self.play(LaggedStart(FadeIn(p_imp, shift=UP * .1),
                                  *[FadeIn(VGroup(p, t), shift=UP * .1)
                                    for p, t in zip(panels[1:], etags)], lag_ratio=.25),
                      run_time=1.2)
            self.settle(*panels, etags)
            vo.wait_until("notice the data")
            marks = VGroup(p_mmd.mark(2), p_one.mark(2), p_shuf.mark(2, 3))
            self.play(FadeIn(marks), run_time=.5)
            vo.wait_until("The test checks")
            self.play(FadeOut(p_imp), FadeIn(logic, shift=UP * .1), run_time=.6)
        self.finish()


# ---------------------------------------------------------------- S05

class S05(Ep):
    def construct(self):
        self.header()
        mouse, human, human7 = toy_cells()
        mx, hx, top, ch = -2.1, 2.1, 1.68, .22
        m_mat = matrix(mouse, mx, top, ch=ch)
        h_mat = matrix(human7, hx, top, ch=ch)
        m_lab = at("mouse test · 5 cells", mx, 1.92, 18, GRAY)
        h_lab = at("human test · 7 cells", hx, 1.92, 18, GRAY)
        r2c = chip("R2Evaluation", 0, -.25, INK, 22)
        into = VGroup(arrow(m_mat.frame.get_bottom() + DOWN * .02, r2c.get_top() + LEFT * .75, INK),
                      arrow(h_mat.frame.get_bottom() + DOWN * .02, r2c.get_top() + RIGHT * .75,
                            INK))
        with self.say(0) as vo:
            self.cue(vo, .03, FadeIn(r2c, shift=UP * .1), run_time=.5)
            vo.wait_until("In a real")
            self.play(FadeIn(m_lab), FadeIn(h_lab),
                      LaggedStart(*[FadeIn(r, shift=DOWN * .1) for r in m_mat.cells],
                                  lag_ratio=.15),
                      LaggedStart(*[FadeIn(r, shift=DOWN * .1) for r in h_mat.cells],
                                  lag_ratio=.12),
                      Create(m_mat.frame), Create(h_mat.frame), run_time=1.1)
            self.settle(m_mat, h_mat)
            self.play(GrowArrow(into[0]), GrowArrow(into[1]), run_time=.5)
            vo.wait_until("Pause and predict")
            pcard = ponder("5 个小鼠细胞对 7 个人类细胞，R2Evaluation 能接受吗？",
                           "5 mouse cells against 7 human cells: does R2Evaluation accept that?",
                           y=-1.47)
            self.play(self.veil(), run_time=.4)
            self.play(FadeIn(pcard, shift=UP * .1), run_time=.5)
        self.hold(0)                 # thinking time after the ponder question

        code = code_panel(rows(CORE, 311, 313), CORE_PATH, 2.6, 1.15, width=7.3, size=20)
        err = error_card("ValueError", ["operands could not be broadcast together",
                                        "with shapes (5,4) (7,4)"],
                         "speciesot_core.py:313 in evaluate", 2.6, -1.22, width=7.3, size=20)
        lm_x, lh_x, ltop = -5.3, -2.95, 1.5
        h5 = matrix(human, lh_x, ltop, ch=ch)            # the 5-cell human test set
        r2_55 = r2_score(mouse, human)                   # identity_end_to_end: 0.1030 (MEASURED)
        assert abs(r2_55 - 0.1030) < 5e-4
        res = VGroup(mono(f"R² = {r2_55:.3f}", 40, RED, bold=True).move_to([2.6, -.55, 0]),
                     at("no error · it pairs unrelated cells", 2.6, -1.25, 22, INK),
                     tag_at("MEASURED", 2.6, -1.8),
                     at("5 mouse vs 5 human toy cells", 2.6, -2.25, 17, GRAY))
        with self.say(1) as vo:
            self.cue(vo, .01, FadeOut(pcard), self.unveil(), FadeOut(r2c), FadeOut(into),
                     run_time=.4)
            vo.wait_until("We tried")
            m_mat.x, h_mat.x = lm_x, lh_x
            m_mat.top = h_mat.top = ltop
            self.play(m_mat.animate.move_to([lm_x, ltop - 5 * ch / 2, 0]),
                      h_mat.animate.move_to([lh_x, ltop - 7 * ch / 2, 0]),
                      Transform(m_lab, at("mouse · 5", lm_x, 1.75, 19, GRAY)),
                      Transform(h_lab, at("human · 7", lh_x, 1.75, 19, GRAY)),
                      FadeIn(code), run_time=.8)
            vo.wait_until("crashed")
            hl = highlight(self, code, 313, run_time=.3)
            self.play(FadeIn(err, shift=UP * .1), run_time=.5)
            vo.wait_until("Five rows")
            pairs = VGroup(*[Line([lm_x + .76, row_y(m_mat, i), 0], [lh_x - .76, row_y(h_mat, i), 0],
                                  color=INK, stroke_width=2) for i in range(5)])
            lost = VGroup(*[red_box(h_mat.cells[i], .0) for i in (5, 6)])
            qs = VGroup(*[at("?", lh_x - 1.05, row_y(h_mat, i), 24, RED, bold=True)
                          for i in (5, 6)])
            self.play(LaggedStart(*[Create(p_) for p_ in pairs], lag_ratio=.15), run_time=.8)
            self.settle(pairs)
            self.play(Create(lost), FadeIn(qs), run_time=.5)
            no = left("5 rows can't line up with 7", -6.2, -.45, 21, RED, bold=True)
            self.play(FadeIn(no), run_time=.4)
            vo.wait_until("five against five")
            self.play(FadeOut(lost), FadeOut(qs), FadeOut(no), FadeOut(err),
                      ReplacementTransform(h_mat, h5),
                      Transform(h_lab, at("human · 5", lh_x, 1.75, 19, GRAY)), run_time=.7)
            vo.wait_until("pairs unrelated")
            unrel = VGroup(left("row i ↔ row i:", -6.2, -.4, 21, RED, bold=True),
                           left("unrelated cells", -6.2, -.78, 21, RED, bold=True))
            self.play(pairs.animate.set_color(RED).set_stroke(width=3), FadeIn(unrel), run_time=.5)
            vo.wait_until("reports an R")
            self.play(FadeIn(res[0], shift=UP * .1), run_time=.5)
            self.play(FadeIn(res[1:]), pairs.animate.set_color(INK).set_stroke(width=2),
                      unrel.animate.set_color(INK), run_time=.5)

        # two R-squared formulas, side by side
        div = Line([0, 2.0, 0], [0, -2.4, 0], color=FAINT, stroke_width=1.5)
        L_head = left("per-gene R² · R2Evaluation", -6.2, 1.86, 22, INK, bold=True)
        L_tag = source_tag("READ IN CODE").move_to([-1.0, 1.47, 0])
        L_ref = VGroup(mono_left("same formula as _pergene_r2 in", -6.2, 1.47, 16, GRAY),
                       mono_left("atlas-paper-vae/scripts/02_eval_metrics.py:47", -6.2, 1.18,
                                 16, GRAY))
        R_head = left("R² of means · your benchmark", .3, 1.86, 22, INK, bold=True)
        R_tag = source_tag("READ IN CODE").move_to([5.45, 1.47, 0])
        R_ref = VGroup(mono_left("_r2_means in", .3, 1.47, 16, GRAY),
                       mono_left("cellot/…/decoded_frame_metrics.py:68", .3, 1.18, 16, GRAY))
        rng = np.random.default_rng(7)
        recon = mouse + rng.normal(0, .25, size=mouse.shape)     # a sketch of reconstructions
        ltop = .62
        cells_m = matrix(mouse, -4.85, ltop)
        recon_m = matrix(recon, -2.05, ltop)
        c_lab = at("cells", -4.85, ltop + .22, 17, GRAY)
        r_lab = at("their reconstructions (sketch)", -2.05, ltop + .22, 17, GRAY)
        own = VGroup(*[Line([-4.85 + .72, row_y(cells_m, i), 0], [-2.05 - .72, row_y(cells_m, i), 0],
                            color=INK, stroke_width=2) for i in range(5)])
        code_l = code_panel(rows(CORE, 311, 313), CORE_PATH, -3.25, -1.52, width=5.95, size=17)
        rm_x, rh_x = 1.45, 4.85
        mean_y = [-1.55, -2.02]
        m_mean = matrix(mouse.mean(0)[None, :], 3.15, mean_y[0] + .125)
        h_mean = matrix(human7.mean(0)[None, :], 3.15, mean_y[1] + .125)
        mean_lab = VGroup(left("mouse mean", 4.15, mean_y[0], 17, GRAY),
                          left("human mean", 4.15, mean_y[1], 17, GRAY))
        gene_ticks = VGroup(*[Line([3.15 - .54 + j * .36, mean_y[0] - .125, 0],
                                   [3.15 - .54 + j * .36, mean_y[1] + .125, 0], color=RED,
                                   stroke_width=3) for j in range(4)])
        with self.say(2) as vo:
            self.cue(vo, .01, FadeOut(res), FadeOut(pairs), FadeOut(unrel), FadeOut(hl),
                     FadeOut(m_lab), FadeOut(h_lab), FadeOut(m_mat), FadeOut(h5),
                     FadeIn(div), ReplacementTransform(code, code_l), run_time=.8)
            hl2 = highlight(self, code_l, 313, run_time=.3)
            vo.wait_until("It's the same")
            self.play(FadeIn(L_head), FadeIn(L_tag), FadeIn(L_ref), run_time=.6)
            vo.wait_until("where every cell")
            self.play(FadeIn(cells_m), FadeIn(recon_m), FadeIn(c_lab), FadeIn(r_lab), run_time=.5)
            self.play(LaggedStart(*[Create(o) for o in own], lag_ratio=.15), run_time=.7)
            self.settle(own)
            vo.wait_until("Your benchmark")
            m_mat2 = matrix(mouse, rm_x, ltop, ch=.24)
            h_mat2 = matrix(human7, rh_x, ltop, ch=.24)
            rm_lab = at("predicted (mouse) · 5", rm_x, ltop + .22, 17, GRAY)
            rh_lab = at("truth (human) · 7", rh_x, ltop + .22, 17, GRAY)
            self.play(FadeIn(R_head), FadeIn(R_tag), FadeIn(R_ref), FadeIn(m_mat2),
                      FadeIn(h_mat2), FadeIn(rm_lab), FadeIn(rh_lab), run_time=.7)
            vo.wait_until("average expression")
            self.play(ReplacementTransform(m_mat2.cells.copy(), m_mean),
                      ReplacementTransform(h_mat2.cells.copy(), h_mean), FadeIn(mean_lab),
                      run_time=1.0)
            self.play(Create(gene_ticks), run_time=.5)
            vo.wait_until("wouldn't even notice")
            order = [3, 0, 4, 1, 2]
            self.play(*[m_mat2.cells[i].animate.move_to([rm_x, row_y(m_mat2, order.index(i)), 0])
                        for i in range(5)],
                      *[recon_m.cells[i].animate.move_to([-2.05, row_y(cells_m, order.index(i)), 0])
                        for i in range(5)],
                      *[own[i].animate.put_start_and_end_on(
                          [-4.85 + .72, row_y(cells_m, i), 0],
                          [-2.05 - .72, row_y(cells_m, order.index(i)), 0]) for i in range(5)],
                      run_time=1.1)
            proof = left("shuffle-proof", .3, -2.12, 21, RED, bold=True)
            self.play(Create(red_box(VGroup(m_mean, h_mean), .06)), FadeIn(proof), run_time=.6)

        qn = at("Which R² does the experiment need?", 0, 1.55, 36, INK, bold=True)
        qzh = at("实验需要哪一种 R²？", 0, 1.0, 24, GRAY)
        optA = card("per-gene R²", "needs a true partner for every cell", -3.15, -.2, 5.6,
                    1.35)
        optB = card("R² of means", "gene averages · any cell counts", 3.15, -.2, 5.6, 1.35)
        cant = at("a test can't choose for you", 0, -1.25, 21, GRAY)
        hidden = DashedVMobject(Rectangle(width=5.4, height=.6, color=GRAY), num_dashes=40)\
            .move_to([0, -1.95, 0])
        hid_t = at("a hidden assumption", 0, -1.95, 22, GRAY)
        dec = Rectangle(width=6.4, height=.6, stroke_color=RED, stroke_width=3)\
            .move_to([0, -1.95, 0])
        dec_t = at("a decision, made on purpose", 0, -1.95, 22, RED, bold=True)
        with self.say(3) as vo:
            self.cue(vo, .01, *[FadeOut(m) for m in self.content()
                                if m not in (L_head, R_head)],
                     ReplacementTransform(L_head, optA), ReplacementTransform(R_head, optB),
                     run_time=.7)
            self.play(FadeIn(qn, shift=DOWN * .1), FadeIn(qzh), run_time=.5)
            vo.wait_until("can't answer")
            self.play(FadeIn(cant), run_time=.4)
            vo.wait_until("hidden assumption")
            self.play(Create(hidden), FadeIn(hid_t), run_time=.5)
            vo.wait_until("a decision")
            self.play(FadeOut(hidden), Create(dec), ReplacementTransform(hid_t, dec_t),
                      run_time=.7)
        self.finish()


# ---------------------------------------------------------------- S06

def tier(y0, y1, cx=-3.05, base_w=6.3, ybase=-2.35, yapex=2.4, color=INK):
    def w(y):
        return base_w * (yapex - y) / (yapex - ybase)
    pts = [[cx - w(y0) / 2, y0, 0], [cx + w(y0) / 2, y0, 0], [cx + w(y1) / 2, y1, 0],
           [cx - w(y1) / 2, y1, 0]]
    return Polygon(*pts, stroke_color=color, stroke_width=2.5, fill_color=PAPER, fill_opacity=1)


class S06(Ep):
    def construct(self):
        self.header()
        cx = -3.05
        spans = [(-2.35, -.95), (-.85, .55), (.65, 2.0)]
        tiers = VGroup(*[tier(a, b) for a, b in spans])
        names = VGroup(at("unit", cx, -1.45, 28, INK, bold=True),
                       at("integration", cx, .0, 26, INK, bold=True),
                       at("system", cx, 1.12, 22, INK, bold=True))
        subs = VGroup(at("单元测试", cx, -1.95, 19, GRAY), at("集成测试", cx, -.5, 19, GRAY),
                      at("系统", cx, .78, 17, GRAY))
        ax = .75
        ann = []
        rows_y = [-1.65, -.15, 1.33]
        texts = [("one class · toy arrays", "milliseconds"),
                 ("whole Experiment · tiny h5ad files", "seconds"),
                 ("e24_replica.ipynb · real atlas · cluster", "minutes to hours")]
        widths = [.2, .9, 2.3]
        counts = [("write many", 12), ("a handful", 3), ("once the rest is green", 1)]
        for (t1, t2), wbar, (cnt, n), y in zip(texts, widths, counts, rows_y):
            r1 = left(t1, ax, y + .42, 21, INK, bold=True)
            bar = Rectangle(width=wbar, height=.18, stroke_width=0, fill_color=INK,
                            fill_opacity=1).move_to([ax + wbar / 2, y, 0])
            r2 = left(t2, ax + wbar + .2, y, 19, GRAY)
            dotsg = VGroup(*[Dot([ax + .1 + i * .22, y - .4, 0], radius=.06, color=INK)
                             for i in range(n)])
            r3 = left(cnt, ax + .1 + n * .22 + .15, y - .4, 19, INK)
            ann.append(VGroup(r1, bar, r2, dotsg, r3))
        with self.say(0) as vo:
            self.cue(vo, .02, *[Create(t) for t in tiers], run_time=.8)
            vo.wait_until("At the bottom")
            self.play(tiers[0].animate.set_stroke(RED), FadeIn(names[0]), FadeIn(subs[0]),
                      run_time=.5)
            self.play(FadeIn(ann[0][0]), GrowFromEdge(ann[0][1], LEFT), FadeIn(ann[0][2]),
                      run_time=.6)
            vo.wait_until("Write many")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in ann[0][3]], lag_ratio=.08),
                      FadeIn(ann[0][4]), run_time=.8)
            self.settle(ann[0])

        toy = mono_left("Tests/toy_config.yaml", ax, -1.05, 19, INK)
        seed = left("the seed of this layer", ax, -1.42, 20, RED, bold=True)
        upd = VGroup(left("needs updating first:", ax, -1.82, 18, GRAY),
                     mono_left("setup() → KeyError: 'experiment'", ax, -2.15, 17, INK))
        upd.add(source_tag("MEASURED").scale(.9).next_to(upd[0], RIGHT, buff=.3))
        with self.say(1) as vo:
            self.cue(vo, .02, tiers[0].animate.set_stroke(INK), tiers[1].animate.set_stroke(RED),
                     FadeIn(names[1]), FadeIn(subs[1]), run_time=.5)
            vo.wait_until("the whole Experiment")
            self.play(FadeIn(ann[1][0]), run_time=.4)
            vo.wait_until("Seconds")
            self.play(GrowFromEdge(ann[1][1], LEFT), FadeIn(ann[1][2]), run_time=.6)
            vo.wait_until("A handful")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in ann[1][3]], lag_ratio=.2),
                      FadeIn(ann[1][4]), run_time=.6)
            self.settle(ann[1])
            vo.wait_until("toy_config")
            self.play(FadeOut(ann[0]), FadeIn(toy), FadeIn(seed), run_time=.5)
            vo.wait_until("brought up to date")
            self.play(FadeIn(upd, shift=UP * .08), run_time=.5)

        oks = VGroup(tick(0, 0, 30, INK).next_to(names[0], RIGHT, buff=.25),
                     tick(0, 0, 30, INK).next_to(names[1], RIGHT, buff=.2))
        with self.say(2) as vo:
            self.cue(vo, .02, tiers[1].animate.set_stroke(INK), tiers[2].animate.set_stroke(RED),
                     FadeIn(names[2]), FadeIn(subs[2]), FadeOut(toy), FadeOut(seed), FadeOut(upd),
                     FadeIn(ann[0]), run_time=.5)
            self.play(FadeIn(ann[2][0]), run_time=.4)
            vo.wait_until("minutes to hours")
            self.play(GrowFromEdge(ann[2][1], LEFT), FadeIn(ann[2][2]), run_time=.8)
            vo.wait_until("Run it once")
            self.play(LaggedStart(FadeIn(oks[0], scale=1.4), FadeIn(oks[1], scale=1.4),
                                  lag_ratio=.5), run_time=.7)
            self.settle(oks)
            self.play(FadeIn(ann[2][3]), FadeIn(ann[2][4]), run_time=.4)
            vo.wait_until("not instead")
            order = arrow([-5.85, -1.5, 0], [-5.85, 1.35, 0], RED)
            first = left("bottom up", -6.25, 1.62, 18, RED, bold=True)
            self.play(GrowArrow(order), FadeIn(first), run_time=.7)

        lx = 3.5
        steps = ["change one thing", "run pytest", "see green", "then: the notebook"]
        ys = [1.6, .45, -.7, -2.0]
        nodes = VGroup(*[chip(s, lx, y, INK if i < 3 else RED, 21, font=LATIN)
                         for i, (s, y) in enumerate(zip(steps, ys))])
        links = VGroup(*[Arrow(nodes[i].get_bottom(), nodes[i + 1].get_top(), buff=.08,
                               color=INK if i < 2 else RED, stroke_width=3,
                               max_tip_length_to_length_ratio=.3) for i in range(3)])
        tok = Dot([lx - 2.0, ys[0], 0], radius=.08, color=RED)
        back = CurvedArrow(nodes[2].get_right() + RIGHT * .05, nodes[0].get_right() + RIGHT * .05,
                           angle=PI / 1.6, color=GRAY, stroke_width=2.5, tip_length=.18)
        loop_lab = at("loop", lx + 2.45, .55, 19, GRAY)
        with self.say(3) as vo:
            self.cue(vo, .01, *[FadeOut(a) for a in ann], FadeOut(oks), FadeOut(order),
                     FadeOut(first),
                     tiers[2].animate.set_stroke(INK), run_time=.4)
            vo.wait_until("change one")
            self.play(FadeIn(nodes[0]), FadeIn(tok), run_time=.3)
            vo.wait_until("run pytest")
            self.play(GrowArrow(links[0]), FadeIn(nodes[1]), tok.animate.move_to([lx - 2.0, ys[1], 0]),
                      run_time=.35)
            vo.wait_until("see green")
            self.play(GrowArrow(links[1]), FadeIn(nodes[2]), Create(back), FadeIn(loop_lab),
                      tok.animate.move_to([lx - 2.0, ys[2], 0]), run_time=.45)
            vo.wait_until("only then")
            self.play(GrowArrow(links[2]), FadeIn(nodes[3]), Indicate(names[2], color=RED),
                      tok.animate.move_to([lx - 2.0, ys[3], 0]), run_time=.5)
        self.finish()


# ---------------------------------------------------------------- S07

class S07(Ep):
    def construct(self):
        self.header()

        def frame(x, accent=False):
            return Rectangle(width=6.0, height=2.0, stroke_color=RED if accent else INK,
                             stroke_width=2, fill_color=PAPER, fill_opacity=1).move_to([x, 1.0, 0])
        f1 = frame(-3.15, accent=True)
        t1 = left("a question with a known answer", -5.95, 1.62, 26, RED, 5.6, True)
        mini = terminal(["$ pytest", "."], -4.75, .6, width=2.0, size=20)
        runs = VGroup(left("finds and runs every", -3.45, .8, 20, GRAY),
                      left("test_* function", -3.45, .45, 20, GRAY))
        with self.say(0) as vo:
            self.cue(vo, .03, FadeIn(f1), FadeIn(t1, shift=UP * .08), run_time=.5)
            vo.wait_until("pytest finds")
            self.play(FadeIn(mini, shift=UP * .08), FadeIn(runs), run_time=.5)
            self.play(Indicate(mini.lines[1], color=RED, scale_factor=1.6), run_time=.5)

        f2 = frame(3.15, accent=True)
        t2 = left("known answers come from meaning", .35, 1.62, 26, RED, 5.6, True)
        dy = .78
        ring_pts = [(.55, dy + .12), (.75, dy - .1), (.95, dy + .18), (.62, dy - .25),
                    (1.0, dy - .05)]
        a1 = VGroup(*[Circle(radius=.075, color=GRAY, stroke_width=2).move_to([px, py, 0])
                      for px, py in ring_pts])
        b1 = VGroup(*[Dot([px, py, 0], radius=.05, color=INK) for px, py in ring_pts])\
            .shift(RIGHT * .55 + UP * .1)
        r1 = mono("= 0", 24, INK, bold=True).move_to([2.0, dy, 0])
        ys_ = [dy + .25, dy, dy - .25]
        p_l = VGroup(*[Dot([2.75, y, 0], radius=.055, color=GRAY) for y in ys_])
        p_r = VGroup(*[Dot([3.45, y, 0], radius=.055, color=INK) for y in ys_])
        p_ln = VGroup(*[Line([2.8, y, 0], [3.4, y, 0], color=INK, stroke_width=2) for y in ys_])
        r2 = mono("= 1", 24, INK, bold=True).move_to([4.05, dy, 0])
        bar = Rectangle(width=.28, height=.02, stroke_width=0, fill_color=INK,
                        fill_opacity=1).move_to([4.95, dy - .38, 0])
        r3 = mono("↑", 26, INK, bold=True).move_to([5.45, dy, 0])
        labs = VGroup(at("identical", 1.05, .23, 17, GRAY), at("perfect", 3.25, .23, 17, GRAY),
                      at("more shift", 5.15, .23, 17, GRAY))
        with self.say(1) as vo:
            self.cue(vo, .02, f1.animate.set_stroke(INK), t1.animate.set_color(INK),
                     mini.lines[1].animate.set_color("#D9D5CB"), FadeIn(f2),
                     FadeIn(t2, shift=UP * .08), run_time=.5)
            vo.wait_until("identical clouds")
            self.play(FadeIn(a1), FadeIn(b1), FadeIn(labs[0]), run_time=.3)
            self.play(b1.animate.move_to(a1.get_center()), FadeIn(r1), run_time=.6)
            vo.wait_until("a perfect")
            self.play(FadeIn(p_l), FadeIn(p_r), FadeIn(labs[1]), run_time=.3)
            self.play(Create(p_ln), FadeIn(r2), run_time=.5)
            vo.wait_until("more shift")
            self.play(FadeIn(bar), FadeIn(labs[2]), run_time=.2)
            self.play(bar.animate.stretch_to_fit_height(.78).move_to([4.95, dy, 0]),
                      FadeIn(r3), run_time=.6)

        ex_head = left("your exercises · 练习", -6.1, -.5, 24, INK, bold=True)
        tasks = ["turn each known answer into a test",
                 "move test_model.py's code into a test function that uses tiny files",
                 "decide which R² the experiment means"]
        boxes, tlabs = VGroup(), VGroup()
        for t, y in zip(tasks, [-1.05, -1.52, -1.99]):
            boxes.add(Square(side_length=.28, stroke_color=INK, stroke_width=2)
                      .move_to([-5.95, y, 0]))
            tlabs.add(left(t, -5.6, y, 22, INK))
        with self.say(2) as vo:
            self.cue(vo, .02, f2.animate.set_stroke(INK), t2.animate.set_color(INK),
                     FadeIn(ex_head), run_time=.4)
            for i, w in enumerate(["turn each", "move test_model", "decide which"]):
                vo.wait_until(w)
                anims = [FadeIn(boxes[i]), FadeIn(tlabs[i], shift=RIGHT * .1)]
                if i:
                    anims += [boxes[i - 1].animate.set_stroke(INK)]
                self.play(*anims, run_time=.45)
                self.play(boxes[i].animate.set_stroke(RED, 3), run_time=.2)
        self.finish()
