"""S02 · Filling the board: nine factorial.

Beats: an empty board fills up move by move: X completes the top row on move 5 (YELLOW line, 'X won!'),
but the players ignore it and keep going (moves 6-9 dimmer) until the board is full; then the move
numbers shuffle: in how many orders can the board fill? -> the board shrinks into the root of a tree:
9 first moves for X, then the 8 replies for O under the first one, which pack into a small bundle
that is copied under every first move: 9 groups of 8 = 72 -> that label becomes the start of the
product 9 x 8 x 7 x ... x 1, built term by term with the running total under each term -> it
collapses to 9 x 8 x ... x 1 = 9! = 362,880 ("nine factorial") -> 362,880 next to 255,168 as two
bars: too many!  Where do the extra games come from?
"""

import numpy as np
from manim import *

from explainer import i18n
from explainer import style as S
from explainer.scene import VoiceScene

from common import (COUNT_COLOR, NARRATION, NINE_FACTORIAL, TOTAL_GAMES, UNDO_COLOR, WIN_COLOR, WIN_LINES,
                    X_COLOR, Board, mark_anim, mini_board, move_number, o_mark, winner, x_mark)

SAY = NARRATION["S02"]

# A fill that ignores three in a row: X completes the top row on move 5 (X0 O3 X1 O4 X2), and the
# players keep going (O8 X5 O6 X7) until the board is full. The top row is the only line ever made.
FILL_GAME = [(0, "X"), (3, "O"), (1, "X"), (4, "O"), (2, "X"), (8, "O"), (5, "X"), (6, "O"), (7, "X")]
WIN_MOVE, WIN_ENDS = 5, (0, 2)
# Two other fill orders (move numbers swap among X's squares and among O's squares; every number
# moves each time). They are fills, not real games: nobody stops for a line here.
SHUFFLES = [
    {5: 1, 7: 3, 0: 5, 2: 7, 1: 9, 6: 2, 8: 4, 3: 6, 4: 8},
    {1: 1, 5: 3, 7: 5, 0: 7, 2: 9, 4: 2, 6: 4, 8: 6, 3: 8},
]


def _check_fill_orders():
    """The first fill is legal up to X's win on move 5 (the only line it ever makes), then fills the
    board taking turns; every shown order is an alternating fill (odd numbers on X, even on O)."""
    assert sorted(sq for sq, _ in FILL_GAME) == list(range(9))
    board = ["."] * 9
    for n, (sq, sym) in enumerate(FILL_GAME, start=1):
        assert sym == ("X" if n % 2 else "O")
        board[sq] = sym
        assert winner(board) == ("X" if n >= WIN_MOVE else None)
    lines = [(a, c) for a, b, c in WIN_LINES if board[a] == board[b] == board[c]]
    assert lines == [WIN_ENDS] and board[WIN_ENDS[0]] == "X"
    final = dict(FILL_GAME)
    orders = [{sq: n for n, (sq, _) in enumerate(FILL_GAME, start=1)}, *SHUFFLES]
    for order in orders:
        assert sorted(order.values()) == list(range(1, 10))
        assert all(final[sq] == ("X" if n % 2 else "O") for sq, n in order.items())
    for before, after in zip(orders, orders[1:]):
        assert all(after[sq] != before[sq] for sq in after)          # every number visibly moves


_check_fill_orders()

# ------------------------------------------------------------------ tree layout
ROOT_Y = 3.0
KID_Y = 1.25
KID_SIZE = 0.8
KID_X = [-5.6 + 1.4 * i for i in range(9)]
WIDE_Y = -0.75                      # O's 8 replies under the first X move, big enough to read
WIDE_X = [-5.6 + 1.0 * j for j in range(8)]
TINY = 0.36                         # boards inside a packed bundle of 8
LABEL_C = np.array([3.6, ROOT_Y, 0])

