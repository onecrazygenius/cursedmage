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
            Button(text, 200, 200, self.change_screen_size),
            Button("Toggle Fullscreen", SCREEN_WIDTH // 2 + 100, 200, self.game.toggle_fullscreen),
            Button("Return to Main Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200, self.return_to_main_menu),
            Button("Exit", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, self.exit_game)
        ]
        self.sliders = [
            Slider(200, 250, 200, self.game.get_master_volume(), 100, self.game.change_master_volume),
            Slider(SCREEN_WIDTH // 2 + 100, 250, 200, self.game.get_sfx_volume(), 100, self.game.change_sfx_volume)
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
            
        # Update the positions and sizes of the buttons and sliders
        for button in self.buttons:
            button.update_size_and_position()  # This is a new method that you would need to implement in the Button class

        for slider in self.sliders:
            slider.update_size_and_position()  # This is a new method that you would need to implement in the Slider class

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
            print("Here")
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
