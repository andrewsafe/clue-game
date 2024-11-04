from game_system.suggestion import Suggestion
from game_system.accusation import Accusation
from game_system.player import Player
from game_system.solution import Solution
class Game:
    def __init__(self):
        self.players = {
            "player1": {"position": "Room1"},  # Initialize players with starting positions
            "player2": {"position": "Room2"},
            # Add more players as needed
        }
        self.current_turn = None
        self.game_state = "ongoing"  # Example of tracking game state

    def start_turn(self, player_id):
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        # Start the turn for the player
        self.current_turn = player_id
        return "Player's turn started."

    def end_turn(self, player_id):
        # Logic to end the turn and determine the next player
        if player_id != self.current_turn:
            raise ValueError(f"It's not {player_id}'s turn.")
        # Update game state if needed
        self.current_turn = None  # Or logic to move to the next player
        return "Player's turn ended."

    def move_player(self, player_id, destination):
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        # Update player's position
        self.players[player_id]['position'] = destination
        return f"Player {player_id} moved to {destination}."

    def make_suggestion(self, player_id, suggestion):
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        #will flesh out for minimal/target requirements
        #suggestion.checkSuggestion(player_id.cards)
        return f"Player {player_id} made a suggestion: {suggestion}."

    def make_accusation(self, player_id, accusation):
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        #will flesh out for minimal/target requirements
        #accusation.checkAccusation(solution)
        return f"Player {player_id} made an accusation: {accusation}."
