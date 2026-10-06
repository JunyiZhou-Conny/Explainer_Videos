"""S07 · The Laplace mechanism — the heart of the paper (Example 1, Proposition 1).

Beats: the Laplace density -> two worlds 41 / 42 -> their log ratio swept out (bounded by the
shift over the scale) -> on a log scale the densities are tents of slope 1/lambda, and the gap
between tents is the log ratio -> the one-line proof with a number line of distances ->
Proposition 1 (vector noise, L1 diamonds) -> ponder: uniform noise? -> its edges give an infinite
ratio -> a Gaussian's parabolas drift apart without bound -> the recipe noise scale = S(f)/eps.
"""

import numpy as np
from manim import *

from explainer import i18n
from explainer import style as S
from explainer.components import laplace_pdf, ponder_card
from explainer.scene import VoiceScene

from common import EPS_COLOR, NARRATION, NOISE_COLOR, SENS_COLOR, X_COLOR, XP_COLOR

SAY = NARRATION["S07"]
LAM = 1.0            # Laplace scale used in the pictures (so 1/lambda = 1)
A, B = 41.0, 42.0    # f(x), f(x')
T0, T1 = 36.0, 47.0  # visible output range
LOG_LO, LOG_HI = -6.3, -0.3     # y-range of the log-density panel
LN2PI_HALF = 0.5 * np.log(2 * np.pi)


def log_ratio(t, a=A, b=B, lam=LAM):
    """ln[h(t-a)/h(t-b)] for Laplace(lam): (|t-b| - |t-a|)/lam."""
    return (abs(t - b) - abs(t - a)) / lam


def log_lap(t, mu, lam=LAM):
    return -abs(t - mu) / lam - np.log(2 * lam)


def log_gauss(t, mu, sigma=1.0):
    return -0.5 * ((t - mu) / sigma) ** 2 - np.log(sigma) - LN2PI_HALF


class Panel(VGroup):
    """A plot area over t in [t0, t1] with its own t-axis.

    c2p(t, y) maps with the panel's y-range; mapper(y0, y1) gives the map for another y-range over
    the same rectangle (so one drawn axis can carry a density and then a log density)."""

    def __init__(self, t0, t1, y0, y1, width, height, axis_y=None, tick_labels=True):
        super().__init__()
        self.t0, self.t1, self.y0, self.y1 = t0, t1, y0, y1
        self.ref = Rectangle(width=width, height=height).set_stroke(opacity=0).set_fill(opacity=0)
        self.add(self.ref)
        ay = y0 if axis_y is None else axis_y
        self.axis = Line(self.c2p(t0, ay), self.c2p(t1, ay), color=S.GREY, stroke_width=2)
        self.yaxis = Line(self.c2p(t0, y0), self.c2p(t0, y1), color=S.GREY, stroke_width=2)
        vals = range(int(np.ceil(t0)) + 1, int(np.floor(t1)))
        self.ticks = VGroup(*[Line(UP * 0.06, DOWN * 0.06, color=S.GREY, stroke_width=2)
                              .move_to(self.c2p(v, ay)) for v in vals])
        self.add(self.axis, self.yaxis, self.ticks)
        if tick_labels:
            self.labels = VGroup(*[S.text(str(v), 20, S.GREY).next_to(self.c2p(v, ay), DOWN, buff=0.12)
                                   for v in vals])
            self.add(self.labels)

    def mapper(self, y0, y1):
        def c2p(t, y):
            dl = self.ref.get_corner(DL)
            return dl + np.array([(t - self.t0) / (self.t1 - self.t0) * self.ref.width,
                                  (y - y0) / (y1 - y0) * self.ref.height, 0.0])
        return c2p

    def c2p(self, t, y):
        return self.mapper(self.y0, self.y1)(t, y)

    def plot(self, f, a=None, b=None, step=0.01, kinks=(), color=S.WHITE, sw=5, c2p=None):
        a = self.t0 if a is None else a
        b = self.t1 if b is None else b
        c2p = c2p or self.c2p
        ts = np.r_[np.arange(a, b, step), b, [k for k in kinks if a < k < b]]
        ts = np.unique(np.round(ts, 6))
        return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(
            [c2p(t, f(t)) for t in ts])


def area_under(panel, f, color, opacity=0.12, step=0.02):
    """Light fill under a density on a panel (S08 draws its two worlds' Laplace curves this way)."""
    ts = np.unique(np.round(np.r_[np.arange(panel.t0, panel.t1, step), panel.t1, A, B], 6))
    pts = [panel.c2p(t, f(t)) for t in ts] + [panel.c2p(panel.t1, 0), panel.c2p(panel.t0, 0)]
    return Polygon(*pts, stroke_width=0).set_fill(color, opacity)


def probe_line(panel, tracker, y0, y1):
    """Vertical dashed line at t = tracker over a panel; built once, moved by an updater."""
    line = DashedLine(panel.c2p(panel.t0, y0), panel.c2p(panel.t0, y1), color=S.GREY, stroke_width=2,
                      dash_length=0.08)
    line.add_updater(lambda m: m.move_to(panel.c2p(tracker.get_value(), (y0 + y1) / 2)))
    return line.update()


def bracket(p0, p1, color, sw=4, tick=0.1):
    """|----| between two points (a distance bracket)."""
    return VGroup(Line(p0, p1, color=color, stroke_width=sw),
                  Line(p0 + DOWN * tick, p0 + UP * tick, color=color, stroke_width=sw),
                  Line(p1 + DOWN * tick, p1 + UP * tick, color=color, stroke_width=sw))


def ponder_at(scene, question, pos, width, size=S.BODY_SIZE) -> VGroup:
    """The ponder card of explainer.components.pause_and_ponder, faded in at `pos` (timer not started)."""
    card = ponder_card(question, width=width, size=size).move_to(pos)
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    return card


def drain(scene, card, seconds: float) -> None:
    """The silent ponder timer of pause_and_ponder, for a card already on screen."""
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)


