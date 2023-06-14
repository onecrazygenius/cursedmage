import pygame


class Popup:
    def __init__(self, x, y, start_time, text="Popup", width=100, height=100):
        self.x = x
        self.y = y
        self.start_time = start_time
        self.text = text
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, text_rect)