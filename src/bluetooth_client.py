"""Bluetooth LE client for Nordic Thingy:52."""

import asyncio
import logging
import struct
from typing import List, Optional

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice

from .constants import (
    AIR_QUALITY_UUID,
    BATTERY_LEVEL_UUID,
    COLOR_UUID,
    HUMIDITY_UUID,
    LED_UUID,
    PRESSURE_UUID,
    SPEAKER_DATA_UUID,
    STEP_COUNTER_UUID,
    TEMPERATURE_UUID,
    THINGY_NAME_PATTERNS,
)
from .models import ColorData, DeviceInfo, EnvironmentalData

logger = logging.getLogger(__name__)


class ThingyBLEClient:
    """Bluetooth LE client for Nordic Thingy:52 devices."""

    def __init__(self) -> None:
        """Initialize the BLE client."""
        self.client: Optional[BleakClient] = None
        self.device: Optional[BLEDevice] = None
        self._connected = False
        self._notification_data: Optional[bytes] = None
        self._notification_event: Optional[asyncio.Event] = None

    @property
    def is_connected(self) -> bool:
        """Check if connected to a device."""
        return self._connected and self.client is not None and self.client.is_connected

    async def scan(self, timeout: float = 10.0) -> List[DeviceInfo]:
        """
        Scan for nearby Thingy:52 devices.

        Args:
            timeout: Scan duration in seconds

        Returns:
            List of discovered Thingy devices
        """
        logger.info(f"Scanning for Thingy devices (timeout: {timeout}s)...")

        # Use BleakScanner with callback to get RSSI
        discovered_devices = {}

        def detection_callback(device, advertisement_data):
            """Callback to capture device and RSSI."""
            if device.name and any(pattern in device.name for pattern in THINGY_NAME_PATTERNS):
                discovered_devices[device.address] = {
                    "device": device,
                    "rssi": advertisement_data.rssi
                }

        scanner = BleakScanner(detection_callback=detection_callback)
        await scanner.start()
        await asyncio.sleep(timeout)
        await scanner.stop()

        thingy_devices = []
        for address, info in discovered_devices.items():
            device = info["device"]
            rssi = info["rssi"]
            thingy_devices.append(
                DeviceInfo(address=device.address, name=device.name, rssi=rssi)
            )
            logger.info(f"Found Thingy: {device.name} ({device.address}) RSSI: {rssi}")

        return thingy_devices

    async def connect(self, address: str, timeout: float = 30.0) -> bool:
        """
        Connect to a Thingy device.

        Args:
            address: Bluetooth MAC address
            timeout: Connection timeout in seconds

        Returns:
            True if connection successful
        """
        try:
            logger.info(f"Connecting to {address}...")
            self.client = BleakClient(address, timeout=timeout)
            await self.client.connect()
            self._connected = True
            logger.info(f"Successfully connected to {address}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {address}: {e}")
            self._connected = False
            return False

    async def disconnect(self) -> bool:
        """
        Disconnect from the current device.

        Returns:
            True if disconnection successful
        """
        if self.client and self.is_connected:
            try:
                await self.client.disconnect()
                logger.info("Disconnected successfully")
            except Exception as e:
                logger.error(f"Error during disconnect: {e}")
            finally:
                self._connected = False
                return True
        return False

    async def _read_via_notification(self, char_uuid: str, timeout: float = 5.0) -> Optional[bytes]:
        """
        Read a characteristic via notification (Thingy sensors use notifications, not direct reads).

        Args:
            char_uuid: Characteristic UUID to read
            timeout: Timeout in seconds

        Returns:
            Received data or None on timeout
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        self._notification_data = None
        self._notification_event = asyncio.Event()

        def notification_handler(sender, data):
            """Handle incoming notification."""
            self._notification_data = data
            if self._notification_event:
                self._notification_event.set()

        try:
            # Subscribe to notifications
            await self.client.start_notify(char_uuid, notification_handler)

            # Wait for notification with timeout
            try:
                await asyncio.wait_for(self._notification_event.wait(), timeout=timeout)
                data = self._notification_data
            except asyncio.TimeoutError:
                logger.warning(f"Timeout waiting for notification from {char_uuid}")
                data = None
            finally:
                # Stop notifications
                await self.client.stop_notify(char_uuid)

            return data
        except Exception as e:
            logger.error(f"Failed to read via notification from {char_uuid}: {e}")
            return None

    async def read_temperature(self) -> Optional[float]:
        """Read temperature sensor via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(TEMPERATURE_UUID, timeout=5.0)

            if data is None:
                logger.error("No temperature data received")
                return None

            logger.debug(f"Raw temperature data: {data.hex()} (length: {len(data)})")

            if len(data) < 2:
                logger.error(f"Temperature data too short: expected 2 bytes, got {len(data)}")
                return None

            # Thingy:52 temperature format: integer (1 byte) + decimal (1 byte)
            integer = int.from_bytes([data[0]], "little", signed=True)
            decimal = data[1]
            temp = float(f"{integer}.{decimal:02d}")
            logger.info(f"Temperature: {temp}°C")
            return temp
        except Exception as e:
            logger.error(f"Failed to read temperature: {e}", exc_info=True)
            return None

    async def read_humidity(self) -> Optional[float]:
        """Read humidity sensor via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(HUMIDITY_UUID, timeout=5.0)

            if data is None:
                logger.error("No humidity data received")
                return None

            logger.debug(f"Raw humidity data: {data.hex()} (length: {len(data)})")

            if len(data) < 1:
                logger.error(f"Humidity data empty")
                return None

            # Humidity is single unsigned byte
            humidity = float(data[0])
            logger.info(f"Humidity: {humidity}%")
            return humidity
        except Exception as e:
            logger.error(f"Failed to read humidity: {e}", exc_info=True)
            return None

    async def read_pressure(self) -> Optional[float]:
        """Read pressure sensor via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(PRESSURE_UUID, timeout=5.0)

            if data is None:
                logger.error("No pressure data received")
                return None

            logger.debug(f"Raw pressure data: {data.hex()} (length: {len(data)})")

            if len(data) < 5:
                logger.error(f"Pressure data too short: expected 5 bytes, got {len(data)}")
                return None

            # Pressure: integer (4 bytes) + decimal (1 byte) in Pascal
            integer = int.from_bytes(data[0:4], "little", signed=False)
            decimal = data[4]
            pressure_pa = float(f"{integer}.{decimal:02d}")
            # Convert to hPa
            pressure_hpa = pressure_pa / 100.0
            logger.info(f"Pressure: {pressure_hpa} hPa")
            return pressure_hpa
        except Exception as e:
            logger.error(f"Failed to read pressure: {e}", exc_info=True)
            return None

    async def read_air_quality(self) -> tuple[Optional[int], Optional[int]]:
        """Read air quality sensor (CO2 and TVOC) via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(AIR_QUALITY_UUID, timeout=5.0)

            if data is None:
                logger.error("No air quality data received")
                return (None, None)

            # CO2 (eCO2): 2 bytes, TVOC: 2 bytes
            co2 = int.from_bytes(data[0:2], "little", signed=False)
            tvoc = int.from_bytes(data[2:4], "little", signed=False)
            logger.debug(f"Air quality - CO2: {co2} ppm, TVOC: {tvoc} ppb")
            return (co2, tvoc)
        except Exception as e:
            logger.error(f"Failed to read air quality: {e}")
            return (None, None)

    async def read_color(self) -> Optional[ColorData]:
        """Read color sensor via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(COLOR_UUID, timeout=5.0)

            if data is None:
                logger.error("No color sensor data received")
                return None

            # RGBC: 2 bytes each
            red = int.from_bytes(data[0:2], "little", signed=False)
            green = int.from_bytes(data[2:4], "little", signed=False)
            blue = int.from_bytes(data[4:6], "little", signed=False)
            clear = int.from_bytes(data[6:8], "little", signed=False)
            return ColorData(red=red, green=green, blue=blue, clear=clear)
        except Exception as e:
            logger.error(f"Failed to read color sensor: {e}")
            return None

    async def read_battery(self) -> Optional[int]:
        """Read battery level."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self.client.read_gatt_char(BATTERY_LEVEL_UUID)
            battery = int(data[0])
            logger.debug(f"Battery: {battery}%")
            return battery
        except Exception as e:
            logger.error(f"Failed to read battery: {e}")
            return None

    async def read_step_count(self) -> Optional[int]:
        """Read step counter via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(STEP_COUNTER_UUID, timeout=5.0)

            if data is None:
                logger.error("No step count data received")
                return None

            steps = int.from_bytes(data[0:4], "little", signed=False)
            logger.debug(f"Steps: {steps}")
            return steps
        except Exception as e:
            logger.error(f"Failed to read step count: {e}")
            return None

    async def read_all_environmental(self) -> EnvironmentalData:
        """Read all environmental sensors at once."""
        if not self.is_connected:
            raise ConnectionError("Not connected to a device")

        temp = await self.read_temperature()
        humidity = await self.read_humidity()
        pressure = await self.read_pressure()
        co2, tvoc = await self.read_air_quality()

        return EnvironmentalData(
            temperature=temp, humidity=humidity, pressure=pressure, co2=co2, tvoc=tvoc
        )

    async def set_led(
        self, mode: int, red: int, green: int, blue: int, intensity: int = 100, delay: int = 0
    ) -> bool:
        """
        Set LED color and mode.

        Args:
            mode: 1=constant, 2=breathe, 3=one-shot
            red: Red value (0-255)
            green: Green value (0-255)
            blue: Blue value (0-255)
            intensity: Brightness (0-100)
            delay: Delay in ms for breathe/one-shot modes

        Returns:
            True if successful
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            # Apply intensity scaling
            r = int(red * intensity / 100)
            g = int(green * intensity / 100)
            b = int(blue * intensity / 100)

            # LED data format: mode (1 byte) + R (1) + G (1) + B (1) + delay (1 byte)
            # Note: delay is in units of 50ms, so delay=20 = 1 second
            delay_byte = min(255, delay // 50) if delay > 0 else 0
            data = bytes([mode, r, g, b, delay_byte])
            await self.client.write_gatt_char(LED_UUID, data)
            logger.info(f"LED set to RGB({r},{g},{b}) mode={mode}")
            return True
        except Exception as e:
            logger.error(f"Failed to set LED: {e}")
            return False

    async def play_sound(self, sound_id: int) -> bool:
        """
        Play a preset sound.

        Args:
            sound_id: Sound ID (1-8)

        Returns:
            True if successful
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        if sound_id not in range(1, 9):
            raise ValueError("Sound ID must be between 1 and 8")

        try:
            # Speaker data format: sound_id (1 byte)
            data = bytes([sound_id])
            # Speaker characteristic requires write-without-response
            await self.client.write_gatt_char(SPEAKER_DATA_UUID, data, response=False)
            logger.info(f"Playing sound {sound_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to play sound: {e}")
            return False
