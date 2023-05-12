import unittest
from unittest.mock import MagicMock, patch

from pygame import MOUSEBUTTONDOWN

from app.engine.components.button import Button
from app.menus.victory_screen import VictoryScreen


class TestVictoryScreen(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.victory_screen = VictoryScreen(self.game)

    def test_init(self):
        self.assertIsInstance(self.victory_screen.button, Button)
        self.assertEqual(self.victory_screen.button.text, "Back to Main Menu")
        self.assertEqual(self.victory_screen.button.x, self.game.config.get_width() // 2)
        self.assertEqual(self.victory_screen.button.y, 300)
        self.assertEqual(self.victory_screen.button.callback, self.victory_screen.back_to_main_menu)

    def test_back_to_main_menu(self):
        self.victory_screen.back_to_main_menu()
        self.game.show_main_menu.assert_called_once()

    def test_handle_event(self):
        event = MagicMock()
        event.type = MOUSEBUTTONDOWN
        event.button = 1  # 1 is left mouse button
        with patch.object(self.victory_screen.button, "handle_click") as mock_handle_click:
            self.victory_screen.handle_event(event)
            mock_handle_click.assert_called_once_with(event)


if __name__ == "__main__":
    unittest.main()
