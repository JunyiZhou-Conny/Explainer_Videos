"""S04 · Defining privacy: epsilon-indistinguishability (Definition 1, p. 270; App. A).

Picture before formula: two neighbouring worlds -> two output distributions -> a sliding ratio
readout that never leaves [e^-eps, e^eps] -> only then Definition 1 as a caption for it.

The pictured mechanism adds *logistic* noise of scale s = 5 to the count. Its log-density has slope
at most 1/s everywhere, so for counts 41 vs 42 the log-ratio stays strictly inside +-0.2: a genuine
eps = 0.2 mechanism with smooth curves (the Laplace kink is saved for S07).
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import database_rows, person_icon, ponder_card
from explainer.scene import VoiceScene

from common import ALICE, EPS_COLOR, NARRATION, X_COLOR, XP_COLOR

SAY = NARRATION["S04"]

ANALYST = S.PURPLE          # analyst / attacker role colour (as in S03)
COIN = S.GOLD
CHECK = S.TEAL
A, B = 41.0, 42.0           # f(x), f(x')
S_NOISE = 5.0               # logistic scale -> eps = 1/S_NOISE = 0.2
EPS = 1.0 / S_NOISE
T0, T1 = 20.0, 63.0         # visible output range
NAMES = ["Bob", "Carol", "Alice", "Dan", "Eve"]
VALUES = ["no X", "has X", "no X", "no X", "has X"]
ALICE_ROW = 2


def pdf(t, mu):
    """Logistic density with scale S_NOISE (smooth, and eps-private for shifts of 1)."""
    z = (np.asarray(t, dtype=float) - mu) / (2 * S_NOISE)
    return 1.0 / (4 * S_NOISE) / np.cosh(z) ** 2


def ratio(t):
    return float(pdf(t, A) / pdf(t, B))


# ---------------------------------------------------------------- small glyphs


def db_stack(frame_color, alice_value="no X", values=True, width=3.4, row_h=0.5, size=24) -> VGroup:
    """Row stack in the video's database style. Returns VGroup(frame, rows, alice_hl, vdots)."""
    vals = list(VALUES)
    vals[ALICE_ROW] = alice_value
    rows = database_rows(NAMES, vals if values else None, color=S.GREY, width=width, row_height=row_h,
                         size=size)
    if values:
        for r in rows:
            r[3].set_color(S.GREY).align_to(r[0], RIGHT).shift(LEFT * 0.2)
    a = rows[ALICE_ROW]
    a[0].set_fill(interpolate_color(ManimColor(S.GREY_DARKER), ManimColor(ALICE), 0.16), 1)
    a[1].set_fill(ALICE, 1)
    a[2].set_color(ALICE)
    if values:
        a[3].set_color(ALICE)
    hl = Rectangle(width=a[0].width, height=a[0].height, stroke_color=ALICE, stroke_width=3).move_to(a[0])
    dots = S.math(r"\vdots", size=30, color=S.GREY).next_to(rows, DOWN, buff=0.1)
    frame = SurroundingRectangle(VGroup(rows, dots), color=frame_color, buff=0.14, corner_radius=0.1,
                                 stroke_width=3)
    return VGroup(frame, rows, hl, dots)


def die_glyph(size=0.34, color=S.WHITE) -> VGroup:
    sq = RoundedRectangle(width=size, height=size, corner_radius=size * 0.18, stroke_color=color,
                          stroke_width=2)
    pips = VGroup(*[Dot(sq.get_center() + np.array([dx, dy, 0]) * size * 0.27, radius=size * 0.07,
                        color=color) for dx, dy in [(-1, 1), (0, 0), (1, -1)]])
    return VGroup(sq, pips)


def mech_box(color) -> VGroup:
    box = RoundedRectangle(width=1.45, height=0.82, corner_radius=0.12, stroke_color=color, stroke_width=3)
    box.set_fill(S.GREY_DARKER, 1)
    m = S.math("M", size=44).move_to(box).shift(LEFT * 0.25)
    die = die_glyph(0.32).move_to(box).shift(RIGHT * 0.38)
    return VGroup(box, m, die)


def coin_glyph(radius=0.24) -> VGroup:
    c = Circle(radius=radius, stroke_color=interpolate_color(ManimColor(COIN), ManimColor(S.BG), 0.35),
               stroke_width=3).set_fill(COIN, 0.9)
    inner = Circle(radius=radius * 0.62, stroke_color=S.BG, stroke_width=1.5, stroke_opacity=0.5)
    return VGroup(c, inner)


def cigarette() -> VGroup:
    body = Rectangle(width=0.5, height=0.09, stroke_width=0).set_fill(S.WHITE, 1)
    filt = Rectangle(width=0.15, height=0.09, stroke_width=0).set_fill(COIN, 1).next_to(body, LEFT, buff=0)
    ash = Rectangle(width=0.05, height=0.09, stroke_width=0).set_fill(S.GREY, 1).next_to(body, RIGHT, buff=0)
    smoke = VMobject(stroke_color=S.GREY, stroke_width=2).set_points_smoothly(
        [ash.get_right() + np.array([0.02 + 0.05 * np.sin(k * 1.6), 0.08 * k, 0]) for k in range(6)])
    return VGroup(filt, body, ash, smoke)


def flip(coin, turns: int = 2):
    """A coin toss: squash to edge-on and back, `turns` times."""
    return Succession(*[coin.animate(rate_func=there_and_back).stretch(0.06, 0) for _ in range(turns)])


def ponder_at(scene, question, seconds, pos, width=6.0) -> VGroup:
    """pause_and_ponder, but placed at `pos` so the supporting picture stays visible."""
    card = ponder_card(question, width=width).move_to(pos)
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return card


