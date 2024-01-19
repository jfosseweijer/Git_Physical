# lonly file to quickly create a graph

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Get the current working directory
current_dir = os.getcwd()

# Move two directories above
grandparent_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))

# Path to the directory containing your CSV files
csv_dir = os.path.join(grandparent_dir, 'data', 'random_states')

# Iterate over files in the directory
for filename in os.listdir(csv_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(csv_dir, filename)
        data = pd.read_csv(file_path)

        # Clear the figure
        plt.clf()

        # Create a histogram with KDE
        sns.histplot(data['unique states after 1000 moves'], kde=True)

        # Create a KDE plot without plotting
        kde_values = sns.kdeplot(data['unique states after 1000 moves'], legend=False).lines[0].get_ydata()

        # Find the position and value of the peak
        peak_position = kde_values.argmax()

        plt.title(f'Histogram for {filename}')
        plt.xlabel('Value')
        plt.ylabel('Density')

        # Display peak position and value
        plt.annotate(f'Peak: {peak_position:.2f}', xy=(0.7, 0.9), xycoords='axes fraction', fontsize=10, color='green')

        save_path = os.path.join(csv_dir[:-13], f'graphs\plot_{filename[:-4]}.png')
        plt.savefig(save_path)

