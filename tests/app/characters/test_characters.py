import unittest

from app.characters.character import Character
from app.combat.card import Card


class TestCharacter(unittest.TestCase):
    def setUp(self):
        # Create Character named "Player", with 100 health, 10 attack, 5 defence and 0 shield
        self.character = Character("Player", 100, 10, 5, 0)

    # Test the character class is initialised correctly
    def test_character_initialisation(self):
        self.assertEqual(self.character.name, "Player")
        self.assertEqual(self.character.max_health, 100)
        self.assertEqual(self.character.current_health, 100)
        self.assertEqual(self.character.attack, 10)
        self.assertEqual(self.character.defense, 5)
        self.assertEqual(self.character.shield, 0)

    # Test if the is dead method works for all edge cases
    def test_character_dead(self):
        # Not dead when current health is greater than max health
        self.character.current_health = 110
        self.character.max_health = 100
        self.assertFalse(self.character.is_dead())

        # Not dead when current health is greater than 0
        self.character.current_health = 50
        self.assertFalse(self.character.is_dead())

        # Not dead when the current health is 1
        self.character.current_health = 1
        self.assertFalse(self.character.is_dead())

        # Dead when the current health is 0
        self.character.current_health = 0
        self.assertTrue(self.character.is_dead())

        # Dead when the current health is -1
        self.character.current_health = -1
        self.assertTrue(self.character.is_dead())

        # Dead when the current health exceeds max health but in the negative
        self.character.current_health = -110
        self.character.max_health = 100
        self.assertTrue(self.character.is_dead())

    def test_default_hand(self):
        # Check the character has the correct number of cards by default
        self.assertEqual(len(self.character.hand), 4)
        # Check each card in the hand is an instance of Card
        for card in self.character.hand:
            self.assertIsInstance(card, Card)
        # TODO: Add check that no cursed cards are in the hand when initialised


if __name__ == '__main__':
    unittest.main()
