# app/logic/battle_manager.py
from app.constants import *
from app.logic.combat.characters.enemy import Enemy
import random

class BattleManager:

    def __init__(self, player, enemies):
        self.current_turn = player
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
        # if the player doesn't have enough cost, they can't play the card
        if (self.player.cost - card.cost) < 0:
            return False
        # apply cost to player
        self.player.cost -= card.cost
        # if the player has enough cost, play the card
        return True

    # handle a card being played
    def play_card(self, card):
        # Apply cost to player
        if not self.apply_cost(card):
            return False
        # Apply damage to enemy
        self.apply_damage(card)
        # Discard card from who currently playing
        self.current_turn.deck.discard_card(card)
        
        return True

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
    def simulate_enemy_turn(self):
        # check current turn is an enemy
        if self.current_turn == self.player:
            return
        # get the enemy
        enemy = self.current_turn
        # choose a card to play
        card = enemy.deck.hand[random.randint(0, len(enemy.deck.hand) - 1)]
        # play the card
        self.handle_turn(card)
        print(f"{enemy.name} played {card.name}")
    
    # handle end of turn
    def end_turn(self):
        print("End of Turn")
        # the player has done their turn,
        # now we pause to let each enemy attack
        # then we give the turn back to the player
        for enemy in self.enemies:
            self.current_turn = enemy
            self.simulate_enemy_turn()
        self.current_turn = self.player
        self.player.cost = self.player.max_cost
        self.player.deck.draw_card(3 - len(self.player.deck.hand))

    
    # handle logic of a turn
    def handle_turn(self, card):
        # Play card
        if not self.play_card(card):
            return FAILED
        # Check if floor is cleared
        if self.check_floor_cleared():
            return FLOOR_COMPLETE
        # Check if player is dead
        if self.check_player_dead():
            return GAME_OVER
        # If player is alive and floor is not cleared, continue
        # Check if they have enough cost to play another card
        if self.current_turn.cost < 1:
            return END_TURN
        return CONTINUE
    