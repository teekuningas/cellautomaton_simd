import numpy as np


def match_pattern(tl, tr, bl, br):
    """Helper to match patterns."""
    ###
    if np.array_equal([tl, tr, bl, br], ['x', 'o', 'o', 'o']):
        return np.array(['o', 'o','o', 'x'])
    if np.array_equal([tl, tr, bl, br], ['o', 'o', 'o', 'x']):
        return np.array(['x', 'o','o', 'o'])
    ###
    if np.array_equal([tl, tr, bl, br], ['o', 'o', 'x', 'o']):
        return np.array(['o', 'x','o', 'o'])
    if np.array_equal([tl, tr, bl, br], ['o', 'x', 'o', 'o']):
        return np.array(['o', 'o','x', 'o'])
    ###
    if np.array_equal([tl, tr, bl, br], ['x', 'x', 'o', 'o']):
        return np.array(['o', 'o','x', 'x'])
    if np.array_equal([tl, tr, bl, br], ['o', 'o', 'x', 'x']):
        return np.array(['x', 'x','o', 'o'])
    ###
    if np.array_equal([tl, tr, bl, br], ['o', 'x', 'o', 'x']):
        return np.array(['x', 'o','x', 'o'])
    if np.array_equal([tl, tr, bl, br], ['x', 'o', 'x', 'o']):
        return np.array(['o', 'x','o', 'x'])
    ###
    if np.array_equal([tl, tr, bl, br], ['o', 'x', 'x', 'o']):
        return np.array(['x', 'o','o', 'x'])
    if np.array_equal([tl, tr, bl, br], ['x', 'o', 'o', 'x']):
        return np.array(['o', 'x','x', 'o'])
    ###
    if np.array_equal([tl, tr, bl, br], ['x', 'x', 'x', 'o']):
        return np.array(['o', 'x','x', 'x'])
    if np.array_equal([tl, tr, bl, br], ['o', 'x', 'x', 'x']):
        return np.array(['x', 'x','x', 'o'])
    ###
    if np.array_equal([tl, tr, bl, br], ['x', 'o', 'x', 'x']):
        return np.array(['x', 'x','o', 'x'])
    if np.array_equal([tl, tr, bl, br], ['x', 'x', 'o', 'x']):
        return np.array(['x', 'o','x', 'x'])
    ### wall rules
    if np.array_equal([tl, tr, bl, br], ['o', 'x', 'w', 'w']):
        return np.array(['x', 'o','w', 'w'])
    if np.array_equal([tl, tr, bl, br], ['x', 'o', 'w', 'w']):
        return np.array(['o', 'x','w', 'w'])
    ###
    if np.array_equal([tl, tr, bl, br], ['w', 'x', 'w', 'o']):
        return np.array(['w', 'o','w', 'x'])
    if np.array_equal([tl, tr, bl, br], ['w', 'o', 'w', 'x']):
        return np.array(['w', 'x','w', 'o'])
    ###
    if np.array_equal([tl, tr, bl, br], ['w', 'w', 'x', 'o']):
        return np.array(['w', 'w','o', 'x'])
    if np.array_equal([tl, tr, bl, br], ['w', 'w', 'o', 'x']):
        return np.array(['w', 'w','x', 'o'])
    ###
    if np.array_equal([tl, tr, bl, br], ['x', 'w', 'o', 'w']):
        return np.array(['o', 'w','x', 'w'])
    if np.array_equal([tl, tr, bl, br], ['o', 'w', 'x', 'w']):
        return np.array(['x', 'w','o', 'w'])

    return np.array([tl, tr, bl, br])


def apply_rule(state, idx):
    """Given state, compute next one."""

    n_rows = state.shape[0]
    n_columns = state.shape[1]

    if n_rows % 2 != 0:
        raise Exception("Height should be divisible by 2")

    if n_columns % 2 != 0:
        raise Exception("Width should be divisible by 2")

    # precompute block division variables
    if idx % 2 == 0:
        start_idx = 0
        block_count_columns = int(n_columns / 2)
        block_count_rows = int(n_rows / 2)
    else:
        start_idx = 1
        block_count_columns = int((n_columns / 2 - 1))
        block_count_rows = int((n_rows / 2 - 1))

    # copy previous state as the base
    new_state = np.copy(state)

    # then replace the contents that can change
    i = 0
    while (i < block_count_rows):
        j = 0
        while (j < block_count_columns):
            # implement c-like replace system
            idx_11_i = i*2 + start_idx
            idx_11_j = j*2 + start_idx
            idx_21_i = idx_11_i + 1
            idx_21_j = idx_11_j
            idx_12_i = idx_11_i
            idx_12_j = idx_11_j + 1
            idx_22_i = idx_11_i + 1
            idx_22_j = idx_11_j + 1
            tl = state[idx_11_i, idx_11_j]
            bl = state[idx_21_i, idx_21_j]
            tr = state[idx_12_i, idx_12_j]
            br = state[idx_22_i, idx_22_j]
            new_tl, new_tr, new_bl, new_br = match_pattern(tl, tr, bl, br)
            new_state[idx_11_i, idx_11_j] = new_tl
            new_state[idx_21_i, idx_21_j] = new_bl
            new_state[idx_12_i, idx_12_j] = new_tr
            new_state[idx_22_i, idx_22_j] = new_br
            j += 1
        i += 1

    return new_state
