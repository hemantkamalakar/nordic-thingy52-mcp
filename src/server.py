"""Nordic Thingy:52 MCP Server using FastMCP."""

import logging
import sys
from typing import List, Optional, Union

from mcp.server.fastmcp import FastMCP

from .bluetooth_client import ThingyBLEClient
from .constants import LED_COLORS, LED_MODE_BREATHE, LED_MODE_CONSTANT, LED_MODE_OFF
from .models import ConnectionStatus, DeviceInfo, EnvironmentalData

# Configure logging with more visible format
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG to see more details
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Print startup banner
print("=" * 70)
print("  Nordic Thingy:52 MCP Server")
print("  Version: 1.0.0")
print("=" * 70)
logger.info("Initializing Nordic Thingy:52 MCP Server...")

# Initialize FastMCP server
mcp = FastMCP("Nordic Thingy:52")
logger.info("FastMCP server instance created")

# Global BLE client instance
ble_client = ThingyBLEClient()
logger.info("Bluetooth LE client initialized")


# === Device Management Tools ===

logger.info("Registering device management tools...")


@mcp.tool()
async def scan_devices(timeout: Union[int, float] = 10.0) -> List[DeviceInfo]:
    """
    Scan for nearby Nordic Thingy:52 devices.

    Args:
        timeout: Scan duration in seconds (default: 10.0, accepts both int and float)

    Returns:
        List of discovered Thingy devices with their addresses, names, and signal strength
    """
    # Convert timeout to float to ensure compatibility
    timeout_float = float(timeout)
    logger.info(f"Scanning for Thingy devices with timeout={timeout_float}s")
    devices = await ble_client.scan(timeout=timeout_float)
    logger.info(f"Found {len(devices)} Thingy device(s)")
    return devices


@mcp.tool()
async def connect_device(address: str, timeout: float = 30.0) -> dict[str, str]:
    """
    Connect to a Nordic Thingy:52 device.

    Args:
        address: Bluetooth MAC address of the device (e.g., "AA:BB:CC:DD:EE:FF")
        timeout: Connection timeout in seconds (default: 30.0)

    Returns:
        Connection status message
    """
    logger.info(f"Attempting to connect to {address}")
    success = await ble_client.connect(address, timeout=timeout)

    if success:
        return {"status": "success", "message": f"Connected to {address}"}
    else:
        return {"status": "error", "message": f"Failed to connect to {address}"}


@mcp.tool()
async def disconnect_device() -> dict[str, str]:
    """
    Disconnect from the currently connected Thingy device.

    Returns:
        Disconnection status message
    """
    logger.info("Disconnecting from device")
    success = await ble_client.disconnect()

    if success:
        return {"status": "success", "message": "Disconnected successfully"}
    else:
        return {"status": "error", "message": "Not connected to any device"}


@mcp.tool()
async def get_device_status() -> dict:
    """
    Get the current device connection status and battery level.

    Returns:
        Connection status including battery level, reconnection state, and retry count
    """
    if not ble_client.is_connected:
        return {
            "connected": False,
            "connection_state": ble_client.connection_state,
            "reconnecting": ble_client.is_reconnecting,
            "retry_count": ble_client._retry_count if ble_client.is_reconnecting else 0,
            "last_address": ble_client._last_address,
        }

    # Try to read battery level
    try:
        battery = await ble_client.read_battery()
    except Exception as e:
        logger.warning(f"Could not read battery: {e}")
        battery = None

    return {
        "connected": True,
        "connection_state": ble_client.connection_state,
        "address": ble_client.client.address if ble_client.client else None,
        "battery_level": battery,
        "auto_reconnect_enabled": ble_client.auto_reconnect,
    }


