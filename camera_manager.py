"""Camera management module for the Raspberry Pi Camera."""

import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import config


class CameraManager:
    """Class to manage PiCamera operations."""
    
    def __init__(self, resolution=config.CAMERA_RESOLUTION, rotation=config.CAMERA_ROTATION, framerate=config.CAMERA_FRAMERATE):
        """Initialize the camera with specified settings.
        
        Args:
            resolution: Camera resolution as (width, height) tuple
            rotation: Camera rotation in degrees
            framerate: Camera frame rate for video
        """
        self.camera = None
        self.resolution = resolution
        self.rotation = rotation
        self.framerate = framerate
        self.is_initialized = False
    
    def initialize(self):
        """Initialize the camera and get it ready for capturing.
        
        Returns:
            bool: True if initialization is successful, False otherwise
        """
        if self.is_initialized:
            return True
            
        try:
            self.camera = PiCamera()
            self.camera.resolution = self.resolution
            self.camera.rotation = self.rotation
            self.camera.framerate = self.framerate
            print("Camera initialized. Warming up...")
            time.sleep(config.CAMERA_WARMUP_TIME)
            self.is_initialized = True
            return True
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def capture_image(self, filename):
        """Capture an image and save it to the specified filename.
        
        Args:
            filename: Name of the file to save the image
            
        Returns:
            bool: True if capture is successful, False otherwise
        """
        if not self.is_initialized and not self.initialize():
            return False
            
        try:
            self.camera.capture(filename)
            print(f"Image captured and saved as {filename}")
            return True
        except Exception as e:
            print(f"Error capturing image: {e}")
            return False
    
    def get_video_stream(self):
        """Get a video stream from the camera.
        
        Returns:
            tuple: (camera, rawCapture) objects for video streaming
            None: If initialization fails
        """
        if not self.is_initialized and not self.initialize():
            return None
            
        try:
            # Initialize the array for holding the frames
            rawCapture = PiRGBArray(self.camera, size=self.resolution)
            # Allow the camera to warmup
            time.sleep(config.CAMERA_WARMUP_TIME)
            return self.camera, rawCapture
        except Exception as e:
            print(f"Error setting up video stream: {e}")
            return None
    
    def close(self):
        """Close the camera and release resources."""
        if not self.is_initialized:
            return
            
        try:
            self.camera.close()
            self.is_initialized = False
            print("Camera closed.")
        except Exception as e:
            print(f"Error closing camera: {e}") 