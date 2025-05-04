# IoT Motion-Activated Smart Light

#### Student Name: _Yong Hsiang Hsieh_  
#### Student ID: _20100776_

## Project Description
In modern smart homes, optimizing energy usage while maintaining convenience is crucial. This project aims to develop a motion-activated smart lighting system using a **Raspberry Pi 4**, **Energizer Smart Bulb powered by Tuya**, and **Blynk cloud service**. The system will automatically turn on the light when motion is detected and turn it off after one minute of inactivity. Additionally, the **Blynk mobile app** will provide remote control functionality, allowing users to manually toggle the light and switch between automatic and manual modes.

### **Real-World Impact**  
The hallway light in my home often disrupts my sleep due to its brightness penetrating into my room. Manually turning it off requires me to get up and walk to the switch, which is inconvenient, especially if someone turns it back on later in the night, causing further disturbance. Additionally, the hallway light is primarily used for brief moments, such as when going to the bathroom or upstairs, making it inefficient to keep it on continuously.  

To address this, the system will use a **motion sensor and light sensor** to ensure the hallway light **only turns on when needed**. When someone approaches and the ambient light level is low, the Tuya-powered smart bulb will illuminate the hallway for a short duration before automatically switching off if no further motion is detected. This minimizes **energy waste** while maintaining **convenience and comfort**.  

For **future enhancements**, a **camera module** can be integrated to improve motion detection accuracy and enable advanced features such as **AI-based movement recognition**, further optimizing the system’s responsiveness and security.

The project follows an **IoT architecture**, integrating key layers:
1. **Sensor Layer** – PIR motion sensor detects human presence, and a light sensor determines ambient light levels.
2. **Processing Node** – Raspberry Pi 4 processes sensor data and controls the smart bulb.
3. **Gateway Layer** – 
4. **Application Layer** – Remote monitoring and control via the **Blynk IoT App**, displaying current light state (on/off), current color, and the latest recognized user. It also allows switching between automatic and manual modes.

## Tools, Technologies, and Equipment
- **Hardware:**
  - Raspberry Pi 4
  - PIR Motion Sensor (HC-SR501)
  - Light Sensor (LDR or BH1750 Digital Light Sensor) for detecting ambient light levels
  - (Optional) Raspberry Pi Camera Module for AI-based motion detection
  - Energizer Smart Bulb powered by Tuya (2.4GHz Wi-Fi, port 6668)
  
- **Software & Cloud Services:**
  - Python (for scripting and automation)
  - Blynk IoT App (for displaying current light state, color, recognized user, and switching between auto/manual modes)
  - MQTT or HTTP Protocols (for device communication)
  - OpenCV (if camera integration is implemented, for motion detection and AI-based image analysis)
  - GitHub (for version control and documentation)

## **GitHub Repository Structure**
The project will be managed in a structured GitHub repository with the following layout:
```
- /src (Python scripts for sensor integration, Azure IoT connectivity, and smart bulb control)
- /docs (Diagrams, README, and technical documentation)
- /data (Sensor logs and test results)
- /presentation (Slides and demo videos)
```
