"""Smart security system orchestrator module."""

import os
import time
import threading
from datetime import datetime
import face_recognition
import config
from sensors import MotionSensor, LightSensor, IndicatorLED
from camera_manager import CameraManager
from smart_bulb import SmartBulb
from face_recognition_service import FaceRecognitionService
from utils import Timer, generate_filename, safe_delete_file, get_timestamp
from blynk_service import BlynkService


class SecuritySystem:
    """Smart security system that integrates motion detection, lighting control, and face recognition."""
    
    def __init__(self):
        """Initialize the security system components."""
        # Initialize counters and state
        self.motion_count = 0
        self.running = False
        self.lock = threading.Lock()  # For thread safety
        
        # Initialize components
        self.motion_sensor = MotionSensor()
        self.light_sensor = LightSensor()
        self.led = IndicatorLED()
        self.camera = CameraManager()
        self.bulb = SmartBulb()
        self.face_service = FaceRecognitionService()
        self.blynk_service = BlynkService()
        
        # Preload registered faces
        self._preload_registered_faces()
    
    def _preload_registered_faces(self):
        """Preload registered faces to avoid loading them each time motion is detected."""
        self.registered_encodings, self.registered_info = self.face_service.load_registered_faces()
        print(f"Preloaded {len(self.registered_encodings)} registered faces")
    
    def start(self):
        """Start the security system and begin monitoring for motion."""
        if self.running:
            print("Security system is already running")
            return
        
        # Initialize camera
        if not self.camera.initialize():
            print("Failed to initialize camera. Security system will not start.")
            return
        
        # Set up motion sensor callback
        self.motion_sensor.set_callback(self._handle_motion)
        
        # Start Blynk service
        self.blynk_service.start()
        
        self.running = True
        print("🟢 Security system is active and monitoring for motion...")
    
    def stop(self):
        """Stop the security system and release resources."""
        self.running = False
        self.camera.close()
        self.blynk_service.stop()
        print("Security system has been stopped.")
    
    def _handle_motion(self):
        """Handle motion detection event.
        
        This method is called when the motion sensor detects motion. It performs
        the following steps:
        1. Checks if the environment is dark
        2. If dark, turns on the smart bulb
        3. Activates face recognition for 30 seconds
        4. Changes bulb color based on recognized person's preference
        5. Turns off the bulb after 2 minutes
        """
        # Check if we're in manual mode from Blynk
        if self.blynk_service.get_operation_mode() == "manual":
            print("System in manual mode - ignoring motion detection")
            return
        
        # Avoid race conditions with multiple detections
        with self.lock:
            self.motion_count += 1
            count = self.motion_count  # Store current count for this detection
            
            now = get_timestamp()
            print(f"\n[{now}] 🚨 Motion detected! Total count: {count}")
            
            # Check light level
            light_level = self.light_sensor.get_light_level()
            print(f"Current light level: {light_level}")
            
            # Only proceed if environment is dark
            if not self.light_sensor.is_dark():
                print("Bright environment detected. No action needed.")
                return
                
            print("Dark environment detected. Activating security response...")
            
            # Turn on the bulb with default color
            if not self.bulb.connect():
                print("Failed to connect to smart bulb. Aborting security response.")
                return
                
            self.bulb.turn_on()
            self.bulb.set_default_color()
            
            # Update Blynk with light state
            self.blynk_service.update_light_state(True, "default")
            
            # Create timers for face recognition and bulb control
            face_recog_timer = Timer(config.FACE_RECOGNITION_DURATION).start()
            bulb_timer = Timer(config.BULB_ON_DURATION).start()
            
            # Start face recognition thread
            face_thread = threading.Thread(
                target=self._run_face_recognition, 
                args=(count, face_recog_timer, bulb_timer)
            )
            face_thread.daemon = True
            face_thread.start()
            
            # Wait for the bulb timer in the main thread
            while not bulb_timer.has_expired() and self.running:
                time.sleep(1)
                
            # Turn off the bulb after the specified duration
            print(f"[{get_timestamp()}] Turning off bulb after {config.BULB_ON_DURATION} seconds")
            self.bulb.turn_off()
            
            # Update Blynk with light state
            self.blynk_service.update_light_state(False, "none")
    
    def _run_face_recognition(self, count, face_timer, bulb_timer):
        """Run face recognition for the specified duration.
        
        Args:
            count: The motion detection count for this event
            face_timer: Timer for face recognition duration
            bulb_timer: Timer for bulb on duration (to set color when face is recognized)
        """
        print(f"[{get_timestamp()}] Starting face recognition for {config.FACE_RECOGNITION_DURATION} seconds")
        
        # Reload registered faces to ensure we have the latest
        if count % 10 == 0:  # Reload every 10 detections to avoid constant reloading
            self._preload_registered_faces()
        
        recognized_face = False
        recognized_color = None
        
        # Get the video stream from the camera
        video_stream = self.camera.get_video_stream()
        if not video_stream:
            print("Failed to start video stream for face recognition")
            return
            
        camera, rawCapture = video_stream
        
        # Signal with LED for video stream starting
        self.led.on()
        
        try:
            # Process video frames until timer expires or a face is recognized
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # Check if time is up
                if face_timer.has_expired() or not self.running or bulb_timer.has_expired():
                    break
                    
                # Get the array from the frame
                image = frame.array
                
                # Process the frame to recognize faces
                results = self.face_service.process_frame(
                    image, 
                    self.registered_encodings, 
                    self.registered_info
                )
                
                # Filter strong matches only (name is recognized and distance is below threshold)
                strong_matches = [r for r in results if r[1] and r[3] < config.FACE_RECOGNITION_THRESHOLD]

                if strong_matches:
                    # Choose the best (most confident) match among strong ones
                    best_match = min(strong_matches, key=lambda r: r[3])
                    (top, right, bottom, left), name, color, distance, gap = best_match
                    recognized_face = True
                    recognized_color = color
                    print(f"[{get_timestamp()}] Recognized {name}! Setting bulb to favorite color: {color}")

                    # Try to parse the color and set the bulb
                    self._set_bulb_color(color)

                    # Update Blynk with the recognized face and color
                    self.blynk_service.add_recognized_face(name)
                    self.blynk_service.update_light_state(True, color)

                    # Exit the video loop if we recognized someone
                    break
                    
                # Clear the stream for the next frame
                rawCapture.truncate(0)
                rawCapture.seek(0)
                
                # Brief delay between frames
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error during video face recognition: {e}")
            
        finally:
            # Turn off the LED
            self.led.off()
        
        if not recognized_face and self.running and not bulb_timer.has_expired():
            print(f"[{get_timestamp()}] No face recognized during the detection period")
            # Set the bulb to red if no face was recognized
            self.bulb.set_color(255, 0, 0)  # Red
            self.blynk_service.update_light_state(True, "red")
            
        print(f"[{get_timestamp()}] Face recognition completed for motion #{count}")
    
    def _set_bulb_color(self, color_name):
        """Set the bulb color based on a color name.
        
        Args:
            color_name: Name of the color to set
        """
        # Use the centralized color mapping from config
        color = config.SUPPORTED_COLORS.get(color_name.lower(), (100, 100, 100))
        self.bulb.set_color(*color)