# Product Requirements Document (PRD)
## Nordic Thingy:52 MCP Server for Claude Desktop

**Version:** 1.0  
**Date:** October 15, 2025  
**Status:** Draft  
**Owner:** Development Team

---

## Executive Summary

The Nordic Thingy:52 MCP Server transforms Claude Desktop into a powerful IoT control center, enabling natural language control and monitoring of Nordic Thingy:52 devices. This production-ready implementation provides seamless Bluetooth LE connectivity, comprehensive sensor monitoring, and intelligent automation capabilities through the Model Context Protocol (MCP).

---

## 1. Product Overview

### 1.1 Vision
Enable users to control and monitor IoT devices through natural conversation with Claude, eliminating the need for complex IoT platforms or custom mobile apps.

### 1.2 Goals
- **Primary:** Production-ready MCP server for Nordic Thingy:52 integration
- **Secondary:** Comprehensive automation framework for IoT scenarios
- **Tertiary:** Reference implementation for other BLE device integrations

### 1.3 Target Users
- IoT developers and prototypers
- Smart home enthusiasts
- Research labs and educational institutions
- Office environment managers
- Health and wellness monitoring users

---

## 2. Nordic Thingy:52 Capabilities

### 2.1 Hardware Specifications

#### Environmental Sensors
| Sensor | Measurement | Range | Use Cases |
|--------|-------------|-------|-----------|
| **Temperature** | °C/°F | -40°C to 85°C | Climate monitoring, HVAC control |
| **Humidity** | % RH | 0-100% | Comfort monitoring, mold prevention |
| **Pressure** | hPa | 260-1260 hPa | Weather prediction, altitude |
| **CO2 (eCO2)** | ppm | 400-8192 ppm | Air quality, ventilation alerts |
| **TVOC** | ppb | 0-1187 ppb | Air quality, chemical detection |
| **Color Sensor** | RGB + Clear | Full spectrum | Ambient light, color matching |
| **Light Intensity** | Lux | 0-100k+ lux | Daylight sensing, energy saving |

#### Motion Sensors (9-Axis)
| Component | Axes | Features |
|-----------|------|----------|
| **Accelerometer** | 3-axis | Tap detection, orientation, activity |
| **Gyroscope** | 3-axis | Rotation rate, angular velocity |
| **Magnetometer** | 3-axis | Compass heading, magnetic field |

#### Advanced Motion Processing
- **Quaternions**: Rotation representation without gimbal lock
- **Euler Angles**: Roll, pitch, yaw in degrees
- **Rotation Matrix**: 3x3 transformation matrix
- **Gravity Vector**: Normalized gravity direction
- **Compass Heading**: Magnetic north direction (0-360°)
- **Step Counter**: Pedometer functionality
- **Tap Detection**: Single/double tap events
- **Orientation**: Device position (portrait, landscape, etc.)

#### Actuators & I/O
| Component | Specification | Capabilities |
|-----------|---------------|--------------|
| **RGB LED** | 16.7M colors | Breathing, constant, one-shot modes |
| **Speaker** | 8-bit 8kHz | 8 preset sounds + streaming |
| **Microphone** | 16-bit 16kHz ADPCM | Audio streaming to host |
| **Button** | Single push button | Press, long-press, release events |
| **NFC** | Type 2 Tag | Configuration, pairing |

#### Power & Connectivity
- **Battery**: 1440 mAh Li-Po (30+ days typical use)
- **Charging**: USB micro-B, 5V
- **Bluetooth**: BLE 5.0 (nRF52832)
- **Range**: ~10 meters typical
- **OTA Updates**: Secure DFU capability

---

## 3. Core Features

### 3.1 Device Management

#### F1: Device Discovery
**Priority:** P0 (Must Have)
- Automatic BLE scanning for nearby Thingy:52 devices
- Filter by device name pattern ("Thingy", "Nordic Thingy")
- Display discovered devices with MAC addresses and signal strength (RSSI)
- Re-scan capability for discovering new devices

