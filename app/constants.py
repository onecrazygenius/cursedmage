import pygame, os, sys

# Screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# TEMP Dungeon size
DUNGEON_SIZE_X = 5
DUNGEON_SIZE_Y = 5

# Events
ENEMY_TURN_EVENT = pygame.USEREVENT + 1
PLAYER_TURN_EVENT = pygame.USEREVENT + 4
GAME_OVER_EVENT = pygame.USEREVENT + 2
PAUSE = pygame.USEREVENT + 3

PAUSE_TIME_MS = 1000
PAUSE_TIME_S = 1

# Turn Results
CONTINUE = "continue"
GAME_OVER = "game_over"
FLOOR_COMPLETE = "floor_complete"
FAILED = "failed"
END_TURN = "end_turn"

# resource path for pyinstaller.
# ONLY USE FOR RELATIVE FILE PATHS.
# For absolute paths (eg. the save files) this should not be used.
def relative_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path.lstrip('/'))