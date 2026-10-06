# Why are there exactly 255,168 games of tic-tac-toe? — narration script & visual plan (v2)

Audience: a middle-school student (about 11–14). Knows multiplication and the rules of
tic-tac-toe. No algebra, factorials, or programming assumed. Goal: understand (1) counting by
multiplying choices, (2) why games that stop early make the count smaller (each real game was
counted many times), (3) how a short recursive program counts every game by exploring a tree and
undoing moves.

All numbers below were checked by running the program (`assets/verify_counts.py`) and by three
independent reviews (accuracy, middle-school pedagogy, spoken flow).

Conventions
- `SAY:` lines are spoken verbatim (one `voiceover` block each) and become subtitles. Numbers are
  written as digits (the narrator reads them correctly); say "nine factorial", never "9!".
  Never end a SAY sentence on a digit followed by "!" (it reads as a factorial in the subtitles).
- `SHOW:` lines describe what is on screen during that `SAY:` line.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer), then remove the card at the start of the next block.
- Semantic colours (fixed for the whole video):
  **X** = BLUE · **O** = ORANGE · winning line = YELLOW · draw = GREY · counts / totals = GREEN ·
  "ghost" moves that never get played = faded GREY, dashed · undo / erase = RED ·
  code = the shared code style in `scenes/common.py`.
- Board squares are numbered 0–8, left to right, top to bottom (as in the program).
- Spelling on screen: American ("center"), to match the subtitles.
- Tone: friendly, concrete, short sentences; never talk down. One idea per beat.
- Code on screen: S05 shows `board`, `WIN_LINES` and `winner()`; S06–S07 show only `explore()`
  (lines 23–35 of `assets/play_all_games.py`), at the same size and position in both scenes.

---

## S01 · How many games? — `s01_hook.py` · `Hook`

SHOW: An empty 3×3 board. A quick game plays out (X center, O corner, …) ending with X's three in
a row lighting up YELLOW.
SAY: Here's a question that sounds easy. How many different games of tic-tac-toe are there?

SHOW: Two small boards side by side with the same final position (X on 0, 1, 2 with the top row
YELLOW; O on 3, 4), each square showing its move number. Left: X0=1, O3=2, X1=3, O4=4, X2=5.
Right: X2=1, O4=2, X0=3, O3=4, X1=5. A "≠" between them; caption "same board, different order →
different games". Then a rotated copy of the left board appears briefly with "≠" too.
SAY: By a game, we mean the whole list of moves, in order. So if two games end with the same board, but the moves happened in a different order, they count as two different games. Flipped or turned versions count separately too.

SHOW: PONDER(8 s, "How many different games of tic-tac-toe are there? Write down a guess!")
SAY: Take a guess. A hundred? A million? Pause the video and write your guess down.

SHOW: Big GREEN "255,168". Then a small preview of the program's last line printing 255168.
SAY: The answer is 255,168. In this video we'll find out where that number comes from: first by careful counting, and then with a short computer program that plays every single game.

---

## S02 · Filling the board: nine factorial — `s02_fill.py` · `FillTheBoard`

SHOW: Empty board; caption "What if the game never stopped early?" A fill plays out: X completes a
line on move 5 (it flashes YELLOW with a small "X won!" tag), but the players keep going, moves 6–9
in dimmer marks, until the board is full. Then the move numbers fly to show other fill orders.
SAY: Let's start with a simpler question. Suppose the players ignore three in a row, and just keep going until all nine squares are full. In how many different orders can the board fill up?

