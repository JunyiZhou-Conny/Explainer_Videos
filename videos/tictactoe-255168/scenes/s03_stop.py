"""S03 · Games stop early.

Beats: a real game stops when X wins on move 5, so the 4 empty squares are never played (GREY
dashed ghost moves 6-9) -> the ghost moves shuffle through all 24 orders while a GREEN counter
ticks 1..24: this 1 game was counted 24 times in 362,880 ("ghost games") -> a timeline of moves
1-9: X's 3rd mark is move 5 -> ponder: how many games does X win on move 5? -> three steps on the
board: 8 lines, 6 orders of X's marks, 6 x 5 places for O's marks -> 8 x 6 x 30 = 1,440.
"""

import itertools

import numpy as np
from manim import *
from math import factorial  # after the star import, so nothing shadows it

from explainer import style as S
from explainer.components import highlight_box, ponder_card
from explainer.scene import VoiceScene

from common import (BY_MOVE, COUNT_COLOR, GHOST_COLOR, NARRATION, NINE_FACTORIAL, O_COLOR,
                    WIN_COLOR, WIN_LINES, X_COLOR, Board, mark, mark_anim, move_number, winner)

SAY = NARRATION["S03"]

BOARD_SIZE = 4.0
MARK_SCALE = 0.48                       # marks leave room for the move number in the corner
BOARD_HOME = np.array([0.0, -0.25, 0])  # first beat: the game alone, centred
BOARD_LEFT = np.array([-4.35, -0.25, 0])
PANEL_X = 2.2                           # centre of the right-hand column

GAME = [(0, "X"), (4, "O"), (1, "X"), (8, "O"), (2, "X")]   # X wins on the top row, move 5
GHOST_SQUARES = (3, 5, 6, 7)                                # never played
GHOST_SYMBOLS = ("O", "X", "O", "X")                        # ghost moves 6, 7, 8, 9


# ------------------------------------------------------------------ the numbers on screen, checked
def _games_won_by_x_on_move_5() -> int:
    n = 0
    for seq in itertools.permutations(range(9), 5):
        b = ["."] * 9
        for k, sq in enumerate(seq):
            if winner(b) is not None:
                break
            b[sq] = "X" if k % 2 == 0 else "O"
        else:
            # no one won before move 5 (X has only 2 marks before it), X wins on move 5
            n += winner(b) == "X"
    return n


def _check_numbers():
    b = ["."] * 9
    for i, sym in GAME:
        assert b[i] == "." and winner(b) is None
        b[i] = sym
    assert winner(b) == "X"
    assert tuple(i for i in range(9) if b[i] == ".") == GHOST_SQUARES
    assert factorial(4) == 24 and NINE_FACTORIAL == factorial(9) == 362_880
    assert len(WIN_LINES) == 8 and 8 * factorial(3) * (6 * 5) == BY_MOVE[5] == 1_440
    assert _games_won_by_x_on_move_5() == 1_440


_check_numbers()


# ------------------------------------------------------------------ helpers
def corner(board: Board, i: int) -> np.ndarray:
    """Where a move number sits in square i (lower-right corner, as move_number() puts it)."""
    return board.center_of(i) + np.array([0.36, -0.36, 0]) * board.cell


def ghost_move(board: Board, i: int, symbol: str, n: int) -> VGroup:
    """A ghost move: faded dashed GREY mark + faded GREY move number."""
    g = board.ghost_at(i, symbol, scale=MARK_SCALE)
    num = S.text(str(n), 24, GHOST_COLOR, font=S.FONT_SANS).move_to(corner(board, i)).set_opacity(0.8)
    return VGroup(g, num)


