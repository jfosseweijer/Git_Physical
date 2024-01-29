"""
Function(s) for the random solution baseline.
These are meant to be called by the board class.

Author: Nanne Hempel
"""
import numpy as np
import random
import pandas as pd
import string



def generate_car_names(num_cars):
    letters = list(string.ascii_uppercase)
    letters.remove('X')
    car_list = []
    alphabet_num = 25

    # Makes a list of the alphabet, 
    # if a letter is already in the list, entry will be that letter twice.
    for i in range(num_cars - 1):
        if i < alphabet_num:
            car_list.append(letters[i%alphabet_num])
        else:
            car_list.append(letters[i%alphabet_num]+letters[i%alphabet_num])

    return car_list


def place_car(car, col, row, orientation, length, direction, position_array, x_col, x_row):
    """
    Places a car on the board.
    Will only place a car if it fits on the board.

    Parameters
    ----------
        car str : Name of the car.
        col int : Column number.
        row int : Row number.
        orientation str : Orientation of the car, either 'H' or 'V'.
        length int : Length of the car.
        direction int : Direction of the car, either -1 or 1.
        position_array np.array : Array representing the board.

    Returns
    -------
        position_array np.array : Array representing the board. With new car placed.

    """
    size = position_array.shape[0]
    path = length * direction
    # Horizontal cars can only be placed left of the red car
    if orientation == 'H' and row == x_row:
        between_x_and_exit = (col + path + 1) >= x_col + 2 if direction == -1 else (col) >= x_col + 2
        if between_x_and_exit:
            raise ValueError("Car cannot be placed between X and exit")
        

    if orientation == 'H':
        start, stop = (col+path+1, col+1) if direction == -1 else (col, col+path)
        in_bounds = start >= 0 if direction == -1 else stop <= size
        new_positions = position_array[row, start:stop]
    elif orientation == 'V':
        start, stop = (row+path+1, row+1) if direction == -1 else (row, row+path)
        in_bounds = start >= 0 if direction == -1 else stop <= size
        new_positions = position_array[start:stop, col]

    if np.core.defchararray.equal(new_positions, ' ').all() and not np.core.defchararray.equal(new_positions, 'X').any() and in_bounds:
        new_positions[:] = car
        return position_array
    else:
        raise ValueError("Car does not fit on the board")

def random_board(size, num_cars, car_truck_ratio, lock_limit, exit_distance, HV_ratio=(1,1)):
    """
    Generates a random board. Fingers crossed it's solvable.

    Parameters
    ----------
        size int : Size of the board.
        num_cars int : Number of cars on the board.
        car_truck_ratio int : Ratio of cars to trucks.
        lock_limit int : Minimum number of open spaces in column or row
        before it is considered locked. Higher values result in easier boards.

    Returns
    -------
        initial_state pd.DataFrame : Initial state of the board.
        can be used to fill the board class with .set_board()
    """

    # Create an empty array to keep track of the board
    position_array = np.array([[' '] * size] * size, dtype=str)
    index = np.arange(size)
    x_row = random.choice(range(1, size - 2))
    x_col = random.choice(range(1, size - exit_distance - 1))
    position_array[x_row, x_col:x_col+2] = 'X'

    # Create a list of car names excluding 'X'
    car_names = generate_car_names(num_cars)

    initial_state = pd.DataFrame(columns=['orientation', 'col', 'row', 'length'], index=pd.Index(car_names, name='car'))
    initial_state.loc['X'] = ['H', x_col, x_row, 2]

    # Arrays that keep track of the cars that are placed
    # If a row or column is full, and all cars are in-line,
    # that row or column is locked. And a new board should be generated.
    row_horizontals = np.zeros(size, dtype=int)
    col_verticals = np.zeros(size, dtype=int)

    # Car parameters
    directions = [-1, 1]
    orientations = ['H' for _ in range(HV_ratio[0])] + ['V' for _ in range(HV_ratio[1])]
    lengths = [2 for _ in range(car_truck_ratio[0])] + [3 for _ in range(car_truck_ratio[1])]

    placed = 0
    errors = 0

    while placed < num_cars - 1 and errors < 100000:
        name = car_names[placed]
        column = random.choice(index)
        row = random.choice(index)
        orientation = random.choice(orientations)
        length = random.choice(lengths)
        direction = random.choice(directions)
        
        try:
            position_array = place_car(name, column, row, orientation, length, direction, position_array, x_col, x_row)
            if direction == 1:
                initial_state.loc[name] = [orientation, column, row, length]
            elif direction == -1:
                initial_state.loc[name] = [orientation, column - length + 1, row, length] if orientation == 'H' \
                                     else [orientation, column, row - length + 1, length]
            placed += 1
            errors = 0
            
            if orientation == 'H':
                row_horizontals[row] += length
            elif orientation == 'V':
                col_verticals[column] += length

            ## This can be set as a difficulty parameter
            locked_rows = np.any(row_horizontals >= size - lock_limit)
            locked_cols = np.any(col_verticals >= size - lock_limit)

            if locked_rows or locked_cols:
                position_array = np.array([[' '] * size] * size, dtype=str)
                row_horizontals = np.zeros(size, dtype=int)
                col_verticals = np.zeros(size, dtype=int)
                position_array[x_row, x_col:x_col+2] = 'X'
                initial_state.loc['X'] = ['H', x_col, x_row, 2]
                placed = 0
                continue

        except ValueError:
            errors += 1
            continue

    if errors == 100000:
        print("Could not place all cars on the board")

    # Add 1 to the column and row numbers to make it human readable
    initial_state['col'] += 1
    initial_state['row'] += 1
    return initial_state.dropna()

def random_step(board):
    """
    Randomly select a step that is valid.
    """
    options = {}
    # For each vehicle on the board, check if it can move
    for vehicle in board.vehicles_list:
        possible_moves = []

        for direction in [-1, 1]:
            move = 1
            stuck = False
            
            while move < board.size and not stuck:
                try:
                    new_positions = board.move_piece(vehicle.name, move * direction)
                    possible_moves.append((move * direction, new_positions))
                    move += 1

                except ValueError:
                    stuck = True
            
            if possible_moves:
                options[vehicle.name] = possible_moves
                
    if len(options) == 0:
        raise ValueError("No possible moves found")
    
    # Select a random vehicle and a random move
    vehicle = random.choice(list(options.keys()))
    movement, position = random.choice(options[vehicle])

    return vehicle, movement, position

