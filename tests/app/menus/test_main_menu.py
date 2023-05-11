import unittest
from unittest.mock import MagicMock

from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP

from app.menus.main_menu import MainMenu


# Most of this class isn't testable through unit tests
class TestMainMenu(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.main_menu = MainMenu(self.game)

    def test_init(self):
        self.assertEqual(len(self.main_menu.buttons), 4)

    def test_handle_mousebuttondown_event(self):
        event = MagicMock()
        event.type = MOUSEBUTTONDOWN

        for button in self.main_menu.buttons:
            button.handle_click = MagicMock()

        self.main_menu.handle_event(event)

        for button in self.main_menu.buttons:
            button.handle_click.assert_called_once_with(event)

    def test_handle_mousebuttonup_event(self):
        event = MagicMock()
        event.type = MOUSEBUTTONUP

        for button in self.main_menu.buttons:
            button.handle_click = MagicMock()

        self.main_menu.handle_event(event)

        for button in self.main_menu.buttons:
            button.handle_click.assert_called_once_with(event)


if __name__ == "__main__":
    unittest.main()
