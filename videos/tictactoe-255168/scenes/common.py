"""Shared look for the tic-tac-toe video: semantic colours, the board, X/O marks, the program text.

Every scene draws boards, marks and code with these helpers, so the same object always looks the
same. See script.md for the colour table.
"""

from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Circle, Code, Line, Rectangle, RoundedRectangle,
                   VGroup, VMobject, DashedVMobject)

from explainer import style as S
from explainer.script import load_narration

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"

# ------------------------------------------------------------------ semantic colours
X_COLOR = S.BLUE
O_COLOR = S.ORANGE
WIN_COLOR = S.YELLOW       # the winning line
DRAW_COLOR = S.GREY        # draws
COUNT_COLOR = S.GREEN      # counts and totals
GHOST_COLOR = S.GREY       # moves that never get played (draw faded + dashed)
UNDO_COLOR = S.RED         # undo / erase / "too many"
GRID_COLOR = S.WHITE
INDEX_COLOR = S.GREY

NARRATION = load_narration(PROJECT / "script.md")

# ------------------------------------------------------------------ the rules (for computing)
WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a]


# Verified numbers (assets/verify_counts.py)
TOTAL_GAMES = 255_168
NINE_FACTORIAL = 362_880
BY_MOVE = {5: 1_440, 6: 5_328, 7: 47_952, 8: 72_576, 9: 127_872}
MOVE9_X_WINS, MOVE9_DRAWS = 81_792, 46_080
X_WINS, O_WINS, DRAWS = 131_184, 77_904, 46_080
FIRST_MOVE_GAMES = {"corner": 27_732, "edge": 29_592, "centre": 25_872}
ALIVE_AT_DEPTH = [1, 9, 72, 504, 3_024, 15_120, 54_720, 148_176, 200_448, 127_872]


# ------------------------------------------------------------------ marks
def x_mark(size: float = 0.6, color: str = X_COLOR, stroke: float = 8) -> VGroup:
    """An X drawn as two strokes, `size` wide."""
    h = size / 2
    return VGroup(Line([-h, -h, 0], [h, h, 0], color=color, stroke_width=stroke),
                  Line([-h, h, 0], [h, -h, 0], color=color, stroke_width=stroke))


def o_mark(size: float = 0.6, color: str = O_COLOR, stroke: float = 8) -> Circle:
    """An O drawn as a ring, `size` wide."""
    return Circle(radius=size / 2, color=color, stroke_width=stroke)


def mark(symbol: str, size: float = 0.6, **kw):
    return x_mark(size, **kw) if symbol == "X" else o_mark(size, **kw)


def ghost(symbol: str, size: float = 0.6) -> VMobject:
    """A faded, dashed mark for a move that never gets played."""
    m = mark(symbol, size, color=GHOST_COLOR, stroke=5)
    parts = m if isinstance(m, VGroup) else VGroup(m)
    return VGroup(*[DashedVMobject(p, num_dashes=8 if isinstance(p, Line) else 14) for p in parts]).set_opacity(0.55)


# ------------------------------------------------------------------ the board
class Board(VGroup):
    """A 3x3 tic-tac-toe grid of side `size`, squares numbered 0-8 left-to-right, top-to-bottom.

    board = Board(size=3)            # VGroup of the 4 grid lines
    board.center_of(4)               # point at the centre square
    board.mark_at(4, "X")            # a new X mobject placed (not added) at square 4
    board.index_labels()             # VGroup of small grey numbers 0-8
    board.win_line(0, 8)             # YELLOW line through squares 0 and 8 (extends a bit)
    board.place_all("X.O..X..O")     # VGroup of marks for a 9-char string ('.' = empty)
    """

    def __init__(self, size: float = 3.0, color: str = GRID_COLOR, stroke: float = 6, **kw):
        super().__init__(**kw)
        self.size = size
        s, c = size, size / 3
        lines = [Line([-s / 2 + c, -s / 2, 0], [-s / 2 + c, s / 2, 0]),
                 Line([-s / 2 + 2 * c, -s / 2, 0], [-s / 2 + 2 * c, s / 2, 0]),
                 Line([-s / 2, s / 2 - c, 0], [s / 2, s / 2 - c, 0]),
                 Line([-s / 2, s / 2 - 2 * c, 0], [s / 2, s / 2 - 2 * c, 0])]
        for ln in lines:
            ln.set_stroke(color, stroke)
        self.add(*lines)

    @property
    def cell(self) -> float:
        return self.width / 3

    def center_of(self, i: int) -> np.ndarray:
        r, c = divmod(i, 3)
        ul = self.get_center() + np.array([-self.width / 2, self.height / 2, 0])
        return ul + np.array([(c + 0.5) * self.cell, -(r + 0.5) * self.cell, 0])

    def mark_at(self, i: int, symbol: str, scale: float = 0.62, **kw):
        return mark(symbol, self.cell * scale, **kw).move_to(self.center_of(i))

    def ghost_at(self, i: int, symbol: str, scale: float = 0.62):
        return ghost(symbol, self.cell * scale).move_to(self.center_of(i))

    def place_all(self, cells: str, scale: float = 0.62) -> VGroup:
        return VGroup(*[self.mark_at(i, ch, scale) for i, ch in enumerate(cells) if ch in "XO"])

    def index_labels(self, size: float = 22) -> VGroup:
        return VGroup(*[S.text(str(i), size, INDEX_COLOR, font=S.FONT_SANS)
                        .move_to(self.center_of(i) + np.array([-0.34, 0.34, 0]) * self.cell)
                        for i in range(9)])

    def win_line(self, a: int, b: int, color: str = WIN_COLOR, stroke: float = 10) -> Line:
        p, q = self.center_of(a), self.center_of(b)
        d = (q - p) / np.linalg.norm(q - p)
        return Line(p - d * self.cell * 0.42, q + d * self.cell * 0.42, color=color, stroke_width=stroke)

    def square(self, i: int, color: str = WIN_COLOR, opacity: float = 0.25) -> Rectangle:
        return Rectangle(width=self.cell * 0.94, height=self.cell * 0.94, stroke_width=0) \
            .set_fill(color, opacity).move_to(self.center_of(i))


