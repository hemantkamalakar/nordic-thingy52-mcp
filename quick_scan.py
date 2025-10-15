#!/usr/bin/env python3
"""Quick 5-second scan showing all devices with names."""

import asyncio
from bleak import BleakScanner


async def quick_scan():
    print("Quick 5-second scan starting NOW...")
    print("(Make sure Thingy was just powered on)\n")

    devices = await BleakScanner.discover(timeout=5.0, return_adv=True)

    print(f"Found {len(devices)} devices:\n")

    for address, (device, adv_data) in devices.items():
        name = device.name or "Unknown"
        rssi = adv_data.rssi

        # Highlight devices with names (not "Unknown")
        marker = ">>>" if name != "Unknown" else "   "

        print(f"{marker} {name}")
        print(f"    Address: {address}")
        print(f"    RSSI: {rssi} dBm")

        # Check for Thingy keywords
        if any(keyword in name.lower() for keyword in ["thingy", "nordic", "dfu"]):
            print(f"    *** LOOKS LIKE A THINGY! ***")

        print()


if __name__ == "__main__":
    asyncio.run(quick_scan())
