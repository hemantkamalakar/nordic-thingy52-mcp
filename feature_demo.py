#!/usr/bin/env python3
"""Comprehensive feature demo for Nordic Thingy:52 MCP Server."""

import asyncio
import logging
from src.bluetooth_client import ThingyBLEClient

# Enable debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Thingy52Demo:
    """Demo class for Thingy:52 features."""

    def __init__(self):
        """Initialize the demo."""
        self.client = ThingyBLEClient()
        self.device_address = None

    async def scan_devices(self, timeout: float = 10.0):
        """Scan for Thingy:52 devices."""
        print("\n=== Device Discovery ===")
        print(f"Scanning for {timeout} seconds...")
        
        devices = await self.client.scan(timeout=timeout)
        if not devices:
            print("❌ No devices found!")
            return False
        
        print(f"\n✅ Found {len(devices)} device(s):")
        for i, device in enumerate(devices, 1):
            print(f"\nDevice {i}:")
            print(f"  Name: {device.name}")
            print(f"  Address: {device.address}")
            print(f"  Signal Strength: {device.rssi} dBm")
            
        # Use the first device found
        self.device_address = devices[0].address
        return True

    async def connect(self):
        """Connect to the Thingy:52 device."""
        if not self.device_address:
            print("❌ No device address available. Run scan first.")
            return False

        print(f"\n=== Connecting to {self.device_address} ===")
        success = await self.client.connect(self.device_address)
        if success:
            print("✅ Connected successfully!")
            return True
        else:
            print("❌ Connection failed!")
            return False

    async def configure_speaker(self):
        """Configure speaker settings."""
        print("\n=== Configuring Speaker ===")
        
        try:
            # Enable speaker with max volume
            await self.client.configure_speaker(volume=100)
            print("✅ Speaker configured")
            return True
        except Exception as e:
            print(f"❌ Failed to configure speaker: {e}")
            return False

    async def test_environmental_sensors(self):
        """Test all environmental sensors."""
        print("\n=== Environmental Sensors ===")
        
        # Temperature
        temp = await self.client.read_temperature()
        print(f"Temperature: {temp:.1f}°C" if temp else "Temperature: N/A")
        
        # Humidity
        humidity = await self.client.read_humidity()
        print(f"Humidity: {humidity:.1f}%" if humidity else "Humidity: N/A")
        
        # Pressure
        pressure = await self.client.read_pressure()
        print(f"Pressure: {pressure:.1f} hPa" if pressure else "Pressure: N/A")
        
        # Air Quality
        air_quality = await self.client.read_air_quality()
        if air_quality and isinstance(air_quality, tuple) and len(air_quality) == 2:
            co2, tvoc = air_quality
            print(f"CO2: {co2} ppm")
            print(f"TVOC: {tvoc} ppb")
        else:
            print("Air Quality: N/A")

    async def test_motion_sensors(self):
        """Test motion sensors."""
        print("\n=== Motion Sensors ===")
        
        # Quaternion (orientation)
        quat = await self.client.read_quaternion()
        if quat:
            w, x, y, z = quat
            print("Quaternion:")
            print(f"  w: {w:.3f}")
            print(f"  x: {x:.3f}")
            print(f"  y: {y:.3f}")
            print(f"  z: {z:.3f}")
        
        # Step counter
        steps = await self.client.read_step_count()
        print(f"\nStep Count: {steps}" if steps is not None else "Step Count: N/A")
        
        # Get heading
        heading = await self.client.read_heading()
        print(f"Compass Heading: {heading:.1f}°" if heading is not None else "Heading: N/A")
        
        # Get raw motion data
        raw_data = await self.client.read_raw_motion()
        if raw_data:
            print("\nRaw Motion Data:")
            print("Accelerometer:")
            print(f"  X: {raw_data['accelerometer']['x']}")
            print(f"  Y: {raw_data['accelerometer']['y']}")
            print(f"  Z: {raw_data['accelerometer']['z']}")
            print("Gyroscope:")
            print(f"  X: {raw_data['gyroscope']['x']}")
            print(f"  Y: {raw_data['gyroscope']['y']}")
            print(f"  Z: {raw_data['gyroscope']['z']}")
            print("Magnetometer:")
            print(f"  X: {raw_data['magnetometer']['x']}")
            print(f"  Y: {raw_data['magnetometer']['y']}")
            print(f"  Z: {raw_data['magnetometer']['z']}")

    async def test_led_controls(self):
        """Test LED features."""
        print("\n=== LED Control ===")
        
        colors = [
            (255, 0, 0, "Red"),
            (0, 255, 0, "Green"),
            (0, 0, 255, "Blue"),
            (255, 0, 255, "Purple"),
            (255, 255, 0, "Yellow"),
            (0, 255, 255, "Cyan")
        ]
        
        # Test constant colors
        print("\nTesting solid colors...")
        for r, g, b, name in colors:
            print(f"\nSetting LED to {name}...")
            await self.client.set_led(mode=1, red=r, green=g, blue=b)
            await asyncio.sleep(1)
        
        # Test breathing mode
        print("\nTesting breathing effect (blue)...")
        await self.client.set_led(mode=2, red=0, green=0, blue=255)
        await asyncio.sleep(5)
        
        # Test one-shot mode
        print("\nTesting one-shot effect (green)...")
        await self.client.set_led(mode=3, red=0, green=255, blue=0)
        await asyncio.sleep(3)
        
        print("\nTurning LED off...")
        await self.client.set_led(mode=0, red=0, green=0, blue=0)

    async def test_sound_features(self):
        """Test sound features."""
        print("\n=== Sound Features ===")
        
        # Configure speaker first
        await self.configure_speaker()
        await asyncio.sleep(1)
        
        # Test all sound patterns
        print("\nTesting all sound patterns...")
        for sound_id in range(1, 9):
            print(f"\nPlaying sound pattern {sound_id}...")
            success = await self.client.play_sound(sound_id)
            print(f"Result: {'✅ Success' if success else '❌ Failed'}")
            await asyncio.sleep(2)

    async def run_all_tests(self):
        """Run all feature tests."""
        print("\n=== Thingy:52 Feature Demo ===")
        
        # Scan and connect
        if not await self.scan_devices():
            return
        if not await self.connect():
            return
        
        try:
            # Run all tests
            await self.test_environmental_sensors()
            await self.test_motion_sensors()
            await self.test_led_controls()
            await self.test_sound_features()
            
            print("\n✅ Demo completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Error during demo: {e}")
        finally:
            # Cleanup
            if self.client.is_connected:
                await self.client.disconnect()
                print("\nDisconnected from device.")

async def main():
    """Main entry point."""
    demo = Thingy52Demo()
    await demo.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())