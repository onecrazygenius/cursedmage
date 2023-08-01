from app.logic.combat.characters.character import Character
from app.states.components.button import Button
from app.states.components.popup import Popup
from app.states.dungeon import Dungeon
from app.states.state import State
from app.constants import *
from pygame.locals import *
import pygame

class CharacterSelection(State):
    DEFAULT_NAME_TEXT = "Enter Name"
    active_popup = None

    def __init__(self, game):
        # Call the parent class (State) constructor
        super().__init__(game)

        self.game = game
        self.characters = [
            Character("Warrior"),
            Character("Mage"),
            Character("Rogue"),
        ]
        self.difficulties = DIFFICULTIES
        self.selected_character = 0
        self.selected_difficulty = 0
        self.start_game_button = Button("Start Game", SCREEN_WIDTH // 2, SCREEN_HEIGHT// 2 + 400, self.start_game)
        self.character_left_arrow = Button("<", SCREEN_WIDTH // 3, SCREEN_HEIGHT// 2, self.select_previous_character)
        self.character_right_arrow = Button(">", 2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT// 2, self.select_next_character)
        self.difficulty_left_arrow = Button("<", SCREEN_WIDTH // 3, SCREEN_HEIGHT// 2 + 100, self.select_previous_difficulty)
        self.difficulty_right_arrow = Button(">", 2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT// 2 + 100, self.select_next_difficulty)

        self.input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 200, 75)
        self.input_box_active = False
        self.input_box_text = self.DEFAULT_NAME_TEXT

    def draw(self, surface):
        # Set background as background image 
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/main_menu.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        character_font = pygame.font.Font(relative_resource_path("app/assets/fonts/pixel_font.ttf"), 36)
        character_text = self.characters[self.selected_character].name
        character_surface = character_font.render(character_text, True, BLACK)
        character_rect = character_surface.get_rect()
        character_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # blitz onto canvas
        surface.blit(character_surface, character_rect)

        difficulty_font = pygame.font.Font(relative_resource_path("app/assets/fonts/pixel_font.ttf"), 36)
        difficulty_text = self.difficulties[self.selected_difficulty]
        difficulty_surface = difficulty_font.render(difficulty_text, True, BLACK)
        difficulty_rect = difficulty_surface.get_rect()
        difficulty_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        surface.blit(difficulty_surface, difficulty_rect)

        self.start_game_button.draw(surface)
        self.character_left_arrow.draw(surface)
        self.character_right_arrow.draw(surface)
        self.difficulty_left_arrow.draw(surface)
        self.difficulty_right_arrow.draw(surface)

        # Draw the Name Text
        name_font = pygame.font.Font(relative_resource_path("app/assets/fonts/pixel_font.ttf"), 36)
        txt_surface = name_font.render(self.input_box_text, True, BLACK)

        # Calculate centered text position
        text_width, text_height = txt_surface.get_size()
        text_x = self.input_box.x + (self.input_box.width - text_width) // 2
        text_y = self.input_box.y + (self.input_box.height - text_height) // 2
        surface.blit(txt_surface, (text_x, text_y))

        # If there are any active popups, show them on the screen
        if self.active_popup is not None:
            # Draw the popup only if the difference between current time and popup start time is less than 2 seconds
            if pygame.time.get_ticks() - self.active_popup.start_time < DUNGEON_POPUP_DURATION_MS:
                self.active_popup.draw(surface)
            else:
                self.active_popup = None

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            self.start_game_button.handle_click(event)
            self.character_left_arrow.handle_click(event)
            self.character_right_arrow.handle_click(event)
            self.difficulty_left_arrow.handle_click(event)
            self.difficulty_right_arrow.handle_click(event)

        # Handle Name Box Actions
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.input_box_active = self.input_box.collidepoint(self.game.screen_to_surface(event.pos))
            if self.input_box_active and self.input_box_text == self.DEFAULT_NAME_TEXT:
                self.input_box_text = ""
                return
        if event.type == pygame.KEYDOWN and self.input_box_active:
            if event.key == pygame.K_RETURN:
                self.game.player_name = self.input_box_text
                self.input_box_text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.input_box_text = self.input_box_text[:-1]
            else:
                self.input_box_text += event.unicode

    def select_previous_character(self):
        self.selected_character = (self.selected_character - 1) % len(self.characters)

    def select_next_character(self):
        self.selected_character = (self.selected_character + 1) % len(self.characters)

    def select_previous_difficulty(self):
        self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)

    def select_next_difficulty(self):
        self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)

    def start_game(self):
        # Don't let the player start the game without entering a name
        if self.input_box_text is self.DEFAULT_NAME_TEXT:
            self.show_popup("Please enter your character name first.")
            return

        self.game.character = self.characters[self.selected_character]
        self.game.player_name = self.input_box_text
        self.game.difficulty = self.difficulties[self.selected_difficulty]
        self.game.dungeon = Dungeon(self.game)
        self.game.save_game()
        self.game.change_state(self.game.dungeon)

    def show_popup(self, text):
        popup = Popup(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            pygame.time.get_ticks(),
            text,
            width=575,
            height=100,
        )
        self.active_popup = popup