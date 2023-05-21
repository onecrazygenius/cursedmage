# app/main.py
from app.logic.config_manager import ConfigManager
from app.logic.save_manager import SaveManager
from app.constants import *
from app.states.character_selection import CharacterSelection
from app.states.victory_screen import VictoryScreen
from app.states.settings import SettingsMenu
from app.states.main_menu import MainMenu
from app.states.dungeon import Dungeon
import pygame, os

# Game class definition
class Game:

    """
        This class represents the main control flow for the game "Cursed Mage".
        It manages the game states, settings, sound volume, screen size, 
        and loading/saving game data.
        
        Attributes:
            config (ConfigManager): Configuration manager for game settings.
            save_manager (SaveManager): Manages saving and loading game data.

            screen (pygame.Surface): The main display surface.
            surface (pygame.Surface): The surface on which game states are drawn.
            clock (pygame.time.Clock): Game clock for managing frame rate.

            done (bool): A flag indicating whether the game loop should continue running.

            character: The player character.
            difficulty: The game difficulty level.

            states (list): A list representing the stack of game states.
            just_switched (bool): A flag indicating whether the game state has just changed.
            
            settings_menu_open (bool): A flag indicating whether the settings menu is currently open.
    """

    def __init__(self):
        # Initialize pygame and pygame.mixer
        pygame.init()
        pygame.mixer.init()

        # Initialize config and save manager instances
        self.config = ConfigManager()
        self.save_manager = SaveManager()

        # Initialize screen and clock with config-provided width and height
        self.screen = pygame.display.set_mode((self.config.get_width(), self.config.get_height()))
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        path = os.path.dirname(os.path.abspath(__file__))

        # Load game icon and set window caption
        icon = pygame.image.load(os.path.join(path, "assets/images/team_logo.png"))
        pygame.display.set_caption("Cursed Mage")
        pygame.display.set_icon(icon)

        # Initialize basic game state variables
        self.done = False
        self.character = None
        self.difficulty = None
        self.just_switched = False

        # Initialize game state stack
        self.states = [MainMenu(self)]

        # Flag for tracking if the settings menu is currently open
        self.settings_menu_open = False  

    # State management functions

    def push_state(self, state):
        # Add a new state to the state stack
        self.states.append(state)

    def pop_state(self):
        # Remove the current state from the state stack
        if self.states:
            self.states.pop()

    def change_state(self, state):
        # Change the current state by popping the old one and pushing the new one
        if self.states:
            self.pop_state()
        self.push_state(state)
        self.just_switched = True

    def screen_to_canvas(self, pos):
        # Convert screen coordinates to canvas coordinates
        return pos[0] - (self.config.get_width() - SCREEN_WIDTH) // 2, pos[1] - (self.config.get_height() - SCREEN_HEIGHT) // 2

    # Game data management functions

    def save_game(self):
        # Save game data with the save manager
        game_data = {"character": self.character, "difficulty": self.difficulty, "dungeon": self.dungeon.get_data()}
        self.save_manager.save(game_data)

    def load_game(self):
        # Load game data with the save manager
        data = self.save_manager.load()
        if not data:  # If there is no data, return immediately
            return
        # Set up the game with the loaded data
        self.character = data["character"]
        self.difficulty = data["difficulty"]
        self.dungeon = Dungeon(self, game_data=data["dungeon"])
        self.change_state(self.dungeon)

    # Sound volume management functions

    def change_master_volume(self, volume):
        # Set master volume and save the change in config
        volume = float(volume) / 100
        pygame.mixer.music.set_volume(volume)
        self.config.update("audio", "master_volume", str(volume))

    def change_sfx_volume(self, volume):
        # Set SFX volume and save the change in config
        volume = float(volume) / 100
        self.config.update("audio", "sfx_volume", str(volume))

    def get_master_volume(self):
        # Get current master volume from config
        return int(float(self.config.get("audio", "master_volume")) * 100)
    
    def get_sfx_volume(self):
        # Get current SFX volume from config
        return int(float(self.config.get("audio", "sfx_volume")) * 100)
    
    # Screen size management functions

    def resize_screen(self, width, height):
        # Resize the screen and save the new dimensions in config
        self.screen = pygame.display.set_mode((width, height), self.screen.get_flags())
        self.config.update("graphics", "width", str(width))
        self.config.update("graphics", "height", str(height))

    def toggle_fullscreen(self):
        # Toggle fullscreen mode and save the change in config
        if self.screen.get_flags() & pygame.FULLSCREEN:
            pygame.display.set_mode((self.config.get_width(), self.config.get_height()), pygame.RESIZABLE)
            self.config.update("graphics", "fullscreen", "False")
        else:
            pygame.display.set_mode((self.config.get_width(), self.config.get_height()), pygame.FULLSCREEN | pygame.RESIZABLE)
            self.config.update("graphics", "fullscreen", "True")

    # Scene change functions

    def new_game(self):
        # Start a new game by changing to the character selection state
        self.change_state(CharacterSelection(self))

    def show_main_menu(self):
        # Show the main menu by changing to the main menu state
        self.change_state(MainMenu(self))

    def victory(self):
        # Go to the victory screen by changing to the victory screen state
        print("Victory!")
        self.change_state(VictoryScreen(self))

    def show_dungeon(self):
        # Show the dungeon by changing to the dungeon state
        self.change_state(self.dungeon)

    def show_settings(self):
        # Show the settings menu by pushing the settings menu state onto the stack
        if not self.settings_menu_open:
            self.states.append(SettingsMenu(self))
            self.settings_menu_open = True

    def hide_settings(self):
        # Hide the settings menu by popping the settings menu state from the stack
        if self.settings_menu_open:
            self.states.pop()
            self.settings_menu_open = False

    def quit_game(self):
        # Quit the game by setting the 'done' flag
        self.done = True

    def run(self):
        # Main game loop
        while not self.done:
            self.clock.tick(60)  # Limit the game to 60 frames per second
            # Process pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # If ESC is pressed, show/hide settings depending on current state
                        if isinstance(self.states[-1], SettingsMenu):
                            self.hide_settings()
                        else:
                            self.show_settings()
                self.states[-1].handle_event(event)
            # Draw the current state
            for state in self.states:
                state.draw(self.surface)
            # Scale the surface to the screen size and display it
            pygame.transform.scale(self.surface, (self.config.get_width(), self.config.get_height()), self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    # If this script is the main entry point, create a game instance and run it
    game = Game()
    game.run()
