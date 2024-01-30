import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk, simpledialog
from ttkthemes import ThemedStyle 
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ..classes.stack import Stack
from code_files.visualisation.int_vis import plot as visualize
from code_files.visualisation.visualize import plot as figure
from code_files.classes.board_setup import Board as Board
from ..algorithms.no_reverse import random_without_reverse
from ..algorithms.breadth_search import breadth_search
from ..algorithms.randomise import random_step
from ..algorithms.depth_search import depth_search

import time
import copy
import pandas as pd


class Interface:
    def __init__(self, master, gameboards):
        self.gameboards = gameboards
        self.master = master
        self.input_name = False
        self.output_name = False
        self.home()

    def home(self):
        """
        Set up the home interface with dropdowns, buttons, and options.
        """
        # Clear existing interface
        self.clear_interface()
        self.master.title("RUSH HOUR")
        
        # Set the theme
        self.style = ThemedStyle(self.master)
        self.style.set_theme("yaru")

        # Create dropdown for images
        self.image_var = tk.StringVar()
        # Set a default image
        self.image_var.set("game 1")
        # Add options
        images = ["game 1", "game 2", "game 3", "game 4", "game 5", "game 6", "game 7", "game 8"]

        # Set image menu
        image_menu = ttk.Combobox(master = self.master, textvariable = self.image_var, values = images)
        image_menu.pack(pady = 10)
        
        # Couple the corresponding game visualization
        image_menu.bind("<<ComboboxSelected>>", self.load_image)

        # Create dropdown for visualization
        self.vis_var = tk.StringVar()
        # Set a default image
        self.vis_var.set("show visualisation")
        # Add options
        options = ["show visualisation", "no visualisation"]

        # Set the menu
        self.visualization_choice = ttk.Combobox(master = self.master, textvariable = self.vis_var, values = options)
        self.visualization_choice.pack(pady = 10)

        # Trace changes in the vis_var and call toggle_widgets
        self.vis_var.trace_add("write", self.toggle_widgets)

        # Create button and label (initially hidden)
        self.save_button = tk.Button(master = self.master, text = "Save Figure", command = self.input_prompt)
        self.save_button.pack(pady=10, after = self.visualization_choice)

        self.repeat_label = ttk.Label(self.master, text = "Enter an Integer:")
        self.repeat_label.pack(pady=10, after = self.visualization_choice)

        self.integer_entry = ttk.Entry(self.master, textvariable = self.repeat_label)
        self.integer_entry.pack(pady=10, after = self.repeat_label)
        self.repeat_label.pack_forget()
        self.integer_entry.pack_forget()

        # Create the label for the image once during initialization
        self.image_label = tk.Label(self.master)
        self.image_label.pack()
        
        # Manually load the initial image
        self.load_image()  

        # Buttons for different functionalities
        user_button = ttk.Button(master = self.master, text = "depth_search", command = lambda: self.experiment(int(image_menu.get()[-1])-1, alg_type = 'depth', visual = self.visualization_choice.get()))
        user_button.pack(side=tk.BOTTOM, fill=tk.X)

        algorithm_button = ttk.Button(master = self.master, text = "breadth_search", command = lambda: self.experiment(int(image_menu.get()[-1])-1, alg_type = 'breadth', visual = self.visualization_choice.get()))
        algorithm_button.pack(side=tk.BOTTOM, fill=tk.X)

        algorithm_button = ttk.Button(master = self.master, text = "Not reversing random algorithm", command = lambda: self.experiment(int(image_menu.get()[-1])-1, alg_type = 'non-reverse', visual = self.visualization_choice.get()))
        algorithm_button.pack(side=tk.BOTTOM, fill=tk.X)

        random_button = ttk.Button(master = self.master, text = "Random", command = lambda: self.experiment(int(image_menu.get()[-1])-1, alg_type = 'random', visual = self.visualization_choice.get()))
        random_button.pack(side=tk.BOTTOM, fill=tk.X)

        user_button = ttk.Button(master = self.master, text = "User", command = lambda: self.create_user(int(image_menu.get()[-1])-1))
        user_button.pack(side=tk.BOTTOM, fill=tk.X)

    def create_user(self, board_number):
        """
        Set up the user interface with input entry and move button.

        Parameters:
        - board_number (int): The index of the selected game board.

        Returns:
        None
        """
        # Clear existing interface
        self.clear_interface()
        self.master.title("user")

        # Create subplots for the image and legend
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [10, 1]}, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create option to provide input and output label
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
        """
        Move the selected car on the board based on user input.

        Returns:
        None
        """
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

    def experiment(self, board_number, alg_type, visual):
        self.experimenttimes = []
        self.visual = visual
        self.winner = False
        
        try:
            repeats = int(self.integer_entry.get())
        except ValueError:
            repeats = 1

        for run in range(repeats):
             # Initialize variables
            self.iterations = 0
            self.algorithm(board_number, alg_type)
            self.display_text(f'{run/repeats}', message=True)

        df = pd.DataFrame(self.experimenttimes, columns=['time'], index=['Index_{}'.format(i) for i in range(1, len(self.experimenttimes)+1)])

        # Export dataframe to CSV
        df.to_csv('experiment.csv')


    def algorithm(self, board_number, alg_type):
        """
        Run a specified algorithm on the given Rush Hour board.

        Parameters:
        - board_number (int): Index of the board to be used.
        - alg_type (str): Type of algorithm to be executed.
        - visual (str): Visualization option ('show visualisation' or 'no visualisation').

        Returns:
        None
        """
        # Clear the interface and set the title
        self.clear_interface()
        self.master.title("algorithm")

        # Set up visualization if selected
        if self.visual == "show visualisation":
            self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [10, 1]}, figsize=(10, 5))
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create an instance of the Board class
        self.board = Board(self.gameboards[board_number][1])
        self.board.setup_board(self.gameboards[board_number][0])

        # Initialize move based on the algorithm type
        if alg_type == 'non-reverse':
            move = (None, 0, None)
        elif alg_type == 'breadth':
            current_layer_boards = []
            current_layer_index = None
            former_layer_boards = [(self.board, (None, 0, None))]
            former_layer_index = 0
            move = (None, 0, None, current_layer_boards, current_layer_index, former_layer_boards, former_layer_index)
            self.board: Board = copy.deepcopy(former_layer_boards[former_layer_index][0])
        elif alg_type == 'depth':
            bottom = 30
            history = Stack()
            made_moves = {}
            move = (None, 0, None, history, made_moves)

        # Save the initial figure
        if self.input_name and self.visual == 'show visualisation':
            figure(self.board.vehicles_list, self.board.size, self.board.exit, self.input_name)

        # Record the start time
        start = time.time()

        # Main loop for algorithm iterations
        while not self.winner and self.iterations < 1000:
            # Clear previous error labels after a certain number of iterations
            if self.iterations > 10:
                self.clear_labels()
            self.iterations += 1

            # Visualization update
            if self.visual == "show visualisation":
                visualize(self.board, self.ax1, self.ax2)
                time.sleep(0.2)
                self.canvas.draw()
                self.master.update_idletasks()

            # Execute the selected algorithm
            if alg_type == 'random':
                move = random_step(self.board)
            elif alg_type == 'non-reverse':
                move = random_without_reverse(self.board, move)
            elif alg_type == 'breadth':
                move = breadth_search(move[3], move[4], move[5], move[6])
                self.board: Board = copy.deepcopy(move[5][move[6]][0])
                print(move)
            elif alg_type == 'depth':
                move = depth_search(self.board, move[3], move[4], bottom)

            # Try to find the vehicle based on the move
            try:
                vehicle = self.board.find_vehicle(move[0])
            except UnboundLocalError:
                break

            # Update the board 
            self.board.update_positions_set(vehicle, move[2])

            # Update breadth-first search history
            if alg_type == 'breadth':
                move[3].append((self.board, (move[0], move[1], move[2])))

            # Check if the game is complete and calculate the time
            if self.visual == 'no visualisation':
                runtime = self.check_winner(move[0], time.time() - start)
            else:
                # Display the move
                self.display_text((move[0], move[1]), move=True)
                # Check if the move wins the game
                self.check_winner(move[0], time.time() - start - self.iterations * 0.2)
        
        if not self.winner:
            self.runtime = time.time() - start
            self.experimenttimes.append(self.runtime)
        else:
            self.experimenttimes.append(self.runtime)


        # Save the final figure
        if self.visual == 'show visualisation':
            # Clear the interface after algorithm completion
            self.clear_interface()
            if self.output_name:
                figure(self.board.vehicles_list, self.board.size, self.board.exit, self.output_name)

    def toggle_widgets(self, *args):
        # Show/hide widgets based on the value of vis_var
        if self.vis_var.get() == "show visualisation":
            self.save_button.pack(pady = 10, after = self.visualization_choice)
            self.repeat_label.pack_forget()
            self.integer_entry.pack_forget()
            
        elif self.vis_var.get() == "no visualisation":
            self.save_button.pack_forget()
            self.repeat_label.pack(pady = 10, after = self.visualization_choice)
            self.integer_entry.pack(pady = 10, after = self.repeat_label)

    def input_prompt(self):
        # Ask the user for input using a dialog box
        user_input = simpledialog.askstring("Input", "Return filenames: 'input, output'")
        
        try:
            self.input_name, self.output_name = user_input.split(',')
        except ValueError:
            self.display_text('Inputs not valid', error = True)

    def display_text(self, text_message, error=False, message=False):
        """
        Display a message in the Tkinter interface.

        Parameters:
        - text_message: The message to be displayed.
        - error (bool): Indicates whether the message is an error message.
        - move (bool): Indicates whether the message is related to a move.
        """

        # Display the error message in the Tkinter interface using Label
        if error:
            # Create a red label for error messages
            error_label = tk.Label(self.master, text=f"Error: {text_message}", fg="red")
            error_label.pack()
        elif message:
            # Create a blue label for move-related messages
            move_label = tk.Label(self.master, text=f"{text_message}", fg="blue")
            move_label.pack()

    def load_image(self, event=None):
        # Use self.image_var.get() to get the selected value
        board_number = int(self.image_var.get()[-1])
        path = f"data/gameboards_start_layout/game{board_number}.png"

        image = Image.open(path)
        image = image.resize((600, 300))
        self.photo = ImageTk.PhotoImage(image)

        # Update the image of the existing label
        self.image_label.config(image=self.photo)

    def check_winner(self, car_name, runtime):
        """
        Check if the player has won and display a message.
        """
        if car_name.upper() == 'X':
            # Check if the board is in a winning state
            if self.board.is_won():
                print('won')
                if self.visual == "show visualisation":
                    self.clear_interface()

                    # Display a congratulatory message
                    win_label = tk.Label(self.master, text="Congratulations! You have won!", font=("Helvetica", 16), pady=20)
                    win_label.pack()

                    # Display the time taken to win
                    time_label = tk.Label(self.master, text=f"Time taken: {time:.2f} seconds", font=("Helvetica", 12), pady=10)
                    time_label.pack()

                    # Display a button to proceed
                    proceed_button = ttk.Button(self.master, text="Proceed", command=self.home)
                    proceed_button.pack()
                else:
                    print('time')
                    self.winner = True
                    self.runtime = runtime
        else:
            # The specified car is not the exit car, do nothing
            pass

    def clear_labels(self):
        """
        Clear all existing error and move labels.
        """
        for widget in self.master.winfo_children():
            # Check if the widget is a Label and has foreground color "red"
            if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                widget.destroy()
            # Check if the widget is a Label and has foreground color "blue"
            elif isinstance(widget, tk.Label) and widget.cget("fg") == "blue":
                widget.destroy()
                break

    def clear_interface(self):
        """
        Destroy all widgets in the master window, clearing the entire interface.
        """
        for widget in self.master.winfo_children():
            widget.destroy()
