import unittest
import cv2
import os
from src.fire_detector import FireDetector

class TestFireDetector(unittest.TestCase):

    def setUp(self):
        self.detector = FireDetector()
        self.detector.alarm_delay = 15
        self.video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/videos"))

    def check_video(self, filename):
        full_path = os.path.join(self.video_path, filename)
        if not os.path.exists(full_path):
            self.skipTest(f"Video not found: {filename}")
        cap = cv2.VideoCapture(full_path)
        alarm_triggered = False
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if self.detector.detect(frame):
                alarm_triggered = True
                break
        cap.release()
        return alarm_triggered

    def test_real_fire_should_trigger(self):
        result = self.check_video("fire_video.mp4")
        self.assertTrue(result, "Fire not detected")

    def test_static_lamp_should_ignore(self):
        result = self.check_video("orange_video.mp4")
        self.assertFalse(result, "Fire detected!")

    def test_moving_object_should_ignore(self):
        result = self.check_video("fire_moving_left_to_right_video.mp4")
        self.assertFalse(result, "Fire detected")