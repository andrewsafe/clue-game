class Player:
    _id_counter = 1  # Class-level counter for unique IDs

    def __init__(self, name, character, player_id, position=None):
        """
        Initialize a Player instance.

        :param name: The name of the player.
        :param character: The character associated with the player.
        :param position: The starting position or room for the player.
        """
        self.id = player_id  # Assign a unique ID
        self.name = name
        self.character = character  # Add character attribute
        self.position = position  # Add position attribute
        self.cards = []  # List to hold the player's cards

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def show_cards(self):
        return [str(card) for card in self.cards]

    def __str__(self):
        return f"Player: {self.name}, Character: {self.character}, Position: {self.position}, Cards: {', '.join(self.show_cards())}"
