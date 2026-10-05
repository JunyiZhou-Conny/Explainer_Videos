# Why are there exactly 255,168 games of tic-tac-toe? — narration script & visual plan

Audience: a middle-school student (about 11–14). Knows multiplication and the rules of
tic-tac-toe. No algebra, factorials, or programming assumed. Goal: understand (1) counting by
multiplying choices, (2) why games that stop early make the count smaller, (3) how a short
recursive program counts every game by exploring a tree and undoing moves.

All numbers below were checked by running the program (`assets/verify_counts.py`).

Conventions
- `SAY:` lines are spoken verbatim (one `voiceover` block each) and become subtitles. Numbers are
  written as digits (the narrator reads them correctly); say "nine factorial", never "9!".
- `SHOW:` lines describe what is on screen during that `SAY:` line.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer), then remove the card at the start of the next block.
- Semantic colours (fixed for the whole video):
  **X** = BLUE · **O** = ORANGE · winning line = YELLOW · draw = GREY · counts / totals = GREEN ·
  "ghost" moves that never get played = faded GREY, dashed · undo / erase = RED ·
  code = the shared code style in `scenes/common.py`.
- Board squares are numbered 0–8, left to right, top to bottom (as in the program).
- Tone: friendly, concrete, short sentences; never talk down. One idea per beat.

---

## S01 · How many games? — `s01_hook.py` · `Hook`

SHOW: An empty 3×3 board. A quick game plays out (X centre, O corner, …) ending with X's three in
a row lighting up YELLOW.
SAY: Here's a question that sounds easy. How many different games of tic-tac-toe are there?

SHOW: Two small boards side by side that end in the same final position, but with small move
numbers 1, 2, 3… in each square showing a different order. A "≠" between them; caption
"same board, different order → different games".
SAY: By a game, we mean the whole list of moves, in order. So if two games end with the same board, but the moves happened in a different order, they count as two different games.

SHOW: PONDER(8 s, "How many different games of tic-tac-toe are there? Write down a guess!")
SAY: Take a guess. A hundred? A million? Pause the video and write your guess down.

SHOW: Big GREEN "255,168". Then a small preview of the program's last line printing 255168.
SAY: The answer is 255,168. That's a strangely exact number. In this video we'll find out where it comes from: first by careful counting, and then with a short computer program that plays every single game.

---

## S02 · Filling the board: nine factorial — `s02_fill.py` · `FillTheBoard`

SHOW: Empty board; caption "What if nobody ever wins?"
SAY: Let's start with a simpler question. Suppose nobody ever wins, and the players just keep going until all nine squares are full. In how many different orders can the board fill up?

