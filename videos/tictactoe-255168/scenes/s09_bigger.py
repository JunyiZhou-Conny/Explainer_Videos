"""S09 · Bigger games, and your turn (the last scene of the video).

Beats
1. "X always wins?" gets a RED ✗ on "No.", and the question later makes way for the answer.
   A REAL position (X to move, 6 marks placed) whose whole subtree is small: 6 finished games.
   The leaves keep their result colours; the colours bubble up level by level (at X's turn the
   best result for X, at O's turn the best for O) and the root ends GREY: perfect play -> draw.
   Everything shown is computed below from the rules (and the empty board is checked to be a draw).
2. Chess is far too big: digit strips drawn to scale, one box per digit
   (255,168: 6 boxes · atoms in the observable universe: 81 · chess games (Shannon 1950): 121).
3. Chess programs look a few moves ahead in a huge tree and estimate who's winning.
4. Recap cards.  5. Challenge cards, then everything fades out.
"""

from functools import lru_cache

import numpy as np
from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (COUNT_COLOR, DRAW_COLOR, NARRATION, NINE_FACTORIAL, O_COLOR, TOTAL_GAMES,
                    UNDO_COLOR, WIN_LINES, X_COLOR, Board, mark_anim, mini_board, move_number,
                    winner)

SAY = NARRATION["S09"]

RESULT_COLOR = {"X": X_COLOR, "O": O_COLOR, "D": DRAW_COLOR}
PREFER = {"X": "XDO", "O": "ODX"}           # each player's results, best first


# ====================================================================== the rules: minimax
def other(p: str) -> str:
    return "O" if p == "X" else "X"


def play(cells: str, square: int, player: str) -> str:
    return cells[:square] + player + cells[square + 1:]


@lru_cache(maxsize=None)
def perfect_play(cells: str, player: str) -> str:
    """Result ('X', 'O' or 'D') if both players play perfectly from here."""
    w = winner(cells)
    if w is not None:
        return w
    if "." not in cells:
        return "D"
    results = [perfect_play(play(cells, s, player), other(player)) for s in range(9) if cells[s] == "."]
    return min(results, key=PREFER[player].index)


def game_tree(cells: str, player: str, move=None) -> dict:
    """The whole subtree below `cells` (player to move), with minimax results."""
    node = {"cells": cells, "player": player, "move": move, "kids": [], "line": None}
    w = winner(cells)
    if w is not None or "." not in cells:
        node["result"] = w or "D"
        for a, b, c in WIN_LINES:
            if cells[a] != "." and cells[a] == cells[b] == cells[c]:
                node["line"] = (a, c)
        return node
    node["kids"] = [game_tree(play(cells, s, player), other(player), s)
                    for s in range(9) if cells[s] == "."]
    node["best"] = min(node["kids"], key=lambda k: PREFER[player].index(k["result"]))
    node["result"] = node["best"]["result"]
    return node


def tree_levels(tree: dict) -> list:
    rows, row = [], [tree]
    while row:
        rows.append(row)
        row = [k for n in row for k in n["kids"]]
    return rows


# X O X / . O O / . X .   X to move (move 7): O threatens the middle row, so X must block.
ROOT_CELLS = "XOX.OO.X."
TREE = game_tree(ROOT_CELLS, "X")
LEVELS = tree_levels(TREE)
LEAVES = [n for row in LEVELS for n in row if not n["kids"]]
assert ROOT_CELLS.count("X") == ROOT_CELLS.count("O") == 3 and winner(ROOT_CELLS) is None
assert TREE["result"] == "D" == perfect_play(ROOT_CELLS, "X")
assert len(LEAVES) == 6 and {n["result"] for n in LEAVES} == {"X", "O", "D"}
assert [len(r) for r in LEVELS] == [1, 3, 6, 4]
assert perfect_play("." * 9, "X") == "D"          # the full game: perfect play is a draw


def legal_game(moves) -> str:
    """Final cells of a game [(square, symbol), ...]; asserts nobody won before the last move."""
    cells = "." * 9
    for k, (s, sym) in enumerate(moves):
        assert cells[s] == "." and sym == "XO"[k % 2] and winner(cells) is None
        cells = play(cells, s, sym)
    return cells


GAME_STOPS = [(0, "X"), (4, "O"), (1, "X"), (8, "O"), (2, "X")]                 # S03's game
GAME_X_WINS = [(0, "X"), (1, "O"), (4, "X"), (2, "O"), (8, "X")]
GAME_MOVE7 = [(0, "X"), (4, "O"), (8, "X"), (2, "O"), (6, "X"), (3, "O"), (7, "X")]
assert winner(legal_game(GAME_STOPS)) == "X" and winner(legal_game(GAME_X_WINS)) == "X"
assert winner(legal_game(GAME_MOVE7)) == "X"


# ====================================================================== beat 1: drawing the tree
ROW_Y = [2.75, 1.2, -0.35, -1.9]
TREE_DX = 0.6
NODE = 0.82                                      # mini-board size
FRAME = NODE + 0.26
LABEL_X = -5.62


