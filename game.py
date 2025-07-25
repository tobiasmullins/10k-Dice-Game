

    def takeTurn(self, turnTotal=0):
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
                    while True:
                        try:
                            for i in range(len(self.p.dice)):
                                print(f"D{i + 1}", end=" ")
                            print("")
                            for d in self.p.dice:
                                print(f" {d.getValue()}", end=" ")

                            diceToHold = input("\nWhich dice do you want to hold? \n" + \
                                               "Enter the number (D1 = 1), separated by spaces: ")
                            diceToHold = diceToHold.strip()
                            
                            holding = [int(index) - 1 for index in diceToHold.split(" ")]
                            
                            if any(h < 0 or h >= len(self.p.dice) for h in holding):
                                print("Invalid input. Please only enter numbers for the dice shown.")
                                continue 
                                
                            self.p.hold(holding)
                            break 
                            
                        except ValueError:
                            print("Invalid input. Please only enter numbers separated by spaces.")


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
