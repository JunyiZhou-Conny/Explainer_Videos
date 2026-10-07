"""S09 · Many questions: the privacy budget (Theorem 1, p. 273; histograms, §3.2)."""

import numpy as np
from manim import *

from explainer import i18n
from explainer import style as S
from explainer.components import person_icon, ponder_card
from explainer.scene import VoiceScene

from common import (ALICE, ANALYST_COLOR, EPS_COLOR, NARRATION, NOISE_COLOR, SENS_COLOR, X_COLOR,
                    XP_COLOR, budget_bar)
from s02_map import map_chip

SAY = NARRATION["S09"]
ANALYST = S.GREY          # the analyst's factors in the transcript formula: identical in both worlds


# ---------------------------------------------------------------- helpers

def ponder_at(scene, question: str, seconds: float, pos=ORIGIN, **kw) -> VGroup:
    """pause_and_ponder, but placed at `pos` so a supporting picture can stay visible."""
    card = ponder_card(question, **kw).move_to(pos)
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return card


def build_tex(spec, size=34):
    """spec = [(name, [(tex, color|None), ...]), ...] -> (MathTex, {name: VGroup of its parts})."""
    parts, owners, cols = [], [], []
    for name, segs in spec:
        for tex, col in segs:
            parts.append(tex)
            owners.append(name)
            cols.append(col)
    m = S.math(*parts, size=size)
    groups = {}
    for i, (name, col) in enumerate(zip(owners, cols)):
        if col:
            m[i].set_color(col)
        groups.setdefault(name, VGroup()).add(m[i])
    return m, groups


def mini_hist(heights, color=X_COLOR, bar_w=0.17, gap=0.05):
    bars = VGroup(*[Rectangle(width=bar_w, height=h, stroke_width=0).set_fill(color, 0.85) for h in heights])
    bars.arrange(RIGHT, buff=gap, aligned_edge=DOWN)
    base = Line(bars.get_corner(DL) + LEFT * 0.05, bars.get_corner(DR) + RIGHT * 0.05, color=S.GREY,
                stroke_width=1.5)
    return VGroup(bars, base)


def card_frame(w, h):
    return RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=S.GREY,
                            stroke_width=2).set_fill(S.GREY_DARKER, 1)


def q_card(i: int, sub: str, w: float = 2.2) -> VGroup:
    head = S.math(f"f_{i}", size=36)
    s = S.text(sub, 20, S.GREY)
    body = VGroup(head, s).arrange(DOWN, buff=0.08)
    frame = card_frame(w, 1.0)
    body.move_to(frame)
    return VGroup(frame, head, s)


def a_card(i: int, heights, w: float = 2.2) -> VGroup:
    hist = mini_hist(heights)
    lab = S.math(f"a_{i}", size=34)
    body = VGroup(hist, lab).arrange(RIGHT, buff=0.3)
    frame = card_frame(w, 1.05)
    body.move_to(frame)
    return VGroup(frame, hist, lab)


def strike_line(m, color=S.WHITE, width=3.5, pad=0.08):
    return Line(m.get_corner(DL) + np.array([-pad, -pad, 0]), m.get_corner(UR) + np.array([pad, pad, 0]),
                color=color, stroke_width=width)


def x_mark(m, color=NOISE_COLOR, width=6, pad=0.1):
    c = m.get_center()
    w, h = m.width / 2 + pad, m.height / 2 + pad
    return VGroup(Line(c + np.array([-w, -h, 0]), c + np.array([w, h, 0]), color=color, stroke_width=width),
                  Line(c + np.array([-w, h, 0]), c + np.array([w, -h, 0]), color=color, stroke_width=width))


# true histogram for the d = 100 comparison (smooth two-bump shape) and seeded noise, eps = 1
D_BINS = 100
EPS_DEMO = 1.0
_j = np.arange(D_BINS)
TRUE_COUNTS = np.round(40 + 420 * np.exp(-((_j - 32) / 11.0) ** 2) + 260 * np.exp(-((_j - 70) / 8.0) ** 2))
_rng = np.random.default_rng(2006)
NOISY_SEPARATE = TRUE_COUNTS + _rng.laplace(0, D_BINS / EPS_DEMO, D_BINS)   # Lap(d / eps) per bin
NOISY_JOINT = TRUE_COUNTS + _rng.laplace(0, 2 / EPS_DEMO, D_BINS)           # Lap(2 / eps) per bin
Y_MIN, Y_MAX = -300, 800


