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
        self.deck    = [] + self.cards
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
        if card in self.hand:
            self.hand.remove(card)

    def shuffle_discard_to_deck(self):
        # Shuffle discard into deck
        random.shuffle(self.discard)
        self.deck = self.discard
        self.discard = []

    def add_card(self, card):
        # Add card to the full deck list
        self.cards.append(card)
        # Add card to the discard pile
        self.discard.append(card)