"""Tests for Pydantic models."""

import pytest
from datetime import datetime

from src.models import DeviceInfo, EnvironmentalData, LEDConfig, ConnectionStatus


def test_device_info_creation():
    """Test DeviceInfo model."""
    device = DeviceInfo(address="AA:BB:CC:DD:EE:FF", name="Thingy", rssi=-50)
    assert device.address == "AA:BB:CC:DD:EE:FF"
    assert device.name == "Thingy"
    assert device.rssi == -50


def test_environmental_data_optional_fields():
    """Test EnvironmentalData with optional fields."""
    data = EnvironmentalData(temperature=22.5)
    assert data.temperature == 22.5
    assert data.humidity is None
    assert data.co2 is None


def test_led_config_validation():
    """Test LEDConfig validation."""
    # Valid config
    config = LEDConfig(mode=1, red=255, green=128, blue=0, intensity=50)
    assert config.mode == 1
    assert config.intensity == 50

    # Invalid mode should raise validation error
    with pytest.raises(Exception):
        LEDConfig(mode=5, red=255, green=0, blue=0)

    # Invalid RGB values should raise validation error
    with pytest.raises(Exception):
        LEDConfig(mode=1, red=300, green=0, blue=0)


def test_connection_status():
    """Test ConnectionStatus model."""
    # Disconnected
    status = ConnectionStatus(connected=False)
    assert not status.connected
    assert status.address is None

    # Connected
    status = ConnectionStatus(
        connected=True, address="AA:BB:CC:DD:EE:FF", battery_level=85, rssi=-45
    )
    assert status.connected
    assert status.battery_level == 85
