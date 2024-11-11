from flask import Flask, request, jsonify
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

#Add initial players for testing
game_system.add_player("Andrew")
game_system.add_player("Justin")
game_system.add_player("Elliot")

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

@app.route('/detailed-board', methods=['GET'])
def get_detailed_board():
    board_state = board_manager.draw_detailed_board()
    return jsonify(board_state)
    

@app.route('/api/players/add', methods=['POST'])
def add_player():
    data = request.json
    print(f"Received data: {data}")  # Debugging line
    player_name = data.get("playerName")
    print(f"Player name extracted: {player_name}")  # Debugging line

    if not player_name:
        return jsonify({"error": "Player name is required"}), 400

    if player_name in [player.name for player in game_system.players]:
        return jsonify({"error": f"{player_name} already exists"}), 400

    game_system.add_player(player_name)
    print(f"{player_name} added to the game.")
    return jsonify({"message": f"{player_name} added successfully"}), 200


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
        next_player = game_system.end_turn(player_id)
        print(f"Turn ended for Player {player_id}. Next player: {next_player}.")
        return jsonify({"message": f"Turn ended. Next player: {next_player}"}), 200
    else:
        return jsonify({"error": "Invalid action"}), 400

@app.route('/api/players/move', methods=['POST'])
def player_move():
    try:
        data = request.json
        player_id = data.get("playerId")
        destination = data.get("destination")

        if not player_id or not destination:
            return jsonify({"error": "Missing playerId or destination"}), 400

        print(f"{player_id} is moving to {destination}.")

        # Call the `move_player` method from `game_system`
        message = game_system.move_player(player_id, destination)
        print(f"{player_id} moved to {destination}.")

        # Include a flag in the response to indicate the move was successful and buttons should be shown
        response = {
            "message": message,
            "showMoveButtons": True  # New field for the frontend to check
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

    result = game_system.check_accusation(player_id, accusation)
    if result:
        print(f"{player_id} has won the game.")
        return jsonify({"message": "Correct accusation. {player_id} wins!"}), 200
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