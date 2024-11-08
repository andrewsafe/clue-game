#room dictionary, holds player locations.

class board:

  def __init__(self):
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
        
  def get_coordinates(self, location):
    """Get the row and column coordinates of a given location."""
    for row in range(len(self.clue_board)):
        for col in range(len(self.clue_board[row])):
            if self.clue_board[row][col] == location:
                return row, col
    return None
  
  #Get the value at a specific row and column on the board.
  def get_location(self, row, col):
    if 0 <= row < len(self.clue_board) and 0 <= col < len(self.clue_board[0]):
        return self.clue_board[row][col]
    else:
        return "Invalid location"
        
