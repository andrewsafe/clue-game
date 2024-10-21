from flask import Flask, request, jsonify
from game import Game

app = Flask(__name__)
game = Game()  # Create an instance of the Game class

@app.route('/api/players/turn', methods=['POST'])
def player_turn():
    data = request.json
    action = data.get("action")
    player_id = data.get("playerId")
    
    if action == "start":
        message = game.start_turn(player_id)
        return jsonify({"message": message}), 200
    elif action == "end":
        next_player = game.end_turn(player_id)
        return jsonify({"message": f"Turn ended. Next player: {next_player}"}), 200
    else:
        return jsonify({"error": "Invalid action"}), 400

@app.route('/api/players/move', methods=['POST'])
def player_move():
    data = request.json
    player_id = data.get("playerId")
    destination = data.get("destination")
    message = game.move_player(player_id, destination)
    return jsonify({"message": message}), 200

@app.route('/api/players/suggestion', methods=['POST'])
def player_suggestion():
    data = request.json
    player_id = data.get("playerId")
    suggestion = data.get("suggestion")
    message = game.make_suggestion(player_id, suggestion)
    return jsonify({"message": message}), 200

@app.route('/api/players/accusation', methods=['POST'])
def player_accusation():
    data = request.json
    player_id = data.get("playerId")
    accusation = data.get("accusation")
    message = game.make_accusation(player_id, accusation)
    return jsonify({"message": message}), 200

if __name__ == '__main__':
    app.run(debug=True)
