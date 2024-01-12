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
        self.vehicle_position_list = []
        self.size = size

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
            self.vehicle_position_list.append(vehicle.positions)

        #TODO: unpack lists?
        # itertools.chain(*self.vehicle_position_list)
    

    # Method to ensure pieces are actually on the board
    def find_vehicle(self, name):
        for vehicle in self.vehicles_list:
            if vehicle.name == name:
                return vehicle
        return None

    def position_error(self, vehicle):
        self.vehicle_position_list.append(vehicle.positions)
        raise ValueError("New position already occupied")
    
    def move_piece(self, name, movement):
        # Make sure piece excists
        vehicle = self.find_vehicle(name)
        if vehicle is None:
            raise ValueError("Piece not found")        

        # vehicles.positions = (col, row)
        # Makes sure the piece stays on the board
        if vehicle.orientation == 'H':
            if movement > 0 and not 0 <= vehicle.positions[-1][1] + movement < self.size:
                raise ValueError("Position out of bounds")
            elif movement < 0 and not 0 <= vehicle.positions[0][1] + movement < self.size:
                raise ValueError("Position out of bounds")
        else:
            if movement > 0 and not 0 <= vehicle.positions[-1][0] + movement < self.size:
                raise ValueError("Position out of bounds")
            elif movement < 0 and not 0 <= vehicle.positions[0][0] + movement < self.size:
                raise ValueError("Position out of bounds")

        #TODO: what if position is occupied, reset list
        self.vehicle_position_list.remove(vehicle.positions)
        
        new_positions=[]
        if vehicle.orientation == 'V':
            for position in vehicle.positions:
                col, row = position
                new_positions.append((col + movement, row))
        else:
            for position in vehicle.positions:
                col, row = position
                new_positions.append((col, row + movement))

        
        # Check if new position is already occupied
        for position in new_positions:
            for position_list in self.vehicle_position_list:
                if position in position_list:
                    self.position_error(vehicle)
        
        # Update positions
        vehicle.change_position(new_positions)
        self.vehicle_position_list.append(vehicle.positions)        


    def print_board(self):
        """ 
        Prints the board in a neat format.
        """
        visualize(self.vehicles_list, self.size)


