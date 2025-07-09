# Contributing to MyCobot MCP

Thank you for your interest in contributing to MyCobot MCP!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/[yourusername]/mycobot-mcp.git
   cd mycobot-mcp
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Install in development mode:
   ```bash
   pip install -e .
   ```

## Testing

Test in simulation mode:
```bash
export SIMULATE=1  # On Windows: set SIMULATE=1
python -m mycobot_mcp.server
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Submitting Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request

## Reporting Issues

Please use the GitHub issue tracker to report bugs or request features. 