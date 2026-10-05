"""S08 · 255,168, explained.

Beats: explore() exactly as S07 left it (S06/S07 size, winner check struck out) -> the strike is
erased, the panel grows, then folds into the "..." of play_all_games() -> the program runs in a
terminal and prints 255168
-> a bar chart of games by the move they end on (linear scale: moves 5 and 6 are tiny slivers)
-> each bar times its ghost multiplier (x24, x6, x2, x1, x1) stacks into nine factorial
-> the same bars regroup by result: X wins / O wins / draws
-> ponder: which first move gives the most games? -> edge > corner > center, and the winning lines
   through each first mark explain why -> more games is not a better move (X's share of wins).
"""

from collections import Counter

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.scene import VoiceScene

from common import (BY_MOVE, COUNT_COLOR, DRAW_COLOR, DRAWS, FIRST_MOVE_GAMES, GHOST_COLOR,
                    MOVE9_DRAWS, MOVE9_X_WINS, NARRATION, NINE_FACTORIAL, O_COLOR, O_WINS,
                    TOTAL_GAMES, UNDO_COLOR, WIN_COLOR, WIN_LINES, X_COLOR, X_WINS, Board,
                    code_block, explore_code, line_highlight, strike, winner)

SAY = NARRATION["S08"]
MONO = "DejaVu Sans Mono"


# ------------------------------------------------------------------ numbers (all checked here)
def _results_by_first_move():
    """{first square: Counter(X=..., O=..., D=...)} by playing every game, like the program."""
    board, out = ["."] * 9, {s: Counter() for s in range(9)}

    def explore(player, first):
        w = winner(board)
        if w is not None or "." not in board:
            out[first][w or "D"] += 1
            return
        for sq in range(9):
            if board[sq] == ".":
                board[sq] = player
                explore("O" if player == "X" else "X", sq if first is None else first)
                board[sq] = "."

    explore("X", None)
    return out


FIRST = _results_by_first_move()
CENTER, EDGE, CORNER = FIRST[4], FIRST[1], FIRST[0]
assert sum(CENTER.values()) == FIRST_MOVE_GAMES["centre"] == 25_872
assert sum(EDGE.values()) == FIRST_MOVE_GAMES["edge"] == 29_592
assert sum(CORNER.values()) == FIRST_MOVE_GAMES["corner"] == 27_732
assert (CENTER["X"], EDGE["X"]) == (15_648, 14_232)          # 60.5 % and 48.1 %
assert 4 * 27_732 + 4 * 29_592 + 25_872 == TOTAL_GAMES
assert sum(BY_MOVE.values()) == TOTAL_GAMES and MOVE9_X_WINS + MOVE9_DRAWS == BY_MOVE[9]
GHOSTS = {5: 24, 6: 6, 7: 2, 8: 1, 9: 1}                         # (9 - k)! ghost endings
GHOST_WHY = {5: "(4×3×2×1)", 6: "(3×2×1)", 7: "(2×1)"}
assert sum(BY_MOVE[k] * GHOSTS[k] for k in BY_MOVE) == NINE_FACTORIAL
assert BY_MOVE[5] + BY_MOVE[7] + MOVE9_X_WINS == X_WINS and BY_MOVE[6] + BY_MOVE[8] == O_WINS


def fmt(n: int) -> str:
    return f"{n:,}"


# ------------------------------------------------------------------ chart geometry
Y0 = -2.45                                   # baseline of every bar chart in this scene
BAR_W = 1.3
XS = {5: -5.0, 6: -3.0, 7: -1.0, 8: 1.0, 9: 3.0}
U2 = 4.2 / BY_MOVE[9]                        # units per game: the chart of real games
U3 = 5.3 / NINE_FACTORIAL                    # zoomed out so that nine factorial fits
STACK_X = 5.75
COLS = {"X": -3.5, "O": 0.0, "D": 3.5}       # X wins / O wins / draws


def bar(x: float, h: float, color: str, bottom: float = Y0, width: float = BAR_W) -> Rectangle:
    return Rectangle(width=width, height=h, stroke_width=0).set_fill(color, 1) \
        .move_to([x, bottom + h / 2, 0])


def ghost_block(x: float, bottom: float, h: float) -> VGroup:
    """The ghost part of a bar: faded GREY with a dashed outline (moves that never get played)."""
    fill = Rectangle(width=BAR_W, height=h, stroke_width=0).set_fill(GHOST_COLOR, 0.28)
    edge = DashedVMobject(Rectangle(width=BAR_W, height=h, stroke_color=GHOST_COLOR, stroke_width=3),
                          num_dashes=max(8, int((2 * BAR_W + 2 * h) / 0.16)))
    return VGroup(fill, edge).move_to([x, bottom + h / 2, 0])


def above(m: Mobject, top: float, buff: float = 0.12) -> np.ndarray:
    """Centre for `m` so that it sits `buff` above height `top`."""
    return np.array([m.get_center()[0], top + buff + m.height / 2, 0])


