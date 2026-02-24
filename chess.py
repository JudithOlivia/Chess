import pygame 
import sys
import math

PIECE_VALUES = {
    'pawn': 100,
    'knight': 320,
    'bishop': 330,
    'rook': 500,
    'queen': 900,
    'king': 20000 
}

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

White = (255, 255, 255)
Black = (0, 0, 0)
Light_brown = (240, 217, 181)
Dark_brown = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)  
MOVE_HIGHLIGHT = (130, 151, 105)  

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
    
        elif piece.piece_type == 'rook':
            directions = [(0,1), (0,-1), (1,0), (-1,0)]
            for dr, dc in directions:
                for i in range(1, 8):
                    new_row, new_col = piece.row + dr*i, piece.col + dc*i
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        target = self.board[new_row][new_col]
                        if not target:
                            moves.append((new_row, new_col))
                        elif target.color != piece.color:
                            moves.append((new_row, new_col))
                            break
                        else:
                            break
                    else:
                        break
        
        elif piece.piece_type == 'knight':
            jumps = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                    (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in jumps:
                new_row, new_col = piece.row + dr, piece.col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if not target or target.color != piece.color:
                        moves.append((new_row, new_col))
        return moves

    def evaluate_board(self):
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    value = PIECE_VALUES[piece.piece_type]
                    if piece.color == 'white':
                        score += value
                    else:
                        score -= value
        return score
    
    
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

    def get_all_moves(self, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for move in self.get_valid_moves(piece):
                        moves.append((piece, move[0], move[1]))
        return moves

class ChessAI:
    def __init__(self, depth=2):
        self.depth = depth 

    def minimax(self, board, depth, alpha, beta, maximizing):
        if depth == 0:
            return board.evaluate_board()
        if maximizing:
            max_eval = -math.inf
            for move in board.get_all_moves('white'):
                piece, new_row, new_col = move 
                old_row, old_col, = piece.row, piece.col 
                target = board.board[new_row][new_col]

                board.move_piece(piece, new_row, new_col)

                eval = self.minimax(board, depth - 1, alpha, beta, False)

                board.board[old_row][old_col] = piece.piece.row, piece.col = old_row, old_col 
                board.board[new_row][new_col] = target

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        
        else:
            min_eval = math.inf
            for move in board.get_all_moves('black'):
                piece, new_row, new_col = move
                old_row, old_col = piece.row, piece.col
                target = board.board[new_row][new_col]

                board.move_piece(piece, new_row, new_col)

                eval = self.minimax(board, depth - 1, alpha, beta, True)

                board.board[old_row][old_col] = piece
                piece.row, piece.col = old_row, old_col
                board.board[new_row][new_col] = target

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
        
    
    def get_best_move(self, board):
        best_move = None
        best_value = -math.inf

        for move in board.get_all_moves('black'):
            piece, new_row, new_col = move
            old_row, old_col = piece.row, piece.col 
            target = board.board[new_row][new_col]

            board.move_piece(piece, new_row, new_col)

            move_value = self.minimax(board, self.depth-1, -math.inf, math.inf, True)

            board.board[old_row][old_col] = piece
            piece.row, piece.col = old_row, old_col
            board.board[new_row][new_col] = target

            if move_value > best_value:
                best_value = move_value
                best_move = move 

        return best_move



board = Board()
game_over = False 
running = True

ai = ChessAI(depth=2)

for row in range(ROWS):
    for col in range(COLS):
        piece = board.board[row][col]
        if piece:
            print(piece, end=' ')
    print()

test_pawn = board.board[6][0]
moves = board.get_valid_moves(test_pawn)
print(f"Pawn moves: {moves}")

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

if board.current_turn == 'black':
    best_move = ai.get_best_move(board)
    if best_move:
        piece, new_row, new_col = best_move
        board.move_piece(piece, new_row, new_col)
        board.current_turn = 'white'
    pygame.time.wait(500)

for row in range(ROWS):
    for col in range(COLS):
        piece = board.board[row][col]
        if piece:
           pass

if board.selected_piece: 
    pygame.draw.rect(win, HIGHLIGHT, 
                     (board.selected_piece.col * SQUARE_SIZE,
                      board.selected_piece.row * SQUARE_SIZE,
                      SQUARE_SIZE, SQUARE_SIZE), 4)
    
for move in board.valid_moves: 
    row, col = move 
    pygame.draw.circle(win, MOVE_HIGHLIGHT, 
                       (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2),5 )

for row in range(ROWS):
        for col in range(COLS):
            piece = board.board[row][col]
            if piece:
                color = White if piece.color == 'white' else Black
                pygame.draw.circle(win, color, 
                                 (col * SQUARE_SIZE + SQUARE_SIZE//2,
                                  row * SQUARE_SIZE + SQUARE_SIZE//2), 25)

pygame.display.update()