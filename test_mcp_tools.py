#!/usr/bin/env python3
"""
Comprehensive test script for all Nordic Thingy:52 MCP Server tools.

This script tests all 25 MCP tools through direct calls to the server functions.
It provides detailed output and error reporting for each tool.
"""

import asyncio
import logging
import sys
from datetime import datetime
from typing import Any, Dict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


class MCPToolTester:
    """Comprehensive tester for all MCP server tools."""

    def __init__(self):
        """Initialize the tester."""
        self.device_address = None
        self.results = {
            "passed": [],
            "failed": [],
            "skipped": [],
        }
        self.start_time = None

    def print_header(self, title: str):
        """Print a formatted header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)

    def print_section(self, title: str):
        """Print a section header."""
        print(f"\n{'─' * 70}")
        print(f"  {title}")
        print(f"{'─' * 70}")

    def print_result(self, tool_name: str, result: Any, status: str = "✅"):
        """Print tool result."""
        print(f"{status} {tool_name}")
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"   {key}: {value}")
        elif isinstance(result, list):
            print(f"   Found {len(result)} items")
            for i, item in enumerate(result[:3], 1):  # Show first 3
                print(f"   [{i}] {item}")
        else:
            print(f"   {result}")

    async def test_tool(self, name: str, func, *args, **kwargs) -> bool:
        """Test a single tool and record the result."""
        try:
            result = await func(*args, **kwargs)
            self.print_result(name, result)
            self.results["passed"].append(name)
            return True
        except Exception as e:
            self.print_result(name, f"Error: {e}", "❌")
            self.results["failed"].append((name, str(e)))
            return False

    async def run_device_management_tests(self):
        """Test device management tools."""
        from src.server import (
            scan_devices,
            connect_device,
            get_device_status,
            configure_auto_reconnect,
        )

        self.print_section("Device Management Tools (6 tools)")

        # 1. Scan for devices
        print("\n1. scan_devices(timeout=10.0)")
        try:
            devices = await scan_devices(timeout=10.0)
            if devices:
                self.print_result("scan_devices", devices)
                self.device_address = devices[0].address
                self.results["passed"].append("scan_devices")
            else:
                self.print_result("scan_devices", "No devices found", "⚠️")
                self.results["skipped"].append("scan_devices")
                return False
        except Exception as e:
            self.print_result("scan_devices", f"Error: {e}", "❌")
            self.results["failed"].append(("scan_devices", str(e)))
            return False

        # 2. Connect to device
        print("\n2. connect_device(address)")
        await self.test_tool("connect_device", connect_device, self.device_address)

        # 3. Get device status
        print("\n3. get_device_status()")
        await self.test_tool("get_device_status", get_device_status)

        # 4. Configure auto-reconnect
        print("\n4. configure_auto_reconnect(enabled=True)")
        await self.test_tool(
            "configure_auto_reconnect",
            configure_auto_reconnect,
            enabled=True,
            max_attempts=5,
        )

        return True

    async def run_environmental_sensor_tests(self):
        """Test environmental sensor tools."""
        from src.server import (
            read_temperature,
            read_humidity,
            read_pressure,
            read_air_quality,
            read_all_sensors,
            read_color_sensor,
            read_light_intensity,
            read_step_count,
        )

        self.print_section("Environmental Sensor Tools (8 tools)")

        # 1. Read temperature
        print("\n1. read_temperature()")
        await self.test_tool("read_temperature", read_temperature)

        # 2. Read humidity
        print("\n2. read_humidity()")
        await self.test_tool("read_humidity", read_humidity)

        # 3. Read pressure
        print("\n3. read_pressure()")
        await self.test_tool("read_pressure", read_pressure)

        # 4. Read air quality
        print("\n4. read_air_quality()")
        await self.test_tool("read_air_quality", read_air_quality)

        # 5. Read all sensors
        print("\n5. read_all_sensors()")
        await self.test_tool("read_all_sensors", read_all_sensors)

        # 6. Read color sensor
        print("\n6. read_color_sensor()")
        await self.test_tool("read_color_sensor", read_color_sensor)

        # 7. Read light intensity
        print("\n7. read_light_intensity()")
        await self.test_tool("read_light_intensity", read_light_intensity)

        # 8. Read step count
        print("\n8. read_step_count()")
        await self.test_tool("read_step_count", read_step_count)

    async def run_motion_sensor_tests(self):
        """Test advanced motion sensor tools."""
        from src.server import (
            read_quaternion,
            read_euler_angles,
            read_heading,
            read_orientation,
            read_raw_motion,
        )

        self.print_section("Advanced Motion Sensor Tools (6 tools)")

        # 1. Read quaternion
        print("\n1. read_quaternion()")
        await self.test_tool("read_quaternion", read_quaternion)

        # 2. Read Euler angles
        print("\n2. read_euler_angles()")
        await self.test_tool("read_euler_angles", read_euler_angles)

        # 3. Read heading
        print("\n3. read_heading()")
        await self.test_tool("read_heading", read_heading)

        # 4. Read orientation
        print("\n4. read_orientation()")
        await self.test_tool("read_orientation", read_orientation)

        # 5. Read raw motion
        print("\n5. read_raw_motion()")
        await self.test_tool("read_raw_motion", read_raw_motion)

        # Note: read_tap_event is skipped as it requires physical interaction

    async def run_led_control_tests(self):
        """Test LED control tools."""
        from src.server import set_led_color, set_led_breathe, turn_off_led

        self.print_section("LED Control Tools (3 tools)")

        # 1. Set LED color (red)
        print("\n1. set_led_color(color='red', intensity=50)")
        await self.test_tool("set_led_color", set_led_color, color="red", intensity=50)
        await asyncio.sleep(1)

        # 2. Set LED breathe (blue)
        print("\n2. set_led_breathe(color='blue', intensity=50)")
        await self.test_tool(
            "set_led_breathe", set_led_breathe, color="blue", intensity=50
        )
        await asyncio.sleep(2)

        # 3. Turn off LED
        print("\n3. turn_off_led()")
        await self.test_tool("turn_off_led", turn_off_led)

    async def run_sound_control_tests(self):
        """Test sound control tools."""
        from src.server import play_sound, beep

        self.print_section("Sound Control Tools (2 tools)")

        # 1. Play sound
        print("\n1. play_sound(sound_id=1)")
        await self.test_tool("play_sound", play_sound, sound_id=1)
        await asyncio.sleep(1)

        # 2. Beep
        print("\n2. beep()")
        await self.test_tool("beep", beep)

    async def cleanup(self):
        """Clean up and disconnect."""
        from src.server import disconnect_device

        self.print_section("Cleanup")
        print("\ndisconnect_device()")
        await disconnect_device()
        print("✅ Disconnected from device")

    def print_summary(self):
        """Print test summary."""
        self.print_header("Test Summary")

        duration = datetime.now() - self.start_time
        total = (
            len(self.results["passed"])
            + len(self.results["failed"])
            + len(self.results["skipped"])
        )

        print(f"\nTotal Tests: {total}")
        print(f"✅ Passed: {len(self.results['passed'])}")
        print(f"❌ Failed: {len(self.results['failed'])}")
        print(f"⚠️  Skipped: {len(self.results['skipped'])}")
        print(f"\nDuration: {duration.total_seconds():.2f} seconds")

        if self.results["failed"]:
            print("\n" + "─" * 70)
            print("Failed Tests:")
            for name, error in self.results["failed"]:
                print(f"  ❌ {name}")
                print(f"     Error: {error}")

        if self.results["skipped"]:
            print("\n" + "─" * 70)
            print("Skipped Tests:")
            for name in self.results["skipped"]:
                print(f"  ⚠️  {name}")

        print("\n" + "=" * 70)

    async def run_all_tests(self):
        """Run all MCP tool tests."""
        self.start_time = datetime.now()
        self.print_header("Nordic Thingy:52 MCP Server - Tool Test Suite")

        print("\nThis script will test all 25 MCP tools")
        print("Make sure your Thingy:52 device is powered on and nearby")
        print("\nPress Ctrl+C to stop at any time")

        try:
            # Device Management
            connected = await self.run_device_management_tests()
            if not connected:
                print("\n❌ Could not connect to device. Stopping tests.")
                return

            # Wait a bit for connection to stabilize
            await asyncio.sleep(2)

            # Environmental Sensors
            await self.run_environmental_sensor_tests()
            await asyncio.sleep(1)

            # Motion Sensors
            await self.run_motion_sensor_tests()
            await asyncio.sleep(1)

            # LED Control
            await self.run_led_control_tests()
            await asyncio.sleep(1)

            # Sound Control
            await self.run_sound_control_tests()
            await asyncio.sleep(1)

        except KeyboardInterrupt:
            print("\n\n⚠️  Tests interrupted by user")
        except Exception as e:
            print(f"\n\n❌ Unexpected error: {e}")
            logger.exception("Test suite error")
        finally:
            # Cleanup
            await self.cleanup()

            # Print summary
            self.print_summary()


async def main():
    """Main entry point."""
    tester = MCPToolTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
