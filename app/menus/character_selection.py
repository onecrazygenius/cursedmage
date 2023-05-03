import pygame
from pygame.locals import *
from app.engine.components.button import Button
from app.engine.constants import *
from app.characters.character import Character
from app.menus.dungeon import Dungeon

class CharacterSelection:
    def __init__(self, game):
        self.game = game
        self.characters = [
            Character("Warrior", 150, 15, 5),
            Character("Mage", 100, 25, 3),
            Character("Rogue", 120, 10, 7)
        ]
        self.difficulties = ["Easy", "Normal", "Hard"]
        self.selected_character = 0
        self.selected_difficulty = 0
        self.start_game_button = Button("Start Game", self.game.config.get_width() // 2, 300, self.start_game)
        self.character_left_arrow = Button("<", self.game.config.get_width() // 3, 150, self.select_previous_character)
        self.character_right_arrow = Button(">", 2 * self.game.config.get_width() // 3, 150, self.select_next_character)
        self.difficulty_left_arrow = Button("<", self.game.config.get_width() // 3, 200, self.select_previous_difficulty)
        self.difficulty_right_arrow = Button(">", 2 * self.game.config.get_width() // 3, 200, self.select_next_difficulty)

    def draw(self):
        self.game.screen.fill(WHITE)

        character_font = pygame.font.Font(None, 36)
        character_text = self.characters[self.selected_character].name
        character_surface = character_font.render(character_text, True, BLACK)
        character_rect = character_surface.get_rect()
        character_rect.center = (self.game.config.get_width() // 2, 150)
        self.game.screen.blit(character_surface, character_rect)

        difficulty_font = pygame.font.Font(None, 36)
        difficulty_text = self.difficulties[self.selected_difficulty]
        difficulty_surface = difficulty_font.render(difficulty_text, True, BLACK)
        difficulty_rect = difficulty_surface.get_rect()
        difficulty_rect.center = (self.game.config.get_width() // 2, 200)
        self.game.screen.blit(difficulty_surface, difficulty_rect)

        self.start_game_button.draw(self.game.screen)
        self.character_left_arrow.draw(self.game.screen)
        self.character_right_arrow.draw(self.game.screen)
        self.difficulty_left_arrow.draw(self.game.screen)
        self.difficulty_right_arrow.draw(self.game.screen)

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