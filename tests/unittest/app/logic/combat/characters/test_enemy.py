import unittest

from app.logic.combat.characters.enemy import Enemy

class TestCharacter(unittest.TestCase):
    def test_valid_character_initialisation(self):
       enemy  = Enemy("Goblin")
       self.assertEqual(enemy.name, "Goblin") 
       self.assertEqual(enemy.max_health, 100)
       self.assertEqual(enemy.attack, 3)
       self.assertEqual(enemy.defense, 4)
       self.assertEqual(enemy.cost, 3)
       self.assertIsNotNone(enemy.sprite)

    def test_invalid_enemy_initialisation(self):
       enemy  = Enemy("Goblin")
       self.assertNotEqual(enemy.name, "Mage") 
       self.assertNotEqual(enemy.max_health, 5)
       self.assertNotEqual(enemy.attack, 5)
       self.assertNotEqual(enemy.defense, 5)
       self.assertNotEqual(enemy.cost, 5)       


    def test_health_stats(self):
        enemy = Enemy("Goblin")
        enemy.cur_health = 200
        self.assertEqual(enemy.cur_health, 200)
        self.assertFalse(enemy.is_dead)