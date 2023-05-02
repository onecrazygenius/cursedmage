from app.engine.components.button import Button
from app.engine.components.slider import Slider
from app.engine.constants import *
from pygame.locals import *
import pygame


class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button("Screen Size: 800x600", 200, 200, self.change_screen_size),
            Button("Toggle Fullscreen", (SCREEN_WIDTH //2) + 100, 200, self.game.toggle_fullscreen),
            Button("Return to Main Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200, self.return_to_main_menu),
            Button("Exit", SCREEN_WIDTH // 2, SCREEN_HEIGHT-100 , self.exit_game)
        ]
        self.sliders = [
            Slider(200, 250, 200, self.game.get_master_volume(), 100, self.game.change_master_volume),
            Slider((SCREEN_WIDTH // 2) + 100, 250, 200, self.game.get_sfx_volume(), 100, self.game.change_sfx_volume)
        ]
        self.slider_labels = [
            ("Master Volume", (160, 220)),
            ("SFX Volume", (SCREEN_WIDTH // 2 + 60, 220))
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
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            for slider in self.sliders:
                slider.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.callback()

    def draw_label(self, text, position):
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, (255, 255, 255))  # White text
        self.game.screen.blit(text_surface, position)

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Settings Menu", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.game.screen.blit(text_surface, text_rect)

        for button in self.buttons:
            button.draw(self.game.screen)

        for slider, (label_text, label_pos) in zip(self.sliders, self.slider_labels):
            self.draw_label(label_text, label_pos)
            slider.draw(self.game.screen)

        pygame.display.flip()