# Why are there exactly 255,168 games of tic-tac-toe?

## 00:00 — How many games?
Here's a question that sounds easy. How many different games of tic-tac-toe are there?
By a game, we mean the whole list of moves, in order. So if two games end with the same board, but the moves happened in a different order, they count as two different games. Flipped or turned versions count separately too.
Take a guess. A hundred? A million? Pause the video and write your guess down.
The answer is 255,168. In this video we'll find out where that number comes from: first by careful counting, and then with a short computer program that plays every single game.

## 00:48 — Filling the board: 9!
Let's start with a simpler question. Suppose the players ignore three in a row, and just keep going until all nine squares are full. In how many different orders can the board fill up?
X goes first and has 9 squares to choose from. For each of those, O has 8 squares left. That's 9 groups of 8, so the choices multiply: 9 times 8 is 72 different ways to make the first two moves.
Keep going: 9 times 8 times 7, and so on, all the way down to 1. Mathematicians have a short name for this: nine factorial, written as a 9 with an exclamation mark. It equals 362,880.
But wait. That's more than 255,168. Our count is too high. Where are all those extra games coming from?

## 01:40 — Games stop early
Here's the catch. Real tic-tac-toe stops as soon as someone gets three in a row. In this game, X wins on the fifth move, so the last four squares are never played.
But our 362,880 counted those missing moves anyway, as if the players kept going after the win. The 4 empty squares can be filled in 4 times 3 times 2 times 1, so 24 ways. So this one game got counted 24 times! Let's call those made-up endings ghost games. We want to count each real game only once.
So when can a game end? Not before move 5. X plays moves 1, 3 and 5, so the fifth move is the first time anyone can have three marks.
Pause and ponder: how many games end with X winning on move 5? Try to count them before I show you.
Here's one way, in three steps. First, pick the line X wins with. There are 8: 3 rows, 3 columns and 2 diagonals. Second, X fills that line in some order: 3 times 2 times 1, which is 3 factorial, so 6 orders. Third, O's first mark can go on any of the other 6 squares, and O's second mark on any of the 5 left: 6 times 5 is 30 ways. Multiply: 8 times 6 times 30 is 1,440 games.

## 03:22 — Counting by hand gets messy
What about games that O wins on move 6? O needs three in a row. But careful: if X's three marks also make a line, X already won on move 5, and the game stopped before O could finish.
Use the same three steps: 8 lines for O, 6 orders for O's marks, and 6 times 5 times 4 ways to place X's three marks. That's 5,760 ways for O to finish a line. Then we subtract the 432 where X's three marks made a line too, a row or column parallel to O's, so X sneaked in a win first. That leaves 5,328 games.
For games that end on moves 7, 8 and 9, it gets much worse: we'd have to check every earlier move for a win, and a full board might be a win or a draw. It turns into a tangled mess.
When counting gets this messy, there's another plan. Don't count cleverly. Instead, teach a computer the rules, and let it play every possible game, one by one.

## 04:25 — Teaching a computer the rules
First, the computer needs a board. We'll use a list of 9 squares. In Python, the programming language we're using, the spots in a list are numbered starting from zero, so our squares are numbered 0 to 8. An empty square holds a dot.
Next, the computer needs to know what counts as a win. We simply list all 8 winning lines, as groups of three square numbers. Squares 0, 1 and 2 make the top row. Squares 0, 4 and 8 make a diagonal.
Next comes a function: a little mini-program with a name. This one, called winner, checks every line. If all three squares on a line hold the same mark, and that mark isn't a dot, that player has won. If no line matches, winner finds nothing, and hands back None, which means nobody.

