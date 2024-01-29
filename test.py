
import numpy as np
import code_files.algorithms.randomise as randomise
import code_files.classes.board_setup as setup
from code_files.visualisation.my_experiment import Experiment


#class Experiment:
    #def __init__(self, size, num_cars, algorithms=[], size_range=1, num_cars_range=1, car_truck_ratio=(3,1), car_truck_range=(1,1), HV_ratio=(1,1), HV_ratio_range=(1,1), lock_limit=1, lock_limit_range=1, min_exit_distance=2, move_max=10000, num_runs=1000):
experiment = Experiment(size=6, size_range=2, num_cars=10, num_cars_range=2, num_runs=10)
algoririthms = ['random', 'no_reverse']
experiment.run()
print(experiment.df_data)
experiment.plot()
