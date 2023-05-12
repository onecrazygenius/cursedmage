import pygame, os
import app.constants as constants

class State:
    '''
    State class for the game. All states inherit from this class.
    '''
    def __init__(self, game):
        self.game = game
        self.screen = game.canvas
        self.const = constants

        path = os.path.dirname(os.path.abspath(__file__))
        self.font = pygame.font.Font(os.path.join(path + '/../assets/fonts/cursed_font.tff'), 24)

    def handle_event(self):
        pass

    def draw(self):
        pass