SHOW: A tree grows from an empty-board root: 9 branches (X's first move, each a tiny board with
one BLUE X). Under the first of them, 8 branches (O's reply, tiny boards with one ORANGE O). Then
faded copies of that 8-bundle drop under each of the other 8 first moves; label
"9 groups of 8 = 72" in GREEN.
SAY: X goes first and has 9 squares to choose from. For each of those, O has 8 squares left. That's 9 groups of 8, so the choices multiply: 9 times 8 is 72 different ways to make the first two moves.

SHOW: The product builds term by term with a running total underneath:
9 → 72 → 504 → 3,024 → 15,120 → 60,480 → 181,440 → 362,880 (GREEN). Then the compact form
"9 × 8 × 7 × 6 × 5 × 4 × 3 × 2 × 1 = 9! = 362,880" with "9!" labelled "nine factorial".
SAY: Keep going: 9 times 8 times 7, and so on, all the way down to 1. Mathematicians have a short name for this: nine factorial, written as a 9 with an exclamation mark. It equals 362,880.

SHOW: "362,880" next to "255,168"; a RED "too many!" tag on 362,880.
SAY: But wait. That's more than 255,168. Our count is too high. Where are all those extra games coming from?

---

## S03 · Games stop early — `s03_stop.py` · `GamesStop`

SHOW: A game plays move by move with move numbers in the squares (X1 top-left, O2 center,
X3 top-middle, O4 bottom-right, X5 top-right): X wins on move 5 (YELLOW top row). The 4 empty
squares then fill with faded, dashed "ghost" marks labelled "never played".
SAY: Here's the catch. Real tic-tac-toe stops as soon as someone gets three in a row. In this game, X wins on the fifth move, so the last four squares are never played.

SHOW: The 4 ghost marks shuffle through several different orders (small ghost move numbers 6–9
changing) while a GREEN counter ticks up "1, 2, 3, … 24"; caption "4 × 3 × 2 × 1 = 24". Tag:
"this 1 game was counted 24 times in 362,880". Caption "ghost games" over the ghost marks.
SAY: But our 362,880 counted those missing moves anyway, as if the players kept going after the win. The 4 empty squares can be filled in 4 times 3 times 2 times 1, so 24 ways. So this one game got counted 24 times! Let's call those made-up endings ghost games. We want to count each real game only once.

SHOW: A timeline of moves 1–9, coloured X, O, X, O, X, …; X's moves 1, 3, 5 light up;
"X's 3rd mark: move 5".
SAY: So when can a game end? Not before move 5. X plays moves 1, 3 and 5, so the fifth move is the first time anyone can have three marks.

SHOW: PONDER(20 s, "How many games end with X winning on move 5?\nHint: (1) Which line?\n(2) In
what order does X fill it?\n(3) Where can O's 2 marks go?") with the board and the timeline still
visible.
SAY: Pause and ponder: how many games end with X winning on move 5? Try to count them before I show you.

SHOW: Three steps, each with its number in GREEN:
(1) the 8 winning lines flash one by one on the board → "8 lines";
(2) X's three marks on one line get move labels 1-3-5, then 1-5-3, 3-1-5, … (all 6 orders) →
"3 × 2 × 1 = 3! = 6";
(3) O's first mark hops through the 6 other squares ("6"), then O's second mark through the 5 left
("× 5") → "6 × 5 = 30".
Then "8 × 6 × 30 = 1,440".
SAY: Here's one way, in three steps. First, pick the line X wins with. There are 8: 3 rows, 3 columns and 2 diagonals. Second, X fills that line in some order: 3 times 2 times 1, which is 3 factorial, so 6 orders. Third, O's first mark can go on any of the other 6 squares, and O's second mark on any of the 5 left: 6 times 5 is 30 ways. Multiply: 8 times 6 times 30 is 1,440 games.

---

## S04 · Counting by hand gets messy — `s04_messy.py` · `Messy`

SHOW: A board where O completes a line on move 6 (O's line YELLOW). Then a second board where X's
three marks ALSO form a line (the row parallel to O's row): it gets a RED "already over at move 5!"
stamp (no "!", which would read as a factorial).
SAY: What about games that O wins on move 6? O needs three in a row. But careful: if X's three marks also make a line, X already won on move 5, and the game stopped before O could finish.

SHOW: "ways O could line up: 5,760" with the small breakdown
"8 lines × 6 orders × (6 × 5 × 4 for X's 3 marks)"; minus "X already won: 432" with
"12 pairs (O's line, X's parallel line) × 6 × 6" (two tiny boards: two rows, two columns);
= "5,328" (GREEN).
SAY: Use the same three steps: 8 lines for O, 6 orders for O's marks, and 6 times 5 times 4 ways to place X's three marks. That's 5,760 ways for O to finish a line. Then we subtract the 432 where X's three marks made a line too, a row or column parallel to O's, so X sneaked in a win first. That leaves 5,328 games.

SHOW: A table: move 5 → 1,440 ✓, move 6 → 5,328 ✓, move 7 → ?, move 8 → ?, move 9 → ?
Around the question marks, a tangle of crossing arrows and small boards labelled "did X win
before?", "did O win before?", "win or draw?".
SAY: For games that end on moves 7, 8 and 9, it gets much worse: we'd have to check every earlier move for a win, and a full board might be a win or a draw. It turns into a tangled mess.

SHOW: The tangle fades; a laptop icon appears. Caption "Plan B: let a computer play every game".
SAY: When counting gets this messy, there's another plan. Don't count cleverly. Instead, teach a computer the rules, and let it play every possible game, one by one.

---

## S05 · Teaching a computer the rules — `s05_board_code.py` · `BoardCode`

SHOW: Top-right checklist: "board · winning lines · spot a winner" (each ticks GREEN as its beat
ends). The board with small GREY numbers 0–8 in the squares (left to right, top to bottom). Then
the nine squares slide into a row of nine boxes, each holding a dot, and the code
`board = ["."] * 9` appears with the caption "a dot, 9 times".
SAY: First, the computer needs a board. We'll use a list of 9 squares. In Python, the programming language we're using, the spots in a list are numbered starting from zero, so our squares are numbered 0 to 8. An empty square holds a dot.

SHOW: The WIN_LINES code (rows, columns, diagonals). As each triple is highlighted in the code,
its line lights up YELLOW on the numbered board: (0, 1, 2) top row … (0, 4, 8), (2, 4, 6) diagonals.
SAY: Next, the computer needs to know what counts as a win. We simply list all 8 winning lines, as groups of three square numbers. Squares 0, 1 and 2 make the top row. Squares 0, 4 and 8 make a diagonal.

SHOW: The winner() code, with small labels: `!=` "is not", `==` "is the same as", beside the
for-line "for each line: squares a, b, c". On an example board, a scanner checks the lines one by
one (GREY ✗ for "not all the same"), until a line with three X's lights YELLOW and the function
hands back "X". Then on a board with no line: the scanner finds nothing → GREY tag
"nothing found → None (nobody)".
SAY: Next comes a function: a little mini-program with a name. This one, called winner, checks every line. If all three squares on a line hold the same mark, and that mark isn't a dot, that player has won. If no line matches, winner finds nothing, and hands back None, which means nobody.

---

## S06 · Exploring every game — `s06_explore.py` · `Explore`

SHOW: The explore() code appears (lines 23–35 only). Its name and `player` are highlighted; the
`next_player` line is dimmed with the label "switch turns". Small labels: `range(9)` "squares 0 to
8"; `total +=` "add to the total".
SAY: Now for the clever part: a function called explore. We tell it whose turn it is, and its job is to count every game that can still happen from the current board.

SHOW: The two stopping lines are highlighted in turn. Beside them: a won board → "1 game";
a full board with no line (GREY) → "1 game (a draw)".
SAY: It starts with two stopping rules. If someone has already won, that's one finished game, so explore hands back the number 1. If the board is full with no winner, that's a draw, also one finished game.

SHOW: The for-loop lines are highlighted, with side labels "← try each empty square" and "← count
games from here". On a board (X to move, 3 empty squares), the empty squares blink; X's mark drops
into each in turn; arrows lead to 3 smaller boards (O to move) whose "?" become their answers 2, 1, 2;
"total +=" collects the answers in a GREEN counter: 0 → 2 → 3 → 5.
SAY: Otherwise, the game isn't over yet. So explore tries every empty square. It puts the player's mark there, and then asks itself the same question, now for the other player: how many games can happen from here? It adds up all the answers.

SHOW: Zoom into the first child of the loop beat (the one whose answer is 2): board X · · / X X O /
O X O (cells "X..XXOOXO"), caption "O to move". A tiny tree under it: O → square 2 (top-right),
column 2-5-8 lights YELLOW, leaf "1". RED eraser removes that O. O → square 1 (top-middle), then
X → square 2, full board, GREY draw, leaf "1". RED eraser undoes both. GREEN "1 + 1 = 2" travels up
to the root. Zoom back out to the loop beat: "2 + 1 + 2 = 5".
SAY: Let's zoom into the first of those, with O to move. If O takes the top-right square, O wins: that's 1 game. Erase it, and try the top-middle square instead. Then X fills the last square, and it's a draw: 1 more. Undo both moves, and add up: 2 games. With the other two branches, 2 plus 1 plus 2 makes 5.

SHOW: Zoom out to the full game tree, upside down: the empty board at the top, 9 branches, then
8 under each (label "same 9 × 8 as before!"), … leaves (finished games) at the tips, some short
(early wins), most deep. A highlighted path walks down one branch to a leaf (the board changing
along the way), the leaf flashes GREEN and the counter goes up by 1.
SAY: A function that calls itself like this is called recursive. That might sound like it goes on forever, but each call adds one more mark, so a stopping rule always kicks in. Picture an upside-down tree. The empty board is at the top, every possible move is a branch, and every finished game is a leaf. Explore walks down every branch, one at a time, and counts the leaves it reaches.

SHOW: The undo line is highlighted RED. A single whiteboard icon: every branch shares the same
board. On the board, the last mark is erased (RED eraser swipe) and the highlighted path steps back
up the tree, then goes down the next branch. Caption "try → explore → undo = backtracking".
SAY: There's one more line, and it's easy to miss. The program plays every game on just one board, like a single whiteboard. So after exploring a move, it erases that mark. That's called undoing the move, and it means the next branch starts fresh. Trying a path, then stepping back to try the next one, is called backtracking.

---

## S07 · Change one line — `s07_experiments.py` · `Experiments`

SHOW: explore() (lines 23–35), same size and position as in S06. The undo line gets a RED
strike-through.
PONDER(10 s, "What happens if we delete the undo line?")
SAY: A great way to understand a program is to break it on purpose. Pause and ponder: what do you think happens if we delete the undo line?

SHOW: A board fills square by square in order 0 → 6 with move numbers (X O X O X O X), never
erased. The 2-4-6 diagonal lights YELLOW; GREEN counter "1". No eraser: X's mark on 6 stays. A BLUE
X drops onto square 7 (counter 2, RED "?!"), then onto square 8 (counter 3, RED "?!"); the diagonal
is still YELLOW. The board is full (X O X / O X O / X X X). Output "3".
SAY: The program prints just 3. Without undo, nothing ever gets erased. The program plays one game, filling the squares in order, until X makes a diagonal on move 7. That's 1. Then it tries X's other choices, but the old X is still there. X lands on the bottom-middle square, and the old diagonal counts as a win again: that's 2. Then the bottom-right square: that's 3. Now the board is full, so there's nothing left to try.

SHOW: Undo restored; now the winner-check lines get the strike-through.
PONDER(10 s, "Now delete the winner check instead.\nWhat number comes out?\n(Hint: you've met it before!)")
SAY: Now put undo back, and delete the winner check instead, so games only stop when the board is full. Pause and predict the answer.

SHOW: Output "362,880"; it slides next to "9! = 362,880" from S02; a GREEN ✓ "the ghost games are
back". The strikes stay on until the end of the scene (S08 puts every line back).
SAY: 362,880. That's nine factorial! Without the winner check, the program keeps playing after a win, so it counts all the ghost games. It rediscovered our very first count.

---

## S08 · 255,168, explained — `s08_answer.py` · `Answer`

SHOW: explore() with the winner check restored (the strike is erased), then the end of the program
(lines 37–40) with lines 37 and 40 highlighted, label "start: empty board, X's turn". Then a terminal window: `python play_all_games.py` →
`255168` (GREEN).
SAY: Now let's put every line back and run the real program. After a moment, it prints 255,168.

SHOW: A bar chart by the move on which the game ends. Bars for moves 5 and 7 BLUE (X's moves),
6 and 8 ORANGE (O's moves), move 9 BLUE (81,792 X wins) stacked with GREY (46,080 draws); exact
labels on every bar (1,440 · 5,328 · 47,952 · 72,576 · 81,792 + 46,080). Bars 5 and 6 get a GREEN
✓ "counted by hand". Bars 7, 8, 9 grow on "Then the bars shoot up"; a bracket "just over half"
spans the move-9 bar. The exact sum writes out on "Together":
1,440 + 5,328 + 47,952 + 72,576 + 81,792 + 46,080 = 255,168.
SAY: Let's split that total by when each game ends. 1,440 end on move 5, and 5,328 on move 6, the same numbers we found by hand. Then the bars shoot up: about 48 thousand end on move 7, and 73 thousand on move 8. Just over half of all games use all 9 moves: about 82 thousand X wins, plus 46,080 draws. Together, that's 255,168.

SHOW: Each bar gets its ghost multiplier: ×24 (4 × 3 × 2 × 1) for move 5, ×6 for move 6, ×2 for
move 7, ×1 for moves 8 and 9. Products: 34,560 · 31,968 · 95,904 · 72,576 · 127,872. They stack
into one tall GREEN bar labelled 362,880 = 9!.
SAY: And here's how it connects to nine factorial. Remember, nine factorial counted each game that ends on move 5 a total of 24 times, once for each ghost ending. A game ending on move 6 was counted 6 times, and on move 7, twice. Games that end on move 8 or 9 have at most one empty square, so they were counted just once. Multiply each bar by its number, add them up, and you get exactly nine factorial again.

SHOW: The BLUE bars slide together into "X wins 131,184" (BLUE), the ORANGE bars into
"O wins 77,904" (ORANGE), the GREY part into "draws 46,080" (GREY).
SAY: Who wins the most games? X wins 131,184 of them, O wins 77,904, and 46,080 are draws. X wins in more than half of all possible games, because going first gives X more chances to win.

SHOW: PONDER(10 s, "Which first move for X leads to the MOST different games: corner, edge, or center?")
with three small boards: X in a corner, on an edge, in the center.
SAY: One last puzzle. Which first move for X leads to the most different games: a corner, an edge, or the center? Pause and guess.

SHOW: Under the three boards: "each corner 27,732 (×4)" · "each edge 29,592 (×4)" (crowned) ·
"center 25,872 (×1)", then "4 × 27,732 + 4 × 29,592 + 25,872 = 255,168". Then each first mark
shows its winning lines: center 4, corner 3, edge 2.
SAY: Surprise: the edge, with 29,592 games. Each corner gives 27,732, and the center the fewest, just 25,872. Why? The center sits on 4 winning lines, a corner on 3, and an edge on just 2. More lines give X more chances to win early, on move 5 or 7, and every early win chops whole branches off the tree.

SHOW: The edge board's crown turns into a small caution sign. Two win bars: "start in the center:
X wins about 6 in 10 games" vs "start on an edge: X wins fewer than half".
SAY: But careful: more games doesn't mean a better move. Out of all the games that start in the center, X wins about 6 in 10. Starting on an edge, X wins fewer than half.

---

## S09 · Bigger games, and your turn — `s09_bigger.py` · `Bigger`

SHOW: A small game tree with leaves keeping their real colours (BLUE X wins, ORANGE O wins, GREY
draws). Colours bubble up from the leaves: at X's turns a node takes the best result for X, at O's
turns the best result for O. The root ends up GREY; caption "perfect play → draw".
SAY: So does going first mean X always wins? No. A computer can do more than count. At every branch it can pick the best move: best for X on X's turns, and best for O on O's turns. Doing that, it has solved tic-tac-toe: if both players play perfectly, every game ends in a draw.

SHOW: A chessboard. Three written-out numbers as digit strips: "tic-tac-toe: 255,168 (6 digits)",
"atoms in the observable universe: about 1 followed by 80 zeros", "chess: at least 1 followed by
120 zeros (Shannon, 1950)", the strips drawn to length so the chess strip is the longest.
SAY: Could we do the same for chess? Not a chance. In 1950, the mathematician and engineer Claude Shannon estimated that chess has at least 10 to the power of 120 possible games. That's a 1 followed by 120 zeros! The whole observable universe has only about 10 to the power of 80 atoms.

SHOW: A huge tree where only a few branches near the top are explored a few levels deep; at the
cut-off, small "≈ who's winning?" gauges appear; caption "look a few moves ahead + estimate who's
winning (learned from millions of practice games)".
SAY: So chess programs can't explore every branch. They look only so many moves ahead, then estimate who's winning, using what they learned from millions of practice games. But underneath, it's the same idea you just learned: a tree of moves, explored one branch at a time.

SHOW: Recap cards: "multiply choices → nine factorial = 362,880" · "games stop early → ghost
games" · "try → explore → undo → 255,168".
SAY: Let's recap. Multiplying the choices gives nine factorial, 362,880 orders. But games stop when someone wins, so many of those orders are ghost games. And a short recursive program counts every real game by trying a move, exploring, and undoing it. The answer is exactly 255,168.

SHOW: Challenge cards: "Count only X's wins" · "Count the games that end on move 7" · "What if O
went first?" Footer: "program + challenges: linked in the description".
SAY: Now it's your turn. Change the program so it counts only the games X wins, or only the games that end on move 7, or see what happens if O goes first. The program and the challenges are linked in the description. Have fun exploring!
