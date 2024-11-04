from game_system.suggestion import Suggestion
from game_system.accusation import Accusation
from game_system.player import Player
from game_system.solution import Solution

#for future use/reference (text based GUI)

optionTable = """  
========================================================================
||......Characters.......||......Weapons......||........Rooms........||
||  1.) Colonel Mustard  ||  1.) Dagger       ||  1.) Hall           ||
||  2.) Professor Plum   ||  2.) Candlestick  ||  2.) Lounge         ||
||  3.) Reverend Green   ||  3.) Revolver     ||  3.) Library        ||
||  4.) Mrs. Peacock     ||  4.) Rope         ||  4.) Kitchen        ||
||  5.) Miss Scarlett    ||  5.) Lead piping  ||  5.) Billiard Room  ||
||  6.) Mrs. White       ||  6.) Spanner      ||  6.) Study          ||
||                       ||                   ||  7.) Ballroom       ||
||                       ||                   ||  8.) Dining Room    ||
||                       ||                   ||  9.) Conservatory   ||
========================================================================
"""

cards = [
    ["Colonel Mustard", "Professor Plum", "Reverend Green", "Mrs. Peacock", "Mrs. White", "Miss Scarlett"],
    ["Dagger", "Candlestick", "Revolver", "Rope", "Lead piping", "Spanner"], 
    ["Hall", "Study", "Billiard Room", "Lounge", "Library", "Kitchen"]
]

characters = {1: "Colonel Mustard", 2: "Professor Plum", 3: "Reverend Green", 4: "Mrs. Peacock", 5: "Miss Scarlett", 6: "Mrs. White"}
weapons = {1: "Dagger", 2: "Candlestick", 3: "Revolver", 4: "Rope", 5: "Lead piping", 6: "Spanner"}
rooms = {1: "Hall", 2: "Lounge", 3: "Library", 4: "Kitchen", 5: "Billiard Room", 6: "Study", 7: "Ballroom", 8: "Dining Room", 9: "Conservatory"}

players = []

def setup():
    return 0

    def distributeCards():
        # Logic to distribute cards to players can go here.
        pass

    def displayMenu():
        """
        Display the menu options to the user.
        """
        print("----- Main Menu -----")
        print("1. Move player to an adjacent room or hallway")
        print("2. Make a suggestion")
        print("3. Make an accusation")

    def playerTurn(player: Player):
        displayMenu()

    action = input("Action (Enter number): ")

    if action == "1":
        # Logic to move player to a new room/hallway goes here.
        print("Player is moving.")
        pass  # Replace with actual implementation

    elif action == "2":
        print(optionTable)
        print("Select a character, weapon, and room from the options above (number).")
        character = int(input("Character: "))
        weapon = int(input("Weapon: "))
        room = int(input("Room: "))
        suggestion = Suggestion(characters[character], weapons[weapon], rooms[room])

        for player in players:
            suggestion.checkSuggestion(player.cards)

    elif action == "3":
        print(optionTable)
        print("Select a character, weapon, and room from the options above (number).")
        character = int(input("Character: "))
        weapon = int(input("Weapon: "))
        room = int(input("Room: "))
        accusation = Accusation(characters[character], weapons[weapon], rooms[room])

        # Assuming you have a `solution` object available for the game
        if accusation.checkAccusation(solution):
            print(f"Player {player.username} has won the game.")
        else:
            print(f"Player {player.username} has made an incorrect accusation.")

    else:
        print("Invalid input for action")