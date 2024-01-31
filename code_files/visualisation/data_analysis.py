"""
This script processes the data gathered by `gather_data.py` and creates visualizations.
The visualizations are saved in the `data/experiment_plots` directory.
The parameters of the plots can be changed with command-line arguments.
The parameters are:
- Whether to only use solved boards
- Maximum number of moves
- Number of cars
- Size of the board

Usage:
    python data_analysis.py -s -m <move_max> -n <num_cars> -si <size>
"""

import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
import numpy as np
import argparse


def main(solved, move_max, num_cars, size):
    # Read data
    df = read_data()

    # Clean unnecessary variations
    df = df[df['HV_ratio'] == '(1, 1)']
    df = df[df['car_truck_ratio'] == '(3, 1)']

    # Filter out boards with more than move_max moves
    df = df[df['moves'] <= move_max]

    df = df[df['size'] == size]

    if num_cars != 0:
        df = df[df['num_cars'] == num_cars]
    
    if solved:
        df, path = only_solved(df)
    else:
        path = 'data/experiment_plots/all/'


    path += f'max:{move_max}_num_cars:{num_cars}_size:{size}/'
    os.makedirs(path, exist_ok=True)
    
    time_plot(df, path)
    time_dist(df, path)
    move_plot(df, path)

    if solved:
        solved_by_cars(df, path)
    
    print("Files saved in: ", path)
    print_means(df)


def print_means(df):
    print(df.groupby(['algorithm', 'size', 'num_cars'])['moves'].mean())

def only_solved(df):
    # Filter out unsolved boards and make new directory
    df = df[df['solved'] == 'Solved']
    path = 'data/experiment_plots/solved/'

    return df, path

def read_data():
    # Move to experiments directory
    current_dir = os.getcwd()
    data_dir = os.path.join(current_dir, 'data')
    experiments_dir = os.path.join(data_dir, 'experiment')

    # Read files 
    files = [file for file in os.listdir(experiments_dir)]

    # Read files into dataframes
    dfs = []
    for file in files:
        df = pd.read_csv(os.path.join(experiments_dir, file))
        dfs.append(df)

    # Concatenate dataframes
    df = pd.concat(dfs)
    # Name first column 'board'
    df = df.rename(columns={'Unnamed: 0': 'board'})
    df['board'] = df.index // 4
    return df

def move_plot(df, path):
    
    depth_baseline = pd.concat([df[df['algorithm'] == 'Depth-first'], df[df['algorithm'] == 'Random']])
    breadth_baseline = pd.concat([df[df['algorithm'] == 'Breadth-first'], df[df['algorithm'] == 'Random']])

    depth_no_reverse_baseline = pd.concat([df[df['algorithm'] == 'Depth-first'], df[df['algorithm'] == 'No_reverse']])
    breadth_no_reverse_baseline = pd.concat([df[df['algorithm'] == 'Breadth-first'], df[df['algorithm'] == 'No_reverse']])

    # Plot distribution of moves log scale
    sns.set_style('darkgrid')
    sns.displot(df, x='moves', bins=125, hue='algorithm')
    plt.savefig(path + 'moves_all.png')
    
    # Plot distribution of moves log scale
    sns.set_style('darkgrid')
    sns.displot(depth_baseline, x='moves', bins=125, hue='algorithm')
    plt.savefig(path + 'depth_base_moves.png')

    plt.clf()
    sns.set_style('darkgrid')
    sns.displot(breadth_baseline, x='moves', bins=125, hue='algorithm')
    plt.savefig(path + 'breadth_base_moves.png')
    plt.clf()

    sns.set_style('darkgrid')
    sns.displot(depth_no_reverse_baseline, x='moves', bins=125, hue='algorithm')
    plt.savefig(path + 'depth_no_reverse_base_moves.png')
    plt.clf()

    sns.set_style('darkgrid')
    sns.displot(breadth_no_reverse_baseline, x='moves', bins=125, hue='algorithm')
    plt.savefig(path + 'breadth_no_reverse_base_moves.png')


