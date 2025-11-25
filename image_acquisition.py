# src/image_acquisition.py
import cv2
import numpy as np

class ImageCapture:
    def __init__(self):
        self.camera = None
    
    def initialize_camera(self, camera_id=0):
        """Initialize camera for live capture"""
        self.camera = cv2.VideoCapture(camera_id)
        return self.camera.isOpened()
    
    def capture_frame(self):
        """Capture single frame from camera"""
        if self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return frame
        return None
    
    def capture_multiple_frames(self, count=5):
        """Capture multiple frames for analysis"""
        frames = []
        for _ in range(count):
            frame = self.capture_frame()
            if frame is not None:
                frames.append(frame)
        return frames
    
    def release_camera(self):
        """Release camera resources"""
        if self.camera:
            self.camera.release()
    
    def load_image(self, image_path):
        """Load image from file path"""
        try:
            image = cv2.imread(image_path)
            if image is not None:
                return image
            return None
        except Exception as e:
            print(f"Error loading image: {e}")
            return None