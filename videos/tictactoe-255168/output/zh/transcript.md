# 井字棋为什么恰好有 255,168 种对局？

## 00:00 — 到底有多少种对局？
有个问题，听起来很简单。井字棋有多少种不同的对局？
> Here's a question that sounds easy. How many different games of tic-tac-toe are there?

这里说的“一局”，指的是从第一步到最后一步、按顺序排好的全部走法。所以，如果两局最后的棋盘一样，但走棋的顺序不同，那它们要算作两种不同的对局。棋盘翻转或旋转后得到的对局，也分开算。
> By a game, we mean the whole list of moves, in order. So if two games end with the same board, but the moves happened in a different order, they count as two different games. Flipped or turned versions count separately too.

猜一猜。一百？一百万？暂停一下视频，把你猜的数写下来。
> Take a guess. A hundred? A million? Pause the video and write your guess down.

答案是 255,168。在这个视频里，我们会弄清楚这个数字是怎么来的：先仔细地算，再用一段短短的电脑程序，把每一局都下一遍。
> The answer is 255,168. In this video we'll find out where that number comes from: first by careful counting, and then with a short computer program that plays every single game.


## 00:51 — 填满棋盘：9 的阶乘
先看一个更简单的问题。假设有人三子连成一线了，双方也不停，一直下到九个格子都填满。填满棋盘有多少种不同的顺序？
> Let's start with a simpler question. Suppose the players ignore three in a row, and just keep going until all nine squares are full. In how many different orders can the board fill up?

X 先走，有 9 个格子可以选。不管 X 下在哪儿，O 都还剩 8 个格子。这就是 9 个 8，所以选择数要相乘：9 乘 8 等于 72，前两步就有 72 种不同的下法。
> X goes first and has 9 squares to choose from. For each of those, O has 8 squares left. That's 9 groups of 8, so the choices multiply: 9 times 8 is 72 different ways to make the first two moves.

继续乘下去：9 乘 8 乘 7，依此类推，一直乘到 1。数学家给这种连乘起了个名字：9 的阶乘，写成 9 后面加一个感叹号。它等于 362,880。
> Keep going: 9 times 8 times 7, and so on, all the way down to 1. Mathematicians have a short name for this: nine factorial, written as a 9 with an exclamation mark. It equals 362,880.

可是，等一下。这比 255,168 还要多。我们算出来的太多了。这些多出来的对局，都是从哪儿来的？
> But wait. That's more than 255,168. Our count is too high. Where are all those extra games coming from?


## 01:42 — 对局会提前结束
问题就在这儿。真正的井字棋，一有人三子连成一线，就结束了。这一局，X 在第 5 步就赢了，所以剩下的四个格子从没下过。
> Here's the catch. Real tic-tac-toe stops as soon as someone gets three in a row. In this game, X wins on the fifth move, so the last four squares are never played.

可是 362,880 还是把这几步没下的棋也算进去了，就好像赢了以后，双方还在接着下。填满这 4 个空格子，有 4 乘 3 乘 2 乘 1，也就是 24 种不同的顺序。所以这一局被算了 24 次！我们把这些编出来的对局叫作“幽灵对局”。我们要让每一局真实的对局都只算一次。
> But our 362,880 counted those missing moves anyway, as if the players kept going after the win. The 4 empty squares can be filled in 4 times 3 times 2 times 1, so 24 ways. So this one game got counted 24 times! Let's call those made-up endings ghost games. We want to count each real game only once.

一局最早什么时候能结束？至少要到第 5 步。X 下的是第 1、3、5 步，所以到了第 5 步，才可能有人凑齐三个棋子。
> So when can a game end? Not before move 5. X plays moves 1, 3 and 5, so the fifth move is the first time anyone can have three marks.

暂停想一想：有多少种对局是 X 在第 5 步赢下的？先自己算一算，再看答案。
> Pause and ponder: how many games end with X winning on move 5? Try to count them before I show you.

这里有个办法，分三个步骤。第一，选出 X 获胜的那条线。一共有 8 条：3 排、3 列和 2 条对角线。第二，X 可以按不同的顺序填满这条线：3 乘 2 乘 1，也就是 3 的阶乘，所以有 6 种顺序。第三，第一个 O 有另外 6 个格子可以选，第二个 O 还剩 5 个格子可以选：6 乘 5 等于 30 种放法。把它们乘起来：8 乘 6 乘 30 等于 1,440 种对局。
> Here's one way, in three steps. First, pick the line X wins with. There are 8: 3 rows, 3 columns and 2 diagonals. Second, X fills that line in some order: 3 times 2 times 1, which is 3 factorial, so 6 orders. Third, O's first mark can go on any of the other 6 squares, and O's second mark on any of the 5 left: 6 times 5 is 30 ways. Multiply: 8 times 6 times 30 is 1,440 games.


