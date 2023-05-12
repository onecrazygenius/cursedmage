from app.combat.deck.card import Card
import random

class Deck:
    '''
    Base class for all decks in the game.
    '''
    def __init__(self, 
                 cards=[],
                ):
        self.cards = cards

        # Per turn variables
        self.deck    = []
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