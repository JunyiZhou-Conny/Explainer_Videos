def _check_numbers():
    b = ["."] * 9
    for i, sym in GAME:
        assert b[i] == "." and winner(b) is None
        b[i] = sym
    assert winner(b) == "X"
    assert tuple(i for i in range(9) if b[i] == ".") == GHOST_SQUARES
    assert factorial(4) == 24 and NINE_FACTORIAL == factorial(9) == 362_880
    assert len(WIN_LINES) == 8 and 8 * factorial(3) * (6 * 5) == BY_MOVE[5] == 1_440
    assert _games_won_by_x_on_move_5() == 1_440
    assert sorted(GHOST_WALK) == sorted(GHOST_SQUARES)
