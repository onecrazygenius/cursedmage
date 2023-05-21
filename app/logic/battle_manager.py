# app/logic/battle_manager.py

from app.constants import *
from app.logic.combat.enemy_logic import EnemyLogic


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
        # if the current turn character doesn't have enough cost, they can't play the card
        if (self.current_turn.cost - card.cost) < 0:
            return False
        # apply cost to current turn character
        self.current_turn.cost -= card.cost
        # if the current turn character has enough cost, play the card
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
    def simulate_all_enemy_turns(self):
        for i, enemy in enumerate(self.enemies):
            turn_result = CONTINUE
            # TODO: This logic makes it very different to the player. Should probably re-evaluate this later
            while turn_result == CONTINUE:
                # choose a card to play
                card = EnemyLogic.select_card(enemy, self.player)
                print(f"Enemy No. {i} {enemy.name} played {card.name}")
                # play the card
                turn_result = self.handle_turn(card)
            # Draw cards
            enemy.deck.draw_card(3 - len(enemy.deck.hand))
            self.current_turn = self.enemies[i+1] if i+1 < len(self.enemies) else self.current_turn
        return turn_result

    
    # handle end of turn
    def end_turn(self):
        self.current_turn.cost = self.current_turn.max_cost
        if self.current_turn == self.player:
            self.current_turn = self.enemies[0]
            pygame.event.post(pygame.event.Event(ENEMY_TURN_EVENT))
        else:
            self.current_turn = self.player
            self.player.deck.draw_card(3 - len(self.player.deck.hand))

    
    # handle logic of a turn
    def handle_turn(self, card):
        # Check if player is dead
        if self.check_player_dead():
            return GAME_OVER
        # Check if floor is cleared
        if self.check_floor_cleared():
            return FLOOR_COMPLETE
        # Play card
        if not self.play_card(card):
            return FAILED
        # If player is alive and floor is not cleared, continue
        # Check if they have enough cost to play another card
        if self.current_turn.cost < 1 or len([card for card in self.current_turn.deck.hand if card.cost <= self.current_turn.cost]) == 0:
            return END_TURN
        return CONTINUE
    