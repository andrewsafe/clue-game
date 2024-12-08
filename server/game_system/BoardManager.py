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
            "Miss Scarlett": "Hallway2",
            "Professor Plum": "Hallway3",
            "Colonel Mustard": "Hallway5",
            "Mrs. Peacock": "Hallway8",
            "Reverend Green": "Hallway11",
            "Mrs. White": "Hallway12"
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
            ["Study", "Hallway1", "Hall", "Hallway2", "Lounge"],
            ["Hallway3", None, "Hallway4", None, "Hallway5"],
            ["Library", "Hallway6", "Billiard Room", "Hallway7", "Dining Room"],
            ["Hallway8", None, "Hallway9", None, "Hallway10"],
            ["Conservatory", "Hallway11", "Ballroom", "Hallway12", "Kitchen"]
            ]

        self._initialized = True


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
        # Find the current room of the player
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
                    if self.is_hall_occupied(destination) == False:
                        directions.append((direction, destination))
                    

        # Add secret passages if applicable
        secret_passages = {
            'Study': 'Kitchen',
            'Kitchen': 'Study',
            'Lounge': 'Conservatory',
            'Conservatory': 'Lounge'
        }

        if room_name in secret_passages:
            destination = secret_passages[room_name]
            directions.append(('Secret Passage', destination))

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
        Returns a JSON-serializable structure of the board state.
        Instead of ASCII art, we provide a structured JSON:
        [
        [
            { "type": "room", "name": "Study", "characters": ["Miss Scarlett"] },
            { "type": "hallway", "name": "Hallway1", "characters": [] },
            ...
        ],
        ...
        ]
        """

        rows = len(self.clue_board)
        cols = len(self.clue_board[0])

        # Create a dictionary to track which characters are in each cell
        cell_characters = {(r, c): [] for r in range(rows) for c in range(cols)}

        # Fill cell_characters based on character_locations
        for character, location in self.character_locations.items():
            coords = self.find_room_position(location)
            if coords:
                cell_characters[coords].append(character)

        json_grid = []
        for r in range(rows):
            row_cells = []
            for c in range(cols):
                cell = self.clue_board[r][c]
                cell_data = {
                    "type": None,
                    "name": None,
                    "characters": cell_characters[(r, c)]
                }

                if cell is None:
                    # Blocked or empty space
                    cell_data["type"] = "blocked"
                elif cell.startswith('Hallway'):
                    # Hallway cell
                    cell_data["type"] = "hallway"
                    cell_data["name"] = cell
                else:
                    # Room cell
                    cell_data["type"] = "room"
                    cell_data["name"] = cell

                row_cells.append(cell_data)
            json_grid.append(row_cells)

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

    #Check room against all characters and return if occupied or not.
    def is_hall_occupied(self, room_name):
        # Iterate through all character locations
        for character, location in self.character_locations.items():
            if "Hallway" in location:
                if location == room_name:
                    print("Room is currently occupied by" + character)
                    return True
        return False
    
    def print_JSON_board(self, json_grid):
        # Determine the number of lines per cell (CELL_HEIGHT)
        CELL_HEIGHT = 5  # Must match the value in draw_detailed_board()
        # Iterate through each row in the grid
        for row in json_grid:
            # Initialize a list to hold each line of the row
            row_lines = ['' for _ in range(CELL_HEIGHT)]
            
            # Iterate through each cell in the row
            for cell in row:
                cell_lines = cell.split('\n')
                for i in range(CELL_HEIGHT):
                    row_lines[i] += cell_lines[i].ljust(15) + ' | '  # Adjust padding as needed
            
            # Print each line of the row
            for line in row_lines:
                print(line)
            
            # Print a separator after each row
            print('-' * (len(row) * (15 + 3)))  # 15 for CELL_WIDTH, 3 for ' | '