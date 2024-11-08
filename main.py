# main.py
from flask import Flask, request, jsonify
from game_system.game_system import GameSystem
from game_system.turn_manager import TurnManager
from game_system.solution import Solution
from game_system.card import Card
from game_system.suggestion import Suggestion
from game_system.accusation import Accusation
from game_system.BoardManager import BoardManager
import random

app = Flask(__name__)
game_system = GameSystem()
turn_manager = TurnManager(game_system.players)
board_manager = BoardManager()

# Add initial players for testing
game_system.add_player("player1")
game_system.add_player("player2")
game_system.add_player("player3")

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

@app.route('/api/players/turn', methods=['POST'])
def player_turn():
    data = request.json
    action = data.get("action")
    player_id = data.get("playerId")

    print(f"Player {player_id} is trying to {action} their turn.")

    if action == "start":
        message = game_system.start_turn(player_id)
        print(f"Turn started for Player {player_id}.")
        return jsonify({"message": message}), 200
    elif action == "end":
        next_player = game_system.end_turn(player_id)
        print(f"Turn ended for Player {player_id}. Next player: {next_player}.")
        return jsonify({"message": f"Turn ended. Next player: {next_player}"}), 200
    else:
        print(f"Invalid action: {action} for Player {player_id}.")
        return jsonify({"error": "Invalid action"}), 400

@app.route('/api/players/move', methods=['POST'])
def player_move():
    data = request.json
    player_id = data.get("playerId")
    destination = data.get("destination")

    print(f"Player {player_id} is moving to {destination}.")

    message = game_system.move_player(player_id, destination)
    print(f"Player {player_id} moved to {destination}.")
    return jsonify({"message": message}), 200

@app.route('/api/players/suggestion', methods=['POST'])
def player_suggestion():
    data = request.json
    player_id = data.get("playerId")
    suggestion_data = data.get("suggestion")

    print(f"Player {player_id} made a suggestion: {suggestion_data}.")

    suggestion = Suggestion(
        cards[0][suggestion_data['character'] - 1],
        cards[1][suggestion_data['weapon'] - 1],
        cards[2][suggestion_data['room'] - 1]
    )

    message = game_system.make_suggestion(player_id, suggestion)
    print(f"Suggestion processed for Player {player_id}.")
    return jsonify({"message": message}), 200

@app.route('/api/players/accusation', methods=['POST'])
def player_accusation():
    data = request.json
    player_id = data.get("playerId")
    accusation_data = data.get("accusation")

    print(f"Player {player_id} made an accusation: {accusation_data}.")

    accusation = Accusation(
        cards[0][accusation_data['character'] - 1],
        cards[1][accusation_data['weapon'] - 1],
        cards[2][accusation_data['room'] - 1]
    )

    result = game_system.check_accusation(player_id, accusation)
    if result:
        print(f"Player {player_id} has won the game.")
        return jsonify({"message": "Correct accusation. Player wins!"}), 200
    else:
        print(f"Player {player_id} made an incorrect accusation.")
        return jsonify({"message": "Incorrect accusation."}), 200

def displayMenu():
    """
    Display the menu options to the user.
    """
    print("----- Main Menu -----")
    print("1. Move player to an adjacent room or hallway")
    print("2. Make a suggestion")
    print("3. Make an accusation")

if __name__ == "__main__":
    app.run(debug=True)
