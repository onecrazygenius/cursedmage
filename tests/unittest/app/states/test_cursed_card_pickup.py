import unittest
import pygame
from unittest.mock import MagicMock, Mock

from app.states.cursed_card_pickup import CursedCardPickupScreen

class TestCursedCardPickupScreen(unittest.TestCase):

    def setUp(self):
        pygame.font.Font = MagicMock()
        pygame.image.load = MagicMock()
        pygame.transform.scale = MagicMock()
        pygame.display.flip = MagicMock()
        pygame.Rect = MagicMock()

        self.mock_game = MagicMock()
        self.mock_player = MagicMock()

        self.screen = CursedCardPickupScreen(self.mock_game, self.mock_player)

    def tearDown(self):
        del self.screen

    def test_pickup_card(self):
        mock_card = MagicMock()
        self.mock_player.deck.add_card = MagicMock()

        # Mocking Card class
        with unittest.mock.patch("app.logic.combat.deck.card.Card") as mock_card_class:
            mock_card_class.return_value = mock_card

            self.screen.pickup_card()

            self.assertTrue(self.mock_player.deck.add_card.called)

    def test_handle_event(self):
        mock_event = MagicMock()
        mock_event.type = pygame.MOUSEBUTTONUP
        mock_event.button = 1

        mock_rect_instance = pygame.Rect.return_value
        mock_rect_instance.collidepoint.return_value = True

        self.screen.handle_event(mock_event)

        self.assertTrue(self.mock_game.pop_state.called)

if __name__ == "__main__":
    unittest.main()