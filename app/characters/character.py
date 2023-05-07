from app.combat.card import Card
from app.combat.cursed_card import CursedCard

class Character:
    def __init__(self, name, max_health, attack, defense, shield=0):
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.attack = attack
        self.defense = defense
        self.shield = shield
        self.level = 1
        self.hand = [
            Card("Attack 1", 5, 0, "enemy"),
            Card("Attack 2", 10, 0, "enemy"),
            Card("Shield", 0, 5, "player"),
            CursedCard(),
        ]

    def is_dead(self):
        return self.current_health <= 0
    
    def add_card(self, card):
        self.hand.append(card)