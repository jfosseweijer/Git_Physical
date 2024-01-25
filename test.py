
import numpy as np
import code_files.algorithms.randomise as randomise
import code_files.classes.board_setup as setup


random_board, state = randomise.generate_random_board(6, 14)
print(random_board)

board = setup.Board(6)
board.setup_board(random_board)
board.print_board()
print(state)