"""Sensors module for handling motion detection and light level sensing."""

from grove.grove_mini_pir_motion_sensor import GroveMiniPIRMotionSensor
from grove.adc import ADC
from grove.grove_led import GroveLed
import config


class LightSensor:
    """Class to handle light level sensing using Grove ADC."""
    
    def __init__(self, adc_address=0x08, channel=0):
        """Initialize the Light Sensor with ADC.
        
        Args:
            adc_address: I2C address of the ADC
            channel: ADC channel to read from
        """
        self.adc = ADC(adc_address)
        self.channel = channel
    
    def get_light_level(self):
        """Read the current light level.
        
        Returns:
            int: Current light level reading
        """
        return self.adc.read(self.channel)
    
    def is_dark(self):
        """Check if the environment is dark based on the light threshold.
        
        Returns:
            bool: True if it's dark, False otherwise
        """
        return self.get_light_level() < config.LIGHT_THRESHOLD


class MotionSensor:
    """Class to handle motion detection using Grove Mini PIR Motion Sensor."""
    
    def __init__(self, pin=config.PIR_SENSOR_PIN):
        """Initialize the Motion Sensor.
        
        Args:
            pin: GPIO pin number for the PIR sensor
        """
        self.sensor = GroveMiniPIRMotionSensor(pin)
        self.callback = None
    
    def set_callback(self, callback):
        """Set the callback function to be called when motion is detected.
        
        Args:
            callback: Function to call when motion is detected
        """
        self.callback = callback
        self.sensor.on_detect = self._on_motion_detected
    
    def _on_motion_detected(self):
        """Internal method called when motion is detected."""
        if self.callback:
            self.callback()


class IndicatorLED:
    """Class to handle the indicator LED."""
    
    def __init__(self, pin=config.LED_PIN):
        """Initialize the LED.
        
        Args:
            pin: GPIO pin number for the LED
        """
        self.led = GroveLed(pin)
    
    def on(self):
        """Turn on the LED."""
        self.led.on()
    
    def off(self):
        """Turn off the LED."""
        self.led.off() 