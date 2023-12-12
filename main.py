import pygame
from board import ChessBoard
from pieces import Empty
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, SQUARE_SIZE

pygame.init()

# Initialize the screen, clock, etc.
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Board")
clock = pygame.time.Clock()


# Initialize the board
chess_board = ChessBoard()

# Game loop
running = True
dragging = True
piece = None
moves = []
row = None
col = None

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse clicks for user input
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button down
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # print('Mouse_x: ', mouse_x, ' Mouse_y: ', mouse_y)
            if mouse_x <= BOARD_WIDTH and mouse_y <= BOARD_HEIGHT:  # Check if click was within the board area
                row = mouse_y // SQUARE_SIZE
                col = mouse_x // SQUARE_SIZE
                print('Row: ', row,' Col: ', col)
                piece = chess_board.chess_board[row][col]
                if not isinstance(piece, Empty):    # Check if there is a piece there
                    # Bind piece to the mouse
                    dragging = True
                    # Display possible moves (updates moves which gets sent to board.py for rendering through drag_piece function)
                    if chess_board.in_check(piece.color):   # Check if king for clicked piece is in check
                        moves = piece.get_valid_moves_check(row, col, chess_board)  # TODO: Valid moves from check position
                    else:
                        moves = piece.get_valid_moves(row, col, chess_board)
                        print(moves)

            

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:    # Check for left mouse button up
            dragging = False
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x <= BOARD_WIDTH and mouse_y <= BOARD_HEIGHT:  # Check if click was within the board area
                new_row = mouse_y // SQUARE_SIZE
                new_col = mouse_x // SQUARE_SIZE
                if new_row != row or new_col != col:   # Check if piece is in a new position
                    if (new_row, new_col) in moves:    # Check if new position is a valid move
                        piece.update_position(new_row, new_col)
                        print(piece.position)
                        chess_board.update_piece(piece, new_row, new_col)    
                chess_board.stop_drag()
            else: # Not within board area
                # TODO: Reset piece
                print('TODO')

        if dragging:
            chess_board.drag_piece(piece, pygame.mouse.get_pos(), moves)


    # Rendering the board and pieces
    chess_board.render(win)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
