import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.collections as clt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation

import numpy as np
import random
import time

from wind_automaton import apply_rule


def update_py(state, weights):
    """Calls python-side function to update state"""

    # return density
    return np.reshape(
        apply_rule(list(state.flatten()), list(weights.flatten()), state.shape[1]),
        weights.shape,
    )


if __name__ == "__main__":
    """Run as a script."""

    n_cells = 70
    n_layers = 5

    sphere_radius = 10
    cell_radius = 1.0

    density = np.random.random((n_layers, n_cells))
    energy = np.ones((n_layers, n_cells)) * 0.25

    # Create a tickless figure
    fig, (ax_density, ax_energy) = plt.subplots(ncols=2)
    ax_density.axis("off")
    ax_energy.axis("off")

    # Prepare the permanent plot properties
    ax_density.set_xlim([-2 * sphere_radius, 2 * sphere_radius])
    ax_density.set_ylim([-2 * sphere_radius, 2 * sphere_radius])

    # Prepare the permanent plot properties
    ax_energy.set_xlim([-2 * sphere_radius, 2 * sphere_radius])
    ax_energy.set_ylim([-2 * sphere_radius, 2 * sphere_radius])

    ax_density.set_title("Density")
    ax_energy.set_title("Energy")

    # Add a blue sphere
    sphere = plt.Circle((0, 0), sphere_radius, color="b")
    ax_density.add_patch(sphere)
    sphere = plt.Circle((0, 0), sphere_radius, color="b")
    ax_energy.add_patch(sphere)

    # Add a couple of green spheres
    sphere1 = plt.Circle(
        ((1 / 3) * sphere_radius, (1 / 3) * sphere_radius), sphere_radius / 4, color="g"
    )
    sphere2 = plt.Circle((-(1 / 3) * sphere_radius, 0), sphere_radius / 4, color="g")
    sphere3 = plt.Circle(
        ((1 / 3) * sphere_radius, -(1 / 3) * sphere_radius),
        sphere_radius / 4,
        color="g",
    )
    ax_density.add_patch(sphere1)
    ax_density.add_patch(sphere2)
    ax_density.add_patch(sphere3)
    sphere1 = plt.Circle(
        ((1 / 3) * sphere_radius, (1 / 3) * sphere_radius), sphere_radius / 4, color="g"
    )
    sphere2 = plt.Circle((-(1 / 3) * sphere_radius, 0), sphere_radius / 4, color="g")
    sphere3 = plt.Circle(
        ((1 / 3) * sphere_radius, -(1 / 3) * sphere_radius),
        sphere_radius / 4,
        color="g",
    )
    ax_energy.add_patch(sphere1)
    ax_energy.add_patch(sphere2)
    ax_energy.add_patch(sphere3)

    # create a initial configuration of cells in a PatchCollection for faster plotting
    paths = []
    for layer_idx in range(n_layers):
        for cell_idx in range(n_cells):
            x = np.cos(cell_idx / (n_cells / (np.pi * 2))) * (
                sphere_radius + layer_idx * cell_radius * 2
            )
            y = np.sin(cell_idx / (n_cells / (np.pi * 2))) * (
                sphere_radius + layer_idx * cell_radius * 2
            )

            circle = patches.Circle((x, y), radius=cell_radius)
            paths.append(circle)
    density_face_collection = clt.PatchCollection(
        paths, edgecolors="green", facecolors=["white"], linewidths=0.01
    )
    ax_density.add_collection(density_face_collection)

    # create a initial configuration of cells in a PatchCollection for faster plotting
    paths = []
    for layer_idx in range(n_layers):
        for cell_idx in range(n_cells):
            x = np.cos(cell_idx / (n_cells / (np.pi * 2))) * (
                sphere_radius + layer_idx * cell_radius * 2
            )
            y = np.sin(cell_idx / (n_cells / (np.pi * 2))) * (
                sphere_radius + layer_idx * cell_radius * 2
            )

            circle = patches.Circle((x, y), radius=cell_radius)
            paths.append(circle)
    energy_face_collection = clt.PatchCollection(
        paths, edgecolors="green", facecolors=["white"], linewidths=0.01
    )
    ax_energy.add_collection(energy_face_collection)

    # "main loop"
    def animation_func(idx):
        """Helper to update a single frame."""

        # Get the global state
        global energy
        global density

        # Update density
        density = update_py(density, np.ones(density.shape))

        # Update energy
        energy = update_py(energy, density)

        # simulate physics
        energy_before = np.sum(energy)
        for j in range(n_cells // 4 - 2, n_cells // 4 + 2):
            energy[0, j] = 0.5 * random.random() + 0.5
        energy = energy * (energy_before / np.sum(energy))

        # Simulate gravity
        density_before = np.sum(density)
        for i in range(n_layers - 1):
            for j in range(n_cells):
                change = (
                    (1 / density[i, j]) * density[i + 1, j] * 0.2 * (0.5 - energy[i, j])
                )
                density[i, j] = density[i, j] + change
                density[i + 1, j] = density[i + 1, j] - change
        density = density * (density_before / np.sum(density))

        # Draw colors
        density_colors = []
        energy_colors = []
        for layer_idx in range(n_layers):
            for cell_idx in range(n_cells):
                density_colors.append(str(min(1, max(0, density[layer_idx, cell_idx]))))
                energy_colors.append(str(min(1, max(0, energy[layer_idx, cell_idx]))))
        # And update them
        density_face_collection.set_facecolors(density_colors)
        energy_face_collection.set_facecolors(energy_colors)

    # Let matplotlib do the real work
    ani = FuncAnimation(fig, animation_func, frames=10000, interval=500, blit=False)
    plt.show()
