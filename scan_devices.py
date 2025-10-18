#!/usr/bin/env python3
"""Simple script to scan for Thingy52 devices."""

import asyncio
from src.bluetooth_client import ThingyBLEClient

async def main():
    print("\n=== Scanning for Thingy:52 Devices ===\n")
    client = ThingyBLEClient()
    
    print("Scanning for 10 seconds...")
    devices = await client.scan(timeout=10.0)
    
    if not devices:
        print("\n❌ No Thingy:52 devices found!")
        print("\nTroubleshooting tips:")
        print("1. Make sure your Thingy:52 is powered on (blue LED pulsing)")
        print("2. Check that it's within range (10 meters)")
        print("3. Ensure Bluetooth is enabled on your computer")
        print("4. Try power cycling the Thingy:52")
        return
    
    print(f"\n✅ Found {len(devices)} Thingy:52 device(s):\n")
    for i, device in enumerate(devices, 1):
        print(f"Device {i}:")
        print(f"  Name: {device.name}")
        print(f"  Address: {device.address}")
        print(f"  Signal Strength: {device.rssi} dBm")
        print()

if __name__ == "__main__":
    asyncio.run(main())