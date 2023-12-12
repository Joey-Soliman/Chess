import pygame
from constants import ROWS, COLS, SQUARE_SIZE, WHITE, BLACK, GREEN, BOARD_HEIGHT, BOARD_WIDTH
from pieces import King, Queen, Bishop, Knight, Rook, Pawn, Empty


class ChessBoard:
    def __init__(self):
        # Initialize the board
        # Create the pieces
        black_king = King('black', (0,4))
        black_queen = Queen('black', (0,3))
        black_bishop = Bishop('black', (0,2))
        black_bishop2 = Bishop('black', (0,5))
        black_knight = Knight('black', (0,1))
        black_knight2 = Knight('black', (0,6))
        black_rook = Rook('black', (0,0))
        black_rook2 = Rook('black', (0,7))
        black_pawn = Pawn('black', (1,0))
        black_pawn2 = Pawn('black', (1,1))
        black_pawn3 = Pawn('black', (1,2))
        black_pawn4 = Pawn('black', (1,3))
        black_pawn5 = Pawn('black', (1,4))
        black_pawn6 = Pawn('black', (1,5))
        black_pawn7 = Pawn('black', (1,6))
        black_pawn8 = Pawn('black', (1,7))

        white_king = King('white', (7,4))
        white_queen = Queen('white', (7,3))
        white_bishop = Bishop('white', (7,2))
        white_bishop2 = Bishop('white', (7,5))
        white_knight = Knight('white', (7,1))
        white_knight2 = Knight('white', (7,6))
        white_rook = Rook('white', (7,0))
        white_rook2 = Rook('white', (7,7))
        white_pawn = Pawn('white', (6,0))
        white_pawn2 = Pawn('white', (6,1))
        white_pawn3 = Pawn('white', (6,2))
        white_pawn4 = Pawn('white', (6,3))
        white_pawn5 = Pawn('white', (6,4))
        white_pawn6 = Pawn('white', (6,5))
        white_pawn7 = Pawn('white', (6,6))
        white_pawn8 = Pawn('white', (6,7))

        empty_piece = Empty()

        self.chess_board = [[Empty() for _ in range(COLS)] for _ in range(ROWS)]

        self.chess_board[0] = [black_rook, black_knight, black_bishop, black_queen, black_king, black_bishop2, black_knight2, black_rook2]
        self.chess_board[1] = [black_pawn, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8]
        self.chess_board[6] = [white_pawn, white_pawn2, white_pawn3, white_pawn4, white_pawn5, white_pawn6, white_pawn7, white_pawn8]
        self.chess_board[7] = [white_rook, white_knight, white_bishop, white_queen, white_king, white_bishop2, white_knight2, white_rook2]

        self.black_pieces = [black_rook, black_knight, black_bishop, black_queen, black_king, black_bishop2, black_knight2, black_rook2,
                             black_pawn, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8]
        self.white_pieces = [white_rook, white_knight, white_bishop, white_queen, white_king, white_bishop2, white_knight2, white_rook2,
                             white_pawn, white_pawn2, white_pawn3, white_pawn4, white_pawn5, white_pawn6, white_pawn7, white_pawn8]

        self.black_pieces_taken = []
        self.white_pieces_taken = []

        self.piece = None
        self.position = None
        self.dragging = False
        self.moves = []

    
        
    def render(self, win):
        transparent_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)  # Transparent surface to draw indicators on
        # Render the board
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                # Render the pieces
                piece = self.chess_board[row][col]
                if not isinstance(piece, Empty):  # Check if the square is not empty
                    # Calculate offsets to center the piece within the square
                    offset_x = col * SQUARE_SIZE + (SQUARE_SIZE - piece.image.get_width()) // 2
                    offset_y = row * SQUARE_SIZE + (SQUARE_SIZE - piece.image.get_height()) // 2

                    win.blit(piece.image, (offset_x, offset_y))

                # Draw indicator transparent green square over piece starting position
                if piece == self.piece and self.dragging:        
                    pygame.draw.rect(transparent_surface, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw indicators for valid moves
                if (row, col) in self.moves and self.dragging:
                    drag_col = self.position[0] // SQUARE_SIZE
                    drag_row = self.position[1] // SQUARE_SIZE
                    if drag_col == col and drag_row == row:
                        pygame.draw.rect(transparent_surface, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    else:
                        if not isinstance(self.chess_board[row][col], Empty):   # Check if not empty and green triangle for indicator                     
                            vertices = [(col * SQUARE_SIZE, row * SQUARE_SIZE), 
                                        (col * SQUARE_SIZE + SQUARE_SIZE / 5, row * SQUARE_SIZE), 
                                        (col * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE / 5)]
                            pygame.draw.polygon(transparent_surface, GREEN, vertices)
                        else:   # Green circles for indicators for valid moves into free spaces
                            pygame.draw.circle(transparent_surface, GREEN, (col * SQUARE_SIZE + (SQUARE_SIZE / 2), row * SQUARE_SIZE + (SQUARE_SIZE / 2)), 20)

        win.blit(transparent_surface, (0, 0))
                         
                
        # Render dragging piece
        if self.piece is not None and self.dragging:
            offset_x = self.position[0] - self.piece.image.get_width() // 2
            offset_y = self.position[1] - self.piece.image.get_height() // 2
            win.blit(self.piece.image, (offset_x, offset_y))



    def drag_piece(self, piece, position, moves):
        # TODO: Add a translucent film over the square
        # Copy the piece image and add to render
        self.dragging = True
        self.piece = piece
        self.position = position
        self.moves = moves

    
    def stop_drag(self):
        self.dragging = False  


    def update_piece(self, piece, new_row, new_col):
        # Find current position of piece and remove piece
        for row_index, row in enumerate(self.chess_board):
            for col_index, board_piece in enumerate(row):
                if board_piece == piece:
                    empty_piece = Empty()
                    self.chess_board[row_index][col_index] = empty_piece    # Remove piece from original position and replace with empty piece
                    # Check if new spot has a piece, if so, add that piece to list of taken pieces and remove from list of current pieces
                    old_piece = self.chess_board[new_row][new_col]
                    if not isinstance(old_piece, Empty):
                        if old_piece.color == 'white':
                            self.white_pieces.remove(old_piece)
                            self.white_pieces_taken.append(old_piece)
                        else:
                            self.black_pieces.remove(old_piece)
                            self.black_pieces_taken.append(old_piece)
                    self.chess_board[new_row][new_col] = piece  # Add piece to new position
                    return



class Move:
    def __init__(self, piece, row, col):
        self.piece = piece
        self.row = row
        self.col = col

    def updateMove(self, piece, row, col):
        self.piece = piece
        self.row = row
        self.col = col