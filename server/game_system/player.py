class Player:
    _id_counter = 1  # Class-level counter for unique IDs

    def __init__(self, name):
        """
        Initialize a Player instance.

        :param name: The name of the player.
        """
        self.id = Player._id_counter  # Assign a unique ID
        Player._id_counter += 1
        self.name = name
        self.cards = []  # List to hold the player's cards

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def show_cards(self):
        return [str(card) for card in self.cards]

    def __str__(self):
        return f"Player: {self.name}, Cards: {', '.join(self.show_cards())}"
