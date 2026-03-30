from collections import deque

from solitaire.models.deck import Deck

from solitaire.models.card import Card


class Board:
    """
    Represents the playing board for a Solitaire game.
    """

    def __init__(self):
        """
        Initializes the board with its four main components:
        foundation, tableau, stock, and waste.
        """
        deck = Deck()
        deck.shuffle()
        self.foundation = [[] for _ in range(4)]
        self.tableau = [[] for _ in range(7)]
        self.stock = deque()
        self.waste = []
        # takes the deck and builds tableau and stock
        self._build(deck)
        
    def _build(self, deck: Deck):
        for i, pile in enumerate(self.tableau):
            for _ in range(i + 1):
                self.tableau[i].append(deck.draw())
        
        # the remaining cards in the deck are placed in the stock
        while len(deck) > 0:
            self.stock.append(deck.draw())
        
        # tableau piles have the last card revealed to the user
        for pile in self.tableau:
            if pile:
                card = pile[-1]
                if not card.flipped:
                    card.flip()

        # the first card in the stock should be revealed to the user
        if self.stock:
            if not self.stock[0].flipped:
                self.stock[0].flip()

    def print_board(self):
        """
        Prints the current state of the board.
        """
        print("Foundation:\n")
        self.print_foundation()
        print("Tableau:\n")
        for i, pile in enumerate(self.tableau):
            print(f"Printing pile {i}:\n")
            self.print_tableau_pile(pile)
        print("Stock:\n")
        for card in self.stock:
            card.print_unicode()
        print("Waste:\n")
        for card in self.waste:
            card.print_unicode()

    def print_tableau_pile(self, pile: list[Card]):
        # Note: This function will be adapted once an interactive board is made
        for i, card in enumerate(reversed(pile)):
            print(f"{i}:\n")
            card.print_unicode()

    def print_foundation(self):
        suit_symbols = {
            0: "\U00002664",  # Spades
            1: "\U00002661",  # Hearts
            2: "\U00002662",  # Diamonds
            3: "\U00002667"  # Clubs
        }
        for i, pile in enumerate(self.foundation):
            if len(pile) > 0:
                pile[-1].print_unicode()
            else:
                print(suit_symbols[i])
