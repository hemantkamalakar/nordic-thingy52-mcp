# Nordic Thingy:52 MCP Server

**Transform your Nordic Thingy:52 into an AI-controlled IoT powerhouse**

A production-ready Model Context Protocol (MCP) server that bridges physical sensor data with AI reasoning. Control and monitor your Nordic Thingy:52 IoT device through natural language conversations with Claude.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Why This MCP Server?

- **25 Comprehensive Tools**: Full sensor suite, device control, and automation
- **3 MCP Resources**: Real-time connection status, sensor guides, and automation examples
- **2 Smart Prompts**: Quick access to sensor readings and device control
- **Auto-Reconnect**: Robust connection management with automatic recovery
- **Zero Config**: Works out of the box with Claude Desktop
- **Production Ready**: Battle-tested with comprehensive error handling

## Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Thingy52MCPServer.git
   cd Thingy52MCPServer
   ```

2. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Claude Desktop**

   Add to your Claude Desktop config file:

   **MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

   **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

   ```json
   {
     "mcpServers": {
       "thingy52": {
         "command": "uv",
         "args": [
           "--directory",
           "/absolute/path/to/Thingy52MCPServer",
           "run",
           "python",
           "run_server.py"
         ]
       }
     }
   }
   ```

4. **Restart Claude Desktop**

5. **Start exploring!**
   ```
   "Find my Thingy device and show me all available sensors"
   ```

## Device Capabilities

### Environmental Sensors
- **Temperature**: -40°C to 85°C precision monitoring
- **Humidity**: 0-100% RH for comfort tracking
- **Pressure**: 260-1260 hPa barometric readings
- **Air Quality**: CO2 (400-8192 ppm) and TVOC (0-1187 ppb)
- **Light & Color**: RGB + Clear channel ambient sensing

### Advanced Motion Tracking
- **9-Axis Fusion**: Accelerometer + Gyroscope + Magnetometer
- **Quaternion**: Rotation representation for 3D orientation
- **Euler Angles**: Roll, pitch, yaw calculations
- **Heading**: Magnetic compass direction (0-360°)
- **Step Counter**: Activity and movement detection
- **Tap Events**: Physical interaction detection

### Device Control
- **RGB LED**: 16.7M colors with 3 modes (constant, breathe, one-shot)
- **Speaker**: 8 preset sound samples
- **Battery Monitor**: Real-time power level tracking
- **Auto-Reconnect**: Seamless connection recovery

## The 25 MCP Tools

### Device Management (4 tools)
- `scan_devices()` - Discover nearby Thingy:52 devices
- `connect_device(address)` - Connect to a specific device
- `disconnect_device()` - Gracefully disconnect
- `get_device_status()` - Connection and battery status
- `configure_auto_reconnect(enabled, max_attempts)` - Configure reconnection

### Environmental Sensors (8 tools)
- `read_temperature()` - Current temperature in °C
- `read_humidity()` - Relative humidity percentage
- `read_pressure()` - Barometric pressure in hPa
- `read_air_quality()` - CO2 and TVOC levels
- `read_color_sensor()` - RGBC color values
- `read_light_intensity()` - Ambient light in lux
- `read_all_sensors()` - Complete environmental snapshot
- `configure_sensor_intervals()` - Adjust sampling rates

### Motion & Orientation (6 tools)
- `read_quaternion()` - 3D orientation quaternion
- `read_euler_angles()` - Roll, pitch, yaw angles
- `read_heading()` - Compass direction (0-360°)
- `read_orientation()` - Human-readable orientation
- `read_raw_motion()` - Raw accelerometer/gyro/magnetometer
- `read_step_count()` - Activity tracking

### Device Control (4 tools)
- `set_led_color(color, intensity)` - Solid color LED
- `set_led_breathe(color, intensity, delay)` - Breathing effect
- `turn_off_led()` - Disable LED
- `play_sound(sound_id)` - Play preset sounds (1-8)
- `beep()` - Quick notification sound

### Battery (1 tool)
- `read_battery()` - Battery level percentage

## MCP Resources

### 1. Connection Status (`thingy://status`)
Real-time connection information including device address, battery level, auto-reconnect status, and connection state.

### 2. Sensor Guide (`thingy://sensors/guide`)
Comprehensive reference for all available sensors with capabilities, ranges, and use cases.

### 3. Automation Examples (`thingy://automation/examples`)
Pre-built automation scenarios and workflow templates.

## MCP Prompts

### 1. Quick Sensor Check
One-click access to read all environmental sensors with formatted output.

### 2. Device Control Panel
Interactive control interface for LED and sound with visual feedback.

## Advanced Usage Examples

### Smart Home Environment Monitoring

**Scenario**: Monitor room comfort and automatically alert when conditions are poor

