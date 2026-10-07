"""S13 · Recap and questions.

Four recap panels reuse the formulas exactly as typeset in S04 (Definition 1), S06 (L1 sensitivity),
S07 (Laplace mechanism) and S11 (Theorem 3 threshold); then three test-yourself cards, each followed
by a silent ponder timer; then the closing questions and the paper citation.
"""

import numpy as np
from manim import *

from explainer import i18n
from explainer import style as S
from explainer.components import paper_page, person_icon
from explainer.scene import VoiceScene

from common import (ALICE, EPS_COLOR, NARRATION, NOISE_COLOR, PAPER_P1, SENS_COLOR, TRUTH_COLOR,
                    X_COLOR, XP_COLOR)

SAY = NARRATION["S13"]

MASK = S.WHITE                       # a row's parity mask: WHITE outlines, as in S11 (PURPLE = analyst)
BIT_ON, BIT_OFF = S.GREY, S.GREY_DARKER   # S11's compact tables: a 1 bit is a GREY cell
PANEL_W, PANEL_H = 6.4, 3.2
PANEL_XY = [(-3.32, 1.75), (3.32, 1.75), (-3.32, -1.75), (3.32, -1.75)]
CARD_W, CARD_SIZE = 11.6, 32
CARD_Y = 1.15


def lap_tent(t, mu, b=0.32):
    """A Laplace density (peak 1), drawn small: the output of M in world x or x' (as in S07/S08)."""
    return np.exp(-abs(t - mu) / b)


def badge(num, color, r=0.3):
    c = Circle(radius=r, color=color, stroke_width=3).set_fill(color, 0.15)
    return VGroup(c, S.text(str(num), 26, color).move_to(c))


def panel(i, title, color, en_tag=None):
    """VGroup(frame, badge, title); the frame and badge appear first, the title with the content.
    `en_tag`: in a translated render, a core term's English name follows its title, small and
    grey (the key, e.g. "Laplace mechanism [en]", is translated to the English name by a scoped
    strings entry, so it cannot collide with the title's own key)."""
    frame = RoundedRectangle(width=PANEL_W, height=PANEL_H, corner_radius=0.2, stroke_color=S.GREY_DARK,
                             stroke_width=2.5).set_fill(S.GREY_DARKER, 0.55)
    frame.move_to([*PANEL_XY[i], 0])
    b = badge(i + 1, color).move_to(frame.get_corner(UL) + RIGHT * 0.5 + DOWN * 0.48)
    t = S.text(title, 32, S.WHITE).next_to(b, RIGHT, buff=0.25)
    if en_tag and i18n.active():
        tag = S.text(en_tag, 20, S.GREY).next_to(t, RIGHT, buff=0.18).align_to(t, DOWN)
        t = VGroup(t, tag)
    return VGroup(frame, b, t)


def pic_anchor(p):
    """Centre of the picture slot (middle band) of a panel."""
    return p[0].get_top() + DOWN * 1.38


def formula_anchor(p):
    return p[0].get_bottom() + UP * 0.66


def question_card(lines, width=CARD_W):
    """explainer.components.ponder_card, but with TeX lines so n, [0, 1] and C are typeset as maths.
    Returns VGroup(frame, header, question, timer_bar), like ponder_card."""
    header = S.text("Pause and ponder", S.SMALL_SIZE, S.YELLOW, weight="BOLD")
    q = VGroup(*[S.tex(l, size=CARD_SIZE * 1.38) for l in lines]).arrange(DOWN, buff=0.2)
    if q.width > width - 0.6:
        q.scale_to_fit_width(width - 0.6)
    body = VGroup(header, q).arrange(DOWN, buff=0.35)
    frame = RoundedRectangle(width=width, height=body.height + 0.9, corner_radius=0.2, stroke_color=S.YELLOW,
                             stroke_width=3).set_fill(S.BG, 0.96)
    body.move_to(frame).shift(UP * 0.12)
    bar = Line(frame.get_corner(DOWN + LEFT) + RIGHT * 0.3 + UP * 0.25,
               frame.get_corner(DOWN + RIGHT) + LEFT * 0.3 + UP * 0.25, color=S.YELLOW, stroke_width=4)
    return VGroup(frame, header, q, bar).move_to([0, CARD_Y, 0])


