import pygame, os
from pygame.locals import *
from app.constants import *
from app.states.state import State
from app.states.components.button import Button

class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.buttons = [
            Button("New Game", SCREEN_WIDTH // 2, 200, self.game.new_game),
            Button("Load Game", SCREEN_WIDTH // 2, 300, self.game.load_game),
            Button("Settings", SCREEN_WIDTH // 2, 400, self.game.show_settings),
            Button("Quit", SCREEN_WIDTH // 2, 500, self.game.quit_game)
        ]
        
        # Music
        path = os.path.dirname(os.path.abspath(__file__))
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(path, "../assets/music/deku.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.game.config.get_master_volume())


    def draw(self, surface):
        # Set white background
        surface.fill(self.const.WHITE)
        # Title
        title_font = pygame.font.Font(None, 48)
        title_text = "Cursed Mage"
        title_surface = title_font.render(title_text, True, self.const.BLACK)
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, 100)
        surface.blit(title_surface, title_rect)

        for button in self.buttons:
            button.draw(surface)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for button in self.buttons:
                button.handle_click(event)