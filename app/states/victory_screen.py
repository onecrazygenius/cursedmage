import pygame, os
from pygame.locals import *
from app.states.components.button import Button
from app.constants import *
from app.states.state import State


class VictoryScreen(State):
    def __init__(self, game):
        super().__init__(game)
        self.button = Button("Back to Main Menu", SCREEN_WIDTH // 2, 600, self.back_to_main_menu)

    def back_to_main_menu(self):
        self.game.show_main_menu()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Check if the button was clicked
            if self.button.rect.collidepoint(self.game.screen_to_surface(event.pos)):
                self.back_to_main_menu()

    def draw(self, surface):
        # Set background as background image 
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/victory.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        cursed_font = pygame.font.Font(relative_resource_path('app/assets/fonts/cursed_font.tff'), 100)

        # Draw text
        text_surface = cursed_font.render("Victory!", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, 420)
        surface.blit(text_surface, text_rect)
        self.button.draw(surface)

        # nuke save file
        self.game.save_manager.nuke_save_file()

        # Update the display
        pygame.display.flip()
