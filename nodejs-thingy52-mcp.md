MCP Server Requirements: Nordic Thingy:52 (Node.js Version)
1. Introduction
Purpose: Implement an MCP (Model Context Protocol) server in Node.js for controlling and reading data from Nordic Thingy:52 IoT devices via Bluetooth Low Energy (BLE).

Goal: Provide all features in the reference Python version, plus leverage advanced sensor and hardware capabilities available in the Node.js thingy52 package.

2. Functional Requirements
Device Discovery and Connection
Scan for nearby Thingy:52 devices and list found devices with name, address, RSSI.

API: Thingy.discover()

Connect to a device via Bluetooth MAC address.

API: new Thingy({address}), connect(callback)

Disconnect from currently connected device.

API: disconnect(callback)

Hardware Control
Set RGB LED color (range 0-255 per channel).

API: led.set({r, g, b}, callback)

Turn off LED (set RGB to 0,0,0).

API: led.set({r:0, g:0, b:0}, callback)

Play pre-programmed sounds using onboard speaker (sound IDs, tones, effects).

API: sound.playSound(soundId, callback)

Play custom tones or streamed audio data to speaker.

API: sound.playTone({frequency, duration}, callback), sound.streamAudio(buffer)

Play a beep (shortcut for a simple sound).

API: sound.playSound(1)

Sensor Reading
Read all environmental sensors:

Temperature (temperature.read() or subscribe)

Humidity (humidity.read())

Pressure (pressure.read())

Gas/air quality (gas.read() for CO2, TVOC)

Color sensor (color.read() returns RGB, intensity, etc.)

Subscribe to real-time notifications for sensor changes.

API: temperature.on('data', callback) etc.

Motion and Orientation
Access all motion sensors:

Accelerometer, Gyroscope, Magnetometer (9-axis IMU)

APIs: motion.on('data', callback)

Get Tap, Orientation, Step Counter, Quaternion, Euler, Rotation matrix, Gravity vector, Compass heading.

Advanced: Add APIs such as motion.getOrientation(), motion.getStepCount(), etc.

Microphone and Audio Streaming
Stream microphone data (ADPCM, 16-bit/16kHz) and provide raw access or callback event for new audio chunks.

API: microphone.on('data', callback)

Optional: Save, process, or transmit microphone streams via MCP.

Device Status
Return connection status and metadata (name, address, battery level, firmware version).

API: device.getStatus()

Utility Commands
List all available commands/tools.

Error handling for invalid/missing connections.

3. Advanced Features (Node.js Only)
These are in addition to Python version and should be highlighted:

Full motion data streaming and analytics (not just one-shot reading).

Real-time event subscription for sensors with callback/event model.

Microphone/audio streaming (Python version does not support this fully).

Firmware and battery info via additional GATT characteristics.

OTA firmware update trigger (if available via BLE).

Custom BLE characteristic read/write for extendibility.

4. Non-Functional Requirements
Must support multiple concurrent MCP client connections.

All Bluetooth operations asynchronous, with event-based notification.

Logging for all operations and errors.

Structured and documented REST/gRPC/stdio endpoints as needed for MCP protocol.

Clearly expose each MCP tool/resource via API (for integration with Claude/agents).

5. Security and Performance
Handle BLE connection timeouts, retries, and error states gracefully.

Validate all incoming API/tool parameters.

Ensure resource cleanup on disconnect/failure.

6. Documentation
Inline code docs (JSDoc style).

README with example usage for all tools.

API list documenting available commands, sensor mappings, events, and callbacks.

7. Stretch Goals (Optional)
Implement multi-device scanning/connection support for labs.

Add visualization/resource proxy endpoint (e.g. live sensor dashboard).

Integrate webhook/callback for real-time event streaming to cloud/Claude.

This requirements doc covers and expands on all Python MCP server features, ensuring your Node.js implementation will be more feature-rich, modern, and maintainable. If you need auto-generation/Claude spec.md or plan.md derived from this, let me know!



