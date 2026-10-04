"""S06 · Sensitivity [Def. 2, p. 271; Example 3, p. 271-272]."""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import database_rows, person_icon, ponder_card
from explainer.scene import VoiceScene

from common import ALICE, EPS_COLOR, NARRATION, SENS_COLOR, X_COLOR, XP_COLOR

SAY = NARRATION["S06"]

# ---------------------------------------------------------------- histogram geometry
H_LEFT, H_RIGHT = -6.3, -0.3     # x-extent of the histogram
H_BASE = -2.7                    # baseline y
H_MAX = 3.1                      # screen height of the tallest stack (Alice included) in every view
N_ROWS = 150                     # rows besides Alice: enough that even 60 bins read as a histogram
BAR_FILL = 0.55
# Alice's value in [0, 1): in B2 at d = 5, then B4 (her change), then her hops at d = 20 and d = 60
ALICE_U = (0.33, 0.67, 0.32, 0.74)


def db_stack(names, values, width=2.7, row_h=0.46, size=22):
    """Database row stack with a vertical-dots gap before the last row ("n rows").

    Returns (stack, rows, dots); rows[i] = VGroup(box, icon, name, value)."""
    rows = database_rows(names, values, color=S.GREY, width=width, row_height=row_h, size=size)
    rows[-1].shift(DOWN * row_h)
    dots = S.math(r"\vdots", size=28, color=S.GREY)
    dots.move_to((rows[-2].get_bottom() + rows[-1].get_top()) / 2)
    return VGroup(rows, dots), rows, dots


def style_row(row, changed: bool):
    """The one changed row is PINK (Alice's colour); the others are neutral."""
    row[0].set_stroke(ALICE if changed else S.GREY_DARK, 2.5 if changed else 1.5)
    row[1].set_fill(ALICE if changed else S.GREY, 1)
    row[2].set_color(ALICE if changed else S.WHITE)


def ponder_at(scene, question, seconds, width, pos, size=30):
    """Like pause_and_ponder, but placed at `pos` so a picture can stay visible beside it."""
    card = ponder_card(question, width=width, size=size).move_to(pos)
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return card


def bin_x(d, j):
    w = (H_RIGHT - H_LEFT) / d
    return H_LEFT + w * (j + 0.5), w


def bin_of(u, d):
    return min(int(u * d), d - 1)


def row_values(n=N_ROWS, mu=0.48, sd=0.28, floor=0.15):
    """Values in [0, 1) of the other rows (deterministic): the quantiles of a smooth bell on a low
    floor, so every histogram of them (5, 20 or 60 bins) has a smooth outline and no empty bins."""
    grid = np.linspace(0, 1, 20001)
    dens = np.exp(-0.5 * ((grid - mu) / sd) ** 2) + floor
    cdf = np.cumsum(dens)
    cdf = (cdf - cdf[0]) / (cdf[-1] - cdf[0])
    return np.interp((np.arange(n) + 0.5) / n, cdf, grid)


ROW_U = row_values()
COUNTS5 = [sum(bin_of(u, 5) == j for u in ROW_U) for j in range(5)]
# one row = one block; the vertical scale is set per view so the tallest stack is H_MAX high
# (an unlabelled count axis, rescaled as the bins get finer, like a density histogram)
UNIT = {d: H_MAX / (max(sum(bin_of(u, d) == j for u in ROW_U) for j in range(d)) + 1) for d in (5, 20, 60)}
STROKE = {5: 1.2, 20: 1.1, 60: 0.8}


def unit_block(d, j, k, color, opacity):
    """One row drawn as a unit block: the (k+1)-th block from the bottom of bin j of a d-bin histogram."""
    cx, w = bin_x(d, j)
    u = UNIT[d]
    b = Rectangle(width=w * 0.8, height=u, stroke_color=color, stroke_width=STROKE[d] + (0.5 if color == ALICE else 0))
    return b.set_fill(color, opacity).move_to([cx, H_BASE + (k + 0.5) * u, 0])


def layout(d, alice_u):
    """The same rows binned into d bins: (one block per other row, Alice's block on top of her bin, counts)."""
    counts = [0] * d
    blocks = []
    for u in ROW_U:
        j = bin_of(u, d)
        blocks.append(unit_block(d, j, counts[j], X_COLOR, BAR_FILL))
        counts[j] += 1
    ja = bin_of(alice_u, d)
    return blocks, unit_block(d, ja, counts[ja], ALICE, 0.95), counts


