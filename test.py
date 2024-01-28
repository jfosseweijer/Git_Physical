
import numpy as np
import code_files.algorithms.randomise as randomise
import code_files.classes.board_setup as setup
from code_files.visualisation.my_experiment import Experiment


#(self, size, size_range, num_cars, num_cars_range=1, car_truck_ratio=3, lock_limit=1, lock_limit_range=1, min_exit_distance=2, move_max=10000, num_runs=1000):
experiment = Experiment(6, 1, 10, 1, 3, 1, 1, 2, 10000, 10)
experiment.run_all()
print(experiment.df_data)
