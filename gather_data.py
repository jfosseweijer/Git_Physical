from code_files.classes.my_experiment import Experiment
import datetime
import argparse



def main():
    parser = argparse.ArgumentParser(description="Run the experiment with given parameters.")
    parser.add_argument('-r', '--num_runs', type=int, required=True, help='Number of runs (default: 1000)')
    parser.add_argument('-s', '--size', type=int, required=True, help='Size of the board')
    parser.add_argument('-sr', '--size_range', type=int, default=1, help='Range of the size of the board (default: 1)')
    parser.add_argument('-c', '--num_cars', type=int, required=True, help='Number of cars on the board')
    parser.add_argument('-cr', '--num_cars_range', type=int, default=1, help='Range of the number of cars (default: 1)')
    parser.add_argument('-ctr', '--car_truck_ratio', type=int, nargs=2, default=[3, 1], help='Ratio of cars to trucks (default: 3,1)')
    parser.add_argument('-hv', '--HV_ratio', type=int, nargs=2, default=[1, 1], help='Ratio of horizontal to vertical cars (default: 1,1)')
    parser.add_argument('-l', '--lock_limit', type=int, default=1, help='Minimum number of accessible spaces in column or row before it is considered locked (default: 1)')
    parser.add_argument('-lr', '--lock_limit_range', type=int, default=1, help='Range of the lock limit (default: 1)')
    parser.add_argument('-m', '--min_exit_distance', type=int, default=2, help='Minimal distance of the red car to the exit (default: 2)')
    parser.add_argument('-mr', '--min_exit_distance_range', type=int, default=1, help='Range of the min exit distance (default: 1)')
    parser.add_argument('-mm', '--move_max', type=int, default=2500, help='Maximum number of moves. If exceeded, the board is considered unsolvable (default: 2500)')

    args = parser.parse_args()

    experiment = Experiment(
        num_runs=args.num_runs,
        size=args.size,
        num_cars=args.num_cars,
        size_range=args.size_range,
        num_cars_range=args.num_cars_range,
        car_truck_ratio=tuple(args.car_truck_ratio),
        HV_ratio=tuple(args.HV_ratio),
        lock_limit=args.lock_limit,
        lock_limit_range=args.lock_limit_range,
        min_exit_distance=args.min_exit_distance,
        min_exit_distance_range=args.min_exit_distance_range,
        move_max=args.move_max
    )

    experiment.run()

    date = datetime.datetime.now().strftime("%m-%d_%H:%M")
    experiment.save(f'data/experiment/{args.size}_{args.num_cars}-{args.num_cars + args.num_cars_range}:{date}.csv')

    if input("Do you want to save the unsolved boards? (y/n) ") == 'y':
        experiment.save_unsolved(f'data/experiment/unsolved_{args.size}_{args.num_cars}-{args.num_cars + args.num_cars_range}:{date}.csv')
    print("Experiment finished.")


if __name__ == "__main__":
    main()
