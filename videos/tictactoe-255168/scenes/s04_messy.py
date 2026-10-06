"""S04 · Counting by hand gets messy.

Beats:
  1. A legal game that O wins on move 6 (X0 O3 X1 O4 X6 O5, O's middle row YELLOW). A copy slides
     right and X's 5th mark hops from square 6 to square 2: now X's top row is complete too, so the
     game was "already over at move 5" (RED stamp) and O's 6th mark becomes a ghost.
  2. Column subtraction with pictures: ways O could line up 5,760 (8 lines x 6 orders x 6 x 5 x 4,
     each factor pulsing with its picture as it is named; the "already over" board leaves meanwhile),
     minus X already won 432: on "Then we subtract" the "already over" board comes back small next to
     its label and "-432" is written; then it grows (opening board style, move numbers) and a quarter
     turn of it gives the column version: O's row with X's parallel row, O's column with X's parallel
     column, side by side, with the count of the pairs under them ("3 rows x 2 other rows + 3 columns
     x 2 other columns = 12 pairs", O's choices in O's colour, X's in X's). Both pulse on "so X
     sneaked", then shrink into the row as the count gives way to "12 pairs (O's line, X's parallel
     line) x 6 x 6". = 5,328 (GREEN); the heading slides down to label it.
  3. A table of hand counts (move 5 -> 1,440, move 6 -> 5,328, moves 7-9 -> ?) wrapped in a tangle of
     crossing arrows, small legal boards and grey questions.
  4. The tangle fades; a laptop draws itself and plays games one by one (the first games the program
     really finds), with a GREEN counter: "Plan B: let a computer play every game".

All boards are legal positions (checked against winner()); all numbers are exact.
"""

import numpy as np
from manim import *

from explainer import i18n
from explainer import style as S
from explainer.scene import VoiceScene

from common import (BY_MOVE, COUNT_COLOR, DRAW_COLOR, GHOST_COLOR, NARRATION, O_COLOR, UNDO_COLOR,
                    WIN_COLOR, WIN_LINES, X_COLOR, Board, mark_anim, mini_board, move_number, winner)

SAY = NARRATION["S04"]
W = S.WHITE


# ------------------------------------------------------------------ helpers
def rich(parts, size, font=S.FONT):
    """One Text (so the baseline stays straight) coloured piece by piece.

    parts = [(string, colour), ...]; returns (text, [VGroup of the glyphs of each part]).
    In a language version each part is translated on its own (i18n part keys), so the colours and
    the per-part pieces land on the translated glyphs (English: tr() returns the part unchanged)."""
    parts = [(i18n.tr(p), col) for p, col in parts]
    if i18n.active():
        # no half-width spaces next to a full-width bracket, which has its own white space
        # ("6 种顺序  ×  （6 × 5" -> "6 种顺序  ×（6 × 5", zh glossary B1)
        for i in range(len(parts) - 1):
            (a, ca), (b, cb) = parts[i], parts[i + 1]
            if b[:1] in "（“":
                parts[i] = (a.rstrip(), ca)
            if a[-1:] in "）”":
                parts[i + 1] = (b.lstrip(), cb)
    s = "".join(p for p, _ in parts)
    t = S.text(s, size, W, font=font, disable_ligatures=True)
    assert len(t) == len(s), "glyphs and characters out of step"
    pieces, k = [], 0
    for p, col in parts:
        piece = VGroup(*t[k:k + len(p)])
        piece.set_color(col)
        pieces.append(piece)
        k += len(p)
    return t, pieces


def first_games(n: int):
    """The first n finished games in the order the program (explore) finds them."""
    out, board = [], ["."] * 9

    def explore(player, seq):
        if len(out) >= n:
            return
        w = winner(board)
        if w is not None or "." not in board:
            line = next((ln for ln in WIN_LINES if board[ln[0]] != "."
                         and board[ln[0]] == board[ln[1]] == board[ln[2]]), None)
            out.append(("".join(board), list(seq), line))
            return
        for sq in range(9):
            if board[sq] == ".":
                board[sq] = player
                explore("O" if player == "X" else "X", seq + [sq])
                board[sq] = "."

    explore("X", [])
    return out


def check_legal(moves) -> str:
    """Play squares in order (X first); assert nobody had won before the last move."""
    b = ["."] * 9
    for k, sq in enumerate(moves):
        assert b[sq] == "." and winner(b) is None, (moves, k)
        b[sq] = "X" if k % 2 == 0 else "O"
    return "".join(b)


