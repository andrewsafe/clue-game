class TurnManager:
    def __init__(self, players):
        """
        Initialize a TurnManager instance.

        :param players: A list of Player instances.
        """
        self.players = players
        self.current_turn = 0  # Index of the current player

    def next_turn(self):
        """
        Advance to the next player's turn.
        """
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def current_player(self):
        """
        Get the player whose turn it is currently.

        :return: The current Player instance.
        """
        return self.players[self.current_turn]

    def reset_turns(self):
        """
        Reset the turn order back to the first player.
        """
        self.current_turn = 0

    def __str__(self):
        """
        String representation of the TurnManager instance.

        :return: A string showing the current player and turn order.
        """
        return f"Current turn: {self.current_player().name}"
