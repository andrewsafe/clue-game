from game_system.game_system import GameSystem
from game_system.turn_manager import TurnManager
from game import Game
from game_system.solution import Solution
from game_system.card import Card
from game_system.suggestion import Suggestion
from game_system.accusation import Accusation
import random

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
    solution = Solution(character, weapon, room)
    cards.remove(character)
    cards.remove(weapon)
    cards.remove(room)
    return solution

def main():
    # Create a GameSystem instance
    game = GameSystem()

    # Add players to the game
    game.add_player("Andrew")
    game.add_player("Justin")
    game.add_player("Elliot")


    # Create Solution and remove those cards from the deck
    solution = createSolution(game.cards)

    # Start the game
    game.start_game()

    # Create a TurnManager instance
    turn_manager = TurnManager(game.players)

    # Simulate a few turns
    for _ in range(len(game.players)):
        current_player = turn_manager.current_player()
        print(f"It's {current_player.name}'s turn.")
        # Simulate some action (like making a suggestion or moving)
        # Display menu options and prompt player to choose an option
        displayMenu()

        action = input("Action (Enter number): ")

        if action == "1":
            # Logic to move player to a new room/hallway goes here.
            print("Player is moving.")
            pass  # Replace with actual implementation
        
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
            else:
                print(f"Player {current_player.name} has made an incorrect accusation.")
        
        else:
            print("Invalid option selected.")

        print(f"{current_player.name}'s cards: {current_player.show_cards()}")

        # Advance to the next player's turn
        turn_manager.next_turn()

    # Reset turns and show the current player again
    turn_manager.reset_turns()
    print(turn_manager)  # Output: Current turn: Alice

if __name__ == "__main__":
    main()
