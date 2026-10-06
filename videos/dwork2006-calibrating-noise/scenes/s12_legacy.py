"""S12 · What grew from this paper — the mentor map, continued to the right.

Opens on the exact final frame of S02 (rebuilt from s02_map), compresses the ancestors to the
left, moves this paper's card to the centre with its four idea slots, and grows the descendants
to the right. Every descendant hangs off the idea slot it came from and carries a thumbnail that
echoes an earlier scene; while a descendant is narrated, its thumbnail opens into a panel.
"""

from __future__ import annotations

import numpy as np
from manim import *

from explainer import i18n
from explainer import style as S
from explainer.components import database_rows, gaussian_pdf, person_icon, ponder_card
from explainer.scene import VoiceScene

from common import ALICE, EPS_COLOR, NARRATION, NOISE_COLOR, SENS_COLOR, X_COLOR, XP_COLOR, budget_bar
from s02_map import (LANE_NAMES, PACK_X0, PACK_X1, PAPERS, bit_cell, build_packed_map, coin, coin_flip,
                     pulse, rr_plot, this_paper_card)

SAY = NARRATION["S12"]

# ------------------------------------------------------------------ layout
MAP_X0, MAP_X1 = -6.55, -4.62                 # the compressed ancestor map
MAP_Y = [1.5, 0.6, -0.3]
MAP_SCALE = (MAP_X1 - MAP_X0) / (PACK_X1 + 0.06 - PACK_X0)
CARD_C = np.array([-2.37, 0.6, 0])            # this paper's card
THUMB_X, THUMB_W, THUMB_H = 0.85, 0.86, 0.6   # thumbnails carried by the arrows
DESC_X0, DESC_X1 = 1.4, 6.55                  # descendant cards
ROW_Y = [3.1, 2.22, 1.34, 0.46, -0.42, -1.3, -2.18, -3.06]
PANEL_C, PANEL_W, PANEL_H = np.array([-3.13, 0.0, 0]), 6.9, 6.7    # left edge -6.58 (stroke inside -6.6) covers the map
SLOT_COLORS = [EPS_COLOR, SENS_COLOR, NOISE_COLOR, S.GREY]
SIG = 2.2                                     # Gaussian noise scale in the (eps, delta) panel
T_LO, T_HI = 41.5 - SIG ** 2, 41.5 + SIG ** 2  # where its log-ratio leaves the band |.| <= 1


# ------------------------------------------------------------------ small builders


def desc_card(l1, l2, color, width: float = DESC_X1 - DESC_X0, h: float = 0.7) -> VGroup:
    """Descendant card: VGroup(frame, strip, line1, line2); the strip is the idea slot's colour."""
    l1 = l1 if isinstance(l1, Mobject) else S.text(l1, 20, S.WHITE, weight="BOLD")
    l2 = l2 if isinstance(l2, Mobject) else S.text(l2, 20, S.GREY)
    for line in (l1, l2):
        if line.width > width - 0.38:
            line.scale_to_fit_width(width - 0.38)
    body = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    frame = RoundedRectangle(width=width, height=h, corner_radius=0.1, stroke_color=S.GREY,
                             stroke_width=2).set_fill(S.GREY_DARKER, 1)
    strip = RoundedRectangle(width=0.08, height=h - 0.18, corner_radius=0.04, stroke_width=0).set_fill(color, 1)
    strip.move_to(frame.get_left() + RIGHT * 0.12)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.26)
    return VGroup(frame, strip, l1, l2)


def fan_arrow(p0, p3, color) -> VGroup:
    """Smooth S-shaped arrow (horizontal at both ends) from a slot to a descendant."""
    d = (p3[0] - p0[0]) * 0.55
    curve = CubicBezier(p0, p0 + RIGHT * d, p3 + LEFT * d, p3 + LEFT * 0.1)
    curve.set_stroke(color, 2.5, opacity=0.9)
    tip = Triangle(stroke_width=0).set_fill(color, 1).scale(0.075).rotate(-PI / 2).move_to(p3 + LEFT * 0.07)
    return VGroup(curve, tip)


def fit(m: Mobject, w: float = THUMB_W, h: float = THUMB_H) -> Mobject:
    t = m.copy()
    t.scale(min(w / t.width, h / t.height))
    return t


def coin_stack(n: int = 7, capped: int = 4) -> VGroup:
    """S06's income: a stack of gold coins, sliced by a GREEN cap line."""
    coins = VGroup()
    for i in range(n):
        e = Ellipse(width=0.8, height=0.26, stroke_color="#9A7228", stroke_width=2).set_fill(S.GOLD, 1)
        e.move_to(UP * 0.13 * i)
        if i >= capped:
            e.set_fill(S.GOLD, 0.22).set_stroke(opacity=0.35)
        coins.add(e)
    cap = Line(LEFT * 0.62, RIGHT * 0.62, color=SENS_COLOR, stroke_width=4).move_to(UP * (0.13 * capped - 0.05))
    return VGroup(coins, cap)


def table_icon(rows: int = 4, cols: int = 2, w: float = 4.8, h: float = 2.4, fill: float = 1.0) -> VGroup:
    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            cell = Rectangle(width=w / cols, height=h / rows, stroke_color=S.WHITE if r == 0 else S.GREY,
                             stroke_width=2.5).set_fill(S.GREY_DARKER, fill)
            cell.move_to([(c + 0.5) * w / cols, -(r + 0.5) * h / rows, 0])
            cells.add(cell)
    cells.move_to(ORIGIN)
    return cells


def net_icon(layers=(3, 4, 4, 2), dx: float = 0.45, dy: float = 0.32) -> VGroup:
    cols = [VGroup(*[Dot(radius=0.06, color=S.WHITE) for _ in range(k)]).arrange(DOWN, buff=dy - 0.12)
            for k in layers]
    for i, c in enumerate(cols):
        c.move_to(RIGHT * dx * i)
    edges = VGroup(*[Line(a.get_center(), b.get_center(), color=S.GREY_DARK, stroke_width=1.2)
                     for c1, c2 in zip(cols, cols[1:]) for a in c1 for b in c2])
    return VGroup(edges, *cols).move_to(ORIGIN)


def trophy(height: float = 1.4) -> VGroup:
    cup = Polygon([-0.5, 0.55, 0], [0.5, 0.55, 0], [0.4, 0.05, 0], [0.16, -0.18, 0], [-0.16, -0.18, 0],
                  [-0.4, 0.05, 0], stroke_width=0).set_fill(S.GOLD, 1)
    hl = Arc(radius=0.2, start_angle=PI / 2, angle=PI, color=S.GOLD, stroke_width=6).move_to([-0.55, 0.3, 0])
    hr = Arc(radius=0.2, start_angle=-PI / 2, angle=PI, color=S.GOLD, stroke_width=6).move_to([0.55, 0.3, 0])
    stem = Rectangle(width=0.12, height=0.3, stroke_width=0).set_fill(S.GOLD, 1).move_to([0, -0.33, 0])
    base = RoundedRectangle(width=0.62, height=0.14, corner_radius=0.05, stroke_width=0).set_fill(S.GOLD, 1)
    base.move_to([0, -0.53, 0])
    return VGroup(hl, hr, cup, stem, base).scale_to_fit_height(height)


