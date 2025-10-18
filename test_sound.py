#!/usr/bin/env python3
"""Test script for Thingy52 sound functionality."""

import asyncio
import logging
from src.bluetooth_client import ThingyBLEClient

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

async def configure_speaker(client):
    """Configure speaker settings."""
    if not client.is_connected:
        return False
    
    try:
        # Speaker config characteristic UUID
        SPEAKER_CONFIG_UUID = "EF680502-9B35-4933-9B10-52FFA9740042"
        SPEAKER_MODE_UUID = "EF680503-9B35-4933-9B10-52FFA9740042"
        
        # Set speaker mode to 1 (enable)
        print("Enabling speaker...")
        await client.client.write_gatt_char(SPEAKER_MODE_UUID, bytes([1]))
        await asyncio.sleep(0.5)
        
        # Set volume to maximum (100%)
        print("Setting volume to maximum...")
        await client.client.write_gatt_char(SPEAKER_CONFIG_UUID, bytes([100]))
        print("Speaker configured with maximum volume")
        return True
    except Exception as e:
        print(f"Failed to configure speaker: {e}")
        return False

async def test_sounds(client):
    """Test all sound patterns."""
    print("\n=== Sound Test ===")
    
    # Configure speaker settings
    print("\nConfiguring speaker...")
    if not await configure_speaker(client):
        print("❌ Failed to configure speaker")
        return
    
    await asyncio.sleep(1)  # Wait for settings to take effect
    
    # Try each sound ID
    for sound_id in range(1, 9):
        print(f"\nTesting sound pattern {sound_id}...")
        success = await client.play_sound(sound_id)
        print(f"Result: {'✅ Success' if success else '❌ Failed'}")
        await asyncio.sleep(2)  # Wait longer between sounds

async def main():
    print("\n=== Thingy:52 Sound Test ===")
    client = ThingyBLEClient()
    
    device_address = "6F7B7547-571E-9B48-5370-256B16ACFE2F"
    print(f"\nConnecting to device: {device_address}")
    
    if not await client.connect(device_address):
        print("❌ Connection failed!")
        return
    
    print("✅ Connected successfully!")
    
    try:
        await test_sounds(client)
        print("\n✅ Test completed!")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
    finally:
        await client.disconnect()
        print("Disconnected from device.")

if __name__ == "__main__":
    asyncio.run(main())