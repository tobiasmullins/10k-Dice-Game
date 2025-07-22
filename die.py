# die.py
# Tobias Mullins
# CSC-220 Final Project
# July 22, 2025

from random import randint

class Die():
    def __init__(self):
        self.value = 1
        self.roll()

    def roll(self):
        newValue = randint(1, 6)
        self.value = newValue

    def getValue(self):
        return self.value
