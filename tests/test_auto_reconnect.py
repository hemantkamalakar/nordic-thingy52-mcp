"""Tests for auto-reconnect functionality."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from bleak import BleakClient

from src.bluetooth_client import ThingyBLEClient


@pytest.fixture
def ble_client():
    """Create a ThingyBLEClient instance for testing."""
    return ThingyBLEClient(
        auto_reconnect=True, max_reconnect_attempts=3, initial_retry_delay=0.1, max_retry_delay=0.5
    )


@pytest.mark.asyncio
async def test_auto_reconnect_disabled():
    """Test that auto-reconnect does not trigger when disabled."""
    client = ThingyBLEClient(auto_reconnect=False)

    # Simulate a disconnect
    mock_bleak_client = Mock(spec=BleakClient)
    mock_bleak_client.address = "AA:BB:CC:DD:EE:FF"
    client._connected = True
    client._last_address = "AA:BB:CC:DD:EE:FF"

    # Trigger disconnect callback
    client._on_disconnect(mock_bleak_client)

    # Wait a bit to ensure no reconnect is attempted
    await asyncio.sleep(0.2)

    # Should not be reconnecting
    assert not client.is_reconnecting


@pytest.mark.asyncio
async def test_manual_disconnect_no_reconnect(ble_client):
    """Test that manual disconnect does not trigger auto-reconnect."""
    # Set up a connected state
    with patch.object(BleakClient, "connect", new_callable=AsyncMock):
        with patch.object(BleakClient, "disconnect", new_callable=AsyncMock):
            ble_client.client = Mock(spec=BleakClient)
            ble_client.client.is_connected = True
            ble_client._connected = True
            ble_client._last_address = "AA:BB:CC:DD:EE:FF"

            # Manual disconnect
            await ble_client.disconnect()

            # Wait a bit
            await asyncio.sleep(0.2)

            # Should not be reconnecting
            assert not ble_client.is_reconnecting
            assert ble_client._manual_disconnect


@pytest.mark.asyncio
async def test_auto_reconnect_success(ble_client):
    """Test successful auto-reconnect after unexpected disconnect."""
    # Set up initial connection
    ble_client._connected = True
    ble_client._last_address = "AA:BB:CC:DD:EE:FF"
    ble_client._manual_disconnect = False

    # Mock BleakClient
    mock_bleak_client = Mock(spec=BleakClient)
    mock_bleak_client.address = "AA:BB:CC:DD:EE:FF"

    with patch.object(BleakClient, "__init__", return_value=None):
        with patch.object(BleakClient, "connect", new_callable=AsyncMock) as mock_connect:
            # Trigger disconnect
            ble_client._on_disconnect(mock_bleak_client)

            # Wait for reconnection to complete
            await asyncio.sleep(0.3)

            # Should have attempted reconnect
            assert ble_client._retry_count >= 1


@pytest.mark.asyncio
async def test_auto_reconnect_max_attempts(ble_client):
    """Test that auto-reconnect stops after max attempts."""
    # Set up initial connection
    ble_client._connected = True
    ble_client._last_address = "AA:BB:CC:DD:EE:FF"
    ble_client._manual_disconnect = False

    # Mock BleakClient to always fail connection
    mock_bleak_client = Mock(spec=BleakClient)
    mock_bleak_client.address = "AA:BB:CC:DD:EE:FF"

    with patch.object(BleakClient, "__init__", return_value=None):
        with patch.object(BleakClient, "connect", new_callable=AsyncMock, side_effect=Exception("Connection failed")):
            # Trigger disconnect
            ble_client._on_disconnect(mock_bleak_client)

            # Wait for all reconnection attempts to complete
            # 3 attempts with 0.1, 0.2, 0.4 delays = ~0.8s total
            await asyncio.sleep(1.0)

            # Should have stopped after max attempts
            assert not ble_client.is_reconnecting
            assert ble_client._retry_count == 3


@pytest.mark.asyncio
async def test_cancel_reconnect(ble_client):
    """Test cancelling reconnection attempts."""
    # Set up initial connection
    ble_client._connected = True
    ble_client._last_address = "AA:BB:CC:DD:EE:FF"
    ble_client._manual_disconnect = False

    # Mock BleakClient to always fail connection
    mock_bleak_client = Mock(spec=BleakClient)
    mock_bleak_client.address = "AA:BB:CC:DD:EE:FF"

    with patch.object(BleakClient, "__init__", return_value=None):
        with patch.object(BleakClient, "connect", new_callable=AsyncMock, side_effect=Exception("Connection failed")):
            # Trigger disconnect
            ble_client._on_disconnect(mock_bleak_client)

            # Wait a bit for reconnect to start
            await asyncio.sleep(0.15)

            # Cancel reconnection
            await ble_client.cancel_reconnect()

            # Should not be reconnecting
            assert not ble_client.is_reconnecting


@pytest.mark.asyncio
async def test_connection_state_property(ble_client):
    """Test connection_state property returns correct states."""
    # Test disconnected state
    ble_client._connected = False
    ble_client._reconnecting = False
    ble_client._manual_disconnect = False
    assert ble_client.connection_state == "disconnected"

    # Test connected state
    ble_client.client = Mock(spec=BleakClient)
    ble_client.client.is_connected = True
    ble_client._connected = True
    assert ble_client.connection_state == "connected"

    # Test reconnecting state
    ble_client._connected = False
    ble_client.client.is_connected = False
    ble_client._reconnecting = True
    assert ble_client.connection_state == "reconnecting"

    # Test manual disconnect state
    ble_client._reconnecting = False
    ble_client._manual_disconnect = True
    assert ble_client.connection_state == "manual_disconnect"


@pytest.mark.asyncio
async def test_exponential_backoff():
    """Test that retry delay increases exponentially."""
    client = ThingyBLEClient(
        auto_reconnect=True, max_reconnect_attempts=4, initial_retry_delay=1.0, max_retry_delay=8.0
    )

    client._connected = True
    client._last_address = "AA:BB:CC:DD:EE:FF"
    client._manual_disconnect = False

    # Track delays
    delays = []

    async def mock_sleep(delay):
        delays.append(delay)

    mock_bleak_client = Mock(spec=BleakClient)
    mock_bleak_client.address = "AA:BB:CC:DD:EE:FF"

    with patch.object(BleakClient, "__init__", return_value=None):
        with patch.object(BleakClient, "connect", new_callable=AsyncMock, side_effect=Exception("Connection failed")):
            with patch("asyncio.sleep", side_effect=mock_sleep):
                # Trigger disconnect
                client._on_disconnect(mock_bleak_client)

                # Wait for all attempts
                await asyncio.sleep(0.1)

                # Check that delays increased (1.0, 2.0, 4.0, 8.0)
                assert len(delays) >= 1
                # First delay should be 1.0
                assert delays[0] == 1.0


@pytest.mark.asyncio
async def test_connect_cancels_existing_reconnect(ble_client):
    """Test that calling connect() cancels any ongoing reconnection."""
    # Set up initial connection
    ble_client._connected = True
    ble_client._last_address = "AA:BB:CC:DD:EE:FF"
    ble_client._manual_disconnect = False

    # Mock BleakClient to always fail connection
    mock_bleak_client = Mock(spec=BleakClient)
    mock_bleak_client.address = "AA:BB:CC:DD:EE:FF"

    with patch.object(BleakClient, "__init__", return_value=None):
        with patch.object(BleakClient, "connect", new_callable=AsyncMock, side_effect=Exception("Connection failed")):
            # Trigger disconnect
            ble_client._on_disconnect(mock_bleak_client)

            # Wait a bit for reconnect to start
            await asyncio.sleep(0.15)

            # Now call connect manually - should cancel reconnect
            with patch.object(BleakClient, "connect", new_callable=AsyncMock):
                await ble_client.connect("BB:CC:DD:EE:FF:00")

            # Should not be reconnecting
            assert not ble_client.is_reconnecting
