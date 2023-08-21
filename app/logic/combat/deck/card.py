import json

from app.constants import *
from app.logic.combat.effect import Effect


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
        self.upgrades_to = self.get_stat_for_card("upgrades_to")
        self.image = self.get_card_image()
        self.hit_sound = self.get_hit_sound()
        self.target = None
        self.position = (0, 0)

        self.effects = []
        effect_names = self.get_stat_for_card("effects")
        for effect_name in effect_names:
            self.effects.append(Effect(effect_name))

    def get_stat_for_card(self, stat_name):
        try:
            json_file = (relative_resource_path('app/assets/data/cards.json'))
            with open(json_file, 'r') as file:
                data = json.load(file)

            for card in data:
                if card['name'] == self.name:
                    return card[stat_name]

            return None
        except KeyError as e:
            return None
    
    def get_hit_sound(self):
        sound_name = self.get_stat_for_card("hit_sound")
        if sound_name is None or sound_name == "":
            sound_name = "card_hit"
        return pygame.mixer.Sound(relative_resource_path("app/assets/music/sounds/" + sound_name + ".mp3"))

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
        if self.upgrades_to == "MAXLEVEL":
            text = font.render(self.name, True, UPGRADED_CARD_GREEN)
        # Calculate the scaled position of the text, accounting for the base position and scale factor
        text_position = (position[0] + 75 * scale - text.get_width() // 2,
                         position[1] + 33 * scale - text.get_height() // 2)
        # Blit the text to the screen
        screen.blit(text, text_position)

        # Mana cost
        text = font.render(str(self.cost), True, BLUE)
        # Calculate the scaled position of the text, accounting for the base position and scale factor
        text_position = (position[0] + 31 * scale - text.get_width() // 2,
                         position[1] + 63 * scale - text.get_height() // 2)
        # Blit the text to the screen
        screen.blit(text, text_position)

        # Power
        text = font.render(str(self.power), True, WHITE)
        # Calculate the scaled position of the text, accounting for the base position and scale factor
        text_position = (position[0] + 122 * scale - text.get_width() // 2,
                         position[1] + 63 * scale - text.get_height() // 2)
        # Blit the text to the screen
        screen.blit(text, text_position)

    def __getstate__(self):
        # Remove the image and hit sound from the card's state before pickling
        state = self.__dict__.copy()
        del state["image"]
        del state["hit_sound"]
        return state

    def __setstate__(self, state):
        # Update the object's state with the data that was pickled
        self.__dict__.update(state)
        # Recreate the image and hit sound after unpickling
        self.image = self.get_card_image()
        self.hit_sound = self.get_hit_sound()    