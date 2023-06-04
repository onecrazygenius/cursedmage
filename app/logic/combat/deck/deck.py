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
                self.move_discard_to_deck()
            if len(self.deck) == 0:
                return
            card = self.deck.pop()
            self.hand.append(card)

    def discard_card(self, card):
        # Add the card played to the discard pile
        self.discard.append(card)
        # Discard card from hand
        self.hand.remove(card)

    def move_discard_to_deck(self):
        # Move all cards in discard back to deck
        self.deck.extend(self.discard)
        self.discard = []

    def move_hand_to_deck(self):
        # Move all cards in hand back to deck
        self.deck.extend(self.hand)
        self.hand = []

    def add_card(self, card):
        # Add card to the full deck list
        self.cards.append(card)
        # Add card to the discard pile
        self.discard.append(card)

    def ready_deck_for_combat(self):
        self.move_discard_to_deck()
        self.move_hand_to_deck()
        random.shuffle(self.deck)
