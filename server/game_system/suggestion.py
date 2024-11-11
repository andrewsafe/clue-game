class Suggestion:
    def __init__(self, character, weapon, room):
        """
        Initialize a Suggestion object.

        :param character: The character used in the suggestion.
        :param weapon: The weapon used in the suggestion.
        :param room: The room used in the suggestion.
        """
        self.character = character
        self.weapon = weapon
        self.room = room

    def __str__(self):
        """
        Return a string representation of the Suggestion object.
        """
        return f"Character: {self.character}, Weapon: {self.weapon}, Room: {self.room}"

    def checkSuggestion(self, cards):
        """
        Check if the suggestion is correct.

        :param cards: The cards the current player we're checking with has.

        Return any cards the player we are checking with has. If there are no cards that match, return an empty list.
        """
        incorrectCards = []
        if self.character in cards:
            incorrectCards.append(self.character)
        if self.room in cards:
            incorrectCards.append(self.room)
        if self.weapon in cards:
            incorrectCards.append(self.weapon)
        return incorrectCards
