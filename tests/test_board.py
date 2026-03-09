from collections import deque
from solitaire.models.board import Board

def test_board_initialization():
    """Test that the board initializes with correct fields and types."""
    board = Board()
    
    # Check foundations (should be 4 empty lists)
    assert len(board.foundation) == 4
    for f in board.foundation:
        assert isinstance(f, list)
        assert len(f) == 0
        
    # Check tableau (should be 7 lists)
    assert len(board.tableau) == 7
    for i, t in enumerate(board.tableau):
        assert isinstance(t, list)
        assert len(t) == i + 1
        
    # Check stock (should be a deque instance)
    assert isinstance(board.stock, deque)
    # 52 cards - (1+2+3+4+5+6+7) = 52 - 28 = 24
    assert len(board.stock) == 24
    
    # Check waste (should be an empty list)
    assert isinstance(board.waste, list)
    assert len(board.waste) == 0

def test_tableau_card_visibility():
    """
    Test that all cards in the tableau are NOT flipped (shown)
    unless they are the last one in the list.
    """
    board = Board()
    for pile in board.tableau:
        for i, card in enumerate(pile):
            if i == len(pile) - 1:
                assert card.flipped is True, f"Last card in pile of size {len(pile)} should be flipped"
            else:
                assert card.flipped is False, f"Card at index {i} in pile of size {len(pile)} should NOT be flipped"

def test_solitaire_setup():
    """
    Test that tableau, waste, stock, and foundations have the proper set-up for solitaire.
    """
    board = Board()
    
    # Foundation: 4 empty lists
    assert len(board.foundation) == 4
    assert all(len(f) == 0 for f in board.foundation)
    
    # Tableau: 7 piles with 1, 2, 3, 4, 5, 6, 7 cards
    assert len(board.tableau) == 7
    for i in range(7):
        assert len(board.tableau[i]) == i + 1
        
    # Waste: Empty list
    assert isinstance(board.waste, list)
    assert len(board.waste) == 0
    
    # Stock: 24 cards remaining (52 - 28)
    assert len(board.stock) == 24

    # The first card in stock should be flipped, the rest should be face down (not flipped)
    for i, card in enumerate(board.stock):
        if i == 0:
            assert card.flipped is True
        else:
            assert card.flipped is False
