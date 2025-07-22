# game.py
# Tobias Mullins
# CSC-220 Final Project
# July 21, 2025

from die import Die
from player import Player
from collections import Counter
from display import printDiceAscii, displayScoreboard

class Game:
    GAME_LIMIT = 10000

    def __init__(self, playerList):
        self.gameWon = False
        self.players = playerList
        self.currentPlayer = 0

    def play(self):
        while not self.gameWon:
            displayScoreboard(self.players)
            self.p = self.players[self.currentPlayer]
            print(f"\n\n{self.p.name}'s turn.")
            print("============")
            self.takeTurn()
            if not self.gameWon:
                self.nextPlayer()

        displayScoreboard(self.players)
        winner = self.players[self.currentPlayer]
        print(f"\nGame over! Congratulations {winner.name}!")
        return

    def takeTurn(self, turnTotal = 0):
        self.p.rollDice()
        rollVal, scoringDice = self.calculateRollValue()

        print("You rolled:")
        printDiceAscii([d.getValue() for d in self.p.dice])

        print(f"\nScore for this roll: {rollVal}")

        currentTurnTotal = turnTotal + rollVal
        print(f"Total for this turn so far: {currentTurnTotal}")

        if rollVal == 0:
            print("Zilch!")
            self.p.resetDice()
            return

        goAgain = input("Roll again? (y/n): ")
        if goAgain.lower() == "y":
            if scoringDice == len(self.p.dice) + len(self.p.heldDice):
                print("Hot hand! All your dice scored. Rolling 6 again.")
                self.p.resetDice()
            else:
                holds = input("Do you want to hold any dice? (y/n): ")
                if holds.lower() == "y":
                    for i in range(len(self.p.dice)):
                        print(f"D{i + 1}", end=" ")
                    print("")
                    for d in self.p.dice:
                        print(f" {d.getValue()}", end=" ")

                    diceToHold = input("\nWhich dice do you want to hold? \n" + \
                                       "Enter the number (D1 = 1), separated by spaces: ")
                    diceToHold = diceToHold.strip()
                    holding = [int(index) -1 for index in diceToHold.split(" ")]

                    self.p.hold(holding)

            self.takeTurn(currentTurnTotal)

        else:
            if self.p.isOnBoard(currentTurnTotal):
                self.p.addToScore(currentTurnTotal)

            self.p.resetDice()
            if self.p.getTotalScore() >= self.GAME_LIMIT:
                self.gameWon = True
                print("YOU WIN!")
            self.showScores()
            return

    def nextPlayer(self):
        if self.currentPlayer < len(self.players) - 1:
            self.currentPlayer += 1
        else:
            self.currentPlayer = 0

    def calculateRollValue(self):
        totalSum = 0
        scoringDiceCount = 0
        rolledDice = self.p.dice

        values = [d.getValue() for d in rolledDice]
        countedValues = Counter(values)

        if len(rolledDice) == 6:
            if len(countedValues) == 6:
                return 1500, 6
            if len(countedValues) == 3 and all(v == 2 for v in countedValues.values()):
                return 1500, 6

        for val, count in countedValues.items():
            if count >= 3:
                scoringDiceCount += count
                if val == 1:
                    baseScore = 1000
                    totalSum += baseScore * (2 ** (count - 3)) if count > 3 else baseScore
                else:
                    baseScore = val * 100
                    totalSum += baseScore * (2 ** (count - 3)) if count > 3 else baseScore

        remainingValues = list(values)
        for val, count in countedValues.items():
            if count >= 3:
                for _ in range(count):
                    remainingValues.remove(val)

        singlesCounter = Counter(remainingValues)
        if 1 in singlesCounter:
            totalSum += 100 * singlesCounter[1]
            scoringDiceCount += singlesCounter[1]
        if 5 in singlesCounter:
            totalSum += 50 * singlesCounter[5]
            scoringDiceCount += singlesCounter[5]

        return totalSum, scoringDiceCount

    def showScores(self):
        playerObj = self.players[self.currentPlayer]
        print(f"{playerObj.name}'s score is now: {playerObj.getTotalScore()}")
                    
