import random
from game_system.card import Card
from game_system.player import Player

class GameSystem:
    def __init__(self):
        """
        Initialize a GameSystem instance.
        """
        self.players = []  # List to hold player instances
        self.cards = []    # List to hold all card instances
        self.setup_cards() # Setup the cards for the game

    def setup_cards(self):
        """
        Setup the cards for the game. This includes suspects, weapons, and rooms.
        """
        suspects = [
            Card("Colonel Mustard", "suspect"),
            Card("Professor Plum", "suspect"),
            Card("Reverend Green", "suspect"),
            Card("Mrs. Peacock ", "suspect"),
            Card("Miss Scarlett", "suspect"),
            Card("Mrs. White ", "suspect")
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

    def add_player(self, player_name):
        """
        Add a player to the game.

        :param player_name: The name of the player.
        """
        new_player = Player(player_name)
        self.players.append(new_player)

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

    def start_game(self):
        """
        Start the game by distributing cards and displaying player cards.
        """
        #will have to create solution first before distributing remaining cards
        self.distribute_cards()
        self.show_player_cards()