```
"Monitor the temperature and humidity every 30 seconds. If temperature exceeds 26°C
or humidity goes above 65%, set the LED to orange and notify me. If CO2 exceeds
1000 ppm, make it red and play sound 3."
```

### Meeting Room Occupancy Detection

**Scenario**: Detect when a meeting room is occupied and track air quality

```
"Read the step counter and motion data. If motion is detected and CO2 is rising,
the room is likely occupied. Track CO2 levels and alert me if it exceeds 1200 ppm
(indicating poor ventilation). Flash the LED yellow as a warning."
```

### 3D Orientation Tracking

**Scenario**: Use the device as a motion controller or tilt sensor

```
"Read the quaternion and euler angles. Tell me the current 3D orientation.
If the device is tilted more than 45 degrees from level, change LED to red.
If it's level, make it green."
```

### Plant Health Monitor

**Scenario**: Track environmental conditions for optimal plant growth

```
"Create a plant health monitoring system:
1. Read temperature (ideal: 18-24°C)
2. Read humidity (ideal: 40-60%)
3. Read light intensity (needs >500 lux)
4. If all conditions are good: green LED
5. If any condition is poor: yellow LED + beep
6. If multiple conditions are bad: red LED + sound 5"
```

### Air Quality Alert System

**Scenario**: Real-time air quality monitoring with multi-level alerts

```
"Monitor air quality continuously:
- CO2 < 800 ppm: Green LED (excellent)
- CO2 800-1000 ppm: Blue LED (good)
- CO2 1000-1500 ppm: Yellow LED + sound 1 (moderate)
- CO2 > 1500 ppm: Red LED breathe + sound 3 (poor - ventilate!)
Also track TVOC and alert if it exceeds 500 ppb"
```

### Motion-Activated Night Light

**Scenario**: Detect movement and provide temporary lighting

```
"Use tap detection and motion sensors. When a tap is detected:
1. Read the light intensity
2. If it's dark (< 10 lux), turn on LED to warm white at 50% brightness
3. After 30 seconds of no motion, turn off the LED
4. Play a gentle sound (sound 2) when activated"
```

### Weather Station with Trends

**Scenario**: Track barometric pressure for weather prediction

```
"Read the barometric pressure every 5 minutes for the next hour.
Track the trend:
- Rapidly falling pressure (>3 hPa drop): Red LED - storm approaching
- Slowly falling: Yellow LED - weather may worsen
- Rising pressure: Green LED - improving weather
- Stable: Blue LED - weather steady
Also display current temperature and humidity"
```

### Desk Posture Reminder

**Scenario**: Use orientation to detect slouching or poor posture

```
"Mount the Thingy on my monitor. Read the euler angles every minute:
- If pitch angle changes by more than 15° from the baseline, I might be slouching
- Flash yellow LED and play sound 1 as a gentle reminder
- After 2 hours, play sound 4 as a break reminder regardless of posture
Track total sitting time using the step counter"
```

### Smart Lab Incubator Monitor

**Scenario**: Precision environmental control for scientific applications

```
"Monitor incubator conditions:
1. Read temperature (target: 37°C ± 0.5°C)
2. Read humidity (target: 80-90%)
3. Read CO2 (5% CO2 environment = ~50000 ppm)
4. If any parameter is out of range:
   - Red LED breathe
   - Play sound 8 (urgent alert)
   - Report exact values and deviation
5. If all parameters stable: slow green breathe
Log readings every 2 minutes"
```

### Package Delivery Detection

**Scenario**: Detect when a package is placed near the door

```
"Use as a package detector:
1. Monitor light sensor (package blocks light)
2. Detect tap/impact when package is set down
3. Check orientation change if package knocks device
4. When delivery detected:
   - Play sound 6 (delivery notification)
   - Flash green LED 3 times
   - Report: 'Package delivered at [time]'
5. Send me the light level change and tap strength"
```

## Natural Language Command Examples

### Device Discovery & Connection
```
"Scan for Thingy devices nearby"
"Connect to the Thingy with the strongest signal"
"What's the battery level of my Thingy?"
"Enable auto-reconnect with 5 retry attempts"
```

### Environmental Monitoring
```
"What's the current temperature and humidity?"
"Read all environmental sensors and format as a table"
"Is the air quality good in this room?"
"How bright is it right now? Give me the light intensity"
"What color is the ambient light? Read the RGB sensor"
```

### Motion & Orientation
```
"What direction is the device pointing? Give me the compass heading"
"Tell me the 3D orientation as euler angles"
"Is the device moving? Check the accelerometer"
"How many steps have been counted today?"
"Read the quaternion for 3D orientation tracking"
```

### LED Control
```
"Set the LED to warm white at 70% brightness"
"Make the LED breathe slowly in blue"
"Create a gentle red pulse effect with 2 second interval"
"Turn off the LED"
"Flash purple 5 times to signal completion"
```

