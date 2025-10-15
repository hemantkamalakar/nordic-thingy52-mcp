#!/usr/bin/env python3
"""
Test script for all Thingy:52 MCP server tools.

This script will:
1. Use provided MAC address or scan for nearby Thingy devices
2. Connect to a device
3. Test all sensors
4. Test LED control
5. Test sound playback
6. Disconnect

Run with:
    python3 test_all_tools.py                     # Scan for devices
    python3 test_all_tools.py F4:37:FC:B0:3B:5F  # Connect to specific device
"""

import asyncio
import sys
from datetime import datetime
import re

# Import our modules
from src.bluetooth_client import ThingyBLEClient
from src.constants import LED_COLORS

def is_valid_mac(mac):
    """Validate MAC address format."""
    mac_pattern = re.compile(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$')
    return bool(mac_pattern.match(mac))


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_test(name, status, message=""):
    """Print a test result."""
    symbol = "✓" if status else "✗"
    status_text = "PASS" if status else "FAIL"
    print(f"{symbol} {name}: {status_text}", end="")
    if message:
        print(f" - {message}")
    else:
        print()


async def main():
    """Run all tests."""
    print_header("Nordic Thingy:52 MCP Server - Tool Test Suite")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Get MAC address from command line if provided
    mac_address = sys.argv[1] if len(sys.argv) > 1 else None
    if mac_address and not is_valid_mac(mac_address):
        print(f"❌ Invalid MAC address format: {mac_address}")
        print("   Expected format: XX:XX:XX:XX:XX:XX (uppercase hex values)")
        sys.exit(1)

    client = ThingyBLEClient()
    device_address = mac_address
    test_results = {"passed": 0, "failed": 0}

    try:
        # ===== TEST 1: Device Discovery =====
        print_header("Test 1: Device Discovery")
        
        print("Scanning for Thingy devices (10 seconds)...")
        devices = await client.scan(timeout=10.0)
        
        if device_address:
            # If MAC address provided, check if it's in scan results
            matching_device = next((dev for dev in devices if dev.address.upper() == device_address.upper()), None)
            if matching_device:
                print(f"Found specified device: {matching_device.name}")
                print(f"  Address: {matching_device.address}")
                print(f"  RSSI: {matching_device.rssi} dBm")
                device_address = matching_device.address  # Use exact case from scan
                print_test("Device Discovery", True, "Found specified device")
                test_results["passed"] += 1
            else:
                print_test("Device Discovery", False, f"Specified device {device_address} not found in scan")
                print("\n⚠️  Make sure your Thingy is:")
                print("   - Powered on (blue LED pulsing)")
                print("   - Within 10 meters")
                print("   - Not connected to another device (close the Android app)")
                test_results["failed"] += 1
                return test_results
        else:
            if devices:
                print_test("Device Discovery", True, f"Found {len(devices)} device(s)")
                for i, device in enumerate(devices, 1):
                    print(f"  [{i}] {device.name}")
                    print(f"      Address: {device.address}")
                    print(f"      RSSI: {device.rssi} dBm")
                device_address = devices[0].address
                test_results["passed"] += 1
            else:
                print_test("Device Discovery", False, "No devices found")
                print("\n⚠️  Make sure your Thingy is:")
                print("   - Powered on (blue LED pulsing)")
                print("   - Within 10 meters")
                print("   - Not connected to another device")
                test_results["failed"] += 1
                return test_results

        # ===== TEST 2: Connection =====
        print_header("Test 2: Device Connection")
        
        MAX_RETRIES = 3
        for attempt in range(MAX_RETRIES):
            if attempt > 0:
                print(f"\nRetry attempt {attempt + 1} of {MAX_RETRIES}...")
                await asyncio.sleep(2)  # Wait between retries
                
            print(f"Connecting to {device_address}...")
            connected = await client.connect(device_address, timeout=20.0)
            
            if connected:
                print_test("Connection", True, "Successfully connected")
                test_results["passed"] += 1
                break
            elif attempt < MAX_RETRIES - 1:
                print("Connection failed, will retry...")
            else:
                print_test("Connection", False, "Failed to connect after all retries")
                print("\n⚠️  Troubleshooting tips:")
                print("   - Close any other apps connected to the device")
                print("   - Try power cycling the device")
                print("   - Make sure you're within range")
                test_results["failed"] += 1
                return test_results

        # Give the device a moment to stabilize
        print("Waiting 2 seconds for device to stabilize...")
        await asyncio.sleep(2)

        # ===== TEST 3: Battery Level =====
        print_header("Test 3: Battery Status")
        battery = await client.read_battery()

        if battery is not None:
            print_test("Battery Reading", True, f"{battery}%")
            test_results["passed"] += 1
        else:
            print_test("Battery Reading", False, "Could not read battery")
            test_results["failed"] += 1

        # ===== TEST 4: Temperature Sensor =====
        print_header("Test 4: Temperature Sensor")
        temp = await client.read_temperature()

        if temp is not None:
            print_test("Temperature", True, f"{temp}°C")
            test_results["passed"] += 1
        else:
            print_test("Temperature", False, "Could not read temperature")
            test_results["failed"] += 1

        # ===== TEST 5: Humidity Sensor =====
        print_header("Test 5: Humidity Sensor")
        humidity = await client.read_humidity()

        if humidity is not None:
            print_test("Humidity", True, f"{humidity}%")
            test_results["passed"] += 1
        else:
            print_test("Humidity", False, "Could not read humidity")
            test_results["failed"] += 1

        # ===== TEST 6: Pressure Sensor =====
        print_header("Test 6: Pressure Sensor")
        pressure = await client.read_pressure()

        if pressure is not None:
            print_test("Pressure", True, f"{pressure} hPa")
            test_results["passed"] += 1
        else:
            print_test("Pressure", False, "Could not read pressure")
            test_results["failed"] += 1

        # ===== TEST 7: Air Quality Sensor =====
        print_header("Test 7: Air Quality Sensor")
        co2, tvoc = await client.read_air_quality()

        if co2 is not None and tvoc is not None:
            print_test("Air Quality", True, f"CO2: {co2} ppm, TVOC: {tvoc} ppb")
            test_results["passed"] += 1
        else:
            print_test("Air Quality", False, "Could not read air quality")
            test_results["failed"] += 1

        # ===== TEST 8: Color Sensor =====
        print_header("Test 8: Color Sensor")
        color = await client.read_color()

        if color is not None:
            print_test("Color Sensor", True, f"R:{color.red} G:{color.green} B:{color.blue} C:{color.clear}")
            test_results["passed"] += 1
        else:
            print_test("Color Sensor", False, "Could not read color sensor")
            test_results["failed"] += 1

        # ===== TEST 9: Step Counter =====
        print_header("Test 9: Step Counter")
        steps = await client.read_step_count()

        if steps is not None:
            print_test("Step Counter", True, f"{steps} steps")
            test_results["passed"] += 1
        else:
            print_test("Step Counter", False, "Could not read step counter")
            test_results["failed"] += 1

        # ===== TEST 10: All Sensors at Once =====
        print_header("Test 10: All Environmental Sensors")
        print("Reading all environmental sensors at once...")

        all_data = await client.read_all_environmental()

        if any([all_data.temperature, all_data.humidity, all_data.pressure]):
            print_test("All Sensors", True)
            print(f"  Temperature: {all_data.temperature}°C")
            print(f"  Humidity: {all_data.humidity}%")
            print(f"  Pressure: {all_data.pressure} hPa")
            print(f"  CO2: {all_data.co2} ppm")
            print(f"  TVOC: {all_data.tvoc} ppb")
            test_results["passed"] += 1
        else:
            print_test("All Sensors", False, "No sensor data returned")
            test_results["failed"] += 1

        # ===== TEST 11: LED Control =====
        print_header("Test 11: LED Control")
        print("Testing LED colors (watch your Thingy)...")

        # Test Red
        success = await client.set_led(1, 255, 0, 0, 100)
        if success:
            print_test("LED Red", True)
            test_results["passed"] += 1
        else:
            print_test("LED Red", False)
            test_results["failed"] += 1
        await asyncio.sleep(1)

        # Test Green
        success = await client.set_led(1, 0, 255, 0, 100)
        if success:
            print_test("LED Green", True)
            test_results["passed"] += 1
        else:
            print_test("LED Green", False)
            test_results["failed"] += 1
        await asyncio.sleep(1)

        # Test Blue
        success = await client.set_led(1, 0, 0, 255, 100)
        if success:
            print_test("LED Blue", True)
            test_results["passed"] += 1
        else:
            print_test("LED Blue", False)
            test_results["failed"] += 1
        await asyncio.sleep(1)

        # Test Breathing Effect
        print("Testing breathing effect (purple)...")
        success = await client.set_led(2, 128, 0, 128, 100, 1000)
        if success:
            print_test("LED Breathing", True)
            test_results["passed"] += 1
        else:
            print_test("LED Breathing", False)
            test_results["failed"] += 1
        await asyncio.sleep(3)

        # Turn off LED
        await client.set_led(1, 0, 0, 0, 0)
        print("LED turned off")

        # ===== TEST 12: Sound Control =====
        print_header("Test 12: Sound Control")
        print("Testing sound playback...")

        # Test beep (sound 1)
        success = await client.play_sound(1)
        if success:
            print_test("Sound Playback (beep)", True)
            test_results["passed"] += 1
        else:
            print_test("Sound Playback (beep)", False)
            test_results["failed"] += 1
        await asyncio.sleep(1)

        # Test another sound
        print("Playing sound 3...")
        success = await client.play_sound(3)
        if success:
            print_test("Sound Playback (sound 3)", True)
            test_results["passed"] += 1
        else:
            print_test("Sound Playback (sound 3)", False)
            test_results["failed"] += 1

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # ===== Cleanup =====
        if client.is_connected:
            print_header("Cleanup")
            print("Disconnecting from device...")
            await client.disconnect()
            print_test("Disconnect", True)

    # ===== Summary =====
    print_header("Test Summary")
    total = test_results["passed"] + test_results["failed"]
    print(f"Total Tests: {total}")
    print(f"✓ Passed: {test_results['passed']}")
    print(f"✗ Failed: {test_results['failed']}")

    if test_results["failed"] == 0:
        print("\n🎉 All tests passed! Your Thingy:52 is working perfectly.")
    elif test_results["passed"] > 0:
        print(f"\n⚠️  Some tests failed. {test_results['passed']}/{total} tests passed.")
        print("Check the output above for details on what failed.")
    else:
        print("\n❌ All tests failed. Check your device and connection.")

    success_rate = (test_results["passed"] / total * 100) if total > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")

    print("\n" + "=" * 70)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

    return test_results


if __name__ == "__main__":
    print("\n⚠️  Important Notes:")
    print("  - Make sure your Thingy:52 is powered on")
    print("  - Close the Nordic Thingy app if it's running")
    print("  - Keep the Thingy within 10 meters")
    print("  - The test will take about 30-60 seconds")
    
    if len(sys.argv) > 1:
        print(f"\nUsing MAC address: {sys.argv[1]}")
    else:
        print("\nNo MAC address provided - will scan for nearby devices")
    
    print("\nPress Enter to start testing, or Ctrl+C to cancel...")

    try:
        input()
    except KeyboardInterrupt:
        print("\n\nTest cancelled.")
        sys.exit(0)

    # Run the async main function
    results = asyncio.run(main())

    # Exit with appropriate code
    sys.exit(0 if results["failed"] == 0 else 1)
