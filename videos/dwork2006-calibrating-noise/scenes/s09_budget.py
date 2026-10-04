"""S09 · Many questions: the privacy budget (Theorem 1, p. 273; histograms, §3.2)."""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import paper_card, person_icon, ponder_card
from explainer.scene import VoiceScene

from common import ALICE, EPS_COLOR, NARRATION, NOISE_COLOR, SENS_COLOR, X_COLOR, XP_COLOR

SAY = NARRATION["S09"]
ANALYST = S.GREY          # analyst factors: identical in both worlds


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
        analyst = VGroup(person_icon(S.WHITE, 0.75), S.text("analyst", 22, S.GREY)).arrange(DOWN, buff=0.12)
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

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(analyst, shift=RIGHT * 0.2), FadeIn(curator, shift=RIGHT * 0.2), run_time=0.6)
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
        self.parts = dict(qs=qs, ans=ans, down=down, diag=diag, q_dots=q_dots)

    # ============================================================ 1. Theorem 1: the ratio telescopes
    def theorem_beat(self):
        P = self.parts
        title = S.text("Theorem 1", 32, EPS_COLOR, weight="BOLD").to_corner(UL, buff=0.4)

        prod_spec = [
            ("lhs", [(r"\Pr[t \mid ", None), ("x", X_COLOR), ("]", None)]),
            ("eq", [("=", None)]),
            ("F1", [(r"\Pr[f_1]", ANALYST)]),
            ("C1", [(r"\Pr[a_1 \mid ", None), ("x", X_COLOR), ("]", None)]),
            ("dot", [(r"\cdot", None)]),
            ("F2", [(r"\Pr[f_2 \mid a_1]", ANALYST)]),
            ("C2", [(r"\Pr[a_2 \mid a_1;\, ", None), ("x", X_COLOR), ("]", None)]),
            ("dots", [(r"\cdots", None)]),
        ]
        prod, pg = build_tex(prod_spec, size=36)
        prod.move_to([0, -1.1, 0])
        legend = VGroup(
            VGroup(Square(0.22, stroke_width=0).set_fill(ANALYST, 1),
                   S.text("analyst picks the next question", 24, ANALYST)).arrange(RIGHT, buff=0.2),
            VGroup(Square(0.22, stroke_width=0).set_fill(S.WHITE, 1),
                   S.text("curator answers with Laplace noise", 24, S.WHITE)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(prod, DOWN, buff=0.55)

        ratio_spec = [
            ("lhs", [(r"\frac{\Pr[t \mid ", None), ("x", X_COLOR), (r"]}{\Pr[t \mid ", None), ("x'", XP_COLOR),
                     ("]}", None)]),
            ("eq", [("=", None)]),
            ("F1", [(r"\frac{\Pr[f_1]}{\Pr[f_1]}", ANALYST)]),
            ("C1", [(r"\frac{\Pr[a_1 \mid ", None), ("x", X_COLOR), (r"]}{\Pr[a_1 \mid ", None),
                    ("x'", XP_COLOR), ("]}", None)]),
            ("dot", [(r"\cdot", None)]),
            ("F2", [(r"\frac{\Pr[f_2 \mid a_1]}{\Pr[f_2 \mid a_1]}", ANALYST)]),
            ("C2", [(r"\frac{\Pr[a_2 \mid a_1;\, ", None), ("x", X_COLOR), (r"]}{\Pr[a_2 \mid a_1;\, ", None),
                    ("x'", XP_COLOR), ("]}", None)]),
            ("dots", [(r"\cdots", None)]),
        ]
        ratio, rg = build_tex(ratio_spec, size=36)
        ratio.move_to([0, 1.95, 0])
        # compact version once the analyst factors are gone
        comp_spec = [s for s in ratio_spec if s[0] not in ("F1", "F2")]
        comp, cg = build_tex(comp_spec, size=36)
        comp.move_to([0, 1.95, 0])

        strikes = VGroup(strike_line(rg["F1"]), strike_line(rg["F2"]))
        cancel = S.text("same in both worlds: cancels", 24, ANALYST)
        cancel.move_to([(rg["F1"].get_x() + rg["F2"].get_x()) / 2, rg["F1"].get_bottom()[1] - 0.4, 0])
        ptrs = VGroup(*[Line(cancel.get_top() + UP * 0.05, f.get_bottom() + DOWN * 0.08, color=ANALYST,
                             stroke_width=1.5) for f in (rg["F1"], rg["F2"])])

        b_le = S.math(r"\le", size=36)
        b1 = S.math(r"e^{|\Delta_1|/\lambda}", size=36)
        b_dot = S.math(r"\cdot", size=36)
        b2 = S.math(r"e^{|\Delta_2|/\lambda}", size=36)
        b_dots = S.math(r"\cdots", size=36)
        bound_y = 0.55
        b_le.move_to([cg["eq"].get_x(), bound_y, 0])
        b1.move_to([cg["C1"].get_x(), bound_y, 0])
        b_dot.move_to([cg["dot"].get_x(), bound_y, 0])
        b2.move_to([cg["C2"].get_x(), bound_y, 0])
        b_dots.move_to([cg["dots"].get_x(), bound_y, 0])
        bounds = VGroup(b_le, b1, b_dot, b2, b_dots)
        delta_cap = S.math(r"\Delta_i = f_i(", "x", r") - f_i(", "x'", r")", size=30)
        delta_cap[1].set_color(X_COLOR)
        delta_cap[3].set_color(XP_COLOR)
        delta_txt = S.text("how much question i's true answer differs between the worlds", 22, S.GREY)
        delta = VGroup(delta_cap, delta_txt).arrange(RIGHT, buff=0.35).move_to([0, -0.35, 0])

        l3 = S.math(r"=", r"\exp\Big(", r"\sum_i", r"|\Delta_i|/\lambda", r"\Big)", r"=",
                    r"\exp\big(\|f_t(", "x", r") - f_t(", "x'", r")\|_1/\lambda\big)", r"\le", r"e^{\varepsilon}",
                    size=36)
        l3[7].set_color(X_COLOR)
        l3[9].set_color(XP_COLOR)
        l3[12][1].set_color(EPS_COLOR)
        l3.move_to([0, -1.45, 0])
        l3.shift(RIGHT * (b_le.get_x() - l3[0].get_x()))
        if l3.get_right()[0] > 6.5:
            l3.shift(LEFT * (l3.get_right()[0] - 6.5))
        when = S.math(r"\text{when}\quad", r"\lambda = \max_t\,", r"S(f_t)", r"/", r"\varepsilon", size=36)
        when[2].set_color(SENS_COLOR)
        when[4].set_color(EPS_COLOR)
        when.next_to(l3, DOWN, buff=0.4).align_to(l3[5], LEFT)
        ft_cap = S.text("f_t: all the questions asked along t", 20, S.GREY)
        ft_cap = VGroup(S.math("f_t", size=26, color=S.GREY), S.text(": all the questions asked along t", 20, S.GREY))
        ft_cap.arrange(RIGHT, buff=0.08).next_to(when, RIGHT, buff=0.6)
        rl = VGroup(S.text("RL:", 24, S.WHITE, weight="BOLD"),
                    S.text("analyst = environment (cancels),  curator = policy", 24, S.GREY))
        rl.arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.35)

        with self.voiceover(SAY[0 + 1]) as vo:
            self.play(self.ledger.animate.scale(0.7).to_corner(UR, buff=0.3), FadeIn(title, shift=RIGHT * 0.2),
                      run_time=1.0)
            vo.wait_until("Write the probability")
            self.play(Write(pg["lhs"]), Write(pg["eq"]), run_time=0.6)
            sources = [("F1", P["qs"][0][1]), ("C1", P["down"][0]), ("F2", P["diag"][0]), ("C2", P["down"][1])]
            for name, src in sources:
                self.play(TransformFromCopy(src, pg[name]), *( [FadeIn(pg["dot"])] if name == "F2" else []),
                          run_time=0.55)
            self.play(FadeIn(pg["dots"]), FadeIn(legend, shift=UP * 0.15), run_time=0.6)

            vo.wait_until("The analyst's choice")
            self.play(Indicate(pg["F1"], color=S.WHITE), Indicate(pg["F2"], color=S.WHITE), run_time=0.8)
            self.play(FadeOut(self.ledger), FadeOut(legend), run_time=0.5)
            self.play(*[ReplacementTransform(pg[k], rg[k]) for k in pg], run_time=1.3)
            vo.wait_until("so in the ratio")
            self.play(Create(strikes), run_time=0.6)
            self.play(FadeIn(cancel), Create(ptrs), run_time=0.5)
            vo.wait_until("leaving one Laplace")
            self.play(FadeOut(VGroup(rg["F1"], rg["F2"], strikes, cancel, ptrs)), run_time=0.5)
            self.play(*[ReplacementTransform(rg[k], cg[k]) for k in cg], run_time=0.8)
            self.play(FadeIn(b_le), TransformFromCopy(cg["C1"], b1), TransformFromCopy(cg["C2"], b2),
                      FadeIn(b_dot), FadeIn(b_dots), run_time=1.0)
            self.play(FadeIn(delta, shift=UP * 0.1), run_time=0.6)

            vo.wait_until("If you know")
            self.play(FadeIn(rl, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("whatever is identical")
            self.play(FadeIn(l3[0]), TransformFromCopy(VGroup(b1, b2, b_dots), VGroup(*l3[1:5])), run_time=1.1)
            self.play(Write(VGroup(*l3[5:11])), run_time=1.0)
            self.play(Write(VGroup(*l3[11:])), run_time=0.5)
            vo.wait_until("the per-step")
            self.play(Indicate(l3[2], color=EPS_COLOR), FadeIn(when, shift=UP * 0.1), FadeIn(ft_cap), run_time=0.8)
            self.play(Circumscribe(VGroup(l3[11:], when), color=EPS_COLOR), run_time=vo.remaining(0.6))
        self.thm = VGroup(title, cg["lhs"], cg["eq"], cg["C1"], cg["dot"], cg["C2"], cg["dots"], bounds, delta,
                          l3, when, ft_cap, rl)
        self.eps_glyph = l3[12]

    # ============================================================ 2. the privacy budget
    def budget_beat(self):
        bar_l, bar_r, bar_y, bar_h = -2.4, 4.0, 1.4, 0.6
        costs = [0.25, 0.3, 0.2, 0.25]
        width = bar_r - bar_l
        outline = Rectangle(width=width, height=bar_h, stroke_color=EPS_COLOR, stroke_width=2.5)
        outline.move_to([(bar_l + bar_r) / 2, bar_y, 0])
        segs = VGroup()
        x = bar_l
        for c in costs:
            w = c * width
            segs.add(Rectangle(width=w, height=bar_h, stroke_color=S.BG, stroke_width=2)
                     .set_fill(EPS_COLOR, 0.9).move_to([x + w / 2, bar_y, 0]))
            x += w
        bar_lab = S.math(r"\text{privacy budget }", r"\varepsilon", size=38, color=EPS_COLOR)
        bar_lab.next_to(outline, UP, buff=0.25)
        curator = VGroup(person_icon(S.WHITE, 0.8), S.text("curator", 22, S.GREY)).arrange(DOWN, buff=0.12)
        curator.move_to([5.4, bar_y - 0.1, 0])

        q_ys = [2.7, 1.85, 1.0, 0.15, -0.7]
        qcards = []
        for i, yy in enumerate(q_ys):
            f = card_frame(1.1, 0.62)
            qcards.append(VGroup(f, S.math(f"f_{i + 1}", size=32).move_to(f)).move_to([-5.6, yy, 0]))
        chips = []
        for i, c in enumerate(costs):
            w = c * width * 0.38
            chip = Rectangle(width=w, height=0.3, stroke_width=0).set_fill(EPS_COLOR, 0.9)
            chip.next_to(qcards[i], RIGHT, buff=0.25)
            lab = S.math(rf"\varepsilon_{i + 1}", size=28, color=EPS_COLOR).next_to(chip, RIGHT, buff=0.12)
            chips.append(VGroup(chip, lab))
        refused = S.text("refused", 30, NOISE_COLOR).next_to(curator, DOWN, buff=0.25)
        x5 = x_mark(qcards[4], pad=0.05)

        dn = paper_card("Dinur & Nissim", 2003, "too many accurate answers ⇒ reconstruction", color=S.WHITE,
                        width=4.6, size=24)
        dn.move_to([0.8, -1.0, 0])
        dn_arrow = Arrow(dn.get_top(), outline.get_bottom(), buff=0.12, color=S.GREY, stroke_width=3,
                         tip_length=0.16)
        dn_lab = S.text("limit on questions,\nnow explicit and measurable", 22, S.GREY, line_spacing=0.9)
        dn_lab.next_to(dn_arrow, RIGHT, buff=0.25)
        caption = S.text("refusing depends only on the queries' sensitivity, not the data", 24, S.GREY)
        caption.to_edge(DOWN, buff=0.45)

        with self.voiceover(SAY[2]) as vo:
            keep = self.eps_glyph
            self.play(FadeOut(VGroup(*[m for m in self.thm if m is not self.thm[9]])),
                      FadeOut(VGroup(*[p for p in self.thm[9] if p is not keep])), run_time=0.7)
            self.play(ReplacementTransform(keep, bar_lab[1]), FadeIn(bar_lab[0]), run_time=0.9)
            self.play(Create(outline), LaggedStart(*[GrowFromEdge(s, LEFT) for s in segs], lag_ratio=0.6),
                      FadeIn(curator), run_time=1.4)

            vo.wait_until("Each answer spends")
            for i in range(4):
                seg = segs[3 - i]
                self.play(FadeIn(qcards[i], shift=RIGHT * 0.2), run_time=0.25)
                self.play(ReplacementTransform(seg, chips[i][0]), FadeIn(chips[i][1]), run_time=0.55)
            vo.wait_until("once it is spent")
            self.play(FadeIn(qcards[4], shift=RIGHT * 0.2), run_time=0.3)
            self.play(Indicate(outline, color=NOISE_COLOR, scale_factor=1.03), run_time=0.5)
            self.play(Create(x5), FadeIn(refused, scale=1.3), run_time=0.5)

            vo.wait_until("That is the answer")
            dn_start = dn.copy().move_to([-9.5, -1.0, 0])
            self.play(ReplacementTransform(dn_start, dn), run_time=1.0, rate_func=smooth)
            self.play(GrowArrow(dn_arrow), FadeIn(dn_lab), run_time=0.7)
            vo.wait_until("the budget makes")
            self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
            self.play(Indicate(VGroup(*[c[0] for c in chips]), color=S.WHITE), run_time=vo.remaining(0.6))
        self.wait(0.2)
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

        bb_l, bb_r, bb_y = 0.9, 6.0, -2.2
        bwid = bb_r - bb_l
        b_outline = Rectangle(width=bwid, height=0.5, stroke_color=EPS_COLOR, stroke_width=2.5)
        b_outline.move_to([(bb_l + bb_r) / 2, bb_y, 0])
        slices = VGroup(*[Rectangle(width=bwid / d_small, height=0.5, stroke_color=S.BG, stroke_width=2)
                          .set_fill(EPS_COLOR, 0.9) for _ in range(d_small)]).arrange(RIGHT, buff=0)
        slices.move_to(b_outline)
        b_lab = S.math(r"\text{total budget }", r"\varepsilon", size=32, color=EPS_COLOR)
        b_lab.next_to(b_outline, UP, buff=0.25)
        chips = VGroup(*[Rectangle(width=bw, height=0.12, stroke_width=0).set_fill(EPS_COLOR, 0.95)
                         .next_to(b, UP, buff=0.08) for b in bars])
        chip_lab = S.math(r"\varepsilon / d", r"\text{ each}", size=30, color=EPS_COLOR)
        chip_lab.next_to(chips[-1], UP, buff=0.25).shift(RIGHT * 0.4)
        q_noise = S.math(r"\text{noise per bin} = \;?", size=34, color=NOISE_COLOR).move_to(b_outline)

        with self.voiceover(SAY[3]) as vo:
            vo.wait_until("Pause: a histogram")
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08),
                      FadeIn(h_title), run_time=1.3)
            self.play(Create(b_outline), FadeIn(slices), FadeIn(b_lab), run_time=0.8)
            vo.wait_until("Treat each bin")
            self.play(LaggedStart(*[Indicate(b, color=S.WHITE, scale_factor=1.08) for b in bars], lag_ratio=0.08),
                      run_time=1.2)
            vo.wait_until("split the budget")
            self.play(LaggedStart(*[ReplacementTransform(s, c) for s, c in zip(slices, chips)], lag_ratio=0.08),
                      run_time=1.6)
            self.play(FadeIn(chip_lab), FadeOut(b_lab), run_time=0.5)
            vo.wait_until("How much noise")
            self.play(FadeIn(q_noise, scale=1.1), run_time=0.6)
        card = ponder_at(self, "d bins, total budget ε. Each bin as its own counting query,\n"
                               "budget split evenly: noise per bin?", seconds=12, pos=UP * 1.55, width=11.0)

        # ---- the answer: two panels on the same data
        ax_l, bars_l, truth_l = hist_panel(TRUE_COUNTS, NOISY_SEPARATE)
        ax_r, bars_r, truth_r = hist_panel(TRUE_COUNTS, NOISY_JOINT)
        ax_l.move_to([-3.35, 0.15, 0])
        ax_r.move_to([3.35, 0.15, 0])
        for b in (bars_l, truth_l):
            b.shift(ax_l.get_center() - ax_r.get_center() + (ax_r.get_center() - ax_l.get_center()))
        # (hist_panel built both at the origin; move bars/outlines with their axes)
        ax_l2, bars_l, truth_l = hist_panel(TRUE_COUNTS, NOISY_SEPARATE)
        shift_l = np.array([-3.35, 0.15, 0]) - ax_l2.get_center()
        for m in (ax_l2, bars_l, truth_l):
            m.shift(shift_l)
        ax_l = ax_l2
        ax_r2, bars_r, truth_r = hist_panel(TRUE_COUNTS, NOISY_JOINT)
        shift_r = np.array([3.35, 0.15, 0]) - ax_r2.get_center()
        for m in (ax_r2, bars_r, truth_r):
            m.shift(shift_r)
        ax_r = ax_r2

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
        note.to_edge(DOWN, buff=0.35)

        def grow(bars):
            return LaggedStart(*[GrowFromEdge(b, b.grow_dir) for b in bars], lag_ratio=0.012)

        small = VGroup(bars, base, h_title, chips, chip_lab, q_noise, b_outline)
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
