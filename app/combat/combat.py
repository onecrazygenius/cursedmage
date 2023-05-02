import pygame, random
from pygame.locals import *
from app.engine.components.button import Button
from app.engine.constants import *
from app.combat.card import Card
from app.combat.cursedCard import CursedCard
from app.menus.victory_screen import VictoryScreen
from app.menus.main_menu import MainMenu

class Combat:
    def __init__(self, game, player, enemy):
        self.game = game
        self.player = player
        self.enemy = enemy
        self.player_health = self.player.max_health
        self.enemy_health = self.enemy.max_health
        self.player_shield = 0
        self.enemy_shield = 0
        self.player_hand = self.player.hand
        self.player_turn = True

    def apply_damage(self, damage, target):
        if target == "enemy":
            remaining_damage = damage - self.enemy_shield
            if remaining_damage > 0:
                self.enemy_shield = 0
                self.enemy_health -= remaining_damage
            else:
                self.enemy_shield -= damage
        elif target == "player":
            remaining_damage = damage - self.player_shield
            if remaining_damage > 0:
                self.player_shield = 0
                self.player_health -= remaining_damage
            else:
                self.player_shield -= damage

    def apply_shield(self, shield):
        self.player_shield += shield

    def check_win_condition(self):
        if self.enemy_health <= 0:
            # update room to be completed
            x, y = self.game.dungeon.player_position
            self.game.dungeon.rooms[x][y].completed = True
            # return to dungeon, update player position and save game
            self.game.dungeon.update_player_position()
            # update next room to be available
            x, y = self.game.dungeon.player_position
            self.game.dungeon.rooms[x][y].next = True
            self.game.save_game()

            # check if the player has completed the dungeon
            if self.game.dungeon.player_position == (DUNGEON_SIZE_X - 1, DUNGEON_SIZE_Y - 1):
                # Victory!
                self.game.push_state(VictoryScreen(self.game))
            self.game.pop_state()
        elif self.player_health <= 0:
            # return to main menu
            print("You died!")
            self.game.change_state(MainMenu(self.game))

    def play_card(self, card_index):
        if card_index < len(self.player_hand):
            card = self.player_hand[card_index]
            card.play(self)

    def update_health_bars(self):
        player_health_ratio = self.player_health / self.player.max_health
        enemy_health_ratio = self.enemy_health / self.enemy.max_health
        player_bar_width = int(player_health_ratio * HEALTH_BAR_WIDTH)
        enemy_bar_width = int(enemy_health_ratio * HEALTH_BAR_WIDTH)

        self.game.screen.fill((0, 0, 0))
        pygame.draw.rect(self.game.screen, PLAYER_HEALTH_COLOR, (50, 50, player_bar_width, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(self.game.screen, ENEMY_HEALTH_COLOR, (SCREEN_WIDTH - 50 - enemy_bar_width, 50, enemy_bar_width, HEALTH_BAR_HEIGHT))

    def handle_event(self, event):
        if self.player_turn and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i, card in enumerate(self.player_hand):
                card_x = CARD_START_X + (CARD_WIDTH + CARD_GAP) * i
                card_y = CARD_START_Y
                card_rect = pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
                if card_rect.collidepoint(event.pos):
                    self.play_card(i)
                    self.player_turn = False
                    # Check if the enemy is dead
                    if self.enemy_health >= 0:
                        pygame.time.wait(1000)  # Delay to simulate enemy's turn
                        self.enemy_turn(card)
                    self.check_win_condition()

    def enemy_turn(self, card):
        # Simulate enemy's turn
        if isinstance(card, CursedCard) == False:
            damage = random.randint(5, 10)
            self.apply_damage(damage, "player")
        self.player_turn = True

    def draw(self):
        self.update_health_bars()

        for i, card in enumerate(self.player_hand):
            card_x = CARD_START_X + (CARD_WIDTH + CARD_GAP) * i
            card_y = CARD_START_Y
            pygame.draw.rect(self.game.screen, (255, 255, 255), pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT))
            font = pygame.font.Font(None, 24)
            text_surface = font.render(card.name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(card_x + CARD_WIDTH // 2, card_y + CARD_HEIGHT // 2))
            self.game.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def popup(self, text):
        popup_width = 300
        popup_height = 100
        popup_x = SCREEN_WIDTH // 2 - popup_width // 2
        popup_y = SCREEN_HEIGHT // 2 - popup_height // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.game.screen, (255, 255, 255), popup_rect)
        font = pygame.font.Font('app\\assets\\fonts\\cursedFont.tff', 24)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height // 2))
        self.game.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.display.flip()
