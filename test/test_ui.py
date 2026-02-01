import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from src.ui import UserInterface


class TestUserInterface(unittest.TestCase):

    def setUp(self):
        self.ui = UserInterface()
        self.frame = np.zeros((480, 640, 3), dtype=np.uint8)

    @patch('cv2.imshow')
    def test_update_view_calls_imshow(self, mock_imshow):
        self.ui.update_view(self.frame, event_data=None, alert_active=False)
        mock_imshow.assert_called_once()
        args, _ = mock_imshow.call_args
        self.assertEqual(args[0], "Fire Detection System", "Wrong Title")

    @patch('cv2.rectangle')
    @patch('cv2.putText')
    @patch('cv2.imshow')
    def test_draws_box_on_fire_event(self, mock_imshow, mock_text, mock_rect):
        event_data = {
            "timestamp": "2026-02-02T14:30:00",
            "box": (10, 10, 50, 50)  # x, y, w, h
        }

        self.ui.update_view(self.frame, event_data=event_data, alert_active=True)

        mock_rect.assert_called()
        mock_text.assert_called()

    @patch('cv2.waitKey')
    def test_check_input(self, mock_waitkey):
        mock_waitkey.return_value = ord('q')
        key = self.ui.check_input()
        self.assertEqual(key, ord('q'))