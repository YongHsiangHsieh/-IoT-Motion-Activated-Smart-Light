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
   git clone https://github.com/YongHsiangHsieh/IoT-Motion-Smart-Light.git
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

3. **Set Up Blynk:**
   - Create a Blynk account at [blynk.io](https://blynk.io/)
   - Create a new template with the following virtual pins:
     - V0: Light state (ON/OFF)
     - V1: Current light color
     - V2: Recognized faces
     - V3: Mode selection (auto/manual)
   - Get your BLYNK_TEMPLATE_ID and BLYNK_AUTH_TOKEN from the Blynk console

4. **Create Required Directories:**
   ```bash
   mkdir -p registered_faces
   ```


### **Obtain Tuya Device Credentials**

To control your smart light bulb via the local network, you need to retrieve its unique credentials. Follow these steps:

1. **Set up the light bulb using the Smart Life app:**
   - Download and install the **Smart Life** app on your phone.
   - Ensure your phone is connected to the same **2.4GHz Wi-Fi network** as your Raspberry Pi.
   - Add the smart light bulb to the app by following the pairing instructions and entering your Wi-Fi password.

2. **Create and configure a Tuya IoT Cloud project:**
   - Go to the [Tuya IoT Platform](https://iot.tuya.com/) and sign up for an account.
   - Create a new cloud project.
   - Select **"Smart Home"** as the development type and choose **EU** as the data center region.
   - Enable required APIs such as **Device Status Notification**, **Device Control**, and **Device Management**.

3. **Link your Smart Life app to the Tuya IoT platform:**
   - In the Tuya Cloud project, go to **Devices > Link Tuya App Account**.
   - A QR code will appear. Open the Smart Life app, navigate to **Me > Developer Mode** and scan the QR code.
   - Once linked, the devices from your Smart Life app will appear in your cloud project.

4. **Retrieve device credentials:**
   - In the Tuya IoT platform, under your project’s **Devices** section, locate your light bulb.
   - Note down the **Device ID**, **Local IP Address**, and **Local Key**.

5. **Use `tinytuya` to verify credentials on your Raspberry Pi:**
   - Run the wizard on your Pi:
     ```bash
     tinytuya wizard
     ```
   - Paste the credentials when prompted.
   - The wizard will verify the device and confirm it is working.

6. **Configure your environment:**
   - Open the `.env` file and paste the following with your actual values:
     ```
     DEVICE_ID=your_tuya_device_id
     DEVICE_IP=your_tuya_device_ip
     LOCAL_KEY=your_tuya_local_key
     ```
   - Save the file. Your smart light bulb is now fully integrated and ready to be controlled locally!

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

2. **Bulb IP Address Changes:**
   - Since the IP address of the smart bulb is assigned via DHCP, it may change over time.
   - To find the current IP address, run the following command on your Raspberry Pi:
     ```bash
     tinytuya scan
     ```
   - This will list all Tuya devices on your local network. Locate your device using the DEVICE_ID and note the updated IP address.
   - Update the `.env` file with the new IP address under `DEVICE_IP=`.

3. **Face Recognition Problems:**
   - Improve lighting conditions during registration
   - Re-register with multiple angles for better recognition
   - Adjust FACE_RECOGNITION_THRESHOLD in config.py (lower = stricter)

4. **Motion Detection Issues:**
   - Verify the PIR sensor is properly connected
   - Adjust the sensor position for better coverage
   - Check the sensor's sensitivity with a voltmeter

5. **Blynk Connectivity:**
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

## Development Insights and Decisions

During the development of the facial recognition component, I initially intended to implement it locally for better performance and enhanced security—keeping facial data off the internet. After researching local face recognition solutions for the Raspberry Pi 4, I narrowed down three viable options:

1. **Dlib’s Face Recognition via `face_recognition` Library**
2. **OpenCV’s YuNet (for face detection) + SFace (for recognition)**
3. **Classical LBPH (Local Binary Patterns Histograms) Approach**

I chose the OpenCV approach using YuNet and SFace because of several advantages:
- Optimized for edge devices
- Pre-trained models and real-time performance
- Efficient processing pipeline
- High flexibility for integration

However, I encountered issues with incompatible OpenCV versions when trying to use YuNet on the Raspberry Pi 4. Despite attempting various workarounds, the hardware and software constraints of the Pi made this approach unfeasible.

As a result, I opted to use the `face_recognition` library, which is built on Dlib. Although this method is considered relatively heavy for a Raspberry Pi, it turned out to perform reliably without any noticeable issues during testing. This experience highlighted the importance of balancing system capabilities with implementation goals, and I learned to remain flexible and adaptive in choosing the right tools based on real-world constraints.

## Blynk Integration Journey

While integrating Blynk into the system, I initially chose not to follow the lab instructions. Instead, I tried using `blynklib>=0.2.6`—a newer-looking library that I thought would be more up-to-date. However, it didn't work as expected. I spent time troubleshooting the issue, suspecting it might be a problem with the template ID or Blynk configuration, but the system still failed to connect.

Eventually, I reverted to the lab-provided method using a custom `BlynkLib.py` script (installed via a direct link). This worked perfectly. Through this process, I discovered that the `blynklib>=0.2.6` package hadn’t been maintained and lacked support for the newer Blynk IoT platform features or stable Legacy support.

I also learned about the two versions of Blynk:

- **Legacy Blynk** (released around 2015):
  - Uses a raw TCP binary protocol (port 8442)
  - No encryption by default
  - Free to use
  - Beginner-friendly and easy to hack with
  - Think of it as the "Arduino IDE" of IoT—simple and accessible

- **New Blynk IoT** (released in 2021):
  - Uses HTTPS and secure WebSocket APIs (like MQTT under the hood)
  - Supports TLS/SSL encryption
  - Offers OAuth support and powerful new cloud features
  - Designed for scalability, better security, and modern IoT needs
  - Comes with tiered plans (Free, Plus, Pro, Business)
  - More like the "VS Code + GitHub + CI/CD" of IoT—cloud-native and production-ready

This journey helped me better understand Blynk’s evolution and its ecosystem, highlighting how project decisions must sometimes balance ease-of-use, reliability, and future scalability.
