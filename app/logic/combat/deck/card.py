import pygame, os
from app.constants import *

class Card:

    '''
    Card class for the game
    '''
    def __init__(self, 
                 name, 
                 card_type, 
                 power=1,
                 cost=1, 
                 target=None, 
                 cursed=False,
                 position=(0,0),
                 image="back"    
            ):
        self.name = name
        self.card_type = card_type
        self.power = power
        self.cost = cost
        self.target = target
        self.cursed = cursed
        self.position = position

        if not image:
            image = "back"
        self.image = "app/assets/images/cards/" + image + ".png"

    def draw(self, screen, position=None):
        # Position set to default if not specified
        if position is None:
            position = self.position
        self.position = position
        
        # Draw the card on the screen using the image
        image = pygame.image.load(self.image)
        # Scale the image to fit the card
        image = pygame.transform.scale(image, (150, 225))
        screen.blit(image, position)
        
        # Load the font
        font = pygame.font.Font(resource_path('app/assets/fonts/cursed_font.tff'), 24)
        # Render text
        text = font.render(self.name, True, (0, 0, 0))

        # Blit the text to the screen
        screen.blit(text, (position[0] + 10, position[1] + 10))
