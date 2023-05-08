import unittest
from unittest.mock import MagicMock, patch

import pygame
from pygame import MOUSEBUTTONUP, MOUSEBUTTONDOWN

from app.menus.character_selection import CharacterSelection


class TestCharacterSelection(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.character_selection = CharacterSelection(self.game)

    def test_init(self):
        self.assertEqual(self.character_selection.game, self.game)
        self.assertEqual(len(self.character_selection.characters), 3)
        self.assertEqual(len(self.character_selection.difficulties), 3)
        self.assertEqual(self.character_selection.selected_character, 0)
        self.assertEqual(self.character_selection.selected_difficulty, 0)

    def test_select_previous_character(self):
        self.character_selection.selected_character = 0
        self.character_selection.select_previous_character()
        self.assertEqual(self.character_selection.selected_character, 2)

    def test_select_next_character(self):
        self.character_selection.selected_character = 0
        self.character_selection.select_next_character()
        self.assertEqual(self.character_selection.selected_character, 1)

    def test_select_previous_difficulty(self):
        self.character_selection.selected_difficulty = 0
        self.character_selection.select_previous_difficulty()
        self.assertEqual(self.character_selection.selected_difficulty, 2)

    def test_select_next_difficulty(self):
        self.character_selection.selected_difficulty = 0
        self.character_selection.select_next_difficulty()
        self.assertEqual(self.character_selection.selected_difficulty, 1)

    def test_start_game(self):
        self.character_selection.start_game()
        self.game.save_game.assert_called_once()
        self.game.change_state.assert_called_with(self.game.dungeon)

    def test_handle_event(self):
        pygame.init()  # This is a horrible workaround! I'm not sure why this is necessary but it fixes the issue
        event = MagicMock()
        event.type = MOUSEBUTTONUP

        # Mock each button to assert the handle_click method is called for each
        with patch.object(self.character_selection, "start_game_button",
                          wraps=self.character_selection.start_game_button) as mock_start_game_button, \
                patch.object(self.character_selection, "character_left_arrow",
                             wraps=self.character_selection.character_left_arrow) as mock_character_left_arrow, \
                patch.object(self.character_selection, "character_right_arrow",
                             wraps=self.character_selection.character_right_arrow) as mock_character_right_arrow, \
                patch.object(self.character_selection, "difficulty_left_arrow",
                             wraps=self.character_selection.difficulty_left_arrow) as mock_difficulty_left_arrow, \
                patch.object(self.character_selection, "difficulty_right_arrow",
                             wraps=self.character_selection.difficulty_right_arrow) as mock_difficulty_right_arrow:
            # Call the handle_event method and check all relevant buttons would have been triggered
            event.reset_mock()
            self.character_selection.handle_event(event)
            mock_start_game_button.handle_click.assert_called_with(event)
            mock_character_left_arrow.handle_click.assert_called_with(event)
            mock_character_right_arrow.handle_click.assert_called_with(event)
            mock_difficulty_left_arrow.handle_click.assert_called_with(event)
            mock_difficulty_right_arrow.handle_click.assert_called_with(event)

    def test_handle_event_invalid_event(self):
        pygame.init()  # This is a horrible workaround! I'm not sure why this is necessary but it fixes the issue
        event = MagicMock()
        event.type = MOUSEBUTTONDOWN

        # Mock each button to assert the handle_click method is called for each
        with patch.object(self.character_selection, "start_game_button",
                          wraps=self.character_selection.start_game_button) as mock_start_game_button, \
                patch.object(self.character_selection, "character_left_arrow",
                             wraps=self.character_selection.character_left_arrow) as mock_character_left_arrow, \
                patch.object(self.character_selection, "character_right_arrow",
                             wraps=self.character_selection.character_right_arrow) as mock_character_right_arrow, \
                patch.object(self.character_selection, "difficulty_left_arrow",
                             wraps=self.character_selection.difficulty_left_arrow) as mock_difficulty_left_arrow, \
                patch.object(self.character_selection, "difficulty_right_arrow",
                             wraps=self.character_selection.difficulty_right_arrow) as mock_difficulty_right_arrow:

            # Call the handle_event method with the wrong event type and check all relevant buttons would not have been triggered
            self.character_selection.handle_event(event)
            mock_start_game_button.handle_click.assert_not_called()
            mock_character_left_arrow.handle_click.assert_not_called()
            mock_character_right_arrow.handle_click.assert_not_called()
            mock_difficulty_left_arrow.handle_click.assert_not_called()
            mock_difficulty_right_arrow.handle_click.assert_not_called()


if __name__ == "__main__":
    unittest.main()
