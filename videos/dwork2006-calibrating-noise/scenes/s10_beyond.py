"""S10 · Beyond counting — three insensitive functions from the paper (§3.2–3.3, p. 274–276).

Three tiles; each one grows to fill the frame while it is narrated, then shrinks back:
  1. distance to a property (min cut of a social network)     [p. 274]
  2. functions with low sample complexity (Lemma 1)            [p. 275]
  3. outputs in a metric space (Theorem 2, bit strings)        [p. 276]
"""

from itertools import combinations
from math import comb

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.scene import VoiceScene

from common import (ALICE, EPS_COLOR, NARRATION, NOISE_COLOR, SENS_COLOR, TRUTH_COLOR, X_COLOR,
                    XP_COLOR)

SAY = NARRATION["S10"]

TILE_W, TILE_H, TILE_Y = 4.0, 4.3, -0.45
TILE_XS = (-4.25, 0.0, 4.25)
BIG_W, BIG_H = 13.0, 7.0
HEADER_Y = 2.95
COIN = S.GOLD          # Warner's coin, as in S11
COIN_EDGE = "#A87B2C"

# ------------------------------------------------------------------ tile 1: the network
NAMES = "ABCDEFGHIJ"
NET_CENTER = np.array([-2.6, -0.1, 0.0])
_ANG = {"A": 90, "B": 162, "C": 234, "D": 306, "E": 18,       # left cluster
        "F": 90, "G": 18, "H": 306, "I": 234, "J": 162}       # right cluster (mirrored)
_CLUSTER = {n: (-1.9 if n in "ABCDE" else 1.9) for n in NAMES}
NET_R = 1.25
EDGES = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A"), ("A", "C"), ("B", "D"),
         ("C", "E"),
         ("F", "G"), ("G", "H"), ("H", "I"), ("I", "J"), ("J", "F"), ("F", "H"), ("G", "I"),
         ("H", "J"),
         ("E", "J"), ("D", "I")]                                # the two bridges
BRIDGES = (16, 17)
CHANGED = 17                                                     # link D–I is removed


def min_cut(edges):
    """Global minimum edge cut by brute force (10 nodes: 511 bipartitions)."""
    best = None
    for mask in range(1, 2 ** (len(NAMES) - 1)):
        side = {NAMES[i] for i in range(len(NAMES)) if mask >> i & 1}
        c = sum((u in side) != (v in side) for u, v in edges)
        best = c if best is None else min(best, c)
    return best


assert min_cut(EDGES) == 2
assert min_cut([e for i, e in enumerate(EDGES) if i != CHANGED]) == 1


def node_pos(center, scale):
    out = {}
    for n in NAMES:
        a = np.deg2rad(_ANG[n])
        p = np.array([_CLUSTER[n] + NET_R * np.cos(a), NET_R * np.sin(a), 0.0])
        out[n] = center + scale * p
    return out


def build_network(center, scale, sw_edge, sw_node):
    pos = node_pos(center, scale)
    edges = VGroup(*[Line(pos[u], pos[v], color=S.GREY, stroke_width=sw_edge) for u, v in EDGES])
    nodes = VGroup(*[Circle(radius=0.27 * scale, color=S.WHITE, stroke_width=sw_node)
                     .set_fill(S.GREY_DARKER, 1).move_to(pos[n]) for n in NAMES])
    nodes.set_z_index(2)
    return VGroup(edges, nodes), pos


def link_rows(items, width=3.6, h=0.46):
    """Database rows for links, same look as explainer.components.database_rows."""
    rows = VGroup()
    for lab, val in items:
        box = Rectangle(width=width, height=h, stroke_color=S.GREY_DARK, stroke_width=1.5)
        box.set_fill(S.GREY_DARKER, 1)
        if lab is None:
            rows.add(VGroup(box, S.math(r"\vdots", size=26, color=S.GREY).move_to(box)))
            continue
        glyph = VGroup(Dot(radius=0.05, color=S.GREY), Line(LEFT * 0.14, RIGHT * 0.14, color=S.GREY,
                                                             stroke_width=2),
                       Dot(radius=0.05, color=S.GREY))
        glyph[0].move_to(glyph[1].get_start())
        glyph[2].move_to(glyph[1].get_end())
        glyph.move_to(box.get_left() + RIGHT * 0.32)
        name = S.text(lab, 24, S.WHITE, font=S.FONT_SANS).next_to(glyph, RIGHT, buff=0.2)
        v = value_text(val).move_to(box.get_right() + LEFT * 0.75)
        rows.add(VGroup(box, glyph, name, v))
    rows.arrange(DOWN, buff=0)
    return rows


