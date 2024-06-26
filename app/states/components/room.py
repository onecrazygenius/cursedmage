from pygame.locals import *

from app.constants import *


class Room:
    DOOR_SPRITES = {
        "locked": pygame.image.load(relative_resource_path("app/assets/images/backgrounds/doors/locked.png")),
        "broken": pygame.image.load(relative_resource_path("app/assets/images/backgrounds/doors/broken.png")),
        "open": pygame.image.load(relative_resource_path("app/assets/images/backgrounds/doors/open.png")),
        "unlocked": pygame.image.load(relative_resource_path("app/assets/images/backgrounds/doors/unlocked.png")),
        "unlocked_boss": pygame.image.load(relative_resource_path("app/assets/images/backgrounds/doors/unlocked_boss.png")),
        "locked_boss": pygame.image.load(relative_resource_path("app/assets/images/backgrounds/doors/locked_boss.png")),
        "broken_boss": pygame.image.load(relative_resource_path("app/assets/images/backgrounds/doors/broken_boss.png")),
        "open_boss": pygame.image.load(relative_resource_path("app/assets/images/backgrounds/doors/open_boss.png"))
    }

    def __init__(self, game, position, enemies=None, next=False, visited=False, completed=False, is_boss_room=False):
        self.game = game
        self.position = position
        if enemies is None:
            enemies = []
        self.enemies = enemies
        self.next = next
        self.visited = visited
        self.completed = completed
        self.is_boss_room = is_boss_room

        self.children = []  # List of connected rooms
        self.parents = []  # The room(s) that leads to this room
        self.offset = [0, 0]

        self.rect = None
        self.room_sprite = None

    def draw(self, screen, offset=(0, 0), zoom_level=1.0):
        x, y = self.position
        # Update the scroll offset
        self.offset = offset

        # calculate offset
        screen_width = screen.get_width()
        gap = screen_width - (DUNGEON_MAX_SIZE_X * 300 * zoom_level) + 140 * zoom_level
        self.offset = gap / 2

        # calculate position with offset, scrolling, and zooming
        pos_x = self.offset + (x * 300 * zoom_level) - offset[0]
        pos_y = -(50 * zoom_level + (y * 280 * zoom_level) - offset[1])

        # update rect
        self.rect = pygame.Rect(pos_x, pos_y, int(100 * zoom_level), int(140 * zoom_level))

        # Only draw if the room is visible
        if not self.rect.colliderect(screen.get_rect()):
            return

        door_type = "locked"
        # if the room is complete make the door open
        if self.next:
            door_type = "unlocked"
        if self.visited:
            door_type = "open"
        if self.completed:
            door_type = "broken"
        # if the room is a boss room
        if self.is_boss_room:
            door_type = door_type + "_boss"

        # To prevent loading from files every time you draw the room, save the sprite and just check if it's none or changed
        if self.room_sprite is None or Room.DOOR_SPRITES[door_type] is not self.room_sprite:
            self.room_sprite = Room.DOOR_SPRITES[door_type]
            self.room_sprite = pygame.transform.scale(self.room_sprite, (int(100 * zoom_level), int(140 * zoom_level)))

        # make so that row of rooms are spaced out to the width of the screen
        screen.blit(self.room_sprite, (pos_x, pos_y))

    def handle_click(self, event):
        x, y = self.position

        # calculate the rect of the room
        rect = pygame.Rect(self.offset + (x * 300), 50 + (y * 280), 100, 140)

        if event.type == MOUSEBUTTONUP and event.button == 1:
            if rect.collidepoint(self.game.screen_to_surface(event.pos)) and not self.completed:
                # Check if the room is the next available room starting with 0,0 or if it was the boss room
                if self.position == self.game.dungeon.player_room or self.is_boss_room:
                    self.game.dungeon.move_to_room(self.position)


    def calculate_score(self):
        score = 0
        for enemy in self.enemies:
            score += SCORE_VALUE.get(enemy.name)
        if self.is_boss_room:
            score += SCORE_VALUE.get("Boss_Room")
        else:
            score += SCORE_VALUE.get("Room")
        return score

    def get_data(self):
        return {
            "position": self.position,
            "next": self.next,
            "visited": self.visited,
            "completed": self.completed
        }

    def has_enemies(self):
        return len(self.enemies) > 0

    def enemies_defeated(self):
        return all([enemy.cur_health <= 0 for enemy in self.enemies])
