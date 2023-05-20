# app/logic/battle_manager.py
from app.constants import FLOOR_COMPLETE, GAME_OVER, CONTINUE


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
                print(f"Applying {card.power} damage to {enemy.name}")
                # apply damage to enemy
                enemy.cur_health -= card.power - enemy.defense - enemy.shield
                return
        # if no enemy was found, apply damage to player
        self.player.cur_health -= card.power - self.player.defense - self.player.shield

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
        self.current_turn.deck.discard_card(card)

    # win condition check
    def check_floor_cleared(self):
        # List current enemies and their health/max health
        for enemy in self.enemies:
            print(f"{enemy.name}: {enemy.cur_health}/{enemy.max_health}")
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
    
    # handle logic of a turn
    def handle_turn(self, card):
        # Play card
        self.play_card(card)
        # Redraw another card
        self.current_turn.deck.draw_card(1)
        # Check if floor is cleared
        if self.check_floor_cleared():
            return FLOOR_COMPLETE
        # Check if player is dead
        if self.check_player_dead():
            return GAME_OVER
        # If player is alive and floor is not cleared, continue
        return CONTINUE