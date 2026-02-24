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
        self.selected_piece = None 
        self.valid_moves = []

    def create_board(self):
        for col in range(COLS):
            self.board[1][col] = Piece(1, col, 'black', 'pawn')
            self.board[6][col] = Piece(6, col, 'white', 'pawn')

        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']

        for col, piece_type in enumerate(piece_order):
            self.board[0][col] = Piece(0, col, 'black', piece_type)
            self.board[7][col] = Piece(7, col, 'white', piece_type)

    def get_valid_moves(self, piece):
        moves = []

        if piece.piece_type == 'pawn':
            direction = -1 if piece.color == 'white' else 1

            if 0 <= piece.row + direction < 8 and not self.board[piece.row + direction][piece.col]:
                moves.append((piece.row + direction, piece.col))

            for dcol in [-1, 1]:
                new_row, new_col = piece.row + direction, piece.col + dcol 
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target and target.color != piece.color:
                        moves.append((new_row, new_col))
        return moves
    
    def move_piece(self, piece, new_row, new_col):
        self.board[piece.row][piece.col] = None
        piece.row = new_row
        piece.col = new_col
        self.board[new_row][new_col] = piece
        piece.moved = True

    
    def handle_click(self, row, col):
        clicked_piece = self.board[row][col]

        if clicked_piece and clicked_piece.color == self.current_turn:
            self.selected_piece = clicked_piece
            self.valid_moves = self.get_valid_moves(clicked_piece)

        elif self.selected_piece and (row, col) in self.valid_moves:
            self.move_piece(self.selected_piece, row, col)
            self.selected_piece = None 
            self.valid_moves = []
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'


running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
            pygame.quit()
            sys.exit()
        if not game_over and board.current_turn == 'white':
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                board.handle_click(row, col)

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

test_pawn = board.board[6][0]
moves = board.get_valid_moves(test_pawn)
print(f"Pawn moves: {moves}")

pygame.display.update()