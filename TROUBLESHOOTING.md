# Troubleshooting Guide

## Installation Issues

### "No module named 'mcp'"

**Problem**: FastMCP SDK not installed

**Solution**:
```bash
uv pip install -r requirements.txt
```

Verify with:
```bash
python3 test_setup.py
```

### "No module named 'bleak'"

**Problem**: Bleak (Bluetooth library) not installed

**Solution**:
```bash
uv pip install bleak
```

### "Python version too old"

**Problem**: Python < 3.10

**Solution**: Install Python 3.10 or higher
- macOS: `brew install python@3.11`
- Ubuntu: `sudo apt install python3.11`
- Windows: Download from python.org

## Server Issues

### Server starts but shows no output

**Expected**: The server should show startup messages like:
```
======================================================================
  Nordic Thingy:52 MCP Server
  Version: 1.0.0
======================================================================
[INFO] Initializing Nordic Thingy:52 MCP Server...
```

**If you see nothing**:
1. Check you're running the right file: `python3 run_server.py`
2. Check dependencies: `python3 test_setup.py`
3. Try running with verbose output: Edit `src/server.py` and change `level=logging.DEBUG`

### "Server not responding" in Claude

**Problem**: Claude can't connect to the MCP server

**Solutions**:

1. **Verify configuration path is absolute**:
   ```json
   "cwd": "/Users/username/path/to/Thingy52MCPServer"  ✓ Good
   "cwd": "~/path/to/Thingy52MCPServer"                ✗ Bad (~ not expanded)
   "cwd": "./Thingy52MCPServer"                        ✗ Bad (relative)
   ```

2. **Test server manually**:
   ```bash
   cd /path/to/Thingy52MCPServer
   python3 run_server.py
   ```
   Should show startup messages.

3. **Check Claude Developer Tools**:
   - Open Claude Desktop
   - Help → Developer Tools
   - Console tab → Look for errors

4. **Restart Claude completely**:
   - Quit Claude Desktop (Cmd+Q on Mac)
   - Relaunch

5. **Check the config file location**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

### "ImportError" when running server

**Problem**: Can't import src modules

**Solution**:
Make sure you're running from the project root:
```bash
cd /path/to/Thingy52MCPServer
python3 run_server.py
```

## Bluetooth Issues

### "Cannot find any Thingy devices"

**Checklist**:
- [ ] Thingy is powered on (blue LED pulsing)
- [ ] Bluetooth enabled on computer
- [ ] Thingy within 10 meters
- [ ] No other app connected to Thingy

**Solutions**:

1. **Check Bluetooth on your computer**:
   ```bash
   # macOS
   system_profiler SPBluetoothDataType | grep "Bluetooth Power"

   # Linux
   hcitool dev

   # Should show Bluetooth is on
   ```

2. **Restart Thingy**:
   - Power off (slide switch)
   - Wait 3 seconds
   - Power on (blue LED should pulse)

3. **Close other Bluetooth apps**:
   - Close Nordic Thingy mobile app
   - Close nRF Connect
   - Disconnect from phone Bluetooth

4. **Increase scan timeout**:
   ```
   Claude: "Scan for devices with timeout 20 seconds"
   ```

### "Connection failed"

**Common causes**:
- Thingy already connected to another device
- Bluetooth interference
- Out of range
- Low battery on Thingy

**Solutions**:

1. **Ensure only one connection**:
   - Close Nordic Thingy app
   - Disconnect from phone
   - Try: `"Disconnect"` then `"Connect"` again

2. **Power cycle Thingy**:
   - Turn off → wait 5s → turn on

3. **Check battery**:
   - Charge Thingy via USB
   - Wait 5 minutes
   - Try again

4. **Reduce distance**:
   - Move Thingy closer (< 3 meters)
   - Remove obstacles

### "Connection drops frequently"

**Causes**:
- Low battery
- Interference (WiFi, microwave)
- Out of range
- Firmware issue

**Solutions**:

1. **Charge the battery**:
   - Connect USB cable
   - Charge for 30+ minutes

2. **Reduce interference**:
   - Move away from WiFi router
   - Turn off microwave
   - Avoid metal obstacles