def laptop(center, w: float = 4.4, h: float = 2.75) -> VGroup:
    """A simple laptop: screen (outer frame + dark glass) and a keyboard trapezoid with keys."""
    c = np.array(center, dtype=float)
    outer = RoundedRectangle(width=w, height=h, corner_radius=0.18, stroke_color=S.GREY,
                             stroke_width=4).set_fill(S.GREY_DARKER, 1).move_to(c)
    glass = Rectangle(width=w - 0.36, height=h - 0.36, stroke_width=0).set_fill("#07090D", 1).move_to(c)
    yb, x0 = outer.get_bottom()[1], c[0]
    top_hw, bot_hw, dh = w / 2 + 0.12, w / 2 + 0.62, 0.48
    base = Polygon([x0 - top_hw, yb - 0.04, 0], [x0 + top_hw, yb - 0.04, 0],
                   [x0 + bot_hw, yb - 0.04 - dh, 0], [x0 - bot_hw, yb - 0.04 - dh, 0],
                   stroke_color=S.GREY, stroke_width=3).set_fill(S.GREY_DARK, 1)
    keys = VGroup()
    for r, (y, n) in enumerate([(yb - 0.15, 13), (yb - 0.27, 14)]):
        frac = (yb - 0.04 - y) / dh
        half = top_hw + (bot_hw - top_hw) * frac - 0.35
        for j in range(n):
            x = x0 - half + 2 * half * (j + 0.5) / n
            keys.add(Rectangle(width=2 * half / n * 0.72, height=0.07, stroke_width=0)
                     .set_fill(S.GREY, 0.55).move_to([x, y, 0]))
    pad = RoundedRectangle(width=0.9, height=0.09, corner_radius=0.04, stroke_width=0) \
        .set_fill(S.GREY, 0.7).move_to([x0, yb - 0.41, 0])
    g = VGroup(outer, glass, base, keys, pad)
    g.glass = glass
    return g


class DimmedMove(Transform):
    """Transform that fades the moving text down mid-way (so it passes faintly over other text)."""

    def __init__(self, mobject, target, low: float = 0.06, **kw):
        self.low = low
        super().__init__(mobject, target, **kw)

    def interpolate_mobject(self, alpha: float) -> None:
        super().interpolate_mobject(alpha)
        dip = min(1.0, 2.8 * np.sin(PI * alpha))             # 0 at both ends, 1 for most of the way
        self.mobject.set_fill(opacity=1 - (1 - self.low) * dip)


class SwoopMove(Transform):
    """Transform whose mobject swoops into place as one rigid piece (scaling as it goes): its centre
    follows a curve that starts sideways (dipping `dip` lower) and ends going straight up (or, given
    `ctrl`, the quadratic curve through that control point).

    (Transform's own path_arc moves every point on its own arc, which tilts a shrinking board mid-way;
    here the straight-path Transform is shifted so that only the group's centre follows the curve.)"""

    def __init__(self, mobject, target, dip: float = 0.25, ctrl=None, **kw):
        self.c0, self.c1 = mobject.get_center(), target.get_center()
        self.ctrl = (np.array([self.c1[0], self.c0[1] - dip, 0.0]) if ctrl is None
                     else np.array(ctrl, dtype=float))
        super().__init__(mobject, target, **kw)

    def interpolate_mobject(self, alpha: float) -> None:
        super().interpolate_mobject(alpha)
        a = self.rate_func(alpha)
        on_curve = (1 - a) ** 2 * self.c0 + 2 * (1 - a) * a * self.ctrl + a ** 2 * self.c1
        self.mobject.shift(on_curve - interpolate(self.c0, self.c1, a))


