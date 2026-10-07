WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7),(2, 5, 8),
    (0, 4, 8), (2, 4, 6),
    )

def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != "." and board[a] ==  board[b] == board[c]:
            return board[a]

# A function check for a finished game
# try each empty sqaure
# recursively? with the other player
# undo the move and return the sum


def play_all_games():
    board = ["."] * 9

    def explore(player):
        # I guess a single win ends the game, even if empty squares remain
        if winner(board) is not None:
            return 1
        if "." not in board:
            return 1 # Draw case



# Set the initial amount to 0
        total = 0
        for square in range(9):
            if board[square] == ".":
                board[square] = player
                next_player = "0" if player == "X" else "X"
                total += explore(next_player)
                board[square] = "." # undo before trying another square i suppose
        return total

    return explore("X")

print(play_all_games())