## 03:31 — 手算越来越乱
那 O 在第 6 步赢下的对局呢？O 需要三子连成一线。但要小心：如果三个 X 也连成了一线，X 在第 5 步就已经赢了，还没等 O 连完，这一局就结束了。
> What about games that O wins on move 6? O needs three in a row. But careful: if X's three marks also make a line, X already won on move 5, and the game stopped before O could finish.

还是用那三个步骤：O 有 8 条线可选，O 填满这条线有 6 种顺序，三个 X 有 6 乘 5 乘 4 种放法。这样，O 一共有 5,760 种方法连成一线。然后再减去 432 种情况：三个 X 也连成了一线，正好是和 O 那条线平行的一排或一列，所以 X 抢先赢了。最后剩下 5,328 种对局。
> Use the same three steps: 8 lines for O, 6 orders for O's marks, and 6 times 5 times 4 ways to place X's three marks. That's 5,760 ways for O to finish a line. Then we subtract the 432 where X's three marks made a line too, a row or column parallel to O's, so X sneaked in a win first. That leaves 5,328 games.

在第 7、8、9 步结束的对局就麻烦多了：我们必须检查之前的每一步有没有人赢，而且下满的棋盘可能是有人赢，也可能是平局。这就变成了一团乱麻。
> For games that end on moves 7, 8 and 9, it gets much worse: we'd have to check every earlier move for a win, and a full board might be a win or a draw. It turns into a tangled mess.

手算变得这么乱的时候，我们还有 Plan B。别再想巧办法了。不如教电脑学会规则，再让它一局接一局，把所有可能的对局都下一遍。
> When counting gets this messy, there's another plan. Don't count cleverly. Instead, teach a computer the rules, and let it play every possible game, one by one.


## 04:39 — 教电脑学规则
首先，电脑需要一个棋盘。我们用一个列表来存 9 个格子。我们用的编程语言叫 Python；在 Python 里，列表里的位置从零开始编号，所以格子的编号是 0 到 8。空格子里放一个点。
> First, the computer needs a board. We'll use a list of 9 squares. In Python, the programming language we're using, the spots in a list are numbered starting from zero, so our squares are numbered 0 to 8. An empty square holds a dot.

接下来，电脑要知道怎样才算赢。我们直接把所有能赢的线都列出来，一共 8 条，每条线写成一组三个格子编号。0、1、2 号格组成最上面一排。0、4、8 号格组成一条对角线。
> Next, the computer needs to know what counts as a win. We simply list all 8 winning lines, as groups of three square numbers. Squares 0, 1 and 2 make the top row. Squares 0, 4 and 8 make a diagonal.

接下来是一个函数：在编程里，函数就是一小段有名字的程序。这个函数叫 winner，意思是“赢家”，它会检查每一条线。如果一条线上三个格子放的都一样，而且不是点，那这是谁的棋子，谁就赢了。如果没有一条线符合，winner 什么也没找到，就返回 None，意思是“没有人”。
> Next comes a function: a little mini-program with a name. This one, called winner, checks every line. If all three squares on a line hold the same mark, and that mark isn't a dot, that player has won. If no line matches, winner finds nothing, and hands back None, which means nobody.


## 05:39 — 探索每一局
最巧妙的部分来了：一个叫 explore 的函数，explore 就是“探索”的意思。我们告诉它轮到谁，它的任务是统计从现在这个棋盘往后，还可能出现多少局。
> Now for the clever part: a function called explore. We tell it whose turn it is, and its job is to count every game that can still happen from the current board.

它一开头就是两个停止条件。如果已经有人赢了，那就是下完的一局，所以 explore 返回数字 1。如果棋盘满了却没有人赢，那就是平局，也算下完的一局。
> It starts with two stopping rules. If someone has already won, that's one finished game, so explore hands back the number 1. If the board is full with no winner, that's a draw, also one finished game.

否则，这一局就还没结束。于是 explore 会试每一个空格子。它在那里放上这一方的棋子，再问自己同一个问题，这次轮到对方：从这里往后，还能下出多少局？它把所有的答案加起来。
> Otherwise, the game isn't over yet. So explore tries every empty square. It puts the player's mark there, and then asks itself the same question, now for the other player: how many games can happen from here? It adds up all the answers.

我们把第一个小棋盘放大看看，这时轮到 O。如果 O 下在右上角那格，O 就赢了：算 1 局。擦掉它，这回试试上边中间那格。然后 X 填上最后一格，结果是平局：再算 1 局。撤销这两步，再加起来：2 局。再算上另外两个分支，2 加 1 加 2 等于 5。
> Let's zoom into the first of those, with O to move. If O takes the top-right square, O wins: that's 1 game. Erase it, and try the top-middle square instead. Then X fills the last square, and it's a draw: 1 more. Undo both moves, and add up: 2 games. With the other two branches, 2 plus 1 plus 2 makes 5.

