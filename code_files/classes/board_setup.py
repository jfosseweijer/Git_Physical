import numpy as np
import itertools
import copy
from ..algorithms import generator as generator
from ..classes.queue import Queue as Queue
from ..classes.stack import Stack as Stack
from ..visualisation.visualize import plot as visualize
from ..algorithms.no_reverse import random_without_reverse
from ..algorithms.depth_search import depth_search
from ..algorithms.breadth_search import breadth_search
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

        ## Er was een -1 in de tuple waardoor generate_random_board niet werkte
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
    def __init__(self, size, show_board=False):
        """
        Initializes the Board class with the specified size.

        Parameters:
        - size (int): The size of the board.
        - show_board (bool): Whether or not to update board.png every step.
        """

        self.vehicles_list = []
        self.nested_vehicle_positions = []
        self.size = size
        self.show_board = show_board
        self.iterations = 0

    def setup_board(self, gameboard):
        """
        Sets up the board with vehicles and their initial positions.

        Parameters:
        - gameboard (DataFrame): DataFrame containing vehicle information.
        """

        # Set the grid of the board exit
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
    
    def move_piece(self, name, movement, user_input=False):
        """
        Moves a vehicle on the board.

        Parameters:
        - name (str): The name of the vehicle to move.
        - movement (int): The number of steps to move the vehicle.
        """

        # Make sure piece excists
        vehicle = self.find_vehicle(name)
        if vehicle is None:
            print(f"Vehicle {name.name} not found")
            raise ValueError("Piece not found")        

        # Makes sure the piece stays on the board
        self.check_boundries(vehicle, movement)
        route, new_positions = self.make_path(vehicle, movement)

        # Check if new position is already occupied
        if route & self.vehicle_position_set:
            raise ValueError("New position already occupied")

        if user_input:
            # Update positions
            self.update_positions_set(vehicle, new_positions)
        else: 
            return new_positions
    
    def check_boundries(self, vehicle, movement):
        """
        Checks if moving a vehicle is within the board boundaries.

        Parameters:
        - vehicle (Vehicle): The vehicle to check.
        - movement (int): The number of steps to move the vehicle.
        """

        if vehicle.orientation == 'H':
            #print(vehicle.positions)
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

        #print(route, final_positions)
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

    def plot_information(self):
        return self.vehicles_list, self.size, self.exit
    
    def random_solve(self, move_max=10000):
        self.iterations = 0
        while not self.is_won() and self.iterations < move_max:
            #self.print_board()
            self.iterations += 1
            name, movement, position = random_step(self)
            vehicle = self.find_vehicle(name)
            self.update_positions_set(vehicle, position)
            #time.sleep(0.05)
            #print(name, movement)

        if self.is_won():
            print(f"Game is won in {self.iterations} moves")
        else:
            print(f"Game not solved after {self.iterations} moves")

    def no_reverse_solve(self, move_max=10000):
        self.iterations = 0
        move = (None, 0, None)
        while not self.is_won() and self.iterations < move_max:
            #self.print_board()
            self.iterations += 1
            move = random_without_reverse(self, move)
            vehicle = self.find_vehicle(move[0])
            self.update_positions_set(vehicle, move[2])
            #time.sleep(0.05)
            #print(move[0], move[1])
            
        if self.is_won():
            print(f"Game is won in {self.iterations} moves")
        else:
            print(f"Game not solved after {self.iterations} moves")

    def depth_search(self, move_max=10000):
        self.iterations = 0
        bottom = 50
        history = Stack()
        made_moves = {}
        while not self.is_won() and self.iterations < move_max:
            #self.print_board()
            self.iterations += 1
            name, movement, position, history, made_moves = depth_search(self, history, made_moves, bottom)
            vehicle = self.find_vehicle(name)
            self.update_positions_set(vehicle, position)
            #time.sleep(0.05)
            #print(name, movement)
            
        if self.is_won():
            print(f"Game is won in {self.iterations} moves")
        else:
            print(f"Game not solved after {self.iterations} moves")

    def breadth_search(self, move_max=10000):
        self.iterations = 0
        current_layer_boards = []
        current_layer_index = None
        former_layer_boards = [(self, (None, None, None))]
        former_layer_index = 0
        played_boards = []
        board: Board = copy.deepcopy(former_layer_boards[former_layer_index][0])
        #board.print_board()
        while not board.is_won() and self.iterations < move_max:
            self.iterations += 1
            name, movement, position, current_layer_boards, current_layer_index, former_layer_boards, former_layer_index = breadth_search(current_layer_boards, current_layer_index, former_layer_boards, former_layer_index)
            board: Board = copy.deepcopy(former_layer_boards[former_layer_index][0])
            vehicle = board.find_vehicle(name)
            board.update_positions_set(vehicle, position)
            current_layer_boards.append((board, (name, movement, position)))
            #board.print_board()
            #time.sleep(0.05)
            #print(name, movement)
            #if self.iterations % 1000 == 0:
            #    print(self.iterations)

        if board.is_won():
            print(f"Game is won in {self.iterations} moves")
            # Heb deze variabel nodig want: while board.is_won() en niet while self.is_won()
            self.won = True
        else:
            print(f"Game not solved after {self.iterations} moves")
            self.won = False

    def astar_solve(self, move_max=10000):
        pass

    def random_board_df(size, num_cars, car_truck_ratio, lock_limit, exit_distance, HV_ratio):
        """
        Returns a random board as a DataFrame.
        Sometimes we want just the dataframe, so we can set up
        multiple boards at with the same initial state.

        Parameters
        ----------
            size int : Size of the board.
            num_cars int : Number of cars on the board.
            car_truck_ratio tuple : Ratio of cars to trucks.
            lock_limit int : Minimum number of open spaces in column or row
            before it is considered locked. Higher values result in easier boards.
            HV_ratio tuple : Ratio of horizontal to vertical cars.
        
        Returns
        -------
            initial_state pd.DataFrame : Initial state of the board.
            can be used to fill the board class with .set_board()
        """
        df_board_start = generator.random_board(size, num_cars, car_truck_ratio, lock_limit, exit_distance, HV_ratio)
        return df_board_start
    
    def generate_random_board(self, num_cars, car_truck_ratio, lock_limit, exit_distance, HV_ratio):
        """
        Generates a random board and immediately sets it up.

        Parameters
        ----------
            size int : Size of the board.
            num_cars int : Number of cars on the board.
            car_truck_ratio tuple : Ratio of cars to trucks.
            lock_limit int : Minimum number of open spaces in column or row
            before it is considered locked. Higher values result in easier boards.
            HV_ratio tuple : Ratio of horizontal to vertical cars.
        """
        self.setup_board(self.random_board_df(num_cars, car_truck_ratio, lock_limit, exit_distance, HV_ratio))

    def is_won(self):
        """
        Checks if the player has won the game.

        Returns:
        - bool: True if the player has won, False otherwise.
        """
    
        red_car = self.find_vehicle('X')

        if red_car.positions[-1][0] == self.exit[1]:
            #self.print_board()
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
        self.colours = [[0, 1, 0], [0, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 1], [1, 0.5, 0], [0.5, 0, 1], [0.5, 1, 0], [0, 0.5, 0.5], [1, 0.5, 0.5], [0.5, 0.25, 0], [0.8, 0.8, 0.8],  [0.2, 0.2, 0.2], [0.6, 0.3, 0.1],  [0.7, 0.5, 0.2], [0.4, 0.8, 0.2], [0, 0.8, 0.8], [0.8, 0.2, 0.2], [0.5, 0.5, 1], [0.9, 0.9, 0], [0.3, 0.5, 0.7],  [0.4, 0.6, 0.2], [0.7, 0.2, 0.7], [0.6, 0.8, 0.9], [0.8, 0.4, 0.8], [0.9, 0.6, 0.4], [0.1, 0.3, 0.6], [0.7, 0.5, 0.8], [0.4, 0.1, 0.4], [0.9, 0.9, 0.5], [0.6, 0.6, 0.6], [0.1, 0.5, 0.3], [0.9, 0.2, 0.5], [0.8, 0.7, 0.1], [0.2, 0.7, 0.4], [0.5, 0.5, 0.7], [0.7, 0.5, 0.5], [0.4, 0.2, 0.6], [0.8, 0.3, 0.3], [0.4, 0.8, 0.7],  [0.8, 0.6, 0.2], [0.1, 0.6, 0.3], [0.9, 0.4, 0.6],[0.3, 0.1, 0.8],[0.5, 0.7, 0.9], [0.7, 0.3, 0.5], [0.2, 0.9, 0.5], [0.6, 0.1, 0.9], [0.3, 0.8, 0.1], [0.9, 0.3, 0.2], [0.2, 0.4, 0.9], [0.5, 0.9, 0.3], [0.1, 0.7, 0.8], [0.8, 0.1, 0.1], [0.3, 0.4, 0.5], [0.7, 0.9, 0.4], [0.4, 0.3, 0.3], [0.9, 0.7, 0.7], [0.2, 0.8, 0.6], [0.6, 0.9, 0.8], [0.1, 0.2, 0.3], [0.5, 0.3, 0.9], [0.8, 0.9, 0.1], [0.3, 0.6, 0.8], [0.9, 0.1, 0.9], [0.2, 0.1, 0.7], [0.7, 0.8, 0.3], [0.4, 0.7, 0.1], [0.9, 0.8, 0.6], [0.2, 0.5, 0.8], [0.6, 0.4, 0.3], [0.1, 0.4, 0.8], [0.8, 0.1, 0.6], [0.3, 0.9, 0.9], [0.7, 0.6, 0.9], [0.4, 0.9, 0.9], [0.9, 0.4, 0.1], [0.2, 0.6, 0.5]]
        return self.colours[index]