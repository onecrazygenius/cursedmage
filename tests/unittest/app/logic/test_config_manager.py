import unittest
import os
from app.logic.battle_manager import BattleManager
from app.logic.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary test config directory and file
        self.temp_config_dir = os.path.join(os.path.expanduser("~"), ".cursed_mage_test")
        self.temp_config_file = os.path.join(self.temp_config_dir, "config.ini")
        if not os.path.exists(self.temp_config_dir):
            os.makedirs(self.temp_config_dir)

    def test_defaults(self):
        # Test if the default values are set correctly when creating a new ConfigManager
        config_manager = ConfigManager()

        # Check the default values
        self.assertEqual(config_manager.get_width(), 1280)
        self.assertEqual(config_manager.get_height(), 720)
        self.assertFalse(config_manager.is_fullscreen())
        self.assertAlmostEqual(config_manager.get_master_volume(), 1.0, places=2)

    def tearDown(self):
        # Remove the temporary test config directory and file
        if os.path.exists(self.temp_config_file):
            os.remove(self.temp_config_file)
        if os.path.exists(self.temp_config_dir):
            os.rmdir(self.temp_config_dir)

        

    def test_save_and_load(self):
        # Test saving and loading the config
        config_manager = ConfigManager()

        # Update some values
        config_manager.update("graphics", "width", "1920")
        config_manager.update("graphics", "height", "1080")
        config_manager.update("audio", "master_volume", "0.8")

        # Save the config to the temporary file
        config_manager.config_file = self.temp_config_file
        config_manager.save()

        # Create a new ConfigManager instance and load the saved config
        new_config_manager = ConfigManager()
        new_config_manager.config_file = self.temp_config_file
        new_config_manager.config.read(self.temp_config_file)

        # Check if the loaded config matches the updated values
        self.assertEqual(int(new_config_manager.get_width()), 1920)
        self.assertEqual(int(new_config_manager.get_height()), 1080)
        self.assertAlmostEqual(new_config_manager.get_master_volume(), 0.8, places=2)




        #IS THIS RIGHT???

    def test_update(self):
        # Test updating a config value and saving it
        config_manager = ConfigManager()

        # Update a value
        config_manager.update("graphics", "fullscreen", "True")

        # Check if the value was updated
        self.assertTrue(config_manager.is_fullscreen())

        # Save the config to the temporary file
        config_manager.config_file = self.temp_config_file
        config_manager.save()

        # Create a new ConfigManager instance and load the saved config
        new_config_manager = ConfigManager()
        new_config_manager.config_file = self.temp_config_file
        new_config_manager.config.read(self.temp_config_file)

        # Check if the updated value was saved and loaded correctly
        self.assertTrue(new_config_manager.is_fullscreen())

if __name__ == '__main__':
    unittest.main()
