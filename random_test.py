import string
import numpy as np
import random

def place_car(car, col, row, orientation, position_array):
    """
    Places a car on the board.
    """
    if np.core.defchararray.not_equal(position_array[row, col:col+length], '0').any() and col + length * direction <= n - 1:
        print("it fits")
        position_array[row, col:col+length] = car
        return position_array
    else:
        raise ValueError("Car does not fit on the board")


#n = int(input("Enter a number: "))
n = 6
num_cars = int(input("Enter a number of cars: "))
lengths = 2
letters = list(string.ascii_uppercase)
list = []
alphabet_num = 26

# Makes a list of the alphabet, if a letter is already in the list, entry will be that letter twice.
# For example: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
# 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', AA, BB, CC, DD, EE, FF, GG, HH, II, JJ, KK, LL, MM,]

for i in range(n):
    if i < alphabet_num:
        list.append(letters[i%alphabet_num])
    else:
        list.append(letters[i%alphabet_num]+letters[i%alphabet_num])

index = np.arange(n)

position_array = np.zeros((n, n), dtype = str)
index = np.arange(n)

x_position = (n - 1) // 2
position_array[x_position, 0:2] = 'X'

placed = 0
length = 2
direction = 1

while placed < num_cars:

    car = list[placed]
    col = random.choice(index)
    row = random.choice(index)
    orientation = 'H'
    print(f"trying to place {car} at {col + 1}, {row + 1}")
    try:
        print(position_array[row, col:col+length]) 
        position_array = place_car(car, col, row, orientation, position_array)
        placed += 1
        print(position_array, end='\n\n')
    except ValueError:
        print("it doesn't fit", end='\n\n')
        continue
