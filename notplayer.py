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

    def hold(self, diceIndices):
        diceToMove = []
        for index in sorted(diceIndices, reverse = True):
            if 0 <= index < len(self.dice):
                diceToMove.append(self.dice.pop(index))
        self.heldDice.extend(diceToMove)

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
