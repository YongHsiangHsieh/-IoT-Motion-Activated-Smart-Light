"""Smart bulb controller module for Tuya bulbs."""

import tinytuya
import config


class SmartBulb:
    """Class to control a Tuya smart bulb."""
    
    def __init__(self, device_id=config.DEVICE_ID, ip_address=config.DEVICE_IP, local_key=config.LOCAL_KEY):
        """Initialize the SmartBulb controller.
        
        Args:
            device_id: Tuya device ID
            ip_address: IP address of the bulb
            local_key: Local key for Tuya device
        """
        self.device_id = device_id
        self.ip_address = ip_address
        self.local_key = local_key
        self.bulb = None
        self.connected = False
    
    def connect(self):
        """Connect to the Tuya bulb device.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            self.bulb = tinytuya.BulbDevice(self.device_id, self.ip_address, self.local_key)
            self.bulb.set_version(3.5)
            status = self.bulb.status()
            print("Connection successful. Bulb status:", status)
            self.connected = True
            return True
        except tinytuya.TuyaError as e:
            print(f"Tuya Error during bulb initialization: {e}")
        except Exception as e:
            print(f"Unexpected error during bulb initialization: {e}")
        
        self.connected = False
        return False
    
    def turn_on(self):
        """Turn the bulb on.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected and not self.connect():
            return False
        
        try:
            self.bulb.turn_on()
            print("Bulb turned on.")
            return True
        except tinytuya.TuyaError as e:
            print(f"Tuya Error while turning on: {e}")
        except Exception as e:
            print(f"Unexpected error while turning on: {e}")
        
        return False
    
    def turn_off(self):
        """Turn the bulb off.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected and not self.connect():
            return False
        
        try:
            self.bulb.turn_off()
            print("Bulb turned off.")
            return True
        except tinytuya.TuyaError as e:
            print(f"Tuya Error while turning off: {e}")
        except Exception as e:
            print(f"Unexpected error while turning off: {e}")
        
        return False
    
    def set_color(self, r, g, b):
        """Set the bulb color using RGB values.
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected and not self.connect():
            return False
        
        try:
            self.bulb.set_colour(r, g, b)
            print(f"Bulb color set to RGB({r}, {g}, {b}).")
            return True
        except tinytuya.TuyaError as e:
            print(f"Tuya Error while setting color: {e}")
        except Exception as e:
            print(f"Unexpected error while setting color: {e}")
        
        return False
        
    def set_default_color(self):
        """Set the bulb to a default warm color (Sienna).
        
        Returns:
            bool: True if successful, False otherwise
        """
        return self.set_color(255, 255, 255) 