"""S05 · Why so strict? — statistical distance vs. the ratio test [Example 2, p. 271]."""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import database_rows, gaussian_pdf, laplace_pdf
from explainer.scene import VoiceScene

from common import ALICE, EPS_COLOR, NARRATION, X_COLOR, XP_COLOR

SAY = NARRATION["S05"]
SIG = 1.8                  # width of the two illustrative output curves (beat 1)
MU_X, MU_XP = 41.0, 42.0   # running example: f(x) = 41, f(x') = 42
T0, T1 = 34.0, 49.0
BAR_H = 1.7                # bar height that stands for probability 1/n


def db_stack(names, values, width=3.0, row_h=0.5, size=24):
    """Database row stack with a vertical-dots gap before the last row ("n rows").

    Returns (stack, rows, dots); rows[i] = VGroup(box, icon, name, value)."""
    rows = database_rows(names, values, color=S.GREY, width=width, row_height=row_h, size=size)
    rows[-1].shift(DOWN * row_h)
    dots = S.math(r"\vdots", size=30, color=S.GREY)
    dots.move_to((rows[-2].get_bottom() + rows[-1].get_top()) / 2)
    return VGroup(rows, dots), rows, dots


def mark_alice(row):
    row[0].set_stroke(ALICE, 2.5)
    row[1].set_fill(ALICE, 1)
    row[2].set_color(ALICE)


def lens(ax, f_hi, f_lo, a, b, color, opacity=0.5, step=0.02):
    """Filled region between two curves on [a, b] (f_hi >= f_lo there)."""
    ts = np.arange(a, b + step / 2, step)
    pts = [ax.c2p(t, f_hi(t)) for t in ts] + [ax.c2p(t, f_lo(t)) for t in ts[::-1]]
    return Polygon(*pts, stroke_width=0).set_fill(color, opacity)


def frac_split(glyphs):
    """(numerator glyphs, denominator glyphs), each sorted left to right, of the widest fraction."""
    bar = max(glyphs, key=lambda m: m.width / max(m.height, 1e-3))
    x0, x1, yb = bar.get_left()[0] - 0.01, bar.get_right()[0] + 0.01, bar.get_y()
    inside = [m for m in glyphs if m is not bar and x0 <= m.get_x() <= x1]
    num = sorted([m for m in inside if m.get_y() > yb], key=lambda m: m.get_x())
    den = sorted([m for m in inside if m.get_y() < yb], key=lambda m: m.get_x())
    return num, den


def frac_infty(num, den, size=60):
    """num/den = infinity, with the numerator ORANGE (world x'), denominator BLUE (world x)."""
    m = S.math(r"\frac{" + num + "}{" + den + r"}", "=", r"\infty", size=size)
    n, d = frac_split(m[0])
    VGroup(*n).set_color(XP_COLOR)
    VGroup(*d).set_color(X_COLOR)
    m[2].set_color(S.RED)
    return m


