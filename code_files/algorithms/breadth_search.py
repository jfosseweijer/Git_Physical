"""
Function for the broad search algorithm.
It is meant to be called by the board_setup class.

Author: Jaap Osseweijer
"""

def breadth_search(current_layer_boards: list, current_layer_index, former_layer_boards: list, former_layer_index):
    """
    Cycles through the possible moves of the board, exluding moves that undo the last move
    """

    if current_layer_index != None and current_layer_index < 0:
        current_layer_index = None
        former_layer_index += 1

    if former_layer_index == len(former_layer_boards):
        former_layer_boards.clear()
        former_layer_boards = current_layer_boards[:]
        former_layer_index = 0
        current_layer_index = None
        current_layer_boards.clear()


    board = former_layer_boards[former_layer_index][0]

    options = []
    # For each vehicle on the board, check if it can move
    for vehicle in board.vehicles_list:

        for direction in [-1, 1]:
            move = 1
            stuck = False
            
            while move < board.size and not stuck:
                try:
                    if not (vehicle.name == former_layer_boards[former_layer_index][1][0] and (move*direction) == -former_layer_boards[former_layer_index][1][1]):
                        new_positions = board.move_piece(vehicle.name, move * direction)
                        options.append((vehicle.name, (move * direction, new_positions)))
                    move += 1

                except ValueError:
                    stuck = True
                
    if len(options) == 0:
        raise ValueError("No possible moves found")
    
    # Select a random vehicle and a random move
    if current_layer_index == None:
        current_layer_index = len(options)

    if current_layer_index >= 0:
        current_layer_index -= 1
        vehicle = options[current_layer_index][0]
        movement, position = options[current_layer_index][1]

    return vehicle, movement, position, current_layer_boards, current_layer_index, former_layer_boards, former_layer_index
