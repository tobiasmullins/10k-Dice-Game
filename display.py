# display.py
# Tobias Mullins
# CSC-220 Final Project
# July 21, 2025

# A dictionary containing ASCII art for each possible die face.
DICE_ART = {
    1: [
        "┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"
    ],
    2: [
        "┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"
    ],
    3: [
        "┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"
    ],
    4: [
        "┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"
    ],
    5: [
        "┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"
    ],
    6: [
        "┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘"
    ]
}

# Prints a horizontal row of dice using their ASCII art representations.
def printDiceAscii(diceValues):
    # Do nothing if the list of dice values is empty.
    if not diceValues:
        return
    # Iterate through the 5 lines that make up the dice art.
    for i in range(5):
        lineToPrint = ""
        # Build each line by concatenating the corresponding line from each die's art.
        for value in diceValues:
            lineToPrint += DICE_ART[value][i] + " "
        print(lineToPrint)

# Displays a formatted scoreboard with player names and scores.
def displayScoreboard(players):
    print("\n" + "─" * 36)
    print("│              SCOREBOARD              │")
    print("├──────────────────────────────────┤")
    # Loop through each player and display their name and score.
    for player in players:
        name = player.name
        score = player.getTotalScore()
        print(f"│ {name:<20} {score:>10} │")
    print("└──────────────────────────────────┘")

