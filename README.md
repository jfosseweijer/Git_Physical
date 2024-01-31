# Git_Physical

# Dependencies:
  - python=3.11
  - numpy
  - pandas
  - random
  - matplotlib
  - matplotlib.backends.backend_tkagg
  - seaborn
  - itertools
  - string
  - time
  - datetime
  - tqdm
  - os
  - argparse
  - tkinter
  - PIL
  - ttkthemes
  - copy


Description:
Rush Hour Solver is a Python project in which we try to solve the game by implementing several algorithms. The game involves a grid with vehicles of different sizes, and the player's objective is to maneuver the vehicles to free the target vehicle (usually marked 'X') and navigate it to the exit. This project contains several features:

Algorithmic Approaches:                 Utilizes different algorithmic strategies, including random moves, breadth-first search, depth-first    search, and more, to find optimal solutions to Rush Hour puzzles.
Visualization Options:                  Provides options for visualizing the solving process, allowing users to observe the moves made by the algorithm.
User Interaction:                       Allows users to interact with the game boards, input their own moves, and experiment with different algorithms to solve the puzzles.
Experimentation:                        Supports experimentation with multiple game board configurations, offering insights into the efficiency of various solving algorithms.

Algorithms:
Random (`randomise.py`):                The random algorithm creates a dictionary of all posible moves and picks a random step. This process will be repeated for the n iterations or untill the game is   solved.
Depth Search (`depth_search.py`):   
Breadth search (`breadth_search.py`):   

Installation:
Export the whole project on your computer and make sure all dependencies (see `environment.yml`) are installed.

Example installation:
conda env create -f environment.yml

git clone https://github.com/your-username/your-repo.git


Usage:
In this project an interface was designed to simplify the usage. This interface provides a dropdown menu to choose from different Rush Hour game boards (labeled "game 1" to "game 8"). Select a game board from the dropdown to visualize its initial state. Choose visualization options from the second dropdown menu ("show visualisation" or "no visualisation"). 

Select "show visualisation" to observe the solving process visually. If desired, use the "Save Figure" button to provide a name and thereby save the visual representation of the first and last game board.
Choose "no visualisation" for a faster solution without visual feedback. Without visualisation it is also possible to repeat the process a number of times by providing this number in the entry box. This will create a experiment.csv providing the times of each experiment.

Experiment with different solving algorithms using the provided buttons. The algorithms also correspond to the algoritms explained above:
"depth_search":                         Executes the depth-first search algorithm.
"breadth_search":                       Executes the breadth-first search algorithm.
"Not reversing random algorithm":       Executes a random algorithm without reversing moves.
"Random":                               Executes a random move algorithm.
"User":                                 Allows the user to input moves and interact with the game board.

Example code to open the interface:
python main.py

It is also possible to collect results using `gather_data.py`.

example use:
python generate_data.py -r 1000 -s 9 -c 10 -cr 5

Various parameters can be specified; use python generate_data.py -h for an overview.

Generating data may take some time, depending on the chosen parameters.
After data generation, you will be prompted to decide whether to save the unsolved boards.
Saving unsolved boards is recommended only for a low number of runs.

The generated data is stored in 'data/experiment/'. The files are named as follows:
'size_startcars-endcars:date.csv' and optionally 'unsolved_size_startcars-endcars:date.csv' for the unsolved boards.

Experiment Methodology:

A grid search is conducted on the following parameters:

size: the size of the board
numcars: the number of cars placed on the board
lock_limit: the minimum accessible squares in a row or column
exit_distance: the minimum distance between the red car and the exit
For each combination of these parameters, a board is generated, and each algorithm is applied to it.

This process is repeated num_runs times.

It is recommended to vary only one variable by setting a range for it.
Other variations are better executed in separate terminals.

The results will later be aggregated for creating the plots.

Contributing:
This project was made by Jaap, Nanne Hempel and Thijn Swinkels


Special Thanks:
We would like to thank our supervisors, Jip Greven and Kim Koomen, for their guidance and support throughout the project. We would also like to thank the TAs for their help and feedback.