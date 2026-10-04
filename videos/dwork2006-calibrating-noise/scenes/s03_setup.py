"""S03 · The setup: a trusted curator answers queries with f(x) + noise (§2, p. 269–270)."""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import database_rows, person_icon
from explainer.scene import VoiceScene

from common import ALICE, ANALYST_COLOR, NARRATION, NOISE_COLOR, SENS_COLOR, TRUTH_COLOR, X_COLOR

SAY = NARRATION["S03"]

CURATOR = S.WHITE       # the curator knows the true answer (true answer = WHITE)
NAMES = ["Bob", "Carol", "Alice", "Dan", "Eve"]
VALUES = ["no X", "has X", "no X", "no X", "has X"]
ALICE_ROW = 2


# ---------------------------------------------------------------- small glyphs


def db_stack(frame_color, alice_value="no X", width=2.8, row_h=0.44, size=22) -> VGroup:
    """Row stack in the video's database style. Returns VGroup(frame, rows, alice_hl, vdots)."""
    vals = list(VALUES)
    vals[ALICE_ROW] = alice_value
    rows = database_rows(NAMES, vals, color=S.GREY, width=width, row_height=row_h, size=size)
    for r in rows:
        r[3].set_color(S.GREY).align_to(r[0], RIGHT).shift(LEFT * 0.18)
    a = rows[ALICE_ROW]
    a[0].set_fill(interpolate_color(ManimColor(S.GREY_DARKER), ManimColor(ALICE), 0.16), 1)
    a[1].set_fill(ALICE, 1)
    a[2].set_color(ALICE)
    a[3].set_color(ALICE)
    hl = Rectangle(width=a[0].width, height=a[0].height, stroke_color=ALICE, stroke_width=3).move_to(a[0])
    dots = S.math(r"\vdots", size=30, color=S.GREY).next_to(rows, DOWN, buff=0.1)
    frame = SurroundingRectangle(VGroup(rows, dots), color=frame_color, buff=0.14, corner_radius=0.1,
                                 stroke_width=3)
    return VGroup(frame, rows, hl, dots)


def lock_icon(color=S.GREY, height=0.42) -> VGroup:
    body = RoundedRectangle(width=0.34, height=0.26, corner_radius=0.05, stroke_width=0).set_fill(color, 1)
    arc = Arc(radius=0.11, start_angle=0, angle=PI, stroke_color=color, stroke_width=4)
    legs = VGroup(Line(arc.get_start(), arc.get_start() + DOWN * 0.07),
                  Line(arc.get_end(), arc.get_end() + DOWN * 0.07)).set_stroke(color, 4)
    shackle = VGroup(arc, legs).next_to(body, UP, buff=-0.02)
    hole = Dot(radius=0.035, color=S.BG).move_to(body)
    g = VGroup(shackle, body, hole)
    g.scale_to_fit_height(height)
    return g


def noise_blob(radius=0.42) -> VGroup:
    """A wobbly RED blob labelled Y: 'random noise'. Returns VGroup(blob, Y)."""
    ang = np.linspace(0, TAU, 48, endpoint=False)
    rr = radius * (1 + 0.14 * np.sin(3 * ang + 0.4) + 0.07 * np.cos(5 * ang + 1.3))
    pts = [np.array([r * np.cos(a), r * np.sin(a), 0.0]) for r, a in zip(rr, ang)]
    blob = VMobject().set_points_smoothly(pts + [pts[0]])
    blob.set_fill(NOISE_COLOR, 0.22).set_stroke(NOISE_COLOR, 3)
    y = S.math("Y", size=40, color=NOISE_COLOR).move_to(blob)
    return VGroup(blob, y)


def table_icon(color=S.GREY, width=1.0, height=0.72, rows=4, cols=3) -> VGroup:
    cells = VGroup(*[Rectangle(width=width / cols, height=height / rows, stroke_color=color,
                               stroke_width=2, stroke_opacity=0.7, fill_opacity=0)
                     for _ in range(rows * cols)])
    cells.arrange_in_grid(rows=rows, cols=cols, buff=0)
    for c in cells[:cols]:
        c.set_fill(color, 0.35)
    return cells


def smooth_pdf(t, mu, lam):
    """A smooth bell (logistic, scale lam/2: same peak height 1/(2 lam) as Laplace(lam)).

    Deliberately not the Laplace density: which distribution Y should have is the question this
    scene asks, and the Laplace kink is S07's reveal (S04 pictures smooth curves too)."""
    s = lam / 2
    z = (np.asarray(t, dtype=float) - mu) / (2 * s)
    return 1.0 / (4 * s) / np.cosh(z) ** 2