@mcp.tool()
async def configure_auto_reconnect(
    enabled: bool, max_attempts: int = 10, initial_delay: float = 1.0, max_delay: float = 30.0
) -> dict[str, str]:
    """
    Configure auto-reconnect settings.

    Args:
        enabled: Enable or disable auto-reconnect
        max_attempts: Maximum reconnection attempts (0 = infinite)
        initial_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds

    Returns:
        Status message
    """
    ble_client.auto_reconnect = enabled
    ble_client.max_reconnect_attempts = max_attempts
    ble_client.initial_retry_delay = initial_delay
    ble_client.max_retry_delay = max_delay

    return {
        "status": "success",
        "message": f"Auto-reconnect {'enabled' if enabled else 'disabled'} "
        f"(max_attempts={max_attempts}, initial_delay={initial_delay}s, max_delay={max_delay}s)",
    }


@mcp.tool()
async def cancel_reconnect_attempts() -> dict[str, str]:
    """
    Cancel any ongoing reconnection attempts.

    Returns:
        Status message
    """
    if ble_client.is_reconnecting:
        await ble_client.cancel_reconnect()
        return {"status": "success", "message": "Reconnection attempts cancelled"}
    else:
        return {"status": "info", "message": "No reconnection in progress"}


# === Sensor Reading Tools ===

logger.info("Registering sensor reading tools...")


@mcp.tool()
async def read_temperature() -> dict:
    """
    Read the current temperature from the Thingy device.

    Returns:
        Temperature in Celsius
    """
    temp = await ble_client.read_temperature()
    return {"temperature_celsius": temp, "unit": "°C"}


@mcp.tool()
async def read_humidity() -> dict:
    """
    Read the current humidity from the Thingy device.

    Returns:
        Relative humidity in percentage
    """
    humidity = await ble_client.read_humidity()
    return {"humidity_percent": humidity, "unit": "%"}


@mcp.tool()
async def read_pressure() -> dict:
    """
    Read the current atmospheric pressure from the Thingy device.

    Returns:
        Pressure in hectopascals (hPa)
    """
    pressure = await ble_client.read_pressure()
    return {"pressure_hpa": pressure, "unit": "hPa"}


@mcp.tool()
async def read_air_quality() -> dict:
    """
    Read air quality sensors (CO2 and TVOC) from the Thingy device.

    IMPORTANT: The CCS811 gas sensor requires warm-up time:
    - First use: 20 min to 48 hours
    - After power cycle: 30+ minutes
    - For best accuracy: >100 hours continuous operation

    If you see 0 values, the sensor is still warming up. This is normal.
    Leave the device powered on for 30-60 minutes before expecting readings.

    Returns:
        CO2 in ppm, TVOC in ppb, and air quality status
    """
    co2, tvoc = await ble_client.read_air_quality()

    # Add helpful message if sensor is warming up
    status = _assess_air_quality(co2)
    if co2 == 0 and tvoc == 0:
        status = "warming_up"

    return {
        "co2_ppm": co2,
        "tvoc_ppb": tvoc,
        "air_quality_status": status,
        "note": "Values of 0 indicate sensor warm-up period (30-60 min required)" if co2 == 0 and tvoc == 0 else None,
    }


@mcp.tool()
async def read_all_sensors() -> EnvironmentalData:
    """
    Read all environmental sensors at once.

    Returns:
        Complete environmental data including temperature, humidity, pressure, CO2, and TVOC
    """
    logger.info("Reading all environmental sensors")
    data = await ble_client.read_all_environmental()
    return data


@mcp.tool()
async def read_color_sensor() -> dict:
    """
    Read the color sensor (RGB + Clear channel).

    Returns:
        RGBC values from the color sensor
    """
    color_data = await ble_client.read_color()
    if color_data:
        return {
            "red": color_data.red,
            "green": color_data.green,
            "blue": color_data.blue,
            "clear": color_data.clear,
        }
    return {"error": "Failed to read color sensor"}


@mcp.tool()
async def read_step_count() -> dict:
    """
    Read the step counter from the motion sensor.

    Returns:
        Number of steps counted
    """
    steps = await ble_client.read_step_count()
    return {"steps": steps}


