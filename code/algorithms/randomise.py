"""
Function(s) for the random solution baseline.
These are meant to be called by the board class.

Author: Nanne Hempel
"""
import random

def true_random_step(board):
    """
    Randomly select a step wether it's valid or not. 
    """
    return

def random_step(board):
    """
    Randomly select a step that is valid.
    """
    possible_moves = {}
    # For each vehicle on the board, check if it can move
    for vehicle in board.vehicles_list:
        possible_moves[vehicle.name] = []
        for move in range(1, board.size):
            for direction in [-move, move]:
                try:
                    board.move_piece(vehicle, direction)
                    possible_moves[vehicle.name].append(direction)
                except ValueError:
                    pass

    if len(possible_moves) == 0:
        raise ValueError("No possible moves found")

    # Select a random vehicle and a random move
    vehicle = random.choice(list(possible_moves.keys()))
    movement = random.choice(possible_moves[vehicle])

    return vehicle, movement