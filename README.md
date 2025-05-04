# IoT Motion-Activated Smart Light with Face Recognition

#### Student Name: _Yong Hsiang Hsieh_  
#### Student ID: _20100776_

## Project Description

This project implements a smart security lighting system that integrates motion detection, light sensing, facial recognition, and IoT connectivity. The system automatically turns on a smart light bulb when motion is detected in dark conditions, recognizes registered users through facial recognition, and sets the bulb color to match the user's preference. Unrecognized faces trigger a red alert color.

### **Real-World Impact**  

This system enhances home security and convenience by providing:
- Energy efficiency by only activating lights when needed (motion + darkness)
- Personalized lighting based on facial recognition
- Security alerts for unrecognized visitors
- Remote monitoring and control through a mobile app

The project follows an **IoT architecture**, integrating key layers:
1. **Sensor Layer** – PIR motion sensor, light sensor, LED indicator, and Raspberry Pi Camera
2. **Processing Node** – Raspberry Pi 4 for edge computing, running facial recognition algorithms
3. **Gateway Layer** – Local Wi-Fi network (2.4GHz) connecting the Pi to smart light and cloud services
4. **Application Layer** – Blynk cloud platform for remote monitoring and control

## Tools, Technologies, and Equipment

### **Hardware:**
- Raspberry Pi 4
- PIR Motion Sensor (Grove Mini PIR Motion Sensor)
- Light Sensor (Grove ADC)
- Indicator LED (Grove LED)
- Raspberry Pi Camera Module
- Energizer Smart Light Bulb (Tuya-compatible)

### **Software & Cloud Services:**
- **Programming Language:** Python 3
- **Face Recognition:** face_recognition library (built on dlib)
- **Smart Bulb Control:** tinytuya library for local Tuya device communication
- **Sensor Interface:** grove.py and RPi.GPIO for sensor management
- **Camera Interface:** picamera library for the Raspberry Pi Camera
- **Cloud Connectivity:** Blynk IoT platform for remote monitoring and control
- **Networking:** Local 2.4GHz Wi-Fi network with Tuya devices on port 6668

## **GitHub Repository Structure**

- **main.py** - Main entry point for the security system
- **security_system.py** - Core orchestrator module that coordinates all components
- **sensors.py** - Interface for motion, light sensors, and LED indicator
- **camera_manager.py** - Manages the Raspberry Pi Camera operations
- **face_recognition_service.py** - Handles face detection and recognition
- **smart_bulb.py** - Controls the Tuya-compatible smart bulb
- **blynk_service.py** - Manages communication with the Blynk IoT cloud
- **registration.py** - Utility for registering new users and their preferences
- **config.py** - Configuration settings for all system components
- **utils.py** - Helper functions and utilities
- **requirements.txt** - Python package dependencies

## **System Architecture**

The system operates with the following workflow:

1. The PIR motion sensor continuously monitors for movement
2. When motion is detected, the light sensor reads the ambient light level
3. If the environment is dark (light level below threshold), the system:
   - Turns on the smart bulb with a default warm color
   - Activates the camera for facial recognition
   - Tries to identify the detected person for 30 seconds
4. If a registered face is recognized:
   - The bulb color changes to the person's favorite color
   - The recognition is logged and displayed in the Blynk app
5. If no face is recognized:
   - The bulb turns red as an alert indicator
6. After a configurable duration (default 60 seconds), the light turns off
7. All events and states are reported to the Blynk cloud for remote monitoring

## **Installation and Setup**

### **Hardware Setup**

1. **Raspberry Pi Setup:**
   - Connect the Pi Camera to the CSI port
   - Connect the Grove sensors to the GPIO pins:
     - PIR motion sensor: PIN 5
     - Indicator LED: PIN 18
     - Light sensor: Connect to the Grove ADC (I2C)

2. **Network Setup:**
   - Connect the Raspberry Pi to your 2.4GHz Wi-Fi network
   - Ensure your Tuya smart bulb is also connected to the same network
   - Note the IP address of your smart bulb for configuration

### **Software Installation**

1. **Install Required Packages:**
   ```bash
   git clone https://github.com/yourusername/IoT-Motion-Smart-Light.git
   cd IoT-Motion-Smart-Light
   pip install -r requirements.txt
   sudo pip install https://bit.ly/3C0PMVY  # Install BlynkLib
   ```

