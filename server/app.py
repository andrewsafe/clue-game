import random
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from game_system.game_system import GameSystem
from game_system.turn_manager import TurnManager
from game_system.solution import Solution
from game_system.card import Card
from game_system.suggestion import Suggestion
from game_system.accusation import Accusation
from game_system.BoardManager import BoardManager

app = Flask(__name__)
CORS(app)
game_system = GameSystem()
turn_manager = TurnManager(game_system.players)
board_manager = BoardManager()

# Add initial players for testing, using standardized character names
game_system.add_player("Andrew", "Mustard", "Hall")
game_system.add_player("Justin", "Plum", "Lounge")
game_system.add_player("Elliot", "Peacock", "Library")



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


option_table = """  
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

def createSolution():
    # Create Solution for game
    character = game_system.cards[random.randint(0, 5)]
    weapon = game_system.cards[6 + random.randint(0, 5)]
    room = game_system.cards[12 + random.randint(0, 8)]
    print(f"Solution:  Character: {character}  Weapon: {weapon}  Room:  {room}")
    game_system.cards.remove(character)
    game_system.cards.remove(weapon)
    game_system.cards.remove(room)
    return Solution(character, weapon, room)

solution = createSolution()

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route('/detailed-board', methods=['GET'])
def get_detailed_board():
    board_state = board_manager.draw_detailed_board()
    return jsonify(board_state)
    
@app.route('/api/optionTable', methods=['GET'])
def get_option_table():
    return jsonify({"optionTable" : option_table})

@app.route('/api/players/add', methods=['POST'])
def add_player():
    data = request.json
    print(f"Received data: {data}")  # Debugging line

    player_name = data.get("playerName")
    character = data.get("character")  # Get character from request body

    if not player_name or not character:
        return jsonify({"error": "Player name and character are required"}), 400

    # Check if the player already exists by name
    if player_name in [player.name for player in game_system.players]:
        return jsonify({"error": f"{player_name} already exists"}), 400

    # Add player with name and character
    message = game_system.add_player(player_name, character)
    print(f"{player_name} added to the game as {character}.")
    return jsonify({"message": message}), 200

@app.route('/api/players', methods=['GET'])
def get_players():
    """
    API endpoint to return player information and their assigned cards.
    """

    players_info = []
    for player in game_system.players:
        player_cards = [card.to_dict() for card in player.cards]  # Assuming cards have a to_dict() method
        players_info.append({
            "id": player.id,
            "name": player.name,
            "cards": player_cards
        })
    
    return jsonify({"players": players_info}), 200


@app.route('/api/players/turn', methods=['POST'])
def player_turn():
    data = request.json
    action = data.get("action")  # Either "start" or "end"
    player_id = data.get("playerId")

    if not action or not player_id:
        return jsonify({"error": "Missing action or playerId"}), 400

    print(f"Player {player_id} is trying to {action} their turn.")

    if action == "start":
        message = game_system.start_turn(player_id)
        print(f"Turn started for Player {player_id}.")
        return jsonify({"message": message}), 200
    elif action == "end":
        game_system.counter = game_system.counter + 1 if game_system.counter + 1 < len(game_system.players) else 0
        next_player = game_system.players[game_system.counter].name
        print(f"Turn ended for Player {player_id}. Next player: {next_player}. Counter: {game_system.counter}")
        return jsonify({"message": f"Turn ended. Next player: {next_player}"}), 200
    else:
        return jsonify({"error": "Invalid action"}), 400
    
@app.route('/api/players/move-options', methods=['GET'])
def get_move_options():
    try:
        player_id = request.args.get("playerId")
        print(f"Received player_id: {player_id}")

        if not player_id:
            return jsonify({"error": "Missing playerId"}), 400

        # Find the player object in GameSystem
        player = next((p for p in game_system.players if p.name == player_id), None)
        if not player:
            return jsonify({"error": "Player not found"}), 404

        # Retrieve the player's character and current location
        player_character = player.character
        print(f"Player character found: {player_character}")

        # Get current location of the player on the board
        current_location = board_manager.character_locations.get(player_character)
        if not current_location:
            return jsonify({"error": "Player's current location not found"}), 404
        print(f"Player's current location: {current_location}")

        # Get possible moves using `get_possible_moves`
        directions = board_manager.get_possible_moves(player_character)
        print(f"Possible directions: {directions}")

        # Format the response with current location and options
        formatted_directions = [{"direction": d[0], "destination": d[1]} for d in directions]
        response = {
            "currentLocation": current_location,
            "options": formatted_directions
        }

        return jsonify(response), 200

    except ValueError as ve:
        print(f"Error: {ve}")
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/api/players/suggestion', methods=['POST'])
def player_suggestion():
    data = request.json
    player_id = data.get("playerId")
    suggestion_data = data.get("suggestion")

    print(f"{player_id} made a suggestion: {suggestion_data}.")

    # Ensure the values are integers
    character_index = int(suggestion_data['character'])
    weapon_index = int(suggestion_data['weapon'])
    room_index = int(suggestion_data['room'])

    suggestion = Suggestion(
        cards[0][character_index - 1],
        cards[1][weapon_index - 1],
        cards[2][room_index - 1]
    )

    message = game_system.make_suggestion(player_id, suggestion)
    print(f"Suggestion processed for {player_id}.")
    return jsonify({"message": message}), 200


@app.route('/api/players/accusation', methods=['POST'])
def player_accusation():
    data = request.json
    player_id = data.get("playerId")
    accusation_data = data.get("accusation")

    print(f"{player_id} made an accusation: {accusation_data}.")

    character_index = int(accusation_data['character'])
    weapon_index = int(accusation_data['weapon'])
    room_index = int(accusation_data['room'])

    accusation = Accusation(
        cards[0][character_index - 1],
        cards[1][weapon_index - 1],
        cards[2][room_index - 1]
    )

    #result = game_system.check_accusation(player_id, accusation)
    result = accusation.checkAccusation(solution)
    if result:
        print(f"{player_id} has won the game.")
        return jsonify({"message": f"Correct accusation. {player_id} wins!"}), 200
    else:
        print(f"{player_id} made an incorrect accusation.")
        return jsonify({"message": "Incorrect accusation."}), 200
    
@app.route('/start-game', methods=['POST'])
def start_game_api():
    try:
        game_system.start_game()
        response = {
            'status': 'success',
            'message': 'Game started successfully. Cards have been distributed and shown to players.'
        }
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }

    return jsonify(response)
    
if __name__ == "__main__":
    app.run(debug=True)