def random_row_thumb() -> VGroup:
    """Thumbnail of S05's verdict on 'publish one random row': 1/n in one world, 0 in the other, a RED x."""
    frame = RoundedRectangle(width=3.3, height=2.0, corner_radius=0.12, stroke_color=S.GREY,
                             stroke_width=2).set_fill(S.GREY_DARKER, 0.95)
    c = frame.get_center()
    title = S.text("publish a random row", 20, S.GREY).move_to(frame.get_top() + DOWN * 0.3)
    base = Line(LEFT * 0.6, RIGHT * 0.6, color=S.GREY, stroke_width=2).move_to(c + LEFT * 0.45 + DOWN * 0.55)
    bar = Rectangle(width=0.3, height=0.65, stroke_width=0).set_fill(XP_COLOR, 0.9)
    bar.next_to(base.get_center() + LEFT * 0.3, UP, buff=0)
    zero = Line(ORIGIN, RIGHT * 0.3, color=X_COLOR, stroke_width=6).move_to(base.get_center() + RIGHT * 0.3)
    n_lab = S.math("1/n", size=26, color=XP_COLOR).next_to(bar, UP, buff=0.08)
    z_lab = S.math("0", size=26, color=X_COLOR).next_to(zero, UP, buff=0.08)
    cross = Cross(Square(0.55), stroke_color=S.RED, stroke_width=7).move_to(c + RIGHT * 0.95 + DOWN * 0.2)
    return VGroup(frame, title, base, bar, zero, n_lab, z_lab, cross)


