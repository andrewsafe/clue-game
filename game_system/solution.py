from suggestion import Suggestion
class Solution(Suggestion)
    def __init__(self, character, room, weapon):
        """
        Initialize a Solution object, inheriting from the Suggestion Class.

        :param character: The character used in the suggestion.
        :param weapon: The weapon used in the suggestion.
        :param room: The room used in the suggestion.
        """
        super().__init__(character, weapon, room)