class Messy(VoiceScene):
    def regroup(self, *mobs) -> VGroup:
        """Replace several top-level mobjects by one group (so later transforms leave nothing behind)."""
        return self.adopt(VGroup(*mobs))

    def adopt(self, group):
        """Make `group` the only top-level owner of its members, so FadeOut(group) really removes them
        (FadeOut of a wrapper leaves members that were added on their own behind)."""
        fam = {id(m) for m in group.get_family()}
        self.remove(*[m for m in self.mobjects if any(id(s) in fam for s in m.get_family())])
        self.add(group)
        return group

    def construct(self):
        self.beat_two_lines()
        self.beat_subtract()
        self.beat_tangle()
        self.beat_plan_b()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)

    # ============================================================== 1. O wins on move 6 ... unless
    def beat_two_lines(self):
        heading, _ = rich([("O", O_COLOR), (" wins on move 6", W)], 44)
        heading.to_edge(UP, buff=0.45)
        left = Board(size=3.4).move_to(LEFT * 3.4 + DOWN * 0.25)
        right = Board(size=3.4).move_to(RIGHT * 3.4 + DOWN * 0.25)
        game = [(0, "X"), (3, "O"), (1, "X"), (4, "O"), (6, "X"), (5, "O")]
        assert check_legal([sq for sq, _ in game]) == "XX.OOOX.." and winner("XX.OOOX..") == "O"
        assert winner("XXXOO....") == "X"          # the second board: X's top row at move 5

        with self.voiceover(SAY[0]) as vo:
            self.play(Write(heading), LaggedStart(*[Create(ln) for ln in left], lag_ratio=0.2),
                      run_time=0.8)
            marks, nums = {}, {}
            for n, (i, sym) in enumerate(game, start=1):
                marks[i] = left.mark_at(i, sym, scale=0.46)
                nums[i] = move_number(left, i, n, sym)
                self.play(mark_anim(marks[i]), FadeIn(nums[i], scale=0.6), run_time=0.3)

            vo.wait_until("O needs three")
            oline = left.win_line(3, 5)
            tick = S.math(r"\checkmark", size=60, color=COUNT_COLOR).next_to(left, DOWN, buff=0.3)
            self.play(Create(oline), run_time=0.5)
            self.play(FadeIn(tick, scale=0.5),
                      Indicate(VGroup(marks[3], marks[4], marks[5]), color=O_COLOR, scale_factor=1.15),
                      run_time=0.7)

            # the same game, copied to the right ...
            vo.wait_until("But careful")
            r_grid = left.copy()
            r_marks = {i: m.copy() for i, m in marks.items()}
            r_nums = {i: t.copy() for i, t in nums.items()}
            r_oline = oline.copy()
            self.add(r_grid, *r_marks.values(), *r_nums.values(), r_oline)
            shift = right.get_center() - left.get_center()
            self.play(*[m.animate.shift(shift) for m in
                        [r_grid, *r_marks.values(), *r_nums.values(), r_oline]], run_time=0.8)

            # ... but X's 5th mark goes on square 2 instead of 6: X's top row is complete too
            vo.wait_until("if X's three")
            self.play(r_marks[6].animate(path_arc=PI / 2).move_to(right.center_of(2)),
                      r_nums[6].animate(path_arc=PI / 2).move_to(move_number(right, 2, 5, "X")),
                      run_time=0.9)
            xline = right.win_line(0, 2)
            self.play(Create(xline), run_time=0.5)

            vo.wait_until("X already won")
            # no "!" after the 5: right after S02, "5!" would read as five factorial
            words = S.text("already over at move 5", 30, UNDO_COLOR, weight=BOLD)
            box = SurroundingRectangle(words, color=UNDO_COLOR, buff=0.16, corner_radius=0.08,
                                       stroke_width=5).set_fill(S.BG, 0.88)
            stamp = VGroup(box, words).rotate(7 * DEGREES).move_to(right.center_of(7) + DOWN * 0.05)
            self.play(FadeIn(stamp, scale=1.6), run_time=0.4)
            self.play(Indicate(VGroup(r_marks[0], r_marks[1], r_marks[6]), color=X_COLOR,
                               scale_factor=1.15), run_time=0.7)

            # so O's 6th move never happens: it turns into a ghost and O's line goes away
            vo.wait_until("and the game stopped")
            ghost_o = right.ghost_at(5, "O", scale=0.46).set_fill(opacity=0)   # no fill: stays a ring
            self.play(Transform(r_marks[5], ghost_o),
                      r_nums[5].animate.set_color(GHOST_COLOR).set_opacity(0.5),
                      Uncreate(r_oline), run_time=0.9)

        # hand the pieces we keep to the next beat, as clean groups
        self.heading = heading
        self.left_parts = (left, VGroup(*[marks[i] for i in sorted(marks)]), oline)
        self.right_parts = (r_grid, VGroup(r_marks[0], r_marks[1], r_marks[6], r_marks[3], r_marks[4]),
                            xline, r_marks[5])
        self.to_fade = VGroup(*nums.values(), tick, *r_nums.values(), stamp)
        self.clear()
        self.add(heading, *self.left_parts, *self.right_parts, self.to_fade)

    # ============================================================== 2. 5,760 - 432 = 5,328
    def beat_subtract(self):
        heading = self.heading
        LBL_X, NUM_X = -3.8, 6.3                         # label column (left edge), number column (right edge)
        Y1, Y2, YR = 2.1, -0.2, -2.35                   # label rows: O lines up / X won / result

        mini1 = mini_board("XX.OOOX..", size=1.8, stroke=4, line=(3, 5)).move_to([-5.3, 1.8, 0])

        # "X already won": the "already over at move 5" board (X's top row; O's middle row, whose third
        # mark on square 5 stays a ghost) and its quarter turn (X's right column, O's middle column)
        ROW_GAME, COL_GAME = [0, 3, 1, 4, 2], [2, 1, 5, 4, 8]     # moves 1-5; O's ghost 6th: 5 / 7
        assert check_legal(ROW_GAME) == "XXXOO...." and winner("XXXOO....") == "X"
        assert check_legal(COL_GAME) == ".OX.OX..X" and winner(".OX.OX..X") == "X"
        assert winner("XXXOOO...") == "X"                         # O's ghost 6th would finish O's row
        ROWS_AT, COLS_AT = np.array([-5.95, -0.5, 0]), np.array([-4.72, -0.5, 0])   # in the row
        # the big boards sit between "X already won" and the count of the pairs under them
        BIG, ROWS_BIG, COLS_BIG = 2.3, np.array([-1.5, -1.8, 0]), np.array([1.5, -1.8, 0])
        COUNT_Y = -3.33

        # the small pictures in the subtraction row (same look as the O-wins picture above them)
        rows = mini_board("XXXOO....", size=1.08, stroke=4, line=(0, 2))
        rows.add(rows.board.ghost_at(5, "O", scale=0.6).set_stroke(width=3).set_fill(opacity=0))
        rows.move_to(ROWS_AT)
        rows_small = rows.copy()
        cols_small = rows.copy().rotate(-PI / 2).move_to(COLS_AT)

        # the same two boards at a readable size, in the style of the opening boards (with move numbers)
        def big_board(cells, game, ghost_sq, line, at):
            b = Board(size=BIG).move_to(at)
            marks = VGroup(*[b.mark_at(i, ch, scale=0.46) for i, ch in enumerate(cells) if ch in "XO"])
            g = VGroup(b, marks, b.win_line(*line), b.ghost_at(ghost_sq, "O", scale=0.46).set_fill(opacity=0))
            nums = VGroup(*[move_number(b, sq, n, "X" if n % 2 else "O") for n, sq in enumerate(game, start=1)],
                          move_number(b, ghost_sq, 6, "O").set_color(GHOST_COLOR).set_opacity(0.5))
            return g, nums

        rows_big, rows_nums = big_board("XXXOO....", ROW_GAME, 5, (0, 2), ROWS_BIG)
        cols_ref, cols_nums = big_board(".OX.OX..X", COL_GAME, 7, (2, 8), COLS_BIG)
        # a quarter turn (clockwise) about this pivot carries the row board onto the column board
        pivot = (ROWS_BIG + COLS_BIG) / 2 + DOWN * np.linalg.norm(COLS_BIG - ROWS_BIG) / 2
        turned = rows_big.copy().rotate(-PI / 2, about_point=pivot)

        def spots(ms):
            return sorted(tuple(np.round(m.get_center(), 4)) for m in ms)
        assert spots(turned[1][:3]) == spots([m for m in cols_ref[1] if isinstance(m, VGroup)])  # X
        assert spots([*turned[1][3:], turned[3]]) == spots([*[m for m in cols_ref[1] if isinstance(m, Circle)],
                                                             cols_ref[3]])                     # O

        label1, _ = rich([("ways ", W), ("O", O_COLOR), (" could line up", W)], 34)
        label1.move_to([0, Y1, 0]).align_to([LBL_X, 0, 0], LEFT)
        brk1, p1 = rich([("8 lines", WIN_COLOR), ("  ×  ", S.GREY), ("6 orders", O_COLOR),
                         ("  ×  ", S.GREY), ("(6 × 5 × 4 for X's 3 marks)", X_COLOR)], 26)
        brk1.next_to(label1, DOWN, buff=0.25, aligned_edge=LEFT)
        n1 = S.text(f"{8 * 6 * 6 * 5 * 4:,}", 52, W).move_to([0, Y1, 0]).align_to([NUM_X, 0, 0], RIGHT)

        label2, _ = rich([("X", X_COLOR), (" already won", W)], 34)
        label2.move_to([0, Y2, 0]).align_to([LBL_X, 0, 0], LEFT)
        # "12 pairs of parallel lines" alone reads as 6 (3 row pairs + 3 column pairs): spell out that a
        # pair is (O's line, X's parallel line), i.e. 6 choices for O's row/column x 2 parallel X lines
        if i18n.active():
            # a language version names the two 6s instead ("12 对 × 6（O 的顺序）× 6（X 的顺序）"): the
            # pair is already spelled out by the count under the boards that this row replaces, and
            # the English wording would not fit next to the two glosses. Same 5 pieces as in English.
            brk2, p2 = rich([("12 pairs", WIN_COLOR), ("  ×  ", S.GREY), ("6", O_COLOR),
                             (" (O's order)", O_COLOR), ("  ×  ", S.GREY), ("6", X_COLOR),
                             (" (X's order)", X_COLOR)], 26)
            p2 = [p2[0], p2[1], VGroup(*p2[2:4]), p2[4], VGroup(*p2[5:7])]
        else:
            brk2, p2 = rich([("12 pairs (", WIN_COLOR), ("O", O_COLOR), ("'s line, ", WIN_COLOR), ("X", X_COLOR),
                             ("'s parallel line)", WIN_COLOR), ("  ×  ", S.GREY), ("6", O_COLOR),
                             ("  ×  ", S.GREY), ("6", X_COLOR)], 26)
            p2 = [VGroup(*p2[:5]), *p2[5:]]
        assert 6 * 2 == 12 and 12 * 6 * 6 == 432
        brk2.next_to(label2, DOWN, buff=0.25, aligned_edge=LEFT)
        # where the 12 pairs come from, under the two boards: O's line (O's colour) x X's parallel line
        # (X's colour), for rows and for columns
        count, cp = rich([("3 rows", O_COLOR), (" × ", S.GREY), ("2 other rows", X_COLOR), ("  +  ", S.GREY),
                          ("3 columns", O_COLOR), (" × ", S.GREY), ("2 other columns", X_COLOR),
                          (" = ", S.GREY), ("12 pairs", WIN_COLOR)], 28)
        count.move_to([0, COUNT_Y, 0])
        assert 3 * 2 + 3 * 2 == 12
        n2 = S.math(rf"-\,{12 * 6 * 6}", size=56, color=UNDO_COLOR).move_to([0, Y2, 0]).align_to([NUM_X, 0, 0], RIGHT)

        assert 8 * 6 * 6 * 5 * 4 - 12 * 6 * 6 == BY_MOVE[6] == 5_328
        bar = Line([3.6, -1.25, 0], [NUM_X + 0.05, -1.25, 0], color=W, stroke_width=3)
        result = S.text(f"{BY_MOVE[6]:,}", 66, COUNT_COLOR).move_to([0, YR, 0]).align_to([NUM_X, 0, 0], RIGHT)
        heading_target = heading.copy().scale(38 / 44).move_to([0, YR, 0]).align_to([LBL_X, 0, 0], LEFT)

        L_grid, L_marks, L_line = self.left_parts
        R_grid, R_marks, R_line, R_ghost = self.right_parts

        with self.voiceover(SAY[1]) as vo:
            # the O-wins board shrinks into the pictures column; the "already over" board leaves for now
            # (a copy comes back at "Then we subtract", when it is needed)
            self.play(FadeOut(self.to_fade), run_time=0.35)
            r_board = self.adopt(VGroup(R_grid, R_marks, R_line, R_ghost))
            self.play(ReplacementTransform(L_grid, mini1[0]), ReplacementTransform(L_marks, mini1[1]),
                      ReplacementTransform(L_line, mini1[2]), FadeOut(r_board, scale=0.85),
                      run_time=0.9)
            self.adopt(mini1)
            self.play(FadeIn(label1, shift=RIGHT * 0.2), run_time=0.5)

            # the same three steps, each factor with its picture as it is named:
            # "8 lines for O": the 8 lines are drawn one by one (as in S03), then cleared
            vo.wait_until("8 lines for O")
            lines8 = VGroup(*[mini1.board.win_line(a, c, stroke=5) for a, _, c in WIN_LINES])
            self.play(FadeIn(p1[0], shift=UP * 0.15), mini1[1].animate.set_stroke(opacity=0.35),
                      LaggedStart(*[Create(ln) for ln in lines8], lag_ratio=0.45), run_time=1.0)
            o_marks = VGroup(*mini1[1][2:5])
            x_marks = VGroup(mini1[1][0], mini1[1][1], mini1[1][5])     # squares 0, 1, 6: moves 1, 3, 5
            self.play(FadeOut(lines8), mini1[1].animate.set_stroke(opacity=1), run_time=0.25)
            # "6 orders for O's marks"
            vo.wait_until("6 orders")
            self.play(FadeIn(VGroup(p1[1], p1[2]), shift=UP * 0.15),
                      Indicate(o_marks, color=O_COLOR, scale_factor=1.3), run_time=0.8)
            # "6 times 5 times 4 ways to place X's three marks": X's marks pulse one per factor
            vo.wait_until("6 times 5 times 4")
            self.play(FadeIn(VGroup(p1[3], p1[4]), shift=UP * 0.15),
                      LaggedStart(*[Indicate(m, color=X_COLOR, scale_factor=1.3) for m in x_marks],
                                  lag_ratio=0.5), run_time=1.4)
            self.remove(*p1)
            self.add(brk1)
            vo.wait_until("That's 5,760")
            self.play(Write(n1), run_time=0.6)
            # "... ways for O to finish a line": O's line on the picture pulses
            vo.wait_until("to finish a line")
            self.play(Indicate(mini1[2], color=WIN_COLOR, scale_factor=1.2), run_time=0.8)

            # subtract the games where X's row (or column) was finished first: the "already over" board
            # comes back, small, next to its label, and "-432" is written as the number is spoken ...
            vo.wait_until("Then we subtract")
            self.play(FadeIn(label2, shift=RIGHT * 0.2), FadeIn(VGroup(rows[0], rows[1], rows[3])),
                      run_time=0.6)
            self.play(Write(n2), run_time=0.6)
            # "... where X's three marks made a line too": X's marks pulse, then X's line is drawn
            vo.wait_until("where X's three marks")
            self.play(Indicate(rows[1][:3], color=X_COLOR, scale_factor=1.3), run_time=0.8)
            self.play(Create(rows[2]), run_time=0.5)
            self.adopt(rows)

            # "a row or column parallel to O's": it grows to a readable size (with its move numbers) and
            # a quarter turn of it gives the column version beside it
            # (it grows going down first, then right, so it passes under "X already won")
            vo.wait_until("a row or column parallel")
            self.play(SwoopMove(rows, rows_big, ctrl=[ROWS_AT[0], ROWS_BIG[1], 0]), run_time=0.7)
            cols = rows.copy()
            self.add(cols)
            # ... and under them, the count of the pairs (O's line, X's parallel line): the rows part
            # while the column board turns, the columns part with its move numbers
            self.play(Rotate(cols, -PI / 2, about_point=pivot), FadeIn(rows_nums),
                      LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in cp[:3]], lag_ratio=0.2,
                                  rate_func=squish_rate_func(linear, 0.35, 1)), run_time=0.8)
            self.play(FadeIn(cols_nums),
                      LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in cp[3:]], lag_ratio=0.15), run_time=0.7)

            # "so X sneaked in a win first": X's marks (moves 1, 3, 5) and X's lines pulse
            vo.wait_until("so X sneaked")
            self.play(*[Indicate(VGroup(*bd[1][:3], *nm[0:5:2]), color=X_COLOR, scale_factor=1.2)
                        for bd, nm in ((rows, rows_nums), (cols, cols_nums))],
                      *[Indicate(bd[2], color=WIN_COLOR, scale_factor=1.1) for bd in (rows, cols)],
                      run_time=0.9)
            # ... then both shrink into the subtraction row (swooping between the breakdown row and the
            # count), the count fades once the boards have passed it, and the breakdown is written in the
            # row the boards have just left (all before "That leaves")
            self.play(SwoopMove(rows, rows_small, dip=0.95), SwoopMove(cols, cols_small, dip=0.95),
                      *[FadeOut(nm, rate_func=squish_rate_func(smooth, 0, 0.3)) for nm in (rows_nums, cols_nums)],
                      *[FadeOut(p, rate_func=squish_rate_func(smooth, 0.4, 0.85)) for p in cp],
                      FadeIn(p2[0], shift=UP * 0.15, rate_func=squish_rate_func(smooth, 0.35, 0.75)),
                      LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in p2[1:]], lag_ratio=0.35,
                                  rate_func=squish_rate_func(linear, 0.45, 1)),
                      run_time=min(1.2, max(0.9, vo.until("That leaves") - 0.1)))
            self.remove(*p2)
            self.add(brk2)

            vo.wait_until("That leaves")
            # the heading comes down to label the answer, fading low while it crosses rows 1 and 2
            self.play(Create(bar), DimmedMove(heading, heading_target), run_time=0.9)
            self.play(Write(result), run_time=0.7)
            self.play(Circumscribe(result, color=COUNT_COLOR, buff=0.12), run_time=vo.remaining(1.0))

        self.result = result
        self.subtract_rest = VGroup(heading, mini1, rows, cols, label1, brk1, n1, label2, brk2, n2, bar)

    # ============================================================== 3. moves 7, 8, 9: a tangled mess
    def beat_tangle(self):
        TY = [1.95, 1.0, 0.05, -0.9, -1.85]               # table rows: moves 5..9
        MOVE_X, NUM_R, TICK_X, Q_X = -6.2, -2.95, -2.45, -3.55
        header = VGroup(S.text("game ends on", 24, S.GREY).move_to([0, 2.8, 0]).align_to([MOVE_X, 0, 0], LEFT),
                        S.text("games", 24, S.GREY).move_to([0, 2.8, 0]).align_to([NUM_R, 0, 0], RIGHT))
        movelabels = VGroup(*[S.text(f"move {k}", 30, W).move_to([0, y, 0]).align_to([MOVE_X, 0, 0], LEFT)
                              for k, y in zip(range(5, 10), TY)])
        seps = VGroup(*[Line([-6.3, y, 0], [-2.1, y, 0], color=S.GREY_DARK, stroke_width=2)
                        for y in [2.45] + [(TY[i] + TY[i + 1]) / 2 for i in range(4)]])
        num5 = S.text(f"{BY_MOVE[5]:,}", 34, COUNT_COLOR).move_to([0, TY[0], 0]).align_to([NUM_R, 0, 0], RIGHT)
        num6 = S.text(f"{BY_MOVE[6]:,}", 34, COUNT_COLOR).move_to([0, TY[1], 0]).align_to([NUM_R, 0, 0], RIGHT)
        ticks = VGroup(*[S.math(r"\checkmark", size=40, color=COUNT_COLOR).move_to([TICK_X, y, 0])
                         for y in TY[:2]])
        qs = VGroup(*[S.text("?", 44, W).move_to([Q_X, y, 0]) for y in TY[2:]])

        # the tangle: small legal boards, grey questions, crossing arrows (drawn under the boards)
        def tile(cells, moves, line, pos, draw=False):
            assert check_legal(moves) == cells
            g = mini_board(cells, size=1.35, stroke=3, line=line)
            if draw:
                assert winner(cells) is None and "." not in cells
                g[1].set_color(DRAW_COLOR)
            else:
                assert winner(cells) is not None
            back = Square(1.5, stroke_width=0).set_fill(S.BG, 1)
            t = VGroup(back, g).move_to(pos)
            t.set_z_index(2)
            return t

        b1 = tile("XOXOXOX..", [0, 1, 2, 3, 4, 5, 6], (2, 6), [0.3, 1.35, 0])          # X wins, move 7
        b2 = tile("XXOOOOX.X", [0, 4, 8, 2, 6, 3, 1, 5], (3, 5), [4.85, 0.95, 0])     # O wins, move 8
        b3 = tile("XOXXOOOXX", [0, 1, 2, 4, 3, 5, 7, 6, 8], None, [1.75, -1.75, 0], draw=True)
        b4 = tile("XOXOXOOXX", [0, 1, 2, 3, 4, 5, 7, 6, 8], (0, 8), [4.4, -1.75, 0])  # X wins, move 9

        def tag(s, pos):
            t = S.text(s, 26, S.GREY)
            g = VGroup(BackgroundRectangle(t, color=S.BG, fill_opacity=1, buff=0.08), t).move_to(pos)
            g.set_z_index(3)
            return g

        l1 = tag("did O win before?", [0.3, 2.55, 0])
        l2 = tag("did X win before?", [4.85, 2.15, 0])
        l3 = tag("win or draw?", [3.07, -3.1, 0])

        def edge(b, d, slide=0.0):
            """A point just outside tile b in direction d (slid sideways along the edge by `slide`)."""
            d = np.array(d, dtype=float)
            side = np.array([-d[1], d[0], 0.0])
            return (b.get_center() + 0.8 * d + slide * side)[:2]

        def arrow(p, q, angle):
            a = CurvedArrow(np.array([*p, 0.0]), np.array([*q, 0.0]), angle=angle, color=S.GREY,
                            stroke_width=3.5, tip_length=0.2)
            a.set_stroke(opacity=0.85).set_z_index(1)
            return a

        q7, q8, q9 = [(-3.15, y) for y in TY[2:]]
        L_, R_, U_, D_ = LEFT, RIGHT, UP, DOWN
        wave1 = [arrow(q7, edge(b1, L_, 0.2), -0.7), arrow(q7, edge(b2, L_, 0.3), 0.45),
                 arrow(q8, edge(b1, D_), 0.9)]
        wave2 = [arrow(edge(b1, R_), edge(b2, L_, -0.3), -0.6),
                 arrow(edge(b2, D_, 0.4), edge(b1, D_, -0.35), -0.8),
                 arrow(q9, edge(b2, D_), -0.9), arrow(q8, edge(b2, L_), 0.25)]
        wave3 = [arrow(q9, edge(b3, L_), 0.5), arrow(edge(b1, D_, 0.35), edge(b3, U_, 0.3), 0.8),
                 arrow(edge(b2, D_, -0.2), edge(b4, U_, -0.25), -1.1),
                 arrow(edge(b3, U_, -0.3), edge(b4, U_, 0.3), -0.9), arrow(q8, edge(b4, L_, -0.2), -0.45)]
        wave4 = [arrow(q7, edge(b3, U_), -1.2), arrow(edge(b4, L_, 0.3), edge(b3, R_, -0.3), -2.0),
                 arrow(edge(b4, U_, -0.45), edge(b1, R_, -0.3), 0.6), arrow(q9, edge(b1, D_, 0.4), 1.1),
                 arrow(edge(b1, R_, 0.3), edge(b2, U_, 0.3), 1.3)]

        with self.voiceover(SAY[2]) as vo:
            self.adopt(self.subtract_rest)
            self.play(FadeOut(self.subtract_rest), run_time=0.5)
            self.play(self.result.animate.become(num6),
                      FadeIn(VGroup(header, seps, movelabels[:2], num5)), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in ticks], lag_ratio=0.4), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(VGroup(m, q), shift=LEFT * 0.2)
                                    for m, q in zip(movelabels[2:], qs)], lag_ratio=0.35), run_time=0.9)

            vo.wait_until("it gets much worse")
            self.play(LaggedStart(*[Create(a) for a in wave1], lag_ratio=0.25),
                      FadeIn(b1, scale=0.8), FadeIn(b2, scale=0.8), run_time=1.2)
            vo.wait_until("we'd have to check")
            self.play(FadeIn(l1, shift=DOWN * 0.15), FadeIn(l2, shift=DOWN * 0.15),
                      LaggedStart(*[Create(a) for a in wave2], lag_ratio=0.25), run_time=1.4)
            self.play(Indicate(qs, color=W, scale_factor=1.2), run_time=0.8)
            vo.wait_until("and a full board")
            self.play(FadeIn(b3, scale=0.8), FadeIn(b4, scale=0.8), FadeIn(l3, shift=UP * 0.15),
                      LaggedStart(*[Create(a) for a in wave3], lag_ratio=0.25), run_time=1.4)
            vo.wait_until("It turns into")
            arrows = VGroup(*wave1, *wave2, *wave3, *wave4)
            self.play(LaggedStart(*[Create(a) for a in wave4], lag_ratio=0.2), run_time=0.9)
            self.play(LaggedStart(*[Wiggle(b, scale_value=1.1, rotation_angle=0.025 * TAU)
                                    for b in (b1, b2, b3, b4)], lag_ratio=0.15),
                      Wiggle(qs, scale_value=1.15), run_time=vo.remaining(0.6))

        self.table = VGroup(header, seps, movelabels, num5, self.result, ticks, qs)
        self.tangle = VGroup(arrows, b1, b2, b3, b4, l1, l2, l3)

    # ============================================================== 4. Plan B: a computer
    def beat_plan_b(self):
        center = np.array([2.4, 0.55, 0])
        lap = laptop(center)
        screen_board = Board(size=1.75, stroke=4).move_to(center + LEFT * 0.95)
        games_word = S.text("games", 24, S.GREY).move_to(center + RIGHT * 1.15 + UP * 0.45)
        counter = S.text("0", 48, COUNT_COLOR).move_to(center + RIGHT * 1.15 + DOWN * 0.2)
        caption = S.text("Plan B: let a computer play every game", 32, W).move_to([center[0], -2.35, 0])

        games = first_games(10)
        for cells, seq, _ in games:
            assert check_legal(seq) == cells

        def final_board(cells, line):
            m = screen_board.place_all(cells, scale=0.6).set_stroke(width=5)
            if line is None:
                m.set_color(DRAW_COLOR)
                return m
            return VGroup(m, screen_board.win_line(line[0], line[2], stroke=6))

        with self.voiceover(SAY[3]) as vo:
            self.adopt(self.tangle)
            self.play(FadeOut(self.tangle, scale=0.85), run_time=0.9)
            vo.wait_until("there's another plan")
            self.play(LaggedStart(Create(lap[0]), FadeIn(lap[1]), DrawBorderThenFill(lap[2]),
                                  FadeIn(lap[3]), FadeIn(lap[4]), lag_ratio=0.25),
                      FadeIn(caption, shift=UP * 0.2, rate_func=squish_rate_func(smooth, 0.4, 1)),
                      run_time=1.2)

            vo.wait_until("Don't count")
            self.play(self.table.animate.fade(0.65), run_time=0.7)

            # teach it the rules: a board and its 8 winning lines
            vo.wait_until("Instead, teach")
            self.play(LaggedStart(*[Create(ln) for ln in screen_board], lag_ratio=0.2),
                      FadeIn(games_word), FadeIn(counter), run_time=0.5)
            rules = VGroup(*[screen_board.win_line(a, c, stroke=5) for a, _, c in WIN_LINES])
            self.play(LaggedStart(*[Create(ln) for ln in rules], lag_ratio=0.4), run_time=1.1)
            self.play(FadeOut(rules), run_time=0.35)

            # ... and let it play every game, one by one (the program's own first games)
            vo.wait_until("and let it play")
            cells, seq, line = games[0]
            shown = VGroup()
            for n, sq in enumerate(seq):
                m = screen_board.mark_at(sq, "X" if n % 2 == 0 else "O", scale=0.6).set_stroke(width=5)
                shown.add(m)
                self.play(mark_anim(m), run_time=0.1)
            win = screen_board.win_line(line[0], line[2], stroke=6)
            self.play(Create(win), Transform(counter, S.text("1", 48, COUNT_COLOR).move_to(counter)),
                      run_time=0.2)
            cur = self.regroup(*shown, win)
            per = max(0.16, (vo.remaining() - 0.15) / (len(games) - 1))
            for k, (cells, seq, line) in enumerate(games[1:], start=2):
                nxt = final_board(cells, line)
                self.play(FadeOut(cur), FadeIn(nxt),
                          Transform(counter, S.text(str(k), 48, COUNT_COLOR).move_to(counter)),
                          run_time=per)
                cur = nxt
