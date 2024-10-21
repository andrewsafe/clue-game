from flask import Flask, request, jsonify
from game import Game

app = Flask(__name__)
game = Game()  # Create an instance of the Game class

@app.route('/api/players/turn', methods=['POST'])
def player_turn():
    data = request.json
    action = data.get("action")
    player_id = data.get("playerId")
    
    # Log the request action
    print(f"Player {player_id} is trying to {action} their turn.")

    if action == "start":
        message = game.start_turn(player_id)
        print(f"Turn started for Player {player_id}.")
        return jsonify({"message": message}), 200
    elif action == "end":
        next_player = game.end_turn(player_id)
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
    
    # Log the movement request
    print(f"Player {player_id} is moving to {destination}.")

    message = game.move_player(player_id, destination)
    print(f"Player {player_id} moved to {destination}.")
    return jsonify({"message": message}), 200

@app.route('/api/players/suggestion', methods=['POST'])
def player_suggestion():
    data = request.json
    player_id = data.get("playerId")
    suggestion = data.get("suggestion")
    
    # Log the suggestion request
    print(f"Player {player_id} made a suggestion: {suggestion}.")

    message = game.make_suggestion(player_id, suggestion)
    print(f"Suggestion processed for Player {player_id}.")
    return jsonify({"message": message}), 200

@app.route('/api/players/accusation', methods=['POST'])
def player_accusation():
    data = request.json
    player_id = data.get("playerId")
    accusation = data.get("accusation")
    
    # Log the accusation request
    print(f"Player {player_id} made an accusation: {accusation}.")

    message = game.make_accusation(player_id, accusation)
    print(f"Accusation processed for Player {player_id}.")
    return jsonify({"message": message}), 200

if __name__ == '__main__':
    app.run(debug=True)
