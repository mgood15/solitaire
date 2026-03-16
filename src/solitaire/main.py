from solitaire.models.board import Board

def game_setup():
    board = Board()
    board.print_board()

def main():
    print("Hello world!")
    game_setup()

if __name__ == "__main__":
    main()