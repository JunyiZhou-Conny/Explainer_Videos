def moves_to(moves, path_arc: float):
    """A step for play_steps: moves = [(mobject, point), ...], each travels along an arc to its point.
    The `.animate`s are made only when the step plays."""
    return lambda: [m.animate(path_arc=path_arc).move_to(p) for m, p in moves]
