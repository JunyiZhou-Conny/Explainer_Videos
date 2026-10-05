# Challenges — Why are there 255,168 games of tic-tac-toe?

Try each one *before* opening the answer. Grab paper and a pencil; for the coding ones, open
[`assets/play_all_games.py`](assets/play_all_games.py) (Python 3, no extra installs needed):

```bash
python assets/play_all_games.py      # prints 255168
```

## Warm-ups (pencil and paper)

**1. The first moves.** In how many different ways can the first two moves happen (X, then O)?
The first three moves?

<details><summary>Answer</summary>

9 × 8 = **72** ways for two moves, and 9 × 8 × 7 = **504** for three. Each new move multiplies
the number of possibilities by the number of empty squares left.
</details>

**2. Why not O?** Why can't O ever win on move 5?

<details><summary>Answer</summary>

After 5 moves, O has played only twice (moves 2 and 4). You need three marks for three in a row.
O's earliest possible win is move 6.
</details>

**3. Diagonal wins.** How many games end with X winning on move 5 *along a diagonal*?

<details><summary>Answer</summary>

Same recipe as in the video, but with only 2 lines to choose from instead of 8:
2 × (3 × 2 × 1) × (6 × 5) = 2 × 6 × 30 = **360**.
</details>

**4. Tiny tic-tac-toe.** Play on a 2 × 2 board where *two* in a row wins (rows, columns and
diagonals all count). How many different games are there?

<details><summary>Answer</summary>

On a 2 × 2 board, *every* pair of squares is a line! So X always wins with their second mark, on
move 3. The number of games is just the number of ways to make 3 moves: 4 × 3 × 2 = **24**.
</details>

## Coding challenges

**5. Count only X's wins.** Change the program so it counts only the games that X wins.
Expected answer: **131,184**.

<details><summary>Hint and solution</summary>

When someone has won, return 1 only if that someone is X:

```python
w = winner(board)
if w is not None:
    return 1 if w == "X" else 0
if "." not in board:
    return 0          # draws don't count either
```
</details>

**6. Count the games that end on move 7.** Expected answer: **47,952**.

<details><summary>Hint and solution</summary>

When a game is over, count how many marks are on the board:
`moves = 9 - board.count(".")`. Return 1 only if `moves == 7`, otherwise 0.
</details>

**7. What if O goes first?** Change `explore("X")` to `explore("O")`. What do you get, and why?

<details><summary>Answer</summary>

Still **255,168**. Swapping the names X and O doesn't change the shape of the game tree; only the
labels change.
</details>

**8. Corner, edge or centre?** Make the program count the games where X's first move is in a
corner (square 0), on an edge (square 1), or in the centre (square 4). Do your numbers match the
video (27,732 · 29,592 · 25,872)? Check that 4 × corner + 4 × edge + centre = 255,168.

<details><summary>Hint</summary>

Put X on that square first (`board[0] = "X"`), then start the search with `explore("O")`.
</details>

**9. Break it on purpose.** Delete the undo line and run it. The video says it prints 3. Can you
explain *why* by following the first few moves by hand? (Write down the board after each move.)

<details><summary>Answer</summary>

Without undo, marks are never erased, so the very first game just keeps filling the board in
order: X at 0, O at 1, X at 2, O at 3, X at 4, O at 5, X at 6. Now X has 2, 4, 6, a diagonal:
that's game number 1. But the program is still inside X's loop, and X's mark on 6 was never
erased, so X also "tries" square 7 (game 2: X has still won) and square 8 (game 3). Now the board
is full, every earlier loop finds no empty squares, and the search ends with a total of **3**.
</details>

## For the curious

- With perfect play, every game of tic-tac-toe is a draw. A computer can prove this by checking
  the whole game tree (look up the **minimax** algorithm).
- There are 5,478 different boards that can appear in real games, but only 765 if you treat
  rotated and mirrored boards as the same.
- Chess is far too big for this: Claude Shannon estimated around 10¹²⁰ possible games in 1950.
  Chess programs search only the most promising branches.
