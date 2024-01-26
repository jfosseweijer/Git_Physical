"""
Function(s) for the random solution baseline.
These are meant to be called by the board class.

Author: 
"""
import random
import pandas as pd

def random_without_reverse(board, last_move):
    """
    Randomly select a step that is valid. Steps that undo the last move are invalid
    """
<<<<<<< HEAD

=======
>>>>>>> a28fddbadc46a82be6cf081c24a84bce5d14e635
    options = {}
    # For each vehicle on the board, check if it can move
    for vehicle in board.vehicles_list:
        possible_moves = []

        for direction in [-1, 1]:
            move = 1
            stuck = False
            
            while move < board.size and not stuck:
                try:
                    if not (vehicle.name == last_move[0] and (move*direction) == -last_move[1]):
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