def mini_board(cells: str = ".........", size: float = 0.9, stroke: float = 3, line=None) -> VGroup:
    """A small finished/partial board for trees and tables. Returns VGroup(board, marks[, line])."""
    b = Board(size=size, stroke=stroke)
    g = VGroup(b, b.place_all(cells, scale=0.6).set_stroke(width=max(2, stroke)))
    if line is not None:
        g.add(b.win_line(*line, stroke=max(3, stroke + 1)))
    g.board = b
    return g


# ------------------------------------------------------------------ the program
PROGRAM_PATH = ASSETS / "play_all_games.py"
PROGRAM = PROGRAM_PATH.read_text()


def program_lines(first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of the program shown in the video."""
    return "\n".join(PROGRAM.splitlines()[first - 1:last])


def _house_code_style():
    """Monokai, but with light comments: the `# ...` notes are the plain-English labels a
    12-year-old needs, so they must be readable (monokai's comment grey is too dim)."""
    from pygments.styles import get_style_by_name
    from pygments.token import Comment
    base = get_style_by_name("monokai")
    return type("HouseCodeStyle", (base,), {"styles": {**base.styles, Comment: "#D9D3B8",
                                                        Comment.Single: "#D9D3B8"}})


HOUSE_CODE_STYLE = _house_code_style()


def code_block(source: str, font_size: float = 22, line_numbers: bool = False,
               width: float | None = None) -> Code:
    """The house code style: monokai colours (with light comments) on a dark rounded panel.

    Pass `width` to scale the whole panel to that width (keep the text >= ~20 pt on screen)."""
    c = Code(code_string=source, language="python", formatter_style=HOUSE_CODE_STYLE,
                add_line_numbers=line_numbers,
                background="rectangle",
                background_config={"fill_color": S.GREY_DARKER, "stroke_color": S.GREY_DARK,
                                   "stroke_width": 2, "corner_radius": 0.15},
                paragraph_config={"font_size": font_size, "font": "DejaVu Sans Mono"})
    if width is not None:
        c.scale_to_fit_width(width)
    return c


def big_number(n: int, size: float = 96, color: str = COUNT_COLOR):
    return S.text(f"{n:,}", size, color)


# ------------------------------------------------------------------ explore() on screen (S06, S07)
EXPLORE_FIRST, EXPLORE_LAST = 23, 35        # explore() in assets/play_all_games.py (1-based, inclusive)
EXPLORE_SOURCE = program_lines(EXPLORE_FIRST, EXPLORE_LAST)
EXPLORE_WIDTH = 8.0                         # same size in S06 and S07, so strike-throughs land on known lines


def explore_code() -> Code:
    """The explore() function as shown in S06 and S07: same size, placed at the left edge.

    code.code_lines[k] is line k (0-based) of EXPLORE_SOURCE:
      0 def explore(player):          5 total = 0                  10 total += explore(next_player)
      1 if winner(...) is not None:   6 for square in range(9):    11 board[square] = "."  (undo)
      2     return 1                  7     if board[square] == ".":  12 return total
      3 if "." not in board:          8         board[square] = player
      4     return 1                  9         next_player = ...
    """
    c = code_block(EXPLORE_SOURCE, font_size=24, width=EXPLORE_WIDTH)
    return c.to_edge(LEFT, buff=0.35)


def code_line(code: Code, k: int):
    """Line k (0-based) of a code block's text."""
    return code.code_lines[k]


def line_highlight(code: Code, k: int, color: str = WIN_COLOR, opacity: float = 0.22) -> Rectangle:
    """A translucent bar over line k of `code`, spanning the panel width. Add it AFTER the code (the
    code panel is opaque, so a bar behind it would be hidden); the text stays readable through it."""
    ln = code_line(code, k)
    bg = code.background
    return Rectangle(width=bg.width - 0.12, height=ln.height + 0.12, stroke_width=0) \
        .set_fill(color, opacity).move_to([bg.get_center()[0], ln.get_center()[1], 0])


def strike(code: Code, k: int, color: str = UNDO_COLOR) -> Line:
    """A RED strike-through across the text of line k ("delete this line")."""
    ln = code_line(code, k)
    y = line_highlight(code, k).get_center()[1]
    return Line([ln.get_left()[0] - 0.08, y, 0], [ln.get_right()[0] + 0.08, y, 0], color=color, stroke_width=6)


# ------------------------------------------------------------------ move numbers and playing moves
def move_number(board: Board, i: int, n: int, symbol: str, size: float = 24):
    """Small move number in the lower-right corner of square i, in the player's colour."""
    color = X_COLOR if symbol == "X" else O_COLOR
    return S.text(str(n), size, color, font=S.FONT_SANS) \
        .move_to(board.center_of(i) + np.array([0.36, -0.36, 0]) * board.cell)


def mark_anim(m):
    """Draw a mark the way a hand would: an O in one stroke, an X as two strokes."""
    from manim import Create, LaggedStart
    return LaggedStart(*[Create(s) for s in m], lag_ratio=0.5) if isinstance(m, VGroup) else Create(m)
