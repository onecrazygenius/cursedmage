import pygame, os

class Popup:
    def __init__(self, x, y, text="Popup", width=100, height=100):
        self.x = x
        self.y = y
        self.text = text
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x, self.y)
        screen.blit(text_surface, text_rect)