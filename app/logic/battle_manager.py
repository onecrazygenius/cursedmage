# app/logic/battle_manager.py
from collections import deque

from app.constants import *
from app.logging_config import logger
from app.logic.combat.effect import Effect
from app.logic.combat.enemy_logic import EnemyLogic


class BattleManager:

    def __init__(self, player, enemies, game):
        self.participants = deque([player] + enemies)
        self.current_turn = self.participants[0]
        self.player = player
        self.enemies = enemies
        self.game = game

    # apply damage to a character
    def apply_damage(self, card):
        # check who the card is targeting
        for enemy in self.enemies:
            if card.target == enemy:
                logger.debug("Applying {} card damage to {}".format(card.name, card.target.name))
                # apply damage to enemy
                enemy.cur_health -= card.power - enemy.defense - enemy.shield
                return
        # if no enemy was found, apply damage to player
        self.player.cur_health -= card.power - self.player.defense - self.player.shield

    # Cost handler
    def apply_cost(self, card):
        # apply cost to current turn character
        self.current_turn.cost -= card.cost
    
    def check_cost(self, card):
        # if the current turn character doesn't have enough cost, they can't play the card
        if (self.current_turn.cost - card.cost) < 0:
            return False
        return True

    # handle a card being played
    def play_card(self, card):
        # Check if the card can be played
        if not self.check_cost(card):
            return False

        self.add_effects(card)

        # check if playing heal
        if card.is_heal():
            # check who the card is targeting
            if not self.apply_heal(card):
                return False
        else:
            # Apply damage to enemy
            self.apply_damage(card)

        # if the turn is the player's, play the card hit sound
        if self.current_turn == self.player:
            card.hit_sound.play()
            card.hit_sound.set_volume(float(self.game.config.get("audio", "sfx_volume")))
            # pygame.mixer.Sound.play(
            #     card.hit_sound
            # )
            # pygame.mixer.Sound.set_volume(self.game.config.get())

        # apply cost to player
        self.apply_cost(card)

        self.apply_effects("on_card_played")

        # Discard card from who currently playing
        self.current_turn.deck.discard_card(card)
        return True

    # Applies an effect to the appropriate target
    def add_effects(self, card):
        # If the card has no effects don't try to add any
        if not card.effects:
            logger.debug(f"Card {card.name} has no effects, therefore no effect was applied")
            return

        # The target will be none if an enemy is trying to play it. In this case set the target to the player
        if card.target is None and self.current_turn in self.enemies:
            logger.debug(f"Card target was none. Presuming it's being played against the player. {self.current_turn.name} played the card.")
            card.target = self.player

        for effect in card.effects:
            if effect.target == "target":
                if not card.target.has_effect(effect.name):
                    logger.debug(f"Target Effect {effect.name} added to {card.target.name}")
                    card.target.active_effects.append(Effect(effect.name))

            if effect.target == "multihit":
                if self.current_turn == self.player:
                    for enemy in self.enemies:
                        if not enemy.has_effect(effect.name):
                            logger.debug(f"Multihit Effect {effect.name} added to enemy team")
                            enemy.active_effects.append(Effect(effect.name))
                else:
                    if not self.player.has_effect(effect.name):
                        logger.debug(f"Multihit Effect {effect.name} added to players team")
                        self.player.active_effects.append(Effect(effect.name))


            if effect.target == "self":
                if not self.current_turn.has_effect(effect.name):
                    logger.debug(f"Self Effect {effect.name} added to {self.current_turn.name}")
                    self.current_turn.active_effects.append(Effect(effect.name))

    # This will apply all effects which apply to the phase parameter
    def apply_effects(self, phase):
        for effect in [e for e in self.player.active_effects if e.phase == phase]:
            self.apply_effect_to_character(effect, self.player)
            effect.reduce_counter(self.player)
            logger.debug(f"Effect {effect.name} happened to the player. It has {effect.turns_remaining} turns remaining")

        # TODO: What about multiple enemies where some are dead
        for enemy in self.enemies:
            for effect in [e for e in enemy.active_effects if e.phase == phase]:
                self.apply_effect_to_character(effect, enemy)
                effect.reduce_counter(enemy)
                logger.debug(f"Effect {effect.name} happened to {enemy.name}. It has {effect.turns_remaining} turns remaining")

    def apply_effect_to_character(self, effect, target):
        if effect.is_heal():
            if target.cur_health + effect.power < target.max_health:
                target.cur_health += effect.power
            else:
                target.cur_health = target.max_health
        else:  # It must be a damage effect
            target.cur_health -= effect.power - target.defense - target.shield

    # Handle heal cards
    def apply_heal(self, card):
        # check if the card is targeting the player
        if card.target == self.player:
            # apply heal to self.player, can't go over max health
            if self.player.cur_health + card.power < self.player.max_health:
                self.player.cur_health += card.power
            else:
                self.player.cur_health = self.player.max_health
            return True
        # The target will be none if an enemy is trying to play it. In this case
        if card.target is None and self.current_turn in self.enemies:
            if self.current_turn.cur_health + card.power < self.current_turn.max_health:
                self.current_turn.cur_health += card.power
            else:
                self.current_turn.cur_health = self.current_turn.max_health
            return True
        return False

    # win condition check
    def check_floor_cleared(self):
        # List current enemies and their health/max health
        # Check if all enemies are dead
        for enemy in self.enemies:
            if not enemy.is_dead():
                return False
        # If all enemies are dead, return True
        return True
 
    # check if the player is dead
    def check_player_dead(self):
        # Check if player is dead
        return self.player.is_dead()
    
    # simulate enemy turn
    def simulate_enemy_turn(self, enemy, game_difficulty):

        card = EnemyLogic.select_card(enemy, self.player.cur_health, game_difficulty)
        logger.debug("Enemy {} chose to play {}".format(enemy.name, card.name if card is not None else "nothing. They could not afford to play a card"))

        # If enemy can't play a card, they should end their turn
        if card is not None:
            turn_result = self.handle_turn(card)
        else:
            turn_result = END_TURN

        logger.debug("Turn result was " + turn_result)
        return turn_result

    def next_turn(self):
        logger.debug("It was {}'s turn".format(self.current_turn.name))
        if self.current_turn == self.player:  # If current turn is player's
            current_index = -1
        else:  # If current turn is an enemy's
            current_index = self.enemies.index(self.current_turn)
            # Replenish the enemy that just played
            self.current_turn.cost = self.current_turn.max_cost
            self.current_turn.deck.draw_card(3 - len(self.current_turn.deck.hand))

        # Move to the next alive enemies turn. If there are none move back to the players turn
        while True:
            current_index += 1
            if current_index >= len(self.enemies):  # If no more enemies left that could play
                self.current_turn = self.player  # Change to the player's turn
                break
            elif not self.enemies[current_index].is_dead():  # If next enemy is not dead
                # Set the current turn to the next enemy
                self.current_turn = self.enemies[current_index]
                break

        logger.debug("It's now {}'s turn".format(self.current_turn.name))

        # Post event
        if self.current_turn == self.player:
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))
            logger.debug("Player Turn Event Sent")
        else:
            pygame.event.post(pygame.event.Event(ENEMY_TURN_EVENT))
            logger.debug("Enemy Turn Event Sent")

    # handle end of turn
    def end_turn(self):
        logger.debug("{} chose to end their turn".format(self.current_turn.name))
        # Set the current turn character to full cost and draw back to 3 cards
        # self.current_turn.cost = self.current_turn.max_cost
        # self.current_turn.deck.draw_card(3 - len(self.current_turn.deck.hand))

        # If player is dead, game is over
        if self.player.is_dead():
            pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))
            return

        # Otherwise continue the game by rotating to the next character
        pygame.event.post(pygame.event.Event(PAUSE))
        logger.debug("Pause Event Sent")
        self.next_turn()

    
    # handle logic of a turn
    def handle_turn(self, card):
        # Play card
        if not self.play_card(card):
            return FAILED
        
        # Check if player is dead
        if self.check_player_dead():
            return GAME_OVER
        # Check if floor is cleared
        if self.check_floor_cleared():
            return FLOOR_COMPLETE
        
        # If player is alive and floor is not cleared, continue
        # Check if they have enough cost to play another card
        if self.current_turn.cost < 1 or len([card for card in self.current_turn.deck.hand if card.cost <= self.current_turn.cost]) == 0:
            return END_TURN
        return CONTINUE

    