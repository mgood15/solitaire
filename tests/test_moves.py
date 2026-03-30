import pytest
from solitaire.models.board import Board
from solitaire.models.card import Card

def test_move_within_tableau():
    board = Board()
    # Ensure source pile has at least one card
    source_idx = 1
    dest_idx = 2
    initial_source_len = len(board.tableau[source_idx])
    initial_dest_len = len(board.tableau[dest_idx])
    
    success = board.move_card(source_type="tableau", source_idx=source_idx, 
                              dest_type="tableau", dest_idx=dest_idx, num_cards=1)
    
    assert success is True
    assert len(board.tableau[source_idx]) == initial_source_len - 1
    assert len(board.tableau[dest_idx]) == initial_dest_len + 1

def test_move_tableau_to_foundation():
    board = Board()
    source_idx = 0
    dest_idx = 0
    initial_source_len = len(board.tableau[source_idx])
    
    success = board.move_card(source_type="tableau", source_idx=source_idx, 
                              dest_type="foundation", dest_idx=dest_idx)
    
    assert success is True
    assert len(board.tableau[source_idx]) == initial_source_len - 1
    assert len(board.foundation[dest_idx]) == 1

def test_move_waste_to_tableau():
    board = Board()
    # Use draw_from_stock to put card in waste
    board.draw_from_stock()
    
    dest_idx = 0
    initial_dest_len = len(board.tableau[dest_idx])
    
    success = board.move_card(source_type="waste", dest_type="tableau", dest_idx=dest_idx)
    
    assert success is True
    assert len(board.waste) == 0
    assert len(board.tableau[dest_idx]) == initial_dest_len + 1

def test_auto_flip_after_move():
    board = Board()
    # Ensure pile 1 has 2 cards, top is flipped, bottom is not.
    assert len(board.tableau[1]) == 2
    assert board.tableau[1][1].flipped is True
    assert board.tableau[1][0].flipped is False
    
    # Move the top card away
    board.move_card(source_type="tableau", source_idx=1, dest_type="foundation", dest_idx=0)
    
    # The remaining card in pile 1 should now be flipped
    assert len(board.tableau[1]) == 1
    assert board.tableau[1][0].flipped is True

def test_move_multiple_cards_tableau():
    board = Board()
    # Pile 2 has 3 cards. Let's move 2 cards to pile 3.
    # (Note: In real Solitaire only face-up cards can be moved together, 
    # but our stub allows it for now)
    source_idx = 2
    dest_idx = 3
    
    success = board.move_card(source_type="tableau", source_idx=source_idx, 
                              dest_type="tableau", dest_idx=dest_idx, num_cards=2)
    
    assert success is True
    assert len(board.tableau[source_idx]) == 1
    assert len(board.tableau[dest_idx]) == 6 # 4 initial + 2 moved

def test_invalid_move_returns_false():
    board = Board()
    # Invalid source type
    success = board.move_card(source_type="invalid", dest_type="tableau", dest_idx=0)
    assert success is False
    
    # Invalid destination type
    success = board.move_card(source_type="waste", dest_type="invalid")
    assert success is False
