"""
Function for a deep search algorithm.
It is meant to be called by the board_setup class.

Author: Jaap Osseweijer
"""

import random
from ..classes.stack import Stack

def depth_search(board, history: Stack, made_moves, bottom):
    """
    Randomly select a step that is valid and hasn't been played yet
    """
    try:
        last_move = history.top()
    except AssertionError:
        last_move = (None, 0, None)

    new_move = False
    if history.size() <= bottom:
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
        while not new_move and len(options) != 0:
            vehicle = random.choice(list(options.keys()))
            movement, position = random.choice(options[vehicle])
            new_move = True

            if vehicle in made_moves:
                if history.size() in made_moves[vehicle]:
                    for made_move in made_moves[vehicle][history.size()][0]:
                        if made_move == (movement, position):
                            options[vehicle].remove((movement, position))
                            new_move = False
                        elif movement == -last_move[1] and vehicle == last_move[0] and new_move:
                            options[vehicle].remove((movement, position))
                            new_move = False                        
            
            if len(options[vehicle]) == 0:
                del options[vehicle]
                new_move = False
        
        if new_move:
            history.push((vehicle, movement, position))

    if history.size() >= bottom or not new_move:
        undo_move = history.pop()
        if undo_move[0] in made_moves:
            if history.size() in made_moves[undo_move[0]]:
                made_moves[undo_move[0]][history.size()].append(((undo_move[1], undo_move[2])))
            else:
                made_moves[undo_move[0]] = {}
                made_moves[undo_move[0]][history.size()] = [((undo_move[1], undo_move[2]))]
        elif len(options) == 0:
            vehicle, movement, position = undo_move
            movement = -movement
            print("back")
        else:
            made_moves[undo_move[0]] = {}
            made_moves[undo_move[0]][history.size()] = [((undo_move[1], undo_move[2]))]

    return vehicle, movement, position, history, made_moves

