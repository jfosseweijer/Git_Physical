"""
Function(s) for the random solution baseline.
These are meant to be called by the board class.

Author: Nanne Hempel
"""
import random
import pandas as pd
import string

def generate_random_board(size, num_cars):
    """
    Generates a random board. Fingers crossed it's solvable.
    """
    # Create a list of all possible positions on the board
    positions = [(row, column) for row in range(size) for column in range(size)]
    # Define the number of rows you want in your DataFrame
    num_rows = 100

    # Define the possible values for each column
    cars = list(string.ascii_uppercase)
    orientations = ['H', 'V']
    positions = list(range(size)) 
    lengths = [2, 3]

    # Always include 'X' car with length 2
    data = [('X', random.choice(orientations), random.choice(positions), random.choice(positions), 2)]

    # Generate the rest of the data
    for _ in range(num_rows - 1):
        car = random.choice(cars)
        orientation = random.choice(orientations)
        col = random.choice(positions)
        row = random.choice(positions)
        length = 2 if car == 'X' else random.choice(lengths)
        data.append((car, orientation, col, row, length))

    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=['car', 'orientation', 'col', 'row', 'length'])

    # Write the DataFrame to a CSV file
    df.to_csv('output.csv', index=False)
    return

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