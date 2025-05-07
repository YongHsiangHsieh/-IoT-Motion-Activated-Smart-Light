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

## System Diagram
![Screenshot 2025-05-04 at 10 25 44 a m](https://github.com/user-attachments/assets/1ee58686-0379-4cef-a5da-bb826662a120)

## Demo Video
https://youtu.be/ELm-J6DMwxA

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
   - Ensure your phone is connected to the same **2.4GHz Wi-Fi network** as your smart light bulb.
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
   - In the Tuya IoT platform, under your project's **Devices** section, locate your light bulb.
   - Note down the **Device ID**, **Local IP Address**, and **Local Key**.

5. **Use `tinytuya` to verify credentials on your Raspberry Pi, making sure it's on the same 2.4GHz Wi-Fi network as the smart light bulb:**
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
   - Monitor the current light state and color
   - View the last recognized user
   - Switch between automatic and manual modes

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

## **Technical Implementation Details**

### **Face Recognition Algorithm**

After thorough testing of three different face recognition approaches, I implemented a custom "Relative Distance Check" algorithm that demonstrated superior accuracy and reliability:

1. **Algorithm Comparison and Selection**
   - **Original Min Distance Approach**: Basic distance threshold check
   - **Built-in Compare_Faces Method**: face_recognition library's default method
   - **Relative Distance Check**: Custom implementation with confidence gap analysis

   The Relative Distance Check consistently performed best in cross-comparison testing with diverse lighting conditions, distances, and face angles.

2. **How the Relative Distance Check Works**
   ```python
   # Calculate distances to all registered faces
   distances = []
   for i, reg_encoding in enumerate(registered_encodings):
       distance = np.linalg.norm(face_encoding - reg_encoding)
       distances.append((registered_info[i], distance))
   
   # Sort by distance (ascending)
   sorted_distances = sorted(distances, key=lambda x: x[1])
   
   # Get the best match and calculate gap between best and second-best match
   (best_name, best_color), best_distance = sorted_distances[0]
   gap = sorted_distances[1][1] - best_distance
   
   # Apply threshold and gap criteria for confident recognition
   if best_distance < self.threshold and gap >= self.min_gap:
       # Recognition successful
   ```

3. **Mathematical Foundation**
   - **Euclidean Distance**: The `np.linalg.norm()` function calculates the Euclidean (L2) distance between two 128-dimensional face encoding vectors
   - **Confidence Threshold**: Lower distances indicate higher similarity (below 0.6 is considered a match)
   - **Confidence Gap**: The difference between the best and second-best match provides a confidence measure
   - **Dual Criteria**: Recognition requires both passing the absolute threshold AND having a sufficient gap to the next-best match

   This approach significantly reduces false positives by ensuring the system only identifies faces when there's both a good match AND a clear distinction from other registered faces.

### **Multi-Threading Architecture**

The system employs a sophisticated multi-threading architecture to ensure responsive performance while handling concurrent operations:

1. **Thread Organization**
   - **Main Thread**: Coordinates the overall system workflow and processes sensor data
   - **Face Recognition Thread**: Dedicated thread that processes video frames and performs computationally intensive facial recognition
   - **Timer Threads**: Multiple timer threads manage time-sensitive operations like face recognition duration and bulb control

2. **Thread Synchronization**
   ```python
   # Avoid race conditions with multiple detections
   with self.lock:
       self.motion_count += 1
       # Event handling within the protected section
   ```

   A threading lock prevents race conditions when multiple motion events are detected in rapid succession, ensuring that state variables remain consistent.

3. **Asynchronous Face Recognition**
   ```python
   # Start face recognition thread
   face_thread = threading.Thread(
       target=self._run_face_recognition, 
       args=(count, face_recog_timer, bulb_timer)
   )
   face_thread.daemon = True
   face_thread.start()
   ```

   By processing face recognition asynchronously, the main thread remains responsive to new events and can continue monitoring sensors, maintaining system reliability.

4. **Blynk IoT Communication Thread**
   ```python
   # Start the Blynk thread
   self.running = True
   self.thread = threading.Thread(target=self._blynk_thread)
   self.thread.daemon = True
   self.thread.start()
   ```

   The Blynk service runs in its own dedicated daemon thread, enabling continuous communication with the Blynk cloud without blocking the main application. This architecture provides several crucial benefits:

   - **Non-blocking Cloud Communication**: The Blynk thread continuously maintains the connection to the Blynk cloud and processes incoming commands, all without affecting the responsiveness of the main security system
   
   - **Event-Driven Mode Switching**: Mode changes from the Blynk app (auto/manual) are processed through event handlers:
     ```python
     @self.blynk.on("V" + str(config.BLYNK_MODE_PIN))
     def handle_mode_write(value):
         self._mode_write_handler(value)
     ```
   
   - **State-Based Decision Making**: The main thread checks the current mode before responding to motion events, allowing remote control of system behavior without requiring direct thread communication:
     ```python
     # Check if we're in manual mode from Blynk
     if self.blynk_service.get_operation_mode() == "manual":
         print("System in manual mode - ignoring motion detection")
         return
     ```
   
   - **Asynchronous Dashboard Updates**: The Blynk thread periodically updates the mobile app dashboard with the latest system state, including light status, recognized users, and current operation mode
   
   This approach creates a clean separation between the IoT communication layer and the core security system logic, ensuring that network delays or cloud communication issues don't impact the system's ability to respond to local events.

### **Video Processing Pipeline**

The video processing pipeline efficiently extracts, analyzes, and processes video frames for face recognition:

1. **Frame Acquisition and Processing**
   ```python
   # Process video frames until timer expires or a face is recognized
   for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
       # Get the array from the frame
       image = frame.array
       
       # Process the frame to recognize faces
       results = self.face_service.process_frame(
           image, 
           self.registered_encodings, 
           self.registered_info
       )
   ```

   The PiCamera's video port provides a continuous stream of frames that are individually processed, enabling real-time face recognition.

2. **Result Filtering and Selection**
   ```python
   # Filter strong matches only
   strong_matches = [r for r in results if r[1] and r[3] < config.FACE_RECOGNITION_THRESHOLD]

   if strong_matches:
       # Choose the best (most confident) match among strong ones
       best_match = min(strong_matches, key=lambda r: r[3])
   ```

   The system filters recognition results to include only strong matches, then selects the single best match based on confidence metrics.

3. **Adaptive Recognition Strategy**
   - The system attempts recognition for a configurable duration (default 30 seconds)
   - Recognition stops immediately when a high-confidence match is found, conserving processing resources
   - If no face is recognized within the time window, a security alert is triggered (red light)
   - Face encodings are preloaded to improve performance but refreshed periodically (every 10 motion events) to ensure up-to-date recognition

This intelligent video processing approach balances accuracy, performance, and resource utilization to deliver reliable face recognition even on the resource-constrained Raspberry Pi platform.

### **Smart Bulb Control Implementation**

The system uses the TinyTuya library to communicate with Tuya-compatible smart bulbs directly over the local network:

1. **Protocol and Communication**
   ```python
   # Initialize the bulb connection
   self.bulb = tinytuya.BulbDevice(self.device_id, self.ip_address, self.local_key)
   self.bulb.set_version(3.5)  # Set protocol version for device communication
   ```

   The implementation uses the local control API (v3.5) that communicates directly with the device over your local network on port 6668 rather than through the cloud, minimizing latency and ensuring the system continues to work even during internet outages.

2. **Command Structure**
   ```python
   # Color control example
   def set_color(self, r, g, b):
       try:
           self.bulb.set_colour(r, g, b)
           print(f"Bulb color set to RGB({r}, {g}, {b}).")
           return True
       except Exception as e:
           print(f"Error while setting color: {e}")
           return False
   ```

   The system handles various bulb commands through abstracted methods (turn_on, turn_off, set_color) that manage the underlying protocol details while providing a clean interface for the security system.

3. **Reconnection Logic**
   ```python
   if not self.connected and not self.connect():
       return False
   ```

   Every command automatically attempts to reestablish connection if the bulb is disconnected, providing resilience against temporary network issues.

### **Error Handling Strategy**

The system implements robust error handling throughout its architecture to ensure reliability in real-world conditions:

1. **Graceful Degradation**
   The system is designed to continue operating even when certain components fail:
   
   - If bulb connection fails, the system continues monitoring motion and performing face recognition
   - If face recognition fails to detect any faces, the system defaults to security mode (red light)
   - If the Blynk service disconnects, the system continues to function locally

2. **Exception Management**
   ```python
   try:
       # Operation code
   except tinytuya.TuyaError as e:
       print(f"Tuya Error: {e}")
   except Exception as e:
       print(f"Unexpected error: {e}")
   ```

   Component-specific exceptions (like TuyaError) are caught separately from general exceptions, allowing for specialized handling of different error types.

3. **Network Resilience**
   
   - **Bulb Control**: The system maintains local control using TinyTuya, enabling bulb operation even when the internet is down
   - **Reconnection Logic**: Each component attempts to reconnect when communication fails
   - **Timeouts**: Operations that might block (like face recognition) are limited by configurable timeouts

4. **User Feedback**
   When errors occur, the system provides feedback through:
   
   - Console logging for troubleshooting
   - Visual indicators (LED, bulb color) for user awareness
   - Status updates to the Blynk dashboard when available

This multi-layered error handling ensures the system remains operational and provides appropriate feedback even when faced with various failure scenarios.

### **Security Considerations**

The system implements several security measures to protect both user data and device operation:

1. **Local Network Operation**
   - The smart bulb control operates over the local network only, eliminating cloud-based vulnerabilities
   - The Tuya protocol uses AES encryption for device commands, securing the communication channel
   - Device credentials (Device ID, IP, Local Key) are stored in a separate .env file (excluded from version control)

2. **User Data Protection**
   - Face recognition encodings are stored locally on the Raspberry Pi
   - No biometric data is sent to cloud services, preserving user privacy
   - User preferences are stored alongside face encodings with simple file naming conventions for minimal overhead

3. **Access Control**
   - The system distinguishes between registered and unregistered users
   - Only recognized faces trigger personalized responses (favorite colors)
   - Unrecognized faces trigger alert mode (red light)

4. **Restricted Scope**
   - Component permissions are limited to required functions only
   - The project follows separation of concerns principles, with each module having clearly defined responsibilities

These security considerations make the system suitable for home environments where privacy and reliable operation are important, while keeping the solution accessible for educational purposes.

## **Future Enhancements**

Potential improvements to the system include:

- Multiple device support for controlling several lights
- Integration with other smart home systems via MQTT
- Enhanced security with two-factor authentication
- Machine learning for improved face recognition accuracy
- Mobile notifications for security alerts
- Voice control integration

## Development Insights and Decisions

During the development of the facial recognition component, I initially intended to implement it locally for better performance and enhanced security—keeping facial data off the internet. After researching local face recognition solutions for the Raspberry Pi 4, I narrowed down three viable options:

1. **Dlib's Face Recognition via `face_recognition` Library**
2. **OpenCV's YuNet (for face detection) + SFace (for recognition)**
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

Eventually, I reverted to the lab-provided method using a custom `BlynkLib.py` script (installed via a direct link). This worked perfectly. Through this process, I discovered that the `blynklib>=0.2.6` package hadn't been maintained and lacked support for the newer Blynk IoT platform features or stable Legacy support.

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

This journey helped me better understand Blynk's evolution and its ecosystem, highlighting how project decisions must sometimes balance ease-of-use, reliability, and future scalability.

## **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## **Acknowledgements**

- Face recognition powered by [face_recognition](https://github.com/ageitgey/face_recognition)
- Tuya device control via [tinytuya](https://github.com/jasonacox/tinytuya)
- IoT connectivity provided by [Blynk](https://blynk.io/)
