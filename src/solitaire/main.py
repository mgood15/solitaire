import pygame
from solitaire.models.board import Board

# Constants for the game window and layout
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BACKGROUND_COLOR = (0, 128, 0)  # Classic green solitaire background
CARD_WIDTH = 80
CARD_HEIGHT = 120
CARD_MARGIN = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 14)

    def draw_card(self, card, x, y):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        if not card.flipped:
            pygame.draw.rect(self.screen, GRAY, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
        else:
            pygame.draw.rect(self.screen, WHITE, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            
            color = RED if card.color == "Red" else BLACK
            
            # Full text representation of the card
            name_text = self.font.render(card._actual_name, True, color)
            suit_text = self.font.render(card.suit, True, color)
            self.screen.blit(name_text, (x + 5, y + 5))
            self.screen.blit(suit_text, (x + 5, y + 25))

    def draw_empty_slot(self, x, y):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(self.screen, (0, 100, 0), rect, 2)

    def draw_board(self, board):
        # Draw Stock and Waste
        stock_x = CARD_MARGIN
        stock_y = CARD_MARGIN
        if board.stock:
            self.draw_card(board.stock[0], stock_x, stock_y)
        else:
            self.draw_empty_slot(stock_x, stock_y)
            
        waste_x = stock_x + (CARD_WIDTH + CARD_MARGIN)
        waste_y = CARD_MARGIN
        if board.waste:
            self.draw_card(board.waste[-1], waste_x, waste_y)
        else:
            self.draw_empty_slot(waste_x, waste_y)

        # Draw Foundations on the right
        found_end_x = SCREEN_WIDTH - CARD_MARGIN - CARD_WIDTH
        for i, pile in enumerate(reversed(board.foundation)):
            x = found_end_x - i * (CARD_WIDTH + CARD_MARGIN)
            y = CARD_MARGIN
            if pile:
                self.draw_card(pile[-1], x, y)
            else:
                self.draw_empty_slot(x, y)

        # Draw Tableau
        tableau_start_x = CARD_MARGIN
        tableau_y = CARD_MARGIN * 2 + CARD_HEIGHT
        for i, pile in enumerate(board.tableau):
            x = tableau_start_x + i * (CARD_WIDTH + CARD_MARGIN)
            if not pile:
                self.draw_empty_slot(x, tableau_y)
            else:
                for j, card in enumerate(pile):
                    # Stack cards vertically in tableau
                    self.draw_card(card, x, tableau_y + j * 20)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Solitaire")
    clock = pygame.time.Clock()
    
    board = Board()
    renderer = Renderer(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    mouse_x, mouse_y = event.pos
                    # Check if Stock was clicked
                    stock_x = CARD_MARGIN
                    stock_rect = pygame.Rect(stock_x, CARD_MARGIN, CARD_WIDTH, CARD_HEIGHT)
                    if stock_rect.collidepoint(mouse_x, mouse_y):
                        if board.stock:
                            # Draw from stock
                            card = board.stock.popleft()
                            # Cards in waste should be face down
                            # If it was face up, flip it face down.
                            if card.flipped:
                                card.flip()
                            board.waste.append(card)
                            # Flip the next card in stock face-up
                            if board.stock and not board.stock[0].flipped:
                                board.stock[0].flip()
                        elif board.waste:
                            # Refill stock from waste if empty
                            while board.waste:
                                card = board.waste.pop()
                                if card.flipped:
                                    card.flip()
                                board.stock.append(card) # append to end
                            # Flip the first card of new stock face-up
                            if board.stock and not board.stock[0].flipped:
                                board.stock[0].flip()
        
        screen.fill(BACKGROUND_COLOR)
        renderer.draw_board(board)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()