@mcp.tool()
async def read_light_intensity() -> dict:
    """
    Read light intensity (lux) from the ambient light sensor.

    Returns:
        Light intensity in lux
    """
    lux = await ble_client.read_light_intensity()
    return {"light_intensity_lux": lux, "unit": "lux"}


# === Advanced Motion Sensor Tools ===

logger.info("Registering advanced motion sensor tools...")


@mcp.tool()
async def read_quaternion() -> dict:
    """
    Read quaternion orientation data (w, x, y, z).

    Quaternions provide rotation information without gimbal lock issues.

    Returns:
        Quaternion components (w, x, y, z)
    """
    quat = await ble_client.read_quaternion()
    if quat:
        w, x, y, z = quat
        return {
            "w": w,
            "x": x,
            "y": y,
            "z": z,
            "format": "quaternion"
        }
    return {"error": "Failed to read quaternion"}


@mcp.tool()
async def read_euler_angles() -> dict:
    """
    Read Euler angles (roll, pitch, yaw) in degrees.

    Returns:
        Roll, pitch, and yaw angles in degrees
    """
    angles = await ble_client.read_euler_angles()
    if angles:
        roll, pitch, yaw = angles
        return {
            "roll_degrees": roll,
            "pitch_degrees": pitch,
            "yaw_degrees": yaw,
            "unit": "degrees"
        }
    return {"error": "Failed to read Euler angles"}


@mcp.tool()
async def read_heading() -> dict:
    """
    Read compass heading in degrees (0-360).

    Returns:
        Compass heading in degrees
    """
    heading = await ble_client.read_heading()
    return {"heading_degrees": heading, "unit": "degrees", "range": "0-360"}


@mcp.tool()
async def read_orientation() -> dict:
    """
    Read device orientation (portrait, landscape, etc.).

    Returns:
        Current device orientation
    """
    orientation = await ble_client.read_orientation()

    orientation_map = {
        0: "portrait",
        1: "landscape",
        2: "reverse_portrait",
        3: "reverse_landscape",
    }

    orientation_name = "unknown"
    if orientation is not None:
        orientation_name = orientation_map.get(orientation, "unknown")

    return {
        "orientation": orientation_name,
        "orientation_code": orientation
    }


@mcp.tool()
async def read_tap_event(timeout: int = 10) -> dict:
    """
    Wait for and detect tap events on the device.

    This is an event-based sensor - it will wait up to timeout seconds for a tap.

    Args:
        timeout: Maximum seconds to wait for a tap event (default: 10)

    Returns:
        Tap event details including type (single/double) and direction
    """
    tap = await ble_client.read_tap_event()
    if tap:
        return {
            "tap_detected": True,
            "type": tap["type"],
            "direction": tap["direction"],
            "count": tap["count"]
        }
    return {"tap_detected": False, "message": "No tap detected within timeout"}


@mcp.tool()
async def read_raw_motion() -> dict:
    """
    Read raw accelerometer, gyroscope, and magnetometer data.

    Provides low-level motion sensor data for custom processing.

    Returns:
        Raw 3-axis data for accelerometer, gyroscope, and magnetometer
    """
    motion = await ble_client.read_raw_motion()
    if motion:
        return motion
    return {"error": "Failed to read raw motion data"}


# === LED Control Tools ===

logger.info("Registering LED control tools...")


