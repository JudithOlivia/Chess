import pygame 
import sys

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

White = (255, 255, 255)
Black = (0, 0, 0)
Light_brown = (240, 217, 181)
Dark_brown = (181, 136, 99)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

class Piece:
    def __init__(self, row, col, color, piece_type):
        self.row = row
        self.col = col
        self.color = color
        self.piece_type = piece_type
        self.moved = False

    def __repr__(self):
        return f"{self.color[0]}{self.piece_type[0]}"

class Board:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.create_board()
        self.current_turn = 'white'

    def create_board(self):
        for col in range(COLS):
            self.board[1][col] = Piece(1, col, 'black', 'pawn')
            self.board[6][col] = Piece(6, col, 'white', 'pawn')

        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']

        for col, piece_type in enumerate(piece_order):
            self.board[0][col] = Piece(0, col, 'black', piece_type)
            self.board[7][col] = Piece(7, col, 'white', piece_type)

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
            pygame.quit()
            sys.exit()

    for row in range(ROWS):
        for col in range(COLS):
            color = Light_brown if (row + col) % 2 == 0 else Dark_brown 
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

board = Board()
for row in range(ROWS):
    for col in range(COLS):
        piece = board.board[row][col]
        if piece:
            print(piece, end=' ')
    print()

    pygame.display.update()