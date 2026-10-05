"""S06 · Exploring every game.

Beats
1. explore() appears (lines 23-35, the shared S06/S07 panel): its name and `player` are boxed;
   small tags: "whose turn", range(9) "squares 0 to 8", the dimmed next_player line "switch
   turns", total += "add to the total".
2. The two stopping rules, each with a legal finished board: X wins (diagonal) -> "1 game";
   a full board with no line turns GREY -> "1 game (a draw)". The 1s fly out of `return 1`.
3. The loop on  . . . / X X O / O X O  (X to move): the empty squares blink, X drops into each,
   the board slides down to a smaller copy ("explore: how many games from here?"), the answers
   2, 1, 2 come back and `total +=` collects them in a GREEN counter: 5.
4. Worked example  X X O / O X . / X . O  (O to move) on one working board with a tiny tree of
   snapshots under it: O middle-right wins (1); a RED eraser takes it back; O bottom-middle, then X
   fills the last square: a GREY draw (1); 1 + 1 = 2 travels up to the root.
5. Recursion: explore(next_player) jumps back to `def explore`; a staircase of calls adds one mark
   each until a stopping rule fires. The staircase becomes the leftmost branch of the whole game
   tree (empty board on top, 9 first moves, 9 x 8 = 72 like S02, then a sampled fringe whose leaves
   end at different depths). explore walks down to its first leaf (X0 O1 X2 O3 X4 O5 X6, a real
   first game) with the side board filling up; the leaf flashes GREEN, "games counted" 1.
6. Undo (RED line): the side board becomes "one shared board" (a whiteboard); a close-up of the
   bottom of the branch; the eraser takes back X6, the path steps up, then goes down the next
   branches in explore's real order (X7 O6 X8 -> 2, then X7 O8 X6 -> 3).
   Caption: try -> explore -> undo = backtracking.

Every board and number is checked in _check() (runs on import).
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (COUNT_COLOR, DRAW_COLOR, EXPLORE_SOURCE, NARRATION, O_COLOR, UNDO_COLOR,
                    WIN_COLOR, X_COLOR, Board, code_line, explore_code, line_highlight,
                    mark_anim, winner)

SAY = NARRATION["S06"]
SRC = EXPLORE_SOURCE.splitlines()
MONO = "DejaVu Sans Mono"
TAG = 26

# ------------------------------------------------------------------ the boards of this scene
B2_WON = "XO.OX...X"      # X wins on move 5 with the 0-4-8 diagonal
B2_DRAW = "XOXXOOOXX"     # full, no line: a draw
B3 = "...XXOOXO"          # X to move; explore after X on 0, 1, 2 gives 2, 1, 2
B3_TRY = [0, 1, 2]
B3_ANS = [2, 1, 2]
B4 = "XXOOX.X.O"          # O to move; explore gives 2
PATH = [(0, "X"), (1, "O"), (2, "X"), (3, "O"), (4, "X"), (5, "O"), (6, "X")]   # explore's 1st game
NEXT1 = [(7, "X"), (6, "O"), (8, "X")]     # after undoing X6: the 2nd game explore finds
NEXT2 = [(8, "O"), (6, "X")]               # after undoing X8 and O6: the 3rd game


def put(cells: str, s: int, sym: str) -> str:
    return cells[:s] + sym + cells[s + 1:]


def explore_count(cells: str, player: str) -> int:
    """explore() from assets/play_all_games.py, started on `cells`."""
    b = list(cells)

    def ex(p):
        if winner(b) is not None:
            return 1
        if "." not in b:
            return 1
        t = 0
        for s in range(9):
            if b[s] == ".":
                b[s] = p
                t += ex("O" if p == "X" else "X")
                b[s] = "."
        return t

    return ex(player)


def first_games(n: int):
    """The first n finished games explore() reaches from the empty board, as move lists."""
    out, b, moves = [], ["."] * 9, []

    def ex(p):
        if len(out) >= n:
            return
        if winner(b) is not None or "." not in b:
            out.append(list(moves))
            return
        for s in range(9):
            if b[s] == ".":
                b[s] = p
                moves.append((s, p))
                ex("O" if p == "X" else "X")
                moves.pop()
                b[s] = "."

    ex("X")
    return out


def _check():
    def legal_no_win(c, to_move):
        nx, no = c.count("X"), c.count("O")
        return winner(list(c)) is None and (nx - no) == (1 if to_move == "O" else 0)

    assert winner(list(B2_WON)) == "X" and B2_WON.count("X") == B2_WON.count("O") + 1
    assert winner(list(B2_DRAW)) is None and "." not in B2_DRAW
    assert legal_no_win(B3, "X") and [c for c in range(9) if B3[c] == "."] == B3_TRY
    assert [explore_count(put(B3, s, "X"), "O") for s in B3_TRY] == B3_ANS
    assert winner(list(put(B3, 1, "X"))) == "X"                     # X on 1: column 1-4-7
    assert legal_no_win(B4, "O") and explore_count(B4, "O") == 2
    assert winner(list(put(B4, 5, "O"))) == "O"                     # O on 5: column 2-5-8
    full = put(put(B4, 7, "O"), 5, "X")
    assert winner(list(put(B4, 7, "O"))) is None and winner(list(full)) is None and "." not in full
    g = first_games(3)
    assert g[0] == PATH and g[1] == PATH[:6] + NEXT1 and g[2] == PATH[:6] + NEXT1[:1] + NEXT2


_check()

# ------------------------------------------------------------------ small helpers


def glyphs(code, k: int, token: str, nth: int = 0) -> VGroup:
    """The glyphs of `token` in line k of the explore() panel (glyphs skip spaces)."""
    line, tok = SRC[k].replace(" ", ""), token.replace(" ", "")
    start = -1
    for _ in range(nth + 1):
        start = line.index(tok, start + 1)
    return VGroup(*code.code_lines[k][start:start + len(tok)])


def lines_bar(code, k0: int, k1: int | None = None, color: str = WIN_COLOR,
              opacity: float = 0.22) -> Rectangle:
    """One translucent bar over code lines k0..k1 (inclusive)."""
    k1 = k0 if k1 is None else k1
    top, bot = line_highlight(code, k0, color, opacity), line_highlight(code, k1, color, opacity)
    y0, y1 = bot.get_bottom()[1], top.get_top()[1]
    x0 = max(top.get_left()[0], -6.58)          # the panel itself starts just off the safe area
    x1 = top.get_right()[0]
    return Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=0).set_fill(color, opacity) \
        .move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def line_tag(code, k: int, s: str, color: str = S.WHITE, dy: float = 0.0, size: float = TAG,
             **kw) -> Text:
    """'<- label' just right of the code panel, level with line k."""
    y = code_line(code, k).get_center()[1] + dy
    return S.text("← " + s, size, color, **kw).move_to([code.get_right()[0] + 0.15, y, 0],
                                                       aligned_edge=LEFT)


def token_box(m, color: str = WIN_COLOR) -> SurroundingRectangle:
    return SurroundingRectangle(m, color=color, buff=0.045, stroke_width=2.5, corner_radius=0.04)


def to_move(sym: str, size: float = 30) -> Text:
    return S.text(f"{sym} to move", size, S.WHITE, t2c={sym: X_COLOR if sym == "X" else O_COLOR})


def count_value(n: int, size: float = 48) -> Text:
    return S.text(f"{n:,}", size, COUNT_COLOR, font=S.FONT_SANS)


def drop(m, d: float = 0.3):
    """A mark dropping into its square."""
    return FadeIn(m, shift=DOWN * d, scale=1.15)


def snap(cells: str, size: float, center, stroke: float = 3, line=None) -> VGroup:
    """Board + marks (in square order) [+ YELLOW line]. Same structure for every size, so one
    board Transforms cleanly into a smaller or bigger copy of itself."""
    b = Board(size=size, stroke=stroke).move_to(center)
    ms = VGroup(*[b.mark_at(i, ch, 0.6, stroke=stroke + 1.5) for i, ch in enumerate(cells)
                  if ch in "XO"])
    g = VGroup(b, ms)
    if line is not None:
        g.add(b.win_line(*line, stroke=stroke + 3))
    g.board = b
    return g


def draw_board(scene, g: VGroup, run_time: float = 1.1, extra=()):
    """Grid lines, then the marks, of a snap() board."""
    scene.play(LaggedStart(*[Create(ln) for ln in g[0]], lag_ratio=0.15), *extra,
               run_time=run_time * 0.45)
    scene.play(LaggedStart(*[FadeIn(m, scale=0.7) for m in g[1]], lag_ratio=0.15),
               run_time=run_time * 0.55)


def make_eraser(w: float) -> VGroup:
    body = RoundedRectangle(width=w, height=w * 0.5, corner_radius=w * 0.09) \
        .set_fill(UNDO_COLOR, 1).set_stroke(S.WHITE, 1.5, 0.8)
    sleeve = Rectangle(width=w * 0.36, height=w * 0.5).set_fill(S.WHITE, 0.85).set_stroke(width=0) \
        .move_to(body).shift(RIGHT * w * 0.2)
    return VGroup(body, sleeve).rotate(25 * DEGREES)


def erase(scene, targets, center, cell: float, run_time: float = 0.7):
    """A RED eraser scrubs over a square while `targets` fade away."""
    c = np.array(center, dtype=float)
    offs = [(0.45, 0.32), (-0.28, 0.14), (0.28, 0.0), (-0.28, -0.14), (0.3, -0.3)]
    pts = [c + np.array([dx, dy, 0]) * cell for dx, dy in offs]
    e = make_eraser(max(0.32, cell * 0.8)).move_to(pts[0])
    path = VMobject().set_points_smoothly(pts)
    scene.play(FadeIn(e, scale=0.6), run_time=0.15)
    scene.play(MoveAlongPath(e, path, rate_func=linear), FadeOut(targets), run_time=run_time)
    scene.play(FadeOut(e, shift=UR * 0.15), run_time=0.15)


# ------------------------------------------------------------------ many segments / dots as ONE mobject


def seg_points(segs: np.ndarray, t: float) -> np.ndarray:
    a, b = segs[:, 0], segs[:, 1]
    e = a + (b - a) * t
    return np.stack([a, a + (e - a) / 3, a + 2 * (e - a) / 3, e], axis=1).reshape(-1, 3)


def seg_mob(segs, color=S.GREY, width: float = 1.0, opacity: float = 1.0) -> VMobject:
    segs = np.asarray(segs, dtype=float)
    vm = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    vm.set_points(seg_points(segs, 1.0))
    vm.segs = segs
    return vm


def grow(vm: VMobject, **kw):
    """All segments of a seg_mob grow from their top ends at once (branches growing down)."""
    return UpdateFromAlphaFunc(vm, lambda m, a: m.set_points(seg_points(m.segs, smooth(a))), **kw)


def dots_mob(points, r: float, color=S.WHITE) -> VMobject:
    tpl = Circle(radius=1).points
    pts = np.concatenate([tpl * r + np.asarray(p, dtype=float) for p in points])
    vm = VMobject(stroke_width=0).set_points(pts)
    vm.set_fill(color, 1).set_stroke(width=0)
    return vm


# ------------------------------------------------------------------ the big tree (beat 5)
ROOT_C = np.array([1.3, 2.95, 0])
ROOT_S, L1_S = 0.7, 0.5
L1_Y, L2_Y = 1.95, 1.0
DEPTH_Y = {3: 0.45, 4: -0.1, 5: -0.65, 6: -1.2, 7: -1.75, 8: -2.3, 9: -2.85}
L1_X = [-3.6 + 1.225 * i for i in range(9)]
L2_X = np.linspace(-3.85, 6.45, 72)
SLOT = L2_X[1] - L2_X[0]
SIDE_C = np.array([-5.4, 0.25, 0])      # the board beside the path
SIDE_S = 1.7


def sample_tree(seed: int = 11):
    """The real game tree below the 72 two-move positions, sampled: 2 branches per node at depths
    3-4, then 1 (a random real move) down to wherever that game really ends. The branch under
    X0, O1 follows explore's own order (lowest square first), so its leftmost path is explore's
    first game. Returns (segments by depth, leaf points, leftmost path points depth 3..7)."""
    rng = np.random.default_rng(seed)
    segs = {d: [] for d in range(3, 10)}
    leaves, path = [], []

    def rec(board, player, depth, lo, hi, parent, on_path):
        empties = [s for s in range(9) if board[s] == "."]
        k = min(2 if depth <= 4 else 1, len(empties))
        if on_path:
            rest = rng.choice(empties[1:], size=k - 1, replace=False).tolist() if k > 1 else []
            chosen = [empties[0]] + sorted(rest)
        else:
            chosen = sorted(rng.choice(empties, size=k, replace=False).tolist())
        w = (hi - lo) / len(chosen)
        for n, s in enumerate(chosen):
            b = board[:]
            b[s] = player
            pt = np.array([lo + (n + 0.5) * w, DEPTH_Y[depth], 0])
            segs[depth].append((parent, pt))
            here = on_path and n == 0
            if here:
                path.append(pt)
            if winner(b) is not None or "." not in b:
                leaves.append(pt)
            else:
                rec(b, "O" if player == "X" else "X", depth + 1, lo + n * w, lo + (n + 1) * w,
                    pt, here)

    for i in range(9):
        for jj, o in enumerate([s for s in range(9) if s != i]):
            j = 8 * i + jj
            b = ["."] * 9
            b[i], b[o] = "X", "O"
            x = L2_X[j]
            rec(b, "X", 3, x - SLOT / 2, x + SLOT / 2, np.array([x, L2_Y, 0]), j == 0)
    return segs, leaves, path


# ------------------------------------------------------------------ the close-up (beat 6)
CU = {"top": (3.6, 3.45), "A": (3.6, 2.95),
      "X6": (2.1, 1.95), "X7": (3.6, 1.95), "X8": (5.1, 1.95),
      "O6": (2.9, 0.95), "O8": (4.3, 0.95),
      "X8b": (2.9, -0.05), "X6b": (4.3, -0.05)}
CU = {k: np.array([x, y, 0]) for k, (x, y) in CU.items()}
CU_EDGES = [("A", "X6", 6, "X"), ("A", "X7", 7, "X"), ("A", "X8", 8, "X"),
            ("X7", "O6", 6, "O"), ("X7", "O8", 8, "O"), ("O6", "X8b", 8, "X"), ("O8", "X6b", 6, "X")]
CU_LEAVES = ["X6", "X8", "X8b", "X6b"]
WB_C = np.array([3.9, -2.32, 0])       # the whiteboard (clear of the "<- undo" tag)
WB_S = 1.6


class Explore(VoiceScene):
    def construct(self):
        self.code = explore_code()
        self.beat_intro()
        self.beat_stops()
        self.beat_loop()
        self.beat_example()
        self.beat_tree()
        self.beat_undo()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)

    # ================================================================ 1. meet explore()
    def beat_intro(self):
        code = self.code
        name = glyphs(code, 0, "explore")
        player = glyphs(code, 0, "player")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(code, shift=RIGHT * 0.3), run_time=1.0)
            vo.wait_until("a function called explore")
            name_box = token_box(name)
            self.play(Create(name_box), Indicate(name, color=WIN_COLOR, scale_factor=1.15),
                      run_time=0.8)
            vo.wait_until("We tell it whose turn")
            p_box = token_box(player)
            turn = line_tag(code, 0, "whose turn: X or O", t2c={"X": X_COLOR, "O": O_COLOR})
            self.play(Create(p_box), FadeIn(turn, shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("and its job is")
            rng_box = token_box(glyphs(code, 6, "range(9)"))
            rng_tag = line_tag(code, 6, "squares 0 to 8")
            self.play(Create(rng_box), FadeIn(rng_tag, shift=LEFT * 0.2), run_time=0.7)
            sw_tag = line_tag(code, 9, "switch turns", S.GREY, dy=0.14)
            self.play(code_line(code, 9).animate.set_opacity(0.3), FadeIn(sw_tag, shift=LEFT * 0.2),
                      run_time=0.7)
            tot_box = token_box(glyphs(code, 10, "total +="), COUNT_COLOR)
            tot_tag = line_tag(code, 10, "add to the total", COUNT_COLOR, dy=-0.17)
            self.play(Create(tot_box), FadeIn(tot_tag, shift=LEFT * 0.2), run_time=0.7)
        self.intro_marks = VGroup(name_box, p_box, turn, rng_box, rng_tag, sw_tag, tot_box, tot_tag)

    # ================================================================ 2. two stopping rules
    def beat_stops(self):
        code = self.code
        won = snap(B2_WON, 1.9, [2.65, 0.55, 0], stroke=5, line=(0, 8))
        draw = snap(B2_DRAW, 1.9, [5.1, 0.55, 0], stroke=5)
        lab_won = S.text("1 game", 28, COUNT_COLOR).next_to(won, DOWN, buff=0.35)
        lab_draw = S.text("1 game (a draw)", 28, COUNT_COLOR, t2c={"(a draw)": DRAW_COLOR}) \
            .next_to(draw, DOWN, buff=0.35)
        lab_draw.align_to(lab_won, DOWN)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(self.intro_marks), run_time=0.5)
            bar = lines_bar(code, 1, 2)
            bar_b = lines_bar(code, 3, 4)
            self.play(LaggedStart(FadeIn(bar), FadeIn(bar_b), lag_ratio=0.6), run_time=1.0)
            vo.wait_until("If someone has already won")
            self.play(FadeOut(bar_b), Indicate(code_line(code, 1), color=WIN_COLOR, scale_factor=1.03),
                      run_time=0.5)
            draw_board(self, won, run_time=1.2)
            self.play(Create(won[2]), run_time=0.5)
            vo.wait_until("so explore hands back")
            self.play(TransformFromCopy(glyphs(code, 2, "1"), lab_won[0]), run_time=0.8)
            self.play(FadeIn(lab_won[1:], shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("If the board is full")
            self.play(Transform(bar, lines_bar(code, 3, 4)), run_time=0.5)
            draw_board(self, draw, run_time=1.1)
            self.play(draw[1].animate.set_color(DRAW_COLOR), run_time=0.6)
            self.play(TransformFromCopy(glyphs(code, 4, "1"), lab_draw[0]), run_time=0.7)
            self.play(FadeIn(lab_draw[1:], shift=LEFT * 0.1), run_time=0.4)
        self.stop_stuff = VGroup(won, draw, lab_won, lab_draw, bar)

    # ================================================================ 3. the loop: try every square
    def beat_loop(self):
        code = self.code
        parent = snap(B3, 1.6, [4.3, 2.4, 0], stroke=4)
        cap = to_move("X", 30).next_to(parent, LEFT, buff=0.45)
        slots = [np.array([x, 0.05, 0]) for x in (2.6, 4.3, 6.0)]
        total_lab = S.text("total =", 32, S.WHITE, font=MONO)
        total_num = S.text("0", 40, COUNT_COLOR, font=MONO)
        counter = VGroup(total_lab, total_num).arrange(RIGHT, buff=0.25).move_to([4.3, -2.85, 0])
        ask = S.text("explore: how many\ngames from here?", 26, S.WHITE, line_spacing=1.0) \
            .move_to([4.3, -1.62, 0])
        kids, arrows, qs = [], [], []

        def try_square(n: int, rt: float = 1.0):
            s = B3_TRY[n]
            x = parent.board.mark_at(s, "X", 0.6, stroke=5.5)
            self.play(drop(x), run_time=0.4 * rt)
            kid = snap(put(B3, s, "X"), 1.0, slots[n], stroke=2.5)
            new = kid[1][[i for i, ch in enumerate(put(B3, s, "X")) if ch in "XO"].index(s)]
            base = VGroup(kid[0], VGroup(*[m for m in kid[1] if m is not new]))
            arr = Arrow(parent.get_bottom(), kid.get_top(), buff=0.1, color=S.GREY, stroke_width=3,
                        tip_length=0.15, max_tip_length_to_length_ratio=0.2)
            self.play(GrowArrow(arr), TransformFromCopy(parent[:2], base), ReplacementTransform(x, new),
                      run_time=0.8 * rt)
            w = winner(list(put(B3, s, "X")))
            if w is not None:
                line = kid.board.win_line(1, 7, stroke=5)
                self.play(Create(line), run_time=0.35)
                kid.add(line)
            q = S.text("?", 40, S.WHITE).next_to(kid, DOWN, buff=0.18)
            kids.append(kid)
            arrows.append(arr)
            qs.append(q)
            return q

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(self.stop_stuff), code_line(code, 9).animate.set_opacity(1), run_time=0.6)
            draw_board(self, parent, run_time=1.0, extra=[FadeIn(cap, shift=RIGHT * 0.2)])
            bar = lines_bar(code, 5)
            self.play(FadeIn(bar), TransformFromCopy(glyphs(code, 5, "total = 0"), counter),
                      run_time=0.9)

            vo.wait_until("So explore tries")
            self.play(Transform(bar, lines_bar(code, 6, 7)), run_time=0.4)
            blink = VGroup(*[parent.board.square(i, WIN_COLOR, 0.35) for i in B3_TRY])
            for _ in range(2):
                self.play(FadeIn(blink), run_time=0.3)
                self.play(FadeOut(blink), run_time=0.3)

            vo.wait_until("It puts the player's mark")
            self.play(Transform(bar, lines_bar(code, 8)), run_time=0.35)
            q0 = try_square(0)

            vo.wait_until("and then asks itself")
            self.play(Transform(bar, lines_bar(code, 9, 10)), FadeIn(ask, shift=UP * 0.15),
                      FadeIn(q0, scale=0.5), run_time=0.7)
            q1 = try_square(1, rt=0.75)
            self.play(FadeIn(q1, scale=0.5), run_time=0.25)
            vo.wait_until("now for the other player")
            o_tag = to_move("O", 24).move_to([2.35, 1.2, 0])
            self.play(FadeIn(o_tag, shift=DOWN * 0.1), Indicate(code_line(code, 9), color=O_COLOR,
                                                                scale_factor=1.03), run_time=0.6)
            q2 = try_square(2, rt=0.75)
            self.play(FadeIn(q2, scale=0.5), run_time=0.25)

            # the question is asked of each child board (the ?s pulse), then the answers come back
            vo.wait_until("how many games can")
            self.play(*[Indicate(q, color=S.WHITE, scale_factor=1.35) for q in qs], run_time=0.5)
            vo.wait_until("happen from here")
            answers = [S.text(str(a), 40, COUNT_COLOR).move_to(q) for a, q in zip(B3_ANS, qs)]
            self.play(*[ReplacementTransform(q, a) for q, a in zip(qs, answers)], run_time=0.5)

            vo.wait_until("It adds up")
            self.play(Transform(bar, lines_bar(code, 10)), run_time=0.25)
            running = 0
            for a, v in zip(answers, B3_ANS):
                running += v
                new_num = S.text(str(running), 40, COUNT_COLOR, font=MONO).move_to(total_num)
                self.play(FadeOut(a.copy(), target_position=total_num.get_center(), scale=0.6),
                          Transform(total_num, new_num), Indicate(a, color=COUNT_COLOR), run_time=0.4)
            self.play(Circumscribe(counter, color=COUNT_COLOR, buff=0.12), run_time=0.4)
        self.loop_stuff = VGroup(parent, cap, *kids, *arrows, *answers, ask, o_tag, counter, bar)

    # ================================================================ 4. a tiny worked example
    def beat_example(self):
        work = Board(size=2.0, stroke=5).move_to([0, 2.35, 0])
        on = {}                                  # square -> mark on the working board

        def place(s, sym):
            m = work.mark_at(s, sym, 0.6, stroke=6)
            on[s] = m
            return m

        for i, ch in enumerate(B4):
            if ch in "XO":
                place(i, ch)

        def state(line=None):
            g = VGroup(work, VGroup(*[on[s] for s in sorted(on)]))
            if line is not None:
                g.add(line)
            return g

        cap = to_move("O", 32).next_to(work, LEFT, buff=0.7)
        L = np.array([-3.4, -0.25, 0])
        R = np.array([3.4, -0.25, 0])
        G = np.array([3.4, -2.65, 0])
        snap_l = snap(put(B4, 5, "O"), 1.5, L, stroke=3, line=(2, 8))
        snap_r = snap(put(B4, 7, "O"), 1.5, R, stroke=3)
        snap_g = snap(put(put(B4, 7, "O"), 5, "X"), 1.5, G, stroke=3)

        def arrow(a, b):
            return Arrow(a, b, buff=0.12, color=S.GREY, stroke_width=3, tip_length=0.16,
                         max_tip_length_to_length_ratio=0.15)

        arr_l = arrow(work.get_bottom() + LEFT * 0.35, snap_l.get_top())
        arr_r = arrow(work.get_bottom() + RIGHT * 0.35, snap_r.get_top())
        arr_g = arrow(snap_r.get_bottom(), snap_g.get_top())
        one_l = S.text("1", 48, COUNT_COLOR).next_to(snap_l, RIGHT, buff=0.35)
        one_g = S.text("1", 48, COUNT_COLOR).next_to(snap_g, LEFT, buff=0.35)
        tag_l = S.text("O wins", 26, O_COLOR).next_to(snap_l, LEFT, buff=0.3)
        tag_g = S.text("draw", 26, DRAW_COLOR).next_to(snap_g, RIGHT, buff=0.3)
        total = S.text("1 + 1 = 2 games", 40, COUNT_COLOR).next_to(work, RIGHT, buff=0.45)
        # glyphs of "1+1=2games": 0 '1' | 1 '+' | 2 '1' | 3 '=' | 4 '2' | 5.. 'games'

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(self.loop_stuff), FadeOut(self.code, shift=LEFT * 1.2), run_time=0.7)
            self.play(LaggedStart(*[Create(ln) for ln in work], lag_ratio=0.15), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(on[s], scale=0.7) for s in sorted(on)], lag_ratio=0.12),
                      FadeIn(cap, shift=RIGHT * 0.2), run_time=0.9)

            vo.wait_until("If O takes")
            o5 = place(5, "O")
            self.play(mark_anim(o5), run_time=0.5)
            col = work.win_line(2, 8)
            self.play(Create(col), run_time=0.4)
            self.play(GrowArrow(arr_l), TransformFromCopy(state(col), snap_l), run_time=0.9)
            self.play(FadeIn(one_l, scale=0.5), FadeIn(tag_l, shift=RIGHT * 0.15), run_time=0.5)

            vo.wait_until("Erase it")
            del on[5]
            erase(self, VGroup(o5, col), work.center_of(5), work.cell, run_time=0.8)

            vo.wait_until("and try the bottom-middle")
            o7 = place(7, "O")
            self.play(mark_anim(o7), run_time=0.5)
            self.play(GrowArrow(arr_r), TransformFromCopy(state(), snap_r), run_time=0.8)

            vo.wait_until("Then X fills")
            x5 = place(5, "X")
            self.play(mark_anim(x5), run_time=0.5)
            self.play(GrowArrow(arr_g), TransformFromCopy(state(), snap_g), run_time=0.8)
            self.play(snap_g[1].animate.set_color(DRAW_COLOR), FadeIn(tag_g, shift=LEFT * 0.15),
                      run_time=0.5)
            self.play(FadeIn(one_g, scale=0.5), run_time=0.4)
            # back to the starting board (undo X, then undo O)
            del on[5], on[7]
            erase(self, x5, work.center_of(5), work.cell, run_time=0.3)
            erase(self, o7, work.center_of(7), work.cell, run_time=0.3)

            vo.wait_until("Total")
            self.play(ReplacementTransform(one_l, total[0]), ReplacementTransform(one_g, total[2]),
                      run_time=0.8)
            self.play(FadeIn(total[1]), FadeIn(total[3]), FadeIn(total[4:], shift=LEFT * 0.15),
                      run_time=0.4)
        self.example_stuff = VGroup(work, *on.values(), cap, snap_l, snap_r, snap_g, arr_l, arr_r,
                                    arr_g, tag_l, tag_g, total)

    # ================================================================ 5. recursion and the game tree
    def beat_tree(self):
        code = self.code
        call = glyphs(code, 10, "explore(next_player)")
        defn = glyphs(code, 0, "explore(player)")

        # the staircase of calls: explore's first game, one more mark per call
        chain_c = [np.array([2.05 + 0.6 * k, 3.0 - 0.82 * k, 0]) for k in range(8)]
        cells = ["." * 9]
        for s, sym in PATH:
            cells.append(put(cells[-1], s, sym))
        chain = [snap(cells[k], 0.62, chain_c[k], stroke=2) for k in range(8)]
        chain_win = chain[7].board.win_line(2, 6, stroke=4)
        chain_edges = [Line(chain[k].get_bottom(), chain[k + 1].get_top(), color=S.GREY,
                            stroke_width=2) for k in range(7)]
        each = S.text("each call:\n1 more mark", 26, S.WHITE, line_spacing=1.0).move_to([3.0, -1.7, 0])
        stop = S.text("stop!", 28, S.WHITE, weight="BOLD").next_to(chain[7], LEFT, buff=0.3)

        # the big tree
        segs, leaves, deep = sample_tree()
        root = snap("." * 9, ROOT_S, ROOT_C, stroke=2)
        l1 = [snap(put("." * 9, i, "X"), L1_S, [L1_X[i], L1_Y, 0], stroke=1.5) for i in range(9)]
        l2_pts = [np.array([x, L2_Y, 0]) for x in L2_X]
        e1 = seg_mob([(root.get_bottom(), b.get_top()) for b in l1], width=2)
        e2 = seg_mob([(l1[j // 8].get_bottom(), l2_pts[j]) for j in range(72)], width=1.5)
        l2_dots = dots_mob(l2_pts, 0.03, S.GREY)
        fringe = [seg_mob(segs[d], width=0.9, opacity=0.4) for d in range(3, 10)]
        leaf_dots = dots_mob(leaves, 0.03, S.WHITE)
        nine_eight = S.text("same 9 × 8 as before!", 26, S.WHITE, t2c={"9 × 8": COUNT_COLOR}) \
            .move_to([4.45, 3.1, 0])
        leaf_lab = S.text("leaves = finished games", 24, S.WHITE).move_to([3.6, -3.3, 0])

        # the leftmost branch = explore's first game; the staircase turns into it
        nodes = [root.get_bottom(), l1[0].get_top(), l1[0].get_bottom(), l2_pts[0], *deep]
        path_from = [nodes[0], nodes[2], nodes[3], *deep[:-1]]
        path_to = [nodes[1], nodes[3], *deep]
        path_edges = [Line(a, b, color=S.GREY, stroke_width=1.5) for a, b in zip(path_from, path_to)]
        path_dots = [Dot(p, radius=0.045, color=S.GREY) for p in [l2_pts[0], *deep]]

        side = Board(size=SIDE_S, stroke=5).move_to(SIDE_C)
        cnt_lab = S.text("games counted", 24, S.WHITE).move_to([SIDE_C[0], -1.55, 0])
        cnt = count_value(0, 52).move_to([SIDE_C[0], -2.25, 0])

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(self.example_stuff), run_time=0.45)
            self.play(FadeIn(code, shift=RIGHT * 1.0), run_time=0.6)
            call_box, def_box = token_box(call), token_box(defn)
            self.play(Create(call_box), run_time=0.3)
            fly = call.copy()
            self.play(Transform(fly, defn.copy(), path_arc=-PI / 2), run_time=0.8)
            self.play(FadeOut(fly), Create(def_box), Indicate(defn, color=WIN_COLOR, scale_factor=1.1),
                      run_time=0.5)
            vo.wait_until("is called recursive")
            rec = S.text("recursive", 52, S.WHITE).move_to([3.95, 0.55, 0])
            rec_sub = S.text("a function that calls itself", 26, S.GREY).next_to(rec, DOWN, buff=0.3)
            self.play(Write(rec), FadeIn(rec_sub, shift=UP * 0.15), run_time=0.8)

            vo.wait_until("That might sound")
            bar = lines_bar(code, 10)
            self.play(FadeOut(VGroup(rec, rec_sub, call_box, def_box)), FadeIn(bar), run_time=0.4)
            self.play(LaggedStart(*[Create(ln) for ln in chain[0][0]], lag_ratio=0.15), run_time=0.35)
            for k in range(1, 8):
                new = chain[k][1][-1]
                base = VGroup(chain[k][0], chain[k][1][:-1])
                self.play(Create(chain_edges[k - 1]), TransformFromCopy(chain[k - 1][:2], base),
                          drop(new, 0.15), run_time=0.45)
                if k == 3:
                    vo.wait_until("but each call adds")
                    self.play(FadeIn(each, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("so a stopping rule")
            self.play(Transform(bar, lines_bar(code, 1, 2)), Create(chain_win), run_time=0.6)
            self.play(FadeIn(stop, scale=0.6), Indicate(code_line(code, 2), color=WIN_COLOR),
                      run_time=0.6)
            self.play(Indicate(chain[7], color=WIN_COLOR, scale_factor=1.1), run_time=0.7)

            vo.wait_until("Picture an upside-down")
            self.play(FadeOut(code, shift=LEFT * 1.0), FadeOut(VGroup(bar, each, stop, chain_win)),
                      run_time=0.6)
            self.play(ReplacementTransform(chain[0], root), ReplacementTransform(chain[1], l1[0]),
                      *[FadeTransform(chain[k], path_dots[k - 2]) for k in range(2, 8)],
                      *[ReplacementTransform(e, p) for e, p in zip(chain_edges, path_edges)],
                      run_time=1.3)

            vo.wait_until("The empty board is at the top")
            self.play(Indicate(root, color=S.WHITE, scale_factor=1.3), TransformFromCopy(root[0], side),
                      run_time=0.9)
            vo.wait_until("every possible move")
            self.play(grow(e1), LaggedStart(*[FadeIn(b, scale=0.6) for b in l1[1:]], lag_ratio=0.1),
                      run_time=0.7)
            self.play(grow(e2), FadeIn(l2_dots), FadeIn(nine_eight, shift=DOWN * 0.15), run_time=0.7)
            for d, f in zip(range(3, 10), fringe):
                self.play(grow(f), run_time=0.16, rate_func=linear)
            self.bring_to_front(*path_edges, *path_dots)

            vo.wait_until("and every finished game")
            self.play(FadeIn(leaf_dots, scale=1.0), FadeIn(leaf_lab, shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(cnt_lab), FadeIn(cnt, scale=0.6), run_time=0.5)

            # explore walks down its first branch, the board beside it filling up
            vo.wait_until("Explore walks down")
            cursor = Dot(nodes[0], radius=0.08, color=WIN_COLOR)
            trail, side_marks = [], {}
            self.play(FadeIn(cursor, scale=0.5), run_time=0.2)
            for (s, sym), a, b in zip(PATH, path_from, path_to):
                seg = Line(a, b, color=WIN_COLOR, stroke_width=6)
                m = side.mark_at(s, sym, 0.6, stroke=6)
                trail.append(seg)
                side_marks[s] = m
                self.play(Create(seg), cursor.animate.move_to(b), mark_anim(m), run_time=0.3)
            side_win = side.win_line(2, 6)
            leaf = Dot(path_to[-1], radius=0.07, color=COUNT_COLOR)
            new_cnt = count_value(1, 52).move_to(cnt)
            self.play(Create(side_win), FadeIn(leaf, scale=2), Flash(leaf, color=COUNT_COLOR,
                      line_length=0.18, flash_radius=0.22), FadeOut(cnt, shift=UP * 0.3),
                      FadeIn(new_cnt, shift=UP * 0.3), run_time=0.7)
            cnt = new_cnt

        self.tree = VGroup(root, *l1, e1, e2, l2_dots, *fringe, leaf_dots, nine_eight, leaf_lab,
                           *path_edges, *path_dots)
        self.walk = dict(trail=trail, cursor=cursor, leaf=leaf, side=side, side_marks=side_marks,
                         side_win=side_win, cnt=cnt, cnt_lab=cnt_lab, deep=deep)

    # ================================================================ 6. undo = backtracking
    def beat_undo(self):
        code = self.code
        w = self.walk
        side, marks, cnt, cnt_lab = w["side"], w["side_marks"], w["cnt"], w["cnt_lab"]

        # the close-up of the bottom of the branch
        cu_edges = {}
        for a, b, s, sym in CU_EDGES:
            cu_edges[b] = Line(CU[a], CU[b], color=S.GREY, stroke_width=2.5)
        stub = DashedLine(CU["top"], CU["A"], color=S.GREY, stroke_width=2.5, dash_length=0.06)
        nodes = {k: Dot(CU[k], radius=0.075, color=S.GREY) for k in CU if k != "top"}
        for k in CU_LEAVES:
            nodes[k].set_color(S.WHITE)
        labels = VGroup()
        for a, b, s, sym in CU_EDGES:
            pa, pb = CU[a], CU[b]
            mid = pa + (pb - pa) * 0.55
            side_dir = LEFT if pb[0] < pa[0] - 0.01 else RIGHT
            col = X_COLOR if sym == "X" else O_COLOR
            lab = S.text(f"{sym}{s}", 26, col, font=S.FONT_SANS, weight="BOLD")   # as in S01: X0 O3 ...
            lab.move_to(mid + side_dir * 0.34)
            labels.add(lab)
        closeup = VGroup(stub, *cu_edges.values(), *nodes.values(), labels)
        hl_stub = Line(CU["top"], CU["A"], color=WIN_COLOR, stroke_width=6)
        hl = {"X6": Line(CU["A"], CU["X6"], color=WIN_COLOR, stroke_width=6)}
        counted = {"X6": Dot(CU["X6"], radius=0.09, color=COUNT_COLOR)}
        cursor = Dot(CU["X6"], radius=0.1, color=WIN_COLOR)

        zoom = Rectangle(width=0.7, height=1.5, color=S.WHITE, stroke_width=2).move_to([-3.9, -1.55, 0])
        zoom_to = SurroundingRectangle(closeup, buff=0.12, color=S.WHITE, stroke_width=2,
                                       corner_radius=0.1)

        # the whiteboard
        frame = RoundedRectangle(width=WB_S + 0.45, height=WB_S + 0.45, corner_radius=0.14,
                                 stroke_color=S.WHITE, stroke_width=3).set_fill(S.GREY_DARKER, 1)
        frame.move_to(WB_C)
        tray = RoundedRectangle(width=WB_S + 0.8, height=0.09, corner_radius=0.04, stroke_width=0) \
            .set_fill(S.GREY, 1).next_to(frame, DOWN, buff=0.04)
        pen = VGroup(RoundedRectangle(width=0.55, height=0.11, corner_radius=0.05, stroke_width=0)
                     .set_fill(S.WHITE, 1),
                     Rectangle(width=0.14, height=0.11, stroke_width=0).set_fill(X_COLOR, 1))
        pen[1].align_to(pen[0], RIGHT)
        pen.next_to(tray, UP, buff=0.0).shift(RIGHT * 0.55)
        wb_icon = VGroup(frame, tray, pen)
        shared = S.text("one\nshared\nboard", 28, S.WHITE, line_spacing=0.9) \
            .next_to(frame, RIGHT, buff=0.3)
        cap1 = S.text("try → explore → undo", 30, S.WHITE, t2c={"undo": UNDO_COLOR})
        cap2 = S.text("= backtracking", 30, S.WHITE, weight="BOLD")
        VGroup(cap1, cap2).arrange(RIGHT, buff=0.25).move_to([code.get_center()[0], -2.6, 0])
        # the counter sits in the free space left of the close-up (not next to the X8 label)
        cnt_lab_to = cnt_lab.copy().move_to([0.3, 3.15, 0])
        cnt_to = cnt.copy().move_to([0.3, 2.5, 0])

        side_group = VGroup(side, *marks.values(), w["side_win"])
        scale = WB_S / SIDE_S

        def wb_mark(s, sym):
            m = side.mark_at(s, sym, 0.6, stroke=6)
            marks[s] = m
            return m

        def go_down(key, s, sym, rt=0.45):
            seg = Line(cursor.get_center(), CU[key], color=WIN_COLOR, stroke_width=6)
            hl[key] = seg
            m = wb_mark(s, sym)
            self.play(Create(seg), cursor.animate.move_to(CU[key]), mark_anim(m), run_time=rt)

        def step_back(key, up_key, s, extra_targets=(), rt=0.5):
            seg = hl.pop(key)
            m = marks.pop(s)
            erase(self, VGroup(m, *extra_targets), side.center_of(s), side.cell, run_time=rt)
            tip = CU[up_key] + 0.02 * (CU[key] - CU[up_key])
            self.play(seg.animate.set_color(UNDO_COLOR).put_start_and_end_on(CU[up_key], tip),
                      cursor.animate.move_to(CU[up_key]), run_time=0.4)
            self.remove(seg)

        def count_leaf(key, n):
            nonlocal cnt
            dot = Dot(CU[key], radius=0.09, color=COUNT_COLOR)
            counted[key] = dot
            new = count_value(n, 52).move_to(cnt)
            self.play(FadeIn(dot, scale=2), Flash(dot, color=COUNT_COLOR, line_length=0.16,
                                                   flash_radius=0.24),
                      FadeOut(cnt, shift=UP * 0.3), FadeIn(new, shift=UP * 0.3), run_time=0.6)
            cnt = new

        with self.voiceover(SAY[5]) as vo:
            # zoom in on the bottom of the branch; the side board becomes the whiteboard
            self.play(Create(zoom), run_time=0.4)
            self.play(FadeOut(self.tree), FadeOut(VGroup(*w["trail"], w["cursor"], w["leaf"])),
                      ReplacementTransform(zoom, zoom_to),
                      FadeIn(VGroup(closeup, hl_stub, hl["X6"], counted["X6"], cursor)),
                      side_group.animate.scale(scale).move_to(WB_C),
                      Transform(cnt_lab, cnt_lab_to), Transform(cnt, cnt_to), run_time=1.1)
            self.play(FadeOut(zoom_to), FadeIn(code, shift=RIGHT * 1.0), run_time=0.7)
            undo_bar = lines_bar(code, 11, color=UNDO_COLOR, opacity=0.32)
            undo_tag = line_tag(code, 11, "undo", UNDO_COLOR)
            self.play(FadeIn(undo_bar), FadeIn(undo_tag, shift=LEFT * 0.2),
                      Indicate(code_line(code, 11), color=UNDO_COLOR, scale_factor=1.05), run_time=0.7)

            vo.wait_until("The program plays")
            frame.set_z_index(-1)
            self.play(FadeIn(frame), FadeIn(tray), FadeIn(pen, shift=LEFT * 0.2), run_time=0.7)
            links = VGroup(*[DashedLine(CU[k], frame.get_top(), color=S.GREY, stroke_width=2,
                                        dash_length=0.08)
                             for k in ("A", "X6", "X7", "X8", "O6", "X6b")])
            self.play(LaggedStart(*[Create(ln) for ln in links], lag_ratio=0.12), run_time=1.0)
            vo.wait_until("like a single whiteboard")
            self.play(FadeOut(links), FadeIn(shared, shift=LEFT * 0.15), run_time=0.6)
            self.play(Circumscribe(VGroup(frame, tray), color=S.WHITE, buff=0.08), run_time=0.9)

            # undo the last move: erase X6, step back up to A
            vo.wait_until("So after exploring")
            self.play(Indicate(code_line(code, 11), color=UNDO_COLOR, scale_factor=1.05),
                      Indicate(undo_tag, color=UNDO_COLOR), run_time=0.6)
            step_back("X6", "A", 6, extra_targets=[w["side_win"]], rt=0.8)

            vo.wait_until("That's called undoing")
            self.play(undo_bar.animate(rate_func=there_and_back).set_fill(opacity=0.7),
                      Indicate(undo_tag, color=UNDO_COLOR, scale_factor=1.25),
                      Indicate(cursor, color=WIN_COLOR, scale_factor=1.6), run_time=1.0)

            # the next branch starts fresh: X7, O6, X8 -> the 2nd game
            vo.wait_until("and it means the next branch")
            go_down("X7", 7, "X")
            go_down("O6", 6, "O")
            go_down("X8b", 8, "X")
            win2 = side.win_line(0, 8)
            self.play(Create(win2), run_time=0.35)
            count_leaf("X8b", 2)

            # backtracking: undo X8 and O6, try O8 then X6 -> the 3rd game
            vo.wait_until("Trying a path")
            self.play(FadeIn(cap1, shift=UP * 0.15), run_time=0.6)
            step_back("X8b", "O6", 8, extra_targets=[win2], rt=0.45)
            step_back("O6", "X7", 6, rt=0.45)
            go_down("O8", 8, "O", rt=0.4)
            go_down("X6b", 6, "X", rt=0.4)
            win3 = side.win_line(2, 6)
            self.play(Create(win3), run_time=0.3)
            count_leaf("X6b", 3)
            vo.wait_until("is called backtracking")
            self.play(Write(cap2), run_time=0.8)
            self.play(Circumscribe(VGroup(cap1, cap2), color=S.WHITE, buff=0.12), run_time=0.8)
        self.wait(0.8)
