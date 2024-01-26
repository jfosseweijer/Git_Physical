import matplotlib.pyplot as plt
import numpy as np

def plot(self, ax1, ax2):
    """
    Plot the game board with vehicles and exit.

    Parameters:
    - vehicles: List of Vehicle objects representing the vehicles on the board.
    - size: Size of the game board.
    - exit: Tuple representing the position of the exit (row, column).
    """
    # Create a grid for the game board
    grid = np.ones((self.size, self.size, 3))

    # Mark positions of vehicles on the grid
    for vehicle in self.vehicles_list:
        for position in vehicle.positions:
            col, row = position
            grid[row][col] = vehicle.colour

    # Create a rectangle for the exit with a black border
    rect = plt.Rectangle((self.exit[1] + 0.5, self.exit[0] - 0.5), 1, 1, linewidth=5, edgecolor='black', facecolor='none', zorder=2)

    # Clear the previous plots
    ax1.clear()
    ax2.clear()

    # Plot the image with the grid on the first subplot
    ax1.imshow(grid, interpolation='nearest')

    ax1.set_xticks(np.arange(0.5, self.size + 0.5, 1))
    ax1.set_yticks(np.arange(0.5, self.size + 0.5, 1))
    ax1.grid(axis='both', color='white', linewidth=2)
    ax1.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)

    # Add the rectangle to the plot
    ax1.add_patch(rect)

    # Create legend with explicit labels on the second subplot
    for vehicle in self.vehicles_list:
        ax2.plot([], [], color=np.array(vehicle.colour), label=vehicle.name)
        ax2.legend()
        ax2.axis('off')

    # Adjust layout to prevent clipping of legend
    plt.tight_layout()
