import unittest

import pytest

from app.characters.enemy import Enemy
from app.characters.enemy import generate_enemy


class TestEnemy(unittest.TestCase):

    def setUp(self):
        # Create enemy named "Brute", with 100 health, 10 attack, 5 defence and 0 shield
        self.enemy = Enemy("Brute", 100, 10, 5, 0)

    # Test the enemy class is initialised correctly
    def test_enemy_initialisation(self):
        self.assertEqual(self.enemy.name, "Brute")
        self.assertEqual(self.enemy.max_health, 100)
        self.assertEqual(self.enemy.current_health, 100)
        self.assertEqual(self.enemy.attack, 10)
        self.assertEqual(self.enemy.defense, 5)
        self.assertEqual(self.enemy.shield, 0)

    # Test if the is dead method works for all edge cases
    def test_enemy_dead(self):
        # Not dead when current health is greater than max health
        self.enemy.current_health = 110
        self.enemy.max_health = 100
        self.assertFalse(self.enemy.is_dead())

        # Not dead when current health is greater than 0
        self.enemy.current_health = 50
        self.assertFalse(self.enemy.is_dead())

        # Not dead when the current health is 1
        self.enemy.current_health = 1
        self.assertFalse(self.enemy.is_dead())

        # Dead when the current health is 0
        self.enemy.current_health = 0
        self.assertTrue(self.enemy.is_dead())

        # Dead when the current health is -1
        self.enemy.current_health = -1
        self.assertTrue(self.enemy.is_dead())

        # Dead when the current health exceeds max health but in the negative
        self.enemy.current_health = -110
        self.enemy.max_health = 100
        self.assertTrue(self.enemy.is_dead())


@pytest.mark.repeat(50)
def test_generate_enemy_level_one():
    tc = unittest.TestCase()
    enemy = generate_enemy(1)
    tc.assertIsInstance(enemy, Enemy)
    tc.assertEqual(enemy.name, "Goblin")
    # Test max health is within the bounds of 50 - 100 (Inclusive)
    tc.assertGreaterEqual(enemy.max_health, 50)
    tc.assertLessEqual(enemy.max_health, 100)
    # Test attack is within the bounds of 5 - 15 (Inclusive)
    tc.assertGreaterEqual(enemy.attack, 5)
    tc.assertLessEqual(enemy.attack, 15)
    # Test defence is within the bounds of 3 - 10 (Inclusive)
    tc.assertGreaterEqual(enemy.defense, 3)
    tc.assertLessEqual(enemy.defense, 10)

@pytest.mark.repeat(50)
def test_generate_enemy_level_three():
    tc = unittest.TestCase()
    enemy = generate_enemy(3)
    tc.assertIsInstance(enemy, Enemy)
    tc.assertEqual(enemy.name, "Goblin")
    # Test max health is within the bounds of 50 - 100 * 3 (Inclusive)
    tc.assertGreaterEqual(enemy.max_health, 150)
    tc.assertLessEqual(enemy.max_health, 300)
    # Test attack is within the bounds of 5 - 15 * 3 (Inclusive)
    tc.assertGreaterEqual(enemy.attack, 15)
    tc.assertLessEqual(enemy.attack, 45)
    # Test defence is within the bounds of 3 - 10 * 3(Inclusive)
    tc.assertGreaterEqual(enemy.defense, 9)
    tc.assertLessEqual(enemy.defense, 30)


if __name__ == '__main__':
    unittest.main()