像这样，函数自己调用自己，也就是自己问自己同一个问题，就叫作递归。听起来好像会没完没了，但每调用一次就多一个棋子，所以总会碰到停止条件。想象一棵倒过来的树。空棋盘在最上面，每一种可能的走法是一个分支，而下完的每一局都是一片叶子。我们的 explore 会沿着每一条分支往下走，一次走一条，再数一数走到了多少片叶子。
> When a function calls itself, asking itself the same question like this, it's called recursive. That might sound like it goes on forever, but each call adds one more mark, so a stopping rule always kicks in. Picture an upside-down tree. The empty board is at the top, every possible move is a branch, and every finished game is a leaf. Explore walks down every branch, one at a time, and counts the leaves it reaches.

还有一行代码，很容易被忽略。程序下每一局都用同一个棋盘，就像只有一块白板。所以每探索完一步，它就要擦掉那个棋子。这叫“撤销”这一步，这样棋盘恢复原样，下一个分支就能接着试。先试走一条路，再退回来试下一条，这就叫回溯。
> There's one more line, and it's easy to miss. The program plays every game on just one board, like a single whiteboard. So after exploring a move, it erases that mark. That's called undoing the move, and it means the next branch starts fresh. Trying a path, then stepping back to try the next one, is called backtracking.


## 07:39 — 只改一行代码
想弄懂一个程序，有个好办法：故意把它改坏。暂停想一想：如果删掉“撤销”那一行，你觉得会发生什么？
> A great way to understand a program is to break it on purpose. Pause and ponder: what do you think happens if we delete the undo line?

程序只输出 3。没有了撤销，什么都不会被擦掉。程序先下一局，按顺序一格一格地填，直到 X 在第 7 步连成一条对角线。这是第 1 局。接着它去试 X 的其他下法，可是原来那个 X 还在。X 下在下边中间那格，原来那条对角线又算赢了一次：这是第 2 局。然后是右下角那格：第 3 局。现在棋盘满了，再也没有可以试的了。
> The program prints just 3. Without undo, nothing ever gets erased. The program plays one game, filling the squares in order, until X makes a diagonal on move 7. That's 1. Then it tries X's other choices, but the old X is still there. X lands on the bottom-middle square, and the old diagonal counts as a win again: that's 2. Then the bottom-right square: that's 3. Now the board is full, so there's nothing left to try.

现在把“撤销”那一行放回去，改成删掉“判断输赢”，这样对局要等棋盘满了才会停。暂停一下，先猜猜答案。
> Now put undo back, and delete the winner check instead, so games only stop when the board is full. Pause and predict the answer.

362,880。这正是 9 的阶乘！没有了判断输赢，程序在有人赢了之后还会接着下，所以它把所有幽灵对局都算进去了。它自己又找回了我们最早算出的那个数。
> 362,880. That's nine factorial! Without the winner check, the program keeps playing after a win, so it counts all the ghost games. It rediscovered our very first count.


## 09:05 — 255,168 是怎么来的
现在，我们把每一行都放回去，运行真正的程序。过了一小会儿，它输出了 255,168。
> Now let's put every line back and run the real program. After a moment, it prints 255,168.

我们按对局在第几步结束，把这个总数拆开来看。1,440 局在第 5 步结束，5,328 局在第 6 步结束，和我们手算的结果一样。然后柱子一下子升高了：约 4.8 万局在第 7 步结束，7.3 万局在第 8 步结束。有一半多一点的对局会下满 9 步：约 8.2 万局是 X 赢，还有 46,080 局是平局。加起来就是 255,168。
> Let's split that total by when each game ends. 1,440 end on move 5, and 5,328 on move 6, the same numbers we found by hand. Then the bars shoot up: about 48 thousand end on move 7, and 73 thousand on move 8. Just over half of all games use all 9 moves: about 82 thousand X wins, plus 46,080 draws. Together, that's 255,168.

再来看看，这和 9 的阶乘有什么关系。还记得吗，9 的阶乘把在第 5 步结束的每一局，都算了 24 次，每个幽灵对局算一次。在第 6 步结束的一局被算了 6 次，在第 7 步结束的，算了两次。在第 8 步或第 9 步结束的对局，最多只剩一个空格子，所以它们只算了一次。把每根柱子乘上各自被算的次数，再全部加起来，正好又是 9 的阶乘。
> And here's how it connects to nine factorial. Remember, nine factorial counted each game that ends on move 5 a total of 24 times, once for each ghost ending. A game ending on move 6 was counted 6 times, and on move 7, twice. Games that end on move 8 or 9 have at most one empty square, so they were counted just once. Multiply each bar by its number, add them up, and you get exactly nine factorial again.

