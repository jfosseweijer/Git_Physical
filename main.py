from code_files.visualisation.interface import Interface as Interface
import os
import pandas as pd
import tkinter as tk

def main(gameboards):
    root = tk.Tk()
    Interface(root, gameboards)
    root.mainloop()

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