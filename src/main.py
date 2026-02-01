import cv2
import os
import time
from src.video_input import VideoInput
from src.fire_detector import FireDetector
from src.ui import UserInterface
from src.logger import EventLogger
from src.communicator import RaspberryPiCommunicator

def main():
    print("Fire Detection System")

    source_input = input("Enter URL or 'temp_video.mp4': ").strip()
    if not source_input: return

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_dir, "resources", "logs", "events.csv")
    print(f"Log file: {log_path}")

    video = VideoInput(source=source_input, target_width=640)
    detector = FireDetector()
    ui = UserInterface()
    logger = EventLogger(filepath=log_path)

    communicator = RaspberryPiCommunicator(pi_ip="192.168.137.86")

    if not video.start():
        return

    print("System running. Waiting for fire...")

    while True:
        success, frame = video.get_frame()
        if not success:
            print("Video ended.")
            break

        is_fire = detector.detect(frame)
        event_data = detector.last_event_data

        ui.update_view(frame, event_data=event_data, alert_active=is_fire)

        if is_fire and event_data:
            print("\n!!!FIRE DETECTED - ALARM TRIGGERED!!!")
            print(f"Timestamp: {event_data['timestamp']}")

            logger.log_event(event_data)

            communicator.activate_alarm()

            print("-> Video stopped. Alarm sent to Pi.")
            print("-> Press 'q' to stop alarm and exit.")

            while True:
                key = cv2.waitKey(100) & 0xFF
                if key == ord('q'):
                    print("-> Stopping alarm...")

                    communicator.deactivate_alarm()

                    time.sleep(0.5)

                    print("-> Alarm deactivated. Exiting.")
                    break

            break

        if ui.check_input() == ord('q'):
            break

    video.release()
    ui.close()
    print("Program finished.")

if __name__ == "__main__":
    main()