# display.py
# Tobias Mullins
# CSC-220 Final Project
# July 21, 2025


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

def printDiceAscii(diceValues):
    if not diceValues:
        return
    for i in range(5):
        lineToPrint = ""
        for value in diceValues:
            lineToPrint += DICE_ART[value][i] + " "
        print(lineToPrint)

def displayScoreboard(players):
    print("\n" + "─" * 36)
    print("│           SCOREBOARD           │")
    print("├──────────────────────────────────┤")
    for player in players:
        name = player.name
        score = player.getTotalScore()
        print(f"│ {name:<20} {score:>10} │")
    print("└──────────────────────────────────┘")

