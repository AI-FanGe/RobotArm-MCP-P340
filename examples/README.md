# RobotArm MCP P340 Examples

This directory contains examples and guides for using the MyCobot MCP server.

## Files

- **example_config.json** - Basic Cursor configuration example
- **demo_action_sequence.py** - Python example showing how to design action sequences
- **ACTION_SEQUENCE_GUIDE.md** - Detailed guide for creating custom action sequences

## Quick Start

1. Copy `example_config.json` to your Cursor configuration
2. Modify paths according to your environment
3. Set `SIMULATE: "1"` for testing without hardware
4. Restart Cursor to load the MCP server

## Testing Action Sequences

Run the demo script to see example action sequences:

```bash
python demo_action_sequence.py
```

Note: This requires the MCP server to be running and connected. 