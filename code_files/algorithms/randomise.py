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
    car_list = []
    alphabet_num = 26

    # Makes a list of the alphabet, 
    # if a letter is already in the list, entry will be that letter twice.
    for i in range(num_cars):
        if i < alphabet_num:
            car_list.append(letters[i%alphabet_num])
        else:
            car_list.append(letters[i%alphabet_num]+letters[i%alphabet_num])

    return car_list

def place_car(car, col, row, orientation, length, direction, position_array):
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
    if orientation == 'H' and row == (size - 1) // 2:
        raise ValueError("Would block X from exiting")

    path = length * direction
    if orientation == 'H':
        start, stop = (col+path+1, col+1) if direction == -1 else (col, col+path)
        in_bounds = start >= 0 if direction == -1 else stop <= size
        new_positions = position_array[row, start:stop]
    elif orientation == 'V':
        start, stop = (row+path+1, row+1) if direction == -1 else (row, row+path)
        in_bounds = start >= 0 if direction == -1 else stop <= size
        new_positions = position_array[start:stop, col]

    if np.core.defchararray.equal(new_positions, ' ').all() and in_bounds:
        new_positions[:] = car
        return position_array
    else:
        raise ValueError("Car does not fit on the board")

def generate_random_board(size, num_cars):
    """
    Generates a random board. Fingers crossed it's solvable.

    Parameters
    ----------
        size int : Size of the board.
        num_cars int : Number of cars on the board.

    Returns
    -------
        initial_state pd.DataFrame : Initial state of the board.
        can be used to fill the board class with .set_board()
    """

    # Create a list of car names
    car_names = generate_car_names(num_cars)
    if 'X' in car_names:
        car_names.remove('X')
    
    initial_state = pd.DataFrame(columns=['orientation', 'col', 'row', 'length'], index=pd.Index(car_names, name='car'))
    
    # Create an empty array to keep track of the board
    position_array = np.array([[' '] * size] * size, dtype=str)
    index = np.arange(size)
    x_position = (size - 1) // 2
    position_array[x_position, 0:2] = 'X'

    # Arrays that keep track of the cars that are placed
    # If a row or column is full, and all cars are in-line,
    # that row or column is locked. And a new board should be generated.
    row_horizontals = np.zeros(size, dtype=int)
    col_verticals = np.zeros(size, dtype=int)

    # Car parameters
    directions = [-1, 1]
    orientations = ['H', 'V']
    lengths = [2, 2, 2, 3]

    placed = 0
    errors = 0

    while placed < num_cars and errors < 100000:
        name = car_names[placed]
        column = random.choice(index)
        row = random.choice(index)
        orientation = random.choice(orientations)
        length = random.choice(lengths)
        direction = random.choice(directions)
        
        try:
            position_array = place_car(name, column, row, orientation, length, direction, position_array)
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

            locked_rows = np.any(row_horizontals == size)
            locked_cols = np.any(col_verticals == size)

            if locked_rows or locked_cols:
                position_array = np.array([[' '] * size] * size, dtype=str)
                row_horizontals = np.zeros(size, dtype=int)
                col_verticals = np.zeros(size, dtype=int)
                position_array[x_position, 0:2] = 'X'
                placed = 0
                continue

        except ValueError:
            errors += 1
            continue

    if errors == 100000:
        print("Not all cars could be placed")

    return initial_state

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

