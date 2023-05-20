from app.states.card_pickup import CardPickupScreen
from app.logic.battle_manager import BattleManager
from app.states.components.button import Button
from app.states.components.popup import Popup
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
        self.end_turn_button = Button("End Turn", self.game.config.get_width() // 2, 300, self.end_turn)

    def update_health_bars(self):
        player_health_ratio = self.battle_manager.player.cur_health / self.battle_manager.player.max_health
        player_bar_width = int(player_health_ratio * 100)

        self.surface.fill(BLACK)
        pygame.draw.rect(self.surface, GREEN, (50, 50, player_bar_width, 100))
        
        # draw the enemies health bars
        for i, enemy in enumerate(self.battle_manager.enemies):
            enemy_health_ratio = enemy.cur_health / enemy.max_health
            enemy_bar_width = int(enemy_health_ratio * 100)
            pygame.draw.rect(self.surface, RED, (self.game.config.get_width() - 50 - enemy_bar_width, 50 + (150*i), enemy_bar_width, 100))

    def handle_event(self, event):
        if event.type == ENEMY_TURN_EVENT:
            turn_result = self.battle_manager.simulate_enemy_turn()
            self.post_turn_actions(turn_result)

        # check if the player turn
        if self.battle_manager.current_turn == self.battle_manager.player:
            # check if the player clicked the mouse button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Was the end turn button clicked?
                if self.end_turn_button.rect.collidepoint(event.pos):
                    self.battle_manager.end_turn()
                    return

                for i, card in enumerate(self.battle_manager.player.deck.hand):
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
                self.battle_manager.player.deck.hand[self.dragging_card].position = (card_x, card_y)

            # check if the player released the mouse button
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # check if the player was dragging a card
                if self.dragging_card is not None:
                    # get the card that was being dragged
                    card = self.battle_manager.player.deck.hand[self.dragging_card]
                    card_x, card_y = card.position

                    turn_result = None
                    # check if the card was dropped on an enemy
                    for i, enemy in enumerate(self.battle_manager.enemies):
                        if enemy.is_dead():
                            continue
                        enemy_sprite_pos = pygame.Rect((self.game.config.get_width() / 2 + (i * 300)), (self.game.config.get_height() / 2), 250, 250)
                        if enemy_sprite_pos.collidepoint(self.game.screen_to_canvas(event.pos)):
                            card.target = enemy
                            turn_result = self.battle_manager.handle_turn(card)
                            self.post_turn_actions(turn_result)

                    # check if the card was dropped on a player
                    player_sprite_pos = pygame.Rect((self.game.config.get_width() / 4), (self.game.config.get_height() / 2), 250, 250)
                    if player_sprite_pos.collidepoint(self.game.screen_to_canvas(event.pos)):
                        card.target = self.battle_manager.player
                        turn_result = self.battle_manager.handle_turn(card)
                        self.post_turn_actions(turn_result)

                    # If the card wasn't on a character put it back into the hand
                    # If turn result isn't defined then the card wasn't dropped on a target
                    if turn_result is None:
                        card.position = (100 + (100 + 100) * self.dragging_card, 100)
                        self.dragging_card = None

    def post_turn_actions(self, turn_result):
        # Check Turn Result and perform the appropriate actions
        if turn_result == END_TURN:
            self.battle_manager.end_turn()
        if turn_result == FAILED:
            # Not enough cost
            self.popup("Not enough cost")
        if turn_result == GAME_OVER:
            self.game.quit_game()
            # TODO: Game over screen
        if turn_result == FLOOR_COMPLETE:
            self.game.change_state(CardPickupScreen(self.game, self.battle_manager.player, self.battle_manager.enemies))
        if turn_result == CONTINUE:
            self.update_health_bars()
        self.dragging_card = None
        pygame.display.flip()

    def draw(self, surface):
        # draw health bars
        self.update_health_bars()
        # Visually draw an enemy and player respectively
        # Multiple enmies will be offset from each other
        for i, enemy in enumerate(self.battle_manager.enemies):
            if enemy.is_dead():
                continue
            pygame.draw.rect(surface, RED, pygame.Rect((self.game.config.get_width() / 2 + (i * 300)), (self.game.config.get_height() / 2), 250, 250))

        
        pygame.draw.rect(surface, GREEN, pygame.Rect((self.game.config.get_width() / 4), (self.game.config.get_height() / 2), 250, 250))

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
            card = self.battle_manager.player.deck.hand[self.dragging_card]
            card_x, card_y = card.position
            card.draw(surface, (card_x, card_y))

        # Show the player's cost
        font = pygame.font.Font(None, 24)
        text_surface = font.render("Cost: " + str(self.battle_manager.player.cost), True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.game.config.get_width() // 2, 50)
        surface.blit(text_surface, text_rect)

        # add an end turn button
        self.end_turn_button.draw(surface)

        # update the display
        pygame.display.flip()

    def end_turn(self):
        # end the player's turn
        self.battle_manager.end_turn()

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