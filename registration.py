"""
Face Registration Utility

This script allows users to register their faces and favorite colors in the security system.
It captures a photo of the user and saves it with their name and color preference for 
later recognition by the security system.
"""

import time
import sys
import config
from camera_manager import CameraManager
from face_recognition_service import FaceRecognitionService
from utils import generate_filename


def main():
    """Main function to handle user registration."""
    # Display welcome message
    print("=" * 60)
    print("Face Registration Utility")
    print("Register your face for the smart security system")
    print("=" * 60)
    
    # Initialize components
    camera = CameraManager()
    face_service = FaceRecognitionService()
    
    try:
        # Initialize camera
        if not camera.initialize():
            print("Failed to initialize camera. Registration cannot proceed.")
            return
        
        # Get user information
        name = input("Enter your name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        
        favorite_color = input("Enter your favorite color: ").strip().lower()
        valid_colors = ["red", "green", "blue", "yellow", "cyan", "magenta", 
                      "white", "purple", "orange", "pink"]
        
        if not favorite_color:
            print("Color cannot be empty.")
            return
        
        if favorite_color not in valid_colors:
            print(f"Warning: '{favorite_color}' is not in the list of recognized colors: {', '.join(valid_colors)}")
            print("The system will use this color but it may default to blue if not recognized.")
            confirm = input("Continue with this color? (y/n): ").strip().lower()
            if confirm != 'y':
                return
        
        # Capture user's face
        print("\nPreparing to capture your face...")
        print("Position yourself in front of the camera.")
        
        # Countdown
        for i in range(3, 0, -1):
            print(f"Taking photo in {i}...")
            time.sleep(1)
        
        # Capture the image
        image_path = generate_filename(f"registration")
        if not camera.capture_image(image_path):
            print("Failed to capture image. Registration cannot proceed.")
            return
        
        # Register face
        success = face_service.register_face(image_path, name, favorite_color)
        
        if success:
            print("\n✅ Registration successful!")
            print(f"Welcome {name}! Your favorite color ({favorite_color}) has been saved.")
            print("The system will now recognize you and set the light to your favorite color.")
        else:
            print("\n❌ Registration failed.")
            print("Please try again, ensuring your face is clearly visible to the camera.")
    
    except KeyboardInterrupt:
        print("\nRegistration canceled.")
    except Exception as e:
        print(f"\nError during registration: {e}")
    finally:
        # Clean up
        camera.close()
        print("\nThank you for using the registration utility.")


if __name__ == "__main__":
    main() 