class LaplaceMechanism(VoiceScene):
    def construct(self):
        # ============================================================ 0. the Laplace density
        ax0 = Axes(x_range=[-6, 6, 1], y_range=[0, 1.05, 0.5], x_length=10, y_length=4.2,
                   tips=False, axis_config={"color": S.GREY, "stroke_width": 2},
                   x_axis_config={"include_ticks": True}).shift(DOWN * 0.8)
        lam = ValueTracker(1.0)
        curve0 = always_redraw(lambda: ax0.plot(
            lambda y: laplace_pdf(y, 0, lam.get_value()), x_range=[-6, 6, 0.01],
            color=NOISE_COLOR, stroke_width=5))
        formula0 = S.math(r"h(y)", r"\;\propto\;", r"e^{-|y|/\lambda}", size=54)
        formula0[2].set_color(NOISE_COLOR)
        formula0.to_edge(UP, buff=0.6)
        title0 = S.text("The Laplace distribution", 36, S.WHITE).next_to(formula0, DOWN, buff=0.25)
        lam_pos = ax0.c2p(4.2, 0.85)
        lam_label = always_redraw(lambda: VGroup(
            S.math(r"\lambda =", size=40, color=NOISE_COLOR),
            DecimalNumber(lam.get_value(), num_decimal_places=1, font_size=40, color=NOISE_COLOR),
        ).arrange(RIGHT, buff=0.15).move_to(lam_pos))
        scale_lab = S.text("scale", 24, S.GREY).next_to(lam_pos, DOWN, buff=0.35)
        mirror = DashedLine(ax0.c2p(0, 0), ax0.c2p(0, 0.62), color=S.GREY, stroke_width=2)
        half = ax0.plot(lambda y: laplace_pdf(y, 0, 1.0), x_range=[-6, 0, 0.01], color=S.WHITE,
                        stroke_width=5)

        with self.voiceover(SAY[0]) as vo:
            self.play(Create(ax0), Write(formula0), run_time=1.2)
            self.play(Create(curve0), FadeIn(title0), run_time=1.4)
            vo.wait_until("symmetric")
            self.play(Create(mirror), FadeIn(half), run_time=0.4)
            self.play(half.animate.flip(UP, about_point=ax0.c2p(0, 0)), run_time=0.7)
            self.play(FadeOut(half), FadeOut(mirror), Flash(ax0.c2p(0, 0.5), color=NOISE_COLOR,
                                                              flash_radius=0.35), run_time=0.6)
            vo.wait_until("falling off exponentially")
            self.play(Indicate(formula0[2], color=NOISE_COLOR), run_time=1.0)
            vo.wait_until("Its width")
            self.add(lam_label)
            self.play(FadeIn(scale_lab), lam.animate.set_value(2.0), run_time=0.9)
            self.play(lam.animate.set_value(0.6), run_time=0.9)
            self.play(lam.animate.set_value(1.0), run_time=vo.remaining(0.6))
        curve0.clear_updaters()
        lam_label.clear_updaters()
        self.play(FadeOut(VGroup(ax0, curve0, lam_label, title0, scale_lab)),
                  formula0.animate.scale(0.75).to_corner(UR, buff=0.55), run_time=0.8)

        # ============================================================ 1. two worlds: 41 vs 42
        top = Panel(T0, T1, 0, 0.6, 11.5, 2.4).move_to([0, 1.45, 0])
        dens_lab = S.text("density", 22, S.GREY).next_to(top.c2p(T0, 0.6), RIGHT, buff=0.15).shift(DOWN * 0.15)
        out_lab = S.math("t", size=30, color=S.GREY).next_to(top.c2p(T1, 0), RIGHT, buff=0.15)
        pdf_a = top.plot(lambda t: laplace_pdf(t, A, LAM), kinks=[A], color=X_COLOR, sw=4)
        pdf_b = top.plot(lambda t: laplace_pdf(t, B, LAM), kinks=[B], color=XP_COLOR, sw=4)
        area_a = area_under(top, lambda t: laplace_pdf(t, A, LAM), X_COLOR)
        area_b = area_under(top, lambda t: laplace_pdf(t, B, LAM), XP_COLOR)
        stem_a = DashedLine(top.c2p(A, 0), top.c2p(A, laplace_pdf(A, A, LAM)), color=X_COLOR, stroke_width=2,
                            dash_length=0.06)
        stem_b = DashedLine(top.c2p(B, 0), top.c2p(B, laplace_pdf(B, B, LAM)), color=XP_COLOR, stroke_width=2,
                            dash_length=0.06)
        lab_a = S.math(r"f(x) = 41", size=34, color=X_COLOR).next_to(top.c2p(A, 0.5), LEFT, buff=0.35)
        lab_b = S.math(r"f(x') = 42", size=34, color=XP_COLOR).next_to(top.c2p(B, 0.5), RIGHT, buff=0.35)
        m_a = S.math("M(x)", size=32, color=X_COLOR).move_to(top.c2p(38.4, 0.17))
        m_b = S.math("M(x')", size=32, color=XP_COLOR).move_to(top.c2p(44.7, 0.17))

        with self.voiceover(SAY[1]) as vo:
            self.play(Create(top), FadeIn(dens_lab), FadeIn(out_lab), run_time=1.0)
            vo.wait_until("Center one")
            self.play(Create(pdf_a), FadeIn(area_a), Create(stem_a), FadeIn(lab_a, shift=DOWN * 0.1), run_time=1.3)
            vo.wait_until("and another")
            self.play(Create(pdf_b), FadeIn(area_b), Create(stem_b), FadeIn(lab_b, shift=DOWN * 0.1), run_time=1.3)
            vo.wait_until("the output distributions")
            self.play(FadeIn(m_a, shift=UP * 0.1), FadeIn(m_b, shift=UP * 0.1), run_time=0.7)
            self.play(ShowPassingFlash(pdf_a.copy().set_stroke(X_COLOR, 9), time_width=0.5),
                      ShowPassingFlash(pdf_b.copy().set_stroke(XP_COLOR, 9), time_width=0.5),
                      run_time=vo.remaining(0.8))

        # ============================================================ 2. the log ratio, swept out
        bot = Panel(T0, T1, -2, 2, 11.5, 2.6, axis_y=0, tick_labels=False).move_to([0, -2.05, 0])
        bot_lab = S.math(r"\ln\big[\,h(t-", "41", r")\,/\,h(t-", "42", r")\,\big]", size=30)
        bot_lab[1].set_color(X_COLOR)
        bot_lab[3].set_color(XP_COLOR)
        bot_lab.next_to(bot.c2p(T0, -1.5), RIGHT, buff=0.2)
        hi = bot.c2p(T0, 1 / LAM)[1]
        lo = bot.c2p(T0, -1 / LAM)[1]
        band = Rectangle(width=bot.ref.width, height=hi - lo, stroke_width=0).set_fill(EPS_COLOR, 0.08)
        band.move_to(bot.c2p((T0 + T1) / 2, 0))
        band_hi = DashedLine(bot.c2p(T0, 1 / LAM), bot.c2p(T1, 1 / LAM), color=EPS_COLOR, stroke_width=3)
        band_lo = DashedLine(bot.c2p(T0, -1 / LAM), bot.c2p(T1, -1 / LAM), color=EPS_COLOR, stroke_width=3)
        hi_lab = S.math(r"+1/\lambda", size=30, color=EPS_COLOR).next_to(band_hi, RIGHT, buff=0.1)
        lo_lab = S.math(r"-1/\lambda", size=30, color=EPS_COLOR).next_to(band_lo, RIGHT, buff=0.1)
        shift_lab = S.math(r"\text{shift}/\text{scale} = (", "42", "-", "41", r")/\lambda", size=32,
                           color=EPS_COLOR)
        shift_lab[1].set_color(XP_COLOR)
        shift_lab[3].set_color(X_COLOR)
        shift_lab.move_to(bot.c2p(44.2, 1.5))        # above the +1/lambda line, left of the parked probe

        t = ValueTracker(T0 + 0.3)
        probe_top = probe_line(top, t, 0, 0.52)          # stops below the 'density' label
        probe_bot = probe_line(bot, t, -1.15, 2)         # stays clear of the panel label below -1
        dot_a = always_redraw(lambda: Dot(top.c2p(t.get_value(), laplace_pdf(t.get_value(), A, LAM)),
                                          color=X_COLOR, radius=0.07))
        dot_b = always_redraw(lambda: Dot(top.c2p(t.get_value(), laplace_pdf(t.get_value(), B, LAM)),
                                          color=XP_COLOR, radius=0.07))
        dot_r = always_redraw(lambda: Dot(bot.c2p(t.get_value(), log_ratio(t.get_value())),
                                          color=S.WHITE, radius=0.07))
        trace = TracedPath(dot_r.get_center, stroke_color=S.WHITE, stroke_width=4)
        ratio_graph = bot.plot(log_ratio, T0 + 0.3, T1 - 0.3, kinks=[A, B], color=S.WHITE, sw=4)
        ramp = bot.plot(log_ratio, A, B, color=S.YELLOW, sw=8)

        with self.voiceover(SAY[2]) as vo:
            self.play(Create(bot), FadeIn(bot_lab), run_time=1.0)
            self.play(FadeIn(VGroup(probe_top, probe_bot, dot_a, dot_b, dot_r)), run_time=0.4)
            self.add(trace)
            vo.wait_until("To the left")
            self.play(t.animate.set_value(A), run_time=vo.until("To the right"), rate_func=linear)
            self.play(t.animate.set_value(B), run_time=1.2, rate_func=linear)
            self.play(t.animate.set_value(T1 - 0.3), run_time=vo.until("In between", 1.2), rate_func=linear)
            self.add(ratio_graph)
            self.remove(trace)
            self.play(Create(ramp), run_time=0.8)
            self.play(FadeOut(ramp), run_time=0.4)
            vo.wait_until("It never rises")
            self.play(FadeIn(band), Create(band_hi), FadeIn(hi_lab), run_time=0.8)
            vo.wait_until("and never falls")
            self.play(Create(band_lo), FadeIn(lo_lab), run_time=0.8)
            vo.wait_until("the shift, divided")
            self.play(FadeIn(shift_lab, shift=DOWN * 0.15), run_time=0.8)
            self.play(Indicate(VGroup(hi_lab, lo_lab), color=EPS_COLOR), run_time=vo.remaining(0.6))
        for m in (probe_top, probe_bot, dot_a, dot_b, dot_r):
            m.clear_updaters()
        self.play(FadeOut(VGroup(probe_top, probe_bot, dot_a, dot_b, dot_r, shift_lab)), run_time=0.4)

        # ============================================================ 3. log scale: tents
        L = top.mapper(LOG_LO, LOG_HI)

        def clipped(f, mu, reach):
            """t-range around mu where the log density stays inside the panel."""
            return max(T0, mu - reach), min(T1, mu + reach)

        lap_reach = (-np.log(2 * LAM) - LOG_LO) * LAM

        def tent(mu, col, sw=5):
            a, b = clipped(log_lap, mu, lap_reach)
            return top.plot(lambda s: log_lap(s, mu), a, b, kinks=[mu], color=col, sw=sw, c2p=L)

        tent_a = tent(A, X_COLOR)
        mu_b = ValueTracker(A)
        tent_b = always_redraw(lambda: tent(mu_b.get_value(), XP_COLOR))
        log_lab = S.text("log density", 22, S.GREY).move_to(dens_lab, aligned_edge=LEFT)
        formula_log = S.math(r"\ln h(y)", "=", r"-|y|/\lambda", r"+\,c", size=40)
        formula_log[2].set_color(NOISE_COLOR)
        formula_log.to_corner(UR, buff=0.55)

        def slope_label(tex, t_at, side):
            p, q = L(t_at - 0.5, log_lap(t_at - 0.5, A)), L(t_at + 0.5, log_lap(t_at + 0.5, A))
            ang = np.arctan2(q[1] - p[1], q[0] - p[0])
            lab = S.math(tex, size=28, color=S.WHITE).rotate(ang)
            normal = np.array([-np.sin(ang), np.cos(ang), 0.0])
            return lab.move_to((p + q) / 2 + side * 0.3 * normal)

        slope_l = slope_label(r"\text{slope } +1/\lambda", 39.9, +1)     # clear of the probe parked at 38.5
        slope_r = slope_label(r"\text{slope } -1/\lambda", 44.6, -1)

        probe = ValueTracker(38.5)

        def gap_value():
            p = probe.get_value()
            return log_lap(p, A) - log_lap(p, mu_b.get_value())

        def gap_arrow():
            p = probe.get_value()
            if abs(gap_value()) < 0.12:
                return VGroup()
            return DoubleArrow(L(p, log_lap(p, mu_b.get_value())), L(p, log_lap(p, A)), buff=0,
                               color=EPS_COLOR, stroke_width=4, tip_length=0.13,
                               max_tip_length_to_length_ratio=0.45)

        gap = always_redraw(gap_arrow)
        gap_note = S.math(r"|\text{gap}| \le \text{slide} \times 1/\lambda", size=34, color=EPS_COLOR)
        gap_note.move_to([-5.75, 3.2, 0], aligned_edge=LEFT)
        probe_bot2 = probe_line(bot, probe, -1.15, 2)
        dot_g = always_redraw(lambda: Dot(bot.c2p(probe.get_value(), log_ratio(probe.get_value())),
                                          color=EPS_COLOR, radius=0.08))
        principle = S.text("privacy needs noise whose log density is never steep", 30, S.WHITE)
        principle.to_edge(UP, buff=0.4)

        with self.voiceover(SAY[3]) as vo:
            self.play(ReplacementTransform(pdf_a, tent_a), FadeOut(pdf_b),
                      FadeOut(VGroup(lab_a, lab_b, m_a, m_b, area_a, area_b, stem_a, stem_b)),
                      FadeTransform(dens_lab, log_lab), run_time=1.4)
            vo.wait_until("On a log scale")
            self.play(ReplacementTransform(formula0, formula_log), run_time=1.0)
            vo.wait_until("a tent whose sides")
            self.play(FadeIn(slope_l, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(slope_r, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("never steeper")
            self.play(Indicate(VGroup(slope_l, slope_r), color=S.WHITE, scale_factor=1.1), run_time=0.9)
            vo.wait_until("Slide the tent")
            self.add(tent_b, gap)
            self.play(mu_b.animate.set_value(B), run_time=1.6)
            self.play(FadeIn(gap_note, shift=UP * 0.1), run_time=0.6)
            # the gap at each t is exactly the log ratio plotted below: sweep the probe through it
            self.play(FadeIn(probe_bot2), FadeIn(dot_g), run_time=0.3)
            self.play(probe.animate.set_value(45.5), run_time=vo.until("That is the whole", 2.0),
                      rate_func=smooth)
            self.play(FadeOut(VGroup(formula_log, gap_note)), run_time=0.35)
            self.play(FadeIn(principle, shift=DOWN * 0.15), run_time=0.6)
            self.play(ShowPassingFlash(tent_a.copy().set_stroke(X_COLOR, 10), time_width=0.4),
                      ShowPassingFlash(tent_b.copy().set_stroke(XP_COLOR, 10), time_width=0.4),
                      run_time=vo.remaining(0.6))
        for m in (tent_b, gap, probe_bot2, dot_g):
            m.clear_updaters()
        # clear the plots between the two clips (the principle stays), so the proof starts on its first words
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not principle])), run_time=0.5)

        # ============================================================ 4. the one-line proof
        fx, fxp = r"f(x)", r"f(x')"
        l1 = S.math(r"\left|\,\ln\frac{h(t-", fx, r")}{h(t-", fxp, r")}\,\right|", r"=",
                    r"\frac{\big|\,|t-", fxp, r"|-|t-", fx, r"|\,\big|}{\lambda}", size=42)
        l2 = S.math(r"\le", r"\frac{|", fx, "-", fxp, r"|}{\lambda}", size=42)
        l3 = S.math(r"\le", r"\frac{S(f)}{\lambda}", size=42)
        for line in (l1, l2):
            for part in line:
                if part.get_tex_string() == fx:
                    part.set_color(X_COLOR)
                elif part.get_tex_string() == fxp:
                    part.set_color(XP_COLOR)
        l3[1][0:4].set_color(SENS_COLOR)
        l1.move_to([0, 2.75, 0])
        l2.next_to(l1, DOWN, buff=0.35)
        l2.shift(RIGHT * (l1[5].get_left()[0] - l2[0].get_left()[0]))
        l3.next_to(l2, DOWN, buff=0.3)
        l3.shift(RIGHT * (l1[5].get_left()[0] - l3[0].get_left()[0]))
        tri = S.text("triangle inequality", 24, S.GREY).next_to(l2, RIGHT, buff=0.5)
        sens = S.text("sensitivity", 24, SENS_COLOR).next_to(l3, RIGHT, buff=0.5)

        nl = NumberLine(x_range=[35.5, 45.5, 1], length=10, color=S.GREY, stroke_width=2,
                        include_ticks=True, tick_size=0.06).move_to([0, -2.6, 0])
        tt = ValueTracker(38.0)
        H_B, H_O = 0.42, 1.2

        t_glyph = S.math("t", size=32)

        def t_dot():
            return VGroup(Dot(nl.n2p(tt.get_value()), color=S.WHITE, radius=0.09),
                          t_glyph.copy().next_to(nl.n2p(tt.get_value()), DOWN, buff=0.2))

        dot_t = always_redraw(t_dot)
        dot_fx = VGroup(Dot(nl.n2p(A), color=X_COLOR, radius=0.09),
                        S.math("f(x)", size=30, color=X_COLOR).next_to(nl.n2p(A), DOWN, buff=0.2))
        dot_fxp = VGroup(Dot(nl.n2p(B), color=XP_COLOR, radius=0.09),
                         S.math("f(x')", size=30, color=XP_COLOR).next_to(nl.n2p(B), DOWN, buff=0.2))
        dot_fx[1].shift(LEFT * 0.12)
        dot_fxp[1].shift(RIGHT * 0.12)

        def dist(c, h, col, tex):
            glyph = S.math(tex, size=28, color=col)

            def make():
                a, b = sorted([tt.get_value(), c])
                br = bracket(nl.n2p(a) + UP * h, nl.n2p(b) + UP * h, col)
                return VGroup(br, glyph.copy().next_to(br, UP, buff=0.1))
            return make

        d_blue = always_redraw(dist(A, H_B, X_COLOR, r"|t-f(x)|"))
        d_orng = always_redraw(dist(B, H_O, XP_COLOR, r"|t-f(x')|"))
        extra = Line(nl.n2p(A) + UP * H_O, nl.n2p(B) + UP * H_O, color=S.WHITE, stroke_width=9)
        guide = DashedLine(nl.n2p(A) + UP * H_B, nl.n2p(A) + UP * H_O, color=S.GREY, stroke_width=2,
                           dash_length=0.06)
        extra_lab = S.math(r"\text{differ by} \le |f(x)-f(x')|", size=28).next_to(extra, RIGHT, buff=0.25)
        diff_txt = S.math(r"|t-", "f(x')", r"|-|t-", "f(x)", r"| =", size=28).move_to([-4.3, -0.95, 0])
        diff_txt[1].set_color(XP_COLOR)
        diff_txt[3].set_color(X_COLOR)
        diff_num = always_redraw(lambda: DecimalNumber(log_ratio(tt.get_value()), num_decimal_places=2,
                                                       include_sign=True, font_size=30)
                                 .next_to(diff_txt, RIGHT, buff=0.12))

        sub = S.math(r"\lambda = \frac{S(f)}{\varepsilon}", r"\quad\Longrightarrow\quad",
                     r"\left|\ln\frac{\Pr[M(x)=t]}{\Pr[M(x')=t]}\right|", r"\le", r"\varepsilon", size=44)
        sub[0][2:6].set_color(SENS_COLOR)
        sub[0][-1].set_color(EPS_COLOR)
        sub[4].set_color(EPS_COLOR)
        frac = sub[2]
        bar_g = max(frac, key=lambda m: m.width / max(m.height, 1e-3))
        num = [m for m in frac if m is not bar_g and m.get_y() > bar_g.get_y()
               and bar_g.get_left()[0] - 0.01 <= m.get_x() <= bar_g.get_right()[0] + 0.01]
        den = [m for m in frac if m is not bar_g and m.get_y() < bar_g.get_y()
               and bar_g.get_left()[0] - 0.01 <= m.get_x() <= bar_g.get_right()[0] + 0.01]
        VGroup(*sorted(num, key=lambda m: m.get_x())[3:7]).set_color(X_COLOR)     # M(x)
        VGroup(*sorted(den, key=lambda m: m.get_x())[3:8]).set_color(XP_COLOR)    # M(x')
        sub.move_to([0, -1.75, 0])
        box = SurroundingRectangle(sub, color=EPS_COLOR, buff=0.2, corner_radius=0.1)
        every = S.text("for every output t and every pair of neighbors", 26, S.GREY).next_to(box, DOWN, buff=0.3)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(principle), Write(l1), Create(nl), FadeIn(dot_fx), FadeIn(dot_fxp), FadeIn(dot_t),
                      run_time=vo.until("two distances to t", 0.8))
            self.play(FadeIn(d_blue, shift=UP * 0.1), FadeIn(d_orng, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("at most the distance")
            self.play(Create(guide), Create(extra), FadeIn(extra_lab, shift=LEFT * 0.15), run_time=0.6)
            self.play(Write(l2), FadeIn(tri, shift=LEFT * 0.2), run_time=0.9)
            vo.wait_until("So the privacy loss")
            # 'any output': drag t across the centres; the difference of distances never leaves [-1, +1]
            self.play(FadeOut(VGroup(extra, guide, extra_lab)), FadeIn(diff_txt), FadeIn(diff_num), run_time=0.4)
            self.play(tt.animate.set_value(44.5), run_time=2.0, rate_func=smooth)
            vo.wait_until("the sensitivity divided")
            self.play(Write(l3), FadeIn(sens, shift=LEFT * 0.2), run_time=1.0)
            self.play(Indicate(l3[1], color=SENS_COLOR, scale_factor=1.15), run_time=1.0)
            vo.wait_until("Set lambda")
            for m in (dot_t, d_blue, d_orng, diff_num):
                m.clear_updaters()
            self.play(FadeOut(VGroup(nl, dot_t, dot_fx, dot_fxp, d_blue, d_orng, diff_txt, diff_num)),
                      run_time=0.5)
            self.play(Write(sub), run_time=1.8)
            vo.wait_until("for every output")
            self.play(FadeIn(every, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("Privacy, proven")
            self.play(Create(box), run_time=0.8)

        # ============================================================ 5. vectors: Proposition 1
        prop_title = S.text("Proposition 1", 30, S.YELLOW, weight="BOLD")
        prop = S.math(r"M(x) = f(x) + (Y_1, \dots, Y_d)", size=40)
        prop2 = S.math(r"Y_i \sim \mathrm{Lap}\!\left(", r"S(f)", "/", r"\varepsilon", r"\right)\ \text{i.i.d.}",
                       size=40)
        prop2[1].set_color(SENS_COLOR)
        prop2[3].set_color(EPS_COLOR)
        card = VGroup(prop_title, prop, prop2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        card.to_edge(LEFT, buff=0.9).shift(DOWN * 0.6)
        frame = SurroundingRectangle(card, color=S.GREY, buff=0.3, corner_radius=0.12)

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=4.4, y_length=4.4,
                            background_line_style={"stroke_color": S.GREY_DARK, "stroke_width": 1},
                            axis_config={"stroke_color": S.GREY}).to_edge(RIGHT, buff=0.9).shift(DOWN * 0.55)
        ca, cb = (-0.5, -0.4), (0.5, 0.4)

        def diamonds(c, col):
            g = VGroup()
            for r, op in [(0.5, 1.0), (1.0, 0.7), (1.5, 0.45), (2.0, 0.25)]:
                pts = [plane.c2p(c[0] + r, c[1]), plane.c2p(c[0], c[1] + r), plane.c2p(c[0] - r, c[1]),
                       plane.c2p(c[0], c[1] - r)]
                g.add(Polygon(*pts, color=col, stroke_width=3, stroke_opacity=op))
            g.add(Dot(plane.c2p(*c), color=col, radius=0.07))
            return g

        dz = diamonds(ca, X_COLOR)
        dzp = diamonds(cb, XP_COLOR)
        l1_note = S.math(r"\text{density} \propto e^{-\|y-f(x)\|_1/\lambda}", size=32).next_to(plane, UP, buff=0.3)
        l1_note.set_x(plane.get_x())
        stair = VMobject(stroke_color=SENS_COLOR, stroke_width=6).set_points_as_corners(
            [plane.c2p(*ca), plane.c2p(cb[0], ca[1]), plane.c2p(*cb)])
        stair_lab = S.math(r"\|f(x)-f(x')\|_1", "=", r"|\Delta_1|+|\Delta_2|", size=32)
        stair_lab[0].set_color(SENS_COLOR)
        stair_lab.next_to(plane, DOWN, buff=0.25).set_x(plane.get_x())
        if stair_lab.get_bottom()[1] < -3.55:
            stair_lab.shift(UP * (-3.55 - stair_lab.get_bottom()[1]))
        # f(x) in 'density ∝ e^{-||y - f(x)||_1 / λ}', counted from the end (the word before ∝ is translated)
        l1_note[0][-8:-4].set_color(X_COLOR)
        # the picture is drawn centre stage, then slides right to make room for the Proposition 1 card
        pgroup = VGroup(plane, dz, dzp, l1_note, stair, stair_lab)
        home_x = plane.get_x()
        pgroup.shift(LEFT * home_x)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(l1, l2, l3, tri, sens, every)),
                      VGroup(sub, box).animate.scale(0.62).to_edge(UP, buff=0.4), run_time=0.8)
            self.play(Create(plane), run_time=0.9)
            vo.wait_until("add independent")
            self.play(LaggedStart(*[Create(m) for m in dz], lag_ratio=0.15), run_time=1.4)
            vo.wait_until("The joint density")
            self.play(FadeIn(l1_note), run_time=0.7)
            self.play(LaggedStart(*[Create(m) for m in dzp], lag_ratio=0.15), run_time=1.4)
            vo.wait_until("which is exactly why")
            self.play(Create(stair), FadeIn(stair_lab, shift=UP * 0.1), run_time=1.2)
            vo.wait_until("That is Proposition 1")
            self.play(pgroup.animate.shift(RIGHT * home_x), FadeIn(frame), Write(prop_title), run_time=1.0)
            self.play(Write(prop), run_time=1.0)
            self.play(Write(prop2), run_time=1.1)
            self.play(Indicate(prop2[1:4], color=S.WHITE, scale_factor=1.1), run_time=vo.remaining(0.6))

        # ============================================================ 6. ponder: why not uniform noise?
        u_axis = NumberLine(x_range=[-12, 12, 2], length=8.4, color=S.GREY, stroke_width=2,
                            include_ticks=True, tick_size=0.06).move_to([0, 0.75, 0])
        u_labs = VGroup(*[S.math(s, size=28, color=S.GREY).next_to(u_axis.n2p(v), DOWN, buff=0.15)
                          for v, s in [(-10, "-10"), (0, "0"), (10, "+10")]])
        U_H = 1.6
        u_box = Rectangle(width=u_axis.n2p(10)[0] - u_axis.n2p(-10)[0], height=U_H, stroke_color=NOISE_COLOR,
                          stroke_width=4).set_fill(NOISE_COLOR, 0.2)
        u_box.next_to(u_axis.n2p(0), UP, buff=0)
        u_title = S.text("uniform noise", 28, NOISE_COLOR).next_to(u_box, UP, buff=0.2)
        u_group = VGroup(u_axis, u_labs, u_box, u_title)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
            self.play(Create(u_axis), FadeIn(u_labs), GrowFromEdge(u_box, DOWN), FadeIn(u_title), run_time=0.9)
            vo.wait_until("like uniform noise")
            self.play(Indicate(u_title, color=NOISE_COLOR, scale_factor=1.15), run_time=0.8)
            vo.wait_until("anywhere between")
            self.play(Indicate(u_labs[0], color=S.WHITE, scale_factor=1.3),
                      Indicate(u_labs[2], color=S.WHITE, scale_factor=1.3), run_time=vo.remaining(0.8))
        card_u = ponder_at(self, "Why not uniform noise,\nanywhere between −10 and +10?", pos=[0, -2.0, 0],
                           width=9.0)
        drain(self, card_u, 10)                       # PONDER(10 s): silent timer

        # ============================================================ 7. the edges: an infinite ratio
        ax_u = NumberLine(x_range=[29, 54, 1], length=12.0, color=S.GREY, stroke_width=2,
                          include_ticks=True, tick_size=0.05).move_to([0, -1.25, 0])
        BOX_H = 2.0                                   # stands for density 1/20
        box_x = Rectangle(width=ax_u.n2p(51)[0] - ax_u.n2p(31)[0], height=BOX_H, stroke_color=X_COLOR,
                          stroke_width=4).set_fill(X_COLOR, 0.12)
        box_x.next_to(ax_u.n2p(41), UP, buff=0)
        box_xp = Rectangle(width=box_x.width, height=BOX_H, stroke_color=XP_COLOR,
                           stroke_width=4).set_fill(XP_COLOR, 0.12)
        box_xp.next_to(ax_u.n2p(42), UP, buff=0)
        top_y = box_x.get_top()[1]
        w_x = S.math(r"f(x) + U", size=30, color=X_COLOR).move_to([ax_u.n2p(34.5)[0], top_y + 0.32, 0])
        w_xp = S.math(r"f(x') + U", size=30, color=XP_COLOR).move_to([ax_u.n2p(48.0)[0], top_y + 0.32, 0])
        e_labs = VGroup(*[S.text(str(v), 22, col).next_to(ax_u.n2p(v), DOWN, buff=dy)
                          for v, col, dy in [(31, X_COLOR, 0.15), (41, X_COLOR, 0.15), (51, X_COLOR, 0.15),
                                             (32, XP_COLOR, 0.5), (42, XP_COLOR, 0.5), (52, XP_COLOR, 0.5)]])
        T_OUT = 51.5
        out_line = DashedLine(ax_u.n2p(T_OUT) + DOWN * 0.05, ax_u.n2p(T_OUT) + UP * (BOX_H + 1.0),
                              color=S.WHITE, stroke_width=3, dash_length=0.08)
        out_lab = S.math(r"t = 51.5", size=30).next_to(out_line, UP, buff=0.1)
        o_dot = Dot([ax_u.n2p(T_OUT)[0], top_y, 0], color=XP_COLOR, radius=0.1)
        o_lab = S.math(r"x'\!:\ 1/20", size=30, color=XP_COLOR).next_to(o_dot, RIGHT, buff=0.3)
        o_lab.shift(DOWN * 0.3)
        b_dot = Dot(ax_u.n2p(T_OUT), color=X_COLOR, radius=0.1)
        b_lab = S.math(r"x\!:\ 0", size=30, color=X_COLOR).next_to(b_dot, RIGHT, buff=0.3).shift(UP * 0.3)
        ratio = S.math(r"\frac{1/20}{0}", "=", r"\infty", size=52)
        ratio[0][0:4].set_color(XP_COLOR)
        ratio[0][5:].set_color(X_COLOR)
        ratio[2].set_color(S.RED)
        ratio.move_to([1.3, 2.5, 0])
        thumb = random_row_thumb().move_to([-4.5, 2.5, 0])
        same = S.text("same as", 24, S.GREY).move_to([(thumb.get_right()[0] + ratio.get_left()[0]) / 2, 2.5, 0])
        rule = S.text("Good noise must never rule an output out.", 32, S.WHITE).to_edge(DOWN, buff=0.4)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(card_u), FadeOut(u_labs), FadeOut(u_title), ReplacementTransform(u_axis, ax_u),
                      ReplacementTransform(u_box, box_x), TransformFromCopy(u_box, box_xp),
                      FadeIn(w_x), FadeIn(w_xp), FadeIn(e_labs), run_time=1.0)
            # 'Look at the edges': the four vertical box edges flash in their world's colour
            edge_hl = VGroup(*[Line(ax_u.n2p(v), ax_u.n2p(v) + UP * BOX_H, color=col, stroke_width=10)
                               for v, col in ((31, X_COLOR), (51, X_COLOR), (32, XP_COLOR), (52, XP_COLOR))])
            self.play(*[ShowPassingFlash(e, time_width=0.7) for e in edge_hl],
                      *[Indicate(e_labs[i], color=(X_COLOR if i < 3 else XP_COLOR), scale_factor=1.4)
                        for i in (0, 2, 3, 5)],
                      run_time=0.9)
            vo.wait_until("An output of")
            self.play(Create(out_line), FadeIn(out_lab), run_time=0.8)
            vo.wait_until("is possible if")
            self.play(FadeIn(o_dot, scale=0.5), FadeIn(o_lab), run_time=0.6)
            vo.wait_until("but impossible")
            self.play(FadeIn(b_dot, scale=0.5), FadeIn(b_lab), Flash(b_dot, color=X_COLOR, flash_radius=0.3),
                      run_time=0.7)
            vo.wait_until("the same infinite ratio")
            self.play(Write(ratio), run_time=0.9)
            vo.wait_until("that sank")
            self.play(FadeIn(thumb, shift=RIGHT * 0.3), FadeIn(same), run_time=0.8)
            vo.wait_until("Good noise")
            self.play(FadeIn(rule, shift=UP * 0.2), run_time=0.8)

        # ============================================================ 8. why not a Gaussian?
        top2 = Panel(T0, T1, LOG_LO, LOG_HI, 11.5, 2.4).move_to([0, 1.45, 0])
        R2 = 2.6                                      # log-ratio range of this panel: [-R2, R2]
        bot2 = Panel(T0, T1, -R2, R2, 11.5, 2.6, axis_y=0, tick_labels=False).move_to([0, -2.05, 0])
        L2 = top2.c2p
        log_lab2 = S.text("log density", 22, S.GREY).next_to(top2.c2p(T0, LOG_HI), RIGHT, buff=0.15)
        log_lab2.shift(DOWN * 0.15)

        def tent2(mu, col):
            a, b = clipped(log_lap, mu, lap_reach)
            return top2.plot(lambda s: log_lap(s, mu), a, b, kinks=[mu], color=col)

        g_reach = np.sqrt(2 * (-LN2PI_HALF - LOG_LO))

        def parab(mu, col):
            a, b = clipped(log_gauss, mu, g_reach)
            return top2.plot(lambda s: log_gauss(s, mu), a, b, color=col)

        tA, tB = tent2(A, X_COLOR), tent2(B, XP_COLOR)
        pA, pB = parab(A, X_COLOR), parab(B, XP_COLOR)
        kind_lap = S.text("Laplace", 26, NOISE_COLOR)
        kind_gau = S.text("Gaussian", 26, S.GREY)
        for k in (kind_lap, kind_gau):
            k.next_to(log_lab2, RIGHT, buff=0.3)
        hi2 = bot2.c2p(T0, 1)[1] - bot2.c2p(T0, 0)[1]
        band_h = ValueTracker(1.0)

        mid2 = bot2.c2p((T0 + T1) / 2, 0)
        band_g = VGroup(Rectangle(width=bot2.ref.width, height=2 * hi2, stroke_width=0).set_fill(EPS_COLOR, 0.08),
                        DashedLine(LEFT * bot2.ref.width / 2, RIGHT * bot2.ref.width / 2, color=EPS_COLOR,
                                   stroke_width=3),
                        DashedLine(LEFT * bot2.ref.width / 2, RIGHT * bot2.ref.width / 2, color=EPS_COLOR,
                                   stroke_width=3))

        def band_upd(g):          # built once; the updater only resizes / moves (stable submobjects)
            hgt = band_h.get_value() * hi2
            g[0].stretch_to_fit_height(2 * hgt).move_to(mid2)
            g[1].move_to(mid2 + UP * hgt)
            g[2].move_to(mid2 + DOWN * hgt)

        band_g.add_updater(band_upd).update()
        eps_hi = S.math(r"+\varepsilon", size=30, color=EPS_COLOR)
        eps_lo = S.math(r"-\varepsilon", size=30, color=EPS_COLOR)
        eps_hi.add_updater(lambda m: m.next_to(bot2.c2p(T1, band_h.get_value()), RIGHT, buff=0.1)).update()
        eps_lo.add_updater(lambda m: m.next_to(bot2.c2p(T1, -band_h.get_value()), RIGHT, buff=0.1)).update()
        lap_line = bot2.plot(log_ratio, kinks=[A, B], color=S.WHITE, sw=4)
        g_lo_t, g_hi_t = (A + B) / 2 - R2, (A + B) / 2 + R2          # where 41.5 - t leaves the panel
        gauss_line = bot2.plot(lambda s: (A + B) / 2 - s, g_lo_t, g_hi_t, color=S.GREY, sw=6)
        ratio_lab = S.text("log ratio", 22, S.GREY).next_to(bot2.c2p(T0, -2.2), RIGHT, buff=0.2)
        # direct labels in free space: under the Laplace line's +1 shelf (inside the band), and above
        # the widened band at the left, where the Gaussian line leaves it
        lap_key = S.text("Laplace: stays inside", 24, S.WHITE)
        lap_key.move_to(bot2.c2p(T0, 0.5), aligned_edge=LEFT).shift(RIGHT * 0.2)
        gau_key = S.text("Gaussian: escapes", 24, S.GREY)            # above the widened band, by the exit
        gau_key.move_to(bot2.c2p(T0, 2.2), aligned_edge=LEFT).shift(RIGHT * 0.2)
        keys = VGroup(lap_key, gau_key)
        up_arrow = Arrow(bot2.c2p(g_lo_t, R2) + DOWN * 0.05, bot2.c2p(g_lo_t, R2) + UP * 0.38 + LEFT * 0.44,
                         color=S.RED, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.4)
        dn_arrow = Arrow(bot2.c2p(g_hi_t, -R2) + UP * 0.05, bot2.c2p(g_hi_t, -R2) + DOWN * 0.2 + RIGHT * 0.24,
                         color=S.RED, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.5)
        gprobe = ValueTracker(40.5)

        def ggap():
            p = gprobe.get_value()
            return DoubleArrow(L2(p, log_gauss(p, B)), L2(p, log_gauss(p, A)), buff=0, color=EPS_COLOR,
                               stroke_width=4, tip_length=0.13, max_tip_length_to_length_ratio=0.45)

        g_gap = always_redraw(ggap)
        g_txt = S.math(r"\text{gap} =", size=32, color=EPS_COLOR).move_to([-5.9, 3.2, 0], aligned_edge=LEFT)
        g_num = always_redraw(lambda: DecimalNumber((A + B) / 2 - gprobe.get_value(), num_decimal_places=2,
                                                    font_size=32, color=EPS_COLOR).next_to(g_txt, RIGHT, buff=0.12))
        later = VGroup(S.text("comes back later:", 24, S.GREY),
                       S.text("training neural networks privately", 24, S.WHITE)).arrange(RIGHT, buff=0.15)
        later.move_to([1.6, 3.2, 0])

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
            self.play(FadeIn(VGroup(top2, log_lab2, kind_lap, tA, tB)), FadeIn(VGroup(bot2, ratio_lab, lap_line)),
                      FadeIn(band_g), FadeIn(eps_hi), FadeIn(eps_lo), run_time=1.0)
            vo.wait_until("On a log scale")
            # Chinese glyphs do not morph into one another cleanly (拉普拉斯 -> 高斯): cross-fade them
            relabel = (ReplacementTransform(kind_lap, kind_gau) if not i18n.active()
                       else FadeTransform(kind_lap, kind_gau, stretch=False))
            self.play(ReplacementTransform(tA, pA), ReplacementTransform(tB, pB), relabel, run_time=1.6)
            vo.wait_until("so the gap")
            self.play(FadeIn(g_gap), FadeIn(g_txt), FadeIn(g_num), run_time=0.4)
            self.play(gprobe.animate.set_value(38.8), run_time=2.2)
            vo.wait_until("In the tails")
            self.play(Create(gauss_line), run_time=1.1)
            self.play(GrowArrow(up_arrow), GrowArrow(dn_arrow), run_time=0.7)
            vo.wait_until("no single epsilon")
            self.play(band_h.animate.set_value(1.6), run_time=1.2)
            self.play(FadeIn(keys), Indicate(up_arrow, color=S.RED, scale_factor=1.25),
                      Indicate(dn_arrow, color=S.RED, scale_factor=1.25), run_time=0.7)
            vo.wait_until("Hold on to that")
            self.play(FadeIn(later, shift=DOWN * 0.15), run_time=0.8)
            self.play(ShowPassingFlash(pA.copy().set_stroke(X_COLOR, 10), time_width=0.4),
                      ShowPassingFlash(pB.copy().set_stroke(XP_COLOR, 10), time_width=0.4),
                      Indicate(kind_gau, color=S.WHITE), run_time=vo.remaining(1.2))
        for m in (band_g, eps_hi, eps_lo, g_gap, g_num):
            m.clear_updaters()

        # ============================================================ 9. the recipe
        recipe = S.math(r"\text{noise scale}", r"=", r"\frac{S(f)}{\varepsilon}", size=72)
        recipe[2][0:4].set_color(SENS_COLOR)
        recipe[2][-1].set_color(EPS_COLOR)
        recipe.shift(UP * 0.8)
        a1 = S.text("more sensitive question  →  more noise", 32, SENS_COLOR)
        a2 = S.text("stronger privacy (smaller ε)  →  more noise", 32, EPS_COLOR)
        notes = VGroup(a1, a2).arrange(DOWN, buff=0.35).next_to(recipe, DOWN, buff=0.8)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
            self.play(Write(recipe), run_time=1.5)
            vo.wait_until("noise scale equals")
            self.play(Circumscribe(recipe[2], color=S.WHITE), run_time=1.2)
            vo.wait_until("A more sensitive")
            self.play(FadeIn(a1, shift=UP * 0.2), Indicate(recipe[2][0:4], color=SENS_COLOR), run_time=0.9)
            vo.wait_until("Stronger privacy")
            self.play(FadeIn(a2, shift=UP * 0.2), Indicate(recipe[2][-1], color=EPS_COLOR), run_time=0.9)
        self.wait(0.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
