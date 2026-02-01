import cv2
import yt_dlp
import os


class VideoInput:
    def __init__(self, source: str, target_width=None):
        if not isinstance(source, str):
            raise ValueError("VideoInput source must be a string (filepath or URL).")

        self.source = source
        self.target_width = target_width
        self.cap = None
        self.is_url = "http" in source or "www." in source

    def start(self) -> bool:
        video_path = self.source

        if self.is_url:
            print(f"URL accepted")
            video_path = self._download_video_smart(self.source)
            if not video_path:
                return False
            print(f"Try opening: {video_path}")

        video_path = os.path.abspath(video_path)

        if not os.path.exists(video_path):
            print(f"ERROR: Doesnt exist: {video_path}")
            return False

        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            print(f"FEHLER: OpenCV could not load data: {video_path}")
            return False

        return True

    def _download_video_smart(self, url):
        filename = "temp_video.mp4"
        info_file = "temp_video_url.txt"

        if os.path.exists(filename) and os.path.exists(info_file):
            with open(info_file, "r") as f:
                last_url = f.read().strip()
            if last_url == url:
                print("-> Video already downloaded.")
                return filename
            else:
                try:
                    os.remove(filename)
                except:
                    pass

        print("-> starting download...")
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': filename,
            'quiet': False,
            'overwrites': True,
            'ignoreerrors': True,
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                with open(info_file, "w") as f:
                    f.write(url)
                return filename
            else:
                print("ERROR: Download is empty.")
                return None
        except Exception as e:
            print(f"Download Exception: {e}")
            return None

    def get_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                return False, None

            if self.target_width:
                h, w = frame.shape[:2]
                aspect_ratio = self.target_width / w
                new_h = int(h * aspect_ratio)
                frame = cv2.resize(frame, (self.target_width, new_h))

            return True, frame

        return False, None

    def release(self):
        if self.cap:
            self.cap.release()