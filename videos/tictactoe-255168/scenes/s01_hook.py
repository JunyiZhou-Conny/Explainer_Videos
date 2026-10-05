"""S01 · How many games? (reference scene for the rest of the video).

Beats: a quick game on a big board -> two games with the same final board but different move
orders (move numbers in the squares) -> a turned copy is a different game too -> ponder: guess ->
255,168, and a preview of the program that prints it.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.scene import VoiceScene

from common import COUNT_COLOR, NARRATION, O_COLOR, TOTAL_GAMES, X_COLOR, Board, code_block

SAY = NARRATION["S01"]


def move_number(board: Board, i: int, n: int, symbol: str, size: float = 24) -> Text:
    """Small move number in the lower-right corner of square i, in the player's colour."""
    color = X_COLOR if symbol == "X" else O_COLOR
    return S.text(str(n), size, color, font=S.FONT_SANS) \
        .move_to(board.center_of(i) + np.array([0.36, -0.36, 0]) * board.cell)


def play_moves(scene, board: Board, moves, numbers: bool = False, scale: float = 0.46,
               run_time: float = 0.45) -> VGroup:
    """Animate moves [(square, 'X'|'O'), ...] onto `board`; returns VGroup of marks (+ numbers)."""
    placed = VGroup()
    for n, (i, sym) in enumerate(moves, start=1):
        m = board.mark_at(i, sym, scale=scale)
        anims = [Create(m) if sym == "O" else LaggedStart(*[Create(s) for s in m], lag_ratio=0.5)]
        placed.add(m)
        if numbers:
            num = move_number(board, i, n, sym)
            anims.append(FadeIn(num, scale=0.6))
            placed.add(num)
        scene.play(*anims, run_time=run_time)
    return placed


def rotate_cw(i: int) -> int:
    """Square index after turning the board a quarter turn clockwise."""
    r, c = divmod(i, 3)
    return c * 3 + (2 - r)


