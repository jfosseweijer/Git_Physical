import numpy as np
import pandas as pd
import os
from code.classes.board_setup import Vehicle as Vehicle
from code.classes.board_setup import Board as Board

def main(gameboards):
    board_number = int(input(f"Which board do you want to play 1-{len(gameboards)}?  ")) - 1
    assert board_number >= 0 and board_number < len(gameboards), "Invalid board number"
    
    # Create bord class and initiate
    board = Board(size=gameboards[board_number]['col'].max(axis=0))
    board.setup_board(gameboards[board_number])

    moved_X = False
    while not moved_X:
        board.print_board()
        car_name = input("Enter the name of the car to move: ")

        # Find the car and print its current position
        car = board.find_vehicle(car_name)
        if car is not None:
            print(f"The current position of {car_name} is {car.position}")
        else:
            print(f"No car named {car_name} found on the board")
            continue

        # Check if input syntax is correct
        while True:
            try:
                new_position = input("Enter the new position of the car (Shape = x,y): ")
                if len(new_position.split(',')) != 2:
                    raise ValueError
                new_position = tuple(map(int, new_position.split(',')))
            except ValueError:
                print("Make sure to enter the position in the correct format! (Shape = x,y)")
                #better try again... Return to the start of the loop
                continue
            else:
                break

        try:
            board.move_piece(car_name, new_position)
            print(f"Moved {car_name} to {new_position}:")

            if car_name == 'X':
                moved_X = True
        except ValueError as e:
            print(f"Failed to move {car_name} to {new_position}: {e}")

def open_gameboards():
    # Saves the boards in a list. 
    gameboards = []
    path = os.path.join(os.getcwd(), 'data/gameboards')
    for filename in os.listdir(path):
        board_df = pd.read_csv(os.path.join(path, filename))
        board_df.set_index('car', inplace=True)
        gameboards.append(board_df)
    return gameboards

if __name__ == "__main__":
    gameboards = open_gameboards()
    main(gameboards)
    