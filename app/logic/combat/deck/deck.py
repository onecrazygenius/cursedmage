from app.logic.combat.deck.card import Card
import random

x = [
            Card(
                name="Test Card",
                card_type="attack",
                power=10,
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
        # Draw cards from deck
        for i in range(num):
            # If deck is empty, shuffle discard into deck
            if len(self.deck) == 0:
                self.shuffle()
                self.replenish()
            # Draw card
            self.hand.append(self.deck.pop())

    def discard_card(self, index=0):
        # Discard card from hand
        self.discard.append(self.hand.pop(index))

    def shuffle(self):
        # Shuffle discard into deck
        random.shuffle(self.discard)
        self.deck = self.discard
        self.discard = []

    def replenish(self):
        # Replenish deck from discard
        self.deck = self.discard