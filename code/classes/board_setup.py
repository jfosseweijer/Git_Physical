import numpy as np
import itertools
from ..visualisation.visualize import plot as visualize

class Vehicle:
    def __init__(self, length, orientation, position, name, colour='white'):
        self.length = int(length)
        self.orientation = orientation
        self.name = name
        self.colour = colour
        self.set_positions(position)

    def set_positions(self, position):
        row, col = position

        col -= 1
        row -= 1
        
        if self.orientation == 'H':
            self.positions = [(col, row + i) for i in range(self.length + 1)]
        else:
            self.positions = [(col + i, row) for i in range(self.length + 1)]

    def change_position(self, new_positions):
        self.positions = new_positions
            
class Board:
    def __init__(self, size):
        self.vehicles_list = []
        self.nested_vehicle_positions = []
        self.size = size

    def update_positions_set(self, vehicle=False, new_positions=False):
        if new_positions:
            self.nested_vehicle_positions.remove(vehicle.positions)
            self.nested_vehicle_positions.append(new_positions)
        self.vehicle_position_set = set(itertools.chain(*self.nested_vehicle_positions))    


    def setup_board(self, gameboard):
        # Set the grid of the board
        for name, car in gameboard.iterrows():
            # Set length to be an int instead of string
            length = int(car['length']) - 1

            if name == 'X':
                colour = np.array([255, 0, 0])
            else:
                # Random rgb colour
                colour = np.random.choice(range(256), size=3)

            # Create vehicle object and add it to the board, n serves as name
            vehicle = Vehicle(length, car['orientation'], (car['col'], car['row']), name, colour)
            self.vehicles_list.append(vehicle)                  
            self.nested_vehicle_positions.append(vehicle.positions)

        self.update_positions_set()

    # Method to ensure pieces are actually on the board
    def find_vehicle(self, name):
        for vehicle in self.vehicles_list:
            if vehicle.name == name:
                return vehicle
        return None
    
    #TODO: piece can move down out the box
    #TODO: get error out
    def move_piece(self, name, movement):
        # Make sure piece excists
        vehicle = self.find_vehicle(name)
        if vehicle is None:
            raise ValueError("Piece not found")        

        # vehicles.positions = (col, row)
        # Makes sure the piece stays on the board
        if vehicle.orientation == 'V':
            if movement > 0 and not 0 <= vehicle.positions[-1][1] + movement < self.size:
                raise ValueError("Position out of bounds")
            elif movement < 0 and not 0 <= vehicle.positions[0][1] + movement < self.size:
                raise ValueError("Position out of bounds")
        else:
            if movement > 0 and not 0 <= vehicle.positions[-1][0] + movement < self.size:
                raise ValueError("Position out of bounds")
            elif movement < 0 and not 0 <= vehicle.positions[0][0] + movement < self.size:
                raise ValueError("Position out of bounds")

        if vehicle.orientation == 'V':
            if movement > 0:
                route = {(vehicle.positions[-1][0], vehicle.positions[-1][1] + step + 1) for step in range(movement)}
            else:
                route = {(vehicle.positions[-1][1], vehicle.positions[0][1] + step + 1) for step in range(movement)}
            
            new_positions = [(position[0] + movement, position[1]) for position in vehicle.positions]

        else:
            if movement > 0:
                route = {(vehicle.positions[-1][0] + step + 1, vehicle.positions[-1][1]) for step in range(movement)}
            else:
                route = {(vehicle.positions[0][0] + step + 1, vehicle.positions[0][1]) for step in range(movement)}
        
            new_positions = [(position[0], position[1] + movement) for position in vehicle.positions]

        # Check if new position is already occupied
        if route & self.vehicle_position_set:
            print("hier")
            raise ValueError("New position already occupied")

        # Update positions
        vehicle.positions = new_positions
        self.update_positions_set(vehicle, new_positions)   


    def print_board(self):
        """ 
        Prints the board in a neat format.
        """
        visualize(self.vehicles_list, self.size)

    def is_won(self):
        red_car = self.find_vehicle('X')

        if red_car.positions[-1][1] >= self.size:
            return True
        else:
            return False