**User Stories:**
- As a user, I want to ask "Find my Thingy" and see all nearby devices
- As a user, I want to see signal strength to identify the closest device
- As a developer, I want to discover multiple Thingys for multi-device setups

#### F2: Connection Management
**Priority:** P0 (Must Have)
- Connect to device by MAC address or device name
- Maintain persistent connection with automatic reconnection
- Graceful disconnect with cleanup
- Connection status monitoring
- Battery level reporting

**User Stories:**
- As a user, I want to connect by saying "Connect to my office Thingy"
- As a user, I want automatic reconnection if connection drops
- As a user, I want to know battery level to plan charging

#### F3: Multi-Device Support
**Priority:** P1 (Should Have)
- Manage multiple Thingy devices simultaneously
- Device nicknames/aliases for easy reference
- Switch between devices in conversation
- Synchronized operations across multiple devices

**User Stories:**
- As a user, I want to control multiple Thingys in different rooms
- As a user, I want to create "scenes" affecting multiple devices
- As a developer, I want to compare sensor readings across locations

### 3.2 Environmental Monitoring

#### F4: Real-Time Sensor Reading
**Priority:** P0 (Must Have)
- Read all environmental sensors on demand
- Individual sensor queries (temperature only, humidity only, etc.)
- Formatted output with units
- Historical data tracking (in-memory for session)

**User Stories:**
- As a user, I want to ask "What's the temperature?" and get instant response
- As a user, I want to check air quality with "Is the air quality good?"
- As a health-conscious user, I want CO2 alerts for proper ventilation

#### F5: Continuous Monitoring
**Priority:** P1 (Should Have)
- Subscribe to sensor updates at configurable intervals
- Background monitoring with periodic reports
- Threshold-based alerts and notifications
- Data logging to file (CSV/JSON)

**User Stories:**
- As a user, I want to monitor CO2 every 5 minutes during work hours
- As a facility manager, I want daily air quality reports
- As a researcher, I want to log all sensor data for analysis

#### F6: Environmental Analytics
**Priority:** P2 (Nice to Have)
- Trend analysis (temperature rising/falling)
- Comfort index calculation (temp + humidity)
- Air quality scoring (CO2 + TVOC combined)
- Predictive alerts based on trends

**User Stories:**
- As a user, I want to know if temperature is trending up
- As a homeowner, I want comfort recommendations
- As a lab manager, I want environmental compliance reporting

### 3.3 Motion & Activity Tracking

#### F7: Motion Sensing
**Priority:** P0 (Must Have)
- Raw accelerometer, gyroscope, magnetometer data
- Quaternion and Euler angle representation
- Tap detection (single/double tap)
- Orientation detection
- Step counting

**User Stories:**
- As a user, I want tap detection for simple interactions
- As a developer, I want raw motion data for custom algorithms
- As a fitness user, I want step counting functionality

#### F8: Advanced Motion Processing
**Priority:** P1 (Should Have)
- Gesture recognition (shake, flip, rotate)
- Fall detection
- Activity classification (walking, running, stationary)
- Compass functionality
- Motion-triggered actions

**User Stories:**
- As a user, I want to shake the device to trigger an alert
- As an elderly care provider, I want fall detection alerts
- As a user, I want motion-activated lighting

### 3.4 LED Control & Visual Feedback

#### F9: LED Control
**Priority:** P0 (Must Have)
- Set RGB color (hex, RGB values, or color names)
- Brightness control (0-100%)
- LED modes: constant, breathing, one-shot
- Turn off LED
- Pre-defined color presets (red, green, blue, warm white, etc.)

**User Stories:**
- As a user, I want to say "Set LED to red" for visual indicators
- As a user, I want breathing blue for a calming effect
- As a developer, I want precise RGB control for status indication

#### F10: LED Effects & Patterns
**Priority:** P1 (Should Have)
- Flashing/blinking patterns
- Rainbow cycle
- Color transitions
- Alert patterns (red flash for warnings)
- Custom sequences

**User Stories:**
- As a user, I want a rainbow effect for parties
- As a meeting room manager, I want color-coded room status
- As a notification user, I want different colors for different alerts

### 3.5 Audio Control

