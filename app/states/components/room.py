import pygame
from pygame.locals import *

class Room:
    def __init__(self, game, position, enemies=[], next=False, visited=False, completed=False):
        self.game = game
        self.position = position
        self.enemies = enemies
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
        x, y = self.position
        rect = pygame.Rect(x * 100 + 50, y * 100 + 50, 50, 50)
        if event.type == MOUSEBUTTONUP and event.button == 1:
            if rect.collidepoint(event.pos) and not self.completed:
                # Check if the room is the next available room starting with 0,0
                if self.position == self.game.dungeon.player_position:
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