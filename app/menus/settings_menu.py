import pygame
from pygame.locals import *
from engine.button import Button
from engine.constants import *


class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button("Screen Size: 800x600", 100, 200, self.change_screen_size),
            Button("Toggle Fullscreen", 100, 250, self.game.toggle_fullscreen),
            Button("Return to Main Menu", SCREEN_WIDTH // 2, 200, self.return_to_main_menu),
            Button("Exit", SCREEN_WIDTH // 2, 250, self.exit_game)
        ]

    def change_screen_size(self):
        # Switch to windowed mode if fullscreen
        if self.game.screen.get_flags() & pygame.FULLSCREEN:
            self.game.toggle_fullscreen()
        
        # Change screen size
        if self.game.screen.get_size() == (SCREEN_WIDTH, SCREEN_HEIGHT):
            self.game.resize_screen(800, 600)
            self.buttons[0].text = "Screen Size: 800x600"
        else:
            self.game.resize_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.buttons[0].text = "Screen Size: 1280x720"

    def return_to_main_menu(self):
        self.game.show_main_menu()

    def exit_game(self):
        self.game.quit_game()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.callback()

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Settings Menu", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.game.screen.blit(text_surface, text_rect)

        for button in self.buttons:
            button.draw(self.game.screen)

        pygame.display.flip()