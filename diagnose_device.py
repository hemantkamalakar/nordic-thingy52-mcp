#!/usr/bin/env python3
"""
Diagnostic tool to inspect available services and characteristics on a Thingy device.

This helps identify if the device is in DFU mode or normal mode.

Usage:
    python3 diagnose_device.py
"""

import asyncio
from src.bluetooth_client import ThingyBLEClient


async def main():
    print("=" * 70)
    print("  Thingy:52 Device Diagnostic Tool")
    print("=" * 70)

    client = ThingyBLEClient()

    # Step 1: Scan
    print("\n[1/3] Scanning for devices...")
    devices = await client.scan(timeout=10.0)

    if not devices:
        print("❌ No Thingy devices found!")
        return

    device = devices[0]
    print(f"✓ Found: {device.name}")
    print(f"  Address: {device.address}")
    print(f"  RSSI: {device.rssi} dBm")

    # Check if device is in DFU mode
    if "Dfu" in device.name or "DFU" in device.name:
        print("\n⚠️  WARNING: Device appears to be in DFU (firmware update) mode!")
        print("   Device name contains 'Dfu' which indicates DFU mode.")
        print("\n   In DFU mode, sensor services are NOT available.")
        print("   Only firmware update services are exposed.")

    # Step 2: Connect
    print(f"\n[2/3] Connecting to {device.address}...")
    connected = await client.connect(device.address, timeout=20.0)

    if not connected:
        print("❌ Connection failed!")
        return

    print("✓ Connected successfully")

    # Step 3: Discover services
    print("\n[3/3] Discovering services and characteristics...")
    print("\nAvailable Services:")
    print("-" * 70)

    if client.client is None:
        print("❌ Client is None!")
        return

    # Get all services
    for service in client.client.services:
        print(f"\n📦 Service: {service.uuid}")
        print(f"   Description: {service.description}")

        # Check if it's a DFU service
        if "DFU" in service.description.upper() or "FE59" in str(service.uuid):
            print("   ⚠️  This is a DFU (firmware update) service!")

        # List characteristics
        for char in service.characteristics:
            print(f"   └─ Characteristic: {char.uuid}")
            print(f"      Properties: {', '.join(char.properties)}")
            if char.description != "Unknown":
                print(f"      Description: {char.description}")

    print("\n" + "=" * 70)

    # Check for expected Thingy services
    print("\n📋 Checking for expected Thingy:52 services...")

    expected_services = {
        "EF680200-9B35-4933-9B10-52FFA9740042": "Environment Service",
        "EF680400-9B35-4933-9B10-52FFA9740042": "Motion Service",
        "EF680300-9B35-4933-9B10-52FFA9740042": "UI Service",
        "EF680500-9B35-4933-9B10-52FFA9740042": "Sound Service",
    }

    found_services = [str(s.uuid) for s in client.client.services]
    missing_services = []

    for uuid, name in expected_services.items():
        if uuid.lower() in [s.lower() for s in found_services]:
            print(f"✓ {name}: Found")
        else:
            print(f"✗ {name}: MISSING")
            missing_services.append(name)

    # Diagnosis
    print("\n" + "=" * 70)
    print("  Diagnosis")
    print("=" * 70)

    if missing_services:
        print("\n❌ Missing expected Thingy:52 services!")
        print(f"   Missing: {', '.join(missing_services)}")

        if "Dfu" in device.name or "DFU" in device.name:
            print("\n🔧 FIX: Your Thingy is in DFU mode")
            print("\n   To exit DFU mode and return to normal operation:")
            print("   1. Power off the Thingy (slide power switch)")
            print("   2. Wait 3 seconds")
            print("   3. Power on the Thingy")
            print("   4. The LED should pulse BLUE (not other colors)")
            print("   5. The device name should be 'Thingy' (not 'ThingyDfu')")
            print("\n   If it still shows 'ThingyDfu' after restart:")
            print("   - Try pressing the button while powering on")
            print("   - Or update firmware using the Nordic Thingy app")
        else:
            print("\n🔧 Possible issues:")
            print("   1. Device firmware is corrupted or outdated")
            print("   2. Device needs to be reset")
            print("   3. Wrong device type (not a Thingy:52)")
    else:
        print("\n✅ All expected services found!")
        print("   Device is in normal operation mode.")
        print("   All sensors should be accessible.")

    # Disconnect
    await client.disconnect()
    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
