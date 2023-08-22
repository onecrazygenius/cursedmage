# app/logic/battle_manager.py
import time
from collections import deque
from app.constants import *
from app.logic.combat.enemy_logic import EnemyLogic


class BattleManager:

    def __init__(self, player, enemies):
        self.participants = deque([player] + enemies)
        self.current_turn = self.participants[0]
        self.player = player
        self.enemies = enemies

    # apply damage to a character
    def apply_damage(self, card):
        # check who the card is targeting
        for enemy in self.enemies:
            if card.target == enemy:
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
        # check if playing heal
        if card.is_heal():
            # check who the card is targeting
            if not self.apply_heal(card):
                return False
        else:
            # Apply damage to enemy
            self.apply_damage(card)

        # apply cost to player
        self.apply_cost(card)

        # Discard card from who currently playing
        self.current_turn.deck.discard_card(card)
        return True
    
    # Handle heal cards
    def apply_heal(self, card):
        # check if the card is targeting the player
        if card.target == self.player:
            #if self.player.cur_health == self.player.max_health:
                #return False
            # apply heal to self.player, can't go over max health
            if self.player.cur_health + card.power < self.player.max_health:
                self.player.cur_health += card.power
            else:
                self.player.cur_health = self.player.max_health
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
    def simulate_enemy_turn(self, enemy):

        card = EnemyLogic.select_card(enemy, self.player)

        #print("Enemy " + enemy.name + " played " + (card.name if card is not None else "nothing"))
        # If enemy can't play a card, they should end their turn
        if card is not None:
            turn_result = self.handle_turn(card)
        else:
            turn_result = END_TURN

        return turn_result

    def next_turn(self):
        if self.current_turn in self.enemies:
            current_index = self.enemies.index(self.current_turn)
        else:
            current_index = -1

        if current_index == -1 and current_index < len(self.enemies) - 1:
            self.current_turn = self.enemies[current_index + 1]  # Move to the next enemy's turn
            # replenish enemy
            self.current_turn.cost = self.current_turn.max_cost
            self.current_turn.deck.draw_card(3 - len(self.current_turn.deck.hand))
            pygame.event.post(pygame.event.Event(ENEMY_TURN_EVENT))
        else:
            self.current_turn = self.player  # Change to the player's turn
            pygame.event.post(pygame.event.Event(PLAYER_TURN_EVENT))

    
    # handle end of turn
    def end_turn(self):
        # Set the current turn character to full cost and draw back to 3 cards
        # self.current_turn.cost = self.current_turn.max_cost
        # self.current_turn.deck.draw_card(3 - len(self.current_turn.deck.hand))

        # If player is dead, game is over
        if self.player.is_dead():
            pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))
            return

        # Otherwise continue the game by rotating to the next character
        pygame.event.post(pygame.event.Event(PAUSE))
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

    