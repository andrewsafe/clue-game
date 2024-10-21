class Player:
    def __init__(self, player_username, avatar, cards, location):
        """
        Initialize a Accusation object.

        :param player_username: The username of the player making the accusation.
        :param avatar: The character the player is playing as in the game.
        :param cards: The clue cards the player has.
        :param location: The current location of the player.
        """
        self.player_username = player_username
        self.avatar = avatar
        self.cards = cards
        self.location = location