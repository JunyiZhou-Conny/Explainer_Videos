"""S02 · Where this paper sits — the mentor map of the paper's ancestors.

Three lanes (Randomize / Attacks / Provable noise) over a 1960–2010 axis. Each paper is a chip on
its lane, pinned to its exact year; the stage below the map shows what each paper contributed.
At the end the map packs to the left and every lane flows into this paper's YELLOW card.

The map pieces (coin, chips, the 2006 card, the packed map) are exported so that S12 can rebuild
exactly the same picture before growing the descendants.
"""

from __future__ import annotations

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import database_rows, person_icon, timeline
from explainer.scene import VoiceScene

from common import ALICE, EPS_COLOR, NARRATION, NOISE_COLOR, SENS_COLOR, X_COLOR

SAY = NARRATION["S02"]

# ------------------------------------------------------------------ map geometry
YEAR0, YEAR1 = 1960, 2010
AX_X0, AX_X1, AX_Y = -4.45, 6.3, 0.2         # the shared year axis (timeline layout)
LANE_NAMES = ["Randomize", "Attacks", "Provable noise"]
LANE_Y = [2.55, 1.6, 0.65]                    # timeline layout: lane lines
LANE_X0, LANE_X1 = -4.55, 6.45
CHIP_LIFT = 0.15                              # timeline layout: chip bottom above its lane
PACK_Y = [2.3, 0.95, -0.4]                    # packed layout: lane lines (chips sit on them)
PACK_X0, PACK_X1 = -6.5, 0.4                  # packed layout: chips right-aligned to PACK_X1
ARROW_X1 = 3.0                                # packed layout: arrows end at the card
CARD_W = 3.5
CARD_CENTER = np.array([4.8, 0.95, 0])        # packed layout: the 2006 card
HEADER_Y = -0.85                              # stage header line
COIN_RIM = "#9A7228"
CHIP_H = 0.62
HANDOVER = ["randomness", "must survive\nany attacker", "noise you\ncan analyse"]

# key, lane, name, year label, pin years, x-centre in the timeline layout (None = at its pin)
PAPERS = [
    ("warner", 0, "Warner", "1965", (1965,), None),
    ("sdc", 0, "Disclosure control", "1980 · 1989", (1980, 1989), None),
    ("egs", 0, "Evfimievski", "et al. 2003", (2003,), None),
    ("sweeney", 1, "Sweeney", "1997", (1997,), 2.85),
    ("dn03", 1, "Dinur & Nissim", "2003", (2003,), 4.9),
    ("dn04", 2, "Dwork & Nissim", "2004", (2004,), 3.8),
    ("sulq", 2, "SuLQ", "2005", (2005,), 5.75),
]
WARNER_ICON = 0.52          # extra room inside the Warner chip for the coin badge


def year_x(y: float) -> float:
    return AX_X0 + (AX_X1 - AX_X0) * (y - YEAR0) / (YEAR1 - YEAR0)


# ------------------------------------------------------------------ small glyphs


def coin(radius: float = 0.28, face: str = "H", letter: bool = True) -> VGroup:
    """Warner's coin: a gold disc with a rim and an H/T face."""
    disc = Circle(radius=radius, stroke_width=0).set_fill(S.GOLD, 1)
    rim = Circle(radius=radius, stroke_color=COIN_RIM, stroke_width=3)
    inner = Circle(radius=radius * 0.78, stroke_color=COIN_RIM, stroke_width=1.5)
    g = VGroup(disc, rim, inner)
    if letter:
        g.add(S.text(face, radius * 85, S.BG, weight="BOLD").move_to(disc))
    g.face = face
    return g


def coin_flip(c: VGroup, faces: str, run_time: float = 1.0, hop: float = 0.3):
    """Animate coin `c` through len(faces) half-turns, landing on faces[-1] (e.g. "THTH")."""
    r = c[0].width / 2
    letter = len(c) > 3
    centre = c.get_center().copy()
    start = getattr(c, "face", "H")
    tmpl = {f: coin(r, f, letter) for f in "HT"}
    k = len(faces)

    def upd(m, a):
        ph = a * k
        i = min(int(ph), k - 1)
        fr = ph - i
        face = faces[i] if fr >= 0.5 else (start if i == 0 else faces[i - 1])
        m.become(tmpl[face].copy().move_to(centre + UP * hop * np.sin(np.pi * a)))
        m.stretch(max(abs(np.cos(np.pi * fr)), 0.04), 1)

    c.face = faces[-1]
    return UpdateFromAlphaFunc(c, upd, run_time=run_time, rate_func=linear)


