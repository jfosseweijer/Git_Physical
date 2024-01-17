"""
Function(s) for the random solution baseline.
These are meant to be called by the board class.

Author: Nanne Hempel
"""
import random
import pandas as pd
from ..classes.history import Queue

def generate_random_board(board):
    """
    Generates a random board. Fingers crossed it's solvable.
    """
    # Create a list of all possible positions on the board
    positions = [(row, column) for row in range(board.size) for column in range(board.size)]


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