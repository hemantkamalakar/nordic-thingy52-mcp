# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a production-ready Nordic Thingy:52 MCP (Model Context Protocol) server that enables Claude Desktop to control and monitor Nordic Thingy:52 IoT devices via Bluetooth LE. Built using FastMCP and the latest MCP specifications, it provides natural language control of IoT sensors and actuators.

## Development Commands

```bash
# Setup environment (using uv)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Run the MCP server directly (for testing)
python3 run_server.py

# Or with uv
uv run python3 run_server.py

# Or use uv to run commands directly without activating
uv run pytest tests/

# Run tests
uv run pytest tests/
uv run pytest --cov=src tests/  # With coverage

# Code formatting and linting
uv run black src/
uv run ruff check src/
uv run mypy src/

# Install in development mode
uv pip install -e ".[dev]"
```

## Architecture

The system follows a simplified layered architecture using FastMCP:

1. **MCP Server Layer** (`src/server.py`) - FastMCP with decorator-based tools
2. **Business Logic Layer** (`src/bluetooth_client.py`) - BLE operations and data parsing
3. **Hardware Layer** - Nordic Thingy:52 device via Bluetooth LE

### Key Files

- `src/server.py` - Main MCP server using FastMCP with @mcp.tool() decorators
- `src/bluetooth_client.py` - ThingyBLEClient class wrapping Bleak
- `src/models.py` - Pydantic models for data validation
- `src/constants.py` - All Bluetooth UUIDs and constants
- `pyproject.toml` - Modern Python project configuration
- `requirements.txt` - Dependencies including mcp[cli]

## Nordic Thingy:52 Hardware Capabilities

### Environmental Sensors
- Temperature (-40°C to 85°C)
- Humidity (0-100% RH)
- Pressure (260-1260 hPa)
- CO2/eCO2 (400-8192 ppm)
- TVOC (0-1187 ppb)
- Color sensor (RGB + Clear)
- Light intensity (lux)

### Motion Sensors (9-axis)
- Accelerometer, gyroscope, magnetometer
- Quaternions, Euler angles
- Step counting, tap detection
- Compass heading

### Actuators
- RGB LED (16.7M colors, breathing/flashing modes)
- Speaker (8 preset sounds + tone generation)
- Button (press/long-press events)

## Key Service UUIDs

Reference `src/constants.py` (to be created) for complete UUIDs:
- Environment Service: `EF680200-9B35-4933-9B10-52FFA9740042`
- Motion Service: `EF680400-9B35-4933-9B10-52FFA9740042`
- UI Service: `EF680300-9B35-4933-9B10-52FFA9740042`
- Sound Service: `EF680500-9B35-4933-9B10-52FFA9740042`

## Implementation Status

✅ **Core Implementation Complete**

The MCP server is fully functional with:
- Device discovery and connection management
- All environmental sensors (temperature, humidity, pressure, CO2, TVOC, color)
- Motion sensors (step counter)
- LED control with colors and breathing effects
- Sound playback (8 preset sounds)
- Proper error handling and logging
- Cross-platform support (Windows, macOS, Linux)

**Future Enhancements** (see IMPLEMENTATION_PLAN.md):
- Advanced motion processing (quaternions, Euler angles)
- Automation engine with rules
- Continuous monitoring with alerts
- Data logging and analytics

## Key Design Decisions

### FastMCP with Decorators
The server uses FastMCP's modern decorator-based approach:
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Nordic Thingy:52")

@mcp.tool()
async def read_temperature() -> dict[str, Optional[float]]:
    """Read the current temperature from the Thingy device."""
    temp = await ble_client.read_temperature()
    return {"temperature_celsius": temp, "unit": "°C"}
```

### Asynchronous Architecture
All BLE operations use Python's `asyncio` due to Bleak's async nature. Every tool function is `async`.

### Error Handling
- All BLE operations wrapped in try/except
- Graceful degradation when sensors fail
- Comprehensive error messages returned to Claude
- Connection state checked before operations

### Data Validation
Use Pydantic v2 for all data structures:
```python
class EnvironmentalData(BaseModel):
    timestamp: datetime
    temperature: Optional[float] = Field(None, description="Temperature in Celsius")
    humidity: Optional[float] = Field(None, description="Humidity in %")
