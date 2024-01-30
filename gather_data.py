from code_files.classes.my_experiment import Experiment
import datetime



#class Experiment:
    #def __init__(self, size, num_cars, algorithms=[], size_range=1, num_cars_range=1, car_truck_ratio=(3,1), car_truck_range=(1,1), HV_ratio=(1,1), HV_ratio_range=(1,1), lock_limit=1, lock_limit_range=1, min_exit_distance=2, move_max=10000, num_runs=1000):

def main():
    Kwargs = {}
    
    print("Please enter parameters for the experiment. Press enter to use default values.")
    Kwargs['num_runs'] = int(input("Number of runs: (Default 1000) ") or 1000)
    Kwargs['size'] = int(input("Size of the board: (Required) "))
    Kwargs['num_cars'] = int(input("Number of cars on the board: (Required, Rec by size: 6-12, 9-24) "))
    Kwargs['size_range'] = int(input("Range of the size of the board: (Default 1) ") or 1)
    Kwargs['num_cars_range'] = int(input("Range of the number of cars: (Default 1) ") or 1)
    Kwargs['car_truck_ratio'] = tuple(map(int, (input("Ratio of cars to trucks: (Tuple (Cars, Trucks)), Default (3,1) ") or "3,1").strip('()').split(',')))
    Kwargs['HV_ratio'] = tuple(map(int, (input("Ratio of horizontal to vertical cars: (Tuple (Horizontal, Vertical), Default (1,1)) ") or "1,1").strip('()').split(',')))
    Kwargs['lock_limit'] = int(input("Minimum number of accesible spaces in column or row before it is considered locked: (Default 1 )") or 1)
    Kwargs['lock_limit_range'] = int(input("Range of the lock limit: (Default 1) ") or 1)
    Kwargs['min_exit_distance'] = int(input("Minimal distance of the red car to the exit: (Default 2) ") or 2)
    Kwargs['min_exit_distance_range'] = int(input("Range of the min exit distance: (Make sure it fits on the board), (Default 1) ") or 1)
    Kwargs['move_max'] = int(input("Maximum number of moves. If exceeded, the board is considered unsolvable: (Default 2500) ") or 2500)


    experiment = Experiment(**Kwargs)
    experiment.run()
    date = datetime.datetime.now().strftime("%m-%d_%H-%M")
    experiment.save(f'data/experiment/{Kwargs["size"]}_{Kwargs["num_cars"]}-{Kwargs["num_cars"] + Kwargs["num_cars_range"]}:{date}.csv')

    if input("Do you want to save the unsolved boards? (y/n) ") == 'y':
        experiment.save_unsolved(f'data/experiment/unsolved_{Kwargs["size"]}_{Kwargs["num_cars"]}-{Kwargs["num_cars"] + Kwargs["num_cars_range"] }:{date}.csv')
    print("Experiment finished.")


if __name__ == "__main__":
    main()
