"""S05 · Teaching a computer the rules.

Checklist strip (top right): board · winning lines · spot a winner -- each item ticks GREEN as
its beat ends.

1. board: the numbered 3x3 board -> its nine squares slide into a row (a Python list, spots 0-8),
   each gets a dot -> `board = ["."] * 9`  ("a dot, 9 times").
2. winning lines: the row rolls back into the board; the WIN_LINES code; each triple highlighted
   in the code lights its line YELLOW on the board: (0, 1, 2), (0, 4, 8), then the rest quickly
   -> "8 winning lines".
3. spot a winner: winner() ("function = a mini-program with a name"); a scanner walks the lines of
   an example board (GREY ✗ for each line that is not three equal marks; a line of dots fails the
   `!= "."` test) until X's middle column lights YELLOW and the function hands back "X". Then ("If no
   line matches") X's last mark moves so no line is complete: every line gets ✗ -> "nothing found →
   None (nobody)" on "hands back None"; the scene fades out right after the narration.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (COUNT_COLOR, GRID_COLOR, NARRATION, WIN_COLOR, WIN_LINES, X_COLOR, Board,
                    code_block, program_lines, winner)

SAY = NARRATION["S05"]
MONO = "DejaVu Sans Mono"

# Example boards for winner() (squares 0-8, '.' = empty). Both are legal positions:
# EX_WIN: X 4, O 2, X 1, O 8, X 7 -> X completes the middle column on move 5 (O has no line).
#   Scan order: rows ✗ (. X O / . X . / . X O), left column ". . ." ✗ (only dots), then X X X.
# EX_NONE: the same board with X's last mark on 5 instead of 7 -> nobody has three in a row.
EX_WIN, EX_WIN_ORDER, WIN_AT = ".XO.X..XO", [4, 2, 1, 8, 7], (1, 4, 7)
EX_NONE = ".XO.XX..O"
assert winner(list(EX_WIN)) == "X" and winner(list(EX_NONE)) is None
assert EX_WIN.count("X") == 3 and EX_WIN.count("O") == 2 and EX_NONE.count("X") == 3


# ------------------------------------------------------------------ small helpers
def glyphs(code, k, i0, i1) -> VGroup:
    """Characters i0..i1-1 (spaces don't count) of line k of a code block."""
    return VGroup(*code.code_lines[k][i0:i1])


def glyph_box(m, color=WIN_COLOR, opacity=0.25, buff=0.05):
    """Translucent highlight around a few characters of code (add it after the code)."""
    return SurroundingRectangle(m, buff=buff, corner_radius=0.05, stroke_color=color,
                                stroke_width=2).set_fill(color, opacity)


def code_bar(code, k, color=WIN_COLOR, opacity=0.16):
    """Translucent bar behind the text of line k (only as wide as the text)."""
    ln = code.code_lines[k]
    return Rectangle(width=ln.width + 0.3, height=0.4, stroke_width=0).set_fill(color, opacity) \
        .move_to(ln.get_center())


def op_box(m):
    """Soft chip around an operator in the code (!= or ==)."""
    return SurroundingRectangle(m, buff=0.07, corner_radius=0.06, stroke_color=S.WHITE,
                                stroke_width=1.5, stroke_opacity=0.8).set_fill(S.WHITE, 0.12)


def outlined(t):
    """Give a small label a dark outline so it stays readable on top of lines."""
    return t.set_stroke(S.BG, 5, background=True)


def list_brackets(row: VGroup, color=S.WHITE) -> VGroup:
    """Big square brackets [ ... ] around a row of boxes: "this row is a Python list"."""
    h, w, gap = row.height + 0.36, 0.22, 0.2
    y0, y1 = row.get_center()[1] - h / 2, row.get_center()[1] + h / 2
    xl, xr = row.get_left()[0] - gap, row.get_right()[0] + gap
    left = VMobject().set_points_as_corners([[xl + w, y1, 0], [xl, y1, 0], [xl, y0, 0], [xl + w, y0, 0]])
    right = VMobject().set_points_as_corners([[xr - w, y1, 0], [xr, y1, 0], [xr, y0, 0], [xr - w, y0, 0]])
    return VGroup(left, right).set_stroke(color, 5)


def make_checklist() -> VGroup:
    items = VGroup()
    for name in ("board", "winning lines", "spot a winner"):
        box = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.06, stroke_color=S.GREY,
                               stroke_width=2.5)
        items.add(VGroup(box, S.text(name, 26, S.GREY)).arrange(RIGHT, buff=0.16))
    items.arrange(RIGHT, buff=0.55)
    return items.move_to([6.45 - items.width / 2, 3.27, 0])


