# die.py
# Tobias Mullins
# CSC-220 Final Project
# July 22, 2025

# Import the randint function from the random module to generate random integers.
from random import randint

# Define the Die class, which represents a single six-sided die.
class Die():
    """A class to represent a single game die."""

    # The __init__ method is the constructor for the class.
    # It initializes the die's attributes.
    def __init__(self):
        """Initialize the die's starting value."""
        # Set a default value for the die.
        self.value = 1
        # Roll the die to get an initial random value.
        self.roll()

    # The roll method simulates rolling the die.
    def roll(self):
        """Roll the die and update its value."""
        # Generate a new random integer between 1 and 6.
        newValue = randint(1, 6)
        # Assign the new random number to the die's value.
        self.value = newValue

    # The getValue method returns the current value of the die.
    def getValue(self):
        """Return the current face value of the die."""
        return self.value
