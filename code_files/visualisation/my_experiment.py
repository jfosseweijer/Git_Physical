"""
Experiment class for generating data.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from ..classes.board_setup import Board
from tqdm import tqdm
from itertools import product

class Experiment:
    def __init__(self, size, size_range, num_cars, num_cars_range=1, car_truck_ratio=3, car_truck_range=1 ,lock_limit=1, lock_limit_range=1, min_exit_distance=2, move_max=10000, num_runs=1000):
        """
        Parameters
        ----------
            size int : Size of the board.
            size_range int : Range of the board size.
            num_cars int : Number of cars on the board.
            num_cars_range int : Range of the number of cars.
            car_truck_ratio int : Ratio of cars to trucks.
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
        self.lock_limit = lock_limit
        self.lock_limit_range = lock_limit_range
        self.min_exit_distance = min_exit_distance
        self.move_max = move_max
        self.num_runs = num_runs
        self.df_data = pd.DataFrame(columns=['size', 'num_cars', 'algorithm', 'solved', 'lock_limit', 'moves'])
        self.data = []

    def a_star(self):
        pass

    def breadth_first(self, size, state, cars, lock_lim):
        breadth_board = Board(size)
        breadth_board.setup_board(state)
        breadth_board.breadth_search()
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'Breadth-first', 'solved': breadth_board.is_won(), 'lock_limit': lock_lim, 'moves': breadth_board.iterations})

    def depth_first(self, size, state, cars, lock_lim):
        depth_board = Board(size)
        depth_board.setup_board(state)
        depth_board.depth_search()
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'Depth-first', 'solved': depth_board.is_won(), 'lock_limit': lock_lim, 'moves': depth_board.iterations})

    def randomise(self, size, state, cars, lock_lim):
        random_board = Board(size)
        random_board.setup_board(state)
        random_board.random_solve()
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'Random', 'solved': random_board.is_won(), 
        'lock_limit': lock_lim, 'moves': random_board.iterations})

    def no_reverse(self, size, state, cars, lock_lim):
        no_reverse_board = Board(size)
        no_reverse_board.setup_board(state)
        no_reverse_board.no_reverse_solve()
        self.data.append({'size': size, 'num_cars': cars, 'algorithm': 'No_reverse', 'solved': no_reverse_board.is_won(), 
        'lock_limit': lock_lim, 'moves': no_reverse_board.iterations})       

    def histogram(self):
        pass

    def plot(self):
        pass

    def save(self):
        pass

    def run(self):
        pass

    def run_all(self):
        sizes = range(self.size, self.size + self.size_range)
        cars_range = range(self.num_cars, self.num_cars + self.num_cars_range)
        lock_limits = range(self.lock_limit, self.lock_limit + self.lock_limit_range)
        ratios = range(self.car_truck_ratio, self.car_truck_ratio + self.car_truck_range)

        for i in tqdm(range(self.num_runs)):
            for size, cars, lock_lim, ratio in product(sizes, cars_range, lock_limits, ratios):
                initial_state = Board.random_board_df(size, cars, ratio, lock_lim, self.min_exit_distance)
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
                #a_star_board = Board(size)
                #a_star_board.setup_board(initial_state)
                #a_star_board.a_star_search()
                #self.df_data.append({'size': size, 'num_cars': cars, 'algorithm': 'A_star', 'solved': a_star_board.is_won, 'lock_limit': lock_lim, 'moves': a_star_board.iterations})
        self.df_data = pd.DataFrame(self.data)

    def export(self):
        pass

