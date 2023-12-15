import pygame
from constants import REMATCH_COLOR_ACITVE, REMATCH_COLOR_INACTIVE, TEXT_COLOR, SQUARE_SIZE, DARK_GREY



# Timer
def display_timer(win):
    pass


# Restart Button
def rematch_button(win, text, active):
    rect_width = SQUARE_SIZE * (4 + 2/3)
    rect_height = SQUARE_SIZE * (1 + 1/3)
    top_left_x = SQUARE_SIZE * (1 + 2/3)
    top_left_y = SQUARE_SIZE * (2 + 2/3)
    mid_left_y = SQUARE_SIZE * 4

    # Game over dialogue box
    font = pygame.font.Font(None, 32)
    text_surface_gg = font.render(text, True, TEXT_COLOR)
    text_rect_gg = text_surface_gg.get_rect(center = (top_left_x + rect_width / 2, top_left_y + rect_height / 2))
    pygame.draw.rect(win, DARK_GREY, (top_left_x, top_left_y, rect_width, rect_height * 2))
    win.blit(text_surface_gg, text_rect_gg)

    # Rematch button
    button_color = REMATCH_COLOR_ACITVE if active else REMATCH_COLOR_INACTIVE
    font = pygame.font.Font(None, 46)
    text_surface = font.render('REMATCH', True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center = (top_left_x + rect_width / 2, mid_left_y + rect_height / 2))
    pygame.draw.rect(win, button_color, (top_left_x, mid_left_y, rect_width, rect_height))
    win.blit(text_surface, text_rect)
