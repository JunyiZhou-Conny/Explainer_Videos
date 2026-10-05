"""S07 · Change one line.

Beats: explore() (same panel as S06) with the undo line struck through -> ponder -> the broken
program's exact trace: squares 0..6 fill in order and are never erased, X's 2-4-6 diagonal on
move 7 counts 1, then the X that was never erased lets X land on 7 and 8 too (2, 3) -> output 3
-> undo back, winner check struck through -> ponder -> 362,880 slides into "9! = 362,880", and a
quick replay of S03's game shows the ghost games coming back. The code is restored at the end.

Verified (running the program without the undo line): moves X0 O1 X2 O3 X4 O5 X6, counts at
XOXOXOX.., XOXOXOXX., XOXOXOXXX -> prints 3. Without the winner check it prints 362,880.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.scene import VoiceScene

from common import (COUNT_COLOR, GHOST_COLOR, NARRATION, NINE_FACTORIAL, O_COLOR, UNDO_COLOR,
                    WIN_COLOR, X_COLOR, Board, code_line, explore_code, line_highlight, mark_anim,
                    move_number, strike)

SAY = NARRATION["S07"]

MONO = "DejaVu Sans Mono"
COL_X = 4.1                       # centre of the right-hand column (code panel ends at x = 1.24)
ROW_Y = -2.45                     # bottom row: program output (left) and our own count (right)
CARD_X = 3.95                     # ponder cards sit in the right-hand column (x 1.3 .. 6.6)
WINNER_LINES, DRAW_LINES, UNDO_LINE, MOVE_LINE = (1, 2), (3, 4), 11, 8


# ------------------------------------------------------------------ helpers
def lines_bar(code, k0: int, k1: int, color: str = WIN_COLOR, opacity: float = 0.22) -> Rectangle:
    """One translucent bar covering code lines k0..k1 (inclusive)."""
    top, bot = line_highlight(code, k0, color, opacity), line_highlight(code, k1, color, opacity)
    y0, y1 = bot.get_bottom()[1], top.get_top()[1]
    return Rectangle(width=top.width, height=y1 - y0, stroke_width=0).set_fill(color, opacity) \
        .move_to([top.get_center()[0], (y0 + y1) / 2, 0])


def line_tag(code, k0: int, k1: int, s: str, color: str, size: float = 26) -> Text:
    """A big '<- label' just right of the code panel, pointing at lines k0..k1 (the code is small)."""
    y = (code_line(code, k0).get_center()[1] + code_line(code, k1).get_center()[1]) / 2
    return S.text("← " + s, size, color).move_to([code.get_right()[0] + 0.15, y, 0], aligned_edge=LEFT)


def side_ponder(scene, question: str, seconds: float, y: float, width: float = 5.3,
                size: float = 30) -> VGroup:
    """pause_and_ponder, but the card sits in the right-hand column so the code stays visible."""
    card = ponder_card(question, width=width, size=size).move_to([CARD_X, y, 0])
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return card


def out_value(s: str, color: str = COUNT_COLOR) -> Text:
    return S.text(s, 48, color, font=MONO)


def count_value(n: int) -> Text:
    return S.text(f"{n:,}", 48, COUNT_COLOR, font=S.FONT_SANS)


def corner_tag(board: Board, i: int, s: str, color: str, size: float = 26) -> Text:
    """A small tag where the move number goes (lower-right corner of square i)."""
    return S.text(s, size, color, font=S.FONT_SANS, weight="BOLD") \
        .move_to(board.center_of(i) + np.array([0.34, -0.34, 0]) * board.cell)


class Experiments(VoiceScene):
    def construct(self):
        code = explore_code()                         # same size and place as in S06
        undo_text = code_line(code, UNDO_LINE)

        heading1 = S.text("Experiment 1: delete the undo line", 30, S.WHITE)
        heading2 = S.text("Experiment 2: delete the winner check", 30, S.WHITE)
        for h in (heading1, heading2):
            h.next_to(code, UP, buff=0.45).align_to([-6.45, 0, 0], LEFT)
        heading0 = S.text("Break it on purpose!", 34, S.WHITE).move_to(heading1, aligned_edge=LEFT)

        # the program's output, under the program
        out_frame = RoundedRectangle(width=4.8, height=1.0, corner_radius=0.15,
                                     stroke_color=S.GREY_DARK, stroke_width=2).set_fill(S.GREY_DARKER, 1)
        out_frame.move_to([code.get_center()[0], ROW_Y, 0])
        out_label = S.text("output", 26, S.GREY, font=S.FONT_SANS) \
            .move_to(out_frame.get_left() + RIGHT * 0.85)
        out_anchor = out_label.get_right() + RIGHT * 0.45

        def place_out(v: Text) -> Text:
            return v.move_to(out_anchor, aligned_edge=LEFT).set_y(ROW_Y)

        out_q = place_out(out_value("?", S.WHITE))

        # ================================================================ beat 1: strike the undo line
        undo_bar = line_highlight(code, UNDO_LINE, UNDO_COLOR, 0.3)
        undo_strike = strike(code, UNDO_LINE)
        undo_tag = line_tag(code, UNDO_LINE, UNDO_LINE, "undo", UNDO_COLOR)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(code, shift=RIGHT * 0.3), run_time=1.0)
            vo.wait_until("break it on purpose")
            self.play(Write(heading0), run_time=0.9)
            vo.wait_until("Pause and ponder")
            self.play(FadeIn(undo_bar), Indicate(undo_text, color=UNDO_COLOR, scale_factor=1.04),
                      FadeIn(undo_tag, shift=LEFT * 0.2), run_time=0.8)
            self.play(FadeIn(out_frame), FadeIn(out_label), FadeIn(out_q, scale=0.6), run_time=0.6)
            vo.wait_until("delete the undo line")
            self.play(Create(undo_strike), undo_text.animate.set_opacity(0.35), FadeOut(undo_bar),
                      TransformMatchingShapes(heading0, heading1), run_time=0.9)
        # the card stays above the "undo" tag, so the struck line and its label stay visible
        card = side_ponder(self, "What happens if we\ndelete the undo line?", seconds=10, y=0.85)

        # ================================================================ beat 2: the broken program's trace
        board = Board(size=3.0).move_to([COL_X, 0.75, 0])
        fill = [(0, "X"), (1, "O"), (2, "X"), (3, "O"), (4, "X"), (5, "O"), (6, "X")]
        marks, nums = {}, {}

        def drop(i: int, sym: str, n: int | None, run_time: float = 0.5, extra=()):
            m = board.mark_at(i, sym, scale=0.5)
            marks[i] = m
            anims = [mark_anim(m), *extra]
            if n is not None:
                nums[i] = move_number(board, i, n, sym)
                anims.append(FadeIn(nums[i], scale=0.6))
            self.play(*anims, run_time=run_time)

        count_label = S.text("games counted", 26, S.WHITE)
        count = count_value(1)
        VGroup(count_label, count).arrange(RIGHT, buff=0.3).move_to([COL_X, ROW_Y, 0])
        count.set_y(ROW_Y)

        def bump(n: int) -> list:
            """Animations that roll the counter up to n (play them with the win check)."""
            nonlocal count
            new = count_value(n).move_to(count, aligned_edge=LEFT)
            anims = [FadeOut(count, shift=UP * 0.35), FadeIn(new, shift=UP * 0.35),
                     Flash(new.get_center(), color=COUNT_COLOR, line_length=0.18, flash_radius=0.45)]
            count = new
            return anims

        out_3 = place_out(out_value("3"))
        bar = line_highlight(code, MOVE_LINE)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            self.play(ReplacementTransform(out_q, out_3), run_time=0.6)
            self.play(Circumscribe(out_frame, color=COUNT_COLOR, buff=0.06), run_time=0.8)

            vo.wait_until("Without undo")
            self.play(LaggedStart(*[Create(ln) for ln in board], lag_ratio=0.15),
                      Indicate(undo_strike, color=UNDO_COLOR, scale_factor=1.15),
                      Indicate(undo_tag, color=UNDO_COLOR), run_time=0.9)

            vo.wait_until("The program plays")
            self.play(FadeIn(bar), FadeOut(undo_tag), run_time=0.3)
            for n, (i, sym) in enumerate(fill[:-1], start=1):
                drop(i, sym, n, run_time=0.5)
            vo.wait_until("until X makes")
            drop(6, "X", 7, run_time=0.5)
            win = board.win_line(2, 6)
            self.play(Create(win), run_time=0.6)
            self.play(Transform(bar, lines_bar(code, *WINNER_LINES)), run_time=0.5)

            vo.wait_until("That's 1")
            self.play(FadeIn(count_label, shift=UP * 0.2), FadeIn(count, scale=0.5), run_time=0.6)

            # X's other choices for move 7: the two squares still empty
            vo.wait_until("Then it tries")
            blink = VGroup(board.square(7, X_COLOR, 0.35), board.square(8, X_COLOR, 0.35)).set_z_index(-1)
            self.play(Transform(bar, line_highlight(code, MOVE_LINE)), FadeIn(blink), run_time=0.5)
            self.play(FadeOut(blink), run_time=0.4)
            self.play(FadeIn(blink), run_time=0.35)
            self.play(FadeOut(blink), run_time=0.35)

            # ...but nothing erased the X on square 6
            vo.wait_until("but the old X")
            stuck = board.square(6, UNDO_COLOR, 0.3).set_z_index(-1)
            still = S.text("still there", 24, UNDO_COLOR).next_to(board, DOWN, buff=0.22) \
                .set_x(board.center_of(6)[0])
            self.play(FadeIn(stuck), FadeIn(still, shift=UP * 0.15),
                      Indicate(marks[6], color=X_COLOR, scale_factor=1.25), run_time=0.8)

            # program order: X on 7 -> winner check -> count; X on 8 -> winner check -> count
            # (kept short so it ends before "The old diagonal ...", which then explains it)
            vo.wait_until("so X lands")
            tag7, tag8 = corner_tag(board, 7, "?!", UNDO_COLOR), corner_tag(board, 8, "?!", UNDO_COLOR)
            drop(7, "X", None, run_time=0.45, extra=[FadeOut(still), FadeIn(tag7, scale=0.5)])
            self.play(Indicate(win, color=WIN_COLOR, scale_factor=1.06),
                      Transform(bar, lines_bar(code, *WINNER_LINES)), *bump(2), run_time=0.55)
            self.play(Transform(bar, line_highlight(code, MOVE_LINE)), run_time=0.25)
            drop(8, "X", None, run_time=0.45, extra=[FadeIn(tag8, scale=0.5)])
            self.play(Indicate(win, color=WIN_COLOR, scale_factor=1.06),
                      Transform(bar, lines_bar(code, *WINNER_LINES)), *bump(3), run_time=0.55)

            vo.wait_until("The old diagonal")
            self.play(ShowPassingFlash(win.copy().set_stroke(S.WHITE, 16), time_width=0.5),
                      Indicate(bar, color=WIN_COLOR, scale_factor=1.0),
                      Indicate(VGroup(tag7, tag8), color=UNDO_COLOR, scale_factor=1.3), run_time=1.0)
            self.play(Indicate(win, color=WIN_COLOR, scale_factor=1.06), run_time=0.7)

            vo.wait_until("That's 3")
            self.play(Circumscribe(count, color=COUNT_COLOR, buff=0.1),
                      Circumscribe(out_3, color=COUNT_COLOR, buff=0.1), run_time=0.6)
            vo.wait_until("and the board is full")
            full = S.text("board full", 26, S.GREY).next_to(board, DOWN, buff=0.22)
            self.play(FadeIn(full, shift=UP * 0.15), FadeOut(bar),
                      Circumscribe(VGroup(board, *marks.values()), color=S.GREY, buff=0.12),
                      run_time=1.0)

        trace = VGroup(board, *marks.values(), *nums.values(), win, stuck, tag7, tag8, full,
                       count_label, count)

        # ================================================================ beat 3: undo back, winner check out
        out_q2 = place_out(out_value("?", S.WHITE))
        win_strikes = VGroup(*[strike(code, k) for k in WINNER_LINES])
        win_texts = VGroup(*[code_line(code, k) for k in WINNER_LINES])
        undo_back = line_highlight(code, UNDO_LINE, COUNT_COLOR, 0.3)
        draw_bar = lines_bar(code, *DRAW_LINES)
        win_tag = line_tag(code, *WINNER_LINES, "winner check", UNDO_COLOR)
        draw_tag = line_tag(code, *DRAW_LINES, "board full", S.WHITE)

        with self.voiceover(SAY[2]) as vo:
            # "Now put undo back": the strike comes off and the line lights up GREEN
            self.play(FadeOut(trace), ReplacementTransform(out_3, out_q2), Uncreate(undo_strike),
                      undo_text.animate.set_opacity(1), FadeIn(undo_back), run_time=0.8)
            vo.wait_until("and delete the winner")
            self.play(FadeOut(undo_back), TransformMatchingShapes(heading1, heading2), run_time=0.8)
            self.play(LaggedStart(*[Create(s) for s in win_strikes], lag_ratio=0.4),
                      win_texts.animate.set_opacity(0.35), FadeIn(win_tag, shift=LEFT * 0.2),
                      run_time=0.8)
            vo.wait_until("so games only stop")
            self.play(FadeIn(draw_bar), FadeIn(draw_tag, shift=LEFT * 0.2),
                      Indicate(VGroup(*[code_line(code, k) for k in DRAW_LINES]), color=S.WHITE,
                               scale_factor=1.04), run_time=0.9)
            vo.wait_until("Pause and predict")
            self.play(Indicate(out_q2, color=S.WHITE, scale_factor=1.3), run_time=0.7)
        # the card sits under the two tags, so the struck lines and their labels stay visible
        card = side_ponder(self, "Now delete the\nwinner check instead.\nWhat number comes out?\n"
                                 "(Hint: you've met it before!)", seconds=10, y=-1.7)

        # ================================================================ beat 4: 362,880 = nine factorial
        out_big = place_out(out_value(f"{NINE_FACTORIAL:,}"))
        eq = S.math("9!", "=", "362{,}880", size=60)
        eq[2].set_color(COUNT_COLOR)
        eq.move_to([COL_X, ROW_Y, 0])
        nf = S.text("nine factorial", 26, S.WHITE).next_to(eq[0], DOWN, buff=0.22)

        # S03's game (X wins on move 5), then the ghost moves that the program now plays anyway
        gboard = Board(size=2.4, stroke=5).move_to([COL_X, 1.1, 0])
        real = [(0, "X"), (4, "O"), (1, "X"), (8, "O"), (2, "X")]
        ghosts = [(3, "O"), (5, "X"), (6, "O"), (7, "X")]
        check = VGroup(S.math(r"\checkmark", size=48, color=COUNT_COLOR),
                       S.text("the ghost games are back", 28, COUNT_COLOR)).arrange(RIGHT, buff=0.2)
        check.next_to(gboard, DOWN, buff=0.45).set_x(COL_X)

        with self.voiceover(SAY[3]) as vo:
            # the tags make way for the ghost board; the strikes stay
            self.play(FadeOut(card), FadeOut(draw_bar), FadeOut(draw_tag), FadeOut(win_tag), run_time=0.4)
            # the output rolls over like a counter (a one-glyph "?" can't morph into seven digits)
            self.play(FadeOut(out_q2, shift=UP * 0.4), FadeIn(out_big, shift=UP * 0.4), run_time=0.6)
            self.play(Circumscribe(out_frame, color=COUNT_COLOR, buff=0.06), run_time=0.8)

            vo.wait_until("That's nine factorial")
            # the program's answer slides over and becomes the value of nine factorial
            self.play(Write(eq[:2]), out_big.animate.move_to(eq[2]), FadeOut(out_frame),
                      FadeOut(out_label), run_time=1.1)
            self.play(ReplacementTransform(out_big, eq[2]), FadeIn(nf, shift=UP * 0.15), run_time=0.5)

            vo.wait_until("Without the winner check")
            self.play(LaggedStart(*[Create(ln) for ln in gboard], lag_ratio=0.15),
                      Indicate(win_strikes, color=UNDO_COLOR, scale_factor=1.1), run_time=0.6)
            played = VGroup()
            for n, (i, sym) in enumerate(real, start=1):
                m = gboard.mark_at(i, sym, scale=0.5)
                num = move_number(gboard, i, n, sym, size=22)
                played.add(m, num)
                self.play(mark_anim(m), FadeIn(num, scale=0.6), run_time=0.28)
            gwin = gboard.win_line(0, 2, stroke=8)
            self.play(Create(gwin), run_time=0.4)
            for n, (i, sym) in enumerate(ghosts, start=6):     # keeps playing after the win
                g = gboard.ghost_at(i, sym, scale=0.5)
                num = move_number(gboard, i, n, sym, size=22).set_color(GHOST_COLOR).set_opacity(0.8)
                played.add(g, num)
                self.play(Create(g), FadeIn(num, scale=0.6), run_time=0.3)

            vo.wait_until("so it counts all")
            self.play(Write(check[0]), FadeIn(check[1], shift=UP * 0.15), run_time=0.8)

            vo.wait_until("It rediscovered")
            self.play(Circumscribe(VGroup(eq, nf), color=COUNT_COLOR, buff=0.15), run_time=1.0)

        # put the winner check back, so S08 can say "put every line back"
        self.play(Uncreate(win_strikes), win_texts.animate.set_opacity(1),
                  FadeOut(heading2, shift=UP * 0.2), run_time=0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
