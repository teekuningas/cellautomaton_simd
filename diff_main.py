import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.collections as clt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation

import numpy as np
import random
import time

from diff_automaton import apply_rule


def update_py(state):
    """Calls python-side function to update state"""

    return np.reshape(apply_rule(list(state.flatten()), state.shape[1]), state.shape)


def finite_difference(state):
    """Computes finite difference dx, dy for every cell"""
    di = np.empty(state.shape)
    dj = np.empty(state.shape)
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if i == 0:
                di[i, j] = state[i + 1, j] - state[i, j]
            elif i == state.shape[0] - 1:
                di[i, j] = state[i, j] - state[i - 1, j]
            else:
                di[i, j] = (state[i + 1, j] - state[i - 1, j]) / 2

            if j == 0:
                dj[i, j] = state[i, j + 1] - state[i, j]
            elif j == state.shape[1] - 1:
                dj[i, j] = state[i, j] - state[i, j - 1]
            else:
                dj[i, j] = (state[i, j + 1] - state[i, j - 1]) / 2
    return di, dj


if __name__ == "__main__":
    """Run as a script."""

    # Get a random initial pattern
    width = 30
    height = 20
    initial_pattern = np.empty((height, width), dtype=float)
    for i in range(height):
        for j in range(width):
            initial_pattern[i, j] = random.random()
    state = initial_pattern

    n_rows = state.shape[0]
    n_columns = state.shape[1]

    # Create a tickless figure
    fig, ax = plt.subplots()
    ax.axis("off")

    # Prepare the permanent plot properties
    ax.set_xlim([0 - 0.5, n_columns + 0.5])
    ax.set_ylim([0 - 0.5, n_rows + 0.5])

    # create a initial configuration of cells in a PatchCollection for faster plotting
    paths = []
    for column_idx in range(n_columns):
        for row_idx in range(n_rows):
            rect = patches.Rectangle(
                (column_idx, n_rows - row_idx - 1),
                1,
                1,
            )
            paths.append(rect)
    face_collection = clt.PatchCollection(
        paths, edgecolors="green", facecolors=["white"], linewidths=0.01
    )
    ax.add_collection(face_collection)

    # create a initial configuration of wind arrows
    arrows = []
    for column_idx in range(n_columns):
        for row_idx in range(n_rows):
            arrow = patches.Arrow(
                column_idx + 0.5,
                n_rows - row_idx - 0.5,
                random.random() - 0.5,
                random.random() - 0.5,
                width=0.3,
            )
            arrows.append(arrow)
    arrow_collection = clt.PatchCollection(
        arrows,
        color="blue",
    )
    ax.add_collection(arrow_collection)

    clrmap = mpl.colormaps["Greys"]

    # "main loop"
    def animation_func(idx):
        """Helper to update a single frame."""

        # time it
        beginning = time.time()

        # Get the global state
        global state

        # And update it via the automaton rule.
        state = update_py(state)

        # computation finished time
        comp_time = time.time()

        # simulate physics
        energy_before = np.sum(state)
        for j in range(n_columns // 2 - 2, n_columns // 2 + 2):
            for i in range(n_rows // 2 - 2, n_rows // 2 + 2):
                state[i, j] += random.random() / 10

        # renormalize
        energy_after = np.sum(state)
        state = state * (energy_before / energy_after)

        # compute derivative
        di, dj = finite_difference(state)

        # physics simulation finished time
        physics_time = time.time()

        # Figure out the color of each cell
        colors = []
        for column_idx in range(n_columns):
            for row_idx in range(n_rows):
                cell = state[row_idx, column_idx]
                facecolor = clrmap(1 - cell)
                colors.append(facecolor)

        # And update them
        face_collection.set_facecolors(colors)

        # Update the wind arrows
        global arrow_collection
        arrow_collection.remove()
        arrows = []
        for column_idx in range(n_columns):
            for row_idx in range(n_rows):
                arrow = patches.Arrow(
                    column_idx + 0.5,
                    n_rows - row_idx - 0.5,
                    -(dj[row_idx, column_idx] * 10),
                    (di[row_idx, column_idx] * 10),
                    width=0.3,
                )
                arrows.append(arrow)
        arrow_collection = clt.PatchCollection(
            arrows,
            color="blue",
        )
        ax.add_collection(arrow_collection)

        # timing information
        times = [
            comp_time - beginning,
            physics_time - comp_time,
            time.time() - physics_time,
        ]
        print(f"Computation: {times[0]}, physics: {times[1]}, plotting: {times[2]}")

    # Let matplotlib do the real work
    ani = FuncAnimation(fig, animation_func, frames=10000, interval=200, blit=False)
    plt.show()