def play_moves(scene, board: Board, moves, start: int = 1, run_time: float = 0.45):
    """Animate moves [(square, 'X'|'O'), ...] with move numbers; returns (marks, numbers)."""
    marks, nums = VGroup(), VGroup()
    for n, (i, sym) in enumerate(moves, start=start):
        m = board.mark_at(i, sym, scale=MARK_SCALE)
        num = move_number(board, i, n, sym)
        scene.play(mark_anim(m), FadeIn(num, scale=0.6), run_time=run_time)
        marks.add(m)
        nums.add(num)
    return marks, nums


def plain_changes(n: int) -> list[tuple[int, ...]]:
    """All n! orders of range(n), each one swap away from the last (Steinhaus-Johnson-Trotter)."""
    perm, dirs = list(range(n)), [-1] * n
    out = [tuple(perm)]
    while True:
        mobile, at = -1, -1
        for idx, v in enumerate(perm):
            j = idx + dirs[v]
            if 0 <= j < n and perm[j] < v and v > mobile:
                mobile, at = v, idx
        if mobile < 0:
            break
        j = at + dirs[mobile]
        perm[at], perm[j] = perm[j], perm[at]
        for v in range(mobile + 1, n):
            dirs[v] *= -1
        out.append(tuple(perm))
    assert len(set(out)) == factorial(n)
    return out


def count_tex(k: int, at, size: float = 44) -> MathTex:
    return S.math(str(k), size=size, color=COUNT_COLOR).move_to(at)


def colour_parts(tex: MathTex, green: tuple[int, ...]) -> MathTex:
    for k, part in enumerate(tex):
        part.set_color(COUNT_COLOR if k in green else S.WHITE)
    return tex


def timeline_strip(y: float) -> VGroup:
    """Moves 1-9 as a row of slots: VGroup of slots, each VGroup(box, mark, number)."""
    slots = VGroup()
    for k in range(1, 10):
        sym = "X" if k % 2 else "O"
        color = X_COLOR if sym == "X" else O_COLOR
        box = RoundedRectangle(width=0.62, height=0.62, corner_radius=0.1,
                               stroke_color=S.GREY_DARK, stroke_width=2).set_fill(S.GREY_DARKER, 1)
        m = mark(sym, 0.32, stroke=5)
        num = S.text(str(k), 26, color, font=S.FONT_SANS).next_to(box, DOWN, buff=0.14)
        slots.add(VGroup(box, m.move_to(box), num))
    slots.arrange(RIGHT, buff=0.1, aligned_edge=UP)
    return slots.move_to([PANEL_X, y, 0], aligned_edge=UP)


