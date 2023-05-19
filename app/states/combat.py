from app.states.card_pickup import CardPickupScreen
from app.states.victory_screen import VictoryScreen
from app.logic.battle_manager import BattleManager
from app.states.components.popup import Popup
from app.states.main_menu import MainMenu
from app.states.state import State
from pygame.locals import *
from app.constants import *
import pygame

# Timers
ENEMY_TURN_EVENT = pygame.USEREVENT + 1

class Combat(State):
    def __init__(self, game, player, enemies):
        super().__init__(game)

        self.game = game
        self.battle_manager = BattleManager(player, enemies)
        self.dragging_card = None
        self.dragging_card_offset = (0, 0)

    def update_health_bars(self):
        player_health_ratio = self.battle_manager.player.cur_health / self.battle_manager.player.max_health
        # for each enemy, draw the enemy's health bar
        for i, enemy in enumerate(self.battle_manager.enemies):
            enemy_health_ratio = enemy.cur_health / enemy.max_health
            enemy_bar_width = int(enemy_health_ratio * 100)
            pygame.draw.rect(self.surface, RED, (self.game.config.get_width() - 50 - enemy_bar_width, 50, enemy_bar_width, 100))
        player_bar_width = int(player_health_ratio * 100)
        enemy_bar_width = int(enemy_health_ratio * 100)

        self.surface.fill(BLACK)
        pygame.draw.rect(self.surface, GREEN, (50, 50, player_bar_width, 100))
        
        # draw the enemies health bars
        for i, enemy in enumerate(self.battle_manager.enemies):
            enemy_health_ratio = enemy.cur_health / enemy.max_health
            enemy_bar_width = int(enemy_health_ratio * 100)
            pygame.draw.rect(self.surface, RED, (self.game.config.get_width() - 50 - enemy_bar_width, 50, enemy_bar_width, 100))

    def handle_event(self, event):
        # check if the player turn
        if self.battle_manager.current_turn == self.battle_manager.player:
            card_played = False
            # check if the player clicked the mouse button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, card in enumerate(self.player_hand):
                    if card.cursed:
                        continue
                    card_x = 100 + (100 + 100) * i
                    card_y = 100
                    card_rect = pygame.Rect(card_x, card_y, 100, 100)
                    if card_rect.collidepoint(event.pos):
                        self.dragging_card = i
                        self.dragging_card_offset = (event.pos[0] - card_x, event.pos[1] - card_y)

            # check if the player is dragging a card
            elif event.type == pygame.MOUSEMOTION and self.dragging_card is not None:
                card_x = event.pos[0] - self.dragging_card_offset[0]
                card_y = event.pos[1] - self.dragging_card_offset[1]
                self.player_hand[self.dragging_card].position = (card_x, card_y)

            # check if the player released the mouse button
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # check if the player was dragging a card
                if self.dragging_card is not None:
                    # get the card that was being dragged
                    card = self.player_hand[self.dragging_card]
                    card_x, card_y = card.position

                    # create two rectangles to represent the left and right areas of the screen
                    left_area = pygame.Rect(0, 0, self.game.config.get_width() // 2, self.game.config.get_height())
                    right_area = pygame.Rect(self.game.config.get_width() // 2, 0, self.game.config.get_width() // 2, self.game.config.get_height())

                    # check if the card was dropped in the left or right area
                    try: 
                        if left_area.collidepoint(event.pos):
                            if not self.play_card(self.dragging_card, "player"):
                                # raise an exception if the card couldn't be played
                                raise Exception("Invalid target!")
                        elif right_area.collidepoint(event.pos):
                            if not self.play_card(self.dragging_card, "enemy"):
                                # raise an exception if the card couldn't be played
                                raise Exception("Invalid target!")
                        else:
                            # raise an exception if the card couldn't be played
                            raise Exception("Invalid target!")
                            
                        # if the card was played, it's no longer in the player's hand
                        card_played = True
                        self.player_turn = False
                    except:
                        self.popup("Invalid target!")
                        card.position = (100 + (100 + 100) * self.dragging_card, 100)
                
                # if the card was played, it's no longer in the player's hand
                if card_played:
                    
                    # Remove the played card from the player's hand
                    # self.player_hand.pop(self.dragging_card)

                    # Update the enemy health bar and check win condition
                    self.update_health_bars()
                    self.check_win_condition()

                    # If the enemy is still alive, wait a second before the enemy's turn
                    if self.enemy_health > 0:
                        self.popup("Enemy's turn!")
                        pygame.time.set_timer(ENEMY_TURN_EVENT, 1000)


                pygame.display.flip()
                self.dragging_card = None

            # Check if enemy's turn event has been triggered
        elif event.type == ENEMY_TURN_EVENT:
            print("Enemy's turn!")
            pygame.time.set_timer(ENEMY_TURN_EVENT, 0)  # Stop the timer
            self.enemy_turn()
            self.player_turn = True
            #self.check_win_condition()
            self.update_health_bars()
            self.popup("Your turn!")

    def draw(self, surface):
        # draw health bars
        self.update_health_bars()

        # for each card in the player's hand, draw the card
        for i, card in enumerate(self.battle_manager.player.deck.hand):
            # if the card is being dragged, don't draw it here
            if i == self.dragging_card:
                continue
            # offset the x position of the card based on the index
            card_x = 100 + (100 + 100) * i
            card_y = 100
            # draw the card
            card.draw(surface, (card_x, card_y))

        # if the player is dragging a card, draw it last so it's on top
        if self.dragging_card is not None:
            card = self.player_hand[self.dragging_card]
            card_x, card_y = card.position
            card.draw(surface, (card_x, card_y))

        # update the display
        pygame.display.flip()

    def popup(self, text):
        popup = Popup(
            self.game.config.get_width() // 2, 
            self.game.config.get_height() // 2, 
            text,
            width=300,
            height=100
        )
        popup.draw(self.surface)
        pygame.display.flip()
        pygame.time.wait(500)
        pygame.display.flip()