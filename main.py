import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.collections as clt
from matplotlib.animation import FuncAnimation

import numpy as np
import time

from automaton import Cell
from automaton import State2D
from automaton import RuleSimulation


if __name__ == "__main__":
    """Run as a script."""


    initial_pattern_str = """
        wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooooooooooooooooooooooooooxooooooooooooooooooooooooow
        woooooxooooooooooooooooooooxooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooooooooooooooooxooooooooooooxoooooooooooooooooooooow
        wooooooooooooooooooooxoooxoooooooooooooooooooooooooooooooooxooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooxoooooooooooooooxooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooxooooooooooooooxooooooooooooooooooooooooxooooooxoooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooooooooooooooooooooooooooooooooxooooooooooooooooooow
        woooooooooooooooooooooooooooooxoooooooooooooxoooooooooooooooooooooooooow
        woooooooooooooooooooooxooooooooooooooooooooooooooooooxooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooxoooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooxoooooooooooxooooooooooooooooooooooooxoooooooooooooooooooooooow
        wooooooooooooooooooooooooooooooooooooooooooooooooooooooxooooooooooooooow
        wooooooooooooooooooooooooooooooxooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooxoooooooxoooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooxoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooxooooooooooooxooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooooooxooooooooooooooxooooooooxooooooooooooooooooooow
        wooooooooooooooooooooooooooooxooooooooooooooooooooooooooooooooooooooooow
        woooooooxooooooooooooooooooooooooooooooooooooooooooooooxooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooxooooooooxoooooooooxooooooooxoooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooxoooooooooooooooxooooooooooooooooooooxoooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooxoooooooooooooooooooooooooooooooooxooooooooooooooow
        wooooooooooooxooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooxooooooooooooooooxooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooxoooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooooooooooooooooooooooooooooooooxooooooooooooooooooow
        woooooooooooooooxoooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooxooooooooooooooooooooxooooooooxooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooxoooooooooooooooooooooooxooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooxooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooooooooooooooooxoooooooooooooooxooooooooooooooooooow
        woooooooooooooooooooxoooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooxooooxoooooooooooooooooxooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooxoooooooooooooooooooooooooooxooooooooooxooooooooooooooooooow
        woooooooooooooooooooooooxooooooooooooooooooooooooooooooooooxooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooooooooooooxooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooooooooooooooooooooooooooooxooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooxooooooooooooooooooooooooooxoooooxooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wooooooooooooooooooooxoooooooooooooooooooooooooooooooooxooooooooooooooow
        woooooooooooooooooooooooooooooooxoooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooooooxooooooooooooooooooooooxooooooooooooooow
        wooooooooooooooooooooooooooooooooooooooooooooooxooooooooooooooooooooooow
        wooooooooooooooooooooooooooooooooooooooooooooooooooooxooooooooooooooooow
        woooooooooooxoooooooooooooooooxoooooooooooooooooooooooooooooooooooooooow
        woooooooooooooooooooooooooooxooooooooooooooooooooooooxooooooooooooooooow
        woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow
        wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
    """

    initial_pattern = []
    for row in initial_pattern_str.split('\n'):
        rowvals = []
        for letter in row.strip():
            if letter == 'w':
                rowvals.append(Cell.WALL)
            if letter == 'o':
                rowvals.append(Cell.DEAD)
            if letter == 'x':
                rowvals.append(Cell.ALIVE)
        if rowvals:
            initial_pattern.append(rowvals)
    initial_pattern = np.array(initial_pattern, dtype=Cell)

    state = State2D(initial_pattern)
    rule = RuleSimulation()

    n_rows = state.data.shape[0]
    n_columns = state.data.shape[1]

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
    collection = clt.PatchCollection(paths, edgecolors='black', facecolors=['white'], linewidths=0.1)
    ax.add_collection(collection)

    def animation_func(idx):
        """Helper to update a single frame."""

        # time it
        beginning = time.time()

        # Get the global state
        global state

        # And update it via the automaton rule.
        state = rule.apply(state, idx)

        middlepoint = time.time()

        # Figure out the color of each cell
        colors = []
        for column_idx in range(n_columns):
            for row_idx in range(n_rows):
                cell = state.data[row_idx, column_idx]
                if cell == Cell.ALIVE:
                    facecolor = "black"
                elif cell == Cell.DEAD:
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
