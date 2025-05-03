"""
Smart Security System Main Module

This is the main entry point for the smart security system that:
1. Detects motion using a PIR sensor
2. Measures ambient light using an ADC sensor
3. Turns on a smart bulb when motion is detected in dark conditions
4. Performs face recognition during detection
5. Changes bulb color based on recognized users' preferences
6. Connects to Blynk IoT cloud for remote monitoring and control
"""

import time
import sys
import signal
from security_system import SecuritySystem

# Global variable for the security system instance
security_system = None

def signal_handler(sig, frame):
    """Handle SIGINT (Ctrl+C) to gracefully stop the security system."""
    print("\nShutting down the security system...")
    if security_system:
        security_system.stop()
    sys.exit(0)

def main():
    """Main function to initialize and start the security system."""
    global security_system
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Display welcome message
    print("=" * 60)
    print("Smart Security System")
    print("Motion-activated lighting with facial recognition")
    print("Connected to Blynk IoT cloud platform")
    print("=" * 60)
    
    try:
        # Create and start the security system
        security_system = SecuritySystem()
        security_system.start()
        
        # Keep the main thread running
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        if security_system:
            security_system.stop()

if __name__ == "__main__":
    main()