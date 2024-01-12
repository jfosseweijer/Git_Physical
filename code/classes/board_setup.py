import numpy as np
#TODO: import visualize

class Vehicle:
    def __init__(self, length, orientation, position, name, colour='white'):
        self.length = int(length)
        self.orientation = orientation
        self.position = position
        self.name = name
        self.colour = colour

class Board:
    def __init__(self, size=6):
        self.grid = np.array([[' '] * size] * size, dtype=object)
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

            for i in length:
                if car['orientation'] == 'H':
                    self.vehicle_positions.append((car['col'] + i, car['row']))
                else:
                    self.vehicle_positions.append((car['col'], car['row'] + i))

            # Create vehicle object and add it to the board, n serves as name
            self.vehicles_list.append(Vehicle(length, car['orientation'], (car['col'], car['row']), n, colour))
            

    # Method to ensure pieces are actually on the board
    def find_vehicle(self, name):
        for vehicle in self.vehicles_list:
            if vehicle.name == name:
                return vehicle
        return None

    def move_piece(self, name, new_position):
        # Make sure piece excists
        vehicle = self.find_vehicle(name)
        if vehicle is None:
            raise ValueError("Piece not found")

        old_col, old_row = vehicle.position
        new_col, new_row = new_position
        
        # Subtract 1 to make inputs zero-indexed
        new_col -= 1
        new_row -= 1

        # Create lists of positions
        if vehicle.orientation == 'H':
            old_positions = [(old_col + i, old_row) for i in range(vehicle.length)]
            new_positions = [(new_col + i, new_row) for i in range(vehicle.length)]
        else:
            old_positions = [(old_col, old_row + 1) for i in range(vehicle.length)]
            new_positions = [(new_col, new_row + 1) for i in range(vehicle.length)]

        # Makes sure the piece is moving along it's orientation 
        if vehicle.orientation == 'H' and old_row != new_row:
            raise ValueError("Invalid move")
        elif vehicle.orientation == 'V' and old_col != new_col:
            raise ValueError("Invalid move")


        # Makes sure new position is within the board
        for item in new_positions:
            if not 0 < item < self.size:
                raise ValueError("Position out of bounds")

        # Check if new position is already occupied
        for place in new_positions:
            if place not in old_positions and place in self.vehicle_positions:
                raise ValueError("New position already occupied")

        # update position
        self.vehicle_positions.remove(old_positions)
        self.vehicle_positions.append(new_position)
        vehicle.position = new_position

    def print_board(self):
        """ 
        Prints the board in a neat format.
        """
        visualize(self.grid, self.size)

