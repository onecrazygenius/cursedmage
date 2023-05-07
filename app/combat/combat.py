import pygame, random
from pygame.locals import *
from app.engine.components.button import Button
from app.engine.components.popup import Popup
from app.engine.constants import *
from app.combat.card import Card
from app.combat.cursed_card import CursedCard
from app.menus.card_pickup import CardPickupScreen
from app.menus.victory_screen import VictoryScreen
from app.menus.main_menu import MainMenu

ENEMY_TURN_EVENT = pygame.USEREVENT + 1

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
        self.dragging_card = None
        self.dragging_card_offset = (0, 0)

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
            #display the victory and card pickup screen
            self.game.change_state(CardPickupScreen(self.game, self.player))
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
        elif self.player_health <= 0:
            # return to main menu
            self.popup("You died!")
            self.game.change_state(MainMenu(self.game))

    def play_card(self, card_index, target):
        if card_index >= len(self.player_hand):
            return False
        
        card = self.player_hand[card_index]

        if card.target != target:
            return False
    
        card.play(self)
        return True

    def update_health_bars(self):
        player_health_ratio = self.player_health / self.player.max_health
        enemy_health_ratio = self.enemy_health / self.enemy.max_health
        player_bar_width = int(player_health_ratio * HEALTH_BAR_WIDTH)
        enemy_bar_width = int(enemy_health_ratio * HEALTH_BAR_WIDTH)

        self.game.screen.fill((0, 0, 0))
        pygame.draw.rect(self.game.screen, PLAYER_HEALTH_COLOR, (50, 50, player_bar_width, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(self.game.screen, ENEMY_HEALTH_COLOR, (self.game.config.get_width() - 50 - enemy_bar_width, 50, enemy_bar_width, HEALTH_BAR_HEIGHT))

    def handle_event(self, event):
        # check if the player turn
        if self.player_turn:
            card_played = False
            # check if the player clicked the mouse button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, card in enumerate(self.player_hand):
                    if isinstance(card, CursedCard):
                        continue
                    card_x = CARD_START_X + (CARD_WIDTH + CARD_GAP) * i
                    card_y = CARD_START_Y
                    card_rect = pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
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
                            
                        # if the card was played, it's no longer in the player's hand
                        card_played = True
                        self.player_turn = False
                    except:
                        self.popup("Invalid target!")
                        card.position = (CARD_START_X + (CARD_WIDTH + CARD_GAP) * self.dragging_card, CARD_START_Y)
                
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
            self.check_win_condition()
            self.update_health_bars()
            self.popup("Your turn!")

    def enemy_turn(self):
        # Simulate enemy's turn
        damage = random.randint(5, 10)
        self.apply_damage(damage, "player")

    def draw(self):
        # draw health bars
        self.update_health_bars()

        # for each card in the player's hand, draw the card
        for i, card in enumerate(self.player_hand):
            # if the card is being dragged, don't draw it here
            if i == self.dragging_card:
                continue
            # offset the x position of the card based on the index
            card_x = CARD_START_X + (CARD_WIDTH + CARD_GAP) * i
            card_y = CARD_START_Y
            # draw the card
            card.draw(self.game.screen, (card_x, card_y))

        # if the player is dragging a card, draw it last so it's on top
        if self.dragging_card is not None:
            card = self.player_hand[self.dragging_card]
            card_x, card_y = card.position
            card.draw(self.game.screen, (card_x, card_y))

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
        popup.draw(self.game.screen)
        pygame.display.flip()
        pygame.time.wait(500)
        pygame.display.flip()