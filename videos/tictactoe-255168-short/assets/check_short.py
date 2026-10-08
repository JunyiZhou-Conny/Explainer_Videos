"""Acceptance checks for the tic-tac-toe short. No render needed, standard library + PyYAML only.

    python3 videos/tictactoe-255168-short/assets/check_short.py

1. NUMBERS: recomputes every number the short shows, by an exhaustive search of the real rules, the
   program's broken variant, and the two hand counts, and compares each with the table below.
2. BOARDS: replays every board and move list script.md draws, and checks each is legal and ends
   (or does not end) where the script says.
3. LAYOUT: the facts the radial game tree ("the galaxy") relies on: ring sizes, angular shares,
   the counter at each wedge boundary, where game A's leaf sits, the minimax colours.
4. CAPTIONS and PLAN: captions.yaml (count, widths, words, durations, overlaps, picture-only share,
   glossary rules), script.md (bars 1-106 covered once, every caption quoted verbatim in the right
   scene and bar), video.yaml (scenes, bars, grid).
Prints one line per check and exits 1 if any fails.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from functools import lru_cache
from itertools import permutations
from math import factorial
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
FAILS: list[str] = []
BAR_S = 2.4


def check(name: str, ok: bool, detail: str = "") -> None:
    print(("ok    " if ok else "FAIL  ") + name + (f"  ({detail})" if detail else ""))
    if not ok:
        FAILS.append(name)


# ====================================================================== the rules (as the program)
WIN_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def winner(cells) -> str | None:
    for a, b, c in WIN_LINES:
        if cells[a] != "." and cells[a] == cells[b] == cells[c]:
            return cells[a]
    return None


def replay(moves) -> tuple[str, str | None]:
    """Play squares in order (X first). Asserts every move is legal (empty square, game not over).
    Returns (cells, result) with result 'X' / 'O' / 'D' when the game is finished, else None."""
    cells = ["."] * 9
    for k, s in enumerate(moves, 1):
        assert cells[s] == ".", f"square {s} taken at move {k} in {moves}"
        assert winner(cells) is None, f"move {k} played after a win in {moves}"
        cells[s] = "X" if k % 2 else "O"
    w = winner(cells)
    return "".join(cells), (w if w else ("D" if "." not in cells else None))


def other(p: str) -> str:
    return "O" if p == "X" else "X"


# ====================================================================== exhaustive search
LEAVES: list[tuple[tuple, str]] = []          # (moves, result) in the program's (DFS) order
ALIVE = Counter()                             # explore() calls by depth (marks on the board)


def _walk(cells: list, player: str, seq: list) -> None:
    ALIVE[len(seq)] += 1
    w = winner(cells)
    if w or "." not in cells:
        LEAVES.append((tuple(seq), w or "D"))
        return
    for s in range(9):
        if cells[s] == ".":
            cells[s] = player
            seq.append(s)
            _walk(cells, other(player), seq)
            seq.pop()
            cells[s] = "."


_walk(["."] * 9, "X", [])


def variant(check_win: bool = True, undo: bool = True) -> int:
    """The program with its winner check or its undo line deleted."""
    b = ["."] * 9

    def explore(p):
        if check_win and winner(b) is not None:
            return 1
        if "." not in b:
            return 1
        t = 0
        for s in range(9):
            if b[s] == ".":
                b[s] = p
                t += explore(other(p))
                if undo:
                    b[s] = "."
        return t
    return explore("X")


PREFER = {"X": "XDO", "O": "ODX"}            # each player's results, best first


@lru_cache(maxsize=None)
def perfect(cells: str, player: str) -> str:
    w = winner(cells)
    if w:
        return w
    if "." not in cells:
        return "D"
    rs = [perfect(cells[:s] + player + cells[s + 1:], other(player)) for s in range(9) if cells[s] == "."]
    return min(rs, key=PREFER[player].index)


by_move = Counter(len(m) for m, _ in LEAVES)
by_result = Counter(r for _, r in LEAVES)
by_move_result = Counter((len(m), r) for m, r in LEAVES)
calls = sum(ALIVE.values())

# ====================================================================== 1. NUMBERS shown on screen
NUMBERS = {
    "total games": (len(LEAVES), 255_168),
    "nine factorial": (factorial(9), 362_880),
    "end on move 5": (by_move[5], 1_440),
    "end on move 6": (by_move[6], 5_328),
    "end on move 7": (by_move[7], 47_952),
    "end on move 8": (by_move[8], 72_576),
    "end on move 9": (by_move[9], 127_872),
    "move 9: X wins": (by_move_result[(9, "X")], 81_792),
    "move 9: draws": (by_move_result[(9, "D")], 46_080),
    "X wins": (by_result["X"], 131_184),
    "O wins": (by_result["O"], 77_904),
    "draws": (by_result["D"], 46_080),
    "x24 (move 5)": (by_move[5] * 24, 34_560),
    "x6 (move 6)": (by_move[6] * 6, 31_968),
    "x2 (move 7)": (by_move[7] * 2, 95_904),
    "x1 (move 8)": (by_move[8] * 1, 72_576),
    "x1 (move 9)": (by_move[9] * 1, 127_872),
    "sum of products = 9!": (sum(n * factorial(9 - k) for k, n in by_move.items()), 362_880),
    "program without the winner check": (variant(check_win=False), 362_880),
    "program without undo (not shown; sanity)": (variant(undo=False), 3),
    "explore() calls (HUD)": (calls, 549_946),
    "undos (HUD) = every mark placed is erased": (calls - 1, 549_945),
    "8 lines x 3! orders x 6 x 5 places": (8 * factorial(3) * 6 * 5, 1_440),
    "O lines: 8 x 6 x (6 x 5 x 4)": (8 * 6 * (6 * 5 * 4), 5_760),
    "X already won: 12 pairs x 6 x 6": (12 * 6 * 6, 432),
    "5,760 - 432": (5_760 - 432, 5_328),
    "digit strip: 255,168": (len(str(255_168)), 6),
    "digit strip: 10^80": (len(str(10 ** 80)), 81),
    "digit strip: 10^120": (len(str(10 ** 120)), 121),
}
for name, (got, want) in NUMBERS.items():
    check(f"number  {name} = {want:,}", got == want, "" if got == want else f"got {got:,}")

check("only odd moves end in X wins, only even moves in O wins",
      all((k % 2 == 1) == (r == "X") for (k, r) in by_move_result if r != "D"))
check("draws happen only on a full board (move 9)", all(k == 9 for (k, r) in by_move_result if r == "D"))
check("earliest end is move 5, O's earliest win is move 6",
      min(by_move) == 5 and min(k for (k, r) in by_move_result if r == "O") == 6)
share = by_result["X"] / len(LEAVES)
check("X wins 'just over half' (c24)", 0.5 < share < 0.55, f"{share:.3f}")
check("perfect play from the empty board is a draw", perfect("." * 9, "X") == "D")

running = [factorial(9) // factorial(9 - k) for k in range(1, 10)]
check("running products 9 → 72 → … → 362,880 (S02 HUD)",
      running == [9, 72, 504, 3_024, 15_120, 60_480, 181_440, 362_880, 362_880], str(running))

# the 1,440 by hand: exactly the move-5 games of the search
hand5 = set()
for line in WIN_LINES:
    rest = [s for s in range(9) if s not in line]
    for order in permutations(line):
        for o1 in rest:
            for o2 in rest:
                if o2 != o1:
                    hand5.add((order[0], o1, order[1], o2, order[2]))
search5 = {m for m, r in LEAVES if len(m) == 5}
check("8 x 6 x 30 enumerates exactly the 1,440 move-5 games", hand5 == search5 and len(hand5) == 1_440)
check("nobody has 3 marks before move 5 (why 8 x 6 x 30 needs no subtraction)",
      all(replay(m[:4])[1] is None for m in hand5))

# the 5,328 by hand: O completes a line on move 6, minus the boards where X's 3 marks made a line
o_line_games, x_already = [], []
pairs = set()
for line in WIN_LINES:
    rest = [s for s in range(9) if s not in line]
    for order in permutations(line):
        for xs in permutations(rest, 3):
            seq = (xs[0], order[0], xs[1], order[1], xs[2], order[2])
            o_line_games.append(seq)
            xl = next((l for l in WIN_LINES if set(l) == set(xs)), None)
            if xl:
                x_already.append(seq)
                pairs.add((line, xl))
check("O can finish a line in 5,760 ways", len(o_line_games) == 5_760)
check("X's 3 marks already made a line in 432 of them", len(x_already) == 432)
par = {(0, 1, 2), (3, 4, 5), (6, 7, 8)}
check("…always a row or column parallel to O's: 12 pairs",
      len(pairs) == 12 and all((a in par) == (b in par) for a, b in pairs))
search6 = {m for m, r in LEAVES if len(m) == 6}
check("the other 5,328 are exactly the move-6 games", set(o_line_games) - set(x_already) == search6)

# ====================================================================== 2. BOARDS in script.md
def rot_cw(i: int) -> int:
    r, c = divmod(i, 3)
    return c * 3 + (2 - r)


GAME_A = (0, 3, 1, 4, 2)          # cold open, ghost games, callback: X wins the top row on move 5
GAME_B = (2, 4, 0, 3, 1)          # same final board, another order
TURNED = tuple(rot_cw(s) for s in GAME_A)

cells_a, res_a = replay(GAME_A)
cells_b, res_b = replay(GAME_B)
cells_t, res_t = replay(TURNED)
check("game A: X0 O3 X1 O4 X2 is a finished game, X wins the top row on move 5",
      cells_a == "XXXOO...." and res_a == "X" and all(replay(GAME_A[:k])[1] is None for k in range(5)))
check("game B: X2 O4 X0 O3 X1 ends on the same board, X wins on move 5",
      cells_b == cells_a and res_b == "X" and all(replay(GAME_B[:k])[1] is None for k in range(5)))
check("game A turned a quarter turn: X2 O1 X5 O4 X8, a different game and board, X wins on move 5",
      TURNED == (2, 1, 5, 4, 8) and res_t == "X" and cells_t != cells_a and TURNED != GAME_A)
check("A, B and the turned copy are three different leaves of the tree",
      len({GAME_A, GAME_B, TURNED} & {m for m, _ in LEAVES}) == 3)

# square-pitch map (the motif): row 0 high … row 2 low, D Lydian
PITCH = ["C#5", "D5", "E5", "G#4", "A4", "B4", "D4", "E4", "F#4"]
check("motif of game A: C#5 G#4 D5 A4 E5", [PITCH[s] for s in GAME_A] == ["C#5", "G#4", "D5", "A4", "E5"])
check("game B: same five notes, another order: E5 A4 C#5 G#4 D5",
      [PITCH[s] for s in GAME_B] == ["E5", "A4", "C#5", "G#4", "D5"])
check("turned copy: other notes, falling: E5 D5 B4 A4 F#4",
      [PITCH[s] for s in TURNED] == ["E5", "D5", "B4", "A4", "F#4"])

# ghost games of game A: 4 empty squares, 24 orders, and 9! counts game A exactly 24 times
empty_a = [s for s in range(9) if cells_a[s] == "."]
ghost_orders = list(permutations(empty_a))
check("game A leaves squares 5, 6, 7, 8 empty", empty_a == [5, 6, 7, 8])
check("4 x 3 x 2 x 1 = 24 ghost orders, all different", len(set(ghost_orders)) == 24)
FIRST_GHOSTS = (6, 5, 8, 7)        # moves 6-9 drawn first in S03: O6 X5 O8 X7
ghost_board = list(cells_a)
for k, s in enumerate(FIRST_GHOSTS, 6):
    ghost_board[s] = "X" if k % 2 else "O"
lines_on = [l for l in WIN_LINES if ghost_board[l[0]] != "." and ghost_board[l[0]] == ghost_board[l[1]] == ghost_board[l[2]]]
check("first ghost order shown, O6 X5 O8 X7, is one of the 24 and forms no second line",
      FIRST_GHOSTS in ghost_orders and lines_on == [(0, 1, 2)], f"{''.join(ghost_board)} {lines_on}")
full_orders_with_prefix = sum(1 for p in permutations(range(9)) if p[:5] == GAME_A)
check("9! counts game A 24 times (fill orders that start with its 5 moves)", full_orders_with_prefix == 24)

# one example game per end move (S03 row of tiny boards, x24 x6 x2 x1 x1)
END_EXAMPLES = {5: (GAME_A, "XXXOO....", "X"),
                6: ((0, 3, 1, 4, 6, 5), "XX.OOOX..", "O"),
                7: ((0, 1, 2, 3, 4, 5, 6), "XOXOXOX..", "X"),
                8: ((0, 4, 8, 2, 6, 3, 1, 5), "XXOOOOX.X", "O"),
                9: ((0, 1, 2, 3, 4, 5, 7, 6, 8), "XOXOXOOXX", "X")}
for k, (moves, want_cells, want_res) in END_EXAMPLES.items():
    c, r = replay(moves)
    ok = (len(moves) == k and c == want_cells and r == want_res
          and all(replay(moves[:j])[1] is None for j in range(k)))
    check(f"end-move example, move {k}: {want_cells} ({want_res})", ok, f"{c} {r}")

# S04: the move-6 annotation boards
c6, r6 = replay((0, 3, 1, 4, 6, 5))
check("S04 O-row board XX.OOOX..: O wins row 3-4-5 on move 6, X has no line", c6 == "XX.OOOX.." and r6 == "O")
cx, rx = replay((0, 3, 1, 4, 2))
check("S04 'X already won' board XXXOO....: game over on move 5, O's row never finishes",
      cx == "XXXOO...." and rx == "X")

# S05: the first six games the program finds, and the undos between them
FIRST_SIX = [((0, 1, 2, 3, 4, 5, 6), "X"), ((0, 1, 2, 3, 4, 5, 7, 6, 8), "X"), ((0, 1, 2, 3, 4, 5, 7, 8, 6), "X"),
             ((0, 1, 2, 3, 4, 5, 8), "X"), ((0, 1, 2, 3, 4, 6, 5, 7, 8), "X"), ((0, 1, 2, 3, 4, 6, 5, 8, 7), "D")]
check("the program's first six games, in order (game 6 is the first draw)", LEAVES[:6] == FIRST_SIX)
check("…and no draw comes earlier", all(r != "D" for _, r in LEAVES[:5]))


def undos(a, b):                   # marks erased between consecutive leaves a and b
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]:
        k += 1
    return len(a) - k


check("undos between games 1-6: 1, 2, 3, 2, 2",
      [undos(FIRST_SIX[i][0], FIRST_SIX[i + 1][0]) for i in range(5)] == [1, 2, 3, 2, 2])
check("game 1 X wins the 2-4-6 diagonal on move 7, games 2 and 3 on move 9 (0-4-8, 2-4-6)",
      replay(FIRST_SIX[0][0])[0] == "XOXOXOX.." and replay(FIRST_SIX[1][0])[0] == "XOXOXOOXX"
      and replay(FIRST_SIX[2][0])[0] == "XOXOXOXXO")
check("game 6 board XOXOXXOXO is full with no line", replay(FIRST_SIX[5][0]) == ("XOXOXXOXO", "D"))

# S08: game A's mistake. After X0, only the centre keeps the draw for O; O3 gives the game away.
seq_vals = []
cells, p = "." * 9, "X"
for s in GAME_A:
    before = perfect(cells, p)
    nxt = cells[:s] + p + cells[s + 1:]
    after = perfect(nxt, other(p))
    best = [t for t in range(9) if cells[t] == "." and perfect(cells[:t] + p + cells[t + 1:], other(p)) == before]
    seq_vals.append((p, s, before, after, best))
    cells, p = nxt, other(p)
mistakes = [(i + 1, v) for i, v in enumerate(seq_vals) if PREFER[v[0]].index(v[3]) > PREFER[v[0]].index(v[2])]
check("game A has exactly one mistake: O3 on move 2 (draw → X wins)",
      len(mistakes) == 1 and mistakes[0][0] == 2 and mistakes[0][1][:4] == ("O", 3, "D", "X"))
check("…the only move that kept the draw was the centre (square 4)", seq_vals[1][4] == [4])

# ====================================================================== 3. LAYOUT of the galaxy
# Every node splits its wedge equally among its children, so a leaf after k moves owns (9-k)! of the
# 9! slots on the circle: exactly the ghost games S03 and S07 count. Same layout in S02, S05-S09.
order = 0
leaf_slot = {}
for m, r in LEAVES:
    leaf_slot[m] = order
    order += factorial(9 - len(m))
check("the leaves' slots tile the circle: Σ (9-k)! = 9!", order == factorial(9))
shares = {k: by_move[k] * factorial(9 - k) / factorial(9) for k in range(5, 10)}
check("ring shares of the circle 9.5 / 8.8 / 26.4 / 20.0 / 35.2 %",
      [round(100 * shares[k], 1) for k in range(5, 10)] == [9.5, 8.8, 26.4, 20.0, 35.2],
      str({k: round(100 * v, 2) for k, v in shares.items()}))
check("ring sizes of the fill-order tree (S02): 9, 72, 504, 3,024, 15,120, 60,480, 181,440, 362,880, 362,880",
      [factorial(9) // factorial(9 - k) for k in range(1, 10)] == running)
check("nodes per ring of the real tree: 1, 9, 72, 504, 3,024, 15,120, 54,720, 148,176, 200,448, 127,872",
      [ALIVE[d] for d in range(10)] == [1, 9, 72, 504, 3_024, 15_120, 54_720, 148_176, 200_448, 127_872])
wedges = Counter(m[0] for m, _ in LEAVES)
cum = []
t = 0
for s in range(9):
    t += wedges[s]
    cum.append(t)
check("counter at the end of each first-move wedge (S05 bar lines 51.1 … 59.1)",
      cum == [27_732, 57_324, 85_056, 114_648, 140_520, 170_112, 197_844, 227_436, 255_168], str(cum))
idx_a = [m for m, _ in LEAVES].index(GAME_A) + 1
ang_a = leaf_slot[GAME_A] / factorial(9) * 360
check("game A is the 7,317th game the program finds, at 10.12° clockwise from 12 o'clock",
      idx_a == 7_317 and abs(ang_a - 10.119) < 0.001, f"{idx_a}, {ang_a:.3f}°")

# S08 bubble, ring 2: 48 nodes turn cyan (O's reply loses) and 24 stay grey
ring2 = Counter(perfect("".join("X" if i == a else "O" if i == b else "." for i in range(9)), "X")
                for a in range(9) for b in range(9) if a != b)
check("minimax colours of ring 2: 48 X wins, 24 draws", ring2 == Counter({"X": 48, "D": 24}), str(dict(ring2)))
radii = [round(2.9 * (d / 9) ** 0.75, 2) for d in range(1, 10)]
check("ring radii r_d = 2.9 (d/9)^0.75: 0.56 … 2.90",
      radii == [0.56, 0.94, 1.27, 1.58, 1.87, 2.14, 2.4, 2.65, 2.9], str(radii))
UNIT = 30_240                                  # S07: one length scale, 9! = 12 units
check("S07 scale: 9! = 12 units; bars 1,440 → 0.05, X 4.34, O 2.58, draws 1.52",
      factorial(9) / UNIT == 12 and round(1_440 / UNIT, 2) == 0.05
      and [round(n / UNIT, 2) for n in (131_184, 77_904, 46_080)] == [4.34, 2.58, 1.52])
t_pass = 64 * BAR_S + (255_168 / factorial(9)) * 2 * BAR_S       # S06: uniform sweep 65.1 → 67.1
bar_pass, rest = divmod(t_pass, BAR_S)
check("S06: the re-run passes 255,168 at about 66.2+ (beat 2 and a half of bar 66)",
      int(bar_pass) + 1 == 66 and 0.6 <= rest < 1.2, f"{t_pass:.2f} s, bar {int(bar_pass) + 1} + {rest:.2f} s")
# the explore() plate: the file lines script.md names (S05, S06)
src = (PROJECT.parent / "tictactoe-255168" / "assets" / "play_all_games.py").read_text().splitlines()
want = {23: "def explore(player):", 24: "if winner(board) is not None:", 25: "return 1",
        26: 'if "." not in board:', 27: "return 1", 31: "board[square] = player",
        33: "total += explore(next_player)", 34: 'board[square] = "."', 35: "return total"}
bad_lines = [n for n, t in want.items() if not src[n - 1].strip().startswith(t)]
check("explore() plate: file lines 23-35 as script.md names them (24-25 winner check, 34 undo …)",
      not bad_lines, str(bad_lines))
# minimax colour of every node, ring by ring (S08 bubble): the root ends grey, all 9 first moves grey
first_moves = {perfect("." * s + "X" + "." * (8 - s), "O") for s in range(9)}
check("all 9 first moves are draws under perfect play (ring 1 turns grey)", first_moves == {"D"})

# ====================================================================== 4. CAPTIONS, PLAN, video.yaml
BAR, BEAT, TOTAL = 2.4, 0.6, 254.4
vy = yaml.safe_load((PROJECT / "video.yaml").read_text(encoding="utf-8"))
first_bar = {Path(sc["file"]).stem: (f"S{k + 1:02d}", sc["bars"]) for k, sc in enumerate(vy["scenes"])}
table = yaml.safe_load((PROJECT / "captions.yaml").read_text(encoding="utf-8"))
check("captions.yaml has only scene keys, in video.yaml order",
      list(table) == [k for k in first_bar if k in table] and all(isinstance(v, list) for v in table.values()),
      ", ".join(table))
caps = []                   # the explainer/captions.py format: per scene stem, at = "bar:beat" from 0
for stem, items in table.items():
    sid, (b0, b1) = first_bar[stem]
    for c in items:
        rb, rbeat = (c["at"].split(":") + ["0"])[:2]
        start = (b0 - 1 + int(rb)) * BAR + float(rbeat) * BEAT
        caps.append({**c, "scene": sid, "stem": stem, "start": round(start, 4),
                     "end": round(start + float(c["dur"]), 4), "bar": b0 + int(rb), "rel_beat": float(rbeat),
                     "range": (b0, b1)})


HAN = re.compile(r"[\u4e00-\u9fff]")
WIDE = re.compile(r"[\u3000-\u303f\uff00-\uffef\u4e00-\u9fff“”‘’……]")


def width(s: str) -> float:
    return sum(1.0 if WIDE.match(ch) else 0.5 for ch in s)


check("caption count 25-30", 25 <= len(caps) <= 30, str(len(caps)))
check("caption ids c01 … in order", [c["id"] for c in caps] == [f"c{i:02d}" for i in range(1, len(caps) + 1)])
off = [c["id"] for c in caps if abs(c["rel_beat"] * 2 - round(c["rel_beat"] * 2)) > 1e-9 or c["rel_beat"] >= 4]
check("each caption's `at` is on the eighth-note grid of its scene", not off, ", ".join(off))
outside = [c["id"] for c in caps if not (c["range"][0] <= c["bar"] <= c["range"][1])]
check("each caption starts inside its own scene's bars", not outside, ", ".join(outside))
bad_d = [f'{c["id"]} {c["end"] - c["start"]:.1f}s' for c in caps if not 3.0 - 1e-9 <= c["end"] - c["start"] <= 4.0 + 1e-9]
check("each caption stays up 3.0-4.0 s", not bad_d, ", ".join(bad_d))
gaps = [(a["id"], b["id"]) for a, b in zip(caps, caps[1:]) if b["start"] < a["end"] + 0.2 - 1e-9]
check("no two captions overlap (>= 0.2 s apart)", not gaps, str(gaps))
check("all captions inside 0-254.4 s", all(0 <= c["start"] and c["end"] <= TOTAL for c in caps))
wide = [f'{c["id"]} {width(c["zh"])}' for c in caps if width(c["zh"]) > 21 or len(HAN.findall(c["zh"])) > 20]
check("zh lines: at most 20 Han characters and width 21", not wide, ", ".join(wide))
long_en = [f'{c["id"]} {len(c["en"].split())}' for c in caps if len(c["en"].split()) > 14]
check("en lines: at most 14 words", not long_en, ", ".join(long_en))
han_total = sum(len(HAN.findall(c["zh"])) for c in caps)
check("zh text in total about 400-550 CJK characters (counting full-width punctuation)",
      380 <= sum(len(WIDE.findall(c["zh"])) for c in caps) <= 550,
      f"{han_total} Han, {sum(len(WIDE.findall(c['zh'])) for c in caps)} with punctuation")
covered, last = 0.0, 0.0
for c in sorted(caps, key=lambda c: c["start"]):
    s, e = max(c["start"], last), c["end"]
    if e > s:
        covered += e - s
        last = e
pic = 1 - covered / TOTAL
check("picture-only share >= 40 %", pic >= 0.40, f"{100 * pic:.1f} % picture only, {covered:.1f} s with a caption")
cmap = {c["id"]: c for c in caps}
quiet = cmap["c19"]["start"] - cmap["c18"]["end"]
check("hero shot: >= 10 s with no words while the counter runs to 255,168 (c18 → c19)", quiet >= 10, f"{quiet:.1f} s")
check("title hit (bar 10.1 = 21.6 s) has no caption over it",
      all(not (c["start"] <= 21.6 <= c["end"]) for c in caps))
turn = [c["id"] for c in caps if c["start"] < 63 * BAR + BAR and c["end"] > 63 * BAR]
check("the turn's bar of silence (bar 64) has no caption", not turn, str(turn))

# glossary rules on the zh lines
RULES = [
    (r"游戏|棋局|一盘|盘棋|\d\s*盘", "a game is 对局 / 局 / 种, never 游戏 / 棋局 / 盘"),
    (r"(?<!国际)象棋", "chess is 国际象棋"),
    (r"空格(?!子)", "empty square is 空格子"),
    (r"胜", "labels and lines say 赢, not 胜"),
    (r"幽灵结局", "only 幽灵对局"),
    (r"被数|数了", "counted = 算 (被算了 24 次)"),
    (r"小程序|计算机|打印|破解|悔棋|和棋|程式|函式", "banned words (glossary A4, A5)"),
    (r"!", "no half-width ! in captions"),
    (r"\d！", "never ！ right after a digit"),
    (r"[。，]$", "no 。 or ， at the end of a caption"),
    (r"[一-鿿][A-Za-z0-9]|[A-Za-z0-9][一-鿿]", "half-width space between CJK and Latin / digits"),
    (r"\d，\d", "no full-width comma inside a number"),
    (r"9!", "the symbol 9! only in on-screen maths"),
]
for pat, why in RULES:
    hits = [c["id"] for c in caps if re.search(pat, c["zh"])]
    check(f"glossary: {why}", not hits, ", ".join(hits))
check("en lines: no digit followed by '!'", not any(re.search(r"\d!", c["en"]) for c in caps))
first_ghost = next(c for c in caps if "幽灵对局" in c["zh"])
check("幽灵对局 is first used where it is named, in “”", "“幽灵对局”" in first_ghost["zh"], first_ghost["id"])
check("no section label uses 幽灵对局 before it is named (c09, bar 27)",
      all("幽灵对局" not in h["text"] or h["bars"][0] >= 27 for h in vy["sections"]))

# script.md: bars, scenes and the captions it quotes
script = (PROJECT / "script.md").read_text(encoding="utf-8")
heads = re.findall(r"^## (S\d\d) · .+? — `scenes/(s\d\d_\w+)\.py` · `(\w+)`", script, flags=re.M)
ranges = [tuple(map(int, m)) for m in re.findall(r"^Bars (\d+)–(\d+)", script, flags=re.M)]
blocks = [tuple(map(int, m)) for m in re.findall(r"^BARS (\d+)-(\d+):", script, flags=re.M)]
check("script.md has one header and one bar range per scene", len(heads) == len(ranges) > 0,
      f"{len(heads)} headers, {len(ranges)} ranges")
flat = [b for a, z in blocks for b in range(a, z + 1)]
check("BARS blocks cover bars 1-106 exactly once, in order", flat == list(range(1, 107)),
      f"{len(flat)} bars, first gap at {next((i + 1 for i, b in enumerate(flat) if b != i + 1), None)}")
check("scene bar ranges are contiguous 1-106",
      [b for a, z in ranges for b in range(a, z + 1)] == list(range(1, 107)))
quoted = re.findall(r"CAPTION (c\d\d): 「(.+?)」 / \"(.+?)\"", script)
qmap = {}
for cid, zh, en in quoted:
    qmap.setdefault(cid, []).append((zh, en))
mism = [cid for cid, c in cmap.items() if qmap.get(cid) != [(c["zh"], c["en"])]]
check("script.md quotes every caption once, verbatim", not mism, ", ".join(mism))
# each caption sits in the scene captions.yaml names, inside a BARS block that contains its cue bar
pos = {}
cur_scene, cur_block = None, None
for line in script.splitlines():
    m = re.match(r"^## (S\d\d) ", line)
    if m:
        cur_scene = m.group(1)
    m = re.match(r"^BARS (\d+)-(\d+):", line)
    if m:
        cur_block = (int(m.group(1)), int(m.group(2)))
    m = re.search(r"CAPTION (c\d\d):", line)
    if m:
        pos[m.group(1)] = (cur_scene, cur_block)
misplaced = [cid for cid, c in cmap.items()
             if cid in pos and not (pos[cid][0] == c["scene"] and pos[cid][1][0] <= c["bar"] <= pos[cid][1][1])]
check("each caption is quoted in its own scene and BARS block", not misplaced, ", ".join(misplaced))
check("script.md has no SAY: lines (the short has no voice)", not re.search(r"^SAY:", script, flags=re.M))

# video.yaml
check("video.yaml: format short, 100 BPM, 106 bars, zh-first master first, papers []",
      vy.get("format") == "short" and vy["grid"]["bpm"] == 100 and vy["grid"]["bars"] == 106
      and vy["captions"]["layouts"][0] == "zh-first" and vy.get("papers") == [])
vs = [(Path(s["file"]).stem, s["cls"], tuple(s["bars"])) for s in vy["scenes"]]
check("video.yaml scenes match script.md headers and bar ranges",
      [(f, c) for f, c, _ in vs] == [(f, c) for _, f, c in heads] and [b for _, _, b in vs] == ranges)
check("video.yaml duration = 106 bars = 254.4 s", abs(vy["grid"]["bars"] * BAR - TOTAL) < 1e-9
      and abs(float(vy["grid"]["duration_s"]) - TOTAL) < 1e-9)

print()
print(f"{len(FAILS)} failed" if FAILS else "all checks passed")
sys.exit(1 if FAILS else 0)
