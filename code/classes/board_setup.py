import numpy as np
import itertools
from ..visualisation.visualize import plot as visualize
from ..algorithms.randomise import random_step

class Vehicle:
    def __init__(self, length, orientation, col, row, name, colour='white'):
        """
        Initializes a Vehicle instance.

        Parameters:
        - length (int or str): The length of the vehicle.
        - orientation (str): The orientation of the vehicle ('H' for horizontal, 'V' for vertical).
        - col (int): The column of the top-left corner of the vehicle.
        - row (int): The row of the top-left corner of the vehicle.
        - name (str): The name of the vehicle.
        - colour (str or list): The color of the vehicle (default is 'white').
        """
        self.length = int(length)
        self.orientation = orientation
        self.name = name
        self.colour = colour
        self.set_positions((col, row))

    def set_positions(self, position):
        """
        Sets the positions of the vehicle based on its orientation and top-left corner.

        Parameters:
        - position (tuple): The (col, row) coordinates of the top-left corner.
        """  

        if self.orientation == 'H':
            self.positions = [(position[0] + i - 1, position[1] - 1) for i in range(self.length)]
        else:
            self.positions = [(position[0] - 1, position[1] + i - 1) for i in range(self.length)]

    def change_position(self, new_positions):
        """
        Changes the position of the vehicle.

        Parameters:
        - new_positions (list): The new positions of the vehicle.
        """

        self.positions = new_positions
            
