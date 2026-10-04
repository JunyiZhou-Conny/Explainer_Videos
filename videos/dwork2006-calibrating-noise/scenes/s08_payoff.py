"""S08 · Privacy for individuals, accuracy for populations.

Back to the S01 hospital with the Laplace mechanism switched on (epsilon = 0.5, scale 2), then
why the noise does not grow with n, and what goes wrong when epsilon << 1/n (the hybrid argument;
S11's chain of databases is drawn in the same `mini_db` look: 4 rows, GREY arrows, steps above).
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import laplace_pdf, person_grid, person_icon, ponder_card
from explainer.scene import VoiceScene

from common import ALICE, EPS_COLOR, NARRATION, NOISE_COLOR, SENS_COLOR, X_COLOR, XP_COLOR

SAY = NARRATION["S08"]

EPS = 0.5
LAM = 1 / EPS                 # S(count) = 1, so the Laplace scale is 1 / 0.5 = 2
A, B = 41.0, 42.0             # f(x), f(x')
WEEK1, WEEK2 = 43.7, 40.6     # the two released answers (script numbers)
POST_MAX = np.exp(EPS) / (1 + np.exp(EPS))      # 0.6225: best posterior from a 50/50 prior
POST_MIN = 1 - POST_MAX


# ---------------------------------------------------------------- shared helpers

def query_card(question: str, width: float = 4.6) -> VGroup:
    """The S01 query card."""
    q = S.text(question, 28, S.WHITE, line_spacing=1.0)
    if q.width > width - 0.5:
        q.scale_to_fit_width(width - 0.5)
    head = S.text("Query", 22, S.GREY, font=S.FONT_SANS)
    body = VGroup(head, q).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    frame = RoundedRectangle(width=width, height=body.height + 0.5, corner_radius=0.15,
                             stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
    body.move_to(frame)
    return VGroup(frame, head, q)


def hospital_grid(icon_h: float = 0.2) -> VGroup:
    """The S01 hospital: 15 x 8 slots, the same 41 PINK patients (same seed), Alice = last slot."""
    rng = np.random.default_rng(3)
    cols, rows = 15, 8
    n_slots = cols * rows
    sick = set(rng.choice(n_slots - 1, size=41, replace=False).tolist())
    icons = VGroup(*[person_icon(ALICE if (i in sick or i == n_slots - 1) else S.GREY, height=icon_h)
                     for i in range(n_slots)])
    k = icon_h / 0.34
    icons.arrange_in_grid(rows=rows, cols=cols, buff=(0.14 * k, 0.16 * k))
    return icons


def ponder_at(scene, question: str, seconds: float, pos=ORIGIN, **kw) -> VGroup:
    """pause_and_ponder, but placed at `pos` so a supporting picture can stay visible."""
    card = ponder_card(question, **kw).move_to(pos)
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return card


def mini_db(n_rows: int, changed: int, frame_color: str, width: float = 1.38,
            row_h: float = 0.3, changed_color: str = ALICE) -> VGroup:
    """A small database: n_rows rows, the first `changed` of them replaced (PINK; newest brightest).

    Returns VGroup(frame, rows) with rows[i] = VGroup(box, icon)."""
    rows = VGroup()
    for i in range(n_rows):
        box = Rectangle(width=width, height=row_h, stroke_color=S.GREY_DARK, stroke_width=1.5)
        col = S.GREY
        if i < changed:
            newest = i == changed - 1
            box.set_fill(changed_color, 0.55 if newest else 0.22)
            col = changed_color
        else:
            box.set_fill(S.GREY_DARKER, 1)
        icon = person_icon(col, height=row_h * 0.7).move_to(box.get_left() + RIGHT * 0.19)
        rows.add(VGroup(box, icon))
    rows.arrange(DOWN, buff=0)
    frame = SurroundingRectangle(rows, buff=0.06, color=frame_color, stroke_width=2.5,
                                 corner_radius=0.06)
    return VGroup(frame, rows)


def hybrid_chain(n_rows: int = 4, steps=(0, 1, 2, None, "n"), step_tex: str = r"\times\, e^{\varepsilon}",
                 start_tex: str = r"x = x^{(0)}", end_tex: str = r"x^{(n)} = y",
                 start_color: str = X_COLOR, end_color: str = S.WHITE, changed_color: str = ALICE,
                 gap: float = 1.25, label_size: float = 34, step_color: str = EPS_COLOR) -> VGroup:
    """The hybrid-argument chain x = x(0) -> x(1) -> ... -> x(n) = y, one row changing per step.

    `steps` lists the nodes: an int k = database with k rows changed, None = an ellipsis,
    "n" = all rows changed. Returns VGroup(nodes, arrows, step_labels, node_labels) where
    nodes[i] is a mini_db (or the ellipsis), arrows[j] joins nodes j and j+1."""
    nodes = VGroup()
    for k in steps:
        if k is None:
            nodes.add(S.math(r"\cdots", size=44, color=S.GREY))
        else:
            kk = n_rows if k == "n" else k
            col = start_color if k == 0 else (end_color if k == "n" else S.GREY)
            nodes.add(mini_db(n_rows, kk, col, changed_color=changed_color))
    nodes.arrange(RIGHT, buff=gap)
    arrows, step_labels = VGroup(), VGroup()
    for a, b in zip(nodes[:-1], nodes[1:]):
        arr = Arrow(a.get_right(), b.get_left(), buff=0.1, color=S.GREY, stroke_width=3,
                    tip_length=0.16, max_tip_length_to_length_ratio=0.3)
        lab = S.math(step_tex, size=label_size)
        lab.set_color(step_color)
        lab.next_to(arr, UP, buff=0.12)
        arrows.add(arr)
        step_labels.add(lab)
    node_labels = VGroup()
    names = {0: start_tex, "n": end_tex}
    for node, k in zip(nodes, steps):
        if k is None:
            node_labels.add(VMobject())
            continue
        tex = names.get(k, rf"x^{{({k})}}")
        col = start_color if k == 0 else (end_color if k == "n" else S.WHITE)
        node_labels.add(S.math(tex, size=label_size, color=col).next_to(node, DOWN, buff=0.18))
    return VGroup(nodes, arrows, step_labels, node_labels)


def bump_shape(center, units_per_data: float, lam: float, height: float, y: float,
               x_min: float = -6.6, x_max: float = 6.6, n_half: int = 80, half_width: float | None = None):
    """Laplace(lam) density drawn as a filled tent of fixed peak `height`, in screen coordinates.

    center = screen x of the mean; the curve spans +-half_width data units (default 7 lam),
    clipped to the visible [x_min, x_max]. Always 2 * n_half + 3 points (so bumps Transform)."""
    hw = 7 * lam if half_width is None else half_width
    lo = max(-hw, (x_min - center) / units_per_data)
    hi = min(hw, (x_max - center) / units_per_data)
    u = np.concatenate([np.linspace(lo, 0, n_half + 1), np.linspace(0, hi, n_half + 1)[1:]])
    xs = center + u * units_per_data
    ys = y + height * np.exp(-np.abs(u) / lam)
    pts = [np.array([xs[0], y, 0])] + [np.array([a, b, 0]) for a, b in zip(xs, ys)] + \
          [np.array([xs[-1], y, 0])]
    m = VMobject().set_points_as_corners(pts)
    m.set_stroke(NOISE_COLOR, 3).set_fill(NOISE_COLOR, 0.35)
    return m


def strike(m, color=NOISE_COLOR, width=6, pad=0.12):
    """A big diagonal X over m."""
    c = m.get_center()
    w, h = m.width / 2 + pad, m.height / 2 + pad
    return VGroup(Line(c + np.array([-w, -h, 0]), c + np.array([w, h, 0]), color=color, stroke_width=width),
                  Line(c + np.array([-w, h, 0]), c + np.array([w, -h, 0]), color=color, stroke_width=width))


# ---------------------------------------------------------------- the scene

class Payoff(VoiceScene):
    def construct(self):
        self.hospital_beat()
        self.depends_beat()
        self.populations_beat()
        self.slogan_beat()
        self.tiny_eps_beats()

    # ============================================================ 0. the hospital, privately
    def hospital_beat(self):
        # the S01 picture, smaller: query card (S01's card, same width), "Hospital database" over
        # the grid, the "has condition X" legend under it, Alice's name under her slot
        cx = -4.2                                   # centre of the left column
        card = query_card("How many patients\nhave condition X?")
        card.move_to([cx, 3.45 - card.height / 2, 0])
        db_label = S.text("Hospital database", 24, S.GREY).next_to(card, DOWN, buff=0.15)
        icons = hospital_grid(0.2)
        icons.next_to(db_label, DOWN, buff=0.15).set_x(cx)
        alice = icons[-1]
        patients = VGroup(*icons[:-1])
        alice_slot = alice.get_center()
        legend = VGroup(person_icon(ALICE, 0.22), S.text("has condition X", 20, S.GREY))
        legend.arrange(RIGHT, buff=0.12).next_to(icons, DOWN, buff=0.2).align_to(icons, LEFT)
        alice_lab = S.text("Alice", 22, ALICE)

        # formula: epsilon -> noise scale
        eps_eq = S.math(r"\varepsilon = 0.5", size=36, color=EPS_COLOR)
        implies = S.math(r"\Rightarrow", size=36)
        scale_eq = S.math(r"\text{noise scale}", r"=", r"\frac{S(f)}{\varepsilon}", r"=",
                          r"\frac{1}{0.5}", r"=", r"2", size=36)
        scale_eq[2][0:4].set_color(SENS_COLOR)
        scale_eq[2][5].set_color(EPS_COLOR)
        scale_eq[4][0].set_color(SENS_COLOR)
        scale_eq[4][2:].set_color(EPS_COLOR)
        scale_eq[6].set_color(NOISE_COLOR)
        top = VGroup(eps_eq, implies, scale_eq).arrange(RIGHT, buff=0.3).move_to([2.55, 3.0, 0])

        # the two worlds' output distributions (scale 2)
        ax = Axes(x_range=[31, 52, 1], y_range=[0, 0.28, 0.1], x_length=7.8, y_length=2.5, tips=False,
                  axis_config={"color": S.GREY, "stroke_width": 2},
                  y_axis_config={"include_ticks": False}).move_to([2.55, 0.5, 0])
        out_lab = S.text("released answer", 20, S.GREY).next_to(ax.x_axis.get_right(), DOWN, buff=0.18)
        out_lab.align_to(ax.x_axis, RIGHT)

        def world(mu, col, label_tex, side):
            curve = ax.plot(lambda t: laplace_pdf(t, mu, LAM), x_range=[31, 52, 0.02], color=col,
                            stroke_width=4)
            area = ax.get_area(curve, x_range=[31, 52], color=col, opacity=0.12)
            stem = DashedLine(ax.c2p(mu, 0), ax.c2p(mu, laplace_pdf(mu, mu, LAM)), color=col,
                              stroke_width=2, dash_length=0.06)
            lab = S.math(label_tex, size=30, color=col)
            lab.next_to(ax.c2p(mu, laplace_pdf(mu, mu, LAM)), side, buff=0.3)
            return curve, area, stem, lab

        pdf_a, area_a, stem_a, lab_a = world(A, X_COLOR, r"f(x) = 41", LEFT)
        pdf_b, area_b, stem_b, lab_b = world(B, XP_COLOR, r"f(x') = 42", RIGHT)

        def sample(mu, value, col):
            dot = Dot(ax.c2p(value, laplace_pdf(value, mu, LAM)), color=col, radius=0.08)
            line = DashedLine(ax.c2p(value, laplace_pdf(value, mu, LAM)), ax.c2p(value, 0), color=col,
                              stroke_width=2, dash_length=0.05)
            lab = S.math(f"{value:.1f}", size=32, color=col).next_to(ax.c2p(value, 0), DOWN, buff=0.22)
            return dot, line, lab

        dot1, drop1, val1 = sample(A, WEEK1, X_COLOR)
        dot2, drop2, val2 = sample(B, WEEK2, XP_COLOR)

        # left column: released answers and the subtraction
        ans1 = VGroup(S.text("week 1", 22, S.GREY), S.math(f"{WEEK1:.1f}", size=46, color=X_COLOR))
        ans2 = VGroup(S.text("week 2", 22, S.GREY), S.math(f"{WEEK2:.1f}", size=46, color=XP_COLOR))
        for g, x in ((ans1, cx - 0.95), (ans2, cx + 0.95)):
            g.arrange(DOWN, buff=0.12).move_to([x, -2.17, 0])
        diff = S.math(f"{WEEK2:.1f}", "-", f"{WEEK1:.1f}", "=", f"{WEEK2 - WEEK1:.1f}", size=44)
        diff[0].set_color(XP_COLOR)
        diff[2].set_color(X_COLOR)
        diff.move_to([cx, -3.08, 0])

        # belief meter (attacker starts at 50/50)
        m_left, m_right, m_y = 0.9, 6.2, -2.75

        def mx(p):
            return m_left + (m_right - m_left) * p

        meter = Line([m_left, m_y, 0], [m_right, m_y, 0], color=S.GREY, stroke_width=3)
        m_ticks = VGroup(*[Line([mx(p), m_y - 0.09, 0], [mx(p), m_y + 0.09, 0], color=S.GREY, stroke_width=2)
                           for p in (0, 0.5, 1)])
        m_labs = VGroup(*[S.text(s, 20, S.GREY).next_to([mx(p), m_y, 0], DOWN, buff=0.18)
                          for s, p in (("0%", 0), ("50%", 0.5), ("100%", 1))])
        band = Rectangle(width=mx(POST_MAX) - mx(POST_MIN), height=0.34, stroke_color=EPS_COLOR,
                         stroke_width=2).set_fill(EPS_COLOR, 0.2).move_to([mx(0.5), m_y, 0])
        p_track = ValueTracker(0.5)
        needle = Triangle(color=S.WHITE, fill_opacity=1, stroke_width=0).scale(0.11).rotate(PI)
        needle.add_updater(lambda m: m.move_to([mx(p_track.get_value()), m_y + 0.3, 0]))
        m_head = VGroup(S.text("Alice has X?", 24, S.GREY), S.text("50/50", 26, S.WHITE),
                        S.math(r"\to", size=30), S.text("at most 62%", 26, EPS_COLOR))
        m_head.arrange(RIGHT, buff=0.2).move_to([mx(0.5), -1.95, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(card, shift=RIGHT * 0.3), FadeIn(db_label), FadeIn(legend),
                      LaggedStart(*[FadeIn(p, scale=0.6) for p in patients], lag_ratio=0.006),
                      run_time=1.6)
            self.play(Write(eps_eq), run_time=0.7)
            vo.wait_until("Laplace noise")
            self.play(FadeIn(implies), Write(scale_eq), run_time=1.4)
            self.play(Create(ax), FadeIn(out_lab), run_time=0.7)

            vo.wait_until("Week one")
            # pulse the question only: Indicate on the whole card would paint its fill white
            self.play(Indicate(card[2], color=S.WHITE, scale_factor=1.08), run_time=0.5)
            self.play(Create(pdf_a), FadeIn(area_a), Create(stem_a), FadeIn(lab_a), run_time=1.2)
            self.add(dot1)
            self.play(FadeIn(dot1, scale=0.5), run_time=0.3)
            self.play(dot1.animate.move_to(ax.c2p(WEEK1, 0)), Create(drop1), run_time=0.7)
            self.play(FadeIn(val1, shift=DOWN * 0.1), run_time=0.4)
            self.play(TransformFromCopy(val1, ans1[1]), FadeIn(ans1[0]), run_time=0.7)

            vo.wait_until("Week two")
            # as in S01, Alice slides into the last slot from the right, her name under her
            # (a short slide: the plot's axis starts just to the right of the grid)
            alice.move_to(alice_slot + RIGHT * 0.75)
            alice_lab.next_to(alice, DOWN, buff=0.12).set_y(legend[1].get_y())
            self.play(FadeIn(alice), FadeIn(alice_lab), run_time=0.3)
            self.play(alice.animate.move_to(alice_slot), alice_lab.animate.shift(LEFT * 0.75),
                      Indicate(card[2], color=S.WHITE, scale_factor=1.08),
                      run_time=0.9)
            self.play(Create(pdf_b), FadeIn(area_b), Create(stem_b), FadeIn(lab_b), run_time=1.1)
            self.add(dot2)
            self.play(FadeIn(dot2, scale=0.5), run_time=0.3)
            self.play(dot2.animate.move_to(ax.c2p(WEEK2, 0)), Create(drop2), run_time=0.7)
            self.play(FadeIn(val2, shift=DOWN * 0.1), run_time=0.3)
            self.play(TransformFromCopy(val2, ans2[1]), FadeIn(ans2[0]), run_time=0.6)

            vo.wait_until("Subtract as before")
            self.play(TransformFromCopy(ans2[1], diff[0]), TransformFromCopy(ans1[1], diff[2]),
                      FadeIn(diff[1]), run_time=0.9)
            self.play(Write(diff[3:]), run_time=0.5)
            vo.wait_until("Alice seems")
            arrow = CurvedArrow(diff.get_right() + RIGHT * 0.12, alice_lab.get_right() + RIGHT * 0.1,
                                angle=1.1, color=ALICE, stroke_width=4, tip_length=0.18)
            self.play(Create(arrow), run_time=0.8)
            self.play(Indicate(diff[4], color=ALICE), run_time=0.7)
            cross = strike(Square(0.42).move_to(arrow.point_from_proportion(0.5)), pad=0.0)
            self.play(Create(cross), run_time=0.5)

            vo.wait_until("A fifty-fifty")
            self.add(needle)
            self.play(Create(meter), FadeIn(m_ticks), FadeIn(m_labs), FadeIn(band), FadeIn(needle),
                      FadeIn(m_head[:2]), run_time=0.8)
            self.play(p_track.animate.set_value(POST_MAX), FadeIn(m_head[2:]), run_time=1.5)
            self.play(Flash([mx(POST_MAX), m_y, 0], color=EPS_COLOR, flash_radius=0.3), run_time=0.6)
            self.play(Indicate(m_head[3], color=EPS_COLOR, scale_factor=1.08), run_time=vo.remaining(0.6))
        needle.clear_updaters()

        self.hosp = VGroup(icons, db_label, legend, card, alice_lab, ans1, ans2, diff, arrow, cross)
        self.plot = VGroup(ax, out_lab, pdf_a, area_a, stem_a, lab_a, pdf_b, area_b, stem_b, lab_b,
                           dot1, drop1, val1, dot2, drop2, val2)
        self.meter = VGroup(meter, m_ticks, m_labs, band, needle, m_head)
        self.top = VGroup(eps_eq, implies, scale_eq)
        self.scale_eq = scale_eq

    # ============================================================ 1. what the scale depends on
    def depends_beat(self):
        se = self.scale_eq
        keep = VGroup(se[0], se[1], se[2])
        target = keep.copy().scale(1.7).move_to(UP * 0.5 + LEFT * 1.2)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(self.hosp), FadeOut(self.plot), FadeOut(self.meter),
                      FadeOut(VGroup(self.top[0], self.top[1], se[3:])), run_time=0.8)
            self.play(Transform(keep, target), run_time=1.0)
            frac = keep[2]
            c_s = Ellipse(width=frac[0:4].width + 0.45, height=frac[0:4].height + 0.22, color=SENS_COLOR,
                          stroke_width=4).move_to(frac[0:4]).shift(UP * 0.05)
            c_e = Circle(radius=frac[5].height * 0.6 + 0.1, color=EPS_COLOR, stroke_width=4).move_to(frac[5])
            c_e.shift(DOWN * 0.04)
            l_s = S.text("sensitivity", 28, SENS_COLOR).next_to(c_s, UP, buff=0.2)
            l_e = S.text("privacy level", 28, EPS_COLOR).next_to(c_e, DOWN, buff=0.2)
            vo.wait_until("the sensitivity")
            self.play(Create(c_s), FadeIn(l_s, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("and epsilon")
            self.play(Create(c_e), FadeIn(l_e, shift=UP * 0.15), run_time=0.7)
            n_tok = S.math("n", size=96, color=S.GREY).next_to(keep, RIGHT, buff=1.6)
            n_lab = S.text("database size", 26, S.GREY).next_to(n_tok, DOWN, buff=0.3)
            n_x = strike(n_tok, width=7, pad=0.15)
            vo.wait_until("Not the size")
            self.play(FadeIn(n_tok, scale=1.2), FadeIn(n_lab), run_time=0.5)
            self.play(Create(n_x), run_time=vo.remaining(0.5))
        self.play(FadeOut(VGroup(keep, c_s, c_e, l_s, l_e, n_tok, n_lab, n_x)), run_time=0.6)

    # ============================================================ 2. same noise, any n
    def populations_beat(self):
        x0, length = -3.4, 6.4
        rows_spec = [(100, "100", "50", "≈ 4%", 2.25), (10_000, "10,000", "5,000", "≈ 0.04%", 0.95),
                     (1_000_000, "1,000,000", "500,000", "≈ 0.0004%", -0.35)]
        rows = []
        for n, n_s, mid_s, pct, y in rows_spec:
            line = Line([x0, y, 0], [x0 + length, y, 0], color=S.GREY, stroke_width=3)
            ticks = VGroup(*[Line([x0 + length * p, y - 0.1, 0], [x0 + length * p, y + 0.1, 0], color=S.GREY,
                                  stroke_width=2) for p in (0, 1)])
            truth = Line([x0 + length / 2, y - 0.16, 0], [x0 + length / 2, y + 0.16, 0], color=S.WHITE,
                         stroke_width=4)
            labs = VGroup(S.text("0", 20, S.GREY).next_to([x0, y, 0], DOWN, buff=0.22),
                          S.text(mid_s, 20, S.WHITE).next_to([x0 + length / 2, y, 0], DOWN, buff=0.22),
                          S.text(n_s, 20, S.GREY).next_to([x0 + length, y, 0], DOWN, buff=0.22))
            name = S.math(r"n = " + n_s.replace(",", "{,}"), size=32).next_to([x0 - 0.35, y, 0], LEFT, buff=0)
            bump = bump_shape(x0 + length / 2, length / n, LAM, 0.6, y, half_width=14)
            p_lab = S.text(pct, 28, NOISE_COLOR).next_to([x0 + length + 0.4, y, 0], RIGHT, buff=0)
            rows.append(dict(line=line, ticks=ticks, truth=truth, labs=labs, name=name, bump=bump, pct=p_lab))
        legend = VGroup(bump_shape(0, 0.04, LAM, 0.32, 0, half_width=12),
                        S.text("noise of typical size 2, the same in every row", 26, S.GREY))
        legend.arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.45)
        pct_head = S.text("noise ÷ answer", 20, S.GREY).next_to(rows[0]["pct"], UP, buff=0.35)
        pct_head.align_to(rows[0]["pct"], LEFT)

        # zoom inset on the million-row line
        r3 = rows[2]
        zx, zy = x0 + length / 2, r3["line"].get_y()
        lens = Circle(radius=0.26, color=S.WHITE, stroke_width=2).move_to([zx, zy + 0.25, 0])
        inset = RoundedRectangle(width=7.0, height=2.25, corner_radius=0.15, stroke_color=S.GREY,
                                 stroke_width=2).set_fill(S.BG, 1).move_to([zx, -2.4, 0])
        cone = VGroup(Line(lens.point_at_angle(PI * 1.15), inset.get_corner(UL) + RIGHT * 0.15, color=S.GREY,
                           stroke_width=1.5),
                      Line(lens.point_at_angle(-PI * 0.15), inset.get_corner(UR) + LEFT * 0.15, color=S.GREY,
                           stroke_width=1.5))
        z_half, z_len, z_y = 6.0, 6.2, -3.05
        z_upd = z_len / (2 * z_half)          # screen units per count

        def zpx(v):                            # v = count - 500,000
            return zx + v * z_upd

        z_axis = Line([zpx(-z_half), z_y, 0], [zpx(z_half), z_y, 0], color=S.GREY, stroke_width=2)
        z_ticks = VGroup(*[Line([zpx(v), z_y - 0.07, 0], [zpx(v), z_y + 0.07, 0], color=S.GREY, stroke_width=2)
                           for v in range(-5, 6)])
        z_labs = VGroup(*[S.text(s, 20, S.GREY).next_to([zpx(v), z_y, 0], DOWN, buff=0.12)
                          for s, v in (("499,995", -5), ("500,000", 0), ("500,005", 5))])
        z_bump = bump_shape(zpx(0), z_upd, LAM, 1.25, z_y, half_width=z_half)
        alice_seg = Line([zpx(0), z_y + 0.04, 0], [zpx(1), z_y + 0.04, 0], color=ALICE, stroke_width=9)
        alice_lab = S.text("Alice's row: 1", 22, ALICE).move_to([zpx(3.8), z_y + 0.95, 0])
        alice_ptr = Line(alice_lab.get_bottom() + DOWN * 0.05 + LEFT * 0.5, alice_seg.get_center() + UP * 0.08,
                         color=ALICE, stroke_width=2)
        noise_lab = S.text("noise ≈ 2", 22, NOISE_COLOR).move_to([zpx(-3.9), z_y + 0.95, 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(legend, shift=DOWN * 0.2), run_time=0.6)
            r = rows[0]
            self.play(FadeIn(r["name"]), Create(r["line"]), FadeIn(r["ticks"]), run_time=0.8)
            self.play(FadeIn(r["truth"]), FadeIn(r["labs"]), run_time=0.5)
            self.play(TransformFromCopy(legend[0], r["bump"]), run_time=0.9)
            vo.wait_until("is a few percent")
            self.play(FadeIn(pct_head), FadeIn(r["pct"], shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("With a million")
            for prev, cur in ((rows[0], rows[1]), (rows[1], rows[2])):
                geo = lambda r: VGroup(r["line"], r["ticks"], r["truth"])
                self.play(TransformFromCopy(geo(prev), geo(cur)), TransformFromCopy(prev["bump"], cur["bump"]),
                          FadeIn(cur["labs"], shift=DOWN * 0.3), FadeIn(cur["name"], shift=DOWN * 0.3),
                          run_time=0.8)
                self.play(FadeIn(cur["pct"], shift=LEFT * 0.2), run_time=0.35)
            vo.wait_until("Alice is protected")
            self.play(Create(lens), run_time=0.4)
            self.play(Create(cone), FadeIn(inset), run_time=0.6)
            self.play(Create(z_axis), FadeIn(z_ticks), FadeIn(z_labs), run_time=0.6)
            self.play(GrowFromEdge(z_bump, DOWN), FadeIn(noise_lab), run_time=0.9)
            vo.wait_until("her own contribution")
            self.play(Create(alice_seg), FadeIn(alice_lab), Create(alice_ptr), run_time=0.8)
            vo.wait_until("but tiny compared")
            self.play(Indicate(r3["line"], color=S.WHITE, scale_factor=1.02), Indicate(r3["pct"], color=S.WHITE),
                      run_time=vo.remaining(0.8))
        self.wait(0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)

    # ============================================================ 3. the slogan
    def slogan_beat(self):
        l1 = S.text("Privacy for individuals.", 50, S.WHITE)
        l2 = S.text("Accuracy for populations.", 50, S.WHITE)
        i1 = person_icon(ALICE, 0.85)
        i2 = person_grid(16, cols=4, color=S.GREY, height=0.2, buff=0.06)
        row1 = VGroup(i1, l1).arrange(RIGHT, buff=0.5)
        row2 = VGroup(i2, l2).arrange(RIGHT, buff=0.5)
        rows = VGroup(row1, row2).arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to(ORIGIN)
        i1.set_x(i2.get_x())
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(i1, scale=0.6), Write(l1), run_time=1.3)
            vo.wait_until("Accuracy for")
            self.play(FadeIn(i2, lag_ratio=0.05), Write(l2), run_time=1.3)
            vo.wait_until("That is the bargain")
            self.play(Circumscribe(rows, color=S.WHITE, buff=0.3), run_time=vo.remaining(0.8))
        self.slogan = rows

    # ============================================================ 4-5. epsilon << 1/n, hybrid argument
    def tiny_eps_beats(self):
        n_data = 100
        x0, length, y = -2.5, 5.0, -0.6       # built mid-frame, dropped to Y_LOW for the ponder card
        y_low = -2.75
        upd = length / n_data                # screen units per count

        def px(v):
            return x0 + v * upd

        ext = DashedLine([-6.6, y, 0], [6.6, y, 0], color=S.GREY, stroke_width=2, dash_length=0.12)
        seg = Line([px(0), y, 0], [px(n_data), y, 0], color=S.GREY, stroke_width=4)
        ticks = VGroup(*[Line([px(v), y - 0.1, 0], [px(v), y + 0.1, 0], color=S.GREY, stroke_width=2)
                         for v in (0, n_data)])
        truth = Line([px(50), y - 0.16, 0], [px(50), y + 0.16, 0], color=S.WHITE, stroke_width=4)
        labs = VGroup(S.math("0", size=30, color=S.GREY).next_to([px(0), y, 0], DOWN, buff=0.2),
                      S.text("true count", 20, S.WHITE).next_to([px(50), y, 0], DOWN, buff=0.22),
                      S.math("n", size=32, color=S.GREY).next_to([px(n_data), y, 0], DOWN, buff=0.2))
        lam = ValueTracker(LAM)

        def make_bump():
            return bump_shape(px(50), upd, lam.get_value(), 0.9, y_low,
                              half_width=max(14.0, 7 * lam.get_value()))

        bump0 = make_bump().shift(UP * (y - y_low))
        n_lab = S.math(r"\text{noise} \approx", r"\frac{1}{\varepsilon}", size=36)
        n_lab[0].set_color(NOISE_COLOR)
        n_lab[1][2].set_color(EPS_COLOR)
        n_lab.next_to([px(50), y + 0.9, 0], UP, buff=0.2)
        line_grp = VGroup(ext, seg, ticks, truth, labs)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(self.slogan), run_time=0.6)
            self.play(Create(ext), Create(seg), FadeIn(ticks), FadeIn(truth), FadeIn(labs), run_time=1.0)
            vo.wait_until("the noise has size")
            self.play(GrowFromEdge(bump0, DOWN), run_time=0.6)
            self.play(Write(n_lab), run_time=0.9)
            vo.wait_until("What goes wrong")
            self.play(Indicate(n_lab[1], color=EPS_COLOR), run_time=1.0)
            self.play(VGroup(line_grp, bump0, n_lab).animate.shift(DOWN * (y - y_low)), run_time=vo.remaining(0.6))
        card = ponder_at(self, "Noise ≈ 1/ε.\nWhat goes wrong if ε is much smaller than 1/n?", seconds=12,
                         pos=UP * 1.45, width=10.0)

        # ---- 5a. the noise outgrows n
        rng = np.random.default_rng(8)
        draws = [int(round(50 + v)) for v in rng.laplace(0, 1000, 5)]
        eps_dn = DecimalNumber(EPS, num_decimal_places=3, font_size=36, color=EPS_COLOR)
        eps_dn.add_updater(lambda m: m.set_value(1 / lam.get_value()))
        noise_dn = Integer(2, font_size=36, color=NOISE_COLOR, group_with_commas=True)
        noise_dn.add_updater(lambda m: m.set_value(int(round(lam.get_value()))))
        # the "<<" is only revealed once epsilon has actually dropped to 0.001 (while it sweeps
        # down from 0.5 the relation would be false)
        rel_sym = S.math(r"\ll", size=36, color=S.GREY)
        r_eps = VGroup(S.math(r"\varepsilon =", size=36, color=EPS_COLOR), eps_dn, rel_sym,
                       S.math(r"\tfrac{1}{n} = 0.01", size=36, color=S.GREY)).arrange(RIGHT, buff=0.18)
        r_eps[3].shift(RIGHT * 0.05)
        r_noise = VGroup(S.math(r"\text{noise} \approx", size=36, color=NOISE_COLOR), noise_dn).arrange(RIGHT, buff=0.18)
        readouts = VGroup(r_eps, r_noise).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0, 1.9, 0])
        rel_head = S.text("released:", 28, S.GREY)
        rel_val = S.math(f"{draws[0]:,}".replace(",", "{,}"), size=40)
        rel = VGroup(rel_head, rel_val).arrange(RIGHT, buff=0.25).next_to(readouts, DOWN, buff=0.5)
        rel.set_x(0)
        pure = S.text("pure noise", 30, NOISE_COLOR).next_to(rel, DOWN, buff=0.35)

        with self.voiceover(SAY[5]) as vo:
            rel_sym.set_opacity(0)
            self.play(FadeOut(card), FadeOut(n_lab), FadeIn(readouts), run_time=0.6)
            self.remove(bump0)
            bump = always_redraw(make_bump)
            self.add(bump)
            self.play(lam.animate(rate_func=lambda t: t ** 3).set_value(1000), run_time=2.4)
            eps_dn.clear_updaters()
            noise_dn.clear_updaters()
            bump.clear_updaters()
            self.play(rel_sym.animate.set_opacity(1), FadeIn(rel, shift=UP * 0.15), run_time=0.4)
            for d in draws[1:4]:
                new = S.math(f"{d:,}".replace(",", "{,}"), size=40).move_to(rel_val, aligned_edge=LEFT)
                self.play(Transform(rel_val, new), run_time=0.3)
            self.play(FadeIn(pure, scale=1.2), run_time=0.4)

            # ---- 5b. not Laplace's fault: the chain
            # the noise picture stays up while the narrator says it is not Laplace's fault, so
            # "pure noise" stays readable; it clears when the chain starts
            vo.wait_until("This is not")
            not_lap = S.text("Not Laplace's fault: this holds for any ε-private mechanism M", 30, S.GREY)
            not_lap.to_edge(UP, buff=0.5)
            noise_pic = VGroup(readouts, rel, pure, line_grp, bump)
            self.play(FadeIn(not_lap, shift=DOWN * 0.2), run_time=0.8)

            chain = hybrid_chain().move_to(UP * 1.35)
            nodes, arrows, steps, names = chain
            vo.wait_until("Any two databases")
            self.play(FadeOut(noise_pic), run_time=0.4)
            self.play(FadeIn(nodes[0], shift=RIGHT * 0.2), FadeIn(names[0]),
                      FadeIn(nodes[-1], shift=LEFT * 0.2), FadeIn(names[-1]), run_time=0.8)
            vo.wait_until("linked by a chain")
            seq = []
            for k in range(1, len(nodes) - 1):
                seq.append(AnimationGroup(GrowArrow(arrows[k - 1]), FadeIn(nodes[k], shift=RIGHT * 0.2),
                                          FadeIn(names[k])))
            seq.append(GrowArrow(arrows[-1]))
            self.play(LaggedStart(*seq, lag_ratio=0.6), run_time=2.6)
            # flash the single changed row in each step
            new_rows = [nodes[k][1][k - 1][0] for k in (1, 2)] + [nodes[-1][1][-1][0]]
            self.play(LaggedStart(*[Indicate(r, color=ALICE, scale_factor=1.15) for r in new_rows],
                                  lag_ratio=0.3), run_time=1.2)
            vo.wait_until("each changing probabilities")
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.15) for s in steps], lag_ratio=0.25), run_time=1.3)

            brace = Brace(VGroup(names, nodes), DOWN, buff=0.2, color=S.GREY)
            b_lab = S.math(r"n \text{ steps:}\quad", r"e^{\varepsilon}\cdot e^{\varepsilon}\cdots e^{\varepsilon}",
                           r"=", r"e^{n\varepsilon}", size=38)
            b_lab[1].set_color(EPS_COLOR)
            b_lab[3].set_color(EPS_COLOR)
            b_lab.next_to(brace, DOWN, buff=0.2)
            ends = S.math(r"\Pr[M(", "x", r")=t]", r"\;\le\;", r"e^{n\varepsilon}", r"\cdot", r"\Pr[M(", "y",
                          r")=t]", size=48)
            ends[1].set_color(X_COLOR)
            ends[4].set_color(EPS_COLOR)
            ends.next_to(b_lab, DOWN, buff=0.55)
            vo.wait_until("so the ends")
            self.play(GrowFromCenter(brace), FadeIn(b_lab), run_time=0.9)
            self.play(Write(ends), run_time=1.2)

            vo.wait_until("If n epsilon")
            approx = S.math(r"\Pr[M(", "x", r")=t]", r"\;\approx\;", r"\Pr[M(", "y", r")=t]", size=48)
            approx[1].set_color(X_COLOR)
            approx.move_to(ends)
            cond = S.math(r"n\varepsilon \ll 1", r"\;\Rightarrow\;", r"e^{n\varepsilon} \approx 1", size=38)
            cond[0][1].set_color(EPS_COLOR)
            cond[2][0:3].set_color(EPS_COLOR)
            cond.move_to(b_lab)
            self.play(ReplacementTransform(b_lab, cond), run_time=0.8)
            self.play(TransformMatchingTex(ends, approx), run_time=1.0)
            vo.wait_until("every database looks alike")
            alike = S.text("all databases look alike  ⇒  nothing can be learned", 34, S.WHITE)
            alike.next_to(approx, DOWN, buff=0.55)
            # pulse the frames together ("they all look alike"); Indicate on a whole mini database
            # would paint its filled rows white
            frames = VGroup(*[nd[0] for nd in nodes if isinstance(nd, VGroup) and len(nd) == 2])
            self.play(LaggedStart(*[Indicate(f, color=S.WHITE, scale_factor=1.06) for f in frames],
                                  lag_ratio=0.12), run_time=1.0)
            self.play(FadeIn(alike, shift=UP * 0.15), run_time=0.7)

            vo.wait_until("This chain trick")
            tag_txt = S.text("hybrid argument", 34, S.WHITE, weight="BOLD")
            tag = VGroup(RoundedRectangle(width=tag_txt.width + 0.6, height=tag_txt.height + 0.4, corner_radius=0.12,
                                          stroke_color=S.WHITE, stroke_width=2.5).set_fill(S.GREY_DARKER, 1),
                         tag_txt)
            tag.to_edge(UP, buff=0.45)
            self.play(FadeOut(not_lap, shift=UP * 0.2), FadeIn(tag, shift=UP * 0.2), run_time=0.8)
            self.play(Indicate(tag[1], color=S.WHITE, scale_factor=1.12), run_time=1.0)
            self.play(LaggedStart(*[Indicate(a, color=S.WHITE, scale_factor=1.15) for a in arrows], lag_ratio=0.2),
                      run_time=vo.remaining(1.0))
        self.wait(0.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
