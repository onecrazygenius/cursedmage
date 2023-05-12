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

        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.slider_height))
        pygame.draw.circle(screen, (255, 0, 0), (int(self.handle_x), self.y + self.slider_height // 2), self.handle_radius)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._is_on_handle(event.pos):
                pygame.mouse.set_visible(False)
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                pygame.mouse.set_visible(True)
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_x = event.pos[0]
                self.handle_x = min(max(self.x, self.handle_x), self.x + self.width)
                self.value = int((self.handle_x - self.x) / self.width * self.max_value)
                self.callback(self.value)

    def _is_on_handle(self, pos):
        distance = ((pos[0] - self.handle_x) ** 2 + (pos[1] - (self.y + self.slider_height // 2)) ** 2) ** 0.5
        return distance <= self.handle_radius