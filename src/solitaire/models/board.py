from collections import deque

from solitaire.models.deck import Deck
from solitaire.models.card import Card
from solitaire.models.suit import Suit
from solitaire.models.color import Color


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
            self._ensure_top_card_flipped(pile)

    def _ensure_top_card_flipped(self, pile: list[Card] | deque[Card]):
        """
        Ensures the top card of a pile is flipped face up.
        """
        if pile:
            card = pile[-1] if isinstance(pile, list) else pile[0]
            if not card.flipped:
                card.flip()

    def draw_from_stock(self) -> bool:
        """
        Draws a card from the stock and moves it to the waste.
        If the stock is empty, resets the stock by moving all cards from waste back to stock.
        :return: True if successful, False otherwise
        """
        if not self.stock:
            if not self.waste:
                return False
            # Reset stock: move waste back to stock
            # In Solitaire, the waste is flipped back and put into stock
            while self.waste:
                card = self.waste.pop()
                if card.flipped:
                    card.flip()
                self.stock.append(card)
            
            if self.stock:
                # Stock is face-down by default
                pass
            return True

        card = self.stock.popleft()
        if not card.flipped:
            card.flip()
        self.waste.append(card)
        
        return True

    def is_move_valid(self, source_type: str, source_idx: int, dest_type: str, dest_idx: int, num_cards: int = 1) -> bool:
        """
        Stub for move validation logic. Currently always returns True.
        
        :param source_type: Type of the source (tableau, foundation, waste)
        :param source_idx: Index of the source pile (if applicable)
        :param dest_type: Type of the destination (tableau, foundation)
        :param dest_idx: Index of the destination pile (if applicable)
        :param num_cards: Number of cards to move (relevant for tableau)
        :return: True if move is valid, False otherwise
        """
        # Logic to "reject" a move will be implemented in a separate issue.
        return True

    def move_card(self, source_type: str, dest_type: str, source_idx: int = None, dest_idx: int = None, num_cards: int = 1):
        """
        Moves cards between board components.
        
        :param source_type: Type of the source (tableau, foundation, waste)
        :param dest_type: Type of the destination (tableau, foundation)
        :param source_idx: Index of the source pile
        :param dest_idx: Index of the destination pile
        :param num_cards: Number of cards to move
        :return: True if move was successful, False otherwise
        """
        if not self.is_move_valid(source_type, source_idx, dest_type, dest_idx, num_cards):
            return False

        # Get source cards
        cards_to_move = []
        source_pile = None
        
        if source_type == "tableau":
            source_pile = self.tableau[source_idx]
            if len(source_pile) < num_cards:
                return False
            cards_to_move = source_pile[-num_cards:]
            self.tableau[source_idx] = source_pile[:-num_cards]
        elif source_type == "foundation":
            source_pile = self.foundation[source_idx]
            if not source_pile:
                return False
            cards_to_move = [source_pile.pop()]
        elif source_type == "waste":
            if not self.waste:
                return False
            cards_to_move = [self.waste.pop()]
        else:
            return False

        # Get destination pile
        dest_pile = None
        if dest_type == "tableau":
            dest_pile = self.tableau[dest_idx]
        elif dest_type == "foundation":
            dest_pile = self.foundation[dest_idx]
        else:
            # If invalid destination, return cards to source
            if source_type == "tableau":
                self.tableau[source_idx].extend(cards_to_move)
            elif source_type == "foundation":
                self.foundation[source_idx].extend(cards_to_move)
            elif source_type == "waste":
                self.waste.append(cards_to_move[0])
            return False

        # Apply move
        dest_pile.extend(cards_to_move)

        # Post-move cleanup: ensure top card of source tableau is flipped
        if source_type == "tableau":
            self._ensure_top_card_flipped(self.tableau[source_idx])

        return True

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
            Suit.SPADES: "\U00002664",  # Spades
            Suit.HEARTS: "\U00002661",  # Hearts
            Suit.DIAMONDS: "\U00002662",  # Diamonds
            Suit.CLUBS: "\U00002667"  # Clubs
        }
        for i, pile in enumerate(self.foundation):
            if len(pile) > 0:
                pile[-1].print_unicode()
            else:
                # This might need to be indexed differently if we want specific suit symbols for each foundation slot
                # For now, let's keep the logic as it was (indexed by 0-3) if possible, 
                # but it's better to use Suit enums.
                # Assuming foundation[0] is Spades, 1 is Hearts, etc. based on the previous dictionary.
                suits = [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]
                print(suit_symbols[suits[i]])
