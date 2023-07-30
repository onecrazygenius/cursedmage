import os
import pygame
import sys

# Debug Mode
DEBUG = False

# Screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DUNGEON_LINE = (145, 142, 142, 30)

BUTTON_BACKGROUND = (247, 58, 33)
BUTTON_SHADOW = BLACK

# TEMP Dungeon size
DUNGEON_MAX_SIZE_X = 6  # The max width of the dungeon
DUNGEON_MIN_SIZE_X = 2
DUNGEON_SIZE_Y = 200  # The max depth of the dungeon, this is effectively endless

DIFFICULTY_SCALING_CONSTANT = 20  # This means after ~ 20 floors you will hit max difficulty

# Events
ENEMY_TURN_EVENT = pygame.USEREVENT + 1
PLAYER_TURN_EVENT = pygame.USEREVENT + 4
GAME_OVER_EVENT = pygame.USEREVENT + 2
PAUSE = pygame.USEREVENT + 3

PAUSE_TIME_MS = 1000
PAUSE_TIME_S = 1

# Popup Durations
COMBAT_POPUP_DURATION_MS = 1500
DUNGEON_POPUP_DURATION_MS = 2500

# Difficulties
DIFFICULTIES = ["Easy", "Normal", "Hard"]
DIFFICULTY_INT_MAPPING = {  # Used in difficulty scaling calculations
    "Easy": 1,
    "Normal": 2,
    "Hard": 3
}

# The score value of rooms and enemies
SCORE_VALUE = {
    "Goblin": 10,
    "Brute": 25,
    "Reaper": 50,
    "Boss": 100,
    "Room": 5,
    "Boss_Room": 10
}

# % Chance to pickup a cursed card after each combat
CURSED_CARD_CHANCE = 100

# Number of Cursed Cards required for the boss room to open
BOSS_CURSED_CARD_REQUIREMENT = 2

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