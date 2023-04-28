import pygame, os
from pygame.locals import *
from app.engine.components.button import Button
from app.engine.constants import *

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button("New Game", SCREEN_WIDTH // 2, 200, self.game.new_game),
            Button("Load Game", SCREEN_WIDTH // 2, 300, self.game.load_game),
            Button("Settings", SCREEN_WIDTH // 2, 400, self.game.show_settings),
            Button("Quit", SCREEN_WIDTH // 2, 500, self.game.quit_game)
        ]
        
        # Music
        path = os.path.dirname(os.path.abspath(__file__))
        pygame.mixer.music.load(os.path.join(path, "../assets/music/deku.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)


    def draw(self):
        self.game.screen.fill(WHITE)
        title_font = pygame.font.Font(None, 48)
        title_text = "Cursed Mage"
        title_surface = title_font.render(title_text, True, BLACK)
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, 100)
        self.game.screen.blit(title_surface, title_rect)

        for button in self.buttons:
            button.draw(self.game.screen)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
            for button in self.buttons:
                button.handle_click(event)