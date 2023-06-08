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

        # Calculate scaled font size based on scale factor
        font_size = int(30 * (scale + 0.2))
        # Load the font with the scaled font size
        font = pygame.font.Font(relative_resource_path('app/assets/fonts/pixel_font.ttf'), font_size)

        # Make the text white and bold
        text = font.render(self.name, True, WHITE)
        # Calculate the scaled position of the text, accounting for the base position and scale factor
        text_position = (
        position[0] + 75 * scale - text.get_width() // 2, position[1] + 86 * scale - text.get_height() // 2)
        # Blit the text to the screen
        screen.blit(text, text_position)

        # Mana cost
        text = font.render(str(self.cost), True, BLUE)
        # Calculate the scaled position of the text, accounting for the base position and scale factor
        text_position = (
        position[0] + 28 * scale - text.get_width() // 2, position[1] + 30 * scale - text.get_height() // 2)
        # Blit the text to the screen
        screen.blit(text, text_position)

        # Power
        text = font.render(str(self.power), True, WHITE)
        # Calculate the scaled position of the text, accounting for the base position and scale factor
        text_position = (
        position[0] + 122 * scale - text.get_width() // 2, position[1] + 30 * scale - text.get_height() // 2)
        # Blit the text to the screen
        screen.blit(text, text_position)

