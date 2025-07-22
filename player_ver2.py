# In file: player.py
from die import Die

class Player:
    """Represents a player, managing their dice, score, and game state."""

    def __init__(self, name):
        self.name = name
        self.totalScore = 0
        self.dice = []       # Dice just rolled, available to be held
        self.heldDice = []   # Dice kept for points this turn

    def rollDice(self):
        """Rolls the dice that are not currently being held."""
        numToRoll = 6 - len(self.heldDice)
        self.dice = [Die() for _ in range(numToRoll)]

    def hold(self, diceValuesToKeep):
        """
        Moves dice from the active roll to the held list based on their values.
        
        Args:
            diceValuesToKeep (list): A list of integer values of dice to keep.
        """
        keptDieObjects = []
        
        # For each value we need to keep, find a matching Die object
        for value in diceValuesToKeep:
            for dieObject in self.dice:
                if dieObject.getValue() == value:
                    keptDieObjects.append(dieObject)
                    self.dice.remove(dieObject) # Remove it so it can't be matched again
                    break # Move to the next value to keep
        
        self.heldDice.extend(keptDieObjects)


    def resetDice(self):
        """Resets the player's hand for the next turn."""
        self.dice = []
        self.heldDice = []

    def addToScore(self, points):
        """Adds points to the player's total score."""
        self.totalScore += points

    def getTotalScore(self):
        """Returns the player's total score."""
        return self.totalScore

    def isOnBoard(self, turnTotal):
        """Checks if the player is "on the board"."""
        if self.onBoard:
            return True
        if turnTotal >= 1000:
            self.onBoard = True
            return True
        print(f"You need 1000 points in a single turn to get on the board. You only scored {turnTotal}.")
        return False
