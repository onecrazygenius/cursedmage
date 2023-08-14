import random
import threading
from collections import deque

from app.constants import *
from app.logging_config import logger
from app.logic.battle_manager import BattleManager
from app.states.card_pickup import CardPickupScreen
from app.states.components.button import Button
from app.states.components.popup import Popup
from app.states.cursed_card_pickup import CursedCardPickupScreen
from app.states.state import State
from app.states.upgrade_card import UpgradeCardScreen


class Combat(State):
    event_queue = deque()
    def __init__(self, game, player, enemies):
        super().__init__(game)
        self.game = game
        self.battle_manager = BattleManager(player, enemies)
        self.dragging_card = None
        self.dragging_card_offset = (0, 0)
        self.end_turn_button = Button("End Turn", 150, SCREEN_HEIGHT // 2, self.end_turn)
        self.active_popup = None
        self.hovered_card = None
        player.replenish(health=True)

        self.game_difficulty = DIFFICULTY_INT_MAPPING[self.game.difficulty]

        # Initialize the animation state
        self.current_frame = 0
        self.frame_time = 0

        self.paused = False
        self.pause_timer = None

    def update_health_bars(self):
        player_health_ratio = self.battle_manager.player.cur_health / self.battle_manager.player.max_health
        player_bar_width = int(player_health_ratio * 200)

        pygame.draw.rect(self.surface, GREEN, (50, 50, player_bar_width, 20))
        # add a border to the health bar
        pygame.draw.rect(self.surface, WHITE, (50, 50, 200, 20), 2)

        # draw the enemies health bars
        for i, enemy in enumerate(self.battle_manager.enemies):
            enemy_health_ratio = enemy.cur_health / enemy.max_health
            enemy_bar_width = int(enemy_health_ratio * 200)
            pygame.draw.rect(self.surface, RED, (SCREEN_WIDTH - 50 - enemy_bar_width, 50 + (40*i), enemy_bar_width, 20))
            # add a border to the health bar
            pygame.draw.rect(self.surface, WHITE, (SCREEN_WIDTH - 50 - 200, 50 + (40*i), 200, 20), 2)

    def unpause(self):
        while self.paused:
            # Check if the pause timer has reached zero
            if self.paused and pygame.time.get_ticks() >= self.pause_timer:
                self.paused = False
                logger.debug("Game Unpaused")
                pygame.event.post(pygame.event.Event(UNPAUSE))

    def handle_event(self, event):
        if event.type == PAUSE:
            self.paused = True
            self.pause_timer = pygame.time.get_ticks() + PAUSE_TIME_MS
            logger.debug("Game Paused")

            thread = threading.Thread(target=self.unpause)
            thread.start()

        if self.paused:
            # Queue allowed events
            for allowed_event in [PLAYER_TURN_EVENT, ENEMY_TURN_EVENT, GAME_OVER_EVENT]:
                if event.type == allowed_event:
                    self.event_queue.append(event)
                    return

        if event.type == UNPAUSE:
            logger.debug("Event Queue has {} events".format(len(self.event_queue)))
            # Process queued events
            while self.event_queue:
                queued_event = self.event_queue.popleft()
                self.handle_event(queued_event)
                return

        if event.type == PLAYER_TURN_EVENT:
            logger.debug("Player Turn Event Received")
            # refresh the player's energy
            self.battle_manager.player.replenish()

        if event.type == GAME_OVER_EVENT:
            logger.debug("Game Over Event Received")
            print("Game Over")
            self.game.quit_game()

        if self.battle_manager.current_turn != self.battle_manager.player and event.type == ENEMY_TURN_EVENT:
            logger.debug("Enemy Turn Event Received")
            turn_result = CONTINUE
            while turn_result == CONTINUE:
                turn_result = self.battle_manager.simulate_enemy_turn(self.battle_manager.current_turn, self.game_difficulty)
                self.post_turn_actions(turn_result)

        # check if the player turn
        if self.battle_manager.current_turn == self.battle_manager.player:
            # check if the player clicked the mouse button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                for i, card in enumerate(self.battle_manager.player.deck.hand):
                    if card.cursed:
                        continue
                    card_x = 100 + (100 + 100) * i
                    card_y = 800
                    card_rect = pygame.Rect(card_x, card_y, 150, 225)
                    if card_rect.collidepoint(self.game.screen_to_surface(event.pos)):
                        self.dragging_card = i
                        self.dragging_card_offset = (event.pos[0] - card_x, event.pos[1] - card_y)

            # check if the player is dragging a card
            elif event.type == pygame.MOUSEMOTION and self.dragging_card is not None:
                dragging_card_pos = (
                    self.game.screen_to_surface(event.pos)[0] - 50,
                    self.game.screen_to_surface(event.pos)[1] - 100
                )
                self.battle_manager.player.deck.hand[self.dragging_card].position = dragging_card_pos

            # check if the player has hovered over a card
            elif event.type == pygame.MOUSEMOTION:
                # Make the card bigger when the mouse is over it
                # set self.hovered_card to the card that is being hovered over
                for i, card in enumerate(self.battle_manager.player.deck.hand):
                    if card.cursed:
                        continue
                    card_x = 100 + (100 + 100) * i
                    card_y = 800
                    card_rect = pygame.Rect(card_x, card_y, 150, 225)
                    if card_rect.collidepoint(self.game.screen_to_surface(event.pos)):
                        self.hovered_card = i
                        break
                # if the card is no longer being hovered over, set self.hovered_card to None
                else:
                    self.hovered_card = None



            # check if the player released the mouse button
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                 # Was the end turn button clicked?
                if self.end_turn_button.rect.collidepoint(self.game.screen_to_surface(event.pos)):
                    self.battle_manager.end_turn()
                    return
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
                        enemy_sprite_pos = pygame.Rect((SCREEN_WIDTH / 2 + (i * 300)), (SCREEN_HEIGHT / 2 - 100), 250, 250)
                        if enemy_sprite_pos.collidepoint(self.game.screen_to_surface(event.pos)):
                            card.target = enemy
                            turn_result = self.battle_manager.handle_turn(card)
                            self.post_turn_actions(turn_result)

                    # check if the card was dropped on a player
                    player_sprite_pos = pygame.Rect((SCREEN_WIDTH / 4), (SCREEN_HEIGHT / 2), 250, 250)
                    if player_sprite_pos.collidepoint(self.game.screen_to_surface(event.pos)):
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

            logger.debug("Applying Card Effects")
            self.battle_manager.apply_effects("end_of_turn")
        if turn_result == FAILED:
            # Not enough cost
            self.popup("Not Enough Mana")
            pygame.display.flip()
        # Check for results which would end the combat phase
        self.post_combat_actions(turn_result)
        if turn_result == CONTINUE:
            self.update_health_bars()
        # To prevent visual issues. After each turn set the hovered card back to none
        self.hovered_card = None
        self.dragging_card = None
        pygame.display.flip()

    def post_combat_actions(self, turn_result):
        if turn_result == GAME_OVER:
            self.game.game_over()
        # Card effects could kill even without a floor complete event so that check is required
        if turn_result == FLOOR_COMPLETE or self.battle_manager.check_floor_cleared():
            # Boss rooms allow you to upgrade a card instead of picking up a card.
            if self.game.dungeon.player_room.is_boss_room:
                self.game.change_state(UpgradeCardScreen(self.game, self.battle_manager.player))
            else:
                self.game.change_state(CardPickupScreen(self.game, self.battle_manager.player, self.battle_manager.enemies))

            # After completing a floor, you have a chance to pickup a cursed card
            if random.randint(1, 100) <= CURSED_CARD_CHANCE:
                # Use push_state instead of change_state because this state is informational
                # and afterwards we want to return to the card pickup screen without coming back
                # to the combat class
                self.game.push_state(CursedCardPickupScreen(self.game, self.battle_manager.player))

    def draw(self, surface):
        # Set background as background image 
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/dungeon.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))
        # draw health bars
        self.update_health_bars()
        self.increment_frametime()

        # Visually draw an enemy and player respectively
        # Multiple enmies will be offset from each other
        for i, enemy in enumerate(self.battle_manager.enemies):
            if enemy.is_dead():
                continue
            # Draw the enemy's frame
            enemy_sprite = enemy.character_frames[self.current_frame]
            surface.blit(enemy_sprite, (SCREEN_WIDTH / 2 + (i * 300), SCREEN_HEIGHT / 2 - 100))

        # Draw the player frame
        player_sprite = self.battle_manager.player.character_frames[self.current_frame]
        surface.blit(player_sprite, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2 - 100))


        # for each card in the player's hand, draw the card
        for i, card in enumerate(self.battle_manager.player.deck.hand):
            # if the card is being dragged, don't draw it here
            if i == self.dragging_card:
                continue
            # center the cards in the middle of the screen
            card_x = 100 + (100 + 100) * i
            card_y = 800
            # draw the card, if the current card is self.hovering_card, draw it slightly bigger
            if i == self.hovered_card:
                card.draw(surface, (card_x, card_y), 1.2)
            else:
                card.draw(surface, (card_x, card_y))

        # if the player is dragging a card, draw it last so it's on top
        if self.dragging_card is not None:
            card = self.battle_manager.player.deck.hand[self.dragging_card]
            card_x, card_y = card.position
            card.draw(surface, (card_x, card_y))

        # Show the player's cost
        font = pygame.font.Font(relative_resource_path("app/assets/fonts/pixel_font.ttf"), 42)
        text_surface = font.render("Mana: " + str(self.battle_manager.player.cost), True, BLUE)
        text_rect = text_surface.get_rect()
        text_rect.center = (150, SCREEN_HEIGHT // 2 - 50)
        surface.blit(text_surface, text_rect)

        # Show the current turn
        font = pygame.font.Font(relative_resource_path("app/assets/fonts/pixel_font.ttf"), 36)
        text_surface = font.render(str(self.battle_manager.current_turn.name) + "'s Turn", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH / 2, 50)
        surface.blit(text_surface, text_rect)

        # add an end turn button
        self.end_turn_button.draw(surface)

        if self.active_popup is not None:
            # Draw the popup only if the difference between current time and popup start time is less than 2 seconds
            if pygame.time.get_ticks() - self.active_popup.start_time < COMBAT_POPUP_DURATION_MS:
                self.active_popup.draw(surface)
            else:
                self.active_popup = None

        # update the display
        pygame.display.flip()

    # Used to manage the frametime
    def increment_frametime(self):
        animation_speed = 5  # The lower this number the faster the animation plays
        self.frame_time += 1
        if self.frame_time > animation_speed:
            self.current_frame = (self.current_frame + 1) % 8  # Loop back to the start if we've gone through all the frames
            self.frame_time = 0

    def end_turn(self):
        # end the player's turn
        self.battle_manager.end_turn()

    def popup(self, text):
        popup = Popup(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            pygame.time.get_ticks(),
            text,
            width=300,
            height=100,
        )
        self.active_popup = popup