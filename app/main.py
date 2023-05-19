from app.logic.config_manager import ConfigManager
from app.logic.save_manager import SaveManager
from app.constants import *
#from app.states.character_selection import CharacterSelection
#from app.states.victory_screen import VictoryScreen
from app.states.settings import SettingsMenu
from app.states.main_menu import MainMenu
#from app.states.dungeon import Dungeon
import pygame, os


class Game:
    def __init__(self):
        # Initialize pygame and pygame.mixer
        pygame.init()
        pygame.mixer.init()

        # Initialize the config and save managers
        self.config = ConfigManager()
        self.save_manager = SaveManager()

        # Initialize the screen and clock
        self.screen = pygame.display.set_mode((self.config.get_width(), self.config.get_height()))
        self.canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.wait_time_after_state = STATE_WAIT_TIME

        path = os.path.dirname(os.path.abspath(__file__))
        # Set the window title and icon in assets/images
        icon = pygame.image.load(os.path.join(path, "assets/images/team_logo.png"))
        pygame.display.set_caption("Cursed Mage")
        pygame.display.set_icon(icon)

        # Initialize game variables
        self.done = False
        self.character = None
        self.difficulty = None
        self.just_switched = False

        self.states = [MainMenu(self)]

        self.settings_menu_open = False  # Flag to track if the settings menu is open

    # State management
    def push_state(self, state):
        pygame.time.wait(self.wait_time_after_state_change)
        self.states.append(state)

    def pop_state(self):
        pygame.time.wait(self.wait_time_after_state_change)
        if self.states:
            self.states.pop()

    def change_state(self, state):
        if self.states:
            self.pop_state()
        self.push_state(state)
        self.just_switched = True

    def screen_to_canvas(self, pos):
        # Convert the mouse position from the screen to the canvas
        return pos[0] - (self.config.get_width() - SCREEN_WIDTH) // 2, pos[1] - (self.config.get_height() - SCREEN_HEIGHT) // 2

    # Data management
    def save_game(self):
        game_data = {
            "character": self.character,
            "difficulty": self.difficulty,
            "dungeon": self.dungeon.get_data(),
        }
        self.save_manager.save(game_data)

    def load_game(self):
        data = self.save_manager.load()
        if not data:
            return
        self.character = data["character"]
        self.difficulty = data["difficulty"]
        #self.dungeon = Dungeon(self, game_data=data["dungeon"])
        self.change_state(self.dungeon)

    # Sounds
    def change_master_volume(self, volume):
        # Convert the volume to a float between 0 and 1
        volume = float(volume) / 100
        pygame.mixer.music.set_volume(volume)
        # Save the volume to the config
        self.config.update("audio", "master_volume", str(volume))

    def change_sfx_volume(self, volume):
        # Convert the volume to a float between 0 and 1
        volume = float(volume) / 100
        # Save the volume to the config
        self.config.update("audio", "sfx_volume", str(volume))
        pass

    def get_master_volume(self):
        return int(float(self.config.get("audio", "master_volume")) * 100)
    
    def get_sfx_volume(self):
        return int(float(self.config.get("audio", "sfx_volume")) * 100)
    
    # Screen Size
    def resize_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), self.screen.get_flags())
        # Update the screen size in the config
        self.config.update("graphics", "width", str(width))
        self.config.update("graphics", "height", str(height))

    def toggle_fullscreen(self):
        if self.screen.get_flags() & pygame.FULLSCREEN:
            # Switch to windowed mode
            pygame.display.set_mode((self.config.get_width(), self.config.get_height()), pygame.RESIZABLE)
            self.config.update("graphics", "fullscreen", "False")
        else:
            # Switch to fullscreen mode
            pygame.display.set_mode((self.config.get_width(), self.config.get_height()), pygame.FULLSCREEN | pygame.RESIZABLE)
            self.config.update("graphics", "fullscreen", "True")


    # Change scene
    # def new_game(self):
    #     self.change_state(CharacterSelection(self))

    def show_main_menu(self):
        self.change_state(MainMenu(self))

    # def victory(self):
    #     self.change_state(VictoryScreen(self))

    def show_settings(self):
        if not self.settings_menu_open:
            self.states.append(SettingsMenu(self))
            self.settings_menu_open = True

    def hide_settings(self):
        if self.settings_menu_open:
            self.states.pop()
            self.settings_menu_open = False

    def quit_game(self):
        self.done = True

    def run(self):
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if isinstance(self.states[-1], SettingsMenu):
                            self.hide_settings()
                        else:
                            self.show_settings()
                self.states[-1].handle_event(event)
            for state in self.states:
                state.draw(self.canvas)
            pygame.transform.scale(self.canvas, (self.config.get_width(), self.config.get_height()), self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()