@mcp.tool()
async def set_led_color(
    color: Optional[str] = None,
    red: Optional[int] = None,
    green: Optional[int] = None,
    blue: Optional[int] = None,
    intensity: int = 100,
) -> dict[str, str]:
    """
    Set the LED to a specific color.

    You can either specify a color name (e.g., "red", "blue", "green", "purple")
    or provide RGB values directly.

    Args:
        color: Named color (e.g., "red", "blue", "green", "purple", "warm_white")
        red: Red value 0-255 (used if color not specified)
        green: Green value 0-255 (used if color not specified)
        blue: Blue value 0-255 (used if color not specified)
        intensity: Brightness percentage 0-100 (default: 100)

    Returns:
        Status message
    """
    if color:
        color_lower = color.lower().replace(" ", "_")
        if color_lower in LED_COLORS:
            r, g, b = LED_COLORS[color_lower]
        else:
            return {
                "status": "error",
                "message": f"Unknown color '{color}'. Available: {', '.join(LED_COLORS.keys())}",
            }
    elif red is not None and green is not None and blue is not None:
        r, g, b = red, green, blue
    else:
        return {
            "status": "error",
            "message": "Must provide either 'color' name or RGB values",
        }

    success = await ble_client.set_led(LED_MODE_CONSTANT, r, g, b, intensity)

    if success:
        return {
            "status": "success",
            "message": f"LED set to RGB({r},{g},{b}) at {intensity}% intensity",
        }
    else:
        return {"status": "error", "message": "Failed to set LED"}


@mcp.tool()
async def set_led_breathe(color: str = "blue", intensity: int = 100, delay: int = 1000) -> dict:
    """
    Create a breathing effect with the LED.

    Args:
        color: Color name (default: "blue")
        intensity: Maximum brightness 0-100 (default: 100)
        delay: Breathing cycle duration in milliseconds (default: 1000)

    Returns:
        Status message
    """
    color_lower = color.lower().replace(" ", "_")
    if color_lower not in LED_COLORS:
        return {
            "status": "error",
            "message": f"Unknown color '{color}'. Available: {', '.join(LED_COLORS.keys())}",
        }

    r, g, b = LED_COLORS[color_lower]
    success = await ble_client.set_led(LED_MODE_BREATHE, r, g, b, intensity, delay)

    if success:
        return {"status": "success", "message": f"LED breathing effect set to {color}"}
    else:
        return {"status": "error", "message": "Failed to set LED breathing effect"}


@mcp.tool()
async def turn_off_led() -> dict[str, str]:
    """
    Turn off the LED.

    Returns:
        Status message
    """
    success = await ble_client.set_led(LED_MODE_OFF, 0, 0, 0)

    if success:
        return {"status": "success", "message": "LED turned off"}
    else:
        return {"status": "error", "message": "Failed to turn off LED"}


# === Resources ===

logger.info("Registering resources...")


@mcp.resource(
    "thingy://device/info",
    name="Device Information",
    description="Nordic Thingy:52 device capabilities, sensors, and specifications",
    mime_type="text/markdown"
)
def get_device_info() -> str:
    """Get information about the Nordic Thingy:52 device."""
    return """# Nordic Thingy:52 Device Information

## Overview
The Nordic Thingy:52 is a compact IoT prototyping platform with multiple sensors and actuators.

## Sensors

### Environmental Sensors
- **Temperature**: -40°C to 85°C (±0.5°C accuracy)
- **Humidity**: 0-100% RH (±3% accuracy)
- **Pressure**: 260-1260 hPa
- **Air Quality**:
  - CO2: 400-8192 ppm
  - TVOC: 0-1187 ppb
- **Color/Light**: RGB + Clear channel sensor

### Motion Sensors
- **9-Axis Motion**:
  - 3-axis accelerometer
  - 3-axis gyroscope
  - 3-axis magnetometer
- **Orientation**: Quaternion and Euler angles
- **Step Counter**: Activity tracking
- **Tap Detection**: Single/double tap events
- **Compass**: 360° heading

## Actuators
- **RGB LED**: 16.7M colors, multiple modes (constant, breathe, one-shot)
- **Speaker**: 8 preset sounds with volume control
- **Button**: User input

## Connectivity
- **Bluetooth 5.0**: Low Energy (BLE)
- **Range**: Up to 100m (line of sight)
- **Battery**: Rechargeable Li-Po, with battery monitoring

## Use Cases
- Environmental monitoring
- Motion detection and tracking
- IoT prototyping
- Smart home integration
- Activity tracking
- Educational projects
"""


