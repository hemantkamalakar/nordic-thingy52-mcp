#!/usr/bin/env python3
"""
Test script to verify the MCP server setup.

Run this to check if all dependencies are installed correctly:
    python3 test_setup.py
"""

import sys

print("\n" + "=" * 70)
print("  Nordic Thingy:52 MCP Server - Setup Test")
print("=" * 70 + "\n")

# Track if all checks pass
all_passed = True

# Check Python version
print("✓ Checking Python version...")
if sys.version_info >= (3, 10):
    print(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor} - OK")
else:
    print(f"  ✗ Python {sys.version_info.major}.{sys.version_info.minor} - NEED 3.10+")
    all_passed = False

# Check required imports
dependencies = [
    ("mcp.server.fastmcp", "FastMCP (MCP SDK)"),
    ("bleak", "Bleak (Bluetooth LE)"),
    ("pydantic", "Pydantic (Data validation)"),
]

print("\n✓ Checking dependencies...")
for module, name in dependencies:
    try:
        __import__(module)
        print(f"  ✓ {name} - Installed")
    except ImportError:
        print(f"  ✗ {name} - NOT FOUND")
        all_passed = False

# Check if our modules can be imported
print("\n✓ Checking project modules...")
try:
    from src.constants import LED_COLORS
    print(f"  ✓ src.constants - OK")
except ImportError as e:
    print(f"  ✗ src.constants - FAILED: {e}")
    all_passed = False

try:
    from src.models import DeviceInfo
    print(f"  ✓ src.models - OK")
except ImportError as e:
    print(f"  ✗ src.models - FAILED: {e}")
    all_passed = False

try:
    from src.bluetooth_client import ThingyBLEClient
    print(f"  ✓ src.bluetooth_client - OK")
except ImportError as e:
    print(f"  ✗ src.bluetooth_client - FAILED: {e}")
    all_passed = False

try:
    from src.server import mcp
    print(f"  ✓ src.server - OK")
except ImportError as e:
    print(f"  ✗ src.server - FAILED: {e}")
    all_passed = False

# Summary
print("\n" + "=" * 70)
if all_passed:
    print("✅ All checks passed! Your setup is ready.")
    print("\nNext steps:")
    print("  1. Run: python3 run_server.py")
    print("  2. Configure Claude Desktop (see QUICKSTART.md)")
    print("  3. Restart Claude Desktop")
else:
    print("❌ Some checks failed. Please fix the issues above.")
    print("\nTo install dependencies:")
    print("  uv pip install -r requirements.txt")
print("=" * 70 + "\n")

sys.exit(0 if all_passed else 1)