def check_mark(size: float = 0.42, color: str = COUNT_COLOR, stroke: float = 8) -> VMobject:
    pts = [np.array(p) * size for p in ([-0.5, 0.05, 0], [-0.12, -0.4, 0], [0.55, 0.45, 0])]
    return VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners(pts)


def crown(width: float = 0.9, color: str = S.GOLD) -> Polygon:
    w, h = width / 2, width * 0.6
    pts = [(-w, 0), (w, 0), (w, h), (w * 0.45, h * 0.45), (0, h), (-w * 0.45, h * 0.45), (-w, h)]
    return Polygon(*[np.array([x, y, 0]) for x, y in pts], color=color, stroke_width=3) \
        .set_fill(color, 1)


def caution_sign(width: float = 0.85, color: str = UNDO_COLOR) -> VGroup:
    tri = Triangle(color=color, stroke_width=6).set_fill(S.BG, 1).scale_to_fit_width(width)
    tri.round_corners(0.06)
    bang = S.text("!", 34, color, weight=BOLD).move_to(tri.get_center() + DOWN * 0.08 * width)
    return VGroup(tri, bang)


def terminal(width: float = 7.4, height: float = 2.3) -> VGroup:
    """A dark terminal window: frame, title strip, three dots."""
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.16,
                             stroke_color=S.GREY_DARK, stroke_width=2).set_fill("#05070B", 1)
    strip_y = frame.get_top()[1] - 0.36
    sep = Line([frame.get_left()[0], strip_y, 0], [frame.get_right()[0], strip_y, 0],
               color=S.GREY_DARK, stroke_width=2)
    dots = VGroup(*[Circle(radius=0.065, stroke_width=0).set_fill(S.GREY_DARK, 1) for _ in range(3)]) \
        .arrange(RIGHT, buff=0.12).move_to([frame.get_left()[0] + 0.45, (frame.get_top()[1] + strip_y) / 2, 0])
    return VGroup(frame, sep, dots)


def on_baseline(t: Text, x: float, y: float) -> Text:
    """Centre text t at x with the bottom of its first letter (an x-height letter) at height y,
    so words with and without ascenders/descenders line up."""
    t.set_x(x)
    t.shift(UP * (y - t[0].get_bottom()[1]))
    return t


def first_move_board(square: int, x: float, y: float, size: float = 2.0) -> VGroup:
    b = Board(size=size, stroke=5).move_to([x, y, 0])
    g = VGroup(b, b.mark_at(square, "X", scale=0.6))
    g.board = b
    return g


def mini_tree(center_x: float = 0.0, top: float = -1.8):
    """A small schematic game tree: root, 3 children, 3 grandchildren each, 2 leaves each."""
    ys = [top, top - 0.5, top - 1.0, top - 1.45]
    nodes, edges = {}, VGroup()
    nodes[()] = np.array([center_x, ys[0], 0])
    for i, dx in enumerate((-1.8, 0, 1.8)):
        nodes[(i,)] = np.array([center_x + dx, ys[1], 0])
        for j, dx2 in enumerate((-0.55, 0, 0.55)):
            nodes[(i, j)] = nodes[(i,)] + np.array([dx2, ys[2] - ys[1], 0])
            for k, dx3 in enumerate((-0.14, 0.14)):
                nodes[(i, j, k)] = nodes[(i, j)] + np.array([dx3, ys[3] - ys[2], 0])
    dots, lines = {}, {}
    for key, p in nodes.items():
        dots[key] = Dot(p, radius=0.06 if len(key) < 3 else 0.045, color=S.WHITE)
        if key:
            lines[key] = Line(nodes[key[:-1]], p, color=S.GREY, stroke_width=2.5)
    return nodes, dots, lines


