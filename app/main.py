import pygame, pickle, os
from pygame.locals import *
from app.engine.constants import *
from app.menus.main_menu import MainMenu
from app.menus.character_selection import CharacterSelection
from app.menus.dungeon import Dungeon
from app.menus.settings_menu import SettingsMenu
from app.menus.victory_screen import VictoryScreen


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

        self.character = None
        self.difficulty = None

        self.states = [MainMenu(self)]

        self.dungeon = None
        self.combat = None

        self.settings_menu_open = False  # Flag to track if the settings menu is open

    def resize_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), self.screen.get_flags())

    def toggle_fullscreen(self):
        if self.screen.get_flags() & pygame.FULLSCREEN:
            # Switch to windowed mode
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        else:
            # Switch to fullscreen mode
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.RESIZABLE)


    def push_state(self, state):
        self.states.append(state)

    def pop_state(self):
        if self.states:
            self.states.pop()

    def change_state(self, state):
        if self.states:
            self.pop_state()
        self.push_state(state)

    def new_game(self):
        self.change_state(CharacterSelection(self))

    def save_game(self):
        with open("savegame.pkl", "wb") as savefile:
            game_data = {
                "character": self.character,
                "difficulty": self.difficulty,
                "dungeon": self.dungeon.get_data(),
            }
            pickle.dump(game_data, savefile)

    def load_game(self):
        try:
            with open("savegame.pkl", "rb") as savefile:
                game_data = pickle.load(savefile)
                self.character = game_data["character"]
                self.difficulty = game_data["difficulty"]
                self.dungeon = Dungeon(self, game_data=game_data["dungeon"])
                self.change_state(self.dungeon)
        except FileNotFoundError:
            print("No save file found.")

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