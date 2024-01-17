import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import numpy as np

class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("RUSH HOUR")

        # Load image and display it
        self.load_image('interface.png')

        # Buttons for different functionalities
        user_button = tk.Button(master=self.master, text="User", command=self.create_game('User'))
        user_button.pack(side=tk.LEFT)

        random_button = tk.Button(master=self.master, text="Random", command=self.create_game('Random'))
        random_button.pack(side=tk.LEFT)

        algorithm_button = tk.Button(master=self.master, text="Algorithm", command=self.create_game('Algorithm'))
        algorithm_button.pack(side=tk.LEFT)

    def create_game(self, name):
        self.clear_interface()
        self.master.title(name)

        # Matplotlib figure and canvas for plotting
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot_canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.plot_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Button to trigger the plot
        self.plot_button = tk.Button(master=self.master, text="Plot", command=self.plot_data)
        self.plot_button.pack(side=tk.BOTTOM)

    def load_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((600, 300))
        self.photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.master, image=self.photo)
        label.pack()

    def plot_data(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')

        self.plot_canvas.draw()
    
    def clear_interface(self):
        # Destroy all widgets in the master window
        for widget in self.master.winfo_children():
            widget.destroy()
