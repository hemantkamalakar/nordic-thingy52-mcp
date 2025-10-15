# Quick Start Guide

Get your Nordic Thingy:52 MCP Server running in 5 minutes!

## Prerequisites

- Python 3.10+ installed
- `uv` package manager ([install here](https://docs.astral.sh/uv/getting-started/installation/))
- Nordic Thingy:52 device
- Claude Desktop app installed

## Installation Steps

### 1. Clone and Setup (2 minutes)

```bash
# Clone the repository
git clone <repository-url>
cd Thingy52MCPServer

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 2. Verify Installation (1 minute)

```bash
# Run setup test to verify everything is installed correctly
python3 test_setup.py

# You should see:
# ✅ All checks passed! Your setup is ready.
```

If any checks fail, install dependencies:
```bash
uv pip install -r requirements.txt
```

### 3. Test the Server (1 minute)

```bash
# Run the server to verify it starts correctly
python3 run_server.py

# You should see startup messages like:
# ======================================================================
#   Nordic Thingy:52 MCP Server
#   Version: 1.0.0
# ======================================================================
# [INFO] Initializing Nordic Thingy:52 MCP Server...
# [INFO] FastMCP server instance created
# [INFO] Bluetooth LE client initialized
# [INFO] Starting FastMCP server...
# [INFO] Listening for MCP requests from Claude Desktop...

# Press Ctrl+C to stop
```

### 4. Configure Claude Desktop (2 minutes)

Find your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Edit it (create if doesn't exist) and add:

```json
{
  "mcpServers": {
    "thingy52": {
      "command": "python3",
      "args": [
        "run_server.py"
      ],
      "cwd": "/Users/YOUR_USERNAME/path/to/Thingy52MCPServer"
    }
  }
}
```

**Important**: Replace the `cwd` path with your **absolute** project path!

To get your absolute path:
```bash
# Run this in your project directory
pwd  # macOS/Linux
cd   # Windows (displays current directory)
```

### 5. Restart Claude Desktop

Completely quit and reopen Claude Desktop.

### 6. Power On Your Thingy:52

1. Slide the power switch on the side
2. Blue LED should pulse (advertising mode)
3. Keep it within 10 meters of your computer

## First Commands

Open Claude Desktop and try these:

```
"Find nearby Thingy devices"
```

You should see your device listed with its MAC address.

```
"Connect to device AA:BB:CC:DD:EE:FF"
```

Replace with your device's actual MAC address.

```
"What's the temperature?"
```

```
"Turn the LED red"
```

```
"Make it beep"
```

## Troubleshooting

### "Command 'uv' not found"

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# Or visit https://docs.astral.sh/uv/ for Windows
```

### "Cannot find any devices"

- Ensure Thingy is powered on (blue LED blinking)
- Check Bluetooth is enabled on your computer
- Move Thingy closer
- Try scanning again: `"Scan for Thingy devices"`

### "Server not responding in Claude"

1. Verify the path in config is absolute (no `~` or relative paths)
2. Test server manually: `python3 run_server.py`
3. Check Claude Developer Tools for error messages
4. Restart Claude Desktop completely
5. Make sure dependencies are installed: `uv pip install -r requirements.txt`

### "Connection failed"

- Close Nordic Thingy app if running
- Restart Thingy (power off/on)
- Ensure no other apps are connected to it
- Try: `"Disconnect"` then `"Connect"` again

## What's Next?

- See [README.md](README.md) for full documentation
- Check [CLAUDE.md](CLAUDE.md) for development details
- Explore all available commands in README

## Example Use Cases

Once connected, try:

```
"Read all sensors"
"Set LED to breathing blue effect"
"What's the air quality?"
"Check the battery level"
"Turn LED to warm white"
"Play sound 3"
```

---

🎉 **You're all set! Enjoy controlling your Thingy with natural language!**