def tint(color: str, alpha: float = 0.24) -> ManimColor:
    return ManimColor(S.BG).interpolate(ManimColor(color), alpha)


def result_frame_anim(frame, result: str, width: float = 4):
    c = RESULT_COLOR[result]
    return frame.animate.set_stroke(c, width).set_fill(tint(c), 1)


def layout_tree():
    TREE["pos"] = np.array([TREE_DX, ROW_Y[0], 0])
    for kid, x in zip(TREE["kids"], (-3.6, 0.0, 3.6)):
        kid["pos"] = np.array([x + TREE_DX, ROW_Y[1], 0])
        for g, dx in zip(kid["kids"], (-0.85, 0.85)):
            g["pos"] = np.array([kid["pos"][0] + dx, ROW_Y[2], 0])
            for leaf in g["kids"]:
                leaf["pos"] = np.array([g["pos"][0], ROW_Y[3], 0])


def build_node(node: dict, parent: dict | None):
    frame = RoundedRectangle(width=FRAME, height=FRAME, corner_radius=0.1)
    frame.set_stroke(S.GREY_DARK, 2).set_fill(S.BG, 1)
    mb = mini_board(node["cells"], size=NODE, stroke=3)
    mob = VGroup(frame)
    if node["move"] is not None:            # the square just played: a faint highlight
        mob.add(mb.board.square(node["move"], color=S.WHITE, opacity=0.16))
    mob.add(mb)
    mob.move_to(node["pos"])
    node.update(mob=mob, frame=frame, board=mb.board)
    node["win"] = mb.board.win_line(*node["line"], stroke=4) if node["line"] else None
    if parent is not None:
        node["edge"] = Line(parent["frame"].get_bottom(), frame.get_top()) \
            .set_stroke(S.WHITE, 2.5, opacity=0.35)


def swatch(result: str, label: str) -> VGroup:
    c = RESULT_COLOR[result]
    sq = RoundedRectangle(width=0.36, height=0.36, corner_radius=0.06).set_stroke(c, 3).set_fill(tint(c), 1)
    return VGroup(sq, S.text(label, 24, c)).arrange(RIGHT, buff=0.15)


# ====================================================================== beat 2: chess and digits
LIGHT_SQ, DARK_SQ = "#EAD7B4", "#A87C59"      # a wooden chessboard
CHESS_COLOR = LIGHT_SQ
ATOM_COLOR = S.PURPLE
PITCH, CELL_W, CELL_H = 0.085, 0.062, 0.3     # one box per digit, all strips to the same scale
STRIP_X0 = -5.05
ICON_X = -5.85
ICON_W = 0.85
ROW2_Y = {"ttt": 1.85, "atoms": 0.1, "chess": -1.65}


def glyph(ch: str, scale: float) -> VGroup:
    """A chess-piece glyph as plain shapes (an icon, not text)."""
    t = Text(ch, font="DejaVu Sans", font_size=48)
    return VGroup(*t.submobjects).scale(scale)


def chessboard(size: float) -> VGroup:
    q = size / 8
    squares = VGroup(*[Square(q, stroke_width=0).set_fill(LIGHT_SQ if (r + c) % 2 == 0 else DARK_SQ, 1)
                       .move_to([(c - 3.5) * q, (3.5 - r) * q, 0]) for r in range(8) for c in range(8)])
    k = q * 0.8 / Text("♚", font="DejaVu Sans", font_size=48).height
    pieces = VGroup()
    back = "♜♞♝♛♚♝♞♜"
    for r, glyphs, white in ((0, back, False), (1, "♟" * 8, False), (6, "♟" * 8, True), (7, back, True)):
        for c, ch in enumerate(glyphs):
            p = glyph(ch, k).move_to(squares[r * 8 + c])
            if white:
                p.set_fill("#FBFBFB", 1).set_stroke("#2A2A2A", 0.8)
            else:
                p.set_fill("#1B1B1B", 1).set_stroke(width=0)
            pieces.add(p)
    border = Square(size).set_stroke(S.WHITE, 2)
    return VGroup(squares, pieces, border)


def atom_icon(size: float = ICON_W, color: str = ATOM_COLOR) -> VGroup:
    orbits = VGroup(*[Ellipse(width=size, height=size * 0.34).set_stroke(color, 2.5).rotate(a)
                      for a in (0, PI / 3, 2 * PI / 3)])
    return VGroup(orbits, Dot(radius=size * 0.08, color=color))


def digit_strip(n: int, color: str, y: float) -> VGroup:
    return VGroup(*[Rectangle(width=CELL_W, height=CELL_H, stroke_width=0).set_fill(color, 1)
                    .move_to([STRIP_X0 + PITCH * (i + 0.5), y, 0]) for i in range(n)])


# ====================================================================== beat 3: a huge tree
ROOT3 = np.array([0, 2.95, 0])
TOP3 = np.array([0, 2.45, 0])
Y3 = [1.75, 0.55, -0.65, -1.5, -2.0]
GAUGE_R = 0.2


def segments(segs, width: float, opacity: float, color: str = S.WHITE) -> VMobject:
    """Many line segments as ONE cheap VMobject."""
    m = VMobject()
    for p, q in segs:
        m.start_new_path(p)
        m.add_line_to(q)
    return m.set_stroke(color, width, opacity)


