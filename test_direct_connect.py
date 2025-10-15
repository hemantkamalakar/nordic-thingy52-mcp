#!/usr/bin/env python3
"""Test direct connection to a Thingy by MAC address (skip scanning)."""

import asyncio
import sys
from src.bluetooth_client import ThingyBLEClient


async def test_direct_connection(mac_address: str):
    """Test direct connection without scanning."""
    print(f"Attempting direct connection to {mac_address}...")
    print("This bypasses scanning and tries to connect directly.\n")

    client = ThingyBLEClient()

    try:
        print("Connecting (this may take up to 20 seconds)...")
        connected = await client.connect(mac_address, timeout=20.0)

        if connected:
            print("✓ Successfully connected!")
            print("\nReading battery level...")
            battery = await client.read_battery()
            if battery:
                print(f"✓ Battery: {battery}%")

            print("\nReading temperature...")
            temp = await client.read_temperature()
            if temp:
                print(f"✓ Temperature: {temp}°C")

            print("\nDisconnecting...")
            await client.disconnect()
            print("✓ Disconnected")
            return True
        else:
            print("✗ Connection failed!")
            print("\nPossible reasons:")
            print("  1. Device is connected to another app")
            print("  2. Device is powered off")
            print("  3. Device is out of range")
            print("  4. MAC address is incorrect")
            print("\nTroubleshooting:")
            print("  - Close the Nordic Thingy mobile app completely")
            print("  - Close nRF Connect if open")
            print("  - Power cycle the Thingy (off, wait 3s, on)")
            print("  - Ensure Thingy LED is pulsing blue")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_direct_connect.py <MAC_ADDRESS>")
        print("Example: python3 test_direct_connect.py F4:37:FC:B0:3B:5F")
        sys.exit(1)

    mac = sys.argv[1]
    success = asyncio.run(test_direct_connection(mac))
    sys.exit(0 if success else 1)