@mcp.resource(
    "thingy://connection/status",
    name="Connection Status",
    description="Real-time connection status and device information",
    mime_type="text/markdown"
)
async def get_connection_status() -> str:
    """Get current connection status and device information."""
    if not ble_client.is_connected:
        return """# Connection Status

**Status**: ❌ Not Connected

To connect to a device:
1. Use `scan_devices()` to find nearby Thingy:52 devices
2. Use `connect_device(address)` with the device address
"""

    try:
        battery = await ble_client.read_battery()
    except Exception:
        battery = None

    return f"""# Connection Status

**Status**: ✅ Connected
**Address**: {ble_client.client.address if ble_client.client else 'Unknown'}
**Battery Level**: {battery}% {_get_battery_emoji(battery) if battery else ''}
**Auto-Reconnect**: {'Enabled' if ble_client.auto_reconnect else 'Disabled'}
**Connection State**: {ble_client.connection_state}
"""


@mcp.resource(
    "thingy://sensors/guide",
    name="Sensor Reading Guide",
    description="Guide for reading sensors and interpreting sensor values",
    mime_type="text/markdown"
)
def get_sensor_guide() -> str:
    """Get a guide for reading sensors and interpreting values."""
    return """# Sensor Reading Guide

## Environmental Sensors

### Temperature
- **Range**: -40°C to 85°C
- **Typical Indoor**: 18-25°C
- **Use**: `read_temperature()`

### Humidity
- **Range**: 0-100% RH
- **Comfortable**: 30-60%
- **Use**: `read_humidity()`

### Pressure
- **Range**: 260-1260 hPa
- **Sea Level**: ~1013 hPa
- **Use**: `read_pressure()`

### Air Quality
- **CO2 Levels**:
  - Excellent: < 800 ppm
  - Good: 800-1000 ppm
  - Acceptable: 1000-1500 ppm
  - Poor: 1500-2000 ppm
  - Bad: > 2000 ppm
- **TVOC**: Total Volatile Organic Compounds
- **Use**: `read_air_quality()`

### Color Sensor
- **Channels**: Red, Green, Blue, Clear
- **Use**: `read_color_sensor()`
- **Applications**: Color detection, ambient light sensing

### Light Intensity
- **Unit**: Lux
- **Ranges**:
  - Bright sunlight: 10,000+ lux
  - Office lighting: 320-500 lux
  - Dim room: < 50 lux
- **Use**: `read_light_intensity()`

## Motion Sensors

### Quaternion
- **Format**: (w, x, y, z) rotation
- **Use**: `read_quaternion()`
- **Best for**: 3D orientation without gimbal lock

### Euler Angles
- **Format**: Roll, Pitch, Yaw in degrees
- **Use**: `read_euler_angles()`
- **Best for**: Human-readable orientation

### Heading
- **Range**: 0-360 degrees
- **0°/360°**: North
- **90°**: East
- **180°**: South
- **270°**: West
- **Use**: `read_heading()`

### Orientation
- **States**: Portrait, Landscape, Reverse Portrait, Reverse Landscape
- **Use**: `read_orientation()`

### Raw Motion
- **Accelerometer**: Linear acceleration (mg)
- **Gyroscope**: Angular velocity (°/s)
- **Magnetometer**: Magnetic field (µT)
- **Use**: `read_raw_motion()`

### Step Count
- **Use**: `read_step_count()`
- **Note**: Accumulates over time

## LED Control

### Available Colors
- red, green, blue, cyan, yellow, purple, white, warm_white, orange, pink

### Modes
- **Constant**: Solid color
- **Breathe**: Pulsing effect
- **One-shot**: Single flash

### Usage
```
set_led_color(color="blue", intensity=100)
set_led_breathe(color="red", intensity=50, delay=1000)
turn_off_led()
```

## Sound Control

### Sound IDs
- 1-8: Various preset sounds and melodies

### Important Notes
- Volume control is NOT available for preset sounds (sample mode)
- Preset sounds play at a fixed volume
- Volume control only works in frequency mode

### Usage
```
play_sound(sound_id=1)  # Play preset sound 1
beep()  # Quick beep (uses sound 1)
```
"""


