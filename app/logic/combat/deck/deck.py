import random

from app.logging_config import logger


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
        self.max_hand_size = 3

    def draw_card(self, num=5):
        # Draw cards from deck, up to the max hand size
        while len(self.hand) < self.max_hand_size and num > 0:
            if len(self.deck) == 0:
                self.move_discard_to_deck()
            if len(self.deck) == 0:
                return
            card = self.deck.pop()
            # add card to hand
            self.hand.append(card)

        # if all the cards are cursed, discard them and draw again
        if len(self.hand) > 0:
            if all(card.is_cursed() for card in self.hand):
                self.ready_deck_for_combat()
                self.draw_card(num)

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
        logger.debug(f"Player had {len(self.deck)} cards in the deck, "
                     f"{len([card for card in self.deck if card.cursed])} of which are cursed")
        # Add card to the full deck list
        self.cards.append(card)
        # Add card to the discard pile
        self.deck.append(card)
        logger.debug(f"After Adding a card, Player had {len(self.deck)} cards in the deck, "
                     f"{len([card for card in self.deck if card.cursed])} of which are cursed")

    # Removes the card entirely. NOT to be confused with discard_card
    def remove_card(self, card):
        # The card object does not actually exist in the deck, it's a new instance so remove the same type.
        # Always use the 0 index from the returning list as it doesn't matter exactly which card is upgraded
        card = [player_card for player_card in self.cards if player_card.name == card.name][0]

        logger.debug(f"Player had {len(self.deck)} cards in the deck, "
                     f"{len([card for card in self.deck if card.cursed])} of which are cursed")
        self.cards.remove(card)
        try:
            self.deck.remove(card)
        except ValueError:
            # Do nothing
            pass
        try:
            self.hand.remove(card)
        except ValueError:
            # Do nothing
            pass
        try:
            self.discard.remove(card)
        except ValueError:
            # Do nothing
            pass

        logger.debug(f"After Removing a Card, Player had {len(self.deck)} cards in the deck, "
                     f"{len([card for card in self.deck if card.cursed])} of which are cursed")

    def ready_deck_for_combat(self):
        self.move_discard_to_deck()
        self.move_hand_to_deck()
        random.shuffle(self.deck)