class Answer(VoiceScene):
    def construct(self):
        # ================================================================ 1. run the real program
        # S07 ends on explore() at the S06/S07 size and place with the winner check struck out and
        # dimmed: S08 opens on exactly that, erases the strike, and only then grows the panel so it
        # can be read (~21 pt instead of ~13 pt)
        code = explore_code()
        cuts = VGroup(strike(code, 1), strike(code, 2))          # how S07 left the winner check
        win_texts = VGroup(code.code_lines[1], code.code_lines[2])
        win_texts.set_opacity(0.35)                              # dimmed, as in S07
        # the end of the program; "..." is where explore() lives (the panel folds into it)
        tail = code_block('def play_all_games():\n'
                          '    board = ["."] * 9\n'
                          '    ...\n'
                          '    return explore("X")\n'
                          '\n'
                          'print(play_all_games())', font_size=26).move_to([-2.4, 1.85, 0])
        RET, DOTS, PRINT = 3, 2, 5                               # tail.code_lines indices
        hl_ret, hl_print = line_highlight(tail, RET), line_highlight(tail, PRINT)
        y_ret = tail.code_lines[RET].get_center()[1]
        start_board = Board(size=0.9, stroke=3)
        start_txt = VGroup(S.text("start: empty board,", 26, S.WHITE),
                           S.text("X's turn", 26, X_COLOR)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        start_lab = VGroup(start_board, start_txt).arrange(RIGHT, buff=0.25)
        start_lab.move_to([tail.get_right()[0] + 0.75 + start_lab.width / 2, y_ret - 0.1, 0])
        start_arrow = Arrow(start_lab.get_left() + LEFT * 0.05, [tail.get_right()[0] + 0.02, y_ret, 0], buff=0.05,
                            color=S.GREY, stroke_width=3, max_tip_length_to_length_ratio=0.35)

        term = terminal().move_to([2.4, -1.6, 0])
        tframe = term[0]
        prompt = S.text("$", 28, S.GREY, font=MONO)
        cmd = S.text("python play_all_games.py", 28, S.WHITE, font=MONO)
        cmd_line = VGroup(prompt, cmd).arrange(RIGHT, buff=0.22)
        cmd_line.move_to(tframe.get_corner(UL) + np.array([0.3 + cmd_line.width / 2, -0.75, 0]))
        output = S.text("255168", 44, COUNT_COLOR, font=MONO)
        output.next_to(cmd_line, DOWN, buff=0.3).align_to(cmd_line, LEFT)
        cursor = Rectangle(width=0.16, height=0.34, stroke_width=0).set_fill(S.WHITE, 0.8) \
            .next_to(cmd_line, DOWN, buff=0.35).align_to(cmd_line, LEFT)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(code), FadeIn(cuts), run_time=0.4)
            vo.wait_until("put every line back")
            # GREEN bars on the restored lines (inset a little so they stay inside x >= -6.6)
            back = VGroup(*[line_highlight(code, k, COUNT_COLOR).stretch_to_fit_width(code.background.width - 0.36)
                            for k in (1, 2)])
            self.play(Uncreate(cuts), win_texts.animate.set_opacity(1), FadeIn(back), run_time=0.7)
            # now grow the whole panel to a readable size
            explore_panel = VGroup(code, back).set_z_index(1)    # stays in front of the tail below
            self.play(explore_panel.animate.scale_to_fit_width(13.0).move_to([0, 0.2, 0]), run_time=0.6)
            self.wait(0.3)
            # the end of the program: explore() folds away into the "..." inside play_all_games()
            dots = tail.code_lines[DOTS]
            self.play(explore_panel.animate.scale(0.7 / explore_panel.width).move_to(dots.get_center())
                      .set_opacity(0),
                      FadeIn(tail, run_time=0.6), run_time=0.9)
            self.remove(explore_panel)
            self.play(FadeIn(hl_ret), GrowArrow(start_arrow), FadeIn(start_txt, shift=LEFT * 0.15),
                      Create(start_board), run_time=0.7)
            self.play(FadeIn(hl_print), run_time=0.3)
            vo.wait_until("After a moment")
            self.play(FadeIn(term), run_time=0.4)
            self.play(FadeIn(prompt, run_time=0.1), AddTextLetterByLetter(cmd, run_time=0.8))
            self.add(cursor)
            while vo.time_until("it prints") > 0.4:           # the program thinks...
                self.play(cursor.animate.set_opacity(0.0), run_time=0.25)
                self.play(cursor.animate.set_opacity(0.8), run_time=0.25)
            vo.wait_until("it prints")
            self.remove(cursor)
            self.play(FadeIn(output, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(output, color=COUNT_COLOR, scale_factor=1.15), run_time=0.8)

        # ================================================================ 2. split by the move a game ends on
        total = S.text(fmt(TOTAL_GAMES), 44, COUNT_COLOR).move_to([0, 3.05, 0])
        axis = Line([-6.2, Y0, 0], [4.1, Y0, 0], color=S.GREY, stroke_width=3)
        ticks = VGroup(*[S.text(f"move {m}", 26, S.GREY).move_to([XS[m], Y0 - 0.35, 0]) for m in XS])
        legend = VGroup(*[VGroup(Square(0.3, stroke_width=0).set_fill(c, 1), S.text(t, 26, c))
                          .arrange(RIGHT, buff=0.2) for c, t in ((X_COLOR, "X wins"), (O_COLOR, "O wins"),
                                                                  (DRAW_COLOR, "draws"))])
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-5.15, 1.1, 0])

        bars = {m: bar(XS[m], BY_MOVE[m] * U2, X_COLOR if m % 2 else O_COLOR) for m in (5, 6, 7, 8)}
        b9x = bar(XS[9], MOVE9_X_WINS * U2, X_COLOR)
        b9d = bar(XS[9], MOVE9_DRAWS * U2, DRAW_COLOR, bottom=b9x.get_top()[1])
        vals = {}
        for m in (5, 6, 7, 8):
            vals[m] = S.text(fmt(BY_MOVE[m]), 28, S.WHITE)
            vals[m].move_to(above(vals[m], bars[m].get_top()[1])).set_x(XS[m])
        in9x = VGroup(S.text(fmt(MOVE9_X_WINS), 26, S.BG, weight=BOLD), S.text("X wins", 24, S.BG)) \
            .arrange(DOWN, buff=0.1).move_to(b9x)
        in9d = VGroup(S.text(fmt(MOVE9_DRAWS), 26, S.BG, weight=BOLD), S.text("draws", 24, S.BG)) \
            .arrange(DOWN, buff=0.1).move_to(b9d)
        by_hand = VGroup(check_mark(), S.text("counted by hand", 28, COUNT_COLOR)).arrange(RIGHT, buff=0.2)
        by_hand.move_to([(XS[5] + XS[6]) / 2, -1.25, 0])
        nine = VGroup(b9x, b9d)
        brace = Brace(nine, RIGHT, buff=0.12, color=S.WHITE)
        half_lab = S.text("just over half", 28, S.WHITE).next_to(brace, RIGHT, buff=0.15)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(tail, hl_ret, hl_print, start_lab, start_arrow,
                                     term, prompt, cmd)),
                      FadeTransform(output, total), run_time=1.0)    # "255168" -> "255,168": no glyph morph
            self.play(Create(axis), FadeIn(ticks, lag_ratio=0.1), FadeIn(legend, shift=RIGHT * 0.2),
                      run_time=1.0)
            vo.wait_until("1,440 end on")
            self.play(GrowFromEdge(bars[5], DOWN), FadeIn(vals[5], shift=UP * 0.2), run_time=0.8)
            vo.wait_until("and 5,328")
            self.play(GrowFromEdge(bars[6], DOWN), FadeIn(vals[6], shift=UP * 0.2), run_time=0.8)
            vo.wait_until("the same numbers")
            self.play(Create(by_hand[0]), FadeIn(by_hand[1], shift=UP * 0.15), run_time=0.8)
            self.play(Indicate(VGroup(vals[5], vals[6]), color=COUNT_COLOR, scale_factor=1.12), run_time=1.0)
            vo.wait_until("Then the bars")
            self.play(LaggedStart(GrowFromEdge(bars[7], DOWN), GrowFromEdge(bars[8], DOWN),
                                  Succession(GrowFromEdge(b9x, DOWN), GrowFromEdge(b9d, DOWN)),
                                  lag_ratio=0.3), run_time=1.8)
            vo.wait_until("about 48")
            self.play(FadeIn(vals[7], shift=UP * 0.2), run_time=0.5)
            vo.wait_until("and 73")
            self.play(FadeIn(vals[8], shift=UP * 0.2), run_time=0.5)
            vo.wait_until("Just over half")
            self.play(GrowFromCenter(brace), FadeIn(half_lab, shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("about 82")
            self.play(FadeIn(in9x, scale=0.8), run_time=0.5)
            vo.wait_until("plus 46,080")
            self.play(FadeIn(in9d, scale=0.8), run_time=0.5)

            # the exact sum: every bar label flies up into one line
            vo.wait_until("Together")
            terms = [vals[5], vals[6], vals[7], vals[8], in9x[0], in9d[0]]
            parts = VGroup()
            for i, t in enumerate(terms):
                parts.add(S.text(t.text, 30, S.WHITE))
                parts.add(S.text("+" if i < len(terms) - 1 else "=", 30, S.GREY))
            parts.add(S.text(fmt(TOTAL_GAMES), 30, COUNT_COLOR, weight=BOLD))
            parts.arrange(RIGHT, buff=0.16).move_to([0, 3.05, 0])
            self.play(LaggedStart(*[TransformFromCopy(t, parts[2 * i]) for i, t in enumerate(terms)],
                                  lag_ratio=0.12),
                      FadeIn(VGroup(*[parts[2 * i + 1] for i in range(len(terms))]), lag_ratio=0.1),
                      ReplacementTransform(total, parts[-1]), run_time=1.8)
            self.play(Circumscribe(parts[-1], color=COUNT_COLOR, fade_out=True), run_time=vo.remaining())

        # ================================================================ 3. ghost multipliers -> nine factorial
        f = U3 / U2
        chart_bars = VGroup(*[bars[m] for m in (5, 6, 7, 8)], b9x, b9d)
        tops = {m: Y0 + BY_MOVE[m] * U3 for m in XS}
        lab9 = S.text(fmt(BY_MOVE[9]), 28, S.WHITE)
        lab9.move_to([XS[9], tops[9] + 0.12 + lab9.height / 2, 0])
        prods, mults, ghosts = {}, {}, {}
        # the target: an empty dashed GREEN outline as tall as nine factorial, waiting to be filled
        goal_h = NINE_FACTORIAL * U3
        goal = DashedVMobject(Rectangle(width=BAR_W, height=goal_h, stroke_color=COUNT_COLOR, stroke_width=3),
                              num_dashes=int((2 * BAR_W + 2 * goal_h) / 0.2)) \
            .move_to([STACK_X, Y0 + goal_h / 2, 0])
        goal_lab = S.text("9!", 36, S.WHITE)
        goal_lab.move_to([STACK_X, Y0 + goal_h + 0.14 + goal_lab.height / 2, 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(parts, legend, by_hand, brace, half_lab), run_time=0.6),
                      chart_bars.animate.stretch(f, 1, about_point=np.array([0, Y0, 0])),
                      *[vals[m].animate.move_to(above(vals[m], tops[m])) for m in (5, 6, 7, 8)],
                      FadeTransform(VGroup(in9x[0], in9d[0]), lab9),
                      FadeOut(VGroup(in9x[1], in9d[1])), run_time=1.3)
            vals[9] = lab9
            vo.wait_until("connects to nine")
            self.play(Create(goal), FadeIn(goal_lab, shift=DOWN * 0.15), run_time=0.9)

            def multiply(m: int, grow_at: str | None, play: bool = True):
                """Show xk above bar m, then grow its ghost part and turn its label into the product."""
                k = GHOSTS[m]
                head = S.text(f"×{k}", 34, S.WHITE)
                mult = VGroup(head)
                if m in GHOST_WHY:
                    mult.add(S.text(GHOST_WHY[m], 24, S.GREY))
                mult.arrange(DOWN, buff=0.08)
                mult.move_to(above(mult, vals[m].get_top()[1], 0.14)).set_x(XS[m])
                mults[m] = mult
                if not play:                      # x1: no ghosts, the bar stays as it is
                    prods[m] = vals[m]
                    return FadeIn(mult, shift=DOWN * 0.2)
                self.play(FadeIn(mult, shift=DOWN * 0.2), run_time=0.6)
                if grow_at:
                    vo.wait_until(grow_at)
                h = BY_MOVE[m] * U3
                gh = ghost_block(XS[m], Y0 + h, BY_MOVE[m] * (k - 1) * U3)
                ghosts[m] = gh
                new_top = gh.get_top()[1]
                prod = S.text(fmt(BY_MOVE[m] * k), 28, S.WHITE)
                prod.move_to([XS[m], new_top + 0.12 + prod.height / 2, 0])
                prods[m] = prod
                mult_target = mult.copy().move_to(above(mult, prod.get_top()[1], 0.14)).set_x(XS[m])
                self.play(GrowFromEdge(gh, DOWN), FadeTransform(vals[m], prod),
                          mult.animate.move_to(mult_target), run_time=1.3)

            vo.wait_until("each game that ends")
            self.play(Circumscribe(VGroup(bars[5], vals[5]), color=S.WHITE, buff=0.12), run_time=1.0)
            vo.wait_until("a total of 24")
            multiply(5, None)
            vo.wait_until("once for each ghost")
            self.play(Indicate(ghosts[5], color=S.WHITE, scale_factor=1.08), run_time=0.9)
            vo.wait_until("A game ending on move 6")
            multiply(6, None)
            vo.wait_until("and on move 7")
            multiply(7, None)
            # moves 8 and 9 leave at most one empty square: no ghosts, x1
            vo.wait_until("Games that end on move 8")
            ones = [multiply(m, None, play=False) for m in (8, 9)]
            self.play(*ones, run_time=0.6)
            vo.wait_until("so they were counted")
            self.play(Indicate(VGroup(mults[8], mults[9]), color=S.WHITE, scale_factor=1.2), run_time=0.8)

            # multiply and add: the products fly up into one sum (straight up their own column, above
            # every bar), the pieces rise to their height in the stack, then slide right into the 9! outline
            vo.wait_until("Multiply each bar")
            self.play(FadeOut(VGroup(*mults.values()), shift=UP * 0.2), run_time=0.3)
            order = (5, 6, 7, 8, 9)
            sum_line = VGroup()
            for i, m in enumerate(order):
                sum_line.add(S.text(fmt(BY_MOVE[m] * GHOSTS[m]), 30, S.WHITE))
                if i < len(order) - 1:
                    sum_line.add(S.text("+", 30, S.GREY))
            sum_line.arrange(RIGHT, buff=0.18).move_to([-0.8, 3.2, 0])
            pieces, rise, y = {}, [], Y0
            for m in (9, 8, 7, 6, 5):                 # the tallest product (move 9) at the bottom
                solid = VGroup(bars[m].copy()) if m != 9 else VGroup(b9x.copy(), b9d.copy())
                piece = VGroup(solid, ghosts[m]) if m in ghosts else solid
                self.add(piece)                       # ghosts[m] is re-added on top of the solid copy
                rise.append(piece.animate.shift(UP * (y - Y0)))
                pieces[m] = piece
                y += BY_MOVE[m] * GHOSTS[m] * U3
            self.play(*rise, *[ReplacementTransform(prods[m], sum_line[2 * i]) for i, m in enumerate(order)],
                      FadeIn(VGroup(*sum_line[1::2])), run_time=0.9)
            vo.wait_until("add them up")
            self.play(LaggedStart(*[pieces[m].animate.shift(RIGHT * (STACK_X - XS[m])) for m in pieces],
                                  lag_ratio=0.08), run_time=1.0)

            vo.wait_until("and you get exactly")
            tower = Rectangle(width=BAR_W, height=y - Y0, stroke_width=0).set_fill(COUNT_COLOR, 1) \
                .move_to([STACK_X, (Y0 + y) / 2, 0])
            tbrace = Brace(tower, LEFT, buff=0.12, color=S.WHITE)
            fact = VGroup(S.text(fmt(NINE_FACTORIAL), 40, COUNT_COLOR, weight=BOLD),
                          S.text("= 9!", 40, S.WHITE)).arrange(RIGHT, buff=0.2)
            fact.next_to(tbrace, LEFT, buff=0.3)
            self.play(ReplacementTransform(VGroup(*pieces.values()), tower), FadeOut(goal),
                      FadeTransform(sum_line, fact[0]), GrowFromCenter(tbrace), run_time=1.0)
            self.play(FadeTransform(goal_lab, fact[1]), run_time=0.6)
            # let it land: hold the full stack (362,880 = 9!) for ~1.5 s before the next beat
            self.play(Indicate(fact, color=COUNT_COLOR, scale_factor=1.06), run_time=1.5)

        # ================================================================ 4. who wins?
        g = U2 / U3
        x_parts = [bars[5], bars[7], b9x]
        o_parts = [bars[6], bars[8]]
        new_axis = Line([-5.3, Y0, 0], [5.3, Y0, 0], color=S.GREY, stroke_width=3)
        res = {"X": (X_WINS, X_COLOR, "X wins"), "O": (O_WINS, O_COLOR, "O wins"),
               "D": (DRAWS, DRAW_COLOR, "draws")}
        res_num, res_name = {}, {}
        for key, (n, c, name) in res.items():
            res_num[key] = S.text(fmt(n), 36, c, weight=BOLD)
            res_num[key].move_to([COLS[key], Y0 + n * U2 + 0.14 + res_num[key].height / 2, 0])
            res_name[key] = S.text(name, 32, c).move_to([COLS[key], Y0 - 0.4, 0])
        half_y = Y0 + TOTAL_GAMES / 2 * U2
        half_line = DashedLine([-4.7, half_y, 0], [4.7, half_y, 0], color=S.WHITE, stroke_width=3,
                               dash_length=0.14)
        half_txt = S.text("half of all games", 26, S.WHITE).next_to(half_line.get_right(), UP, buff=0.12) \
            .align_to(half_line, RIGHT)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(tower, tbrace, fact, ticks), run_time=0.6),
                      chart_bars.animate.stretch(g, 1, about_point=np.array([0, Y0, 0])),
                      ReplacementTransform(axis, new_axis), run_time=1.0)
            # sort the pieces into three columns by result
            moves, yx = [], Y0
            for p in x_parts:
                moves.append((p, np.array([COLS["X"], yx + p.height / 2, 0])))
                yx += p.height
            yo = Y0
            for p in o_parts:
                moves.append((p, np.array([COLS["O"], yo + p.height / 2, 0])))
                yo += p.height
            moves.append((b9d, np.array([COLS["D"], Y0 + b9d.height / 2, 0])))
            self.play(*[p.animate(path_arc=(PI / 2 if p is b9x else 0)).move_to(t) for p, t in moves],
                      run_time=1.3)
            self.play(FadeIn(res_num["X"], shift=UP * 0.2), FadeIn(res_name["X"], shift=UP * 0.2),
                      run_time=0.6)
            vo.wait_until("O wins")
            self.play(FadeIn(res_num["O"], shift=UP * 0.2), FadeIn(res_name["O"], shift=UP * 0.2),
                      run_time=0.6)
            vo.wait_until("and 46,080")
            self.play(FadeIn(res_num["D"], shift=UP * 0.2), FadeIn(res_name["D"], shift=UP * 0.2),
                      run_time=0.6)
            vo.wait_until("X wins in more")
            self.play(Create(half_line), FadeIn(half_txt), run_time=1.0)
            x_col = VGroup(*x_parts)
            self.play(Indicate(VGroup(x_col, res_num["X"]), color=X_COLOR, scale_factor=1.05), run_time=1.0)
            vo.wait_until("because going first")
            self.play(Circumscribe(VGroup(res_name["X"], res_num["X"], x_col), color=X_COLOR, fade_out=True),
                      run_time=1.4)

        # ================================================================ 5. ponder: the best first move
        spots = {"corner": 0, "edge": 1, "center": 4}
        bx = {"corner": -4.4, "edge": 0.0, "center": 4.4}
        boards = {k: Board(size=2.0, stroke=5).move_to([bx[k], -1.35, 0]) for k in spots}
        xs_ = {k: boards[k].mark_at(spots[k], "X", scale=0.6) for k in spots}
        names = {k: on_baseline(S.text(k, 30, S.WHITE), bx[k], -2.75) for k in spots}

        card = ponder_card("Which first move for X leads to the MOST different games:\n"
                           "corner, edge, or center?", width=11.8).to_edge(UP, buff=0.5)

        with self.voiceover(SAY[4]) as vo:
            # "One last puzzle": the wins chart fades while the three boards are already being drawn
            self.play(LaggedStart(FadeOut(Group(*self.mobjects), run_time=0.8),
                                  LaggedStart(*[Create(ln) for k in spots for ln in boards[k]],
                                              lag_ratio=0.04, run_time=1.5),
                                  lag_ratio=0.2))
            for k, anchor in (("corner", "a corner"), ("edge", "an edge"), ("center", "or the center")):
                vo.wait_until(anchor)
                self.play(LaggedStart(*[Create(s) for s in xs_[k]], lag_ratio=0.5),
                          FadeIn(names[k], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Pause and guess")                    # the card is up as "Pause" is said
            self.play(FadeIn(card, scale=0.95), run_time=0.6)
        timer = card[3]
        self.play(timer.animate(rate_func=linear).become(timer.copy().scale(0.001, about_point=timer.get_start())),
                  run_time=10)

        # ================================================================ 6. edge > corner > center, and why
        up = UP * 2.6
        board_groups = {k: VGroup(boards[k], xs_[k]) for k in spots}
        counts = {"corner": FIRST_MOVE_GAMES["corner"], "edge": FIRST_MOVE_GAMES["edge"],
                  "center": FIRST_MOVE_GAMES["centre"]}
        times = {"corner": "×4", "edge": "×4", "center": "×1"}
        new_names, nums = {}, {}
        for k in spots:
            new_names[k] = S.text(("each " if k != "center" else "") + k, 28, S.WHITE)
            on_baseline(new_names[k], bx[k], -2.75 + up[1])
            nums[k] = VGroup(S.text(fmt(counts[k]), 34, COUNT_COLOR, weight=BOLD),
                             S.text(f"({times[k]})", 28, S.GREY)).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        for k in spots:                      # same height for all three (no descender in "each corner")
            nums[k].next_to(new_names["corner"], DOWN, buff=0.18).set_x(bx[k])
        top_board = boards["edge"].get_top() + up
        king = crown().move_to(top_board + UP * 0.45)
        sum_terms = ["4 ×", fmt(counts["corner"]), "+", "4 ×", fmt(counts["edge"]), "+",
                     fmt(counts["center"]), "=", fmt(TOTAL_GAMES)]
        sum_line = VGroup(*[S.text(t, 34, COUNT_COLOR if i == 8 else (S.WHITE if i in (1, 4, 6) else S.GREY))
                            for i, t in enumerate(sum_terms)]).arrange(RIGHT, buff=0.18).move_to([0, -3.05, 0])
        tags, wlines = {}, {}

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(card, run_time=0.5),
                      *[board_groups[k].animate.shift(up) for k in spots],
                      *[names[k].animate.shift(up) for k in spots], run_time=1.0)
            def add_each(k: str) -> list:
                """'edge' -> 'each edge' with no letter morphing: the word itself slides into place
                (same letters) and 'each' fades in in front of it."""
                tgt, n = new_names[k], len(new_names[k]) - len(names[k])     # n = glyphs of "each"
                assert tgt.text.replace(" ", "")[n:] == names[k].text
                return [ReplacementTransform(names[k], tgt[n:]), FadeIn(tgt[:n], shift=RIGHT * 0.15)]

            self.play(*add_each("edge"),
                      FadeIn(nums["edge"], shift=UP * 0.2), FadeIn(king, shift=DOWN * 0.4), run_time=1.0)
            self.add(new_names["edge"])                                 # one mobject again
            vo.wait_until("Each corner")
            self.play(*add_each("corner"), FadeIn(nums["corner"], shift=UP * 0.2), run_time=0.8)
            self.add(new_names["corner"])
            vo.wait_until("and the center the fewest")
            self.play(ReplacementTransform(names["center"], new_names["center"]),   # same word, just moves
                      FadeIn(nums["center"], shift=UP * 0.2), run_time=0.8)
            # the check-sum (not spoken) is written while this sentence is still going, and is gone
            # by "Why?" so it doesn't compete with the winning lines
            self.play(TransformFromCopy(nums["corner"][0], sum_line[1]),
                      TransformFromCopy(nums["edge"][0], sum_line[4]),
                      TransformFromCopy(nums["center"][0], sum_line[6]),
                      FadeIn(VGroup(sum_line[0], sum_line[2], sum_line[3], sum_line[5], sum_line[7])),
                      run_time=1.2)
            self.play(Write(sum_line[8]), run_time=0.6)

            vo.wait_until("Why?")
            self.play(FadeOut(sum_line, shift=DOWN * 0.2),
                      *[Indicate(xs_[k], color=S.WHITE, scale_factor=1.25) for k in spots],   # each in place
                      run_time=0.8)
            for k, anchor, n in (("center", "The center sits", 4), ("corner", "a corner on 3", 3),
                                 ("edge", "an edge on just 2", 2)):
                vo.wait_until(anchor)
                b = boards[k]
                wlines[k] = VGroup(*[b.win_line(ln[0], ln[2], stroke=7) for ln in WIN_LINES if spots[k] in ln]) \
                    .set_z_index(1)
                xs_[k].set_z_index(2)                # X's mark stays on top of its lines
                assert len(wlines[k]) == n
                tags[k] = S.text(f"on {n} winning lines", 26, WIN_COLOR).next_to(nums[k], DOWN, buff=0.2)
                self.play(LaggedStart(*[Create(w) for w in wlines[k]], lag_ratio=0.25),
                          FadeIn(tags[k], shift=UP * 0.15), run_time=0.9)

            # early wins chop whole branches off the tree
            vo.wait_until("More lines give X")
            nodes, dots, lines = mini_tree(center_x=-0.4, top=-1.9)
            tree = VGroup(*lines.values(), *dots.values())
            self.play(Indicate(wlines["center"], color=WIN_COLOR, scale_factor=1.06),
                      FadeIn(tree, lag_ratio=0.02), run_time=1.2)
            vo.wait_until("and every early win")
            win_key = (2,)
            win_ring = Circle(radius=0.16, color=WIN_COLOR, stroke_width=5).move_to(nodes[win_key])
            early = S.text("early win", 24, WIN_COLOR).next_to(win_ring, RIGHT, buff=0.2)
            sub = [key for key in nodes if len(key) > 1 and key[0] == win_key[0]]
            sub_parts = VGroup(*[dots[k] for k in sub], *[lines[k] for k in sub])
            wx, wy = nodes[win_key][:2]
            cut = Line([wx - 0.8, wy - 0.15, 0], [wx + 0.8, wy - 0.38, 0], color=UNDO_COLOR, stroke_width=7)
            self.play(Create(win_ring), dots[win_key].animate.set_color(WIN_COLOR),
                      FadeIn(early, shift=LEFT * 0.15), run_time=0.7)
            self.play(Create(cut), run_time=0.5)
            self.play(sub_parts.animate.set_opacity(0.15).shift(DOWN * 0.15), FadeOut(cut), run_time=0.8)
            self.play(FadeOut(sub_parts), run_time=0.5)

        # ================================================================ 7. more games is not a better move
        caution = caution_sign().move_to(king)
        ROW = {"center": 1.5, "edge": -1.5}            # y of each row's bar (gap leaves room for the sign)
        BAR_L, BAR_LEN = -3.6, 9.4
        row_board_target = {}
        for k in ("center", "edge"):
            tgt = board_groups[k].copy().scale(0.8)
            tgt.move_to([-5.15, ROW[k] + 0.15, 0])
            row_board_target[k] = tgt
        caution_target = caution.copy().scale(0.75).next_to(row_board_target["edge"], UP, buff=0.12)
        rows = {}
        for k, data, text in (("center", CENTER, "start in the center: X wins about 6 in 10 games"),
                              ("edge", EDGE, "start on an edge: X wins fewer than half")):
            n = sum(data.values())
            segs, x = VGroup(), BAR_L
            for key, c in (("X", X_COLOR), ("O", O_COLOR), ("D", DRAW_COLOR)):
                w = BAR_LEN * data[key] / n
                segs.add(Rectangle(width=w, height=0.62, stroke_width=0).set_fill(c, 1)
                         .move_to([x + w / 2, ROW[k], 0]))
                x += w
            inner = VGroup(S.text(f"X wins {fmt(data['X'])} of {fmt(n)}", 24, S.BG, weight=BOLD)
                           .move_to(segs[0]).align_to(segs[0], LEFT).shift(RIGHT * 0.25),
                           S.text("O wins", 24, S.BG).move_to(segs[1]),
                           S.text("draws", 24, S.BG).move_to(segs[2]))
            label = S.text(text, 28, S.WHITE).next_to(segs, UP, buff=0.24).align_to(segs, LEFT)
            rows[k] = (segs, inner, label)
        half_x = BAR_L + BAR_LEN / 2
        halves = VGroup(*[DashedLine([half_x, ROW[k] + 0.42, 0], [half_x, ROW[k] - 0.42, 0], color=S.WHITE,
                                     stroke_width=4, dash_length=0.1) for k in ROW])
        half_word = S.text("half", 26, S.WHITE).next_to(halves[0], DOWN, buff=0.12)
        half_word_low = half_word.copy().next_to(halves[1], DOWN, buff=0.12)

        with self.voiceover(SAY[6]) as vo:
            self.play(ReplacementTransform(king, caution), run_time=0.8)
            leave = VGroup(board_groups["corner"], new_names["corner"], nums["corner"], tags["corner"],
                           wlines["corner"], new_names["edge"], nums["edge"], tags["edge"], new_names["center"],
                           nums["center"], tags["center"], tree, win_ring, early, wlines["center"],
                           wlines["edge"])
            self.play(FadeOut(leave, run_time=0.6),
                      *[board_groups[k].animate.scale(0.8).move_to(row_board_target[k]) for k in ("center", "edge")],
                      caution.animate.scale(0.75).move_to(caution_target), run_time=1.1)
            vo.wait_until("Out of all")
            segs, inner, label = rows["center"]
            self.play(FadeIn(label, shift=RIGHT * 0.2), run_time=0.5)
            self.play(LaggedStart(*[GrowFromEdge(s, LEFT) for s in segs], lag_ratio=0.6), run_time=1.2)
            self.play(FadeIn(inner), Create(halves[0]), FadeIn(half_word), run_time=0.6)
            vo.wait_until("Starting on an edge")
            segs, inner, label = rows["edge"]
            self.play(FadeIn(label, shift=RIGHT * 0.2), run_time=0.5)
            self.play(LaggedStart(*[GrowFromEdge(s, LEFT) for s in segs], lag_ratio=0.6), run_time=1.2)
            self.play(FadeIn(inner), Create(halves[1]), half_word.animate.move_to(half_word_low), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