@mcp.resource(
    "thingy://examples/automation",
    name="Automation Examples",
    description="Practical automation scenarios and examples for the Thingy:52",
    mime_type="text/markdown"
)
def get_automation_examples() -> str:
    """Get examples of automation scenarios with the Thingy:52."""
    return """# Automation Examples

## Air Quality Monitoring

Monitor CO2 levels and alert when air quality is poor:

```
1. Read air quality: read_air_quality()
2. If CO2 > 1000 ppm: set_led_color(color="red")
3. Play alert sound: play_sound(sound_id=3)
4. Check every 5 minutes
```

## Temperature Alerts

Alert when temperature goes outside comfort zone:

```
1. Read temperature: read_temperature()
2. If temp < 18°C or temp > 25°C:
   - set_led_color(color="orange")
   - beep()
```

## Motion Detection

Detect when device is moved or tapped:

```
1. Read orientation: read_orientation()
2. Detect taps: read_tap_event(timeout=30)
3. On tap: set_led_breathe(color="blue")
4. Count steps: read_step_count()
```

## Environmental Dashboard

Create a complete environmental monitoring system:

```
1. Read all sensors: read_all_sensors()
2. Check air quality thresholds
3. Monitor temperature and humidity
4. Visual feedback:
   - Good conditions: LED green
   - Warning: LED yellow
   - Alert: LED red + sound
```

## Battery Monitoring

Monitor battery and alert when low:

```
1. Get device status: get_device_status()
2. If battery < 20%:
   - Flash LED red
   - Sound alert
```

## Smart Notifications

Use LED and sound for different alerts:

```
- Info: Blue LED, sound 1
- Warning: Yellow LED, sound 3
- Error: Red LED, sound 5
- Success: Green LED, sound 2
```
"""


# === Prompts ===

logger.info("Registering prompts...")


@mcp.prompt()
def connect_and_monitor() -> str:
    """
    Connect to Thingy:52 and start monitoring all sensors.

    A comprehensive prompt for setting up monitoring.
    """
    return """I'll help you connect to your Thingy:52 device and start monitoring.

Please follow these steps:

1. First, scan for nearby Thingy:52 devices:
   - Use the scan_devices tool
   - This will show all available devices with their addresses

2. Connect to your device:
   - Use connect_device with the address from step 1
   - Enable auto-reconnect if desired

3. Read all environmental sensors:
   - Use read_all_sensors for a complete overview
   - Or use individual sensor tools for specific readings

4. Check motion and orientation:
   - Use read_orientation for device position
   - Use read_quaternion or read_euler_angles for precise orientation
   - Use read_heading for compass direction

5. Monitor battery level:
   - Use get_device_status to check battery

Would you like me to proceed with scanning for devices?
"""


@mcp.prompt()
def setup_air_quality_alert() -> str:
    """
    Set up air quality monitoring with LED alerts.

    Configure automated air quality monitoring with visual feedback.
    """
    return """I'll set up air quality monitoring with LED alerts for your Thingy:52.

This automation will:

1. Monitor CO2 levels continuously
2. Provide visual feedback via LED:
   - Green: Excellent air quality (CO2 < 800 ppm)
   - Yellow: Good air quality (CO2 800-1000 ppm)
   - Orange: Acceptable (CO2 1000-1500 ppm)
   - Red: Poor air quality (CO2 > 1500 ppm)
3. Sound alert when air quality drops to poor

Steps to implement:

1. Connect to your Thingy:52 device
2. Read baseline air quality: read_air_quality()
3. Set initial LED based on current CO2 level
4. Set up periodic checking (every 5 minutes recommended)

Would you like me to:
a) Just check current air quality once?
b) Set up manual checking (you tell me when to check)?
c) Provide code for automated monitoring?
"""


