import pygame
from constants import PIECE_WIDTH, PIECE_HEIGHT

# Load piece images
white_king_img = pygame.image.load('images/w_king.png')
white_queen_img = pygame.image.load('images/w_queen.png')
white_bishop_img = pygame.image.load('images/w_bishop.png')
white_knight_img = pygame.image.load('images/w_knight.png')
white_rook_img = pygame.image.load('images/w_rook.png')
white_pawn_img = pygame.image.load('images/w_pawn.png')
black_king_img = pygame.image.load('images/b_king.png')
black_queen_img = pygame.image.load('images/b_queen.png')
black_bishop_img = pygame.image.load('images/b_bishop.png')
black_knight_img = pygame.image.load('images/b_knight.png')
black_rook_img = pygame.image.load('images/b_rook.png')
black_pawn_img = pygame.image.load('images/b_pawn.png')

class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.moved = False

    def update_position(self, row, col):
        self.position = (row, col)
        self.moved = True

    def get_valid_moves(self, row, col, board):
        return []


class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.image = white_king_img if color == 'white' else black_king_img
        self.image = pygame.transform.smoothscale(self.image, (PIECE_WIDTH, PIECE_HEIGHT))

    def get_valid_moves(self, row, col, board):
        # TODO: Castle - needs a state to check if king or rook has moved yet, cannot castle through check
        valid_moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        # Check if moves are valid
        for direction in directions:
            new_row = row + direction[0]
            new_col = col + direction[1]
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:   # Check if new position is within board limits
                # TODO: Check if leaves king in check
                if isinstance(board.chess_board[new_row][new_col], Empty):
                    valid_moves.append((new_row, new_col))
                elif board.chess_board[new_row][new_col].color != self.color:
                    valid_moves.append((new_row, new_col))
                else:
                    continue
            else:
                continue

        return valid_moves
    

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.image = white_queen_img if color == 'white' else black_queen_img
        self.image = pygame.transform.smoothscale(self.image, (PIECE_WIDTH, PIECE_HEIGHT))

    def get_valid_moves(self, row, col, board):
        valid_moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        # Check valid moves in each direction
        for direction in directions:
            for i in range(1, 8):  # Check up to 7 squares in each direction
                new_row = row + direction[0] * i
                new_col = col + direction[1] * i

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if isinstance(board.chess_board[new_row][new_col], Empty):  # Check if square is empty
                        valid_moves.append((new_row, new_col))
                    elif board.chess_board[new_row][new_col].color != self.color:
                        valid_moves.append((new_row, new_col))
                        break  # Stop in this direction if we encounter opponent's piece
                    else:
                        break  # Stop in this direction if we encounter own piece
                else:
                    break  # Stop if we reach the board's edge

        return valid_moves


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.image = white_bishop_img if color == 'white' else black_bishop_img
        self.image = pygame.transform.smoothscale(self.image, (PIECE_WIDTH, PIECE_HEIGHT))
    
    def get_valid_moves(self, row, col, board):
        valid_moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        # Check valid moves in each direction
        for direction in directions:
            for i in range(1, 8): # Check up to 7 squares in each direction
                new_row = row + direction[0] * i
                new_col = col + direction[1] * i

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if isinstance(board.chess_board[new_row][new_col], Empty):  # Check if square is empty
                            valid_moves.append((new_row, new_col))
                    elif board.chess_board[new_row][new_col].color != self.color:
                        valid_moves.append((new_row, new_col))
                        break   # Stop in this direction if we encounter opponent's piece
                    else:
                        break  # Stop in this direction if we encounter own piece
                else:
                    break  # Stop if we reach the board's edge

        return valid_moves


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.image = white_knight_img if color == 'white' else black_knight_img
        self.image = pygame.transform.smoothscale(self.image, (PIECE_WIDTH, PIECE_HEIGHT))

    def get_valid_moves(self, row, col, board):
        valid_moves = []
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        # Check valid moves in each direction
        for direction in directions:
            new_row = row + direction[0]
            new_col = col + direction[1]

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if isinstance(board.chess_board[new_row][new_col], Empty):  # Check if square is empty
                    valid_moves.append((new_row, new_col))
                elif board.chess_board[new_row][new_col].color != self.color:
                    valid_moves.append((new_row, new_col))  # Add if we encounter opponent's piece
                else:
                    continue    # Don't add if we encounter own piece
            else:
                continue    # Don't add if we reach the board's edge

        return valid_moves



class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.image = white_rook_img if color == 'white' else black_rook_img
        self.image = pygame.transform.smoothscale(self.image, (PIECE_WIDTH, PIECE_HEIGHT))

    def get_valid_moves(self, row, col, board):
        valid_moves = []
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        # Check valid moves in each direction
        for direction in directions:
            for i in range(1, 8): # Check up to 7 squares in each direction
                new_row = row + direction[0] * i
                new_col = col + direction[1] * i

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if isinstance(board.chess_board[new_row][new_col], Empty):  # Check if square is empty
                            valid_moves.append((new_row, new_col))
                    elif board.chess_board[new_row][new_col].color != self.color:
                        valid_moves.append((new_row, new_col))
                        break   # Stop in this direction if we encounter opponent's piece
                    else:
                        break  # Stop in this direction if we encounter own piece
                else:
                    break  # Stop if we reach the board's edge

        return valid_moves
    

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.image = white_pawn_img if color == 'white' else black_pawn_img
        self.image = pygame.transform.smoothscale(self.image, (PIECE_WIDTH, PIECE_HEIGHT))

    def get_valid_moves(self, row, col, board):
        valid_moves = []

        direction = -1 if self.color == 'white' else 1

        # Forward movement (one square)
        new_row = row + direction
        if 0 <= new_row < 8 and isinstance(board.chess_board[new_row][col], Empty):
            valid_moves.append((new_row, col))

            # Allow double move if haven't moved
            new_row += direction
            if not self.moved and 0 <= new_row < 8 and isinstance(board.chess_board[new_row][col], Empty):
                valid_moves.append((new_row, col))

        # Diagonal captures
        for col_offset in [-1, 1]:  # Check left and right diagonals
            new_row = row + direction
            new_col = col + col_offset

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                piece_at_diagonal = board.chess_board[new_row][new_col]
                if not isinstance(piece_at_diagonal, Empty) and piece_at_diagonal.color != self.color:    # Check diagonal is not empty and diagonal is enemy
                    valid_moves.append((new_row, new_col))

        return valid_moves


class Empty(Piece):
    def __init__(self):
        super().__init__(None, None)
