#!/usr/bin/env python3
"""Find Thingy by connecting to devices and checking for Thingy services."""

import asyncio
from bleak import BleakScanner, BleakClient

# Thingy:52 service UUIDs
THINGY_SERVICES = {
    "EF680200-9B35-4933-9B10-52FFA9740042": "Environment Service",
    "EF680400-9B35-4933-9B10-52FFA9740042": "Motion Service",
    "EF680300-9B35-4933-9B10-52FFA9740042": "UI Service",
    "EF680500-9B35-4933-9B10-52FFA9740042": "Sound Service",
}


async def check_if_thingy(address: str, name: str) -> bool:
    """Connect to device and check if it has Thingy services."""
    print(f"\nChecking device: {name} ({address})")

    try:
        async with BleakClient(address, timeout=10.0) as client:
            print(f"  ✓ Connected!")

            # Check for Thingy services
            thingy_services_found = []
            for service in client.services:
                uuid = str(service.uuid).upper()
                for thingy_uuid, service_name in THINGY_SERVICES.items():
                    if uuid == thingy_uuid.upper():
                        thingy_services_found.append(service_name)

            if thingy_services_found:
                print(f"  🎉 THIS IS A THINGY! Found services: {', '.join(thingy_services_found)}")
                print(f"\n{'='*80}")
                print(f"✓✓✓ FOUND YOUR THINGY ✓✓✓")
                print(f"{'='*80}")
                print(f"Device Name: {name}")
                print(f"macOS Address (UUID): {address}")
                print(f"\nIMPORTANT: On macOS, use this UUID address, not the MAC address!")
                print(f"Update your tests and config to use: {address}")
                return True
            else:
                print(f"  ✗ Not a Thingy (no Thingy services found)")
                return False

    except Exception as e:
        print(f"  ✗ Could not connect: {e}")
        return False


async def main():
    """Scan and identify Thingy device."""
    print("Scanning for BLE devices and checking for Thingy services...")
    print("This may take a minute as we connect to each device.\n")

    devices = await BleakScanner.discover(timeout=10.0)
    print(f"Found {len(devices)} devices. Checking each one...\n")
    print("=" * 80)

    for device in devices:
        name = device.name or "Unknown"
        address = device.address

        # Try to identify if this is a Thingy
        is_thingy = await check_if_thingy(address, name)

        if is_thingy:
            print(f"\n{'='*80}")
            print("SUCCESS! Save this address for future use.")
            print(f"{'='*80}\n")
            return address

        # Small delay between checks
        await asyncio.sleep(0.5)

    print("\n" + "=" * 80)
    print("✗ No Thingy device found among scanned devices.")
    print("\nTroubleshooting:")
    print("  1. Ensure Thingy is powered on (LED pulsing blue)")
    print("  2. Close all other apps connected to the Thingy")
    print("  3. Try power cycling the Thingy")
    print("  4. Ensure Thingy is not in DFU mode")
    print("=" * 80)
    return None


if __name__ == "__main__":
    thingy_address = asyncio.run(main())
    exit(0 if thingy_address else 1)
