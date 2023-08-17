
from app.constants import *
from app.states.state import State
from app.states.components.button import Button

class Tutorial(State):

    def __init__(self, game):
        super().__init__(game)

        self.game = game

    def draw(self, surface):
        # Set background as background image
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/brick.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        # update the screen
        pygame.display.flip()
    
    def handle_event(self, event):
        pass