## 05:14 — Exploring every game
Now for the clever part: a function called explore. We tell it whose turn it is, and its job is to count every game that can still happen from the current board.
It starts with two stopping rules. If someone has already won, that's one finished game, so explore hands back the number 1. If the board is full with no winner, that's a draw, also one finished game.
Otherwise, the game isn't over yet. So explore tries every empty square. It puts the player's mark there, and then asks itself the same question, now for the other player: how many games can happen from here? It adds up all the answers.
Let's zoom into the first of those, with O to move. If O takes the top-right square, O wins: that's 1 game. Erase it, and try the top-middle square instead. Then X fills the last square, and it's a draw: 1 more. Undo both moves, and add up: 2 games. With the other two branches, 2 plus 1 plus 2 makes 5.
When a function calls itself, asking itself the same question like this, it's called recursive. That might sound like it goes on forever, but each call adds one more mark, so a stopping rule always kicks in. Picture an upside-down tree. The empty board is at the top, every possible move is a branch, and every finished game is a leaf. Explore walks down every branch, one at a time, and counts the leaves it reaches.
There's one more line, and it's easy to miss. The program plays every game on just one board, like a single whiteboard. So after exploring a move, it erases that mark. That's called undoing the move, and it means the next branch starts fresh. Trying a path, then stepping back to try the next one, is called backtracking.

## 07:00 — Change one line
A great way to understand a program is to break it on purpose. Pause and ponder: what do you think happens if we delete the undo line?
The program prints just 3. Without undo, nothing ever gets erased. The program plays one game, filling the squares in order, until X makes a diagonal on move 7. That's 1. Then it tries X's other choices, but the old X is still there. X lands on the bottom-middle square, and the old diagonal counts as a win again: that's 2. Then the bottom-right square: that's 3. Now the board is full, so there's nothing left to try.
Now put undo back, and delete the winner check instead, so games only stop when the board is full. Pause and predict the answer.
362,880. That's nine factorial! Without the winner check, the program keeps playing after a win, so it counts all the ghost games. It rediscovered our very first count.

## 08:18 — 255,168, explained
Now let's put every line back and run the real program. After a moment, it prints 255,168.
Let's split that total by when each game ends. 1,440 end on move 5, and 5,328 on move 6, the same numbers we found by hand. Then the bars shoot up: about 48 thousand end on move 7, and 73 thousand on move 8. Just over half of all games use all 9 moves: about 82 thousand X wins, plus 46,080 draws. Together, that's 255,168.
And here's how it connects to nine factorial. Remember, nine factorial counted each game that ends on move 5 a total of 24 times, once for each ghost ending. A game ending on move 6 was counted 6 times, and on move 7, twice. Games that end on move 8 or 9 have at most one empty square, so they were counted just once. Multiply each bar by its number, add them up, and you get exactly nine factorial again.
Who wins the most games? X wins 131,184 of them, O wins 77,904, and 46,080 are draws. X wins in more than half of all possible games, because going first gives X more chances to win.
One last puzzle. Which first move for X leads to the most different games: a corner, an edge, or the center? Pause and guess.
Surprise: the edge, with 29,592 games. Each corner gives 27,732, and the center the fewest, just 25,872. Why? The center sits on 4 winning lines, a corner on 3, and an edge on just 2. More lines give X more chances to win early, on move 5 or 7, and every early win chops whole branches off the tree.
But careful: more games doesn't mean a better move. Out of all the games that start in the center, X wins about 6 in 10. Starting on an edge, X wins fewer than half.

## 10:45 — Bigger games, and your turn
So does going first mean X always wins? No. A computer can do more than count. It starts at the bottom of the tree, where every game is finished, and works upward. At every branch it picks the best move: best for X on X's turns, and best for O on O's turns. Doing that, it has solved tic-tac-toe: if both players play perfectly, every game ends in a draw. So every one of X's wins needs a mistake by O somewhere.
Could we do the same for chess? Not a chance. In 1950, the mathematician and engineer Claude Shannon estimated that chess has at least 10 to the power of 120 possible games. That's a 1 followed by 120 zeros! The whole observable universe has only about 10 to the power of 80 atoms.
So chess programs can't explore every branch. They look only so many moves ahead, then estimate who's winning, using what they learned from millions of practice games. But underneath, it's the same idea you just learned: a tree of moves, explored one branch at a time.
Let's recap. Multiplying the choices gives nine factorial, 362,880 orders. But games stop when someone wins, so many of those orders are ghost games. And a short recursive program counts every real game by trying a move, exploring, and undoing it. The answer is exactly 255,168.
Now it's your turn. Change the program so it counts only the games X wins, or only the games that end on move 7, or see what happens if O goes first. The program and the challenges are linked in the description. Have fun exploring!
