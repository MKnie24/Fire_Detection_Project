import unittest
import os
import csv
from src.logger import EventLogger


class TestEventLogger(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_events.csv"
        self.logger = EventLogger(filepath=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_file_creation_and_logging(self):
        event_data = {
            "timestamp": "2026-01-20T12:00:00",
            "box": (10, 20, 100, 200)
        }

        self.logger.log_event(event_data)

        self.assertTrue(os.path.exists(self.test_file), "Log file was not created")

        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn("FIRE DETECTED", content)
            self.assertIn("2026-01-20 12:00:00", content)
            self.assertIn("X: 10, Y: 20", content)

    def test_avoid_duplicate_logging(self):
        event_data = {"timestamp": "12:00:01", "box": (0, 0, 0, 0)}
        logged_1 = self.logger.log_event(event_data)
        self.assertTrue(logged_1)
        logged_2 = self.logger.log_event(event_data)
        self.assertFalse(logged_2)