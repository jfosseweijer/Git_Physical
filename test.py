from code_files.visualisation.my_experiment import Experiment



#class Experiment:
    #def __init__(self, size, num_cars, algorithms=[], size_range=1, num_cars_range=1, car_truck_ratio=(3,1), car_truck_range=(1,1), HV_ratio=(1,1), HV_ratio_range=(1,1), lock_limit=1, lock_limit_range=1, min_exit_distance=2, move_max=10000, num_runs=1000):

algoririthm = []

experiment = Experiment(size=9, size_range=1, num_cars=18, num_cars_range=10, num_runs=1000, move_max=500, HV_ratio=(1,1))
experiment.run()
print(experiment.df_data)
experiment.save(path='data/experiments/HV_1:3.csv')
#experiment.lmplot()
#experiment.catplot()

