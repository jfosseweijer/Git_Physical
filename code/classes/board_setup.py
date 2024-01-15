import numpy as np
import itertools
from ..visualisation.visualize import plot as visualize

class Vehicle:
    def __init__(self, length, orientation, col, row, name, colour='white'):
        """
        Creates a vehicle object
        """
        self.length = int(length)
        self.orientation = orientation
        self.name = name
        self.colour = colour
        self.set_positions((col, row))

    def set_positions(self, position):
        """
        Set a vehicles coordinates
        """      
        if self.orientation == 'H':
            self.positions = [(position[0] + i - 1, position[1] - 1) for i in range(self.length)]
        else:
            self.positions = [(position[0] - 1, position[1] + i - 1) for i in range(self.length)]

    def change_position(self, new_positions):
        """
        Updates a vehicles position
        """
        self.positions = new_positions
            
class Board:
    def __init__(self, size):
        """
        Sets board parameters
        """
        self.vehicles_list = []
        self.nested_vehicle_positions = []
        self.size = size

    def setup_board(self, gameboard):
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
        for vehicle in self.vehicles_list:
            if vehicle.name == name:
                return vehicle
        return None
    
    def move_piece(self, name, movement):
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
        if new_positions:
            self.nested_vehicle_positions.remove(vehicle.positions)
            self.nested_vehicle_positions.append(new_positions)
            vehicle.change_position(new_positions)
        self.vehicle_position_set = set(itertools.chain(*self.nested_vehicle_positions))

    def print_board(self):
        """ 
        Prints the board in a neat format.
        """
        visualize(self.vehicles_list, self.size, self.exit)

    def is_won(self):
        red_car = self.find_vehicle('X')

        if red_car.positions[-1][0] >= self.exit[0]:
            return True
        else:
            return False

    def create_colours(self, index):
        self.colours = [[0, 1, 0], [0, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 1], [1, 0.5, 0], [0.5, 0, 1], [0.5, 1, 0], [0, 0.5, 0.5], [1, 0.5, 0.5], [0.5, 0.25, 0], [0.8, 0.8, 0.8],  [0.2, 0.2, 0.2], [0.6, 0.3, 0.1],  [0.7, 0.5, 0.2], [0.4, 0.8, 0.2], [0, 0.8, 0.8], [0.8, 0.2, 0.2], [0.5, 0.5, 1], [0.9, 0.9, 0], [0.3, 0.5, 0.7],  [0.4, 0.6, 0.2], [0.7, 0.2, 0.7], [0.6, 0.8, 0.9], [0.8, 0.4, 0.8], [0.9, 0.6, 0.4], [0.1, 0.3, 0.6], [0.7, 0.5, 0.8], [0.4, 0.1, 0.4], [0.9, 0.9, 0.5], [0.6, 0.6, 0.6], [0.1, 0.5, 0.3], [0.9, 0.2, 0.5], [0.8, 0.7, 0.1], [0.2, 0.7, 0.4], [0.5, 0.5, 0.7], [0.7, 0.5, 0.5], [0.4, 0.2, 0.6], [0.8, 0.3, 0.3], [0.4, 0.8, 0.7],  [0.8, 0.6, 0.2], [0.1, 0.6, 0.3], [0.9, 0.4, 0.6],[0.3, 0.1, 0.8],[0.5, 0.7, 0.9],]
        return self.colours[index]