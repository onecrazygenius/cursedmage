import pygame, os
import app.constants as constants

from app.constants import relative_resource_path

class State:
    '''
    State class for the game. All states inherit from this class.
    '''
    def __init__(self, game):
        self.game = game
        self.surface = game.surface
        self.const = constants

        self.font = pygame.font.Font(relative_resource_path('/app/assets/fonts/cursed_font.tff'), 24)

    def handle_event(self):
        pass

    def draw(self, canvas):
        pass