谁赢的对局最多？X 赢了 131,184 局，O 赢了 77,904 局，还有 46,080 局是平局。在所有可能的对局里，X 赢的超过一半，因为先走让 X 有更多机会赢。
> Who wins the most games? X wins 131,184 of them, O wins 77,904, and 46,080 are draws. X wins in more than half of all possible games, because going first gives X more chances to win.

最后一道题。X 的第一步下在哪儿，能下出的不同对局最多：角上、边上，还是中心？暂停一下，猜一猜。
> One last puzzle. Which first move for X leads to the most different games: a corner, an edge, or the center? Pause and guess.

没想到吧：答案是边格，也就是每条边正中间的那一格，有 29,592 种对局。每个角格有 27,732，而中心最少，只有 25,872。为什么？中心在 4 条获胜线上，角格在 3 条上，而边格只在 2 条上。线越多，X 越有机会在第 5 步或第 7 步提前赢，而每一次提前赢，都会从树上砍掉一大片分支。
> Surprise: the edge, with 29,592 games. Each corner gives 27,732, and the center the fewest, just 25,872. Why? The center sits on 4 winning lines, a corner on 3, and an edge on just 2. More lines give X more chances to win early, on move 5 or 7, and every early win chops whole branches off the tree.

但要小心：能下出的对局多，不代表这一步更好。在所有先下中心的对局里，X 每 10 局大约赢 6 局。先下边格的话，X 赢不到一半。
> But careful: more games doesn't mean a better move. Out of all the games that start in the center, X wins about 6 in 10. Starting on an edge, X wins fewer than half.


## 11:38 — 更复杂的棋，轮到你了
那么，先走的 X 是不是总能赢？不是。电脑能做的，不只是统计对局。它从树的最底下开始，那里每一局都已经下完，然后一层一层往上推。每到一个分支，它都挑最好的一步：轮到 X 时挑对 X 最好的，轮到 O 时挑对 O 最好的。这样一来，它就把井字棋彻底算透了：如果双方都不失误，每一局都会是平局。所以 X 赢下的每一局，都少不了 O 在某一步的失误。
> So does going first mean X always wins? No. A computer can do more than count. It starts at the bottom of the tree, where every game is finished, and works upward. At every branch it picks the best move: best for X on X's turns, and best for O on O's turns. Doing that, it has solved tic-tac-toe: if both players play perfectly, every game ends in a draw. So every one of X's wins needs a mistake by O somewhere.

国际象棋也能这样算吗？完全不可能。1950 年，数学家兼工程师克劳德·香农估计，国际象棋至少有 10 的 120 次方种可能的对局。那可是 1 后面跟着 120 个零！而我们能观测到的整个宇宙，也只有大约 10 的 80 次方个原子。
> Could we do the same for chess? Not a chance. In 1950, the mathematician and engineer Claude Shannon estimated that chess has at least 10 to the power of 120 possible games. That's a 1 followed by 120 zeros! The whole observable universe has only about 10 to the power of 80 atoms.

所以，国际象棋程序没法探索每一个分支。它们只往后看几步，再估计谁更有希望赢，靠的是从几百万局练习中学到的经验。但说到底，思路和你刚学的一样：把走法排成一棵树，一个分支一个分支地探索。
> So chess programs can't explore every branch. They look only so many moves ahead, then estimate who's winning, using what they learned from millions of practice games. But underneath, it's the same idea you just learned: a tree of moves, explored one branch at a time.

我们来小结一下。把每一步的选择数乘起来，就得到 9 的阶乘，一共 362,880 种顺序。但只要有人赢，对局就会停下，所以这些顺序里有很多都是幽灵对局。而一段短短的递归程序，先试走一步，往下探索，再撤销，就把每一局真实对局都统计了一遍。答案正好是 255,168。
> Let's recap. Multiplying the choices gives nine factorial, 362,880 orders. But games stop when someone wins, so many of those orders are ghost games. And a short recursive program counts every real game by trying a move, exploring, and undoing it. The answer is exactly 255,168.

现在，轮到你了。改一改程序，让它只统计 X 赢的对局，或者只统计在第 7 步结束的对局，或者看看如果 O 先走会怎样。程序和挑战题的链接都在视频简介里。动手去探索吧！
> Now it's your turn. Change the program so it counts only the games X wins, or only the games that end on move 7, or see what happens if O goes first. The program and the challenges are linked in the description. Have fun exploring!

