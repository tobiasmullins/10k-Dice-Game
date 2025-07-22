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

    def takeTurn(self, turnTotal=0):
        self.p.rollDice()
        
        print("You rolled:")
        rolledValues = [d.getValue() for d in self.p.dice]
        printDiceAscii(rolledValues)

        scoringGroups = self.findScoringGroups(rolledValues)

        if not scoringGroups:
            print("\nZilch! No scoring dice.")
            self.p.resetDice()
            return

        print("\nScoring Options:")
        for i, (score, dice) in enumerate(scoringGroups):
            print(f"  {i + 1}: {dice} for {score} points")

        scoreThisRound = 0
        diceToKeep = []
        
        while True:
            try:
                choiceStr = input("Choose which group(s) to keep (e.g., '1' or '1,2'). You must keep at least one: ")
                choices = [int(c.strip()) for c in choiceStr.split(',')]
                
                if not choices or any(c < 1 or c > len(scoringGroups) for c in choices):
                    raise ValueError("Invalid choice.")

                # Process valid choices
                tempDiceToKeep = []
                for choice in set(choices): # Use set to avoid duplicate choices
                    score, diceList = scoringGroups[choice - 1]
                    scoreThisRound += score
                    tempDiceToKeep.extend(diceList)
                
                diceToKeep = tempDiceToKeep
                break # Exit validation loop

            except (ValueError, IndexError):
                print("Invalid input. Please enter numbers from the list, separated by commas.")
        
        self.p.hold(diceToKeep)
        currentTurnTotal = turnTotal + scoreThisRound
        
        print(f"\nYou kept {sorted(diceToKeep)}, earning {scoreThisRound} points.")
        print(f"Total for this turn so far: {currentTurnTotal}")

        # Check if all dice have been held
        if len(self.p.heldDice) == 6:
            print("Hot hand! All your dice scored. Rolling 6 again.")
            self.p.resetDice()
            self.takeTurn(currentTurnTotal)
            return

        goAgain = input("Roll again? (y/n): ")
        if goAgain.lower() == "y":
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

    def findScoringGroups(self, diceValues):
        """Finds all possible scoring groups and returns them as a list."""
        groups = []
        counts = Counter(diceValues)
        
        # Handle 6-dice combos first, as they are exclusive
        if len(diceValues) == 6:
            if len(counts) == 6:
                groups.append((1500, sorted(diceValues)))
                return groups
            if len(counts) == 3 and all(v == 2 for v in counts.values()):
                groups.append((1500, sorted(diceValues)))
                return groups

        # Find N-of-a-kind
        remainingValues = list(diceValues)
        for val, count in counts.items():
            if count >= 3:
                diceList = [val] * count
                if val == 1:
                    baseScore = 1000
                    score = baseScore * (2 ** (count - 3))
                else:
                    baseScore = val * 100
                    score = baseScore * (2 ** (count - 3))
                groups.append((score, diceList))
                # Remove these from consideration for singles
                for die in diceList:
                    remainingValues.remove(die)
        
        # Find singles in the remaining dice
        for val in remainingValues:
            if val == 1:
                groups.append((100, [1]))
            elif val == 5:
                groups.append((50, [5]))
        
        return groups

    def showScores(self):
        playerObj = self.players[self.currentPlayer]
        print(f"{playerObj.name}'s score is now: {playerObj.getTotalScore()}")
