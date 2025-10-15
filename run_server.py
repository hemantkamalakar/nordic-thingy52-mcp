#!/usr/bin/env python3
"""
Simple entry point to run the MCP server.

This script can be run directly without installing the package:
    python3 run_server.py
"""

import sys
import logging

if __name__ == "__main__":
    try:
        print("\n🚀 Starting Nordic Thingy:52 MCP Server...\n")

        # Import and run the server
        from src.server import mcp
        mcp.run()

    except ImportError as e:
        print("\n❌ Error: Failed to import required modules")
        print(f"   {e}")
        print("\n💡 Make sure you've installed the dependencies:")
        print("   uv pip install -r requirements.txt\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        sys.exit(1)
