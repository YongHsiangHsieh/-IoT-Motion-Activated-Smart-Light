"""Blynk IoT cloud platform integration service using BlynkLib."""

import BlynkLib
import threading
import time
import config


class BlynkService:
    """Service to manage communication with Blynk IoT platform."""
    
    def __init__(self, auth_token=None):
        """Initialize the Blynk service.
        
        Args:
            auth_token: Authentication token for Blynk (defaults to config value)
        """
        self.auth_token = auth_token or config.BLYNK_AUTH_TOKEN
        self.blynk = None
        self.running = False
        self.thread = None
        self.mode = "auto"  # Default mode is auto
        
        # Track the most recent recognized face
        self.latest_face = None  # Tuple of (name, timestamp)
        
        # Current light state
        self.light_state = {
            "power": False,  # True for on, False for off
            "color": "none",  # Current color name
        }
    
    def start(self):
        """Start the Blynk service in a separate thread."""
        if self.running:
            print("Blynk service is already running")
            return False
        
        try:
            # Initialize Blynk with auth token
            print(f"Connecting to Blynk using auth token: {self.auth_token}")
            self.blynk = BlynkLib.Blynk(self.auth_token)
            
            # Register handler for mode control (V3)
            @self.blynk.on("V" + str(config.BLYNK_MODE_PIN))
            def handle_mode_write(value):
                self._mode_write_handler(value)
            
            # Start the Blynk thread
            self.running = True
            self.thread = threading.Thread(target=self._blynk_thread)
            self.thread.daemon = True
            self.thread.start()
            print("🔵 Blynk service started successfully")
            return True
        except Exception as e:
            print(f"Failed to start Blynk service: {e}")
            import traceback
            traceback.print_exc()
            self.running = False
            return False
    
    def stop(self):
        """Stop the Blynk service."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        print("Blynk service stopped")
    
    def _blynk_thread(self):
        """Thread function to run Blynk event loop and update dashboard."""
        print("Blynk thread started")
        update_interval = 2  # Update every 2 seconds
        
        try:
            while self.running:
                # Run Blynk event processing
                self.blynk.run()
                
                # Update dashboard
                self._update_dashboard()
                
                # Short delay to avoid high CPU usage
                time.sleep(update_interval)
        except Exception as e:
            print(f"Error in Blynk thread: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_dashboard(self):
        """Update the Blynk dashboard with current system state."""
        try:
            # Update light state
            self.blynk.virtual_write(config.BLYNK_LIGHT_STATE_PIN, 1 if self.light_state["power"] else 0)
            
            # Update current color
            self.blynk.virtual_write(config.BLYNK_COLOR_PIN, self.light_state["color"])
            
            # Update current mode
            self.blynk.virtual_write(config.BLYNK_MODE_PIN, 1 if self.mode == "auto" else 0)
            
            # Update latest recognized face
            latest_face_text = self._format_latest_face()
            self.blynk.virtual_write(config.BLYNK_FACES_PIN, latest_face_text)
        except Exception as e:
            print(f"Error updating Blynk dashboard: {e}")
    
    def _format_latest_face(self):
        """Format the latest recognized face for display on Blynk."""
        if not self.latest_face:
            return "No user detected"
        
        name, timestamp = self.latest_face
        time_str = time.strftime("%H:%M:%S", time.localtime(timestamp))
        return f"Latest User: {name}\nDetected at: {time_str}"
    
    def _mode_write_handler(self, value):
        """Handle mode change from Blynk app."""
        try:
            mode_value = int(value[0])
            self.mode = "auto" if mode_value == 1 else "manual"
            print(f"System mode changed to: {self.mode}")
        except Exception as e:
            print(f"Error in mode write handler: {e}")
    
    def update_light_state(self, power, color):
        """Update the light state (power and color).
        
        Args:
            power: Boolean indicating if the light is on (True) or off (False)
            color: String name of the current color
        """
        self.light_state["power"] = power
        
        # Extract the basic color name
        if color and '_' in color:
            color = color.split('_')[0]
        
        self.light_state["color"] = color
        
        # Immediately update the values on Blynk
        try:
            self.blynk.virtual_write(config.BLYNK_LIGHT_STATE_PIN, 
                                  1 if power else 0)
            self.blynk.virtual_write(config.BLYNK_COLOR_PIN, color)
        except Exception as e:
            print(f"Error immediately updating light state: {e}")
    
    def add_recognized_face(self, name):
        """Add a recognized face and update the latest face.
        
        Args:
            name: Name of the recognized person
        """
        current_time = time.time()
        self.latest_face = (name, current_time)
        print(f"Updated latest recognized face to: {name}")
        
        # Immediately update the face display on Blynk
        try:
            latest_face_text = self._format_latest_face()
            self.blynk.virtual_write(config.BLYNK_FACES_PIN, latest_face_text)
        except Exception as e:
            print(f"Error immediately updating latest face: {e}")
    
    def get_operation_mode(self):
        """Get the current operation mode.
        
        Returns:
            str: Current mode ('auto' or 'manual')
        """
        return self.mode 