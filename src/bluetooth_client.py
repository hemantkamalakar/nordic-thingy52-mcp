"""Bluetooth LE client for Nordic Thingy:52."""

import asyncio
import logging
from typing import List, Optional

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice

from .constants import (
    AIR_QUALITY_UUID,
    BATTERY_LEVEL_UUID,
    COLOR_UUID,
    EULER_UUID,
    HEADING_UUID,
    HUMIDITY_UUID,
    LED_UUID,
    ORIENTATION_UUID,
    PRESSURE_UUID,
    QUATERNION_UUID,
    RAW_DATA_UUID,
    SPEAKER_DATA_UUID,
    SPEAKER_STATUS_UUID,
    STEP_COUNTER_UUID,
    TAP_UUID,
    TEMPERATURE_UUID,
    THINGY_NAME_PATTERNS,
)
from .models import ColorData, DeviceInfo, EnvironmentalData

logger = logging.getLogger(__name__)


class ThingyBLEClient:
    """Bluetooth LE client for Nordic Thingy:52 devices."""

    def __init__(
        self,
        auto_reconnect: bool = True,
        max_reconnect_attempts: int = 10,
        initial_retry_delay: float = 1.0,
        max_retry_delay: float = 30.0,
    ) -> None:
        """
        Initialize the BLE client.

        Args:
            auto_reconnect: Enable automatic reconnection on unexpected disconnects
            max_reconnect_attempts: Maximum number of reconnection attempts (0 = infinite)
            initial_retry_delay: Initial delay between retry attempts in seconds
            max_retry_delay: Maximum delay between retry attempts in seconds
        """
        self.client: Optional[BleakClient] = None
        self.device: Optional[BLEDevice] = None
        self._connected = False
        self._notification_data: Optional[bytes] = None
        self._notification_event: Optional[asyncio.Event] = None

        # Auto-reconnect configuration
        self.auto_reconnect = auto_reconnect
        self.max_reconnect_attempts = max_reconnect_attempts
        self.initial_retry_delay = initial_retry_delay
        self.max_retry_delay = max_retry_delay

        # Connection state tracking
        self._last_address: Optional[str] = None
        self._manual_disconnect = False
        self._reconnecting = False
        self._reconnect_task: Optional[asyncio.Task] = None
        self._retry_count = 0

    @property
    def is_connected(self) -> bool:
        """Check if connected to a device."""
        return self._connected and self.client is not None and self.client.is_connected

    @property
    def is_reconnecting(self) -> bool:
        """Check if currently attempting to reconnect."""
        return self._reconnecting

    @property
    def connection_state(self) -> str:
        """
        Get the current connection state.

        Returns:
            One of: 'connected', 'disconnected', 'reconnecting', 'manual_disconnect'
        """
        if self.is_connected:
            return "connected"
        elif self._reconnecting:
            return "reconnecting"
        elif self._manual_disconnect:
            return "manual_disconnect"
        else:
            return "disconnected"

    def _on_disconnect(self, client: BleakClient) -> None:
        """
        Callback when device disconnects.

        Args:
            client: The BleakClient that disconnected
        """
        logger.warning(f"Device disconnected: {client.address}")
        self._connected = False

        # Only trigger auto-reconnect if it wasn't a manual disconnect
        if not self._manual_disconnect and self.auto_reconnect and not self._reconnecting:
            logger.info("Unexpected disconnect - starting auto-reconnect...")
            # Schedule reconnection in the background
            try:
                loop = asyncio.get_event_loop()
                self._reconnect_task = loop.create_task(self._auto_reconnect())
            except RuntimeError:
                logger.error("Cannot schedule reconnection: no event loop running")

    async def _auto_reconnect(self) -> None:
        """
        Automatically attempt to reconnect with exponential backoff.
        """
        if not self._last_address:
            logger.error("Cannot auto-reconnect: no previous address stored")
            return

        self._reconnecting = True
        self._retry_count = 0
        delay = self.initial_retry_delay

        logger.info(
            f"Starting auto-reconnect to {self._last_address} "
            f"(max attempts: {'infinite' if self.max_reconnect_attempts == 0 else self.max_reconnect_attempts})"
        )

        while True:
            # Check if we've exceeded max attempts
            if self.max_reconnect_attempts > 0 and self._retry_count >= self.max_reconnect_attempts:
                logger.error(
                    f"Auto-reconnect failed after {self._retry_count} attempts. Giving up."
                )
                self._reconnecting = False
                return

            self._retry_count += 1
            logger.info(
                f"Reconnection attempt {self._retry_count}"
                f"{f'/{self.max_reconnect_attempts}' if self.max_reconnect_attempts > 0 else ''} "
                f"in {delay:.1f}s..."
            )

            # Wait before attempting reconnection
            await asyncio.sleep(delay)

            # Attempt to reconnect
            try:
                logger.info(f"Attempting to reconnect to {self._last_address}...")
                # Don't use the public connect() method to avoid recursion issues
                # Create a new client and attempt connection
                self.client = BleakClient(self._last_address, disconnected_callback=self._on_disconnect)
                await self.client.connect()
                self._connected = True
                self._reconnecting = False
                self._retry_count = 0
                logger.info(f"Successfully reconnected to {self._last_address}")
                return
            except Exception as e:
                logger.warning(f"Reconnection attempt {self._retry_count} failed: {e}")

            # Calculate next delay with exponential backoff
            delay = min(delay * 2, self.max_retry_delay)

    async def cancel_reconnect(self) -> None:
        """Cancel any ongoing reconnection attempts."""
        if self._reconnect_task and not self._reconnect_task.done():
            logger.info("Cancelling reconnection attempts...")
            self._reconnect_task.cancel()
            try:
                await self._reconnect_task
            except asyncio.CancelledError:
                pass
        self._reconnecting = False
        self._retry_count = 0

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
        # Cancel any ongoing reconnection attempts
        await self.cancel_reconnect()

        try:
            logger.info(f"Connecting to {address}...")
            # Create client with disconnect callback
            self.client = BleakClient(
                address, timeout=timeout, disconnected_callback=self._on_disconnect
            )
            await self.client.connect()
            self._connected = True
            self._last_address = address
            self._manual_disconnect = False
            logger.info(f"Successfully connected to {address}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {address}: {e}")
            self._connected = False
            return False

    async def disconnect(self) -> bool:
        """
        Disconnect from the current device.

        This is a manual disconnect, so auto-reconnect will not be triggered.

        Returns:
            True if disconnection successful
        """
        # Mark as manual disconnect to prevent auto-reconnect
        self._manual_disconnect = True

        # Cancel any ongoing reconnection attempts
        await self.cancel_reconnect()

        if self.client and self.is_connected:
            try:
                await self.client.disconnect()
                logger.info("Disconnected successfully (manual)")
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
                logger.error("Humidity data empty")
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
        """Read color sensor via notification (includes light intensity in clear channel)."""
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

            # Clear channel represents light intensity (approximation of lux)
            # Nordic Thingy uses clear channel as ambient light sensor
            logger.debug(f"Color: R={red}, G={green}, B={blue}, Light={clear} lux")

            return ColorData(red=red, green=green, blue=blue, clear=clear)
        except Exception as e:
            logger.error(f"Failed to read color sensor: {e}")
            return None

    async def read_light_intensity(self) -> Optional[int]:
        """
        Read light intensity (lux) from color sensor.

        Note: This uses the clear channel of the color sensor.
        """
        color_data = await self.read_color()
        if color_data:
            return color_data.clear
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
            delay: Delay in ms for breathe/one-shot modes (ignored - not supported by Thingy LED characteristic)

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

            # LED data format: mode (1 byte) + R (1) + G (1) + B (1) = 4 bytes total
            # Note: Thingy:52 LED characteristic expects exactly 4 bytes
            data = bytes([mode, r, g, b])
            await self.client.write_gatt_char(LED_UUID, data)
            logger.info(f"LED set to RGB({r},{g},{b}) mode={mode}")
            return True
        except Exception as e:
            logger.error(f"Failed to set LED: {e}")
            return False

    async def configure_speaker(self, volume: int = 100) -> bool:
        """
        Configure speaker settings.

        Args:
            volume: Speaker volume (0-100)

        Returns:
            True if successful
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        if not 0 <= volume <= 100:
            raise ValueError("Volume must be between 0 and 100")

        try:
            # Enable speaker
            logger.info("Enabling speaker...")
            await self.client.write_gatt_char(SPEAKER_STATUS_UUID, bytes([1]), response=False)
            await asyncio.sleep(0.5)

            # Set volume
            logger.info(f"Setting volume to {volume}%...")
            await self.client.write_gatt_char(SPEAKER_STATUS_UUID, bytes([volume]), response=False)
            logger.info("✅ Speaker configured successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to configure speaker: {e}")
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

    # === Advanced Sensor Methods ===

    async def read_quaternion(self) -> Optional[tuple[float, float, float, float]]:
        """Read quaternion orientation data via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(QUATERNION_UUID, timeout=5.0)

            if data is None:
                logger.error("No quaternion data received")
                return None

            # Quaternion: 4 floats (w, x, y, z), 4 bytes each = 16 bytes total
            # Format: signed 32-bit fixed point with 30 fractional bits
            w = int.from_bytes(data[0:4], "little", signed=True) / (1 << 30)
            x = int.from_bytes(data[4:8], "little", signed=True) / (1 << 30)
            y = int.from_bytes(data[8:12], "little", signed=True) / (1 << 30)
            z = int.from_bytes(data[12:16], "little", signed=True) / (1 << 30)

            logger.debug(f"Quaternion: w={w}, x={x}, y={y}, z={z}")
            return (w, x, y, z)
        except Exception as e:
            logger.error(f"Failed to read quaternion: {e}")
            return None

    async def read_euler_angles(self) -> Optional[tuple[float, float, float]]:
        """Read Euler angles (roll, pitch, yaw) via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(EULER_UUID, timeout=5.0)

            if data is None:
                logger.error("No Euler angle data received")
                return None

            # Euler angles: 3 signed 32-bit integers in degrees * 65536
            roll = int.from_bytes(data[0:4], "little", signed=True) / 65536.0
            pitch = int.from_bytes(data[4:8], "little", signed=True) / 65536.0
            yaw = int.from_bytes(data[8:12], "little", signed=True) / 65536.0

            logger.debug(f"Euler angles: roll={roll}°, pitch={pitch}°, yaw={yaw}°")
            return (roll, pitch, yaw)
        except Exception as e:
            logger.error(f"Failed to read Euler angles: {e}")
            return None

    async def read_heading(self) -> Optional[float]:
        """Read compass heading via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(HEADING_UUID, timeout=5.0)

            if data is None:
                logger.error("No heading data received")
                return None

            # Heading: signed 32-bit integer in degrees * 65536
            heading = int.from_bytes(data[0:4], "little", signed=True) / 65536.0

            # Normalize to 0-360
            heading = heading % 360
            if heading < 0:
                heading += 360

            logger.debug(f"Heading: {heading}°")
            return heading
        except Exception as e:
            logger.error(f"Failed to read heading: {e}")
            return None

    async def read_tap_event(self) -> Optional[dict]:
        """
        Subscribe to tap detection events.

        Note: This is an event-based sensor that requires continuous monitoring.
        Use this for event-driven applications.
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(TAP_UUID, timeout=10.0)

            if data is None:
                logger.warning("No tap event within timeout")
                return None

            # Tap data format: direction (1 byte) + count (1 byte)
            direction = data[0]  # 1=X+, 2=X-, 3=Y+, 4=Y-, 5=Z+, 6=Z-
            count = data[1]  # 1=single tap, 2=double tap

            direction_map = {
                1: "X+", 2: "X-", 3: "Y+", 4: "Y-", 5: "Z+", 6: "Z-"
            }

            tap_type = "double" if count == 2 else "single"

            logger.info(f"Tap detected: {tap_type} tap on {direction_map.get(direction, 'unknown')}")
            return {
                "type": tap_type,
                "direction": direction_map.get(direction, "unknown"),
                "count": count,
            }
        except Exception as e:
            logger.error(f"Failed to read tap event: {e}")
            return None

    async def read_orientation(self) -> Optional[int]:
        """Read device orientation via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(ORIENTATION_UUID, timeout=5.0)

            if data is None:
                logger.error("No orientation data received")
                return None

            # Orientation: 1 byte (0=portrait, 1=landscape, 2=reverse portrait, 3=reverse landscape)
            orientation = data[0]

            orientation_map = {
                0: "portrait",
                1: "landscape",
                2: "reverse_portrait",
                3: "reverse_landscape",
            }

            logger.debug(f"Orientation: {orientation_map.get(orientation, 'unknown')}")
            return orientation
        except Exception as e:
            logger.error(f"Failed to read orientation: {e}")
            return None

    async def read_raw_motion(self) -> Optional[dict]:
        """Read raw accelerometer, gyroscope, and magnetometer data via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            data = await self._read_via_notification(RAW_DATA_UUID, timeout=5.0)

            if data is None:
                logger.error("No raw motion data received")
                return None

            # Raw data format: accel (3x2 bytes) + gyro (3x2 bytes) + compass (3x2 bytes)
            # All values are signed 16-bit integers
            accel_x = int.from_bytes(data[0:2], "little", signed=True)
            accel_y = int.from_bytes(data[2:4], "little", signed=True)
            accel_z = int.from_bytes(data[4:6], "little", signed=True)

            gyro_x = int.from_bytes(data[6:8], "little", signed=True)
            gyro_y = int.from_bytes(data[8:10], "little", signed=True)
            gyro_z = int.from_bytes(data[10:12], "little", signed=True)

            compass_x = int.from_bytes(data[12:14], "little", signed=True)
            compass_y = int.from_bytes(data[14:16], "little", signed=True)
            compass_z = int.from_bytes(data[16:18], "little", signed=True)

            return {
                "accelerometer": {"x": accel_x, "y": accel_y, "z": accel_z},
                "gyroscope": {"x": gyro_x, "y": gyro_y, "z": gyro_z},
                "magnetometer": {"x": compass_x, "y": compass_y, "z": compass_z},
            }
        except Exception as e:
            logger.error(f"Failed to read raw motion data: {e}")
            return None
