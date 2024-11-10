#room dictionary, holds player locations.

class Board:
  _instance = None
  _initialized = False

  def __new__(cls):
      if cls._instance is None:
          cls._instance = super(Board, cls).__new__(cls)
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

            self.board_grid = [
            ["Study", "Hallway2", "Hall", "Hallway4", "Lounge"],
            ["Hallway6", None, "Hallway8", None, "Hallway10"],
            ["Library", "Hallway12", "Billiard Room", "Hallway14", "Dining Room"],
            ["Hallway16", None, "Hallway18", None, "Hallway20"],
            ["Conservatory", "Hallway21", "Ballroom", "Hallway23", "Kitchen"]
            ]

      
  #Update character to be in specific room.
  def moveCharToRoom(self, character, new_room ):
    if character in self.character_locations:
      self.character_locations[character] = new_room
      print(f"{character} has moved to the {new_room}.")
    else:
      print(f"{character, new_room in self.character_locations.items()}")

  #Get the value at a specific row and column on the board.
  def moveWeaponToRoom(self, weapon, new_room ):
    if weapon in self.weapon_locations:
      self.weapon_locations[weapon] = new_room
      print(f"{weapon} has moved to the {new_room}.")
    else:
      print(f"{weapon, new_room in self.character_locations.items()}")

  # Check if Character's move to specific locatin is valid
  def is_valid_move(self, character, desired_location):
    if character not in self.character_locations:
      return False
    
    current_location = self.character_locations[character]
    current_coords = self.get_coordinates(current_location)
    desired_coords = self.get_coordinates(desired_location)

    if not current_coords or not desired_coords:
      return False

    current_row, current_col = current_coords
    desired_row, desired_col = desired_coords

    # Check if the desired location is adjacent to the current location
    row_diff = abs(current_row - desired_row)
    col_diff = abs(current_col - desired_col)

    # A valid move is either one step vertically or horizontally to a connected room/hallway
    if (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1):
    # Check if the desired location is not None (i.e., it's a valid room or hallway)
      if self.board[desired_row][desired_col] is not None:
          return True
        
  def draw_detailed_board(self, character):
        """
        Draws a detailed text-based map of the Clue board.
        Displays room names at the top of each room cell (excluding hallways),
        fills empty spaces with placeholders, and shows players in their current
        locations with their names in purple.
        """
        # ANSI escape code for purple (bright magenta)
        PURPLE = '\033[95m'
        RESET = '\033[0m'

        rows = len(self.board_grid)
        cols = len(self.board_grid[0])

        # Define cell dimensions
        CELL_WIDTH = 15
        CELL_HEIGHT = 5  # Adjust as needed

        # Build a display grid
        display_grid = []

        for row_index in range(rows):
            row_cells = []

            for col_index in range(cols):
                cell_content = []
                cell = self.board_grid[row_index][col_index]

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

                row_cells.append(cell_lines)

            display_grid.append(row_cells)

        # Place characters in their locations
        for character, location in self.character_locations.items():
            coords = self.find_room_position(location)
            if coords:
                row, col = coords
                cell_lines = display_grid[row][col]
                player_name = PURPLE + character + RESET

                # Place player name in the last line of the cell content
                cell_lines[-1] = player_name.center(CELL_WIDTH)

        # Print the display grid
        total_width = cols * (CELL_WIDTH + 3) - 3  # Adjust for separators
        print("\n" + "=" * total_width)
        for row_index, row_cells in enumerate(display_grid):
            # For each line in the cell height
            for line_index in range(CELL_HEIGHT):
                row_line = ''
                for cell_lines in row_cells:
                    row_line += cell_lines[line_index] + ' | '
                print(row_line.rstrip(' | '))
            if row_index < len(display_grid) - 1:
                # Print separator between rows
                print("-" * total_width)
        print("=" * total_width + "\n")

#get the coordinates of a specifc room.
  def get_coordinates(self, location):
    """Get the row and column coordinates of a given location."""
    for row in range(len(self.clue_board)):
        for col in range(len(self.clue_board[row])):
            if self.clue_board[row][col] == location:
                return row, col
    return None
  
  #Get the room at a specific row and column on the board.
  def get_location(self, row, col):
    if 0 <= row < len(self.clue_board) and 0 <= col < len(self.clue_board[0]):
        return self.clue_board[row][col]
    else:
        return "Invalid location"
          
