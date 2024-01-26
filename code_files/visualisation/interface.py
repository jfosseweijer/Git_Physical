import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle 
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ..classes.queue import Queue
from code_files.visualisation.int_vis import plot as visualize
from code_files.classes.board_setup import Board as Board
from ..algorithms.no_reverse import random_without_reverse
from ..algorithms.breadth_search import breadth_search
from ..algorithms.randomise import random_step

import time
import copy


class Interface:
    def __init__(self, master, gameboards):
        self.gameboards = gameboards
        self.master = master
        self.home()

    def home(self):
        self.clear_interface()
        self.master.title("RUSH HOUR")
        
        self.style = ThemedStyle(self.master)
        self.style.set_theme("yaru")

        # Create dropdown
        self.image_var = tk.StringVar()
        # Set a default image
        self.image_var.set("game 1")
        # Add options
        images = ["game 1", "game 2", "game 3", "game 4", "game 5", "game 6", "game 7", "game 8"]

        # Couple the corresponding game visualization
        image_menu = ttk.Combobox(master=self.master, textvariable=self.image_var, values=images)
        image_menu.pack(pady=10)
        image_menu.bind("<<ComboboxSelected>>", self.load_image)

        # Create the label for the image once during initialization
        self.image_label = tk.Label(self.master)
        self.image_label.pack()
        
        # Manually load the initial image
        self.load_image()  

        # Buttons for different functionalities
        user_button = ttk.Button(master=self.master, text="User", command=lambda: self.create_user(int(image_menu.get()[-1])-1))
        user_button.pack(side=tk.BOTTOM, fill=tk.X)

        random_button = ttk.Button(master=self.master, text="Random", command=lambda: self.algorithm(int(image_menu.get()[-1])-1, alg_type = 'random'))
        random_button.pack(side=tk.BOTTOM, fill=tk.X)

        algorithm_button = ttk.Button(master=self.master, text="Not reversing random algorithm", command=lambda: self.algorithm(int(image_menu.get()[-1])-1, alg_type = 'non-reverse'))
        algorithm_button.pack(side=tk.BOTTOM, fill=tk.X)

        algorithm_button = ttk.Button(master=self.master, text="breadth_search", command=lambda: self.algorithm(int(image_menu.get()[-1])-1, alg_type = 'breadth'))
        algorithm_button.pack(side=tk.BOTTOM, fill=tk.X)

    def create_user(self, board_number):
        self.clear_interface()
        self.master.title("user")

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [10, 1]}, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(self.master, textvariable=self.input_var)
        input_entry.pack(pady=10)

        move_button = ttk.Button(master=self.master, text="Move", command=lambda: self.move_car())
        move_button.pack()

        # Create an instance of the Board class
        self.board = Board(self.gameboards[board_number][1])
        self.board.setup_board(self.gameboards[board_number][0])

        # Call the plot_information method on the board instance
        visualize(self.board, self.ax1, self.ax2)
        self.canvas.draw()
        self.master.update_idletasks()

    def move_car(self):
        # Clear previous error labels
        self.clear_labels()

        move = self.input_var.get()

        # Split the move input and handle invalid syntax
        try:
            car_name, movement = map(str.strip, move.split(','))
            movement = int(movement)
        except ValueError:
            self.display_text("Please use this format 'A,1'", error=True)
            return

        # Find the car and handle invalid car name
        car = self.board.find_vehicle(car_name.upper())
        if car is None:
            self.display_text(f"No car named {car_name} found on the board", error=True)
            return

        # Try to move the piece and handle invalid moves
        try:
            self.board.move_piece(car_name.upper(), movement, move)
            visualize(self.board, self.ax1, self.ax2)
            self.canvas.draw()
            self.master.update_idletasks()

        except ValueError as e:
            self.display_text(str(e), error=True)

        self.check_winner(car_name)
        
    def algorithm(self, board_number, alg_type):
        self.clear_interface()
        self.master.title("random")
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [10, 1]}, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Create an instance of the Board class
        self.board = Board(self.gameboards[board_number][1])
        self.board.setup_board(self.gameboards[board_number][0])
        
        iterations = 0
        is_won = False
        if alg_type == 'non-reverse':
            move = (None, 0, None)
        elif alg_type == 'breadth':
            current_layer_boards = []
            current_layer_index = 0
            former_layer_boards = [(self.board, (None, 0, None))]
            former_layer_index = 0
            move = (None, 0, None, current_layer_boards, current_layer_index, former_layer_boards, former_layer_index)
            self.board: Board = copy.deepcopy(former_layer_boards[former_layer_index][0])

        start = time.time()
        while not is_won and iterations < 100:
            if iterations > 10:
                self.clear_labels()
            visualize(self.board, self.ax1, self.ax2)
            self.canvas.draw()
            self.master.update_idletasks()

            iterations += 1
            
            if alg_type == 'random':
                move = random_step(self.board)
            elif alg_type == 'non-reverse':
                move = random_without_reverse(self.board, move)
            elif alg_type == 'breadth':
                move = breadth_search(move[3], move[4], move[5], move[6])
                self.board: Board = copy.deepcopy(move[5][move[6]][0])
                print(move)
            
            try:            
                vehicle = self.board.find_vehicle(move[0])
            except UnboundLocalError:
                break

            self.board.update_positions_set(vehicle, move[2])
            time.sleep(0.2)
            self.display_text((move[0], move[1]), move=True)
            self.check_winner(move[0], time.time() - start - iterations * 0.2)

    def display_text(self, text_message, error=False, move=False):
        # Display the error message in the Tkinter interface using Label
        if error:
            error_label = tk.Label(self.master, text=f"Error: {text_message}", fg="red")
            error_label.pack()
        elif move:
            move_label = tk.Label(self.master, text=f"Moved: {text_message}", fg="blue")
            move_label.pack()
            
    def create_Algorithm(self):
        self.clear_interface()
        self.master.title("user")

    def load_image(self, event=None):
        # Use self.image_var.get() to get the selected value
        board_number = int(self.image_var.get()[-1])
        path = f"data/gameboards_start_layout/game{board_number}.png"

        image = Image.open(path)
        image = image.resize((600, 300))
        self.photo = ImageTk.PhotoImage(image)

        # Update the image of the existing label
        self.image_label.config(image=self.photo)

    def check_winner(self, car_name, time):
        if car_name == 'X' or car_name == 'x':
            if self.board.is_won():
                self.clear_interface()
                
                # Display a message and a button to proceed
                win_label = tk.Label(self.master, text="Congratulations! You have won!", font=("Helvetica", 16), pady=20)
                win_label.pack()

                proceed_button = ttk.Button(self.master, text="Proceed", command=self.home())
                proceed_button.pack()
        else:
            pass
    
    def clear_labels(self):
        # Clear all existing error labels
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                widget.destroy()
            if isinstance(widget, tk.Label) and widget.cget("fg") == "blue":
                widget.destroy()
                break

    def clear_interface(self):
        # Destroy all widgets in the master window
        for widget in self.master.winfo_children():
            widget.destroy()