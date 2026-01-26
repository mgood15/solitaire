class Card:
    """
    Represents a single playing card in a deck.
    """

    VALID_SUITS = ["Hearts", "Diamonds", "Spades", "Clubs"]
    NAMES = {
        1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
        6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
        11: "Jack", 12: "Queen", 13: "King"
    }

    def __init__(self, suit: str, value: int):
        """
        Initializes a card with a suit and a numerical value (1-13).
        """
        self.suit = suit.capitalize()
        if self.suit not in Card.VALID_SUITS:
            raise ValueError(f"Invalid suit: {self.suit}. Must be one of {Card.VALID_SUITS}")

        if not (1 <= value <= 13):
            raise ValueError(f"Invalid value: {value}. Must be between 1 and 13")

        self.value = value
        self.flipped = False

        # Determine color based on suit
        if self.suit in ["Hearts", "Diamonds"]:
            self.color = "Red"
        else:
            self.color = "Black"

        # Map numerical value to name

        self.name = Card.NAMES.get(value, str(value))

    def flip(self):
        """
        Toggles the 'flipped' state of the card back and forth.
        """
        self.flipped = not self.flipped

    def print_unicode(self):
        """
        Prints the Unicode symbol for the specific card.
        Mapping follows the Unicode Playing Cards block (U+1F0A0 - U+1F0DF).
        """
        # Base offsets for suits in the Unicode block
        suit_offsets = {
            "Spades": 0x1F0A0,
            "Hearts": 0x1F0B0,
            "Diamonds": 0x1F0C0,
            "Clubs": 0x1F0D0
        }

        if self.suit not in suit_offsets:
            print(f"Unable to print unknown suit {self.suit}")
            return

        # The Unicode block for cards maps values 1-13 (Ace to King).
        # Note: Unicode includes a 'Knight' card at offset 12, so we adjust
        # the mapping for Jack, Queen, and King.
        unicode_val = suit_offsets[self.suit] + self.value
        if self.value > 11:
            unicode_val += 1

        print(chr(unicode_val))

    def print_full_name(self):
        """
        Prints the human-readable full name of the card (e.g., "Ace of Spades").
        """
        print(f"{self.name} of {self.suit}")
