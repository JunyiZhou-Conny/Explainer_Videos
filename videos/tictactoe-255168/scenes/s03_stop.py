"""S03 · Games stop early.

Beats: a real game stops when X wins on move 5, so the 4 empty squares are never played (GREY
dashed ghost moves 6-9) -> the ghost moves shuffle through all 24 orders while a GREEN tally under
the board counts them 1..24: this 1 game was counted 24 times in 362,880 ("ghost games" = made-up
moves after someone already won) -> a timeline of moves 1-9: X's 3rd mark is move 5 -> ponder
(hints arrive one by one): how many games does X win on move 5? -> three steps on the
board: 8 lines, 3 x 2 x 1 = 3! = 6 orders of X's marks, 6 x 5 places for O's marks (O hops between
neighbouring squares) -> 8 x 6 x 30 = 1,440. In steps 2 and 3 the GREEN running counts sit under
the board ('orders shown: n', 'places for first/second O: n'), and the formula's result is written
only after they are done.
"""

import itertools

import numpy as np
from manim import *
from math import factorial  # after the star import, so nothing shadows it

from explainer import i18n
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
# The ghost shuffle swaps neighbours along this walk through the empty squares
# (3 -6 -7 -5: down, right, diagonal up), so no ghost ever jumps across the board over a real mark.
GHOST_WALK = (3, 6, 7, 5)
# O's marks hop between neighbouring squares only (step 3); both tours start at square 3.
O1_TOUR = (3, 6, 7, 8, 5, 4)    # O's first mark: the 6 squares X did not use, ends in the center
O2_TOUR = (3, 6, 7, 8, 5)       # O's second mark: the 5 squares left, ends at square 5


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
    assert sorted(GHOST_WALK) == sorted(GHOST_SQUARES)
    # step 3: X holds the top row; O's tours cover exactly the free squares, one neighbour at a time
    assert sorted(O1_TOUR) == [3, 4, 5, 6, 7, 8] and sorted(O2_TOUR) == [3, 5, 6, 7, 8]
    for tour in (O1_TOUR, O2_TOUR):
        assert all(abs(a // 3 - b // 3) + abs(a % 3 - b % 3) == 1 for a, b in zip(tour, tour[1:]))
    # the board at the end of step 3 is a legal game X wins on move 5:
    # X labels 5-3-1 on squares 0-2 (so X1@2, X3@1, X5@0), O2 at O1_TOUR[-1], O4 at O2_TOUR[-1]
    b = ["."] * 9
    for i, sym in [(2, "X"), (O1_TOUR[-1], "O"), (1, "X"), (O2_TOUR[-1], "O"), (0, "X")]:
        assert b[i] == "." and winner(b) is None
        b[i] = sym
    assert winner(b) == "X"


_check_numbers()


# ------------------------------------------------------------------ helpers
# Phrase times are estimated per sentence from character counts. Where that estimate is off by more
# than ~0.4 s, the anchor gets a `shift` measured from the pauses in this narration's audio
# (e.g. a spoken "362,880" lasts ~3 s but is only 7 characters).
# The shifts belong to the English audio: a language version (explainer.i18n) ignores them, and its
# narration anchors point at the words the animation goes with instead.
def wait_for(scene, vo, phrase: str, shift: float = 0.0) -> None:
    """vo.wait_until(phrase), moved by `shift` seconds."""
    if i18n.active():
        shift = 0.0
    t = vo.time_until(phrase) + shift
    if t > 1 / 30:
        scene.wait(t)


def until(vo, phrase: str, shift: float = 0.0, minimum: float = 0.3) -> float:
    """Seconds from now until `phrase` (+ shift) is spoken."""
    if i18n.active():
        shift = 0.0
    return max(minimum, vo.time_until(phrase) + shift)


def play_steps(scene, steps, events=(), on_land=None) -> None:
    """Play steps [(make_anims, move_time, hold_time), ...] back to back.

    make_anims is a function that builds the step's animations; it is called right before the step
    plays. (Building `.animate` ahead of time does not work for a mobject that moves in several
    steps: each `.animate` overwrites the mobject's one `.target`, so every step would jump to the
    last step's position.)

    events: [(t, anims)] with t in seconds from now; each event's anims join the step (or hold)
    that is running when t comes up. on_land(k) is called right after step k's motion lands.

    Each play lasts a whole number of frames and is timed to end at its planned moment, so many
    short steps don't drift late (a play always rounds its run time up to whole frames)."""
    events = sorted(events, key=lambda e: e[0])
    fps = config.frame_rate
    t0 = scene.renderer.time

    def run(anims, end):          # play `anims` (or wait) so that they end at t0 + end
        frames = max(1, round((t0 + end - scene.renderer.time) * fps))
        run_time = (frames - 0.5) / fps          # -> exactly `frames` frames
        if anims:
            scene.play(*anims, run_time=run_time)
        else:
            scene.wait(run_time)

    t = 0.0
    for k, (make_anims, dt, hold) in enumerate(steps):
        anims = list(make_anims())               # built now, from where things are now
        while events and events[0][0] <= t + dt / 2:
            anims += events.pop(0)[1]
        t += dt
        run(anims, t)
        if on_land is not None:
            on_land(k)
        if hold > 0:
            extra = []
            while events and events[0][0] <= t + hold / 2:
                extra += events.pop(0)[1]
            t += hold
            run(extra, t)
    for _, anims in events:   # anything the steps finished before
        scene.play(*anims, run_time=0.3)


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


def moves_to(moves, path_arc: float):
    """A step for play_steps: moves = [(mobject, point), ...], each travels along an arc to its point.
    The `.animate`s are made only when the step plays."""
    return lambda: [m.animate(path_arc=path_arc).move_to(p) for m, p in moves]


def count_tex(k: int, at, size: float = 44) -> MathTex:
    return S.math(str(k), size=size, color=COUNT_COLOR).move_to(at)


def text_t2c(s: str, size: float, color, t2c: dict, **kw) -> Text:
    """S.text(s, size, color, t2c=t2c, **kw). Pango lays out each t2c run on its own, and in CJK
    text a run of only Latin letters or digits (the 'X' of 'X 在第 5 步赢了', the '24' of a
    counter) sits ~0.05-0.08 units above the line; a language version copies the colours onto
    the same text laid out in one piece."""
    t = S.text(s, size, color, t2c=t2c, **kw)
    if not (i18n.active() and i18n.has_cjk(t.text)):
        return t
    plain = S.text(s, size, color, **kw)
    assert len(plain) == len(t), (t.text, len(plain), len(t))
    for g, c in zip(plain, t):
        g.set_color(c.get_color())
    return plain


def ghost_tally(k: int, left) -> Text:
    """'ghost endings counted: k' (k GREEN), its left end at `left`, so the words stay put as k grows."""
    return text_t2c(f"ghost endings counted: {k}", 26, S.GREY, {str(k): COUNT_COLOR}) \
        .move_to(left, aligned_edge=LEFT)


def board_tally(words: str, k: int, left, t2c=None) -> Text:
    """'words: k' (k GREEN) for a count kept under the board, away from the formula line (where
    '3 × 2   3' would read as a wrong product); its left end at `left`, so the words stay put."""
    t = text_t2c(f"{words}: {k}", 26, S.GREY, t2c or {})
    t[-len(str(k)):].set_color(COUNT_COLOR)       # the number's glyphs (Text has no glyphs for spaces)
    return t.move_to(left, aligned_edge=LEFT)


def card_lines(question: Text) -> list[VGroup]:
    """The glyphs of a multi-line Text, one VGroup per line (glyph counts can differ from character
    counts, e.g. the 'fi' ligature, so lines are found by where each glyph sits)."""
    lines, y_line = [], None
    for g in question:
        y = g.get_center()[1]
        if y_line is None or y_line - y > 0.25:      # dropped to the next line
            lines.append(VGroup())
            y_line = y
        lines[-1].add(g)
    return lines


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
        caption = text_t2c("X wins on move 5", 32, S.WHITE, {"X": X_COLOR})
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
        tag2 = text_t2c("24 times in 362,880", 32, S.WHITE, {"24": COUNT_COLOR, "362,880": COUNT_COLOR})
        tag = VGroup(tag1, tag2).arrange(DOWN, buff=0.18).move_to([PANEL_X, -1.75, 0])
        ghost_label = S.text("ghost games", 38, GHOST_COLOR)
        ghost_def = S.text("made-up moves after someone already won", 26, GHOST_COLOR)

        with self.voiceover(SAY[1]) as vo:
            self.play(VGroup(board, marks, nums, win, ghosts, caption, never).animate.shift(
                BOARD_LEFT - board.get_center()), run_time=1.0)
            self.play(Write(top), FadeIn(top_cap, shift=UP * 0.1), run_time=1.0)
            # "counted those missing moves": the ghost moves and their label pulse
            wait_for(self, vo, "counted those", shift=2.2)
            self.play(Indicate(never, color=S.WHITE, scale_factor=1.15),
                      *[Indicate(g[0], color=S.WHITE, scale_factor=1.12) for g in ghosts], run_time=1.0)
            # "as if the players kept going": the ghost moves get played, 6, 7, 8, 9
            wait_for(self, vo, "as if the players", shift=1.3)
            self.play(LaggedStart(*[Indicate(g, color=S.WHITE, scale_factor=1.25) for g in ghosts],
                                  lag_ratio=0.55), run_time=2.0)

            # the 4 ghost moves shuffle through all 24 orders while a GREEN tally under the board
            # counts them; the formula on the right only gets its "= 24" once the tally is done
            vo.wait_until("The 4 empty")
            tally_at = ghost_tally(24, ORIGIN).next_to(never, DOWN, buff=0.2).get_left()   # centred at 24
            tally = ghost_tally(1, tally_at)
            self.play(FadeIn(ways_cap, shift=DOWN * 0.1), FadeIn(tally, shift=UP * 0.1), run_time=0.5)
            # every order is one swap of two neighbouring ghosts away from the last (plain changes);
            # perms[k][p] says which ghost sits at walk spot p (ghost order = GHOST_SQUARES order)
            start = [GHOST_SQUARES.index(sq) for sq in GHOST_WALK]
            spot = [board.center_of(sq) for sq in GHOST_WALK]
            offset = [g.get_center() - board.center_of(sq) for g, sq in zip(ghosts, GHOST_SQUARES)]
            perms = plain_changes(4)
            # the tally reaches 24 as "24 ways" is spoken; the factors appear as they are spoken.
            # The first swaps are slow enough to follow, then the shuffle speeds up.
            budget = until(vo, "so 24 ways", -0.1)
            base = [max(0.17, 0.45 * 0.9 ** k) for k in range(len(perms) - 1)]
            durations = [d * budget / sum(base) for d in base]
            steps = []
            for k in range(1, len(perms)):
                prev, cur = perms[k - 1], perms[k]
                moved = [p for p in range(4) if prev[p] != cur[p]]
                arc = 0.35 * PI if moved == [2, 3] else 0.5 * PI     # 7 <-> 5 is the diagonal swap
                d = durations[k - 1]
                hold = 0.25 * d if d > 0.3 else 0.0                    # the slow first swaps settle
                steps.append((moves_to([(ghosts[start[cur[p]]], spot[p] + offset[start[cur[p]]])
                                        for p in moved], arc), d - hold, hold))
            factor_events = [(until(vo, "4 times 3", -0.9, 0), [FadeIn(formula[0], shift=DOWN * 0.1)]),
                             (until(vo, "3 times 2", -0.95, 0), [FadeIn(formula[1:3], shift=DOWN * 0.1)]),
                             (until(vo, "2 times 1", -1.0, 0), [FadeIn(formula[3:5], shift=DOWN * 0.1)]),
                             (until(vo, "times 1,", -0.6, 0), [FadeIn(formula[5:7], shift=DOWN * 0.1)])]
            play_steps(self, steps, factor_events,
                       on_land=lambda k: tally.become(ghost_tally(k + 2, tally_at)))
            # the tally has reached 24: it leaves, then "= 24" is written (24 is never on screen twice)
            self.play(FadeOut(tally, shift=DOWN * 0.1), run_time=0.3)
            self.play(FadeIn(formula[7]), FadeIn(formula[8], scale=1.5), run_time=0.45)

            # this one real game was counted 24 times
            vo.wait_until("So this one game")
            arrow = Arrow(tag1.get_left() + LEFT * 0.1, board.get_right() + RIGHT * 0.15 + DOWN * 0.45,
                          buff=0.05, color=S.GREY, stroke_width=4, max_tip_length_to_length_ratio=0.15)
            self.play(FadeIn(tag1, shift=UP * 0.1), GrowArrow(arrow),
                      TransformFromCopy(formula[8], tag2[0:2]),
                      Indicate(top, color=COUNT_COLOR, scale_factor=1.12),     # "...in 362,880" (the one up top)
                      FadeIn(tag2[2:]), run_time=1.2)

            # those made-up endings are ghost games: the label (with what it means) stays under the
            # board, next to the dashed ghost moves, until the next block
            vo.wait_until("Let's call")
            ghost_label.next_to(board, DOWN, buff=0.22).align_to(board, LEFT)
            ghost_def.next_to(ghost_label, DOWN, buff=0.14, aligned_edge=LEFT)
            self.play(LaggedStart(*[Wiggle(g, scale_value=1.15) for g in ghosts], lag_ratio=0.15),
                      FadeTransform(never, ghost_label, rate_func=squish_rate_func(smooth, 0.4, 1.0)),
                      run_time=1.2)
            self.play(FadeIn(ghost_def, shift=UP * 0.1), run_time=0.5)

            # count each real game only once: the right-hand panel leaves first, then the goal comes in
            vo.wait_until("We want")
            goal = VGroup(S.text("count each real game", 34, S.WHITE),
                          S.text("only once", 44, COUNT_COLOR)).arrange(DOWN, buff=0.25) \
                .move_to([PANEL_X, 0.2, 0])
            self.play(FadeOut(VGroup(top, top_cap, ways_cap, formula, tag, arrow), shift=UP * 0.3),
                      run_time=0.5)
            self.play(FadeIn(goal, shift=UP * 0.3), run_time=0.6)
            self.play(LaggedStart(*[Indicate(n, scale_factor=1.5) for n in nums], lag_ratio=0.25),
                      run_time=1.2)

        # ============================================================== 3. when can a game end?
        slots = timeline_strip(y=0.35)
        hl5 = highlight_box(slots[4], color=WIN_COLOR, buff=0.08)
        third = text_t2c("X's 3rd mark: move 5", 30, S.WHITE, {"X's 3rd mark": X_COLOR})
        third.next_to(hl5, UP, buff=0.75)
        third_arrow = Arrow(third.get_bottom(), hl5.get_top(), buff=0.08, color=WIN_COLOR,
                            stroke_width=4, max_tip_length_to_length_ratio=0.3)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(goal, shift=UP * 0.3), FadeOut(caption), FadeOut(ghosts, scale=0.6),
                      FadeOut(VGroup(ghost_label, ghost_def)), run_time=0.5)
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
            self.wait(0.5)                                # "1", "3" and "5" are spoken ~0.6 s apart
            self.play(LaggedStart(*[AnimationGroup(
                s[0].animate.set_fill(X_COLOR, 0.3).set_stroke(X_COLOR, 3),
                Indicate(s[1], color=X_COLOR, scale_factor=1.3),
                Indicate(n, color=X_COLOR, scale_factor=1.7)) for s, n in zip(x_slots, x_nums)],
                lag_ratio=0.6), run_time=2.1)
            wait_for(self, vo, "so the fifth move", shift=1.0)
            self.play(FadeIn(third, shift=DOWN * 0.15), GrowArrow(third_arrow),
                      Indicate(marks[4], color=WIN_COLOR, scale_factor=1.2), run_time=0.9)
            # the timeline slides down as the sentence ends, making room for the ponder card
            strip = VGroup(slots, hl5, third, third_arrow)
            wait_for(self, vo, "three marks", shift=-0.3)
            self.play(strip.animate.shift(DOWN * (slots.get_top()[1] + 2.15)), run_time=0.9)

        # ============================================================== 4. ponder
        # The card comes in on "Pause" with just the question; during the silent timer the hints
        # come in one at a time, so the wait keeps giving something new.
        card = ponder_card("How many games end with X winning on move 5?\nHint: (1) Which line?\n"
                           "(2) In what order does X fill it?\n(3) Where can O's 2 marks go?",
                           width=8.4, size=26).move_to([PANEL_X, 1.6, 0])
        q_lines = card_lines(card[2])                  # question, hint (1), hint (2), hint (3)
        assert len(q_lines) == 4
        card_top = VGroup(card[0], card[1], q_lines[0], card[3])   # frame, header, question, timer
        with self.voiceover(SAY[3]) as vo:
            vo.wait_until("Pause")
            self.play(FadeIn(card_top, scale=0.95), run_time=0.6)
            self.play(Indicate(win, color=WIN_COLOR, scale_factor=1.1), run_time=0.8)
            vo.wait_until("Try to count")
            self.play(Indicate(VGroup(marks[0], marks[2], marks[4]), color=X_COLOR, scale_factor=1.15),
                      run_time=0.8)
        # the timer bar drains over the whole ponder; hints (1), (2), (3) arrive along the way
        ponder, hint_at = 20.0, (4.0, 9.0, 14.0)
        bar = card[3]
        full, bar_start = bar.copy(), bar.get_start()
        times = (0.0, *hint_at, ponder)
        for k, (a, b) in enumerate(zip(times, times[1:])):
            left = full.copy().scale(max(0.001, 1 - b / ponder), about_point=bar_start)
            anims = [bar.animate(rate_func=linear).become(left)]
            if k > 0:
                anims.append(FadeIn(q_lines[k], shift=RIGHT * 0.15,
                                    rate_func=squish_rate_func(smooth, 0, 0.7 / (b - a))))
            self.play(*anims, run_time=b - a)
        self.remove(card_top, *q_lines[1:])            # the whole card is on screen now:
        self.add(card)                                 # hand it over as one mobject

        # ============================================================== 5. three steps -> 1,440
        heads = VGroup(S.text("(1) Which line?", 28), S.text("(2) In what order does X fill it?", 28),
                       S.text("(3) Where can O's 2 marks go?", 28))
        r1 = colour_parts(S.math("8", r"\text{ lines}", size=44), green=(0,))
        r2 = colour_parts(S.math("3", r"\times", "2", r"\times", "1", "=", "3!", "=", "6", size=44),
                          green=(8,))     # "which is 3 factorial" (S02 wrote 9! as "nine factorial")
        r3 = colour_parts(S.math("6", r"\times", "5", "=", "30", size=44), green=(0, 2, 4))
        rows = VGroup(*[VGroup(h, r) for h, r in zip(heads, (r1, r2, r3))])
        for h, r in rows:
            r.next_to(h, DOWN, buff=0.22, aligned_edge=LEFT).shift(RIGHT * 0.45)
        rows.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([PANEL_X - 0.35, 1.05, 0])
        heads.set_color(S.GREY)
        sep = Line(LEFT * 3.3, RIGHT * 3.3, color=S.GREY_DARK, stroke_width=2) \
            .move_to([PANEL_X, rows.get_bottom()[1] - 0.4, 0])
        final = colour_parts(S.math("8", r"\times", "6", r"\times", "30", "=", r"1{,}440",
                                    r"\ \ \text{games}", size=54), green=(0, 2, 4, 6))
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

            # (2) X fills that line: 3 x 2 x 1 = 3! = 6 orders
            vo.wait_until("Second, X fills")
            self.play(FadeOut(VGroup(*lines[1:])), lines[0].animate.set_stroke(opacity=1),
                      heads[0].animate.set_color(S.GREY), heads[1].animate.set_color(S.WHITE),
                      run_time=0.5)
            orders = list(itertools.permutations((1, 3, 5)))   # move labels on squares 0, 1, 2
            xs = VGroup(*[board.mark_at(i, "X", scale=MARK_SCALE) for i in (0, 1, 2)])
            labels = {n: move_number(board, i, n, "X") for i, n in zip((0, 1, 2), orders[0])}
            # the GREEN count of orders shown sits under the board, not on the formula line
            # (where "3 × 2 × 1   4" read like a wrong answer); its words are centred at 6
            order_at = board_tally("orders shown", 6, ORIGIN).next_to(board, DOWN, buff=0.35).get_left()
            c2 = board_tally("orders shown", 1, order_at)
            self.play(LaggedStart(*[mark_anim(x) for x in xs], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(labels[n], scale=0.6) for n in orders[0]], lag_ratio=0.3),
                      FadeIn(c2, shift=UP * 0.1), run_time=0.8)
            # the labels go through the other 5 orders (each one lands, then holds a moment) while
            # "3 times 2 times 1" writes itself; the count lands on 6 as "which is 3 factorial" starts
            # (each step moves the 2 or 3 labels whose square changes; built lazily, see play_steps)
            dt = until(vo, "which is 3", 0.2) / (len(orders) - 1)
            steps = [(moves_to([(labels[n], corner(board, cur.index(n)))
                                for n in cur if cur.index(n) != prev.index(n)], -0.45 * PI),
                      0.6 * dt, 0.4 * dt)
                     for prev, cur in zip(orders, orders[1:])]
            events = [(until(vo, "3 times 2", -0.4, 0), [FadeIn(r2[0], shift=DOWN * 0.1)]),
                      (until(vo, "2 times 1", -0.45, 0), [FadeIn(r2[1:3], shift=DOWN * 0.1)]),
                      (until(vo, "times 1,", 0.0, 0), [FadeIn(r2[3:5], shift=DOWN * 0.1)])]
            play_steps(self, steps, events,
                       on_land=lambda k: c2.become(board_tally("orders shown", k + 2, order_at)))
            # all 6 orders shown: the count leaves as "= 3!" is written, then "= 6" on "so 6 orders"
            # (6 is never on screen twice)
            self.play(FadeOut(c2, shift=DOWN * 0.1), FadeIn(r2[5:7], shift=DOWN * 0.1), run_time=0.5)
            wait_for(self, vo, "so 6 orders", -0.2)
            self.play(FadeIn(r2[7]), FadeIn(r2[8], scale=1.5),
                      Indicate(VGroup(*labels.values()), scale_factor=1.3), run_time=0.6)

            # (3) O's 2 marks: 6 x 5 = 30
            vo.wait_until("Third, O")
            self.play(heads[1].animate.set_color(S.GREY), heads[2].animate.set_color(S.WHITE), run_time=0.4)
            dots = VGroup()
            # the GREEN counts of places sit under the board, one line per O mark (the first O's
            # 6 stays up while the second O's count goes 1..5); "6 × 5 = 30" is written on the
            # formula line only once both are done
            o_words = ("places for first O", "places for second O")
            o_colors = {"O": O_COLOR}
            o_left = board_tally(o_words[1], 5, ORIGIN, o_colors).next_to(board, DOWN, buff=0.35).get_left()
            o_at = (o_left, o_left + DOWN * 0.45)

            def o_tally(j, k):
                return board_tally(o_words[j], k, o_at[j], o_colors)

            def hop_through(squares, n, j, budget):
                """O's mark n starts on squares[0] and hops to each next (neighbouring) square,
                leaving an ORANGE dot where it was; its GREEN count (line j) ticks as it lands."""
                o = VGroup(board.mark_at(squares[0], "O", scale=MARK_SCALE),
                           move_number(board, squares[0], n, "O"))
                off = o.get_center() - board.center_of(squares[0])
                c = o_tally(j, 1)
                self.play(Create(o[0]), FadeIn(o[1], scale=0.6), FadeIn(c, shift=UP * 0.1), run_time=0.45)
                dt = min(0.6, max(0.3, (budget - 0.45) / (len(squares) - 1)))
                for k, sq in enumerate(squares[1:], start=2):
                    dot = Dot(board.center_of(squares[k - 2]), radius=0.08, color=O_COLOR).set_opacity(0.7)
                    dots.add(dot)
                    self.play(o.animate(path_arc=-0.35 * PI).move_to(board.center_of(sq) + off),
                              FadeIn(dot, scale=0.5), run_time=dt)
                    c.become(o_tally(j, k))
                return o, c

            _, c3a = hop_through(O1_TOUR, 2, 0, until(vo, "and O's second", -0.7) - 0.4)
            self.play(FadeOut(dots), Indicate(c3a[-1], color=COUNT_COLOR, scale_factor=1.3), run_time=0.4)
            dots.remove(*dots.submobjects)
            wait_for(self, vo, "and O's second", -0.7)
            _, c3b = hop_through(O2_TOUR, 4, 1, until(vo, "6 times 5", -1.1) - 0.3)
            # both counts are done: they leave as "6 × 5" is written (each number as it is spoken),
            # then "= 30"
            wait_for(self, vo, "6 times 5", -1.1)
            self.play(FadeOut(VGroup(c3a, c3b), shift=DOWN * 0.1), FadeOut(dots),
                      LaggedStart(*[FadeIn(p, shift=DOWN * 0.1) for p in r3[0:3]], lag_ratio=0.35),
                      run_time=0.8)
            wait_for(self, vo, "is 30", -0.5)
            self.play(FadeIn(r3[3:5], shift=LEFT * 0.1), run_time=0.6)

            # multiply: 8, 6 and 30 fly down as they are spoken
            vo.wait_until("Multiply")
            self.play(heads[2].animate.set_color(S.GREY), Create(sep), run_time=0.4)
            vo.wait_until("8 times 6")
            self.play(LaggedStart(TransformFromCopy(r1[0], final[0]),
                                  AnimationGroup(FadeIn(final[1]), TransformFromCopy(r2[8], final[2])),
                                  AnimationGroup(FadeIn(final[3]), TransformFromCopy(r3[4], final[4])),
                                  lag_ratio=0.4), run_time=1.4)
            wait_for(self, vo, "is 1,440", -0.45)
            self.play(Write(final[5:]), run_time=0.8)
            box = highlight_box(final[6], color=COUNT_COLOR, buff=0.08)
            self.play(Create(box), Indicate(final[6], color=COUNT_COLOR, scale_factor=1.15), run_time=0.6)

        self.wait(0.8)   # let the answer sit for a moment before the cut
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
