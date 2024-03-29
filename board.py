import pygame
import copy
from constants import ROWS, COLS, SQUARE_SIZE, WHITE, BLACK, GREEN, YELLOW, RED, GREY, ORANGE, BOARD_HEIGHT, BOARD_WIDTH, PIECE_WIDTH, PIECE_HEIGHT
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
        self.check_pos = None   # Position of King under check
        self.check_color = None # Color of King under check
        self.lastMove = Move()  # Keeps track of last move (piece, old_row, old_col, new_row, new_col)
        self.lastMoves = [self.lastMove]    # Keeps track of all moves
        self.white_win = False
        self.stalemate = False
        self.black_win = False
        self.pawn_back_rank = None

    
        
    def render(self, win):
        transparent_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)  # Transparent surface to draw indicators on
        # Render the board
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                # Draw indicator for last move -  yellow squares
                if row == self.lastMove.old_row and col == self.lastMove.old_col:
                    pygame.draw.rect(win, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if row == self.lastMove.new_row and col == self.lastMove.new_col:
                    pygame.draw.rect(win, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                # Render the pieces
                piece = self.chess_board[row][col]
                if not isinstance(piece, Empty):  # Check if the square is not empty
                    # Calculate offsets to center the piece within the square
                    offset_x = col * SQUARE_SIZE + (SQUARE_SIZE - piece.image.get_width()) // 2
                    offset_y = row * SQUARE_SIZE + (SQUARE_SIZE - piece.image.get_height()) // 2

                    win.blit(piece.image, (offset_x, offset_y))

                # Draw indicator over starting position - transparent green square
                if piece == self.piece and self.dragging:        
                    pygame.draw.rect(transparent_surface, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw indicators for valid moves
                if (row, col) in self.moves and self.dragging:
                    drag_col = self.position[0] // SQUARE_SIZE
                    drag_row = self.position[1] // SQUARE_SIZE
                    if drag_col == col and drag_row == row:
                        pygame.draw.rect(transparent_surface, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    else:
                        if not isinstance(self.chess_board[row][col], Empty):   # Check if not empty and add green triangle for indicator                     
                            vertices = [(col * SQUARE_SIZE, row * SQUARE_SIZE), 
                                        (col * SQUARE_SIZE + SQUARE_SIZE / 5, row * SQUARE_SIZE), 
                                        (col * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE / 5)]
                            pygame.draw.polygon(transparent_surface, GREEN, vertices)
                        else:   # Green circles for indicators for valid moves into free spaces
                            pygame.draw.circle(transparent_surface, GREEN, (col * SQUARE_SIZE + (SQUARE_SIZE / 2), row * SQUARE_SIZE + (SQUARE_SIZE / 2)), 20)
                
                # Draw indicator for check
                if (row, col) == self.check_pos:
                    pygame.draw.circle(transparent_surface, RED, (col * SQUARE_SIZE + (SQUARE_SIZE / 2), row * SQUARE_SIZE + (SQUARE_SIZE / 2)), 48)

        win.blit(transparent_surface, (0, 0))
                                   
        # Render dragging piece
        if self.piece is not None and self.dragging:
            offset_x = self.position[0] - self.piece.image.get_width() // 2
            offset_y = self.position[1] - self.piece.image.get_height() // 2
            win.blit(self.piece.image, (offset_x, offset_y))


        if self.pawn_back_rank != None:
            self.draw_pawn_promote(win)



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
                    dead_pawn = None
                    if not isinstance(old_piece, Empty):    # Check if new spot is not empty
                        if old_piece.color == 'white':
                            self.white_pieces.remove(old_piece)
                            self.white_pieces_taken.append(old_piece)
                        else:
                            self.black_pieces.remove(old_piece)
                            self.black_pieces_taken.append(old_piece)
                    else:   # if spot is empty check for en passant
                        if isinstance(piece, Pawn) and col_index != new_col:    # Check if piece is pawn and moved diagonally
                            if piece.color == 'white':
                                dead_pawn = self.chess_board[new_row + 1][new_col]
                                self.black_pieces.remove(dead_pawn)
                                self.black_pieces_taken.append(dead_pawn)
                                empty_piece = Empty()
                                self.chess_board[new_row + 1][new_col] = empty_piece
                            else:
                                dead_pawn = self.chess_board[new_row - 1][new_col]
                                self.white_pieces.remove(dead_pawn)
                                self.white_pieces_taken.append(dead_pawn)
                                empty_piece = Empty()
                                self.chess_board[new_row - 1][new_col] = empty_piece
                        # Check for castle
                        if isinstance(piece, King):    # Check if piece is king
                            if new_col == col_index + 2:    # Right side castle
                                empty_piece = Empty()
                                rook = self.chess_board[row_index][col_index + 3]
                                self.chess_board[row_index][col_index + 1] = rook     # Move the rook
                                self.chess_board[row_index][col_index + 3] = empty_piece
                                rook.update_position(row_index, col_index + 1)
                            if new_col == col_index - 2:
                                empty_piece = Empty()
                                rook = self.chess_board[row_index][col_index - 4]
                                self.chess_board[row_index][col_index - 1] = rook
                                self.chess_board[row_index][col_index - 4] = empty_piece
                                rook.update_position(row_index, col_index - 1)               
                            
                    self.chess_board[new_row][new_col] = piece  # Add piece to new position
                    # Update lastMove
                    if old_piece.type != 'Empty':   # Enemy piece captured
                        self.lastMove.updateMove(piece, row_index, col_index, new_row, new_col, old_piece)
                    elif dead_pawn != None:     # En passant
                        self.lastMove.updateMove(piece, row_index, col_index, new_row, new_col, dead_pawn)
                    else:   # No piece taken
                        self.lastMove.updateMove(piece, row_index, col_index, new_row, new_col, None)
                    self.look_for_check(piece.color)    # See if move introduces check to enemy king
                    # TODO: Check if pawn reaches back rank to promote
                    if piece.type == 'Pawn' and new_row == 0 or new_row == 7:
                        self.pawn_back_rank = piece
                    return
                
    
    # Look for check on enemy king after you move (takes color of the piece that just moved)
    def look_for_check(self, color):
        self.check_pos = None
        self.check_color = None
        # Get location of king
        king_row = None
        king_col = None
        for row_index, row in enumerate(self.chess_board):
            found = False
            for col_index, piece in enumerate(row):
                if piece.type == 'King' and piece.color != color:
                    king_row = row_index
                    king_col = col_index
                    break
            if found:
                break
        # Check to see if any valid moves from any piece of same color will target enemy king
        for row_index, row in enumerate(self.chess_board):
            for col_index, piece in enumerate(row):
                if piece.color == color:
                    moves = piece.get_attacks(row_index, col_index, self)
                    if moves != None and (king_row, king_col) in moves:   # if king is in valid move
                        self.check_pos = (king_row, king_col)
                        if color == 'white': self.check_color = 'black'
                        else: self.check_color = 'white'
        # TODO: Check for checkmate: see if King has any valid moves or if other piece can take attacking piece
        if self.check_pos != None:
            total_moves = []
            for row_index, row in enumerate(self.chess_board):
                for col_index, piece in enumerate(row):
                    if piece.color != color:
                        moves = piece.get_valid_moves(row_index, col_index, self)
                        if moves != None:
                            for x in moves: total_moves.append(x)
            if not total_moves:
                if color == 'white' and self.check_color == 'black': self.white_win = True
                if color == 'black' and self.check_color == 'white': self.black_win = True
                if self.check_color == None: self.stalemate = True
        return
    



    # Check if move leaves own King in check - return True if move is valid, false if move leaves king in check
    def validate_move_check(self, old_row, old_col, new_row, new_col):
        temp_board = self.copy_board()  # Copy Board to test moves
        # Move piece
        piece = temp_board.chess_board[old_row][old_col]
        temp_board.chess_board[new_row][new_col] = piece
        piece.update_position(new_row, new_col)
        temp_board.chess_board[old_row][old_col] = Empty()
        
        # Get location of king
        king_row = None
        king_col = None
        for row_index, row in enumerate(temp_board.chess_board):
            found = False
            for col_index, board_piece in enumerate(row):
                if board_piece.type == 'King' and board_piece.color == piece.color:
                    king_row = row_index
                    king_col = col_index
                    break
            if found:
                break

        # Check to see if any enemy pieces have a valid move attacking the king
        for row_index, row in enumerate(temp_board.chess_board):
            for col_index, board_piece in enumerate(row):
                if board_piece.color != piece.color:    # Enemy piece
                    moves = board_piece.get_attacks(row_index, col_index, temp_board)
                    if moves != None  and (king_row, king_col) in moves:   # if king is in valid move
                        return False
        return True
    

    # Check if caslte is legal - return True if leagl
    def validate_castle(self, king, rook, side):
        if king.moved or rook.moved:    # Check if king or rook has moved 
            return False
        spaces = [king.position]
        if king.color == 'white':
            if side == 'right':
                spaces.extend([(7, 5), (7, 6)])
            else:
                spaces.extend([(7, 3), (7, 2)])
        else:
            if side == 'right':
                spaces.extend([(0, 5), (0, 6)])
            else:
                spaces.extend([(0, 3), (0, 2)])
        for x in spaces[1:]:    # Check if any pieces in the way
            if self.chess_board[x[0]][x[1]].type != 'Empty':
                return False
        # Check to see if any enemy pieces have a valid move attacking the king
        for row_index, row in enumerate(self.chess_board):
            for col_index, board_piece in enumerate(row):
                if board_piece.color != king.color:    # Enemy piece
                    moves = board_piece.get_attacks(row_index, col_index, self)
                    if moves:
                        matching = set(moves).intersection(set(spaces))
                        if matching:
                            return False
        return True


    # Create a copy of the chessboard and last move
    def copy_board(self):
        new_board = ChessBoard()
        new_board.chess_board = [
            [piece.copy_piece() for piece in row] for row in self.chess_board
        ]
        new_board.lastMove = copy.copy(self.lastMove)
        return new_board


    # Tell main if checkmate or stalemate has occured
    def game_over(self):
        if self.white_win == True or self.black_win == True or self.stalemate == True:
            return True
        return False


    # Render pawn promotion
    def draw_pawn_promote(self, win):
        if self.pawn_back_rank != None:
            # Draw film over board
            transparent_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(transparent_surface, GREY, (0, 0, BOARD_WIDTH, BOARD_HEIGHT))
            win.blit(transparent_surface, (0, 0))
            # Draw white circles with promotion pieces in vertical line (queen, knight, rook, bishop)
            row = self.pawn_back_rank.position[0]
            col = self.pawn_back_rank.position[1]
            row_t = row
            # Load piece images
            white_queen_img = pygame.image.load('images/w_queen.png')
            white_bishop_img = pygame.image.load('images/w_bishop.png')
            white_knight_img = pygame.image.load('images/w_knight.png')
            white_rook_img = pygame.image.load('images/w_rook.png')
            black_queen_img = pygame.image.load('images/b_queen.png')
            black_bishop_img = pygame.image.load('images/b_bishop.png')
            black_knight_img = pygame.image.load('images/b_knight.png')
            black_rook_img = pygame.image.load('images/b_rook.png')
            white = [white_queen_img, white_knight_img, white_rook_img, white_bishop_img]
            black = [black_queen_img, black_knight_img, black_rook_img, black_bishop_img]
            if row == 0:    # White pawn promotion
                while row_t <= 3:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if col * SQUARE_SIZE <= mouse_x <= (col + 1) * SQUARE_SIZE and row_t * SQUARE_SIZE <= mouse_y <= (row_t + 1) * SQUARE_SIZE:
                        pygame.draw.rect(win, ORANGE, (SQUARE_SIZE * col, SQUARE_SIZE * row_t, SQUARE_SIZE, SQUARE_SIZE))
                    else:
                        pygame.draw.circle(win, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE / 2, row_t * SQUARE_SIZE + SQUARE_SIZE / 2), 48)
                    image = pygame.transform.smoothscale(white[row_t], (PIECE_WIDTH, PIECE_HEIGHT))
                    win.blit(image, (SQUARE_SIZE * col + (SQUARE_SIZE - PIECE_WIDTH) / 2, SQUARE_SIZE * row_t + (SQUARE_SIZE - PIECE_HEIGHT) / 2))
                    row_t += 1
            else:
                while row_t >= 4:
                    pygame.draw.circle(win, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE / 2, row_t * SQUARE_SIZE + SQUARE_SIZE / 2), 48)
                    image = pygame.transform.smoothscale(black[7 - row_t], (PIECE_WIDTH, PIECE_HEIGHT))
                    win.blit(image, (SQUARE_SIZE * col + (SQUARE_SIZE - PIECE_WIDTH) / 2, SQUARE_SIZE * row_t + (SQUARE_SIZE - PIECE_HEIGHT) / 2))
                    row_t -= 1
    

    # Update piece pawn promotion
    def update_pawn(self, piece):
        pawn = self.pawn_back_rank
        row = pawn.position[0]
        col = pawn.position[1]
        if piece == 1:
            new_piece = Queen(pawn.color, (row,col))
        elif piece == 2:
            new_piece = Knight(pawn.color, (row,col))
        elif piece == 3:
            new_piece = Rook(pawn.color, (row,col))
        else:
            new_piece = Bishop(pawn.color, (row,col))
        if pawn.color == 'white':
            self.white_pieces.append(new_piece)
            self.white_pieces.remove(pawn)
            self.white_pieces_taken.append(pawn)
        else:
            self.black_pieces.append(new_piece)
            self.black_pieces.remove(pawn)
            self.black_pieces_taken.append(pawn)
        self.chess_board[row][col] = new_piece
        new_piece.update_position(row, col)
        self.pawn_back_rank = None
        king_row = None
        king_col = None
        for row_index, row in enumerate(self.chess_board):
            found = False
            for col_index, piece in enumerate(row):
                if piece.type == 'King' and piece.color != new_piece.color:
                    king_row = row_index
                    king_col = col_index
                    break
            if found:
                break
        moves = new_piece.get_attacks(new_piece.position[0], new_piece.position[1], self)
        if moves != None and (king_row, king_col) in moves:
            self.check_color = piece.color
            self.check_pos = (king_row, king_col)


# Check for stalemate
def look_for_stalemate(self):
    pass


class Move:
    def __init__(self):
        self.piece = None
        self.old_row = None
        self.old_col = None
        self.new_row = None
        self.new_col = None
        self.piece_taken = None
        self.color = 'black'

    def updateMove(self, piece, old_row, old_col, new_row, new_col, piece_taken):
        self.piece = piece
        self.old_row = old_row
        self.old_col = old_col
        self.new_row = new_row
        self.new_col = new_col
        self.piece_taken = piece_taken
        self.color = piece.color