### Sound Effects
```
"Play sound pattern 3"
"Make a beep to confirm the action"
"Play all 8 sounds in sequence so I can hear them"
```

### Complex Workflows
```
"Create a focus mode: Set LED to cool white at 40%, then monitor CO2.
If it exceeds 1000 ppm, remind me to open a window with sound 2"

"Build a temperature alarm: If temp goes above 28°C, flash red LED
and play sound 8. If it drops below 18°C, flash blue and play sound 4"

"Make a presence detector: Use motion, step counter, and CO2 to determine
if someone is in the room. Adjust LED color based on occupancy status"
```

## Project Structure

```
Thingy52MCPServer/
├── README.md                    # This file
├── PROMPT_GUIDE.md             # Advanced automation examples
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project configuration
├── run_server.py               # MCP server entry point
├── test_mcp_tools.py           # Comprehensive test suite
└── src/
    ├── __init__.py
    ├── bluetooth_client.py     # BLE communication layer
    ├── server.py               # MCP server (25 tools, 3 resources, 2 prompts)
    ├── models.py               # Data models for sensor readings
    └── constants.py            # BLE UUIDs and device constants
```

## Testing

Run the comprehensive test suite to verify all 25 tools:

```bash
python test_mcp_tools.py
```

This will test:
- Device discovery and connection
- All environmental sensors
- Motion and orientation sensors
- LED control (constant, breathe, off)
- Sound playback
- Auto-reconnect functionality
- Battery monitoring

## Troubleshooting

### Device Not Found
- Ensure Thingy:52 is powered on (press button, LED should flash)
- Check Bluetooth is enabled on your computer
- Move device closer (BLE range ~10 meters)
- Try `scan_devices()` with longer timeout

### Connection Failed
- Only one connection at a time (close Nordic Thingy app if running)
- Reset device: hold button for 10 seconds until LED turns off
- Check battery level (charge if below 20%)
- Restart Bluetooth on your computer

### Sensors Return None
- Wait 2-3 seconds after connection for sensors to initialize
- Some sensors need configuration first (use `configure_sensor_intervals()`)
- Check device is not in sleep mode (tap or press button)

### LED Not Changing
- Breathe mode may take time to start effect
- Try turning LED off first, then setting new mode
- Check if another application is controlling the LED

### MCP Server Not Appearing in Claude
- Verify config file path is absolute, not relative
- Check JSON syntax (common error: missing commas)
- Restart Claude Desktop completely
- View Claude logs for MCP server errors

## Technical Details

### BLE Implementation
- **Library**: Bleak (cross-platform BLE support)
- **Protocol**: Bluetooth Low Energy 5.0
- **Services**: 5 GATT services (environment, motion, UI, sound, battery)
- **Characteristics**: 25+ BLE characteristics
- **Connection**: Async/await pattern for performance

### Sensor Specifications
- **Temperature**: BME280 sensor, ±0.5°C accuracy
- **Humidity**: BME280 sensor, ±3% RH accuracy
- **Pressure**: BME280 sensor, ±1 hPa accuracy
- **Air Quality**: CCS811 sensor (eCO2 and TVOC)
- **Motion**: MPU-9250 9-axis IMU
- **Color**: BH1745 RGB sensor
- **Light**: BH1745 ambient light sensor

### Performance
- **Scan Time**: 5-10 seconds for device discovery
- **Connection**: 2-3 seconds typical
- **Sensor Read**: 50-200ms per reading
- **Reconnect**: Automatic with exponential backoff
- **Battery Life**: 3-7 days typical (varies with usage)

## Contributing

Contributions are welcome! Areas for enhancement:

- **Firmware Updates**: OTA firmware update support
- **Data Logging**: Historical sensor data storage
- **Alerting**: Email/SMS notifications for conditions
- **Multi-Device**: Support for multiple Thingy devices
- **Custom Sounds**: Upload custom audio samples
- **Calibration**: Sensor calibration routines

## License

MIT License - see [LICENSE](LICENSE) for details.

## Resources

- [Nordic Thingy:52 Official Page](https://www.nordicsemi.com/Products/Development-hardware/Nordic-Thingy-52)
- [Thingy:52 Hardware Documentation](https://infocenter.nordicsemi.com/topic/struct_nrf52/struct/nrf52_ble_thingy52.html)
- [Model Context Protocol Docs](https://modelcontextprotocol.io/)
- [Bleak Documentation](https://bleak.readthedocs.io/)

## Acknowledgments

Built with:
- [FastMCP](https://github.com/jlowin/fastmcp) - Fast MCP server framework
- [Bleak](https://github.com/hbldh/bleak) - Cross-platform BLE library
- Nordic Semiconductor for the amazing Thingy:52 hardware

---

**Made for the IoT and AI community**

Turn your legacy IoT devices into AI-powered automation nodes!
