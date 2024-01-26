"""
Experiment class for generating data.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from ..classes.board_setup import Board


class Experiment:
    def __init__(self, size, size_range, num_cars, algorithm, num_cars_range=1, car_truck_ratio=3, lock_limit=1, lock_limit_range=1, exit_distance=2, move_max=10000, num_runs=1000):
        """
        Parameters
        ----------
            size int : Size of the board.
            size_range int : Range of the board size.
            num_cars int : Number of cars on the board.
            num_cars_range int : Range of the number of cars.
            algorithm str : Algorithm to be used.
            car_truck_ratio int : Ratio of cars to trucks.
            lock_limit int : Minimum number of open spaces in column or row
            before it is considered locked. Higher values result in easier boards.
            lock_limit_range int : Range of the lock limit.
            exit_distance int : Minimal distance of the red car to the exit.
            move_max int : Maximum number of moves. If exceeded, the board is considered unsolvable.
            num_runs int : Number of runs.
        """
        self.size = size
        self.size_range = size_range
        self.num_cars = num_cars
        self.num_cars_range = num_cars_range
        self.algorithm = algorithm
        self.car_truck_ratio = car_truck_ratio
        self.lock_limit = lock_limit
        self.lock_limit_range = lock_limit_range
        self.exit_distance = exit_distance
        self.move_max = move_max
        self.num_runs = num_runs
        self.data = pd.DataFrame()

    def generate_board(self, size, num_cars, car_truck_ratio, lock_limit, exit_distance):
        """
        Generate a board.
        """
        board = Board(size)
        board.generate_random_board(num_cars, car_truck_ratio, lock_limit, exit_distance)
        return board

    def a_star(self):
        pass

    def breadth_first(self):
        pass

    def depth_first(self):
        pass

    def randomise(self):
        pass

    def histogram(self):
        pass

    def plot(self):
        pass

    def save(self):
        pass

    def run(self):
        pass

    def export(self):
        pass

