import json
import random

import numpy
from pygame.locals import *

from app.constants import *
from app.logic.combat.characters.boss import Boss
from app.logic.combat.characters.enemy import Enemy
from app.states.combat import Combat
from app.states.components.popup import Popup
from app.states.components.room import Room
from app.states.state import State
from app.util.run_once import run_once


class Dungeon(State):

    def __init__(self, game, game_data=None):
        # Call the parent class (State) constructor
        super().__init__(game)


        self.game = game
        self.player_position = (0, 0)
        self.rooms = []
        self.boss_room = self.generate_boss_room() # The boss room is always the same at the moment, so can be generated

        self.active_popup = None

        if game_data:
            self.load_data(game_data)
        else:
            self.generate_rooms()
            # set first room as next
            self.rooms[0][0].next = True

    def draw(self, surface):
        # Set background as background image
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/brick.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))
        # Generate map

        # If the boss requirements are met, draw the room
        if self.game.character.boss_requirements_met():
            self.boss_appeared_popup("The boss has finally shown itself! Challenge it at the red-outlined door.")
            # If you managed to get to the boss, you completed the first floor. So for now override it
            # TODO: In map rework give this a proper position
            self.rooms[self.boss_room.position[0]][self.boss_room.position[1]] = self.boss_room
        for x in range(DUNGEON_SIZE_X):
            for y in range(DUNGEON_SIZE_Y):
                room = self.rooms[x][y]
                room.draw(surface)

        # If there are any active popups, show them on the screen
        if self.active_popup is not None:
            # Draw the popup only if the difference between current time and popup start time is less than 2 seconds
            if pygame.time.get_ticks() - self.active_popup.start_time < DUNGEON_POPUP_DURATION_MS:
                self.active_popup.draw(surface)
            else:
                self.active_popup = None

        # Update the display
        pygame.display.flip()

    def generate_rooms(self):
        for x in range(DUNGEON_SIZE_X):
            self.rooms.append([])
            for y in range(DUNGEON_SIZE_Y):
                position = (x, y)
                # Create the enemies for the room
                enemies = self.create_enemies(x, y)
                room = Room(self.game, position, enemies)
                self.rooms[x].append(room)

    def generate_boss_room(self):
        # Create boss room if requirements are met
        boss_position = (0, 0)  # For now put this position at 0,0. This should be changed eventually
        boss_enemy = Boss("Boss")
        return Room(self.game, boss_position, [boss_enemy], is_boss_room=True)

    # Based on the position of the room, between 1 and 3 enemies will be created whereas you progress
    # Through the dungeon, there is a higher chance of more enemies being in the room
    def create_enemies(self, room_position_x, room_position_y):
        # These factors control how much each variable contributes to the output.
        # Since DUNGEON_SIZE_Y should have a bigger impact, we give it a higher weight
        base_factor_x = 0.3
        base_factor_y = 0.7

        # Calculate the room's relative position in the dungeon
        relative_position_x = room_position_x / DUNGEON_SIZE_X
        relative_position_y = room_position_y / DUNGEON_SIZE_Y

        # Based on the room position and the base factor of the X and Y dimensions, create a weighted position value
        relative_position_weighted = base_factor_x * relative_position_x + base_factor_y * relative_position_y

        # Add some randomness to the calculation. This will add a random value between -0.2 and 0.2 to the result
        # This randomness scales with the difficulty
        difficulty_multiplier = DIFFICULTY_INT_MAPPING[self.game.difficulty]
        randomness = numpy.random.uniform(-0.2 / difficulty_multiplier, 0.2 * difficulty_multiplier)

        # Scale the relative position to the range of 1-3 and add randomness
        # Use 1 + 2 to ensure the minimum value will be 1 before randomness instead of 0 if just 3 was used.
        scaled_enemy_number = 1 + 2 * (relative_position_weighted + randomness)

        # Make sure the result stays within the range of 1-3
        scaled_enemy_number_within_bounds = max(min(scaled_enemy_number, 3), 1)

        number_of_enemies = round(scaled_enemy_number_within_bounds)
        enemy_names = self.choose_enemy_names_from_difficulty(scaled_enemy_number_within_bounds, number_of_enemies)
        enemies = []
        for name in enemy_names:
            enemies.append(Enemy(name))

        # These are extremely useful to debug this method. Leaving these here intentionally
        # print("Room ["+str(room_position_x)+","+str(room_position_y)+"]")
        # print("Room Difficulty: " + str(scaled_enemy_number_within_bounds))
        # print("Randomness: " + str(randomness))
        # print("Number Of Enemies: " + str(number_of_enemies))
        # print("Enemies: " + str(enemy_names))
        # print("\n")
        return enemies

    def choose_enemy_names_from_difficulty(self, difficulty_threshold, number_of_enemies):
        json_file = (relative_resource_path('app/assets/data/enemies.json'))
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Get a list of names where the difficulty is less than or equal to the threshold
        eligible_names = [enemy['name'] for enemy in data if enemy['difficulty'] <= difficulty_threshold]
        return random.choices(eligible_names, k=number_of_enemies)

    def move_to_room(self, position):
        self.player_position = position
        room = self.rooms[position[0]][position[1]]
        room.visited = True

        if not room.enemies_defeated():
            self.game.save_game()
            self.game.combat = Combat(self.game, self.game.character, room.enemies)
            self.game.change_state(self.game.combat)
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
        if x == DUNGEON_SIZE_X - 1:
            # update the player position to the next row
            self.player_position = (0, y + 1)
        else:
            # update the player position to the next column
            self.player_position = (x + 1, y)

    def win_conditions_met(self):
        return self.player_position == self.boss_room.position and self.game.character.boss_requirements_met()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            # The Boss Room is not in Rooms as it's not part of the standard dungeon. Also check if it was clicked
            self.boss_room.handle_click(event)
            # Iterate over all rooms to see if one was clicked
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
    @run_once
    def boss_appeared_popup(self, text):
        popup = Popup(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            pygame.time.get_ticks(),
            text,
            width=575,
            height=100,
        )
        self.active_popup = popup