def drain(scene, card, seconds):
    """The ponder timer: the card's bar drains silently (same as pause_and_ponder)."""
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)


class Recap(VoiceScene):
    def construct(self):
        self.recap_beat()
        leftovers = self.questions_beat()
        self.closing_beat(leftovers)

    # ================================================================ 1. four panels
    def recap_beat(self):
        p1 = panel(0, "Privacy", EPS_COLOR)
        p2 = panel(1, "Sensitivity", SENS_COLOR, en_tag="Sensitivity [en]")
        p3 = panel(2, "Laplace mechanism", NOISE_COLOR, en_tag="Laplace mechanism [en]")
        p4 = panel(3, "One published table", S.GREY)

        # --- 1: Definition 1, exactly as in S04
        f1 = S.math(r"\left|\,", r"\ln", r"\!\left(", r"{\Pr[M(x)=t]", r"\over", r"\Pr[M(x')=t]}",
                    r"\right)", r"\,\right|", r"\le", r"\varepsilon", size=40)
        f1[3].set_color(X_COLOR)
        f1[5].set_color(XP_COLOR)
        f1[9].set_color(EPS_COLOR)
        f1.move_to(formula_anchor(p1) + DOWN * 0.04)
        c1 = pic_anchor(p1) + UP * 0.1
        base1 = Line(c1 + LEFT * 1.6 + DOWN * 0.4, c1 + RIGHT * 1.6 + DOWN * 0.4, color=S.GREY, stroke_width=2)

        MU = 0.2                          # the two worlds' answers, f(x) and f(x'), on this little axis

        def bump(mu, col):
            """Laplace tent (sharp peak: no smoothing, and the kink is a sample point)."""
            us = np.unique(np.r_[np.arange(-1.6, 1.6001, 0.02), mu])
            pts = [c1 + DOWN * 0.4 + np.array([u, 0.85 * lap_tent(u, mu), 0]) for u in us]
            return VMobject(color=col, stroke_width=3.5).set_points_as_corners(pts)

        b_x, b_xp = bump(-MU, X_COLOR), bump(MU, XP_COLOR)
        tt = ValueTracker(-1.2)

        def probe():
            u = tt.get_value()
            p = c1 + DOWN * 0.4 + RIGHT * u
            ha, hb = 0.85 * lap_tent(u, -MU), 0.85 * lap_tent(u, MU)
            return VGroup(DashedLine(p, p + UP * max(ha, hb), color=S.GREY, stroke_width=2.5, dash_length=0.05),
                          Dot(p + UP * ha, radius=0.055, color=X_COLOR),
                          Dot(p + UP * hb, radius=0.055, color=XP_COLOR),
                          S.math("t", size=30, color=S.GREY).next_to(p, DOWN, buff=0.06))

        probe_m = always_redraw(probe)

        # --- 2: L1 sensitivity, exactly as in S06
        f2 = S.math(r"S(f)", "=", r"\max_{x,\,x'\ \text{neighbors}}", r"\big\|", r"f(x)", "-", r"f(x')",
                    r"\big\|_1", size=36)
        f2[0].set_color(SENS_COLOR)
        f2[4].set_color(X_COLOR)
        f2[6].set_color(XP_COLOR)
        f2.move_to(formula_anchor(p2))
        c2 = pic_anchor(p2)
        nl2 = Line(c2 + LEFT * 1.3, c2 + RIGHT * 1.3, color=S.GREY, stroke_width=2)
        d_x = Dot(c2 + LEFT * 0.5, radius=0.09, color=X_COLOR).set_z_index(2)
        d_xp = Dot(c2 + RIGHT * 0.5, radius=0.09, color=XP_COLOR).set_z_index(2)
        gap = Line(d_x.get_center(), d_xp.get_center(), color=SENS_COLOR, stroke_width=8)
        l_x = S.math("f(x)", size=30, color=X_COLOR).next_to(d_x, DOWN, buff=0.12)
        l_xp = S.math("f(x')", size=30, color=XP_COLOR).next_to(d_xp, DOWN, buff=0.12)
        pic2 = VGroup(nl2, gap, d_x, d_xp, l_x, l_xp).move_to(c2)

        # --- 3: the Laplace mechanism (S07's Proposition 1 card: Lap\!\left(S(f)/eps\right), S GREEN, eps YELLOW)
        f3 = S.math(r"M(x)", "=", r"f(x)", "+", r"\mathrm{Lap}\!\left(", r"S(f)", "/", r"\varepsilon", r"\right)",
                    size=42)
        f3[5].set_color(SENS_COLOR)
        f3[7].set_color(EPS_COLOR)
        f3.move_to(formula_anchor(p3) + UP * 0.16)
        c3 = pic_anchor(p3)
        tent = FunctionGraph(lambda u: 0.85 * np.exp(-abs(u) / 0.32), x_range=[-1.6, 1.6, 0.01], color=NOISE_COLOR,
                             stroke_width=4).shift(c3 + DOWN * 0.4)
        base3 = Line(c3 + LEFT * 1.6 + DOWN * 0.4, c3 + RIGHT * 1.6 + DOWN * 0.4, color=S.GREY, stroke_width=2)
        tick3 = Line(c3 + DOWN * 0.5, c3 + DOWN * 0.3, color=TRUTH_COLOR, stroke_width=4)
        no_n = S.tex(r"error does not grow with $n$", size=32, color=S.GREY).next_to(f3, DOWN, buff=0.2)

        # --- 4: the separation (S11's threshold)
        rng = np.random.default_rng(13)
        bits = rng.integers(0, 2, (4, 8))
        masks = np.zeros((4, 8), int)
        for r in range(4):
            masks[r, rng.choice(8, int(rng.integers(2, 5)), replace=False)] = 1
        cell = 0.23
        rows = VGroup(*[VGroup(*[Square(cell, stroke_color=S.BG, stroke_width=1)
                                 .set_fill(BIT_ON if v else BIT_OFF, 1) for v in b])
                        .arrange(RIGHT, buff=0) for b in bits]).arrange(DOWN, buff=0.05)
        over = VGroup(*[Square(cell * 0.8, stroke_color=MASK, stroke_width=2.5).move_to(rows[r][j])
                        for r in range(4) for j in np.flatnonzero(masks[r])])
        par = VGroup(*[S.text(str(int(np.dot(b, m) % 2)), 22, S.WHITE, font=S.FONT_SANS)
                       .next_to(rows[r], RIGHT, buff=0.14) for r, (b, m) in enumerate(zip(bits, masks))])
        pic4 = VGroup(rows, over, par)
        pic4.move_to(pic_anchor(p4) + UP * 0.04)
        t4 = S.text("can’t answer most parity counts", 26, S.WHITE)
        f4 = S.math(r"\text{unless}\quad n", r"\gtrsim", r"2^{d/4}", "/", r"\sqrt{\varepsilon}", size=38)
        f4[4][-1].set_color(EPS_COLOR)
        VGroup(t4, f4).arrange(DOWN, buff=0.18).move_to(formula_anchor(p4) + UP * 0.05)

        panels = [p1, p2, p3, p4]

        def lit(k):
            """Light panel k's frame, return the previous one to grey."""
            return [p[0].animate.set_stroke(S.WHITE if j == k else S.GREY_DARK, 3 if j == k else 2.5)
                    for j, p in enumerate(panels)]

        with self.voiceover(SAY[0]) as vo:
            self.play(LaggedStart(*[FadeIn(VGroup(p[0], p[1]), shift=UP * 0.15) for p in panels], lag_ratio=0.15),
                      run_time=1.1)
            vo.wait_until("One: privacy")
            self.play(*lit(0), FadeIn(p1[2], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Create(base1), Create(b_x), Create(b_xp), run_time=1.0)
            vo.wait_until("changes the probability")
            self.play(Write(f1), run_time=1.4)
            self.add(probe_m)
            self.play(tt.animate.set_value(1.2), run_time=2.4, rate_func=there_and_back_with_pause)
            vo.wait_until("e to the epsilon")
            self.play(Indicate(f1[9], color=EPS_COLOR, scale_factor=1.5), FadeOut(probe_m), run_time=0.8)
            probe_m.clear_updaters()

            vo.wait_until("Two: a query")
            self.play(*lit(1), FadeIn(p2[2], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Create(nl2), FadeIn(d_x), FadeIn(d_xp), FadeIn(l_x), FadeIn(l_xp), run_time=0.6)
            self.play(Create(gap), Write(f2), run_time=1.4)
            self.play(Indicate(f2[0], color=SENS_COLOR, scale_factor=1.3), run_time=0.8)

            vo.wait_until("Three: Laplace")
            self.play(*lit(2), FadeIn(p3[2], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Create(base3), Create(tent), FadeIn(tick3), run_time=0.9)
            self.play(Write(f3), run_time=1.3)
            self.play(Circumscribe(f3[4:], color=NOISE_COLOR, buff=0.08), run_time=1.0)
            vo.wait_until("with error that")
            self.play(FadeIn(no_n, shift=UP * 0.15), run_time=0.7)

            vo.wait_until("Four: one private")
            self.play(*lit(3), FadeIn(p4[2], shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(rows), run_time=0.5)
            self.play(Create(over), FadeIn(par), run_time=0.8)
            self.play(FadeIn(t4, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("unless the database")
            self.play(Write(f4), run_time=1.0)
            self.play(Indicate(f4[2], color=S.WHITE, scale_factor=1.35), run_time=vo.remaining(0.8))
        self.play(p4[0].animate.set_stroke(S.GREY_DARK, 2.5), run_time=0.4)

    # ================================================================ 2. test yourself
    def questions_beat(self):
        head = S.text("Test yourself", 44, S.YELLOW).to_edge(UP, buff=0.45)

        # --- question 1: the average of n numbers in [0, 1]
        card1 = question_card([r"Sensitivity of the average of $n$ numbers in $[0,\,1]$?"])
        ly = -1.75
        nl = Line([-4.5, ly, 0], [4.5, ly, 0], color=S.GREY, stroke_width=2.5)
        ends = VGroup(*[VGroup(Line([x, ly - 0.12, 0], [x, ly + 0.12, 0], color=S.GREY, stroke_width=2.5),
                               S.text(lab, 26, S.GREY).move_to([x, ly - 0.42, 0]))
                        for x, lab in ((-4.5, "0"), (4.5, "1"))])
        vals = [0.18, 0.27, 0.36, 0.44, 0.58, 0.63, 0.71, 0.86]
        X = lambda v: -4.5 + 9.0 * v
        others = VGroup(*[Dot([X(v), ly, 0], radius=0.1, color=S.GREY) for v in vals])
        av = ValueTracker(0.05)
        alice = always_redraw(lambda: Dot([X(av.get_value()), ly, 0], radius=0.12, color=ALICE).set_z_index(3))
        alice_l = always_redraw(lambda: S.text("Alice", 22, ALICE).move_to([X(av.get_value()), ly + 0.4, 0]))

        def mean():
            return (sum(vals) + av.get_value()) / (len(vals) + 1)

        avg = always_redraw(lambda: VGroup(
            Triangle(color=TRUTH_COLOR, stroke_width=0).set_fill(TRUTH_COLOR, 1).scale(0.11)
            .move_to([X(mean()), ly - 0.32, 0]),
            S.text("average", 24, TRUTH_COLOR).move_to([X(mean()), ly - 0.7, 0])))

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)          # the recap panels
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("First:")
            self.play(FadeIn(card1, scale=0.95), run_time=0.6)
            self.play(Create(nl), FadeIn(ends), LaggedStart(*[FadeIn(d, scale=0.5) for d in others],
                                                             lag_ratio=0.1), run_time=0.9)
            self.add(alice, alice_l, avg)
            self.wait(0.3)
            self.play(av.animate.set_value(0.95), run_time=1.6)
            self.play(av.animate.set_value(0.05), run_time=vo.remaining(0.8))
        drain(self, card1, 8)
        for m in (alice, alice_l, avg):
            m.clear_updaters()
        pic1 = VGroup(nl, ends, others, alice, alice_l, avg)

        # --- question 2: one patient, fifty clipped slice gradients
        card2 = question_card([r"Each patient contributes 50 slices;",
                               r"each slice's gradient is clipped to size $C$.",
                               r"How much can one patient change the summed gradient?"])
        card2.move_to([0, CARD_Y - 0.15, 0])
        py = -2.05
        patient = person_icon(ALICE, height=0.85).move_to([-5.2, py + 0.1, 0])
        patient_l = S.text("one patient", 22, ALICE).next_to(patient, DOWN, buff=0.15)
        slices = VGroup(*[RoundedRectangle(width=0.75, height=0.75, corner_radius=0.08, stroke_color=S.GREY,
                                           stroke_width=2).set_fill(S.GREY_DARKER, 1)
                          .shift(RIGHT * 0.09 * k + UP * 0.09 * k) for k in range(5)])
        slices.move_to([-3.25, py + 0.1, 0])
        slices_l = S.text("50 slices", 22, S.GREY).next_to(slices, DOWN, buff=0.12)
        patient_l.set_y(slices_l.get_y())
        a1 = Arrow(patient.get_right(), slices.get_left(), buff=0.15, color=S.GREY, stroke_width=3,
                   tip_length=0.16)
        grad_rng = np.random.default_rng(21)
        R = 0.4
        xs = [-1.25, -0.15, 0.95, 2.05, 3.15]
        circles, grads, clipped = VGroup(), VGroup(), []
        for x in xs:
            ang = grad_rng.uniform(0, 2 * np.pi)
            ln = grad_rng.uniform(0.25, 0.85)
            c = np.array([x, py + 0.1, 0])
            u = np.array([np.cos(ang), np.sin(ang), 0])
            circles.add(DashedVMobject(Circle(radius=R, color=SENS_COLOR, stroke_width=2), num_dashes=18)
                        .move_to(c))
            grads.add(Arrow(c, c + ln * u, buff=0, color=S.WHITE, stroke_width=3.5, tip_length=0.12,
                            max_tip_length_to_length_ratio=0.5))
            clipped.append(Arrow(c, c + min(ln, R) * u, buff=0, color=S.WHITE, stroke_width=3.5, tip_length=0.12,
                                 max_tip_length_to_length_ratio=0.5))
        more = S.math(r"\cdots", size=40, color=S.GREY).move_to([4.15, py + 0.1, 0])
        a2 = Arrow(slices.get_right(), [xs[0] - R - 0.05, py + 0.1, 0], buff=0.15, color=S.GREY, stroke_width=3,
                   tip_length=0.16)
        clip_l = S.math(r"\text{each slice: }\ \|g\|", r"\le", r"C", size=30)
        clip_l[2].set_color(SENS_COLOR)
        clip_l.move_to([1.0, patient_l.get_y(), 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(card1, pic1)), run_time=0.5)
            self.play(FadeIn(card2, scale=0.95), run_time=0.6)
            vo.wait_until("each patient contributes")
            self.play(FadeIn(patient, shift=RIGHT * 0.2), FadeIn(patient_l), run_time=0.6)
            self.play(GrowArrow(a1), LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in slices], lag_ratio=0.15),
                      FadeIn(slices_l), run_time=0.9)
            vo.wait_until("and each slice")
            self.play(GrowArrow(a2), LaggedStart(*[GrowArrow(g) for g in grads], lag_ratio=0.12), FadeIn(more),
                      run_time=1.0)
            vo.wait_until("is clipped to size C")
            self.play(LaggedStart(*[Create(c) for c in circles], lag_ratio=0.1), FadeIn(clip_l), run_time=0.8)
            self.play(*[Transform(g, cg) for g, cg in zip(grads, clipped)], run_time=0.8)
            vo.wait_until("How much can one patient")
            self.play(Indicate(patient, color=ALICE, scale_factor=1.2), run_time=vo.remaining(0.8))
        drain(self, card2, 10)
        pic2 = VGroup(patient, patient_l, slices, slices_l, a1, a2, circles, grads, more, clip_l)

        # --- question 3: the median
        card3 = question_card([r"Why does the median give", r"the Laplace mechanism trouble?"])
        my = -2.35
        nl3 = Line([-4.5, my, 0], [4.5, my, 0], color=S.GREY, stroke_width=2.5)
        mvals = [-3.9, -3.1, -2.2, -1.6, -0.2, 0.9, 1.7, 2.9, 3.8]
        mdots = VGroup(*[Dot([v, my, 0], radius=0.1, color=S.WHITE if k == 4 else S.GREY)
                         for k, v in enumerate(mvals)]).set_z_index(2)
        med_l = S.text("median", 24, TRUTH_COLOR).next_to(mdots[4], DOWN, buff=0.18)
        mtent = FunctionGraph(lambda u: 1.3 * np.exp(-abs(u) / 0.55), x_range=[-2.6, 2.6, 0.01], color=NOISE_COLOR,
                              stroke_width=4).shift([mvals[4], my, 0])
        lap_l = S.math(r"+\ \mathrm{Lap}\!\left(", r"S(\mathrm{median})", "/", r"\varepsilon", r"\right)", size=32)
        lap_l[1].set_color(SENS_COLOR)
        lap_l[3].set_color(EPS_COLOR)
        lap_l.move_to([mvals[4] + 2.75, my + 1.0, 0])
        footer = S.text("answers + more exercises: companion notes (link in the description)", 24, S.GREY)
        footer.move_to([0, -3.3, 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(card2, pic2)), run_time=0.5)
            self.play(FadeIn(card3, scale=0.95), run_time=0.6)
            self.play(Create(nl3), LaggedStart(*[FadeIn(d, scale=0.5) for d in mdots], lag_ratio=0.08), run_time=0.8)
            self.play(Indicate(mdots[4], color=S.WHITE, scale_factor=1.6), FadeIn(med_l), run_time=0.7)
            self.play(Create(mtent), FadeIn(lap_l), run_time=0.8)
            vo.wait_until("Answers, and more")
            self.play(FadeIn(footer, shift=UP * 0.15), run_time=0.6)
        drain(self, card3, 8)
        return VGroup(head, card3, nl3, mdots, med_l, mtent, lap_l, footer)

    # ================================================================ 3. the better questions
    def closing_beat(self, leftovers):
        # Chinese has no italics (Pango would slant the Hanzi synthetically): the quote stays upright there
        quote_kw = {} if i18n.active() else {"slant": ITALIC}
        quote = S.text("“It’s safe: it’s anonymized.”", 36, S.GREY, **quote_kw).move_to([0, 2.2, 0])
        q1 = S.tex(r"What's the ", r"$\varepsilon$", r"?", size=64)
        q1[1].set_color(EPS_COLOR)
        q2 = S.tex(r"What counts as ", r"one person's row", r"?", size=64)
        q2[1].set_color(ALICE)
        qs = VGroup(q1, q2).arrange(DOWN, buff=0.55).move_to([0, -0.35, 0])

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(leftovers), run_time=0.6)                       # question 3's card
            self.play(FadeIn(quote, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("you will know")
            self.play(quote.animate.set_opacity(0.45), run_time=0.6)
            vo.wait_until("what is the epsilon")
            self.play(FadeIn(q1, shift=UP * 0.25), run_time=0.7)
            vo.wait_until("and what counts")
            self.play(FadeIn(q2, shift=UP * 0.25), run_time=0.7)
        self.play(Indicate(q2[1], color=ALICE, scale_factor=1.06), run_time=1.0)   # let the questions land

        # the paper
        img, frame = paper_page(PAPER_P1, height=3.6)
        page = Group(img, frame).move_to([-3.9, -1.3, 0])
        hl = Rectangle(width=img.width * 0.80, height=img.height * 0.062, color=S.YELLOW, stroke_width=3)
        hl.move_to(img.get_corner(UL) + RIGHT * img.width * 0.5 + DOWN * img.height * 0.0995)
        cite = VGroup(
            S.text("C. Dwork, F. McSherry, K. Nissim, A. Smith", 28, S.WHITE),
            S.text("Calibrating Noise to Sensitivity", 32, S.YELLOW, slant=ITALIC),
            S.text("in Private Data Analysis", 32, S.YELLOW, slant=ITALIC),
            S.text("TCC 2006 · LNCS 3876, pp. 265–284", 26, S.GREY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        cite[2].shift(UP * 0.08)
        cite.next_to(page, RIGHT, buff=0.6).align_to(page, UP).shift(DOWN * 0.45)
        sep = S.text("·", 44, S.GREY)
        top = VGroup(q1.copy(), sep, q2.copy())
        top[0].scale(0.62)
        top[2].scale(0.62)
        top.arrange(RIGHT, buff=0.35).move_to([0, 2.3, 0])
        self.play(FadeOut(quote), q1.animate.scale(0.62).move_to(top[0]), q2.animate.scale(0.62).move_to(top[2]),
                  FadeIn(sep), run_time=0.9)
        self.play(FadeIn(page, shift=UP * 0.2), LaggedStart(*[FadeIn(c, shift=LEFT * 0.15) for c in cite],
                                                           lag_ratio=0.15), run_time=1.2)
        self.play(Create(hl), run_time=0.6)
        self.wait(3.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
