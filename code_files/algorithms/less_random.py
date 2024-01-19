"""
Function(s) for the random solution baseline.
These are meant to be called by the board class.

Author: Nanne Hempel
"""
import random
import pandas as pd
from ..classes.history import Queue

def random_without_reverse(board, history: Queue):
    """
    Randomly select a step that is valid. Steps that undo the last move are invalid
    """
    try:
        last_move = history.peek_back()
    except AssertionError:
        last_move = (None, 0, None)

    new_move = False
    while not new_move:
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

        if movement == -abs(last_move[1]) and vehicle == last_move[0]:
            new_move = False
        else:
            new_move = True
            history.enqueue((vehicle, movement, position))

    return vehicle, movement, position, history

