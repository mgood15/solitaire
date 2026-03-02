import pytest
from src.models.card import Card

def test_card_initialization_valid():
    """Test creating cards with valid suits and values."""
    card = Card("Hearts", 1)
    assert card.suit == "Hearts"
    assert card.value == 1
    assert card.name == "Ace"
    assert card.color == "Red"
    assert not card.flipped

    card = Card("spades", 13)
    assert card.suit == "Spades"
    assert card.value == 13
    assert card.name == "King"
    assert card.color == "Black"

def test_card_initialization_invalid_suit():
    """Test that invalid suits raise ValueError."""
    with pytest.raises(ValueError, match="Invalid suit"):
        Card("Joker", 1)
    
    with pytest.raises(ValueError, match="Invalid suit"):
        Card("NotASuit", 5)

def test_card_initialization_invalid_value():
    """Test that invalid values raise ValueError."""
    with pytest.raises(ValueError, match="Invalid value"):
        Card("Hearts", 0)
    
    with pytest.raises(ValueError, match="Invalid value"):
        Card("Diamonds", 14)
    
    with pytest.raises(ValueError, match="Invalid value"):
        Card("Clubs", -1)

def test_card_flip():
    """Test the flip method."""
    card = Card("Clubs", 10)
    assert not card.flipped
    card.flip()
    assert card.flipped
    card.flip()
    assert not card.flipped

def test_card_print_full_name(capsys):
    """Test the print_full_name method."""
    card = Card("Diamonds", 11)
    card.print_full_name()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Jack of Diamonds"
