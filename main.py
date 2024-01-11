import numpy as np
import pandas as pd
import os
from code.classes.board_setup import Vehicle as Vehicle
from code.classes.board_setup import Board as Board

def main(gameboards):
    board_number = int(input("Which board do you want to play (1-3): ")) - 1
    assert board_number >= 0 and board_number < len(gameboards), "Invalid board number"
    
    size = gameboards[board_number]['col'].max(axis=0)
    board = setup_board(gameboards[board_number], size)
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




def setup_board(gameboard, board_size=6):
    # Set the grid of the board
    board = Board(board_size)
    for name, car in gameboard.iterrows():
        # Set length to be an int instead of string
        length = int(car['length'])

        # Subtract 1 from position to make it zero-indexed
        car['row'] -= 1
        car['col'] -= 1

        if name == 'X':
            colour = np.array([255, 0, 0])
        else:
            # Random rgb colour
            colour = np.random.choice(range(256), size=3)

        # Create vehicle object and add it to the board, n serves as name
        vehicle = Vehicle(length, car['orientation'], (car['col'], car['row']), n, colour)
        board.add_vehicle(vehicle)
    return board

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
    