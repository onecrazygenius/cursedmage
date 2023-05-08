import unittest
from unittest.mock import patch, MagicMock

from app.menus.components.room import Room


class TestSaveManager(unittest.TestCase):

    def setUp(self):
        self.game = "Game instance"
        self.position = (1, 2)
        self.enemy = "Enemy instance"
        self.next = True
        self.visited = False
        self.completed = False
        self.room = Room(self.game, self.position, self.enemy, self.next, self.visited, self.completed)

    def test_init(self):
        self.assertEqual(self.room.game, self.game)
        self.assertEqual(self.room.position, self.position)
        self.assertEqual(self.room.enemy, self.enemy)
        self.assertEqual(self.room.next, self.next)
        self.assertEqual(self.room.visited, self.visited)
        self.assertEqual(self.room.completed, self.completed)

    def test_get_data(self):
        expected_data = {
            "enemy": self.enemy,
            "next": self.next,
            "visited": self.visited,
            "completed": self.completed,
        }
        self.assertEqual(self.room.get_data(), expected_data)

    @patch("pygame.Surface")
    @patch("pygame.Rect")
    def test_draw_room_completed(self, mock_rect, mock_surface):
        screen = MagicMock()
        self.room.completed = True
        self.room.visited = False
        self.room.next = False
        self.room.draw(screen)
        mock_surface.return_value.fill.assert_called_with((0, 255, 0))  # Tests that the colour is correct
        screen.blit.assert_called_with(mock_surface.return_value, mock_rect.return_value)

    @patch("pygame.Surface")
    @patch("pygame.Rect")
    def test_draw_room_visited(self, mock_rect, mock_surface):
        screen = MagicMock()
        self.room.completed = False
        self.room.visited = True
        self.room.next = False
        self.room.draw(screen)
        mock_surface.return_value.fill.assert_called_with((0, 0, 255))
        screen.blit.assert_called_with(mock_surface.return_value, mock_rect.return_value)

    @patch("pygame.Surface")
    @patch("pygame.Rect")
    def test_draw_room_next(self, mock_rect, mock_surface):
        screen = MagicMock()
        self.room.completed = False
        self.room.visited = False
        self.room.next = True
        self.room.draw(screen)
        mock_surface.return_value.fill.assert_called_with((255, 0, 0))
        screen.blit.assert_called_with(mock_surface.return_value, mock_rect.return_value)

    @patch("pygame.Surface")
    @patch("pygame.Rect")
    def test_draw_room(self, mock_rect, mock_surface):
        screen = MagicMock()
        self.room.completed = False
        self.room.visited = False
        self.room.next = False
        self.room.draw(screen)
        mock_surface.return_value.fill.assert_called_with((0, 0, 0))
        screen.blit.assert_called_with(mock_surface.return_value, mock_rect.return_value)


if __name__ == '__main__':
    unittest.main()