2. **Create Environment Configuration:**
   Create a `.env` file in the project root with the following content:
   ```
   DEVICE_ID=your_tuya_device_id
   DEVICE_IP=your_tuya_device_ip
   LOCAL_KEY=your_tuya_local_key
   BLYNK_TEMPLATE_ID=your_blynk_template_id
   BLYNK_AUTH_TOKEN=your_blynk_auth_token
   BLYNK_SERVER=blynk.cloud
   BLYNK_PORT=80
   BLYNK_TEMPLATE_NAME=Smart lighting system
   ```

3. **Obtain Tuya Device Credentials:**
   - To get your Tuya device credentials (DEVICE_ID, DEVICE_IP, LOCAL_KEY), you can use the [Tuya IoT Platform](https://iot.tuya.com/) or the [tinytuya wizard](https://github.com/jasonacox/tinytuya#setup-wizard):
     ```bash
     python -m tinytuya wizard
     ```

4. **Set Up Blynk:**
   - Create a Blynk account at [blynk.io](https://blynk.io/)
   - Create a new template with the following virtual pins:
     - V0: Light state (ON/OFF)
     - V1: Current light color
     - V2: Recognized faces
     - V3: Mode selection (auto/manual)
   - Get your BLYNK_TEMPLATE_ID and BLYNK_AUTH_TOKEN from the Blynk console

5. **Create Required Directories:**
   ```bash
   mkdir -p registered_faces
   ```

## **Usage**

### **Registering Users**

1. Run the registration utility:
   ```bash
   python registration.py
   ```

2. Follow the prompts to:
   - Enter your name
   - Select your favorite color from the available options
   - Position yourself in front of the camera for the photo

3. Your face will be registered and associated with your preferred color

### **Starting the System**

1. Start the main application:
   ```bash
   python main.py
   ```

2. The system will initialize and begin monitoring for motion

3. To stop the system, press Ctrl+C for a graceful shutdown

### **Remote Control with Blynk**

1. Download the Blynk IoT app on your smartphone
2. Connect to your Blynk project using the auth token
3. Use the app to:
   - Monitor the current light state
   - View the last recognized user
   - Switch between automatic and manual modes
   - Control the light manually when in manual mode

## **Customization**

### **Configuration Options**

Most system parameters can be adjusted in the `config.py` file:

- **Sensor Thresholds:**
  - `LIGHT_THRESHOLD`: Light level below which the environment is considered dark (default: 500)

- **Timing Settings:**
  - `BULB_ON_DURATION`: How long the light stays on after motion (default: 60 seconds)
  - `FACE_RECOGNITION_DURATION`: How long to attempt face recognition (default: 30 seconds)

- **Face Recognition Parameters:**
  - `FACE_RECOGNITION_THRESHOLD`: Threshold for face matching (default: 0.6)
  - `MIN_FACE_DISTANCE_GAP`: Minimum confidence gap required (default: 0.1)

- **Color Settings:**
  - Add or modify colors in the `SUPPORTED_COLORS` dictionary

### **Adding New Hardware**

The modular design makes it easy to add new hardware components:

1. Create a new module for your component
2. Add necessary configuration to `config.py`
3. Import and integrate the component in `security_system.py`

## **Troubleshooting**

### **Common Issues**

1. **Bulb Connection Failures:**
   - Verify the bulb is powered on and connected to the same network
   - Double-check DEVICE_ID, DEVICE_IP, and LOCAL_KEY in the .env file
   - Ensure port 6668 is open for local Tuya communication

2. **Face Recognition Problems:**
   - Improve lighting conditions during registration
   - Re-register with multiple angles for better recognition
   - Adjust FACE_RECOGNITION_THRESHOLD in config.py (lower = stricter)

3. **Motion Detection Issues:**
   - Verify the PIR sensor is properly connected
   - Adjust the sensor position for better coverage
   - Check the sensor's sensitivity with a voltmeter

4. **Blynk Connectivity:**
   - Verify your AUTH_TOKEN is correct
   - Ensure the Raspberry Pi has internet access
   - Check for firewall restrictions

## **Future Enhancements**

Potential improvements to the system include:

- Multiple device support for controlling several lights
- Integration with other smart home systems via MQTT
- Enhanced security with two-factor authentication
- Machine learning for improved face recognition accuracy
- Mobile notifications for security alerts
- Voice control integration

## **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## **Acknowledgements**

- Face recognition powered by [face_recognition](https://github.com/ageitgey/face_recognition)
- Tuya device control via [tinytuya](https://github.com/jasonacox/tinytuya)
- IoT connectivity provided by [Blynk](https://blynk.io/)