def hover(block):
    """Alice's icon hovering above her block, tethered to it."""
    icon = person_icon(ALICE, height=0.45).move_to(block.get_top() + UP * 0.75)
    name = S.text("Alice", 22, ALICE).next_to(icon, UP, buff=0.06)    # above: clear of the bars' labels
    tether = DashedLine(icon.get_bottom() + DOWN * 0.04, block.get_top(), color=ALICE, stroke_width=2,
                        dash_length=0.06)
    return VGroup(tether, icon, name)


def coin_roll(x0, x1, y, h=0.3, w=0.06, gap=0.012):
    """A row of gold coins seen edge-on, from x0 to x1."""
    g = VGroup()
    x = x0
    while x + w <= x1 + 1e-6:
        c = RoundedRectangle(width=w, height=h, corner_radius=0.02, stroke_color="#9C7426", stroke_width=1)
        c.set_fill(S.GOLD, 1).move_to([x + w / 2, y, 0])
        g.add(c)
        x += w + gap
    return g


def money(v):
    if v >= 1e9:
        return f"${v / 1e9:,.0f}B"
    if v >= 1e6:
        return f"${v / 1e6:,.0f}M"
    return f"${v / 1e3:,.0f}k"


class Sensitivity(VoiceScene):
    def construct(self):
        # ============================================================ 0. what is sensitivity?
        names = ["Bob", "Carol", "Dan", "Alice"]
        base_vals = ["no X", "has X", "no X", "no X"]
        stack, rows, dots = db_stack(names, base_vals)
        stack.move_to([-4.85, 0.95, 0])
        style_row(rows[3], True)
        db_word = S.text("database", 26, S.GREY)
        db_x = S.math("x", size=42, color=X_COLOR)
        db_lab = VGroup(db_word, db_x).arrange(RIGHT, buff=0.15, aligned_edge=DOWN).next_to(stack, UP, buff=0.25)
        db_xp = S.math("x'", size=42, color=XP_COLOR).move_to(db_x, aligned_edge=LEFT)

        machine = RoundedRectangle(width=1.5, height=1.25, corner_radius=0.18, stroke_color=S.WHITE,
                                   stroke_width=3).set_fill(S.GREY_DARKER, 1).move_to([-1.75, 0.95, 0])
        f_lab = S.math("f", size=64).move_to(machine)
        nl = NumberLine(x_range=[0, 10, 1], length=5.4, color=S.GREY, stroke_width=2, tick_size=0.07)
        nl.move_to([3.6, 0.95, 0])
        arr_in = Arrow(stack.get_right(), machine.get_left(), buff=0.15, color=S.GREY, stroke_width=3,
                       max_tip_length_to_length_ratio=0.25, tip_length=0.18)
        arr_out = Arrow(machine.get_right(), nl.get_left(), buff=0.12, color=S.GREY, stroke_width=3,
                        max_tip_length_to_length_ratio=0.25, tip_length=0.18)

        def out_dot(v, col):
            return Dot(nl.n2p(v), radius=0.1, color=col)

        dot_x = out_dot(3.2, X_COLOR)
        dot_xp = out_dot(4.6, XP_COLOR)
        lab_fx = S.math("f(x)", size=32, color=X_COLOR)
        lab_fxp = S.math("f(x')", size=32, color=XP_COLOR)

        def place_labels(vx, vxp):
            return (lab_fx.copy().next_to(nl.n2p(vx), UP, buff=0.22).align_to(nl.n2p(vx) + RIGHT * 0.12, RIGHT),
                    lab_fxp.copy().next_to(nl.n2p(vxp), UP, buff=0.22).align_to(nl.n2p(vxp) + LEFT * 0.12, LEFT))

        lab_fx.move_to(place_labels(3.2, 4.6)[0])
        lab_fxp.move_to(place_labels(3.2, 4.6)[1])

        def gap_seg(vx, vxp):
            return Line(nl.n2p(vx), nl.n2p(vxp), color=SENS_COLOR, stroke_width=8)

        defn = S.math(r"S(f)", "=", r"\max_{x,\,x'\ \text{neighbors}}", r"\big|", r"f(x)", "-", r"f(x')",
                      r"\big|", size=52)
        defn[0].set_color(SENS_COLOR)
        defn[4].set_color(X_COLOR)
        defn[6].set_color(XP_COLOR)
        defn.move_to(DOWN * 2.35)

        # neighbour pairs: (row that changes, its value in x', f(x), f(x'))
        pairs = [(3, "has X", 3.2, 4.6), (0, "has X", 4.3, 5.0), (1, "no X", 2.2, 4.6), (2, "has X", 6.0, 7.6)]
        slot_y = [0.42, 0.17, -0.08, -0.33]

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(stack), FadeIn(db_lab), FadeIn(machine), Write(f_lab), Create(nl),
                      GrowArrow(arr_in), GrowArrow(arr_out), run_time=1.2)
            self.play(TransformFromCopy(f_lab, dot_x), FadeIn(lab_fx), run_time=0.6)
            vo.wait_until("It depends on")
            self.play(Transform(rows[3][3], S.text("has X", 22, XP_COLOR).move_to(rows[3][3])),
                      Transform(db_x, db_xp), *[Indicate(m, color=ALICE, scale_factor=1.15) for m in rows[3][1:3]],
                      run_time=0.8)
            self.play(TransformFromCopy(f_lab, dot_xp), FadeIn(lab_fxp), run_time=0.8)
            seg = gap_seg(3.2, 4.6)
            self.play(Create(seg), run_time=0.5)
            vo.wait_until("its sensitivity")
            self.play(Write(defn), run_time=1.6)
            vo.wait_until("the most that")
            self.play(*[Indicate(m, color=SENS_COLOR, scale_factor=1.06) for m in defn[3:8]],
                      Indicate(seg, color=SENS_COLOR, scale_factor=1.15), run_time=1.0)
            vo.wait_until("over all pairs")
            segs = VGroup()
            for k, (r, v_new, vx, vxp) in enumerate(pairs):
                if k > 0:
                    anims = []
                    for i in range(4):
                        tgt = rows[i].copy()
                        style_row(tgt, i == r)
                        name = names[i] if k < 3 else "?"
                        tgt[2].become(S.text(name, 22, ALICE if i == r else (S.WHITE if k < 3 else S.GREY))
                                      .move_to(rows[i][2], aligned_edge=LEFT))
                        tgt[3].become(S.text(v_new if i == r else base_vals[i], 22,
                                             XP_COLOR if i == r else S.WHITE).move_to(rows[i][3]))
                        anims += [Transform(rows[i][j], tgt[j]) for j in range(4)]
                    lx, lxp = place_labels(vx, vxp)
                    seg = gap_seg(vx, vxp)
                    self.play(*anims, dot_x.animate.move_to(nl.n2p(vx)), dot_xp.animate.move_to(nl.n2p(vxp)),
                              lab_fx.animate.move_to(lx), lab_fxp.animate.move_to(lxp), run_time=0.5)
                    self.play(Create(seg), run_time=0.25)
                self.play(seg.animate.set_y(slot_y[k]).set_stroke(width=6), run_time=0.3)
                segs.add(seg)
            # line the gaps up from a common start: the largest one is S(f)
            left = nl.n2p(0)[0] + 0.1
            self.play(*[sg.animate.shift(RIGHT * (left - sg.get_left()[0])) for sg in segs], run_time=0.5)
            s_lab = S.math("S(f)", size=34, color=SENS_COLOR).next_to(segs[2], RIGHT, buff=0.2)
            self.play(segs[2].animate.set_stroke(width=10), FadeIn(s_lab, shift=LEFT * 0.2),
                      Indicate(defn[2], color=SENS_COLOR), run_time=vo.remaining(0.6))

        # ============================================================ 1. counting query: S = 1
        nl2 = NumberLine(x_range=[37, 47, 1], length=5.4, color=S.GREY, stroke_width=2, tick_size=0.07)
        nl2.move_to(nl)
        nl2_labs = VGroup(*[S.text(str(v), 20, S.GREY).next_to(nl2.n2p(v), DOWN, buff=0.15)
                            for v in range(37, 48)])
        count_lab = S.text("count", 34).move_to(machine)
        reset = []
        for i, row in enumerate(rows):
            tgt = row.copy()
            style_row(tgt, i == 3)
            tgt[2].become(S.text(names[i], 22, ALICE if i == 3 else S.WHITE).move_to(row[2], aligned_edge=LEFT))
            tgt[3].become(S.text(base_vals[i], 22, X_COLOR if i == 3 else S.WHITE).move_to(row[3]))
            reset += [Transform(row[j], tgt[j]) for j in range(4)]
        lx41 = lab_fx.copy().next_to(nl2.n2p(41), UP, buff=0.22).align_to(nl2.n2p(41) + RIGHT * 0.12, RIGHT)
        lx42 = lab_fxp.copy().next_to(nl2.n2p(42), UP, buff=0.22).align_to(nl2.n2p(42) + LEFT * 0.12, LEFT)
        seg1 = Line(nl2.n2p(41), nl2.n2p(42), color=SENS_COLOR, stroke_width=8)
        one = S.math("1", size=34, color=SENS_COLOR).next_to(seg1, DOWN, buff=0.45)
        s_count = S.math(r"S(\text{count})", "=", "1", size=48)
        s_count[0].set_color(SENS_COLOR)
        s_count[2].set_color(SENS_COLOR)
        s_count.move_to([3.6, -0.55, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(segs, s_lab, dot_xp, lab_fxp)), Transform(f_lab, count_lab),
                      Transform(db_x, S.math("x", size=42, color=X_COLOR).move_to(db_x, aligned_edge=LEFT)),
                      *reset, run_time=0.8)
            self.play(ReplacementTransform(nl, nl2), FadeIn(nl2_labs), dot_x.animate.move_to(nl2.n2p(41)),
                      lab_fx.animate.move_to(lx41), run_time=0.8)
            vo.wait_until("one row changes")
            self.play(Transform(rows[3][3], S.text("has X", 22, XP_COLOR).move_to(rows[3][3])),
                      Transform(db_x, S.math("x'", size=42, color=XP_COLOR).move_to(db_x, aligned_edge=LEFT)),
                      run_time=0.6)
            lab_fxp.move_to(lx42)
            dot42 = Dot(nl2.n2p(42), radius=0.1, color=XP_COLOR)
            self.play(TransformFromCopy(dot_x, dot42), FadeIn(lab_fxp), run_time=0.6)
            self.play(Create(seg1), FadeIn(one, shift=UP * 0.1), run_time=0.5)
            self.play(TransformFromCopy(one, s_count[2]), FadeIn(s_count[:2]), run_time=0.7)
            vo.wait_until("Sensitivity one")
            self.play(Circumscribe(s_count, color=SENS_COLOR), run_time=vo.remaining(0.8))

        # ============================================================ 2. histograms: ponder
        defn_top = defn.copy().scale(0.85).move_to(UP * 2.85)
        base_line = Line([H_LEFT - 0.1, H_BASE, 0], [H_RIGHT + 0.1, H_BASE, 0], color=S.GREY, stroke_width=2)
        bin_labs = VGroup(*[S.math(f"B_{j + 1}", size=30, color=S.GREY).move_to([bin_x(5, j)[0], H_BASE - 0.35, 0])
                            for j in range(5)])
        dividers = VGroup(*[DashedLine([H_LEFT + 1.2 * j, H_BASE, 0], [H_LEFT + 1.2 * j, H_BASE + H_MAX + 0.2, 0],
                                       color=S.GREY_DARK, stroke_width=1.5, dash_length=0.08) for j in range(6)])
        blk5, a_blk, cnt5 = layout(5, ALICE_U[0])          # one unit block per row
        assert cnt5 == COUNTS5
        bin5 = [VGroup(*[b for b, u in zip(blk5, ROW_U) if bin_of(u, 5) == j]) for j in range(5)]
        alice = hover(a_blk)
        def d_label(n):
            g = VGroup(S.math("d", "=", str(n), size=44), S.text("bins", 28, S.GREY))
            g.arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
            return g.move_to([-5.6, 1.8, 0], aligned_edge=LEFT)

        d_grp = d_label(5)
        d_lab, d_word = d_grp
        rng = np.random.default_rng(6)
        drops = sorted(((b, rng.random()) for b in blk5), key=lambda t: t[1])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(stack, db_lab, db_x, machine, f_lab, arr_in, arr_out, nl2, nl2_labs, dot_x,
                                     dot42, lab_fx, lab_fxp, seg1, one, s_count)), run_time=0.5)
            self.play(ReplacementTransform(defn, defn_top), run_time=0.7)
            vo.wait_until("split the possible values")
            self.play(Create(base_line), FadeIn(dividers), FadeIn(bin_labs), run_time=0.9)
            self.play(FadeIn(d_grp), run_time=0.6)
            vo.wait_until("and release how many")
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.6) for b, _ in drops], lag_ratio=0.02),
                      run_time=2.2)
            self.play(FadeIn(a_blk, shift=DOWN * 0.6), run_time=0.4)
            self.play(FadeIn(alice[1:], shift=DOWN * 0.2), Create(alice[0]), run_time=0.6)
            vo.wait_until("if Alice's row changes")
            self.play(Wiggle(alice[1:]), run_time=1.0)
            vo.wait_until("how much can the whole")
            self.play(*[Indicate(b, color=S.WHITE, scale_factor=1.0) for b in blk5],
                      Indicate(a_blk, color=S.WHITE, scale_factor=1.0), run_time=1.0)
            vo.wait_until("Does it depend")
            self.play(Indicate(d_lab, color=S.WHITE), FadeOut(dividers), run_time=1.0)
        card = ponder_at(self, "If Alice's row changes,\nhow much can the whole\nhistogram change in total?\n"
                               "Does it depend on the\nnumber of bins?", seconds=8, width=5.9,
                         pos=[3.45, -0.3, 0])

        # ============================================================ 3. the answer: 2, in any dimension
        a_tgt = layout(5, ALICE_U[1])[1]
        ghost = DashedVMobject(a_blk.copy().set_fill(opacity=0).set_stroke(ALICE, 2), num_dashes=16)
        minus = S.math("-1", size=34).next_to(ghost, UP, buff=0.12)
        plus = S.math("+1", size=34)
        zeros = VGroup(*[S.math("0", size=30, color=S.GREY).next_to(bin5[j], UP, buff=0.12) for j in (0, 2, 4)])
        expr = S.math(r"|{-1}|", "+", r"|{+1}|", "=", "2", size=56).move_to([3.5, -0.4, 0])
        expr[4].set_color(SENS_COLOR)
        defn_l1 = S.math(r"S(f)", "=", r"\max_{x,\,x'\ \text{neighbors}}", r"\big\|", r"f(x)", "-", r"f(x')",
                         r"\big\|_1", size=52).scale(0.85).move_to(defn_top)
        defn_l1[0].set_color(SENS_COLOR)
        defn_l1[4].set_color(X_COLOR)
        defn_l1[6].set_color(XP_COLOR)
        l1_note = S.math(r"\|v\|_1", "=", r"|v_1| + |v_2| + \cdots + |v_d|", size=36).next_to(defn_l1, DOWN,
                                                                                             buff=0.3)
        s_big = S.math("S", "=", "2", size=72).move_to(expr)
        s_big[0].set_color(SENS_COLOR)
        s_big[2].set_color(SENS_COLOR)

        # finer histograms of the SAME rows: each bin splits into 4, then each of those into 3
        def hop_labels(old, new):
            """-1 where Alice's block left (on the remaining stack), +1 beside her icon at the new bin."""
            mi = S.math("-1", size=28).next_to(old.get_bottom(), UP, buff=0.04)
            pl = S.math("+1", size=28).next_to(new.get_top() + UP * 0.75 + RIGHT * 0.2, RIGHT, buff=0.08)
            return mi, pl

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(card), run_time=0.5)
            self.add(ghost)
            self.play(VGroup(a_blk, alice).animate.shift(UP * 0.35), run_time=0.5)
            self.play(VGroup(a_blk, alice).animate(path_arc=-PI / 2.5).shift(a_tgt.get_center() - a_blk.get_center()),
                      run_time=1.2)
            vo.wait_until("one count goes down")
            self.play(FadeIn(minus, shift=DOWN * 0.15), Indicate(ghost, color=ALICE), run_time=0.7)
            vo.wait_until("another goes up")
            plus.next_to(a_blk, RIGHT, buff=0.15)
            self.play(FadeIn(plus, shift=UP * 0.15), Indicate(a_blk, color=ALICE), run_time=0.7)
            vo.wait_until("Total change")
            self.play(TransformFromCopy(minus, expr[0]), TransformFromCopy(plus, expr[2]), FadeIn(expr[1]),
                      run_time=0.9)
            self.play(Write(expr[3:]), run_time=0.5)
            vo.wait_until("Adding up absolute")
            self.play(LaggedStart(*[FadeIn(z, shift=DOWN * 0.1) for z in zeros], lag_ratio=0.25), run_time=0.8)
            vo.wait_until("is the L1 norm")
            self.play(*[ReplacementTransform(defn_top[i], defn_l1[i]) for i in range(len(defn_l1))], run_time=1.2)
            self.play(FadeIn(l1_note, shift=DOWN * 0.15), run_time=0.8)
            vo.wait_until("the paper's way")
            self.play(Indicate(defn_l1[3], color=SENS_COLOR), Indicate(defn_l1[7], color=SENS_COLOR),
                      run_time=1.0)
            vo.wait_until("And it is two")
            self.play(ReplacementTransform(VGroup(*expr[:3]), s_big[0]), ReplacementTransform(expr[3], s_big[1]),
                      ReplacementTransform(expr[4], s_big[2]), FadeOut(VGroup(minus, plus, zeros, ghost)),
                      run_time=0.5)
            # 5 -> 20 bins: every bin splits in four; each row's block slides into its sub-bin
            blk20, a20, _ = layout(20, ALICE_U[1])
            self.play(*[Transform(b, t) for b, t in zip(blk5, blk20)], Transform(a_blk, a20),
                      alice.animate.shift(a20.get_top() - a_blk.get_top()), FadeOut(bin_labs),
                      Transform(d_grp, d_label(20)), run_time=0.9)
            a20b = layout(20, ALICE_U[2])[1]
            mi, pl = hop_labels(a20, a20b)
            self.play(VGroup(a_blk, alice).animate(path_arc=PI / 2.5).shift(a20b.get_center() - a_blk.get_center()),
                      FadeIn(mi), run_time=0.7)
            self.play(FadeIn(pl), Indicate(s_big, color=SENS_COLOR, scale_factor=1.08), run_time=0.4)
            self.wait(0.3)
            # 20 -> 60 bins: every bin splits in three
            blk60, a60, _ = layout(60, ALICE_U[2])
            self.play(*[Transform(b, t) for b, t in zip(blk5, blk60)], Transform(a_blk, a60),
                      alice.animate.shift(a60.get_top() - a_blk.get_top()), FadeOut(VGroup(mi, pl)),
                      Transform(d_grp, d_label(60)), run_time=0.9)
            a60b = layout(60, ALICE_U[3])[1]
            mi, pl = hop_labels(a60, a60b)
            self.play(VGroup(a_blk, alice).animate(path_arc=-PI / 2.5).shift(a60b.get_center() - a_blk.get_center()),
                      FadeIn(mi), run_time=0.7)
            self.play(FadeIn(pl), Indicate(s_big, color=SENS_COLOR, scale_factor=1.08), run_time=0.4)
            vo.wait_until("It does not depend")
            self.play(Circumscribe(s_big, color=SENS_COLOR), run_time=vo.remaining(0.8))

        # ============================================================ 4. contrast: the largest income
        X0, PER_M = -3.25, 7.5          # x of $0, screen units per $1M
        ax_y = -2.0

        def xv(v):
            return X0 + PER_M * v / 1e6

        tag = S.text("illustration", 20, S.GREY)
        tag = VGroup(SurroundingRectangle(tag, color=S.GREY, buff=0.08, corner_radius=0.05, stroke_width=1.5), tag)
        tag.to_corner(UL, buff=0.58)        # inside the safe area (x >= -6.6)
        q_txt = S.text("What is the largest income in the database?", 32)
        q_box = SurroundingRectangle(q_txt, color=S.GREY, buff=0.2, corner_radius=0.12, stroke_width=2)
        q_box.set_fill(S.GREY_DARKER, 1)
        query = VGroup(q_box, q_txt).move_to([0.6, 2.75, 0])
        inames = ["Bob", "Carol", "Dan", "Erin", "Femi"]
        incomes = [52e3, 81e3, 38e3, 64e3, 45e3]
        irows = database_rows(inames, [money(v) for v in incomes], color=S.GREY, width=2.9, row_height=0.5,
                              size=22)
        irows.move_to([-5.0, 0.55, 0])
        rolls = VGroup(*[coin_roll(X0, xv(v), r.get_y()) for v, r in zip(incomes, irows)])
        axis = Line([X0, ax_y, 0], [6.35, ax_y, 0], color=S.GREY, stroke_width=2)
        ticks = VGroup()
        for v in [0, 250e3, 500e3, 750e3, 1e6]:
            ticks.add(Line([xv(v), ax_y - 0.07, 0], [xv(v), ax_y + 0.07, 0], color=S.GREY, stroke_width=2))
            ticks.add(S.text("$0" if v == 0 else money(v), 20, S.GREY).next_to([xv(v), ax_y, 0], DOWN, buff=0.14))
        ans_word = S.text("answer", 22, S.GREY).next_to(axis, LEFT, buff=0.25)
        ans = Dot([xv(81e3), ax_y, 0], radius=0.1, color=S.WHITE)
        proj = always_redraw(lambda: DashedLine([ans.get_x(), irows[1].get_y() if ans.get_x() < xv(90e3)
                                                 else irows[3].get_y(), 0],
                                                ans.get_center(), color=S.GREY, stroke_width=2, dash_length=0.08))
        big = coin_roll(X0, 6.55, irows[3].get_y())
        big_val = S.text("$1B", 22, ALICE).move_to(irows[3][3])
        cont = S.text("$1,000,000,000 →", 24, S.GOLD).next_to([6.55, irows[3].get_y(), 0], UP, buff=0.24)
        cont.align_to([6.5, 0, 0], RIGHT)
        huge = Arrow([xv(81e3), ax_y - 0.62, 0], [6.5, ax_y - 0.62, 0], buff=0, color=SENS_COLOR, stroke_width=5,
                     max_tip_length_to_length_ratio=0.04, tip_length=0.25)
        huge_lab = S.text("S huge", 28, SENS_COLOR).next_to(huge, DOWN, buff=0.1)
        cap = DashedLine([xv(1e6), 1.8, 0], [xv(1e6), ax_y, 0], color=SENS_COLOR, stroke_width=3, dash_length=0.12)
        cap_lab = S.text("cap every value at $1M", 24, SENS_COLOR).next_to(cap, UP, buff=0.1)
        cap_lab.align_to([6.5, 0, 0], RIGHT)
        kept = VGroup(*[c for c in big if c.get_x() <= xv(1e6)])
        cut_off = VGroup(*[c for c in big if c.get_x() > xv(1e6)])
        capped_val = S.text("$1M", 22, ALICE).move_to(irows[3][3])
        s_cap = BraceBetweenPoints([X0, ax_y - 0.5, 0], [xv(1e6), ax_y - 0.5, 0], DOWN, color=SENS_COLOR)
        s_cap_lab = S.math(r"S \le \$1\text{M}", size=34, color=SENS_COLOR).next_to(s_cap, DOWN, buff=0.08)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
            self.play(FadeIn(tag), FadeIn(query, shift=DOWN * 0.2), FadeIn(irows), run_time=0.8)
            self.play(Create(axis), FadeIn(ticks), FadeIn(ans_word), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(r, lag_ratio=0.3) for r in rolls], lag_ratio=0.15), run_time=0.9)
            self.play(FadeIn(ans, scale=0.5), Create(proj), Indicate(irows[1][3], color=S.GOLD), run_time=0.7)
            vo.wait_until("One billionaire")
            r3 = irows[3].copy()
            style_row(r3, True)
            self.play(Transform(irows[3][0], r3[0]), Transform(irows[3][1], r3[1]), Transform(irows[3][2], r3[2]),
                      Transform(irows[3][3], big_val), FadeOut(rolls[3]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c) for c in big], lag_ratio=0.02),
                      ans.animate.move_to([6.5, ax_y, 0]), FadeIn(cont), run_time=1.6, rate_func=linear)
            vo.wait_until("and with no cap")
            self.play(GrowArrow(huge), FadeIn(huge_lab), run_time=0.8)
            self.play(Indicate(huge_lab, color=SENS_COLOR), Flash([6.5, ax_y, 0], color=SENS_COLOR), FadeOut(cont),
                      run_time=0.8)
            vo.wait_until("The standard fix")
            self.play(Create(cap), FadeIn(cap_lab), run_time=0.7)
            self.play(LaggedStart(*[c.animate.shift(DOWN * 0.5).set_opacity(0) for c in cut_off], lag_ratio=0.01),
                      Transform(irows[3][3], capped_val), ans.animate.move_to([xv(1e6), ax_y, 0]),
                      run_time=1.2)
            self.play(ReplacementTransform(huge, s_cap), ReplacementTransform(huge_lab, s_cap_lab), run_time=0.8)
            proj.clear_updaters()
            vo.wait_until("Remember that trick")
            # same move in deep learning: clip each example's gradient
            self.play(FadeOut(Group(*[m for m in self.mobjects])), run_time=0.6)
            origin = np.array([0.0, 0.25, 0])
            C = 1.5
            angles = [0.3, 1.1, 1.9, 2.6, 3.5, 4.3, 5.2]
            lengths = [0.9, 2.6, 1.3, 3.0, 0.7, 2.3, 1.9]
            grads = VGroup(*[Arrow(origin, origin + L * np.array([np.cos(a), np.sin(a), 0]), buff=0,
                                   color=S.WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.15,
                                   tip_length=0.2) for a, L in zip(angles, lengths)])
            ring = DashedVMobject(Circle(radius=C, color=SENS_COLOR, stroke_width=3).move_to(origin), num_dashes=40)
            c_lab = S.math("C", size=36, color=SENS_COLOR).move_to(origin + (C + 0.3) * np.array([np.cos(0.7),
                                                                                                  np.sin(0.7), 0]))
            clipped = VGroup(*[Arrow(origin, origin + min(L, C) * np.array([np.cos(a), np.sin(a), 0]), buff=0,
                                     color=SENS_COLOR if L > C else S.WHITE, stroke_width=4,
                                     max_tip_length_to_length_ratio=0.15, tip_length=0.2)
                               for a, L in zip(angles, lengths)])
            g_cap = S.text("private deep learning: clip each example's gradient to size C", 28, S.GREY)
            g_cap.to_edge(DOWN, buff=0.5)
            self.play(LaggedStart(*[GrowArrow(a) for a in grads], lag_ratio=0.1), run_time=0.8)
            self.play(Create(ring), FadeIn(c_lab), FadeIn(g_cap), run_time=0.6)
            self.play(Transform(grads, clipped), run_time=vo.remaining(0.8))

        # ============================================================ 5. a choice vs. a fact
        lbox = RoundedRectangle(width=5.4, height=3.0, corner_radius=0.2, stroke_color=SENS_COLOR, stroke_width=4)
        lbox.set_fill(S.GREY_DARKER, 0.6).move_to([-3.2, 0.7, 0])
        l_sym = S.math("S(f)", size=76, color=SENS_COLOR)
        l_txt = VGroup(S.text("a fact about", 34), S.math("f", size=44)).arrange(RIGHT, buff=0.15)
        VGroup(l_sym, l_txt).arrange(DOWN, buff=0.35).move_to(lbox)
        rbox = lbox.copy().set_stroke(EPS_COLOR).move_to([3.2, 0.7, 0])
        r_sym = S.math(r"\varepsilon", size=84, color=EPS_COLOR)
        r_txt = S.text("a choice (policy)", 34)
        slider = Line(LEFT * 1.3, RIGHT * 1.3, color=S.GREY, stroke_width=3)
        knob = Dot(radius=0.12, color=EPS_COLOR)
        VGroup(r_sym, r_txt, slider).arrange(DOWN, buff=0.3).move_to(rbox)
        knob.move_to(slider.point_from_proportion(0.5))
        not_db = S.text("does not depend on the actual database", 26, S.GREY).next_to(lbox, DOWN, buff=0.35)
        mini_vals = [["no X", "has X", "no X"], ["has X", "has X", "no X"], ["no X", "no X", "has X"]]
        minis = [database_rows(["Bob", "Carol", "Dan"], v, color=S.GREY, width=2.3, row_height=0.34, size=20)
                 for v in mini_vals]
        for m in minis:
            m.next_to(not_db, DOWN, buff=0.25)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
            vo.wait_until("Sensitivity is a property")
            self.play(Create(lbox), Write(l_sym), FadeIn(l_txt), run_time=1.1)
            vo.wait_until("not of the particular")
            self.play(FadeIn(not_db), FadeIn(minis[0]), run_time=0.7)
            for m in minis[1:]:
                self.play(Transform(minis[0], m), Indicate(l_sym, color=SENS_COLOR, scale_factor=1.05),
                          run_time=0.8)
            vo.wait_until("Epsilon is a choice")
            self.play(Create(rbox), Write(r_sym), FadeIn(r_txt), FadeIn(slider), FadeIn(knob), run_time=0.8)
            self.play(knob.animate.move_to(slider.point_from_proportion(0.85)), run_time=0.5)
            self.play(knob.animate.move_to(slider.point_from_proportion(0.25)), run_time=0.5)
            vo.wait_until("Sensitivity is a fact")
            self.play(Circumscribe(lbox, color=SENS_COLOR, buff=0.08), run_time=vo.remaining(0.8))
        self.wait(0.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
