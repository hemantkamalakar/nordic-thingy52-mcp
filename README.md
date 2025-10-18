# Thingy52 MCP Server

A Model Context Protocol (MCP) server for Nordic Thingy:52 IoT devices.

## Core Features

1. BLE Communication:
   - Device scanning and discovery
   - Automatic reconnection handling
   - Robust error recovery

2. Sensor Support:
   - Environmental: Temperature, Humidity, Pressure, Air Quality
   - Motion: Quaternion, Steps, Heading, Raw Data
   - Color and Light Intensity

3. Device Control:
   - LED with RGB colors and effects (constant, breathing, one-shot)
   - Sound patterns with volume control
   - Battery level monitoring

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the feature demo:
   ```bash
   python feature_demo.py
   ```

3. Start the MCP server:
   ```bash
   python run_server.py
   ```

## Project Structure

- `feature_demo.py`: Comprehensive demo of all Thingy:52 features
- `run_server.py`: MCP server implementation
- `src/`: Core library files
  - `bluetooth_client.py`: BLE communication
  - `server.py`: MCP server implementation
  - `models.py`: Data models
  - `constants.py`: BLE UUIDs and constants
- `tests/`: Unit tests

## Documentation

- [Quick Start Guide](QUICK_START.md)
- [Implementation Plan](IMPLEMENTATION_PLAN.md)
- [Testing Guide](TESTING.md)
- [Troubleshooting](TROUBLESHOOTING.md)

## License

MIT License - see [LICENSE](LICENSE) for details.
