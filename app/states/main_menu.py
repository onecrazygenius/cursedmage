from pygame.locals import *

from app.constants import *
from app.states.components.button import Button
from app.states.components.popup import Popup
from app.states.state import State


class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.buttons = [
            Button("New Game", SCREEN_WIDTH // 2, 500, self.game.new_game),
            Button("Load Game", SCREEN_WIDTH // 2, 600, self.game.load_game),
            Button("Tutorial", SCREEN_WIDTH // 2, 700, self.show_tutorial),
            Button("Settings", SCREEN_WIDTH // 2, 800, self.game.show_settings),
            Button("Quit", SCREEN_WIDTH // 2, 900, self.game.quit_game)
        ]
        
        # Music
        pygame.mixer.init()
        pygame.mixer.music.load(relative_resource_path("app/assets/music/8bit.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.game.config.get_master_volume())

        self.active_popup = None


    def draw(self, surface):
        # Set background as background image 
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/main_menu.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        # add black border to the below  text
        title_font = pygame.font.Font(relative_resource_path("app/assets/fonts/cursed_font.tff"), 200)
        title_text = "Cursed Mage"
        title_surface = title_font.render(title_text, True, self.const.BLACK)
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2 + 5, 300 + 5)
        surface.blit(title_surface, title_rect)
        # Title, add a black border to the text
        title_surface = title_font.render(title_text, True, self.const.WHITE)
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, 300)
        surface.blit(title_surface, title_rect)

        for button in self.buttons:
            button.draw(surface)

        if self.active_popup is not None:
            # Draw the popup only if the difference between current time and popup start time is less than 2 seconds
            if pygame.time.get_ticks() - self.active_popup.start_time < DUNGEON_POPUP_DURATION_MS:
                self.active_popup.draw(surface)
            else:
                self.active_popup = None

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for button in self.buttons:
                button.handle_click(event)

    def show_tutorial(self):
        # Show the tutorial by changing to the tutorial state
        try:
            os.startfile(relative_resource_path("app/assets/videos/tutorial.mp4"))
        except Exception as e:
            # Do Popup if there is any error (Likely no media player installed)
            self.show_popup("Unable to play tutorial. Do you have a media player installed?")

    def show_popup(self, text):
        popup = Popup(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            pygame.time.get_ticks(),
            text,
            width=575,
            height=100,
        )
        self.active_popup = popup