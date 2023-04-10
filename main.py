import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.collections as clt
from matplotlib.animation import FuncAnimation

import numpy as np
import time

from automaton import apply_rule


if __name__ == "__main__":
    """Run as a script."""


    initial_pattern_str = """
        wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
        wooxooooooooxoooooooooooooooooooow
        woooooxooooxooxooooxoooooooooxooow
        wooooooooxoooooxoxooooxoooooooooow
        woooooxoooooxooooooxooooooooooooow
        wooxooxooooxoooxoooooooooooooxooow
        woooooxooxoooooooooxooxoooooooooow
        wooxoooooooxoooxooooooooooooooooow
        woooxooooxoooxooooooxooooooooxooow
        woooooxoooooooooxoooooooooooooooow
        wooxoooooooxooooooooooooooooooooow
        woooooooooooooooooooooooooooxoooow
        wooooooooooxooooooooooooooooooooow
        woooxoooooooooooooooooooooxoooooow
        woooooooxoooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooow
        wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
    """

    initial_pattern = []
    for row in initial_pattern_str.split('\n'):
        rowvals = []
        for letter in row.strip():
            rowvals.append(letter)
        if rowvals:
            initial_pattern.append(rowvals)

    state = np.array(initial_pattern)

    n_rows = state.shape[0]
    n_columns = state.shape[1]

    # Create a tickless figure
    fig, ax = plt.subplots()
    ax.axis("off")

    # Prepare the permanent plot properties
    ax.set_xlim([0 - 0.5, n_columns + 0.5])
    ax.set_ylim([0 - 0.5, n_rows + 0.5])

    # create a initial configuration of cells in a PatchCollection for superfast plotting
    paths = []
    for column_idx in range(n_columns):
        for row_idx in range(n_rows):
            rect = patches.Rectangle(
                (column_idx, n_rows - row_idx - 1),
                1,
                1,
            )
            paths.append(rect)
    collection = clt.PatchCollection(paths, edgecolors='green', facecolors=['white'], linewidths=0.1)
    ax.add_collection(collection)

    def animation_func(idx):
        """Helper to update a single frame."""

        # time it
        beginning = time.time()

        # Get the global state
        global state

        # And update it via the automaton rule.
        state = apply_rule(state, idx)

        middlepoint = time.time()

        # Figure out the color of each cell
        colors = []
        for column_idx in range(n_columns):
            for row_idx in range(n_rows):
                cell = state[row_idx, column_idx]
                if cell == 'x':
                    facecolor = "black"
                elif cell == 'o':
                    facecolor = "white"
                else:
                    facecolor = "grey"
                colors.append(facecolor)
        # And only update them
        collection.set_facecolors(colors)

        # timing information
        times = [middlepoint - beginning, time.time() - middlepoint]
        print(f"Computation: {times[0]}, plotting: {times[1]}")

    # Let matplotlib do the real work
    ani = FuncAnimation(fig, animation_func, frames=1000, interval=0, blit=False)
    plt.show()
