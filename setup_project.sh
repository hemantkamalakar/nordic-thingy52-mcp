#!/bin/bash

# Nordic Thingy:52 MCP Server - Setup Script
# This script helps you get started with implementing the MCP server

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Nordic Thingy:52 MCP Server - Project Setup             ║"
echo "║   Production-Ready Implementation for Claude Desktop      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running on supported OS
print_status "Checking operating system..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    print_success "Linux detected"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    print_success "macOS detected"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS="windows"
    print_success "Windows detected"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

# Check Python version
print_status "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        print_success "Python $PYTHON_VERSION found (✓ >= 3.10)"
    else
        print_error "Python 3.10 or higher required. Found: $PYTHON_VERSION"
        echo "Please install Python 3.10+ from https://www.python.org/downloads/"
        exit 1
    fi
else
    print_error "Python 3 not found"
    echo "Please install Python 3.10+ from https://www.python.org/downloads/"
    exit 1
fi

# Check Git
print_status "Checking Git installation..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    print_success "Git $GIT_VERSION found"
else
    print_error "Git not found"
    echo "Please install Git from https://git-scm.com/downloads"
    exit 1
fi

# Ask for project directory
echo ""
print_status "Where would you like to create your project?"
read -p "Enter directory path (default: ./nordic-thingy-mcp): " PROJECT_DIR
PROJECT_DIR=${PROJECT_DIR:-./nordic-thingy-mcp}

# Create project directory
print_status "Creating project directory: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"
print_success "Project directory created"

# Initialize Git repository
print_status "Initializing Git repository..."
git init
print_success "Git repository initialized"

# Create project structure
print_status "Creating project structure..."

# Create directory structure
mkdir -p src/{bluetooth,device,sensors,actuators,automation,tools,utils}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p examples
mkdir -p docs
mkdir -p scripts
mkdir -p .github/workflows

print_success "Project structure created"

# Create requirements.txt
print_status "Creating requirements.txt..."
cat > requirements.txt << 'EOF'
# Core dependencies
bleak>=0.21.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
aiofiles>=23.0.0
python-dateutil>=2.8.0

# Logging and utilities
colorama>=0.4.6

# MCP SDK (update version as needed)
# anthropic-mcp-sdk>=1.0.0
EOF

print_success "requirements.txt created"

# Create dev-requirements.txt
print_status "Creating dev-requirements.txt..."
cat > dev-requirements.txt << 'EOF'
# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0

# Linting and formatting
black>=23.7.0
flake8>=6.1.0
mypy>=1.5.0
pylint>=2.17.0

# Documentation
sphinx>=7.1.0
sphinx-rtd-theme>=1.3.0
EOF

print_success "dev-requirements.txt created"

# Create .gitignore
print_status "Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Configuration
.env
config.local.toml

# Data
data/
*.db
*.sqlite
EOF

print_success ".gitignore created"

# Create README.md
print_status "Creating README.md..."
cat > README.md << 'EOF'
# Nordic Thingy:52 MCP Server

Production-ready MCP server for controlling Nordic Thingy:52 IoT devices through Claude Desktop.

## Features

- 🔍 Device discovery and connection management
- 📊 Environmental sensor reading (temp, humidity, pressure, CO2, TVOC)
- 🎯 9-axis motion sensing with advanced processing
- 💡 RGB LED control with effects
- 🔊 Sound playback and audio streaming
- 🤖 AI-powered automation engine
- 🔄 Real-time monitoring and alerts

## Quick Start

See [QUICK_START.md](docs/QUICK_START.md) for setup instructions.

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [User Guide](docs/USER_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Automation Guide](docs/AUTOMATION_GUIDE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt

# Run tests
pytest tests/
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md).
EOF

print_success "README.md created"

# Create initial Python files
print_status "Creating initial Python files..."

# src/__init__.py
cat > src/__init__.py << 'EOF'
"""
Nordic Thingy:52 MCP Server
Production-ready implementation for Claude Desktop
"""

__version__ = "1.0.0"
__author__ = "Your Name"
EOF

# src/constants.py
cat > src/constants.py << 'EOF'
"""
Constants and UUIDs for Nordic Thingy:52
"""

# Service UUIDs
ENVIRONMENT_SERVICE_UUID = "EF680200-9B35-4933-9B10-52FFA9740042"
MOTION_SERVICE_UUID = "EF680400-9B35-4933-9B10-52FFA9740042"
UI_SERVICE_UUID = "EF680300-9B35-4933-9B10-52FFA9740042"
SOUND_SERVICE_UUID = "EF680500-9B35-4933-9B10-52FFA9740042"
BATTERY_SERVICE_UUID = "0000180F-0000-1000-8000-00805F9B34FB"

