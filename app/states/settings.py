from app.states.components.button import Button
from app.states.components.slider import Slider
from app.states.state import State
from app.constants import *
from pygame.locals import *
import pygame


class SettingsMenu(State):

    def __init__(self, game):
        super().__init__(game)

        self.game = game

        current_screen_size = SCREEN_WIDTH, SCREEN_HEIGHT
        text = "Screen Size: {}x{}".format(current_screen_size[0], current_screen_size[1])
        self.buttons = [
            Button(text, 200, 250, self.change_screen_size),
            Button("Toggle Fullscreen", 200, 350, self.game.toggle_fullscreen),
            Button("Return to Main Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200, self.return_to_main_menu),
            Button("Exit", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, self.exit_game)
        ]
        self.sliders = [
            Slider(SCREEN_WIDTH // 2 + 100, 250, 200, self.game.get_master_volume(), 100, self.game.change_master_volume),
            Slider(SCREEN_WIDTH // 2 + 100, 350, 200, self.game.get_sfx_volume(), 100, self.game.change_sfx_volume)
        ]
        self.slider_labels = [
            ("Master Volume", (SCREEN_WIDTH // 2 + 60, 220)),
            ("SFX Volume", (SCREEN_WIDTH // 2 + 60, 320))
        ]

    def change_screen_size(self):
        # Switch to windowed mode if fullscreen
        if self.game.screen.get_flags() & pygame.FULLSCREEN:
            self.game.toggle_fullscreen()
        
        # Change screen size
        # Default: 1920x1080
        #        : 1080x720

        if self.game.config.get_width() == 1920:
            self.game.resize_screen(1080, 720)
            # Update the button text
            self.buttons[0].text = "Screen Size: 1080x720"
        else:
            self.game.resize_screen(1920, 1080)
            # Update the button text
            self.buttons[0].text = "Screen Size: 1920x1080"

    def return_to_main_menu(self):
        self.game.hide_settings()

    def exit_game(self):
        self.game.quit_game()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            # Convert mouse position to canvas coordinates
            screen_width, screen_height = pygame.display.get_surface().get_size()
            canvas_mouse_pos = (
                event.pos[0] * (SCREEN_WIDTH / screen_width),
                event.pos[1] * (SCREEN_HEIGHT / screen_height),
            )

            for slider in self.sliders:
                slider.handle_event(event, canvas_mouse_pos)
        if event.type == pygame.MOUSEBUTTONUP:
            # Convert mouse position to canvas coordinates
            screen_width, screen_height = pygame.display.get_surface().get_size()
            canvas_mouse_pos = (
                event.pos[0] * (SCREEN_WIDTH / screen_width),
                event.pos[1] * (SCREEN_HEIGHT / screen_height),
            )
            for button in self.buttons:
                if button.rect.collidepoint(canvas_mouse_pos):
                    button.callback()

    def draw(self, surface):
        surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Settings Menu", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(text_surface, text_rect)

        for button in self.buttons:
            button.draw(surface)

        for slider, (label_text, label_pos) in zip(self.sliders, self.slider_labels):
            self.draw_label(surface, label_text, label_pos)
            slider.draw(surface)

    def draw_label(self, surface, text, position):
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, (255, 255, 255))  # White text
        surface.blit(text_surface, position)