#### F11: Sound Playback
**Priority:** P0 (Must Have)
- Play 8 preset sounds (indexed 1-8)
- Quick beep functionality
- Volume control
- Play tones at specific frequencies
- Stop sound playback

**User Stories:**
- As a user, I want to play a beep for acknowledgment
- As a user, I want alarm sounds for alerts
- As a developer, I want to play different sounds for different events

#### F12: Audio Streaming
**Priority:** P2 (Nice to Have)
- Stream custom audio to speaker
- Microphone data streaming
- Voice recording
- Audio notifications

**User Stories:**
- As a user, I want to stream custom audio messages
- As a security user, I want to record audio clips
- As a developer, I want voice-activated controls

### 3.6 Automation & Intelligence

#### F13: Conditional Automations
**Priority:** P1 (Should Have)
- If-then rules based on sensor thresholds
- Time-based automations
- Multi-condition logic (AND/OR)
- Action sequences
- Automation scheduling

**User Stories:**
- As a user, I want LED to turn red if CO2 > 1000 ppm
- As an office manager, I want automatic ventilation alerts
- As a gardener, I want humidity-based watering reminders

#### F14: Smart Scenes
**Priority:** P1 (Should Have)
- Pre-configured automation bundles
- Scene activation/deactivation
- Scene templates (focus mode, sleep mode, party mode)
- Custom scene creation

**User Stories:**
- As a user, I want "Focus Mode" to monitor air quality and dim lights
- As a user, I want "Meeting Mode" to indicate room occupancy
- As a user, I want "Sleep Mode" to turn off all alerts

#### F15: AI-Powered Insights
**Priority:** P2 (Nice to Have)
- Pattern recognition in sensor data
- Anomaly detection
- Predictive maintenance
- Usage recommendations
- Energy optimization suggestions

**User Stories:**
- As a user, I want Claude to notice unusual patterns
- As a facility manager, I want proactive maintenance alerts
- As a homeowner, I want energy-saving recommendations

---

## 4. Automation Use Cases

### 4.1 Home & Office Automation

#### UC1: Air Quality Management
**Scenario:** Automated office ventilation control
- Monitor CO2 and TVOC levels continuously
- Alert when CO2 > 1000 ppm (poor air quality)
- Visual indicator: Green (good), Yellow (fair), Red (poor)
- Integration with HVAC systems via IFTTT

**Implementation:**
```
"Monitor air quality. If CO2 exceeds 1000 ppm, set LED to red and beep twice"
"Check air quality every 10 minutes during work hours"
"Create a ventilation alert when air quality is poor"
```

#### UC2: Meeting Room Status Indicator
**Scenario:** Visual meeting room availability
- Green LED: Room available, good air quality
- Yellow LED: Room occupied or moderate air quality
- Red LED: Room occupied and poor air quality, needs ventilation
- Integration with calendar systems

**Implementation:**
```
"Set up meeting room indicator based on air quality and motion"
"Green LED when CO2 < 800, Yellow for 800-1200, Red for > 1200"
```

#### UC3: Comfort Zone Monitoring
**Scenario:** Optimal work environment
- Monitor temperature (20-24°C ideal) and humidity (40-60% ideal)
- Calculate comfort index
- Provide recommendations (open window, close blinds, adjust AC)
- Daily comfort reports

**Implementation:**
```
"Monitor my office comfort. Alert if temperature or humidity is outside ideal range"
"What's my comfort score right now?"
```

#### UC4: Smart Lighting Automation
**Scenario:** Energy-efficient lighting
- Use color sensor to detect ambient light
- Adjust LED brightness inversely to ambient light
- Simulate daylight with warm/cool color transitions
- Circadian rhythm support

**Implementation:**
```
"Adjust LED brightness based on ambient light"
"Create a daylight simulation from 6 AM to 8 PM"
```

### 4.2 Health & Wellness

#### UC5: Desk Ergonomics Monitor
**Scenario:** Posture and break reminders
- Motion sensor detects prolonged sitting
- Step counter tracks daily activity
- Periodic break reminders (every 60 minutes)
- Movement goal tracking

