import unittest
from unittest.mock import MagicMock, patch

from pygame import FULLSCREEN, RESIZABLE

from app.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from app.logic.save_manager import SaveManager
from app.main import Game
from app.states.character_selection import CharacterSelection
from app.states.main_menu import MainMenu
from app.states.settings import SettingsMenu
from app.menus.victory_screen import VictoryScreen


class TestGame(unittest.TestCase):
    def setUp(self):
        # Patch pygame.init to do nothing so PyGame doesn't actually start
        with patch("pygame.init"):
            self.game = Game()


    def test_init(self):
        # Check save_manager is an instance of SaveManager
        self.assertIsInstance(self.game.save_manager, SaveManager)
        # Check the initial state is an instance of MainMenu
        self.assertIsInstance(self.game.states[0], MainMenu)
        # Check settings_menu_open is set to False
        self.assertFalse(self.game.settings_menu_open)
        # Check character and difficulty are set to None
        self.assertIsNone(self.game.character)
        self.assertIsNone(self.game.difficulty)
        # Check dungeon and combat are set to None
        self.assertIsNone(self.game.dungeon)
        self.assertIsNone(self.game.combat)
        # Check done is set to False
        self.assertFalse(self.game.done)

    def test_resize_screen(self):
        with patch("pygame.display.set_mode") as mock_set_mode:
            # Test resizing to arbitrary width and height
            self.game.resize_screen(1234, 1612)
            mock_set_mode.assert_called_once()

    def test_toggle_fullscreen(self):
        with patch("pygame.display.set_mode") as mock_set_mode:
            self.game.toggle_fullscreen()
            mock_set_mode.assert_called_once_with((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN | RESIZABLE)

    def test_toggle_fullscreen_off(self):
        screen_mock = MagicMock()
        screen_mock.get_flags.return_value = FULLSCREEN  # Set game flags to fullscreen, mocking fullscreen enabled
        with patch("pygame.display.set_mode", return_value=screen_mock) as mock_set_mode:
            self.game.screen = screen_mock
            self.game.toggle_fullscreen()
            mock_set_mode.assert_called_once_with((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)

    def test_push_state(self):
        new_state = MagicMock()
        self.game.push_state(new_state)
        self.assertEqual(self.game.states[-1], new_state)

    def test_pop_state(self):
        initial_state_count = len(self.game.states)
        self.game.pop_state()
        self.assertEqual(len(self.game.states), initial_state_count - 1)

    def test_change_state(self):
        new_state = MagicMock()
        self.game.change_state(new_state)
        self.assertEqual(self.game.states[-1], new_state)
        self.assertEqual(len(self.game.states), 1)

    # Saving and loading the game would form an integration test - See the SaveManager tests for that

    @patch("pygame.mixer.music.set_volume")
    def test_change_master_volume(self, mock_set_volume):
        test_volume = 5
        self.game.change_master_volume(test_volume)
        mock_set_volume.assert_called_once_with(test_volume)

    def test_sfx_volume(self):
        self.fail("SFX Volume not implemented yet")

    def test_new_game(self):
        self.game.new_game()
        self.assertIsInstance(self.game.states[-1], CharacterSelection)

    def test_show_main_menu(self):
        self.game.show_main_menu()
        self.assertIsInstance(self.game.states[-1], MainMenu)

    def test_show_settings(self):
        self.game.show_settings()
        self.assertIsInstance(self.game.states[-1], SettingsMenu)
        self.assertTrue(self.game.settings_menu_open)

    def test_hide_settings(self):
        self.game.show_settings()
        self.game.hide_settings()
        self.assertFalse(self.game.settings_menu_open)

    def test_quit_game(self):
        self.game.quit_game()
        self.assertTrue(self.game.done)

    def test_victory(self):
        self.game.victory()
        self.assertIsInstance(self.game.states[-1], VictoryScreen)


if __name__ == '__main__':
    unittest.main()
