class Vehicle:
    def __init__(self, length, orientation, position, name, colour='black'):
        self.length = int(length)
        self.orientation = orientation
        self.position = position
        self.name = name
        self.colour = colour

class Board:
    def __init__(self, size):
        self.grid = np.array([[' '] * size] * size, dtype=object)
        self.vehicles = []
        self.size = size

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        col, row = vehicle.position
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                self.grid[row][col + i] = vehicle.name
        else:
            for i in range(vehicle.length):
                self.grid[row + i][col] = vehicle.name

    # Method to ensure pieces are actually on the board
    def find_vehicle(self, name):
        for vehicle in self.vehicles:
            if vehicle.name == name:
                return vehicle
        return None
    
    def place_piece(self, vehicle, new_position):
        col, row = new_position
        if col < 0 or col >= self.size or row < 0 or row >= self.size:
            raise ValueError("Position out of bounds")
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                self.grid[row][col + i] = vehicle.name
        else:
            for i in range(vehicle.length):
                self.grid[row + i][col] = vehicle.name

    def move_piece(self, name, new_position):
        # Make sure piece is on the board
        vehicle = self.find_vehicle(name)
        if vehicle is None:
            raise ValueError("Piece not found")

        old_col, old_row = vehicle.position
        new_col, new_row = new_position

        # Makes sure the piece is moving along it's orientation 
        if vehicle.orientation == 'H' and old_row != new_row:
            raise ValueError("Invalid move")
        elif vehicle.orientation == 'V' and old_col != new_col:
            raise ValueError("Invalid move")


        # Makes sure new position is within the board
        if vehicle.orientation == 'H':
            if new_col < 0 or new_col + vehicle.length > self.size:
                raise ValueError("Position out of bounds")
        else:
            if new_row < 0 or new_row + vehicle.length > self.size:
                raise ValueError("Position out of bounds")

        # Check if new position is already occupied
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                if self.grid[new_row][new_col + i] != ' ' and self.grid[new_row][new_col + i] != name:
                    raise ValueError("New position already occupied")
        else:
            for i in range(vehicle.length):
                if self.grid[new_row + i][new_col] != ' ' and self.grid[new_row + i][new_col] != name:
                    raise ValueError("New position already occupied")

        # Clear old position
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                self.grid[old_row][old_col + i] = ' '
        else:
            for i in range(vehicle.length):
                self.grid[old_row + i][old_col] = ' '

        # Place piece at new position
        vehicle.position = new_position
        self.place_piece(vehicle, new_position)

    def print_board(board):
        """ 
        Prints the board in a neat format.
        """
        for row in board.grid:
            print(' '.join(str(x).ljust(2) for x in row))


