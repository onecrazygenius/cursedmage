import pygame
from pygame.locals import *

class Slider:

    def __init__(self, x, y, width, value, max_value, callback):
        self.x = x
        self.y = y
        self.width = width
        self.value = value
        self.max_value = max_value
        self.callback = callback

        self.slider_height = 10
        self.handle_radius = 10
        self.handle_x = self.x + (self.value / self.max_value) * self.width

        # Create a rect attribute for the slider
        self.rect = pygame.Rect(self.x, self.y, self.width, self.slider_height)

        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.handle_x), self.y + self.slider_height // 2), self.handle_radius)

    def handle_event(self, event, canvas_mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._is_on_handle(canvas_mouse_pos):
                self.dragging = True
                pygame.mouse.get_rel()  # Reset relative mouse movement
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            relative_x, _ = pygame.mouse.get_rel()
            self.value = max(0, min(self.max_value, self.value + relative_x))
            self.handle_x = self.x + (self.value / self.max_value) * self.width
            self.callback(self.value)

    def _is_on_handle(self, pos):
        distance = ((pos[0] - self.handle_x) ** 2 + (pos[1] - (self.y + self.slider_height // 2)) ** 2) ** 0.5
        return distance < self.handle_radius