**Implementation:**
```
"Remind me to take a break every hour if I haven't moved"
"Track my daily step count"
"Alert me if I'm sitting for more than 90 minutes"
```

#### UC6: Sleep Environment Optimization
**Scenario:** Better sleep quality
- Monitor bedroom temperature (18-22°C ideal for sleep)
- Track humidity for respiratory health
- Dark and quiet environment detection
- Morning wake-up routine with gradual light

**Implementation:**
```
"Set up sleep mode: monitor temp and humidity, very dim blue LED"
"Wake me gradually with LED brightening from 7:00 AM"
```

#### UC7: Allergen & Air Quality Alerts
**Scenario:** Health condition management
- Monitor TVOC for chemical sensitivity
- CO2 monitoring for breathing issues
- Humidity tracking for mold prevention
- Daily air quality scores

**Implementation:**
```
"Alert me if TVOC levels are high, I'm sensitive to chemicals"
"Monitor humidity to prevent mold (keep between 30-50%)"
```

### 4.3 Security & Safety

#### UC8: Intrusion Detection
**Scenario:** Simple security system
- Motion detection via accelerometer
- Tap detection for forced entry
- Alert with sound and LED flash
- Log security events

**Implementation:**
```
"Alert me if device detects movement or tapping after 11 PM"
"Set up security mode: flash red LED and beep if moved"
```

#### UC9: Fall Detection & Alerts
**Scenario:** Elderly care or workplace safety
- Detect sudden falls using motion sensors
- Automatic alert with sound
- Emergency contact notification (via integration)
- Activity monitoring

**Implementation:**
```
"Detect falls and flash red LED with loud alarm"
"Monitor for unusual inactivity patterns"
```

#### UC10: Environmental Hazard Detection
**Scenario:** Early warning system
- High CO2 levels (>5000 ppm dangerous)
- Rapid temperature changes (fire indicator)
- Extreme humidity (water leak indicator)
- Multi-sensor correlation for accuracy

**Implementation:**
```
"Alert immediately if CO2 exceeds 5000 ppm - dangerous levels"
"Warn if temperature rises more than 10°C in 5 minutes"
```

### 4.4 Research & Education

#### UC11: Science Experiment Monitoring
**Scenario:** Classroom or lab experiments
- Log all sensor data at high frequency
- Real-time visualization
- Experiment comparison
- Data export for analysis

**Implementation:**
```
"Start experiment logging at 1-second intervals"
"Compare today's data with yesterday's experiment"
"Export all sensor data from the last hour"
```

#### UC12: Weather Station
**Scenario:** DIY weather monitoring
- Barometric pressure for weather prediction
- Temperature and humidity tracking
- Historical trends
- Forecast suggestions based on pressure changes

**Implementation:**
```
"Track pressure changes to predict weather"
"What does the pressure trend suggest for tomorrow?"
```

### 4.5 Smart Home Integration

#### UC13: IFTTT Integration
**Scenario:** Connect with other smart devices
- Trigger smart lights based on Thingy LED color
- Send notifications to phone based on sensors
- Control smart plugs based on conditions
- Calendar integration for automation scheduling

**Implementation:**
```
"If CO2 is high, trigger IFTTT to turn on smart fan"
"Send me a phone notification if humidity drops below 30%"
```

#### UC14: Voice Control via Claude
**Scenario:** Complete voice-controlled IoT hub
- Natural language device control
- Context-aware responses
- Multi-step automation via conversation
- Learning user preferences

**Implementation:**
```
"Hey Claude, how's my home environment?"
"Set up my usual evening routine"
"What should I adjust to improve comfort?"
```

### 4.6 Specialized Applications

#### UC15: Plant Care Monitor
**Scenario:** Automated plant health
- Humidity monitoring for soil moisture indication
- Temperature range monitoring
- Light level tracking for photosynthesis
- Watering reminders based on conditions

**Implementation:**
```
"Monitor my plant's environment. Alert if humidity drops below 40%"
"Is there enough light for my plants?"
```

