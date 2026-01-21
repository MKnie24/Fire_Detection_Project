import unittest
import os
import numpy as np
from src.video_input import VideoInput


class TestVideoInput(unittest.TestCase):

    def setUp(self):
        # Dynamic path to resources/videos
        test_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(test_dir)
        self.video_path = os.path.join(project_root, "resources", "videos", "test_video.mp4")

        # Check if test video exists, otherwise skip relevant tests
        self.video_exists = os.path.exists(self.video_path)

    def test_init_webcam(self):
        """
        Test if VideoInput initializes correctly with webcam index (int).
        """
        vi = VideoInput(source=0)
        self.assertEqual(vi.source, 0, "Source should be stored as integer 0")

    def test_init_file(self):
        """
        Test if VideoInput initializes correctly with a file path (str).
        """
        vi = VideoInput(source="some/path.mp4")
        self.assertEqual(vi.source, "some/path.mp4", "Source should be stored as string")

    def test_read_frame_from_file(self):
        """
        Integration Test: Open a real video file and read the first frame.
        """
        if not self.video_exists:
            print(f"DEBUG: Missing {self.video_path}")
            self.skipTest("test_video.mp4 not found in resources/videos")

        # Initialize with local file
        video_input = VideoInput(source=self.video_path)

        # Open source
        success = video_input.start()
        self.assertTrue(success, "Failed to open video file")

        # Read one frame
        ret, frame = video_input.get_frame()

        # Verify result
        self.assertTrue(ret, "Return value should be True for a valid frame")
        self.assertIsNotNone(frame, "Frame should not be None")
        self.assertIsInstance(frame, np.ndarray, "Frame should be a numpy array")
        self.assertGreater(frame.size, 0, "Frame should contain data")

        # Cleanup
        video_input.release()

    def test_youtube_url_detection(self):
        """
        Test if the system correctly identifies a YouTube URL.
        Logic: If string starts with 'http' and contains 'youtu', treat as stream.
        """
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        vi = VideoInput(source=url)
        self.assertTrue(vi.is_youtube, "Should identify YouTube URL correctly")

        local = VideoInput(source="my_video.mp4")
        self.assertFalse(local.is_youtube, "Should not identify local file as YouTube")