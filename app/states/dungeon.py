import json
import math
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
        self.root = []
        self.rooms = []

        self.active_popup = None

        self.scroll_offset = [0, 0]  # The current scroll offset
        self.dragging = False  # Whether the mouse is currently dragging
        self.drag_start = [0, 0]  # The position where the last drag started
        self.zoom_level = 1.0

        if game_data:
            # TODO: Loading doesn't work
            self.load_data(game_data)
        else:
            self.rooms = self.generate_rooms()
            self.root = self.rooms[0][0]
            self.root.next = True

            self.player_position = self.root

    def draw(self, surface):
        # Set background as background image
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/brick.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        # If the boss requirements are met, show the popup
        if self.game.character.boss_requirements_met():
            self.boss_appeared_popup("You are ready to challenge the boss at the end of this floor.")

        # Draw all of the rooms on the map
        self.draw_room(surface)

        # If there are any active popups, show them on the screen
        if self.active_popup is not None:
            # Draw the popup only if the difference between current time and popup start time is less than 2 seconds
            if pygame.time.get_ticks() - self.active_popup.start_time < DUNGEON_POPUP_DURATION_MS:
                self.active_popup.draw(surface)
            else:
                self.active_popup = None

        # Update the display
        pygame.display.flip()

    def draw_room(self, surface):
        # First draw lines to child rooms
        for level in self.rooms:
            for room in level:
                for child in room.children:
                    if room.rect is not None and child.rect is not None:
                        # Calculate parent and child center coordinates for line drawing
                        parent_center = ((room.rect.left + room.rect.width / 2),
                                         (room.rect.top + room.rect.height))
                        child_center = ((child.rect.left + child.rect.width / 2),
                                        (child.rect.top))  # Don't add height for top of sprite

                        # Draw a line between parent and child room
                        pygame.draw.line(surface, pygame.Color(DUNGEON_LINE), parent_center, child_center, 3)

                # Always draw rooms after lines so that the lines go behind rooms
                room.draw(surface, self.scroll_offset, self.zoom_level)


    def generate_rooms(self):
        # Create a list to hold all room layers
        rooms = []

        # Iterate over all layers
        for i in range(DUNGEON_SIZE_Y):
            # Determine the number of rooms for the current layer
            if i < DUNGEON_MIN_SIZE_X:
                num_rooms = i + 1
            else:
                prev_rooms = len(rooms[-1])
                num_rooms = random.randint(max(DUNGEON_MIN_SIZE_X, prev_rooms - 1), min(DUNGEON_MAX_SIZE_X, prev_rooms + 1))

            # Create the current layer with 'None' entries
            current_layer = [None for _ in range(num_rooms)]

            # Calculate the offset to center the rooms
            offset = (DUNGEON_MAX_SIZE_X - num_rooms) / 2.0

            # Iterate over all slots in the current layer
            for j in range(num_rooms):
                # Compute the position, adjusting for the offset
                position = (j + offset, i)

                # Create a room at the current position
                room = Room(self.game, position, self.create_enemies(*position))

                # Add the room to the current layer
                current_layer[j] = room

                # Assign parents and children
                if i > 0:  # If it's not the first layer
                    # Assign parent from the previous layer
                    for dx in [-1, 0, 1]:  # Check the rooms above and to the left, right, and directly above
                        parent_index = j + dx
                        if 0 <= parent_index < len(rooms[i - 1]):
                            parent_room = rooms[i - 1][parent_index]
                            if parent_room is not None and room not in parent_room.children:
                                # Avoid adding rooms as children if the relative distance is greater than 1
                                if abs(parent_room.position[0] - room.position[0]) <= 1:
                                    parent_room.children.append(room)
                                    room.parents.append(parent_room)

            # Add the current layer to the list of all layers
            rooms.append(current_layer)

        return rooms

    def generate_boss_room(self, replaced_room):
        # Room with boss configuration
        boss_enemy = Boss("Boss")
        boss_room = Room(self.game, replaced_room.position, [boss_enemy], is_boss_room=True)
        boss_room.parents = replaced_room.parents
        boss_room.children = replaced_room.children

        # Iterate over all parents of the replaced room
        for parent in replaced_room.parents:
            # Find the index of the replaced room in the children list of the current parent
            index = parent.children.index(replaced_room)
            # Replace the replaced room with the boss room in the children list of the current parent
            parent.children[index] = boss_room

        return boss_room

    # Based on the position of the room, between 1 and 3 enemies will be created whereas you progress
    # Through the dungeon, there is a higher chance of more enemies being in the room
    def create_enemies(self, room_position_x, room_position_y):
        # These factors control how much each variable contributes to the output.
        # Since DUNGEON_SIZE_Y should have a bigger impact, we give it a higher weight
        base_factor_x = 0
        base_factor_y = 1.2

        # Calculate the room's relative position in the dungeon
        relative_position_x = room_position_x / DUNGEON_MAX_SIZE_X
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

    def move_to_room(self, room):
        # The player is now in the new room
        self.player_position = room

        if not room.enemies_defeated():
            self.game.combat = Combat(self.game, self.game.character, room.enemies)
            self.game.change_state(self.game.combat)

    def update_rooms_recursive(self, room):
        room.next = (room.position == self.player_position)
        for child_room in room.children:
            self.update_rooms_recursive(child_room)

    def progress_to_next_room(self):
        self.player_position.completed = True
        self.player_position.next = False

        # First, for the room you just cleared, set its siblings' children next to false, blocking the tree
        for parent in self.player_position.parents:
            for sibling in parent.children:
                sibling.next = False

        # Then, set the player's current room children next to true, opening the tree
        for child in self.player_position.children:
            child.next = True

        if self.game.character.boss_requirements_met():
            # Randomly select a floor between 2-5 floors below
            boss_floor = min(len(self.rooms) - 1, self.player_position.position[1] + random.randint(2, 3))

            # Replace a random room on the selected floor with a boss room
            boss_room_index = random.randint(0, len(self.rooms[boss_floor]) - 1)
            boss_room = self.generate_boss_room(self.rooms[boss_floor][boss_room_index])

            self.rooms[boss_floor][boss_room_index] = boss_room

        self.game.save_game()

    def handle_event(self, event):
        # Handle dragging the map around
        if event.type == pygame.MOUSEMOTION:
            # If currently dragging, adjust the scroll offset based on the mouse motion
            if self.dragging:
                dx, dy = event.rel  # The relative motion of the mouse since the last event
                self.scroll_offset[1] -= dy

        # Handle zooming in and out of the map
        if event.type == pygame.MOUSEWHEEL:
            # Adjust the zoom level based on the mouse wheel motion
            self.zoom_level *= 1.1 ** event.y
            # Limit to 70% - 130% Zoom Levels
            self.zoom_level = min(max(self.zoom_level, 0.7), 1.3)

        # Handle check if a room was clicked or begin dragging the map
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Start dragging
            self.dragging = True
            self.drag_start = list(event.pos)

        # Handle letting go of the map to stop dragging
        if event.type == MOUSEBUTTONUP:
            # Stop dragging
            self.dragging = False
            self.handle_room_click(event)

    def handle_room_click(self, event):
        # Traverse the dungeon and check if any room was clicked
        if self.handle_room_click_recursive(self.root, event.pos):
            return True
        return False

    def handle_room_click_recursive(self, room, pos):
        if room.rect.collidepoint(pos):
            # Only allow the user to click on a room that is opened (Next)
            if room.next:
                self.move_to_room(room)
                return True
        for child_room in room.children:
            if self.handle_room_click_recursive(child_room, pos):
                return True
        return False

    def get_data(self):
        return {
            "player_position": self.player_position.get_data(),
            "rooms": [[room.get_data() for room in row] for row in self.rooms],
        }

    # TODO: Loading is currently broken
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
