def apply_rule(state, weights, n_cells):
    """Given state, compute next one."""

    n_layers = len(state) / n_cells

    # copy previous state as the base
    new_state = state.copy()

    i = 0
    while i < n_layers:
        j = 0
        while j < n_cells:

            # current cell idx and value
            curr_idx = n_cells * i + j
            curr = state[curr_idx]

            densities = []
            energies = []

            # if there exists a higher layer
            if i < n_layers - 1:
                idx = n_cells * (i + 1) + j
            else:
                idx = curr_idx
            densities.append(state[idx])
            energies.append(weights[idx])

            # if there exists a lower layer
            if i > 0:
                idx = n_cells * (i - 1) + j
            else:
                idx = curr_idx
            densities.append(state[idx])
            energies.append(weights[idx])

            # if at the left edge, take the last one
            if j == 0:
                idx = n_cells * i + (n_cells - 1)
            # otherwise take on to the left
            else:
                idx = n_cells * i + (j - 1)
            densities.append(state[idx])
            energies.append(weights[idx])

            # if at the right edge, take the first one
            if j == n_cells - 1:
                idx = n_cells * i
            # otherwise take on to the right
            else:
                idx = n_cells * i + (j + 1)
            densities.append(state[idx])
            energies.append(weights[idx])

            total = curr * weights[curr_idx]
            for nidx in range(len(densities)):
                total += densities[nidx] * energies[nidx]

            # update state by a neighbourhood average
            new_state[curr_idx] = total / (sum(energies) + weights[curr_idx])

            j += 1
        i += 1

    # renormalize to not lose or increase total state
    previous_sum = sum(state)
    new_sum = sum(new_state)
    for idx in range(len(new_state)):
        new_state[idx] = new_state[idx] * (previous_sum / new_sum)

    return new_state
