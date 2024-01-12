import numpy as np
import pandas as pd
import os
from code.classes.board_setup import Vehicle as Vehicle
from code.classes.board_setup import Board as Board

def main(gameboards):
    board_number = int(input(f"Which board do you want to play 1-{len(gameboards)}?  ")) - 1
    assert board_number >= 0 and board_number < len(gameboards), "Invalid board number"
    
    # Create bord class and initiate
    board = Board(gameboards[board_number][1])
    board.setup_board(gameboards[board_number][0])

    moved_X = False
    while not moved_X:
        car = None
        valid_move = False
        while valid_move == False:
            board.print_board()
            player_move = input("Enter the car and it's movement: ")
            player_move = player_move.split(',')
        
            if len(player_move) == 2:
                car_name = player_move[0].upper()
                movement = int(player_move[1])
                valid_move = True

            else:
                player_move = print("Please use this format (A,1): ")

            if valid_move == True:
                # Find the car and print its current position
                car = board.find_vehicle(car_name)

                if car is None:
                    print(f"No car named {car_name} found on the board")
                    valid_move = False

            # Check if input syntax is correct
            if valid_move == True:
                try:
                    board.move_piece(car_name, movement)
                except ValueError:
                    valid_move = False
                    print(f"You can't move {car_name} by {movement}")

                if car_name == 'X':
                    moved_X = True

def open_gameboards():
    # Saves the boards in a list. 
    gameboards = []
    path = os.path.join(os.getcwd(), 'data/gameboards')
    for filename in os.listdir(path):
        size = int(filename[8])
        if size == 1:
            size = 12
        board_df = pd.read_csv(os.path.join(path, filename))
        board_df.set_index('car', inplace=True)
        gameboards.append((board_df, size))
    return gameboards

if __name__ == "__main__":
    gameboards = open_gameboards()
    main(gameboards)
    