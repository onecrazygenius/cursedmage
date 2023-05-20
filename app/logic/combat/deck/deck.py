from app.logic.combat.deck.card import Card
import random

x = [
            Card(
                name="Test Card",
                card_type="attack",
                power=1000,
                cost=1,
            ),
            Card(
                name="Test Card 2",
                card_type="attack",
                power=20,
                cost=2,
            ),
            Card(
                name="Test Card 3",
                card_type="attack",
                power=30,
                cost=3,
            ),
            Card(
                name="Test Card 4",
                card_type="attack",
                power=1000,
                cost=1,
            ),
            Card(
                name="Test Card 5",
                card_type="attack",
                power=20,
                cost=2,
            ),
            Card(
                name="Test Card 6",
                card_type="attack",
                power=30,
                cost=3,
            )
        ]

class Deck:
    '''
    Base class for all decks in the game.
    '''
    def __init__(self, 
                 cards=[],
                ):
        self.cards = cards + x 
        # Per turn variables
        self.deck    = [] + x
        self.hand    = []
        self.discard = []

    def draw_card(self, num=5):
        # Draw cards from deck, up to a maximum of 5
        for i in range(num):
            if len(self.deck) == 0:
                self.shuffle_discard_to_deck()
            if len(self.deck) == 0:
                return
            card = self.deck.pop()
            self.hand.append(card)

    def discard_card(self, card):
        # Add the card played to the discard pile
        self.discard.append(card)
        # Discard card from hand
        self.hand.remove(card)

    def shuffle_discard_to_deck(self):
        # Shuffle discard into deck
        random.shuffle(self.discard)
        self.deck = self.discard
        self.discard = []

    def add_card(self, card):
        # Add card to deck
        self.cards.append(card)
        self.deck.append(card)