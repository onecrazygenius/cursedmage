import json
import random
import time

import numpy
from matplotlib import pyplot as plt
from pygame.locals import *

from app.constants import *
from app.logging_config import logger
from app.logic.combat.characters.boss import Boss
from app.logic.combat.characters.enemy import Enemy
from app.states.combat import Combat
from app.states.components.popup import Popup
from app.states.components.room import Room
from app.states.state import State


class Dungeon(State):

    def __init__(self, game, game_data=None):
        logger.debug("Beginning Dungeon Initialisation")
        start_time = time.perf_counter()

        # Call the parent class (State) constructor
        super().__init__(game)

        self.game = game
        self.root = []
        self.rooms = []

        self.active_popup = None

        self.scroll_offset = [0, SCREEN_HEIGHT / 2]  # The current scroll offset
        self.dragging = False  # Whether the mouse is currently dragging
        self.drag_start = [0, 0]  # The position where the last drag started
        self.zoom_level = 1.0

        self.generated_difficulties = {}

        self.vignette_image = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/vignette.png")).convert_alpha()
        self.vignette_pos = None

        logger.debug(f"Constants Setup in {time.perf_counter() - start_time:0.4f} seconds")

        if game_data:
            self.rooms = self.generate_rooms(game_data["structure"])
            self.root = self.rooms[0][0]

            self.player_room = next(room for room in self.rooms[game_data["player_position"][1]] if room.position[0] == game_data["player_position"][0])
            self.boss_room_position = game_data["boss_room_position"]
            if self.boss_room_position is not None:
                self.generate_boss_room(self.boss_room_position)
        else:
            self.rooms = self.generate_rooms()
            self.root = self.rooms[0][0]
            self.root.next = True

            self.player_room = self.root
            self.boss_room_position = None

        logger.debug(f"Dungeon Initialised in {time.perf_counter() - start_time:0.4f} seconds")

    def draw(self, surface):
        # Set background as background image
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/brick.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        # Draw all of the rooms on the map
        self.draw_room(surface)

        # Draw the vignette around the players room position
        # Only calculate the vignette position if it was set to none, this indicates that it should have moved
        self.vignette_pos = self.calculate_vignette_pos()
        surface.blit(self.vignette_image, self.vignette_pos)

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
                        if room is self.player_room:
                            # Calculate parent and child center coordinates for line drawing
                            parent_center = ((room.rect.left + room.rect.width / 2),
                                             (room.rect.bottom - room.rect.height))
                            child_center = ((child.rect.left + child.rect.width / 2),
                                            (child.rect.bottom))  # Don't add height for top of sprite

                            # Draw a line between parent and child room
                            pygame.draw.line(surface, pygame.Color(DUNGEON_LINE), parent_center, child_center, 3)

                # Always draw rooms after lines so that the lines go behind rooms
                room.draw(surface, self.scroll_offset, self.zoom_level)

    def calculate_vignette_pos(self):
        vignette_pos = (
            self.player_room.rect.centerx - self.vignette_image.get_width() // 2,
            self.player_room.rect.centery - self.vignette_image.get_height() // 2
        )
        return vignette_pos

    def generate_rooms(self, loaded_structure=None):
        logger.debug("Generating Rooms...")
        start_time = time.perf_counter()
        # Create a list to hold all room layers
        rooms = []

        # Iterate over all layers
        for i in range(DUNGEON_SIZE_Y):
            # Determine the number of rooms for the current layer
            if loaded_structure is not None:  # Loaded game
                num_rooms = len(loaded_structure[i])
            else:
                if i < DUNGEON_MIN_SIZE_X:
                    num_rooms = i + 1
                else:
                    prev_rooms = len(rooms[-1])
                    num_rooms = random.randint(max(DUNGEON_MIN_SIZE_X, prev_rooms - 1),
                                               min(DUNGEON_MAX_SIZE_X, prev_rooms + 1))


            # Create the current layer with 'None' entries
            current_layer = [None for _ in range(num_rooms)]

            # Calculate the offset to center the rooms
            offset = (DUNGEON_MAX_SIZE_X - num_rooms) / 2.0

            # Iterate over all slots in the current layer
            for j in range(num_rooms):
                # Compute the position, adjusting for the offset
                position = (j + offset, i)

                if loaded_structure is not None:  # Loaded game
                    position = loaded_structure[i][j]['position']
                    room = Room(self.game, position, next=loaded_structure[i][j]['next'],
                                visited=loaded_structure[i][j]['visited'], completed=loaded_structure[i][j]['completed'])
                else:
                    room = Room(self.game, position)

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

        logger.debug(f"Rooms Generated in {time.perf_counter() - start_time:0.4f} seconds")
        return rooms

    def generate_boss_room(self, loaded_boss_position=None):
        logger.debug("Creating a boss room")
        if loaded_boss_position is None:
            # Randomly select a floor between 2-5 floors below
            boss_floor = min(len(self.rooms) - 1, self.player_room.position[1] + random.randint(2, 5))
            # Select a random room on the selected floor to be replaced with a boss room
            boss_room_index = random.randint(0, len(self.rooms[boss_floor]) - 1)
            replaced_room = self.rooms[boss_floor][boss_room_index]
        else:
            boss_floor = loaded_boss_position[1]
            replaced_room = next((room for room in self.rooms[boss_floor] if room.position[0] == loaded_boss_position[0]))
            boss_room_index = self.rooms[boss_floor].index(replaced_room)

        # Room with boss configuration
        boss_enemy = Boss("Boss")
        boss_room = Room(self.game, position=replaced_room.position, enemies=[boss_enemy], is_boss_room=True)
        boss_room.parents = replaced_room.parents
        boss_room.children = replaced_room.children

        if replaced_room.next:
            boss_room.next = True
        if replaced_room.visited:
            boss_room.visited = True

        # Iterate over all parents of the replaced room
        for parent in replaced_room.parents:
            # Find the index of the replaced room in the children list of the current parent
            index = parent.children.index(replaced_room)
            # Replace the replaced room with the boss room in the children list of the current parent
            parent.children[index] = boss_room

        self.rooms[boss_floor][boss_room_index] = boss_room

        # Save boss room position
        self.boss_room_position = boss_room.position

        self.boss_appeared_popup("A boss room has appeared!")

    # Based on the position of the room, between 1 and 3 enemies will be created whereas you progress
    # Through the dungeon, there is a higher chance of more enemies being in the room

    def create_enemies(self, room_position_y):
        logger.debug("Creating enemies")
        # Calculate the room's relative position in the dungeon
        relative_position_y = room_position_y / DIFFICULTY_SCALING_CONSTANT

        # Use linear scaling for the relative position in Y
        relative_position_weighted = min(relative_position_y, 1)  # Clamp to a maximum of 1

        # Add some randomness to the calculation. This will add a random value between -0.2 and 0.2 to the result
        # This randomness scales with the difficulty
        difficulty_multiplier = DIFFICULTY_INT_MAPPING[self.game.difficulty]
        randomness = numpy.random.uniform(-0.2 / difficulty_multiplier, 0.2 * difficulty_multiplier)

        # Scale the relative position to the range of 1-3 and add randomness
        scaled_enemy_number = 1 + 2 * relative_position_weighted + randomness

        # Make sure the result stays within the range of 1-3
        scaled_enemy_number_within_bounds = max(min(scaled_enemy_number, 3), 1)

        number_of_enemies = round(scaled_enemy_number_within_bounds)
        enemy_names = self.choose_enemy_names_from_difficulty(scaled_enemy_number_within_bounds, number_of_enemies)

        # Add the calculated difficulty to the dictionary
        if DEBUG:
            if room_position_y in self.generated_difficulties:
                self.generated_difficulties[room_position_y].append(scaled_enemy_number_within_bounds)
            else:
                self.generated_difficulties[room_position_y] = [scaled_enemy_number_within_bounds]

        enemies = []
        for name in enemy_names:
            enemies.append(Enemy(name))

        if DEBUG:
            self.plot_difficulties()

        return enemies

    # Used to plot a graph of the dungeon difficulty. Excellent for debugging
    def plot_difficulties(self):
        logger.debug("Plotting Difficulty Graph")
        # Calculate the average difficulty for each floor
        average_difficulties = {floor: sum(difficulties) / len(difficulties) for floor, difficulties in
                                self.generated_difficulties.items()}

        # Sort the floors so they are plotted in order
        sorted_floors = sorted(average_difficulties.keys())
        sorted_difficulties = [average_difficulties[floor] for floor in sorted_floors]

        plt.figure(figsize=(10, 6))
        plt.plot(sorted_floors, sorted_difficulties)

        # Add horizontal lines at 1.5 and 2.5 (For the enemy number thresholds)
        plt.axhline(y=2.5, color='red', linestyle='--', label='Threshold for 3 Enemies')
        plt.axhline(y=1.5, color='orange', linestyle='--', label='Threshold for 2 Enemies')
        # Add a vertical line at DIFFICULTY_SCALING_CONSTANT
        plt.axvline(x=DIFFICULTY_SCALING_CONSTANT, color='pink', linestyle='--', label='Difficulty Scaling Constant')

        plt.scatter(sorted_floors[:DIFFICULTY_SCALING_CONSTANT], sorted_difficulties[:DIFFICULTY_SCALING_CONSTANT], marker='x', color='blue', label="First {} Rooms Marked".format(DIFFICULTY_SCALING_CONSTANT))

        plt.xlabel('Floor')
        plt.ylabel('Average Generated Difficulty')
        plt.title('Average Generated Difficulty for Each Floor')
        plt.grid(True)
        plt.legend()
        plt.savefig('average_floor_difficulty_graph.png')

    def choose_enemy_names_from_difficulty(self, difficulty_threshold, number_of_enemies):
        logger.debug(f"Choosing enemies for the rooms difficulty: {str(difficulty_threshold)}")
        json_file = (relative_resource_path('app/assets/data/enemies.json'))
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Get a list of names where the difficulty is less than or equal to the threshold
        eligible_names = [enemy['name'] for enemy in data if enemy['difficulty'] <= difficulty_threshold]
        return random.choices(eligible_names, k=number_of_enemies)

    def move_to_room(self, room):
        logger.debug(f"Moving to a room on floor {str(room.position[1])}")
        # The player is now in the new room
        self.player_room = room

        for parent in room.parents:
            for sibling in parent.children:
                if sibling != room and sibling.next:
                    sibling.next = False
        room.visited = True

        # Generate the enemies in the room
        room_depth = next(index for index, room_list in enumerate(self.rooms) if room in room_list)
        if not room.is_boss_room:
            room.enemies = self.create_enemies(room_depth)
        # Boss rooms have an enemy when created, no need to create enemies for it

        self.game.save_game()

        if not room.enemies_defeated():
            self.game.combat = Combat(self.game, self.game.character, room.enemies)
            self.game.change_state(self.game.combat)

    def update_rooms_recursive(self, room):
        room.next = (room.position == self.player_room)
        for child_room in room.children:
            self.update_rooms_recursive(child_room)

    def progress_to_next_room(self):
        logger.debug("Player completed a room. Performing actions to ready their progression.")
        # This method is called when a player has completed the room, so add the score here
        self.update_player_score()

        self.player_room.completed = True
        self.player_room.next = False
        self.player_room.visited = False

        # Delete all the enemies to prevent increased memory usage
        self.player_room.enemies = None

        # First, for the room you just cleared, set its siblings' children next to false, blocking the tree
        for parent in self.player_room.parents:
            for sibling in parent.children:
                sibling.next = False

        # Then, set the player's current room children next to true, opening the tree
        for child in self.player_room.children:
            child.next = True

        # After progressing the player's character. Check if they meet the boss requirements.
        # If they do, check there is not an upcoming boss room which they could access.
        if self.game.character.boss_requirements_met() and \
                (self.boss_room_position is None or self.player_room.position[1] > self.boss_room_position[1]):
            self.generate_boss_room()

        self.game.save_game()

        # Scroll the camera up to the next room
        self.scroll_offset[1] += self.player_room.rect.height + (100 * self.zoom_level)

    def update_player_score(self):
        logger.debug("Updating the player's score")
        room_score = self.player_room.calculate_score()
        self.game.player_score += room_score

    def handle_event(self, event):
        # Handle dragging the map around
        if event.type == pygame.MOUSEMOTION:
            # If currently dragging, adjust the scroll offset based on the mouse motion
            if self.dragging:
                dx, dy = event.rel  # The relative motion of the mouse since the last event
                if self.player_room.rect.y <= SCREEN_HEIGHT and dy >= 0 or self.player_room.rect.y >= 0 and dy <= 0:
                    self.scroll_offset[1] += dy

        # Handle zooming in and out of the map
        if event.type == pygame.MOUSEWHEEL:
            # Handle zooming in and out of the map if wheel is used while holding CTRL
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Adjust the zoom level based on the mouse wheel motion
                self.zoom_level *= 1.1 ** event.y
                # Limit to 70% - 130% Zoom Levels
                self.zoom_level = min(max(self.zoom_level, 0.7), 1.3)
            else:
                # Adjust the scroll offset based on the mouse wheel motion
                if self.player_room.rect.y <= SCREEN_HEIGHT and event.y >= 0 or self.player_room.rect.y >= 0 and event.y <= 0:
                    self.scroll_offset[1] += event.y * 30

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
        current_layer_index = self.player_room.position[1]
        # Due to an oversight in the player positioning, the first 2 rows will have the player at the root position
        # Or if you have exited and loaded mid-room the player will have updated, so you need to check the current layer
        if (self.player_room == self.root and self.root.next) or (self.player_room.visited and self.player_room.next):
            next_layer_index = current_layer_index
        else:
            next_layer_index = current_layer_index + 1

        # Check if there's a layer below the player's current position
        if next_layer_index < len(self.rooms):
            # Iterate over the rooms in the next layer
            for room in self.rooms[next_layer_index]:
                # Check if the room is a "next" room and collides with the click position
                if (room.next or room.visited) and room.rect.collidepoint(self.game.screen_to_surface(event.pos)):
                    # Move to the room and return True
                    self.move_to_room(room)
                    return True

        return False

    def get_data(self):
        return {
            "player_position": self.player_room.position,
            "boss_room_position": self.boss_room_position,
            "structure": [[room.get_data() for room in row] for row in self.rooms]
        }


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