def hist_panel(counts, noisy, width=5.6, height=3.3):
    """Axes + released bars (BLUE) + true histogram outline (WHITE). Returns (axes, bars, truth)."""
    ax = Axes(x_range=[0, D_BINS, 10], y_range=[Y_MIN, Y_MAX, 100], x_length=width, y_length=height,
              tips=False, axis_config={"color": S.GREY, "stroke_width": 2, "include_ticks": False})
    bars = VGroup()
    for j, v in enumerate(noisy):
        v = float(np.clip(v, Y_MIN, Y_MAX))
        p0, p1 = ax.c2p(j + 0.1, 0), ax.c2p(j + 0.9, v)
        r = Rectangle(width=abs(p1[0] - p0[0]), height=max(abs(p1[1] - p0[1]), 0.004), stroke_width=0)
        r.set_fill(X_COLOR, 0.75).move_to((p0 + p1) / 2)
        r.grow_dir = DOWN if v >= 0 else UP
        bars.add(r)
    pts = []
    for j, c in enumerate(counts):
        pts += [ax.c2p(j, c), ax.c2p(j + 1, c)]
    truth = VMobject().set_points_as_corners(pts).set_stroke(S.WHITE, 2.5)
    return ax, bars, truth


# ---------------------------------------------------------------- the scene