def time_plot(df, path):

    # Make time column log scale
    df['time'] = np.log10(df['time'])
    df = df.reset_index(drop=True)
    depth_baseline = pd.concat([df[df['algorithm'] == 'Depth-first'], df[df['algorithm'] == 'Random']])
    breadth_baseline = pd.concat([df[df['algorithm'] == 'Breadth-first'], df[df['algorithm'] == 'Random']])

    depth_no_reverse_baseline = pd.concat([df[df['algorithm'] == 'Depth-first'], df[df['algorithm'] == 'No_reverse']])
    breadth_no_reverse_baseline = pd.concat([df[df['algorithm'] == 'Breadth-first'], df[df['algorithm'] == 'No_reverse']])

    # Plot scatterplot of time
    sns.set_style('darkgrid')
    sns.scatterplot(data=df, x='moves', y='time', hue='algorithm')
    plt.savefig(path + 'time_all.png')
    plt.clf()   
    # Plot scatterplot of time
    sns.set_style('darkgrid')
    sns.scatterplot(data=depth_baseline, x='moves', y='time', hue='algorithm')
    plt.savefig(path + 'time_depth_base.png')

    plt.clf()
    # Plot scatterplot of time
    sns.set_style('darkgrid')
    sns.scatterplot(data=breadth_baseline, x='moves', y='time', hue='algorithm')
    plt.savefig(path + 'time_breadth_base.png')
    plt.clf()

    sns.set_style('darkgrid')
    sns.scatterplot(data=depth_no_reverse_baseline, x='moves', y='time', hue='algorithm')
    plt.savefig(path + 'time_depth_no_reverse_base.png')
    plt.clf()

    sns.set_style('darkgrid')
    sns.scatterplot(data=breadth_no_reverse_baseline, x='moves', y='time', hue='algorithm')
    plt.savefig(path + 'time_breadth_no_reverse_base.png')
    plt.clf()

def time_dist(df, path):
    
    depth_baseline = pd.concat([df[df['algorithm'] == 'Depth-first'], df[df['algorithm'] == 'Random']])
    breadth_baseline = pd.concat([df[df['algorithm'] == 'Breadth-first'], df[df['algorithm'] == 'Random']])

    depth_no_reverse_baseline = pd.concat([df[df['algorithm'] == 'Depth-first'], df[df['algorithm'] == 'No_reverse']])
    breadth_no_reverse_baseline = pd.concat([df[df['algorithm'] == 'Breadth-first'], df[df['algorithm'] == 'No_reverse']])

    # Plot distribution of time log scale
    sns.set_style('darkgrid')
    sns.displot(df, x='time', bins=125, hue='algorithm')
    plt.savefig(path + 'dist_time_all.png')
    plt.clf()

    # Plot distribution of time log scale
    sns.set_style('darkgrid')
    sns.displot(depth_baseline, x='time', bins=125, hue='algorithm')
    plt.savefig(path + 'dist_time_depth_base.png')
    plt.clf()

    sns.set_style('darkgrid')
    sns.displot(breadth_baseline, x='time', bins=125, hue='algorithm')
    plt.savefig(path + 'dist_time_breadth_base.png')
    plt.clf()

    sns.set_style('darkgrid')
    sns.displot(depth_no_reverse_baseline, x='time', bins=125, hue='algorithm')
    plt.savefig(path + 'dist_time_depth_no_reverse_base.png')
    plt.clf()

    sns.set_style('darkgrid')
    sns.displot(breadth_no_reverse_baseline, x='time', bins=125, hue='algorithm')
    plt.savefig(path + 'dist_time_breadth_no_reverse_base.png')
    plt.clf()



def solved_by_cars(df, path):

    sns.set_style('darkgrid')
    sns.countplot(data=df, x='num_cars', hue='algorithm')
    plt.title('Count of solved boards per number of cars')
    plt.savefig(path + 'solved_per_num_cars.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--solved', action='store_true')
    parser.add_argument('-si','--board_size', type=int, default=9)
    parser.add_argument('-n','--num_cars', type=int, default=0, help='0 for all')
    parser.add_argument('-m','--move_max', type=int, default=2500)
    args = parser.parse_args()

    
    main(args.solved, args.move_max, args.num_cars, args.board_size)
