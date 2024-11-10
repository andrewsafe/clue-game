class Card:
    def __init__(self, name, category):
        """
        Initialize a Card instance.

        :param name: The name of the card (e.g., character name, weapon, or room).
        :param category: The category of the card (e.g., 'suspect', 'weapon', 'room').
        """
        self.name = name
        self.category = category

    def __str__(self):
        """
        String representation of the Card instance.

        :return: A string describing the card.
        """
        return f"{self.name} ({self.category})"

    def __eq__(self, other):
        """
        Check if two Card instances are equal based on their name and category.

        :param other: Another Card instance to compare.
        :return: True if they are the same card, otherwise False.
        """
        if isinstance(other, Card):
            return self.name == other.name and self.category == other.category
        return False
