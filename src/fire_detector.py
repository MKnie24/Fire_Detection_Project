import cv2
import numpy as np
import math
from datetime import datetime


class FireDetector:
    def __init__(self):

        self.min_area = 100  # area detection
        self.alarm_delay = 15  # sensitivity
        self.max_wandering_distance = 40  # movement tolerance
        self.static_threshold = 0.05  # 5% variance

        self.streak = 0
        self.start_pos = None
        self.area_history = []
        self.last_event_data = None

    def detect(self, frame) -> bool:
        if frame is None: return False
        self.last_event_data = None
        mask = self.isolate_fire_pixels(frame)
        box, area = self.find_largest_object(mask)
        return self.analyze_persistence(box, area)

    def isolate_fire_pixels(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)

        lower = np.array([0, 140, 180], dtype=np.uint8)
        upper = np.array([35, 255, 255], dtype=np.uint8)

        if brightness > 130:
            lower = np.array([0, 170, 220], dtype=np.uint8)

        elif brightness < 80:
            lower = np.array([0, 80, 150], dtype=np.uint8)

        blurred = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.erode(mask, None, iterations=1)

        return mask

    def find_largest_object(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours: return None, 0

        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area < self.min_area: return None, 0
        return cv2.boundingRect(largest), area

    def analyze_persistence(self, box, area):
        if box is None:
            self.decay_streak()
            return False

        if self.streak == 0:
            self.source_tracking(box)
            return False

        if self.source_is_moving(box):
            self.streak_full_reset()
            return False
        if self.source_is_static(area):
            return False
        return self.increment_streak(box)

    def source_is_moving(self, box):
        x, y, w, h = box
        cx, cy = x + w // 2, y + h // 2
        dist = math.hypot(cx - self.start_pos[0], cy - self.start_pos[1])
        return dist > self.max_wandering_distance

    def source_is_static(self, area):
        self.area_history.append(area)
        if len(self.area_history) > 10: self.area_history.pop(0)
        if len(self.area_history) < 5: return False
        min_a = min(self.area_history)
        max_a = max(self.area_history)
        avg = sum(self.area_history) / len(self.area_history)
        if avg == 0: return False
        relative_change = (max_a - min_a) / avg
        return relative_change < self.static_threshold

    def increment_streak(self, box):
        self.streak += 1
        if self.streak >= self.alarm_delay:
            self.last_event_data = {
                "timestamp": datetime.now().isoformat(),
                "box": box
            }
            return True
        return False

    def source_tracking(self, box):
        x, y, w, h = box
        self.start_pos = (x + w // 2, y + h // 2)
        self.area_history = []
        self.streak = 1

    def decay_streak(self):
        if self.streak > 0:
            self.streak -= 2
        else:
            self.streak_full_reset()

    def streak_full_reset(self):
        self.streak = 0
        self.start_pos = None
        self.area_history = []