import unittest

from app.logic.combat.characters.character import Character

class TestCharacter(unittest.TestCase):
    def test_valid_character_initialisation(self):
       character  = Character("Warrior")
       self.assertEqual(character.name, "Warrior") 
       self.assertEqual(character.max_health, 500)
       self.assertEqual(character.attack, 3)
       self.assertEqual(character.defense, 4)
       self.assertEqual(character.cost, 3)
       self.assertIsNotNone(character.sprite)

    def test_invalid_character_initialisation(self):
       character  = Character("Warrior")
       self.assertNotEqual(character.name, "Mage") 
       self.assertNotEqual(character.max_health, 5)
       self.assertNotEqual(character.attack, 5)
       self.assertNotEqual(character.defense, 5)
       self.assertNotEqual(character.cost, 5)       


    def test_health_stats(self):
        character = Character("Warrior")
        character.cur_health = 200
        self.assertEqual(character.cur_health, 200)
        self.assertFalse(character.is_dead)

    

 




       




if __name__ == '__main__':
    unittest.main()