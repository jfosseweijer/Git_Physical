
import numpy as np
import code_files.algorithms.randomise as randomise
import code_files.classes.board_setup as setup

game = setup.Board(6)
game.generate_random_board(13, 3, 1, 2)
game.print_board()
game.depth_search()
game.print_board()
