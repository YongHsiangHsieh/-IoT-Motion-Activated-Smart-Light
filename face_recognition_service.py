"""Face recognition service module for comparing and identifying faces."""

import os
import numpy as np
import face_recognition
from datetime import datetime
import config


class FaceRecognitionService:
    """Service for handling face recognition operations."""
    
    def __init__(self, threshold=config.FACE_RECOGNITION_THRESHOLD, min_gap=config.MIN_FACE_DISTANCE_GAP):
        """Initialize the face recognition service.
        
        Args:
            threshold: Threshold for face matching (lower means stricter matching)
            min_gap: Minimum gap between best and second-best match for confident recognition
        """
        self.threshold = threshold
        self.min_gap = min_gap
        self._ensure_registered_dir()
        
    def _ensure_registered_dir(self):
        """Ensure the directory for registered faces exists."""
        if not os.path.exists(config.REGISTERED_FACES_DIR):
            os.makedirs(config.REGISTERED_FACES_DIR)
            print(f"Created directory for registered faces: {config.REGISTERED_FACES_DIR}")
    
    def compare_face_images(self, image1_path, image2_path):
        """Compare two face images and determine if they match.
        
        Args:
            image1_path: Path to the first image
            image2_path: Path to the second image
            
        Returns:
            tuple: (match_result, distance) where match_result is True if faces match, False otherwise,
                  and distance is the calculated distance between faces. Returns (None, None) if face
                  detection fails.
        """
        try:
            img1 = face_recognition.load_image_file(image1_path)
            img2 = face_recognition.load_image_file(image2_path)
            
            # Extract face encodings
            encodings1 = face_recognition.face_encodings(img1)
            encodings2 = face_recognition.face_encodings(img2)
            
            if not encodings1 or not encodings2:
                print("Could not detect a face in one of the images.")
                return None, None
            
            # Get the face encodings
            face1_enc = encodings1[0]
            face2_enc = encodings2[0]
            
            # Calculate distance between faces
            dist = np.linalg.norm(face1_enc - face2_enc)
            match = dist < self.threshold
            
            print(f"Face comparison distance: {dist}")
            print(f"Faces match? {'Yes' if match else 'No'}")
            
            return match, dist
        except Exception as e:
            print(f"Error comparing faces: {e}")
            return None, None
    
    def load_registered_faces(self):
        """Load all registered face encodings and user information.
        
        Returns:
            tuple: (encodings, info) where encodings is a list of face encodings and
                  info is a list of (name, color) tuples
        """
        registered_encodings = []
        registered_info = []  # List of (name, color) tuples
        
        try:
            for filename in os.listdir(config.REGISTERED_FACES_DIR):
                if filename.lower().endswith(('.jpg', '.png')):
                    file_path = os.path.join(config.REGISTERED_FACES_DIR, filename)
                    img = face_recognition.load_image_file(file_path)
                    encodings = face_recognition.face_encodings(img)
                    
                    if encodings:
                        registered_encodings.append(encodings[0])
                        name_color = filename.rsplit('.', 1)[0]
                        if '_' in name_color:
                            parts = name_color.split('_')
                            name = parts[0]
                            color = parts[1]
                        else:
                            name, color = name_color, "white"
                        registered_info.append((name, color))
            
            print(f"Loaded {len(registered_encodings)} registered faces")
            return registered_encodings, registered_info
        except Exception as e:
            print(f"Error loading registered faces: {e}")
            return [], []
    
    def recognize_face(self, face_encoding, registered_encodings, registered_info):
        """Recognize a face against registered faces using the relative distance check algorithm.
        
        Args:
            face_encoding: The face encoding to recognize
            registered_encodings: List of registered face encodings
            registered_info: List of (name, color) tuples for registered faces
            
        Returns:
            tuple: (name, color, distance, gap) if a match is found, (None, None, None, None) otherwise
        """
        if not registered_encodings or not registered_info:
            print("No registered faces to compare against")
            return None, None, None, None
        
        # Calculate distances to all registered faces
        distances = []
        for i, reg_encoding in enumerate(registered_encodings):
            distance = np.linalg.norm(face_encoding - reg_encoding)
            distances.append((registered_info[i], distance))
        
        # Sort by distance (ascending)
        sorted_distances = sorted(distances, key=lambda x: x[1])
        
        # Get the best match
        (best_name, best_color), best_distance = sorted_distances[0]
        
        # Calculate gap between best and second-best match
        if len(sorted_distances) < 2:
            gap = float('inf')  # Only one registered face
        else:
            gap = sorted_distances[1][1] - best_distance
        
        # Apply threshold and gap criteria for confident recognition
        if best_distance < self.threshold and gap >= self.min_gap:
            print(f"Face recognized as {best_name} with favorite color {best_color}")
            print(f"Distance: {best_distance:.2f}, Gap: {gap:.2f}")
            return best_name, best_color, best_distance, gap
        
        print("Face not recognized with sufficient confidence")
        return None, None, None, None
    
    def register_face(self, image_path, name, favorite_color):
        """Register a new face with the given name and favorite color.
        
        Args:
            image_path: Path to the already saved image with the face
            name: Name of the person
            favorite_color: Favorite color of the person
            
        Returns:
            bool: True if registration is successful, False otherwise
        """
        try:
            # Load the image and check if a face is detected
            img = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(img)
            
            if not encodings:
                print("No face detected in the provided image")
                return False

            print(f"Face registered successfully as {name} with favorite color {favorite_color}")
            return True
        except Exception as e:
            print(f"Error registering face: {e}")
            return False
    
    def process_frame(self, frame, registered_encodings, registered_info, threshold=None):
        """Process a video frame for face recognition.
        
        Args:
            frame: The video frame to process
            registered_encodings: List of registered face encodings
            registered_info: List of (name, color) tuples for registered faces
            threshold: Optional threshold to override the default
            
        Returns:
            list: List of tuples containing face locations and recognition results:
                 [(face_location, name, color, distance, gap), ...]
        """
        if threshold is None:
            threshold = self.threshold
            
        results = []
        
        try:
            # Find face locations and encodings in the current frame
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            # Process each detected face
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Try to recognize the face
                name, color, distance, gap = self.recognize_face(
                    face_encoding, 
                    registered_encodings, 
                    registered_info
                )
                
                # Store the result
                results.append(((top, right, bottom, left), name, color, distance, gap))
                
        except Exception as e:
            print(f"Error processing video frame: {e}")
            
        return results 