# 井字棋为什么恰好有 255,168 种对局？

## 00:00 — How many games? · 有多少种对局？
- 00:07 井字棋有多少种不同的对局？
  How many different games of tic-tac-toe are there?
- 00:11 最后的棋盘一样：算一种对局，还是两种？
  Same final board: one game or two?
- 00:16 顺序不同，或棋盘翻转、旋转：都算不同的对局
  A different order, or a flipped or turned board: a different game.

## 00:26 — Fill the board · 填满棋盘
- 00:26 先不管输赢，填满棋盘有多少种顺序？
  Forget winning: in how many orders can the board fill up?
- 00:41 从 9 一直乘到 1，叫 9 的阶乘：362,880
  Multiplying from 9 down to 1 is called nine factorial: 362,880.
- 00:45 比 255,168 还多：9 的阶乘多算了什么？
  More than 255,168: what did nine factorial count too often?

## 00:48 — Games stop early · 对局会提前结束
- 00:51 真实的对局，有人赢了就结束
  A real game ends as soon as someone wins.
- 01:00 9 的阶乘把这一局算了 24 次
  Nine factorial counted this one game 24 times.
- 01:04 这些编出来的对局，叫“幽灵对局”
  These made-up games are called ghost games.
- 01:09 一局最早也要到第 5 步才结束
  The earliest a game can end is move 5.
- 01:12 结束得越早，身后拖着的幽灵对局就越多
  The earlier a game ends, the more ghost games it drags along.

## 01:16 — Counting by hand · 手算
- 01:26 X 在第 5 步赢下的对局：1,440 种
  Games that X wins on move 5: 1,440.
- 01:33 再往后，手算就成了一团乱麻
  After that, counting by hand becomes a tangled mess.

## 01:36 — Play every game · 探索每一局
- 01:36 要是让电脑把每一局都下一遍呢？
  What if a computer plays every game, one by one?
- 01:48 先试走一步，往下探索，再撤销
  Try a move, explore what follows, then undo it.
- 01:54 有人赢了，或者棋盘满了，这一局就下完了
  Someone won, or the board is full: that game is finished.
- 02:03 按顺序走遍整棵树，一局也不漏
  In order, through the whole tree, without missing a game.
- 02:19 每一局只算一次：255,168
  Every game counted exactly once: 255,168.

## 02:26 — Delete one check · 删掉“判断输赢”
- 02:27 删掉“判断输赢”，再跑一遍
  Delete the winner check, and run it again.
- 02:39 362,880：幽灵对局全回来了
  362,880: the ghost games are back.

## 02:45 — 255,168, explained · 255,168 是怎么来的
- 02:45 255,168 种对局，怎么变成了 362,880？
  How do 255,168 games become 362,880?
- 03:02 乘上各自被算的次数，加起来又是 9 的阶乘
  Multiply each by how often it was counted, and add: nine factorial again.
- 03:09 先走的 X 赢了一半多一点的对局
  X, who goes first, wins just over half of all games.

## 03:12 — Perfect play, and chess · 双方都不失误，还有国际象棋
- 03:14 那先走的 X 只要不失误，就一定能赢吗？
  If X goes first and makes no mistakes, can X always win?
- 03:26 可要是双方都不失误，结果总是平局
  But if neither side makes a mistake, it is always a draw.
- 03:33 那国际象棋，有多少种对局？
  And how many games of chess are there?
- 03:41 国际象棋估计至少有 10 的 120 次方种对局
  By Shannon's estimate, chess has at least 10¹²⁰ games.
- 03:45 整个可观测宇宙也只有约 10 的 80 次方个原子
  The whole observable universe has only about 10⁸⁰ atoms.

## 03:55 — One tree · 同一棵树
- 04:03 255,168 种对局，每一局都是这棵树上的一条路
  255,168 games: each one is a path through this tree.
