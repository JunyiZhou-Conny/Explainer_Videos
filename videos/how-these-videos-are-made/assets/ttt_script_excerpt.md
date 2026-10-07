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

## S03 · Games stop early — `s03_stop.py` · `GamesStop`

SHOW: A game plays move by move with move numbers in the squares (X1 top-left, O2 center,
X3 top-middle, O4 bottom-right, X5 top-right): X wins on move 5 (YELLOW top row). The 4 empty
squares then fill with faded, dashed "ghost" marks labelled "never played".
SAY: Here's the catch. Real tic-tac-toe stops as soon as someone gets three in a row. In this game, X wins on the fifth move, so the last four squares are never played.

SHOW: The 4 ghost marks shuffle through several different orders (small ghost move numbers 6–9
changing) while a GREEN counter ticks up "1, 2, 3, … 24"; caption "4 × 3 × 2 × 1 = 24". Tag:
"this 1 game was counted 24 times in 362,880". Caption "ghost games" over the ghost marks.
SAY: But our 362,880 counted those missing moves anyway, as if the players kept going after the win. The 4 empty squares can be filled in 4 times 3 times 2 times 1, so 24 ways. So this one game got counted 24 times! Let's call those made-up endings ghost games. We want to count each real game only once.
