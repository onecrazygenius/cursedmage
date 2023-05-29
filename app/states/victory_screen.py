import pygame, os
from pygame.locals import *
from app.states.components.button import Button
from app.constants import *
from app.states.state import State

class VictoryScreen(State):
    def __init__(self, game):
        super().__init__(game)
        self.button = Button("Back to Main Menu", SCREEN_WIDTH // 2, 300, self.back_to_main_menu)

    def back_to_main_menu(self):
        self.game.show_main_menu()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.button.handle_click(event)

    def draw(self, surface):
        surface.fill((0, 255, 0))  # Green background for victory screen

        path = os.path.dirname(os.path.abspath(__file__))
        font = pygame.font.Font(resource_path(path + '/../assets/fonts/cursed_font.tff'), 24)
        
        text_surface = font.render("Victory!", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        surface.blit(text_surface, text_rect)
        self.button.draw(surface)
        pygame.display.flip()