def faint_tree(rng) -> tuple[VGroup, VGroup]:
    l1 = [np.array([x, Y3[0], 0]) for x in np.linspace(-6.0, 6.0, 21)]
    l2 = [np.array([x, Y3[1] + rng.uniform(-0.07, 0.07), 0]) for x in np.linspace(-6.3, 6.3, 105)]
    l3 = [np.array([x, Y3[2] + rng.uniform(-0.08, 0.08), 0]) for x in np.linspace(-6.42, 6.42, 315)]
    l4 = [np.array([x, Y3[3] + rng.uniform(-0.08, 0.08), 0]) for x in np.linspace(-6.5, 6.5, 630)]
    l5 = [p + np.array([rng.uniform(-0.06, 0.06), Y3[4] - Y3[3], 0]) for p in l4]
    levels = VGroup(
        segments([(TOP3, p) for p in l1], 2, 0.42),
        segments([(l1[i // 5], p) for i, p in enumerate(l2)], 1.6, 0.3),
        segments([(l2[i // 3], p) for i, p in enumerate(l3)], 1.2, 0.2),
        segments([(l3[i // 2], p) for i, p in enumerate(l4)], 1.0, 0.13),
        segments(list(zip(l4, l5)), 1.0, 0.07),
    )
    dots = VGroup(*[Dot(p, radius=0.045, color=S.WHITE).set_opacity(0.5) for p in l1])
    return levels, dots


def gauge(center) -> VGroup:
    """A tiny 'who's winning?' dial: white side vs black side, with a GOLD needle (starts upright)."""
    white = AnnularSector(inner_radius=0, outer_radius=GAUGE_R, angle=PI / 2, start_angle=PI / 2,
                          color="#F2F2F2", fill_opacity=1)
    black = AnnularSector(inner_radius=0, outer_radius=GAUGE_R, angle=PI / 2, start_angle=0,
                          color="#1E1E1E", fill_opacity=1)
    rim = Arc(radius=GAUGE_R, start_angle=0, angle=PI).set_stroke(S.WHITE, 2)
    base = Line(LEFT * GAUGE_R, RIGHT * GAUGE_R).set_stroke(S.WHITE, 2)
    needle = Line(ORIGIN, UP * GAUGE_R * 0.95).set_stroke(S.GOLD, 4)
    hub = Dot(radius=0.035, color=S.GOLD)
    g = VGroup(white, black, rim, base, needle, hub).shift(center)
    g.needle, g.pivot = needle, np.array(center, dtype=float)
    return g


# ====================================================================== beats 4-5: cards
CARD_W, CARD_H, CARD_Y = 4.1, 4.0, -0.15     # recap and challenge cards share size and place
CARD_X = (-4.3, 0.0, 4.3)


def card_frame(x: float, y: float, h: float, stroke: str = S.GREY_DARK, width: float = 2) -> RoundedRectangle:
    return RoundedRectangle(width=CARD_W, height=h, corner_radius=0.2).set_stroke(stroke, width) \
        .set_fill(S.GREY_DARKER, 1).move_to([x, y, 0])


def card_text(lines, top: float, x: float, size: float = 26, buff: float = 0.18) -> VGroup:
    """Lines (Text mobjects or (string, colour) / string) stacked, centred on x, top edge at `top`."""
    ms = VGroup(*[ln if isinstance(ln, Mobject) else
                  S.text(ln[0], size, ln[1]) if isinstance(ln, tuple) else S.text(ln, size)
                  for ln in lines])
    return ms.arrange(DOWN, buff=buff).move_to([x, 0, 0]).align_to([0, top, 0], UP)


def pulse(m, k: float = 1.15):
    """Grow and shrink back (an Indicate that keeps the colours)."""
    return m.animate(rate_func=there_and_back).scale(k)


def shake(m, amp: float = 0.2, n: int = 3):
    """A quick side-to-side 'no' shake that ends where it started."""
    return m.animate(rate_func=lambda t: np.sin(n * TAU * t) * (1 - t)).shift(RIGHT * amp)


def place_game(board: Board, moves, numbers: bool = False, scale: float = 0.5, num_size: float = 20):
    """Marks (and optional move numbers) of a game on `board`, not yet added. Returns list of VGroups."""
    out = []
    for n, (i, sym) in enumerate(moves, start=1):
        g = VGroup(board.mark_at(i, sym, scale=scale))
        if numbers:
            g.add(move_number(board, i, n, sym, size=num_size))
        out.append(g)
    return out


class Bigger(VoiceScene):
    def construct(self):
        self.solved_tree()
        self.chess_numbers()
        self.chess_programs()
        self.recap()
        self.your_turn()

    # ------------------------------------------------------------------ beat 1: solved!
    def bubble(self, parents, flow_time: float, pick_time: float, extra=()):
        """Each kid's colour flows up its edge; the parent keeps the best one for the player to move."""
        flows = []
        for n in parents:
            n["flows"] = []
            for k in n["kids"]:
                ln = Line(k["frame"].get_top(), n["frame"].get_bottom()) \
                    .set_stroke(RESULT_COLOR[k["result"]], 5)
                n["flows"].append((k, ln))
                flows.append(Create(ln))
        self.play(*flows, run_time=flow_time)
        picks = []
        for n in parents:
            for k, ln in n["flows"]:
                picks.append(ln.animate.set_stroke(width=7) if k is n["best"]
                             else ln.animate.set_stroke(width=3, opacity=0.3))
            picks.append(result_frame_anim(n["frame"], n["result"]))
        self.play(*picks, *extra, run_time=pick_time)

    def solved_tree(self):
        layout_tree()
        for depth, row in enumerate(LEVELS):
            for n in row:
                parent = None if depth == 0 else next(p for p in LEVELS[depth - 1] if n in p["kids"])
                build_node(n, parent)

        row_labels = VGroup(*[S.text(f"{p} to move", 26, S.WHITE, t2c={p: RESULT_COLOR[p]})
                              .move_to([LABEL_X, y, 0]) for p, y in zip("XOX", ROW_Y)])   # as in S06
        best_labels = {d: S.text(f"best for {p}", 24, S.WHITE).next_to(row_labels[d], DOWN, buff=0.16)
                       for d, p in ((0, "X"), (1, "O"))}
        legend = VGroup(swatch("X", "X wins"), swatch("O", "O wins"), swatch("D", "draw")) \
            .arrange(RIGHT, buff=0.5).move_to([0, -3.15, 0]).align_to([-6.3, 0, 0], LEFT)
        caption = S.text("perfect play → draw", 34, S.WHITE, t2c={"draw": DRAW_COLOR})
        caption.next_to(TREE["frame"], RIGHT, buff=0.45).align_to(TREE["frame"], UP).shift(DOWN * 0.02)
        # the opening question sits where its answer (the caption) will appear
        question = S.text("X always wins?", 34, S.WHITE, t2c={"X": X_COLOR})
        no_cross = S.text("✗", 44, S.RED, font="DejaVu Sans")
        ask = VGroup(question, no_cross).arrange(RIGHT, buff=0.3)
        ask.next_to(TREE["frame"], RIGHT, buff=0.45).align_to(caption, LEFT).match_y(caption)
        empty = mini_board(size=0.5, stroke=2)
        empty_frame = RoundedRectangle(width=0.66, height=0.66, corner_radius=0.07) \
            .set_stroke(DRAW_COLOR, 3).set_fill(tint(DRAW_COLOR), 1)
        note = VGroup(S.text("the same on the full tree:", 24, S.WHITE), VGroup(empty_frame, empty),
                      S.text("→ draw", 24, DRAW_COLOR)).arrange(RIGHT, buff=0.15)
        note.move_to([0, -3.15, 0]).align_to([6.35, 0, 0], RIGHT)

        path = [TREE]
        while path[-1]["kids"]:
            path.append(path[-1]["best"])

        with self.voiceover(SAY[0]) as vo:
            # "So does going first mean X always wins?" while the tree grows
            self.play(FadeIn(TREE["mob"], scale=0.9), FadeIn(row_labels[0], shift=RIGHT * 0.2),
                      FadeIn(question, shift=DOWN * 0.15), run_time=0.6)
            for d in (1, 2, 3):
                grow = [AnimationGroup(Create(n["edge"]), FadeIn(n["mob"], shift=DOWN * 0.15))
                        for n in LEVELS[d]]
                extra = [FadeIn(row_labels[d], shift=RIGHT * 0.2)] if d < 3 else []
                self.play(LaggedStart(*grow, lag_ratio=0.12), *extra, run_time=0.75)

            # "No."
            vo.wait_until("No.")
            self.play(FadeIn(no_cross, scale=1.8), shake(question, 0.12), run_time=0.5)

            # every finished game shows its real result (the answered question steps back)
            vo.wait_until("A computer can")
            self.play(*[result_frame_anim(n["frame"], n["result"]) for n in LEAVES],
                      *[Create(n["win"]) for n in LEAVES if n["win"] is not None],
                      FadeIn(legend, shift=UP * 0.2), ask.animate.set_opacity(0.45), run_time=1.0)

            # colours bubble up: X's forced last moves, then O's choices, then X's choice
            vo.wait_until("By finding the best")
            self.bubble([n for n in LEVELS[2] if n["kids"]], 0.5, 0.4,
                        extra=[Indicate(row_labels[2], color=X_COLOR, scale_factor=1.1)])
            self.bubble(LEVELS[1], 0.6, 0.7, extra=[FadeIn(best_labels[1], shift=DOWN * 0.1)])
            self.bubble(LEVELS[0], 0.6, 0.7, extra=[FadeIn(best_labels[0], shift=DOWN * 0.1)])

            # perfect play: follow the best move at every level
            vo.wait_until("if both players")
            flashes = [ShowPassingFlash(Line(a["frame"].get_bottom(), b["frame"].get_top())
                                        .set_stroke(S.WHITE, 10), time_width=1.0, run_time=0.45)
                       for a, b in zip(path, path[1:])]
            self.play(Succession(*flashes), run_time=1.35)
            self.play(*[n["frame"].animate.set_stroke(width=7) for n in path], run_time=0.4)

            vo.wait_until("every game ends")
            self.play(FadeOut(ask, shift=UP * 0.25), Write(caption), run_time=0.8)
            self.play(FadeIn(note, shift=UP * 0.15), run_time=0.6)
        self.wait(1.2)                       # time to read the note before the chess beat

    # ------------------------------------------------------------------ beat 2: chess is huge
    def chess_numbers(self):
        board = chessboard(3.2).move_to(UP * 0.1)
        icon_pos = {k: np.array([ICON_X, y, 0]) for k, y in ROW2_Y.items()}

        def row_label(s, key, **kw):
            return S.text(s, 26, S.WHITE, **kw).next_to([STRIP_X0, ROW2_Y[key] + 0.3, 0], RIGHT, buff=0)

        ttt_icon = mini_board("X...O...X", size=0.7, stroke=2).move_to(icon_pos["ttt"])
        ttt_label = row_label("tic-tac-toe: 255,168 (6 digits)", "ttt", t2c={"255,168": COUNT_COLOR})
        ttt_cells = digit_strip(6, COUNT_COLOR, ROW2_Y["ttt"] - 0.2)

        chess_label = row_label("chess: at least 1 followed by 120 zeros (Shannon, 1950)", "chess")
        chess_cells = digit_strip(121, CHESS_COLOR, ROW2_Y["chess"] - 0.2)
        chess_tag = S.math("10^{120}", size=40).next_to(chess_cells, RIGHT, buff=0.15)
        brace = Brace(VGroup(*chess_cells[1:]), DOWN, buff=0.08, color=S.WHITE)
        brace_lab = S.text("120 zeros", 24, S.WHITE).next_to(brace, DOWN, buff=0.08)
        one_lab = S.text("1", 24, S.WHITE).next_to(chess_cells[0], DOWN, buff=0.12).shift(LEFT * 0.05)

        a_icon = atom_icon().move_to(icon_pos["atoms"])
        a_label = row_label("atoms in the observable universe: about 1 followed by 80 zeros", "atoms")
        a_cells = digit_strip(81, ATOM_COLOR, ROW2_Y["atoms"] - 0.2)
        a_tag = S.math("10^{80}", size=40).next_to(a_cells, RIGHT, buff=0.15)

        key_cell = Rectangle(width=CELL_W, height=CELL_H, stroke_width=0).set_fill(S.WHITE, 1)
        header = VGroup(key_cell, S.text("= one digit", 24, S.GREY)).arrange(RIGHT, buff=0.15)
        header.move_to([0, 3.2, 0]).align_to([STRIP_X0, 0, 0], LEFT)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(Group(*self.mobjects), shift=UP * 0.3), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(s) for s in board[0]], lag_ratio=0.015), Create(board[2]),
                      run_time=0.6)
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.1) for p in board[1]], lag_ratio=0.02),
                      run_time=0.5)
            self.remove(*board.get_family()[1:])          # from now on the board moves as one piece
            self.add(board)

            # "Not a chance": the board shakes its head, then becomes the icon of its row;
            # tic-tac-toe's number for comparison
            vo.wait_until("Not a chance")
            self.play(shake(board), run_time=0.7)
            self.play(board.animate.scale_to_fit_width(ICON_W).move_to(icon_pos["chess"]),
                      FadeIn(ttt_icon), FadeIn(ttt_label, shift=RIGHT * 0.2), FadeIn(header),
                      run_time=1.0)
            self.play(LaggedStart(*[GrowFromEdge(c, DOWN) for c in ttt_cells], lag_ratio=0.3), run_time=0.5)

            vo.wait_until("In 1950")
            self.play(Write(chess_label), run_time=1.4)
            vo.wait_until("Claude Shannon")
            self.play(LaggedStart(*[GrowFromEdge(c, DOWN) for c in chess_cells], lag_ratio=0.2),
                      run_time=max(1.5, vo.until("at least 10")))
            self.play(Write(chess_tag), pulse(board, 1.15), run_time=0.8)

            vo.wait_until("That's a 1")
            self.play(chess_cells[0].animate.set_fill(S.WHITE), FadeIn(one_lab, shift=UP * 0.1), run_time=0.5)
            self.play(GrowFromCenter(brace), FadeIn(brace_lab, shift=UP * 0.1), run_time=0.8)

            vo.wait_until("The whole observable")
            self.play(FadeIn(a_icon, scale=0.6), FadeIn(a_label, shift=RIGHT * 0.2), run_time=0.7)
            self.play(LaggedStart(*[GrowFromEdge(c, DOWN) for c in a_cells], lag_ratio=0.2), run_time=1.6)
            self.play(Write(a_tag), Rotate(a_icon[0], PI / 3), a_cells[0].animate.set_fill(S.WHITE),
                      run_time=0.8)
            self.play(Indicate(chess_tag, color=CHESS_COLOR), run_time=min(1.0, vo.remaining()))
        self.chess_icon = board

    # ------------------------------------------------------------------ beat 3: look ahead + estimate
    def chess_programs(self):
        rng = np.random.default_rng(9)
        icon = self.chess_icon
        faint, faint_dots = faint_tree(rng)

        # the explored part: 3 first moves, 2 replies each, 2 more moves each (cut-off at depth 3)
        e1 = [np.array([x, Y3[0], 0]) for x in (-4.2, 0.0, 4.2)]
        e2 = [p + np.array([dx, Y3[1] - Y3[0], 0]) for p in e1 for dx in (-0.75, 0.75)]
        e3 = [p + np.array([dx, Y3[2] - Y3[1], 0]) for p in e2 for dx in (-0.35, 0.35)]
        top_of = lambda p: p + UP * GAUGE_R                                   # noqa: E731
        edges = [VGroup(*[Line(TOP3, p) for p in e1]),
                 VGroup(*[Line(e1[i // 2], p) for i, p in enumerate(e2)]),
                 VGroup(*[Line(e2[i // 2], top_of(p)) for i, p in enumerate(e3)])]
        for g in edges:
            g.set_stroke(S.WHITE, 3)
        nodes = [VGroup(*[Dot(p, radius=0.065, color=S.WHITE) for p in e1]),
                 VGroup(*[Dot(p, radius=0.065, color=S.WHITE) for p in e2])]
        gauges = [gauge(p) for p in e3]
        angles = rng.uniform(-1.25, 1.25, len(gauges))
        gauge_label = S.text("≈ who's winning?", 24, S.GOLD)
        gauge_label.move_to([0, Y3[2] - 0.62, 0])
        backing = BackgroundRectangle(gauge_label, color=S.BG, fill_opacity=0.9, buff=0.08)
        cap1 = S.text("look a few moves ahead + estimate who's winning", 30, S.WHITE)
        cap2 = S.text("(learned from millions of practice games)", 26, S.GREY)
        caption = VGroup(cap1, cap2).arrange(DOWN, buff=0.14).move_to([0, -2.95, 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(Group(*[m for m in self.mobjects if m is not icon])),
                      icon.animate.scale_to_fit_width(0.95).move_to(ROOT3), run_time=0.9)
            self.play(LaggedStart(FadeIn(faint[0]), FadeIn(faint_dots), FadeIn(faint[1]), FadeIn(faint[2]),
                                  FadeIn(faint[3]), FadeIn(faint[4]), lag_ratio=0.4), run_time=2.0)

            vo.wait_until("They look only")
            self.play(Create(edges[0]), FadeIn(nodes[0]), run_time=0.5)
            self.play(Create(edges[1]), FadeIn(nodes[1]), run_time=0.5)
            self.play(Create(edges[2]), LaggedStart(*[FadeIn(g, scale=0.5) for g in gauges], lag_ratio=0.06),
                      run_time=0.7)

            vo.wait_until("then estimate")
            self.play(*[Rotate(g.needle, a, about_point=g.pivot) for g, a in zip(gauges, angles)],
                      FadeIn(backing), FadeIn(gauge_label, shift=UP * 0.1), FadeIn(cap1, shift=UP * 0.15),
                      run_time=1.2)
            vo.wait_until("using what they")
            nudges = rng.uniform(-0.35, 0.35, len(gauges))
            self.play(*[Rotate(g.needle, a, about_point=g.pivot) for g, a in zip(gauges, nudges)],
                      FadeIn(cap2, shift=UP * 0.15), run_time=1.0)

            # the same idea: walk down one branch, back up (undo), down the next
            vo.wait_until("But underneath")
            walker = Dot(TOP3, radius=0.085, color=S.WHITE)
            self.play(FadeIn(walker, scale=0.5), run_time=0.3)
            A, B, C = e1, e2, [top_of(p) for p in e3]
            steps = [("down", TOP3, A[0]), ("down", A[0], B[0]), ("down", B[0], C[0]), ("look", 0),
                     ("up",), ("down", B[0], C[1]), ("look", 1),
                     ("up",), ("up",), ("down", A[0], B[1]), ("down", B[1], C[2]), ("look", 2),
                     ("up",), ("down", B[1], C[3]), ("look", 3),
                     ("up",), ("up",), ("up",), ("down", TOP3, A[1])]
            weight = {"down": 1.0, "up": 0.8, "look": 0.7}
            unit = max(0.12, (vo.remaining() - 0.3) / sum(weight[s[0]] for s in steps))
            trail = []
            for s in steps:
                rt = weight[s[0]] * unit
                if s[0] == "down":
                    seg = Line(s[1], s[2]).set_stroke(S.WHITE, 8)
                    self.play(Create(seg), MoveAlongPath(walker, Line(s[1], s[2])), run_time=rt)
                    trail.append(seg)
                elif s[0] == "up":
                    seg = trail.pop().set_stroke(UNDO_COLOR)
                    self.play(Uncreate(seg), MoveAlongPath(walker, Line(seg.get_end(), seg.get_start())),
                              run_time=rt)
                else:
                    g = gauges[s[1]]
                    self.play(pulse(g, 1.4), run_time=rt)
        self.wait(0.3)

    # ------------------------------------------------------------------ beat 4: recap
    def recap(self):
        title = S.text("Recap", 48).move_to([0, 2.85, 0])
        Y = CARD_Y
        frames = VGroup(*[card_frame(x, Y, CARD_H) for x in CARD_X])
        pic_y, text_y = Y + 0.95, Y - 0.38

        # card 1: choices multiply (a fan: 9 first moves, 8 replies under each)
        x1 = CARD_X[0] + 0.15
        root = np.array([x1, Y + 1.62, 0])
        l1 = [np.array([x1 + (i - 4) * 0.3, Y + 0.95, 0]) for i in range(9)]
        fan1 = VGroup(*[Line(root, p).set_stroke(X_COLOR, 3) for p in l1])
        fan2 = VGroup(*[Line(p, p + np.array([(j - 3.5) * 0.034, -0.72, 0])).set_stroke(O_COLOR, 1.6)
                        for p in l1 for j in range(8)])
        root_dot = Dot(root, radius=0.06, color=S.WHITE)
        lab9 = S.text("9", 26, X_COLOR).move_to([CARD_X[0] - 1.62, Y + 1.28, 0])
        lab8 = S.text("× 8", 26, O_COLOR).move_to([CARD_X[0] - 1.55, Y + 0.57, 0])
        text1 = card_text(["multiply choices", "→ nine factorial",
                           S.text(f"= {NINE_FACTORIAL:,}", 34, COUNT_COLOR)], text_y, CARD_X[0])

        # card 2: games stop early -> ghost games (S03's game: X wins on move 5)
        b2 = Board(size=1.55, stroke=4).move_to([CARD_X[1], pic_y, 0])
        marks2 = place_game(b2, GAME_STOPS, scale=0.55)
        line2 = b2.win_line(0, 2, stroke=6)
        final2 = legal_game(GAME_STOPS)
        empties = [i for i in range(9) if final2[i] == "."]
        ghosts2 = VGroup(*[b2.ghost_at(i, "OXOX"[k], scale=0.55) for k, i in enumerate(empties)])
        text2 = card_text(["games stop early", S.text("→ ghost games", 26, S.WHITE, t2c={"ghost games": S.GREY})],
                          text_y, CARD_X[1])

        # card 3: try -> explore -> undo (a small tree walked by the program)
        x3 = CARD_X[2]
        t0 = np.array([x3, Y + 1.62, 0])
        t1 = [np.array([x3 + dx, Y + 0.95, 0]) for dx in (-0.95, 0, 0.95)]
        t2 = [p + np.array([dx, -0.7, 0]) for p in t1 for dx in (-0.3, 0.3)]
        tree3 = VGroup(*[Line(t0, p) for p in t1], *[Line(t1[i // 2], p) for i, p in enumerate(t2)]) \
            .set_stroke(S.WHITE, 2.5, opacity=0.45)
        dots3 = VGroup(*[Dot(p, radius=0.06, color=S.WHITE) for p in [t0, *t1, *t2]])
        text3 = card_text([S.text("try → explore → undo", 26, S.WHITE, t2c={"undo": UNDO_COLOR}),
                           S.text(f"→ {TOTAL_GAMES:,}", 34, COUNT_COLOR)], text_y, x3)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
            self.play(Write(title), run_time=0.6)

            vo.wait_until("Multiplying the choices")
            self.play(FadeIn(frames[0], scale=0.95), FadeIn(root_dot), run_time=0.5)
            self.play(LaggedStart(*[Create(ln) for ln in fan1], lag_ratio=0.1), FadeIn(lab9), run_time=0.8)
            self.play(LaggedStart(*[Create(ln) for ln in fan2], lag_ratio=0.01), FadeIn(lab8), run_time=0.9)
            self.play(FadeIn(text1[0], shift=UP * 0.15), run_time=0.5)
            vo.wait_until("gives nine factorial")
            self.play(FadeIn(text1[1], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("362,880 orders")
            self.play(Write(text1[2]), run_time=0.8)

            vo.wait_until("But games stop")
            self.play(FadeIn(frames[1], scale=0.95), Create(b2), run_time=0.5)
            self.play(LaggedStart(*[mark_anim(m[0]) for m in marks2], lag_ratio=0.5), run_time=1.2)
            self.play(Create(line2), FadeIn(text2[0], shift=UP * 0.15), run_time=0.5)
            vo.wait_until("ghost games")
            self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in ghosts2], lag_ratio=0.2),
                      FadeIn(text2[1], shift=UP * 0.15), run_time=0.9)

            vo.wait_until("And a short")
            self.play(FadeIn(frames[2], scale=0.95), Create(tree3), FadeIn(dots3), run_time=0.8)
            walk = Dot(t0, radius=0.09, color=S.WHITE)
            self.play(FadeIn(walk, scale=0.5), run_time=0.3)
            vo.wait_until("by trying a move")
            down1 = Line(t0, t1[0]).set_stroke(S.WHITE, 7)
            down2 = Line(t1[0], t2[0]).set_stroke(S.WHITE, 7)
            self.play(Create(down1), MoveAlongPath(walk, Line(t0, t1[0])),
                      FadeIn(text3[0], shift=UP * 0.15), run_time=0.5)
            self.play(Create(down2), MoveAlongPath(walk, Line(t1[0], t2[0])), run_time=0.5)
            self.play(Flash(t2[0], color=COUNT_COLOR, line_length=0.15, flash_radius=0.15), run_time=0.4)
            vo.wait_until("and undoing it")
            self.play(Uncreate(down2.set_stroke(UNDO_COLOR)), MoveAlongPath(walk, Line(t2[0], t1[0])), run_time=0.5)
            down3 = Line(t1[0], t2[1]).set_stroke(S.WHITE, 7)
            self.play(Create(down3), MoveAlongPath(walk, Line(t1[0], t2[1])), run_time=0.5)

            vo.wait_until("The answer is")
            self.play(Write(text3[1]), run_time=0.9)
            self.play(Circumscribe(text3[1], color=COUNT_COLOR), run_time=1.0)
            cards = [VGroup(frames[0], root_dot, fan1, fan2, lab9, lab8, text1),
                     VGroup(frames[1], b2, *marks2, line2, ghosts2, text2),
                     VGroup(frames[2], tree3, dots3, down1, down3, walk, text3)]
            pulses = LaggedStart(*[pulse(c, 1.04) for c in cards], lag_ratio=0.3)
            self.play(pulses, run_time=min(1.5, vo.remaining()))
            # Drop the temporary wrapper the LaggedStart added (it holds the frames we keep). Scene.remove
            # takes the wrapper's whole family with it, so put the cards' pieces back one by one.
            self.remove(pulses.mobject)
            self.add(*[m for c in cards for m in c])
        self.recap_title, self.recap_frames = title, frames

    # ------------------------------------------------------------------ beat 5: challenges
    def your_turn(self):
        title = S.text("Your turn!", 48, S.YELLOW).move_to([0, 2.85, 0])
        top = CARD_Y + CARD_H / 2                      # same top as the recap cards, a bit shorter
        frames = VGroup(*[card_frame(x, top - 1.85, 3.7, stroke=S.YELLOW, width=3) for x in CARD_X])
        pic_y, text_y = top - 1.12, top - 2.55
        boards = [Board(size=1.75, stroke=4).move_to([x, pic_y, 0]) for x in CARD_X]

        marks1 = place_game(boards[0], GAME_X_WINS, scale=0.55)
        line1 = boards[0].win_line(0, 8, stroke=6)
        text1 = card_text(["Count only X's wins"], text_y, CARD_X[0])

        marks2 = place_game(boards[1], GAME_MOVE7, numbers=True, scale=0.42, num_size=22)
        line2 = boards[1].win_line(6, 8, stroke=6)
        text2 = card_text(["Count the games", "that end on move 7"], text_y, CARD_X[1])

        marks3 = place_game(boards[2], [(4, "O")], numbers=True, scale=0.42, num_size=22)
        text3 = card_text(["What if O went first?"], text_y, CARD_X[2])

        footer = S.text("program + challenges: linked in the description", 28, S.WHITE).move_to([0, -2.8, 0])

        with self.voiceover(SAY[4]) as vo:
            old = Group(*[m for m in self.mobjects if m is not self.recap_title and m not in self.recap_frames])
            self.play(FadeOut(old, shift=UP * 0.2), run_time=0.6)
            self.play(FadeTransform(self.recap_title, title),
                      *[Transform(a, b) for a, b in zip(self.recap_frames, frames)], run_time=0.9)

            vo.wait_until("Change the program")
            self.play(Create(boards[0]), FadeIn(text1, shift=UP * 0.15), run_time=0.6)
            self.play(LaggedStart(*[mark_anim(m[0]) for m in marks1], lag_ratio=0.5), run_time=1.0)
            self.play(Create(line1), run_time=0.4)

            vo.wait_until("or only the games")
            self.play(Create(boards[1]), FadeIn(text2, shift=UP * 0.15), run_time=0.5)
            self.play(LaggedStart(*[AnimationGroup(mark_anim(m[0]), FadeIn(m[1], scale=0.6)) for m in marks2],
                                  lag_ratio=0.45), run_time=1.4)
            self.play(Create(line2), Indicate(marks2[-1][1], color=X_COLOR, scale_factor=1.6), run_time=0.5)

            vo.wait_until("or see what happens")
            self.play(Create(boards[2]), FadeIn(text3, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("if O goes")
            self.play(mark_anim(marks3[0][0]), FadeIn(marks3[0][1], scale=0.6), run_time=0.6)

            vo.wait_until("The program and")
            self.play(FadeIn(footer, shift=UP * 0.2), run_time=0.8)

            vo.wait_until("Have fun")
            cards = [VGroup(self.recap_frames[0], boards[0], *marks1, line1, text1),
                     VGroup(self.recap_frames[1], boards[1], *marks2, line2, text2),
                     VGroup(self.recap_frames[2], boards[2], *marks3, text3)]
            self.play(LaggedStart(*[pulse(c, 1.05) for c in cards], lag_ratio=0.25), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)
        self.wait(0.5)
