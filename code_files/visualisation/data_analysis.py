import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt


# Move to experiments directory
current_dir = os.getcwd()
grandparent_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
data_dir = os.path.join(grandparent_dir, 'data')
experiments_dir = os.path.join(data_dir, 'experiments')

# Read files that start with 'test'
files = [file for file in os.listdir(experiments_dir) if file.startswith('test')]

# Read files into dataframes
dfs = []
for file in files:
    df = pd.read_csv(os.path.join(experiments_dir, file))
    dfs.append(df)

# Concatenate dataframes
df = pd.concat(dfs)

