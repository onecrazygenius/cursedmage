import numpy

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
                # Create the enemies for the room
                enemies = self.create_enemies(x, y)
                room = Room(self.game, position, enemies)
                self.rooms[x].append(room)

    # Based on the position of the room, between 1 and 3 enemies will be created where as you progress
    # Through the dungeon, there is a higher chance of more enemies being in the room
    def create_enemies(self, room_position_x, room_position_y):
        # These factors control how much each variable contributes to the output.
        # Since DUNGEON_SIZE_Y should have a bigger impact, we could give it a higher weight
        base_factor_x = 0.3
        base_factor_y = 0.7

        # Calculate the room's relative position in the dungeon
        relative_position_x = room_position_x / DUNGEON_SIZE_X
        relative_position_y = room_position_y / DUNGEON_SIZE_Y

        # Based on the room position and the base factor of the X and Y dimensions, create a weighted position value
        relative_position_weighted = base_factor_x * relative_position_x + base_factor_y * relative_position_y

        # Add some randomness to the calculation. This will add a random value between -0.2 and 0.2 to the result
        randomness = numpy.random.uniform(-0.2, 0.2)

        # Scale the relative position to the range of 1-3 and add randomness
        # Use 1 + 2 to ensure the minimum value will be 1 before randomness instead of 0 if just 3 was used.
        scaled_position = 1 + 2 * (relative_position_weighted + randomness)

        # Make sure the result stays within the range of 1-3
        scaled_position_within_bounds = max(min(scaled_position, 3), 1)

        number_of_enemies = round(scaled_position_within_bounds)
        enemies = []
        for i in range(number_of_enemies):
            enemies.append(Enemy())

        return enemies

    def move_to_room(self, position):
        self.player_position = position
        room = self.rooms[position[0]][position[1]]
        room.visited = True

        if not room.enemies_defeated():
            self.game.save_game()
            self.game.combat = Combat(self.game, self.game.character, room.enemies)
            self.game.push_state(self.game.combat)
        else:
            self.update_player_position()
            self.draw(self.surface)

    def progress_to_next_room(self):
        x, y = self.player_position
        room = self.rooms[x][y]
        room.completed = True
        room.next = False
        self.update_player_position()
        self.rooms[self.player_position[0]][self.player_position[1]].next = True
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
                enemies = room_data["enemies"]
                next = room_data["next"]
                visited = room_data["visited"]
                completed = room_data["completed"]
                room = Room(self.game, position, enemies, next, visited, completed)
                self.rooms[x].append(room)