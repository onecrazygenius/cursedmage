import pygame, os
import app.constants as constants

class State:
    '''
    State class for the game. All states inherit from this class.
    '''
    def __init__(self, game):
        self.game = game
        self.surface = game.surface
        self.const = constants

        path = os.path.dirname(os.path.abspath(__file__))
        self.font = pygame.font.Font(resource_path(path + '/../assets/fonts/cursed_font.tff'), 24)

    def handle_event(self):
        pass

    def draw(self, canvas):
        pass
