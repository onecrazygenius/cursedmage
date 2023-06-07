from app.logic.combat.characters.character import Character
from app.states.components.button import Button
from app.states.dungeon import Dungeon
from app.states.state import State
from app.constants import *
from pygame.locals import *
import pygame

class CharacterSelection(State):
    def __init__(self, game):
        # Call the parent class (State) constructor
        super().__init__(game)

        self.game = game
        self.characters = [
            Character("Warrior"),
            Character("Mage"),
            Character("Rogue"),
        ]
        self.difficulties = ["Easy", "Normal", "Hard"]
        self.selected_character = 0
        self.selected_difficulty = 0
        self.start_game_button = Button("Start Game", SCREEN_WIDTH // 2, 300, self.start_game)
        self.character_left_arrow = Button("<", SCREEN_WIDTH // 3, 150, self.select_previous_character)
        self.character_right_arrow = Button(">", 2 * SCREEN_WIDTH // 3, 150, self.select_next_character)
        self.difficulty_left_arrow = Button("<", SCREEN_WIDTH // 3, 200, self.select_previous_difficulty)
        self.difficulty_right_arrow = Button(">", 2 * SCREEN_WIDTH // 3, 200, self.select_next_difficulty)

    def draw(self, surface):
        # Set background as background image 
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/main_menu.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        character_font = pygame.font.Font(None, 36)
        character_text = self.characters[self.selected_character].name
        character_surface = character_font.render(character_text, True, BLACK)
        character_rect = character_surface.get_rect()
        character_rect.center = (SCREEN_WIDTH // 2, 150)
        # blitz onto canvas
        surface.blit(character_surface, character_rect)

        difficulty_font = pygame.font.Font(None, 36)
        difficulty_text = self.difficulties[self.selected_difficulty]
        difficulty_surface = difficulty_font.render(difficulty_text, True, BLACK)
        difficulty_rect = difficulty_surface.get_rect()
        difficulty_rect.center = (SCREEN_WIDTH // 2, 200)
        surface.blit(difficulty_surface, difficulty_rect)

        self.start_game_button.draw(surface)
        self.character_left_arrow.draw(surface)
        self.character_right_arrow.draw(surface)
        self.difficulty_left_arrow.draw(surface)
        self.difficulty_right_arrow.draw(surface)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONUP:
            self.start_game_button.handle_click(event)
            self.character_left_arrow.handle_click(event)
            self.character_right_arrow.handle_click(event)
            self.difficulty_left_arrow.handle_click(event)
            self.difficulty_right_arrow.handle_click(event)

    def select_previous_character(self):
        self.selected_character = (self.selected_character - 1) % len(self.characters)

    def select_next_character(self):
        self.selected_character = (self.selected_character + 1) % len(self.characters)

    def select_previous_difficulty(self):
        self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)

    def select_next_difficulty(self):
        self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)

    def start_game(self):
        self.game.character = self.characters[self.selected_character]
        self.game.difficulty = self.difficulties[self.selected_difficulty]
        self.game.dungeon = Dungeon(self.game)
        self.game.save_game()
        self.game.change_state(self.game.dungeon)