class GamesStop(VoiceScene):
    def construct(self):
        # ============================================================== 1. a real game stops
        board = Board(size=BOARD_SIZE).move_to(BOARD_HOME)
        caption = S.text("X wins on move 5", 32, S.WHITE, t2c={"X": X_COLOR})
        never = S.text("never played", 28, GHOST_COLOR)

        with self.voiceover(SAY[0]) as vo:
            self.play(LaggedStart(*[Create(ln) for ln in board], lag_ratio=0.2), run_time=0.9)
            vo.wait_until("Real tic-tac-toe")
            marks, nums = play_moves(self, board, GAME, run_time=0.45)
            vo.wait_until("three in a row")
            win = board.win_line(0, 2)
            self.play(Create(win), run_time=0.5)
            vo.wait_until("In this game")
            caption.next_to(board, UP, buff=0.3)
            self.play(FadeIn(caption, shift=DOWN * 0.15), Indicate(nums[4], scale_factor=1.6),
                      run_time=0.8)
            vo.wait_until("so the last four")
            ghosts = VGroup(*[ghost_move(board, sq, sym, n) for n, (sq, sym)
                              in enumerate(zip(GHOST_SQUARES, GHOST_SYMBOLS), start=6)])
            never.next_to(board, DOWN, buff=0.3)
            self.play(LaggedStart(*[Create(g[0]) for g in ghosts], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(g[1]) for g in ghosts], lag_ratio=0.3),
                      FadeIn(never, shift=UP * 0.15), run_time=1.4)

        # ============================================================== 2. ghost games: 24 orders
        top = S.math(r"362{,}880", size=64, color=COUNT_COLOR).move_to([PANEL_X, 2.55, 0])
        top_cap = S.text("orders to fill all 9 squares", 26, S.GREY).next_to(top, DOWN, buff=0.18)
        ways_cap = S.text("orders to fill the 4 empty squares", 26, S.GREY).move_to([PANEL_X, 0.85, 0])
        formula = colour_parts(S.math("4", r"\times", "3", r"\times", "2", r"\times", "1", "=", "24",
                                      size=56), green=(8,))
        formula.next_to(ways_cap, DOWN, buff=0.3)
        tag1 = S.text("this 1 game was counted", 32, S.WHITE)
        tag2 = S.text("24 times in 362,880", 32, S.WHITE, t2c={"24": COUNT_COLOR, "362,880": COUNT_COLOR})
        tag = VGroup(tag1, tag2).arrange(DOWN, buff=0.18).move_to([PANEL_X, -1.75, 0])
        ghost_label = S.text("ghost games", 32, GHOST_COLOR)

        with self.voiceover(SAY[1]) as vo:
            self.play(VGroup(board, marks, nums, win, ghosts, caption, never).animate.shift(
                BOARD_LEFT - board.get_center()), run_time=1.0)
            self.play(Write(top), FadeIn(top_cap, shift=UP * 0.1), run_time=1.0)
            # "as if the players kept going": the ghost moves get played, 6, 7, 8, 9
            vo.wait_until("as if the players")
            self.play(LaggedStart(*[Indicate(g, color=S.WHITE, scale_factor=1.25) for g in ghosts],
                                  lag_ratio=0.55), run_time=2.2)

            # the 4 ghost moves shuffle through all 24 orders while a GREEN counter ticks
            vo.wait_until("The 4 empty")
            counter = count_tex(1, formula[8].get_center(), size=56)
            self.play(FadeIn(ways_cap, shift=DOWN * 0.1), FadeIn(counter, scale=0.6), run_time=0.6)
            perms = plain_changes(4)
            home = [board.center_of(sq) for sq in GHOST_SQUARES]
            offset = [g.get_center() - home[k] for k, g in enumerate(ghosts)]
            events = [(vo.time_until("4 times 3"), [formula[0]]),
                      (vo.time_until("3 times 2"), [formula[1], formula[2]]),
                      (vo.time_until("2 times 1"), [formula[3], formula[4]]),
                      (vo.time_until("times 1,") + 0.25, [formula[5], formula[6]])]
            budget = vo.time_until("so 24 ways") - 0.1
            base = [max(0.14, 0.5 * 0.9 ** k) for k in range(len(perms) - 1)]
            durations = [d * budget / sum(base) for d in base]
            t0 = 0.0
            for k in range(1, len(perms)):
                prev, cur = perms[k - 1], perms[k]
                anims = [ghosts[mv].animate(path_arc=0.5 * PI).move_to(home[pos] + offset[mv])
                         for pos, mv in enumerate(cur) if prev[pos] != mv]
                dt = durations[k - 1]
                while events and events[0][0] <= t0 + dt / 2:
                    anims += [FadeIn(p, shift=DOWN * 0.1) for p in events.pop(0)[1]]
                self.play(*anims, run_time=dt)
                counter.become(count_tex(k + 1, formula[8].get_center(), size=56))   # ticks on landing
                t0 += dt
            for _, parts in events:   # any part the shuffle finished before
                self.play(*[FadeIn(p) for p in parts], run_time=0.2)
            vo.wait_until("so 24 ways")
            self.play(FadeIn(formula[7]), ReplacementTransform(counter, formula[8]), run_time=0.4)
            self.play(Indicate(formula[8], color=COUNT_COLOR, scale_factor=1.3), run_time=0.6)

            # this one real game was counted 24 times
            vo.wait_until("So this one game")
            arrow = Arrow(tag1.get_left() + LEFT * 0.1, board.get_right() + RIGHT * 0.15 + DOWN * 0.45,
                          buff=0.05, color=S.GREY, stroke_width=4, max_tip_length_to_length_ratio=0.15)
            self.play(FadeIn(tag1, shift=UP * 0.1), GrowArrow(arrow),
                      TransformFromCopy(formula[8], tag2[0:2]),
                      Indicate(top, color=COUNT_COLOR, scale_factor=1.12),     # "...in 362,880" (the one up top)
                      FadeIn(tag2[2:]), run_time=1.2)

            # those made-up endings are ghost games
            vo.wait_until("Let's call")
            ghost_label.move_to(never)
            self.play(ReplacementTransform(never, ghost_label),
                      LaggedStart(*[Wiggle(g, scale_value=1.15) for g in ghosts], lag_ratio=0.15),
                      run_time=1.4)

            # count each real game only once
            vo.wait_until("We want")
            goal = VGroup(S.text("count each real game", 34, S.WHITE),
                          S.text("only once", 44, COUNT_COLOR)).arrange(DOWN, buff=0.25) \
                .move_to([PANEL_X, 0.2, 0])
            self.play(FadeOut(ghosts, scale=0.6), FadeOut(ghost_label),
                      FadeOut(VGroup(top, top_cap, ways_cap, formula, tag, arrow), shift=UP * 0.3),
                      FadeIn(goal, shift=UP * 0.3), run_time=0.9)
            self.play(LaggedStart(*[Indicate(n, scale_factor=1.5) for n in nums], lag_ratio=0.25),
                      run_time=1.2)

        # ============================================================== 3. when can a game end?
        slots = timeline_strip(y=0.35)
        hl5 = highlight_box(slots[4], color=WIN_COLOR, buff=0.08)
        third = S.text("X's 3rd mark: move 5", 30, S.WHITE, t2c={"X's 3rd mark": X_COLOR})
        third.next_to(hl5, UP, buff=0.75)
        third_arrow = Arrow(third.get_bottom(), hl5.get_top(), buff=0.08, color=WIN_COLOR,
                            stroke_width=4, max_tip_length_to_length_ratio=0.3)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(goal, shift=UP * 0.3), FadeOut(caption), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in slots], lag_ratio=0.12),
                      run_time=1.1)
            vo.wait_until("Not before")
            for s in slots[:4]:
                s.save_state()
            self.play(*[s.animate.fade(0.7) for s in slots[:4]], Create(hl5), run_time=0.7)
            vo.wait_until("X plays moves")
            self.play(*[Restore(s) for s in slots[:4]], run_time=0.3)
            x_slots = [slots[0], slots[2], slots[4]]
            x_nums = [nums[0], nums[2], nums[4]]          # X's move numbers 1, 3, 5 on the board
            self.play(LaggedStart(*[AnimationGroup(
                s[0].animate.set_fill(X_COLOR, 0.3).set_stroke(X_COLOR, 3),
                Indicate(s[1], color=X_COLOR, scale_factor=1.3),
                Indicate(n, color=X_COLOR, scale_factor=1.7)) for s, n in zip(x_slots, x_nums)],
                lag_ratio=0.6), run_time=2.0)
            vo.wait_until("so the fifth move")
            self.play(FadeIn(third, shift=DOWN * 0.15), GrowArrow(third_arrow),
                      Indicate(marks[4], color=WIN_COLOR, scale_factor=1.2), run_time=0.9)

        # ============================================================== 4. ponder
        strip = VGroup(slots, hl5, third, third_arrow)
        with self.voiceover(SAY[3]) as vo:
            self.play(strip.animate.shift(DOWN * (slots.get_top()[1] + 2.15)), run_time=1.0)
            self.play(Indicate(win, color=WIN_COLOR, scale_factor=1.1), run_time=0.8)
            vo.wait_until("Try to count")
            self.play(Indicate(VGroup(marks[0], marks[2], marks[4]), color=X_COLOR, scale_factor=1.15),
                      run_time=0.8)
        card = ponder_card("How many games end with X winning on move 5?\nHint: (1) Which line?\n"
                           "(2) In what order does X fill it?\n(3) Where can O's 2 marks go?",
                           width=8.4, size=26).move_to([PANEL_X, 1.6, 0])
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=20)

        # ============================================================== 5. three steps -> 1,440
        heads = VGroup(S.text("(1) Which line?", 28), S.text("(2) In what order does X fill it?", 28),
                       S.text("(3) Where can O's 2 marks go?", 28))
        r1 = colour_parts(S.math("8", r"\text{ lines}", size=44), green=(0,))
        r2 = colour_parts(S.math("3", r"\times", "2", r"\times", "1", "=", "6", size=44), green=(6,))
        r3 = colour_parts(S.math("6", r"\times", "5", "=", "30", size=44), green=(0, 2, 4))
        rows = VGroup(*[VGroup(h, r) for h, r in zip(heads, (r1, r2, r3))])
        for h, r in rows:
            r.next_to(h, DOWN, buff=0.22, aligned_edge=LEFT).shift(RIGHT * 0.45)
        rows.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([PANEL_X - 0.35, 1.05, 0])
        heads.set_color(S.GREY)
        sep = Line(LEFT * 3.3, RIGHT * 3.3, color=S.GREY_DARK, stroke_width=2) \
            .move_to([PANEL_X, rows.get_bottom()[1] - 0.4, 0])
        final = colour_parts(S.math("8", r"\times", "6", r"\times", "30", "=", r"1{,}440",
                                    r"\text{ games}", size=54), green=(0, 2, 4, 6))
        final.next_to(sep, DOWN, buff=0.45).set_x(PANEL_X)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card), FadeOut(strip), FadeOut(VGroup(marks, nums, win)), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(h, shift=RIGHT * 0.2) for h in heads], lag_ratio=0.3),
                      run_time=1.0)

            # (1) pick X's line: 8 of them
            vo.wait_until("First, pick")
            lines = [board.win_line(a, c) for a, _, c in WIN_LINES]
            self.play(heads[0].animate.set_color(S.WHITE), Create(lines[0]), run_time=0.7)
            vo.wait_until("There are 8")
            c1 = count_tex(1, r1[0].get_center())
            self.play(lines[0].animate.set_stroke(opacity=0.3), FadeIn(c1, scale=0.6), run_time=0.4)
            k = 1
            for anchor, group in (("3 rows", (1, 2)), ("3 columns", (3, 4, 5)), ("2 diagonals", (6, 7))):
                vo.wait_until(anchor)
                for j in group:
                    k += 1
                    c1.become(count_tex(k, r1[0].get_center()))
                    self.play(Create(lines[j]), lines[j - 1].animate.set_stroke(opacity=0.3), run_time=0.3)
            self.play(lines[7].animate.set_stroke(opacity=0.3), ReplacementTransform(c1, r1[0]),
                      FadeIn(r1[1], shift=LEFT * 0.1), run_time=0.5)

            # (2) X fills that line: 3 x 2 x 1 = 6 orders
            vo.wait_until("Second, X fills")
            self.play(FadeOut(VGroup(*lines[1:])), lines[0].animate.set_stroke(opacity=1),
                      heads[0].animate.set_color(S.GREY), heads[1].animate.set_color(S.WHITE),
                      run_time=0.6)
            orders = list(itertools.permutations((1, 3, 5)))   # label on squares 0, 1, 2
            xs = VGroup(*[board.mark_at(i, "X", scale=MARK_SCALE) for i in (0, 1, 2)])
            labels = {n: move_number(board, i, n, "X") for i, n in zip((0, 1, 2), orders[0])}
            c2 = count_tex(1, r2[6].get_center())
            self.play(LaggedStart(*[mark_anim(x) for x in xs], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(labels[n], scale=0.6) for n in orders[0]], lag_ratio=0.3),
                      FadeIn(c2, scale=0.6), run_time=0.9)
            budget = max(2.0, vo.time_until("3 times 2") - 0.2)
            for k in range(1, len(orders)):
                self.play(*[labels[n].animate(path_arc=-0.45 * PI).move_to(corner(board, orders[k].index(n)))
                            for n in orders[k] if orders[k].index(n) != orders[k - 1].index(n)],
                          run_time=min(0.6, budget / 5))
                c2.become(count_tex(k + 1, r2[6].get_center()))
            vo.wait_until("3 times 2")
            self.play(FadeIn(r2[0:6], lag_ratio=0.3), run_time=1.2)
            vo.wait_until("which is 3")
            self.play(Indicate(r2[0:5], color=S.WHITE, scale_factor=1.12), run_time=0.8)
            vo.wait_until("so 6 orders")
            self.play(ReplacementTransform(c2, r2[6]), Indicate(VGroup(*labels.values()), scale_factor=1.3),
                      run_time=0.6)

            # (3) O's 2 marks: 6 x 5 = 30
            vo.wait_until("Third, O")
            self.play(heads[1].animate.set_color(S.GREY), heads[2].animate.set_color(S.WHITE), run_time=0.4)
            dots = VGroup()

            def hop_through(squares, n, counter_slot):
                o = VGroup(board.mark_at(squares[0], "O", scale=MARK_SCALE),
                           move_number(board, squares[0], n, "O"))
                off = o.get_center() - board.center_of(squares[0])
                c = count_tex(1, counter_slot)
                self.play(Create(o[0]), FadeIn(o[1], scale=0.6), FadeIn(c, scale=0.6), run_time=0.45)
                for k, sq in enumerate(squares[1:], start=2):
                    dot = Dot(board.center_of(squares[k - 2]), radius=0.08, color=O_COLOR).set_opacity(0.7)
                    dots.add(dot)
                    self.play(o.animate(path_arc=-0.6 * PI).move_to(board.center_of(sq) + off),
                              FadeIn(dot, scale=0.5), run_time=0.42)
                    c.become(count_tex(k, counter_slot))
                return o, c

            _, c3a = hop_through((3, 5, 6, 7, 8, 4), 2, r3[0].get_center())
            self.play(ReplacementTransform(c3a, r3[0]), FadeOut(dots), run_time=0.4)
            dots.remove(*dots.submobjects)
            vo.wait_until("and O's second")
            self.play(FadeIn(r3[1]), run_time=0.3)
            _, c3b = hop_through((3, 5, 6, 7, 8), 4, r3[2].get_center())
            self.play(ReplacementTransform(c3b, r3[2]), FadeOut(dots), run_time=0.4)
            vo.wait_until("6 times 5")
            self.play(FadeIn(r3[3:5], shift=LEFT * 0.1), run_time=0.6)

            # multiply
            vo.wait_until("Multiply")
            self.play(heads[2].animate.set_color(S.GREY), Create(sep), run_time=0.4)
            self.play(TransformFromCopy(r1[0], final[0]), TransformFromCopy(r2[6], final[2]),
                      TransformFromCopy(r3[4], final[4]), FadeIn(final[1]), FadeIn(final[3]),
                      run_time=1.2)
            vo.wait_until("is 1,440")
            self.play(Write(final[5:]), run_time=0.8)
            box = highlight_box(final[6], color=COUNT_COLOR, buff=0.08)
            self.play(Create(box), Indicate(final[6], color=COUNT_COLOR, scale_factor=1.15), run_time=0.6)

        self.wait(0.8)   # let the answer sit for a moment before the cut
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
