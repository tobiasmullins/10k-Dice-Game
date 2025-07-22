# player.py
# Tobias Mullins
# CSC-220: Final Project
# July 22, 2025


from die import Die

class Player:
    
    def __init__(self, name):
        self.name = name
        self.totalScore = 0
        self.dice = []       
        self.heldDice = []  
        self.onBoard = False
        

    def rollDice(self):
        numToRoll = 6 - len(self.heldDice)
        self.dice = [Die() for _ in range(numToRoll)]

    def hold(self, diceValuesToKeep):
        keptDieObjects = []
        for value in diceValuesToKeep:
            for dieObject in self.dice:
                if dieObject.getValue() == value:
                    keptDieObjects.append(dieObject)
                    self.dice.remove(dieObject) # Remove it so it can't be matched again
                    break # Move to the next value to keep
        
        self.heldDice.extend(keptDieObjects)

    def resetDice(self):
        self.dice = []
        self.heldDice = []

    def addToScore(self, points):
        self.totalScore += points

    def getTotalScore(self):
        return self.totalScore

    def isOnBoard(self, turnTotal):
        if self.onBoard:
            return True
        if turnTotal >= 1000:
            self.onBoard = True
            return True
        print(f"You need 1000 points in a single turn to get on the board. You only scored {turnTotal}.")
        return False