#### UC16: Cold Chain Monitoring
**Scenario:** Temperature-sensitive storage
- Continuous temperature logging
- Out-of-range alerts
- Compliance reporting
- Data export for audit trails

**Implementation:**
```
"Monitor refrigerator temp (2-8°C). Alert if outside range"
"Generate daily temperature compliance report"
```

#### UC17: Workout Form Monitoring
**Scenario:** Exercise quality tracking
- Motion pattern recognition for exercises
- Rep counting using accelerometer
- Form feedback based on motion smoothness
- Workout logging

**Implementation:**
```
"Count my push-up reps using motion detection"
"Track my workout session motion data"
```

---

## 5. Technical Requirements

### 5.1 Platform Support
- **Primary:** macOS 12+ (tested and supported)
- **Secondary:** Windows 10/11 with Bluetooth LE
- **Tertiary:** Linux with BlueZ stack

### 5.2 Dependencies
```
Python 3.10+
bleak >= 0.21.0          # Bluetooth LE library
mcp >= 1.0.0             # Model Context Protocol SDK
pydantic >= 2.0.0        # Data validation
asyncio                   # Async operations
typing-extensions >= 4.8.0
dataclasses              # Data structures
```

### 5.3 Performance Requirements
- **Connection Time:** < 5 seconds for device discovery and connection
- **Sensor Reading:** < 500ms for single sensor query
- **Batch Reading:** < 1 second for all sensors
- **LED Response:** < 200ms for visual feedback
- **Memory Usage:** < 100MB during operation
- **Battery Impact:** Minimal (< 5% increase in Thingy battery drain)

### 5.4 Reliability Requirements
- **Connection Stability:** 99% uptime during active use
- **Auto-reconnect:** Automatic within 30 seconds of disconnection
- **Error Recovery:** Graceful degradation, no crashes
- **Data Accuracy:** ±2% for environmental sensors, ±5% for motion

### 5.5 Security Requirements
- **Bluetooth Security:** Encrypted BLE connection
- **Data Privacy:** No cloud transmission without consent
- **Local Processing:** All data processed locally
- **Secure Storage:** Configuration files with appropriate permissions

---

## 6. User Interface

### 6.1 Natural Language Interface
Users interact entirely through Claude Desktop's chat interface using natural language.

### 6.2 Command Examples

#### Discovery & Connection
```
"Find nearby Thingy devices"
"Connect to the Thingy in my office"
"What's the battery level?"
"Disconnect from current device"
```

#### Sensor Reading
```
"What's the temperature?"
"Check air quality"
"Read all sensors"
"Is the humidity too high?"
"What's the CO2 level?"
```

#### LED Control
```
"Turn the LED red"
"Set LED to warm white at 50% brightness"
"Create a breathing blue effect"
"Turn off the LED"
"Flash the LED green three times"
```

#### Sound Control
```
"Play sound 3"
"Make it beep"
"Play an alarm sound"
"Stop the sound"
```

#### Automations
```
"Monitor CO2 and alert me if it exceeds 1000 ppm"
"Set up a meeting room indicator"
"Create a focus mode for my office"
"If temperature exceeds 25°C, turn LED red and beep"
```

#### Status & Information
```
"Is the Thingy connected?"
"What automations are running?"
"Show me the current sensor readings"
"What's the device status?"
```

### 6.3 Response Format
- **Concise:** Clear, actionable responses
- **Visual:** Use of emojis for quick status (🟢 good, 🟡 warning, 🔴 alert)
- **Structured:** Sensor data in tables or lists
- **Contextual:** Relevant follow-up suggestions

---

## 7. Data Model

### 7.1 Device Information
```python
{
  "device_id": "MAC address",
  "name": "Friendly name",
  "alias": "User-defined alias",
  "connected": true/false,
  "battery_level": 0-100,
  "rssi": -90 to -30 dBm,
  "firmware_version": "x.x.x"
}
```

### 7.2 Environmental Data
```python
{
  "timestamp": "ISO 8601",
  "temperature": float,  // °C
  "humidity": float,     // %
  "pressure": float,     // hPa
  "co2": int,           // ppm
  "tvoc": int,          // ppb
  "color": {
    "red": int,
    "green": int,
    "blue": int,
    "clear": int
  },
  "light_intensity": float  // lux
}
```

