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

def generate_random_board(size, num_cars):
    """
    Generates a random board. Fingers crossed it's solvable.
    """

    position_array = np.zeros((size, size), dtype = str)
    index = np.arange(size)

    # Define the possible values for each column
    car_names = generate_car_names(num_cars)
    if 'X' in car_names:
        car_names.remove('X')
    
    # Place the red car
    position_array[(size - 1) // 2, 0:2] = 'X'
    
    orientations = ['H', 'V']
    lengths = [2, 2, 2, 3]
    directions = [-1, 1]

    car_list = []

    # Generate the rest of the car_list
    for i in range(num_cars - 1):
        car = car_names[i]
        orientation = random.choice(orientations)
        col = random.choice(index)
        row = random.choice(index)
        length = random.choice(lengths)
        direction = random.choice(directions)

        # Check if the car fits on the board
        if orientation == 'H':
            if col + length * direction > size - 1:
                direction *= -1
        else:
            if row + length > size - 1:
                direction *= -1
        
    return car_list

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