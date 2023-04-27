import random

class Enemy:
    def __init__(self, name, max_health, attack, defense, shield=0):
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.attack = attack
        self.defense = defense
        self.shield = shield

    def is_dead(self):
        return self.current_health <= 0
    
def generate_enemy(level):
    max_health = random.randint(50, 100) * level
    attack = random.randint(5, 15) * level
    defense = random.randint(3, 10) * level
    return Enemy("Goblin", max_health, attack, defense)