class Hook(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- a quick game
        title = S.text("How many different games of tic-tac-toe?", 44).to_edge(UP, buff=0.6)
        board = Board(size=4.2).shift(DOWN * 0.4)
        game = [(4, "X"), (0, "O"), (1, "X"), (3, "O"), (7, "X")]    # X wins down the middle column

        with self.voiceover(SAY[0]) as vo:
            self.play(LaggedStart(*[Create(ln) for ln in board], lag_ratio=0.2), run_time=1.0)
            marks = play_moves(self, board, game, scale=0.6, run_time=0.4)
            win = board.win_line(1, 7)
            self.play(Create(win), run_time=0.5)
            vo.wait_until("How many")
            self.play(Write(title), run_time=1.2)

        # ---------------------------------------------------------- same board, different order
        # Both games end with X on the top row (0, 1, 2) and O on 3 and 4; X wins on move 5.
        order_a = [(0, "X"), (3, "O"), (1, "X"), (4, "O"), (2, "X")]
        order_b = [(2, "X"), (4, "O"), (0, "X"), (3, "O"), (1, "X")]
        left = Board(size=3.3).move_to(LEFT * 3.5 + DOWN * 0.1)
        right = Board(size=3.3).move_to(RIGHT * 3.5 + DOWN * 0.1)
        neq = S.math(r"\neq", size=84).move_to(DOWN * 0.1)
        caption = S.text("same board, different order  →  different games", 30, S.WHITE) \
            .to_edge(DOWN, buff=0.45)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(board, marks, win)), title.animate.scale(0.75).to_edge(UP, buff=0.45),
                      run_time=0.8)
            self.play(LaggedStart(*[Create(ln) for ln in left], lag_ratio=0.15), run_time=0.6)
            vo.wait_until("the whole list")
            game_a = play_moves(self, left, order_a, numbers=True, run_time=0.35)
            win_a = left.win_line(0, 2)
            self.play(Create(win_a), run_time=0.6)
            vo.wait_until("So if two games")
            self.play(LaggedStart(*[Create(ln) for ln in right], lag_ratio=0.15), run_time=0.6)
            game_b = play_moves(self, right, order_b, numbers=True, run_time=0.35)
            win_b = right.win_line(0, 2)
            self.play(Create(win_b), run_time=0.6)
            vo.wait_until("they count as")
            self.play(Write(neq), FadeIn(caption, shift=UP * 0.2), run_time=0.8)

            # a quarter-turned copy of the left game is a different game too
            vo.wait_until("Flipped or turned")
            turned_caption = S.text("turned board  →  a different game too", 30, S.WHITE) \
                .to_edge(DOWN, buff=0.45)
            self.play(FadeOut(VGroup(right, game_b, win_b)), FadeTransform(caption, turned_caption), run_time=0.6)
            turned = VGroup(left.copy(), *[m.copy() for m in game_a if not isinstance(m, Text)],
                            win_a.copy())
            turned_nums = VGroup(*[m.copy() for m in game_a if isinstance(m, Text)])
            self.play(turned.animate.move_to(right), turned_nums.animate.shift(right.get_center() - left.get_center()),
                      run_time=0.7)
            c = turned[0].get_center()
            targets = []
            for num, (i, _) in zip(turned_nums, order_a):
                q = rotate_cw(i)
                targets.append(right.center_of(q) + np.array([0.36, -0.36, 0]) * right.cell)
            self.play(Rotate(turned, angle=-PI / 2, about_point=c),
                      *[num.animate(path_arc=-PI / 2).move_to(t) for num, t in zip(turned_nums, targets)],
                      run_time=1.2)
            self.play(Indicate(neq, color=S.WHITE), run_time=0.7)
        self.wait(0.8)

        # ---------------------------------------------------------- guess
        guesses = VGroup(S.text("100?", 48, S.WHITE), S.text("1,000,000?", 48, S.WHITE)) \
            .arrange(RIGHT, buff=2.5).move_to(UP * 0.4)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(left, game_a, win_a, neq, turned, turned_nums, turned_caption)),
                      run_time=0.7)
            vo.wait_until("A hundred")
            self.play(FadeIn(guesses[0], scale=0.8), run_time=0.5)
            vo.wait_until("A million")
            self.play(FadeIn(guesses[1], scale=0.8), run_time=0.5)
            vo.wait_until("Pause the video")
            card = ponder_card("How many different games of tic-tac-toe are there?\nWrite down a guess!")
            self.play(FadeOut(guesses), FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ---------------------------------------------------------- the answer
        answer = S.text(f"{TOTAL_GAMES:,}", 120, COUNT_COLOR).move_to(UP * 0.9)
        counting = VGroup(S.text("careful counting", 30, S.WHITE),
                          S.math(r"9 \times 8 \times 7 \times \cdots", size=40)).arrange(DOWN, buff=0.25)
        program = VGroup(S.text("a short program", 30, S.WHITE),
                         code_block("print(play_all_games())", font_size=24, width=4.4),
                         ).arrange(DOWN, buff=0.25)
        output = S.text("255168", 30, COUNT_COLOR, font="DejaVu Sans Mono")
        VGroup(counting, program).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to(DOWN * 1.9)
        output.next_to(program[1], DOWN, buff=0.2).align_to(program[1], LEFT).shift(RIGHT * 0.25)
        arrow = Arrow(counting.get_right(), program.get_left(), buff=0.3, color=S.GREY, stroke_width=4)

        where = S.text("where does it come from?", 36, S.GREY).next_to(answer, DOWN, buff=0.45)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(card), run_time=0.5)
            self.play(Write(answer), run_time=1.4)
            vo.wait_until("In this video")
            self.play(FadeIn(where, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("where that number")
            self.play(Indicate(answer, color=COUNT_COLOR, scale_factor=1.06), Wiggle(where, scale_value=1.05),
                      run_time=1.0)
            vo.wait_until("first by careful")
            self.play(FadeOut(where, shift=UP * 0.2), FadeIn(counting, shift=UP * 0.3), run_time=0.8)
            vo.wait_until("and then with")
            self.play(GrowArrow(arrow), FadeIn(program, shift=UP * 0.3), run_time=0.8)
            self.play(FadeIn(output, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(answer, color=COUNT_COLOR, scale_factor=1.05), run_time=vo.remaining())

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
