"""Configuration settings for the smart security system."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Tuya Bulb configuration
DEVICE_ID = os.getenv('DEVICE_ID', '')
DEVICE_IP = os.getenv('DEVICE_IP', '')
LOCAL_KEY = os.getenv('LOCAL_KEY', '')

# Light and timing thresholds
LIGHT_THRESHOLD = 500  # Below this value, the environment is considered dark
BULB_ON_DURATION = 60  # Duration in seconds to keep the bulb on (1 minute)
FACE_RECOGNITION_DURATION = 30  # Duration in seconds to run face recognition

# Camera settings
CAMERA_RESOLUTION = (640, 480)
CAMERA_ROTATION = 180
CAMERA_WARMUP_TIME = 2  # seconds
CAMERA_FRAMERATE = 30   # frames per second for video

# GPIO pin configurations
PIR_SENSOR_PIN = 5
LED_PIN = 18

# Face recognition settings
FACE_RECOGNITION_THRESHOLD = 0.6
MIN_FACE_DISTANCE_GAP = 0.1

# Directory for registered faces
REGISTERED_FACES_DIR = "registered_faces"

# Blynk IoT configuration
BLYNK_TEMPLATE_ID = os.getenv('BLYNK_TEMPLATE_ID', '')
BLYNK_AUTH_TOKEN = os.getenv('BLYNK_AUTH_TOKEN', '')
BLYNK_SERVER = os.getenv('BLYNK_SERVER', 'blynk.cloud')
BLYNK_PORT = int(os.getenv('BLYNK_PORT', 80))
BLYNK_TEMPLATE_NAME = os.getenv('BLYNK_TEMPLATE_NAME', 'Smart lighting system')

# Blynk virtual pins
BLYNK_LIGHT_STATE_PIN = 0  # V0 - Light state (ON/OFF)
BLYNK_COLOR_PIN = 1        # V1 - Current light color
BLYNK_FACES_PIN = 2        # V2 - Recognized faces
BLYNK_MODE_PIN = 3         # V3 - Mode selection (auto/manual) 

# Supported RGB color values
SUPPORTED_COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "white": (255, 255, 255),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
    "pink": (255, 192, 203)
}