def activate(item) -> AnimationGroup:
    return AnimationGroup(item[0].animate.set_stroke(S.WHITE), item[1].animate.set_color(S.WHITE))


def tick(item) -> AnimationGroup:
    box = item[0]
    c, s = box.get_center(), box.width
    check = VMobject().set_points_as_corners(
        [c + np.array([-0.3, 0.02, 0]) * s, c + np.array([-0.06, -0.26, 0]) * s,
         c + np.array([0.42, 0.42, 0]) * s]).set_stroke(S.GREEN, 5)
    item.add(check)
    return AnimationGroup(Create(check), box.animate.set_stroke(S.GREEN),
                          item[1].animate.set_color(S.GREEN))


# ------------------------------------------------------------------ the scene
class BoardCode(VoiceScene):
    def construct(self):
        strip = make_checklist()

        # ========================================================== 1. the board
        ROW_Y = 0.45
        b1 = Board(size=3.3).move_to(UP * ROW_Y)
        labels = b1.index_labels()
        for lab in labels:
            outlined(lab)
        labels.set_z_index(3)

        def row_x(i):
            return (i - 4) * 1.2

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(strip, shift=DOWN * 0.15), run_time=0.6)
            self.play(activate(strip[0]), LaggedStart(*[Create(ln) for ln in b1], lag_ratio=0.2),
                      run_time=0.9)
            self.play(LaggedStart(*[FadeIn(lab, scale=0.5) for lab in labels], lag_ratio=0.12),
                      run_time=1.0)

            # the nine squares become boxes and slide into a row: a list of 9 spots
            vo.wait_until("We'll use a list")
            tiles = VGroup(*[Square(b1.cell).set_stroke(GRID_COLOR, 4).set_fill(S.GREY_DARKER, 1)
                             .move_to(b1.center_of(i)) for i in range(9)]).set_z_index(1)
            self.play(FadeIn(tiles), FadeOut(b1), run_time=0.5)
            self.play(LaggedStart(*[AnimationGroup(
                tiles[i].animate.scale(1.0 / b1.cell).move_to([row_x(i), ROW_Y, 0]),
                labels[i].animate.scale(28 / 22).move_to([row_x(i), ROW_Y - 0.82, 0]))
                for i in range(9)], lag_ratio=0.08), run_time=1.6)

            # "In Python ... a list": brackets close around the row, the spot numbers light up
            vo.wait_until("In Python")
            brackets = list_brackets(VGroup(*[Square(1.0).move_to([row_x(i), ROW_Y, 0]) for i in range(9)]))
            self.play(FadeIn(brackets[0], shift=RIGHT * 0.3), FadeIn(brackets[1], shift=LEFT * 0.3),
                      run_time=0.6)
            self.play(labels.animate.set_color(S.WHITE), run_time=0.5)

            vo.wait_until("starting from zero")
            self.play(Indicate(labels[0], color=S.WHITE, scale_factor=1.9), run_time=1.0)
            vo.wait_until("so our squares")
            self.play(LaggedStart(*[Indicate(lab, color=S.WHITE, scale_factor=1.45) for lab in labels],
                                  lag_ratio=0.18), run_time=2.0)

            # an empty square holds a dot
            vo.wait_until("An empty square")
            dots = VGroup(*[Dot(tiles[i].get_center(), radius=0.09, color=S.WHITE) for i in range(9)])
            dots.set_z_index(2)
            code1 = code_block('board = ["."] * 9', font_size=32).move_to(DOWN * 1.65)
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1),
                      FadeIn(code1, shift=UP * 0.2), run_time=0.7)
            box_dot = glyph_box(glyphs(code1, 0, 7, 10))     # "."
            box_9 = glyph_box(glyphs(code1, 0, 11, 13))      # * 9
            cap_dot, cap_9 = S.text("a dot,", 30), S.text("9 times", 30)
            VGroup(cap_dot, cap_9).arrange(RIGHT, buff=0.2, aligned_edge=UP).next_to(code1, DOWN, buff=0.35)
            self.play(FadeIn(box_dot), FadeIn(cap_dot, shift=UP * 0.1),
                      LaggedStart(*[Indicate(d, color=S.WHITE, scale_factor=1.8) for d in dots],
                                  lag_ratio=0.08), run_time=0.8)
            self.play(FadeIn(box_9), FadeIn(cap_9, shift=UP * 0.1),
                      LaggedStart(*[t.animate(rate_func=there_and_back).set_stroke(S.YELLOW, 7) for t in tiles],
                                  lag_ratio=0.1), run_time=1.0)
        self.play(tick(strip[0]), run_time=0.5)

        # ========================================================== 2. winning lines
        b2 = Board(size=3.1).move_to(RIGHT * 4.95 + DOWN * 0.35)
        lab2 = b2.index_labels()
        for lab in lab2:
            outlined(lab)
        code2 = code_block(program_lines(7, 11), font_size=21)
        code2.move_to([-6.45 + code2.width / 2, b2.get_center()[1], 0])

        # where each triple sits in the code: (code line, position in that line)
        where = {(0, 1, 2): (1, 0), (3, 4, 5): (1, 1), (6, 7, 8): (1, 2),
                 (0, 3, 6): (2, 0), (1, 4, 7): (2, 1), (2, 5, 8): (2, 2),
                 (0, 4, 8): (3, 0), (2, 4, 6): (3, 1)}

        def triple(t):
            k, j = where[t]
            return glyphs(code2, k, 8 * j, 8 * j + 7)        # "(a,b,c)"

        def light(t):
            return [labels[i].animate.set_color(S.YELLOW if i in t else S.GREY) for i in range(9)]

        win_lines = VGroup()

        def draw_line(t, rt):
            """Draw line t in full YELLOW; earlier lines step back so the new one stands out."""
            ln = b2.win_line(t[0], t[2], stroke=8).set_z_index(2)
            dim = [old.animate.set_stroke(opacity=0.3) for old in win_lines]
            win_lines.add(ln)
            self.play(Create(ln), *dim, run_time=rt)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(code1, box_dot, box_9, cap_dot, cap_9, brackets)), activate(strip[1]),
                      run_time=0.5)
            # the row rolls back up into the board
            self.play(LaggedStart(*[AnimationGroup(
                tiles[i].animate.scale(b2.cell).move_to(b2.center_of(i)),
                dots[i].animate.scale(0.8).move_to(b2.center_of(i)),
                Transform(labels[i], lab2[i])) for i in range(9)], lag_ratio=0.06), run_time=1.6)
            self.play(LaggedStart(*[Create(ln) for ln in b2], lag_ratio=0.15), FadeOut(tiles),
                      run_time=0.7)

            vo.wait_until("We simply list")
            self.play(FadeIn(code2, shift=RIGHT * 0.3), run_time=0.9)
            # count the groups of three: a chip hops over the 8 triples while a GREEN counter ticks 1..8
            vo.wait_until("as groups of three")
            count = S.text("8 winning lines", 32, COUNT_COLOR).next_to(code2, DOWN, buff=0.45)
            num = S.text("1", 32, COUNT_COLOR).move_to(count[0])
            chip = glyph_box(triple(WIN_LINES[0]))
            self.play(FadeIn(chip), FadeIn(num, scale=0.6), run_time=0.3)
            for k, t in enumerate(WIN_LINES[1:], start=2):
                self.play(Transform(chip, glyph_box(triple(t))),
                          Transform(num, S.text(str(k), 32, COUNT_COLOR).move_to(count[0])), run_time=0.2)
            rest = VGroup(*count[1:])                          # "winning lines"
            self.play(FadeOut(chip), FadeIn(rest, shift=LEFT * 0.15), run_time=0.4)
            self.remove(num, rest)                             # swap in the whole label (looks identical)
            self.add(count)

            vo.wait_until("Squares 0, 1 and 2")
            hl = glyph_box(triple((0, 1, 2)))
            self.play(FadeIn(hl), *light((0, 1, 2)), run_time=0.4)
            draw_line((0, 1, 2), 0.6)

            vo.wait_until("Squares 0, 4 and 8")
            self.play(Transform(hl, glyph_box(triple((0, 4, 8)))), *light((0, 4, 8)), run_time=0.4)
            draw_line((0, 4, 8), 0.6)
            self.wait(0.3)

            # the other six, quickly
            for t in [(3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (2, 4, 6)]:
                self.play(Transform(hl, glyph_box(triple(t))), *light(t), run_time=0.15)
                draw_line(t, 0.22)

        self.play(FadeOut(hl), *light(()), win_lines.animate.set_stroke(opacity=0.75),
                  Indicate(count, color=COUNT_COLOR, scale_factor=1.12), tick(strip[1]), run_time=0.7)

        # ========================================================== 3. spot a winner
        B3_SIZE, B3_CENTER = 2.8, np.array([-3.3, -1.68, 0])
        code3 = code_block(program_lines(14, 17), font_size=22).move_to([0, 1.93, 0])
        b3 = b2                                    # same board, moved down-left
        dot_at = {i: dots[i] for i in range(9)}
        mark_on = {}

        def tag_pos(i):
            return b3.center_of(i) + np.array([-0.33, 0.33, 0]) * b3.cell

        def end_pos(line):
            """Just past the last square of a line, outside the board: where its verdict goes."""
            a, b, c = line
            return b3.center_of(c) + (b3.center_of(c) - b3.center_of(b)) * 0.82

        def cross(line):
            return S.text("✗", 30, S.GREY, font="DejaVu Sans").move_to(end_pos(line))

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(code2, shift=UP * 0.4), FadeOut(win_lines), FadeOut(count),
                      FadeOut(labels), activate(strip[2]),
                      VGroup(b2, dots).animate.scale(B3_SIZE / b2.width).move_to(B3_CENTER),
                      FadeIn(code3, shift=DOWN * 0.2), run_time=1.0)

            # a function: a mini-program with a name
            vo.wait_until("a little mini-program")
            fbox = SurroundingRectangle(glyphs(code3, 0, 0, 17), buff=0.08, corner_radius=0.06,
                                        color=S.WHITE, stroke_width=2.5)
            flab = S.text("function = a mini-program with a name", 26, S.WHITE)
            flab.next_to(fbox, RIGHT, buff=0.8)
            farrow = Arrow(flab.get_left(), fbox.get_right(), buff=0.1, color=S.WHITE,
                           stroke_width=3, max_tip_length_to_length_ratio=0.3)
            self.play(Create(fbox), run_time=0.4)
            self.play(GrowArrow(farrow), FadeIn(flab, shift=LEFT * 0.2), run_time=0.5)

            # its name is winner; here is a board to check
            vo.wait_until("This one, called winner")
            call = S.text("winner(board)", 28, S.WHITE, font=MONO).move_to([3.7, -0.4, 0])
            self.play(Transform(fbox, SurroundingRectangle(glyphs(code3, 0, 3, 9), buff=0.07,
                                                           corner_radius=0.06, color=S.WHITE,
                                                           stroke_width=2.5)),
                      TransformFromCopy(glyphs(code3, 0, 3, 16), call), run_time=0.7)
            anims = []
            for i in EX_WIN_ORDER:
                m = b3.mark_at(i, EX_WIN[i], scale=0.48).set_z_index(2)
                mark_on[i] = m
                anims.append(ReplacementTransform(dot_at.pop(i), m))
            self.play(LaggedStart(*anims, lag_ratio=0.25), run_time=0.9)

            # for each line: squares a, b, c
            vo.wait_until("checks every line")
            bar = code_bar(code3, 1)
            forlab = S.text("for each line: squares a, b, c", 26, S.WHITE)
            forlab.next_to(code3.code_lines[1], RIGHT, buff=0.85)
            forarrow = Arrow(forlab.get_left(), code3.code_lines[1].get_right(), buff=0.2,
                             color=S.WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.3)
            band = VGroup(*[b3.square(i, S.WHITE, 0.16) for i in WIN_LINES[0]]).set_z_index(1)
            tags = VGroup(*[outlined(S.text(ch, 22, S.WHITE, font=S.FONT_SANS)).move_to(tag_pos(i))
                            for ch, i in zip("abc", WIN_LINES[0])]).set_z_index(3)
            self.play(FadeOut(VGroup(fbox, flab, farrow)), FadeIn(bar), GrowArrow(forarrow),
                      FadeIn(forlab, shift=LEFT * 0.2), FadeIn(band), FadeIn(tags, scale=0.6), run_time=0.7)

            crosses = VGroup()

            def to_line(line, rt):
                self.play(*[band[j].animate.move_to(b3.center_of(line[j])) for j in range(3)],
                          *[tags[j].animate.move_to(tag_pos(line[j])) for j in range(3)], run_time=rt)

            def reject(line, rt, *extra):
                x = cross(line)
                crosses.add(x)
                self.play(FadeIn(x, scale=1.6), *extra, run_time=rt)

            notsame = S.text("not all the same", 24, S.GREY)
            notsame.next_to(cross(WIN_LINES[0]), RIGHT, buff=0.2)
            reject(WIN_LINES[0], 0.4, FadeIn(notsame, shift=LEFT * 0.1))           # . X O

            # same mark? (==)
            vo.wait_until("If all three squares")
            eq_op = glyphs(code3, 2, 26, 28)
            eq_boxes = VGroup(*[op_box(glyphs(code3, 2, i, i + 2)) for i in (26, 36)])
            eq_leg = VGroup(eq_op.copy().scale(1.3), S.text("is the same as", 26, S.WHITE)) \
                .arrange(RIGHT, buff=0.25).move_to([(eq_boxes[0].get_x() + eq_boxes[1].get_x()) / 2, 0.42, 0])
            self.play(Transform(bar, code_bar(code3, 2)), Create(eq_boxes),
                      TransformFromCopy(eq_op, eq_leg[0]), FadeIn(eq_leg[1], shift=UP * 0.1), run_time=0.7)
            to_line(WIN_LINES[1], 0.3)
            reject(WIN_LINES[1], 0.25)                                              # . X .
            to_line(WIN_LINES[2], 0.3)
            reject(WIN_LINES[2], 0.25, FadeOut(notsame))                            # . X O

            # a line of dots: all the same... but they are dots
            to_line(WIN_LINES[3], 0.35)                                             # . . .
            self.play(LaggedStart(*[Indicate(dot_at[i], color=S.WHITE, scale_factor=2.4)
                                    for i in WIN_LINES[3]], lag_ratio=0.25), run_time=0.8)
            vo.wait_until("and that mark")
            ne_op = glyphs(code3, 2, 10, 12)
            ne_box = op_box(ne_op)
            ne_leg = VGroup(ne_op.copy().scale(1.3), S.text("is not", 26, S.WHITE)) \
                .arrange(RIGHT, buff=0.25).move_to([ne_box.get_x(), 0.42, 0])
            self.play(Create(ne_box), TransformFromCopy(ne_op, ne_leg[0]),
                      FadeIn(ne_leg[1], shift=UP * 0.1), run_time=0.6)
            onlydots = S.text("only dots", 24, S.GREY)
            onlydots.next_to(cross(WIN_LINES[3]), LEFT, buff=0.2)
            reject(WIN_LINES[3], 0.4, FadeIn(onlydots, shift=RIGHT * 0.1))

            # X X X: a winner (the scanner moves on first, the line lights as it is spoken)
            assert WIN_LINES[4] == WIN_AT
            to_line(WIN_AT, 0.3)                                                    # X X X
            vo.wait_until("that player has won")
            win = b3.win_line(WIN_AT[0], WIN_AT[2], stroke=9).set_z_index(2)
            hand = Arrow(call.get_bottom(), call.get_bottom() + DOWN * 0.8, buff=0.08, color=S.GREY,
                         stroke_width=4, max_tip_length_to_length_ratio=0.3)
            hands_lab = S.text("hands back", 24, S.GREY).next_to(hand, RIGHT, buff=0.15)
            out = S.text('"X"', 40, X_COLOR, font=MONO).next_to(hand, DOWN, buff=0.15)
            self.play(band.animate.set_fill(WIN_COLOR, 0.3), Create(win),
                      Transform(bar, code_bar(code3, 3)), run_time=0.6)
            self.play(GrowArrow(hand), FadeIn(hands_lab),
                      FadeTransform(mark_on[WIN_AT[0]].copy(), out, path_arc=-PI / 4), run_time=0.8)
            self.play(Indicate(out, color=X_COLOR, scale_factor=1.25), run_time=0.4)

            # a board with no line: X's last mark moves, the scanner finds nothing -> None
            vo.wait_until("If no line matches")
            self.play(FadeOut(VGroup(crosses, onlydots, win)), out.animate.set_opacity(0.25),
                      *[band[j].animate.set_fill(S.WHITE, 0.16).move_to(b3.center_of(WIN_LINES[0][j]))
                        for j in range(3)],
                      *[tags[j].animate.move_to(tag_pos(WIN_LINES[0][j])) for j in range(3)],
                      Transform(bar, code_bar(code3, 1)),
                      mark_on[7].animate(path_arc=PI / 3).move_to(b3.center_of(5)),
                      dot_at[5].animate(path_arc=PI / 3).move_to(b3.center_of(7)), run_time=0.9)
            assert "".join("X" if i in (1, 4, 5) else "O" if i in (2, 8) else "." for i in range(9)) == EX_NONE
            reject(WIN_LINES[0], 0.12)
            for line in WIN_LINES[1:]:
                to_line(line, 0.13)
                reject(line, 0.11)
            nothing = VGroup(S.text("nothing found → None (nobody)", 26, S.GREY))
            nothing.add_to_back(SurroundingRectangle(nothing[0], buff=0.18, corner_radius=0.12,
                                                     color=S.GREY, stroke_width=2))
            nothing.move_to(out)
            vo.wait_until("hands back None")
            self.play(FadeOut(band), FadeOut(tags), FadeOut(bar), FadeTransform(out, nothing), run_time=0.6)
            vo.wait_until("which means nobody")
            self.play(tick(strip[2]), Indicate(nothing[1], color=S.GREY, scale_factor=1.06), run_time=0.7)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
