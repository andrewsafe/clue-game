class Player:
    def __init__(self, name):
        """
        Initialize a Player instance.

        :param name: The name of the player.
        """
        self.name = name
        self.cards = []  # List to hold the player's cards

    def add_card(self, card):
        """
        Add a card to the player's hand.

        :param card: The card to add (instance of Card).
        """
        self.cards.append(card)

    def remove_card(self, card):
        """
        Remove a card from the player's hand.

        :param card: The card to remove (instance of Card).
        """
        if card in self.cards:
            self.cards.remove(card)

    def show_cards(self):
        """
        Show all the cards held by the player.

        :return: List of card names held by the player.
        """
        return [str(card) for card in self.cards]

    def __str__(self):
        """
        String representation of the Player instance.

        :return: A string describing the player and their cards.
        """
        return f"Player: {self.name}, Cards: {', '.join(self.show_cards())}"
