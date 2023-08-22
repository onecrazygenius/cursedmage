import unittest
import os
import pickle
from app.logic.battle_manager import BattleManager
from app.logic.config_manager import ConfigManager
from app.logic.save_manager import SaveManager

class TestSaveManager(unittest.TestCase):
    #I AM NOT READING THAT ERROR

    def setUp(self):
        # Create a temporary test save directory and file
        self.temp_save_dir = os.path.join(os.path.expanduser("~"), ".cursed_mage_test")
        self.temp_save_file = os.path.join(self.temp_save_dir, "data.pkl")
        if not os.path.exists(self.temp_save_dir):
            os.makedirs(self.temp_save_dir)

    def tearDown(self):
        # Remove the temporary test save directory and file
        if os.path.exists(self.temp_save_file):
            os.remove(self.temp_save_file)
        if os.path.exists(self.temp_save_dir):
            os.rmdir(self.temp_save_dir)

    def test_save_and_load(self):
        # Test saving and loading game state
        save_manager = SaveManager()

        # Test saving and loading when the save file does not exist
        self.assertIsNone(save_manager.load())

        # Create a test data dictionary to save
        test_data = {"player_name": "Warrior", "level": 10, "score": 500}

        # Save the test data to the temporary file
        save_manager.save_file = self.temp_save_file
        save_manager.save(test_data)

        # Create a new SaveManager instance and load the saved data
        new_save_manager = SaveManager()
        new_save_manager.save_file = self.temp_save_file
        loaded_data = new_save_manager.load()

        # Check if the loaded data matches the saved test data
        self.assertEqual(loaded_data, test_data)

    def test_nuke_save_file(self):
        # Test nuking (deleting) the save file
        save_manager = SaveManager()

        # Create a test data dictionary to save
        test_data = {"player_name": "Warrior", "level": 10, "score": 500}

        # Save the test data to the temporary file
        save_manager.save_file = self.temp_save_file
        save_manager.save(test_data)

        # Check if the save file exists before nuking
        self.assertTrue(os.path.exists(self.temp_save_file))

        # Nuke the save file
        save_manager.nuke_save_file()

        # Check if the save file has been deleted
        self.assertFalse(os.path.exists(self.temp_save_file))

if __name__ == '__main__':
    unittest.main()