def answer_token(sub: str = "", size=30) -> MathTex:
    """'f(x) + Y' (f(x) WHITE, Y RED); with sub='2' -> 'f_2(x) + Y_2'."""
    f = rf"f_{sub}(x)" if sub else "f(x)"
    y = rf"Y_{sub}" if sub else "Y"
    m = S.math(f, "+", y, size=size)
    m[0].set_color(TRUTH_COLOR)
    m[2].set_color(NOISE_COLOR)
    return m


class Curator(VoiceScene):
    def construct(self):
        # ============================================================ 0. curator, database, analyst
        boundary_shape = RoundedRectangle(width=7.0, height=4.4, corner_radius=0.3).move_to([-2.75, 0.35, 0])
        boundary = DashedVMobject(boundary_shape.set_stroke(S.GREY, 2), num_dashes=70)
        boundary_lab = S.text("trusted server", 22, S.GREY).next_to(boundary_shape, UP, buff=0.12)
        boundary_lab.align_to(boundary_shape, LEFT).shift(RIGHT * 0.2)

        db = db_stack(X_COLOR).move_to([-4.5, 0.2, 0])
        db_frame, db_rows, db_hl, db_dots = db
        db_lab = VGroup(S.text("database", 28, X_COLOR), S.math("x", size=40, color=X_COLOR))
        db_lab.arrange(RIGHT, buff=0.15, aligned_edge=DOWN).next_to(db_frame, UP, buff=0.14)
        n_cap = S.text("n rows, one per person", 22, S.GREY).next_to(db_frame, DOWN, buff=0.14)

        curator = person_icon(CURATOR, height=0.85).move_to([-1.25, 1.45, 0])
        curator_lab = S.text("curator", 26, CURATOR).next_to(curator, DOWN, buff=0.12)

        analyst = person_icon(ANALYST_COLOR, height=0.9).move_to([5.7, 0.5, 0])
        analyst_lab = S.text("analyst", 26, ANALYST_COLOR).next_to(analyst, DOWN, buff=0.12)

        q_arrow = Arrow([5.0, 1.35, 0], [-0.55, 1.35, 0], buff=0, color=S.GREY, stroke_width=4,
                        max_tip_length_to_length_ratio=0.05, tip_length=0.22)
        q_lab = VGroup(S.text("query", 26, S.WHITE), S.math("f", size=40))
        q_lab.arrange(RIGHT, buff=0.15, aligned_edge=DOWN).next_to(q_arrow, UP, buff=0.12).set_x(2.3)
        ex1 = VGroup(S.text("a number:", 22, S.GREY), S.math(r"f(x) = 41", size=30))
        ex1.arrange(RIGHT, buff=0.18)
        ex2 = VGroup(S.text("a list:", 22, S.GREY), S.math(r"f(x) = (12,\, 7,\, 30,\, 2)", size=30))
        ex2.arrange(RIGHT, buff=0.18)
        # left-aligned, clear of both the dashed boundary (x = 0.75) and the analyst (x >= 5.3)
        VGroup(ex1, ex2).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([1.15, 0.45, 0], aligned_edge=LEFT)

        with self.voiceover(SAY[0]) as vo:
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in db_rows], lag_ratio=0.15),
                      FadeIn(db_dots), FadeIn(db_hl), run_time=1.3)
            vo.wait_until("A trusted server")
            self.play(FadeIn(curator, shift=DOWN * 0.2), FadeIn(curator_lab), run_time=0.7)
            self.play(Create(boundary), FadeIn(boundary_lab), run_time=1.0)
            vo.wait_until("holds a database")
            self.play(Create(db_frame), FadeIn(db_lab, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("n rows")
            self.play(FadeIn(n_cap),
                      LaggedStart(*[Indicate(r[1], scale_factor=1.3, color=S.WHITE) for r in db_rows],
                                  lag_ratio=0.12), run_time=1.1)
            vo.wait_until("An analyst sends")
            self.play(FadeIn(analyst, shift=LEFT * 0.4), FadeIn(analyst_lab), run_time=0.6)
            self.play(GrowArrow(q_arrow), FadeIn(q_lab, shift=LEFT * 0.3), run_time=0.9)
            vo.wait_until("any function")
            self.play(FadeIn(ex1, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("or a list")
            self.play(FadeIn(ex2, shift=UP * 0.15), run_time=0.6)

        # ============================================================ 1. f(x) stays locked; f(x) + Y leaves
        fx = S.math("f(x)", size=42, color=TRUTH_COLOR).move_to([-1.45, -0.45, 0])
        lock = lock_icon(S.GREY, 0.42).next_to(fx, RIGHT, buff=0.2)
        blob = noise_blob(0.36).move_to([-1.2, -1.3, 0])
        a_arrow = Arrow([0.1, -0.45, 0], [5.0, -0.45, 0], buff=0, color=S.GREY, stroke_width=4,
                        max_tip_length_to_length_ratio=0.05, tip_length=0.22)
        out_spot = np.array([2.05, -0.45 + 0.42, 0])     # just outside the trusted boundary
        tok = answer_token().move_to(out_spot)
        inbox_top = analyst_lab.get_bottom() + DOWN * 0.3
        received = VGroup()

        def deliver(token):
            """Move an answer token along the answer arrow into the analyst's growing column."""
            spot = inbox_top + DOWN * (0.42 * len(received) + 0.15)
            received.add(token)
            return token.animate.scale(0.85).move_to(spot)

        inter = VGroup(S.math(r"\circlearrowleft", size=38, color=S.WHITE),
                       S.text("interactive: ask, answer, repeat", 24, S.WHITE)).arrange(RIGHT, buff=0.15)
        inter.move_to([2.75, -2.8, 0])
        table = table_icon(S.GREY)
        table_lab = S.text("non-interactive: publish once", 24, S.GREY)
        pub = VGroup(table, table_lab).arrange(RIGHT, buff=0.25).move_to([-3.75, -2.8, 0])
        gg = S.math(r"\ll", size=48, color=S.WHITE)
        sec4 = S.text("proved in Section 4", 20, S.GREY)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(ex1, ex2)), run_time=0.4)
            self.play(TransformFromCopy(VGroup(*[r[3] for r in db_rows]), fx), run_time=1.2)
            self.play(FadeIn(lock, scale=1.6), run_time=0.5)
            self.play(Wiggle(lock, scale_value=1.15), run_time=0.7)
            vo.wait_until("Instead it draws")
            self.play(GrowFromCenter(blob), run_time=0.7)
            self.play(Rotate(blob[0], angle=PI / 3), run_time=0.7)
            vo.wait_until("and releases")
            self.play(GrowArrow(a_arrow), run_time=0.5)
            self.play(TransformFromCopy(fx, tok[0]), FadeIn(tok[1]), TransformFromCopy(blob[1], tok[2]),
                      run_time=0.8)
            self.play(deliver(tok), run_time=0.9)

            vo.wait_until("Because the analyst")
            for k, rt in (("2", 0.6), ("3", 0.5)):
                # the new query travels just under the arrow, clear of its "query f" label
                q = S.math(f"f_{k}", size=34).next_to(q_arrow.get_start(), DOWN, buff=0.14).shift(LEFT * 0.4)
                self.play(FadeIn(q, scale=0.6), run_time=0.25)
                self.play(q.animate.move_to([q_arrow.get_end()[0] + 0.4, q.get_y(), 0]), run_time=rt)
                ans = answer_token(k).move_to(out_spot)
                self.play(FadeOut(q, scale=0.5), Rotate(blob[0], angle=PI / 2),
                          FadeIn(ans, shift=RIGHT * 0.2), run_time=0.4)
                self.play(deliver(ans), run_time=rt)
            self.play(FadeIn(inter, shift=UP * 0.15), run_time=0.6)

            vo.wait_until("The alternative")
            self.play(TransformFromCopy(db_frame, table), run_time=1.0)
            self.play(FadeIn(table_lab, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("and walking away")
            self.play(curator.animate.set_opacity(0.25), curator_lab.animate.set_opacity(0.25), run_time=0.8)
            vo.wait_until("At the end")
            gg.move_to([(pub.get_right()[0] + inter.get_left()[0]) / 2, -2.8, 0])
            sec4.next_to(gg, DOWN, buff=0.1)
            self.play(curator.animate.set_opacity(1), curator_lab.animate.set_opacity(1),
                      FadeIn(gg, scale=1.4), FadeIn(sec4), run_time=0.8)
            self.play(Indicate(inter, color=S.WHITE, scale_factor=1.08), run_time=1.0)

        # ============================================================ 2. how much noise?
        keep_blob = blob
        others = [m for m in self.mobjects if m is not keep_blob]
        y_q = VGroup(S.math(r"\sim", size=60), S.math("?", size=60, color=S.WHITE))

        # dial: needle angle follows a log-scaled noise level u in [0, 1]
        pivot = np.array([-3.35, -0.75, 0.0])
        R = 1.85
        u = ValueTracker(0.5)

        def lam_of(v):  # 0 -> 0.6 (tiny noise), 0.5 -> 2, 1 -> 30 (huge noise)
            return 0.6 * (2 / 0.6) ** (2 * v) if v <= 0.5 else 2.0 * 15.0 ** (2 * v - 1)

        def unit(a):
            return np.array([np.cos(a), np.sin(a), 0.0])

        arc = Arc(radius=R, start_angle=0, angle=PI, arc_center=pivot, stroke_color=S.GREY_DARK,
                  stroke_width=16)
        ticks = VGroup(*[Line(pivot + (R - 0.28) * unit(a), pivot + (R - 0.08) * unit(a), color=S.GREY,
                              stroke_width=2) for a in np.linspace(0, PI, 9)])
        needle = always_redraw(lambda: Line(pivot, pivot + (R - 0.35) * unit(PI * (1 - u.get_value())),
                                            color=NOISE_COLOR, stroke_width=7))
        hub = Dot(pivot, radius=0.09, color=NOISE_COLOR)
        dial_lab = S.text("noise", 30, NOISE_COLOR).next_to(pivot, DOWN, buff=0.22)
        left_lab = VGroup(S.text("too little", 24, S.WHITE), S.text("Alice exposed", 24, ALICE))
        left_lab.arrange(DOWN, buff=0.08).next_to(pivot + LEFT * R, DOWN, buff=0.22)
        right_lab = VGroup(S.text("too much", 24, S.WHITE), S.text("useless", 24, S.GREY))
        right_lab.arrange(DOWN, buff=0.08).next_to(pivot + RIGHT * R, DOWN, buff=0.22)
        dial = VGroup(arc, ticks, hub, dial_lab, left_lab, right_lab)

        ax = Axes(x_range=[21, 61, 10], y_range=[0, 0.85, 0.85], x_length=5.6, y_length=2.6, tips=False,
                  axis_config={"color": S.GREY, "stroke_width": 2},
                  y_axis_config={"include_ticks": False}).move_to([3.55, -0.35, 0])
        ax_lab = VGroup(S.text("released answer", 22, S.GREY), answer_token(size=30).set_opacity(0.8))
        ax_lab.arrange(RIGHT, buff=0.2).next_to(ax.x_axis, DOWN, buff=0.5)
        truth_tick = Line(ax.c2p(41, 0) + DOWN * 0.12, ax.c2p(41, 0) + UP * 0.12, color=TRUTH_COLOR,
                          stroke_width=3)
        truth_lab = S.math("f(x)", size=28, color=TRUTH_COLOR).next_to(truth_tick, DOWN, buff=0.08)
        curve = always_redraw(lambda: ax.plot(lambda t: smooth_pdf(t, 41, lam_of(u.get_value())),
                                              x_range=[21, 61, 0.04], color=NOISE_COLOR, stroke_width=4))
        phrase = S.text("Calibrate the noise to the sensitivity", 40, S.WHITE,
                        t2c={"noise": NOISE_COLOR, "sensitivity": SENS_COLOR}).move_to([0, -3.0, 0])
        private_q = VGroup(S.text("private", 64, S.YELLOW), S.math(r"=\ ?", size=72)).arrange(RIGHT, buff=0.3)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(Group(*others)), run_time=0.8)
            self.play(keep_blob.animate.scale(1.3).move_to([-0.6, 2.75, 0]), run_time=0.8)
            y_q.arrange(RIGHT, buff=0.25).next_to(keep_blob, RIGHT, buff=0.3)
            self.play(Write(y_q), run_time=0.7)
            self.play(Create(arc), FadeIn(ticks), FadeIn(dial_lab), run_time=0.9)
            self.add(needle)
            self.play(FadeIn(hub), Create(ax), FadeIn(ax_lab), FadeIn(truth_tick), FadeIn(truth_lab),
                      run_time=0.8)
            self.add(curve)
            self.play(FadeIn(left_lab), FadeIn(right_lab), run_time=0.6)
            vo.wait_until("Too little noise")
            self.play(u.animate.set_value(0.03), run_time=1.3)
            self.play(Indicate(left_lab[1], color=ALICE, scale_factor=1.2), run_time=0.8)
            vo.wait_until("Too much")
            self.play(u.animate.set_value(0.97), run_time=1.3)
            self.play(Indicate(right_lab[1], color=S.WHITE, scale_factor=1.2), run_time=0.7)
            vo.wait_until("The title gives")
            self.play(u.animate.set_value(0.5), run_time=1.2)
            vo.wait_until("calibrate the noise")
            self.play(Write(phrase), run_time=1.3)
            vo.wait_until("But first")
            needle.clear_updaters()
            curve.clear_updaters()
            self.play(FadeOut(VGroup(dial, needle, ax, ax_lab, truth_tick, truth_lab, curve, keep_blob, y_q)),
                      phrase.animate.set_opacity(0.35).shift(DOWN * 0.1), FadeIn(private_q, scale=0.8),
                      run_time=0.9)
            self.play(Indicate(private_q[0], color=S.YELLOW, scale_factor=1.08), run_time=vo.remaining(0.8))
        self.wait(0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