# ------------------------------------------------------------------ product row layout
COL_X = [-5.8 + 1.45 * i for i in range(9)]
GLYPH_Y, TERM_Y, TOTAL_Y = 1.1, 0.15, -0.9
RUNNING = [int(np.prod(range(9, 8 - i, -1))) for i in range(9)]   # 9, 72, 504, ..., 362880

# ------------------------------------------------------------------ bars layout
BASE_Y = -2.55
BAR_H = 3.8                         # height of the 362,880 bar
BAR_W = 1.8
LEFT_X, RIGHT_X = -2.2, 2.2


def cells(x_sq: int, o_sq: int | None = None) -> str:
    c = ["."] * 9
    c[x_sq] = "X"
    if o_sq is not None:
        c[o_sq] = "O"
    return "".join(c)


def tex_num(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


def text_t2c(s: str, size: float, color, t2c: dict, **kw) -> Text:
    """S.text(s, size, color, t2c=t2c, **kw). Pango lays out each t2c run on its own, and in CJK
    text a run of only Latin letters or digits (the 'X' of 'X 赢了！') sits ~0.08 units above
    the line; a language version copies the colours onto the same text laid out in one piece."""
    t = S.text(s, size, color, t2c=t2c, **kw)
    if not (i18n.active() and i18n.has_cjk(t.text)):
        return t
    plain = S.text(s, size, color, **kw)
    assert len(plain) == len(t), (t.text, len(plain), len(t))
    for g, c in zip(plain, t):
        g.set_color(c.get_color())
    return plain


def label_pieces(label: Text) -> tuple[int, int, int, int]:
    """Glyph indices of the '9', the '8', the '=' and the first digit of '72' in the
    '9 groups of 8 = 72' label, found in its rendered string (which may be a translation, e.g.
    '9 个 8 = 72'): Text has one glyph per character that is not a space or a line break."""
    chars = [c for c in label.text if not c.isspace()]
    assert len(chars) == len(label), (label.text, len(label))
    eq = chars.index("=")
    return chars.index("9"), max(i for i in range(eq) if chars[i] == "8"), eq, eq + 1


def bundle(i: int, kid_bottom: float, faded: bool) -> VGroup:
    """The 8 boards after X takes square i (one O in each other square), packed in a column under
    child i. Returns VGroup(connector, frame, boards)."""
    boards = VGroup(*[mini_board(cells(i, k), size=TINY, stroke=1.5) for k in range(9) if k != i])
    boards.arrange(DOWN, buff=0.05)
    top = kid_bottom - 0.2
    boards.move_to([KID_X[i], top - boards.height / 2, 0])
    frame = SurroundingRectangle(boards, buff=0.06, corner_radius=0.08, color=S.GREY, stroke_width=1.5)
    conn = Line([KID_X[i], kid_bottom, 0], frame.get_top(), color=S.GREY, stroke_width=2)
    g = VGroup(conn, frame, boards)
    if faded:
        g.set_stroke(opacity=0.4)
    return g


class FillTheBoard(VoiceScene):
    def construct(self):
        # ========================================================== 1. fill the whole board
        board = Board(size=3.6).move_to(DOWN * 0.45)
        caption = S.text("What if the game never stopped early?", 40).to_edge(UP, buff=0.5)

        win = board.win_line(*WIN_ENDS)
        won_text = text_t2c("X won!", 30, WIN_COLOR, {"X": X_COLOR}, weight=BOLD)
        won = VGroup(SurroundingRectangle(won_text, buff=0.12, corner_radius=0.08, color=WIN_COLOR,
                                          stroke_width=2.5).set_fill(S.BG, 0.9), won_text)
        won.next_to(win, RIGHT, buff=0.3)
        dim = 0.4                       # moves 6-9: the players play on after X's win

        with self.voiceover(SAY[0]) as vo:
            self.play(LaggedStart(*[Create(ln) for ln in board], lag_ratio=0.2), run_time=0.8)
            self.play(Write(caption), run_time=1.0)
            marks, nums = VGroup(), {}
            # moves 1-4 run up to "ignore three in a row"; X's winning move 5 lands on it
            step = min(0.5, max(0.3, vo.until("ignore three in a row") / (WIN_MOVE - 1)))
            for n, (sq, sym) in enumerate(FILL_GAME, start=1):
                m = board.mark_at(sq, sym, scale=0.5)
                num = move_number(board, sq, n, sym, size=26)
                marks.add(m)
                nums[sq] = num
                if n == WIN_MOVE:
                    vo.wait_until("ignore three in a row")
                elif n == WIN_MOVE + 1:
                    vo.wait_until("and just keep going")
                if n > WIN_MOVE:
                    m.set_stroke(opacity=dim)
                    num.set_opacity(dim)
                self.play(mark_anim(m), FadeIn(num, scale=0.6), run_time=step if n <= WIN_MOVE else 0.45)
                if n == WIN_MOVE:       # X has three in a row ... and nobody stops
                    self.play(Create(win), FadeIn(won, shift=LEFT * 0.2), run_time=0.45)
                    self.play(Indicate(win, color=WIN_COLOR, scale_factor=1.12), run_time=0.5)
            # other orders: the line goes (it isn't a win at move 5 in every order) and all moves look alike,
            # then the move numbers swap places (X's among X squares, O's among O's)
            vo.wait_until("In how many")
            late = [sq for sq, _ in FILL_GAME[WIN_MOVE:]]
            self.play(FadeOut(win), FadeOut(won), marks[WIN_MOVE:].animate.set_stroke(opacity=1),
                      *[nums[sq].animate.set_opacity(1) for sq in late], run_time=0.45)
            num_of = {sq: n for n, (sq, _) in enumerate(FILL_GAME, start=1)}
            for shuffle in SHUFFLES:
                # the number now in square sq travels to the square that gets it in the new order
                square_of = {n: sq for sq, n in shuffle.items()}
                dest = {sq: square_of[num_of[sq]] for sq in nums}
                corner = np.array([0.36, -0.36, 0]) * board.cell        # as in move_number()
                self.play(*[nums[sq].animate(path_arc=PI / 2).move_to(board.center_of(dest[sq]) + corner)
                            for sq in nums], run_time=0.8)
                nums, num_of = {dest[sq]: nums[sq] for sq in nums}, dict(shuffle)
            question = S.text("?", 110, COUNT_COLOR).next_to(board, RIGHT, buff=0.9)
            self.play(FadeIn(question, scale=0.5), run_time=0.5)

        # ========================================================== 2. a tree of choices
        root = Board(size=0.9, stroke=3).move_to([0, ROOT_Y, 0])
        kids = [mini_board(cells(i), size=KID_SIZE).move_to([KID_X[i], KID_Y, 0]) for i in range(9)]
        kid_bottom = KID_Y - KID_SIZE / 2
        branches = VGroup(*[Line(root.get_bottom(), k.get_top(), color=S.GREY, stroke_width=2.5)
                            for k in kids])

        label_x = VGroup(x_mark(0.3, stroke=6), S.text("9 choices", 32)).arrange(RIGHT, buff=0.22)
        label_x.move_to(LABEL_C)

        wide = [mini_board(cells(0, k), size=0.8).move_to([WIDE_X[j], WIDE_Y, 0])
                for j, k in enumerate(range(1, 9))]
        fan = VGroup(*[Line([KID_X[0], kid_bottom, 0], w.get_top(), color=S.GREY, stroke_width=2)
                       for w in wide])
        label_o = VGroup(o_mark(0.3, stroke=6), S.text("8 choices", 32)).arrange(RIGHT, buff=0.22)
        label_o.move_to([4.2, WIDE_Y, 0])

        bundles = [bundle(i, kid_bottom, faded=i > 0) for i in range(9)]
        groups_label = S.text("9 groups of 8 = 72", 40, COUNT_COLOR).move_to(LABEL_C)
        # glyphs: 0 '9' | 1-8 'groupsof' | 9 '8' | 10 '=' | 11-12 '72' (found by label_pieces)
        g9, g8, g_eq, g72 = label_pieces(groups_label)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(marks, *nums.values(), question, caption)), run_time=0.45)
            self.play(ReplacementTransform(board, root), run_time=0.75)
            # X: 9 first moves
            self.play(LaggedStart(*[AnimationGroup(Create(br), TransformFromCopy(root, k[0]))
                                    for br, k in zip(branches, kids)], lag_ratio=0.1), run_time=1.2)
            self.play(LaggedStart(*[mark_anim(k[1][0]) for k in kids], lag_ratio=0.12),
                      FadeIn(label_x, shift=LEFT * 0.2), run_time=0.9)
            # O: 8 replies under the first move
            vo.wait_until("For each of those")
            self.play(LaggedStart(*[AnimationGroup(Create(f), TransformFromCopy(kids[0][0], w[0]),
                                                   TransformFromCopy(kids[0][1][0], w[1][0]))
                                    for f, w in zip(fan, wide)], lag_ratio=0.08), run_time=1.1)
            vo.wait_until("O has 8")
            self.play(LaggedStart(*[Create(w[1][1]) for w in wide], lag_ratio=0.15), run_time=1.0)
            self.play(FadeIn(label_o, shift=LEFT * 0.2), run_time=0.4)
            # "9" and "8" become the label (one thing at a time: label, then pack, then copies)
            vo.wait_until("That's 9 groups")
            self.play(ReplacementTransform(label_x[1][0], groups_label[g9]),
                      FadeTransform(label_x[1][1:], groups_label[g9 + 1:g8]),     # words cross-fade (no glyph scramble)
                      ReplacementTransform(label_o[1][0], groups_label[g8]),
                      FadeOut(label_x[0], scale=0.3), FadeOut(label_o[0], scale=0.3), FadeOut(label_o[1][1:]),
                      run_time=0.8)
            # pack the 8 into a bundle under the first move
            b0 = bundles[0]
            self.play(*[ReplacementTransform(w, b) for w, b in zip(wide, b0[2])],
                      ReplacementTransform(fan, b0[0]), Create(b0[1]), run_time=0.8)
            # ... and the same bundle drops under every other first move
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.5) for b in bundles[1:]], lag_ratio=0.12),
                      run_time=1.4)
            vo.wait_until("9 times 8 is 72")
            self.play(Write(groups_label[g_eq:]),
                      LaggedStart(*[b[1].animate.set_stroke(COUNT_COLOR, width=2.5, opacity=1)
                                    for b in bundles], lag_ratio=0.15), run_time=1.3)
            vo.wait_until("first two moves")
            self.play(Indicate(groups_label[g72:], color=COUNT_COLOR, scale_factor=1.25), run_time=0.8)

        self.add(groups_label)          # re-gather the label's pieces into one top-level mobject
        tree = [m for m in self.mobjects if m is not groups_label]

        # ========================================================== 3. 9 x 8 x 7 x ... x 1
        terms = [S.math(str(9 - i), size=68).move_to([COL_X[i], TERM_Y, 0]) for i in range(9)]
        times = [S.math(r"\times", size=54, color=S.GREY).move_to([(COL_X[i] + COL_X[i + 1]) / 2, TERM_Y, 0])
                 for i in range(8)]
        glyphs = [(x_mark(0.4, stroke=7) if i % 2 == 0 else o_mark(0.4, stroke=7))
                  .move_to([COL_X[i], GLYPH_Y, 0]) for i in range(9)]
        totals = [S.math(tex_num(RUNNING[i]), size=34, color=COUNT_COLOR).move_to([COL_X[i], TOTAL_Y, 0])
                  for i in range(9)]
        assert RUNNING[-1] == NINE_FACTORIAL

        parts = []
        for i in range(9):
            parts.append(str(9 - i))
            if i < 8:
                parts.append(r"\times")
        eq = S.math(*parts, "=", "9!", "=", tex_num(NINE_FACTORIAL), size=56).move_to([0, TERM_Y, 0])
        for k in range(1, 17, 2):
            eq[k].set_color(S.GREY)
        eq[18].set_color(COUNT_COLOR)
        eq[20].set_color(COUNT_COLOR)
        nf_label = S.text("nine factorial", 32).next_to(eq[18], DOWN, buff=0.85)
        nf_arrow = Arrow(nf_label.get_top(), eq[18].get_bottom(), buff=0.1, color=S.GREY,
                         stroke_width=3, max_tip_length_to_length_ratio=0.3)

        with self.voiceover(SAY[2]) as vo:
            # clear the tree first, so the 9, 8 and 72 fly into the product row over an empty stage
            self.play(FadeOut(Group(*tree)), FadeOut(groups_label[g9 + 1:g8]), FadeOut(groups_label[g_eq]),
                      run_time=0.5)
            # the label's 9, 8 and 72 slide (whole, not glyph-morphed: Text -> MathTex morphs into blobs)
            nine, eight, seventy_two = groups_label[g9], groups_label[g8], groups_label[g72:]
            self.play(nine.animate.scale_to_fit_height(terms[0].height).move_to(terms[0]).set_color(S.WHITE),
                      eight.animate.scale_to_fit_height(terms[1].height).move_to(terms[1]).set_color(S.WHITE),
                      seventy_two.animate.scale_to_fit_height(totals[1].height).move_to(totals[1]),
                      FadeIn(times[0]), FadeIn(glyphs[0], shift=DOWN * 0.15),
                      FadeIn(glyphs[1], shift=DOWN * 0.15), FadeIn(totals[0]), run_time=0.8)
            for m in [seventy_two, *groups_label]:
                self.remove(m)
            self.add(terms[0], terms[1], totals[1])
            for i in range(2, 9):
                if i == 2:
                    vo.wait_until("times 7")
                elif i == 3:
                    vo.wait_until("and so on")
                prev = totals[i - 1]
                self.play(LaggedStart(
                    AnimationGroup(FadeIn(times[i - 1]), FadeIn(glyphs[i], shift=DOWN * 0.15),
                                   FadeIn(terms[i], shift=DOWN * 0.15)),
                    AnimationGroup(ReplacementTransform(prev.copy(), totals[i]),
                                   prev.animate.set_opacity(0.6)),
                    lag_ratio=0.45), run_time=0.5 if i == 2 else 0.44)
            # the compact form: the product slides together and the final running total waits, dimmed,
            # in the slot it will fill (moved and scaled as a whole: a glyph morph scrambles the digits)
            vo.wait_until("Mathematicians")
            final_num = totals[8]
            self.play(*[ReplacementTransform(terms[i], eq[2 * i]) for i in range(9)],
                      *[ReplacementTransform(times[i], eq[2 * i + 1]) for i in range(8)],
                      final_num.animate.scale(eq[20].width / final_num.width).move_to(eq[20])
                      .set_opacity(0.35),
                      FadeOut(VGroup(*glyphs)), FadeOut(VGroup(*totals[:8])), run_time=1.2)
            vo.wait_until("nine factorial")
            self.play(Write(eq[17]), Write(eq[18]), run_time=0.7)
            self.play(GrowArrow(nf_arrow), FadeIn(nf_label, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("exclamation mark")
            self.play(Indicate(eq[18][1], color=COUNT_COLOR, scale_factor=1.8), run_time=0.9)
            vo.wait_until("It equals")
            self.play(Write(eq[19]), final_num.animate.set_opacity(1), run_time=0.8)
            self.play(Circumscribe(VGroup(eq[18], final_num), color=COUNT_COLOR, buff=0.15),
                      run_time=1.2)

        # ========================================================== 4. too many!
        left_bar = Rectangle(width=BAR_W, height=BAR_H, stroke_width=0).set_fill(COUNT_COLOR, 0.85)
        left_bar.move_to([LEFT_X, BASE_Y + BAR_H / 2, 0])
        h_real = BAR_H * TOTAL_GAMES / NINE_FACTORIAL
        right_bar = Rectangle(width=BAR_W, height=h_real, stroke_width=0).set_fill(COUNT_COLOR, 0.85)
        right_bar.move_to([RIGHT_X, BASE_Y + h_real / 2, 0])
        tail = VGroup(eq[18], eq[19], final_num)
        tail_target = tail.copy().move_to([LEFT_X, left_bar.get_top()[1] + 0.45, 0])
        real_num = S.math(tex_num(TOTAL_GAMES), size=56, color=COUNT_COLOR) \
            .move_to([RIGHT_X, right_bar.get_top()[1] + 0.45, 0])
        left_lab = S.text("never stop early", 28).move_to([LEFT_X, BASE_Y - 0.45, 0])
        right_lab = S.text("real games", 28).move_to([RIGHT_X, BASE_Y - 0.45, 0])
        baseline = Line([-4.0, BASE_Y, 0], [4.0, BASE_Y, 0], color=S.GREY, stroke_width=2)

        tag_text = S.text("too many!", 34, UNDO_COLOR, weight=BOLD)
        tag = VGroup(SurroundingRectangle(tag_text, buff=0.15, corner_radius=0.1, color=UNDO_COLOR,
                                          stroke_width=3).set_fill(S.BG, 0.9), tag_text)
        tag.rotate(6 * DEGREES).move_to([LEFT_X - 0.5, tail_target.get_top()[1] + 0.75, 0])

        level = DashedLine([LEFT_X - BAR_W / 2 - 0.3, right_bar.get_top()[1], 0],
                           [RIGHT_X + BAR_W / 2 + 0.3, right_bar.get_top()[1], 0],
                           color=S.WHITE, stroke_width=2.5, dash_length=0.12)
        extra = Rectangle(width=BAR_W, height=BAR_H - h_real, stroke_width=0).set_fill(S.BG, 0.6)
        extra.move_to([LEFT_X, (left_bar.get_top()[1] + right_bar.get_top()[1]) / 2, 0])
        extra_edge = DashedVMobject(Rectangle(width=BAR_W, height=BAR_H - h_real, color=UNDO_COLOR,
                                              stroke_width=4).move_to(extra), num_dashes=28)
        extra_lab = S.text("extra games?", 32, UNDO_COLOR).next_to(extra, LEFT, buff=0.35)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(*eq[:18], nf_label, nf_arrow)), Transform(tail, tail_target),
                      Create(baseline), GrowFromEdge(left_bar, DOWN), FadeIn(left_lab, shift=UP * 0.2),
                      run_time=1.1)
            vo.wait_until("That's more than")
            self.play(GrowFromEdge(right_bar, DOWN), FadeIn(real_num, shift=UP * 0.2),
                      FadeIn(right_lab, shift=UP * 0.2), run_time=1.0)
            self.play(Indicate(real_num, color=COUNT_COLOR, scale_factor=1.1), run_time=0.8)
            vo.wait_until("Our count")
            self.play(FadeIn(tag, scale=1.5), run_time=0.5)
            self.play(Wiggle(tail, scale_value=1.08), run_time=0.8)
            vo.wait_until("Where are all")
            self.play(Create(level), FadeIn(extra), Create(extra_edge), run_time=0.8)
            self.play(Write(extra_lab), run_time=0.7)

        self.wait(0.6)                  # let the closing question land before the cut
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
