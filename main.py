import numpy as np
import pandas as pd
import os
import argparse
from code_files.classes.board_setup import Vehicle as Vehicle
from code_files.classes.board_setup import Board as Board
from code_files.algorithms.user import user_move as user_move

def main(gameboards, user_input, random_solver, no_reverse_solver, astar_solver, deep_solver, broad_solver):
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

    if no_reverse_solver:
        board.no_reverse_solve()

    if astar_solver:
        board.astar_solve()
    
    if deep_solver:
        board.depth_search()

    if broad_solver:
        board.breadth_search()

    if board.is_won():
        board.print_board()
        print("You smart boy!!!")


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
    parser.add_argument("-lr", "--no_reverse_solve", action='store_true', help="set this flag to True, game will be solved using a random moves algorithm while not allowing reverse moves")
    parser.add_argument("-as", "--astar_solver", action='store_true', help="set this flag to True, game will be solved using a a-star algorithm")
    parser.add_argument("-ds", "--deep_solver", action='store_true', help="set this flag to True, game will be solved using a deepsearch algorithm")
    parser.add_argument("-bs", "--broad_solver", action='store_true', help="set this flag to True, game will be solved using a broadsearch algorithm")
    #parser.add_argument("-as", "--astar_solver", action='store_true', help="set this flag to True, game will be solved using an Astar algorithm")


    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(gameboards, args.user_input, args.random_solve, args.no_reverse_solve, args.astar_solver, args.deep_solver, args.broad_solver)