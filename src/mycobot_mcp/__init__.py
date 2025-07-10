"""MCP Server for ElephantRobotics MyCobot"""
import argparse
from .server import mcp

__version__ = "0.1.0"

def main():
    """MyCobot MCP: Control ElephantRobotics robotic arms via natural language."""
    parser = argparse.ArgumentParser(
        description="Control ElephantRobotics MyCobot series robotic arms through MCP protocol."
    )
    parser.parse_args()
    mcp.run()

__all__ = ["main", "mcp"] 