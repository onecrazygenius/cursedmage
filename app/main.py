from app.engine.config_manager import ConfigManager
from app.engine.save_manager import SaveManager
from app.engine.constants import *
from app.menus.character_selection import CharacterSelection
from app.menus.victory_screen import VictoryScreen
from app.menus.settings_menu import SettingsMenu
from app.menus.main_menu import MainMenu
from app.menus.dungeon import Dungeon
from pygame.locals import *
import pygame, os


class Game:
    def __init__(self):
        # Initialize pygame and pygame.mixer
        pygame.init()
        pygame.mixer.init()

        # Initialize the screen and clock
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        path = os.path.dirname(os.path.abspath(__file__))
        # Set the window title and icon in assets/images
        icon = pygame.image.load(os.path.join(path, "assets/images/team_logo.png"))
        
        pygame.display.set_caption("Cursed Mage")
        pygame.display.set_icon(icon)

        # Initialize game variables
        self.done = False
        self.save_manager = SaveManager()
        self.config = ConfigManager()

        self.character = None
        self.difficulty = None

        self.states = [MainMenu(self)]

        self.dungeon = None
        self.combat = None

        self.settings_menu_open = False  # Flag to track if the settings menu is open

    def resize_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), self.screen.get_flags())
        # Update the screen size in the config
        self.config.update("graphics", "width", str(width))
        self.config.update("graphics", "height", str(height))

    def toggle_fullscreen(self):
        if self.screen.get_flags() & pygame.FULLSCREEN:
            # Switch to windowed mode
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            self.config.update("graphics", "fullscreen", "False")
        else:
            # Switch to fullscreen mode
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.RESIZABLE)
            self.config.update("graphics", "fullscreen", "True")


    def push_state(self, state):
        self.states.append(state)

    def pop_state(self):
        if self.states:
            self.states.pop()

    def change_state(self, state):
        if self.states:
            self.pop_state()
        self.push_state(state)

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
        self.dungeon = Dungeon(self, game_data=data["dungeon"])
        self.change_state(self.dungeon)

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

    def new_game(self):
        self.change_state(CharacterSelection(self))

    def show_main_menu(self):
        self.change_state(MainMenu(self))

    def show_settings(self):
        self.states.append(SettingsMenu(self))
        self.settings_menu_open = True

    def hide_settings(self):
        self.states.pop()
        self.settings_menu_open = False

    def quit_game(self):
        self.done = True

    def victory(self):
        self.change_state(VictoryScreen(self))

    def run(self):
        while not self.done:
            self.clock.tick(60)
            current_state = self.states[-1]  # Reference the current state as the top of the stack
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if isinstance(current_state, SettingsMenu):
                            self.hide_settings()
                        elif isinstance(current_state, MainMenu) and self.settings_menu_open:
                            self.hide_settings()
                        else:
                            self.show_settings()
                if current_state:
                    current_state.handle_event(event)

            current_state.draw()
        
        # Quit the game
        pygame.mixer.quit()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()