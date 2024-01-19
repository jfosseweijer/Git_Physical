def user_move(board):
    winner = False
    while not winner:
        car = None
        valid_move = False
        
        while valid_move == False:
            board.print_board()
            player_move = input("Enter the car and it's movement: ")
            
            try:
                player_move = player_move.split(',')
                valid_move = True
            except ValueError:
                valid_move = False
                
            if len(player_move) == 2 and valid_move and len(player_move[1]) != 0 :
                car_name = player_move[0].upper()
                try:
                    movement = int(player_move[1])
                    valid_move = True
                except ValueError:
                    valid_move = False

            if not valid_move:
                player_move = print("Please use this format (A,1): ")

            if valid_move:
                # Find the car and print its current position
                car = board.find_vehicle(car_name)

                if car is None:
                    print(f"No car named {car_name} found on the board")
                    valid_move = False

            # Check if input syntax is correct
            if valid_move:
                try:
                    board.move_piece(car_name, movement, player_move)
                except ValueError as e:
                    print(e)
                    valid_move = False
                    print(f"You can't move {car_name} by {movement}")

        if car_name == 'X':
            winner = board.is_won()