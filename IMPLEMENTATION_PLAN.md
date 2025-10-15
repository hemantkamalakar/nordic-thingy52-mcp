# Implementation Plan
## Nordic Thingy:52 MCP Server for Claude Desktop

**Version:** 1.0  
**Date:** October 15, 2025  
**Timeline:** 4-6 weeks to MVP  
**Team Size:** 1-3 developers

---

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Development Phases](#development-phases)
4. [Technical Implementation](#technical-implementation)
5. [Testing Strategy](#testing-strategy)
6. [Deployment](#deployment)
7. [Documentation](#documentation)
8. [Maintenance](#maintenance)

---

## 1. Overview

### 1.1 Project Scope
Develop a production-ready MCP server that enables Claude Desktop to control and monitor Nordic Thingy:52 devices via Bluetooth LE. The implementation will be a complete rewrite of the reference project, incorporating best practices, comprehensive error handling, and extensive automation capabilities.

### 1.2 Key Deliverables
- ✅ MCP server with 20+ tools
- ✅ Comprehensive documentation
- ✅ Example automations library
- ✅ Automated installer
- ✅ Testing suite
- ✅ Troubleshooting guide

### 1.3 Success Criteria
- All core features (P0 priority) implemented
- 90%+ test coverage
- < 1 second average response time
- Clear, comprehensive documentation
- Successfully deployed to 10+ test users

---

## 2. Architecture

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Desktop                          │
│                    (User Interface)                          │
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Protocol (JSON-RPC)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   MCP Server Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Tool Registry│  │  Request     │  │   Response   │     │
│  │   Handler    │  │  Validator   │  │   Formatter  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              Business Logic Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Device     │  │   Sensor     │  │  Automation  │     │
│  │   Manager    │  │   Manager    │  │   Engine     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     LED      │  │    Sound     │  │    Data      │     │
│  │  Controller  │  │  Controller  │  │   Logger     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│            Bluetooth LE Communication Layer                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Connection  │  │   Service    │  │Characteristic│     │
│  │   Manager    │  │   Discovery  │  │   Handler    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                    (Bleak Library)                           │
└────────────────────────┬────────────────────────────────────┘
                         │ Bluetooth LE Protocol
┌────────────────────────▼────────────────────────────────────┐
│              Nordic Thingy:52 Device                         │
│         (nRF52832 + Sensors + Actuators)                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Component Breakdown

#### 2.2.1 MCP Server Layer
**Responsibilities:**
- Handle MCP protocol communication
- Tool registration and routing
- Input validation and sanitization
- Response formatting
- Error handling and logging

**Key Files:**
- `mcp_server.py` - Main server entry point
- `tools/` - Individual tool implementations
- `validators.py` - Input validation schemas

#### 2.2.2 Business Logic Layer
**Responsibilities:**
- Device lifecycle management
- Sensor data processing and caching
- Automation rule evaluation
- LED pattern generation
- Sound scheduling
- Data persistence

**Key Files:**
- `device_manager.py` - Device connection and state
- `sensor_manager.py` - Sensor reading and monitoring
- `automation_engine.py` - Rule evaluation and execution
- `led_controller.py` - LED effects and patterns
- `sound_controller.py` - Audio playback control
- `data_logger.py` - Data persistence

#### 2.2.3 Bluetooth Layer
**Responsibilities:**
- Low-level BLE communication
- Service and characteristic discovery
- Notification handling
- Connection stability
- Error recovery

**Key Files:**
- `ble_client.py` - BLE connection wrapper
- `characteristics.py` - Thingy:52 GATT definitions
- `services.py` - Service UUID mappings

### 2.3 Data Flow

#### Sensor Reading Flow
```
User: "What's the temperature?"
    ↓
Claude Desktop (via MCP)
    ↓
MCP Server receives tool call: thingy_get_sensors
    ↓
Device Manager checks connection
    ↓
Sensor Manager requests data from BLE client
    ↓
BLE Client reads characteristic
    ↓
Thingy:52 returns raw sensor data
    ↓
Sensor Manager parses and formats data
    ↓
MCP Server returns formatted response
    ↓
Claude Desktop displays: "Temperature: 22.5°C"
```

#### Automation Flow
```
User: "Alert me if CO2 exceeds 1000 ppm"
    ↓
MCP Server receives automation setup request
    ↓
Automation Engine creates rule:
  - Condition: CO2 > 1000
  - Action: Play beep + Flash red LED
    ↓
Background monitor starts (every 60s)
    ↓
[Periodic Check]
Sensor Manager reads CO2 → 1050 ppm
    ↓
Automation Engine evaluates rule → TRIGGERED
    ↓
LED Controller: Flash red
Sound Controller: Play beep
    ↓
User receives visual and audio alert
```

### 2.4 Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Language** | Python 3.10+ | Excellent async support, strong ecosystem |
| **BLE Library** | Bleak 0.21+ | Cross-platform, async, well-maintained |
| **MCP SDK** | Official Anthropic SDK | Protocol compliance, future-proof |
| **Data Validation** | Pydantic 2.0+ | Type safety, automatic validation |
| **Config** | TOML / JSON | Human-readable, standard formats |
| **Logging** | Python logging | Built-in, flexible, production-ready |
| **Testing** | pytest + pytest-asyncio | Industry standard, async support |
| **Documentation** | Markdown + Sphinx | Clear, professional, searchable |

---

## 3. Development Phases

### Phase 0: Setup & Foundation (Week 1)

#### Goals
- Development environment setup
- Project structure
- Core dependencies
- Basic scaffolding

#### Tasks
1. **Repository Setup** (Day 1)
   - [ ] Create Git repository
   - [ ] Initialize Python project structure
   - [ ] Setup .gitignore
   - [ ] Create README.md
   - [ ] Add MIT License
   - [ ] Setup GitHub Actions / CI

2. **Development Environment** (Day 1-2)
   - [ ] Create requirements.txt
   - [ ] Create dev-requirements.txt
   - [ ] Setup virtual environment
   - [ ] Install dependencies
   - [ ] Configure linters (black, flake8, mypy)
   - [ ] Setup pre-commit hooks

3. **Project Structure** (Day 2-3)
   ```
   nordic-thingy-mcp/
   ├── src/
   │   ├── __init__.py
   │   ├── mcp_server.py           # Main entry point
   │   ├── config.py                # Configuration management
   │   ├── constants.py             # UUIDs, constants
   │   ├── exceptions.py            # Custom exceptions
   │   ├── bluetooth/
   │   │   ├── __init__.py
   │   │   ├── client.py            # BLE client wrapper
   │   │   ├── services.py          # Service definitions
   │   │   └── characteristics.py   # Characteristic handlers
   │   ├── device/
   │   │   ├── __init__.py
   │   │   ├── manager.py           # Device lifecycle
   │   │   ├── state.py             # Device state tracking
   │   │   └── models.py            # Data models
   │   ├── sensors/
   │   │   ├── __init__.py
   │   │   ├── manager.py           # Sensor coordination
   │   │   ├── environmental.py     # Environmental sensors
   │   │   ├── motion.py            # Motion sensors
   │   │   └── parsers.py           # Data parsers
   │   ├── actuators/
   │   │   ├── __init__.py
   │   │   ├── led.py               # LED controller
   │   │   └── sound.py             # Sound controller
   │   ├── automation/
   │   │   ├── __init__.py
   │   │   ├── engine.py            # Automation engine
   │   │   ├── rules.py             # Rule definitions
   │   │   └── scheduler.py         # Task scheduling
   │   ├── tools/
   │   │   ├── __init__.py
   │   │   ├── discovery.py         # Device discovery tools
   │   │   ├── connection.py        # Connection tools
   │   │   ├── sensors.py           # Sensor reading tools
   │   │   ├── led.py               # LED control tools
   │   │   ├── sound.py             # Sound control tools
   │   │   └── automation.py        # Automation tools
   │   └── utils/
   │       ├── __init__.py
   │       ├── logger.py            # Logging utilities
   │       ├── validators.py        # Input validators
   │       └── formatters.py        # Output formatters
   ├── tests/
   │   ├── __init__.py
   │   ├── conftest.py              # Pytest configuration
   │   ├── unit/                    # Unit tests
   │   ├── integration/             # Integration tests
   │   └── fixtures/                # Test fixtures
   ├── examples/
   │   ├── basic_usage.py
   │   ├── automation_examples.py
   │   └── advanced_features.py
   ├── docs/
   │   ├── README.md
   │   ├── INSTALLATION.md
   │   ├── USER_GUIDE.md
   │   ├── API_REFERENCE.md
   │   ├── TROUBLESHOOTING.md
   │   └── CONTRIBUTING.md
   ├── scripts/
   │   ├── install.sh               # Installation script
   │   ├── setup_claude.py          # Claude config helper
   │   └── test_connection.py       # Connection tester
   ├── .github/
   │   └── workflows/
   │       └── ci.yml               # CI/CD pipeline
   ├── requirements.txt
   ├── dev-requirements.txt
   ├── setup.py
   ├── pyproject.toml
   └── README.md
   ```

4. **Core Dependencies** (Day 3-4)
   ```python
   # requirements.txt
   bleak>=0.21.0
   anthropic-mcp-sdk>=1.0.0  # Or latest version
   pydantic>=2.0.0
   pydantic-settings>=2.0.0
   asyncio-mqtt>=0.16.0  # For future MQTT integration
   aiofiles>=23.0.0
   python-dateutil>=2.8.0
   colorama>=0.4.6  # For colored console output
   ```

5. **Constants & UUIDs** (Day 4-5)
   ```python
   # constants.py
   # Thingy:52 Service UUIDs
   ENVIRONMENT_SERVICE_UUID = "EF680200-9B35-4933-9B10-52FFA9740042"
   MOTION_SERVICE_UUID = "EF680400-9B35-4933-9B10-52FFA9740042"
   UI_SERVICE_UUID = "EF680300-9B35-4933-9B10-52FFA9740042"
   SOUND_SERVICE_UUID = "EF680500-9B35-4933-9B10-52FFA9740042"
   
   # Characteristic UUIDs (to be defined for each sensor/actuator)
   ```

#### Deliverables
- ✅ Working development environment
- ✅ Complete project structure
- ✅ All dependencies installed
- ✅ Git repository initialized
- ✅ CI/CD pipeline configured

---

### Phase 1: Core Bluetooth & Device Management (Week 2)

#### Goals
- Establish BLE connectivity
- Device discovery and connection
- Basic service interaction
- Connection stability

#### Tasks

1. **BLE Client Implementation** (Day 1-2)
   ```python
   # bluetooth/client.py
   class ThingyBLEClient:
       """Wrapper around Bleak for Thingy:52 communication"""
       
       async def scan(self, timeout: int = 10) -> List[BLEDevice]:
           """Scan for Thingy devices"""
           
       async def connect(self, address: str) -> bool:
           """Connect to device"""
           
       async def disconnect(self) -> bool:
           """Disconnect from device"""
           
       async def read_characteristic(self, uuid: str) -> bytes:
           """Read a characteristic"""
           
       async def write_characteristic(self, uuid: str, data: bytes) -> bool:
           """Write to a characteristic"""
           
       async def subscribe(self, uuid: str, callback) -> bool:
           """Subscribe to notifications"""
   ```

2. **Device Manager** (Day 2-3)
   ```python
   # device/manager.py
   class DeviceManager:
       """Manages device lifecycle and state"""
       
       async def discover_devices(self) -> List[ThingyDevice]:
           """Discover nearby Thingy devices"""
           
       async def connect_device(self, address: str) -> ThingyDevice:
           """Connect to a specific device"""
           
       async def disconnect_device(self) -> None:
           """Disconnect current device"""
           
       async def get_device_info(self) -> DeviceInfo:
           """Get device information and status"""
           
       async def auto_reconnect(self) -> bool:
           """Attempt to reconnect if connection lost"""
   ```

3. **Service Discovery** (Day 3-4)
   ```python
   # bluetooth/services.py
   class ServiceDiscovery:
       """Discover and map Thingy:52 services"""
       
       async def discover_services(self, client: BleakClient) -> Dict:
           """Discover all services and characteristics"""
           
       def get_characteristic_uuid(self, service: str, char: str) -> str:
           """Get UUID for a characteristic"""
   ```

4. **Connection Stability** (Day 4-5)
   - Implement connection monitoring
   - Auto-reconnect on disconnect
   - Connection quality reporting (RSSI)
   - Timeout handling
   - Error recovery

5. **Testing** (Day 5)
   - Unit tests for BLE client
   - Integration tests with actual device
   - Connection stress testing
   - Error scenario testing

#### Deliverables
- ✅ BLE connection established
- ✅ Device discovery working
- ✅ Stable connection with auto-reconnect
- ✅ Service discovery complete
- ✅ Basic error handling
- ✅ Test coverage > 80%

---

### Phase 2: Sensor Reading & Data Management (Week 3)

#### Goals
- Read all environmental sensors
- Read motion sensors
- Parse and format sensor data
- Implement caching and monitoring

#### Tasks

1. **Environmental Sensors** (Day 1-2)
   ```python
   # sensors/environmental.py
   class EnvironmentalSensors:
       """Handle environmental sensor readings"""
       
       async def read_temperature(self) -> float:
           """Read temperature in Celsius"""
           
       async def read_humidity(self) -> float:
           """Read humidity percentage"""
           
       async def read_pressure(self) -> float:
           """Read pressure in hPa"""
           
       async def read_air_quality(self) -> AirQuality:
           """Read CO2 and TVOC"""
           
       async def read_color_sensor(self) -> ColorData:
           """Read color sensor (RGB + Clear)"""
           
       async def read_all(self) -> EnvironmentalData:
           """Read all environmental sensors at once"""
   ```

2. **Motion Sensors** (Day 2-3)
   ```python
   # sensors/motion.py
   class MotionSensors:
       """Handle motion sensor readings"""
       
       async def read_accelerometer(self) -> Vector3D:
           """Read 3-axis accelerometer"""
           
       async def read_gyroscope(self) -> Vector3D:
           """Read 3-axis gyroscope"""
           
       async def read_magnetometer(self) -> Vector3D:
           """Read 3-axis magnetometer"""
           
       async def read_quaternion(self) -> Quaternion:
           """Read quaternion representation"""
           
       async def read_euler_angles(self) -> EulerAngles:
           """Read Euler angles (roll, pitch, yaw)"""
           
       async def read_heading(self) -> float:
           """Read compass heading"""
           
       async def read_step_count(self) -> int:
           """Read step counter"""
           
       async def get_tap_status(self) -> TapEvent:
           """Check for tap events"""
   ```

3. **Data Parsing** (Day 3)
   ```python
   # sensors/parsers.py
   class SensorDataParser:
       """Parse raw sensor data from Thingy"""
       
       @staticmethod
       def parse_temperature(raw: bytes) -> float:
           """Parse temperature from raw bytes"""
           
       @staticmethod
       def parse_humidity(raw: bytes) -> float:
           """Parse humidity from raw bytes"""
           
       # ... parsers for each sensor type
   ```

4. **Sensor Manager** (Day 4)
   ```python
   # sensors/manager.py
   class SensorManager:
       """Coordinate all sensor operations"""
       
       def __init__(self):
           self.environmental = EnvironmentalSensors()
           self.motion = MotionSensors()
           self.cache = SensorCache()
           
       async def read_all_sensors(self) -> AllSensorData:
           """Read all sensors with caching"""
           
       async def start_monitoring(self, interval: int):
           """Start continuous monitoring"""
           
       async def stop_monitoring(self):
           """Stop continuous monitoring"""
   ```

5. **Data Models** (Day 4-5)
   ```python
   # device/models.py
   from pydantic import BaseModel
   from datetime import datetime
   
   class EnvironmentalData(BaseModel):
       timestamp: datetime
       temperature: float
       humidity: float
       pressure: float
       co2: int
       tvoc: int
       color: ColorData
       light_intensity: float
       
   class MotionData(BaseModel):
       timestamp: datetime
       accelerometer: Vector3D
       gyroscope: Vector3D
       magnetometer: Vector3D
       quaternion: Quaternion
       euler: EulerAngles
       heading: float
       steps: int
   ```

6. **Testing** (Day 5)
   - Test all sensor reading functions
   - Verify data parsing accuracy
   - Test caching mechanism
   - Performance testing (read latency)

#### Deliverables
- ✅ All sensors readable
- ✅ Accurate data parsing
- ✅ Proper data models with validation
- ✅ Caching implemented
- ✅ Monitoring capability
- ✅ Test coverage > 85%

---

### Phase 3: Actuator Control (Week 4 - Days 1-3)

#### Goals
- LED control with effects
- Sound playback
- Button event handling

#### Tasks

1. **LED Controller** (Day 1)
   ```python
   # actuators/led.py
   class LEDController:
       """Control Thingy RGB LED"""
       
       async def set_color(self, r: int, g: int, b: int):
           """Set LED to RGB color"""
           
       async def set_color_hex(self, hex_color: str):
           """Set LED using hex color code"""
           
       async def set_brightness(self, brightness: int):
           """Set LED brightness (0-100)"""
           
       async def set_mode(self, mode: LEDMode):
           """Set LED mode (constant, breathing, one-shot)"""
           
       async def turn_off(self):
           """Turn off LED"""
           
       async def create_effect(self, effect: LEDEffect):
           """Create custom LED effect"""
           
       # Predefined effects
       async def breathe(self, color: tuple, duration: int):
           """Breathing effect"""
           
       async def flash(self, color: tuple, count: int, interval: float):
           """Flashing effect"""
           
       async def rainbow_cycle(self, duration: int):
           """Rainbow color cycle"""
   ```

2. **Sound Controller** (Day 2)
   ```python
   # actuators/sound.py
   class SoundController:
       """Control Thingy speaker"""
       
       async def play_sound(self, sound_id: int):
           """Play preset sound (1-8)"""
           
       async def beep(self, duration: int = 100):
           """Quick beep"""
           
       async def play_tone(self, frequency: int, duration: int):
           """Play tone at specific frequency"""
           
       async def set_volume(self, volume: int):
           """Set speaker volume (0-100)"""
           
       async def stop_sound(self):
           """Stop current sound"""
           
       # Future: Audio streaming
       async def stream_audio(self, audio_data: bytes):
           """Stream audio to speaker"""
   ```

3. **Button Handler** (Day 3)
   ```python
   # device/button.py
   class ButtonHandler:
       """Handle button events"""
       
       def on_button_press(self, callback):
           """Register callback for button press"""
           
       def on_button_release(self, callback):
           """Register callback for button release"""
           
       def on_long_press(self, callback, duration: int = 1000):
           """Register callback for long press"""
   ```

4. **Testing** (Day 3)
   - Test LED colors and effects
   - Test sound playback
   - Test button events
   - Visual verification tests

#### Deliverables
- ✅ Full LED control with effects
- ✅ Sound playback working
- ✅ Button event handling
- ✅ Test coverage > 80%

---

### Phase 4: MCP Integration (Week 4 - Days 4-5, Week 5 - Days 1-2)

#### Goals
- Implement all MCP tools
- Request validation
- Response formatting
- Error handling

#### Tasks

1. **Tool Definitions** (Day 1)
   ```python
   # tools/discovery.py
   @mcp_tool("thingy_scan")
   async def scan_for_devices(timeout: int = 10) -> List[Device]:
       """Scan for nearby Thingy:52 devices"""
       
   # tools/connection.py
   @mcp_tool("thingy_connect")
   async def connect_device(address: str) -> ConnectionResult:
       """Connect to a Thingy device"""
       
   @mcp_tool("thingy_disconnect")
   async def disconnect_device() -> bool:
       """Disconnect from current device"""
       
   @mcp_tool("thingy_get_status")
   async def get_device_status() -> DeviceStatus:
       """Get connection and device status"""
       
   # tools/sensors.py
   @mcp_tool("thingy_read_sensors")
   async def read_all_sensors() -> SensorData:
       """Read all sensors"""
       
   @mcp_tool("thingy_read_temperature")
   async def read_temperature() -> float:
       """Read temperature only"""
       
   # ... tools for each sensor type
   
   # tools/led.py
   @mcp_tool("thingy_set_led")
   async def set_led_color(
       color: str = None,
       r: int = None,
       g: int = None,
       b: int = None,
       brightness: int = 100
   ) -> bool:
       """Set LED color"""
       
   @mcp_tool("thingy_led_effect")
   async def led_effect(effect: str, params: Dict) -> bool:
       """Create LED effect"""
       
   @mcp_tool("thingy_led_off")
   async def led_off() -> bool:
       """Turn off LED"""
       
   # tools/sound.py
   @mcp_tool("thingy_play_sound")
   async def play_sound(sound_id: int) -> bool:
       """Play preset sound"""
       
   @mcp_tool("thingy_beep")
   async def beep() -> bool:
       """Quick beep"""
   ```

2. **Input Validation** (Day 2)
   ```python
   # utils/validators.py
   from pydantic import BaseModel, Field, validator
   
   class LEDColorInput(BaseModel):
       r: int = Field(ge=0, le=255)
       g: int = Field(ge=0, le=255)
       b: int = Field(ge=0, le=255)
       brightness: int = Field(ge=0, le=100, default=100)
       
   class SoundInput(BaseModel):
       sound_id: int = Field(ge=1, le=8)
       
   # Add validators for all tool inputs
   ```

3. **Response Formatting** (Day 2)
   ```python
   # utils/formatters.py
   class ResponseFormatter:
       """Format tool responses for Claude"""
       
       @staticmethod
       def format_sensor_data(data: SensorData) -> str:
           """Format sensor data in readable format"""
           
       @staticmethod
       def format_device_list(devices: List[Device]) -> str:
           """Format device list for display"""
           
       @staticmethod
       def format_error(error: Exception) -> str:
           """Format error messages"""
   ```

4. **MCP Server** (Day 3)
   ```python
   # mcp_server.py
   from anthropic_mcp import MCPServer
   
   class ThingyMCPServer(MCPServer):
       """MCP Server for Nordic Thingy:52"""
       
       def __init__(self):
           super().__init__(
               name="nordic-thingy",
               version="1.0.0",
               description="Control Nordic Thingy:52 devices"
           )
           self.device_manager = DeviceManager()
           self.sensor_manager = SensorManager()
           self.led_controller = LEDController()
           self.sound_controller = SoundController()
           self.register_tools()
           
       def register_tools(self):
           """Register all MCP tools"""
           # Register all tools from tools/ directory
           
       async def handle_request(self, request):
           """Handle incoming MCP requests"""
           
       async def shutdown(self):
           """Cleanup on shutdown"""
   
   if __name__ == "__main__":
       server = ThingyMCPServer()
       server.run()
   ```

5. **Error Handling** (Day 4)
   - Connection errors
   - Timeout errors
   - Invalid input errors
   - Device not found errors
   - Graceful degradation

6. **Testing** (Day 4-5)
   - Test all tools individually
   - Test error scenarios
   - Integration testing with Claude Desktop
   - End-to-end workflow testing

#### Deliverables
- ✅ All 20+ MCP tools implemented
- ✅ Input validation working
- ✅ Response formatting polished
- ✅ Error handling comprehensive
- ✅ Integration with Claude tested
- ✅ Test coverage > 90%

---

### Phase 5: Automation Engine (Week 5 - Days 3-5)

#### Goals
- Rule-based automation
- Condition evaluation
- Action execution
- Scheduling

#### Tasks

1. **Rule Engine** (Day 1)
   ```python
   # automation/rules.py
   class AutomationRule:
       """Single automation rule"""
       
       def __init__(
           self,
           name: str,
           conditions: List[Condition],
           actions: List[Action],
           enabled: bool = True
       ):
           self.name = name
           self.conditions = conditions
           self.actions = actions
           self.enabled = enabled
           
       async def evaluate(self, sensor_data: SensorData) -> bool:
           """Evaluate if conditions are met"""
           
       async def execute(self):
           """Execute actions if triggered"""
   
   class Condition:
       """Automation condition"""
       sensor: str
       operator: str  # >, <, ==, !=, >=, <=
       value: float
       
   class Action:
       """Automation action"""
       type: str  # led, sound, notification
       params: Dict
   ```

2. **Automation Engine** (Day 2)
   ```python
   # automation/engine.py
   class AutomationEngine:
       """Manage and execute automation rules"""
       
       def __init__(self):
           self.rules: List[AutomationRule] = []
           self.running = False
           
       async def add_rule(self, rule: AutomationRule):
           """Add automation rule"""
           
       async def remove_rule(self, rule_name: str):
           """Remove automation rule"""
           
       async def start(self):
           """Start automation engine"""
           
       async def stop(self):
           """Stop automation engine"""
           
       async def evaluate_rules(self, sensor_data: SensorData):
           """Evaluate all rules against current sensor data"""
   ```

3. **Scheduler** (Day 2)
   ```python
   # automation/scheduler.py
   class Scheduler:
       """Schedule periodic tasks"""
       
       async def schedule_sensor_read(self, interval: int):
           """Schedule periodic sensor reading"""
           
       async def schedule_rule_evaluation(self, interval: int):
           """Schedule periodic rule evaluation"""
   ```

4. **Automation Tools** (Day 3)
   ```python
   # tools/automation.py
   @mcp_tool("thingy_create_automation")
   async def create_automation(
       name: str,
       condition: str,  # "CO2 > 1000"
       action: str       # "flash_red + beep"
   ) -> bool:
       """Create a new automation rule"""
       
   @mcp_tool("thingy_list_automations")
   async def list_automations() -> List[AutomationRule]:
       """List all automation rules"""
       
   @mcp_tool("thingy_delete_automation")
   async def delete_automation(name: str) -> bool:
       """Delete an automation rule"""
       
   @mcp_tool("thingy_enable_automation")
   async def enable_automation(name: str) -> bool:
       """Enable an automation rule"""
   ```

5. **Testing** (Day 3)
   - Test rule evaluation
   - Test action execution
   - Test scheduling
   - Integration testing

#### Deliverables
- ✅ Automation engine working
- ✅ Rules can be created/deleted
- ✅ Conditions evaluated correctly
- ✅ Actions executed properly
- ✅ Test coverage > 85%

---

### Phase 6: Polish & Production Ready (Week 6)

#### Goals
- Performance optimization
- Comprehensive logging
- Configuration management
- Installation automation
- Documentation

#### Tasks

1. **Performance Optimization** (Day 1)
   - Profile code for bottlenecks
   - Optimize sensor reading (batch reads)
   - Implement connection pooling
   - Cache frequently accessed data
   - Reduce memory footprint

2. **Logging** (Day 1)
   ```python
   # utils/logger.py
   import logging
   
   def setup_logger(name: str, level: str = "INFO"):
       """Setup structured logging"""
       logger = logging.getLogger(name)
       logger.setLevel(level)
       
       # Console handler
       console = logging.StreamHandler()
       console.setFormatter(logging.Formatter(
           '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
       ))
       logger.addHandler(console)
       
       # File handler (optional)
       # file = logging.FileHandler('thingy_mcp.log')
       # logger.addHandler(file)
       
       return logger
   ```

3. **Configuration** (Day 2)
   ```python
   # config.py
   from pydantic_settings import BaseSettings
   
   class Settings(BaseSettings):
       # Server settings
       server_name: str = "nordic-thingy"
       server_version: str = "1.0.0"
       log_level: str = "INFO"
       
       # BLE settings
       scan_timeout: int = 10
       connection_timeout: int = 30
       auto_reconnect: bool = True
       
       # Sensor settings
       default_read_interval: int = 60
       cache_duration: int = 5
       
       # Automation settings
       max_automations: int = 50
       evaluation_interval: int = 60
       
       class Config:
           env_file = ".env"
           env_prefix = "THINGY_"
   ```

4. **Installation Script** (Day 2)
   ```bash
   # scripts/install.sh
   #!/bin/bash
   
   echo "Installing Nordic Thingy:52 MCP Server..."
   
   # Check Python version
   python3 --version | grep -qE "3\.(10|11|12)" || {
       echo "Error: Python 3.10+ required"
       exit 1
   }
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt
   
   # Setup Claude Desktop configuration
   python3 scripts/setup_claude.py
   
   echo "Installation complete!"
   echo "Please restart Claude Desktop."
   ```

5. **Claude Configuration Helper** (Day 2)
   ```python
   # scripts/setup_claude.py
   import json
   import os
   from pathlib import Path
   
   def setup_claude_config():
       """Setup Claude Desktop configuration"""
       
       # Detect OS and config path
       if os.name == 'posix':
           if os.uname().sysname == 'Darwin':  # macOS
               config_path = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
           else:  # Linux
               config_path = Path.home() / ".config/Claude/claude_desktop_config.json"
       else:  # Windows
           config_path = Path(os.getenv('APPDATA')) / "Claude/claude_desktop_config.json"
       
       # Get absolute path to server
       server_path = Path(__file__).parent.parent / "src/mcp_server.py"
       python_path = "python3"
       
       # Load existing config or create new
       if config_path.exists():
           with open(config_path) as f:
               config = json.load(f)
       else:
           config = {"mcpServers": {}}
       
       # Add Thingy server
       config["mcpServers"]["nordic-thingy"] = {
           "command": python_path,
           "args": [str(server_path.absolute())]
       }
       
       # Save config
       config_path.parent.mkdir(parents=True, exist_ok=True)
       with open(config_path, 'w') as f:
           json.dump(config, f, indent=2)
       
       print(f"Configuration saved to: {config_path}")
       print("Please restart Claude Desktop to activate the server.")
   
   if __name__ == "__main__":
       setup_claude_config()
   ```

6. **Documentation** (Day 3-4)
   - Complete README.md
   - Installation guide
   - User guide with examples
   - API reference
   - Troubleshooting guide
   - Contributing guide

7. **Final Testing** (Day 4-5)
   - Full integration testing
   - Cross-platform testing (macOS, Windows, Linux)
   - Real-world scenario testing
   - Performance benchmarking
   - Security audit

8. **Examples & Templates** (Day 5)
   ```python
   # examples/basic_usage.py
   """
   Basic usage examples for Nordic Thingy:52 MCP Server
   """
   
   # Example 1: Connect and read sensors
   # "Find my Thingy and connect"
   # "What's the temperature?"
   
   # Example 2: LED control
   # "Turn the LED blue"
   # "Create a breathing green effect"
   
   # Example 3: Simple automation
   # "Alert me if CO2 exceeds 1000 ppm"
   ```

#### Deliverables
- ✅ Optimized performance
- ✅ Comprehensive logging
- ✅ Easy installation process
- ✅ Complete documentation
- ✅ Example automations
- ✅ Production-ready code
- ✅ Test coverage > 90%

---

## 4. Technical Implementation Details

### 4.1 Bluetooth LE Implementation

#### Connection Management
```python
async def maintain_connection():
    """Maintain stable BLE connection"""
    while True:
        if not client.is_connected:
            try:
                await reconnect()
            except Exception as e:
                logger.error(f"Reconnection failed: {e}")
                await asyncio.sleep(5)
        await asyncio.sleep(1)
```

#### Characteristic Reading
```python
async def read_characteristic_with_retry(uuid: str, retries: int = 3):
    """Read characteristic with retry logic"""
    for attempt in range(retries):
        try:
            return await client.read_gatt_char(uuid)
        except Exception as e:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(0.5 * (attempt + 1))
```

### 4.2 Data Parsing

#### Temperature Parsing (Example)
```python
def parse_temperature(raw_data: bytes) -> float:
    """
    Thingy:52 temperature format:
    - Integer part: 1 byte (signed)
    - Decimal part: 1 byte (unsigned)
    """
    if len(raw_data) < 2:
        raise ValueError("Invalid temperature data")
    
    integer = int.from_bytes([raw_data[0]], 'little', signed=True)
    decimal = raw_data[1]
    
    return float(f"{integer}.{decimal:02d}")
```

### 4.3 LED Control

#### Color Conversion
```python
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Color names mapping
COLOR_PRESETS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255),
    'warm_white': (255, 230, 200),
    'purple': (128, 0, 128),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'orange': (255, 165, 0)
}
```

#### LED Breathing Effect
```python
async def breathing_effect(color: Tuple[int, int, int], duration: int):
    """Create breathing effect"""
    steps = 20
    delay = duration / (steps * 2)
    
    for _ in range(duration // (steps * 2 * delay)):
        # Fade in
        for i in range(steps):
            brightness = int((i / steps) * 100)
            await set_led_with_brightness(color, brightness)
            await asyncio.sleep(delay)
        
        # Fade out
        for i in range(steps, 0, -1):
            brightness = int((i / steps) * 100)
            await set_led_with_brightness(color, brightness)
            await asyncio.sleep(delay)
```

### 4.4 Automation Rule Parsing

#### Natural Language to Rule
```python
def parse_automation_request(request: str) -> AutomationRule:
    """
    Parse natural language automation request
    
    Examples:
    - "Alert if CO2 > 1000" 
    - "Flash red when temperature exceeds 25"
    - "Beep if humidity drops below 30"
    """
    # Use regex or NLP to extract:
    # 1. Sensor name
    # 2. Operator (>, <, ==, etc.)
    # 3. Threshold value
    # 4. Action (flash, beep, etc.)
    
    condition = extract_condition(request)
    action = extract_action(request)
    
    return AutomationRule(
        name=generate_rule_name(),
        conditions=[condition],
        actions=[action]
    )
```

---

## 5. Testing Strategy

### 5.1 Unit Testing

```python
# tests/unit/test_sensor_parsing.py
import pytest
from src.sensors.parsers import SensorDataParser

def test_temperature_parsing():
    """Test temperature data parsing"""
    raw_data = bytes([22, 50])  # 22.50°C
    result = SensorDataParser.parse_temperature(raw_data)
    assert result == 22.50

def test_humidity_parsing():
    """Test humidity data parsing"""
    raw_data = bytes([65])  # 65%
    result = SensorDataParser.parse_humidity(raw_data)
    assert result == 65.0

# Add tests for all parsers
```

### 5.2 Integration Testing

```python
# tests/integration/test_ble_connection.py
import pytest
from src.bluetooth.client import ThingyBLEClient
from src.device.manager import DeviceManager

@pytest.mark.asyncio
async def test_device_discovery():
    """Test device discovery"""
    manager = DeviceManager()
    devices = await manager.discover_devices(timeout=10)
    assert len(devices) > 0
    assert all(d.name.startswith("Thingy") for d in devices)

@pytest.mark.asyncio
async def test_connection_lifecycle():
    """Test connect and disconnect"""
    manager = DeviceManager()
    devices = await manager.discover_devices()
    
    # Connect
    device = await manager.connect_device(devices[0].address)
    assert device.connected
    
    # Read sensor
    data = await device.read_temperature()
    assert -40 <= data <= 85  # Valid temperature range
    
    # Disconnect
    await manager.disconnect_device()
    assert not device.connected
```

### 5.3 End-to-End Testing

```python
# tests/e2e/test_full_workflow.py
import pytest
from src.mcp_server import ThingyMCPServer

@pytest.mark.asyncio
async def test_complete_automation_workflow():
    """Test complete automation workflow"""
    server = ThingyMCPServer()
    
    # 1. Discover and connect
    devices = await server.handle_request("thingy_scan", {})
    await server.handle_request("thingy_connect", {
        "address": devices[0]["address"]
    })
    
    # 2. Read sensors
    sensors = await server.handle_request("thingy_read_sensors", {})
    assert "temperature" in sensors
    
    # 3. Create automation
    await server.handle_request("thingy_create_automation", {
        "name": "high_co2_alert",
        "condition": "CO2 > 1000",
        "action": "flash_red + beep"
    })
    
    # 4. Verify automation created
    automations = await server.handle_request("thingy_list_automations", {})
    assert any(a["name"] == "high_co2_alert" for a in automations)
    
    await server.shutdown()
```

### 5.4 Performance Testing

```python
# tests/performance/test_response_time.py
import pytest
import time

@pytest.mark.asyncio
async def test_sensor_read_latency():
    """Test sensor reading performance"""
    manager = SensorManager()
    
    times = []
    for _ in range(100):
        start = time.time()
        await manager.read_temperature()
        times.append(time.time() - start)
    
    avg_time = sum(times) / len(times)
    assert avg_time < 0.5  # Should be under 500ms
    assert max(times) < 1.0  # No single read > 1s
```

---

## 6. Deployment

### 6.1 Installation Methods

#### Method 1: Automated Installer (Recommended)
```bash
# Download and run installer
curl -sSL https://raw.githubusercontent.com/yourusername/nordic-thingy-mcp/main/scripts/install.sh | bash
```

#### Method 2: Manual Installation
```bash
# Clone repository
git clone https://github.com/yourusername/nordic-thingy-mcp.git
cd nordic-thingy-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup Claude Desktop
python3 scripts/setup_claude.py

# Restart Claude Desktop
```

#### Method 3: pip install (Future)
```bash
pip install nordic-thingy-mcp
nordic-thingy-mcp configure
```

### 6.2 Claude Desktop Configuration

#### Automatic Configuration
The `setup_claude.py` script automatically configures Claude Desktop.

#### Manual Configuration
Edit the configuration file:

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

**Content:**
```json
{
  "mcpServers": {
    "nordic-thingy": {
      "command": "python3",
      "args": ["/absolute/path/to/nordic-thingy-mcp/src/mcp_server.py"],
      "env": {
        "THINGY_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 6.3 Verification

```bash
# Test connection without Claude
python3 scripts/test_connection.py

# Expected output:
# ✓ Bluetooth available
# ✓ Found X Thingy devices
# ✓ Successfully connected
# ✓ Read sensors: Temperature 22.5°C, Humidity 45%
# ✓ LED control working
# ✓ Sound playback working
```

---

## 7. Documentation

### 7.1 Documentation Structure

```
docs/
├── README.md                    # Overview and quick start
├── INSTALLATION.md              # Detailed installation
├── USER_GUIDE.md                # User guide with examples
├── API_REFERENCE.md             # API documentation
├── AUTOMATION_GUIDE.md          # Automation examples
├── TROUBLESHOOTING.md           # Common issues
├── CONTRIBUTING.md              # Contribution guidelines
├── CHANGELOG.md                 # Version history
└── FAQ.md                       # Frequently asked questions
```

### 7.2 Key Documentation Sections

#### README.md
- Project overview
- Quick start
- Feature highlights
- Screenshots/GIFs
- Links to detailed docs

#### USER_GUIDE.md
- Getting started
- Basic usage examples
- Common workflows
- Tips and tricks
- Best practices

#### AUTOMATION_GUIDE.md
- Automation concepts
- Rule syntax
- Condition types
- Action types
- Pre-built templates
- Advanced examples

#### TROUBLESHOOTING.md
- Connection issues
- Platform-specific issues
- Error messages and solutions
- Debugging tips
- FAQ

---

## 8. Maintenance & Support

### 8.1 Version Control

```
Semantic Versioning: MAJOR.MINOR.PATCH

1.0.0 - Initial release
1.1.0 - Add new sensor support
1.0.1 - Bug fix release
2.0.0 - Breaking changes
```

### 8.2 Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in all files
- [ ] Git tag created
- [ ] GitHub release created
- [ ] PyPI package published (future)

### 8.3 Issue Management

**Bug Reports**
- Use GitHub Issues
- Require: OS, Python version, error logs
- Label: bug, priority
- Response time: < 48 hours

**Feature Requests**
- Use GitHub Discussions
- Require: use case description
- Label: enhancement
- Review cycle: monthly

---

## 9. Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| Phase 0: Setup | Week 1 | Project structure, dependencies |
| Phase 1: BLE | Week 2 | Device connection, stability |
| Phase 2: Sensors | Week 3 | All sensors readable |
| Phase 3: Actuators | Week 4 (3 days) | LED & sound control |
| Phase 4: MCP | Week 4-5 | All tools implemented |
| Phase 5: Automation | Week 5 | Automation engine |
| Phase 6: Polish | Week 6 | Production ready |

**Total: 6 weeks for MVP**

---

## 10. Success Metrics

### 10.1 Development Metrics
- ✅ Code coverage > 90%
- ✅ All P0 features complete
- ✅ Zero critical bugs
- ✅ < 100ms average tool response time

### 10.2 Quality Metrics
- ✅ Passes all linting checks
- ✅ Type hints for all functions
- ✅ Docstrings for all public APIs
- ✅ Clean code review

### 10.3 Adoption Metrics
- 🎯 100+ GitHub stars in 3 months
- 🎯 50+ active users in 1 month
- 🎯 10+ community contributions
- 🎯 5+ automation templates

---

## Appendix: Command Reference

### Development Commands
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Lint code
black src/
flake8 src/
mypy src/

# Build documentation
cd docs && make html

# Run server in dev mode
python3 src/mcp_server.py --debug
```

### Deployment Commands
```bash
# Install
./scripts/install.sh

# Configure Claude
python3 scripts/setup_claude.py

# Test connection
python3 scripts/test_connection.py

# Uninstall
./scripts/uninstall.sh
```

---

**Document End**

For questions or clarifications, please contact the development team or open an issue on GitHub.
