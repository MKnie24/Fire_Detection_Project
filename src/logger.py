import csv
import os

class EventLogger:
    def __init__(self, filepath="events.csv"):
        self.filepath = filepath
        self.alert_triggered = False

        log_dir = os.path.dirname(filepath)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if not os.path.exists(self.filepath):
            with open(self.filepath, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Message", "Timestamp", "Position (X, Y)", "Size (W x H)"])

    def log_event(self, event_data):
        if not event_data:
            return False

        if self.alert_triggered:
            return False

        try:
            with open(self.filepath, mode='a', newline='') as f:
                writer = csv.writer(f)

                raw_ts = event_data.get('timestamp', '')
                clean_ts = raw_ts.replace('T', ' ').split('.')[0]

                box = event_data.get('box', (0, 0, 0, 0))
                x, y, w, h = box

                pos_str = f"X: {x}, Y: {y}"
                size_str = f"W: {w} x H: {h}"

                writer.writerow(["FIRE DETECTED", clean_ts, pos_str, size_str])

            self.alert_triggered = True
            return True

        except Exception as e:
            print(f"Error logging event: {e}")
            return False

    def reset_alert(self):
        self.alert_triggered = False