class Card:
    def __init__(self, name, damage, shield, target):
        self.name = name
        self.damage = damage
        self.shield = shield
        self.target = target

    def play(self, combat):
        if self.target == "enemy":
            combat.apply_damage(self.damage, "enemy")
        elif self.target == "player":
            combat.apply_damage(self.damage, "player")
        combat.apply_shield(self.shield)