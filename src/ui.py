import cv2


class UserInterface:
    """
    Manages the graphical user interface using OpenCV HighGUI.
    Responsibilities:
    - Display video feed.
    - Overlay detection visualizations (bounding boxes).
    - Show system status (e.g., Alert Active).
    - Handle user input (quit, deactivate alarm).
    """

    def __init__(self):
        self.window_name = "Fire Detection System"

    def update_view(self, frame, event_data=None, alert_active=False):
        """
        Updates the UI window with the current frame and overlays.

        Args:
            frame: The current video frame.
            event_data: Metadata of detected event (or None).
            alert_active: Bool indicating if the buzzer is currently sounding.
        """
        # Work on a copy to avoid modifying the original frame buffer
        display_frame = frame.copy()

        # 1. Visualizing Detection (if any)
        if event_data and 'box' in event_data:
            x, y, w, h = event_data['box']

            # Draw bounding box (Color: Blue in BGR, Thickness: 2)
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Draw label above the box
            label = f"FIRE {event_data.get('confidence', 0.0):.1f}"
            cv2.putText(display_frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # 2. Visualizing System Status (Top Left Corner)
        if alert_active:
            status_text = "STATUS: ALARM ACTIVE"
            color = (0, 0, 255)  # Red
        else:
            status_text = "STATUS: MONITORING"
            color = (0, 255, 0)  # Green

        cv2.putText(display_frame, status_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Instructions for the user
        cv2.putText(display_frame, "Press 'd' to stop alarm | 'q' to quit", (10, 460),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # 3. Show the frame
        cv2.imshow(self.window_name, display_frame)

    def check_input(self):
        """
        Checks for keyboard input.
        Returns:
            int: The ASCII code of the pressed key (or -1 if none).
        """
        # waitKey(1) waits 1ms for a key press
        return cv2.waitKey(1) & 0xFF

    def close(self):
        """
        Closes all UI windows.
        """
        cv2.destroyAllWindows()