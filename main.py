import numpy as np
import pandas as pd
import os
import argparse
from code_files.classes.board_setup import Vehicle as Vehicle
from code_files.classes.board_setup import Board as Board
from code_files.algorithms.user import user_move as user_move

def main(gameboards, user_input, random_solver):
    board_number = None

    while board_number is None or board_number < 0 or board_number >= len(gameboards):
        try:
            board_number = int(input(f"Which board do you want to play, choose between 1-{len(gameboards)}? ")) - 1
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    # Create bord class and initiate
    board = Board(gameboards[board_number][1])
    board.setup_board(gameboards[board_number][0])

    if user_input:
        user_move(board)

    if random_solver:
        board.random_solve()

    if board.is_won():
        print("You smart boiii!!!")


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

    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "Rush Hour game, either play the game or solve it using an algorithm.")

    # Adding arguments
    parser.add_argument("-u" ,"--user_input", action='store_true', help="set this flag to True, allowing the user to play the game")
    parser.add_argument("-r", "--random_solve", action='store_true', help="set this flag to True, game will be solved using a random moves algorithm")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    if not args.user_input and not args.random_solve:
        print("Usage:'main.py -r' or '-u'")
    else:
        main(gameboards, args.user_input, args.random_solve)