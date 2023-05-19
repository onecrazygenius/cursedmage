# app/logic/battle_manager.py
import pygame
from app.constants import *

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
                enemy.cur_health -= card.damage - enemy.defense - enemy.shield
                # check if enemy is dead
                if enemy.is_dead():
                    # remove enemy from list
                    self.enemies.remove(enemy)
                return
        # if no enemy was found, apply damage to player
        self.player.cur_health -= card.damage - self.player.defense - self.player.shield

    # Cost handler
    def apply_cost(self, card):
        self.player.cost -= card.cost

    # handle a card being played
    def play_card(self, card):
        # Apply damage to enemy
        self.apply_damage(card)
        # Apply cost to player
        self.apply_cost(card)
        # Discard card from who currently playing
        self.current_turn.deck.discard(card)

    # win condition check
    def check_floor_cleared(self):
        # Check if all enemies are dead
        for enemy in self.enemies:
            if not enemy.is_dead():
                return False
        return True
 
    # check if the player is dead
    def check_player_dead(self):
        # Check if player is dead
        return self.player.is_dead()
    
    # handle logic of a turn
    def handle_turn(self, card):
        # Play card
        self.play_card(card)
        # Check if floor is cleared
        if self.check_floor_cleared():
            return "floor_cleared"
        # Check if player is dead
        if self.check_player_dead():
            return "game_over"
        # If player is alive and floor is not cleared, continue
        return "continue"