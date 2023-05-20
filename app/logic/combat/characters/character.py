import json
import os

from app.logic.combat.deck.card import Card
from app.logic.combat.deck.deck import Deck


class Character:
    '''
    Base class for all characters in the game.
    '''
    def __init__(self, 
                 name, 
                 cards=[],
                 health=100, 
                 attack=0, 
                 defense=0, 
                 shield=0,
                 cost=3,
                 filename="characters"
                ):
        # Set the filename where the data is stored
        self.filename = filename

        self.name = name
        self.max_health = health
        self.cur_health = health
        self.attack = attack
        self.defense = defense
        self.shield = shield
        self.cost = cost
        self.max_cost = cost
        self.level = 1
        self.deck = Deck(
            cards=self.starting_deck(),
        )

        # do the first card draw
        self.deck.draw_card()

    def is_dead(self):
        return self.cur_health <= 0

    def replenish(self):
        self.cur_health = self.max_health
        self.deck.shuffle_discard_to_deck()

    def starting_deck(self):
        path = os.path.dirname(os.path.abspath(__file__))
        json_file = (os.path.join(path + '/../../../assets/data/cards.json'))
        with open(json_file, 'r') as file:
            data = json.load(file)

        starting_card_index = self.get_card_indexes_for_character()
        starting_card_data = [data[i] for i in starting_card_index]

        return [Card(**card) for card in starting_card_data]

    def get_card_indexes_for_character(self):
        path = os.path.dirname(os.path.abspath(__file__))
        json_file = (os.path.join(path + '/../../../assets/data/' + self.filename + ".json"))
        with open(json_file, 'r') as file:
            data = json.load(file)

        for character in data:
            if character['name'] == self.name:
                return character['card_indexes']

        return None