# ================================================================== the scene


class Legacy(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- 0 · back to the S02 map
        pm = build_packed_map(3)
        chips, badge, card3 = pm["chips"], pm["badge"], pm["card"]
        card3_parts = VGroup(card3.frame, card3.head, card3.venue, card3.anyf, card3.full)

        card = this_paper_card(4).move_to(CARD_C)
        slot_y = [card.full[i][0].get_center()[1] for i in range(4)]
        slot_x = card.full[0][0].get_right()[0]

        lane_of = {k: ln for k, ln, *_ in PAPERS}

        def squeeze(p, lane):
            return np.array([MAP_X0 + (p[0] - PACK_X0) * MAP_SCALE, MAP_Y[lane], 0])

        chip_t = {}
        for k, c in chips.items():
            t = c.copy().scale(MAP_SCALE).move_to(squeeze(c.get_center(), lane_of[k]))
            t[1].set_opacity(0)
            t[2].set_opacity(0)
            chip_t[k] = t
        badge_t = badge.copy().scale(0.5).move_to(squeeze(badge.get_center(), 0))
        badge_t[3].set_opacity(0)
        lines_t = VGroup(*[Line([MAP_X0, y, 0], [MAP_X1, y, 0], color=S.GREY_DARK, stroke_width=2.5) for y in MAP_Y])
        labels_t = VGroup(*[S.text(n, 20, S.GREY).move_to([MAP_X0, y + 0.3, 0], aligned_edge=LEFT)
                            for n, y in zip(LANE_NAMES, MAP_Y)])
        fl = card.frame.get_left()
        arrows_t = VGroup(*[Arrow([MAP_X1, y, 0], fl + UP * dy + LEFT * 0.03, buff=0, color=S.GREY, stroke_width=3,
                                  tip_length=0.15, max_tip_length_to_length_ratio=0.25)
                            for y, dy in zip(MAP_Y, [0.8, 0.0, -0.8])])

        # ---------------------------------------------------------- descendants (by idea slot)
        p2, p3, p5 = self._gauss_panel(), self._composition_panel(), self._sgd_panel()
        p6, p7, p8 = self._mia_panel(), self._local_panel(), self._census_panel()
        rows = self._rows(dict(delta=fit(p2["base"]), comp=budget_bar(THUMB_W, n=8, spent=3, label=False), sgd=fit(p5["base"]),
                               census=fit(p8["base"])))
        for r in rows.values():
            r["card"].move_to([(DESC_X0 + DESC_X1) / 2, ROW_Y[r["row"]], 0])
            col = SLOT_COLORS[r["slot"]]
            p0 = np.array([slot_x, slot_y[r["slot"]], 0])
            if r["thumb"] is not None:
                r["thumb"].move_to([THUMB_X, ROW_Y[r["row"]], 0])
                end = np.array([r["thumb"].get_left()[0] - 0.06, ROW_Y[r["row"]], 0])
            else:
                end = np.array([DESC_X0 - 0.04, ROW_Y[r["row"]], 0])
            r["fan"] = fan_arrow(p0, end, col)

        # Only the card being narrated is shown in full (WHITE frame). When the next one grows, the
        # older cards shrink to their bold first line and their arrows and thumbnails dim, so the full
        # column never shows eight two-line cards at once.
        narrated = []

        def dim(key):
            r = rows[key]
            frame, _, l1, l2 = r["card"]
            short = r.get("short", l1.copy())
            short.move_to(l1, aligned_edge=LEFT).set_y(frame.get_y())
            anims = [frame.animate.set_stroke(S.GREY_DARK), l2.animate.set_opacity(0),
                     Transform(l1, short.fade(0.35)), r["fan"].animate.fade(0.55)]
            if r["thumb"] is not None:
                anims.append(r["thumb"].animate.fade(0.55))
            return anims

        def grow(key, extra=()):
            r = rows[key]
            older = [a for k in narrated for a in dim(k)]
            narrated[:] = [key]
            r["card"][0].set_stroke(S.WHITE)
            self.play(Create(r["fan"]), *older, run_time=0.55)
            anims = [FadeIn(r["card"], shift=RIGHT * 0.25)]
            if r["thumb"] is not None:
                anims.append(FadeIn(r["thumb"], scale=0.6))
            self.play(*anims, *extra, run_time=0.6)

        # ---------------------------------------------------------- beat 0: the name, (eps, delta)
        with self.voiceover(SAY[0]) as vo:
            self.play(LaggedStart(FadeIn(VGroup(pm["lines"], pm["labels"])),
                                  LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in chips.values()], lag_ratio=0.08),
                                  FadeIn(badge), FadeIn(VGroup(pm["arrows"], pm["handover"])),
                                  FadeIn(card3_parts), lag_ratio=0.25), run_time=1.3)
            self.play(*[Transform(chips[k], chip_t[k]) for k in chips], Transform(badge, badge_t),
                      *[Transform(pm["lines"][i], lines_t[i]) for i in range(3)],
                      *[Transform(pm["labels"][i], labels_t[i]) for i in range(3)],
                      *[Transform(pm["arrows"][i], arrows_t[i]) for i in range(3)],
                      FadeOut(pm["handover"]),
                      ReplacementTransform(card3.frame, card.frame), ReplacementTransform(card3.head, card.head),
                      ReplacementTransform(card3.venue, card.venue), ReplacementTransform(card3.anyf, card.anyf),
                      *[ReplacementTransform(card3.full[i], card.full[i]) for i in range(3)],
                      run_time=1.5)
            self.play(FadeIn(card.full[3], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("in an invited paper")
            grow("name")
            vo.wait_until("titled simply")
            self.play(Circumscribe(rows["name"]["card"][3][1], color=EPS_COLOR, buff=0.06), run_time=1.0)
            vo.wait_until("Dwork introduced")
            self.play(pulse(card.full[0], 1.06), run_time=0.8)
            vo.wait_until("Another 2006 paper")
            grow("delta")
            vo.wait_until("Mironov")
            self.play(Indicate(rows["delta"]["card"][2], color=S.WHITE, scale_factor=1.05),
                      Indicate(rows["delta"]["card"][3][0], color=S.WHITE, scale_factor=1.05), run_time=1.0)
            vo.wait_until("added a tiny slack")
            self.play(Indicate(rows["delta"]["card"][3][1], color=EPS_COLOR, scale_factor=1.3), run_time=0.9)
            vo.wait_until("Remember the Gaussian")
            pop = self._open(rows["delta"]["thumb"], p2["base"], "the Gaussian's log-ratio, again")
            self.play(Create(p2["axes"]), FadeIn(p2["labels"]), run_time=0.7)
            vo.wait_until("escaped the band")
            self.play(*[Flash(a.get_end(), color=NOISE_COLOR, flash_radius=0.3) for a in p2["escape"]],
                      Indicate(p2["gauss_lab"], color=S.WHITE), run_time=0.9)
            vo.wait_until("Delta pays")
            self.play(Create(p2["ax2"]), Create(p2["density"]), FadeIn(p2["dens_lab"]),
                      Create(p2["guides"]), run_time=0.9)
            self.play(FadeIn(p2["tails"]), FadeIn(p2["delta_lab"], shift=UP * 0.1), run_time=0.8)
            vo.wait_until("and lets the bell")
            self.play(FadeIn(p2["verdict"], shift=UP * 0.15), run_time=0.7)
        p2_extras = VGroup(*[p2[k] for k in ("axes", "labels", "ax2", "density", "dens_lab", "guides", "tails",
                                             "delta_lab", "verdict")])

        # ---------------------------------------------------------- beat 1: exponential mechanism, composition
        bits = rows["expmech"]["thumb"]
        with self.voiceover(SAY[1]) as vo:
            self._close(pop, p2["base"], rows["delta"]["thumb"], p2_extras)
            grow("expmech")
            vo.wait_until("became McSherry")
            self.play(self._flicker(bits, ["10010", "11110", "10111", "00110", "10100", "10110"]), run_time=2.6)
            self.play(pulse(rows["expmech"]["card"], 1.04), pulse(card.full[2], 1.06), run_time=0.7)
            vo.wait_until("The privacy budget")
            grow("comp")
            vo.wait_until("with a surprise")
            pop = self._open(rows["comp"]["thumb"], p3["base"], "the cost of k answers")
            self.play(FadeIn(p3["bar_lab"]), Create(p3["axes"]), FadeIn(p3["ax_labels"]), run_time=0.7)
            self.play(Create(p3["basic"]), FadeIn(p3["basic_lab"]), run_time=0.9)
            vo.wait_until("allow that tiny delta")
            self.play(Create(p3["adv"]), FadeIn(p3["adv_lab"]), run_time=1.2)
            vo.wait_until("and the total loss")
            self.play(Create(p3["mark"]), FadeIn(p3["dots"]), FadeIn(p3["vals"]), run_time=0.9)
            vo.wait_until("grows only like")
            self.play(Circumscribe(p3["adv_lab"], color=EPS_COLOR, buff=0.08), run_time=1.1)
        p3_extras = VGroup(*[p3[k] for k in ("bar_lab", "axes", "ax_labels", "basic", "basic_lab", "adv", "adv_lab",
                                             "mark", "dots", "vals")])

        # ---------------------------------------------------------- beat 2: local DP = Warner's coin
        thumb_coin = rows["local"]["thumb"]
        with self.voiceover(SAY[2]) as vo:
            self._close(pop, p3["base"], rows["comp"]["thumb"], p3_extras)
            grow("local")
            self.play(coin_flip(thumb_coin, "THTH", run_time=0.9, hop=0.12), run_time=0.9)
            vo.wait_until("the model Section four")
            self.play(pulse(card.full[3], 1.08), run_time=0.8)
            vo.wait_until("is what we now call")
            self.play(Indicate(rows["local"]["card"][2], color=S.WHITE, scale_factor=1.06), run_time=0.9)
            vo.wait_until("used by Google")
            self.play(Indicate(rows["local"]["card"][3][0], color=S.WHITE, scale_factor=1.1), run_time=0.8)
            vo.wait_until("and by Apple")
            self.play(Indicate(rows["local"]["card"][3][1], color=S.WHITE, scale_factor=1.1), run_time=0.8)
            vo.wait_until("Why the weakest")
            p7["base"].face = thumb_coin.face
            pop = self._open(thumb_coin, p7["base"], "each user flips their own coin")
            vo.wait_until("Nobody has to be")
            self.play(LaggedStart(*[FadeIn(VGroup(p, c), shift=RIGHT * 0.2) for p, c in zip(p7["people"], p7["coins"])],
                                  lag_ratio=0.15), FadeIn(p7["server"]), run_time=0.9)
            self.play(LaggedStart(*[GrowArrow(a) for a in p7["sends"]], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in p7["bits"]], lag_ratio=0.15),
                      *[coin_flip(c, "TH", run_time=0.8, hop=0.1) for c in p7["coins"]], run_time=0.9)
            self.play(FadeIn(p7["noraw"], scale=0.8), run_time=0.6)
            vo.wait_until("and with millions")
            self.play(Create(p7["ax"]), FadeIn(p7["ax_labels"]), Create(p7["true_line"]), FadeIn(p7["plot_lab"]),
                      run_time=0.6)
            self.play(Create(p7["curve"]), run_time=vo.remaining(1.0) - 0.2, rate_func=linear)
        p7_extras = VGroup(*[p7[k] for k in ("people", "coins", "server", "sends", "bits", "noraw", "ax", "ax_labels",
                                             "true_line", "plot_lab", "curve")])

        # ---------------------------------------------------------- beat 3: DP-SGD, membership inference
        with self.voiceover(SAY[3]) as vo:
            self._close(pop, p7["base"], thumb_coin, p7_extras)
            grow("sgd")
            vo.wait_until("made it practical")
            self.play(pulse(rows["sgd"]["card"], 1.04), pulse(card.full[1], 1.06), run_time=0.8)
            vo.wait_until("clip each example")
            pop = self._open(rows["sgd"]["thumb"], p5["base"], "DP-SGD: one training step")
            self.play(FadeIn(p5["cap_lab"]), LaggedStart(*[GrowArrow(a) for a in p5["grads"]], lag_ratio=0.1),
                      Create(p5["circle"]), FadeIn(p5["c_lab"]), run_time=1.0)
            vo.wait_until("like our income cap")
            self.play(*[Transform(a, b) for a, b in zip(p5["grads"], p5["clipped"])],
                      Indicate(p5["base"][1], color=SENS_COLOR), run_time=1.0)
            vo.wait_until("which bounds")
            self.play(FadeIn(p5["clip_lab"], shift=UP * 0.1), run_time=0.7)
            vo.wait_until("add Gaussian noise")
            self.play(GrowArrow(p5["sum"]), FadeIn(p5["sum_lab"]), run_time=0.6)
            self.play(FadeIn(p5["noise"], scale=0.5), FadeIn(p5["noise_lab"]), run_time=0.6)
            vo.wait_until("and track the budget")
            self.play(FadeIn(p5["bar"]), FadeIn(p5["counter"]), FadeIn(p5["bar_lab"]), run_time=0.4)
            p5["bar"].add_updater(p5["drain"])
            self.play(p5["step"].animate.set_value(10000), run_time=2.2, rate_func=linear)
            p5["bar"].clear_updaters()
            p5["counter"].clear_updaters()
            vo.wait_until("If you train")
            self._close(pop, p5["base"], rows["sgd"]["thumb"],
                        VGroup(*[p5[k] for k in ("cap_lab", "grads", "circle", "c_lab", "clip_lab", "sum", "sum_lab",
                                                 "noise", "noise_lab", "bar", "counter", "bar_lab")]))
            self.play(Circumscribe(rows["sgd"]["card"], color=S.WHITE, buff=0.05), run_time=1.2)
            vo.wait_until("A trained network")
            grow("mia")
            pop = self._open(rows["mia"]["thumb"], p6["base"], "membership inference")
            self.play(FadeIn(p6["db"], shift=RIGHT * 0.2), GrowArrow(p6["a1"]), FadeIn(p6["net"]),
                      GrowArrow(p6["a2"]), FadeIn(p6["fx"]), run_time=0.9)
            vo.wait_until("and attacks that ask")
            self.play(FadeIn(p6["question"], shift=UP * 0.15), pulse(p6["alice"], 1.15), run_time=0.8)
            vo.wait_until("are our subtraction")
            self.play(pulse(p6["base"], 1.2), FadeIn(p6["same"], shift=LEFT * 0.2), run_time=0.9)
        p6_extras = VGroup(*[p6[k] for k in ("db", "a1", "net", "a2", "fx", "question", "same")])

        # ---------------------------------------------------------- beat 4: the 2020 Census, ponder
        with self.voiceover(SAY[4]) as vo:
            self._close(pop, p6["base"], rows["mia"]["thumb"], p6_extras)
            grow("census")
            vo.wait_until("protected its published")
            pop = self._open(rows["census"]["thumb"], p8["base"], "US Census 2020")
            self.play(FadeIn(p8["names"]), FadeIn(p8["vals"]), FadeIn(p8["vals_noisy"][0]), run_time=0.7)
            for frame_vals in p8["jitter"]:
                self.play(*[Transform(a, b) for a, b in zip(p8["vals_noisy"][0], frame_vals)], run_time=0.35)
            vo.wait_until("only a few counts")
            self.play(Create(p8["exact_box"]), FadeIn(p8["exact_lab"], shift=LEFT * 0.15), run_time=0.8)
            vo.wait_until("But that is a one-shot")
            self.play(FadeIn(p8["stamp"], scale=1.4), pulse(card.full[3], 1.08), run_time=0.8)
            vo.wait_until("Pause and ponder")
            self._close(pop, p8["base"], rows["census"]["thumb"],
                        VGroup(*[p8[k] for k in ("names", "vals", "vals_noisy", "exact_box", "exact_lab", "stamp")]))
        others = VGroup(*[VGroup(r["card"], r["fan"], *([r["thumb"]] if r["thumb"] is not None else []))
                          for k, r in rows.items() if k != "census"])
        # only the one-shot slot and the Census stay bright: dim the other slots and the ancestor map too
        others.add(*[card.full[i] for i in range(3)], card.anyf,
                   *chips.values(), badge, pm["lines"], pm["labels"], pm["arrows"])
        q = ponder_card("The Census published one release.\nDoes the one-shot limit\n(Section 4) forbid it?",
                        width=6.3, size=30)
        q.move_to([-3.43, 3.5 - q.height / 2, 0])   # left edge at -6.58: covers the lane labels (x >= -6.55)
        q[0].set_fill(S.BG, 1)          # fully opaque: anything less lets bright text ghost through
        self.play(FadeIn(q, scale=0.95), others.animate.fade(0.7), run_time=0.6)
        bar = q[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ---------------------------------------------------------- beat 5: no — quantifiers, trophy, open problems
        # The two lines exactly as S11 showed them (wording, sizes, TEAL tick / RED cross in DejaVu Sans).
        def mark(ch, color, size=44):
            return Text(ch, font="DejaVu Sans", font_size=size, color=color)

        # Chinese has no capitals: the quantifiers ONE / MOST are coloured instead (as in S11)
        quant_kw = {"t2c": {"ONE": S.YELLOW, "MOST": S.YELLOW}} if i18n.active() else {}
        a1 = S.text("Any ONE query, known in advance", 32, S.WHITE, **quant_kw)
        tick1 = mark("✓", S.TEAL)
        b1 = VGroup(S.text("→  easy to publish for", 30, S.GREY), tick1).arrange(RIGHT, buff=0.3)
        census_tick = mark("✓", S.TEAL, 34)
        census = VGroup(S.text("US Census 2020: a fixed set of tables chosen in advance", 26, S.WHITE),
                        census_tick).arrange(RIGHT, buff=0.22)
        a2 = S.text("ONE private release that works for MOST queries", 32, S.WHITE, **quant_kw)
        cross2 = mark("✗", NOISE_COLOR)
        b2 = VGroup(S.text("→  impossible unless n is huge", 30, S.GREY), cross2).arrange(RIGHT, buff=0.3)
        for m in (tick1, cross2):
            m.shift(UP * 0.03)
        item1 = VGroup(a1, b1).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        item2 = VGroup(a2, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        census_box = VGroup(census)
        quant = VGroup(item1, census_box, item2).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        census_box.shift(RIGHT * 0.6)
        quant.move_to([0, 1.55, 0])
        census_frame = SurroundingRectangle(census, color=S.GREY, buff=0.14, corner_radius=0.08, stroke_width=2)
        _w = i18n.tr("MOST")                            # (translated: the scoped key s12_legacy|MOST)
        _i = a2.text.replace(" ", "").index(_w)    # Text drops spaces from its glyphs
        most = a2[_i:_i + len(_w)]
        cup = trophy(1.25)
        prize = VGroup(S.text("Gödel Prize 2017", 28, S.GOLD), S.text("TCC Test-of-Time Award 2016", 24, S.GREY)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        award = VGroup(cup, prize).arrange(RIGHT, buff=0.35).move_to([-3.25, -1.95, 0])   # room for the cup's pulse
        still_t = S.text("Still open", 26, S.YELLOW, weight="BOLD")
        still_1 = S.text("choosing ε in practice", 24, S.WHITE, t2c={"ε": EPS_COLOR})
        still_2 = S.text("when no one can be trusted\nwith the data", 24, S.WHITE, line_spacing=0.9)
        still = VGroup(still_t, still_1, still_2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        still_frame = SurroundingRectangle(still, color=S.GREY, buff=0.25, corner_radius=0.12, stroke_width=2)
        still_card = VGroup(still_frame, still).move_to([3.9, -1.95, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
            vo.wait_until("The Census tuned")
            self.play(FadeIn(a1, shift=LEFT * 0.2), FadeIn(b1[0], shift=LEFT * 0.2), run_time=0.8)
            self.play(FadeIn(tick1, scale=1.6), run_time=0.4)
            self.play(FadeIn(census[0], shift=RIGHT * 0.2), Create(census_frame), run_time=0.9)
            vo.wait_until("chosen in advance")
            self.play(FadeIn(census_tick, scale=1.6), pulse(tick1, 1.3), run_time=0.8)
            vo.wait_until("Section four only")
            self.play(FadeIn(a2, shift=LEFT * 0.2), FadeIn(b2[0], shift=LEFT * 0.2), run_time=0.9)
            self.play(FadeIn(cross2, scale=1.6), run_time=0.4)
            vo.wait_until("that is accurate for most")
            self.play(Indicate(most, color=S.WHITE, scale_factor=1.15), run_time=0.9)
            self.play(pulse(cross2, 1.35), run_time=0.6)
            # the prizes arrive silently as the sentence ends (no narration about them) ...
            self.play(FadeIn(cup, shift=UP * 0.3), FadeIn(prize, shift=LEFT * 0.2), run_time=vo.remaining(0.8))
        # ... and the open problems right after it: a ~3 s tail instead of ~7 s of silence
        self.play(FadeIn(still_card, shift=UP * 0.2), pulse(cup, 1.1), run_time=0.6)
        self.play(Indicate(still_1[8], color=EPS_COLOR, scale_factor=1.5), run_time=0.9)
        self.wait(0.9)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)

    # ================================================================== rows
    def _rows(self, thumbs: dict) -> dict:
        # (Chinese has no italics: Pango would slant 差分隐私 synthetically, so the name stays upright there)
        name_l2 = VGroup(S.text("names it", 20, S.GREY),
                         S.text("differential privacy", 20, S.WHITE, slant=NORMAL if i18n.active() else ITALIC)
                         ).arrange(RIGHT, buff=0.14)
        delta_l2 = VGroup(S.text("Mironov & Naor 2006 ·", 20, S.WHITE, weight="BOLD"),
                          S.math(r"(\varepsilon,\delta)", size=28, color=EPS_COLOR)).arrange(RIGHT, buff=0.14)
        comp_l2 = S.tex(r"composition: $k$ questions cost $\sim\!\sqrt{k}$", size=27, color=S.GREY)
        local_l2 = VGroup(S.text("Google RAPPOR 2014", 20, S.GREY), S.text("· Apple 2016", 20, S.GREY)
                          ).arrange(RIGHT, buff=0.12)
        thumbs = dict(thumbs, expmech=VGroup(*[bit_cell(b, 0.17, 0.28) for b in "10110"]).arrange(RIGHT, buff=0),
                      mia=S.math("42", "-", "41", size=24), local=coin(0.24, "H"))
        spec = [
            ("name", 0, 0, "Dwork 2006 (ICALP)", name_l2),
            ("delta", 0, 1, "Dwork, Kenthapadi, McSherry,", delta_l2),
            ("comp", 0, 2, "Dwork, Rothblum & Vadhan 2010", comp_l2),
            ("mia", 0, 3, "Membership inference (2017)", "Shokri et al.: our attack, on models"),
            ("sgd", 1, 4, "DP-SGD · Abadi et al. 2016", "clip each gradient + Gaussian noise"),
            ("expmech", 2, 5, "McSherry & Talwar 2007", "the exponential mechanism"),
            ("local", 3, 6, "Local differential privacy", local_l2),
            ("census", 3, 7, "US Census 2020", "published tables protected with DP"),
        ]
        out = {}
        for key, slot, row, l1, l2 in spec:
            out[key] = dict(slot=slot, row=row, card=desc_card(l1, l2, SLOT_COLORS[slot]), thumb=thumbs.get(key))
        # dimmed, a card keeps only its bold first line; delta's first line alone would end on a comma
        out["delta"]["short"] = VGroup(S.text("Dwork et al. 2006 ·", 20, S.WHITE, weight="BOLD"),
                                       S.math(r"(\varepsilon,\delta)", size=28, color=EPS_COLOR)
                                       ).arrange(RIGHT, buff=0.14)
        return out

    # ================================================================== pop-out panels
    def _open(self, thumb, base, title: str) -> VGroup:
        panel = RoundedRectangle(width=PANEL_W, height=PANEL_H, corner_radius=0.2, stroke_color=S.GREY_DARK,
                                 stroke_width=2).set_fill(S.BG, 1).move_to(PANEL_C)
        head = S.text(title, 26, S.WHITE, weight="BOLD")
        head.move_to(panel.get_corner(UL) + RIGHT * 0.35 + DOWN * 0.38, aligned_edge=UL)
        ring = SurroundingRectangle(thumb, color=S.WHITE, buff=0.06, stroke_width=2)
        z1 = Line(ring.get_corner(UL), panel.get_corner(UR) + LEFT * 0.15, color=S.GREY_DARK, stroke_width=1.5)
        z2 = Line(ring.get_corner(DL), panel.get_corner(DR) + LEFT * 0.15, color=S.GREY_DARK, stroke_width=1.5)
        base.set_z_index(3)
        # the panel first, then the drawing grows out of its thumbnail onto the (now opaque) panel:
        # growing both at once drew e.g. the Census table across the paper card behind the panel
        self.play(FadeIn(panel), Create(ring), Create(z1), Create(z2), FadeIn(head, shift=RIGHT * 0.2),
                  run_time=0.45)
        self.play(TransformFromCopy(thumb, base), run_time=0.55)
        return VGroup(panel, head, ring, z1, z2)

    def _close(self, pop, base, thumb, extras):
        # Three steps, the reverse of _open: clear the panel's contents and shrink the drawing back
        # into its thumbnail while the panel is still opaque, then fade the panel. (Fading the panel
        # while the drawing moved let the drawing and the card underneath show through each other;
        # FadeOut(extras) after FadeOut(pop) in a single play() also put the panel above its own
        # contents, which then vanished at once.)
        self.play(FadeOut(extras), run_time=0.3)
        self.play(Transform(base, thumb.copy()), run_time=0.4)
        self.remove(base)
        self.play(FadeOut(pop), run_time=0.3)

    @staticmethod
    def _flicker(cells, strings):
        """Bits of the output string flip at random (RED = flipped vs the true answer 10110)."""
        true = "10110"
        anims = []
        for s in strings:
            targets = [bit_cell(b, 0.17, 0.28, color=S.WHITE if b == t else NOISE_COLOR).move_to(c)
                       for b, t, c in zip(s, true, cells)]
            anims.append(AnimationGroup(*[Transform(c, t) for c, t in zip(cells, targets)], run_time=0.4))
        return Succession(*anims)

    # (eps, delta): the Gaussian's log-ratio escapes the band only in rare tails
    def _gauss_panel(self) -> dict:
        t0, t1 = 32, 51
        ax = Axes(x_range=[t0, t1, 1], y_range=[-2.1, 2.1, 1], x_length=5.6, y_length=2.3, tips=False,
                  axis_config={"color": S.GREY, "stroke_width": 2, "include_ticks": False}).move_to([-3.35, 1.15, 0])
        band = Rectangle(width=ax.x_length, height=ax.c2p(0, 1)[1] - ax.c2p(0, -1)[1], stroke_width=0)
        band.set_fill(EPS_COLOR, 0.13).move_to(ax.c2p((t0 + t1) / 2, 0))
        hi = DashedLine(ax.c2p(t0, 1), ax.c2p(t1, 1), color=EPS_COLOR, stroke_width=2.5)
        lo = DashedLine(ax.c2p(t0, -1), ax.c2p(t1, -1), color=EPS_COLOR, stroke_width=2.5)
        lap = ax.plot(lambda t: abs(t - 42) - abs(t - 41), x_range=[t0, t1, 0.01], color=S.WHITE, stroke_width=4)
        gau = ax.plot(lambda t: (41.5 - t) / SIG ** 2, x_range=[t0, t1, 0.05], color=S.GREY, stroke_width=4)
        up = Arrow(ax.c2p(T_LO - 1.6, 1.15), ax.c2p(T_LO - 1.6, 2.05), buff=0, color=NOISE_COLOR, stroke_width=5,
                   tip_length=0.16)
        dn = Arrow(ax.c2p(T_HI + 1.6, -1.15), ax.c2p(T_HI + 1.6, -2.05), buff=0, color=NOISE_COLOR, stroke_width=5,
                   tip_length=0.16)
        base = VGroup(band, hi, lo, lap, gau, up, dn)
        eps_hi = S.math(r"+\varepsilon", size=28, color=EPS_COLOR).next_to(ax.c2p(t1, 1), RIGHT, buff=0.08)
        eps_lo = S.math(r"-\varepsilon", size=28, color=EPS_COLOR).next_to(ax.c2p(t1, -1), RIGHT, buff=0.08)
        y_lab = S.text("log ratio", 20, S.GREY).next_to(ax, UP, buff=0.05).align_to(ax, LEFT).shift(RIGHT * 0.1)
        # S07's keys, in free space: inside the band's upper right (the Laplace line runs along the
        # bottom edge there, the Gaussian is already below the axis, the dashed guides start lower),
        # and above the band just right of the Gaussian's exit arrow
        lap_lab = S.text("Laplace: stays inside", 20, S.WHITE).move_to(ax.c2p(42.35, 0.5), aligned_edge=LEFT)
        gauss_lab = S.text("Gaussian: escapes", 20, S.GREY).move_to(ax.c2p(T_LO - 0.75, 1.62), aligned_edge=LEFT)
        ax2 = Axes(x_range=[t0, t1, 1], y_range=[0, 0.2, 0.1], x_length=5.6, y_length=1.45, tips=False,
                   axis_config={"color": S.GREY, "stroke_width": 2, "include_ticks": False}).move_to([-3.35, -1.25, 0])
        dens = ax2.plot(lambda t: gaussian_pdf(t, 41, SIG), x_range=[t0, t1, 0.05], color=X_COLOR, stroke_width=4)
        dens_lab = S.text("outputs in world x", 20, X_COLOR).next_to(ax2.c2p(44.6, 0.12), RIGHT, buff=0.1)
        # the tails are thin slivers: shade them and also trace the curve over them in YELLOW
        tails = VGroup(ax2.get_area(dens, x_range=[t0, T_LO], color=EPS_COLOR, opacity=0.85),
                       ax2.get_area(dens, x_range=[T_HI, t1], color=EPS_COLOR, opacity=0.85),
                       ax2.plot(lambda t: gaussian_pdf(t, 41, SIG), x_range=[t0, T_LO, 0.05], color=EPS_COLOR,
                                stroke_width=6),
                       ax2.plot(lambda t: gaussian_pdf(t, 41, SIG), x_range=[T_HI, t1, 0.05], color=EPS_COLOR,
                                stroke_width=6))
        guides = VGroup(DashedLine(ax.c2p(T_LO, 1), ax2.c2p(T_LO, 0), color=S.GREY, stroke_width=1.5),
                        DashedLine(ax.c2p(T_HI, -1), ax2.c2p(T_HI, 0), color=S.GREY, stroke_width=1.5))
        delta_txt = VGroup(S.math(r"\delta", size=34, color=EPS_COLOR), S.text("= these rare tails", 22, S.WHITE)
                           ).arrange(RIGHT, buff=0.12).move_to(ax2.c2p(41.5, 0)).shift(DOWN * 0.4)
        delta_arrows = VGroup(
            Arrow(delta_txt.get_left() + LEFT * 0.05, ax2.c2p(34.6, 0.012), buff=0.06, color=EPS_COLOR,
                  stroke_width=2.5, tip_length=0.12),
            Arrow(delta_txt.get_right() + RIGHT * 0.05, ax2.c2p(47.6, 0.006), buff=0.06, color=EPS_COLOR,
                  stroke_width=2.5, tip_length=0.12))
        delta_lab = VGroup(delta_txt, delta_arrows)
        verdict = S.tex(r"Gaussian noise is back in, for a tiny ", r"$\delta$", size=32)
        verdict[1].set_color(EPS_COLOR)
        verdict.move_to([-3.25, -2.85, 0])
        return dict(base=base, axes=ax, labels=VGroup(eps_hi, eps_lo, y_lab, lap_lab, gauss_lab), gauss_lab=gauss_lab,
                    escape=VGroup(up, dn), ax2=ax2, density=dens, dens_lab=dens_lab, tails=tails, guides=guides,
                    delta_lab=delta_lab, verdict=verdict)

    # composition: k answers cost ~k with pure epsilon, ~sqrt(k) once a tiny delta is allowed
    def _composition_panel(self) -> dict:
        base = budget_bar(4.8, n=8, spent=3, label=False).move_to([-3.4, 2.25, 0])   # the video's budget bar
        bar_lab = VGroup(S.text("privacy budget", 22, EPS_COLOR), S.math(r"\varepsilon", size=32, color=EPS_COLOR)
                         ).arrange(RIGHT, buff=0.12).next_to(base, DOWN, buff=0.15).align_to(base, LEFT)
        kmax = 1100
        ax = Axes(x_range=[0, kmax, 500], y_range=[0, 1100, 500], x_length=4.9, y_length=3.0, tips=False,
                  axis_config={"color": S.GREY, "stroke_width": 2, "include_ticks": False}).move_to([-3.2, -0.95, 0])
        ax_labels = VGroup(S.text("k questions", 20, S.GREY).next_to(ax.x_axis.get_right(), DOWN, buff=0.12),
                           S.text("total privacy loss", 20, S.GREY).next_to(ax.y_axis.get_top(), UP, buff=0.08)
                           .align_to(ax, LEFT))
        basic = ax.plot(lambda k: k, x_range=[0, 1050], color=S.GREY, stroke_width=4)
        log_inv_delta = np.log(1e5)
        adv_f = lambda k: np.sqrt(2 * k * log_inv_delta)   # advanced composition, small-epsilon form
        adv = ax.plot(adv_f, x_range=[0.5, 1050, 2], color=EPS_COLOR, stroke_width=5)
        basic_lab = VGroup(S.text("add up:", 22, S.GREY), S.math(r"k\,\varepsilon", size=30, color=S.GREY)
                           ).arrange(RIGHT, buff=0.12).next_to(ax.c2p(560, 620), LEFT, buff=0.3)
        # the curve's actual formula (so its k = 1000 value, 150 epsilon, can be checked), in two lines
        # inside the wedge between the two curves, right-aligned just left of the k = 1000 guide
        adv_lab = VGroup(S.tex(r"with $\delta = 10^{-5}$:", size=30, color=EPS_COLOR),
                         S.math(r"\approx\sqrt{2k\ln(1/\delta)}\;\varepsilon", size=28, color=EPS_COLOR)
                         ).arrange(DOWN, buff=0.08, aligned_edge=RIGHT)
        adv_lab.move_to([ax.c2p(1000, 0)[0] - 0.14, ax.c2p(0, adv_f(1000))[1] + 0.12, 0], aligned_edge=DR)
        mark = DashedLine(ax.c2p(1000, 0), ax.c2p(1000, 1000), color=S.GREY, stroke_width=1.5)
        dots = VGroup(Dot(ax.c2p(1000, 1000), color=S.WHITE, radius=0.06), Dot(ax.c2p(1000, adv_f(1000)),
                                                                                color=EPS_COLOR, radius=0.07))
        vals = VGroup(S.math(r"1000\,\varepsilon", size=26, color=S.GREY).next_to(dots[0], RIGHT, buff=0.1),
                      S.math(r"\approx 150\,\varepsilon", size=26, color=EPS_COLOR).next_to(dots[1], RIGHT, buff=0.1))
        return dict(base=base, bar_lab=bar_lab, axes=ax, ax_labels=ax_labels, basic=basic, basic_lab=basic_lab,
                    adv=adv, adv_lab=adv_lab, mark=mark, dots=dots, vals=vals)

    # local DP: each user flips their own coin, the server never sees raw data
    def _local_panel(self) -> dict:
        base = coin(0.34, "H").move_to([-5.55, 2.1, 0])
        ys = [1.3, 0.72, 0.14]
        people = VGroup(*[person_icon(S.WHITE, 0.5).move_to([-5.7, y, 0]) for y in ys])
        coins = VGroup(*[coin(0.15, "H").move_to([-5.15, y - 0.08, 0]) for y in ys])
        server = RoundedRectangle(width=2.2, height=1.75, corner_radius=0.12, stroke_color=S.GREY,
                                  stroke_width=2).set_fill(S.GREY_DARKER, 1).move_to([-1.35, 0.72, 0])
        s_lab = S.text("server", 22, S.GREY).next_to(server, UP, buff=0.1)
        sends = VGroup(*[Arrow([-4.9, y, 0], [server.get_left()[0] - 0.05, y, 0], buff=0, color=S.GREY,
                               stroke_width=2.5, tip_length=0.14) for y in ys])
        bits = VGroup(*[S.text(b, 22, S.WHITE, font=S.FONT_SANS).move_to([-3.4, y + 0.17, 0])
                        for b, y in zip("101", ys)])
        db_ic = table_icon(3, 2, 0.8, 0.5).move_to(server.get_center() + UP * 0.25)
        cross = VGroup(Line(db_ic.get_corner(UL), db_ic.get_corner(DR)), Line(db_ic.get_corner(DL), db_ic.get_corner(UR))
                       ).set_stroke(NOISE_COLOR, 4)
        noraw = VGroup(db_ic, cross, S.text("no raw data", 20, S.WHITE).next_to(db_ic, DOWN, buff=0.15))
        ax, ax_labels, curve, true_line = rr_plot(width=4.4, height=1.55)
        shift = np.array([-3.0, -1.95, 0]) - ax.get_center()
        for m in (ax, ax_labels, curve, true_line):
            m.shift(shift)
        plot_lab = S.text("many users: the true rate still comes through", 20, S.GREY).next_to(ax, UP, buff=0.12)
        return dict(base=base, people=people, coins=coins, server=VGroup(server, s_lab), sends=sends, bits=bits,
                    noraw=noraw, ax=ax, ax_labels=ax_labels, curve=curve, true_line=true_line, plot_lab=plot_lab)

    # DP-SGD: clip (= the income cap), add Gaussian noise, track the budget
    def _sgd_panel(self) -> dict:
        base = coin_stack().scale(1.15).move_to([-5.45, 1.05, 0])
        cap_lab = S.text("income cap", 20, SENS_COLOR).next_to(base, DOWN, buff=0.15)
        o = np.array([-2.75, 1.0, 0])
        vecs = [(1.8, 0.6), (0.5, 0.45), (1.1, 1.3), (0.2, 0.7), (1.5, -0.4), (0.6, -0.25), (2.0, 1.1)]
        C = 1.0
        grads = VGroup(*[Arrow(o, o + np.array([vx, vy, 0]), buff=0, color=S.WHITE, stroke_width=3, tip_length=0.13,
                               max_tip_length_to_length_ratio=0.3) for vx, vy in vecs])
        clipped_v = [np.array([vx, vy, 0]) * min(1.0, C / np.hypot(vx, vy)) for vx, vy in vecs]
        clipped = VGroup(*[Arrow(o, o + v, buff=0, color=S.WHITE, stroke_width=3, tip_length=0.13,
                                 max_tip_length_to_length_ratio=0.3) for v in clipped_v])
        circle = DashedVMobject(Circle(radius=C, color=SENS_COLOR, stroke_width=3).move_to(o), num_dashes=40)
        c_lab = S.math("C", size=32, color=SENS_COLOR).move_to(o + np.array([-0.8, 0.85, 0]))
        clip_a = VGroup(S.text("clip each example's gradient to size", 22, S.WHITE),
                        S.math(r"\le C", size=30, color=SENS_COLOR)).arrange(RIGHT, buff=0.12)
        # (no number here: the sum's sensitivity is C for add/remove neighbours but 2C for the paper's
        # replace-one-row neighbours)
        clip_b = S.text("⇒  so the sum has bounded sensitivity", 22, SENS_COLOR)
        clip_lab = VGroup(clip_a, clip_b).arrange(DOWN, buff=0.12).move_to([-3.1, -0.38, 0])
        total = sum(clipped_v) * 0.25
        s0 = np.array([-5.45, -2.0, 0])
        sum_arrow = Arrow(s0, s0 + total, buff=0, color=S.WHITE, stroke_width=4, tip_length=0.16)
        sum_lab = S.text("sum", 20, S.GREY).next_to(s0, LEFT, buff=0.12)
        tip = s0 + total
        noise = VGroup(*[Circle(radius=r, stroke_width=0).set_fill(NOISE_COLOR, op).move_to(tip)
                         for r, op in [(0.55, 0.12), (0.38, 0.18), (0.22, 0.3)]],
                       Dot(tip + np.array([0.18, -0.12, 0]), color=NOISE_COLOR, radius=0.06))
        noise_lab = S.text("+ Gaussian noise", 22, NOISE_COLOR).next_to(noise, RIGHT, buff=0.2)
        step = ValueTracker(1)
        bar_x0, bar_w = -5.6, 3.9
        # the video's budget bar (common.budget_bar); 10,000 steps spend 82% of it, from the right
        bar = budget_bar(bar_w, n=10, label=False)
        bar.shift(np.array([bar_x0, -2.75, 0]) - bar.frame.get_left())
        full = bar.segs[0].get_fill_opacity()

        def drain(m):
            spent = 0.82 * len(m.segs) * (step.get_value() - 1) / 9999      # in segments
            for j, seg in enumerate(reversed(m.segs)):
                seg.set_fill(opacity=full * float(np.clip(1 - (spent - j), 0, 1)))

        bar_lab = S.text("privacy budget, tracked", 20, EPS_COLOR).next_to(bar.frame, UP, buff=0.12,
                                                                         aligned_edge=LEFT)
        step_lab = S.text("step", 22, S.GREY).move_to([-1.35, -2.75, 0])
        # set_value() rebuilds the digits at the number's own 30 pt (always_redraw + become() left the
        # comma glyph with a bogus font size, which explainer.check reported as 13.5 pt)
        counter = Integer(1, group_with_commas=True, font_size=30, color=S.WHITE).next_to(step_lab, RIGHT, buff=0.15)
        counter.add_updater(lambda m: m.set_value(int(step.get_value())).next_to(step_lab, RIGHT, buff=0.15))
        return dict(base=base, cap_lab=cap_lab, grads=grads, clipped=clipped, circle=circle, c_lab=c_lab,
                    clip_lab=clip_lab, sum=sum_arrow, sum_lab=sum_lab, noise=noise, noise_lab=noise_lab, step=step,
                    bar=bar, drain=drain, bar_lab=VGroup(bar_lab, step_lab), counter=counter, step_lab=step_lab)

    # membership inference: was Alice in the training set? = tell f(x) from f(x')
    def _mia_panel(self) -> dict:
        base = S.math("42", "-", "41", size=24).scale(2.0).move_to([-5.2, -1.6, 0])
        db = database_rows(["Ann", "Bob", "Alice", "Dee"], None, color=X_COLOR, width=1.7, row_height=0.4, size=20)
        db[2][1].set_color(ALICE)
        db[2][2].set_color(ALICE)
        db.move_to([-5.3, 1.05, 0])
        db_lab = S.text("database x", 22, X_COLOR).next_to(db, UP, buff=0.12)
        net = net_icon().move_to([-3.0, 1.05, 0])
        net_lab = S.text("train", 20, S.GREY).next_to(net, UP, buff=0.12)
        a1 = Arrow(db.get_right(), net.get_left(), buff=0.12, color=S.GREY, stroke_width=3, tip_length=0.15)
        # two-line caption, so the net -> f(x) arrow has room (one line ran into the net's last layer)
        fx = VGroup(S.math("f(x)", size=36, color=X_COLOR),
                    S.text("the trained\nmodel", 20, S.GREY, line_spacing=0.85)).arrange(DOWN, buff=0.1)
        fx.move_to([-1.0, 1.0, 0])
        a2 = Arrow(net.get_right(), fx.get_left(), buff=0.12, color=S.GREY, stroke_width=3, tip_length=0.15)
        question = S.text("“Was Alice in the training set?”", 26, ALICE).move_to([-3.1, -0.35, 0])
        same = VGroup(S.math(r"\Rightarrow", size=36), S.math("f(x)", size=36, color=X_COLOR),
                      S.text("vs", 24, S.GREY), S.math("f(x')", size=36, color=XP_COLOR),
                      S.text("scaled up", 20, S.GREY)).arrange(RIGHT, buff=0.2)
        same.move_to([-2.1, -1.6, 0])
        base_to = [-5.2, -1.6, 0]
        return dict(base=base, base_to=base_to, db=VGroup(db_lab, db), alice=db[2], a1=a1, net=VGroup(net, net_lab),
                    a2=a2, fx=fx, question=question, same=same)

    # the 2020 Census: published tables with noise, a few counts exact
    def _census_panel(self) -> dict:
        base = table_icon(4, 2, 5.0, 2.6, fill=0.0).move_to([-3.1, 0.55, 0])
        cw, rh = 2.5, 0.65
        x_l, x_r = base.get_left()[0] + 0.2, base.get_center()[0] + 0.2
        ys = [base.get_top()[1] - rh * (i + 0.5) for i in range(4)]
        names = VGroup(*[S.text(t, 24, S.WHITE).move_to([x_l, y, 0], aligned_edge=LEFT)
                         for t, y in zip(["state totals", "counties", "tracts", "blocks"], ys)])
        # illustrative total (the earlier 5,893,718 is Wisconsin's real 2020 count)
        exact = S.text("3,486,201", 24, S.WHITE, font=S.FONT_SANS).move_to([x_r, ys[0], 0], aligned_edge=LEFT)
        rng = np.random.default_rng(2020)
        true_vals = [48113, 4102, 37]
        def row_vals(noise):
            return VGroup(*[S.text(f"{v + int(e):,}", 24, NOISE_COLOR, font=S.FONT_SANS).move_to([x_r, y, 0],
                                                                                              aligned_edge=LEFT)
                            for v, e, y in zip(true_vals, noise, ys[1:])])
        noisy0 = row_vals(np.round(rng.laplace(0, 3, 3)))
        jitter = [row_vals(np.round(rng.laplace(0, 3, 3))) for _ in range(4)]
        noise_tags = VGroup(*[S.text("+ noise", 20, NOISE_COLOR).move_to([base.get_right()[0] - 0.15, y, 0],
                                                                         aligned_edge=RIGHT) for y in ys[1:]])
        exact_box = SurroundingRectangle(VGroup(base[0], base[1]), color=S.WHITE, buff=0.04, stroke_width=4)
        exact_lab = S.text("exact", 22, S.WHITE).move_to([base.get_right()[0] - 0.15, ys[0], 0], aligned_edge=RIGHT)
        stamp_t = S.text("published once", 26, S.GREY)
        stamp = VGroup(SurroundingRectangle(stamp_t, color=S.GREY, buff=0.14, corner_radius=0.08, stroke_width=3),
                       stamp_t).rotate(-8 * DEGREES).move_to([-1.9, -1.55, 0])
        return dict(base=base, names=names, vals=VGroup(exact, noise_tags), vals_noisy=VGroup(noisy0), jitter=jitter,
                    exact_box=exact_box, exact_lab=exact_lab, stamp=stamp)
