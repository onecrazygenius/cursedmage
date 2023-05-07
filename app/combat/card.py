import pygame, os
from app.engine.constants import *

class Card:
    def __init__(self, name, damage, shield, target, sprite="cards/back"):
        self.name = name
        self.damage = damage
        self.shield = shield
        self.target = target
        self.sprite = sprite
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

        # draw card with sprite
        path = os.path.dirname(os.path.abspath(__file__))
        card_sprite = pygame.image.load(os.path.join(path + '/../assets/sprites/' + self.sprite + '.png'))
        card_sprite = pygame.transform.scale(card_sprite, (CARD_WIDTH, CARD_HEIGHT))
        screen.blit(card_sprite, position)
        
        font = pygame.font.Font(os.path.join(path + '/../assets/fonts/cursed_font.tff'), 20)
        text = font.render(self.name, True, (0, 0, 0))
        screen.blit(text, (position[0] + 10, position[1] + 10))
