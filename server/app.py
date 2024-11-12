import random
import json
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from game_system.game_system import GameSystem
from game_system.turn_manager import TurnManager
from game_system.solution import Solution
from game_system.card import Card
from game_system.suggestion import Suggestion
from game_system.accusation import Accusation
from game_system.BoardManager import BoardManager

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
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
    c_index = random.randint(0, 5)
    w_index = 6 + random.randint(0, 5)
    r_index = 12 + random.randint(0, 8)
    character = game_system.cards[c_index]
    weapon = game_system.cards[w_index]
    room = game_system.cards[r_index]
    print(f"Solution:  Character: {c_index + 1} {character}  Weapon: {w_index - 5} {weapon}  Room: {r_index - 11} {room}")
    game_system.cards.remove(character)
    game_system.cards.remove(weapon)
    game_system.cards.remove(room)
    return Solution(character, weapon, room)

solution = createSolution()

# --------------------------------------------------------------------
@app.before_request 
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()
# --------------------------------------------------------------------

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    send("Welcome to the WebSocket server!")  # Sends a welcome message to the client upon connection

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('detailed_board')
def detailed_board(data=None):
    try:
        board_state = board_manager.draw_detailed_board()
        emit('detailed_board_response', board_state)
    except Exception as e:
        emit('detailed_board_response', {"error": str(e)})
    
# --------------------------------------------------------------------
@app.route('/api/optionTable', methods=['GET'])
def get_option_table():
    return jsonify({"optionTable" : option_table})
# --------------------------------------------------------------------

@socketio.on('add_player')
def add_player(data):
    # Debugging: log received data
    print(f"Received data: {data}")

    # Parse data as JSON if it is a string
    if isinstance(data, str):
        data = json.loads(data)

    player_name = data.get("playerName")
    character = data.get("character")

    # Check if player name and character are provided
    if not player_name or not character:
        emit('add_player_response', {"error": "Player name and character are required"})
        return

    # Check if the player already exists by name
    if player_name in [player.name for player in game_system.players]:
        emit('add_player_response', {"error": f"{player_name} already exists"})
        return

    # Add player with name and character
    message = game_system.add_player(player_name, character)
    print(f"{player_name} added to the game as {character}.")
    emit('add_player_response', {"message": message})

@socketio.on('get_players')
def get_players():
    """
    WebSocket event to return player information and their assigned cards.
    """
    players_info = []
    for player in game_system.players:
        player_cards = [card.to_dict() for card in player.cards]  # Assuming cards have a to_dict() method
        players_info.append({
            "id": player.id,
            "name": player.name,
            "cards": player_cards
        })
    
    # Emit the player information back to the client
    emit('get_players_response', {"players": players_info})

@socketio.on('get_current_player')
def get_current_player(data=None):  # Add 'data' as a default argument
    """
    WebSocket event to return current player information.
    """
    try:
        name = game_system.players[game_system.counter].name
        emit('get_current_player_response', {"current_player": name})
    except IndexError:
        emit('get_current_player_response', {"error": "No current player found"})

@socketio.on('player_turn')
def player_turn(data):
    # Parse data as JSON if it is a string
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            emit('player_turn_response', {"error": "Invalid JSON format"})
            return

    action = data.get("action")  # Either "start" or "end"
    player_id = game_system.active_players[game_system.counter].name
    gameOver = False

    if not action or not player_id:
        emit('player_turn_response', {"error": "Missing action or playerId"})
        return

    print(f"Player {player_id} is trying to {action} their turn.")

    if action == "start":
        message = game_system.start_turn(player_id)
        if len(game_system.active_players) == 1:
            message = f"Player {player_id} wins by default."
            gameOver = True
        print(f"Turn started for Player {player_id}.")
        emit('player_turn_response', {"message": message, "gameOver": gameOver})
    elif action == "end":
        if len(game_system.active_players) == 0:
            emit('player_turn_response', {"error": "No active players in the game.", "gameOver": True})
            return

        game_system.counter = game_system.counter + 1 if game_system.counter + 1 < len(game_system.active_players) else 0
        next_player = game_system.active_players[game_system.counter].name
        print(f"Turn ended for Player {player_id}. Next player: {next_player}. Counter: {game_system.counter}")
        emit('player_turn_response', {"message": f"Turn ended. Next player: {next_player}", "gameOver": gameOver})
    else:
        emit('player_turn_response', {"error": "Invalid action"})
    
@socketio.on('get_move_options')
def get_move_options():  # Add 'data' as a placeholder argument
    try:
        # Retrieve the current player's ID
        player_id = game_system.players[game_system.counter].name
        print(f"Received player_id: {player_id}")

        if not player_id:
            emit('move_options_response', {"error": "Missing playerId"})
            return

        # Find the player object in GameSystem
        player = next((p for p in game_system.players if p.name == player_id), None)
        if not player:
            emit('move_options_response', {"error": "Player not found"})
            return

        # Retrieve the player's character and current location
        player_character = player.character
        print(f"Player character found: {player_character}")

        # Get current location of the player on the board
        current_location = board_manager.character_locations.get(player_character)
        if not current_location:
            emit('move_options_response', {"error": "Player's current location not found"})
            return
        print(f"Player's current location: {current_location}")

        # Get possible moves using `get_possible_moves`
        directions = board_manager.get_possible_moves(player_character)
        print(f"Possible directions: {directions}")

        # Format the response with current location and options
        formatted_directions = [{"index": i, "direction": directions[0], "destination": directions[1]} for i in range(len(directions))]
        response = {
            "currentLocation": current_location,
            "options": formatted_directions
        }

        emit('move_options_response', response)

    except ValueError as ve:
        print(f"Error: {ve}")
        emit('move_options_response', {"error": str(ve)})
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        emit('move_options_response', {"error": "An unexpected error occurred"})