@mcp.prompt()
def calibrate_motion_sensors() -> str:
    """
    Calibrate and test motion sensors.

    Guide for testing all motion sensing capabilities.
    """
    return """I'll help you calibrate and test the motion sensors on your Thingy:52.

Motion sensors available:
- Accelerometer (linear acceleration)
- Gyroscope (rotation rate)
- Magnetometer (magnetic field/compass)
- Orientation (quaternion and Euler angles)
- Step counter
- Tap detection

Testing procedure:

1. Place the device on a flat, stable surface
2. Read baseline orientation: read_orientation()
3. Read current heading: read_heading()
4. Test quaternion: read_quaternion()
5. Test Euler angles: read_euler_angles()

For motion testing:
6. Read raw motion data while device is stationary
7. Gently tap the device to test tap detection
8. Walk with the device to test step counting

Which test would you like to start with?
a) Orientation and heading
b) Motion detection (tap)
c) Step counting
d) All of the above
"""


@mcp.prompt()
def create_notification_system() -> str:
    """
    Create a multi-level notification system using LED and sound.

    Set up a comprehensive notification system.
    """
    return """I'll help you create a notification system using the Thingy:52's LED and speaker.

Notification Levels:

1. INFO (Blue LED + Sound 1)
   - General information
   - Non-urgent updates

2. SUCCESS (Green LED + Sound 2)
   - Task completed successfully
   - Positive confirmations

3. WARNING (Yellow/Orange LED + Sound 3)
   - Attention needed
   - Non-critical issues

4. ERROR (Red LED + Sound 5)
   - Critical alerts
   - Immediate attention required

5. CUSTOM
   - Define your own color and sound combinations

Available tools:
- set_led_color(color, intensity) - for solid colors
- set_led_breathe(color, intensity, delay) - for pulsing effect
- play_sound(sound_id) - for alert sounds (1-8)
- beep() - for simple beep

Which notification would you like to create first?
"""


@mcp.prompt()
def monitor_environment() -> str:
    """
    Set up comprehensive environmental monitoring.

    Monitor temperature, humidity, pressure, and air quality.
    """
    return """I'll set up comprehensive environmental monitoring for your Thingy:52.

Environmental Sensors Available:

1. Temperature (-40°C to 85°C)
   - Comfortable range: 18-25°C

2. Humidity (0-100% RH)
   - Comfortable range: 30-60%

3. Atmospheric Pressure (260-1260 hPa)
   - Standard sea level: ~1013 hPa

4. Air Quality
   - CO2: 400-8192 ppm (lower is better)
   - TVOC: 0-1187 ppb (volatile organic compounds)

5. Light Intensity
   - Measured in lux

6. Color Sensor
   - RGB + Clear channel

Monitoring Options:

A. Quick Check
   - Read all sensors once: read_all_sensors()
   - Get current snapshot

B. Continuous Monitoring
   - Set up alerts for out-of-range values
   - LED indicators for conditions
   - Regular reading intervals

C. Data Logging
   - Record sensor readings over time
   - Analyze trends

D. Smart Alerts
   - Temperature too high/low
   - High CO2 levels
   - Low light conditions

What type of monitoring would you like to set up?
"""


# === Sound Control Tools ===

logger.info("Registering sound control tools...")


@mcp.tool()
async def play_sound(sound_id: int) -> dict[str, str]:
    """
    Play a preset sound sample from the Thingy speaker.

    The Thingy:52 has 8 preset sound samples stored in the device firmware.
    Each sound ID plays a different preset sound effect or tone.

    NOTE: Volume control is not available for preset sounds. They play at a fixed volume.
    Only frequency mode supports volume control.

    Args:
        sound_id: Sound sample selector (1-8)
            1-8: Different preset sound samples

    Returns:
        Status message
    """
    if sound_id not in range(1, 9):
        return {"status": "error", "message": "Sound ID must be between 1 and 8"}

    success = await ble_client.play_sound(sound_id)

    if success:
        return {"status": "success", "message": f"Playing sound sample {sound_id}"}
    else:
        return {"status": "error", "message": "Failed to play sound"}


