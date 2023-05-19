import pygame

# Screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# TEMP Dungeon size
DUNGEON_SIZE_X = 5
DUNGEON_SIZE_Y = 5

# Events
ENEMY_TURN_EVENT = pygame.USEREVENT + 1

# Turn Results
CONTINUE = "continue"
GAME_OVER = "game_over"
FLOOR_COMPLETE = "floor_complete"