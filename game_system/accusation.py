from solution import Solution
from suggestion import Suggestion
class Accusation(Suggestion):
    def __init__(self, character, weapon, room):
        """
        Initialize a Accusation object, inheriting from the Suggestion Class.

        :param character: The character used in the accusation.
        :param weapon: The weapon used in the accusation.
        :param room: The room used in the accusation.
        """
        super().__init__(character, weapon, room)
    
    def checkAccusation(self, solution: Solution):
        """
        Check if the accusation is correct.

        :param solution: The solution of the current game.

        Return False if the accusation is incorrect. Return True if the accusation is correct.
        """

        if self.character != solution.character:
            return False
        if self.room != solution.room:
            return False
        if self.weapon != weapon:
            return False
        return True