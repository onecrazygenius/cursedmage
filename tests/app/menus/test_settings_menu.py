import unittest
from unittest.mock import MagicMock

import pygame

from app.menus.settings_menu import SettingsMenu


class TestSettingsMenu(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.settings_menu = SettingsMenu(self.game)

    def test_init(self):
        self.assertEqual(len(self.settings_menu.buttons), 4)
        self.assertEqual(len(self.settings_menu.sliders), 2)
        self.assertEqual(len(self.settings_menu.slider_labels), len(self.settings_menu.sliders))

    def test_handle_event_sliders(self):
        event = MagicMock()
        event.pos = (10, 10)  # It doesn't actually matter what this is - It just can't be None
        for event_type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            event.type = event_type

            for slider in self.settings_menu.sliders:
                slider.handle_event = MagicMock()

            self.settings_menu.handle_event(event)

            for slider in self.settings_menu.sliders:
                slider.handle_event.assert_called_once_with(event)

    def test_handle_event_button_clicked(self):
        event = MagicMock()
        event.pos = (10, 10)  # At this point it doesn't actually matter where the click pos is - It just can't be None
        event.type = pygame.MOUSEBUTTONDOWN
        self.settings_menu.sliders = []  # To not test the sliders, override and remove them

        # For each button set the callback method to a MagicMock and set the position of each card.
        base_position = 200
        for button in self.settings_menu.buttons:
            button.callback = MagicMock()
            button.y = 200
            button.x = base_position
            base_position += 200

        self.settings_menu.handle_event(event)

        for button in self.settings_menu.buttons:
            event.pos = (button.x, button.y)  # This ensures the button would have been clicked
            self.settings_menu.handle_event(event)
            button.callback.assert_called_once()

    def test_return_to_main_menu(self):
        self.settings_menu.return_to_main_menu()
        self.game.show_main_menu.assert_called_once()

    def test_exit_game(self):
        self.settings_menu.exit_game()
        self.game.quit_game.assert_called_once()


if __name__ == "__main__":
    unittest.main()
