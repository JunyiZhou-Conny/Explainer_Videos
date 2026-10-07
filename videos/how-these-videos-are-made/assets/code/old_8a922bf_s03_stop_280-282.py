                steps.append(([ghosts[start[cur[p]]].animate(path_arc=arc)
                               .move_to(spot[p] + offset[start[cur[p]]]) for p in moved],
                              durations[k - 1], 0))
