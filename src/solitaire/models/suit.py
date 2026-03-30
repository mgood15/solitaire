from enum import Enum
from solitaire.models.color import Color

class Suit(Enum):
    HEARTS = (Color.RED, "Hearts")
    DIAMONDS = (Color.RED, "Diamonds")
    SPADES = (Color.BLACK, "Spades")
    CLUBS = (Color.BLACK, "Clubs")

    def __init__(self, color, label):
        self.color = color
        self.label = label
