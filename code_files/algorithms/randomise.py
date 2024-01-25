"""
Function(s) for the random solution baseline.
These are meant to be called by the board class.

Author: Nanne Hempel
"""
import numpy as np
import random


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

