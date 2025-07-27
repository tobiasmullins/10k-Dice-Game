# main.py
# Tobias Mullins
# CSC-220 Final Project
# July 21, 2025

from player import Player
from game import Game

# This function sets up and starts the game.
def main():
    # Loop to get a valid number of players from the user.
    while True:
        try:
            numStr = input("Enter the number of players: ")
            num = int(numStr)
            if 1 <= num <= 6:
                break
            else:
                print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Create a list of Player objects based on user input.
    playerList = []
    for i in range(num):
        while True:
            name = input(f"Enter name for Player {i + 1}: ").strip()
            if name:
                playerList.append(Player(name))
                break
            else:
                print("Name cannot be empty. Please enter a name.")

    print()
    print("Let's play Zilch (10,000)!\n")

    # Create a new game instance and start the game.
    game = Game(playerList)
    game.play()

# This ensures the main function runs only when the script is executed directly.
if __name__ == "__main__":
    main()
