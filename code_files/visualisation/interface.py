import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle 
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from code_files.classes.board_setup import Board as Board

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

        random_button = ttk.Button(master=self.master, text="Random", command=lambda: self.create_random(int(image_menu.get()[-1])-1))
        random_button.pack(side=tk.BOTTOM, fill=tk.X)

        algorithm_button = ttk.Button(master=self.master, text="Algorithm", command=lambda: self.create_Algorithm(int(image_menu.get()[-1])-1))
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
        vehicles, size, exit = self.board.plot_information()
        self.plot(vehicles, size, exit)

    def move_car(self):
        # Clear previous error labels
        self.clear_error_labels()

        move = self.input_var.get()

        # Split the move input and handle invalid syntax
        try:
            car_name, movement = map(str.strip, move.split(','))
            movement = int(movement)
        except ValueError:
            self.display_error("Please use this format 'A,1'")
            return

        # Find the car and handle invalid car name
        car = self.board.find_vehicle(car_name.upper())
        if car is None:
            self.display_error(f"No car named {car_name} found on the board")
            return

        # Try to move the piece and handle invalid moves
        try:
            self.board.move_piece(car_name.upper(), movement, move)
            vehicles, size, exit = self.board.plot_information()
            self.plot(vehicles, size, exit)
        except ValueError as e:
            self.display_error(str(e))

        self.check_winner(car_name)
        
    def display_error(self, error_message):
        # Clear previous error labels, if any
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                widget.destroy()

        # Display the error message in the Tkinter interface using Label
        error_label = tk.Label(self.master, text=f"Error: {error_message}", fg="red")
        error_label.pack()

    def clear_error_labels(self):
        # Clear all existing error labels
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                widget.destroy()

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
        rect = plt.Rectangle((exit[1] + 0.5, exit[0] - 0.5), 1, 1, linewidth=5, edgecolor='black', facecolor='none', zorder=2)

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
        self.master.update_idletasks()


    def check_winner(self, car_name):
        print(car_name)

        if car_name == 'X' or car_name == 'x':
            if self.board.is_won():
                self.clear_interface()
                
                # Display a message and a button to proceed
                win_label = tk.Label(self.master, text="Congratulations! You have won!", font=("Helvetica", 16), pady=20)
                win_label.pack()

                proceed_button = ttk.Button(self.master, text="Proceed", command=self.home())
                proceed_button.pack()


    def clear_interface(self):
        # Destroy all widgets in the master window
        for widget in self.master.winfo_children():
            widget.destroy()
