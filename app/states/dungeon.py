from app.states.components.room import Room
from app.states.combat import Combat
from app.logic.combat.characters.enemy import Enemy
from app.states.state import State
from app.constants import *
from pygame.locals import *
import pygame

class Dungeon(State):

    def __init__(self, game, game_data=None):
        # Call the parent class (State) constructor
        super().__init__(game)


        self.game = game
        self.player_position = (0, 0)
        self.rooms = []

        if game_data:
            self.load_data(game_data)
        else:
            self.generate_rooms()
            # set first room as next
            self.rooms[0][0].next = True

    def draw(self, surface):
        # Set white background
        surface.fill(WHITE)
        # Generate map
        for x in range(DUNGEON_SIZE_X):
            for y in range(DUNGEON_SIZE_Y):
                room = self.rooms[x][y]
                room.draw(surface)
        # Update the display
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == KEYDOWN:
            new_x, new_y = self.player_position
            if event.key == K_LEFT:
                new_x -= 1
            elif event.key == K_RIGHT:
                new_x += 1
            elif event.key == K_UP:
                new_y -= 1
            elif event.key == K_DOWN:
                new_y += 1

            if 0 <= new_x < DUNGEON_SIZE_X and 0 <= new_y < DUNGEON_SIZE_Y:
                self.move_to_room((new_x, new_y))

    def generate_rooms(self):
        for x in range(DUNGEON_SIZE_X):
            self.rooms.append([])
            for y in range(DUNGEON_SIZE_Y):
                position = (x, y)
                # Make an enemy character
                enemy = Enemy()
                room = Room(self.game, position, enemy)
                self.rooms[x].append(room)

    def move_to_room(self, position):
        self.player_position = position
        room = self.rooms[position[0]][position[1]]
        room.visited = True

        if room.enemy:
            self.game.save_game()
            self.game.combat = Combat(self.game, self.game.character, room.enemy)
            self.game.push_state(self.game.combat)
        else:
            self.update_player_position()
            self.draw(self.surface)

    def update_player_position(self):
        # move the player 1 room forward
        x, y = self.player_position
        # check if the player is at the end of the dungeon
        if x == DUNGEON_SIZE_X - 1 and y == DUNGEON_SIZE_Y - 1:
            self.game.victory()
        elif x == DUNGEON_SIZE_X - 1:
            # update the player position to the next row
            self.player_position = (0, y + 1)
        else:
            # update the player position to the next column
            self.player_position = (x + 1, y)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for row in self.rooms:
                for room in row:
                    room.handle_click(event)

    def get_data(self):
        return {
            "player_position": self.player_position,
            "rooms": [[room.get_data() for room in row] for row in self.rooms],
        }
    
    def load_data(self, game_data):
        self.player_position = game_data["player_position"]
        for x, row in enumerate(game_data["rooms"]):
            self.rooms.append([])
            for y, room_data in enumerate(row):
                position = (x, y)
                enemy = room_data["enemy"]
                next = room_data["next"]
                visited = room_data["visited"]
                completed = room_data["completed"]
                room = Room(self.game, position, enemy, next, visited, completed)
                self.rooms[x].append(room)