### 7.3 Motion Data
```python
{
  "timestamp": "ISO 8601",
  "accelerometer": {"x": float, "y": float, "z": float},
  "gyroscope": {"x": float, "y": float, "z": float},
  "magnetometer": {"x": float, "y": float, "z": float},
  "quaternion": {"w": float, "x": float, "y": float, "z": float},
  "euler": {"roll": float, "pitch": float, "yaw": float},
  "heading": float,  // 0-360 degrees
  "steps": int,
  "tap_detected": bool,
  "orientation": "string"
}
```

---

## 8. Success Metrics

### 8.1 Technical Metrics
- Connection success rate > 95%
- Average response time < 1 second
- Zero critical bugs in production
- < 0.1% crash rate

### 8.2 User Experience Metrics
- Natural language understanding accuracy > 90%
- User satisfaction score > 4.5/5
- Automation setup success rate > 85%
- Repeat usage rate > 70%

### 8.3 Adoption Metrics
- 100+ GitHub stars in first 3 months
- 50+ active users in first month
- 10+ community-contributed automations
- 3+ integrations with other platforms

---

## 9. Future Enhancements

### 9.1 Phase 2 (3-6 months)
- Web dashboard for visualization
- Mobile companion app
- Cloud sync for multi-device configurations
- Advanced ML-based anomaly detection
- Home Assistant integration

### 9.2 Phase 3 (6-12 months)
- Support for Thingy:53 (newer model)
- Matter protocol support
- Voice control via Claude Voice
- Custom firmware builder
- Marketplace for automation templates

---

## 10. Risks & Mitigation

### 10.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Bluetooth connectivity issues | High | Medium | Robust reconnection logic, clear error messages |
| Platform compatibility | Medium | Medium | Extensive testing, graceful degradation |
| Battery drain on Thingy | Medium | Low | Optimized polling intervals, user control |
| MCP protocol changes | High | Low | Version pinning, migration plan |

### 10.2 User Experience Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Complex setup process | High | Medium | Automated installer, clear documentation |
| Limited hardware availability | Medium | Medium | Support for alternative sensors |
| Learning curve for automations | Medium | High | Templates, examples, guided wizard |

---

## 11. Dependencies & Assumptions

### 11.1 Dependencies
- Claude Desktop application
- Nordic Thingy:52 hardware
- MCP SDK availability
- Bluetooth LE support on host system

### 11.2 Assumptions
- Users have basic familiarity with IoT concepts
- Thingy:52 remains available for purchase
- MCP protocol remains stable
- Bluetooth LE standards remain compatible

---

## 12. Compliance & Standards

### 12.1 Regulatory Compliance
- FCC/CE certified hardware (Thingy:52)
- Bluetooth SIG qualified
- RoHS compliant
- No medical device claims

### 12.2 Software Standards
- MIT License (open source)
- WCAG 2.1 accessibility (documentation)
- GDPR compliant (no user data collection)
- Security best practices (OWASP)

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - Anthropic's protocol for extending Claude |
| **BLE** | Bluetooth Low Energy - Power-efficient wireless protocol |
| **RSSI** | Received Signal Strength Indicator - Connection quality |
| **TVOC** | Total Volatile Organic Compounds - Air quality metric |
| **eCO2** | Equivalent CO2 - Calculated CO2 from TVOC sensor |
| **Quaternion** | 4D number system for 3D rotations |
| **DFU** | Device Firmware Update - Over-the-air updates |
| **IFTTT** | If This Then That - Automation platform |

---

## Appendix B: References

1. Nordic Semiconductor Thingy:52 Documentation: https://infocenter.nordicsemi.com/topic/ug_thingy52/
2. MCP Protocol Documentation: https://docs.anthropic.com/
3. Bleak Library Documentation: https://bleak.readthedocs.io/
4. Bluetooth LE Specifications: https://www.bluetooth.com/specifications/

---

**Document History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-15 | Development Team | Initial draft |