```

### Single Global Client
One ThingyBLEClient instance shared across all tools, maintaining connection state.

## Implemented MCP Tools

### Device Management (4 tools)
- `scan_devices(timeout)` - Find nearby Thingy devices
- `connect_device(address, timeout)` - Connect to device
- `disconnect_device()` - Disconnect current device
- `get_device_status()` - Connection and battery status

### Environmental Sensors (8 tools)
- `read_temperature()` - Temperature in Celsius
- `read_humidity()` - Relative humidity %
- `read_pressure()` - Atmospheric pressure hPa
- `read_air_quality()` - CO2 ppm and TVOC ppb with quality assessment
- `read_all_sensors()` - All environmental sensors at once
- `read_color_sensor()` - RGBC values
- `read_light_intensity()` - Light intensity in lux
- `read_step_count()` - Step counter

### Advanced Motion (6 tools)
- `read_quaternion()` - Quaternion orientation (w, x, y, z)
- `read_euler_angles()` - Roll, pitch, yaw in degrees
- `read_heading()` - Compass heading (0-360 degrees)
- `read_orientation()` - Device orientation (portrait/landscape)
- `read_tap_event()` - Tap detection (single/double, direction)
- `read_raw_motion()` - Raw accelerometer, gyroscope, magnetometer

### LED Control (3 tools)
- `set_led_color(color, red, green, blue, intensity)` - Set LED with named color or RGB
- `set_led_breathe(color, intensity, delay)` - Breathing effect
- `turn_off_led()` - Turn off LED

### Sound (2 tools)
- `play_sound(sound_id)` - Play preset sound 1-8
- `beep()` - Quick beep sound

**Total: 23 tools implemented**

## Testing Requirements

Target 90%+ test coverage:
- Unit tests for parsers, validators, formatters
- Integration tests with actual Thingy:52 hardware
- End-to-end tests via MCP protocol
- Performance tests (sensor read < 500ms)

## Common Automation Use Cases

Refer to PRD Section 4 for 60+ detailed use cases:
- Air quality monitoring with alerts
- Meeting room status indicators
- Comfort zone tracking
- Fall detection for elderly care
- Plant care monitoring
- Cold chain temperature logging

## Dependencies

Core (from requirements.txt):
- `mcp[cli]>=1.0.0` - FastMCP server framework
- `bleak>=0.21.0` - Cross-platform Bluetooth LE
- `pydantic>=2.0.0` - Data validation
- `pydantic-settings>=2.0.0` - Settings management
- `aiofiles>=23.0.0` - Async file operations
- `python-dateutil>=2.8.0` - Date/time utilities
- `colorama>=0.4.6` - Cross-platform colored output

Dev (from pyproject.toml):
- `pytest>=7.4.0` + `pytest-asyncio>=0.21.0`
- `black>=23.7.0` - Code formatting
- `ruff>=0.1.0` - Fast linting
- `mypy>=1.5.0` - Type checking

## Configuration

### Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "thingy52": {
      "command": "python3",
      "args": [
        "run_server.py"
      ],
      "cwd": "/absolute/path/to/Thingy52MCPServer"
    }
  }
}
```

Or with uv:
```json
{
  "mcpServers": {
    "thingy52": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/Thingy52MCPServer",
        "run",
        "python3",
        "run_server.py"
      ]
    }
  }
}
```

### Logging

Logging is configured in `src/server.py`:
```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

Change `level=logging.DEBUG` for verbose output.

## Performance Targets

- Connection time: < 5 seconds
- Single sensor read: < 500ms
- All sensors read: < 1 second
- LED response: < 200ms
- Connection stability: 99% uptime

## Comparison to Reference Implementation

This implementation improves upon the reference (github.com/karthiksuku/nordic-thingy-mcp) with:
- **Modern MCP**: Uses latest FastMCP with decorators instead of old SDK
- **Type Safety**: Full Pydantic v2 validation and mypy type hints
- **Better UX**: All tools have detailed docstrings visible to Claude
- **Error Messages**: Descriptive error messages in responses
- **Code Quality**: Black formatting, ruff linting, modern Python
- **Cross-Platform**: Tested on Windows, macOS, and Linux
- **Documentation**: Comprehensive README and CLAUDE.md

## Important Implementation Notes

### Bluetooth Data Parsing
Each sensor has a specific byte format from Nordic firmware:
- Temperature: integer (1 byte signed) + decimal (1 byte)
- Humidity: single unsigned byte
- Pressure: integer (4 bytes) + decimal (1 byte) in Pascal, convert to hPa
- Air Quality: CO2 (2 bytes) + TVOC (2 bytes)
- Color: RGBC each 2 bytes little-endian

See `src/bluetooth_client.py` for parsing implementations.

### LED Control
The LED characteristic expects:
```python
bytes([mode, red, green, blue]) + delay.to_bytes(2, 'little')
```
Where mode: 1=constant, 2=breathe, 3=one-shot

### Named Colors
`LED_COLORS` dict in constants.py provides named colors:
```python
"red": (255, 0, 0), "warm_white": (255, 230, 200), etc.
```

### Connection Management
- One device at a time (stored in global `ble_client`)
- No auto-reconnect yet (future enhancement)
- Must disconnect before connecting to another device

### Tool Docstrings
FastMCP automatically exposes tool docstrings to Claude, so make them descriptive!

## Code Organization

The codebase is intentionally flat and simple:

```
src/
├── __init__.py           # Package info
├── server.py             # FastMCP server with all tools (400 lines)
├── bluetooth_client.py   # ThingyBLEClient class (300 lines)
├── models.py             # Pydantic models (80 lines)
└── constants.py          # UUIDs and constants (80 lines)
```

This design prioritizes:
- **Readability**: All tools in one file
- **Simplicity**: Minimal abstraction layers
- **Maintainability**: Easy to understand and modify

## Natural Language Interface

Users interact via Claude Desktop using natural language:
- "Find my Thingy" → device discovery
- "What's the temperature?" → sensor reading
- "Turn LED red" → actuator control
- "Alert if CO2 > 1000 ppm" → automation creation

Responses should be concise, use emojis for status (🟢🟡🔴), and format sensor data in readable tables.
