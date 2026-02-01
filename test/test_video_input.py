import unittest
import os
import numpy as np
from src.video_input import VideoInput


class TestVideoInput(unittest.TestCase):

    def setUp(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(test_dir)
        self.video_path = os.path.join(project_root, "resources", "videos", "fire_video.mp4")
        self.video_exists = os.path.exists(self.video_path)

    def test_init_raises_error_on_int(self):
        with self.assertRaises(ValueError):
            VideoInput(source=0)

    def test_init_file(self):
        vi = VideoInput(source="some/path.mp4")
        self.assertEqual(vi.source, "some/path.mp4")
        self.assertFalse(vi.is_url, "Local Path must not be URL")

    def test_url_detection(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        vi = VideoInput(source=url)
        self.assertTrue(vi.is_url, "Link must be URL")

        local = VideoInput(source="my_video.mp4")
        self.assertFalse(local.is_url, "Not a URL")

    def test_resizing(self):
        if not self.video_exists:
            self.skipTest("fire_video.mp4 not found")

        target_w = 100
        vi = VideoInput(source=self.video_path, target_width=target_w)

        vi.start()

        ret, frame = vi.get_frame()
        vi.release()

        self.assertTrue(ret, "Frame not readable")
        self.assertEqual(frame.shape[1], target_w, f"Frame width should be {target_w}")