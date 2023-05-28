import json

import pygame, os
from app.constants import *


class Card:
    '''
    Card class for the game
    '''

    def __init__(self,
                 name,
                 ):
        self.name = name
        self.card_type = self.get_stat_for_card("card_type")
        self.power = self.get_stat_for_card("power")
        self.cost = self.get_stat_for_card("cost")
        self.cursed = self.get_stat_for_card("cursed")
        self.image = self.get_card_image()
        self.target = None
        self.position = (0, 0)

    def get_stat_for_card(self, stat_name):
        path = os.path.dirname(os.path.abspath(__file__))
        json_file = (os.path.join(path + '/../../../assets/data/cards.json'))
        with open(json_file, 'r') as file:
            data = json.load(file)

        for card in data:
            if card['name'] == self.name:
                return card[stat_name]

        return None

    def get_card_image(self):
        image_name = self.get_stat_for_card("image")
        if image_name is None or image_name == "":
            image_name = "back"
        return "app/assets/images/cards/" + image_name + ".png"

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
