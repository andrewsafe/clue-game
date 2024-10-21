from Solution.py import Solution
class Accusation:
    def __init__(self, player_username, character, weapon, room):
        """
        Initialize a Accusation object.

        :param player_username: The username of the player making the accusation.
        :param character: The character used in the accusation.
        :param weapon: The weapon used in the accusation.
        :param room: The room used in the accusation.
        """
        self.player_username = player_username
        self.character = character
        self.weapon = weapon
        self.room = room
    
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