3. **Update firmware** (advanced):
   - Use Nordic Thingy app
   - Download latest firmware from Nordic

## Platform-Specific Issues

### macOS

**"Bluetooth permission denied"**

Solution:
1. System Settings → Privacy & Security → Bluetooth
2. Add Terminal/iTerm (or whichever terminal you use)
3. Restart terminal
4. Try again

**"Command not found: python3"**

Solution:
```bash
# Install Python via Homebrew
brew install python@3.11

# Or use system Python
python3 --version
```

### Windows

**"Python not found"**

Solution:
1. Download Python from python.org
2. During install, check "Add Python to PATH"
3. Restart terminal
4. Verify: `python --version` or `py --version`

**Bluetooth driver issues**

Solution:
1. Device Manager → Bluetooth
2. Update Bluetooth driver
3. Restart computer

### Linux

**"Permission denied" for Bluetooth**

Solution:
```bash
# Add user to bluetooth group
sudo usermod -a -G bluetooth $USER

# Logout and login again (or restart)
```

**"hciconfig: command not found"**

Solution:
```bash
# Install BlueZ
sudo apt install bluez bluez-tools

# Start Bluetooth service
sudo systemctl start bluetooth
sudo systemctl enable bluetooth
```

## Performance Issues

### Slow sensor readings

**Normal behavior**:
- Single sensor: < 500ms
- All sensors: < 1 second

**If slower**:
- Check Bluetooth signal (RSSI)
- Reduce distance to Thingy
- Close other Bluetooth devices
- Restart Thingy

### High CPU usage

**Causes**:
- Continuous scanning
- Multiple rapid requests
- Debug logging enabled

**Solutions**:
1. Don't scan continuously
2. Wait for responses before next request
3. Change logging to INFO (not DEBUG)

## Data Issues

### Sensor readings seem wrong

**CO2 sensor**:
- Needs 5 minutes to stabilize after power on
- Don't cover the sensor
- Normal indoor: 400-1000 ppm

**Temperature**:
- Device self-heating if in sun or enclosed
- Allow air circulation
- Normal range: -10°C to 40°C indoors

**Humidity**:
- Sensor may need calibration
- Normal indoor: 30-60%

## Getting More Help

### Enable Debug Logging

Edit `src/server.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    ...
)
```

### Check Logs

1. **Server logs**: Visible in terminal where you run `python3 run_server.py`

2. **Claude logs**: Claude Desktop → Help → Developer Tools → Console

### Collect Information

When reporting issues, include:
1. Operating system and version
2. Python version: `python3 --version`
3. Output of: `python3 test_setup.py`
4. Error messages (full output)
5. Steps to reproduce

### Resources

- [Nordic Thingy:52 User Guide](https://infocenter.nordicsemi.com/topic/ug_thingy52/)
- [Bleak Documentation](https://bleak.readthedocs.io/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Project GitHub Issues](https://github.com/yourrepo/issues)

## Common Error Messages

### "ConnectionError: Not connected to a device"

**Cause**: Trying to read sensor before connecting

**Solution**:
1. First: `"Scan for devices"`
2. Then: `"Connect to device AA:BB:CC:DD:EE:FF"`
3. Then: `"Read temperature"`

### "ValueError: Sound ID must be between 1 and 8"

**Cause**: Invalid sound ID

**Solution**: Use sound IDs 1-8 only
```
"Play sound 1"  ✓
"Play sound 9"  ✗
```

### "Unknown color 'xyz'"

**Cause**: Color name not recognized

**Solution**: Use available colors:
- red, green, blue, white, warm_white, cool_white
- yellow, cyan, magenta, purple, orange, pink

Or use RGB:
```
"Set LED to RGB 255,100,50"
```

## Still Having Issues?

1. **Reset everything**:
   ```bash
   # Stop the server (Ctrl+C)
   # Power cycle Thingy
   # Restart Claude Desktop
   # Try again
   ```

2. **Start fresh**:
   ```bash
   # Remove virtual environment
   rm -rf .venv

   # Reinstall
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   python3 test_setup.py
   ```

3. **Ask for help**:
   - Check GitHub Issues
   - Create new issue with details above
   - Include `test_setup.py` output
