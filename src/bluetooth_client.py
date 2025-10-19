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
    ENVIRONMENT_CONFIG_UUID,
    EULER_UUID,
    HEADING_UUID,
    HUMIDITY_UUID,
    LED_UUID,
    MOTION_CONFIG_UUID,
    ORIENTATION_UUID,
    PRESSURE_UUID,
    QUATERNION_UUID,
    RAW_DATA_UUID,
    SPEAKER_CONFIG_UUID,
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
                logger.debug(f"Found device: {device.name} ({device.address}) RSSI: {advertisement_data.rssi}")
                discovered_devices[device.address] = {
                    "device": device,
                    "rssi": advertisement_data.rssi
                }

        try:
            # Create scanner with detection callback
            scanner = BleakScanner(detection_callback=detection_callback)
            
            # Start scanning with timeout protection
            logger.debug("Starting BLE scan...")
            try:
                await asyncio.wait_for(scanner.start(), timeout=5.0)
            except asyncio.TimeoutError:
                logger.error("Timeout while starting BLE scan")
                return []
            except Exception as e:
                logger.error(f"Error starting BLE scan: {e}")
                return []
            
            # Wait for scan duration
            try:
                await asyncio.sleep(timeout)
            except asyncio.CancelledError:
                logger.warning("Scan interrupted")
            finally:
                # Always attempt to stop scanner
                try:
                    await asyncio.wait_for(scanner.stop(), timeout=5.0)
                except asyncio.TimeoutError:
                    logger.warning("Timeout while stopping BLE scan")
                except Exception as e:
                    logger.warning(f"Error stopping BLE scan: {e}")

            # Process discovered devices
            thingy_devices = []
            for address, info in discovered_devices.items():
                device = info["device"]
                rssi = info["rssi"]
                thingy_devices.append(
                    DeviceInfo(address=device.address, name=device.name, rssi=rssi)
                )
                logger.info(f"Found Thingy: {device.name} ({device.address}) RSSI: {rssi}")

            return thingy_devices

        except Exception as e:
            logger.error(f"Error during BLE scan: {e}")
            return []

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
            logger.error("Cannot read notifications: not connected to device")
            return None

        self._notification_data = None
        self._notification_event = asyncio.Event()

        def notification_handler(sender, data):
            """Handle incoming notification."""
            logger.debug(f"Received notification from {char_uuid}: {data.hex()}")
            self._notification_data = data
            if self._notification_event:
                self._notification_event.set()

        try:
            # Subscribe to notifications with timeout
            try:
                logger.debug(f"Subscribing to notifications for {char_uuid}")
                await asyncio.wait_for(
                    self.client.start_notify(char_uuid, notification_handler),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                logger.error(f"Timeout subscribing to notifications for {char_uuid}")
                return None
            except Exception as e:
                logger.error(f"Error subscribing to notifications for {char_uuid}: {e}")
                return None

            # Wait for notification with timeout
            try:
                logger.debug(f"Waiting for notification from {char_uuid} (timeout: {timeout}s)")
                await asyncio.wait_for(self._notification_event.wait(), timeout=timeout)
                data = self._notification_data
                if data is None:
                    logger.warning(f"Received empty notification from {char_uuid}")
                return data
            except asyncio.TimeoutError:
                logger.warning(f"Timeout waiting for notification from {char_uuid}")
                return None
            except Exception as e:
                logger.error(f"Error receiving notification from {char_uuid}: {e}")
                return None
            finally:
                # Always try to unsubscribe from notifications
                try:
                    logger.debug(f"Unsubscribing from notifications for {char_uuid}")
                    await asyncio.wait_for(
                        self.client.stop_notify(char_uuid),
                        timeout=5.0
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"Timeout unsubscribing from notifications for {char_uuid}")
                except Exception as e:
                    logger.warning(f"Error unsubscribing from notifications for {char_uuid}: {e}")
        except Exception as e:
            logger.error(f"Critical error in notification handling for {char_uuid}: {e}")
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

            # Pressure format: integer (4 bytes little-endian) + decimal (1 byte)
            # The value is already in hPa (hectopascals), not Pascals
            integer = int.from_bytes(data[0:4], "little", signed=True)
            decimal = data[4]
            # Combine: integer part + decimal part (0-99 range)
            pressure_hpa = integer + (decimal / 100.0)
            logger.info(f"Pressure: {pressure_hpa} hPa (raw: int={integer}, dec={decimal})")
            return pressure_hpa
        except Exception as e:
            logger.error(f"Failed to read pressure: {e}", exc_info=True)
            return None

    async def configure_environment_sensors(
        self,
        temp_interval_ms: Optional[int] = None,
        pressure_interval_ms: Optional[int] = None,
        humidity_interval_ms: Optional[int] = None,
        color_interval_ms: Optional[int] = None,
        gas_mode: Optional[int] = None,
    ) -> bool:
        """
        Configure environment sensor parameters using read-modify-write pattern.

        This uses the same approach as the Nordic Node.js library: read current config,
        modify only the requested parameters, then write back.

        Args:
            temp_interval_ms: Temperature update interval in milliseconds (optional)
            pressure_interval_ms: Pressure update interval in milliseconds (optional)
            humidity_interval_ms: Humidity update interval in milliseconds (optional)
            color_interval_ms: Color sensor update interval in milliseconds (optional)
            gas_mode: Gas sensor mode - 1=1s, 2=10s, 3=60s intervals (optional)

        Returns:
            True if successful
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            # Read current configuration (read-modify-write pattern)
            try:
                current_config = await self.client.read_gatt_char(ENVIRONMENT_CONFIG_UUID)
                config = bytearray(current_config)
                logger.debug(f"Current environment config: {config.hex()}")
            except Exception as e:
                logger.warning(f"Could not read current config, using defaults: {e}")
                # If read fails, create default config
                config = bytearray(9)
                config[0:2] = (1000).to_bytes(2, "little")  # temp: 1000ms
                config[2:4] = (1000).to_bytes(2, "little")  # pressure: 1000ms
                config[4:6] = (1000).to_bytes(2, "little")  # humidity: 1000ms
                config[6:8] = (1000).to_bytes(2, "little")  # color: 1000ms
                config[8] = 1  # gas mode: 1s

            # Ensure config is at least 9 bytes
            if len(config) < 9:
                # Pad with default values if needed
                while len(config) < 9:
                    config.append(0)

            # Environment config format (Nordic Thingy:52 specification):
            # Bytes 0-1: Temperature interval (uint16 little-endian)
            # Bytes 2-3: Pressure interval (uint16 little-endian)
            # Bytes 4-5: Humidity interval (uint16 little-endian)
            # Bytes 6-7: Color interval (uint16 little-endian)
            # Byte 8: Gas sensor mode (uint8: 1, 2, or 3)

            # Modify only the parameters that were provided
            if temp_interval_ms is not None:
                config[0:2] = temp_interval_ms.to_bytes(2, "little")
            if pressure_interval_ms is not None:
                config[2:4] = pressure_interval_ms.to_bytes(2, "little")
            if humidity_interval_ms is not None:
                config[4:6] = humidity_interval_ms.to_bytes(2, "little")
            if color_interval_ms is not None:
                config[6:8] = color_interval_ms.to_bytes(2, "little")
            if gas_mode is not None:
                if gas_mode not in [1, 2, 3]:
                    raise ValueError("Gas mode must be 1, 2, or 3")
                config[8] = gas_mode

            # Write back the modified configuration
            await self.client.write_gatt_char(ENVIRONMENT_CONFIG_UUID, bytes(config), response=False)

            logger.debug(f"Environment config written: {config.hex()}")
            logger.info(
                f"Environment sensors configured: "
                f"temp={int.from_bytes(config[0:2], 'little')}ms, "
                f"pressure={int.from_bytes(config[2:4], 'little')}ms, "
                f"humidity={int.from_bytes(config[4:6], 'little')}ms, "
                f"color={int.from_bytes(config[6:8], 'little')}ms, "
                f"gas_mode={config[8]}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to configure environment sensors: {e}")
            return False

    async def read_air_quality(self) -> tuple[Optional[int], Optional[int]]:
        """
        Read air quality sensor (CO2 and TVOC) via notification.

        IMPORTANT: CCS811 Gas Sensor Warm-up Requirements
        --------------------------------------------------
        The Thingy:52 uses a CCS811 gas sensor which requires significant warm-up time:

        - First-time use: 20 minutes to 48 hours for initial calibration
        - After power cycle: 30+ minutes to restore baseline
        - For accurate readings: >100 hours of continuous operation recommended
        - Baseline calibration: Sensor learns air quality baseline over time

        If you see 0 values for CO2/TVOC, this is NORMAL during warm-up period.
        Leave the device powered on for at least 30-60 minutes before expecting
        accurate readings.

        Returns:
            Tuple of (CO2 in ppm, TVOC in ppb)
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            # Configure environment sensors with gas mode for faster readings
            await self.configure_environment_sensors(gas_mode=1)  # 1 second mode
            await asyncio.sleep(1.5)  # Give gas sensor time to warm up

            data = await self._read_via_notification(AIR_QUALITY_UUID, timeout=5.0)

            if data is None:
                logger.error("No air quality data received")
                return (None, None)

            logger.debug(f"Raw air quality data: {data.hex()} (length: {len(data)})")

            if len(data) < 4:
                logger.error(f"Air quality data too short: expected 4 bytes, got {len(data)}")
                return (None, None)

            # Air quality format (CCS811 sensor):
            # Bytes 0-1: eCO2 (equivalent CO2) in ppm - uint16 little-endian
            # Bytes 2-3: TVOC (Total Volatile Organic Compounds) in ppb - uint16 little-endian
            co2 = int.from_bytes(data[0:2], "little", signed=False)
            tvoc = int.from_bytes(data[2:4], "little", signed=False)

            # Log with context about sensor warm-up
            if co2 == 0 and tvoc == 0:
                logger.info(
                    f"Air quality - CO2: {co2} ppm, TVOC: {tvoc} ppb "
                    "(Note: 0 values indicate sensor is warming up - wait 30-60 minutes)"
                )
            else:
                logger.info(f"Air quality - CO2: {co2} ppm, TVOC: {tvoc} ppb")

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

    async def configure_motion_sensors(
        self,
        step_interval_ms: int = 1000,
        temp_comp_interval_ms: int = 5000,
        mag_comp_interval_ms: int = 5000,
        motion_freq_hz: int = 200,
        wake_on_motion: bool = True,
    ) -> bool:
        """
        Configure motion sensor parameters.

        Args:
            step_interval_ms: Step counter update interval in milliseconds
            temp_comp_interval_ms: Temperature compensation interval in milliseconds
            mag_comp_interval_ms: Magnetometer compensation interval in milliseconds
            motion_freq_hz: Motion processing frequency in Hz (max 200Hz)
            wake_on_motion: Enable wake on motion

        Returns:
            True if successful
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            # Motion config format: 9 bytes
            # Bytes 0-1: Step counter interval (uint16 little-endian)
            # Bytes 2-3: Temp compensation interval (uint16 little-endian)
            # Bytes 4-5: Mag compensation interval (uint16 little-endian)
            # Bytes 6-7: Motion frequency (uint16 little-endian)
            # Byte 8: Wake on motion (uint8)

            config = bytearray(9)
            config[0:2] = step_interval_ms.to_bytes(2, "little")
            config[2:4] = temp_comp_interval_ms.to_bytes(2, "little")
            config[4:6] = mag_comp_interval_ms.to_bytes(2, "little")
            config[6:8] = motion_freq_hz.to_bytes(2, "little")
            config[8] = 1 if wake_on_motion else 0

            await self.client.write_gatt_char(MOTION_CONFIG_UUID, bytes(config), response=False)
            logger.info(
                f"Motion sensors configured: step={step_interval_ms}ms, "
                f"freq={motion_freq_hz}Hz, wake={wake_on_motion}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to configure motion sensors: {e}")
            return False

    async def read_step_count(self) -> Optional[int]:
        """Read step counter via notification."""
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            # Ensure motion sensors are configured
            await self.configure_motion_sensors()
            await asyncio.sleep(0.5)  # Give sensors time to initialize

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

    def _rgb_to_color_code(self, red: int, green: int, blue: int) -> int:
        """
        Convert RGB values to Nordic Thingy:52 color code.

        Color codes:
        0x01 = RED, 0x02 = GREEN, 0x03 = YELLOW, 0x04 = BLUE,
        0x05 = PURPLE, 0x06 = CYAN, 0x07 = WHITE

        Args:
            red: Red value (0-255)
            green: Green value (0-255)
            blue: Blue value (0-255)

        Returns:
            Color code (1-7)
        """
        # Define standard colors as (R, G, B) tuples
        colors = {
            0x01: (255, 0, 0),      # RED
            0x02: (0, 255, 0),      # GREEN
            0x03: (255, 255, 0),    # YELLOW
            0x04: (0, 0, 255),      # BLUE
            0x05: (255, 0, 255),    # PURPLE/MAGENTA
            0x06: (0, 255, 255),    # CYAN
            0x07: (255, 255, 255),  # WHITE
        }

        # Find the closest color using Euclidean distance
        min_distance = float('inf')
        closest_code = 0x01

        for code, (r, g, b) in colors.items():
            distance = ((red - r) ** 2 + (green - g) ** 2 + (blue - b) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_code = code

        return closest_code

    async def set_led(
        self, mode: int, red: int, green: int, blue: int, intensity: int = 100, delay: int = 1000
    ) -> bool:
        """
        Set LED color and mode according to Nordic Thingy:52 specification.

        Args:
            mode: LED mode
                0 = Off
                1 = Constant (uses RGB values directly)
                2 = Breathe (uses color code + intensity + delay)
                3 = One-shot (uses color code + intensity + delay)
            red: Red value (0-255)
            green: Green value (0-255)
            blue: Blue value (0-255)
            intensity: Brightness (0-100) for breathe/one-shot, scaling for constant
            delay: Delay in ms for breathe/one-shot modes (minimum 50ms)

        Returns:
            True if successful
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        try:
            # Turn off LED first for all modes except off to ensure clean state transition
            # This prevents color mixing and ensures the new color is displayed correctly
            # IMPORTANT: OFF command requires write-with-response!
            if mode in [1, 2, 3]:
                logger.debug(f"Turning off LED before setting mode {mode}")
                await self.client.write_gatt_char(LED_UUID, bytes([0x00]), response=True)
                await asyncio.sleep(0.15)

            if mode == 0:
                # Turn off LED
                data = bytes([0x00])
            elif mode == 1:
                # Constant mode: 4 bytes [mode, G, R, B]
                # NOTE: Nordic Thingy:52 uses GRB byte order, not RGB!
                # Apply intensity scaling to RGB values
                r = int(red * intensity / 100)
                g = int(green * intensity / 100)
                b = int(blue * intensity / 100)
                # Send in GRB order
                data = bytes([0x01, g, r, b])
                logger.info(f"LED constant mode: RGB({r},{g},{b}) -> GRB bytes")
                logger.info(f"LED bytes being sent: {list(data)} = {data.hex()}")
                logger.info(f"Input values - red:{red}, green:{green}, blue:{blue}, intensity:{intensity}%")
            elif mode == 2:
                # Breathe mode: 5 bytes [mode, color_code, intensity, delay_lsb, delay_msb]
                # Ensure delay is at least 50ms (Nordic requirement)
                delay = max(50, delay)

                # Convert RGB to color code
                color_code = self._rgb_to_color_code(red, green, blue)

                # Scale intensity to 0-255 range
                intensity_byte = int(intensity * 255 / 100)

                # Convert delay to little-endian uint16
                delay_bytes = delay.to_bytes(2, 'little')

                data = bytes([mode, color_code, intensity_byte, delay_bytes[0], delay_bytes[1]])

                color_names = {
                    0x01: "RED", 0x02: "GREEN", 0x03: "YELLOW", 0x04: "BLUE",
                    0x05: "PURPLE", 0x06: "CYAN", 0x07: "WHITE"
                }
                logger.info(f"LED Breathe mode: {color_names.get(color_code, 'UNKNOWN')} "
                           f"intensity={intensity}% delay={delay}ms")
            elif mode == 3:
                # One-shot mode: 3 bytes [mode, color_code, intensity]
                # Convert RGB to color code
                color_code = self._rgb_to_color_code(red, green, blue)

                # Scale intensity to 0-255 range
                intensity_byte = int(intensity * 255 / 100)

                data = bytes([mode, color_code, intensity_byte])

                color_names = {
                    0x01: "RED", 0x02: "GREEN", 0x03: "YELLOW", 0x04: "BLUE",
                    0x05: "PURPLE", 0x06: "CYAN", 0x07: "WHITE"
                }
                logger.info(f"LED One-shot mode: {color_names.get(color_code, 'UNKNOWN')} "
                           f"intensity={intensity}%")
            else:
                raise ValueError(f"Invalid LED mode: {mode}. Must be 0-3.")

            # Write to LED characteristic
            # IMPORTANT: Constant mode (1) and OFF (0) require write-with-response
            # Breathe (2) and One-shot (3) modes use write-without-response
            use_response = mode in [0, 1]
            logger.debug(f"Writing LED mode {mode} with response={use_response}")
            await self.client.write_gatt_char(LED_UUID, data, response=use_response)

            # Small delay after write to ensure it's processed
            await asyncio.sleep(0.05)
            return True
        except Exception as e:
            logger.error(f"Failed to set LED: {e}")
            return False

    async def configure_speaker(self, speaker_mode: int = 0x03, microphone_mode: int = 0x01) -> bool:
        """
        Configure speaker and microphone modes.

        Nordic Thingy:52 configuration format (from Android app):
        - Byte 0: Speaker mode
        - Byte 1: Microphone mode

        Speaker modes:
        - 0x01: Frequency mode (plays tones at specific frequencies)
        - 0x02: PCM mode (for audio streaming, 8kHz sample rate)
        - 0x03: Sample mode (plays preset sound samples using sample IDs 1-8)

        Microphone modes:
        - 0x01: ADPCM mode (compressed audio)
        - 0x02: SPL mode (Sound Pressure Level)

        Args:
            speaker_mode: Speaker mode (0x01=frequency, 0x02=PCM, 0x03=sample)
            microphone_mode: Microphone mode (0x01=ADPCM, 0x02=SPL)

        Returns:
            True if successful
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        if speaker_mode not in [0x01, 0x02, 0x03]:
            raise ValueError("Speaker mode must be 0x01, 0x02, or 0x03")

        if microphone_mode not in [0x01, 0x02]:
            raise ValueError("Microphone mode must be 0x01 or 0x02")

        try:
            # Nordic Thingy:52 sound configuration format (matches Android app)
            # Byte 0: Speaker mode
            # Byte 1: Microphone mode
            # NOTE: Volume is NOT part of configuration! It goes in speaker data for frequency mode.
            config = bytes([speaker_mode, microphone_mode])

            logger.debug(f"Writing sound config: [0x{speaker_mode:02X}, 0x{microphone_mode:02X}] to {SPEAKER_CONFIG_UUID}")
            # Use write-with-response since the characteristic supports it
            await self.client.write_gatt_char(SPEAKER_CONFIG_UUID, config, response=True)
            logger.debug("Sound configuration written successfully")
            # Increased delay for better reliability
            await asyncio.sleep(0.2)
            return True
        except Exception as e:
            logger.error(f"Failed to configure speaker: {e}", exc_info=True)
            return False

    async def play_sound(self, sound_id: int) -> bool:
        """
        Play a preset sound using sample mode (matches Android app implementation).

        Nordic Thingy:52 has 8 preset sound samples stored in firmware.
        This function uses sample mode (0x03) to play preset sounds.

        NOTE: Volume control is not available for sample mode! Volume only applies
        to frequency mode. Preset samples play at a fixed volume.

        Args:
            sound_id: Sound sample ID (1-8)
                Each ID corresponds to a different preset sound/melody

        Returns:
            True if successful
        """
        if not self.is_connected or self.client is None:
            raise ConnectionError("Not connected to a device")

        if sound_id not in range(1, 9):
            raise ValueError("Sound ID must be between 1 and 8")

        try:
            # Configure speaker to sample mode (0x03) with ADPCM microphone mode (0x01)
            # This matches the Android app implementation
            logger.info(f"Playing sound sample {sound_id}...")
            logger.debug(f"Configuring speaker: mode=0x03 (SAMPLE), mic=0x01 (ADPCM)")

            config_success = await self.configure_speaker(speaker_mode=0x03, microphone_mode=0x01)
            if not config_success:
                logger.error("Failed to configure speaker for sample mode")
                return False

            # Delay to ensure configuration is applied (Android app uses queue system)
            await asyncio.sleep(0.1)

            # Send the sample ID as a single byte to speaker data characteristic
            # Android app uses WRITE_TYPE_NO_RESPONSE for speaker data
            sample_data = bytes([sound_id])
            logger.debug(f"Writing sound sample {sound_id} (0x{sound_id:02X}) to speaker data characteristic")

            await self.client.write_gatt_char(SPEAKER_DATA_UUID, sample_data, response=False)

            logger.info(f"Sound {sound_id} sent to device successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to play sound {sound_id}: {e}", exc_info=True)
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
            # Ensure motion sensors are configured
            await self.configure_motion_sensors()
            await asyncio.sleep(0.5)  # Give sensors time to initialize

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
            # Ensure motion sensors are configured
            await self.configure_motion_sensors()
            await asyncio.sleep(0.5)  # Give sensors time to initialize

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
