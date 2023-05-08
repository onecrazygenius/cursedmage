import unittest
from unittest.mock import MagicMock
import pygame

from app.engine.components.slider import Slider


class TestSlider(unittest.TestCase):

    def setUp(self):
        self.callback = MagicMock()
        self.slider = Slider(10, 20, 100, 50, 200, self.callback)

    def test_init(self):
        self.assertEqual(self.slider.x, 10)
        self.assertEqual(self.slider.y, 20)
        self.assertEqual(self.slider.width, 100)
        self.assertEqual(self.slider.value, 50)
        self.assertEqual(self.slider.max_value, 200)
        self.assertEqual(self.slider.callback, self.callback)

    def test_is_on_handle(self):
        # This fails because 10 < 10 is not true. I believe this is an error in the is_on_handle method
        self.assertTrue(self.slider._is_on_handle((25, 25)))
        self.assertFalse(self.slider._is_on_handle((100, 100)))

    # Various aspects of this test fail because of the error identified in the test above. Needs fixing then reviewing
    def test_handle_event(self):
        # Test MOUSEBUTTONDOWN
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(25, 25))
        self.slider.handle_event(mouse_down_event)
        self.assertTrue(self.slider.dragging)

        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(30, 30))
        self.slider.handle_event(mouse_down_event)
        self.assertTrue(self.slider.dragging)

        # Test MOUSEBUTTONUP
        mouse_up_event = pygame.event.Event(pygame.MOUSEBUTTONUP)
        self.slider.handle_event(mouse_up_event)
        self.assertFalse(self.slider.dragging)

        # Test MOUSEMOTION
        # To test mouse motion there will always have been a button down event too
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(25, 25))
        self.slider.handle_event(mouse_down_event)
        mouse_motion_event = pygame.event.Event(pygame.MOUSEMOTION, pos=(40, 25))
        self.slider.handle_event(mouse_motion_event)
        self.assertTrue(self.slider.dragging)
        self.assertEqual(self.slider.handle_x, 40)
        self.assertEqual(self.slider.value, 60)
        self.callback.assert_called_with(60)


if __name__ == '__main__':
    unittest.main()