class Board:
    def __init__(self, size):
        """
        Initializes the Board class with the specified size.

        Parameters:
        - size (int): The size of the board.
        """

        self.vehicles_list = []
        self.nested_vehicle_positions = []
        self.size = size

    def setup_board(self, gameboard):
        """
        Sets up the board with vehicles and their initial positions.

        Parameters:
        - gameboard (DataFrame): DataFrame containing vehicle information.
        """

        # Set the grid of the board
        for index, (name, car) in enumerate(gameboard.iterrows()):
            # Set length to be an int instead of string
            length = int(car['length'])

            if name == 'X':
                colour = np.array([1, 0, 0])
                self.exit = (car['row'] - 1, self.size - 1)
            else:
                colour = self.create_colours(index)

            # Create vehicle object and add it to the board, n serves as name
            vehicle = Vehicle(length, car['orientation'], car['col'], car['row'], name, colour)
            self.vehicles_list.append(vehicle)                  
            self.nested_vehicle_positions.append(vehicle.positions)

        self.update_positions_set()

    # Method to ensure pieces are actually on the board
    def find_vehicle(self, name):
        """
        Finds a vehicle by its name.

        Parameters:
        - name (str): The name of the vehicle to find.

        Returns:
        - Vehicle or None: The found vehicle or None if not found.
        """

        for vehicle in self.vehicles_list:
            if vehicle.name == name:
                return vehicle
        return None
    
    def move_piece(self, name, movement):
        """
        Moves a vehicle on the board.

        Parameters:
        - name (str): The name of the vehicle to move.
        - movement (int): The number of steps to move the vehicle.
        """

        # Make sure piece excists
        vehicle = self.find_vehicle(name)
        if vehicle is None:
            raise ValueError("Piece not found")        

        # Makes sure the piece stays on the board
        self.check_boundries(vehicle, movement)
        route, new_positions = self.make_path(vehicle, movement)

        # Check if new position is already occupied
        if route & self.vehicle_position_set:
            raise ValueError("New position already occupied")

        # Update positions
        self.update_positions_set(vehicle, new_positions)
    
    def check_boundries(self, vehicle, movement):
        """
        Checks if moving a vehicle is within the board boundaries.

        Parameters:
        - vehicle (Vehicle): The vehicle to check.
        - movement (int): The number of steps to move the vehicle.
        """

        if vehicle.orientation == 'H':
            print(vehicle.positions)
            if movement > 0 and not vehicle.positions[-1][0] + movement < self.size:
                raise ValueError("Position out of right bounds")
            elif movement < 0 and not 0 <= vehicle.positions[0][0] + movement:
                raise ValueError("Position out of left bounds")
        else:
            if movement > 0 and not vehicle.positions[-1][1] + movement < self.size:
                raise ValueError("Position out of top bounds")
            elif movement < 0 and not 0 <= vehicle.positions[0][1] + movement:
                raise ValueError("Position out of bottom bounds")
            
    def make_path(self, vehicle, movement):
        """
        Generates the route and final positions for a vehicle movement.

        Parameters:
        - vehicle (Vehicle): The vehicle to move.
        - movement (int): The number of steps to move the vehicle.

        Returns:
        - tuple: A tuple containing the route (set) and final positions (list).
        """

        if vehicle.orientation == 'H':
            if movement > 0:
                route = {(vehicle.positions[-1][0] + step, vehicle.positions[-1][1]) for step in range(1, movement + 1)}
            else:
                route = {(vehicle.positions[0][0] + step, vehicle.positions[0][1]) for step in range(movement, 0)}
            
            final_positions = [(position[0] + movement, position[1]) for position in vehicle.positions]

        else:
            if movement > 0:
                route = {(vehicle.positions[-1][0], vehicle.positions[-1][1] + step) for step in range(1,movement+1)}
            else:
                route = {(vehicle.positions[0][0], vehicle.positions[0][1] + step) for step in range(movement, 0)}
            
            final_positions = [(position[0], position[1] + movement) for position in vehicle.positions]

        print(route, final_positions)
        return route, final_positions

    def update_positions_set(self, vehicle=False, new_positions=False):
        """
        Updates the set of vehicle positions on the board.

        Parameters:
        - vehicle (Vehicle): The vehicle to update. Default is False.
        - new_positions (list): The new positions of the vehicle. Default is False.
        """
        if new_positions:
            self.nested_vehicle_positions.remove(vehicle.positions)
            self.nested_vehicle_positions.append(new_positions)
            vehicle.change_position(new_positions)
        self.vehicle_position_set = set(itertools.chain(*self.nested_vehicle_positions))

    def print_board(self):
        """Prints the board in a neat format."""

        visualize(self.vehicles_list, self.size, self.exit)

    def random_solve(self):
        """
        Checks if the player has won the game.

        Returns:
        - bool: True if the player has won, False otherwise.
        """

        iterations = 0
        while not self.is_won() and iterations < 1000:
            iterations += 1
            movement = random_step(self)
            self.move_piece(movement[0], movement[1])
        pass

    def is_won(self):
        """
        Checks if the player has won the game.

        Returns:
        - bool: True if the player has won, False otherwise.
        """
    
        red_car = self.find_vehicle('X')

        if red_car.positions[-1][0] >= self.exit[0]:
            return True
        else:
            return False

    def create_colours(self, index):
        """
        Get a unique color to distinguish a care, based on index.

        Parameters:
        - index (int): The index to determine the color.

        Returns:
        - list: A list representing the RGB color.
        """
        self.colours = [[0, 1, 0], [0, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 1], [1, 0.5, 0], [0.5, 0, 1], [0.5, 1, 0], [0, 0.5, 0.5], [1, 0.5, 0.5], [0.5, 0.25, 0], [0.8, 0.8, 0.8],  [0.2, 0.2, 0.2], [0.6, 0.3, 0.1],  [0.7, 0.5, 0.2], [0.4, 0.8, 0.2], [0, 0.8, 0.8], [0.8, 0.2, 0.2], [0.5, 0.5, 1], [0.9, 0.9, 0], [0.3, 0.5, 0.7],  [0.4, 0.6, 0.2], [0.7, 0.2, 0.7], [0.6, 0.8, 0.9], [0.8, 0.4, 0.8], [0.9, 0.6, 0.4], [0.1, 0.3, 0.6], [0.7, 0.5, 0.8], [0.4, 0.1, 0.4], [0.9, 0.9, 0.5], [0.6, 0.6, 0.6], [0.1, 0.5, 0.3], [0.9, 0.2, 0.5], [0.8, 0.7, 0.1], [0.2, 0.7, 0.4], [0.5, 0.5, 0.7], [0.7, 0.5, 0.5], [0.4, 0.2, 0.6], [0.8, 0.3, 0.3], [0.4, 0.8, 0.7],  [0.8, 0.6, 0.2], [0.1, 0.6, 0.3], [0.9, 0.4, 0.6],[0.3, 0.1, 0.8],[0.5, 0.7, 0.9],]
        return self.colours[index]