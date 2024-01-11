import matplotlib.pyplot as plt
import numpy as np

def plot(vehicles, N):
    data = np.zeros(N,N)
    
    data = vehicle.colour for vehicle in grid

    # Show grid
    plt.grid(axis='both', color='white', linewidth=2) 
    plt.xticks(np.arange(0.5, data.shape[1], 1))  
    plt.yticks(np.arange(0.5, data.shape[0], 1))

    # Disable labels
    plt.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False) 
    
    # Plot data matrix
    plt.imshow(rgb_data, interpolation='nearest')

    # Display main axis 
    plt.show()


