## Tester file. Can be deleted later.

import string
import numpy as np
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("num", help="size", type=int)
parser.add_argument("cars", help="number of cars", type=int)
args = parser.parse_args()

n = args.num
num_cars = args.cars

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
    path = length * direction
    if orientation == 'H':
        start, stop = (col+path+1, col+1) if direction == -1 else (col, col+path)
        in_bounds = start >= 0 if direction == -1 else stop <= n
        new_positions = position_array[row, start:stop]
    elif orientation == 'V':
        start, stop = (row+path+1, row+1) if direction == -1 else (row, row+path)
        in_bounds = start >= 0 if direction == -1 else stop <= n
        new_positions = position_array[start:stop, col]

    if np.core.defchararray.equal(new_positions, ' ').all() and in_bounds:
        print(new_positions)
        print("it fits")
        new_positions[:] = car
        return position_array
    else:
        print(new_positions)
        raise ValueError("Car does not fit on the board")

#n = int(input("Enter a number: "))

letters = list(string.ascii_uppercase)
list = []
alphabet_num = 26

# Makes a list of the alphabet, if a letter is already in the list, entry will be that letter twice.
# For example: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
# 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', AA, BB, CC, DD, EE, FF, GG, HH, II, JJ, KK, LL, MM,]

for i in range(num_cars):
    if i < alphabet_num:
        list.append(letters[i%alphabet_num])
    else:
        list.append(letters[i%alphabet_num]+letters[i%alphabet_num])



position_array = np.array([[' '] * n] * n, dtype=str)
index = np.arange(n)
x_position = (n - 1) // 2
position_array[x_position, 0:2] = 'X'

placed = 0
errors = 0
directions = [-1, 1]
orientations = ['H', 'V']
lengths = [2, 2, 2, 3]

while placed < num_cars:

    car = list[placed]
    col = random.choice(index)
    row = random.choice(index)
    orientation = random.choice(orientations)
    length = random.choice(lengths)
    direction = random.choice(directions)
    print(f"trying to place {car} at {col + 1}, {row + 1}, with ori: {orientation} len: {length} dir: {direction}")
    try:
        position_array = place_car(car, col, row, orientation, length, direction, position_array)
        placed += 1
        print(position_array, end='\n\n')
    except ValueError:
        errors += 1
        print("it doesn't fit", end='\n\n')
        continue

