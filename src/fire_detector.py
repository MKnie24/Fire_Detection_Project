import cv2
import numpy as np
from datetime import datetime


class FireDetector:
    """
    Implements fire detection using OpenCV based on HSV color segmentation.

    This module is responsible for:
    1. Processing video frames.
    2. Detecting fire based on color thresholds.
    3. generating metadata for logging.
    4. Returning a boolean status for the alert system.
    """

    def __init__(self):
        """
        Initializes the FireDetector with strict HSV thresholds to avoid false positives
        on reddish-brown objects like tree trunks.
        """
        # HSV Thresholds
        # Hue: 0-35 (Red to Yellow) - stays the same

        # Saturation: 150 (Increased from 120)
        # Why? Tree bark is brownish (low/medium saturation). Fire is vivid (high saturation).
        # This filters out "dull" colors.

        # Value: 180 (Increased from 70)
        # Why? This is the most important change for your forest image.
        # Fire emits light (it is very bright). Tree trunks in the shade are dark.
        # A value of 180 ignores almost all shadows and darker objects.
        self.lower_fire = np.array([0, 150, 180], dtype=np.uint8)

        # Upper bound (White/Yellow hot)
        self.upper_fire = np.array([35, 255, 255], dtype=np.uint8)

        # Minimum area
        # We keep this high to ignore small sun-speckles on leaves
        self.min_area = 1000

        self.last_event_data = None

    def detect(self, frame) -> bool:
        # ... (Input Validierung bleibt gleich) ...
        if frame is None:
            raise ValueError("Input frame cannot be None. Check video source.")

        self.last_event_data = None

        # ... (Blur und HSV bleiben gleich) ...
        blurred = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_fire, self.upper_fire)

        # --- DEBUG START (Neu!) ---
        # Wir speichern das Bild, das der Computer "sieht".
        # Alles was weiß ist, hält er für Feuer.
        cv2.imwrite("debug_mask.jpg", mask)
        # --- DEBUG END ---

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            current_area = cv2.contourArea(largest_contour)

            # --- DEBUG PRINT (Neu!) ---
            # Das zeigt uns in der Konsole, wie groß die erkannte Fläche ist.
            print(f"DEBUG: Gefundene Fläche im Bild: {current_area} Pixel")

            if current_area > self.min_area:
                x, y, w, h = cv2.boundingRect(largest_contour)
                self.last_event_data = {
                    "timestamp": datetime.now().isoformat(),
                    "confidence": 1.0,
                    "box": (x, y, w, h)
                }
                return True

        return False