def map_chip(name: str, year: str, icon_space: float = 0.0, size: float = 20) -> VGroup:
    """A paper chip for the map: bold name over a grey year. VGroup(frame, name, year)."""
    n = S.text(name, size, S.WHITE, weight="BOLD")
    y = S.text(year, size, S.GREY)
    body = VGroup(n, y).arrange(DOWN, buff=0.07)
    frame = RoundedRectangle(width=body.width + 0.34 + icon_space, height=CHIP_H, corner_radius=0.1,
                             stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
    body.move_to(frame).shift(RIGHT * icon_space / 2)
    g = VGroup(frame, n, y)
    g.icon_space = icon_space
    return g


def chip_icon_point(chip: VGroup) -> np.ndarray:
    return chip[0].get_left() + RIGHT * (0.08 + chip.icon_space / 2)


def stage_header(bold: str, rest: str = "", size: float = 26) -> VGroup:
    a = S.text(bold, size, S.WHITE, weight="BOLD")
    g = VGroup(a)
    if rest:
        g.add(S.text(rest, size, S.GREY))
    g.arrange(RIGHT, buff=0.2)
    g.move_to([0, HEADER_Y, 0]).to_edge(LEFT, buff=0.6)
    return g


def mini_table(headers, rows, col_w, row_h: float = 0.36, size: float = 20) -> VGroup:
    """A small table: VGroup(header_row, *data_rows); each row is VGroup of cells VGroup(box, text)."""
    out = VGroup()
    for r, vals in enumerate([headers] + list(rows)):
        row = VGroup()
        x = 0.0
        for w, v in zip(col_w, vals):
            box = Rectangle(width=w, height=row_h, stroke_width=1.5 if r else 0,
                            stroke_color=S.GREY_DARK).set_fill(S.GREY_DARKER, 1 if r else 0)
            box.move_to([x + w / 2, -r * row_h, 0])
            t = S.text(v if v else " ", size, S.GREY if r == 0 else S.WHITE,
                       font=S.FONT_SANS if r else S.FONT)
            if t.width > w - 0.12:
                t.scale_to_fit_width(w - 0.12)
            t.move_to(box)
            row.add(VGroup(box, t))
            x += w
        out.add(row)
    return out


def bit_cell(v: str, w: float = 0.46, h: float = 0.36, color: str = S.WHITE,
             stroke: str = S.GREY_DARK) -> VGroup:
    box = Rectangle(width=w, height=h, stroke_color=stroke, stroke_width=1.5).set_fill(S.GREY_DARKER, 1)
    t = S.text(v, 22, color, font=S.FONT_SANS).move_to(box)
    return VGroup(box, t)


# ------------------------------------------------------------------ randomized response maths

P_TRUE = 0.30          # true share of "yes" in the illustration


def rr_running_estimate(n: int = 5000, seed: int = 1965, p: float = P_TRUE):
    """Simulate Warner's coin for n people; return (answers, running estimate 2*share - 1/2)."""
    rng = np.random.default_rng(seed)
    truth = rng.random(n) < p
    heads = rng.random(n) < 0.5
    second = rng.random(n) < 0.5
    ans = np.where(heads, truth, second)
    share = np.cumsum(ans) / np.arange(1, n + 1)
    return ans, 2 * share - 0.5


def rr_plot(width: float = 3.3, height: float = 1.9, n: int = 5000, seed: int = 1965):
    """Axes + running-estimate curve + dashed true-rate line (log-scale x: people asked)."""
    ax = Axes(x_range=[1, np.log10(n), 1], y_range=[0, 0.6, 0.1], x_length=width, y_length=height,
              tips=False, axis_config={"color": S.GREY, "stroke_width": 2, "include_ticks": True})
    labels = VGroup(*[S.text(t, 20, S.GREY).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                      for k, t in [(1, "10"), (2, "100"), (3, "1000")]])
    _, est = rr_running_estimate(n, seed)
    ns = np.unique(np.logspace(1, np.log10(n), 260).astype(int))
    pts = [ax.c2p(np.log10(k), float(np.clip(est[k - 1], 0.005, 0.595))) for k in ns]
    curve = VMobject(stroke_color=S.WHITE, stroke_width=3).set_points_as_corners(pts)
    true_line = DashedLine(ax.c2p(1, P_TRUE), ax.c2p(np.log10(n), P_TRUE), color=S.GREY,
                           stroke_width=2.5, dash_length=0.08)
    return ax, labels, curve, true_line


# ------------------------------------------------------------------ this paper's card


SLOT_SPECS = [
    ("one definition", lambda: S.math(r"\varepsilon", size=34, color=EPS_COLOR), EPS_COLOR),
    ("one number", lambda: S.math("S(f)", size=30, color=SENS_COLOR), SENS_COLOR),
    ("one recipe", lambda: _recipe_tex(), NOISE_COLOR),
    ("one limit", lambda: S.text("one-shot releases", 20, S.GREY), S.GREY),
]


def _recipe_tex():
    m = S.math(r"\mathrm{Lap}\big(", "S(f)", "/", r"\varepsilon", r"\big)", size=30)
    m[0].set_color(NOISE_COLOR)
    m[1].set_color(SENS_COLOR)
    m[3].set_color(EPS_COLOR)
    m[4].set_color(NOISE_COLOR)
    return m


def this_paper_card(n_slots: int = 3, width: float = CARD_W) -> VGroup:
    """The YELLOW 'this paper' card. Returns VGroup(frame, head, venue, anyf, slots_empty, slots_full)
    with attributes .frame .head .venue .anyf .empty[i] .full[i] (full = VGroup(box, label, symbol))."""
    t1 = S.text("Dwork, McSherry,", 24, S.WHITE, weight="BOLD")
    t2 = S.text("Nissim & Smith", 24, S.WHITE, weight="BOLD")
    head = VGroup(t1, t2).arrange(DOWN, buff=0.08)
    venue = S.text("TCC 2006", 22, S.YELLOW)
    anyf = VGroup(S.text("any query", 22, S.WHITE), S.math("f", size=32)).arrange(RIGHT, buff=0.14)
    anyf[1].shift(DOWN * 0.03)
    slot_w, slot_h = width - 0.36, 0.46
    empty, full = VGroup(), VGroup()
    for label, sym, col in SLOT_SPECS[:n_slots]:
        box = RoundedRectangle(width=slot_w, height=slot_h, corner_radius=0.08,
                               stroke_color=col, stroke_width=2.5).set_fill(col, 0.12)
        dashed = DashedVMobject(RoundedRectangle(width=slot_w, height=slot_h, corner_radius=0.08,
                                                 stroke_color=S.GREY_DARK, stroke_width=2),
                                num_dashes=28)
        lab = S.text(label, 22, S.WHITE).move_to(box.get_left() + RIGHT * 0.14, aligned_edge=LEFT)
        s = sym()
        room = slot_w - lab.width - 0.5
        if s.width > room:
            s.scale(room / s.width)
        s.move_to(box.get_right() + LEFT * 0.14, aligned_edge=RIGHT)
        empty.add(dashed)
        full.add(VGroup(box, lab, s))
    top = VGroup(head, venue).arrange(DOWN, buff=0.12)
    slots = VGroup(*[VGroup(e, f) for e, f in zip(empty, full)]).arrange(DOWN, buff=0.1)
    stack = VGroup(top, anyf, slots).arrange(DOWN, buff=0.17)
    frame = RoundedRectangle(width=width, height=stack.height + 0.42, corner_radius=0.15,
                             stroke_color=S.YELLOW, stroke_width=4).set_fill(S.GREY_DARKER, 1)
    stack.move_to(frame)
    card = VGroup(frame, head, venue, anyf, empty, full)
    card.frame, card.head, card.venue, card.anyf, card.empty, card.full = frame, head, venue, anyf, empty, full
    return card


# ------------------------------------------------------------------ packed layout


def packed_positions(chips: dict) -> dict:
    """Centres of the chips in the packed layout (right-aligned per lane, gap 0.1)."""
    pos = {}
    for lane in range(3):
        keys = [k for k, ln, *_ in PAPERS if ln == lane]
        x = PACK_X1
        for k in reversed(keys):
            w = chips[k].width
            pos[k] = np.array([x - w / 2, PACK_Y[lane], 0])
            x -= w + 0.1
    return pos


def packed_lane_lines() -> VGroup:
    return VGroup(*[Line([PACK_X0, y, 0], [PACK_X1 + 0.06, y, 0], color=S.GREY_DARK, stroke_width=2.5)
                    for y in PACK_Y])


def packed_lane_labels(size: float = 22) -> VGroup:
    return VGroup(*[S.text(n, size, S.GREY).move_to([PACK_X0, y + 0.56, 0], aligned_edge=LEFT)
                    for n, y in zip(LANE_NAMES, PACK_Y)])


def handover_arrows(card: VGroup) -> tuple[VGroup, VGroup]:
    """Arrows from the packed lane ends into the card, and their hand-over labels."""
    fl = card.frame.get_left()
    ends = [fl + UP * 0.8, fl, fl + DOWN * 0.8]
    arrows, labels = VGroup(), VGroup()
    for i, (y, e) in enumerate(zip(PACK_Y, ends)):
        a = Arrow([PACK_X1 + 0.06, y, 0], e + LEFT * 0.04, buff=0, color=S.GREY, stroke_width=3,
                  tip_length=0.18, max_tip_length_to_length_ratio=0.12)
        lab = S.text(HANDOVER[i], 20, S.WHITE, line_spacing=0.8)
        mid = a.point_from_proportion(0.45)
        if i < 2:
            lab.next_to(mid, UP, buff=0.12)
        else:
            lab.next_to(mid, DOWN, buff=0.14)
        arrows.add(a)
        labels.add(lab)
    return arrows, labels


def build_chips() -> dict:
    chips = {}
    for key, lane, name, year, pins, xc in PAPERS:
        chips[key] = map_chip(name, year, icon_space=WARNER_ICON if key == "warner" else 0.0)
    return chips


def build_packed_map(n_slots: int = 3, filled: bool = True) -> dict:
    """Everything of the S02 finale, already in place (used by S12 to return to the map)."""
    chips = build_chips()
    pos = packed_positions(chips)
    for k, c in chips.items():
        c.move_to(pos[k])
    badge = coin(0.24, "H").move_to(chip_icon_point(chips["warner"]))
    card = this_paper_card(n_slots).move_to(CARD_CENTER)
    arrows, labels = handover_arrows(card)
    return dict(lines=packed_lane_lines(), labels=packed_lane_labels(), chips=chips, badge=badge,
                card=card, arrows=arrows, handover=labels)


# ================================================================== the scene


class LineageBefore(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- the empty map
        axis = timeline(YEAR0, YEAR1, width=AX_X1 - AX_X0, step=10)
        axis.shift(RIGHT * (AX_X0 + AX_X1) / 2 + UP * AX_Y)
        lanes = VGroup(*[Line([LANE_X0, y, 0], [LANE_X1, y, 0], color=S.GREY_DARK, stroke_width=2.5)
                         for y in LANE_Y])
        lane_labels = VGroup(*[S.text(n, 22, S.GREY).move_to([LANE_X0 - 0.1, y, 0], aligned_edge=RIGHT)
                               for n, y in zip(LANE_NAMES, LANE_Y)])
        chips = build_chips()
        warner_wide = chips["warner"]
        chips["warner"] = map_chip("Warner", "1965")          # narrow until the coin docks
        pins = {}
        for key, lane, name, year, years, xc in PAPERS:
            c = chips[key]
            x = xc if xc is not None else year_x(sum(years) / len(years))
            c.move_to([x, LANE_Y[lane] + CHIP_LIFT + CHIP_H / 2, 0])
            pins[key] = self._pin(c, lane, years)
        warner_wide.move_to(chips["warner"]).align_to(chips["warner"], RIGHT)
        warner_wide[0].set_stroke(S.WHITE)
        frames = {k: c[0] for k, c in chips.items()}
        active = []

        def show_chip(key, run_time=0.9, keep=False):
            """Pin + chip grow in; the chip is outlined WHITE while it is being narrated."""
            c, p = chips[key], pins[key]
            dots = [m for m in p if isinstance(m, Dot)]
            dim = [] if keep else [frames[k].animate.set_stroke(S.GREY) for k in active]
            if not keep:
                active.clear()
            active.append(key)
            c[0].set_stroke(S.WHITE)
            return AnimationGroup(
                *dim,
                LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2),
                *[Create(m) for m in p if not isinstance(m, Dot)],
                GrowFromPoint(c, dots[0].get_center()),
                *[Flash(d, color=S.WHITE, flash_radius=0.18, line_length=0.1) for d in dots],
                run_time=run_time)

        # ========================================================== 0 · Warner's coin
        header0 = stage_header("Warner 1965", "· randomized response")
        person = person_icon(S.WHITE, 0.9).move_to([-5.8, -2.5, 0])
        q_text = S.text("“Do you have condition X?”", 22, S.WHITE)
        q_box = RoundedRectangle(width=q_text.width + 0.36, height=q_text.height + 0.3, corner_radius=0.14,
                                 stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
        q_text.move_to(q_box)
        question = VGroup(q_box, q_text).move_to([-4.75, -1.45, 0])
        c1 = coin(0.28, "H").move_to([-4.55, -2.5, 0])
        private = S.text("in private", 20, S.GREY).move_to([-5.15, -3.22, 0])
        a_heads = Arrow(c1.get_right() + UP * 0.08, [-3.05, -1.95, 0], buff=0.08, color=S.GREY,
                        stroke_width=3, tip_length=0.16)
        a_tails = Arrow(c1.get_right() + DOWN * 0.08, [-3.05, -3.05, 0], buff=0.08, color=S.GREY,
                        stroke_width=3, tip_length=0.16)
        l_heads = S.text("heads", 20, S.GREY).next_to(a_heads.point_from_proportion(0.55), UP, buff=0.12)
        l_tails = S.text("tails", 20, S.GREY).next_to(a_tails.point_from_proportion(0.55), DOWN, buff=0.12)
        truth = S.text("tell the truth", 24, S.WHITE).next_to(a_heads.get_end(), RIGHT, buff=0.12)
        c2 = coin(0.22, "H").next_to(a_tails.get_end(), RIGHT, buff=0.1)
        say_yes = S.text("H → “yes”", 22, S.WHITE)
        say_no = S.text("T → “no”", 22, S.WHITE)
        results = VGroup(say_yes, say_no).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        results.next_to(c2, RIGHT, buff=0.25)
        tree = VGroup(a_heads, a_tails, l_heads, l_tails, truth, c2, results)

        yes_text = S.text("“yes”", 26, S.WHITE)
        yes_box = RoundedRectangle(width=yes_text.width + 0.36, height=yes_text.height + 0.3,
                                   corner_radius=0.14, stroke_color=S.WHITE, stroke_width=2
                                   ).set_fill(S.GREY_DARKER, 1)
        yes_text.move_to(yes_box)
        yes_bubble = VGroup(yes_box, yes_text).move_to(question, aligned_edge=LEFT)
        which = S.text("truth, or the coin?", 22, S.GREY).next_to(yes_bubble, RIGHT, buff=0.3)

        answers, _ = rr_running_estimate()
        crowd = VGroup(*[person_icon(S.WHITE if answers[i] else S.GREY_DARK, 0.24) for i in range(36)])
        crowd.arrange_in_grid(rows=6, cols=6, buff=(0.1, 0.07)).move_to([0.35, -2.05, 0])
        crowd_lab = VGroup(person_icon(S.WHITE, 0.22), S.text("said “yes”", 20, S.GREY)).arrange(RIGHT, buff=0.12)
        crowd_lab.next_to(crowd, DOWN, buff=0.14)
        ax, ax_labels, est_curve, true_line = rr_plot()
        shift = np.array([4.0, -2.15, 0]) - ax.get_center()
        for m in (ax, ax_labels, est_curve, true_line):
            m.shift(shift)
        ax_title = S.text("estimated true rate", 20, S.GREY).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        x_lab = S.text("people asked", 20, S.GREY).next_to(ax_labels, DOWN, buff=0.08).align_to(ax, RIGHT)
        true_lab = S.text("true rate", 20, S.GREY).next_to(true_line, UP, buff=0.06).align_to(ax, RIGHT)
        badge = coin(0.24, "H")

        with self.voiceover(SAY[0]) as vo:
            self.play(Create(axis[0]), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in axis[1]],
                                                   lag_ratio=0.12),
                      LaggedStart(*[Create(l) for l in lanes], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in lane_labels], lag_ratio=0.2),
                      run_time=2.2)
            vo.wait_until("In 1965")
            self.play(show_chip("warner"), run_time=1.0)
            self.play(FadeIn(header0, shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(person, shift=UP * 0.2), FadeIn(question, shift=UP * 0.2), run_time=0.8)
            self.play(Indicate(q_text, color=S.WHITE, scale_factor=1.06), run_time=1.0)
            vo.wait_until("In a popular")
            self.play(FadeIn(c1, scale=0.5), run_time=0.4)
            self.play(coin_flip(c1, "THTH", run_time=1.4, hop=0.35), FadeIn(private), run_time=1.4)
            vo.wait_until("Heads, you")
            self.play(GrowArrow(a_heads), FadeIn(l_heads), run_time=0.6)
            self.play(FadeIn(truth, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Tails, you")
            self.play(GrowArrow(a_tails), FadeIn(l_tails), run_time=0.6)
            self.play(FadeIn(c2, scale=0.5), run_time=0.3)
            self.play(coin_flip(c2, "THTH", run_time=1.1, hop=0.25), run_time=1.1)
            self.play(FadeIn(say_yes, shift=RIGHT * 0.15), run_time=0.45)
            self.play(FadeIn(say_no, shift=RIGHT * 0.15), run_time=0.45)
            vo.wait_until("Any single yes")
            self.play(ReplacementTransform(question, yes_bubble), run_time=0.7)
            self.play(FadeIn(which, shift=RIGHT * 0.2),
                      Indicate(truth, color=S.WHITE, scale_factor=1.15),
                      Indicate(say_yes, color=S.WHITE, scale_factor=1.25), run_time=1.2)
            vo.wait_until("yet over thousands")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in crowd], lag_ratio=0.03),
                      FadeIn(crowd_lab), run_time=1.0)
            self.play(Create(ax), FadeIn(ax_labels), FadeIn(ax_title), FadeIn(x_lab),
                      Create(true_line), FadeIn(true_lab), run_time=0.7)
            self.play(Create(est_curve), run_time=vo.until("Keep this coin", 1.2), rate_func=linear)
            vo.wait_until("Keep this coin")
            badge.move_to(c1)
            self.add(badge)
            self.play(Transform(chips["warner"], warner_wide),
                      badge.animate.move_to(chip_icon_point(warner_wide)), run_time=1.0)
            self.play(Indicate(badge, color=S.YELLOW, scale_factor=1.3), run_time=vo.remaining(0.4))
        chips["warner"] = VGroup(chips["warner"], badge)

        stage0 = VGroup(header0, person, yes_bubble, which, c1, private, tree, crowd, crowd_lab,
                        ax, ax_labels, est_curve, true_line, ax_title, x_lab, true_lab)

        # ========================================================== 1 · two flavours of scrambling
        header1 = stage_header("Statistical disclosure control", "· Denning 1980 · Adam & Wortmann 1989",
                               size=24)
        names = ["Ann", "Bob", "Cy", "Dee"]
        vals = ["no X", "has X", "no X", "has X"]
        panel_a = self._flavour_panel("scramble inputs", names, vals, [-5.2, -2.55, 0])
        panel_b = self._flavour_panel("scramble outputs", names, vals, [-1.25, -2.55, 0])
        rows_a, rows_b = panel_a[1], panel_b[1]
        flipped = S.text("has X", 20, NOISE_COLOR, font=S.FONT_SANS).move_to(rows_a[2][3])
        arr_a = Arrow(rows_a.get_right(), rows_a.get_right() + RIGHT * 0.9, buff=0.08, color=S.GREY,
                      stroke_width=3, tip_length=0.15)
        ans_a = S.text("3", 34, S.WHITE).next_to(arr_a, RIGHT, buff=0.12)
        cnt_a = S.text("count", 20, S.GREY).next_to(arr_a, UP, buff=0.05)
        arr_b = Arrow(rows_b.get_right(), rows_b.get_right() + RIGHT * 0.9, buff=0.08, color=S.GREY,
                      stroke_width=3, tip_length=0.15)
        ans_b = S.text("2", 34, S.WHITE).next_to(arr_b, RIGHT, buff=0.12)
        ans_b2 = S.text("2.6", 34, S.WHITE).next_to(arr_b, RIGHT, buff=0.12).align_to(ans_b, LEFT)
        cnt_b = S.text("count", 20, S.GREY).next_to(arr_b, UP, buff=0.05)
        noise_b = S.text("+ noise", 22, NOISE_COLOR).next_to(ans_b2, DOWN, buff=0.15)
        jitter_a = VGroup(*[SurroundingRectangle(r[3], color=NOISE_COLOR, buff=0.04, stroke_width=2)
                            for r in rows_a])

        egs_title = VGroup(S.text("Evfimievski, Gehrke", 22, S.WHITE, weight="BOLD"),
                           S.text("& Srikant 2003", 22, S.WHITE, weight="BOLD")).arrange(DOWN, buff=0.06,
                                                                                         aligned_edge=LEFT)
        egs_idea = S.text("worst-case belief change", 22, S.GREY)
        belief = NumberLine(x_range=[0, 1, 0.5], length=3.0, color=S.GREY, stroke_width=2,
                            include_ticks=True, tick_size=0.06)
        b0 = Dot(belief.n2p(0.22), color=S.WHITE, radius=0.07)
        b1 = Dot(belief.n2p(0.58), color=S.WHITE, radius=0.07)
        b_arc = CurvedArrow(b0.get_center() + UP * 0.1, b1.get_center() + UP * 0.1, angle=-1.0,
                            color=S.WHITE, stroke_width=2.5, tip_length=0.12)
        b_lab = S.text("bounded", 20, S.GREY).next_to(b_arc, UP, buff=0.05)
        b_ends = VGroup(S.text("before", 20, S.GREY).next_to(b0, DOWN, buff=0.1),
                        S.text("after", 20, S.GREY).next_to(b1, DOWN, buff=0.1))
        egs_icon = VGroup(belief, b0, b1, b_arc, b_lab, b_ends)
        egs = VGroup(egs_title, egs_idea, egs_icon).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        egs.move_to([4.25, -2.3, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(stage0), run_time=0.6)
            self.play(show_chip("sdc"), FadeIn(header1, shift=RIGHT * 0.2), run_time=1.0)
            self.play(show_chip("egs", keep=True), run_time=0.8)
            self.play(FadeIn(egs, shift=UP * 0.2), run_time=0.7)
            self.play(Create(b_arc), Indicate(b1, color=S.WHITE), run_time=0.8)
            vo.wait_until("refined such")
            self.play(FadeIn(rows_a, shift=UP * 0.2), FadeIn(rows_b, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("in two flavours")
            self.play(FadeIn(panel_a[0], shift=DOWN * 0.15), FadeIn(panel_b[0], shift=DOWN * 0.15),
                      run_time=0.6)
            vo.wait_until("scramble the data")
            self.play(Create(jitter_a), Wiggle(VGroup(*[r[3] for r in rows_a]), scale_value=1.15),
                      run_time=0.7)
            self.play(Transform(rows_a[2][3], flipped), run_time=0.4)
            self.play(GrowArrow(arr_a), FadeIn(cnt_a), FadeIn(ans_a, shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("or scramble the answers")
            self.play(GrowArrow(arr_b), FadeIn(cnt_b), FadeIn(ans_b, shift=RIGHT * 0.1), run_time=0.6)
            self.play(Wiggle(ans_b, scale_value=1.3), FadeIn(noise_b, shift=UP * 0.1), run_time=0.6)
            self.play(Transform(ans_b, ans_b2), run_time=vo.remaining(0.4))
        stage1 = VGroup(header1, panel_a, panel_b, jitter_a, arr_a, ans_a, cnt_a, arr_b, ans_b, cnt_b,
                        noise_b, egs)

        # ========================================================== 2 · Sweeney: names are not enough
        header2 = stage_header("Sweeney 1997", "· “anonymous” ≠ anonymous")
        hosp_rows = [("", "02139", "6/30/71", "F", "asthma"),
                     ("", "02144", "2/11/58", "M", "flu"),
                     ("", "02135", "9/17/43", "M", "cardiac"),
                     ("", "02141", "12/3/82", "F", "fracture")]
        hosp = mini_table(["name", "ZIP", "born", "sex", "diagnosis"], hosp_rows,
                          [1.75, 0.9, 1.05, 0.55, 1.15])
        hosp.move_to([-3.55, -2.6, 0])
        blobs = VGroup(*[RoundedRectangle(width=w, height=0.11, corner_radius=0.05, stroke_width=0)
                         .set_fill(S.GREY, 0.9).move_to(hosp[r + 1][0][0])
                         for r, w in enumerate([1.05, 0.85, 1.2, 0.95])])
        hosp_title = S.text("hospital records", 22, S.WHITE).next_to(hosp, UP, buff=0.14).align_to(hosp, LEFT)
        hosp_title2 = S.text("hospital records, names removed", 22, S.WHITE).move_to(hosp_title,
                                                                                     aligned_edge=LEFT)
        voter_rows = [("A. Ruiz", "02140", "4/22/66", "F"),
                      ("the governor", "02135", "9/17/43", "M"),
                      ("K. Osei", "02139", "1/5/90", "M"),
                      ("M. Novak", "02144", "8/19/77", "F")]
        voter = mini_table(["name", "ZIP", "born", "sex"], voter_rows, [1.75, 0.9, 1.05, 0.55])
        voter.move_to([4.15, -2.6, 0])
        voter_title = S.text("public voter list", 22, S.WHITE).next_to(voter, UP, buff=0.14).align_to(voter, LEFT)
        qi_cols = VGroup(*[hosp[r][c] for r in range(5) for c in (1, 2, 3)])
        qi_box = SurroundingRectangle(qi_cols, color=S.WHITE, buff=0.03, stroke_width=2.5)
        unique = S.text("· ZIP + birth date + sex  →  most people unique", 26, S.WHITE)
        unique.next_to(header2[0], RIGHT, buff=0.2)
        gov_h = VGroup(*[hosp[3][c] for c in (1, 2, 3)])
        gov_v = VGroup(*[voter[2][c] for c in (1, 2, 3)])
        hl_h = SurroundingRectangle(gov_h, color=ALICE, buff=0.02, stroke_width=3)
        hl_v = SurroundingRectangle(gov_v, color=ALICE, buff=0.02, stroke_width=3)
        join = Line(hosp[3].get_right(), voter[2].get_left(), color=ALICE, stroke_width=3)
        gov_name = voter[2][0][1]
        gov_copy = S.text("the governor", 20, ALICE, font=S.FONT_SANS)
        gov_copy.scale_to_fit_width(gov_name.width).move_to(hosp[3][0][0])
        gov_row_hl = SurroundingRectangle(hosp[3], color=ALICE, buff=0.02, stroke_width=3)

        lesson1 = S.text("privacy = a property of the process", 30, S.WHITE)
        lesson1b = S.text("not of how the released table looks", 24, S.GREY)
        lesson2 = S.text("… whatever else the attacker knows", 30, S.WHITE)
        lessons = VGroup(lesson1, lesson1b, lesson2).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        lessons.move_to([-2.9, -2.35, 0])
        side_brace = Brace(voter, LEFT, color=S.GREY, buff=0.1)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(stage1), run_time=0.6)
            self.play(show_chip("sweeney"), FadeIn(header2, shift=RIGHT * 0.2),
                      FadeIn(hosp, shift=UP * 0.2), FadeIn(blobs, shift=UP * 0.2), FadeIn(hosp_title),
                      run_time=1.0)
            vo.wait_until("just remove the names")
            self.play(LaggedStart(*[b.animate.stretch(0.02, 0).set_opacity(0) for b in blobs], lag_ratio=0.15),
                      ReplacementTransform(hosp_title, hosp_title2), run_time=1.0)
            vo.wait_until("kept failing")
            self.play(Indicate(header2[1], color=S.WHITE, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Latanya Sweeney")
            self.play(Indicate(chips["sweeney"], color=S.WHITE, scale_factor=1.12), run_time=0.8)
            vo.wait_until("ZIP code")
            self.play(Create(qi_box), run_time=0.8)
            vo.wait_until("single out most")
            self.play(FadeOut(header2[1], shift=UP * 0.2), FadeIn(unique, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("and in 1997")
            self.play(Flash(pins["sweeney"][0], color=S.WHITE, flash_radius=0.25), run_time=0.7)
            vo.wait_until("linked supposedly")
            self.play(FadeOut(qi_box), Create(hl_h), run_time=0.7)
            self.play(Indicate(hosp[3], color=ALICE, scale_factor=1.04), run_time=0.9)
            vo.wait_until("to a public voter")
            self.play(FadeIn(voter, shift=LEFT * 0.3), FadeIn(voter_title, shift=LEFT * 0.3), run_time=0.8)
            self.play(Create(hl_v), Create(join), run_time=0.6)
            vo.wait_until("and found the governor")
            self.play(gov_name.animate.set_color(ALICE), run_time=0.4)
            self.play(TransformFromCopy(gov_name, gov_copy, path_arc=0.6), run_time=1.1)
            self.play(Create(gov_row_hl), Flash(gov_copy, color=ALICE, flash_radius=0.6), run_time=0.7)
            vo.wait_until("The lesson")
            self.play(FadeOut(VGroup(hosp, hosp_title2, hl_h, gov_row_hl, gov_copy, join, hl_v)),
                      run_time=0.6)
            self.play(FadeIn(lesson1, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("not of how")
            self.play(FadeIn(lesson1b, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("and it must hold")
            self.play(FadeIn(lesson2, shift=UP * 0.2), GrowFromCenter(side_brace), run_time=0.8)
            self.play(Indicate(VGroup(voter, voter_title), color=S.WHITE, scale_factor=1.03),
                      run_time=vo.remaining(0.6))
        stage2 = VGroup(header2[0], unique, lessons, voter, voter_title, side_brace, blobs)

        # ========================================================== 3 · Dinur–Nissim reconstruction
        header3 = stage_header("Dinur & Nissim 2003", "· too many accurate answers ⇒ reconstruction")
        bits = [1, 0, 1, 1, 0, 0, 1, 0]
        cw, x0 = 0.46, -3.0
        cx = [x0 + cw / 2 + i * cw for i in range(8)]
        y_db, y_q, y_copy = -1.45, [-2.0, -2.38, -2.76], -3.3
        db = VGroup(*[bit_cell(str(b), cw, 0.38, stroke=X_COLOR).move_to([cx[i], y_db, 0])
                      for i, b in enumerate(bits)])
        db[0][0].set_stroke(ALICE, 3)
        db[0][1].set_color(ALICE)
        db_lab = S.text("database x", 22, X_COLOR).next_to(db, LEFT, buff=0.3)
        queries = [(0, 2, 3, 6), (1, 2, 4, 5, 7), (0, 1, 5, 6, 7)]
        q_ans = ["4.03", "0.98", "2.01"]
        q_noisy = ["5.7", "−0.6", "3.4"]
        q_rows, q_labs, q_vals, q_bars, q_vals_noisy, q_bars_noisy = (VGroup() for _ in range(6))
        for j, (qs, a, an) in enumerate(zip(queries, q_ans, q_noisy)):
            row = VGroup(*[Dot([cx[i], y_q[j], 0], radius=0.075,
                               color=S.WHITE if i in qs else S.GREY_DARK) for i in range(8)])
            for i in range(8):
                if i not in qs:
                    row[i].set_fill(opacity=0).set_stroke(S.GREY_DARK, 2)
            q_rows.add(row)
            q_labs.add(S.math(f"q_{j + 1}", size=30, color=S.GREY).next_to(row, LEFT, buff=0.4))
            v = S.text(f"→ {a}", 22, S.WHITE).move_to([1.2, y_q[j], 0], aligned_edge=LEFT)
            vn = S.text(f"→ {an}", 22, NOISE_COLOR).move_to([1.2, y_q[j], 0], aligned_edge=LEFT)
            q_vals.add(v)
            q_vals_noisy.add(vn)
            bx = 3.0
            q_bars.add(self._err_bar(bx, y_q[j], 0.04, S.WHITE))
            q_bars_noisy.add(self._err_bar(bx, y_q[j], 0.55, NOISE_COLOR))
        for lab in q_labs:
            lab.align_to(db_lab, RIGHT)
        err_lab = S.math(r"\text{error} \ll \sqrt{n}", size=32).move_to([3.75, y_q[1], 0], aligned_edge=LEFT)
        more = S.text("… many more questions", 20, S.GREY).next_to(err_lab, DOWN, buff=0.25).align_to(err_lab, LEFT)
        copy_bits = ["1", "0", "1", "1", "0", "1", "1", "0"]
        copy_q = VGroup(*[bit_cell("?", cw, 0.38, color=S.GREY).move_to([cx[i], y_copy, 0]) for i in range(8)])
        copy_f = VGroup(*[bit_cell(copy_bits[i], cw, 0.38,
                                   color=NOISE_COLOR if copy_bits[i] != str(bits[i]) else S.WHITE)
                          .move_to([cx[i], y_copy, 0]) for i in range(8)])
        copy_f[0][1].set_color(ALICE)
        copy_lab = S.text("attacker's copy", 22, S.WHITE).next_to(copy_q, LEFT, buff=0.3).align_to(db_lab, RIGHT)
        wrong_mark = S.text("✗", 22, NOISE_COLOR).next_to(copy_f[5], DOWN, buff=0.04)
        sub = S.math("42", "-", "41", "=", "1", size=40)
        sub[4].set_color(ALICE)
        sub.move_to([2.6, y_copy, 0])
        sub_lab = S.text("2 questions", 20, S.GREY).next_to(sub, RIGHT, buff=0.3)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(stage2), run_time=0.6)
            self.play(show_chip("dn03"), FadeIn(header3, shift=RIGHT * 0.2), run_time=1.0)
            self.play(FadeIn(db, shift=UP * 0.15), FadeIn(db_lab), run_time=0.8)
            vo.wait_until("proved something")
            self.play(FadeIn(copy_q, shift=UP * 0.15), FadeIn(copy_lab), run_time=0.8)
            vo.wait_until("Answer too many")
            for j in range(3):
                sel = VGroup(*[db[i] for i in queries[j]])
                self.play(FadeIn(q_labs[j]), LaggedStart(*[GrowFromCenter(d) for d in q_rows[j]], lag_ratio=0.05),
                          Indicate(sel, color=S.WHITE, scale_factor=1.08), run_time=0.55)
                self.play(FadeIn(q_vals[j], shift=RIGHT * 0.15), run_time=0.3)
            vo.wait_until("with errors much")
            self.play(LaggedStart(*[Create(b) for b in q_bars], lag_ratio=0.2), run_time=0.6)
            self.play(Write(err_lab), FadeIn(more), run_time=0.9)
            vo.wait_until("and an attacker")
            self.play(LaggedStart(*[Transform(copy_q[i], copy_f[i]) for i in range(1, 8)], lag_ratio=0.25),
                      run_time=2.2)
            self.play(FadeIn(wrong_mark, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Our subtraction")
            self.play(FadeIn(sub, shift=LEFT * 0.2), FadeIn(sub_lab), run_time=0.7)
            one = sub[4].copy()
            self.play(Transform(copy_q[0], copy_f[0]), one.animate.move_to(copy_f[0][1]).set_opacity(0),
                      run_time=0.9)
            self.remove(one)
            self.play(Flash(copy_q[0], color=ALICE, flash_radius=0.4),
                      Indicate(db[0], color=ALICE, scale_factor=1.15), run_time=0.8)
            vo.wait_until("Noise is the price")
            self.play(*[Transform(q_bars[j], q_bars_noisy[j]) for j in range(3)],
                      *[Transform(q_vals[j], q_vals_noisy[j]) for j in range(3)], run_time=0.9)
            self.play(*[Transform(copy_q[i], bit_cell("?", cw, 0.38, color=S.GREY).move_to(copy_q[i]))
                        for i in range(8)], FadeOut(wrong_mark), run_time=vo.remaining(0.6))
        stage3 = VGroup(header3, db, db_lab, copy_q, copy_lab, q_rows, q_labs, q_vals, q_bars, err_lab,
                        more, sub, sub_lab)

        # ========================================================== 4 · SuLQ: few questions, modest noise
        header4 = stage_header("Dwork & Nissim 2004", "· Blum, Dwork, McSherry & Nissim 2005", size=24)
        track_y = -1.55
        track = RoundedRectangle(width=4.6, height=0.2, corner_radius=0.1, stroke_color=S.GREY_DARK,
                                 stroke_width=1.5).set_fill(S.GREY_DARKER, 1).move_to([-3.0, track_y, 0])
        q_word = S.text("questions", 22, S.GREY).next_to(track, LEFT, buff=0.25)
        n_lab = S.math("n", size=32, color=S.GREY).next_to(track, RIGHT, buff=0.15)
        tick_x = [track.get_left()[0] + 0.12 + 0.17 * i for i in range(5)]
        ticks = VGroup(*[Line([x, track_y - 0.13, 0], [x, track_y + 0.13, 0], color=S.WHITE, stroke_width=3)
                         for x in tick_x])
        k_brace = Brace(ticks, DOWN, buff=0.12, color=S.WHITE)
        k_lab = S.math("k", size=30).next_to(k_brace, DOWN, buff=0.06)
        limit = VGroup(S.text("number of questions", 24, S.WHITE), S.math(r"k \ll n", size=34)).arrange(RIGHT, buff=0.2)
        limit.move_to([-3.0, -2.55, 0])
        bump_ax = Axes(x_range=[-3, 3, 1], y_range=[0, 0.55, 0.5], x_length=1.2, y_length=0.4, tips=False,
                       axis_config={"color": S.GREY_DARK, "stroke_width": 1.5, "include_ticks": False})
        bump = bump_ax.plot(lambda t: 0.5 * np.exp(-abs(t)), x_range=[-3, 3, 0.02], color=NOISE_COLOR,
                            stroke_width=3)
        noise_ic = VGroup(bump_ax, bump)
        noisy = VGroup(S.text("each answer: count +", 22, S.WHITE), noise_ic,
                       S.text("modest noise", 22, NOISE_COLOR)).arrange(RIGHT, buff=0.15)
        noisy.move_to([-3.0, -3.25, 0])
        sulq_big = S.text("SuLQ", 52, S.WHITE, weight="BOLD").move_to([3.7, -1.38, 0])
        sulq_full = S.text("Sub-Linear Queries", 26, S.GREY).next_to(sulq_big, DOWN, buff=0.18)
        for i in (0, 4, 10):                       # S, L, Q
            sulq_full[i].set_color(S.WHITE)
        sums = S.math(r"\textstyle\sum_i", r"g(x_i)", "+", r"\text{noise}", size=36)
        sums[3].set_color(NOISE_COLOR)
        sums.next_to(sulq_full, DOWN, buff=0.22)
        budget = Rectangle(width=ticks.get_right()[0] - track.get_left()[0] + 0.12, height=0.26, stroke_width=0)
        budget.set_fill(EPS_COLOR, 1).move_to(track.get_left(), aligned_edge=LEFT).shift(RIGHT * 0.02)
        seg = VGroup(*[Line([x, track_y - 0.13, 0], [x, track_y + 0.13, 0], color=S.BG, stroke_width=3)
                       for x in tick_x[1:]])
        budget_lab = VGroup(S.text("privacy budget", 24, EPS_COLOR), S.math(r"\varepsilon", size=36, color=EPS_COLOR)
                            ).arrange(RIGHT, buff=0.15).next_to(track, DOWN, buff=0.2).align_to(track, LEFT)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(stage3), run_time=0.6)
            self.play(show_chip("dn04", 0.8), FadeIn(header4, shift=RIGHT * 0.2), run_time=0.8)
            self.play(show_chip("sulq", 0.8, keep=True), run_time=0.8)
            self.play(FadeIn(track), FadeIn(q_word), FadeIn(n_lab), run_time=0.6)
            self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.3), run_time=0.8)
            self.play(GrowFromCenter(k_brace), FadeIn(k_lab), FadeIn(limit, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("modest noise")
            self.play(FadeIn(noisy, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("Dwork, Nissim")
            self.play(Indicate(chips["dn04"], color=S.WHITE, scale_factor=1.1),
                      Indicate(chips["sulq"], color=S.WHITE, scale_factor=1.1), run_time=0.9)
            vo.wait_until("called SuLQ")
            self.play(FadeIn(sulq_big, scale=0.8), run_time=0.6)
            self.play(FadeIn(sulq_full, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(VGroup(sulq_full[0], sulq_full[4], sulq_full[10]), color=S.WHITE, scale_factor=1.3),
                      run_time=0.6)
            vo.wait_until("which answers noisy")
            self.play(Write(sums), run_time=1.0)
            vo.wait_until("Remember that limit")
            self.play(Indicate(limit[1], color=S.WHITE, scale_factor=1.25), Indicate(ticks, color=S.WHITE),
                      run_time=1.1)
            vo.wait_until("This paper turns")
            self.play(FadeIn(budget), FadeIn(seg), FadeOut(ticks), FadeOut(k_brace), FadeOut(k_lab),
                      FadeIn(budget_lab, shift=UP * 0.1), run_time=1.0)
            self.play(Indicate(budget_lab, color=EPS_COLOR, scale_factor=1.08), run_time=vo.remaining(0.4))
        stage4_left = VGroup(header4, track, q_word, n_lab, limit, noisy, budget, seg, budget_lab)

        # ========================================================== 5 · all lanes flow into this paper
        tag_sums = VGroup(S.text("✗", 22, NOISE_COLOR), S.text("only sums", 22, S.GREY)).arrange(RIGHT, buff=0.12)
        tag_leak = VGroup(S.text("✗", 22, NOISE_COLOR), S.text("a tiny chance of a large leak", 22, S.GREY)
                          ).arrange(RIGHT, buff=0.12)
        tags = VGroup(tag_sums, tag_leak).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        tags.next_to(sums, DOWN, buff=0.25).set_x(3.7)

        packed = packed_positions(chips)
        frame_of = {k: (c[0][0] if k == "warner" else c[0]) for k, c in chips.items()}
        card = this_paper_card(3).move_to(CARD_CENTER)
        arrows, hand_labels = handover_arrows(card)
        p_lines = packed_lane_lines()
        p_labels = packed_lane_labels()
        caption = VGroup(S.text("TCC = a cryptography conference:", 26, S.GREY),
                         S.text("define security first,", 26, S.WHITE),
                         S.text("then prove it", 26, S.WHITE)).arrange(RIGHT, buff=0.16)
        caption.move_to([0, -2.95, 0])
        ul1 = Line(caption[1].get_corner(DL), caption[1].get_corner(DR), color=S.WHITE, stroke_width=2.5).shift(DOWN * 0.08)
        ul2 = Line(caption[2].get_corner(DL), caption[2].get_corner(DR), color=S.WHITE, stroke_width=2.5).shift(DOWN * 0.08)
        all_pins = VGroup(*pins.values())

        with self.voiceover(SAY[5]) as vo:
            self.play(Indicate(sums[0:2], color=S.WHITE), FadeIn(tag_sums, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("and its definition")
            self.play(FadeIn(tag_leak, shift=UP * 0.15), run_time=0.7)
            self.wait(max(0.0, vo.time_until("This paper takes") - 2.9))
            self.play(FadeOut(stage4_left), FadeOut(VGroup(sulq_big, sulq_full, sums)),
                      tags.animate.move_to([-3.0, -1.85, 0]), run_time=0.7)
            self.play(FadeOut(axis), FadeOut(all_pins), *[frames[k].animate.set_stroke(S.GREY) for k in active],
                      *[chips[k].animate.shift(packed[k] - frame_of[k].get_center()) for k in chips],
                      *[Transform(lanes[i], p_lines[i]) for i in range(3)],
                      *[Transform(lane_labels[i], p_labels[i]) for i in range(3)],
                      run_time=1.6)
            vo.wait_until("This paper takes")
            self.play(FadeIn(card.frame, scale=0.9), FadeIn(card.head), FadeIn(card.venue), FadeIn(card.empty),
                      run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25),
                      LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in hand_labels], lag_ratio=0.25),
                      run_time=1.2)
            self.bring_to_front(tags)
            vo.wait_until("any function")
            self.play(ReplacementTransform(tag_sums, card.anyf), run_time=0.9)
            vo.wait_until("one clean definition")
            self.play(ReplacementTransform(tag_leak, card.full[0]), FadeOut(card.empty[0]), run_time=0.9)
            vo.wait_until("and one simple rule")
            self.play(FadeOut(card.empty[1]), FadeIn(card.full[1], shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeOut(card.empty[2]), FadeIn(card.full[2], shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("Fittingly")
            self.play(Indicate(card.venue, color=S.YELLOW, scale_factor=1.3), run_time=0.8)
            self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("to define security")
            self.play(Create(ul1), Indicate(caption[1], color=S.WHITE, scale_factor=1.05), run_time=0.9)
            self.play(Circumscribe(card.frame, color=S.YELLOW, buff=0.06), run_time=1.2)
            vo.wait_until("and then prove")
            self.play(Create(ul2), Indicate(caption[2], color=S.WHITE, scale_factor=1.05), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _pin(chip, lane, years) -> VGroup:
        """Dots on the lane at the exact years + thin stems up to the chip (+ a span bar)."""
        y = LANE_Y[lane]
        g = VGroup()
        if len(years) == 2:
            g.add(Line([year_x(years[0]), y, 0], [year_x(years[1]), y, 0], color=S.GREY, stroke_width=6))
        for yr in years:
            px = year_x(yr)
            sx = float(np.clip(px, chip.get_left()[0] + 0.12, chip.get_right()[0] - 0.12))
            g.add(Line([px, y, 0], [sx, chip.get_bottom()[1], 0], color=S.GREY, stroke_width=1.5))
        dots = [Dot([year_x(yr), y, 0], radius=0.055, color=S.WHITE) for yr in years]
        return VGroup(*dots, *g)

    @staticmethod
    def _flavour_panel(title, names, vals, center):
        rows = database_rows(names, vals, color=S.GREY, width=2.05, row_height=0.34, size=20)
        rows.move_to(center)
        t = S.text(title, 24, S.WHITE).next_to(rows, UP, buff=0.22).align_to(rows, LEFT)
        return VGroup(t, rows)

    @staticmethod
    def _err_bar(x, y, half, color):
        w = 0.07
        return VGroup(Line([x - half, y, 0], [x + half, y, 0], color=color, stroke_width=3),
                      Line([x - half, y - w, 0], [x - half, y + w, 0], color=color, stroke_width=3),
                      Line([x + half, y - w, 0], [x + half, y + w, 0], color=color, stroke_width=3))
