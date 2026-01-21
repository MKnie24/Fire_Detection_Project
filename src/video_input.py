import cv2
import yt_dlp


class VideoInput:
    """
    Handles video acquisition from various sources:
    1. Local Video Files
    2. Live Webcams
    3. YouTube URLs (via yt-dlp)
    """

    def __init__(self, source=0):
        """
        Initialize the video input.

        Args:
            source: 
                - int: Camera index (e.g., 0 for default webcam).
                - str: File path to a video file OR a YouTube URL.
        """
        self.source = source
        self.cap = None
        self.is_youtube = False

        # Check if source is a YouTube URL
        if isinstance(self.source, str):
            if "youtube.com" in self.source or "youtu.be" in self.source:
                self.is_youtube = True

    def start(self) -> bool:
        """
        Opens the video source.

        Returns:
            bool: True if source opened successfully, False otherwise.
        """
        input_source = self.source

        # Handle YouTube URLs using yt-dlp to get the direct stream URL
        if self.is_youtube:
            try:
                ydl_opts = {
                    'format': 'best[ext=mp4]/best',  # Get best quality mp4
                    'quiet': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(self.source, download=False)
                    input_source = info['url']  # The actual stream URL for OpenCV
            except Exception as e:
                print(f"Error extracting YouTube stream: {e}")
                return False

        # Initialize OpenCV VideoCapture
        self.cap = cv2.VideoCapture(input_source)

        if not self.cap.isOpened():
            print(f"Error: Could not open video source {self.source}")
            return False

        return True

    def get_frame(self):
        """
        Reads the next frame from the video source.

        Returns:
            tuple: (ret, frame)
                - ret (bool): True if frame is valid, False otherwise (end of video/error).
                - frame (numpy.ndarray): The image data.
        """
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            return ret, frame
        return False, None

    def release(self):
        """
        Releases the video resource.
        """
        if self.cap:
            self.cap.release()