from app.engine.components.button import Button
from app.engine.components.slider import Slider
from app.engine.constants import *
from pygame.locals import *
import pygame


class SettingsMenu:
    def __init__(self, game):
        self.game = game

        current_screen_size = self.game.screen.get_size()
        text = "Screen Size: {}x{}".format(current_screen_size[0], current_screen_size[1])
        self.buttons = [
            Button(text, 200, 200, self.change_screen_size),
            Button("Toggle Fullscreen", (self.game.config.get_width() //2) + 100, 200, self.game.toggle_fullscreen),
            Button("Return to Main Menu", self.game.config.get_width() // 2, self.game.config.get_height() - 200, self.return_to_main_menu),
            Button("Exit", self.game.config.get_width() // 2, self.game.config.get_height()-100 , self.exit_game)
        ]
        self.sliders = [
            Slider(200, 250, 200, self.game.get_master_volume(), 100, self.game.change_master_volume),
            Slider((self.game.config.get_width() // 2) + 100, 250, 200, self.game.get_sfx_volume(), 100, self.game.change_sfx_volume)
        ]
        self.slider_labels = [
            ("Master Volume", (160, 220)),
            ("SFX Volume", (self.game.config.get_width() // 2 + 60, 220))
        ]


    def change_screen_size(self):
        # Switch to windowed mode if fullscreen
        if self.game.screen.get_flags() & pygame.FULLSCREEN:
            self.game.toggle_fullscreen()
        
        # Change screen size
        if self.game.screen.get_size() == (800, 600):
            self.game.resize_screen(1024, 768)
            self.buttons[0].set_text("Screen Size: 1024x768")
        elif self.game.screen.get_size() == (1024, 768):
            self.game.resize_screen(1280, 720)
            self.buttons[0].set_text("Screen Size: 1280x720")
        elif self.game.screen.get_size() == (1280, 720):
            self.game.resize_screen(1920, 1080)
            self.buttons[0].set_text("Screen Size: 1920x1080")
        elif self.game.screen.get_size() == (1920, 1080):
            self.game.resize_screen(800, 600)
            self.buttons[0].set_text("Screen Size: 800x600")

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
        text_rect = text_surface.get_rect(center=(self.game.config.get_width() // 2, 100))
        self.game.screen.blit(text_surface, text_rect)

        for button in self.buttons:
            button.draw(self.game.screen)

        for slider, (label_text, label_pos) in zip(self.sliders, self.slider_labels):
            self.draw_label(label_text, label_pos)
            slider.draw(self.game.screen)

        pygame.display.flip()