class WhyStrict(VoiceScene):
    def construct(self):
        # ============================================================ 0. statistical distance
        title = S.text("Why a ratio, for every output?", 44).to_edge(UP, buff=0.55)
        ax = Axes(x_range=[T0, T1, 1], y_range=[0, 0.25, 0.05], x_length=11.6, y_length=3.0,
                  tips=False, axis_config={"color": S.GREY, "stroke_width": 2}).shift(DOWN * 1.35)
        axis = ax.x_axis
        out_lab = S.text("output t", 22, S.GREY).next_to(axis.get_right(), DOWN, buff=0.2)
        p_x = lambda t: float(gaussian_pdf(t, MU_X, SIG))
        p_xp = lambda t: float(gaussian_pdf(t, MU_XP, SIG))
        c_x = ax.plot(p_x, x_range=[T0, T1, 0.02], color=X_COLOR, stroke_width=5)
        c_xp = ax.plot(p_xp, x_range=[T0, T1, 0.02], color=XP_COLOR, stroke_width=5)
        lab_x = S.math("M(x)", size=34, color=X_COLOR).next_to(ax.c2p(38.3, p_x(38.3)), UL, buff=0.1)
        lab_xp = S.math("M(x')", size=34, color=XP_COLOR).next_to(ax.c2p(44.7, p_xp(44.7)), UR, buff=0.1)
        mid = (MU_X + MU_XP) / 2
        lens_x = lens(ax, p_x, p_xp, T0, mid, X_COLOR)
        lens_xp = lens(ax, p_xp, p_x, mid, T1, XP_COLOR)

        sd = S.math(r"\text{statistical distance}", "=", r"\tfrac{1}{2}", r"\times", r"\text{shaded area}",
                    size=42)
        sd.move_to(UP * 1.75)
        ev = S.math("=", r"\max_{\text{events }A}\ \big|\Pr[", "M(x)", r"\in A]", "-", r"\Pr[", "M(x')",
                    r"\in A]\big|", size=38)
        ev[2].set_color(X_COLOR)
        ev[6].set_color(XP_COLOR)
        ev.next_to(sd, DOWN, buff=0.35)
        ev.shift(RIGHT * (sd[1].get_x() - ev[0].get_x()))
        if ev.get_right()[0] > 6.4:
            ev.shift(LEFT * (ev.get_right()[0] - 6.4))
        ev_line = Line(ax.c2p(T0, 0), ax.c2p(mid, 0), color=S.WHITE, stroke_width=8)
        ev_lab = S.math(r"\text{event } A = \{t < 41.5\}", size=30).next_to(ev_line, DOWN, buff=0.15)

        with self.voiceover(SAY[0]) as vo:
            self.play(Write(title), run_time=1.0)
            self.play(Create(axis), FadeIn(out_lab), Create(c_x), Create(c_xp), run_time=1.6)
            self.play(FadeIn(lab_x), FadeIn(lab_xp), run_time=0.5)
            vo.wait_until("statistical distance")
            self.play(Write(sd[0]), run_time=0.9)
            vo.wait_until("half the area")
            self.play(FadeIn(lens_x), FadeIn(lens_xp), run_time=0.8)
            self.play(Write(sd[1:]), run_time=0.9)
            self.play(Indicate(sd[4], color=S.WHITE), run_time=0.6)
            vo.wait_until("Equivalently")
            self.play(Create(ev_line), FadeIn(ev_lab), run_time=0.8)
            self.play(Write(ev), run_time=1.6)
            self.play(Indicate(lens_x, color=X_COLOR, scale_factor=1.0), run_time=1.0)
            vo.wait_until("The paper shows")
            self.play(Circumscribe(title, color=S.YELLOW), run_time=vo.remaining(1.0))

        # ============================================================ 1. publish one random row
        caption = S.text("Mechanism: publish one random row", 34).to_edge(UP, buff=0.55)
        names = ["Bob", "Carol", "Dev", "Alice"]
        stack, rows, dots = db_stack(names, ["no X", "has X", "no X", "no X"])
        mark_alice(rows[-1])
        rows[-1][3].set_color(X_COLOR)
        stack.move_to([-4.35, 0.15, 0])
        db_word = S.text("database", 28, S.GREY)
        db_x = S.math("x", size=44, color=X_COLOR)
        db_lab = VGroup(db_word, db_x).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        db_lab.next_to(stack, UP, buff=0.3)
        n_lab = S.text("n rows", 24, S.GREY).next_to(stack, DOWN, buff=0.25)
        db_xp = S.math("x'", size=44, color=XP_COLOR).move_to(db_x, aligned_edge=LEFT)

        slots_y = [r.get_y() for r in rows[:3]] + [dots.get_y(), rows[3].get_y()]
        pointer = Triangle(fill_opacity=1, stroke_width=0).set_fill(S.WHITE, 1).rotate(-PI / 2)
        pointer.scale_to_fit_height(0.26).move_to([stack.get_left()[0] - 0.3, slots_y[0], 0])
        hl = Rectangle(width=rows[0].width, height=rows[0].height, stroke_color=S.WHITE,
                       stroke_width=3).move_to([stack.get_x(), slots_y[0], 0])
        spin = ValueTracker(0.0)

        def follow(m):
            k = int(np.floor(spin.get_value() + 1e-6)) % 5
            m.set_y(slots_y[k])

        token_txt = S.text("(Carol, has X)", 28)
        token_box = SurroundingRectangle(token_txt, color=S.WHITE, buff=0.18, corner_radius=0.08,
                                         stroke_width=2).set_fill(S.GREY_DARKER, 1)
        token = VGroup(token_box, token_txt).move_to([0.9, rows[1].get_y(), 0])
        token_head = S.text("published", 22, S.GREY).next_to(token, UP, buff=0.12)

        # --- the output distribution: one slot per possible output (name, value)
        persons = ["Bob", "Carol", "Dev", None, "Alice"]
        truth_x = {"Bob": "no", "Carol": "has", "Dev": "no", "Alice": "no"}
        truth_xp = dict(truth_x, Alice="has")
        slot_w, pair_gap, base_y = 0.76, 0.28, -2.15
        cursor = -1.25
        slot_x = {}
        bases, slot_labs, name_labs = VGroup(), VGroup(), VGroup()
        ell = None
        for p in persons:
            if p is None:
                ell = S.math(r"\cdots", size=34, color=S.GREY).move_to([cursor + 0.3, base_y - 0.3, 0])
                cursor += 0.6 + pair_gap
                continue
            for k, out in enumerate(["no", "has"]):
                cx = cursor + slot_w * (k + 0.5)
                slot_x[(p, out)] = cx
                slot_labs.add(S.text(out, 20, S.GREY).move_to([cx, base_y - 0.27, 0]))
            bases.add(Line([cursor + 0.04, base_y, 0], [cursor + 2 * slot_w - 0.04, base_y, 0],
                           color=S.GREY, stroke_width=2))
            name_labs.add(S.text(p, 22, ALICE if p == "Alice" else S.WHITE)
                          .move_to([cursor + slot_w, base_y - 0.66, 0]))
            cursor += 2 * slot_w + pair_gap
        chart_left = -1.25
        y_tick = VGroup(Line([chart_left - 0.12, base_y + BAR_H, 0], [chart_left + 0.02, base_y + BAR_H, 0],
                             color=S.GREY, stroke_width=2),
                        DashedLine([chart_left, base_y + BAR_H, 0], [cursor - pair_gap, base_y + BAR_H, 0],
                                   color=S.GREY_DARK, stroke_width=1.5, dash_length=0.08))
        y_lab = S.math("1/n", size=30, color=S.GREY).next_to(y_tick[0], LEFT, buff=0.1)

        def bar(p, out, world):
            cx = slot_x[(p, out)] + (-0.15 if world == "x" else 0.15)
            col = X_COLOR if world == "x" else XP_COLOR
            return Rectangle(width=0.26, height=BAR_H, stroke_width=0).set_fill(col, 0.9) \
                .move_to([cx, base_y + BAR_H / 2, 0])

        bars_x = {p: bar(p, truth_x[p], "x") for p in truth_x}
        bars_xp = {p: bar(p, truth_xp[p], "xp") for p in truth_xp}
        leg = VGroup(
            VGroup(Square(0.22, stroke_width=0).set_fill(X_COLOR, 0.9), S.text("world", 24, S.GREY),
                   S.math("x", size=34, color=X_COLOR)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.22, stroke_width=0).set_fill(XP_COLOR, 0.9), S.text("world", 24, S.GREY),
                   S.math("x'", size=34, color=XP_COLOR)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.5).move_to([2.6, 0.25, 0])
        alice_xs = [slot_x[("Alice", "no")], slot_x[("Alice", "has")]]
        alice_box = Rectangle(width=2 * slot_w + 0.16, height=BAR_H + 1.25, stroke_color=ALICE,
                              stroke_width=3).move_to([np.mean(alice_xs), base_y + BAR_H / 2 - 0.42, 0])
        sd_val = S.math(r"\text{statistical distance}", "=", r"\frac12\Big(\frac1n+\frac1n\Big)", "=",
                        r"\frac1n", size=38).move_to([2.6, 1.75, 0])
        tiny = S.text("tiny for a big database: looks private?", 26, S.GREY).next_to(sd_val, DOWN, buff=0.25)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(title, axis, out_lab, c_x, c_xp, lab_x, lab_xp, lens_x, lens_xp, sd, ev,
                                     ev_line, ev_lab)), run_time=0.6)
            self.play(FadeIn(caption, shift=DOWN * 0.2), FadeIn(stack), FadeIn(db_lab), FadeIn(n_lab),
                      FadeIn(bases), FadeIn(slot_labs), FadeIn(name_labs), FadeIn(ell), FadeIn(y_tick),
                      FadeIn(y_lab), run_time=0.8)
            vo.wait_until("pick one row")
            pointer.add_updater(follow)
            hl.add_updater(follow)
            self.play(FadeIn(pointer), FadeIn(hl), run_time=0.2)
            self.play(spin.animate.set_value(11.0), run_time=1.8, rate_func=rate_functions.ease_out_cubic)
            pointer.clear_updaters()
            hl.clear_updaters()
            self.play(TransformFromCopy(rows[1], token), FadeIn(token_head), run_time=0.7)
            self.play(token.animate.scale(0.5).move_to([slot_x[("Carol", "has")], base_y + BAR_H + 0.3, 0])
                      .set_opacity(0), FadeOut(token_head),
                      *[GrowFromEdge(bars_x[p], DOWN) for p in truth_x], FadeIn(leg[0]), run_time=0.8)
            vo.wait_until("Change one person")
            self.play(FadeOut(VGroup(pointer, hl)),
                      Transform(rows[-1][3], S.text("has X", 24, XP_COLOR).move_to(rows[-1][3])),
                      Transform(db_x, db_xp), run_time=0.7)
            self.play(*[GrowFromEdge(bars_xp[p], DOWN) for p in truth_xp], FadeIn(leg[1]), run_time=0.7)
            vo.wait_until("moves by only")
            self.play(Create(alice_box), run_time=0.6)
            self.play(Write(sd_val), run_time=1.3)
            vo.wait_until("For a big database")
            self.play(FadeIn(tiny, shift=UP * 0.15), run_time=0.7)

        # ============================================================ 2. the ratio is infinite
        has_x = slot_x[("Alice", "has")]
        has_base = Line([has_x - slot_w / 2 + 0.04, base_y, 0], [has_x + slot_w / 2 - 0.04, base_y, 0],
                        color=S.GREY, stroke_width=2)
        zero_x = Line([has_x - 0.28, base_y, 0], [has_x - 0.02, base_y, 0], color=X_COLOR, stroke_width=6)
        zoom = VGroup(has_base, slot_labs[-1], bars_xp["Alice"], zero_x)
        zoom_t = zoom.copy().scale(1.6)
        zoom_t.shift(np.array([-2.7, -1.45, 0]) - zoom_t[0].get_center())
        name_t = S.text("Alice", 40, ALICE).next_to(zoom_t[1], DOWN, buff=0.25)
        others = VGroup(*bases, *slot_labs[:-1], *name_labs[:-1], ell, y_tick, y_lab,
                        *bars_x.values(), *[bars_xp[p] for p in ["Bob", "Carol", "Dev"]])
        lab_n = S.math(r"x'\!:\ 1/n", size=40, color=XP_COLOR).next_to(zoom_t[2], UP, buff=0.18)
        lab_0 = S.math(r"x\!:\ 0", size=40, color=X_COLOR).next_to(zoom_t[3], LEFT, buff=0.2)
        lab_0.shift(UP * 0.12)
        has_frame = SurroundingRectangle(VGroup(zoom_t, name_t, lab_n, lab_0), color=S.WHITE, buff=0.25,
                                         corner_radius=0.08)
        has_lab = S.math(r"\text{output }(\text{Alice, has X})", size=36).next_to(has_frame, UP, buff=0.15)
        ratio = frac_infty("1/n", "0", size=66).move_to([3.0, 0.6, 0])
        privacy = S.text("privacy", 44).move_to([3.0, -1.6, 0])
        cross = Cross(privacy, stroke_color=S.RED, stroke_width=8, scale_factor=1.25)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(tiny), LaggedStart(*[Indicate(n, color=S.WHITE, scale_factor=1.25)
                                                   for n in name_labs], lag_ratio=0.2),
                      LaggedStart(*[Indicate(r, color=S.WHITE, scale_factor=1.04) for r in rows],
                                  lag_ratio=0.2), run_time=1.6)
            vo.wait_until("The ratio test")
            self.add(has_base, zero_x)
            self.play(FadeOut(VGroup(caption, stack, db_lab, n_lab, leg, sd_val, alice_box, others)),
                      run_time=0.6)
            self.play(Transform(zoom, zoom_t), Transform(name_labs[-1], name_t), run_time=1.2)
            self.play(Create(has_frame), FadeIn(has_lab), run_time=0.8)
            vo.wait_until("has probability one over n")
            self.play(FadeIn(lab_n, shift=DOWN * 0.15), Indicate(zoom[2], color=XP_COLOR, scale_factor=1.05),
                      run_time=0.9)
            vo.wait_until("and zero in the other")
            self.play(FadeIn(lab_0, shift=RIGHT * 0.15), Flash(zoom[3].get_center(), color=X_COLOR,
                                                               flash_radius=0.4), run_time=0.8)
            self.play(Write(ratio[0]), run_time=0.7)
            vo.wait_until("The ratio is infinite")
            self.play(Write(ratio[1:]), FadeIn(privacy), run_time=0.6)
            self.play(Create(cross), run_time=0.5)

        # ============================================================ 3. averages vs. ratios; rounding
        line1 = S.text("Averages hide catastrophes", 40)
        line2 = S.text("that are rare for each person.", 40)
        avg = VGroup(line1, line2).arrange(DOWN, buff=0.2).move_to(UP * 1.4)
        def1 = S.math(r"\left|\ln\frac{\Pr[M(x)=t]}{\Pr[M(x')=t]}\right|", r"\le", r"\varepsilon", size=48)
        def1[2].set_color(EPS_COLOR)
        every = S.text("for every output t", 30, S.GREY)
        rule = VGroup(def1, every).arrange(RIGHT, buff=0.5).next_to(avg, DOWN, buff=0.75)
        # colour M(x) BLUE / M(x') ORANGE inside the fraction
        num, den = frac_split(def1[0])
        VGroup(*num[3:7]).set_color(X_COLOR)
        VGroup(*den[3:8]).set_color(XP_COLOR)

        nl = NumberLine(x_range=[40, 50, 1], length=10.4, color=S.GREY, stroke_width=2,
                        include_ticks=True, tick_size=0.08).move_to(DOWN * 0.8)
        nl_labs = VGroup(*[S.text(str(v), 22, S.GREY).next_to(nl.n2p(v), DOWN, buff=0.18)
                           for v in range(40, 51)])
        cut = DashedLine(nl.n2p(44.5) + DOWN * 0.25, nl.n2p(44.5) + UP * 2.6, color=S.GREY,
                         stroke_width=2, dash_length=0.1)
        cut_lab = S.text("rounding cut", 22, S.GREY).next_to(cut, UP, buff=0.1)
        dot44 = Dot(nl.n2p(44), color=X_COLOR, radius=0.1)
        dot45 = Dot(nl.n2p(45), color=XP_COLOR, radius=0.1)
        cnt44 = S.math(r"x\!:\ 44", size=32, color=X_COLOR).next_to(nl_labs[4], DOWN, buff=0.22)
        cnt44.align_to(nl_labs[4], RIGHT)
        cnt45 = S.math(r"x'\!:\ 45", size=32, color=XP_COLOR).next_to(nl_labs[5], DOWN, buff=0.22)
        cnt45.align_to(nl_labs[5], LEFT)
        arr44 = CurvedArrow(nl.n2p(44) + UP * 0.18, nl.n2p(40) + UP * 0.18 + RIGHT * 0.12, angle=PI / 3,
                            color=X_COLOR, stroke_width=4, tip_length=0.2)
        arr45 = CurvedArrow(nl.n2p(45) + UP * 0.18, nl.n2p(50) + UP * 0.18 + LEFT * 0.12, angle=-PI / 3,
                            color=XP_COLOR, stroke_width=4, tip_length=0.2)
        SPIKE = 2.3
        spike40 = Rectangle(width=0.16, height=SPIKE, stroke_width=0).set_fill(X_COLOR, 0.95)
        spike40.move_to(nl.n2p(40) + UP * SPIKE / 2)
        spike50 = Rectangle(width=0.16, height=SPIKE, stroke_width=0).set_fill(XP_COLOR, 0.95)
        spike50.move_to(nl.n2p(50) + UP * SPIKE / 2)
        pr40 = S.math(r"\Pr = 1", size=30, color=X_COLOR).next_to(spike40, UP, buff=0.12)
        pr50 = S.math(r"\Pr = 1", size=30, color=XP_COLOR).next_to(spike50, UP, buff=0.12)
        zero50 = Line(nl.n2p(50) + RIGHT * 0.12, nl.n2p(50) + RIGHT * 0.36, color=X_COLOR, stroke_width=7)
        zero50_lab = S.math("0", size=30, color=X_COLOR).next_to(zero50, UP, buff=0.1)
        readout = VGroup(S.math(r"\Pr[\text{output } 50]:", size=36),
                         S.math("1", size=40, color=XP_COLOR), S.text("vs", 28, S.GREY),
                         S.math("0", size=40, color=X_COLOR), S.math(r"\Rightarrow\ \infty", size=40,
                                                                     color=S.RED)).arrange(RIGHT, buff=0.2)
        readout.move_to([2.2, 2.75, 0])
        random_cap = S.text("to pass the ratio test, a mechanism must be random", 30, S.WHITE)
        random_cap.to_edge(DOWN, buff=0.45)
        LAMB = 1.3
        yscale = 1.7 / laplace_pdf(0, 0, LAMB)

        def bump(mu, col):
            pts = [nl.n2p(t) + UP * yscale * float(laplace_pdf(t, mu, LAMB)) for t in np.arange(40, 50.001, 0.02)]
            curve = VMobject(stroke_color=col, stroke_width=5).set_points_as_corners(pts)
            area = Polygon(*pts, nl.n2p(50), nl.n2p(40), stroke_width=0).set_fill(col, 0.18)
            return VGroup(area, curve)

        bump44 = bump(44, X_COLOR)
        bump45 = bump(45, XP_COLOR)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
            self.play(FadeIn(line1, shift=UP * 0.2), run_time=0.8)
            self.play(FadeIn(line2, shift=UP * 0.2), run_time=0.8)
            self.play(Indicate(line2, color=S.WHITE, scale_factor=1.05), run_time=1.0)
            vo.wait_until("A ratio bound")
            self.play(Write(def1), run_time=1.2)
            self.play(FadeIn(every, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("It also settles")
            self.play(FadeOut(VGroup(avg, rule)), run_time=0.6)
            self.play(Create(nl), FadeIn(nl_labs), run_time=0.9)
            vo.wait_until("at the jump")
            self.play(Create(cut), FadeIn(cut_lab), FadeIn(dot44), FadeIn(cnt44), FadeIn(dot45), FadeIn(cnt45),
                      run_time=0.6)
            self.play(Create(arr44), Create(arr45), run_time=0.7)
            vo.wait_until("one world gives")
            self.play(GrowFromEdge(spike40, DOWN), GrowFromEdge(spike50, DOWN), FadeIn(pr40), FadeIn(pr50),
                      run_time=0.9)
            vo.wait_until("the other with probability zero")
            self.play(Create(zero50), FadeIn(zero50_lab), run_time=0.6)
            self.play(FadeIn(readout, shift=DOWN * 0.15), Flash(nl.n2p(50) + UP * 0.1, color=S.RED,
                                                                 flash_radius=0.5), run_time=0.9)
            vo.wait_until("To pass this test")
            self.play(FadeOut(VGroup(arr44, arr45, cut, cut_lab, pr40, pr50, zero50, zero50_lab, readout)),
                      ReplacementTransform(spike40, bump44), ReplacementTransform(spike50, bump45),
                      FadeIn(random_cap, shift=UP * 0.2), run_time=1.6)
        self.wait(0.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
