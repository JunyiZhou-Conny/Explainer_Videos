"""统计井字棋所有可能的对局（视频里讲的那个程序）。

只要有人三子连成一线，或者棋盘满了（平局），这一局就结束了。
两局的走棋顺序不同，就算作两种不同的对局。
"""

WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # 横排
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # 竖列
    (0, 4, 8), (2, 4, 6),              # 对角线
)


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a]


def play_all_games():
    board = ["."] * 9

    def explore(player):
        if winner(board) is not None:   # 有人赢了
            return 1
        if "." not in board:            # 棋盘满了：平局
            return 1
        total = 0
        for square in range(9):
            if board[square] == ".":
                board[square] = player              # 试走一步
                next_player = "O" if player == "X" else "X"
                total += explore(next_player)       # 统计从这里往后有多少局
                board[square] = "."                 # 撤销这一步
        return total

    return explore("X")


print(play_all_games())   # 255168
