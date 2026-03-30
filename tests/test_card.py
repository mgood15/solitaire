import pytest
from solitaire.models.card import Card
from solitaire.models.suit import Suit
from solitaire.models.color import Color

def test_card_initialization_valid():
    """Test creating cards with valid suits and values."""
    card = Card(Suit.HEARTS, 1)
    assert card.suit == Suit.HEARTS
    assert card.value == 1
    assert card._actual_name == "Ace"
    assert card.name == "Hidden Card"
    assert card.color == Color.RED
    assert not card.flipped

    card = Card(Suit.SPADES, 13)
    assert card.suit == Suit.SPADES
    assert card.value == 13
    assert card._actual_name == "King"
    assert card.name == "Hidden Card"
    assert card.color == Color.BLACK

def test_card_initialization_invalid_suit():
    """Test that invalid suits raise ValueError."""
    with pytest.raises(ValueError, match="Invalid suit"):
        Card("Joker", 1)
    
    with pytest.raises(ValueError, match="Invalid suit"):
        Card(None, 5)

def test_card_initialization_invalid_value():
    """Test that invalid values raise ValueError."""
    with pytest.raises(ValueError, match="Invalid value"):
        Card(Suit.HEARTS, 0)
    
    with pytest.raises(ValueError, match="Invalid value"):
        Card(Suit.DIAMONDS, 14)
    
    with pytest.raises(ValueError, match="Invalid value"):
        Card(Suit.CLUBS, -1)

def test_card_flip():
    """Test the flip method."""
    card = Card(Suit.CLUBS, 10)
    assert not card.flipped
    card.flip()
    assert card.flipped
    card.flip()
    assert not card.flipped

def test_card_print_full_name(capsys):
    """Test the print_full_name method."""
    card = Card(Suit.DIAMONDS, 11)
    card.flip()
    card.print_full_name()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Jack of Diamonds"

def test_card_print_full_name_unflipped(capsys):
    """Test that print_full_name shows a masked name when card is not flipped."""
    card = Card(Suit.DIAMONDS, 11)
    assert not card.flipped
    card.print_full_name()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hidden Card"

def test_card_print_unicode_flipped(capsys):
    """Test the print_unicode method when card is flipped."""
    card = Card(Suit.SPADES, 1)
    card.flip()
    card.print_unicode()
    captured = capsys.readouterr()
    # U+1F0A1 is Ace of Spades
    assert captured.out.strip() == "\U0001F0A1"

def test_card_print_unicode_unflipped(capsys):
    """Test that print_unicode shows the card back when card is not flipped."""
    card = Card(Suit.SPADES, 1)
    assert not card.flipped
    card.print_unicode()
    captured = capsys.readouterr()
    # U+1F0A0 is the card back
    assert captured.out.strip() == "\U0001F0A0"