@mcp.tool()
async def beep() -> dict[str, str]:
    """
    Play a quick beep sound.

    Uses preset sound sample 1 for the beep.

    Returns:
        Status message
    """
    # Use sound ID 1 as the beep
    success = await ble_client.play_sound(1)

    if success:
        return {"status": "success", "message": "Beep!"}
    else:
        return {"status": "error", "message": "Failed to beep"}


# === Helper Functions ===


def _assess_air_quality(co2: Optional[int]) -> str:
    """Assess air quality based on CO2 levels."""
    if co2 is None:
        return "unknown"
    elif co2 < 800:
        return "excellent"
    elif co2 < 1000:
        return "good"
    elif co2 < 1500:
        return "acceptable"
    elif co2 < 2000:
        return "poor"
    else:
        return "bad"


def _get_battery_emoji(level: Optional[int]) -> str:
    """Get battery emoji based on level."""
    if level is None:
        return "❓"
    elif level > 80:
        return "🔋"
    elif level > 50:
        return "🔋"
    elif level > 20:
        return "🪫"
    else:
        return "🪫"


def main():
    """Main entry point for the MCP server."""
    logger.info("=" * 70)
    logger.info("Registration complete!")
    logger.info("")
    logger.info("Available MCP Tools (25):")
    logger.info("  Device Management (6): scan_devices, connect_device, disconnect_device, get_device_status,")
    logger.info("                         configure_auto_reconnect, cancel_reconnect_attempts")
    logger.info("  Environmental Sensors (8): read_temperature, read_humidity, read_pressure, read_air_quality,")
    logger.info("                              read_all_sensors, read_color_sensor, read_light_intensity, read_step_count")
    logger.info("  Advanced Motion (6): read_quaternion, read_euler_angles, read_heading,")
    logger.info("                       read_orientation, read_tap_event, read_raw_motion")
    logger.info("  LED Control (3): set_led_color, set_led_breathe, turn_off_led")
    logger.info("  Sound (2): play_sound, beep")
    logger.info("")
    logger.info("Available Resources (4):")
    logger.info("  - thingy://device/info - Device capabilities and specifications")
    logger.info("  - thingy://connection/status - Real-time connection status")
    logger.info("  - thingy://sensors/guide - Sensor reading guide and ranges")
    logger.info("  - thingy://examples/automation - Automation examples and use cases")
    logger.info("")
    logger.info("Available Prompts (5):")
    logger.info("  - connect_and_monitor - Connect and start monitoring")
    logger.info("  - setup_air_quality_alert - Air quality monitoring setup")
    logger.info("  - calibrate_motion_sensors - Motion sensor calibration")
    logger.info("  - create_notification_system - LED/Sound notification system")
    logger.info("  - monitor_environment - Environmental monitoring setup")
    logger.info("=" * 70)
    logger.info("Starting FastMCP server...")
    logger.info("Listening for MCP requests from Claude Desktop...")
    logger.info("Press Ctrl+C to stop the server")
    logger.info("=" * 70)

    try:
        # Run the FastMCP server
        mcp.run()
    except KeyboardInterrupt:
        logger.info("\n" + "=" * 70)
        logger.info("Server shutdown requested")
        logger.info("Cleaning up...")
        logger.info("Server stopped successfully")
        logger.info("=" * 70)
        sys.exit(0)
    except Exception as e:
        logger.error("=" * 70)
        logger.error(f"Server error: {e}")
        logger.error("=" * 70)
        sys.exit(1)


# Main entry point
if __name__ == "__main__":
    main()
