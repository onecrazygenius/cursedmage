import os, configparser

from app.constants import resource_path


# Create a config manager class to handle saving and loading
class ConfigManager:

    def __init__(self):
        # save in the user's home directory, under a folder called cursed_mage
        # if the folder doesn't exist, create it
        self.config_dir = resource_path(os.path.expanduser("~") + ".cursed_mage")
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        # save in a file called config.ini
        self.config_file = resource_path(self.config_dir + "config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

        # Set default values
        if not self.config.has_section("graphics"):
            self.config.add_section("graphics")
        if not self.config.has_option("graphics", "fullscreen"):
            self.config.set("graphics", "fullscreen", "False")
        if not self.config.has_option("graphics", "width"):
            self.config.set("graphics", "width", "1280")
        if not self.config.has_option("graphics", "height"):
            self.config.set("graphics", "height", "720")
        if not self.config.has_option("graphics", "fps"):
            self.config.set("graphics", "fps", "60")

        if not self.config.has_section("audio"):
            self.config.add_section("audio")
        if not self.config.has_option("audio", "master_volume"):
            self.config.set("audio", "master_volume", "1.0")
        if not self.config.has_option("audio", "sfx_volume"):
            self.config.set("audio", "sfx_volume", "1.0")

    def save(self):
        # Save the config to a file
        with open(self.config_file, "w") as f:
            self.config.write(f)

    def get(self, section, option):
        # read a value from the config file
        return self.config.get(section, option)
    
    def update(self, section, option, value):
        self.config.set(section, option, value)
        self.save()

    def get_width(self):
        return int(self.config.get("graphics", "width"))
    
    def get_height(self):
        return int(self.config.get("graphics", "height"))
    
    def get_master_volume(self):
        return float(self.config.get("audio", "master_volume"))