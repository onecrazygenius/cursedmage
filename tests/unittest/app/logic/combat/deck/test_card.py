import unittest

from app.logic.combat.deck.card import Card


class TestCard(unittest.TestCase):
    def test_valid_card_initialisation(self):
        card = Card("Fireball")
        self.assertEqual(card.name, "Fireball")
        self.assertEqual(card.card_type, "attack")
        self.assertEqual(card.power, 20)
        self.assertEqual(card.cost, 1)
        self.assertFalse(card.cursed)
        self.assertIsNotNone(card.image)
        self.assertIsNone(card.target)
        self.assertEqual(card.position, (0, 0))

    def test_invalid_card_initialisation(self):
        self.assertFalse(True)


if __name__ == '__main__':
    unittest.main()
