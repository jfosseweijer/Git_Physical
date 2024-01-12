import numpy as np
from ..visualisation.visualize import plot as visualize

class Vehicle:
    def __init__(self, length, orientation, position, name, colour='white'):
        self.length = int(length) - 1
        self.orientation = orientation
        self.position = position
        self.name = name
        self.colour = colour

class Board:
    def __init__(self, size=12):
        self.vehicles_list = []
        self.vehicle_positions = []
        self.size = size

    def setup_board(self, gameboard):
        # Set the grid of the board
        for name, car in gameboard.iterrows():
            # Set length to be an int instead of string
            length = int(car['length'])

            # Subtract 1 from position to make it zero-indexed
            car['row'] -= 1
            car['col'] -= 1

            if name == 'X':
                colour = np.array([255, 0, 0])
            else:
                # Random rgb colour
                colour = np.random.choice(range(256), size=3)

            for i in range(length):
                if car['orientation'] == 'H':
                    self.vehicle_positions.append((car['col']+i, car['row']))
                else:
                    self.vehicle_positions.append((car['col'], car['row']+i))

            # Create vehicle object and add it to the board, n serves as name
            self.vehicles_list.append(Vehicle(length, car['orientation'], (car['col'], car['row']), name, colour))
            

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

        old_col, old_row = vehicle.position
        if vehicle.orientation == 'H':
            old_positions = [old_col + i for i in range(vehicle.length + 1)]
        else:
            old_positions = [old_row + i for i in range(vehicle.length + 1)]
        
        # Makes sure the piece stays on the board
        if vehicle.orientation == 'H':
            new_row = old_row
            new_col = old_col + movement
            if movement > 0 and not 0 <= new_col + vehicle.length < self.size:
                raise ValueError("Position out of bounds")
            if movement < 0 and not 0 <= new_col < self.size:
                raise ValueError("Position out of bounds")
        else:
            new_col = old_col
            new_row = old_row + movement
            if movement > 0 and not 0 <= new_row + vehicle.length < self.size:
                raise ValueError("Position out of bounds")
            if movement < 0 and not 0 <= new_row < self.size:
                raise ValueError("Position out of bounds")

        for old_place in old_positions:
            if old_place in self.vehicle_positions:
                self.vehicle_positions.remove(old_place)

        # Check if new position is already occupied
        new_positions = []
        for i in range(abs(movement)):
            if vehicle.orientation == 'H':
                new_positions.append((old_col + i, old_row))
                if movement > 0:
                    if old_col + vehicle.length + i in self.vehicles_list:
                        place_error(old_positions)
                else:
                    if old_col - i in self.vehicles_list:
                        place_error(old_positions)
            else:
                new_position.append(old_col, old_row + i)
                if movement > 0:
                    if old_row + vehicle.length + i in self.vehicles_list:
                        place_error(old_positions)
                else:
                    if old_row - i in self.vehicles_list:
                        place_error(old_positions)

        # Update positions
        for new_place in new_positions:
            self.vehicle_positions.append(new_place)
        vehicle.position = (new_col,new_row)

    def place_error(self, old_positions):
        raise ValueError("New position already occupied")
        for old_place in old_positions:
            self.vehicle_positions.append(old_place)



    def print_board(self):
        """ 
        Prints the board in a neat format.
        """
        visualize(self.vehicles_list, self.size)


