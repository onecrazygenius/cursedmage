import json

import pygame

from app.constants import relative_resource_path, BOSS_CURSED_CARD_REQUIREMENT
from app.logic.combat.deck.card import Card
from app.logic.combat.deck.deck import Deck


class Character:
    '''
    Base class for all characters in the game.
    '''

    def __init__(self,
                 name,
                 shield=0,
                 filename="characters"
                 ):
        # Set the filename where the data is stored
        self.filename = filename

        self.name = name
        self.max_health = self.get_stat_for_character("health")
        self.cur_health = self.max_health
        self.attack = self.get_stat_for_character("attack")
        self.defense = self.get_stat_for_character("defence")
        self.shield = shield
        self.cost = self.get_stat_for_character("cost")
        self.max_cost = self.cost
        self.level = 1

        # TODO: Long term this won't be necessary. It's because we are missing 2 character sprites
        sprite = self.get_stat_for_character("sprite")
        if sprite is None or sprite == "None":
            sprite = "mage"
        self.sprite = "app/assets/images/sprites/" + sprite + ".png"
        self.spritesheet_path = "app/assets/images/sprites/" + sprite + "_spritesheet.png"

        self.character_frames = self.spritesheet_to_frames()

        self.deck = Deck(
            cards=self.starting_deck(),
        )

        # do the first card draw
        self.deck.draw_card()

    def __getstate__(self):
        state = self.__dict__.copy()
        # Don't pickle character_frames
        del state["character_frames"]
        return state

    def is_dead(self):
        return self.cur_health <= 0

    def boss_requirements_met(self):
        # For now the only requirement is the player has X or more cursed cards.
        # We may want to add more in the future
        return [card.name for card in self.deck.cards].count("Cursed Card") >= BOSS_CURSED_CARD_REQUIREMENT

    # Used to replenish the players health, cost and put all their cards back into the deck
    def replenish(self, health=False):
        self.deck.ready_deck_for_combat()
        self.deck.draw_card(3 - len(self.deck.hand))
        self.cost = self.max_cost
        if health:
            self.cur_health = self.max_health

    def starting_deck(self):
        json_file = (relative_resource_path('app/assets/data/cards.json'))
        with open(json_file, 'r') as file:
            data = json.load(file)

        starting_card_index = self.get_card_indexes_for_character()
        starting_card_names = [card['name'] for card in [data[i] for i in starting_card_index]]

        return [Card(card_name) for card_name in starting_card_names]

    def get_card_indexes_for_character(self):
        json_file = (relative_resource_path('/app/assets/data/' + self.filename + ".json"))
        with open(json_file, 'r') as file:
            data = json.load(file)

        for character in data:
            if character['name'] == self.name:
                return character['card_indexes']

        return None

    def get_stat_for_character(self, stat_name):
        json_file = (relative_resource_path('app/assets/data/' + self.filename + ".json"))
        with open(json_file, 'r') as file:
            data = json.load(file)

        for character in data:
            if character['name'] == self.name:
                return character[stat_name]

        return None

    def spritesheet_to_frames(self):
        # Cut the spritesheet into frames
        spritesheet = pygame.image.load(relative_resource_path(self.spritesheet_path))
        spritesheet_width, spritesheet_height = spritesheet.get_size()

        # Calculate the dimensions of each frame
        FRAME_WIDTH = spritesheet_width // 8
        FRAME_HEIGHT = spritesheet_height  # Assuming there's only one row

        character_frames = []
        for i in range(8):  # Assuming there are 8 frames horizontally in your spritesheet
            frame = spritesheet.subsurface((i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
            character_frames.append(pygame.transform.scale(frame, (250, 250)))  # Scale the frames

        return character_frames
