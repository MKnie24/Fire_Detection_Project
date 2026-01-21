import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from src.ui import UserInterface


class TestUserInterface(unittest.TestCase):

    def setUp(self):
        self.ui = UserInterface()
        # Dummy frame (black image)
        self.frame = np.zeros((480, 640, 3), dtype=np.uint8)

    @patch('cv2.imshow')
    def test_update_view_calls_imshow(self, mock_imshow):
        """
        Test if update_view actually tries to display the image.
        """
        self.ui.update_view(self.frame, event_data=None, alert_active=False)

        # Verify that cv2.imshow was called exactly once
        mock_imshow.assert_called_once()
        args, _ = mock_imshow.call_args
        self.assertEqual(args[0], "Fire Detection System", "Window title mismatch")

    @patch('cv2.rectangle')
    @patch('cv2.putText')
    @patch('cv2.imshow')  # We need to mock this too, otherwise a window pops up
    def test_draws_box_on_fire_event(self, mock_imshow, mock_text, mock_rect):
        """
        Test if a red box is drawn when fire metadata is present.
        """
        # Simulate fire data
        event_data = {
            "timestamp": "2026-02-02T14:30:00",
            "confidence": 1.0,
            "box": (10, 10, 50, 50)  # x, y, w, h
        }

        self.ui.update_view(self.frame, event_data=event_data, alert_active=True)

        # Verify rectangle was drawn
        mock_rect.assert_called()
        # Verify text "FIRE DETECTED" or similar was written
        mock_text.assert_called()

    @patch('cv2.waitKey')
    def test_check_input(self, mock_waitkey):
        """
        Test input handling.
        """
        # Simulate user pressing 'q' (ASCII 113)
        mock_waitkey.return_value = ord('q')

        key = self.ui.check_input()
        self.assertEqual(key, ord('q'))