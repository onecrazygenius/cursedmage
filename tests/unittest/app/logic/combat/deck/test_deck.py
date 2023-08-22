import unittest

from app.logic.combat.characters.character import Character
from app.logic.combat.deck.card import Card
from app.logic.combat.deck.deck import Deck


class TestDeck(unittest.TestCase):

    def test_deck_size_correct_after_drawing_card(self):
            character = Character("Warrior")
            character.deck.draw_card()
            self.assertEqual(len(character.deck.hand), 3)

    def test_deck_size_correct_after_discarding(self):
         character = Character("Mage")
         self.assertEqual(len(character.deck.hand), 3)
         character.deck.discard_card(character.deck.hand[0])
         self.assertEqual(len(character.deck.hand), 2)

    def test_move_hand_to_deck(self):
        card1 = Card("Fireball")
        card2 = Card("Heal")
        card3 = Card("Cursed Card")
        cards = [card1, card2, card3]
        deck = Deck(cards=cards)

        deck.move_hand_to_deck()

        self.assertEqual(len(deck.deck), 3)
        self.assertEqual(len(deck.hand), 0)

    def test_add_card(self):
        card = Card("Fireball")
        deck = Deck()

        deck.add_card(card)

        self.assertIn(card, deck.cards)
        self.assertIn(card, deck.discard)

    def test_ready_deck_for_combat(self):
        card1 = Card("Fireball")
        card2 = Card("Heal")
        card3 = Card("Cursed Card")
        cards = [card1, card2, card3]
        deck = Deck(cards=cards)

        deck.ready_deck_for_combat()

        self.assertEqual(len(deck.deck), 3)
        self.assertEqual(len(deck.discard), 0)
        self.assertEqual(len(deck.hand), 0)


if __name__ == '__main__':
    unittest.main()