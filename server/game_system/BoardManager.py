class BoardManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BoardManager, cls).__new__(cls)
        return cls._instance
    

    def __init__(self):
        if not self._initialized:
                
            self.character_locations = {
            "Scarlett": "Hallway4",
            "Plum": "Hallway6",
            "Mustard": "Hallway10",
            "Peacock": "Hallway16",
            "Green": "Hallway21",
            "White": "Hallway23"
            }

            self.weapon_locations = {
            "Candlestick": "Dining Room",
            "Dagger": "Study",
            "Leadpipe": "Conservatory",
            "Rope": "Kitchen",
            "Revolver": "Lounge",
            "Wrench": "Study"
            }

            self.clue_board = [
            ["Study", "Hallway2", "Hall", "Hallway4", "Lounge"],
            ["Hallway6", None, "Hallway8", None, "Hallway10"],
            ["Library", "Hallway12", "Billiard Room", "Hallway14", "Dining Room"],
            ["Hallway16", None, "Hallway18", None, "Hallway20"],
            ["Conservatory", "Hallway21", "Ballroom", "Hallway23", "Kitchen"]
            ]

    def check_if_valid_character_input(self, character_name):
        # Normalize the input to lowercase
        character_name_lower = character_name.lower()
        # Create a set of valid character names in lowercase
        valid_characters = {name.lower() for name in self.character_locations.keys()}
        # Check if the normalized input is in the set of valid characters
        return character_name_lower in valid_characters
        
    def check_if_valid_direction_input(self, possible_directions, input_direction):  
        for cur_direction in possible_directions:
            if input_direction == cur_direction:
                return True
            else:
                return False

    def get_possible_moves(self, player_character):
        #Prints out possible directions (Up, Down, Left, Right) you can move from the given room.oom_name (str): The name of the current room.
        #find the room name
        room_name = self.character_locations[player_character]
        # Find the position of the room on the board
        position = self.find_room_position(room_name)
        if position is None:
            print(f"Room '{room_name}' not found on the board.")
            return

        row, col = position
        directions = []
        rows = len(self.clue_board)
        cols = len(self.clue_board[0])

        # Define the possible moves with their corresponding adjustments
        moves = {
            'Up': (row - 1, col),
            'Down': (row + 1, col),
            'Left': (row, col - 1),
            'Right': (row, col + 1)
        }

        # Check each possible move
        for direction, (new_row, new_col) in moves.items():
            if 0 <= new_row < rows and 0 <= new_col < cols:
                destination = self.clue_board[new_row][new_col]
                if destination is not None:
                    directions.append((direction, destination))

        # Print the possible directions
        if directions:
            print(f"From '{room_name}', you can move to:")
            for idx, (direction, destination) in enumerate(directions, start=1):
                print(f"  {idx}. {direction}: {destination}")
            return directions
        else:
            print(f"No available moves from '{room_name}'.")
                
    #Finds the position (row, column) of the given room on the board.
    def find_room_position(self, room_name):
        for row_index, row in enumerate(self.clue_board):
            for col_index, cell in enumerate(row):
                if cell == room_name:
                    return (row_index, col_index)
        return None

    def draw_board(self):
        board_copy = [row[:] for row in self.clue_board]

        # Place characters on the board.
        for character, location in self.character_locations.items():
            coords = self.find_room_position(location)
            if coords:
                row, col = coords
                board_copy[row][col] = character

        # Print the board.
        for row in board_copy:
            print(" | ".join([str(cell) if cell else " " for cell in row]))
            print("-" * 35)

    def draw_detailed_board(self):
        """
        Draws a detailed representation of the Clue board.
        Returns a JSON-serializable structure of the board state.
        """
        # Define cell dimensions
        CELL_WIDTH = 15
        CELL_HEIGHT = 5  # Adjust as needed

        rows = len(self.clue_board)
        cols = len(self.clue_board[0])

        # Create a display grid as a list of lists to be JSON-serializable
        display_grid = []

        for row_index in range(rows):
            row_cells = []

            for col_index in range(cols):
                cell_content = []
                cell = self.clue_board[row_index][col_index]

                # Build cell content
                if cell is None:
                    # Fill empty spaces with a placeholder (e.g., 'X's or spaces)
                    cell_lines = ['X' * CELL_WIDTH for _ in range(CELL_HEIGHT)]
                elif cell.startswith('Hallway'):
                    # Hallway
                    # First line: Hallway name centered
                    cell_lines = [cell.center(CELL_WIDTH)]
                    # Remaining lines: Empty space
                    for _ in range(CELL_HEIGHT - 1):
                        cell_lines.append(' ' * CELL_WIDTH)
                else:
                    # Room
                    # First line: Room name centered
                    cell_lines = [cell.center(CELL_WIDTH)]
                    # Middle lines: Empty space
                    for _ in range(CELL_HEIGHT - 2):
                        cell_lines.append(' ' * CELL_WIDTH)
                    # Placeholder for player names
                    cell_lines.append(' ' * CELL_WIDTH)

                # Append cell content to the current row
                row_cells.append(cell_lines)

            # Append the row to the display grid
            display_grid.append(row_cells)

        # Place characters in their locations
        for character, location in self.character_locations.items():
            coords = self.find_room_position(location)
            if coords:
                row, col = coords
                cell_lines = display_grid[row][col]
                player_name = character  # Remove ANSI escape codes for JSON serialization

                # Place player name in the last line of the cell content
                cell_lines[-1] = player_name.center(CELL_WIDTH)

        # Convert display grid to a JSON-serializable format
        json_grid = [
            ['\n'.join(cell_lines) for cell_lines in row_cells] for row_cells in display_grid
        ]

        return json_grid
 
    def moveCharToRoom(self, character, new_room ):
        if character in self.character_locations:
            self.character_locations[character] = new_room
            print(f"{character} has moved to the {new_room}.")
        else:
            print(f"{character, new_room in self.character_locations.items()}")

    def getCharRoom(self, character):
        if character in self.character_locations:
            return self.character_locations[character]
        
        else:
            print(f"Character '{character}' not found.")
            return None

    def printCharLocations(self):
        print(self.character_locations)
        return