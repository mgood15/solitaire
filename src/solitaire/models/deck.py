import random
from solitaire.models.card import Card

class Deck:
    """
    Represents a full deck of 52 playing cards.
    """

    def __init__(self):
        """
        Initializes a standard 52-card deck.
        """
        self.cards = []
        for suit in Card.VALID_SUITS:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))

    def shuffle(self):
        """
        Shuffles the deck of cards. Utilizes Fisher-Yates algorithm for randomness.
        """
        for i in range(len(self.cards) - 1, 0, -1):
            swap_i = random.randint(0, i)
            self.cards[swap_i], self.cards[i] = self.cards[i], self.cards[swap_i]

    def draw(self):
        """
        Draws (removes and returns) the top card from the deck.
        Raises IndexError if the deck is empty.
        """
        if not self.cards:
            raise IndexError("Cannot draw from an empty deck")
        return self.cards.pop()

    def __len__(self):
        """
        Returns the number of remaining cards in the deck.
        """
        return len(self.cards)