class Budget(VoiceScene):
    def construct(self):
        self.adaptive_beat()
        self.theorem_beat()
        self.budget_beat()
        self.histogram_beats()

    # ============================================================ 0. adaptive questions
    def adaptive_beat(self):
        top_y, bot_y = 1.55, -0.65
        xs = [-2.6, 0.5, 3.6]
        analyst = VGroup(person_icon(ANALYST_COLOR, 0.75), S.text("analyst", 22, ANALYST_COLOR))
        analyst.arrange(DOWN, buff=0.12)
        analyst.move_to([-5.6, top_y, 0])
        db = VGroup(*[Rectangle(width=0.55, height=0.13, stroke_color=X_COLOR, stroke_width=1.5)
                      .set_fill(S.GREY_DARKER, 1) for _ in range(4)]).arrange(DOWN, buff=0)
        cur_icon = VGroup(person_icon(S.WHITE, 0.75), db).arrange(RIGHT, buff=0.15)
        curator = VGroup(cur_icon, S.text("curator", 22, S.GREY)).arrange(DOWN, buff=0.12)
        curator.move_to([-5.6, bot_y, 0])

        subs = ["histogram", "zoom into bin 3", "zoom further"]
        hists = [[0.18, 0.3, 0.72, 0.26, 0.16], [0.28, 0.5, 0.64, 0.4, 0.22], [0.4, 0.55, 0.3, 0.46, 0.25]]
        qs = [q_card(i + 1, subs[i]).move_to([xs[i], top_y, 0]) for i in range(3)]
        ans = [a_card(i + 1, hists[i]).move_to([xs[i], bot_y, 0]) for i in range(3)]
        down = [Arrow(q.get_bottom(), a.get_top(), buff=0.08, color=X_COLOR, stroke_width=3, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.25) for q, a in zip(qs, ans)]
        d_lab = S.math(r"f_1(", "x", r") + ", "Y_1", size=28)
        d_lab[1].set_color(X_COLOR)
        d_lab[3].set_color(NOISE_COLOR)
        d_lab.next_to(down[0], LEFT, buff=0.15)
        q_dots = S.math(r"\cdots", size=44, color=S.GREY).move_to([5.75, top_y, 0])
        a_dots = S.math(r"\cdots", size=44, color=S.GREY).move_to([5.75, bot_y, 0])
        diag = []
        for i in range(3):
            start = ans[i].get_corner(UR) + np.array([-0.15, 0.02, 0])
            end = (qs[i + 1].get_corner(DL) + np.array([0.15, -0.02, 0])) if i < 2 else q_dots.get_bottom() + DOWN * 0.1
            diag.append(Arrow(start, end, buff=0.05, color=ANALYST, stroke_width=3, tip_length=0.16,
                              max_tip_length_to_length_ratio=0.2))
        strip = SurroundingRectangle(VGroup(*ans, a_dots), buff=0.15, color=S.GREY, stroke_width=1.5,
                                     corner_radius=0.12)
        t_lab = S.math(r"\text{transcript}\quad t = [\,a_1,\ a_2,\ a_3,\ \dots\,]", size=32)
        t_lab.next_to(strip, DOWN, buff=0.25)
        spike = ans[0][1][0][2]

        enter = (FadeIn(analyst, shift=RIGHT * 0.2), FadeIn(curator, shift=RIGHT * 0.2))
        if i18n.active():
            # part 2 opens on this scene: a silent lead-in, so the voice does not start on the first frame
            self.play(*enter, run_time=0.6)
            self.wait(0.3)
        with self.voiceover(SAY[0]) as vo:
            if not i18n.active():
                self.play(*enter, run_time=0.6)
            self.play(FadeIn(qs[0], shift=RIGHT * 0.3), run_time=0.5)
            self.play(GrowArrow(down[0]), FadeIn(d_lab), run_time=0.5)
            self.play(FadeIn(ans[0], shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("Real analysts")
            for i in (1, 2):
                self.play(GrowArrow(diag[i - 1]), run_time=0.45)
                self.play(FadeIn(qs[i], shift=RIGHT * 0.2), run_time=0.35)
                self.play(GrowArrow(down[i]), run_time=0.3)
                self.play(FadeIn(ans[i], shift=DOWN * 0.2), run_time=0.35)
            self.play(GrowArrow(diag[2]), FadeIn(q_dots), FadeIn(a_dots), run_time=0.5)
            self.play(Create(strip), Write(t_lab), run_time=1.0)
            vo.wait_until("Maybe you spot")
            box = SurroundingRectangle(spike, buff=0.05, color=S.WHITE, stroke_width=2.5)
            self.play(Create(box), Indicate(spike, color=S.WHITE, scale_factor=1.3), run_time=0.8)
            self.play(ShowPassingFlash(diag[0].copy().set_stroke(S.WHITE, 6), time_width=0.6),
                      Indicate(qs[1][2], color=S.WHITE), run_time=1.0)
            self.play(Indicate(ans[1][1], color=S.WHITE), run_time=vo.remaining(0.5))
        self.ledger = VGroup(analyst, curator, *qs, *ans, *down, *diag, d_lab, q_dots, a_dots, strip, t_lab, box)
        self.parts = dict(qs=qs, ans=ans, down=down, diag=diag, q_dots=q_dots, analyst=analyst, curator=curator)

    # ============================================================ 1. Theorem 1: the ratio telescopes
    def theorem_beat(self):
        P = self.parts
        title = S.text("Theorem 1", 32, EPS_COLOR, weight="BOLD").to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.6)
        size = 36

        def pr(head: str, world: str | None = None):
            """Pr[...] factor; world in {None, 'x', "x'"} adds '; x' style conditioning coloured by world."""
            if world is None:
                return S.math(head, size=size, color=ANALYST)
            m = S.math(head, world, "]", size=size)
            m[1].set_color(X_COLOR if world == "x" else XP_COLOR)
            return m

        def row(world):
            return [pr(r"\Pr[f_1]"), pr(r"\Pr[a_1 \mid ", world), pr(r"\Pr[f_2 \mid a_1]"),
                    pr(r"\Pr[a_2 \mid a_1;\, ", world), S.math(r"\cdots", size=size)]

        names = ["F1", "C1", "F2", "C2", "dots"]
        top, bot = row("x"), row("x'")
        lhs_top, lhs_bot = pr(r"\Pr[t \mid ", "x"), pr(r"\Pr[t \mid ", "x'")

        # step 1: the product along the transcript (world x)
        eq = S.math("=", size=size)
        line1 = VGroup(lhs_top, eq, *top).arrange(RIGHT, buff=0.24).move_to([0, -1.0, 0])
        legend = VGroup(
            VGroup(Square(0.22, stroke_width=0).set_fill(ANALYST, 1),
                   S.text("analyst picks the next question", 24, ANALYST)).arrange(RIGHT, buff=0.2),
            VGroup(Square(0.22, stroke_width=0).set_fill(S.WHITE, 1),
                   S.text("curator answers with Laplace noise", 24, S.WHITE)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(line1, DOWN, buff=0.55)

        # step 2: ratio of the two worlds' products, stacked column by column
        y_top, y_bar, y_bot = 2.45, 2.02, 1.6
        gap = 0.38
        widths = [max(lhs_top.width, lhs_bot.width), eq.width] + \
                 [max(a.width, b.width) for a, b in zip(top, bot)]
        total = sum(widths) + gap * (len(widths) - 1)
        xs, x = [], -total / 2
        for w in widths:
            xs.append(x + w / 2)
            x += w + gap
        targets_top = [lhs_top.copy().move_to([xs[0], y_top, 0]), eq.copy().move_to([xs[1], y_bar, 0])] + \
                      [m.copy().move_to([cx, y_top if n != "dots" else y_bar, 0]) for m, cx, n in zip(top, xs[2:], names)]
        for m, cx, n in zip(bot, xs[2:], names):
            m.move_to([cx, y_bot, 0])
        lhs_bot.move_to([xs[0], y_bot, 0])
        bar_l = Line([xs[0] - widths[0] / 2, y_bar, 0], [xs[0] + widths[0] / 2, y_bar, 0], stroke_width=2.5,
                     color=S.WHITE)
        bar_r = Line([xs[2] - widths[2] / 2, y_bar, 0], [xs[5] + widths[5] / 2, y_bar, 0], stroke_width=2.5,
                     color=S.WHITE)
        col = {n: (top[i], bot[i]) for i, n in enumerate(names)}

        def cancel_line(n):
            a, b = col[n]
            g = VGroup(a, b)
            return Line(g.get_corner(DL) + np.array([-0.08, -0.06, 0]), g.get_corner(UR) + np.array([0.08, 0.06, 0]),
                        color=S.WHITE, stroke_width=3)

        cancel = S.text("same in both worlds: cancels", 24, ANALYST)
        cancel.move_to([(xs[2] + xs[4]) / 2, y_bot - 0.62, 0])

        # the two people leave the ledger with it but stay on, labelled, until the analyst's factors have
        # cancelled: the analyst (PURPLE) heads the "cancels" caption, the curator sits under its Laplace factor
        an, cu = P["analyst"], P["curator"]
        an.generate_target()
        an.target[0].scale_to_fit_height(0.6)
        an.target[1].next_to(an.target[0], DOWN, buff=0.1)
        an.target.next_to(cancel, LEFT, buff=0.35)
        an.target.shift(UP * (cancel.get_y() - 0.08 - an.target[0].get_y()))
        cu.generate_target()
        cu.target[0].scale_to_fit_height(0.6)
        cu.target[1].next_to(cu.target[0], DOWN, buff=0.1)
        cu.target.shift(np.array([xs[5], cancel.get_y() - 0.08, 0]) - cu.target[0].get_center())

        # step 2b: what is left, one Laplace ratio per answer
        comp_w = [widths[0], widths[1], widths[3], 0.3, widths[5], widths[6]]
        total_c = sum(comp_w) + gap * (len(comp_w) - 1)
        cx_c, x = [], -total_c / 2
        for w in comp_w:
            cx_c.append(x + w / 2)
            x += w + gap
        # cx_c: lhs, eq, C1, (dot), C2, dots
        bars_c = VGroup(Line([cx_c[2] - comp_w[2] / 2, y_bar, 0], [cx_c[2] + comp_w[2] / 2, y_bar, 0]),
                        Line([cx_c[4] - comp_w[4] / 2, y_bar, 0], [cx_c[4] + comp_w[4] / 2, y_bar, 0]))
        bars_c.set_stroke(S.WHITE, 2.5)
        dot_c = S.math(r"\cdot", size=size).move_to([cx_c[3], y_bar, 0])
        bound_y = 0.75
        b_le = S.math(r"\le", size=size).move_to([cx_c[1], bound_y, 0])
        b1 = S.math(r"e^{|\Delta_1|/\lambda}", size=size).move_to([cx_c[2], bound_y, 0])
        b_dot = S.math(r"\cdot", size=size).move_to([cx_c[3], bound_y, 0])
        b2 = S.math(r"e^{|\Delta_2|/\lambda}", size=size).move_to([cx_c[4], bound_y, 0])
        b_dots = S.math(r"\cdots", size=size).move_to([cx_c[5], bound_y, 0])
        bounds = VGroup(b_le, b1, b_dot, b2, b_dots)
        delta_cap = S.math(r"\Delta_i = f_i(", "x", r") - f_i(", "x'", r")", size=30)
        delta_cap[1].set_color(X_COLOR)
        delta_cap[3].set_color(XP_COLOR)
        delta_txt = S.text("how much question i's true answer differs between the worlds", 22, S.GREY)
        delta = VGroup(delta_cap, delta_txt).arrange(RIGHT, buff=0.35).move_to([0, -0.05, 0])

        # step 3: the product of exponentials is the exponential of a sum
        l3 = S.math(r"=", r"\exp\Big(", r"\sum_i", r"|\Delta_i|/\lambda", r"\Big)", r"=",
                    r"\exp\big(\|f_t(", "x", r") - f_t(", "x'", r")\|_1/\lambda\big)", r"\le", r"e^{\varepsilon}",
                    size=size)
        l3[7].set_color(X_COLOR)
        l3[9].set_color(XP_COLOR)
        l3[12][1].set_color(EPS_COLOR)
        l3.move_to([0, -1.05, 0])
        when = S.math(r"\text{when}\quad", r"\lambda = \max_t\,", r"S(f_t)", r"/", r"\varepsilon", size=size)
        when[2].set_color(SENS_COLOR)
        when[4].set_color(EPS_COLOR)
        ft_cap = VGroup(S.math("f_t", size=26, color=S.GREY),
                        S.text(": all the questions asked along t", 22, S.GREY)).arrange(RIGHT, buff=0.08)
        when_row = VGroup(when, ft_cap).arrange(RIGHT, buff=0.6).move_to([0, -2.1, 0])
        rl = VGroup(S.text("RL:", 24, S.WHITE, weight="BOLD"),
                    S.text("analyst = environment (cancels),  curator = policy", 24, S.GREY))
        rl.arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.45)

        with self.voiceover(SAY[1]) as vo:
            # shrink the ledger into a reference picture; the query cards' sub-captions ("histogram", ...)
            # would drop below 20 pt, so they fade and the f_i heads re-centre in their cards, while
            # "analyst" / "curator" keep their full 22 pt size so the two people stay named
            L = self.ledger
            L.generate_target()
            T = L.target
            for k in (2, 3, 4):             # query cards: hide the sub-caption, centre f_i
                T[k][2].set_opacity(0)
                T[k][1].move_to(T[k][0])
            T.scale(0.72).to_corner(UR, buff=0.6)
            for k in (0, 1):                # "analyst", "curator": back to 22 pt under their icon
                T[k][1].scale(1 / 0.72).next_to(T[k][0], DOWN, buff=0.1)
            self.play(MoveToTarget(L), FadeIn(title, shift=RIGHT * 0.2), run_time=1.0)
            vo.wait_until("Write the probability")
            self.play(Write(lhs_top), Write(eq), run_time=0.6)
            sources = [P["qs"][0][1], P["down"][0], P["diag"][0], P["down"][1]]
            for m, src in zip(top[:4], sources):
                self.play(Indicate(src, color=S.WHITE, scale_factor=1.1), FadeIn(m, shift=DOWN * 0.25), run_time=0.55)
            self.play(FadeIn(top[4]), FadeIn(legend, shift=UP * 0.15), run_time=0.6)

            vo.wait_until("The analyst's choice")
            self.play(Indicate(top[0], color=S.WHITE), Indicate(top[2], color=S.WHITE), run_time=0.8)
            self.play(FadeOut(VGroup(*self.ledger[2:])), FadeOut(legend), MoveToTarget(an), MoveToTarget(cu),
                      run_time=0.7)
            self.play(*[Transform(m, t) for m, t in zip([lhs_top, eq] + top, targets_top)], run_time=1.0)
            self.play(TransformFromCopy(lhs_top, lhs_bot), *[TransformFromCopy(a, b) for a, b in zip(top[:4], bot[:4])],
                      Create(bar_l), Create(bar_r), run_time=1.0)
            vo.wait_until("so in the ratio")
            strikes = VGroup(cancel_line("F1"), cancel_line("F2"))
            ptrs = VGroup(*[Line(cancel.get_top() + UP * 0.04, VGroup(*col[n]).get_bottom() + DOWN * 0.06,
                                 color=ANALYST, stroke_width=1.5) for n in ("F1", "F2")])
            self.play(Create(strikes), run_time=0.6)
            self.play(FadeIn(cancel), Create(ptrs), Indicate(an[0], color=ANALYST_COLOR, scale_factor=1.2),
                      run_time=0.5)
            vo.wait_until("leaving one Laplace")
            # the analyst leaves with its factors; the curator, whose Laplace ratios remain, a beat later
            self.play(FadeOut(VGroup(*col["F1"], *col["F2"], strikes, cancel, ptrs, an)), run_time=0.5)
            dots_mid = top[4]
            self.play(lhs_top.animate.set_x(cx_c[0]), lhs_bot.animate.set_x(cx_c[0]), bar_l.animate.set_x(cx_c[0]),
                      eq.animate.set_x(cx_c[1]),
                      top[1].animate.set_x(cx_c[2]), bot[1].animate.set_x(cx_c[2]),
                      top[3].animate.set_x(cx_c[4]), bot[3].animate.set_x(cx_c[4]),
                      dots_mid.animate.set_x(cx_c[5]), ReplacementTransform(bar_r, bars_c), FadeIn(dot_c),
                      FadeOut(cu), run_time=0.8)
            self.play(LaggedStart(FadeIn(b_le), FadeIn(b1, shift=DOWN * 0.25), FadeIn(b_dot),
                                  FadeIn(b2, shift=DOWN * 0.25), FadeIn(b_dots), lag_ratio=0.2), run_time=1.0)
            self.play(FadeIn(delta, shift=UP * 0.1), run_time=0.6)

            vo.wait_until("If you know")
            self.play(FadeIn(rl, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("whatever is identical")
            self.play(Write(VGroup(*l3[0:5])), Indicate(VGroup(b1, b2), color=S.WHITE), run_time=1.1)
            self.play(Write(VGroup(*l3[5:11])), run_time=1.0)
            self.play(Write(VGroup(*l3[11:])), run_time=0.5)
            vo.wait_until("the per-step")
            self.play(Indicate(l3[2], color=EPS_COLOR), FadeIn(when_row, shift=UP * 0.1), run_time=0.8)
            self.play(Circumscribe(VGroup(l3[11:], when), color=EPS_COLOR), run_time=vo.remaining(0.6))
        self.thm = VGroup(title, lhs_top, lhs_bot, bar_l, eq, top[1], bot[1], top[3], bot[3], dots_mid, bars_c, dot_c,
                          bounds, delta, when_row, rl)
        self.l3 = l3
        self.eps_glyph = l3[12]


    # ============================================================ 2. the privacy budget
    def budget_beat(self):
        # the shared budget bar: 8 equal segments, each answered query spends 2 of them (4 queries empty it)
        bar_y = 1.4
        bar = budget_bar(width=6.4, n=8, label_size=38)
        bar.shift(np.array([0.8, bar_y, 0]) - bar.frame.get_center())
        outline, segs, bar_lab = bar.frame, bar.segs, bar.label
        per_q = 2
        spent = [segs[len(segs) - per_q * (i + 1):len(segs) - per_q * i] for i in range(4)]  # drained from the right
        curator = VGroup(person_icon(S.WHITE, 0.8), S.text("curator", 22, S.GREY)).arrange(DOWN, buff=0.12)
        curator.move_to([5.4, bar_y - 0.1, 0])

        q_ys = [2.7, 1.85, 1.0, 0.15, -0.7]
        qcards = []
        for i, yy in enumerate(q_ys):
            f = card_frame(1.1, 0.62)
            qcards.append(VGroup(f, S.math(f"f_{i + 1}", size=32).move_to(f)).move_to([-5.6, yy, 0]))
        chips = []
        for i in range(4):
            chip = spent[i].copy().scale(0.55)          # a miniature of the two segments this answer spent
            chip.next_to(qcards[i], RIGHT, buff=0.2)
            lab = S.math(rf"\varepsilon_{i + 1}", size=28, color=EPS_COLOR).next_to(chip, RIGHT, buff=0.12)
            chips.append(VGroup(chip, lab))
        refused = S.text("refused", 30, NOISE_COLOR).next_to(curator, DOWN, buff=0.25)
        x5 = x_mark(qcards[4], pad=0.05)

        # S02's map chip for Dinur & Nissim (scaled up a little), with its idea as a caption
        dn = map_chip("Dinur & Nissim", "2003").scale(1.25).move_to([0.8, -0.8, 0])
        dn_idea = S.text("too many accurate answers ⇒ reconstruction", 22, S.GREY).next_to(dn, DOWN, buff=0.2)
        dn_arrow = Arrow(dn.get_top(), outline.get_bottom(), buff=0.12, color=S.GREY, stroke_width=3,
                         tip_length=0.16)
        dn_lab = S.text("limit on questions,\nnow explicit and measurable", 22, S.GREY, line_spacing=0.9)
        dn_lab.next_to(dn_arrow, LEFT, buff=0.25)
        total = S.math(r"\varepsilon_1", "+", r"\varepsilon_2", "+", r"\varepsilon_3", "+", r"\varepsilon_4",
                       r"\le", r"\varepsilon", size=32, color=EPS_COLOR)
        for k in (1, 3, 5, 7):
            total[k].set_color(S.WHITE)
        total.move_to([-4.6, -1.6, 0])
        caption = S.text("refusing depends only on the queries' sensitivity, not the data", 24, S.GREY)
        caption.to_edge(DOWN, buff=0.45)

        with self.voiceover(SAY[2]) as vo:
            keep = self.eps_glyph
            self.play(FadeOut(self.thm), FadeOut(VGroup(*[p for p in self.l3 if p is not keep])), run_time=0.7)
            self.play(ReplacementTransform(keep, bar_lab[1]), FadeIn(bar_lab[0]), run_time=0.9)
            self.play(Create(outline), LaggedStart(*[GrowFromEdge(s, LEFT) for s in segs], lag_ratio=0.3),
                      FadeIn(curator), run_time=1.4)

            vo.wait_until("Each answer spends")
            per = vo.until("once it is spent", minimum=1.6) / 4     # the bar is empty right at "once it is spent"
            for i in range(4):
                self.play(FadeIn(qcards[i], shift=RIGHT * 0.2), run_time=0.35 * per)
                self.play(*[ReplacementTransform(s, c) for s, c in zip(spent[i], chips[i][0])],
                          FadeIn(chips[i][1]), run_time=0.65 * per)
            vo.wait_until("once it is spent")
            self.play(FadeIn(qcards[4], shift=RIGHT * 0.2), run_time=0.3)
            self.play(Indicate(outline, color=NOISE_COLOR, scale_factor=1.03), run_time=0.5)
            self.play(Create(x5), FadeIn(refused, scale=1.3), run_time=0.5)

            vo.wait_until("That is the answer")
            dn_start = dn.copy().move_to([-9.5, dn.get_y(), 0])
            self.play(ReplacementTransform(dn_start, dn), run_time=1.0, rate_func=smooth)
            self.play(FadeIn(dn_idea, shift=UP * 0.1), GrowArrow(dn_arrow), FadeIn(dn_lab), run_time=0.6)
            vo.wait_until("the budget makes")
            self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.6)
            # the spent pieces add up to the budget: each chip label flies into the sum
            self.play(LaggedStart(*[AnimationGroup(Indicate(chips[i][0], color=S.WHITE, scale_factor=1.15),
                                                   TransformFromCopy(chips[i][1], total[2 * i]))
                                    for i in range(4)], lag_ratio=0.3),
                      FadeIn(VGroup(total[1], total[3], total[5], total[7])),
                      TransformFromCopy(bar_lab[1], total[8]), run_time=1.3)
            self.play(Circumscribe(total, color=EPS_COLOR, buff=0.12), run_time=vo.remaining(0.8))
        self.wait(0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)

    # ============================================================ 3-4. a histogram: d queries vs one
    def histogram_beats(self):
        rng = np.random.default_rng(9)
        d_small = 10
        heights = np.round(0.35 + 1.2 * np.exp(-((np.arange(d_small) - 3.5) / 2.6) ** 2)
                           + 0.15 * rng.random(d_small), 2)
        base_y = -2.95
        bw, gap = 0.42, 0.08
        bars = VGroup(*[Rectangle(width=bw, height=h, stroke_width=0).set_fill(X_COLOR, 0.75) for h in heights])
        bars.arrange(RIGHT, buff=gap, aligned_edge=DOWN)
        bars.move_to([-3.5, base_y, 0], aligned_edge=DOWN)
        base = Line(bars.get_corner(DL) + LEFT * 0.1, bars.get_corner(DR) + RIGHT * 0.1, color=S.GREY,
                    stroke_width=2)
        h_title = S.math(r"\text{histogram, }", "d", r"\text{ bins}", size=32).next_to(bars, UP, buff=0.55)
        h_title.set_x(bars.get_x())

        # the same budget bar, now cut into d equal parts: one per bin
        bud = budget_bar(width=5.1, n=d_small, label_size=32)
        bud.shift(np.array([3.45, -2.2, 0]) - bud.frame.get_center())
        b_outline, slices, b_lab = bud.frame, bud.segs, bud.label
        chips = VGroup(*[s.copy().scale(bw / s.width).next_to(b, UP, buff=0.08) for s, b in zip(slices, bars)])
        chip_lab = S.math(r"\varepsilon / d", r"\text{ each}", size=30, color=EPS_COLOR)
        chip_lab.next_to(chips[-1], UP, buff=0.25).shift(RIGHT * 0.4)
        q_noise = S.math(r"\text{noise per bin} = \;?", size=34, color=NOISE_COLOR).move_to(b_outline)

        with self.voiceover(SAY[3]) as vo:
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08),
                      run_time=1.6)
            vo.wait_until("Pause: a histogram")
            self.play(FadeIn(h_title, shift=DOWN * 0.15), run_time=0.6)
            self.play(Create(b_outline), FadeIn(slices), FadeIn(b_lab), run_time=0.8)
            vo.wait_until("Treat each bin")
            self.play(LaggedStart(*[Indicate(b, color=S.WHITE, scale_factor=1.08) for b in bars], lag_ratio=0.08),
                      run_time=1.2)
            vo.wait_until("split the budget")
            self.play(LaggedStart(*[ReplacementTransform(s, c) for s, c in zip(slices, chips)], lag_ratio=0.08),
                      run_time=1.6)
            self.play(FadeIn(chip_lab), FadeOut(b_lab), FadeOut(b_outline), run_time=0.5)
            vo.wait_until("How much noise")
            self.play(FadeIn(q_noise, scale=1.1), run_time=0.6)
        card = ponder_at(self, "d bins, total budget ε. Each bin as its own counting query,\n"
                               "budget split evenly: noise per bin?", seconds=12, pos=UP * 1.55, width=11.0)

        # ---- the answer: two panels on the same data
        def panel(noisy, center):
            ax, bars, truth = hist_panel(TRUE_COUNTS, noisy)
            shift = np.array(center) - ax.get_center()
            for m in (ax, bars, truth):
                m.shift(shift)
            return ax, bars, truth

        ax_l, bars_l, truth_l = panel(NOISY_SEPARATE, [-3.35, 0.15, 0])
        ax_r, bars_r, truth_r = panel(NOISY_JOINT, [3.35, 0.15, 0])

        t_l = S.text("d separate queries", 30, S.WHITE).move_to([-3.35, 3.25, 0])
        t_r = VGroup(S.text("one query,", 30, S.WHITE), S.math("S = 2", size=34, color=SENS_COLOR))
        t_r.arrange(RIGHT, buff=0.2).move_to([3.35, 3.25, 0])
        lab_l = S.math(r"\mathrm{Lap}(", "d", "/", r"\varepsilon", r")", r"\text{ per bin}", size=34)
        lab_r = S.math(r"\mathrm{Lap}(", "2", "/", r"\varepsilon", r")", r"\text{ per bin}", size=34)
        for lab in (lab_l, lab_r):
            lab[0].set_color(NOISE_COLOR)
            lab[2].set_color(NOISE_COLOR)
            lab[4].set_color(NOISE_COLOR)
            lab[3].set_color(EPS_COLOR)
        lab_r[1].set_color(SENS_COLOR)
        lab_l.next_to(t_l, DOWN, buff=0.2)
        lab_r.next_to(t_r, DOWN, buff=0.2)
        key = VGroup(
            VGroup(Square(0.2, stroke_width=0).set_fill(X_COLOR, 0.75), S.text("released", 22, S.GREY)).arrange(RIGHT, buff=0.12),
            VGroup(Line(ORIGIN, RIGHT * 0.35, color=S.WHITE, stroke_width=2.5), S.text("true counts", 22, S.GREY)).arrange(RIGHT, buff=0.12),
            S.math(r"d = 100,\ \ \varepsilon = 1", size=28, color=S.GREY),
        ).arrange(RIGHT, buff=0.6).move_to([0, -2.35, 0])
        note = VGroup(S.text("earlier SuLQ analysis:", 24, S.GREY),
                      S.math(r"\sim \sqrt{d}/\varepsilon", size=32, color=S.GREY),
                      S.text("per bin — still grows with d", 24, S.GREY)).arrange(RIGHT, buff=0.18)
        note.to_edge(DOWN, buff=0.45)

        def grow(bars):
            return LaggedStart(*[GrowFromEdge(b, b.grow_dir) for b in bars], lag_ratio=0.012)

        small = VGroup(bars, base, h_title, chips, chip_lab, q_noise)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card), FadeOut(small), run_time=0.6)
            self.play(FadeIn(t_l, shift=DOWN * 0.15), Create(ax_l), run_time=0.7)
            self.play(Create(truth_l), FadeIn(key[1]), FadeIn(key[2]), run_time=0.7)
            vo.wait_until("so noise of scale")
            self.play(Write(lab_l), run_time=0.8)
            self.play(grow(bars_l), FadeIn(key[0]), run_time=1.4)
            vo.wait_until("Treated as one")
            self.play(FadeIn(t_r, shift=DOWN * 0.15), Create(ax_r), Create(truth_r), run_time=0.9)
            self.play(Write(lab_r), run_time=0.8)
            self.play(grow(bars_r), run_time=1.4)
            vo.wait_until("whatever d is")
            self.play(Indicate(lab_r[1], color=SENS_COLOR, scale_factor=1.4), run_time=0.8)
            vo.wait_until("The earlier framework")
            self.play(FadeIn(note, shift=UP * 0.15), run_time=0.9)
            self.play(Indicate(note[1], color=S.WHITE), run_time=0.9)
            vo.wait_until("but it still grew")
            self.play(Indicate(lab_l[1], color=S.WHITE, scale_factor=1.4), run_time=vo.remaining(0.8))
        self.wait(0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
