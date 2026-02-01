import cv2


class UserInterface:
    def __init__(self):
        self.window_name = "Fire Detection System"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 640, 480)
        try:
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 1)
        except:
            pass

    def update_view(self, frame, event_data=None, alert_active=False):
        if frame is None: return

        display_frame = frame.copy()

        if event_data and 'box' in event_data:
            x, y, w, h = event_data['box']
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

            label = "FIRE DETECTED"
            cv2.putText(display_frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4)  # Schwarz dick
            cv2.putText(display_frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)  # Rot dünn

        if alert_active:
            status = "ALARM ACTIVE!"
            color = (0, 0, 255)
        else:
            status = "MONITORING"
            color = (0, 255, 0)

        cv2.putText(display_frame, status, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow(self.window_name, display_frame)

    def check_input(self):
        return cv2.waitKey(30) & 0xFF

    def close(self):
        cv2.destroyAllWindows()