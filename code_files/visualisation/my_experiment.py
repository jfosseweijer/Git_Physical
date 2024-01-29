"""
Experiment class for generating data.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
from datetime import datetime
from ..classes.board_setup import Board
from tqdm import tqdm
from itertools import product


class Experiment:
    def __init__(self, size, num_cars, algorithms=[], size_range=[6], num_cars_range=1, car_truck_ratio=(3,1), car_truck_range=(1,1), HV_ratio=(1,1), HV_ratio_range=(1,1), lock_limit=1, lock_limit_range=1, min_exit_distance=2, move_max=10000, num_runs=1000):
        """
        Parameters
        ----------
            size int : Size of the board.
            size_range list : Range of the size of the board.
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
        self.move_max = move_max
        self.num_runs = num_runs
        self.df_data = pd.DataFrame(columns=['size', 'num_cars', 'algorithm', 'solved', 'lock_limit', 'moves'])
        pd.option_context('mode.use_inf_as_na', True)
        self.algorithms = algorithms if len(algorithms) != 0 else ['random', 'no_reverse', 'breadth_first', 'depth_first', 'a_star']
        self.unsolved = []

    def a_star(self, size, state, cars, lock_lim):
        #astar_board = Board(size)
        #astar_board.setup_board(state)
        #start_time = time.time()
        #astar_board.a_star(self.move_max)
        #end_time = time.time()
        #self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'A_star', 'solved': astar_board.won, 'lock_limit': lock_lim, 'moves': astar_board.iterations, 'time': f"{end_time - start_time:.6f}", 'move_max': self.move_max})
        #if not astar_board.won:
        #    self.unsolved.append({'A_star': astar_board})
        pass
    
    def breadth_first(self, size, state, cars, lock_lim):
        breadth_board = Board(size)
        breadth_board.setup_board(state)
        start_time = time.time()  
        breadth_board.breadth_search(self.move_max)
        end_time = time.time()  
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'Breadth-first', 'solved': breadth_board.won, 'lock_limit': lock_lim, 'moves': breadth_board.iterations, 'time': f"{end_time - start_time:.6f}", 'move_max': self.move_max})
        if not breadth_board.won:
            self.unsolved.append({'Breadth-first': breadth_board})


    def depth_first(self, size, state, cars, lock_lim):
        depth_board = Board(size)
        depth_board.setup_board(state)
        start_time = time.time()  
        depth_board.depth_search(self.move_max)
        end_time = time.time()  
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'Depth-first', 'solved': depth_board.is_won(), 'lock_limit': lock_lim, 'moves': depth_board.iterations, 'time': f"{end_time - start_time:.6f}", 'move_max': self.move_max})
        if not depth_board.is_won():
            self.unsolved.append({'Depth-first': depth_board})


    def randomise(self, size, state, cars, lock_lim):
        random_board = Board(size)
        random_board.setup_board(state)
        start_time = time.time()
        random_board.random_solve(self.move_max)
        end_time = time.time()
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'Random', 'solved': random_board.is_won(), 'lock_limit': lock_lim, 'moves': random_board.iterations, 'time': f"{end_time - start_time:.6f}", 'move_max': self.move_max})
        if not random_board.is_won():
            self.unsolved.append({'Random': random_board})

    def no_reverse(self, size, state, cars, lock_lim):
        no_reverse_board = Board(size)
        no_reverse_board.setup_board(state)
        start_time = time.time()
        no_reverse_board.no_reverse_solve(self.move_max)
        end_time = time.time()
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'No_reverse', 'solved': no_reverse_board.is_won(), 'lock_limit': lock_lim, 'moves': no_reverse_board.iterations, 'time': f"{end_time - start_time:.6f}", 'move_max': self.move_max})
        if not no_reverse_board.is_won():
            self.unsolved.append({'No_reverse': no_reverse_board})

    def histogram(self):
        pass

    def lmplot(self):
        sns.set_theme(style="darkgrid")
        sns.lmplot(data=self.df_data, x="moves", y="time",
             hue="algorithm", col="algorithm", col_wrap=2,)
        plt.savefig("lmplot_test_data.png")
    
    def catplot(self):
        sns.set_theme(style="darkgrid")
        sns.catplot(data=self.df_data, x="algorithm", y="moves", hue="solved", kind="bar")
        plt.savefig("catplot_test_data.png")

    def save(self, path=None): 
        now = datetime.now()  # Get the current date and time
        date_time = now.strftime("%m-%d_%H:%M")  # Format it as a string

        if path is None:
            new_path = f"data/experiments/test{date_time}.csv"
        else:
            # Split the path into the directory and the filename
            directory, filename = os.path.split(path)
            # Split the filename into the name and the extension
            name, extension = os.path.splitext(filename)
            # Append the date and time to the name
            new_filename = f"{name}_{date_time}{extension}"
            # Combine the directory and the new filename into the new path
            new_path = os.path.join(directory, new_filename)

        self.df_data.to_csv(new_path)
        

    def run(self):
        self.data = []
        sizes = range(self.size, self.size + self.size_range)
        cars_range = range(self.num_cars, self.num_cars + self.num_cars_range)
        lock_limits = range(self.lock_limit, self.lock_limit + self.lock_limit_range)

        for i in tqdm(range(self.num_runs)):
            for size, cars, lock_lim in product(sizes, cars_range, lock_limits):
                initial_state = Board.random_board_df(size, cars, self.car_truck_ratio, lock_lim, self.min_exit_distance, self.HV_ratio)
                for algorithm in self.algorithms:
                    if algorithm == 'random':
                        self.randomise(size, initial_state, cars, lock_lim)
                    elif algorithm == 'no_reverse':
                        self.no_reverse(size, initial_state, cars, lock_lim)
                    elif algorithm == 'breadth_first':
                        self.breadth_first(size, initial_state, cars, lock_lim)
                    elif algorithm == 'depth_first':
                        self.depth_first(size, initial_state, cars, lock_lim)
                    elif algorithm == 'a_star':
                        self.a_star(size, initial_state, cars, lock_lim)
        self.df_data = pd.DataFrame(self.data)

    def run_all(self):
        sizes = range(self.size, self.size + self.size_range)
        cars_range = range(self.num_cars, self.num_cars + self.num_cars_range)
        lock_limits = range(self.lock_limit, self.lock_limit + self.lock_limit_range)
        ratios = range(self.car_truck_ratio, self.car_truck_ratio + self.car_truck_range)

        for i in tqdm(range(self.num_runs)):
            for size, cars, lock_lim, ratio in product(sizes, cars_range, lock_limits, ratios):
                initial_state = Board.random_board_df(size, cars, ratio, lock_lim, self.min_exit_distance, self.HV_ratio)
                # Random
                self.randomise(size, initial_state, cars, lock_lim)
                print("Random done")
                # No_reverse
                self.no_reverse(size, initial_state, cars, lock_lim)
                print("No_reverse done")
                # Breadt_first
                self.breadth_first(size, initial_state, cars, lock_lim)
                print("Breadth_first done")
                # Depth_first
                self.depth_first(size, initial_state, cars, lock_lim)
                print("Depth_first done")
                # A_star
                self.a_star(size, initial_state, cars, lock_lim)
                print("A_star done")
        self.df_data = pd.DataFrame(self.data)

    def export(self):
        pass