def value_text(present):
    return S.text("present" if present else "absent", 24, S.WHITE if present else S.GREY,
                  font=S.FONT_SANS)


# ------------------------------------------------------------------ tile 2: the crowd
CROWD_ROWS, CROWD_COLS = 5, 12
ALICE_IDX = 4 * CROWD_COLS + 8


def build_crowd():
    icons = VGroup(*[person_icon(ALICE if i == ALICE_IDX else S.GREY, height=0.36)
                     for i in range(CROWD_ROWS * CROWD_COLS)])
    icons.arrange_in_grid(rows=CROWD_ROWS, cols=CROWD_COLS, buff=(0.14, 0.16))
    return icons


# ------------------------------------------------------------------ tile 3: bit strings
TRUE_BITS = [1, 0, 1, 1, 0, 1, 0, 0]
RATE = 0.45                                  # eps / (2 S): the decay rate drawn in the cloud
FLIP_P = 1 / (1 + np.exp(RATE))              # per-bit flip probability (0.389: a bit below 1/2)


def bit_cell(b, side, color=S.WHITE, digits=True):
    """A bit as in S11's tables: 1 = light cell, 0 = dark cell. Flipped bits get color=NOISE_COLOR."""
    flipped = color != S.WHITE
    sq = Square(side, stroke_color=color if flipped else S.BG, stroke_width=3 if flipped else 1.5)
    sq.set_fill(color if b else S.GREY_DARK, 0.85 if b else 1)
    if not digits:
        return VGroup(sq)
    d = S.text(str(b), 26, S.BG if b else (color if flipped else S.GREY), font=S.FONT_SANS).move_to(sq)
    return VGroup(sq, d)


def bit_string(bits, side=0.5, gap=0.1, colors=None, digits=True):
    colors = colors or [S.WHITE] * len(bits)
    g = VGroup(*[bit_cell(b, side, c, digits) for b, c in zip(bits, colors)])
    g.arrange(RIGHT, buff=gap)
    return g


def coin(r=0.17):
    disc = Circle(radius=r, stroke_color=COIN_EDGE, stroke_width=3).set_fill(COIN, 1)
    ring = Circle(radius=r * 0.68, stroke_color=COIN_EDGE, stroke_width=2)
    return VGroup(disc, ring)


def split_glyphs(mob, pieces):
    """Split a Text into VGroups of glyphs, one per piece of its string (pieces concatenate)."""
    full = "".join(pieces)
    keep_spaces = len(mob) == len(full)
    out, i = [], 0
    for p in pieces:
        n = len(p) if keep_spaces else len(p.replace(" ", ""))
        out.append(VGroup(*mob[i:i + n]))
        i += n
    assert i == len(mob), (i, len(mob), full)
    return out


def db_label(prime=False, size=26):
    col = XP_COLOR if prime else X_COLOR
    return VGroup(S.text("database", size, col),
                  S.math("x'" if prime else "x", size=size + 6, color=col)).arrange(RIGHT, buff=0.12,
                                                                                    aligned_edge=DOWN)


def true_label():
    return VGroup(S.text("true answer", 24, S.GREY), S.math("f(x)", size=30, color=TRUTH_COLOR)).arrange(
        RIGHT, buff=0.14, aligned_edge=DOWN)


def early(t):
    """Rate function: done in the first 40% of the animation (clear the other tiles before the grow)."""
    return smooth(min(1.0, 2.5 * t))


def late(t):
    """Rate function: only in the last 40% (bring the other tiles back once the shrink is mostly done)."""
    return smooth(max(0.0, 2.5 * t - 1.5))


def badge(num, color=S.WHITE, r=0.28):
    c = Circle(radius=r, color=color, stroke_width=3).set_fill(color, 0.12)
    return VGroup(c, S.text(str(num), 26, color).move_to(c))


