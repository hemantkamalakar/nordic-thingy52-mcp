# Nordic Thingy:52 MCP Server Documentation

## Project Overview

A Model Context Protocol (MCP) server enabling natural language control of Nordic Thingy:52 IoT devices through Claude Desktop.

### Vision
Enable users to control and monitor IoT devices through natural conversation with Claude, eliminating the need for complex IoT platforms or custom mobile apps.

### Goals
- Production-ready MCP server for Nordic Thingy:52 integration
- Comprehensive automation framework for IoT scenarios
- Reference implementation for other BLE device integrations

## Device Capabilities

### Environmental Sensors
- Temperature (-40°C to 85°C)
- Humidity (0-100% RH)
- Pressure (260-1260 hPa)
- Air Quality (CO2: 400-8192 ppm, TVOC: 0-1187 ppb)
- Color & Light (RGB + Clear channel)

### Motion Sensors
- 9-axis motion (accelerometer, gyroscope, magnetometer)
- Quaternion and Euler angle representation
- Step counting and tap detection
- Orientation sensing

### Actuators
- RGB LED (16.7M colors, multiple modes)
- Speaker (8 preset sounds)
- Button input
- Battery monitoring

## Development Progress

### 1. Core Implementation
✅ BLE Communication
- Robust device discovery
- Auto-reconnect capability
- Connection management
- Error handling

✅ Sensor Integration
- Environmental readings
- Motion data processing
- Real-time monitoring
- Data validation

✅ Device Control
- LED patterns and effects
- Sound system with volume
- Battery monitoring
- Event handling

### 2. Feature Demo
✅ Comprehensive Testing
- Environmental sensor demo
- Motion detection demo
- LED control patterns
- Sound system testing

### 3. Code Organization
✅ Project Structure
- `src/` - Core library
- `tests/` - Unit tests
- Documentation
- Feature demo

## Technical Details

### Core Features
1. Device Discovery & Management
   - BLE scanning
   - Connection handling
   - Auto-reconnect
   - Multi-device support

2. Environmental Monitoring
   - Real-time sensor readings
   - Data formatting
   - Threshold monitoring
   - Air quality analysis

3. Motion Processing
   - Raw sensor access
   - Orientation tracking
   - Activity detection
   - Step counting

4. Control Features
   - RGB LED control
   - Sound playback
   - Volume management
   - Custom patterns

### Implementation Notes

#### BLE Implementation
- Using Bleak library for cross-platform support
- Async/await pattern for performance
- Robust error handling
- Automatic reconnection

#### Project Architecture
- Modular design
- Clear separation of concerns
- Extensive error handling
- Comprehensive logging

#### Testing Strategy
- Unit tests for core functionality
- Integration tests for BLE
- Feature demo for validation
- Continuous testing

## Usage Examples

### Natural Language Commands
```
"Find nearby Thingy devices"
"Connect to the Thingy in my office"
"What's the temperature?"
"Set LED to red"
"Play sound pattern 3"
"Monitor CO2 levels"
```

### Automation Examples
```python
# Air Quality Monitoring
"Alert me if CO2 exceeds 1000 ppm"
"Flash red LED when air quality is poor"

# Environmental Control
"Monitor temperature and humidity"
"Set up comfort zone alerts"

# Motion Detection
"Detect taps and movement"
"Count steps during activity"
```

## Future Improvements

### Short Term
1. Enhanced Features
   - Real-time monitoring
   - Custom LED patterns
   - Extended sound capabilities

2. Code Quality
   - Additional test coverage
   - Performance optimization
   - Error recovery enhancements

### Long Term
1. Platform Integration
   - Home Assistant support
   - IFTTT integration
   - Custom automation platform

2. Advanced Features
   - ML-based anomaly detection
   - Predictive maintenance
   - Multi-device orchestration

## References

- [Nordic Thingy:52 Documentation](https://infocenter.nordicsemi.com/topic/struct_nrf52/struct/nrf52_ble_thingy52.html)
- [Bleak Documentation](https://bleak.readthedocs.io/)
- [Python AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)

## License

MIT License - see [LICENSE](LICENSE) for details.