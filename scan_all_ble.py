#!/usr/bin/env python3
"""Scan for ALL Bluetooth LE devices to diagnose connection issues."""

import asyncio
from bleak import BleakScanner


async def scan_all_devices():
    """Scan for all BLE devices (not just Thingy)."""
    print("Scanning for ALL Bluetooth LE devices...")
    print("This will help diagnose if your Thingy is advertising.\n")
    print("Scanning for 15 seconds...\n")

    devices = await BleakScanner.discover(timeout=15.0, return_adv=True)

    print(f"Found {len(devices)} devices:\n")
    print("=" * 80)

    target_mac = "F4:37:FC:B0:3B:5F"
    found_target = False

    for address, (device, adv_data) in devices.items():
        name = device.name or "Unknown"
        rssi = adv_data.rssi

        # Highlight if this is our target device
        is_target = address.upper() == target_mac.upper()
        if is_target:
            found_target = True
            print(f">>> TARGET DEVICE FOUND <<<")

        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"RSSI: {rssi} dBm")

        # Show service UUIDs if available
        if adv_data.service_uuids:
            print(f"Services: {', '.join(str(uuid) for uuid in adv_data.service_uuids[:3])}")

        # Check for Thingy-related names
        if any(keyword in name.lower() for keyword in ["thingy", "nordic", "dfu"]):
            print("^^^ This looks like a Thingy device! ^^^")

        print("-" * 80)

    print("\n" + "=" * 80)
    if found_target:
        print(f"✓ Found your device at {target_mac}!")
        print("The device is advertising and should be connectable.")
    else:
        print(f"✗ Device {target_mac} was NOT found in scan.")
        print("\nPossible reasons:")
        print("  1. Device is already connected to another app/device")
        print("  2. MAC address may be incorrect or randomized")
        print("  3. Bluetooth privacy/randomization is enabled")
        print("\nLook above for any devices with 'Thingy', 'Nordic', or 'DFU' in the name.")

    return found_target


if __name__ == "__main__":
    found = asyncio.run(scan_all_devices())
    exit(0 if found else 1)
