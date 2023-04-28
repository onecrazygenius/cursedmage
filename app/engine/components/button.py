import pygame
from pygame.locals import *
from app.engine.constants import *

class Button:
    def __init__(self, text, x, y, callback, width=200, height=50, font_size=24):
        self.text = text
        self.x = x
        self.y = y
        self.callback = callback
        self.width = width
        self.height = height
        self.font_size = font_size
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x, self.y)
        screen.blit(text_surface, text_rect)

    def handle_click(self, event):
        if event.type == MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.callback()