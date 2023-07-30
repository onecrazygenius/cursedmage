import os
import pygame
import sys

# Screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Animation
FRAMES_IN_SPRITESHEET = 8
ANIMATION_SPEED = 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BUTTON_BACKGROUND = (247, 58, 33)
BUTTON_SHADOW = BLACK

# TEMP Dungeon size
DUNGEON_SIZE_X = 5
DUNGEON_SIZE_Y = 5

# Events
ENEMY_TURN_EVENT = pygame.USEREVENT + 1
PLAYER_TURN_EVENT = pygame.USEREVENT + 4
GAME_OVER_EVENT = pygame.USEREVENT + 2
PAUSE = pygame.USEREVENT + 3
UNPAUSE = pygame.USEREVENT + 4

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

# % Chance to pickup a cursed card after each combat
CURSED_CARD_CHANCE = 25

# Number of Cursed Cards required for the boss room to open
BOSS_CURSED_CARD_REQUIREMENT = 3

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