import json
import os

from app.constants import relative_resource_path
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
        # TODO: Long term this won't be necessary
        sprite = self.get_stat_for_character("sprite")
        if sprite is None or sprite == "None":
            sprite = "mage"
        self.sprite = "app/assets/images/sprites/" + sprite + ".png"
        self.deck = Deck(
            cards=self.starting_deck(),
        )

        # do the first card draw
        self.deck.draw_card()

    def is_dead(self):
        return self.cur_health <= 0

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
