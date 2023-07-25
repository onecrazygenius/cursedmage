import pygame
from pygame.locals import *
from app.constants import *

class Room:
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

    def draw(self, screen, offset=(0, 0), zoom_level=1.0):
        x, y = self.position
        # Update the scroll offset
        self.offset = offset

        door_type = "locked"
        # if the room is complete make the door open
        if self.completed:
            door_type = "broken"
        if self.visited:
            door_type = "open"
        # if the room is the next room the player should go to make the door unlocked
        if self.next:
            door_type = "unlocked"

        # if the room is a boss room
        if self.is_boss_room:
            door_type = "unlocked_boss"

        # draw the room image
        room_sprite = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/doors/{}.png".format(door_type)))
        room_sprite = pygame.transform.scale(room_sprite, (int(100 * zoom_level), int(140 * zoom_level)))

        # calculate offset
        screen_width = screen.get_width()
        gap = screen_width - (DUNGEON_SIZE_X * 300 * zoom_level) + 140 * zoom_level
        self.offset = gap / 2

        # calculate position with offset, scrolling, and zooming
        pos_x = self.offset + (x * 300 * zoom_level) - offset[0]
        pos_y = 50 * zoom_level + (y * 280 * zoom_level) - offset[1]

        # update rect
        self.rect = pygame.Rect(pos_x, pos_y, int(100 * zoom_level), int(140 * zoom_level))
        # print(f"Updated rect for room at position {self.position} to {self.rect}")

        # make so that row of rooms are spaced out to the width of the screen
        screen.blit(room_sprite, (pos_x, pos_y))

    def handle_click(self, event):
        x, y = self.position

        # calculate the rect of the room
        rect = pygame.Rect(self.offset + (x * 300), 50 + (y * 280), 100, 140)

        if event.type == MOUSEBUTTONUP and event.button == 1:
            if rect.collidepoint(self.game.screen_to_surface(event.pos)) and not self.completed:
                # DONE: print("Clicked on room at position", self.position)
                # Check if the room is the next available room starting with 0,0 or if it was the boss room
                if self.position == self.game.dungeon.player_position or self.is_boss_room:
                    self.game.dungeon.move_to_room(self.position)

    def get_data(self):
        return {
            "enemies": self.enemies,
            "next": self.next,
            "visited": self.visited,
            "completed": self.completed,
        }
    
    def has_enemies(self):
        return len(self.enemies) > 0
    
    def enemies_defeated(self):
        return all([enemy.cur_health <= 0 for enemy in self.enemies])