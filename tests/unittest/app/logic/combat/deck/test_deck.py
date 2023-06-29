import unittest

from app.logic.combat.characters.character import Character


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


if __name__ == '__main__':
    unittest.main()