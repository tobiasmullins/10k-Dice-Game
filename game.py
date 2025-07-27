# game.py
# Tobias Mullins
# CSC-220 Final Project
# July 21, 2025

from die import Die
from player import Player
from collections import Counter
from display import printDiceAscii, displayScoreboard

# The main class that controls the game logic and flow.
class Game:
    # The score required to win the game.
    GAME_LIMIT = 10000

    # Initializes the game state with a list of players.
    def __init__(self, playerList):
        self.gameWon = False
        self.players = playerList
        self.currentPlayer = 0

    # The main game loop that continues until a player wins.
    def play(self):
        while not self.gameWon:
            displayScoreboard(self.players)
            self.p = self.players[self.currentPlayer]
            print(f"\n\n{self.p.name}'s turn.")
            print("============")
            self.takeTurn()
            if not self.gameWon:
                self.nextPlayer()

        # Display final results after the game is won.
        displayScoreboard(self.players)
        winner = self.players[self.currentPlayer]
        print(f"\nGame over! Congratulations {winner.name}! 🎉")
        return

    # Manages a single player's turn, including rolling, scoring, and re-rolling.
    def takeTurn(self, turnTotal=0):
        self.p.rollDice()
        
        print("You rolled:")
        rolledValues = [d.getValue() for d in self.p.dice]
        printDiceAscii(rolledValues)

        # Identify all possible scoring combinations from the roll.
        scoringGroups = self.findScoringGroups(rolledValues)

        # Handle a "Zilch" (no scoring dice).
        if not scoringGroups:
            print("\nZilch! No scoring dice.")
            self.p.resetDice()
            return

        print("\nScoring Options:")
        for i, (score, dice) in enumerate(scoringGroups):
            print(f"  {i + 1}: {dice} for {score} points")

        scoreThisRound = 0
        diceToKeep = []
        
        # Get and validate user input for which dice to keep.
        while True:
            try:
                choiceStr = input("Choose which group(s) to keep (e.g., '1' or '1,2'). You must keep at least one: ")
                choices = [int(c.strip()) for c in choiceStr.split(',')]
                
                if not choices or any(c < 1 or c > len(scoringGroups) for c in choices):
                    raise ValueError("Invalid choice.")

                # Calculate score and identify dice based on user's choice.
                tempDiceToKeep = []
                for choice in set(choices):
                    score, diceList = scoringGroups[choice - 1]
                    scoreThisRound += score
                    tempDiceToKeep.extend(diceList)
                
                diceToKeep = tempDiceToKeep
                break

            except (ValueError, IndexError):
                print("Invalid input. Please enter numbers from the list, separated by commas.")
        
        self.p.hold(diceToKeep)
        currentTurnTotal = turnTotal + scoreThisRound
        
        print(f"\nYou kept {sorted(diceToKeep)}, earning {scoreThisRound} points.")
        print(f"Total for this turn so far: {currentTurnTotal}")

        # Handle a "Hot Hand" where all 6 dice score, allowing a re-roll with all 6.
        if len(self.p.heldDice) == 6:
            print("Hot hand! All your dice scored. Rolling 6 again.")
            self.p.resetDice()
            self.takeTurn(currentTurnTotal) # Recursive call to continue the turn.
            return

        # Force player to roll if they aren't "on the board" with 1000+ points.
        if not self.p.onBoard and currentTurnTotal < 1000:
            print(f"\nNot on the board and you only have {currentTurnTotal} points this turn.")
            print("You must continue rolling until you reach 1000 points or Zilch.")
            input("Press Enter to roll again...")
            self.takeTurn(currentTurnTotal)
            return

        # Ask the player if they want to roll again or bank their points.
        goAgain = input("Roll again? (y/n): ")
        if goAgain.lower() == "y":
            self.takeTurn(currentTurnTotal)
        else:
            # Bank the points from the turn.
            if self.p.isOnBoard(currentTurnTotal):
                self.p.addToScore(currentTurnTotal)

            self.p.resetDice()
            # Check for a win condition.
            if self.p.getTotalScore() >= self.GAME_LIMIT:
                self.gameWon = True
            self.showScores()
            return

    # Advances the game to the next player in the list.
    def nextPlayer(self):
        if self.currentPlayer < len(self.players) - 1:
            self.currentPlayer += 1
        else:
            self.currentPlayer = 0 # Loop back to the first player.

    # Identifies and scores all possible scoring combinations in a set of dice.
    def findScoringGroups(self, diceValues):
        groups = []
        counts = Counter(diceValues)
        
        # Check for special 6-dice combinations (straight, 3 pairs).
        if len(diceValues) == 6:
            if len(counts) == 6: # 1-2-3-4-5-6 straight
                groups.append((1500, sorted(diceValues)))
                return groups
            # Three pairs (includes 4-of-a-kind + pair, or 6-of-a-kind)
            if all(v % 2 == 0 for v in counts.values()):
                groups.append((1500, sorted(diceValues)))
                return groups

        # Find scoring sets of 3-of-a-kind or more.
        remainingValues = list(diceValues)
        for val, count in counts.items():
            if count >= 3:
                diceList = [val] * count
                if val == 1:
                    baseScore = 1000
                else:
                    baseScore = val * 100
                # Score doubles for each die over 3 (e.g., 4-of-a-kind is 2x, 5 is 4x).
                score = baseScore * (2 ** (count - 3))
                groups.append((score, diceList))
                
                # Remove these dice so they aren't scored again as singles.
                for die in diceList:
                    remainingValues.remove(die)
        
        # Find individual scoring dice (1s and 5s).
        for val in remainingValues:
            if val == 1:
                groups.append((100, [1]))
            elif val == 5:
                groups.append((50, [5]))
        
        return groups

    # A simple utility to show the current player's total score.
    def showScores(self):
        playerObj = self.players[self.currentPlayer]
        print(f"{playerObj.name}'s score is now: {playerObj.getTotalScore()}")

