"""Pydantic models for Thingy:52 data structures."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DeviceInfo(BaseModel):
    """Information about a discovered Thingy:52 device."""

    address: str = Field(..., description="Bluetooth MAC address")
    name: str = Field(..., description="Device name")
    rssi: int = Field(..., description="Signal strength in dBm")


class EnvironmentalData(BaseModel):
    """Environmental sensor readings."""

    timestamp: datetime = Field(default_factory=datetime.now)
    temperature: Optional[float] = Field(None, description="Temperature in Celsius")
    humidity: Optional[float] = Field(None, description="Humidity in %")
    pressure: Optional[float] = Field(None, description="Pressure in hPa")
    co2: Optional[int] = Field(None, description="CO2 in ppm")
    tvoc: Optional[int] = Field(None, description="TVOC in ppb")


class ColorData(BaseModel):
    """Color sensor data."""

    red: int = Field(..., ge=0, le=65535)
    green: int = Field(..., ge=0, le=65535)
    blue: int = Field(..., ge=0, le=65535)
    clear: int = Field(..., ge=0, le=65535)


class MotionData(BaseModel):
    """Motion sensor readings."""

    timestamp: datetime = Field(default_factory=datetime.now)
    steps: Optional[int] = Field(None, description="Step count")
    orientation: Optional[str] = Field(None, description="Device orientation")


class QuaternionData(BaseModel):
    """Quaternion rotation representation."""

    w: float
    x: float
    y: float
    z: float


class EulerData(BaseModel):
    """Euler angles (roll, pitch, yaw)."""

    roll: float = Field(..., description="Roll in degrees")
    pitch: float = Field(..., description="Pitch in degrees")
    yaw: float = Field(..., description="Yaw in degrees")


class LEDConfig(BaseModel):
    """LED configuration."""

    mode: int = Field(..., ge=1, le=3, description="LED mode (1=constant, 2=breathe, 3=one-shot)")
    red: int = Field(..., ge=0, le=255)
    green: int = Field(..., ge=0, le=255)
    blue: int = Field(..., ge=0, le=255)
    intensity: int = Field(100, ge=0, le=100, description="Brightness percentage")
    delay: int = Field(0, ge=0, description="Delay in ms for breathe/one-shot modes")


class ConnectionStatus(BaseModel):
    """Device connection status."""

    connected: bool
    address: Optional[str] = None
    name: Optional[str] = None
    battery_level: Optional[int] = Field(None, ge=0, le=100, description="Battery percentage")
    rssi: Optional[int] = Field(None, description="Signal strength in dBm")
