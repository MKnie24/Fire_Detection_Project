import cv2
import numpy as np
from datetime import datetime


class FireDetector:
    def __init__(self):
        # HSV threshold settings for fire detection
        # Lower bound (covers reddish/orange colors)
        self.lower_fire = np.array([0, 100, 100], dtype=np.uint8)
        # Upper bound (covers up to yellow)
        self.upper_fire = np.array([35, 255, 255], dtype=np.uint8)

        # Minimum contour area to filters noise
        self.min_area = 500

        # Storage for the last detected event metadata (required for Logging Module)
        self.last_event_data = None

    def detect(self, frame) -> bool:
        """
        Processes the frame to detect fire.
        Returns:
            True if fire is detected (Signal HIGH).
            False if no fire is detected (Signal LOW).
        Raises:
            ValueError if frame is None.
        """
        # Raise Error if input is invalid (as requested)
        if frame is None:
            raise ValueError("Input frame cannot be None")

        # Reset last event data
        self.last_event_data = None

        # 1. Apply Gaussian Blur
        blurred = cv2.GaussianBlur(frame, (21, 21), 0)

        # 2. Convert BGR to HSV
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # 3. Create mask
        mask = cv2.inRange(hsv, self.lower_fire, self.upper_fire)

        # 4. Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            if cv2.contourArea(largest_contour) > self.min_area:
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Save metadata internally for other modules (Logger/UI)
                self.last_event_data = {
                    "timestamp": datetime.now().isoformat(),
                    "confidence": 1.0,
                    "box": (x, y, w, h)
                }

                # Return True (Signal HIGH for Raspberry Pi)
                return True

        # Return False (Signal LOW)
        return False