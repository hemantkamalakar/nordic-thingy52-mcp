# Testing Guide

## Running the MCP Server

### Method 1: Direct Python (Simplest)

```bash
# From the project directory
python3 run_server.py
```

Press Ctrl+C to stop.

### Method 2: Using uv

```bash
uv run python3 run_server.py
```

### Method 3: With virtual environment

```bash
# Activate virtual environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Run server
python3 run_server.py
```

## Testing with Claude Desktop

1. Configure `claude_desktop_config.json` (see QUICKSTART.md)
2. Restart Claude Desktop completely
3. Open Claude and try:
   - "Scan for Thingy devices"
   - "What tools do you have available?"

## Manual Testing (without hardware)

You can test the MCP server responds correctly even without a Thingy device:

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run server
python3 run_server.py
```

The server will start and expose all MCP tools. When you try to scan or connect, you'll get appropriate error messages if no Thingy is nearby.

## Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run all tests
uv run pytest tests/

# Run with verbose output
uv run pytest tests/ -v

# Run with coverage
uv run pytest --cov=src tests/

# Run specific test file
uv run pytest tests/test_models.py
```

## Code Quality Checks

### Formatting

```bash
# Check formatting
uv run black --check src/

# Apply formatting
uv run black src/
```

### Linting

```bash
# Run ruff linter
uv run ruff check src/

# Fix auto-fixable issues
uv run ruff check --fix src/
```

### Type Checking

```bash
# Run mypy type checker
uv run mypy src/
```

## Integration Testing with Hardware

### Prerequisites
- Nordic Thingy:52 powered on
- Bluetooth enabled on computer
- Device within 10 meters

### Test Sequence

1. **Scan for devices**
   ```
   Ask Claude: "Scan for Thingy devices"
   Expected: List of nearby devices with MAC addresses
   ```

2. **Connect to device**
   ```
   Ask Claude: "Connect to device AA:BB:CC:DD:EE:FF"
   Expected: Success message
   ```

3. **Read sensors**
   ```
   Ask Claude: "Read all sensors"
   Expected: Temperature, humidity, pressure, CO2, TVOC readings
   ```

4. **LED control**
   ```
   Ask Claude: "Turn the LED blue"
   Expected: LED turns blue

   Ask Claude: "Set LED to breathing green effect"
   Expected: LED pulses green
   ```

5. **Sound**
   ```
   Ask Claude: "Make it beep"
   Expected: Beep sound from Thingy
   ```

6. **Disconnect**
   ```
   Ask Claude: "Disconnect from device"
   Expected: Success message
   ```

## Debugging

### Enable Debug Logging

Edit `src/server.py` and change:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

### Check Claude Logs

1. Open Claude Desktop
2. Help → Developer Tools
3. Go to Console tab
4. Look for MCP server messages

### Common Issues

**Import Error**
```
ModuleNotFoundError: No module named 'mcp'
```
Solution: Install dependencies
```bash
uv pip install -r requirements.txt
```

**Bluetooth Permission Error**
Solution: Grant Bluetooth permissions to Terminal/Claude Desktop in System Settings

**Connection Timeout**
- Check Thingy is powered on
- Ensure Bluetooth is enabled
- Move Thingy closer
- Restart Thingy

## Performance Testing

### Response Time Test

```python
import time
from src.bluetooth_client import ThingyBLEClient

async def test_performance():
    client = ThingyBLEClient()

    # Connect
    start = time.time()
    await client.connect("AA:BB:CC:DD:EE:FF")
    print(f"Connection time: {time.time() - start:.2f}s")

    # Read sensor
    start = time.time()
    temp = await client.read_temperature()
    print(f"Sensor read time: {time.time() - start:.2f}s")

    await client.disconnect()
```

Expected:
- Connection: < 5 seconds
- Single sensor read: < 500ms
- All sensors read: < 1 second

## Continuous Integration

The project is set up for CI/CD with pytest:

```yaml
# .github/workflows/test.yml (example)
- name: Run tests
  run: |
    uv pip install -r requirements.txt
    uv pip install -e ".[dev]"
    pytest tests/ --cov=src
```

## Test Coverage Goals

- **Overall**: 85%+
- **Models**: 95%+ (data validation)
- **Bluetooth Client**: 80%+ (hardware dependent)
- **Server**: 70%+ (integration dependent)

## Contributing Tests

When adding new features:

1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain or improve coverage
4. Update this guide with new test cases

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Bleak testing tips](https://bleak.readthedocs.io/en/latest/troubleshooting.html)
