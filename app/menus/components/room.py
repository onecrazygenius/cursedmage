import pygame
from pygame.locals import *

class Room:
    def __init__(self, game, position, enemy=None, next=False, visited=False, completed=False):
        self.game = game
        self.position = position
        self.enemy = enemy
        self.next = next
        self.visited = visited
        self.completed = completed

    def draw(self, screen):
        x, y = self.position
        rect = pygame.Rect(x * 100 + 50, y * 100 + 50, 50, 50)
        room_surface = pygame.Surface((50, 50))
        
        if self.completed:
            room_surface.fill((0, 255, 0))
        elif self.visited:
            room_surface.fill((0, 0, 255))
        elif self.next:
            room_surface.fill((255, 0, 0))
        else:
            room_surface.fill((0, 0, 0))

        screen.blit(room_surface, rect)

    def handle_click(self, event):
        if self.visited:
            return
        
        x, y = self.position
        rect = pygame.Rect(x * 100 + 50, y * 100 + 50, 50, 50)
        if event.type == MOUSEBUTTONUP and event.button == 1:
            if rect.collidepoint(event.pos) and not self.visited:
                print(f"Clicked on room at position {self.position}")
                # Check if the room is the next available room starting with 0,0
                if self.position == self.game.dungeon.player_position:
                    self.game.dungeon.move_to_room(self.position)

    def get_data(self):
        return {
            "enemy": self.enemy,
            "next": self.next,
            "visited": self.visited,
            "completed": self.completed,
        }