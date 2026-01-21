import unittest
import cv2
import numpy as np
import os
from src.fire_detector import FireDetector


class TestFireDetector(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment.
        This method runs before every single test method.
        """
        self.detector = FireDetector()

        # --- PATH FIX ---
        # 1. Get the folder where THIS test file is located (.../test)
        test_dir = os.path.dirname(os.path.abspath(__file__))

        # 2. Go up one level to get the Project Root (.../Fire_Detection_Projekt)
        self.project_root = os.path.dirname(test_dir)

        # 3. Define the path to the images folder safely
        self.images_dir = os.path.join(self.project_root, "resources", "images")

    def test_initialization(self):
        """
        Test if the detector initializes correctly.
        """
        self.assertIsNotNone(self.detector, "Detector instance should not be None")
        self.assertIsNone(self.detector.last_event_data, "Metadata should be None on init")

    def test_detect_raises_error_on_none_input(self):
        """
        Requirement: System must handle invalid input gracefully.
        Expectation: Raises ValueError if the input frame is None.
        """
        with self.assertRaises(ValueError):
            self.detector.detect(None)

    def test_detect_returns_false_for_black_image(self):
        """
        Requirement: No fire should be detected in a completely dark scene.
        Expectation: Returns False.
        """
        # Create a black image (480x640 resolution, 3 color channels)
        black_frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Act
        result = self.detector.detect(black_frame)

        # Assert
        self.assertFalse(result, "Error: Fire detected in a purely black image")
        self.assertIsNone(self.detector.last_event_data, "Metadata should be empty if no fire detected")

    def test_detect_returns_true_for_synthetic_fire(self):
        """
        Requirement: Fire (simulated by orange color) must be detected.
        Expectation: Returns True and populates metadata.
        """
        # Arrange: Create a black frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Draw a solid orange rectangle to simulate fire
        # OpenCV uses BGR format. Orange is roughly (Blue=0, Green=165, Red=255)
        cv2.rectangle(frame, (100, 100), (200, 200), (0, 165, 255), -1)

        # Act
        result = self.detector.detect(frame)

        # Assert (Logic)
        self.assertTrue(result, "Error: Synthetic fire (orange rect) was not detected")

        # Assert (Metadata presence)
        metadata = self.detector.last_event_data
        self.assertIsNotNone(metadata, "Error: Metadata dictionary is missing")
        self.assertIn("timestamp", metadata)
        self.assertIn("confidence", metadata)
        self.assertIn("box", metadata)

    def test_real_image_negative_forest(self):
        """
        Integration Test: Check against a real image of a forest (NO FIRE).
        Expectation: Returns False.
        """
        # Construct the absolute path to the image
        image_path = os.path.join(self.images_dir, "forest.png")

        # Debug: Print path if test fails
        if not os.path.exists(image_path):
            print(f"DEBUG: Looking for image at: {image_path}")
            self.fail(f"Test image not found! Please place 'forest.png' in {self.images_dir}")

        # Load image
        frame = cv2.imread(image_path)
        if frame is None:
            self.fail(f"Failed to load image from {image_path}. Format might be invalid.")

        # Act
        result = self.detector.detect(frame)

        # Assert
        self.assertFalse(result, "Error: False Positive! Fire detected in a normal forest image.")

    def test_real_image_positive_fire(self):
        """
        Integration Test: Check against a real image of a burning forest (FIRE).
        Expectation: Returns True.
        """
        image_path = os.path.join(self.images_dir, "fire.png")

        if not os.path.exists(image_path):
            print(f"DEBUG: Looking for image at: {image_path}")
            self.fail(f"Test image not found! Please place 'fire.png' in {self.images_dir}")

        frame = cv2.imread(image_path)
        if frame is None:
            self.fail(f"Failed to load image from {image_path}. Format might be invalid.")

        # Act
        result = self.detector.detect(frame)

        # Assert
        self.assertTrue(result, "Error: False Negative! Real fire was not detected.")