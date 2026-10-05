from collections import Counter
from math import factorial
WIN_LINES = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
def winner(b):
    for a,c,d in WIN_LINES:
        if b[a] != "." and b[a] == b[c] == b[d]:
            return b[a]
# the user's program, verbatim logic (O written as "0")
def play_all_games():
    board = ["."]*9
    def explore(player):
        if winner(board) is not None: return 1
        if "." not in board: return 1
        total = 0
        for sq in range(9):
            if board[sq] == ".":
                board[sq] = player
                total += explore("0" if player == "X" else "X")
                board[sq] = "."
        return total
    return explore("X")
print("user program:", play_all_games())

# breakdown by length and result
by_len = Counter(); by_res = Counter(); by_len_res = Counter(); alive = Counter()
board = ["."]*9
def ex(player, depth):
    alive[depth] += 1
    w = winner(board)
    if w or "." not in board:
        r = w or "draw"
        by_len[depth] += 1; by_res[r] += 1; by_len_res[(depth, r)] += 1
        return
    for s in range(9):
        if board[s] == ".":
            board[s] = player; ex("O" if player == "X" else "X", depth+1); board[s] = "."
ex("X", 0)
print("by length:", sorted(by_len.items()), "total", sum(by_len.values()))
print("by result:", dict(by_res))
print("by length+result:", sorted(by_len_res.items()))
print("sequences reaching each depth:", sorted(alive.items()))
print("ghost identity:", sum(n*factorial(9-k) for k,n in by_len.items()), "== 9! =", factorial(9))

# variants
def variant(check_win=True, check_full=True, undo=True):
    b = ["."]*9
    def e(p):
        if check_win and winner(b) is not None: return 1
        if check_full and "." not in b: return 1
        t = 0
        for s in range(9):
            if b[s] == ".":
                b[s] = p; t += e("O" if p == "X" else "X")
                if undo: b[s] = "."
        return t
    return e("X")
print("no win check:", variant(check_win=False))
print("no draw check:", variant(check_full=False))
print("no undo:", variant(undo=False))

# hand count checks
print("move5 formula 8*3!*6*5 =", 8*6*6*5)

# distinct positions and symmetry
import itertools
syms = []
def rot(i): r,c = divmod(i,3); return c*3 + (2-r)
def refl(i): r,c = divmod(i,3); return r*3 + (2-c)
perms = []
p = list(range(9))
for k in range(4):
    perms.append(p[:]); perms.append([refl(x) for x in p])
    p = [rot(x) for x in p]
def canon(bd): return min(tuple(bd[q[i]] for i in range(9)) for q in perms)
positions = set(); canon_pos = set(); games_canon = set()
b = ["."]*9
def walk(pl, seq):
    positions.add(tuple(b)); canon_pos.add(canon(b))
    if winner(b) or "." not in b:
        games_canon.add(min(tuple(q[m] for m in seq) for q in perms)); return
    for s in range(9):
        if b[s] == ".":
            b[s] = pl; walk("O" if pl == "X" else "X", seq+[s]); b[s] = "."
walk("X", [])
print("distinct reachable positions:", len(positions), " up to symmetry:", len(canon_pos), " games up to symmetry:", len(games_canon))
