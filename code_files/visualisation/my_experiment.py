"""
Experiment class for generating data.


Author: Nanne Hempel
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from datetime import datetime
from ..classes.board_setup import Board as Board
from tqdm import tqdm
from itertools import product


class Experiment:
    def __init__(self, size, num_cars, algorithms=[], size_range=1, num_cars_range=1, car_truck_ratio=(3,1), car_truck_range=(1,1), HV_ratio=(1,1), HV_ratio_range=(1,1), lock_limit=1, lock_limit_range=1, min_exit_distance=2, min_exit_distance_range=1, move_max=10000, num_runs=1000):
        """
        Parameters
        ----------
            size int : Size of the board.
            size_range int : Range of the size of the board.
            num_cars int : Number of cars on the board.
            num_cars_range int : Range of the number of cars.
            car_truck_ratio tuple : Ratio of cars to trucks.
            car_truck_range tuple : Range of the car-truck ratio.
            HV_ratio tuple : Ratio of horizontal to vertical cars.
            HV_ratio_range tuple : Range of the HV ratio.
            lock_limit int : Minimum number of open spaces in column or row
            before it is considered locked. Higher values result in easier boards.
            lock_limit_range int : Range of the lock limit.
            min_exit_distance int : Minimal distance of the red car to the exit.
            min_exit_distance_range int : Range of the min exit distance.
            move_max int : Maximum number of moves. If exceeded, the board is considered unsolvable.
            num_runs int : Number of runs.
        """
        self.size = size
        self.size_range = size_range
        self.num_cars = num_cars
        self.num_cars_range = num_cars_range
        self.car_truck_ratio = car_truck_ratio
        self.car_truck_range = car_truck_range
        self.HV_ratio = HV_ratio
        self.HV_ratio_range = HV_ratio_range
        self.lock_limit = lock_limit
        self.lock_limit_range = lock_limit_range
        self.min_exit_distance = min_exit_distance
        self.min_exit_distance_range = min_exit_distance_range
        self.move_max = move_max
        self.num_runs = num_runs
        self.df_data = pd.DataFrame(columns=['size', 'num_cars', 'algorithm', 'solved', 'lock_limit', 'moves'])
        pd.option_context('mode.use_inf_as_na', True)
        self.algorithms = algorithms if len(algorithms) != 0 else ['random', 'no_reverse', 'breadth_first', 'depth_first', 'a_star']
        self.unsolved = []
    
    def breadth_first(self, size, state, cars, lock_lim, exit_dist):
        breadth_board = Board(size)
        breadth_board.setup_board(state)
        start_time = time.time()  
        try:
            breadth_board.breadth_search(self.move_max)
            solved = 'Solved' if breadth_board.won else 'Unsolved'
        except ValueError:
            solved = 'Locked'
        end_time = time.time()  
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'Breadth-first', 'solved': solved, 'lock_limit': lock_lim, 'moves': breadth_board.iterations, 'time': f"{end_time - start_time:.6f}", 'move_max': self.move_max, 'car_truck_ratio': self.car_truck_ratio, 'HV_ratio': self.HV_ratio, 'min_exit_distance': exit_dist})
        if solved != 'Solved':
            self.unsolved.append({'Breadth-first': state})


    def depth_first(self, size, state, cars, lock_lim, exit_dist):
        depth_board = Board(size)
        depth_board.setup_board(state)
        start_time = time.time()  
        try:
            depth_board.depth_search(self.move_max)
            solved = 'Solved' if depth_board.is_won() else 'Unsolved'
        except ValueError:
            solved = 'Locked'
        end_time = time.time()  
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'Depth-first', 'solved': solved, 'lock_limit': lock_lim, 'moves': depth_board.iterations, 'time': f"{end_time - start_time:.6f}", 'move_max': self.move_max, 'car_truck_ratio': self.car_truck_ratio, 'HV_ratio': self.HV_ratio, 'min_exit_distance': exit_dist})
        if solved != 'Solved':
            self.unsolved.append({'Depth-first': state})


    def randomise(self, size, state, cars, lock_lim, exit_dist):
        random_board = Board(size)
        random_board.setup_board(state)
        start_time = time.time()
        try:
            random_board.random_solve(self.move_max)
            solved = 'Solved' if random_board.is_won() else 'Unsolved'
        except ValueError:
            solved = 'Locked'
        end_time = time.time()
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'Random', 'solved': solved, 'lock_limit': lock_lim, 'moves': random_board.iterations, 'time': f"{end_time - start_time:.6f}", 'move_max': self.move_max, 'car_truck_ratio': self.car_truck_ratio, 'HV_ratio': self.HV_ratio, 'min_exit_distance': exit_dist})
        if solved != 'Solved':
            self.unsolved.append({'Random': state})

    def no_reverse(self, size, state, cars, lock_lim, exit_dist):
        no_reverse_board = Board(size)
        no_reverse_board.setup_board(state)
        start_time = time.time()
        try:
            no_reverse_board.no_reverse_solve(self.move_max)
            solved = 'Solved' if no_reverse_board.is_won() else 'Unsolved'
        except ValueError:
            solved = 'Locked'
        end_time = time.time()
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'No_reverse', 'solved': solved, 'lock_limit': lock_lim, 'moves': no_reverse_board.iterations, 'time': f"{end_time - start_time:.6f}", 'move_max': self.move_max, 'car_truck_ratio': self.car_truck_ratio, 'HV_ratio': self.HV_ratio, 'min_exit_distance': exit_dist})
        if solved != 'Solved':
            self.unsolved.append({'No_reverse': state})

    def histogram(self):
        pass

    def lmplot(self):
        plt.clf()
        sns.set_theme(style="darkgrid")
        sns.lmplot(data=self.df_data, x="moves", y="time",
             hue="algorithm", col="algorithm", col_wrap=2,)
        plt.savefig("lmplot_test_data.png")
    
    def catplot(self):
        plt.clf()
        sns.set_theme(style="darkgrid")
        sns.catplot(data=self.df_data, x="algorithm", y="moves", hue="solved", kind="bar")
        plt.savefig("catplot_test_data.png")

    def save(self, path=None): 
        now = datetime.now()  # Get the current date and time
        date_time = now.strftime("%m-%d_%H:%M")  # Format it as a string

        if path is None:
            new_path = f"data/experiments/test{date_time}.csv"
        else:
            new_path = path

        self.df_data.to_csv(new_path)

    def save_unsolved(self, path=None):
        now = datetime.now()
        date_time = now.strftime("%m-%d_%H:%M")

        if path is None:
            new_path = f"data/experiments/unsolved{date_time}.csv"
        else:
            new_path = path

        df = pd.DataFrame(self.unsolved)
        df.to_csv(new_path)
        

    def run(self):
        self.data = []
        sizes = range(self.size, self.size + self.size_range)
        cars_range = range(self.num_cars, self.num_cars + self.num_cars_range)
        lock_limits = range(self.lock_limit, self.lock_limit + self.lock_limit_range)
        exit_distances = range(self.min_exit_distance, self.min_exit_distance + self.size_range)

        for i in tqdm(range(self.num_runs)):
            for size, cars, lock_lim, exit_dist in product(sizes, cars_range, lock_limits, exit_distances):
                initial_state = Board.random_board_df(size, cars, self.car_truck_ratio, lock_lim, exit_dist, self.HV_ratio)
                for algorithm in self.algorithms:
                    if algorithm == 'random':
                        self.randomise(size, initial_state, cars, lock_lim, exit_dist)
                    elif algorithm == 'no_reverse':
                        self.no_reverse(size, initial_state, cars, lock_lim, exit_dist)
                    elif algorithm == 'breadth_first':
                        self.breadth_first(size, initial_state, cars, lock_lim, exit_dist)
                    elif algorithm == 'depth_first':
                        self.depth_first(size, initial_state, cars, lock_lim, exit_dist)

        self.df_data = pd.DataFrame(self.data)


    def export(self):
        pass

