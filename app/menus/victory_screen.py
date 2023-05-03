import pygame
from pygame.locals import *
from app.engine.components.button import Button
from app.engine.constants import *

class VictoryScreen:
    def __init__(self, game):
        self.game = game
        self.button = Button("Back to Main Menu", self.game.config.get_width() // 2, 300, self.back_to_main_menu)

    def back_to_main_menu(self):
        self.game.show_main_menu()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.button.handle_click(event)

    def draw(self):
        self.game.screen.fill((0, 255, 0))  # Green background for victory screen
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Victory!", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(self.game.config.get_width() // 2, 200))
        self.game.screen.blit(text_surface, text_rect)
        self.button.draw(self.game.screen)
        pygame.display.flip()