import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle 
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from code.classes.board_setup import Board as Board

class Interface:
    def __init__(self, master, gameboards):
        self.gameboards = gameboards
        self.master = master
        self.master.title("RUSH HOUR")
        
        self.style = ThemedStyle(master)
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
        board_number = int(image_menu.get()[-1])

        # Create the label for the image once during initialization
        self.image_label = tk.Label(self.master)
        self.image_label.pack()
        
        # Manually load the initial image
        self.load_image()  

        # Buttons for different functionalities
        user_button = ttk.Button(master=self.master, text="User", command=lambda: self.create_user(board_number))
        user_button.pack(side=tk.BOTTOM, fill=tk.X)

        random_button = ttk.Button(master=self.master, text="Random", command=lambda: self.create_random(board_number))
        random_button.pack(side=tk.BOTTOM, fill=tk.X)

        algorithm_button = ttk.Button(master=self.master, text="Algorithm", command=lambda: self.create_Algorithm(board_number))
        algorithm_button.pack(side=tk.BOTTOM, fill=tk.X)

    def create_user(self, board_number):
        self.clear_interface()
        self.master.title("user")

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [10, 1]}, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.input_var = tk.StringVar()
        
        move_button = ttk.Button(master=self.master, text="Move", command=self.move_car)
        move_button.pack()

        # Create an instance of the Board class
        board = Board(self.gameboards[board_number][1])
        board.setup_board(self.gameboards[board_number][0])
        
        # Call the plot_information method on the board instance
        vehicles, size, exit = board.plot_information()
        self.plot(vehicles, size, exit)

    def move_car(self, move):
        print(move)
            # car = None
            # valid_move = False
            # while valid_move == False:
            #     board.print_board()
            #     player_move = input("Enter the car and it's movement: ")
            #     try:
            #         player_move = player_move.split(',')
            #         valid_move = True
            #     except ValueError:
            #         valid_move = False
                    
            #     if len(player_move) == 2 and valid_move and len(player_move[1]) != 0 :
            #         car_name = player_move[0].upper()
            #         try:
            #             movement = int(player_move[1])
            #             valid_move = True
            #         except ValueError:
            #             valid_move = False

            #     if not valid_move:
            #         player_move = print("Please use this format (A,1): ")

            #     if valid_move:
            #         # Find the car and print its current position
            #         car = board.find_vehicle(car_name)

            #         if car is None:
            #             print(f"No car named {car_name} found on the board")
            #             valid_move = False

            #     # Check if input syntax is correct
            #     if valid_move:
            #         try:
            #             board.move_piece(car_name, movement, user_input)
            #         except ValueError as e:
            #             print(e)
            #             valid_move = False
            #             print(f"You can't move {car_name} by {movement}")


    def create_random(self):
        self.clear_interface()
        self.master.title("user")
    
    def create_Algorithm(self):
        self.clear_interface()
        self.master.title("user")

    def load_image(self, event=None):
        # Use self.image_var.get() to get the selected value
        board_number = int(self.image_var.get()[-1])
        path = f"data\\gameboards_start_layout\\game{board_number}.png"

        image = Image.open(path)
        image = image.resize((600, 300))
        self.photo = ImageTk.PhotoImage(image)

        # Update the image of the existing label
        self.image_label.config(image=self.photo)

    
    def plot(self, vehicles, size, exit):
        """
        Plot the game board with vehicles and exit.

        Parameters:
        - vehicles: List of Vehicle objects representing the vehicles on the board.
        - size: Size of the game board.
        - exit: Tuple representing the position of the exit (row, column).
        """
        # Create a grid for the game board
        grid = np.ones((size, size, 3))

        # Mark positions of vehicles on the grid
        for vehicle in vehicles:
            for position in vehicle.positions:
                col, row = position
                grid[row][col] = vehicle.colour

        # Create a rectangle for the exit with a black border
        rect = plt.Rectangle((exit[0] + 0.5, exit[1] - 0.5), 1, 1, linewidth=5, edgecolor='black', facecolor='none', zorder=2)

        # Clear the previous plots
        self.ax1.clear()
        self.ax2.clear()

        # Plot the image with the grid on the first subplot
        self.ax1.imshow(grid, interpolation='nearest')

        self.ax1.set_xticks(np.arange(0.5, size + 0.5, 1))
        self.ax1.set_yticks(np.arange(0.5, size + 0.5, 1))
        self.ax1.grid(axis='both', color='white', linewidth=2)
        self.ax1.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)

        # Add the rectangle to the plot
        self.ax1.add_patch(rect)

        # Create legend with explicit labels on the second subplot
        for vehicle in vehicles:
            self.ax2.plot([], [], color=np.array(vehicle.colour), label=vehicle.name)
        self.ax2.legend()
        self.ax2.axis('off')

        # Adjust layout to prevent clipping of legend
        plt.tight_layout()

        # Show the figure
        self.canvas.draw()

    def clear_interface(self):
        # Destroy all widgets in the master window
        for widget in self.master.winfo_children():
            widget.destroy()
