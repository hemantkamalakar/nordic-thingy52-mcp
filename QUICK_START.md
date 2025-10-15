# Quick Start Guide
## Get Your Nordic Thingy:52 MCP Server Running in Minutes

This guide will help you get from zero to controlling your Thingy:52 with Claude Desktop in under 30 minutes.

---

## Prerequisites

### Hardware
- ✅ **Nordic Thingy:52 device** ([Purchase here](https://www.nordicsemi.com/Products/Development-hardware/Nordic-Thingy-52))
- ✅ **Computer with Bluetooth LE** (most modern laptops have this)
- ✅ **Charged Thingy** (or USB cable to charge)

### Software
- ✅ **Python 3.10 or higher**
  ```bash
  # Check your Python version
  python3 --version
  # Should output: Python 3.10.x or higher
  ```

- ✅ **Claude Desktop** ([Download here](https://claude.ai/download))

- ✅ **Git** (to clone the repository)
  ```bash
  # Check if Git is installed
  git --version
  ```

---

## Step 1: Clone and Setup (5 minutes)

### Option A: Automated Setup (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/nordic-thingy-mcp.git
cd nordic-thingy-mcp

# 2. Run the automated installer
chmod +x scripts/install.sh
./scripts/install.sh

# The script will:
# - Create a virtual environment
# - Install all dependencies
# - Configure Claude Desktop
# - Verify everything is working
```

### Option B: Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/nordic-thingy-mcp.git
cd nordic-thingy-mcp

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Configure Claude Desktop
python3 scripts/setup_claude.py
```

---

## Step 2: Prepare Your Thingy (2 minutes)

1. **Power On**
   - Slide the power switch on the side of the Thingy to ON
   - You should see a blue LED pulsing (this means it's advertising)

2. **Check Battery**
   - If LED doesn't turn on, charge via USB for at least 5 minutes
   - The Thingy can stay plugged in during use

3. **Keep Nearby**
   - Keep the Thingy within 10 meters (30 feet) of your computer
   - Avoid obstacles between the device and computer

---

## Step 3: Restart Claude Desktop (1 minute)

1. **Quit Claude Desktop completely**
   - macOS: Cmd+Q or right-click dock icon → Quit
   - Windows: File → Exit or close from system tray
   - Linux: Close window and ensure process is terminated

2. **Reopen Claude Desktop**
   - Launch the application normally
   - Wait for it to fully load

3. **Verify Server Loaded**
   - You should see no error messages
   - The server loads silently in the background

---

## Step 4: Your First Commands (5 minutes)

Now comes the fun part! Try these commands in Claude Desktop:

### 1. Discover Your Thingy
```
"Find my Nordic Thingy"
```

Claude should respond with a list of nearby devices, showing:
- Device names (usually "Thingy" + numbers)
- MAC addresses
- Signal strength (RSSI)

### 2. Connect
```
"Connect to the Thingy"
```

If multiple devices were found, Claude will ask which one. You can say:
- "Connect to the first one"
- "Connect to XX:XX:XX:XX:XX:XX" (using the MAC address)

### 3. Check Status
```
"What's the status of my Thingy?"
```

Should show:
- ✅ Connected
- 🔋 Battery level
- 📡 Signal strength

### 4. Read Sensors
```
"What's the temperature?"
```

Or try:
```
"Check all sensors"
```

Should display:
- 🌡️ Temperature
- 💧 Humidity  
- 🔽 Pressure
- 🌫️ CO2
- 🌬️ TVOC
- 🎨 Light/Color

### 5. Control the LED
```
"Turn the LED red"
```

Your Thingy's LED should turn red!

Try other colors:
```
"Set LED to blue"
"Turn LED green"
"Make the LED warm white"
```

### 6. Create Effects
```
"Create a breathing blue effect"
```

The LED should slowly pulse blue.

### 7. Play Sounds
```
"Make it beep"
```

You should hear a short beep from the Thingy!

Try different sounds:
```
"Play sound 3"
"Play sound 5"
```

---

## Step 5: Set Up Your First Automation (5 minutes)

Now let's create a useful automation:

### Air Quality Monitor
```
"Monitor the air quality. If CO2 exceeds 1000 ppm, flash the LED red and beep twice"
```

Claude will:
1. Create an automation rule
2. Start monitoring CO2 levels
3. Alert you when thresholds are exceeded

### Test the Automation
```
"What automations are running?"
```

Should show your newly created rule.

To manually test:
```
"What's the current CO2 level?"
```

### More Automation Ideas

**Meeting Room Indicator:**
```
"Create a meeting room indicator:
- Green LED when CO2 is below 800 ppm
- Yellow when CO2 is 800-1200 ppm  
- Red when CO2 is above 1200 ppm"
```

**Temperature Alert:**
```
"Alert me if the temperature goes above 25°C"
```

**Motion Detection:**
```
"Alert me if you detect motion between 10 PM and 6 AM"
```

---

## Common First-Time Issues

### "Can't find any Thingy devices"

**Solutions:**
1. ✅ Check Thingy is powered on (blue LED pulsing)
2. ✅ Check Bluetooth is enabled on your computer
3. ✅ Move Thingy closer to computer
4. ✅ Try: "Scan for devices again" or restart Thingy

**Verify Bluetooth:**
```bash
# macOS
system_profiler SPBluetoothDataType

# Linux
hcitool dev
```

### "Connection failed"

**Solutions:**
1. ✅ Restart the Thingy (power off/on)
2. ✅ Try: "Disconnect and reconnect"
3. ✅ Check no other app is connected to the Thingy
4. ✅ Close the official Nordic Thingy app if running

### "Server not responding"

**Solutions:**
1. ✅ Restart Claude Desktop completely
2. ✅ Check the configuration file:
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Should contain "nordic-thingy" entry
   ```
3. ✅ Re-run setup: `python3 scripts/setup_claude.py`
4. ✅ Check server logs in Claude's Developer Tools

### "Python version too old"

**Solution:**
```bash
# macOS (using Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt update
sudo apt install python3.11

# Windows
# Download from python.org
```

---

## Testing Without Claude (Optional)

You can test the Thingy connection directly:

```bash
# Activate virtual environment first
source venv/bin/activate

# Run the test script
python3 scripts/test_connection.py
```

This will:
- ✅ Scan for devices
- ✅ Attempt connection
- ✅ Read sensors
- ✅ Test LED control
- ✅ Test sound playback

---

## Next Steps

Now that you're up and running:

### 📚 Learn More
- Read the [User Guide](docs/USER_GUIDE.md) for detailed features
- Check out [Automation Guide](docs/AUTOMATION_GUIDE.md) for advanced automation
- Browse [Example Automations](examples/automation_examples.py)

### 🎨 Customize
- Create your own automations
- Adjust sensor read intervals
- Configure LED effects
- Set up scenes

### 🤝 Join Community
- ⭐ Star the repository on GitHub
- Share your automations in Discussions
- Report bugs or request features
- Contribute improvements

### 🏗️ Build Projects
Some ideas to get started:
- **Smart Office Monitor**: Track air quality and adjust ventilation
- **Meeting Room Status**: Visual indicator of room availability
- **Plant Monitor**: Track humidity and temperature for plants
- **Security System**: Motion detection alerts
- **Sleep Tracker**: Monitor bedroom environment
- **Workout Companion**: Track movement and count reps

---

## Pro Tips

### Tip 1: Use Natural Language
Claude understands context, so you don't need exact commands:
```
✅ "What's the temp?"
✅ "Is the air quality good?"
✅ "Make it glow blue"
✅ "Set up an alert for high humidity"
```

### Tip 2: Chain Commands
You can give multiple instructions:
```
"Connect to my Thingy, check all sensors, then set the LED to green if air quality is good, or red if it's bad"
```

### Tip 3: Ask for Explanations
```
"Why is the CO2 level important?"
"What does TVOC measure?"
"What's a good humidity range for my home?"
```

### Tip 4: Save Automations
Keep a note of automations that work well for you, so you can recreate them easily.

### Tip 5: Monitor Battery
Check battery regularly:
```
"What's the battery level?"
```

Charge when below 20% for best longevity.

---

## Quick Reference Card

### Discovery & Connection
| Command | What It Does |
|---------|-------------|
| "Find my Thingy" | Scan for devices |
| "Connect to [device]" | Connect to device |
| "Disconnect" | Disconnect current device |
| "Device status?" | Check connection |
| "Battery level?" | Check battery |

### Sensors
| Command | What It Does |
|---------|-------------|
| "What's the temperature?" | Read temperature |
| "Check humidity" | Read humidity |
| "Air quality?" | Read CO2 and TVOC |
| "Read all sensors" | Read everything |

### LED Control
| Command | What It Does |
|---------|-------------|
| "Turn LED [color]" | Set solid color |
| "LED breathing [color]" | Breathing effect |
| "Flash LED [color]" | Flash effect |
| "LED off" | Turn off LED |

### Sounds
| Command | What It Does |
|---------|-------------|
| "Beep" | Quick beep |
| "Play sound [1-8]" | Play preset sound |

### Automation
| Command | What It Does |
|---------|-------------|
| "Alert if [condition]" | Create alert rule |
| "Monitor [sensor]" | Start monitoring |
| "List automations" | Show active rules |
| "Delete [automation]" | Remove rule |

---

## Getting Help

### Documentation
- 📖 [Full User Guide](docs/USER_GUIDE.md)
- 🔧 [Troubleshooting](docs/TROUBLESHOOTING.md)
- ❓ [FAQ](docs/FAQ.md)

### Support Channels
- 💬 GitHub Issues: For bugs and feature requests
- 💡 GitHub Discussions: For questions and ideas
- 📧 Email: your-email@example.com
- 🐦 Twitter: @yourhandle

---

## Congratulations! 🎉

You're now controlling your Nordic Thingy:52 with Claude Desktop!

Enjoy exploring the capabilities, creating automations, and building cool IoT projects.

**Happy Hacking!** 🚀

---

*Last Updated: October 15, 2025*
*Version: 1.0*
