"""S11 · Interactive vs. one-shot releases — Section 4 of the paper.

Theorem 3 (p. 277): for D = {0,1}^d and any eps-indistinguishable NON-interactive M, for at least
2/3 of the parity queries f(x) = sum_i r_i (.) x_i  (a separate non-zero mask r_i per row), M(x) for
x uniform on {f = 0} and for x uniform on {f = n} are within statistical distance
O(n^{4/3} eps^{2/3} 2^{-d/3}).  Proof idea (Sec. 4.2-4.3): Lemma 2 (a random mask's even half is a
pairwise-independent "poll" of {0,1}^d, so an e^{+-eps}-bounded map can't tell it from all of D) +
a hybrid chain of n row swaps, each costing sigma = O((n eps^2 2^{-d})^{1/3}).
Proposition 2 (p. 278): randomized response, SAME mask for every row: needs n = Omega(2^{d/3}/eps^{2/3}).
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import gaussian_pdf, person_icon, ponder_card
from explainer.scene import VoiceScene

from common import ALICE, EPS_COLOR, NARRATION, NOISE_COLOR, SENS_COLOR, X_COLOR, XP_COLOR

SAY = NARRATION["S11"]

MASK = S.PURPLE        # a row's mask r_i: the bit positions that count
EVEN = X_COLOR         # the "every row even" world (true answer 0)
ODD = XP_COLOR         # the "every row odd" world  (true answer n)
TICK = S.TEAL          # ✓
COIN = S.GOLD          # Warner's coin
COIN_EDGE = "#A87B2C"    # as in S10
SYM = "DejaVu Sans"    # font that has ✓ ✗
D = 8                  # bits per row in the pictures
N = 6                  # rows in the small tables


# ============================================================ bits & masks

def parity(bits, mask) -> int:
    return int(np.dot(bits, mask) % 2)


def random_mask(rng, lo: int = 2, hi: int = 4) -> np.ndarray:
    m = np.zeros(D, int)
    m[rng.choice(D, int(rng.integers(lo, hi + 1)), replace=False)] = 1
    return m


def sample_row(rng, mask, target: int) -> np.ndarray:
    """Uniform row with parity(row, mask) == target (flip one masked bit if needed: a bijection)."""
    bits = rng.integers(0, 2, D)
    if parity(bits, mask) != target:
        bits[int(np.flatnonzero(mask)[0])] ^= 1
    return bits


# ============================================================ small pictures

def digit(v, size=24, color=None):
    return S.text(str(v), size, color or (S.WHITE if v else S.GREY), font=S.FONT_SANS)


def bit_table(bits, cell=0.48, icon_color=X_COLOR):
    """Rows of the running database: VGroup(box, icon, cells, digits, parity_cell) per row."""
    rows = VGroup()
    for b in bits:
        icon = person_icon(icon_color, height=cell * 0.72)
        cells = VGroup(*[Square(cell, stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(S.BG, 1)
                         for _ in range(D)]).arrange(RIGHT, buff=0)
        cells.next_to(icon, RIGHT, buff=0.22)
        digs = VGroup(*[digit(v).move_to(c) for v, c in zip(b, cells)]).set_z_index(3)
        pcell = Square(cell, stroke_color=S.GREY, stroke_width=1.5).set_fill(S.BG, 1)
        pcell.next_to(cells, RIGHT, buff=0.3)
        inner = VGroup(icon, cells, pcell)
        box = Rectangle(width=inner.width + 0.3, height=cell + 0.12, stroke_color=S.GREY_DARK,
                        stroke_width=1.5).set_fill(S.GREY_DARKER, 1).move_to(inner)
        rows.add(VGroup(box, icon, cells, digs, pcell))
    return rows.arrange(DOWN, buff=0)


def mask_overlays(cells_per_row, masks, scale=0.84, width=3, fill=0.32):
    out = VGroup()
    for cells, m in zip(cells_per_row, masks):
        for j in np.flatnonzero(m):
            c = cells[int(j)]
            out.add(Square(c.width * scale, stroke_color=MASK, stroke_width=width)
                    .set_fill(MASK, fill).move_to(c).set_z_index(2))
    return out


def mask_card(masks, cell=0.1):
    """A query = one mask per row, drawn as a little card. VGroup(frame, on, off)."""
    grid = VGroup(*[VGroup(*[Square(cell, stroke_color=S.GREY_DARKER, stroke_width=0.8)
                             .set_fill(MASK if v else S.GREY_DARK, 1) for v in m]).arrange(RIGHT, buff=0)
                    for m in masks]).arrange(DOWN, buff=0)
    on = VGroup(*[sq for row, m in zip(grid, masks) for sq, v in zip(row, m) if v])
    off = VGroup(*[sq for row, m in zip(grid, masks) for sq, v in zip(row, m) if not v])
    frame = RoundedRectangle(width=grid.width + 0.22, height=grid.height + 0.22, corner_radius=0.06,
                             stroke_color=S.GREY, stroke_width=1.5).set_fill(S.GREY_DARKER, 1).move_to(grid)
    return VGroup(frame, on, off)


def mini_table(bits, masks, color, cell=0.24):
    """Compact database: filled cells (1 = light), mask outlines, parity digits. VGroup(frame, rows, masks, par)."""
    rows = VGroup(*[VGroup(*[Square(cell, stroke_color=S.BG, stroke_width=1)
                             .set_fill(S.WHITE if v else S.GREY_DARK, 0.85 if v else 1) for v in b])
                    .arrange(RIGHT, buff=0) for b in bits]).arrange(DOWN, buff=0.04)
    over = mask_overlays(rows, masks, scale=0.86, width=2.5, fill=0.0)
    par = VGroup(*[digit(parity(b, m), 22, color).next_to(r, RIGHT, buff=0.16)
                   for b, m, r in zip(bits, masks, rows)])
    frame = SurroundingRectangle(VGroup(rows, par), buff=0.11, corner_radius=0.08, stroke_color=color,
                                 stroke_width=2.5)
    return VGroup(frame, rows, over, par)


def db_icon(color=X_COLOR, w=1.0, n=4, rh=0.22):
    return VGroup(*[Rectangle(width=w, height=rh, stroke_color=color, stroke_width=2).set_fill(color, 0.15)
                    for _ in range(n)]).arrange(DOWN, buff=0)


def release_sheet(rng, w=1.5, h=1.8):
    """A published, sanitized table M(x)."""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=S.WHITE,
                          stroke_width=2).set_fill(S.GREY_DARKER, 1)
    cols, rows = 5, 7
    cw, ch = (w - 0.3) / cols, (h - 0.3) / rows
    cells = VGroup(*[Rectangle(width=cw * 0.8, height=ch * 0.6, stroke_width=0)
                     .set_fill(S.WHITE, float(rng.uniform(0.12, 0.6))) for _ in range(cols * rows)])
    cells.arrange_in_grid(rows=rows, cols=cols, buff=(cw * 0.2, ch * 0.4)).move_to(fr)
    return VGroup(fr, cells)


def m_box(w=0.85, h=0.7):
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=S.WHITE,
                          stroke_width=2).set_fill(S.GREY_DARKER, 1)
    return VGroup(fr, S.math("M", size=40).move_to(fr))


def tag(tex, color=S.WHITE, size=30):
    m = S.math(tex, size=size, color=color)
    fr = RoundedRectangle(width=m.width + 0.3, height=m.height + 0.22, corner_radius=0.08,
                          stroke_color=color, stroke_width=1.5).set_fill(S.GREY_DARKER, 1).move_to(m)
    return VGroup(fr, m)


def coin(r=0.28):
    """Warner's coin (S02's look: gold disc, rim, inner ring; the H face only when it is >= 20 pt)."""
    disc = Circle(radius=r, stroke_color=COIN_EDGE, stroke_width=3).set_fill(COIN, 1)
    ring = Circle(radius=r * 0.78, stroke_color=COIN_EDGE, stroke_width=1.5)
    g = VGroup(disc, ring)
    if r >= 0.235:
        g.add(S.text("H", r * 85, S.BG, weight="BOLD").move_to(disc))
    return g


def budget_bar(w=3.0, h=0.36, k=5):
    frame = Rectangle(width=w, height=h, stroke_color=EPS_COLOR, stroke_width=2.5)
    segs = VGroup(*[Rectangle(width=w / k - 0.07, height=h - 0.1, stroke_width=0).set_fill(EPS_COLOR, 0.85)
                    for _ in range(k)]).arrange(RIGHT, buff=0.07).move_to(frame)
    return VGroup(frame, segs)


def query_card(question, width=8.4):
    """Same card as S01's query card."""
    q = S.text(question, 28, S.WHITE)
    if q.width > width - 0.5:
        q.scale_to_fit_width(width - 0.5)
    head = S.text("Query", 22, S.GREY, font=S.FONT_SANS)
    body = VGroup(head, q).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    frame = RoundedRectangle(width=width, height=body.height + 0.4, corner_radius=0.15,
                             stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
    body.move_to(frame)
    return VGroup(frame, head, q)


def statement_card(title, *lines, width=12.4):
    """GREY-framed card with a YELLOW bold title (same look as S07's Proposition 1 card)."""
    t = S.text(title, 28, S.YELLOW, weight="BOLD")
    body = VGroup(t, *lines).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    if body.width > width - 0.5:
        body.scale_to_fit_width(width - 0.5)
    frame = SurroundingRectangle(body, color=S.GREY, buff=0.22, corner_radius=0.12, stroke_width=2)
    frame.set_fill(S.BG, 0.95)
    return VGroup(frame, body)


def x_mark(m, color=NOISE_COLOR, width=6, pad=0.1):
    """The S09 red cross over a refused query card."""
    c = m.get_center()
    w, h = m.width / 2 + pad, m.height / 2 + pad
    return VGroup(Line(c + np.array([-w, -h, 0]), c + np.array([w, h, 0]), color=color, stroke_width=width),
                  Line(c + np.array([-w, h, 0]), c + np.array([w, -h, 0]), color=color, stroke_width=width))


def lens(ax, f_a, f_b, color_a, color_b, a=0.0, b=10.0, step=0.02, opacity=0.5):
    """S05-style shading of the area between two curves, coloured by whichever curve is on top."""
    ts = np.arange(a, b + step / 2, step)
    diff = np.array([f_a(t) - f_b(t) for t in ts])
    out, start = VGroup(), 0
    for i in range(1, len(ts) + 1):
        if i == len(ts) or np.sign(diff[i]) != np.sign(diff[start]):
            seg = ts[start:i + 1] if i < len(ts) else ts[start:]
            if len(seg) >= 2:
                pts = [ax.c2p(t, f_a(t)) for t in seg] + [ax.c2p(t, f_b(t)) for t in seg[::-1]]
                col = color_a if diff[start] > 0 else color_b
                out.add(Polygon(*pts, stroke_width=0).set_fill(col, opacity))
            start = i
    return out


def sym(ch, size=40, color=TICK):
    return Text(ch, font=SYM, font_size=size, color=color)


def ponder_at(scene, question, seconds, pos, width):
    """pause_and_ponder(), but placed at `pos` so a picture can stay beside the card."""
    card = ponder_card(question, width=width).move_to(pos)
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return card


def fan(cards, center, radius=6.0, spread=0.62):
    """Arrange cards like a hand of playing cards."""
    k = len(cards)
    for i, c in enumerate(cards):
        th = -spread + 2 * spread * i / (k - 1)
        c.rotate(-th).move_to(center + radius * np.array([np.sin(th), np.cos(th) - 1, 0]))
    return cards


class Separation(VoiceScene):
    def construct(self):
        rng = np.random.default_rng(11)

        # fixed data for the whole scene ------------------------------------------------------
        masks = [random_mask(rng) for _ in range(N)]                 # the query of the table
        bits = [rng.integers(0, 2, D) for _ in range(N)]
        pars = [parity(b, m) for b, m in zip(bits, masks)]
        # the row that changes (PINK) in the sensitivity beat: even parity, a masked 0 bit
        flip_i = next(i for i in range(N) if pars[i] == 0 and any(masks[i][j] and not bits[i][j] for j in range(D)))
        flip_j = next(j for j in range(D) if masks[flip_i][j] and not bits[flip_i][j])
        more_masks = [[random_mask(rng) for _ in range(N)] for _ in range(11)]

        # ============================================================ 0. interactive vs one-shot
        FY = 0.75
        divider = DashedLine([0, 2.55, 0], [0, -2.25, 0], color=S.GREY_DARK, stroke_width=2)
        t_left = S.text("Interactive", 34, S.WHITE).move_to([-3.3, 3.05, 0])
        t_right = S.text("Non-interactive", 34, S.WHITE).move_to([3.3, 3.05, 0])

        dbL = db_icon(w=1.15, rh=0.25).move_to([-5.6, FY, 0])
        dbL_lab = S.math("x", size=34, color=X_COLOR).next_to(dbL, DOWN, buff=0.15)
        cur = person_icon(S.WHITE, 1.0).move_to([-4.15, FY, 0])
        cur_lab = S.text("curator", 22, S.GREY).next_to(cur, DOWN, buff=0.15)
        ana = person_icon(S.GREY, 0.95).move_to([-1.05, FY, 0])
        ana_lab = S.text("analyst", 22, S.GREY).next_to(ana, DOWN, buff=0.15)
        capL = S.text("ask, answer, repeat", 24, S.GREY).move_to([-3.3, -1.75, 0])

        dbR = db_icon(w=1.15, rh=0.25).move_to([0.95, FY, 0])
        dbR_lab = S.math("x", size=34, color=X_COLOR).next_to(dbR, DOWN, buff=0.15)
        curR = person_icon(S.WHITE, 1.0).move_to([2.4, FY, 0])
        curR_lab = S.text("curator", 22, S.GREY).next_to(curR, DOWN, buff=0.15)
        sheet = release_sheet(np.random.default_rng(2), w=1.7, h=2.0).move_to([4.5, FY + 0.1, 0])
        sheet_lab = S.math("M(", "x", ")", size=34).next_to(sheet, UP, buff=0.15)
        sheet_lab[1].set_color(X_COLOR)
        users = VGroup(*[person_icon(S.GREY, 0.48) for _ in range(4)]).arrange(RIGHT, buff=0.36)
        users.move_to([4.5, -1.0, 0])
        user_arrows = VGroup(*[Arrow(u.get_top(), sheet.get_bottom() + RIGHT * (u.get_x() - sheet.get_x()) * 0.5,
                                     buff=0.08, color=S.GREY, stroke_width=2.5, tip_length=0.14,
                                     max_tip_length_to_length_ratio=0.3) for u in users])
        capR = S.text("publish once, walk away", 24, S.GREY).move_to([3.3, -1.75, 0])
        defn = S.math(r"\left|\ln\frac{\Pr[M(", "x", r")=t]}{\Pr[M(", "x'", r")=t]}\right|", r"\le",
                      r"\varepsilon", size=40)
        defn[1].set_color(X_COLOR)
        defn[3].set_color(XP_COLOR)
        defn[6].set_color(EPS_COLOR)
        qmark = S.text("?", 54, S.YELLOW)
        defn_q = VGroup(defn, qmark).arrange(RIGHT, buff=0.3).move_to([0, -2.95, 0])

        def trip(k):
            """One round of the interactive protocol: query f_k slides in, noisy answer a_k slides back."""
            q = tag(f"f_{k}").move_to([-3.2, FY + 0.5, 0])
            a = tag(f"a_{k}").move_to([-1.85, FY - 0.4, 0])
            return q, a

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(t_left, shift=DOWN * 0.2), FadeIn(t_right, shift=DOWN * 0.2), Create(divider),
                      run_time=0.8)
            self.play(FadeIn(VGroup(dbL, dbL_lab, cur, cur_lab), shift=RIGHT * 0.2),
                      FadeIn(VGroup(ana, ana_lab), shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("Statisticians")
            q1, a1 = trip(1)
            self.play(FadeIn(q1, shift=LEFT * 1.35), FadeIn(VGroup(dbR, dbR_lab, curR, curR_lab), shift=LEFT * 0.2),
                      run_time=1.0)
            self.play(FadeOut(q1, scale=0.5), FadeIn(a1, shift=RIGHT * 1.35), FadeIn(capL), run_time=1.0)
            q2, a2 = trip(2)                                   # ... and another: a stream of queries
            self.play(FadeOut(a1, scale=0.5), FadeIn(q2, shift=LEFT * 1.35), run_time=0.7)
            self.play(FadeOut(q2, scale=0.5), FadeIn(a2, shift=RIGHT * 1.35), run_time=0.7)
            self.play(FadeOut(a2, scale=0.5), run_time=0.3)
            vo.wait_until("sanitize the data")
            self.play(TransformFromCopy(dbR, sheet), run_time=1.0)
            self.play(FadeIn(sheet_lab, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("publish it")
            self.play(FadeOut(VGroup(curR, curR_lab), shift=LEFT * 0.6),
                      FadeOut(VGroup(dbR, dbR_lab), shift=LEFT * 0.6), FadeIn(capR), run_time=0.8)
            vo.wait_until("and let anyone")
            q3, a3 = trip(3)
            self.play(FadeIn(q3, shift=LEFT * 1.35),
                      LaggedStart(*[AnimationGroup(FadeIn(u, shift=UP * 0.2), GrowArrow(a))
                                    for u, a in zip(users, user_arrows)], lag_ratio=0.25), run_time=1.2)
            self.play(FadeOut(q3, scale=0.5), FadeIn(a3, shift=RIGHT * 1.35), run_time=0.7)
            vo.wait_until("Can that work")
            self.play(Write(defn), FadeOut(a3, scale=0.5), run_time=1.0)
            self.play(FadeIn(qmark, scale=1.4), run_time=0.4)

        # ============================================================ 1. parity queries
        table = bit_table(bits)
        table.move_to([-0.55, 0.05, 0])
        cells = [r[2] for r in table]
        digs = [r[3] for r in table]
        pcells = [r[4] for r in table]
        overlays = mask_overlays(cells, masks)
        x_lab = S.math("x", size=34, color=X_COLOR).next_to(table, UP, buff=0.12).align_to(table, LEFT).shift(RIGHT * 0.12)
        par_head = S.text("parity", 22, S.GREY).next_to(pcells[0], UP, buff=0.12)
        brace = Brace(cells[-1], DOWN, buff=0.1, color=S.GREY)
        brace_lab = S.math(r"d = 8\ \text{bits}", size=30, color=S.GREY).next_to(brace, DOWN, buff=0.1)
        legend = VGroup(Square(0.3, stroke_color=MASK, stroke_width=3).set_fill(MASK, 0.32),
                        S.text("mask: the bits that count", 24, MASK)).arrange(RIGHT, buff=0.15)
        legend.next_to(brace_lab, RIGHT, buff=0.9)
        qcard = query_card("How many rows have odd parity inside their own mask?", width=10.2)
        qcard.move_to([0.6, 2.95, 0])
        pdigs = [digit(p, 26, S.WHITE).move_to(pc).set_z_index(3) for p, pc in zip(pars, pcells)]
        count = S.math("f(", "x", ")", "=", str(sum(pars)), size=52)
        count[1].set_color(X_COLOR)
        count.move_to([4.6, 0.95, 0])
        # the paper's f_g(x) = sum_i r_i (.) x_i, with r_i (.) x_i = <r_i, x_i> mod 2
        formula = S.math("f(", "x", ")", "=", r"\sum_{i=1}^{n}", r"\big(", "r_i", r"\cdot", "x_i",
                         r"\bmod 2", r"\big)", size=40)
        formula[1].set_color(X_COLOR)
        formula[6].set_color(MASK)
        formula[8].set_color(X_COLOR)
        formula.move_to([-0.55, -3.05, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(t_right, divider, sheet, sheet_lab, users, user_arrows, capR, capL, defn_q,
                                     ana, ana_lab, t_left)), run_time=0.8)
            self.play(VGroup(cur, cur_lab).animate.move_to([-5.45, 0.55, 0]), run_time=0.8)
            vo.wait_until("Let each row")
            self.play(ReplacementTransform(dbL, VGroup(*[r[0] for r in table])),
                      ReplacementTransform(dbL_lab, x_lab), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(VGroup(r[1], r[2], r[3], r[4]), shift=RIGHT * 0.15) for r in table],
                                  lag_ratio=0.12), run_time=1.0)
            self.play(GrowFromCenter(brace), FadeIn(brace_lab), run_time=0.5)
            vo.wait_until("Here is a family")
            self.play(FadeIn(qcard, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("give each row")
            row_groups, k = [], 0
            for m in masks:
                c = int(m.sum())
                row_groups.append(VGroup(*overlays[k:k + c]))
                k += c
            self.play(LaggedStart(*[LaggedStart(*[FadeIn(o, scale=1.3) for o in g], lag_ratio=0.15)
                                    for g in row_groups], lag_ratio=0.3), run_time=1.8)
            self.play(FadeIn(legend, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("and count the rows")
            self.play(FadeIn(par_head), run_time=0.3)
            anims = []
            for i in range(N):
                ones = [digs[i][j] for j in range(D) if masks[i][j] and bits[i][j]]
                if ones:
                    anims.append(ReplacementTransform(VGroup(*[o.copy() for o in ones]), pdigs[i]))
                else:
                    anims.append(FadeIn(pdigs[i], scale=0.5))
            self.play(LaggedStart(*anims, lag_ratio=0.22), run_time=1.7)
            odd_rows = [i for i in range(N) if pars[i]]
            self.play(*[pcells[i].animate.set_stroke(S.WHITE, 3) for i in odd_rows],
                      *[Indicate(pdigs[i], color=S.WHITE, scale_factor=1.4) for i in odd_rows], run_time=0.5)
            self.play(TransformFromCopy(VGroup(*[pdigs[i] for i in odd_rows]), count[4]),
                      FadeIn(count[:4]), run_time=0.8)
            self.play(Write(formula), run_time=0.8)

            # sensitivity one: change one row (PINK) -> at most one parity changes -> count moves by <= 1
            vo.wait_until("Each query has")
            row = table[flip_i]
            hl = SurroundingRectangle(row, color=ALICE, buff=0.03, stroke_width=4)
            new_bit = digit(1).move_to(digs[flip_i][flip_j]).set_z_index(3)
            new_par = digit(1, 26, S.WHITE).move_to(pcells[flip_i]).set_z_index(3)
            old_bit = digit(0).move_to(digs[flip_i][flip_j]).set_z_index(3)
            old_par = digit(0, 26, S.WHITE).move_to(pcells[flip_i]).set_z_index(3)
            # one changed row makes the neighbour x' (ORANGE): its count is one more
            count2 = S.math("f(", "x'", ")", "=", str(sum(pars) + 1), size=52)
            count2[1].set_color(XP_COLOR)
            count2.next_to(count, DOWN, buff=0.4).align_to(count, LEFT)
            sens = S.math("S(f) = 1", size=44, color=SENS_COLOR).next_to(count2, DOWN, buff=0.5)
            sens.align_to(count, LEFT)
            self.play(Create(hl), row[1].animate.set_color(ALICE), run_time=0.4)
            self.play(Transform(digs[flip_i][flip_j], new_bit), Flash(digs[flip_i][flip_j], color=ALICE,
                                                                      flash_radius=0.3), run_time=0.45)
            self.play(Transform(pdigs[flip_i], new_par), pcells[flip_i].animate.set_stroke(S.WHITE, 3), run_time=0.4)
            self.play(TransformFromCopy(count, count2), run_time=0.6)
            self.play(FadeIn(sens, shift=UP * 0.15), run_time=0.3)
            vo.wait_until("so an interactive curator")
            # back to x: the curator answers the query on the real database
            self.play(Transform(digs[flip_i][flip_j], old_bit), Transform(pdigs[flip_i], old_par),
                      pcells[flip_i].animate.set_stroke(S.GREY, 1.5), row[1].animate.set_color(X_COLOR),
                      FadeOut(hl), run_time=0.45)
            answer = S.math(str(sum(pars)), r"\pm", r"1/", r"\varepsilon", size=40)
            answer[1:3].set_color(NOISE_COLOR)
            answer[3].set_color(EPS_COLOR)
            ans_frame = SurroundingRectangle(answer, color=S.GREY, buff=0.15, corner_radius=0.1, stroke_width=2)
            ans = VGroup(ans_frame, answer).next_to(cur_lab, DOWN, buff=0.4)
            self.play(TransformFromCopy(count[4], answer[0]), FadeIn(ans_frame), Indicate(cur, color=S.WHITE),
                      run_time=1.0)
            self.play(Write(answer[1:]), run_time=0.8)
            self.play(Circumscribe(answer[1:], color=NOISE_COLOR), run_time=vo.remaining(0.8))

        # ============================================================ 2. Theorem 3
        card0 = mask_card(masks, cell=0.13).move_to([0, 1.4, 0])
        others = VGroup(*[mask_card(mm, cell=0.13) for mm in more_masks])
        hand = VGroup(*others[:6], card0, *others[6:])         # card0 sits in the middle of the fan
        FAN_SPREAD = 0.55
        fan(hand, np.array([0, 1.4, 0]), radius=7.5, spread=FAN_SPREAD)
        th0 = -FAN_SPREAD + 2 * FAN_SPREAD * 6 / 11            # card0's tilt in the fan
        small_scale = 0.62 / card0.height
        fan_lab = S.text("every choice of masks is another query", 28, S.GREY).move_to([0, -0.85, 0])
        bright = {0, 1, 3, 4, 6, 7, 9, 11}                      # 8 of 12 = the 2/3 the theorem covers
        two_thirds = S.text("for at least 2/3 of them ...", 30, S.WHITE).move_to([0, -0.85, 0])

        # the two worlds: same masks as card0
        even_bits = [sample_row(rng, m, 0) for m in masks]
        odd_bits = [sample_row(rng, m, 1) for m in masks]
        tab_e = mini_table(even_bits, masks, EVEN).move_to([-3.55, 1.95, 0])
        tab_o = mini_table(odd_bits, masks, ODD).move_to([-3.55, -0.85, 0])
        lab_e = VGroup(S.text("every row", 24, EVEN), S.text("even", 24, EVEN),
                       S.math(r"\text{answer } 0", size=30, color=EVEN)).arrange(DOWN, buff=0.08)
        lab_e.next_to(tab_e, LEFT, buff=0.25)
        lab_o = VGroup(S.text("every row", 24, ODD), S.text("odd", 24, ODD),
                       S.math(r"\text{answer } n", size=30, color=ODD)).arrange(DOWN, buff=0.08)
        lab_o.next_to(tab_o, LEFT, buff=0.25)
        q_small_pos = np.array([-3.55, 0.55, 0])
        m_e = m_box().move_to([-1.35, 1.95, 0])
        m_o = m_box().move_to([-1.35, -0.85, 0])
        a_e = Arrow(tab_e.get_right(), m_e.get_left(), buff=0.06, color=EVEN, stroke_width=3, tip_length=0.15)
        a_o = Arrow(tab_o.get_right(), m_o.get_left(), buff=0.06, color=ODD, stroke_width=3, tip_length=0.15)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 0.28, 0.1], x_length=5.4, y_length=2.3, tips=False,
                  axis_config={"color": S.GREY, "stroke_width": 2, "include_ticks": False}).move_to([3.6, 0.6, 0])
        axis = ax.x_axis                                          # only the output axis, as in S05
        ax_lab = S.text("output of M", 22, S.GREY).next_to(axis, DOWN, buff=0.15)

        def p0(t):
            return 0.55 * gaussian_pdf(t, 3.4, 0.95) + 0.45 * gaussian_pdf(t, 6.6, 1.25)

        def p1(t):
            return 0.535 * gaussian_pdf(t, 3.47, 0.95) + 0.465 * gaussian_pdf(t, 6.63, 1.27)

        c_e = ax.plot(p0, x_range=[0, 10, 0.02], color=EVEN, stroke_width=5)
        c_o = ax.plot(p1, x_range=[0, 10, 0.02], color=ODD, stroke_width=4)
        sliver = lens(ax, p0, p1, EVEN, ODD)
        b_e = Arrow(m_e.get_right(), ax.c2p(1.6, 0.17), buff=0.1, color=EVEN, stroke_width=3, tip_length=0.15)
        b_o = Arrow(m_o.get_right(), ax.c2p(1.6, 0.02), buff=0.1, color=ODD, stroke_width=3, tip_length=0.15)
        sd_lab = S.text("statistical distance ≈ 0", 28, S.WHITE).next_to(ax, UP, buff=0.2)

        thm_math = S.math(r"\text{statistical distance}", "=", r"O\!\left(n^{4/3}\,", r"\varepsilon", r"^{2/3}",
                          r"\,2^{-d/3}\right)", size=36)
        thm_math[3].set_color(EPS_COLOR)
        thm_line = VGroup(S.text("for at least 2/3 of the queries:", 28, S.WHITE), thm_math).arrange(RIGHT, buff=0.3)
        thm = statement_card("Theorem 3", thm_line).move_to([0, -2.78, 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(cur, cur_lab, ans, count, count2, sens, formula, qcard, legend, brace,
                                     brace_lab, par_head, x_lab)), run_time=0.6)
            self.play(FadeOut(VGroup(table, *pdigs, overlays)), FadeIn(card0[0]), FadeIn(card0[2]),
                      TransformFromCopy(overlays, card0[1]), run_time=1.1)
            self.add(card0)
            self.play(LaggedStart(*[FadeIn(c, target_position=card0.get_center(), scale=0.6) for c in others],
                                  lag_ratio=0.08), FadeIn(fan_lab), run_time=1.5)
            vo.wait_until("Theorem 3")
            self.play(*[hand[i].animate.set_opacity(0.22) for i in range(12) if i not in bright],
                      *[hand[i][0].animate.set_stroke(S.WHITE, 3) for i in bright],
                      ReplacementTransform(fan_lab, two_thirds), run_time=1.3)
            self.play(Indicate(VGroup(*[hand[i] for i in sorted(bright)]), color=S.WHITE, scale_factor=1.04),
                      run_time=1.0)
            vo.wait_until("the release looks")
            self.play(FadeOut(VGroup(*[hand[i] for i in range(12) if i != 6]), two_thirds),
                      card0.animate.rotate(th0).scale(small_scale).move_to(q_small_pos), run_time=1.0)
            self.play(FadeIn(VGroup(m_e, m_o)), Create(axis), FadeIn(ax_lab), run_time=0.8)
            vo.wait_until("for a random database")
            self.play(FadeIn(tab_e[0]), FadeIn(tab_e[1]), TransformFromCopy(card0[1], tab_e[2]), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in tab_e[3]], lag_ratio=0.12),
                      FadeIn(lab_e, shift=RIGHT * 0.15), run_time=0.9)
            self.play(GrowArrow(a_e), run_time=0.4)
            self.play(GrowArrow(b_e), Create(c_e), run_time=1.1)
            vo.wait_until("as for one where")
            self.play(FadeIn(tab_o[0]), FadeIn(tab_o[1]), TransformFromCopy(card0[1], tab_o[2]),
                      LaggedStart(*[FadeIn(d, scale=0.5) for d in tab_o[3]], lag_ratio=0.1),
                      FadeIn(lab_o, shift=RIGHT * 0.15), run_time=1.0)
            self.play(GrowArrow(a_o), run_time=0.3)
            self.play(GrowArrow(b_o), Create(c_o), run_time=1.0)
            self.play(FadeIn(sliver), FadeIn(sd_lab, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("The most extreme")
            self.play(FadeIn(thm, shift=UP * 0.2), run_time=0.8)
            self.play(Indicate(lab_e[2], color=EVEN, scale_factor=1.25),
                      Indicate(lab_o[2], color=ODD, scale_factor=1.25), run_time=0.9)
            vo.wait_until("and it cannot be seen")
            self.play(Indicate(sd_lab, color=S.WHITE), Indicate(VGroup(c_e, c_o), scale_factor=1.04), run_time=1.0)

            # how big must n be?  every 4 extra bits per row doubles it
            vo.wait_until("unless the database")
            thresh = S.math(r"\text{tiny unless}\quad n", r"\gtrsim", r"2^{d/4}", "/", r"\sqrt{\varepsilon}", size=46)
            thresh[4][-1].set_color(EPS_COLOR)
            thresh.move_to([0, 1.38, 0])
            self.play(FadeOut(VGroup(tab_e, tab_o, lab_e, lab_o, card0, m_e, m_o, a_e, a_o, b_e, b_o, axis, ax_lab,
                                     c_e, c_o, sliver, sd_lab)),
                      thm.animate.move_to([0, 2.72, 0]), run_time=0.8)
            self.play(Write(thresh), run_time=1.0)

            cellw = 0.36
            bitrow = VGroup(*[Square(cellw, stroke_color=S.GREY, stroke_width=1.5).set_fill(S.GREY_DARK, 1)
                              for _ in range(16)]).arrange(RIGHT, buff=0).move_to([-3.4, -1.0, 0])
            bitrow.align_to([-6.2, 0, 0], LEFT)
            d_lab = VGroup(S.text("bits per row:", 26, S.GREY), S.math("d = 8", size=38)).arrange(RIGHT, buff=0.2)
            d_lab.next_to(bitrow, UP, buff=0.3).align_to(bitrow, LEFT)
            bars = VGroup(*[Rectangle(width=2.2, height=0.13, stroke_width=0).set_fill(S.WHITE, 0.8)
                            for _ in range(16)]).arrange(UP, buff=0.05)
            bars.move_to([2.5, 0, 0]).align_to([0, -3.4, 0], DOWN)
            n_lab = S.text("rows needed", 26, S.GREY).move_to([5.1, -1.7, 0])
            n_val = S.math(r"\sim 2^{8/4} = 4", size=40).next_to(n_lab, DOWN, buff=0.2).align_to(n_lab, LEFT)
            vo.wait_until("roughly, every four")
            self.play(FadeIn(bitrow[:8]), FadeIn(d_lab), FadeIn(bars[:4]), FadeIn(n_lab), FadeIn(n_val), run_time=0.7)
            for lo, hi, dv, nv in [(8, 12, 12, 8), (12, 16, 16, 16)]:
                plus = S.text("+4 bits", 26, S.WHITE).next_to(bitrow[lo:hi], DOWN, buff=0.15)
                new_d = S.math(f"d = {dv}", size=38).move_to(d_lab[1], aligned_edge=LEFT)
                new_n = S.math(rf"\sim 2^{{{dv}/4}} = {nv}", size=40).move_to(n_val, aligned_edge=LEFT)
                self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in bitrow[lo:hi]], lag_ratio=0.15),
                          FadeIn(plus), Transform(d_lab[1], new_d), run_time=0.8)
                old = bars[:nv // 2]
                x2 = S.math(r"\times 2", size=40).next_to(bars[nv // 2:nv], LEFT, buff=0.3)
                self.play(TransformFromCopy(old, bars[nv // 2:nv]), Transform(n_val, new_n), FadeOut(plus),
                          FadeIn(x2, shift=UP * 0.2), run_time=0.9)
                self.play(FadeOut(x2), run_time=0.2)
        keep_fade = VGroup(thm, thresh, bitrow, d_lab, bars, n_lab, n_val)

        # ============================================================ 3. ponder: why not ask the curator?
        cur2 = person_icon(S.WHITE, 0.9).move_to([-5.3, 1.4, 0])
        cur2_lab = S.text("curator", 22, S.GREY).next_to(cur2, DOWN, buff=0.15)
        deck_rng = np.random.default_rng(23)
        deck = VGroup(*[mask_card([random_mask(deck_rng) for _ in range(N)]).scale(0.8) for _ in range(12)])
        for i, c in enumerate(deck):
            c.move_to([-1.7 + 0.04 * i, 1.4 + 0.04 * i, 0])
        deck_arrow = Arrow([-2.3, 1.4, 0], [-4.6, 1.4, 0], buff=0, color=S.GREY, stroke_width=3, tip_length=0.18)
        deck_lab = S.text("all of them?", 24, S.GREY).next_to(deck, DOWN, buff=0.3)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(keep_fade), run_time=0.5)
            self.play(FadeIn(VGroup(cur2, cur2_lab), shift=RIGHT * 0.2),
                      LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in deck], lag_ratio=0.05), run_time=0.8)
            vo.wait_until("couldn't an analyst")
            self.play(GrowArrow(deck_arrow), FadeIn(deck_lab), run_time=0.8)
            self.play(Wiggle(deck, scale_value=1.05), run_time=vo.remaining(0.8))
        card = ponder_at(self, "Couldn't an analyst ask the\ninteractive curator all of\nthese queries too?",
                         seconds=10, pos=[3.3, 0.6, 0], width=6.2)

        # ============================================================ 4. the budget runs out
        t_left2 = S.text("Interactive", 34, S.WHITE).move_to([-3.3, 3.05, 0])
        t_right2 = S.text("Non-interactive", 34, S.WHITE).move_to([3.3, 3.05, 0])
        divider2 = DashedLine([0, 2.55, 0], [0, -3.2, 0], color=S.GREY_DARK, stroke_width=2)
        bar = budget_bar().move_to([-4.6, -0.55, 0])                       # the S09 budget bar
        bar_lab = S.math(r"\text{privacy budget }", r"\varepsilon", size=32, color=EPS_COLOR)
        bar_lab.next_to(bar, UP, buff=0.14).align_to(bar, LEFT)
        slots = [np.array([-5.85 + 0.93 * k, -1.6, 0]) for k in range(5)]
        ticks = VGroup(*[sym("✓", 30).move_to(p + DOWN * 0.6) for p in slots])
        few_lab = S.text("the few questions actually asked", 24, S.GREY).move_to([-3.95, -2.8, 0])
        refused_pos = np.array([-3.35, 1.4, 0])
        refused = S.text("refused", 30, NOISE_COLOR).move_to(refused_pos + UP * 0.75)   # as in S09
        sheet2 = release_sheet(np.random.default_rng(2)).move_to([1.85, 0.45, 0])
        sheet2_lab = S.math("M(", "x", ")", size=34).next_to(sheet2, UP, buff=0.15)
        sheet2_lab[1].set_color(X_COLOR)
        grid_rng = np.random.default_rng(31)
        qgrid = VGroup(*[mask_card([random_mask(grid_rng) for _ in range(N)]).scale(0.75) for _ in range(12)])
        qgrid.arrange_in_grid(rows=4, cols=3, buff=(0.22, 0.25)).move_to([4.95, 0.45, 0])
        links = VGroup(*[Line(sheet2.get_right(), c.get_left(), color=S.GREY, stroke_width=1.5) for c in qgrid])
        links.set_z_index(-1)                                             # run behind the query cards
        all_lab = S.text("ready for all of them, at once", 24, S.GREY).move_to([3.3, -2.2, 0])
        breaks = x_mark(sheet2, width=8, pad=0.15)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card), FadeOut(VGroup(deck_arrow, deck_lab)), FadeIn(VGroup(bar, bar_lab)),
                      FadeIn(t_left2), run_time=0.6)
            for k in range(6):
                c = deck[-1 - k]
                self.play(c.animate.scale(0.5).move_to(cur2.get_center() + RIGHT * 0.75), run_time=0.2)
                if k < 5:
                    self.play(c.animate.scale(2 * 0.75 / 0.8).move_to(slots[k]),
                              bar[1][4 - k].animate.set_fill(opacity=0.0), run_time=0.26)
                else:
                    self.play(c.animate.scale(2).move_to(refused_pos), Indicate(bar[0], color=NOISE_COLOR,
                                                                                 scale_factor=1.04), run_time=0.3)
                    cross = x_mark(c, pad=0.05)
                    self.play(Create(cross), FadeIn(refused, scale=1.3), run_time=0.4)
            vo.wait_until("the few questions")
            self.play(LaggedStart(*[FadeIn(t, scale=1.4) for t in ticks], lag_ratio=0.15),
                      VGroup(*deck[:6]).animate.set_opacity(0.25), run_time=1.0)
            vo.wait_until("chosen later")
            self.play(FadeIn(few_lab, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("A published release")
            self.play(Create(divider2), FadeIn(t_right2), FadeIn(sheet2), FadeIn(sheet2_lab), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in qgrid], lag_ratio=0.06), run_time=1.2)
            vo.wait_until("so it must be ready")
            self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.05), FadeIn(all_lab), run_time=1.3)
            vo.wait_until("That is where")
            self.play(Create(breaks), Wiggle(sheet2), run_time=0.9)

        # ============================================================ 5. proof idea
        ptag_t = S.text("proof idea", 22, S.GREY)
        ptag = VGroup(SurroundingRectangle(ptag_t, color=S.GREY, buff=0.1, corner_radius=0.08, stroke_width=1.5),
                      ptag_t).move_to([-5.6, 3.3, 0])
        # fact 1: privacy -> every possible row looks almost alike to M
        f1_t = S.text("1 · every row looks almost alike", 26, S.WHITE).move_to([-3.45, 2.45, 0])
        f1_rows_bits = [[0, 0, 1, 0, 1, 1, 0, 1], [1, 1, 1, 0, 0, 0, 1, 0], [0, 1, 0, 1, 1, 1, 1, 0]]
        h_rng = np.random.default_rng(4)
        base = np.array([0.35, 0.72, 0.55, 0.3, 0.5])
        f1 = VGroup()
        for k, rb in enumerate(f1_rows_bits):
            y = 1.45 - 1.05 * k
            rcells = VGroup(*[Square(0.32, stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(S.GREY_DARKER, 1)
                              for _ in range(D)]).arrange(RIGHT, buff=0).move_to([-5.0, y, 0])
            rdig = VGroup(*[digit(v, 22).move_to(c) for v, c in zip(rb, rcells)])
            arr = Arrow([-3.6, y, 0], [-2.55, y, 0], buff=0, color=S.GREY, stroke_width=3, tip_length=0.15)
            arr_m = S.math("M", size=28).next_to(arr, UP, buff=0.04)
            hs = base * (1 + 0.07 * h_rng.uniform(-1, 1, 5))
            hist = VGroup(*[Rectangle(width=0.22, height=h, stroke_width=0).set_fill(S.WHITE, 0.75) for h in hs])
            hist.arrange(RIGHT, buff=0.06, aligned_edge=DOWN).move_to([-1.55, y, 0]).align_to([0, y - 0.38, 0], DOWN)
            base_line = Line([-2.3, y - 0.38, 0], [-0.8, y - 0.38, 0], color=S.GREY, stroke_width=1.5)
            f1.add(VGroup(rcells, rdig, arr, arr_m, hist, base_line))
        vdots = S.math(r"\vdots", size=36, color=S.GREY).move_to([-5.0, -1.55, 0])
        f1_cap = S.math(r"\text{ratios within } e^{\pm", r"\varepsilon", "}", size=32).move_to([-3.35, -2.25, 0])
        f1_cap[1].set_color(EPS_COLOR)
        # fact 2: a random mask splits {0,1}^8 into two salt-and-pepper halves
        f2_t = S.text("2 · a random mask halves all rows", 26, S.WHITE).move_to([3.3, 2.45, 0])
        perm = np.random.default_rng(8).permutation(256)
        strings = [np.array([(int(v) >> (7 - j)) & 1 for j in range(D)]) for v in perm]
        dots = VGroup(*[Dot(radius=0.055, color=S.GREY) for _ in range(256)])
        dots.arrange_in_grid(rows=16, cols=16, buff=0.085).move_to([3.0, -0.2, 0])
        f2_masks = [np.array([1, 0, 1, 1, 0, 0, 1, 0]), np.array([0, 1, 1, 0, 0, 1, 0, 1]),
                    np.array([1, 1, 0, 0, 1, 0, 0, 1])]

        def mask_strip(m):
            cells_ = VGroup(*[Square(0.3, stroke_color=S.GREY_DARK, stroke_width=1.5)
                              .set_fill(MASK if v else S.GREY_DARKER, 0.85 if v else 1) for v in m])
            return cells_.arrange(RIGHT, buff=0).move_to([3.4, 1.62, 0])

        strip = mask_strip(f2_masks[0])
        strip_lab = S.text("mask r", 24, MASK).next_to(strip, LEFT, buff=0.2)
        all_lab2 = S.math(r"\text{all } 2^8 = 256 \text{ possible rows}", size=30, color=S.GREY)
        all_lab2.next_to(dots, DOWN, buff=0.25)
        legend2 = VGroup(VGroup(Dot(radius=0.08, color=EVEN), S.text("even", 24, EVEN)).arrange(RIGHT, buff=0.12),
                         VGroup(Dot(radius=0.08, color=ODD), S.text("odd", 24, ODD)).arrange(RIGHT, buff=0.12))
        legend2.arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(dots, RIGHT, buff=0.35)
        poll_lab = S.text("even half ≈ a random poll of all rows", 26, EVEN).move_to(all_lab2)

        def colour_by(m):
            return [dots[g].animate.set_color(EVEN if parity(strings[g], m) == 0 else ODD) for g in range(256)]

        # the hybrid chain, in S08's look: random rows -> even rows (top lane), -> odd rows (bottom lane)
        CH = 4
        ch_rng = np.random.default_rng(5)
        ch_masks = [random_mask(ch_rng) for _ in range(CH)]
        R_bits = [ch_rng.integers(0, 2, D) for _ in range(CH)]
        E_bits = [sample_row(ch_rng, m, 0) for m in ch_masks]
        O_bits = [sample_row(ch_rng, m, 1) for m in ch_masks]

        def chain_db(states, frame_color=S.GREY, newest=None, width=1.2, row_h=0.26):
            """S08's mini_db with each row's bits drawn in; swapped rows tinted (the newest one brightest)."""
            rws = VGroup()
            for k, st in enumerate(states):
                b = {"r": R_bits, "e": E_bits, "o": O_bits}[st][k]
                col = {"r": S.GREY, "e": EVEN, "o": ODD}[st]
                box = Rectangle(width=width, height=row_h, stroke_color=S.GREY_DARK, stroke_width=1.5)
                box.set_fill(S.GREY_DARKER, 1) if st == "r" else box.set_fill(col, 0.5 if k == newest else 0.2)
                icon = person_icon(col, height=row_h * 0.7).move_to(box.get_left() + RIGHT * 0.17)
                cells = VGroup(*[Square(0.085, stroke_width=0).set_fill(S.WHITE if v else S.BG, 0.9 if v else 0.7)
                                 for v in b]).arrange(RIGHT, buff=0.012).next_to(icon, RIGHT, buff=0.1)
                rws.add(VGroup(box, icon, cells))
            rws.arrange(DOWN, buff=0)
            frame = SurroundingRectangle(rws, buff=0.06, color=frame_color, stroke_width=2.5, corner_radius=0.06)
            return VGroup(frame, rws)

        LY, XS = 1.45, [-3.2, -1.15, 0.55, 2.25]       # lane height; x of: 1 swap, 2 swaps, ..., n swaps
        rand_db = chain_db("rrrr").move_to([-5.5, 0, 0])
        lab_rand = S.text("random rows", 24, S.GREY).next_to(rand_db, DOWN, buff=0.18)

        def lane(key, sgn, col):
            y = sgn * LY
            n1 = chain_db(key + "rrr", newest=0).move_to([XS[0], y, 0])
            n2 = chain_db(key * 2 + "rr", newest=1).move_to([XS[1], y, 0])
            dots_ = S.math(r"\cdots", size=40, color=S.GREY).move_to([XS[2], y, 0])
            nN = chain_db(key * CH, frame_color=col, newest=CH - 1).move_to([XS[3], y, 0])
            kw = dict(color=S.GREY, stroke_width=3, tip_length=0.14, max_tip_length_to_length_ratio=0.35)
            arrs = [Arrow(rand_db.get_right() + UP * 0.32 * sgn, n1.get_left(), buff=0.1, **kw),
                    Arrow(n1.get_right(), n2.get_left(), buff=0.1, **kw),
                    Arrow(n2.get_right(), dots_.get_left(), buff=0.12, **kw),
                    Arrow(dots_.get_right(), nN.get_left(), buff=0.12, **kw)]
            off = np.array([-0.32, 0.3, 0]) if sgn > 0 else np.array([0.34, 0.22, 0])   # keep clear of labels
            sig = VGroup(S.math(r"+\sigma", size=30).move_to(arrs[0].get_center() + off),
                         *[S.math(r"+\sigma", size=30).next_to(a, UP, buff=0.1) for a in arrs[1:]])
            return [n1, n2, dots_, nN], arrs, sig

        top_nodes, top_arrs, top_sig = lane("e", 1, EVEN)
        bot_nodes, bot_arrs, bot_sig = lane("o", -1, ODD)
        lab_even = S.text("every row even", 24, EVEN).next_to(top_nodes[3], UP, buff=0.15)
        lab_odd = S.text("every row odd", 24, ODD).next_to(bot_nodes[3], DOWN, buff=0.15)
        nsig_top = S.math(r"n \text{ swaps: at most } n\sigma", size=32).move_to([4.8, LY + 0.1, 0])
        tiny_lab = S.text("tiny, unless n is huge", 24, S.GREY).next_to(nsig_top, DOWN, buff=0.15)
        nsig_bot = S.math(r"\text{at most } n\sigma", size=32).move_to([4.8, -LY, 0])
        both = DoubleArrow(top_nodes[3].get_bottom(), bot_nodes[3].get_top(), buff=0.08, color=S.WHITE,
                           stroke_width=3, tip_length=0.16)
        both_lab = S.math(r"\text{even vs odd: at most } 2n\sigma", size=32).next_to(both, RIGHT, buff=0.3)
        bound = S.math(r"2n\sigma", "=", r"O\!\left(n^{4/3}\,", r"\varepsilon", r"^{2/3}", r"\,2^{-d/3}\right)",
                       size=36)
        bound[3].set_color(EPS_COLOR)
        bound_lab = S.text("= Theorem 3's bound", 26, S.GREY)
        bound_line = VGroup(bound, bound_lab).arrange(RIGHT, buff=0.3).move_to([0, -3.15, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
            # two facts: both headings appear dim, each lights up when it is spoken
            f1_t.set_opacity(0.3)
            f2_t.set_opacity(0.3)
            self.play(FadeIn(ptag, shift=DOWN * 0.15), run_time=0.5)
            self.play(LaggedStart(FadeIn(f1_t, shift=DOWN * 0.15), FadeIn(f2_t, shift=DOWN * 0.15), lag_ratio=0.4),
                      run_time=0.8)
            vo.wait_until("Privacy forces")
            self.play(f1_t.animate.set_opacity(1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(VGroup(g[0], g[1]), shift=RIGHT * 0.2) for g in f1], lag_ratio=0.2),
                      FadeIn(vdots), run_time=0.9)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(g[2]), FadeIn(g[3]), Create(g[5]),
                                                   GrowFromEdge(g[4], DOWN)) for g in f1], lag_ratio=0.25),
                      run_time=1.6)
            self.play(Write(f1_cap), run_time=0.8)
            vo.wait_until("And a random mask")
            self.play(f2_t.animate.set_opacity(1), FadeIn(dots), FadeIn(all_lab2), run_time=0.8)
            self.play(FadeIn(strip), FadeIn(strip_lab), run_time=0.5)
            self.play(*colour_by(f2_masks[0]), FadeIn(legend2), run_time=1.0)
            vo.wait_until("mixed like salt")
            for m in f2_masks[1:]:
                self.play(Transform(strip, mask_strip(m)), *colour_by(m), run_time=0.7)
            vo.wait_until("so the even half")
            odd_dots = [dots[g] for g in range(256) if parity(strings[g], f2_masks[-1]) == 1]
            self.play(*[d.animate.set_opacity(0.12) for d in odd_dots], ReplacementTransform(all_lab2, poll_lab),
                      legend2[1].animate.set_opacity(0.3), run_time=1.0)
            self.play(Indicate(poll_lab, color=EVEN, scale_factor=1.05), run_time=0.9)

            vo.wait_until("Then the chain trick")
            self.play(FadeOut(VGroup(f1_t, f1, vdots, f1_cap, f2_t, dots, strip, strip_lab, legend2, poll_lab)),
                      run_time=0.6)
            self.play(FadeIn(rand_db, scale=0.85), FadeIn(lab_rand), run_time=0.6)
            vo.wait_until("and swap them")
            prev = rand_db
            for k in (0, 1):
                node = top_nodes[k]
                self.play(GrowArrow(top_arrs[k]), TransformFromCopy(prev, node), run_time=0.5)
                self.play(Indicate(node[1][k][0], color=ALICE, scale_factor=1.15), run_time=0.3)
                prev = node
            self.play(GrowArrow(top_arrs[2]), FadeIn(top_nodes[2]), run_time=0.3)
            self.play(GrowArrow(top_arrs[3]), TransformFromCopy(prev, top_nodes[3]),
                      FadeIn(lab_even, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Each swap")
            self.play(LaggedStart(*[FadeIn(sg, shift=DOWN * 0.1) for sg in top_sig], lag_ratio=0.25), run_time=0.8)
            vo.wait_until("and unless n is huge")
            self.play(FadeIn(nsig_top, shift=LEFT * 0.2), run_time=0.7)
            self.play(FadeIn(tiny_lab), run_time=0.5)
            self.play(LaggedStart(*[Indicate(sg, color=S.WHITE) for sg in top_sig], lag_ratio=0.25), run_time=1.0)
            vo.wait_until("The same goes")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(nd) if nd is bot_nodes[2]
                                                   else TransformFromCopy(rand_db, nd))
                                    for a, nd in zip(bot_arrs, bot_nodes)], lag_ratio=0.3),
                      FadeIn(bot_sig), run_time=1.3)
            self.play(FadeIn(lab_odd, shift=UP * 0.1), FadeIn(nsig_bot, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("so both databases")
            self.play(GrowFromCenter(both), FadeIn(both_lab, shift=LEFT * 0.2), run_time=0.7)
            self.play(Write(bound_line), Indicate(rand_db, color=S.WHITE), run_time=1.0)

        # ============================================================ 6. randomized response
        rr_rng = np.random.default_rng(17)
        rr_bits = [rr_rng.integers(0, 2, D) for _ in range(4)]
        flips = [rr_rng.random(D) < 0.3 for _ in range(4)]
        rr_title = S.text("Randomized response", 34, S.WHITE).move_to([-1.45, 3.2, 0])
        big_coin = coin(0.3).move_to([-1.4, 2.5, 0])
        h_own = S.text("own row", 24, S.GREY).move_to([-3.95, 2.5, 0])
        h_pub = S.text("published", 24, S.GREY).move_to([1.05, 2.5, 0])
        people, raws, coins, arrows_rr, pubs, raw_cells = VGroup(), VGroup(), VGroup(), VGroup(), VGroup(), []
        for k in range(4):
            y = 1.75 - 0.78 * k
            p = person_icon(S.GREY, 0.5).move_to([-6.05, y, 0])
            cl = VGroup(*[Square(0.37, stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(S.GREY_DARKER, 1)
                          for _ in range(D)]).arrange(RIGHT, buff=0).move_to([-3.95, y, 0])
            dg = VGroup(*[digit(v, 24).move_to(c) for v, c in zip(rr_bits[k], cl)]).set_z_index(3)
            cn = coin(0.18).move_to([-1.4, y, 0])
            ar = Arrow([-1.1, y, 0], [-0.55, y, 0], buff=0, color=S.GREY, stroke_width=2.5, tip_length=0.12,
                       max_tip_length_to_length_ratio=0.4)
            pc = cl.copy().move_to([1.05, y, 0])
            pd = VGroup(*[digit(int(v) ^ int(f), 24, NOISE_COLOR if f else None).move_to(c)
                          for v, f, c in zip(rr_bits[k], flips[k], pc)]).set_z_index(3)
            people.add(p)
            raws.add(VGroup(cl, dg))
            raw_cells.append(cl)
            coins.add(cn)
            arrows_rr.add(ar)
            pubs.add(VGroup(pc, pd))
        nobody = VGroup(person_icon(S.GREY, 0.8), db_icon(S.GREY, w=0.8, n=4, rh=0.18)).arrange(RIGHT, buff=0.25)
        nobody.move_to([4.75, 1.2, 0])
        nobody_x = Cross(nobody, stroke_color=NOISE_COLOR, stroke_width=6, scale_factor=1.1)
        nobody_lab = S.text("nobody holds\nthe raw data", 24, S.GREY).next_to(nobody, DOWN, buff=0.35)
        same_mask = np.array([0, 1, 0, 1, 1, 0, 0, 1])
        same_over = mask_overlays(raw_cells, [same_mask] * 4)
        same_lab = S.text("same mask for every row", 24, MASK).move_to([-3.95, -1.15, 0])
        p2_math = S.math(r"n", r"\gtrsim", r"2^{d/3}", "/", r"\varepsilon", r"^{2/3}", size=40)
        p2_math[4].set_color(EPS_COLOR)
        p2_line = VGroup(S.text("for most masks, the odd count can't be estimated unless", 28, S.WHITE),
                         p2_math).arrange(RIGHT, buff=0.3)
        prop2 = statement_card("Proposition 2", p2_line).move_to([0, -2.65, 0])

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
            self.play(FadeIn(big_coin, shift=RIGHT * 2.5 + DOWN * 0.5), FadeIn(rr_title), run_time=0.6)
            self.play(Rotate(big_coin, angle=2 * PI, axis=UP), run_time=0.6)
            vo.wait_until("where each person")
            self.play(LaggedStart(*[FadeIn(VGroup(p, r), shift=RIGHT * 0.2) for p, r in zip(people, raws)],
                                  lag_ratio=0.15), FadeIn(h_own), run_time=1.0)
            self.play(TransformFromCopy(VGroup(*[big_coin.copy() for _ in range(4)]), coins), run_time=0.7)
            self.play(*[Rotate(c, angle=2 * PI, axis=UP) for c in coins],
                      *[GrowArrow(a) for a in arrows_rr],
                      *[TransformFromCopy(r, p) for r, p in zip(raws, pubs)], FadeIn(h_pub), run_time=1.2)
            vo.wait_until("so nobody holds")
            self.play(FadeIn(nobody), run_time=0.5)
            self.play(Create(nobody_x), FadeIn(nobody_lab), run_time=0.8)
            vo.wait_until("is even more limited")
            self.play(*[Rotate(c, angle=2 * PI, axis=UP) for c in coins], Indicate(VGroup(*[p[1] for p in pubs]), color=NOISE_COLOR), run_time=1.0)
            vo.wait_until("even when every row")
            self.play(LaggedStart(*[FadeIn(o, scale=1.3) for o in same_over], lag_ratio=0.04),
                      FadeIn(same_lab, shift=UP * 0.15), run_time=1.2)
            vo.wait_until("for most masks")
            self.play(FadeIn(prop2, shift=UP * 0.2), run_time=1.0)
            vo.wait_until("unless n is")
            self.play(Circumscribe(p2_math, color=S.WHITE), run_time=1.2)

        # ============================================================ 7. the quantifiers
        q_title = S.text("Careful with the quantifiers", 40, S.WHITE).move_to([0, 3.0, 0])
        R1, R2 = 1.45, -0.55
        one_card = mask_card(masks, cell=0.13).move_to([-5.4, R1, 0])
        one_sheet = release_sheet(np.random.default_rng(3), w=1.0, h=1.2).move_to([-3.45, R1, 0])
        one_arr = Arrow(one_card.get_right(), one_sheet.get_left(), buff=0.12, color=S.GREY, stroke_width=3,
                        tip_length=0.15)
        line1 = VGroup(S.text("Any ONE query, known in advance", 32, S.WHITE),
                       S.text("→  easy to publish for", 30, S.GREY)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        line1.next_to(one_sheet, RIGHT, buff=0.55)
        tick1 = sym("✓", 56, TICK).move_to([5.95, R1, 0])
        many_rng = np.random.default_rng(41)
        many = VGroup(*[mask_card([random_mask(many_rng) for _ in range(N)]).scale(0.7) for _ in range(5)])
        fan(many, np.array([-5.4, R2 + 0.3, 0]), radius=3.0, spread=0.22)
        two_sheet = release_sheet(np.random.default_rng(4), w=1.0, h=1.2).move_to([-3.45, R2, 0])
        two_links = VGroup(*[Line(two_sheet.get_left(), c.get_right(), color=S.GREY, stroke_width=1.5) for c in many])
        two_links.set_z_index(-1)
        line2 = VGroup(S.text("ONE private release for MOST queries", 32, S.WHITE),
                       S.text("→  impossible unless n is huge", 30, S.GREY)).arrange(DOWN, buff=0.14,
                                                                                   aligned_edge=LEFT)
        line2.next_to(two_sheet, RIGHT, buff=0.55)
        cross2 = sym("✗", 56, NOISE_COLOR).move_to([5.95, R2, 0])
        cur3 = person_icon(S.WHITE, 0.75)
        loop = Arc(radius=0.62, start_angle=PI * 0.62, angle=-2 * PI * 0.86, color=S.WHITE, stroke_width=3)
        loop.add_tip(tip_length=0.16)
        loop.move_to(cur3)
        lesson_t = S.text("Want broad accuracy + strong privacy?  Keep a curator in the loop.", 32, S.WHITE)
        lesson = VGroup(VGroup(cur3, loop), lesson_t).arrange(RIGHT, buff=0.45)
        if lesson.width > 12.0:
            lesson.scale_to_fit_width(12.0)
        lesson.move_to([0, -2.65, 0])
        lesson_box = SurroundingRectangle(lesson, color=EPS_COLOR, buff=0.25, corner_radius=0.15, stroke_width=4)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
            self.play(FadeIn(q_title, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("For any one query")
            self.play(FadeIn(one_card, shift=RIGHT * 0.2), run_time=0.6)
            self.play(GrowArrow(one_arr), FadeIn(one_sheet, shift=RIGHT * 0.2), run_time=0.7)
            self.play(FadeIn(line1, shift=LEFT * 0.2), run_time=0.8)
            self.play(FadeIn(tick1, scale=1.6), run_time=0.5)
            vo.wait_until("What is impossible")
            self.play(FadeIn(two_sheet, shift=RIGHT * 0.2),
                      LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in many], lag_ratio=0.12), run_time=1.0)
            self.play(LaggedStart(*[Create(l) for l in two_links], lag_ratio=0.1), run_time=0.7)
            vo.wait_until("is one private release")
            self.play(FadeIn(line2, shift=LEFT * 0.2), run_time=0.8)
            self.play(FadeIn(cross2, scale=1.6), run_time=0.5)
            # the whole difference is the order of the quantifiers: ONE query vs MOST queries
            self.play(Indicate(line1[0], color=S.WHITE, scale_factor=1.06), run_time=0.8)
            self.play(Indicate(line2[0], color=S.WHITE, scale_factor=1.06), run_time=0.8)
            vo.wait_until("The lesson")
            self.play(FadeIn(cur3, scale=0.8), Create(loop), run_time=0.9)
            self.play(Write(lesson_t), run_time=1.6)
            vo.wait_until("keep the curator")
            self.play(Create(lesson_box), run_time=0.9)
        self.wait(0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
