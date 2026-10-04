"""S07 · The Laplace mechanism — the heart of the paper (Example 1, Proposition 1)."""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import gaussian_pdf, laplace_pdf
from explainer.scene import VoiceScene

from common import EPS_COLOR, NARRATION, NOISE_COLOR, SENS_COLOR, X_COLOR, XP_COLOR

SAY = NARRATION["S07"]
LAM = 1.0            # Laplace scale used in the pictures (so 1/lambda = 1)
A, B = 41.0, 42.0    # f(x), f(x')
T0, T1 = 36.0, 47.0  # visible output range


def log_ratio(t, a=A, b=B, lam=LAM):
    """ln[h(t-a)/h(t-b)] for Laplace(lam): (|t-b| - |t-a|)/lam."""
    return (abs(t - b) - abs(t - a)) / lam


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
        lam_label = always_redraw(lambda: VGroup(
            S.math(r"\lambda =", size=40, color=NOISE_COLOR),
            DecimalNumber(lam.get_value(), num_decimal_places=1, font_size=40, color=NOISE_COLOR),
        ).arrange(RIGHT, buff=0.15).move_to(ax0.c2p(4.2, 0.85)))

        with self.voiceover(SAY[0]) as vo:
            self.play(Create(ax0), Write(formula0), run_time=1.2)
            self.play(Create(curve0), FadeIn(title0), run_time=1.5)
            vo.wait_until("falls off exponentially")
            # indicate the exponential fall-off on both sides
            self.play(Indicate(formula0[2], color=NOISE_COLOR), run_time=1.0)
            vo.wait_until("Its width")
            self.add(lam_label)
            self.play(lam.animate.set_value(2.0), run_time=1.2)
            self.play(lam.animate.set_value(0.6), run_time=1.2)
            self.play(lam.animate.set_value(1.0), run_time=vo.remaining(0.6))
        curve0.clear_updaters()
        lam_label.clear_updaters()
        self.play(FadeOut(VGroup(ax0, curve0, lam_label, title0)),
                  formula0.animate.scale(0.75).to_corner(UR, buff=0.4), run_time=0.8)

        # ============================================================ 1. two worlds: 41 vs 42
        top = Axes(x_range=[T0, T1, 1], y_range=[0, 0.6, 0.25], x_length=11.5, y_length=2.4,
                   tips=False, axis_config={"color": S.GREY, "stroke_width": 2}).shift(UP * 1.2)
        tick_labels = VGroup(*[S.text(str(v), 20, S.GREY).next_to(top.c2p(v, 0), DOWN, buff=0.12)
                               for v in range(37, 47, 1)])
        pdf_a = top.plot(lambda t: laplace_pdf(t, A, LAM), x_range=[T0, T1, 0.01],
                         color=X_COLOR, stroke_width=5)
        pdf_b = top.plot(lambda t: laplace_pdf(t, B, LAM), x_range=[T0, T1, 0.01],
                         color=XP_COLOR, stroke_width=5)
        lab_a = S.math(r"f(x) = 41", size=34, color=X_COLOR).next_to(top.c2p(A, 0.5), LEFT, buff=0.35)
        lab_b = S.math(r"f(x') = 42", size=34, color=XP_COLOR).next_to(top.c2p(B, 0.5), RIGHT, buff=0.35)
        out_lab = S.text("output t", 22, S.GREY).next_to(top.x_axis.get_right(), DOWN, buff=0.35)

        with self.voiceover(SAY[1]) as vo:
            self.play(Create(top), FadeIn(tick_labels), FadeIn(out_lab), run_time=1.0)
            vo.wait_until("Center one")
            self.play(Create(pdf_a), FadeIn(lab_a), run_time=1.4)
            vo.wait_until("and another")
            self.play(Create(pdf_b), FadeIn(lab_b), run_time=1.4)
            vo.wait_until("These are")
            self.play(Indicate(VGroup(pdf_a, pdf_b), scale_factor=1.03), run_time=vo.remaining(0.8))

        # ============================================================ 2. the log ratio, swept out
        bot = Axes(x_range=[T0, T1, 1], y_range=[-2, 2, 1], x_length=11.5, y_length=2.6,
                   tips=False, axis_config={"color": S.GREY, "stroke_width": 2}).shift(DOWN * 2.15)
        bot_lab = S.math(r"\ln\frac{h(t-41)}{h(t-42)}", size=32).next_to(bot.c2p(T0, 1.6), RIGHT, buff=0.1)
        band_hi = DashedLine(bot.c2p(T0, 1 / LAM), bot.c2p(T1, 1 / LAM), color=EPS_COLOR, stroke_width=3)
        band_lo = DashedLine(bot.c2p(T0, -1 / LAM), bot.c2p(T1, -1 / LAM), color=EPS_COLOR, stroke_width=3)
        band = Rectangle(width=bot.x_length, height=abs(bot.c2p(0, 1)[1] - bot.c2p(0, -1)[1]),
                         stroke_width=0).set_fill(EPS_COLOR, 0.08).move_to(bot.c2p((T0 + T1) / 2, 0))
        hi_lab = S.math(r"+1/\lambda", size=30, color=EPS_COLOR).next_to(band_hi, RIGHT, buff=0.1)
        lo_lab = S.math(r"-1/\lambda", size=30, color=EPS_COLOR).next_to(band_lo, RIGHT, buff=0.1)
        for m in (hi_lab, lo_lab):
            if m.get_right()[0] > 6.95:
                m.shift(LEFT * (m.get_right()[0] - 6.95))

        t = ValueTracker(T0 + 0.3)
        v_a = always_redraw(lambda: DashedLine(top.c2p(t.get_value(), 0),
                                               top.c2p(t.get_value(), laplace_pdf(t.get_value(), A, LAM)),
                                               color=X_COLOR, stroke_width=3))
        dot_a = always_redraw(lambda: Dot(top.c2p(t.get_value(), laplace_pdf(t.get_value(), A, LAM)),
                                          color=X_COLOR, radius=0.07))
        dot_b = always_redraw(lambda: Dot(top.c2p(t.get_value(), laplace_pdf(t.get_value(), B, LAM)),
                                          color=XP_COLOR, radius=0.07))
        dot_r = always_redraw(lambda: Dot(bot.c2p(t.get_value(), log_ratio(t.get_value())),
                                          color=S.WHITE, radius=0.07))
        trace = TracedPath(dot_r.get_center, stroke_color=S.WHITE, stroke_width=4)
        ratio_graph = bot.plot(log_ratio, x_range=[T0 + 0.3, T1 - 0.3, 0.005], color=S.WHITE,
                               stroke_width=4)

        with self.voiceover(SAY[2]) as vo:
            self.play(Create(bot), FadeIn(bot_lab), run_time=1.0)
            self.add(v_a, dot_a, dot_b, dot_r, trace)
            vo.wait_until("Far to the left")
            self.play(t.animate.set_value(A - 0.3), run_time=vo.until("Far to the right"),
                      rate_func=linear)
            self.play(t.animate.set_value(B + 0.3), run_time=1.2, rate_func=linear)
            self.play(t.animate.set_value(T1 - 0.3), run_time=vo.until("In between", 1.5),
                      rate_func=linear)
            self.add(ratio_graph)
            self.remove(trace)
            ramp = bot.plot(log_ratio, x_range=[A, B, 0.005], color=S.YELLOW, stroke_width=7)
            self.play(Create(ramp), run_time=0.8)
            self.play(FadeOut(ramp), run_time=0.4)
            vo.wait_until("It never leaves")
            self.play(FadeIn(band), Create(band_hi), Create(band_lo), FadeIn(hi_lab), FadeIn(lo_lab),
                      run_time=1.2)
        for m in (v_a, dot_a, dot_b, dot_r):
            m.clear_updaters()
        self.play(FadeOut(VGroup(v_a, dot_a, dot_b, dot_r)), run_time=0.4)

        # ============================================================ 3. log scale: tents
        top_log = Axes(x_range=[T0, T1, 1], y_range=[-6, 0, 2], x_length=11.5, y_length=2.4,
                       tips=False, axis_config={"color": S.GREY, "stroke_width": 2}).move_to(top)
        log_lab = S.math(r"\ln h", size=32, color=S.GREY).next_to(top_log.c2p(T0, -0.6), RIGHT, buff=0.1)
        mu_b = ValueTracker(A)

        def tent(mu, col):
            return top_log.plot(lambda s: -abs(s - mu) / LAM - np.log(2 * LAM), x_range=[T0, T1, 0.005],
                                color=col, stroke_width=5)

        tent_a = tent(A, X_COLOR)
        tent_b = always_redraw(lambda: tent(mu_b.get_value(), XP_COLOR))
        probe = 38.5
        gap = always_redraw(lambda: DoubleArrow(
            top_log.c2p(probe, -abs(probe - mu_b.get_value()) / LAM - np.log(2 * LAM)),
            top_log.c2p(probe, -abs(probe - A) / LAM - np.log(2 * LAM)),
            buff=0, color=EPS_COLOR, stroke_width=4, tip_length=0.14,
            max_tip_length_to_length_ratio=0.45) if mu_b.get_value() - A > 0.08 else VGroup())
        gap_lab = always_redraw(lambda: S.math(
            r"\text{gap} = " + f"{(mu_b.get_value() - A) / LAM:.2f}", size=30, color=EPS_COLOR
        ).next_to(top_log.c2p(probe, -abs(probe - A) / LAM - np.log(2 * LAM)), LEFT, buff=0.25))

        with self.voiceover(SAY[3]) as vo:
            self.play(ReplacementTransform(top, top_log), ReplacementTransform(pdf_a, tent_a),
                      FadeOut(pdf_b), FadeOut(lab_a), FadeOut(lab_b), FadeOut(tick_labels), FadeOut(out_lab),
                      FadeIn(log_lab), run_time=1.6)
            self.add(tent_b)
            vo.wait_until("Slide the tent")
            self.add(gap, gap_lab)
            self.play(mu_b.animate.set_value(B), run_time=vo.until("That is the triangle", 2.0))
            self.play(Indicate(gap_lab, color=EPS_COLOR), run_time=vo.remaining(0.6))
        for m in (tent_b, gap, gap_lab):
            m.clear_updaters()

        # ============================================================ 4. the one-line proof
        self.play(FadeOut(VGroup(top_log, tent_a, tent_b, gap, gap_lab, log_lab, formula0,
                                 bot, bot_lab, ratio_graph, band, band_hi, band_lo, hi_lab, lo_lab)),
                  run_time=0.8)
        fx, fxp = r"f(x)", r"f(x')"
        l1 = S.math(r"\ln\frac{h(t-", fx, r")}{h(t-", fxp, r")}", r"=",
                    r"\frac{|t-", fxp, r"|-|t-", fx, r"|}{\lambda}", size=44)
        l2 = S.math(r"\le", r"\frac{|", fx, "-", fxp, r"|}{\lambda}", size=44)
        l3 = S.math(r"\le", r"\frac{S(f)}{\lambda}", size=44)
        for line in (l1, l2):
            for part in line:
                if part.get_tex_string() == fx:
                    part.set_color(X_COLOR)
                elif part.get_tex_string() == fxp:
                    part.set_color(XP_COLOR)
        l3[1].set_color(SENS_COLOR)
        proof = VGroup(l1, l2, l3).arrange(DOWN, buff=0.45, aligned_edge=LEFT).shift(UP * 0.9 + LEFT * 0.5)
        l2.shift(RIGHT * (l1[5].get_left()[0] - l2[0].get_left()[0]))
        l3.shift(RIGHT * (l1[5].get_left()[0] - l3[0].get_left()[0]))
        tri = S.text("triangle inequality", 24, S.GREY).next_to(l2, RIGHT, buff=0.5)
        sub = S.math(r"\lambda = \frac{S(f)}{\varepsilon}", r"\quad\Longrightarrow\quad",
                     r"\left|\ln\frac{\Pr[\mathcal{T}(x)=t]}{\Pr[\mathcal{T}(x')=t]}\right| \le \varepsilon",
                     size=44)
        sub[0][2:6].set_color(SENS_COLOR)
        sub[0][-1].set_color(EPS_COLOR)
        sub[2][-1].set_color(EPS_COLOR)
        sub.next_to(proof, DOWN, buff=0.7).set_x(0)
        box = SurroundingRectangle(sub, color=EPS_COLOR, buff=0.2, corner_radius=0.1)

        with self.voiceover(SAY[4]) as vo:
            self.play(Write(l1), run_time=1.6)
            self.play(Write(l2), FadeIn(tri, shift=LEFT * 0.2), run_time=1.2)
            vo.wait_until("the sensitivity divided by lambda")
            self.play(Write(l3), run_time=1.0)
            vo.wait_until("Set lambda")
            self.play(Write(sub), run_time=1.8)
            vo.wait_until("Privacy, proven")
            self.play(Create(box), run_time=0.8)

        # ============================================================ 5. vectors: Proposition 1
        self.play(FadeOut(VGroup(proof, tri)), VGroup(sub, box).animate.scale(0.7).to_edge(UP, buff=0.35),
                  run_time=0.8)
        prop_title = S.text("Proposition 1", 30, S.YELLOW, weight="BOLD")
        prop = S.math(r"\mathrm{San}_f(x) = f(x) + (Y_1, \dots, Y_d)", size=40)
        prop2 = S.math(r"Y_i \sim \mathrm{Lap}\!\left(", r"S(f)", "/", r"\varepsilon", r"\right)\ \text{i.i.d.}",
                       size=40)
        prop2[1].set_color(SENS_COLOR)
        prop2[3].set_color(EPS_COLOR)
        card = VGroup(prop_title, prop, prop2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        card.to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
        frame = SurroundingRectangle(card, color=S.GREY, buff=0.3, corner_radius=0.12)

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=4.6, y_length=4.6,
                            background_line_style={"stroke_color": S.GREY_DARK, "stroke_width": 1},
                            axis_config={"stroke_color": S.GREY}).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.6)

        def diamonds(cx, cy, col):
            g = VGroup()
            for r, op in [(0.5, 1.0), (1.0, 0.7), (1.5, 0.45), (2.0, 0.25)]:
                pts = [plane.c2p(cx + r, cy), plane.c2p(cx, cy + r), plane.c2p(cx - r, cy), plane.c2p(cx, cy - r)]
                g.add(Polygon(*pts, color=col, stroke_width=3, stroke_opacity=op))
            g.add(Dot(plane.c2p(cx, cy), color=col, radius=0.07))
            return g

        dz = diamonds(-0.5, -0.4, X_COLOR)
        dzp = diamonds(0.5, 0.4, XP_COLOR)
        l1_note = S.math(r"\text{density} \propto e^{-\|y\|_1/\lambda}", size=34).next_to(plane, UP, buff=0.25)
        l1_note.set_x(plane.get_x())
        with self.voiceover(SAY[5]) as vo:
            self.play(Create(plane), run_time=1.0)
            self.play(LaggedStart(*[Create(m) for m in dz], lag_ratio=0.15), run_time=1.4)
            vo.wait_until("The joint density")
            self.play(FadeIn(l1_note), LaggedStart(*[Create(m) for m in dzp], lag_ratio=0.15), run_time=1.6)
            vo.wait_until("That is the paper")
            self.play(FadeIn(frame), Write(prop_title), Write(prop), run_time=1.4)
            self.play(Write(prop2), run_time=vo.remaining(1.0))

        # ============================================================ 6. why not a Gaussian?
        self.play(FadeOut(VGroup(plane, dz, dzp, l1_note, frame, card, sub, box)), run_time=0.8)
        g_ax = Axes(x_range=[T0, T1, 1], y_range=[-2.5, 2.5, 1], x_length=11.5, y_length=4.0,
                    tips=False, axis_config={"color": S.GREY, "stroke_width": 2}).shift(DOWN * 0.5)
        g_title = S.text("log-ratio of the two worlds' densities", 30, S.WHITE).to_edge(UP, buff=0.5)
        g_hi = DashedLine(g_ax.c2p(T0, 1), g_ax.c2p(T1, 1), color=EPS_COLOR, stroke_width=3)
        g_lo = DashedLine(g_ax.c2p(T0, -1), g_ax.c2p(T1, -1), color=EPS_COLOR, stroke_width=3)
        g_band = Rectangle(width=g_ax.x_length, height=abs(g_ax.c2p(0, 1)[1] - g_ax.c2p(0, -1)[1]),
                           stroke_width=0).set_fill(EPS_COLOR, 0.08).move_to(g_ax.c2p((T0 + T1) / 2, 0))
        lap_line = g_ax.plot(log_ratio, x_range=[T0, T1, 0.005], color=NOISE_COLOR, stroke_width=5)
        gauss_line = g_ax.plot(lambda s: (A + B) / 2 - s, x_range=[38.6, 44.4, 0.01], color=S.GREY,
                               stroke_width=5)
        lap_key = VGroup(Line(ORIGIN, RIGHT * 0.6, color=NOISE_COLOR, stroke_width=5),
                         S.text("Laplace: bounded", 26, NOISE_COLOR)).arrange(RIGHT, buff=0.2)
        gau_key = VGroup(Line(ORIGIN, RIGHT * 0.6, color=S.GREY, stroke_width=5),
                         S.text("Gaussian: a straight line, unbounded", 26, S.GREY)).arrange(RIGHT, buff=0.2)
        keys = VGroup(lap_key, gau_key).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        keys.next_to(g_ax, DOWN, buff=0.35).align_to(g_ax, LEFT)
        up_arrow = Arrow(g_ax.c2p(38.9, 1.6), g_ax.c2p(38.6, 2.6), color=NOISE_COLOR, buff=0,
                         stroke_width=5)
        dn_arrow = Arrow(g_ax.c2p(44.1, -1.6), g_ax.c2p(44.4, -2.6), color=NOISE_COLOR, buff=0,
                         stroke_width=5)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(g_title), Create(g_ax), FadeIn(g_band), Create(g_hi), Create(g_lo), run_time=1.2)
            self.play(Create(lap_line), FadeIn(lap_key), run_time=1.2)
            vo.wait_until("the gap between")
            self.play(Create(gauss_line), FadeIn(gau_key), run_time=1.8)
            vo.wait_until("Far out in the tails")
            self.play(GrowArrow(up_arrow), GrowArrow(dn_arrow), run_time=0.8)
            self.play(Flash(g_ax.c2p(38.6, 2.5), color=NOISE_COLOR), Flash(g_ax.c2p(44.4, -2.5), color=NOISE_COLOR),
                      run_time=0.8)
            vo.wait_until("Laplace tails")
            self.play(Indicate(lap_line, color=NOISE_COLOR, scale_factor=1.02), Indicate(lap_key),
                      run_time=vo.remaining(0.8))

        # ============================================================ 7. the recipe
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        recipe = S.math(r"\text{noise scale}", r"=", r"\frac{S(f)}{\varepsilon}", size=72)
        recipe[2][0:4].set_color(SENS_COLOR)
        recipe[2][-1].set_color(EPS_COLOR)
        recipe.shift(UP * 0.8)
        a1 = S.text("more sensitive question  →  more noise", 32, SENS_COLOR)
        a2 = S.text("stronger privacy (smaller ε)  →  more noise", 32, EPS_COLOR)
        a3 = S.text("nothing else", 32, S.GREY)
        notes = VGroup(a1, a2, a3).arrange(DOWN, buff=0.3).next_to(recipe, DOWN, buff=0.7)
        with self.voiceover(SAY[7]) as vo:
            self.play(Write(recipe), run_time=1.5)
            vo.wait_until("A more sensitive")
            self.play(FadeIn(a1, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("Stronger privacy")
            self.play(FadeIn(a2, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("And nothing else")
            self.play(FadeIn(a3, shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(VGroup(recipe, notes)), run_time=0.8)