class BeyondCounting(VoiceScene):
    # ---------------------------------------------------------------- tile mechanics
    def make_tile(self, i, cap_lines, small):
        frame = RoundedRectangle(width=TILE_W, height=TILE_H, corner_radius=0.22,
                                 stroke_color=S.GREY_DARK, stroke_width=2.5)
        frame.set_fill(S.GREY_DARKER, 0.55).move_to([TILE_XS[i], TILE_Y, 0])
        b = badge(i + 1).move_to(frame.get_corner(UL) + RIGHT * 0.5 + DOWN * 0.5)
        cap = VGroup(*[S.text(s, 30, S.WHITE) for s in cap_lines]).arrange(DOWN, buff=0.14)
        cap.move_to(frame.get_bottom() + UP * 0.85)
        small.move_to(frame.get_center() + UP * 0.45)
        tile = VGroup(frame, b, cap, small)
        tile.cap_lines = list(cap_lines)          # (Text.text drops spaces, so keep the strings)
        return tile

    def expand(self, tile, big_content, others, title, run_time=1.1):
        frame, b, cap, content = tile
        tile.save_state()
        big = RoundedRectangle(width=BIG_W, height=BIG_H, corner_radius=0.3, stroke_color=S.WHITE,
                               stroke_width=2.5).set_fill(S.GREY_DARKER, 0.55)
        b_t = badge(b[1].original_text, S.WHITE, r=0.32).move_to([-5.95, HEADER_Y, 0])
        header = S.text(" ".join(tile.cap_lines), 36, S.WHITE)
        header.next_to(b_t, RIGHT, buff=0.3)
        parts = split_glyphs(header, [tile.cap_lines[0] + " ", tile.cap_lines[1]])
        self.play(FadeOut(others, rate_func=early), FadeOut(title, rate_func=early),
                  Transform(frame, big), Transform(b, b_t),
                  Transform(cap[0], parts[0]), Transform(cap[1], parts[1]),
                  Transform(content, big_content), run_time=run_time)

    def collapse(self, tile, others, title, details, run_time=0.75):
        tile.saved_state[0].set_stroke(S.GREY)          # come back marked as "done"
        self.play(FadeOut(details), run_time=0.35)
        self.play(Restore(tile), FadeIn(others, rate_func=late), FadeIn(title, rate_func=late),
                  run_time=run_time)

    def light(self, tile):
        return AnimationGroup(tile[0].animate.set_stroke(S.WHITE, 3.5),
                              Indicate(VGroup(tile[1], tile[2]), color=S.WHITE, scale_factor=1.12))

    # ---------------------------------------------------------------- the scene
    def construct(self):
        title = S.text("Beyond counting", 44).to_edge(UP, buff=0.45)

        # mini + full-size versions of each tile's picture (same structure, so Transform morphs)
        net_small, _ = build_network(ORIGIN, 0.47, 1.8, 1.6)
        net_big, pos = build_network(NET_CENTER, 1.0, 3.5, 2.5)
        crowd_big = build_crowd().move_to([-3.55, 1.15, 0])
        crowd_small = crowd_big.copy().scale(0.62)
        rng = np.random.default_rng(10)
        hint = rng.choice([i for i in range(60) if i != ALICE_IDX], size=6, replace=False)
        for i in hint:
            crowd_small[i].set_fill(S.WHITE)
        bits_big = bit_string(TRUE_BITS, side=0.5, gap=0.1).move_to([3.4, 0.95, 0])
        bits_small = VGroup(*[c[0] for c in bit_string(TRUE_BITS, side=0.31, gap=0.07, digits=False)])
        bits_big_sq = VGroup(*[c[0] for c in bits_big])
        bits_digits = VGroup(*[c[1] for c in bits_big])

        tiles = VGroup(
            self.make_tile(0, ["Distance to", "a property"], net_small),
            self.make_tile(1, ["Small random", "samples"], crowd_small),
            self.make_tile(2, ["Outputs that", "aren’t numbers"], bits_small),
        )

        # ============================================================ 0. three tiles
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in tiles], lag_ratio=0.25),
                      run_time=1.3)
            vo.wait_until("Three examples")
            self.play(LaggedStart(*[self.light(t) for t in tiles], lag_ratio=0.35),
                      run_time=vo.remaining(1.4))
            self.play(*[t[0].animate.set_stroke(S.GREY_DARK) for t in tiles], run_time=0.3)

        # ============================================================ 1. distance to a property
        t1 = tiles[0]
        letters = VGroup(*[S.text(n, 22, S.WHITE, font=S.FONT_SANS).move_to(pos[n]) for n in NAMES])
        letters.set_z_index(3)
        present = set(EDGES)
        absent = [(u, v) for u, v in combinations(NAMES, 2)
                  if (u, v) not in present and (v, u) not in present]
        ghosts = VGroup(*[DashedLine(pos[u], pos[v], color=S.GREY, stroke_width=1.5, dash_length=0.08,
                                     stroke_opacity=0.45) for u, v in absent])
        rows_items = [("A–B", True), ("A–C", True), ("A–D", False), (None, None), ("D–I", True),
                      ("E–J", True), (None, None), ("I–J", True)]
        rows = link_rows(rows_items).move_to([4.25, -0.05, 0])
        db_head = VGroup(db_label(),
                         S.text(f"{len(absent) + len(EDGES)} rows", 22, S.GREY))
        db_head.arrange(RIGHT, buff=0.3, aligned_edge=DOWN).next_to(rows, UP, buff=0.22)
        caption = S.text("each possible link = one row  (present / absent)", 28, S.GREY)
        caption.move_to([0, -2.75, 0])

        cut_x = -2.6
        cut = DashedLine([cut_x, 1.65, 0], [cut_x, -1.75, 0], color=NOISE_COLOR, stroke_width=5,
                         dash_length=0.14)
        cut_lab = VGroup(S.text("min cut =", 30, TRUTH_COLOR), S.text("2", 34, TRUTH_COLOR))
        cut_lab.arrange(RIGHT, buff=0.15, aligned_edge=DOWN).move_to([cut_x, 2.1, 0])
        one = S.text("1", 34, TRUTH_COLOR).move_to(cut_lab[1])
        sens_tag = S.text("1-sensitive", 30, SENS_COLOR).next_to(cut_lab, RIGHT, buff=0.55)

        qa_pieces = ["how many ", "links", " must you ", "cut", " to ", "split the network in two", "?"]
        qb_pieces = ["how many ", "rows", " must you ", "change", " to ", "make P true", "?"]
        qa = S.text("".join(qa_pieces), 30, S.WHITE).move_to(caption)
        qb = S.text("".join(qb_pieces), 30, S.WHITE)
        qb_tail = S.text("→  sensitivity 1", 28, SENS_COLOR)
        VGroup(qb, qb_tail).arrange(RIGHT, buff=0.3).move_to(caption)
        qa_p, qb_p = split_glyphs(qa, qa_pieces), split_glyphs(qb, qb_pieces)
        for k in (1, 3, 5):
            qa_p[k].set_color(S.YELLOW)
            qb_p[k].set_color(S.YELLOW)

        edges = net_small[0]   # after the Transform, net_small has the full-size geometry
        with self.voiceover(SAY[1]) as vo:
            self.expand(t1, net_big, VGroup(tiles[1], tiles[2]), title)
            self.play(FadeIn(letters), run_time=0.5)
            vo.wait_until("each possible link")
            self.play(Create(ghosts, lag_ratio=0.05), FadeIn(db_head),
                      LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.12),
                      run_time=1.5)
            self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.6)
            self.play(FadeOut(ghosts), run_time=0.6)
            vo.wait_until("How many links")
            self.play(FadeOut(caption), FadeIn(qa), run_time=0.6)
            self.play(Create(cut), *[edges[i].animate.set_stroke(NOISE_COLOR, 5) for i in BRIDGES],
                      run_time=0.9)
            self.play(FadeIn(cut_lab, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("That minimum cut")
            self.play(Circumscribe(cut_lab, color=S.WHITE), run_time=1.0)
            vo.wait_until("when one link changes")
            self.play(edges[CHANGED].animate.set_stroke(ALICE, 7), rows[4][0].animate.set_stroke(ALICE, 3),
                      rows[4][2].animate.set_color(ALICE), run_time=0.5)
            gone = DashedLine(pos["D"], pos["I"], color=S.GREY, stroke_width=1.5, dash_length=0.08,
                              stroke_opacity=0.45)
            self.play(edges[CHANGED].animate.set_stroke(opacity=0), FadeIn(gone),
                      Transform(rows[4][3], value_text(False).move_to(rows[4][3])),
                      run_time=0.6)
            self.play(Transform(cut_lab[1], one), Flash(cut_lab[1], color=ALICE, flash_radius=0.35),
                      run_time=0.6)
            vo.wait_until("so it is one-sensitive")
            self.play(FadeIn(sens_tag, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("In general")
            self.play(ShowPassingFlash(Underline(qa_p[5], color=S.YELLOW, stroke_width=4, buff=0.06),
                                       time_width=0.8), run_time=0.9)
            vo.wait_until("how many rows")
            self.play(*[Transform(qa_p[k], qb_p[k]) for k in (0, 2, 4, 6)],
                      *[FadeOut(qa_p[k], shift=UP * 0.25) for k in (1, 3, 5)],
                      *[FadeIn(qb_p[k], shift=UP * 0.25) for k in (1, 3, 5)], run_time=1.2)
            self.remove(qa, *qa_p, *qb_p)
            self.add(qb)
            vo.wait_until("to make something true")
            self.play(ShowPassingFlash(Underline(qb_p[5], color=S.YELLOW, stroke_width=4, buff=0.06),
                                       time_width=0.8), run_time=0.9)
            vo.wait_until("has sensitivity one")
            self.play(FadeIn(qb_tail, shift=LEFT * 0.2), run_time=0.6)
        details1 = VGroup(letters, rows, db_head, cut, cut_lab, sens_tag, qb, qb_tail, gone)

        # ============================================================ 2. small random samples
        t2 = tiles[1]
        crowd = crowd_small              # morphs into crowd_big
        alg = RoundedRectangle(width=1.05, height=0.95, corner_radius=0.12, stroke_color=S.WHITE,
                               stroke_width=2.5).set_fill(S.GREY_DARKER, 1).move_to([0.35, 1.15, 0])
        alg_lab = S.math("A", size=48).move_to(alg)
        alg_g = VGroup(alg, alg_lab)
        db_lab = db_label().move_to([-5.15, -0.42, 0])
        db_lab_p = db_label(prime=True).move_to(db_lab, aligned_edge=LEFT)
        line_y = -1.9
        nline = Line([-6.0, line_y, 0], [0.5, line_y, 0], color=S.GREY, stroke_width=2.5)
        nline_lab = S.text("answers", 22, S.GREY).next_to(nline.get_end(), DOWN, buff=0.18).align_to(nline, RIGHT)
        fx_x, fxp_x, sig = -3.4, -1.9, 0.95

        def tick(x, col):
            return Line([x, line_y - 0.16, 0], [x, line_y + 0.16, 0], color=col, stroke_width=4)

        def band(x, col):
            return Rectangle(width=2 * sig, height=0.56, stroke_width=0).set_fill(col, 0.2).move_to([x, line_y, 0])

        fx_t, fxp_t = tick(fx_x, X_COLOR), tick(fxp_x, XP_COLOR)
        fx_l = S.math("f(x)", size=32, color=X_COLOR).next_to(fx_t, DOWN, buff=0.14)
        fxp_l = S.math("f(x')", size=32, color=XP_COLOR).next_to(fxp_t, DOWN, buff=0.14)
        fx_b, fxp_b = band(fx_x, X_COLOR), band(fxp_x, XP_COLOR)
        sig_br = BraceBetweenPoints([fx_x, line_y + 0.3, 0], [fx_x + sig, line_y + 0.3, 0], UP,
                                    color=X_COLOR, buff=0.02)
        sig_lab = S.math(r"\sigma", size=32, color=X_COLOR).next_to(sig_br, UP, buff=0.06)
        gap_br = BraceBetweenPoints([fx_x, line_y - 0.62, 0], [fxp_x, line_y - 0.62, 0], DOWN,
                                    color=SENS_COLOR, buff=0.02)
        gap_lab = S.math(r"\le 2\sigma", size=32, color=SENS_COLOR).next_to(gap_br, DOWN, buff=0.08)

        lem_head = S.text("Lemma 1", 30, S.YELLOW, weight="BOLD")
        lem = VGroup(
            S.tex(r"If $A$ reads each row", size=38),
            S.tex(r"with probability $\le \alpha$,", size=38),
            S.tex(r"and is within $\sigma$ of $f$", size=38),
            S.tex(r"most of the time,", size=38),
            S.tex(r"on every database,", size=38),
            S.tex(r"then ", r"$S(f) \le 2\sigma$", r".", size=38),
        )
        lem[5][1].set_color(SENS_COLOR)
        lem_note = S.tex(r"(``most'': prob.\ $\ge (1+\alpha)/2$)", size=30, color=S.GREY)
        lem_body = VGroup(lem_head, *lem).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lem_head.shift(UP * 0.1)
        lem_note.next_to(lem_body, DOWN, buff=0.35).align_to(lem_body, LEFT)
        VGroup(lem_body, lem_note).move_to([3.85, 0.45, 0])
        lem_frame = SurroundingRectangle(VGroup(lem_body, lem_note), color=S.GREY_DARK, buff=0.3,
                                         corner_radius=0.12, stroke_width=2)

        samples = [rng.choice([i for i in range(60) if i != ALICE_IDX], size=6, replace=False)
                   for _ in range(3)]
        landings = [-3.0, -3.8, -2.62]                 # A's answers: all within sigma of f(x)

        def sample_round(idx, land, drop=True, rt=1.3):
            lit = [crowd[i].animate.set_fill(S.WHITE) for i in idx]
            self.play(*lit, run_time=0.3 * rt)
            flyers = VGroup(*[crowd[i].copy() for i in idx])
            self.play(LaggedStart(*[f.animate.scale(0.5).move_to(alg) for f in flyers], lag_ratio=0.08),
                      run_time=0.45 * rt)
            self.remove(*flyers)
            dot = Dot(alg.get_bottom(), radius=0.08, color=S.WHITE).set_z_index(4)
            anims = [crowd[i].animate.set_fill(S.GREY) for i in idx]
            if drop:
                self.add(dot)
                anims.append(dot.animate(path_arc=0.5).move_to([land, line_y, 0]))
            self.play(Indicate(alg_lab, color=S.WHITE), *anims, run_time=0.45 * rt)
            return dot if drop else None

        with self.voiceover(SAY[2]) as vo:
            self.collapse(t1, VGroup(tiles[1], tiles[2]), title, details1)
            self.expand(t2, crowd_big, VGroup(tiles[0], tiles[2]), title, run_time=1.0)
            self.play(FadeIn(db_lab), FadeIn(alg_g, shift=LEFT * 0.2), Create(nline), FadeIn(nline_lab),
                      FadeIn(fx_t), FadeIn(fx_l), FadeIn(lem_frame), FadeIn(lem_head),
                      FadeIn(lem[0]), FadeIn(lem[1]), run_time=0.9)
            vo.wait_until("like one working")
            d1 = sample_round(samples[0], landings[0])
            d2 = sample_round(samples[1], landings[1])
            vo.wait_until("approximates f")
            self.play(FadeIn(fx_b), GrowFromCenter(sig_br), FadeIn(sig_lab), FadeIn(lem[2]), FadeIn(lem[3]),
                      run_time=0.8)
            p = sample_round(samples[2], landings[2], rt=1.0)
            vo.wait_until("on every database")
            self.play(ReplacementTransform(db_lab, db_lab_p), Indicate(crowd[ALICE_IDX], color=ALICE,
                                                                      scale_factor=1.5),
                      FadeIn(lem[4]), run_time=0.8)
            self.play(FadeIn(fxp_t), FadeIn(fxp_l), FadeIn(fxp_b), FadeOut(d1), FadeOut(d2),
                      run_time=0.7)
            vo.wait_until("then f has")
            self.play(Flash(p, color=S.WHITE, flash_radius=0.3), run_time=0.6)
            self.play(GrowFromCenter(gap_br), FadeIn(gap_lab), FadeIn(lem[5]), run_time=0.9)
            self.play(FadeIn(lem_note), run_time=0.6)
            vo.wait_until("That is Lemma 1")
            self.play(Circumscribe(VGroup(lem_body, lem_note), color=S.YELLOW, buff=0.25),
                      run_time=vo.remaining(0.9))
        details2 = VGroup(db_lab_p, alg_g, nline, nline_lab, fx_t, fx_l, fxp_t, fxp_l, fx_b, fxp_b,
                          sig_br, sig_lab, gap_br, gap_lab, p, lem_frame, lem_body, lem_note)

        # ============================================================ 3. outputs that aren't numbers
        t3 = tiles[2]
        lab_kw = dict(size=24, color=S.GREY)
        ranking = VGroup(*[S.text(s, 30) for s in ("1.  Bea", "2.  Ann", "3.  Cal")])
        ranking.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([-4.6, 0.85, 0])
        rank_l = S.text("a ranking", **lab_kw).next_to(ranking, UP, buff=0.35)
        aset = S.math(r"\{\,\text{Ann},\ \text{Cal},\ \text{Dee}\,\}", size=42).move_to([-1.0, 0.85, 0])
        set_l = S.text("a set", **lab_kw).move_to([aset.get_x(), rank_l.get_y(), 0])
        bits_l = S.text("a string of bits", **lab_kw).move_to([bits_big.get_x(), rank_l.get_y(), 0])
        any_cap = S.text("rankings, sets, bit strings: anything with a distance", 30, S.WHITE)
        any_cap.move_to([0, -1.25, 0])
        dist_word = split_glyphs(any_cap, ["rankings, sets, bit strings: anything with a ", "distance"])[1]

        # the cloud of candidate outputs, one dot per bit string, ring k = Hamming distance k
        cc = np.array([-3.6, -0.45, 0.0])
        cloud = VGroup()
        for k in range(1, 9):
            n_k, r_k = comb(8, k), 0.62 + 0.26 * (k - 1)
            w = np.exp(-RATE * k)                       # weight of each string at distance k
            phase = 0.37 * k
            ring = VGroup(*[Dot(cc + r_k * np.array([np.cos(phase + 2 * np.pi * j / n_k),
                                                     np.sin(phase + 2 * np.pi * j / n_k), 0]),
                                radius=0.05, color=NOISE_COLOR, fill_opacity=max(0.1, w))
                            for j in range(n_k)])
            cloud.add(ring)
        centre = Dot(cc, radius=0.1, color=TRUTH_COLOR).set_z_index(3)
        centre_l = S.math("f(x)", size=30, color=TRUTH_COLOR).next_to(centre, DOWN, buff=0.06)
        d_arrow = Arrow(cc + 0.66 * np.array([np.cos(2.3), np.sin(2.3), 0]),
                        cc + 2.9 * np.array([np.cos(2.3), np.sin(2.3), 0]), buff=0, color=S.GREY,
                        stroke_width=3, tip_length=0.16)
        d_lab = S.text("distance", 22, S.GREY).next_to(d_arrow.get_end(), UP, buff=0.1)
        cloud_cap = S.text("all 256 strings of 8 bits", 22, S.GREY).next_to(cloud, DOWN, buff=0.18)

        formula = S.math(r"\Pr[y]", r"\;\propto\;", r"\exp\!\Big(-\frac{", r"\varepsilon",
                         r"\,\mathrm{dist}(y,", r"f(x)", r")}{2\,", r"S(f)", r"}\Big)", size=40)
        formula[3].set_color(EPS_COLOR)
        formula[7].set_color(SENS_COLOR)
        formula.move_to([2.95, 0.45, 0])
        thm = S.tex(r"Theorem 2: ", r"$\varepsilon$", r"-indistinguishable", size=32, color=S.GREY)
        thm[1].set_color(EPS_COLOR)
        thm.next_to(formula, DOWN, buff=0.35)
        true_l = true_label()
        bits_top = bits_big.copy().move_to([3.0, 2.0, 0])
        true_l.next_to(bits_top, UP, buff=0.18)

        # bit flipping: Warner's coin applied to the answer
        flip_rng = np.random.default_rng(4)
        draws = []
        while len(draws) < 7:
            f = flip_rng.random(8) < FLIP_P
            if 2 <= f.sum() <= 4:
                draws.append(f)
        true_left = bits_big.copy().move_to([-3.4, 1.35, 0])
        true_left_l = true_label().next_to(true_left, UP, buff=0.18)

        def released(flips):
            vals = [b ^ int(f) for b, f in zip(TRUE_BITS, flips)]
            cols = [NOISE_COLOR if f else S.WHITE for f in flips]
            return bit_string(vals, side=0.5, gap=0.1, colors=cols).move_to([-3.4, -1.25, 0])

        out_bits = released([False] * 8)
        out_l = S.text("released", 24, S.GREY).next_to(out_bits, DOWN, buff=0.18)
        coins = VGroup(*[coin().move_to([c.get_x(), -0.1, 0]) for c in out_bits])
        flip_f = S.math(r"\Pr[\text{bit flips}]", r"=", r"\frac{1}{1+e^{", r"\varepsilon", r"/(2",
                        r"S(f)", r")}}", r"<", r"\tfrac12", size=38)
        flip_f[3].set_color(EPS_COLOR)
        flip_f[5].set_color(SENS_COLOR)
        flip_f.move_to([2.95, -1.45, 0])
        warner = S.text("Warner’s coin again, applied to the answer", 30, COIN).move_to([0, -2.85, 0])

        with self.voiceover(SAY[3]) as vo:
            self.collapse(t2, VGroup(tiles[0], tiles[2]), title, details2)
            self.expand(t3, bits_big_sq, VGroup(tiles[0], tiles[1]), title, run_time=1.0)
            self.play(FadeIn(bits_digits), FadeIn(bits_l), run_time=0.4)
            vo.wait_until("a ranking")
            self.play(FadeIn(rank_l), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in ranking],
                                                  lag_ratio=0.2), run_time=0.7)
            vo.wait_until("a set")
            self.play(FadeIn(set_l), Write(aset), run_time=0.6)
            vo.wait_until("a string of bits")
            self.play(Indicate(VGroup(bits_l, bits_digits), color=S.WHITE), run_time=0.6)
            vo.wait_until("anything with a distance")
            self.play(FadeIn(any_cap, shift=UP * 0.15), run_time=0.7)
            self.play(Indicate(dist_word, color=S.YELLOW), run_time=0.8)

            vo.wait_until("Pick an output")
            sqs = t3[3]                                   # the tile's squares, now full size
            bits_now = VGroup(*[VGroup(sqs[i], bits_digits[i]) for i in range(8)])
            self.play(FadeOut(VGroup(ranking, rank_l, aset, set_l, any_cap, bits_l)),
                      bits_now.animate.move_to(bits_top), FadeIn(true_l), run_time=0.9)
            self.play(FadeIn(centre, scale=0.5), FadeIn(centre_l), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(ring, scale=0.85) for ring in cloud], lag_ratio=0.3),
                      GrowArrow(d_arrow), FadeIn(d_lab), FadeIn(cloud_cap), run_time=2.2)
            vo.wait_until("decays exponentially")
            self.play(Write(formula), run_time=1.6)
            vo.wait_until("at a rate of")
            self.play(Indicate(formula[3], color=EPS_COLOR, scale_factor=1.4),
                      Indicate(formula[7], color=SENS_COLOR, scale_factor=1.2), run_time=1.0)
            self.play(FadeIn(thm, shift=UP * 0.15), run_time=0.6)

            vo.wait_until("For bit strings")
            self.play(FadeOut(VGroup(cloud, centre, centre_l, d_arrow, d_lab, cloud_cap, true_l)),
                      bits_now.animate.move_to(true_left), FadeIn(true_left_l), run_time=0.9)
            self.play(FadeIn(out_bits), FadeIn(out_l), FadeIn(flip_f, shift=UP * 0.15), run_time=0.7)
            cur = out_bits
            for flips in draws[:2]:
                self.play(Transform(cur, released(flips)), run_time=0.4)
                self.wait(0.2)
            vo.wait_until("a little below")
            self.play(Transform(cur, released(draws[2])),
                      Indicate(flip_f[7:], color=S.WHITE, scale_factor=1.3), run_time=0.9)
            vo.wait_until("Warner's coin again")
            self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in coins], lag_ratio=0.08),
                      FadeIn(warner, shift=UP * 0.15), run_time=0.8)
            for flips in draws[3:]:
                if vo.remaining(0) < 0.6:                 # the coins flip while the line is spoken
                    break
                self.play(*[c.animate.stretch_to_fit_width(0.03) for c in coins], run_time=0.18)
                self.play(*[c.animate.stretch_to_fit_width(0.34) for c in coins],
                          Transform(cur, released(flips)), run_time=0.27)
                self.wait(0.3)
        details3 = VGroup(bits_digits, true_left_l, out_bits, out_l, coins, flip_f, formula, thm, warner)
        self.collapse(t3, VGroup(tiles[0], tiles[1]), title, details3)
        self.play(LaggedStart(*[Indicate(VGroup(t[1], t[2]), color=S.WHITE, scale_factor=1.08)
                                for t in tiles], lag_ratio=0.25), run_time=0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
