import matplotlib.pyplot as plt
import numpy as np

def plot(vehicles, size):
    data = np.ones((size, size, 3)) 
    
    for vehicle in vehicles:
        for position in vehicle.positions:
            col, row = position
            data[row][col] = vehicle.colour/255

    fig, (ax1, ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [10, 1]}, figsize=(10, 5))

    # Plot the image with grid on the first subplot
    ax1.imshow(data, interpolation='nearest')
    ax1.grid(axis='both', color='white', linewidth=2)
    ax1.set_xticks(np.arange(0.5, size+0.5, 1))
    ax1.set_yticks(np.arange(0.5, size+0.5, 1))
    ax1.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)

    # Create legend with explicit labels on the second subplot
    for vehicle in vehicles:
        ax2.plot([], [], color=np.array(vehicle.colour) / 255.0, label=vehicle.name)
    ax2.legend()
    ax2.axis('off')

    # Adjust layout to prevent clipping of legend
    plt.tight_layout()

    # Show the figure
    plt.show()
