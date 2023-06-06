import os
import unittest
import tempfile
import shutil
import pickle

from app.constants import relative_resource_path
from app.logic.save_manager import SaveManager


class TestSaveManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing purposes
        self.test_dir = tempfile.mkdtemp()
        self.save_manager = SaveManager()
        # Set the save directory and file to the temporary directory
        self.save_manager.save_dir = self.test_dir
        self.save_manager.save_file = relative_resource_path(self.test_dir + "data.pkl")

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.test_dir)

    def test_save(self):
        test_data = {"test_load_key": "test_load_value"}

        # Save the data using SaveManager
        self.save_manager.save(test_data)

        # Check if the save file was created
        self.assertTrue(os.path.exists(self.save_manager.save_file))

        # Load the data directly from the file and compare
        with open(self.save_manager.save_file, "rb") as f:
            loaded_data = pickle.load(f)

        self.assertEqual(test_data, loaded_data)

    def test_load(self):
        test_data = {"test_load_key": "test_load_value"}

        # Save the data directly to the file
        with open(self.save_manager.save_file, "wb") as f:
            pickle.dump(test_data, f)

        # Load the data using SaveManager and compare
        loaded_data = self.save_manager.load()
        self.assertEqual(test_data, loaded_data)

    def test_save_and_load(self):
        test_data = {"test_save_and_load_key": "test_save_and_load_value"}

        # Save the data using SaveManager
        self.save_manager.save(test_data)

        # Check if the save file was created
        self.assertTrue(os.path.exists(self.save_manager.save_file))

        # Load the data using SaveManager and compare
        loaded_data = self.save_manager.load()

        self.assertEqual(test_data, loaded_data)

    def test_load_non_existent_file(self):
        # Delete the save file if it exists
        if os.path.exists(self.save_manager.save_file):
            os.remove(self.save_manager.save_file)

        # Attempt to load from a non-existent file
        loaded_data = self.save_manager.load()

        # Check if the loaded data is None
        self.assertIsNone(loaded_data)

    def test_save_non_existent_file(self):
        # Delete the save file if it exists
        if os.path.exists(self.save_manager.save_file):
            os.remove(self.save_manager.save_file)

        test_data = {"test_save_non_existent_file_key": "test_save_non_existent_file_value"}

        # Save the data using SaveManager
        self.save_manager.save(test_data)

        # Check if the save file was created
        self.assertTrue(os.path.exists(self.save_manager.save_file))

        # Attempt to load from the file
        loaded_data = self.save_manager.load()
        self.assertEqual(test_data, loaded_data)

    def test_save_invalid_data(self):
        test_data = "Meaningless    badly___formatted:: DATA!"

        # Save the data using SaveManager
        self.save_manager.save(test_data)

        # Check if the save file was created
        self.assertTrue(os.path.exists(self.save_manager.save_file))

        loaded_data = self.save_manager.load()

        # TODO: Data should probably be filtered to ensure it's JSON
        # Check if the loaded data is None
        self.assertIsNone(loaded_data)


if __name__ == '__main__':
    unittest.main()
