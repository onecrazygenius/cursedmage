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
        card =Card("Fireball")
        self.assertNotEqual(card.name, "Thunder")
        self.assertNotEqual(card.card_type, "heal")
        self.assertNotEqual(card.power, 30)
        self.assertNotEqual(card.cost, 2)

    def test_valid_cursed_cards(self):
        card=Card("Cursed Card")
        self.assertEqual(card.name, "Cursed Card")
        self.assertEqual(card.card_type, "cursed")
        self.assertTrue(card.cursed)
    
    def test_valid_healing_cards(self):
        card=Card("Heal")
        self.assertEqual(card.name, "Heal")
        self.assertEqual(card.card_type, "heal")
        self.assertTrue(card.is_heal)




if __name__ == '__main__':
    unittest.main()
