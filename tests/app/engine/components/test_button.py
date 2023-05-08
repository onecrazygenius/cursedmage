import unittest
from unittest.mock import MagicMock, patch
import pygame
from app.engine.components.button import Button


class TestButton(unittest.TestCase):
    def setUp(self):
        self.text = "Test Button"
        self.x = 100
        self.y = 100
        self.callback = MagicMock()
        self.width = 200
        self.height = 50
        self.font_size = 24

        self.button = Button(self.text, self.x, self.y, self.callback, self.width, self.height, self.font_size)

    def test_init(self):
        self.assertEqual(self.button.text, self.text)
        self.assertEqual(self.button.x, self.x)
        self.assertEqual(self.button.y, self.y)
        self.assertEqual(self.button.callback, self.callback)
        self.assertEqual(self.button.width, self.width)
        self.assertEqual(self.button.height, self.height)
        self.assertEqual(self.button.font_size, self.font_size)
        self.assertIsInstance(self.button.rect, pygame.Rect)

    @patch("app.engine.components.button.pygame.draw.rect")
    @patch("app.engine.components.button.pygame.font.Font")
    def test_draw(self, font_mock, rect_mock):
        screen_mock = MagicMock()
        font_instance_mock = font_mock.return_value
        text_surface_mock = font_instance_mock.render.return_value

        self.button.draw(screen_mock)

        rect_mock.assert_called_once_with(screen_mock, (0, 0, 0), self.button.rect)
        font_mock.assert_called_once_with(None, self.font_size)
        font_instance_mock.render.assert_called_once_with(self.text, True, (255, 255, 255))
        text_surface_mock.get_rect.assert_called_once()


if __name__ == "__main__":
    unittest.main()
