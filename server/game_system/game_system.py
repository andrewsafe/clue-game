import random
from game_system.card import Card
from game_system.player import Player
from game_system.solution import Solution
from game_system.suggestion import Suggestion
from game_system.accusation import Accusation

class GameSystem:
    def __init__(self):
        """
        Initialize a GameSystem instance.
        """
        self.players = []  # List to hold player instances
        self.cards = []    # List to hold all card instances
        self.current_turn = None
        self.game_state = "ongoing"  # Example of tracking game state
        self.setup_cards()  # Setup the cards for the game
        self.counter = 0

    def setup_cards(self):
        """
        Setup the cards for the game. This includes suspects, weapons, and rooms.
        """
        suspects = [
            Card("Colonel Mustard", "suspect"),
            Card("Professor Plum", "suspect"),
            Card("Reverend Green", "suspect"),
            Card("Mrs. Peacock", "suspect"),
            Card("Miss Scarlett", "suspect"),
            Card("Mrs. White", "suspect")
        ]

        weapons = [
            Card("Dagger", "weapon"),
            Card("Candlestick", "weapon"),
            Card("Revolver", "weapon"),
            Card("Rope", "weapon"),
            Card("Lead Pipe", "weapon"),
            Card("Wrench", "weapon")
        ]

        rooms = [
            Card("Hall", "room"),
            Card("Lounge", "room"),
            Card("Library", "room"),
            Card("Kitchen", "room"),
            Card("Billiard Room", "room"),
            Card("Study", "room"),
            Card("Ballroom", "room"),
            Card("Dining Room", "room"),
            Card("Conservatory", "room")
        ]

        # Combine all cards into one list
        self.cards = suspects + weapons + rooms

    def start_game(self):
        """
        Start the game by distributing cards and displaying player cards.
        """
        self.distribute_cards()
        self.show_player_cards()

    def add_player(self, player_name, character, starting_position="Hall"):
        # Check if the player already exists
        if player_name in [player.name for player in self.players]:
            return f"{player_name} already exists in the game."

        # Create a new player with character and starting position
        new_player = Player(player_name, character, position=starting_position)
        self.players.append(new_player)
        return f"{player_name} added successfully as {character}."


    def start_turn(self, player_id):
        if player_id not in [player.name for player in self.players]:
            raise ValueError(f"{player_id} does not exist.")
        self.current_turn = player_id
        return f"{player_id}'s turn started."

    def end_turn(self, player_id):
        if player_id != self.current_turn:
            raise ValueError(f"It's not {player_id}'s turn.")
        self.current_turn = None  # Logic for moving to the next player can be added here
        return f"{player_id}'s turn ended."

    def move_player(self, player_id, destination):
        player = next((p for p in self.players if p.name == player_id), None)
        if not player:
            raise ValueError(f"{player_id} does not exist.")
        player.position = destination
        return f"{player_id} moved to {destination}."

    def make_suggestion(self, player_id, suggestion):
        if player_id not in [player.name for player in self.players]:
            raise ValueError(f"Player {player_id} does not exist.")
        # Handle suggestion logic
        return f"Player {player_id} made a suggestion: {suggestion}."

    def check_accusation(self, player_id, accusation):
        if player_id not in [player.name for player in self.players]:
            raise ValueError(f"Player {player_id} does not exist.")
        # Implement accusation checking logic
        return False  # Placeholder for whether the accusation is correct

    def distribute_cards(self):
        """
        Distribute cards among players randomly.
        """
        random.shuffle(self.cards)
        num_players = len(self.players)
        for i, card in enumerate(self.cards):
            self.players[i % num_players].add_card(card)

    def show_player_cards(self):
        """
        Display the cards of all players.
        """
        for player in self.players:
            print(player)
