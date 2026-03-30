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
TABLEAU_Y = CARD_MARGIN * 2 + CARD_HEIGHT
TABLEAU_X_START = CARD_MARGIN
FOUNDATION_X_START = SCREEN_WIDTH - (4 * (CARD_WIDTH + CARD_MARGIN)) - CARD_MARGIN
STOCK_X = CARD_MARGIN
STOCK_Y = CARD_MARGIN
WASTE_X = CARD_MARGIN + CARD_WIDTH + CARD_MARGIN
WASTE_Y = CARD_MARGIN

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

    def draw_board(self, board, dragging_info=None):
        # Draw Stock
        if board.stock:
            # Stock is always face-down
            rect = pygame.Rect(STOCK_X, STOCK_Y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, GRAY, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
        else:
            self.draw_empty_slot(STOCK_X, STOCK_Y)
            
        # Draw Waste (Fanned out top 3)
        if board.waste:
            waste_to_draw = board.waste[-3:]
            # If the top card is being dragged, we don't draw it in its original place
            dragging_from_waste = dragging_info and dragging_info['source']['type'] == 'waste'
            
            num_cards = len(waste_to_draw)
            for i, card in enumerate(waste_to_draw):
                # If it's the top card and it's being dragged, skip it
                if dragging_from_waste and i == num_cards - 1:
                    continue
                
                # Offset each card slightly to the right to fan them
                fan_offset = i * 20
                self.draw_card(card, WASTE_X + fan_offset, WASTE_Y)
        else:
            self.draw_empty_slot(WASTE_X, WASTE_Y)

        # Draw Foundations
        for i, pile in enumerate(board.foundation):
            x = FOUNDATION_X_START + i * (CARD_WIDTH + CARD_MARGIN)
            y = CARD_MARGIN
            # Check if foundation top card is being dragged
            if dragging_info and dragging_info['source']['type'] == 'foundation' and dragging_info['source']['idx'] == i:
                if len(pile) > 1:
                    self.draw_card(pile[-2], x, y)
                else:
                    self.draw_empty_slot(x, y)
            elif pile:
                self.draw_card(pile[-1], x, y)
            else:
                self.draw_empty_slot(x, y)

        # Draw Tableau
        for i, pile in enumerate(board.tableau):
            x = TABLEAU_X_START + i * (CARD_WIDTH + CARD_MARGIN)
            if not pile:
                self.draw_empty_slot(x, TABLEAU_Y)
            else:
                # If dragging from this pile, only draw cards NOT being dragged
                num_to_draw = len(pile)
                if dragging_info and dragging_info['source']['type'] == 'tableau' and dragging_info['source']['idx'] == i:
                    num_to_draw -= dragging_info['source']['num_cards']

                for j in range(num_to_draw):
                    card = pile[j]
                    self.draw_card(card, x, TABLEAU_Y + j * 20)

        # Draw dragging cards last
        if dragging_info:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            offset_x, offset_y = dragging_info['offset']
            for j, card in enumerate(dragging_info['cards']):
                self.draw_card(card, mouse_x - offset_x, mouse_y - offset_y + j * 20)

def get_component_at_pos(pos):
    """Returns (type, idx, num_cards) or None."""
    x, y = pos
    
    # Check Stock
    if STOCK_X <= x <= STOCK_X + CARD_WIDTH and STOCK_Y <= y <= STOCK_Y + CARD_HEIGHT:
        return {"type": "stock", "idx": 0}

    # Check Waste
    num_waste = 0
    # Assuming we can get access to board here to know the number of cards in waste, 
    # but get_component_at_pos only takes pos.
    # However, in main() we have the board.
    # Let's adjust the detection to account for the fanning.
    # The topmost card in waste is at WASTE_X + (min(3, len(waste))-1) * 20
    # For now, let's keep it simple and check the general area.
    # We'll refine it in the main loop where we have the board.
    if WASTE_X <= x <= WASTE_X + CARD_WIDTH + 40 and WASTE_Y <= y <= WASTE_Y + CARD_HEIGHT:
        return {"type": "waste", "idx": 0}

    # Check Foundation
    for i in range(4):
        f_x = FOUNDATION_X_START + i * (CARD_WIDTH + CARD_MARGIN)
        if f_x <= x <= f_x + CARD_WIDTH and CARD_MARGIN <= y <= CARD_MARGIN + CARD_HEIGHT:
            return {"type": "foundation", "idx": i}

    # Check Tableau
    for i in range(7):
        t_x = TABLEAU_X_START + i * (CARD_WIDTH + CARD_MARGIN)
        if t_x <= x <= t_x + CARD_WIDTH and y >= TABLEAU_Y:
            return {"type": "tableau", "idx": i}
            
    return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Solitaire")
    clock = pygame.time.Clock()
    
    board = Board()
    renderer = Renderer(screen)
    
    dragging_info = None
    
    last_click_pos = None
    last_click_time = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    last_click_pos = event.pos
                    last_click_time = pygame.time.get_ticks()
                    
                    comp = get_component_at_pos(event.pos)
                    if not comp:
                        continue
                    
                    # Start dragging logic for everything
                    source_type = comp['type']
                    idx = comp['idx']
                    
                    cards_to_drag = []
                    if source_type == 'waste' and board.waste:
                        cards_to_drag = [board.waste[-1]]
                    elif source_type == 'foundation' and board.foundation[idx]:
                        cards_to_drag = [board.foundation[idx][-1]]
                    elif source_type == 'tableau' and board.tableau[idx]:
                        # Identify which card in the stack was clicked
                        pile = board.tableau[idx]
                        card_idx = (event.pos[1] - TABLEAU_Y) // 20
                        card_idx = min(max(0, card_idx), len(pile) - 1)
                        
                        # Can only drag face-up cards
                        if pile[card_idx].flipped:
                            cards_to_drag = pile[card_idx:]
                    
                    if cards_to_drag:
                        # Ensure card is flipped if it comes from waste
                        # (Already flipped by Board when drawn, but let's be sure for visual consistency)
                        if source_type == 'waste':
                            cards_to_drag[0].flipped = True
                        
                        # Calculate offset (where within the card we clicked)
                        # For tableau, we care about the card we clicked
                        # For simplicity, just use the first card's position
                        if source_type == 'tableau':
                            pile = board.tableau[idx]
                            start_x = TABLEAU_X_START + idx * (CARD_WIDTH + CARD_MARGIN)
                            start_y = TABLEAU_Y + pile.index(cards_to_drag[0]) * 20
                        elif source_type == 'waste':
                            fan_offset = (min(3, len(board.waste)) - 1) * 20
                            start_x = WASTE_X + fan_offset
                            start_y = WASTE_Y
                        else: # foundation (already handled by elif)
                            start_x = FOUNDATION_X_START + idx * (CARD_WIDTH + CARD_MARGIN)
                            start_y = CARD_MARGIN

                        offset = (event.pos[0] - start_x, event.pos[1] - start_y)
                        
                        dragging_info = {
                            "cards": cards_to_drag,
                            "source": {"type": source_type, "idx": idx, "num_cards": len(cards_to_drag)},
                            "offset": offset
                        }

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Check for "click" (minimal movement and short time)
                    curr_time = pygame.time.get_ticks()
                    if last_click_pos:
                        dx = abs(event.pos[0] - last_click_pos[0])
                        dy = abs(event.pos[1] - last_click_pos[1])
                        # If it was a short click without much movement
                        if dx < 5 and dy < 5 and (curr_time - last_click_time) < 250:
                            comp = get_component_at_pos(event.pos)
                            if comp and (comp['type'] == 'stock' or comp['type'] == 'waste'):
                                board.draw_from_stock()
                                dragging_info = None # Cancel drag if it was intended as a click
                    
                    if dragging_info:
                        dest = get_component_at_pos(event.pos)
                        
                        move_success = False
                        if dest and dest['type'] in ['tableau', 'foundation']:
                            source = dragging_info['source']
                            move_success = board.move_card(
                                source_type=source['type'],
                                source_idx=source['idx'],
                                dest_type=dest['type'],
                                dest_idx=dest['idx'],
                                num_cards=source['num_cards']
                            )
                        
                        # If move failed and it was from waste, ensure it's still flipped
                        if not move_success and dragging_info['source']['type'] == 'waste':
                            dragging_info['cards'][0].flipped = True
                        
                        dragging_info = None
                    last_click_pos = None

        screen.fill(BACKGROUND_COLOR)
        renderer.draw_board(board, dragging_info)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()