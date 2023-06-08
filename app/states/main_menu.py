import pygame, os
from pygame.locals import *
from app.constants import *
from app.states.state import State
from app.states.components.button import Button

class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.buttons = [
            Button("New Game", SCREEN_WIDTH // 2, 500, self.game.new_game),
            Button("Load Game", SCREEN_WIDTH // 2, 600, self.game.load_game),
            Button("Settings", SCREEN_WIDTH // 2, 700, self.game.show_settings),
            Button("Quit", SCREEN_WIDTH // 2, 800, self.game.quit_game)
        ]
        
        # Music
        pygame.mixer.init()
        pygame.mixer.music.load(relative_resource_path("app/assets/music/8bit.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.game.config.get_master_volume())


    def draw(self, surface):
        # Set background as background image 
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/main_menu.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))
        # Title
        title_font = pygame.font.Font(relative_resource_path("app/assets/fonts/cursed_font.tff"), 200)
        title_text = "Cursed Mage"
        title_surface = title_font.render(title_text, True, self.const.WHITE)
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, 200)
        surface.blit(title_surface, title_rect)

        for button in self.buttons:
            button.draw(surface)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for button in self.buttons:
                button.handle_click(event)