import pytest
from solitaire.models.deck import Deck
from solitaire.models.card import Card

def test_deck_initialization():
    """Test that a deck initializes with 52 cards, and no duplicates."""
    deck = Deck()
    assert len(deck.cards) == 52
    
    # Check that all suits and values are present
    suits = set()
    values = set()
    cards_set = set()
    
    for card in deck.cards:
        suits.add(card.suit)
        values.add(card.value)
        cards_set.add((card.suit, card.value))
        
    assert len(suits) == 4
    assert len(values) == 13
    assert len(cards_set) == 52

def test_deck_shuffle():
    """Test that shuffling the deck changes the order of cards."""
    deck1 = Deck()
    deck2 = Deck()
    
    # Initially they might be in the same order if the constructor is deterministic
    # Let's assume the constructor creates them in a fixed order.
    
    deck2.shuffle()
    
    # It's technically possible but highly unlikely for a shuffle to result in the same order
    assert [ (c.suit, c.value) for c in deck1.cards ] != [ (c.suit, c.value) for c in deck2.cards ]

def test_deck_draw():
    """Test drawing a card from the deck."""
    deck = Deck()
    initial_count = len(deck.cards)
    
    card = deck.draw()
    assert isinstance(card, Card)
    assert len(deck.cards) == initial_count - 1
    
    # Draw all cards
    for _ in range(51):
        deck.draw()
    
    assert len(deck.cards) == 0
    
    # Drawing from an empty deck should probably return None or raise an error
    with pytest.raises(IndexError):
        deck.draw()

def test_deck_remaining_count():
    """Test the count of remaining cards."""
    deck = Deck()
    assert len(deck) == 52
    deck.draw()
    assert len(deck) == 51
