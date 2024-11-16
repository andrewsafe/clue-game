# main.py
from flask import Flask
from game_system.game_system import GameSystem
from game_system.turn_manager import TurnManager
from game_system.solution import Solution
from game_system.card import Card
from game_system.suggestion import Suggestion
from game_system.accusation import Accusation
from game_system.BoardManager import BoardManager
import random
import json

app = Flask(__name__)
game_system = GameSystem()
turn_manager = TurnManager(game_system.players)
board_manager = BoardManager()

#Add initial players for testing
game_system.add_player("Andrew", "Scarlett")
game_system.add_player("Justin", "Plum")
game_system.add_player("Elliot", "Mustard")

optionTable = """  
========================================================================
||......Characters.......||......Weapons......||........Rooms........||
||  1.) Colonel Mustard  ||  1.) Dagger       ||  1.) Hall           ||
||  2.) Professor Plum   ||  2.) Candlestick  ||  2.) Lounge         ||
||  3.) Reverend Green   ||  3.) Revolver     ||  3.) Library        ||
||  4.) Mrs. Peacock     ||  4.) Rope         ||  4.) Kitchen        ||
||  5.) Miss Scarlett    ||  5.) Lead Pipe    ||  5.) Billiard Room  ||
||  6.) Mrs. White       ||  6.) Wrench       ||  6.) Study          ||
||                       ||                   ||  7.) Ballroom       ||
||                       ||                   ||  8.) Dining Room    ||
||                       ||                   ||  9.) Conservatory   ||
========================================================================
"""

cards = [[
        Card("Colonel Mustard", "suspect"),
        Card("Professor Plum", "suspect"),
        Card("Reverend Green", "suspect"),
        Card("Mrs. Peacock ", "suspect"),
        Card("Miss Scarlett", "suspect"),
        Card("Mrs. White ", "suspect")
    ],
    [
        Card("Dagger", "weapon"),
        Card("Candlestick", "weapon"),
        Card("Revolver", "weapon"),
        Card("Rope", "weapon"),
        Card("Lead Pipe", "weapon"),
        Card("Wrench", "weapon")
    ],
    [
        Card("Hall", "room"),
        Card("Lounge", "room"),
        Card("Library", "room"),
        Card("Kitchen", "room"),
        Card("Billiard Room", "room"),
        Card("Study", "room"),
        Card("Ballroom", "room"),
        Card("Dining Room", "room"),
        Card("Conservatory", "room")    
    ]]

def displayMenu():
    """
    Display the menu options to the user.
    """
    print("----- Main Menu -----")
    print("1. Move player to an adjacent room or hallway")
    print("2. Make a suggestion")
    print("3. Make an accusation")

def createSolution(cards):
    # Create Solution for game
    character = cards[random.randint(0, 5)]
    weapon = cards[6 + random.randint(0, 5)]
    room = cards[12 + random.randint(0, 8)]
    print(f"Solution:  Character: {character}  Weapon: {weapon}  Room:  {room}") # ------------------------------------------------------------------
    solution = Solution(character, weapon, room)
    cards.remove(character)
    cards.remove(weapon)
    cards.remove(room)
    return solution

def main():
    # Create a GameSystem instance
    game = GameSystem()

    #create the board object
    board_manager = BoardManager()
    # Add players to the game
    game.add_player("Andrew", "Scarlett")
    game.add_player("Justin", "Plum")
    game.add_player("Elliot", "Mustard")

    # Make a few character's to Cycle: TODO Implement into game system, or somehow tie characters to player.
    characters_list = ["Scarlett", "Plum", "Green"]
    character_counter = 0

    # Create Solution and remove those cards from the deck
    solution = createSolution(game.cards)

    # Start the game
    game.start_game()
    # Initial Board Draw
    #board_manager.draw_detailed_board()

    # Create a TurnManager instance
    turn_manager = TurnManager(game.players)

    # Simulate a few turns
    for _ in range(len(game.players)):
        board_manager.print_JSON_board(board_manager.draw_detailed_board())
        current_player = turn_manager.current_player()
        print(f"It's {current_player.name} (" + characters_list[character_counter] + ")'s turn.")
        # Simulate some action (like making a suggestion or moving)
        # Display menu options and prompt player to choose an option
        displayMenu()

        action = input("Action (Enter number): ")

        if action == "1":
            #board_manager.draw_detailed_board()
            exit_flag = False

            if board_manager.check_if_valid_character_input(characters_list[character_counter]):
                possible_directions = board_manager.get_possible_moves(characters_list[character_counter])
            else:
                print("Invalid character selected: ")
                return

            #Start movement flagged loop
            while(exit_flag == False):
                input_direction = int(input("Move Option (Enter number): ")) - 1
                selected_move = possible_directions[input_direction]
                direction, destination_room = selected_move  # Unpack the tuple
                selected_move

                if input_direction >= 0 & input_direction < len(possible_directions):
                    board_manager.moveCharToRoom(characters_list[character_counter], destination_room)
                    board_manager.printCharLocations()
                    exit_flag = True
                else:
                    print("Move invalid!")
            #print updated board
            board_manager.print_JSON_board(board_manager.draw_detailed_board())

            
        # Make a Suggestion
        elif action == "2":
            print(optionTable)
            print("Select a character, weapon, and room from the options above (number).")
            character = int(input("Character: ")) - 1
            weapon = int(input("Weapon: ")) - 1
            room = int(input("Room: ")) - 1
            suggestion = Suggestion(cards[0][character], cards[1][weapon], cards[2][room])

            for player in game.players:
                incorrect_cards = suggestion.checkSuggestion(player.cards)
                if incorrect_cards != []:
                    for i in range(len(incorrect_cards)):
                        print(f"{i + 1}:  Card: {incorrect_cards[i].name}  Category: {incorrect_cards[i].category}")
                    print("Select the card you wish to reveal is incorrect (number).")
                    card = int(input("Card: ")) - 1
                    print(f"Card: {incorrect_cards[card].name}  Category: {incorrect_cards[card].category} is incorrect.")
                    break
        
        # Make an Accusation
        elif action == "3":
            print(optionTable)
            print("Select a character, weapon, and room from the options above (number).")
            character = int(input("Character: ")) - 1
            weapon = int(input("Weapon: ")) - 1
            room = int(input("Room: ")) - 1
            accusation = Accusation(cards[0][character], cards[1][weapon], cards[2][room])

            # Checks if accusation is correct
            if accusation.checkAccusation(solution):
                print(f"Player {current_player.name} has won the game.")
                break
            else:
                print(f"Player {current_player.name} has made an incorrect accusation.")
        
        else:
            print("Invalid option selected.")

        print(f"{current_player.name}'s cards: {current_player.show_cards()}")

        # Advance to next character TODO Increment/tie character to Player together.
        character_counter += 1
        if character_counter > 2:
            character_counter = 0

        # Advance to the next player's turn
        turn_manager.next_turn()

    # Reset turns and show the current player again
    turn_manager.reset_turns()
    print(turn_manager)  # Output: Current turn: Alice

if __name__ == "__main__":
    main()
    app.run(debug=True)
