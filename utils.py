"""Utility functions for the smart security system."""

import os
from datetime import datetime
import time


def get_timestamp():
    """Get a formatted timestamp string for the current time.
    
    Returns:
        str: Formatted timestamp string (YYYY-MM-DD HH:MM:SS)
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def generate_filename(prefix="", name=None, color=None, directory=".", extension="jpg"):
    """Generate a filename with the current timestamp.
    
    Args:
        prefix: Prefix for the filename (used if name and color are not provided)
        name: Name to include in the filename
        color: Favorite color to include in the filename
        directory: Directory where the file should be saved
        extension: File extension (without the dot)
        
    Returns:
        str: Full path to the generated filename
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if name and color:
        filename = f"{name}_{color}_{timestamp}.{extension}"
    else:
        filename = f"{prefix}_{timestamp}.{extension}"

    return os.path.join(directory, filename)


def safe_delete_file(file_path):
    """Safely delete a file if it exists.
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        bool: True if the file was deleted or didn't exist, False if deletion failed
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
            return True
        return True 
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False


class Timer:
    """Simple timer class for managing timeouts and delays."""
    
    def __init__(self, duration=0):
        """Initialize the timer.
        
        Args:
            duration: Duration in seconds for the timer
        """
        self.duration = duration
        self.start_time = None
    
    def start(self):
        """Start the timer."""
        self.start_time = time.time()
        return self
    
    def elapsed(self):
        """Get the elapsed time since the timer was started.
        
        Returns:
            float: Elapsed time in seconds
        """
        if self.start_time is None:
            return 0
        return time.time() - self.start_time
    
    def remaining(self):
        """Get the remaining time before the timer expires.
        
        Returns:
            float: Remaining time in seconds (0 if timer has expired)
        """
        if self.start_time is None:
            return self.duration
        elapsed = self.elapsed()
        return max(0, self.duration - elapsed)
    
    def has_expired(self):
        """Check if the timer has expired.
        
        Returns:
            bool: True if the timer has expired, False otherwise
        """
        if self.start_time is None:
            return False
        return self.elapsed() >= self.duration
    
    def wait_remaining(self):
        """Wait for the remaining time on the timer."""
        remaining_time = self.remaining()
        if remaining_time > 0:
            time.sleep(remaining_time) 