import json

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
        json_file = (relative_resource_path('app/assets/data/cards.json'))
        with open(json_file, 'r') as file:
            data = json.load(file)

        for card in data:
            if card['name'] == self.name:
                return card[stat_name]

        return None
    
    def is_cursed(self):
        return self.cursed
    
    def is_heal(self):
        return self.card_type == "heal"

    def get_card_image(self):
        image_name = self.get_stat_for_card("image")
        if image_name is None or image_name == "":
            image_name = "blank"
        return "app/assets/images/cards/" + image_name + ".png"

    def draw(self, screen, position=None, scale=1.0):
        # Position set to default if not specified
        if position is None:
            position = self.position
        self.position = position

        size = (int(150 * scale), int(225 * scale))

        # Draw the card on the screen using the image
        image = pygame.image.load(relative_resource_path(self.image))
        # Scale the image to fit the card
        image = pygame.transform.scale(image, size)
        # Blit the image to the screen
        screen.blit(image, position)

        if self.is_cursed():
            return
        # Load the font
        font = pygame.font.Font(relative_resource_path('app/assets/fonts/cursed_font.tff'), 30)
        # Make the text white and bold
        text = font.render(self.name, True, WHITE)
        # Blit the text to the middle of the card
        if scale == 1.0:
            screen.blit(text, (position[0] + 75 - text.get_width() // 2, position[1] + 88 - text.get_height() // 2))
        # else change the position of the text for the scaled card
        else:
            # TODO: Fix the scaling of the text
            screen.blit(text, (position[0] + 75 - text.get_width() // 2, position[1] + 44 - text.get_height() // 2))

        # Mana cost
        text = font.render(str(self.cost), True, BLUE)
        # Blit the text to the top left of the card, 
        if scale == 1.0:
            screen.blit(text, (position[0] + 28 - text.get_width() // 2, position[1] + 30 - text.get_height() // 2))
        # else change the position of the text for the scaled card
        else:
            # TODO: Fix the scaling of the text
            screen.blit(text, (position[0] + 28 - text.get_width() // 2, position[1] + 15 - text.get_height() // 2))
        
        # Power
        text = font.render(str(self.power), True, RED)
        # Blit the text to the top right of the card
        if scale == 1.0:
            screen.blit(text, (position[0] + 122 - text.get_width() // 2, position[1] + 30 - text.get_height() // 2))
        # else change the position of the text for the scaled card
        else:
            # TODO: Fix the scaling of the text
            screen.blit(text, (position[0] + 122 - text.get_width() // 2, position[1] + 15 - text.get_height() // 2))