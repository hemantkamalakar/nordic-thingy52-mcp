"""Nordic Thingy:52 MCP Server using FastMCP."""

import logging
import sys
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from .bluetooth_client import ThingyBLEClient
from .constants import LED_COLORS, LED_MODE_BREATHE, LED_MODE_CONSTANT
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
async def scan_devices(timeout: float = 10.0) -> List[DeviceInfo]:
    """
    Scan for nearby Nordic Thingy:52 devices.

    Args:
        timeout: Scan duration in seconds (default: 10.0)

    Returns:
        List of discovered Thingy devices with their addresses, names, and signal strength
    """
    logger.info(f"Scanning for Thingy devices with timeout={timeout}s")
    devices = await ble_client.scan(timeout=timeout)
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
async def get_device_status() -> ConnectionStatus:
    """
    Get the current device connection status and battery level.

    Returns:
        Connection status including battery level if connected
    """
    if not ble_client.is_connected:
        return ConnectionStatus(connected=False)

    # Try to read battery level
    try:
        battery = await ble_client.read_battery()
    except Exception as e:
        logger.warning(f"Could not read battery: {e}")
        battery = None

    return ConnectionStatus(
        connected=True,
        address=ble_client.client.address if ble_client.client else None,
        battery_level=battery,
    )


# === Sensor Reading Tools ===

logger.info("Registering sensor reading tools...")


@mcp.tool()
async def read_temperature() -> dict[str, Optional[float]]:
    """
    Read the current temperature from the Thingy device.

    Returns:
        Temperature in Celsius
    """
    temp = await ble_client.read_temperature()
    return {"temperature_celsius": temp, "unit": "°C"}


@mcp.tool()
async def read_humidity() -> dict[str, Optional[float]]:
    """
    Read the current humidity from the Thingy device.

    Returns:
        Relative humidity in percentage
    """
    humidity = await ble_client.read_humidity()
    return {"humidity_percent": humidity, "unit": "%"}


@mcp.tool()
async def read_pressure() -> dict[str, Optional[float]]:
    """
    Read the current atmospheric pressure from the Thingy device.

    Returns:
        Pressure in hectopascals (hPa)
    """
    pressure = await ble_client.read_pressure()
    return {"pressure_hpa": pressure, "unit": "hPa"}


@mcp.tool()
async def read_air_quality() -> dict[str, Optional[int]]:
    """
    Read air quality sensors (CO2 and TVOC) from the Thingy device.

    Returns:
        CO2 in ppm and TVOC in ppb
    """
    co2, tvoc = await ble_client.read_air_quality()
    return {
        "co2_ppm": co2,
        "tvoc_ppb": tvoc,
        "air_quality_status": _assess_air_quality(co2),
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
async def read_step_count() -> dict[str, Optional[int]]:
    """
    Read the step counter from the motion sensor.

    Returns:
        Number of steps counted
    """
    steps = await ble_client.read_step_count()
    return {"steps": steps}


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
    success = await ble_client.set_led(LED_MODE_CONSTANT, 0, 0, 0, 0)

    if success:
        return {"status": "success", "message": "LED turned off"}
    else:
        return {"status": "error", "message": "Failed to turn off LED"}


# === Sound Control Tools ===

logger.info("Registering sound control tools...")


@mcp.tool()
async def play_sound(sound_id: int) -> dict[str, str]:
    """
    Play a preset sound from the Thingy speaker.

    Args:
        sound_id: Sound ID number (1-8)

    Returns:
        Status message
    """
    if sound_id not in range(1, 9):
        return {"status": "error", "message": "Sound ID must be between 1 and 8"}

    success = await ble_client.play_sound(sound_id)

    if success:
        return {"status": "success", "message": f"Playing sound {sound_id}"}
    else:
        return {"status": "error", "message": "Failed to play sound"}


@mcp.tool()
async def beep() -> dict[str, str]:
    """
    Play a quick beep sound.

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


# Main entry point
if __name__ == "__main__":
    logger.info("=" * 70)
    logger.info("Tool registration complete!")
    logger.info("Available tools:")
    logger.info("  Device Management: scan_devices, connect_device, disconnect_device, get_device_status")
    logger.info("  Sensors: read_temperature, read_humidity, read_pressure, read_air_quality,")
    logger.info("           read_all_sensors, read_color_sensor, read_step_count")
    logger.info("  LED Control: set_led_color, set_led_breathe, turn_off_led")
    logger.info("  Sound: play_sound, beep")
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
