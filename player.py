# player.py
# Tobias Mullins
# CSC-220 Final Project
# July 23,2025

from die import Die

class Player:
    """Represents a player, managing their dice, score, and game state."""

    # Initializes a new player with a name and default game values.
    def __init__(self, name):
        self.name = name
        self.totalScore = 0    # Player's overall score.
        self.dice = []         # Dice currently in play for the turn.
        self.heldDice = []     # Dice kept for scoring during a turn.
        self.onBoard = False   # Tracks if the player has met the initial scoring threshold.

    def rollDice(self):
        """Rolls the dice that are not currently being held."""
        # Calculate how many new dice to roll.
        numToRoll = 6 - len(self.heldDice)
        # Create new Die objects for the roll.
        self.dice = [Die() for _ in range(numToRoll)]

    def hold(self, diceValuesToKeep):
        """
        Moves dice from the active roll to the held list based on their values.
        
        Args:
            diceValuesToKeep (list): A list of integer values of dice to keep.
        """
        keptDieObjects = []
        
        # For each value we need to keep, find a matching Die object in the current roll.
        for value in diceValuesToKeep:
            for dieObject in self.dice:
                if dieObject.getValue() == value:
                    keptDieObjects.append(dieObject)
                    self.dice.remove(dieObject) # Remove from roll to prevent it from being kept twice.
                    break # Move to the next value to keep.
        
        # Add the collected Die objects to the player's held hand.
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
        """
        Checks if the player is "on the board."
        Player must score 1000+ in a single turn to start accumulating points.
        """
        # If already on the board, they can bank any score.
        if self.onBoard:
            return True
        # If not on board, check if this turn's score meets the threshold.
        if turnTotal >= 1000:
            self.onBoard = True
            return True
        # If they fail to meet the threshold, the points are lost.
        print(f"You need 1000 points in a single turn to get on the board. You only scored {turnTotal}.")
        return False
