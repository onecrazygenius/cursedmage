import pygame, os
from pygame.locals import *
from app.states.components.button import Button
from app.constants import *
from app.states.state import State

class GameOverScreen(State):
    def __init__(self, game):
        super().__init__(game)
        self.button = Button("Back to Main Menu", SCREEN_WIDTH // 2, 600, self.back_to_main_menu)

    def back_to_main_menu(self):
        self.game.show_main_menu()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.button.handle_click(event)

    def draw(self, surface):
        # Set background as background image 
        background = pygame.image.load(resource_path("app/assets/images/backgrounds/game_over.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        font = pygame.font.Font(resource_path('app/assets/fonts/cursed_font.tff'), 200)
        text_surface = font.render("Game Over!", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 400))
        surface.blit(text_surface, text_rect)
        self.button.draw(surface)
        pygame.display.flip()