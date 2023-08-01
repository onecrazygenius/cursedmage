from app.states.components.button import Button
from app.constants import *
from app.states.state import State

class GameOverScreen(State):
    def __init__(self, game):
        super().__init__(game)
        self.button = Button("See My Score", SCREEN_WIDTH // 2, 600, self.score_screen)

    def score_screen(self):
        self.game.see_score()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.button.handle_click(event)

    def draw(self, surface):
        # Set background as background image 
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/game_over.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        font = pygame.font.Font(relative_resource_path('app/assets/fonts/cursed_font.tff'), 200)
        text_surface = font.render("Game Over!", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 400))
        surface.blit(text_surface, text_rect)
        self.button.draw(surface)

        # nuke save file
        self.game.save_manager.nuke_save_file()

        pygame.display.flip()