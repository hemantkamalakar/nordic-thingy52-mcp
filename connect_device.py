#!/usr/bin/env python3
"""Script to connect to a specific Thingy52 device."""

import asyncio
from src.bluetooth_client import ThingyBLEClient

async def main():
    print("\n=== Connecting to Thingy:52 Device ===\n")
    client = ThingyBLEClient()
    
    device_address = "6F7B7547-571E-9B48-5370-256B16ACFE2F"
    print(f"Attempting to connect to device: {device_address}")
    
    success = await client.connect(device_address)
    
    if success:
        print("\n✅ Successfully connected to the device!")
        print("\nConnection is ready for sensor reading and control.")
        
        # Keep the connection alive until user interrupts
        print("\nPress Ctrl+C to disconnect and exit...")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n\nDisconnecting...")
            await client.disconnect()
            print("Disconnected. Goodbye!")
    else:
        print("\n❌ Connection failed!")
        print("\nTroubleshooting tips:")
        print("1. Make sure the device is still powered on")
        print("2. Verify the device is not connected to another application")
        print("3. Try power cycling the device")

if __name__ == "__main__":
    asyncio.run(main())