import pygame
from board import ChessBoard
from pieces import Empty
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, SQUARE_SIZE
from ui import rematch_button

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

# Game over button
rect_width = SQUARE_SIZE * (4 + 2/3)
rect_height = SQUARE_SIZE * (1 + 1/3)
top_left_x = SQUARE_SIZE * (1 + 2/3)
mid_left_y = SQUARE_SIZE * 4
button_rect = pygame.Rect(top_left_x, mid_left_y, rect_width, rect_height)


while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse clicks for user input
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button down
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x <= BOARD_WIDTH and mouse_y <= BOARD_HEIGHT:  # Check if click was within the board area
                row = mouse_y // SQUARE_SIZE
                col = mouse_x // SQUARE_SIZE
                piece = chess_board.chess_board[row][col]
                if not isinstance(piece, Empty) and piece.color != chess_board.lastMove.color:
                    if not chess_board.game_over():
                        # Bind piece to the mouse
                        dragging = True
                        # Display possible moves (updates moves which gets sent to board.py for rendering through drag_piece function)
                        moves = piece.get_valid_moves(row, col, chess_board)  # Get all valid moves for piece
            if chess_board.game_over():
                if button_rect.collidepoint(mouse_x, mouse_y):
                    chess_board = ChessBoard()      # Start over

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:    # Check for left mouse button up
            dragging = False
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x <= BOARD_WIDTH and mouse_y <= BOARD_HEIGHT:  # Check if click was within the board area
                new_row = mouse_y // SQUARE_SIZE
                new_col = mouse_x // SQUARE_SIZE
                if new_row != row or new_col != col:   # Check if piece is in a new position
                    if (new_row, new_col) in moves:    # Check if new position is a valid move
                        piece.update_position(new_row, new_col)
                        chess_board.update_piece(piece, new_row, new_col)    
                chess_board.stop_drag()
            else: # Not within board area
                # TODO: Reset piece
                print('TODO')

        if dragging:
            chess_board.drag_piece(piece, pygame.mouse.get_pos(), moves)


    # Rendering the board and pieces
    chess_board.render(win)

    # Render game over
    if chess_board.game_over():
        text = 'Checkmate - White is Victorious!'
        if chess_board.black_win:
            text = 'Checkmate - Black is Victorious!'
        if chess_board.stalemate:
            text = 'Stalemate'
        mouse_pos =  pygame.mouse.get_pos()
        button_active = button_rect.collidepoint(mouse_pos)
        rematch_button(win, text, button_active)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
