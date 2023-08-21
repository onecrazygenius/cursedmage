from app.states.components.button import Button
from app.states.components.slider import Slider
from app.states.state import State
from app.constants import *
import pygame


class SettingsMenu(State):

    def __init__(self, game):
        super().__init__(game)

        self.game = game

        current_screen_size = self.game.config.get_width(), self.game.config.get_height()
        text = "Screen Size: {}x{}".format(current_screen_size[0], current_screen_size[1])
        self.buttons = [
            Button(text, SCREEN_WIDTH // 4, 350, self.change_screen_size, width=300, height=75),
            Button(" Toggle Fullscreen ", SCREEN_WIDTH // 4, 475, self.game.toggle_fullscreen, width=300, height=75),
            Button(" Return to Main Menu ", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200, self.return_to_main_menu, width=400, height=75),
            Button("Exit", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, self.exit_game)
        ]
        self.sliders = [
            Slider((SCREEN_WIDTH // 4) * 3 - 100, 350, 200, self.game.get_master_volume(), 100, self.game.change_master_volume),
            Slider((SCREEN_WIDTH // 4) * 3 - 100, 475, 200, self.game.get_sfx_volume(), 100, self.game.change_sfx_volume)
        ]
        self.slider_labels = [
            ("Music Volume:", ((SCREEN_WIDTH // 4) * 3 - 340, 340)),
            ("Sfx Volume:", ((SCREEN_WIDTH // 4) * 3 - 340, 465))
        ]

    def change_screen_size(self):
        # If full screen disable button
        if self.game.screen.get_flags() & pygame.FULLSCREEN:
            return
        
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

        # redraw the screen
        pygame.display.flip()

    def return_to_main_menu(self):
        self.game.settings_menu_open = False
        self.game.show_main_menu()

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
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/brick.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        font = pygame.font.Font(relative_resource_path("app/assets/fonts/pixel_font.ttf"), 64)
        text_surface = font.render("Settings Menu", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(text_surface, text_rect)

        for button in self.buttons:
            button.draw(surface)

        for slider, (label_text, label_pos) in zip(self.sliders, self.slider_labels):
            self.draw_label(surface, label_text, label_pos)
            slider.draw(surface)

    def draw_label(self, surface, text, position):
        font = pygame.font.Font(relative_resource_path("app/assets/fonts/pixel_font.ttf"), 36)
        text_surface = font.render(text, True, (255, 255, 255))  # White text
        surface.blit(text_surface, position)
