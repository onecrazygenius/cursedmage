import os, pickle

# Create a save manager class to handle saving and loading
class SaveManager:
    def __init__(self):
        # save in the user's home directory, under a folder called cursed_mage
        # if the folder doesn't exist, create it
        self.save_dir = os.path.join(os.path.expanduser("~"), ".cursed_mage")
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # save in a file called data.pkl
        self.save_file = os.path.join(self.save_dir, "data.pkl")

    def save(self, data):
        # Save the game state to a file
        with open(self.save_file, "wb") as f:
            pickle.dump(data, f)

    def load(self):
        # Load the game state from a file
        if not os.path.exists(self.save_file):
            return None
        with open(self.save_file, "rb") as f:
            data = pickle.load(f)
        return data