SHOW: A tree grows from an empty-board root: 9 branches (X's first move, each a tiny board with
one BLUE X), then from one of them 8 branches (O's reply). Counter "9 × 8 = 72" in GREEN.
SAY: X goes first and has 9 squares to choose from. Then O has 8 squares left. Every first move can be followed by every second move, so the choices multiply: 9 times 8 is 72 different ways to make the first two moves.

SHOW: The product builds term by term with a running total underneath:
9 → 72 → 504 → 3,024 → 15,120 → 60,480 → 181,440 → 362,880 (GREEN). Then the compact form
"9 × 8 × 7 × 6 × 5 × 4 × 3 × 2 × 1 = 9! = 362,880" with "9!" labelled "nine factorial".
SAY: Keep going: 9 times 8 times 7, and so on, all the way down to 1. Mathematicians have a short name for this: nine factorial, written as a 9 with an exclamation mark. It equals 362,880.

SHOW: "362,880" next to "255,168"; a RED "too many!" tag on 362,880.
SAY: But wait. That's more than 255,168. Our count is too high. Where are all those extra games coming from?

---

## S03 · Games stop early — `s03_stop.py` · `GamesStop`

SHOW: A game plays move by move with move numbers: X wins on move 5 (YELLOW line). The 4 empty
squares then fill with faded, dashed "ghost" marks labelled "never played".
SAY: Here's the catch. Tic-tac-toe stops as soon as someone gets three in a row. In this game, X wins on the fifth move, so the last four squares are never played.

SHOW: The ghost marks wobble; caption "ghost games". The 362,880 number shows a "includes ghosts"
tag.
SAY: But our 362,880 counted those missing moves anyway, as if the players kept going after the win. Let's call those made-up endings ghost games. We need to throw them out.

SHOW: A timeline of turns 1–9, coloured X, O, X, O, X, …; X's marks at turns 1, 3, 5 light up;
"X's 3rd mark: move 5".
SAY: So when can a game end? Not before move 5. X plays on turns 1, 3 and 5, so X can't have three marks until the fifth move.

SHOW: PONDER(12 s, "How many games end with X winning on move 5?") with the board and the
timeline still visible.
SAY: Pause and ponder: how many games end with X winning on move 5? Try to count them before I show you.

SHOW: Three steps, each with its number in GREEN:
(1) the 8 winning lines flash one by one on the board → "8 lines";
(2) X's three marks on one line get the order labels 1-2-3, then 1-3-2, … (all 6) → "3 × 2 × 1 = 6";
(3) O's two marks hop onto the other 6 squares: "6 × 5 = 30".
Then "8 × 6 × 30 = 1,440".
SAY: Here's one way. First, pick the line X wins with. There are 8 lines: 3 rows, 3 columns and 2 diagonals. Next, X places those three marks in some order: 3 times 2 times 1, so 6 orders. Finally, O's two marks go on two of the other 6 squares, in order: 6 times 5, which is 30 ways. Multiply: 8 times 6 times 30 is 1,440 games.

---

## S04 · Counting by hand gets messy — `s04_messy.py` · `Messy`

SHOW: A board where O completes a line on move 6. Then a second board where X's three marks ALSO
form a line: it gets a RED "already over at move 5!" stamp.
SAY: What about games that O wins on move 6? O needs three in a row. But careful: if X's three marks also make a line, X already won on move 5, and the game stopped before O could finish.

SHOW: "all the ways O could line up: 5,760" minus "ways where X already won: 432" = "5,328"
(GREEN).
SAY: So we count all the ways O could finish a line, which is 5,760, and subtract the 432 where X sneaked in a win first. That leaves 5,328 games.

SHOW: A table: move 5 → 1,440 ✓, move 6 → 5,328 ✓, move 7 → ?, move 8 → ?, move 9 → ?
Around the question marks, a tangle of crossing arrows and small boards labelled "did X win
before?", "did O win before?", "win or draw?".
SAY: For moves 7, 8 and 9, it gets much worse. Now we have to check that nobody won on any earlier move, and a full board might be a win or a draw. Counting by hand turns into a tangled mess of special cases.

SHOW: The tangle fades; a laptop icon appears. Caption "Plan B: let a computer play every game".
SAY: When counting gets this messy, there's another plan. Don't count cleverly. Instead, teach a computer the rules, and let it play every possible game, one by one.

---

## S05 · Teaching a computer the rules — `s05_board_code.py` · `BoardCode`

SHOW: The board with small GREY numbers 0–8 in the squares (left to right, top to bottom). Then
the nine squares slide into a row of nine boxes, each holding a dot: `board = ["."] * 9`.
SAY: First, the computer needs a board. We'll use a list of 9 squares, numbered 0 to 8, because computers like to start counting at zero. An empty square holds a dot.

SHOW: The WIN_LINES code (rows, columns, diagonals). As each triple is highlighted in the code,
its line lights up YELLOW on the numbered board: (0, 1, 2) top row … (0, 4, 8), (2, 4, 6) diagonals.
SAY: Next, the computer needs to know what counts as a win. We simply list all 8 winning lines, as groups of three square numbers. 0, 1, 2 is the top row. 0, 4, 8 is a diagonal.

SHOW: The winner() code. On an example board, a scanner checks the lines one by one (GREY ✗ for
"not all the same"), until a line with three X's lights YELLOW and the function returns "X".
SAY: Then a small function called winner checks every line. If all three squares on a line hold the same mark, and that mark isn't a dot, that player has won.

---

## S06 · Exploring every game — `s06_explore.py` · `Explore`

SHOW: The explore() code appears. Its name is highlighted.
SAY: Now for the clever part: a function called explore. Its job is to count every game that can still happen from the board it's given.

SHOW: The two stopping lines are highlighted in turn. Beside them: a won board → "1 game";
a full board with no line (GREY) → "1 game (a draw)".
SAY: It starts with two stopping rules. If someone has already won, that's one finished game, so it returns 1. If the board is full with no winner, that's a draw, also one finished game.

SHOW: The for-loop lines are highlighted. On a board, the empty squares blink; the player's mark
drops into one; an arrow leads to a smaller board labelled "explore(O): how many games from here?";
"total +=" collects the answers in a GREEN counter.
SAY: Otherwise, the game isn't over yet. So explore tries every empty square. It puts the player's mark there, and then asks the same question again, now for the other player: how many games can happen from here? It adds up all the answers.

SHOW: Zoom out to a game tree: the empty board at the top, 9 branches, then 8 under one of them,
… leaves (finished games) at the tips. A highlighted path walks down one branch to a leaf (the
board changing along the way), the leaf flashes GREEN and the counter goes up by 1.
SAY: A function that calls itself like this is called recursive. Picture a tree. The empty board is at the top, every possible move is a branch, and every finished game is a leaf at the tip of a branch. Explore walks down every branch and counts the leaves.

SHOW: The undo line is highlighted RED. On the board, the last mark is erased (RED eraser swipe)
and the highlighted path steps back up the tree, then goes down the next branch. Caption
"try → explore → undo = backtracking".
SAY: There's one more line, and it's easy to miss. After exploring a move, the program erases that mark. That's called undoing the move. It puts the board back exactly as it was, so the next branch starts fresh. Trying a path, then stepping back to try the next one, is called backtracking.

---

## S07 · Change one line — `s07_experiments.py` · `Experiments`

SHOW: The full program, small. The undo line gets a RED strike-through.
PONDER(10 s, "What happens if we delete the undo line?")
SAY: A great way to understand a program is to break it on purpose. Pause and ponder: what do you think happens if we delete the undo line?

SHOW: The board fills with marks that are never erased (X O X O X O X …); the search runs out of
empty squares almost at once; the output shows "3".
SAY: The program prints 3! Without undo, the marks pile up and never get erased, so the board fills up almost right away, and the search stops after just 3 games.

SHOW: Undo restored; now the winner-check lines get the strike-through.
PONDER(10 s, "Now delete the winner check instead. What number comes out?")
SAY: Now put undo back, and delete the winner check instead, so games only stop when the board is full. Pause and predict the answer.

SHOW: Output "362,880"; it slides next to "9! = 362,880" from S02; a GREEN ✓ "the ghost games are
back".
SAY: 362,880. That's nine factorial! Without the win check, the program keeps playing after a win, so it counts all the ghost games. It rediscovered our very first count.

SHOW: Winner check restored; the draw-check line struck through. Output "209,088"; under it
"255,168 − 46,080 = 209,088", with "46,080 draws" in GREY dropping away.
SAY: And if we keep the winner check but delete the draw check? Then a full board with no winner is never counted, so we lose all 46,080 draws, and the program prints 209,088.

---

## S08 · 255,168, explained — `s08_answer.py` · `Answer`

SHOW: A terminal window: `python play_all_games.py` → `255168` (GREEN).
SAY: Now let's run the real program. After a moment, it prints 255,168.

SHOW: A bar chart by the move on which the game ends: 5: 1,440 · 6: 5,328 · 7: 47,952 · 8: 72,576 ·
9: 81,792 X wins (BLUE) stacked with 46,080 draws (GREY). Then the sum written out:
1,440 + 5,328 + 47,952 + 72,576 + 81,792 + 46,080 = 255,168.
SAY: Let's split that total by when the games end. 1,440 end on move 5, just like we counted, and 5,328 on move 6. Then 47,952 on move 7, and 72,576 on move 8. On move 9, there are 81,792 X wins, plus 46,080 draws. Add them all up, and you get 255,168.

SHOW: Each bar gets its ghost multiplier: ×24 (4 × 3 × 2 × 1) for move 5, ×6 for move 6, ×2 for
move 7, ×1 for moves 8 and 9. The products stack into one tall GREEN bar labelled 362,880 = 9!.
SAY: And here's how it connects to nine factorial. A game that ends on move 5 leaves 4 empty squares, which could be filled in 4 times 3 times 2 times 1, so 24 ways. Those are its ghost games. Add up every game together with all of its ghost games, and you get exactly nine factorial again.

SHOW: Three bars: X wins 131,184 (BLUE), O wins 77,904 (ORANGE), draws 46,080 (GREY).
SAY: Who wins most often? X wins 131,184 games, O wins 77,904, and 46,080 are draws. Going first is a real advantage.

SHOW: PONDER(10 s, "Where should X start to have the MOST possible games: corner, edge, or centre?")
with three small boards: X in a corner, on an edge, in the centre.
SAY: One last puzzle. If X wants the most possible games, should X start in a corner, on an edge, or in the center? Pause and guess.

SHOW: Under the three boards: corner 27,732 · edge 29,592 (crowned) · centre 25,872. Then each
first mark shows its winning lines: centre 4, corner 3, edge 2.
SAY: Surprise: the edge, with 29,592 games. A corner gives 27,732, and the center only 25,872. The center sits on 4 winning lines, a corner on 3, and an edge on just 2. More lines means more early wins, and every early win chops off branches of the tree.

---

## S09 · Bigger games, and your turn — `s09_bigger.py` · `Bigger`

SHOW: The game tree again, every leaf coloured by who wins with perfect play → all paths settle on
GREY "draw". Caption "perfect play → draw".
SAY: Because a computer can check every game, tic-tac-toe is completely solved. If both players play perfectly, every game ends in a draw.

SHOW: A chessboard; a number line on a log scale: tic-tac-toe ≈ 2.5 × 10⁵ games, atoms in the
observable universe ≈ 10⁸⁰, chess ≈ 10¹²⁰ (Shannon, 1950).
SAY: Could we do the same for chess? Not a chance. In 1950, the scientist Claude Shannon estimated that chess has around 10 to the power of 120 possible games. That's far more than the number of atoms in the observable universe, which is about 10 to the power of 80.

SHOW: A huge tree where only a few promising branches are highlighted and explored; caption
"search the best branches + learn which ones are promising".
SAY: So programs that play chess or Go have to be clever. They explore only the most promising branches, and they learn from experience which branches look promising. But underneath, it's the same idea you just learned: a tree of moves, explored one branch at a time.

SHOW: Recap cards: "multiply choices → 9! = 362,880" · "games stop early → ghost games" ·
"try → explore → undo → 255,168".
SAY: Let's recap. Multiplying the choices gives nine factorial, 362,880 orders. But games stop when someone wins, so many of those orders are ghost games. And a short recursive program that tries a move, explores, and then undoes it, counts exactly 255,168 real games.

SHOW: Challenge cards: "Count only X's wins" · "Count the games that end on move 7" · "What if O
went first?" Footer: "program + challenges: companion notes (link in the description)".
SAY: Now it's your turn. Change the program so it counts only the games X wins, or only the games that end on move 7. The program and the challenges are in the notes below. Have fun exploring!
