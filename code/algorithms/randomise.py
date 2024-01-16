"""
Function(s) for the random solution baseline.
These are meant to be called by the board class.

Author: Nanne Hempel
"""


def true_random_step(board):
    """
    Randomly select a step wether it's valid or not. 
    """
    return

def random_step(board):
    """
    Randomly select a step that is valid.
    """

    # For each vehicle on the board, check if it can move
    for vehicle in board.vehicles_list:
        for move in range(1, board.size):
            try:
                board.move_piece(vehicle.name, move)
            except ValueError as e:
                print(e)           
            
    return