@socketio.on('move_character')
def handle_move_character(data):

    character = data.get('character')
    new_room = data.get('new_room')

    if not character or not new_room:
        emit('move_character_response', {
            'status': 'error',
            'message': 'Invalid data. "character" and "new_room" are required.'
        })
        return
    
    board_manager.moveCharToRoom(character, new_room)
    updated_board = board_manager.draw_detailed_board()
    emit('move_character_response', updated_board)

# def is_room_occupied(self, room_name):
#     # List to keep track of characters in the room
#     occupants = []
#     # Iterate through all character locations
#     for character, location in self.character_locations.items():
#         if location == room_name:
#             occupants.append(character)
#     if occupants:
#         occupants_str = ', '.join(occupants)
#         message = f"Room '{room_name}' is currently occupied by: {occupants_str}."
#         logging.info(message)
#         return {'status': 'occupied', 'message': message, 'occupants': occupants}
#     else:
#         message = f"Room '{room_name}' is not occupied."
#         logging.info(message)
#         return {'status': 'unoccupied', 'message': message, 'occupants': []}


@socketio.on('player_suggestion')
def player_suggestion(data):
    # Parse data as JSON if it is a string
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            emit('player_suggestion_response', {"error": "Invalid JSON format"})
            return

    player_id = game_system.active_players[game_system.counter].name
    suggestion_data = data.get("suggestion")

    print(f"{player_id} made a suggestion: {suggestion_data}.")

    # Ensure the values are integers
    try:
        character_index = int(suggestion_data['character'])
        weapon_index = int(suggestion_data['weapon'])
        room_index = int(suggestion_data['room'])
    except (ValueError, KeyError, TypeError) as e:
        print("Error parsing suggestion data:", e)
        emit('player_suggestion_response', {"error": "Invalid suggestion data"})
        return

    suggestion = Suggestion(
        cards[0][character_index - 1],
        cards[1][weapon_index - 1],
        cards[2][room_index - 1]
    )

    message = ""
    for player in game_system.players:
        incorrect_cards = suggestion.checkSuggestion(player.cards)
        if incorrect_cards:
            incorrect_card = incorrect_cards[random.randint(0, len(incorrect_cards) - 1)]
            message = f"Incorrect {incorrect_card.category} suggested. Card: {incorrect_card.name}."
            break
    if message == "":
        message = f"Suggestion with Suspect: {suggestion.character}, Weapon: {suggestion.weapon}, Room: {suggestion.room} is correct."
    print(f"Suggestion processed for {player_id}.")
    emit('player_suggestion_response', {"message": message})

@socketio.on('player_accusation')
def player_accusation(data):
    # Parse data as JSON if it is a string
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            emit('player_accusation_response', {"error": "Invalid JSON format"})
            return

    player_id = game_system.active_players[game_system.counter].name
    accusation_data = data.get("accusation")

    print(f"{player_id} made an accusation: {accusation_data}.")

    # Ensure the values are integers
    try:
        character_index = int(accusation_data['character'])
        weapon_index = int(accusation_data['weapon'])
        room_index = int(accusation_data['room'])
    except (ValueError, KeyError, TypeError) as e:
        print("Error parsing accusation data:", e)
        emit('player_accusation_response', {"error": "Invalid accusation data"})
        return

    accusation = Accusation(
        cards[0][character_index - 1],
        cards[1][weapon_index - 1],
        cards[2][room_index - 1]
    )

    result = accusation.checkAccusation(solution)

    if result:
        print(f"{player_id} has won the game.")
        emit('player_accusation_response', {"message": f"Correct accusation. {player_id} wins!", "gameOver": True})
    else:
        # Remove the player from active players
        game_system.active_players.pop(game_system.counter)
        game_system.counter -= 1
        print(f"{player_id} made an incorrect accusation and has been removed from the game.")
        emit('player_accusation_response', {
            "message": f"{player_id} made an incorrect accusation and has lost.",
            "gameOver": False
        })

@socketio.on('start_game')
def start_game_api(data=None):  # Add 'data' as a placeholder argument
    try:
        # Attempt to start the game
        game_system.start_game()
        game_system.active_players = game_system.players.copy()
        # Emit a success response
        emit('start_game_response', {
            'status': 'success',
            'message': 'Game started successfully. Cards have been distributed and shown to players.'
        })
    except Exception as e:
        # Emit an error response if an exception occurs
        emit('start_game_response', {
            'status': 'error',
            'message': str(e)
        })
    
if __name__ == "__main__":
    app.run(debug=True)