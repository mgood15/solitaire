from solitaire.models.board import Board
from solitaire.models.card import Card

def test_draw_from_stock():
    board = Board()
    initial_stock_len = len(board.stock)
    initial_waste_len = len(board.waste)
    
    # Stock should be face-down initially
    assert board.stock[0].flipped is False
    
    # Draw one card
    assert board.draw_from_stock() is True
    assert len(board.stock) == initial_stock_len - 1
    assert len(board.waste) == 1
    # Card in waste should be flipped
    assert board.waste[0].flipped is True
    # Next card in stock remains face-down
    if board.stock:
        assert board.stock[0].flipped is False
    
def test_stock_cycle():
    board = Board()
    stock_len = len(board.stock)
    
    # Draw all cards to waste
    for i in range(stock_len):
        assert board.draw_from_stock() is True
        
    assert len(board.stock) == 0
    assert len(board.waste) == stock_len
    # All waste cards should be flipped
    for card in board.waste:
        assert card.flipped is True
    
    # Draw again should reset stock
    assert board.draw_from_stock() is True
    assert len(board.stock) == stock_len
    assert len(board.waste) == 0
    # All stock cards should be face down after reset
    for i in range(stock_len):
        assert board.stock[i].flipped is False

