class Character:
    def __init__(self, name, max_health, attack, defense, shield=0):
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.attack = attack
        self.defense = defense
        self.shield = shield
        self.level = 1

    def is_dead(self):
        return self.current_health <= 0
    