# Environment Characteristic UUIDs
TEMPERATURE_UUID = "EF680201-9B35-4933-9B10-52FFA9740042"
PRESSURE_UUID = "EF680202-9B35-4933-9B10-52FFA9740042"
HUMIDITY_UUID = "EF680203-9B35-4933-9B10-52FFA9740042"
AIR_QUALITY_UUID = "EF680204-9B35-4933-9B10-52FFA9740042"
COLOR_UUID = "EF680205-9B35-4933-9B10-52FFA9740042"

# UI Characteristic UUIDs
LED_UUID = "EF680301-9B35-4933-9B10-52FFA9740042"
BUTTON_UUID = "EF680302-9B35-4933-9B10-52FFA9740042"

# Sound Characteristic UUIDs
SPEAKER_DATA_UUID = "EF680501-9B35-4933-9B10-52FFA9740042"
SPEAKER_STATUS_UUID = "EF680502-9B35-4933-9B10-52FFA9740042"
MICROPHONE_UUID = "EF680503-9B35-4933-9B10-52FFA9740042"

# Motion Characteristic UUIDs
# (To be added based on firmware documentation)

# Battery UUID
BATTERY_LEVEL_UUID = "00002A19-0000-1000-8000-00805F9B34FB"

# Device name patterns
THINGY_NAME_PATTERNS = ["Thingy", "Nordic Thingy"]

# LED Colors (RGB presets)
LED_COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255),
    'warm_white': (255, 230, 200),
    'cool_white': (200, 230, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'purple': (128, 0, 128),
    'orange': (255, 165, 0),
    'pink': (255, 192, 203),
}
EOF

# Create main server file
cat > src/mcp_server.py << 'EOF'
#!/usr/bin/env python3
"""
Nordic Thingy:52 MCP Server
Main entry point for the MCP server
"""

import asyncio
import sys
from typing import Any, Dict

# MCP imports (update based on actual MCP SDK)
# from anthropic_mcp import MCPServer, Tool

from constants import __version__


class ThingyMCPServer:
    """MCP Server for Nordic Thingy:52 devices"""
    
    def __init__(self):
        self.version = __version__
        self.running = False
        
    async def start(self):
        """Start the MCP server"""
        print(f"Starting Nordic Thingy:52 MCP Server v{self.version}")
        self.running = True
        
        # TODO: Initialize components
        # - Device Manager
        # - Sensor Manager
        # - LED Controller
        # - Sound Controller
        # - Automation Engine
        
        # TODO: Register MCP tools
        
        print("Server started successfully")
        
    async def stop(self):
        """Stop the MCP server"""
        print("Stopping server...")
        self.running = False
        
        # TODO: Cleanup
        # - Disconnect devices
        # - Stop monitoring
        # - Save state
        
        print("Server stopped")
        
    async def run(self):
        """Run the server"""
        await self.start()
        
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nReceived interrupt signal")
        finally:
            await self.stop()


def main():
    """Main entry point"""
    server = ThingyMCPServer()
    
    try:
        asyncio.run(server.run())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
EOF

chmod +x src/mcp_server.py
print_success "Initial Python files created"

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv
print_success "Virtual environment created"

# Activate and install dependencies
print_status "Installing dependencies..."
if [ "$OS" = "windows" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencies installed"

# Create initial commit
print_status "Creating initial commit..."
git add .
git commit -m "Initial project structure

- Set up project directories
- Created requirements files
- Added core constants
- Implemented basic server structure
- Added configuration files"
print_success "Initial commit created"

# Print success message
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║             ✓ Setup Complete!                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
print_success "Your Nordic Thingy:52 MCP Server project is ready!"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the virtual environment:"
echo "   ${YELLOW}cd $PROJECT_DIR${NC}"
if [ "$OS" = "windows" ]; then
    echo "   ${YELLOW}venv\\Scripts\\activate${NC}"
else
    echo "   ${YELLOW}source venv/bin/activate${NC}"
fi
echo ""
echo "2. Review the documentation:"
echo "   - Read ${BLUE}PRODUCT_REQUIREMENTS_DOCUMENT.md${NC} for feature specs"
echo "   - Follow ${BLUE}IMPLEMENTATION_PLAN.md${NC} for development roadmap"
echo "   - Check ${BLUE}QUICK_START.md${NC} for user experience"
echo ""
echo "3. Start implementing Phase 0 (Week 1):"
echo "   - Complete the project structure"
echo "   - Define all Thingy:52 UUIDs in src/constants.py"
echo "   - Set up CI/CD pipeline"
echo ""
echo "4. Clone reference implementation for study:"
echo "   ${YELLOW}git clone https://github.com/karthiksuku/nordic-thingy-mcp.git reference${NC}"
echo ""
echo "5. Run tests as you develop:"
echo "   ${YELLOW}pytest tests/${NC}"
echo ""
echo "Happy coding! 🚀"
echo ""