class Definition(VoiceScene):
    def construct(self):
        rng = np.random.default_rng(4)

        # ============================================================ 0. two neighbouring worlds
        db_x = db_stack(X_COLOR, "no X").move_to([-2.9, -0.1, 0])
        db_xp = db_stack(XP_COLOR, "no X").move_to([2.9, -0.1, 0])
        lab_x = S.math("x", size=64, color=X_COLOR).next_to(db_x[0], LEFT, buff=0.3)
        lab_xp = S.math("x'", size=64, color=XP_COLOR).next_to(db_xp[0], RIGHT, buff=0.3)
        alice_x, alice_xp = db_x[1][ALICE_ROW], db_xp[1][ALICE_ROW]
        has_x = S.text("has X", 24, ALICE, font=S.FONT_SANS).move_to(alice_xp[3]).align_to(alice_xp[3], RIGHT)
        neq = S.math(r"\neq", size=54, color=ALICE).move_to([0, alice_x.get_y(), 0])
        brace = Brace(VGroup(db_x[0], db_xp[0]), direction=UP, color=S.GREY, buff=0.15)
        brace_lab = VGroup(S.text("neighbors:", 30, S.WHITE), S.text("differ in one row", 30, S.GREY))
        brace_lab.arrange(RIGHT, buff=0.2).next_to(brace, UP, buff=0.12)
        cnt_x = S.text("count = 41", 30, X_COLOR).next_to(db_x[0], DOWN, buff=0.3)
        cnt_xp = S.text("count = 42", 30, XP_COLOR).next_to(db_xp[0], DOWN, buff=0.3)
        slot = DashedVMobject(Rectangle(width=alice_x[0].width, height=alice_x[0].height,
                                        stroke_color=S.GREY, stroke_width=2), num_dashes=30)
        cover = VGroup(Rectangle(width=alice_x[0].width + 0.02, height=alice_x[0].height + 0.02,
                                 stroke_width=0).set_fill(S.BG, 1), slot).move_to(alice_x)
        tag_added = S.text("hospital: Alice added", 24, S.GREY).move_to([0, -2.95, 0])
        tag_changed = S.text("here: Alice's row changed", 24, S.GREY).move_to(tag_added)

        with self.voiceover(SAY[0]) as vo:
            self.play(Create(db_x[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in db_x[1]],
                                                   lag_ratio=0.12),
                      FadeIn(db_x[2]), FadeIn(db_x[3]), run_time=1.6)
            vo.wait_until("In one, the database")
            self.play(Write(lab_x), Indicate(db_x[0], color=X_COLOR, scale_factor=1.02), run_time=0.9)
            vo.wait_until("In the other")
            self.play(TransformFromCopy(db_x, db_xp, path_arc=-0.5), run_time=1.3)
            self.play(Write(lab_xp), run_time=0.6)
            vo.wait_until("except for one row")
            self.play(Transform(alice_xp[3], has_x), run_time=0.8)
            vo.wait_until("Say, Alice")
            self.play(Indicate(VGroup(alice_x, db_x[2]), color=ALICE, scale_factor=1.06),
                      Indicate(VGroup(alice_xp, db_xp[2]), color=ALICE, scale_factor=1.06),
                      FadeIn(neq, scale=1.4), run_time=1.0)
            vo.wait_until("Databases like this")
            self.play(GrowFromCenter(brace), FadeIn(brace_lab, shift=DOWN * 0.15), run_time=0.9)
            vo.wait_until("In the hospital")
            self.play(FadeIn(cover), FadeIn(tag_added, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("here, her row")
            self.play(FadeOut(cover), ReplacementTransform(tag_added, tag_changed), run_time=0.7)
            self.play(FadeIn(cnt_x, shift=UP * 0.15), FadeIn(cnt_xp, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("Either way")
            self.play(Circumscribe(VGroup(alice_x, alice_xp, neq), color=ALICE, time_width=0.6),
                      run_time=vo.remaining(1.0))

        # ============================================================ 1. mechanism -> two distributions
        top_y = 2.55
        m_x = mech_box(X_COLOR).move_to([-3.6, 0.8, 0])
        m_xp = mech_box(XP_COLOR).move_to([3.6, 0.8, 0])
        ax1 = Axes(x_range=[T0, T1, 10], y_range=[0, 0.055, 0.055], x_length=11.0, y_length=2.5, tips=False,
                   axis_config={"color": S.GREY, "stroke_width": 2},
                   y_axis_config={"include_ticks": False}).move_to([0, -1.7, 0])
        ticks1 = VGroup(*[S.text(str(v), 20, S.GREY).next_to(ax1.c2p(v, 0), DOWN, buff=0.12)
                          for v in range(20, 51, 10)])
        out_lab1 = VGroup(S.text("output", 22, S.GREY), S.math("t", size=32, color=S.GREY))
        out_lab1.arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        out_lab1.next_to(ax1.x_axis.get_right(), DOWN, buff=0.18).align_to(ax1.x_axis, RIGHT).shift(RIGHT * 0.6)
        foot = VGroup(S.text("paper's notation:", 20, S.GREY),
                      S.math(r"\mathcal{T} = \text{transcript},\ \ \mathrm{San} = \text{sanitizer}", size=28,
                             color=S.GREY)).arrange(DOWN, buff=0.1).move_to([0, 0.8, 0])

        def plot_pair(ax):
            cx = ax.plot(lambda t: pdf(t, A), x_range=[T0 + 0.5, T1 - 0.5, 0.05], color=X_COLOR, stroke_width=4)
            cxp = ax.plot(lambda t: pdf(t, B), x_range=[T0 + 0.5, T1 - 0.5, 0.05], color=XP_COLOR,
                          stroke_width=4)
            fx = ax.get_area(cx, x_range=[T0 + 0.5, T1 - 0.5], color=X_COLOR, opacity=0.07)
            fxp = ax.get_area(cxp, x_range=[T0 + 0.5, T1 - 0.5], color=XP_COLOR, opacity=0.07)
            return cx, cxp, fx, fxp

        c1x, c1xp, a1x, a1xp = plot_pair(ax1)

        def samples(mu, k):
            u = rng.uniform(0.02, 0.98, size=k)
            return np.clip(mu + S_NOISE * np.log(u / (1 - u)), T0 + 1, T1 - 1)

        sx, sxp = samples(A, 18), samples(B, 18)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(brace, brace_lab, neq, cnt_x, cnt_xp, tag_changed)), run_time=0.5)
            self.play(db_x.animate.scale(0.5).move_to([-3.6, top_y, 0]),
                      db_xp.animate.scale(0.5).move_to([3.6, top_y, 0]),
                      lab_x.animate.scale(0.7).move_to([-5.2, top_y, 0]),
                      lab_xp.animate.scale(0.7).move_to([5.25, top_y, 0]), run_time=1.1)
            arr_dx = Arrow(db_x.get_bottom(), m_x.get_top(), buff=0.06, color=S.GREY, stroke_width=3,
                           max_tip_length_to_length_ratio=0.35, tip_length=0.16)
            arr_dxp = Arrow(db_xp.get_bottom(), m_xp.get_top(), buff=0.06, color=S.GREY, stroke_width=3,
                            max_tip_length_to_length_ratio=0.35, tip_length=0.16)
            self.play(GrowArrow(arr_dx), GrowArrow(arr_dxp), FadeIn(m_x, shift=DOWN * 0.15),
                      FadeIn(m_xp, shift=DOWN * 0.15), run_time=0.9)
            vo.wait_until("in each world")
            self.play(Rotate(m_x[2], angle=PI), Rotate(m_xp[2], angle=PI), run_time=0.8)
            vo.wait_until("Whatever the analyst")
            self.play(Create(ax1), FadeIn(ticks1), FadeIn(out_lab1), run_time=0.9)
            # one noisy answer from each world
            first = []
            for val, mbox, col, dy in ((sx[0], m_x, X_COLOR, 0.09), (sxp[0], m_xp, XP_COLOR, 0.22)):
                d = Dot(mbox.get_bottom(), radius=0.07, color=col)
                num = DecimalNumber(val, num_decimal_places=1, font_size=30, color=col)
                num.next_to(ax1.c2p(val, 0), UP, buff=0.32 + dy)
                first.append((d, ax1.c2p(val, 0) + UP * dy, num))
            self.play(*[d.animate.move_to(p) for d, p, _ in first], run_time=0.9)
            self.play(*[FadeIn(num, shift=DOWN * 0.1) for _, _, num in first], FadeIn(foot), run_time=0.6)
            vo.wait_until("for now, a single")
            self.play(*[Indicate(num, color=num.get_color(), scale_factor=1.25) for _, _, num in first],
                      run_time=0.8)
            # many more runs
            rain = []
            for vals, mbox, col, dy in ((sx[1:], m_x, X_COLOR, 0.09), (sxp[1:], m_xp, XP_COLOR, 0.22)):
                for v in vals:
                    d = Dot(mbox.get_bottom(), radius=0.05, color=col)
                    rain.append((d, ax1.c2p(v, 0) + UP * dy))
            order = rng.permutation(len(rain))
            self.play(FadeOut(VGroup(*[num for _, _, num in first])),
                      LaggedStart(*[rain[i][0].animate.move_to(rain[i][1]) for i in order], lag_ratio=0.06),
                      run_time=2.2)
            dots = VGroup(*[d for d, _ in rain], *[d for d, _, _ in first])
            vo.wait_until("Because the mechanism")
            self.play(Create(c1x), Create(c1xp), run_time=1.8)
            self.play(FadeIn(a1x), FadeIn(a1xp), dots.animate.set_opacity(0.25), run_time=0.8)
            vo.wait_until("a whole distribution")
            self.play(Indicate(c1x, color=X_COLOR, scale_factor=1.04), Indicate(c1xp, color=XP_COLOR, scale_factor=1.04),
                      run_time=vo.remaining(0.8))

        # ============================================================ 2. slide t: the ratio stays in a band
        ax2 = Axes(x_range=[T0, T1, 10], y_range=[0, 0.055, 0.055], x_length=8.6, y_length=3.4, tips=False,
                   axis_config={"color": S.GREY, "stroke_width": 2},
                   y_axis_config={"include_ticks": False}).move_to([-2.0, -0.8, 0])
        c2x, c2xp, a2x, a2xp = plot_pair(ax2)
        tv = ValueTracker(33.0)

        def h2(t, mu):  # screen height of a curve at t on ax2
            return ax2.c2p(t, pdf(t, mu))[1] - ax2.c2p(t, 0)[1]

        def stick(mu, col, dx):
            t = tv.get_value()
            h = max(h2(t, mu), 0.01)
            r = Rectangle(width=0.075, height=h, stroke_width=0).set_fill(col, 0.95)
            return r.move_to(ax2.c2p(t, 0) + RIGHT * dx, aligned_edge=DOWN)

        stick_x = always_redraw(lambda: stick(A, X_COLOR, -0.04))
        stick_xp = always_redraw(lambda: stick(B, XP_COLOR, 0.04))
        tri = Triangle(color=S.WHITE, fill_opacity=1, stroke_width=0).scale(0.11)
        t_lab = S.math("t", size=34)
        marker = VGroup(tri, t_lab.next_to(tri, DOWN, buff=0.06))
        marker.add_updater(lambda m: m.move_to(ax2.c2p(tv.get_value(), 0) + DOWN * 0.38))

        # the readout: blue height / orange height, as two bars on one baseline
        K = 0.45
        base_y = 1.25
        bx, bxp = 2.95, 4.25

        def bar(mu, col, x):
            h = max(K * h2(tv.get_value(), mu), 0.01)
            return Rectangle(width=0.44, height=h, stroke_width=0).set_fill(col, 0.95).move_to(
                [x, base_y, 0], aligned_edge=DOWN)

        bar_x = always_redraw(lambda: bar(A, X_COLOR, bx))
        bar_xp = always_redraw(lambda: bar(B, XP_COLOR, bxp))
        div = S.math(r"\div", size=44).move_to([(bx + bxp) / 2, base_y + 0.45, 0])
        eq = S.math("=", size=44).move_to([bxp + 0.62, base_y + 0.45, 0])
        num = DecimalNumber(ratio(tv.get_value()), num_decimal_places=2, font_size=48)
        num.next_to(eq, RIGHT, buff=0.22)
        num.add_updater(lambda m: m.set_value(ratio(tv.get_value())))

        # the gauge (log scale, so the band is symmetric about 1)
        gx, gy, half, vmax = 5.75, -1.0, 1.75, 0.3

        def gpt(v):
            return np.array([gx, gy + half * v / vmax, 0.0])

        g_line = Line(gpt(-vmax), gpt(vmax), color=S.GREY, stroke_width=3)
        g_one = Line(gpt(0) + LEFT * 0.14, gpt(0) + RIGHT * 0.14, color=S.WHITE, stroke_width=3)
        g_one_lab = S.math("1", size=32).next_to(g_one, LEFT, buff=0.15)
        g_title = S.text("ratio", 22, S.GREY).next_to(g_line, UP, buff=0.15)
        band = Rectangle(width=0.5, height=gpt(EPS)[1] - gpt(-EPS)[1], stroke_width=0)
        band.set_fill(EPS_COLOR, 0.16).move_to(gpt(0))
        e_hi = Line(gpt(EPS) + LEFT * 0.25, gpt(EPS) + RIGHT * 0.25, color=EPS_COLOR, stroke_width=4)
        e_lo = Line(gpt(-EPS) + LEFT * 0.25, gpt(-EPS) + RIGHT * 0.25, color=EPS_COLOR, stroke_width=4)
        e_hi_lab = S.math(r"e^{\varepsilon}", size=36, color=EPS_COLOR).next_to(e_hi, LEFT, buff=0.15)
        e_lo_lab = S.math(r"e^{-\varepsilon}", size=36, color=EPS_COLOR).next_to(e_lo, LEFT, buff=0.15)
        g_tri = Triangle(color=S.WHITE, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI / 2)
        g_tri.add_updater(lambda m: m.move_to(gpt(np.log(ratio(tv.get_value()))) + RIGHT * 0.36))

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(db_x, db_xp, lab_x, lab_xp, arr_dx, arr_dxp, m_x, m_xp, foot, dots,
                                     ticks1)), run_time=0.6)
            self.play(ReplacementTransform(ax1, ax2), ReplacementTransform(c1x, c2x),
                      ReplacementTransform(c1xp, c2xp), ReplacementTransform(a1x, a2x),
                      ReplacementTransform(a1xp, a2xp), FadeOut(out_lab1), run_time=1.1)
            self.play(FadeIn(marker, shift=UP * 0.2), GrowFromEdge(stick_x, DOWN), GrowFromEdge(stick_xp, DOWN),
                      run_time=0.7)
            vo.wait_until("compare the heights")
            self.play(TransformFromCopy(stick_x, bar_x), TransformFromCopy(stick_xp, bar_xp), run_time=1.1)
            self.add(bar_x, bar_xp)
            self.play(FadeIn(div), FadeIn(eq), FadeIn(num), run_time=0.5)
            vo.wait_until("Slide t along")
            self.play(Create(g_line), FadeIn(g_one), FadeIn(g_one_lab), FadeIn(g_title), FadeIn(g_tri),
                      run_time=0.6)
            self.play(tv.animate.set_value(50.0), run_time=vo.until("A private mechanism", 1.2))
            self.play(FadeIn(band), Indicate(g_one_lab, color=S.WHITE), tv.animate.set_value(41.5),
                      run_time=1.4)
            self.play(tv.animate.set_value(32.0), run_time=vo.until("never above", 0.8))
            self.play(Create(e_hi), Write(e_hi_lab), tv.animate.set_value(21.0), run_time=1.6)
            vo.wait_until("never below")
            self.play(Create(e_lo), Write(e_lo_lab), tv.animate.set_value(62.0), run_time=vo.remaining(1.8))

        # ============================================================ 3. Definition 1, as a caption
        for m in (stick_x, stick_xp, bar_x, bar_xp, num, marker, g_tri):
            m.clear_updaters()
        defn = S.math(r"\left|\,", r"\ln", r"\!\left(", r"{\Pr[M(x)=t]", r"\over", r"\Pr[M(x')=t]}",
                      r"\right)", r"\,\right|", r"\le", r"\varepsilon", size=58)
        defn[3].set_color(X_COLOR)
        defn[5].set_color(XP_COLOR)
        defn[9].set_color(EPS_COLOR)
        defn.move_to([-1.55, 0.95, 0])
        header = S.tex(r"\textbf{Definition 1}\quad ", r"$\varepsilon$", r"-indistinguishability", size=40)
        header[1].set_color(EPS_COLOR)
        header.move_to([-1.55, 2.85, 0])
        loss_brace = Brace(VGroup(*defn[1:7]), direction=DOWN, color=EPS_COLOR, buff=0.12)
        loss_lab = VGroup(S.text("privacy loss at", 26, EPS_COLOR), S.math("t", size=36, color=EPS_COLOR))
        loss_lab.arrange(RIGHT, buff=0.12, aligned_edge=DOWN).next_to(loss_brace, DOWN, buff=0.1)
        cap = S.tex(r"for all neighbors ", r"$x$", r", ", r"$x'$", r",\quad ", r"all analysts,\quad ",
                    r"all outputs $t$", size=36)
        cap[1].set_color(X_COLOR)
        cap[3].set_color(XP_COLOR)
        cap.move_to([-1.55, -1.25, 0])
        cap_a, cap_b, cap_c = VGroup(*cap[:5]), cap[5], cap[6]
        sym = S.math(r"\left|\ln 2\right| \;=\; \left|\ln \tfrac{1}{2}\right| \;\approx\; 0.69", size=40)
        sym.move_to([-1.55, -2.55, 0])
        small = S.math(r"\text{small } \varepsilon\!:\quad", r"e^{\varepsilon}", r"\approx", r"1+\varepsilon",
                       size=40)
        small[0][5].set_color(EPS_COLOR)
        small[1].set_color(EPS_COLOR)
        small[3][-1].set_color(EPS_COLOR)
        small.move_to(sym)
        zero_lab = S.math("0", size=32).move_to(g_one_lab)
        hi2 = S.math(r"+\varepsilon", size=36, color=EPS_COLOR).next_to(e_hi, LEFT, buff=0.15)
        lo2 = S.math(r"-\varepsilon", size=36, color=EPS_COLOR).next_to(e_lo, LEFT, buff=0.15)
        g_title2 = S.math(r"\ln(\text{ratio})", size=30, color=S.GREY).next_to(g_line, UP, buff=0.15)

        with self.voiceover(SAY[3]) as vo:
            plot = VGroup(ax2, c2x, c2xp, a2x, a2xp, stick_x, stick_xp, marker)
            self.play(FadeOut(plot), FadeOut(VGroup(div, eq, num)),
                      ReplacementTransform(bar_x, defn[3]), ReplacementTransform(bar_xp, defn[5]),
                      FadeIn(defn[4]), run_time=1.5)
            vo.wait_until("which it calls")
            self.play(Write(header), run_time=1.2)
            vo.wait_until("The log of the ratio")
            self.play(Write(defn[1]), Write(defn[2]), Write(defn[6]), run_time=0.9)
            self.play(GrowFromCenter(loss_brace), FadeIn(loss_lab, shift=UP * 0.1),
                      ReplacementTransform(g_one_lab, zero_lab), ReplacementTransform(e_hi_lab, hi2),
                      ReplacementTransform(e_lo_lab, lo2), ReplacementTransform(g_title, g_title2), run_time=1.0)
            vo.wait_until("For every pair")
            self.play(FadeIn(cap_a, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("every analyst")
            self.play(FadeIn(cap_b, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("every output")
            self.play(FadeIn(cap_c, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("it must be at most")
            self.play(Write(defn[0]), Write(defn[7]), Write(defn[8]), Write(defn[9]), run_time=1.0)
            self.play(Indicate(defn[9], color=EPS_COLOR, scale_factor=1.5), Indicate(band, color=EPS_COLOR),
                      run_time=0.8)
            vo.wait_until("in absolute value")
            self.play(Indicate(VGroup(*defn[0:8]), color=S.WHITE, scale_factor=1.06), run_time=1.0)
            vo.wait_until("a ratio of two")
            self.play(Write(sym), run_time=1.2)
            vo.wait_until("For small epsilon")
            self.play(ReplacementTransform(sym, small), run_time=1.0)
            self.play(Indicate(small[1:], color=EPS_COLOR), run_time=vo.remaining(0.6))

        # ============================================================ 4. Warner's coin: ponder
        gauge = VGroup(g_line, g_one, zero_lab, g_title2, band, e_hi, e_lo, hi2, lo2, g_tri)
        alice = person_icon(ALICE, 0.72).move_to([-5.95, -0.55, 0])
        alice_lab = S.text("Alice", 22, ALICE).next_to(alice, DOWN, buff=0.1)
        coin1 = coin_glyph().move_to([-4.75, -0.55, 0])
        leaf_truth = S.text("tell the truth", 30, S.WHITE).move_to([-2.35, 0.8, 0])
        coin2 = coin_glyph().move_to([-3.0, -1.75, 0])
        leaf_yes = S.text("yes", 32, S.WHITE).move_to([-1.3, -1.05, 0])
        leaf_no = S.text("no", 32, S.WHITE).move_to([-1.3, -2.5, 0])

        def edge(a, b, label, up=True):
            ln = Line(a.get_right() + RIGHT * 0.06, b.get_left() + LEFT * 0.1, color=S.GREY, stroke_width=3)
            lab = S.math(label, size=34, color=S.GREY)
            lab.next_to(ln.get_center(), UL if up else DL, buff=0.06)
            return ln, lab

        e_h1, l_h1 = edge(coin1, leaf_truth, r"\text{heads }\tfrac12", up=True)
        e_t1, l_t1 = edge(coin1, coin2, r"\text{tails }\tfrac12", up=False)
        e_h2, l_h2 = edge(coin2, leaf_yes, r"\text{heads }\tfrac12", up=True)
        e_t2, l_t2 = edge(coin2, leaf_no, r"\text{tails }\tfrac12", up=False)
        a_line = Line(alice.get_right() + RIGHT * 0.06, coin1.get_left() + LEFT * 0.06, color=S.GREY,
                      stroke_width=3)
        tree = VGroup(alice, alice_lab, a_line, coin1, e_h1, l_h1, leaf_truth, e_t1, l_t1, coin2, e_h2, l_h2,
                      leaf_yes, e_t2, l_t2, leaf_no)
        tree_title = S.text("Warner's coin (1965)", 30, S.GREY).move_to([-3.7, 1.8, 0])

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(gauge, header, loss_brace, loss_lab, cap, small)),
                      defn.animate.scale(0.62).move_to([0, 2.95, 0]), run_time=1.0)
            self.play(FadeIn(tree_title), FadeIn(alice), FadeIn(alice_lab), Create(a_line), FadeIn(coin1),
                      run_time=0.7)
            self.play(LaggedStart(AnimationGroup(Create(e_h1), FadeIn(l_h1), FadeIn(leaf_truth)),
                                  AnimationGroup(Create(e_t1), FadeIn(l_t1), FadeIn(coin2)),
                                  AnimationGroup(Create(e_h2), FadeIn(l_h2), FadeIn(leaf_yes)),
                                  AnimationGroup(Create(e_t2), FadeIn(l_t2), FadeIn(leaf_no)),
                                  lag_ratio=0.45), run_time=1.6)
            vo.wait_until("Pause and ponder")
            self.play(flip(coin1), run_time=0.8)
            vo.wait_until("how likely is she")
            self.play(Indicate(leaf_yes, color=S.WHITE, scale_factor=1.3), run_time=0.8)
            vo.wait_until("And if it is no")
            self.play(flip(coin2), run_time=vo.remaining(0.6))
        card = ponder_at(self, "Warner's coin: what is its ε?", 12, pos=[3.4, -0.6, 0], width=5.9)

        # ============================================================ 5. the coin's epsilon
        r1 = S.math(r"\text{truth yes}", r"\;\Rightarrow\;", r"\Pr[\text{says yes}]", "=", r"\frac12", "+",
                    r"\frac14", "=", r"\frac34", size=34)
        r1[0].set_color(XP_COLOR)
        r1[8].set_color(XP_COLOR)
        r2 = S.math(r"\text{truth no}", r"\;\Rightarrow\;", r"\Pr[\text{says yes}]", "=", r"\frac14", size=34)
        r2[0].set_color(X_COLOR)
        r2[4].set_color(X_COLOR)
        r3 = S.math(r"\frac34", r"\div", r"\frac14", "=", "3", size=44)
        r3[0].set_color(XP_COLOR)
        r3[2].set_color(X_COLOR)
        r4 = S.math(r"\varepsilon = \ln 3 \approx 1.1", size=50, color=EPS_COLOR)
        table = VGroup(r1, r2, r3, r4).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.2, -0.5, 0])
        r3.set_x(table.get_x())
        r4.set_x(table.get_x())
        r2.align_to(r1, LEFT)
        r2.shift(RIGHT * (r1[3].get_x() - r2[3].get_x()))
        r4_box = SurroundingRectangle(r4, color=EPS_COLOR, buff=0.18, corner_radius=0.1)

        def glow(ln, col):
            return ln.copy().set_stroke(col, 7)

        p_half = S.math(r"\tfrac12", size=40, color=XP_COLOR).next_to(leaf_truth, RIGHT, buff=0.15)
        say_yes = S.text("→ yes", 28, XP_COLOR).next_to(leaf_truth, DOWN, buff=0.1)
        say_no = S.text("→ no", 28, X_COLOR).move_to(say_yes)
        p_q1 = S.math(r"\tfrac14", size=40, color=XP_COLOR).next_to(leaf_yes, RIGHT, buff=0.15)
        p_q2 = S.math(r"\tfrac14", size=40, color=X_COLOR).move_to(p_q1)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(card), run_time=0.5)
            g1, g2, g3 = glow(e_h1, XP_COLOR), glow(e_t1, XP_COLOR), glow(e_h2, XP_COLOR)
            self.play(Create(g1), FadeIn(say_yes), run_time=0.7)
            self.play(FadeIn(p_half, scale=1.3), run_time=0.4)
            vo.wait_until("or tails then heads")
            self.play(Create(g2), run_time=0.4)
            self.play(Create(g3), FadeIn(p_q1, scale=1.3), run_time=0.5)
            self.play(Write(r1), run_time=1.1)
            vo.wait_until("If it is no")
            b2, b3 = glow(e_t1, X_COLOR), glow(e_h2, X_COLOR)
            self.play(FadeOut(VGroup(g1, g2, g3, p_half)), ReplacementTransform(say_yes, say_no),
                      ReplacementTransform(p_q1, p_q2), run_time=0.6)
            self.play(Create(b2), run_time=0.35)
            self.play(Create(b3), run_time=0.35)
            self.play(Write(r2), run_time=0.9)
            vo.wait_until("The worst ratio")
            self.play(TransformFromCopy(r1[8], r3[0]), TransformFromCopy(r2[4], r3[2]), FadeIn(r3[1]),
                      run_time=1.0)
            self.play(Write(r3[3:]), run_time=0.5)
            vo.wait_until("with epsilon equal")
            self.play(Write(r4), run_time=0.9)
            self.play(Create(r4_box), Indicate(defn[9], color=EPS_COLOR, scale_factor=1.4), run_time=0.8)

        # ============================================================ 6. the attacker's view: Bayes
        attacker = person_icon(ANALYST, 0.95).move_to([-5.7, 1.0, 0])
        att_lab = S.text("attacker", 24, ANALYST).next_to(attacker, DOWN, buff=0.12)
        screen = RoundedRectangle(width=1.5, height=0.7, corner_radius=0.1, stroke_color=S.GREY,
                                  stroke_width=2).set_fill(S.GREY_DARKER, 1)
        screen_t = VGroup(S.text("output", 20, S.GREY), S.math("t", size=34)).arrange(RIGHT, buff=0.1)
        scr = VGroup(screen, screen_t.move_to(screen)).next_to(attacker, UP, buff=0.35)
        wonder = S.math("x", r"\text{ or }", "x'", "?", size=34)
        wonder[0].set_color(X_COLOR)
        wonder[2].set_color(XP_COLOR)
        wonder.next_to(att_lab, DOWN, buff=0.15)

        bayes = S.math(r"{\Pr[x \mid t]", r"\over", r"\Pr[x' \mid t]}", "=", r"{\Pr[x]", r"\over", r"\Pr[x']}",
                       r"\times", r"{\Pr[M(x)=t]", r"\over", r"\Pr[M(x')=t]}", size=40)
        for i in (0, 4, 8):
            bayes[i].set_color(X_COLOR)
        for i in (2, 6, 10):
            bayes[i].set_color(XP_COLOR)
        bayes.move_to([0.95, 1.25, 0])
        new_b = Brace(VGroup(*bayes[0:3]), DOWN, buff=0.1, color=S.GREY)
        old_b = Brace(VGroup(*bayes[4:7]), DOWN, buff=0.1, color=S.GREY)
        rat_b = Brace(VGroup(*bayes[8:11]), DOWN, buff=0.1, color=EPS_COLOR)
        new_l = S.text("new odds", 24, S.WHITE).next_to(new_b, DOWN, buff=0.08)
        old_l = S.text("old odds", 24, S.WHITE).next_to(old_b, DOWN, buff=0.08)
        rat_l = S.math(r"\in\, [\,e^{-\varepsilon},\ e^{\varepsilon}\,]", size=34, color=EPS_COLOR)
        rat_l.next_to(rat_b, DOWN, buff=0.08)
        bayes_lab = S.text("Bayes' rule", 24, S.GREY).next_to(bayes, UP, buff=0.3).align_to(bayes, LEFT)

        head = VGroup(S.text("start at 50/50", 26, S.WHITE), S.math(r"\to", size=34),
                      S.text("at most", 26, S.WHITE)).arrange(RIGHT, buff=0.18)
        rows_spec = [("", "= 0.1", 0.1, "52.5%"), ("", "= 0.5", 0.5, "62%"), ("", "= 1", 1.0, "73%"),
                     (r"\text{coin: }", r"= \ln 3", np.log(3), "75%")]
        TRACK = 2.6
        brows = VGroup()
        fills = []
        for pre, post, e, pct in rows_spec:
            lab = S.math(*([pre] if pre else []), r"\varepsilon", post, size=32)
            lab[-2].set_color(EPS_COLOR)
            track = Rectangle(width=TRACK, height=0.24, stroke_color=S.GREY_DARK, stroke_width=1.5)
            track.set_fill(S.GREY_DARKER, 1)
            mid = DashedLine(track.get_top() + UP * 0.06, track.get_bottom() + DOWN * 0.06, color=S.GREY,
                             stroke_width=2, dash_length=0.05)
            p = np.exp(e) / (1 + np.exp(e))
            fill = Rectangle(width=TRACK * p, height=0.24, stroke_width=0).set_fill(ANALYST, 0.9)
            txt = S.text(pct, 26, S.WHITE)
            row = VGroup(lab, VGroup(track, fill, mid), txt)
            brows.add(row)
            fills.append((fill, p))
        for row in brows:
            row[0].move_to(ORIGIN, aligned_edge=RIGHT)
            row[1].next_to(row[0], RIGHT, buff=0.3)
            row[2].next_to(row[1], RIGHT, buff=0.25)
        brows.arrange(DOWN, buff=0.22)
        for row in brows:  # align the bars in a column
            row[1].align_to(brows[0][1], LEFT)
            row[0].next_to(row[1], LEFT, buff=0.3)
            row[2].next_to(row[1], RIGHT, buff=0.25)
            row[1][1].align_to(row[1][0], LEFT)
            row[1][2].move_to(row[1][0])
        bayes_table = VGroup(head, brows).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-2.2, -2.15, 0])
        policy = VGroup(S.tex(r"$\varepsilon$", r" is set by policy", size=36),
                        S.text("the paper calls it the leakage", 24, S.GREY)).arrange(DOWN, buff=0.15)
        policy[0][0].set_color(EPS_COLOR)
        policy.move_to([4.15, -2.15, 0])
        policy_box = SurroundingRectangle(policy, color=EPS_COLOR, buff=0.22, corner_radius=0.12)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(tree, tree_title, b2, b3, say_no, p_q2, table, r4_box, defn)), run_time=0.7)
            self.play(FadeIn(attacker, shift=RIGHT * 0.3), FadeIn(att_lab), run_time=0.6)
            self.play(FadeIn(scr, shift=DOWN * 0.15), Write(wonder), run_time=0.8)
            vo.wait_until("By Bayes")
            self.play(FadeIn(bayes_lab), Write(bayes), run_time=1.6)
            vo.wait_until("your new odds")
            self.play(GrowFromCenter(new_b), FadeIn(new_l), run_time=0.6)
            vo.wait_until("your old odds")
            self.play(GrowFromCenter(old_b), FadeIn(old_l), run_time=0.6)
            vo.wait_until("exactly this ratio")
            self.play(Indicate(VGroup(*bayes[8:11]), color=S.WHITE, scale_factor=1.08), run_time=0.8)
            vo.wait_until("so they move")
            self.play(GrowFromCenter(rat_b), FadeIn(rat_l, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("whatever you knew")
            self.play(Indicate(VGroup(*bayes[4:7]), color=S.WHITE), Indicate(old_l, color=S.WHITE), run_time=0.9)
            vo.wait_until("Starting from")
            self.play(FadeIn(head, shift=UP * 0.15), run_time=0.6)
            for fill, p in fills:  # every bar starts at the 50/50 mark
                fill.stretch_to_fit_width(TRACK * 0.5, about_edge=LEFT)
            for k, phrase in ((0, "epsilon one tenth"), (1, None), (2, "epsilon one,"), (3, None)):
                if phrase:
                    vo.wait_until(phrase)
                row = brows[k]
                self.play(FadeIn(row[0]), FadeIn(row[1]), run_time=0.4)
                fill, p = fills[k]
                self.play(fill.animate.stretch_to_fit_width(TRACK * p, about_edge=LEFT), FadeIn(row[2]),
                          run_time=0.7)
            vo.wait_until("Epsilon is set")
            self.play(FadeIn(policy, shift=UP * 0.15), Create(policy_box), run_time=0.9)

        # ============================================================ 7. what it does not promise
        title7 = S.text("What it does not promise", 34, S.GREY).to_edge(UP, buff=0.45)
        db7 = db_stack(S.GREY, values=False, width=2.6, row_h=0.46, size=22).move_to([-4.6, -0.35, 0])
        row_alice7 = VGroup(db7[1][ALICE_ROW], db7[2])
        headline_txt = VGroup(S.text("Study finds:", 22, S.GREY),
                              S.text("smokers get more heart disease", 30, S.WHITE)).arrange(DOWN, buff=0.1)
        headline_box = RoundedRectangle(width=headline_txt.width + 0.7, height=headline_txt.height + 0.5,
                                        corner_radius=0.15, stroke_color=S.WHITE,
                                        stroke_width=2).set_fill(S.GREY_DARKER, 1)
        headline = VGroup(headline_box, headline_txt.move_to(headline_box)).move_to([2.2, 1.45, 0])
        study = Arrow(db7.get_right() + UP * 0.6, headline.get_left() + DOWN * 0.15, buff=0.15, color=S.GREY,
                      stroke_width=3, tip_length=0.18)
        study_lab = S.text("study", 22, S.GREY).next_to(study.get_center(), UP, buff=0.15)
        alice7 = person_icon(ALICE, 0.95).move_to([0.6, -1.25, 0])
        alice7_lab = S.text("Alice", 24, ALICE).next_to(alice7, DOWN, buff=0.1)
        cig = cigarette().next_to(alice7, RIGHT, buff=0.04).shift(DOWN * 0.18)
        insurer = person_icon(S.GREY, 0.85).move_to([4.6, -1.25, 0])
        worry = S.text("Her insurer now worries", 24, S.WHITE).next_to(insurer, DOWN, buff=0.12)
        bang = S.text("!", 36, S.WHITE).next_to(insurer, UR, buff=0.0)
        look = Arrow(insurer.get_left(), cig.get_right() + RIGHT * 0.12, buff=0.15, color=S.GREY,
                     stroke_width=2, tip_length=0.14)
        stranger = database_rows(["stranger"], None, color=S.GREY, width=db7[1][ALICE_ROW][0].width,
                                 row_height=db7[1][ALICE_ROW][0].height, size=22)[0]
        stranger.move_to(row_alice7)
        verdict1 = S.text("would happen even with Alice's row replaced", 28, S.WHITE)
        verdict2 = VGroup(S.text("✓", 30, CHECK), S.text("not a privacy breach", 30, CHECK)).arrange(RIGHT, buff=0.15)
        verdict = VGroup(verdict1, verdict2).arrange(DOWN, buff=0.15).move_to([0.6, -3.05, 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
            self.play(FadeIn(title7, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("If a study")
            self.play(FadeIn(db7), run_time=0.7)
            self.play(GrowArrow(study), FadeIn(study_lab), run_time=0.6)
            self.play(FadeIn(headline, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("and Alice smokes")
            self.play(FadeIn(alice7, shift=UP * 0.2), FadeIn(alice7_lab), FadeIn(cig), run_time=0.7)
            vo.wait_until("people may now")
            self.play(FadeIn(insurer), FadeIn(worry), GrowArrow(look), run_time=0.8)
            self.play(FadeIn(bang, scale=1.6), Wiggle(insurer), run_time=0.8)
            vo.wait_until("the same lesson")
            self.play(FadeOut(row_alice7, shift=LEFT * 1.6), run_time=0.8)
            self.play(FadeIn(stranger, shift=RIGHT * 1.6), run_time=0.8)
            self.play(ShowPassingFlash(study.copy().set_stroke(S.WHITE, 6), time_width=0.6), run_time=0.8)
            self.play(Circumscribe(headline_box, color=S.WHITE, time_width=0.7),
                      Indicate(headline_txt[1], color=S.WHITE, scale_factor=1.05), run_time=1.0)
            vo.wait_until("so it would happen")
            self.play(FadeIn(verdict1, shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(verdict2, shift=UP * 0.15), run_time=vo.remaining(0.6))
        self.wait(0.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
