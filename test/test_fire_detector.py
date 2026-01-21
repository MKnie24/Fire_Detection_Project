import unittest
import cv2
import numpy as np
from src.fire_detector import FireDetector


class TestFireDetector(unittest.TestCase):

    def setUp(self):
        self.detector = FireDetector()

    def test_error_raised_when_frame_is_none(self):
        # Expect a ValueError if the input is None
        with self.assertRaises(ValueError):
            self.detector.detect(None)

    def test_return_false_for_black_image(self):
        # Scenario: Black image -> No fire
        black_frame = np.zeros((480, 640, 3), dtype=np.uint8)

        result = self.detector.detect(black_frame)

        # Check explicitly for False (Boolean)
        self.assertFalse(result, "Fail: Expected False for black image")

    def test_return_true_for_fire_image(self):
        # Scenario: Orange rectangle -> Fire detected
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Draw orange rectangle (BGR: 0, 165, 255)
        cv2.rectangle(frame, (100, 100), (200, 200), (0, 165, 255), -1)

        result = self.detector.detect(frame)

        # Check explicitly for True (Boolean)
        self.assertTrue(result, "Fail: Expected True for orange image")

        # Verify that metadata was stored internally (needed for Logging module later)
        self.assertIsNotNone(self.detector.last_event_data, "Fail: Metadata not stored")
        self.assertIn('box', self.detector.last_event_data)