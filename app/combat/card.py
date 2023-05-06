import pygame

class Card:
    def __init__(self, name, damage, shield, target):
        self.name = name
        self.damage = damage
        self.shield = shield
        self.target = target
        self.position = (0, 0)

    def play(self, combat):
        if self.target == "enemy":
            combat.apply_damage(self.damage, "enemy")
        elif self.target == "player":
            combat.apply_damage(self.damage, "player")
        elif self.target == "self":
            combat.apply_shield(self.shield)

    def draw(self, screen, position=None):
        if position is None:
            position = self.position

        self.position = position
        
        pygame.draw.rect(screen, (255, 255, 255), (position[0], position[1], 100, 150))
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(self.name, True, (0, 0, 0))
        screen.blit(text, (position[0] + 10, position[1] + 10))
