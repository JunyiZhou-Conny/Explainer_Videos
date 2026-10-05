"""Count every possible game of tic-tac-toe (the program explained in the video).

A game ends as soon as someone gets three in a row, or when the board is full (a draw).
Two games are different if their moves happen in a different order.
"""

WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
)


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a]


def play_all_games():
    board = ["."] * 9

    def explore(player):
        if winner(board) is not None:   # someone won
            return 1
        if "." not in board:            # board full: a draw
            return 1
        total = 0
        for square in range(9):
            if board[square] == ".":
                board[square] = player              # make a move
                next_player = "O" if player == "X" else "X"
                total += explore(next_player)       # count games from here
                board[square] = "."                 # undo the move
        return total

    return explore("X")


print(play_all_games())   # 255168
