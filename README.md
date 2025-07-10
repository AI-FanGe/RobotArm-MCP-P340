# RobotArm MCP P340

[![PyPI version](https://badge.fury.io/py/robotarm-mcp-p340.svg)](https://pypi.org/project/robotarm-mcp-p340/)
[![Python](https://img.shields.io/pypi/pyversions/robotarm-mcp-p340.svg)](https://pypi.org/project/robotarm-mcp-p340/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](#english) | [中文](#chinese)

<a name="english"></a>
## Overview

A Model Context Protocol (MCP) server implementation that provides natural language control for ElephantRobotics MyCobot series robotic arms (especially optimized for ultraArmP340). This server enables controlling robotic arms through conversational AI, making robotics accessible to everyone.

## Features

- 🤖 Support for multiple MyCobot models (ultraArmP340, MyCobot280, MyCobot320)
- 🎮 Natural language control via MCP protocol
- 🔧 Simulation mode for development without physical hardware
- 🛡️ Safety features including emergency stop
- 📊 Real-time status monitoring

## Components

### Tools

The server provides the following control tools:

#### Connection Management
- **connect_robot** - Connect to a robotic arm
  - Input: `model` (string): Robot model
  - Input: `port` (string): Serial port
  - Returns: Connection status

#### Status Monitoring
- **get_robot_status** - Get current robot status
  - Returns: Current angles, coordinates, gripper/pump state, movement status

#### Movement Control
- **move_to_angles** - Move joints to specific angles
  - Input: `angles` (array): Target angles for each joint
  - Input: `speed` (int): Movement speed
  - Returns: Movement confirmation

- **move_to_coords** - Move to specific coordinates
  - Input: `coords` (array): Target coordinates
  - Input: `speed` (int): Movement speed
  - Returns: Movement confirmation

#### End Effector Control
- **control_gripper** - Control gripper open/close
- **control_pump** - Control suction pump on/off

#### System Commands
- **go_zero** - Return robot to zero position
- **emergency_stop** - Emergency stop all movements

#### Advanced Motion Control
- **execute_action_sequence** - Execute custom action sequences
  - Input: `sequence_name` (string): Descriptive name for the sequence
  - Input: `actions` (array): List of actions, each containing:
    - `type`: Action type ("angles", "coords", "gripper", "pump", "wait")
    - `angles/coords`: Target position (based on type)
    - `speed`: Movement speed (optional, default 50)
    - `duration`: Action duration in seconds (optional)
    - `gripper_action`: "open" or "close" (for gripper type)
    - `pump_action`: "on" or "off" (for pump type)
     - Input: `default_interval` (float): Default interval between actions (optional, default 0.5s)
  - Returns: Execution status with completed actions count
  - Note: This tool enables complex behaviors like cat playing, circle drawing, dancing, and custom gestures through action sequences


### Resources

- **status://current** - Real-time robot status information

### Prompts

- **robot_control_guide** - Interactive guidance for robot control
  - Arguments: `task` (task type)
  - Provides step-by-step instructions

- **design_action_sequence** - Template for designing custom action sequences
  - Arguments:
    - `task_description`: Task description (e.g., "dancing", "cat playing", "massage")
  - Provides structured guidance for action sequence design
  - Helps design smooth, continuous movements with proper timing

## QuickStart

### Installation

1. Ensure Python 3.10 is installed
2. Install dependencies:
```bash
pip install robotarm-mcp-p340
```

### Configuration for Cursor

There are three methods to configure MCP in Cursor:

#### Method 1: Python Module Configuration (Recommended for Installed Package)

If you've installed the package via pip:
```json
{
  "mcpServers": {
    "mycobot": {
      "command": "Fill in the python path under the virtual environment folder where robotarm-mcp-p340 is installed",
      "args": ["-u", "-m", "mycobot_mcp"],
      "env": {
        "SIMULATE": "1"
      }
    }
  }
}

Example:

{
  "mcpServers": {
    "mycobot": {
      "command": "D:\\anaconda3\\envs\\test-robotarm\\python.exe",
      "args": ["-u", "-m", "mycobot_mcp"],
      "env": {
        "SIMULATE": "1"
      }
    }
  }
}
```

#### Method 2: Development Configuration (For GitHub Clone)

If you've cloned from GitHub and are developing:

```json
{
  "mcpServers": {
    "mycobot": {
      "command": "Fill in the python path under the project's virtual environment folder",
      "args": [
        "-u",
        "-m",
        "mycobot_mcp"
      ],
      "env": {
        "SIMULATE": "1",
        "PYTHONPATH": "Fill in the absolute path to the src folder"
      },
      "cwd": "Fill in the absolute path to the project root"
    }
  }
}

Example:

{
  "mcpServers": {
    "mycobot": {
      "command": "D:\\Anaconda3\\envs\\mycobot-mcp\\python.exe",
      "args": [
        "-u",
        "-m",
        "mycobot_mcp"
      ],
      "env": {
        "SIMULATE": "1",
        "PYTHONPATH": "D:\\AI\\mycobot-mcp\\src"
      },
      "cwd": "D:\\AI\\mycobot-mcp"
    }
  }
}
```

**Important Notes:**
- "SIMULATE": "1" is for simulation testing without hardware. For real device testing, set SIMULATE to "0"
- Method 2 requires installing the project dependencies from requirements.txt in the project's virtual environment
- Must use `-u` flag to disable Python output buffering
- Set `PYTHONPATH` to include the src directory
- Adjust paths according to your installation

#### Method 3: Batch File Configuration (Windows)

1. Create a batch file `start_mcp_server.bat`:
```batch
@echo off
cd /d D:\AI\mycobot-mcp
set PYTHONPATH=D:\AI\mycobot-mcp\src
set SIMULATE=1
D:\Anaconda3\envs\mycobot-mcp\python.exe -u -m mycobot_mcp
```

2. Configure Cursor:
```json
{
  "mcpServers": {
    "mycobot": {
      "command": "D:\\AI\\mycobot-mcp\\start_mcp_server.bat"
    }
  }
}
```

#### Configuration Steps

1. Open Cursor Settings (Ctrl+,)
2. Search for "MCP" or "Model Context Protocol"
3. Add the configuration using one of the methods above
4. Restart Cursor to apply changes

#### Verification

After successful configuration, you should see:
- ✅ "9 tools enabled" in the MCP status
- ✅ Tools available in chat: `connect_robot`, `get_robot_status`, etc.

### Usage Examples

1. **Connect to robot:**
   - "Connect to my ultraArm P340 robot"
   - "Initialize robot on COM3 port" (adjust the number based on your device's actual COM port, default is 3)

2. **Basic movements:**
   - "Move the robot arm to position [200, 0, 150]"
   - "Set joint angles to [45, 30, -20]"
   - "Return to home position"

3. **Gripper control:**
   - "Open the gripper"
   - "Close gripper to pick up object"
   - "Turn on suction pump"

4. **Complex tasks:**
   - "Play with my cat using the robot arm"
   - "Draw a circle on the table"
   - "Show me how to write Chinese characters"
   - "Make the robot dance to music"
   - "Create a custom waving gesture sequence"

### Development Mode

Set `SIMULATE=1` to test without hardware:
```bash
export SIMULATE=1  # Linux/Mac
set SIMULATE=1     # Windows
```

### Troubleshooting

If tools don't load properly:

1. **Check MCP logs in Cursor:**
   - View → Output → Select "MCP" channel
   - Look for error messages

2. **Test the server locally:**
   ```bash
   # For installed package
   python -m mycobot_mcp
   
   # For development (from project root)
   cd D:\AI\mycobot-mcp
   set PYTHONPATH=src
   python -m mycobot_mcp
   ```

3. **Common issues and solutions:**
   - **"No module named 'mycobot_mcp'"**: 
     - For development: Ensure `PYTHONPATH` includes the `src` folder
     - For installed: Run `pip install -e .` from project root
   
   - **"Tools not loading"**:
     - Check that you're using `-m mycobot_mcp` not `-m mycobot_mcp.server`
     - Verify the `cwd` is set to project root in development mode
   
   - **Configuration tips:**
     - ✅ Always use `-u` flag for unbuffered output
     - ✅ Set `PYTHONPATH` to `src` folder (not `src/mycobot_mcp`)
     - ✅ Use `cwd` to set working directory for development
     - ❌ Don't run `server.py` directly

## Safety Guidelines

⚠️ **Important Safety Information:**

1. Always ensure a clear workspace around the robot
2. Keep hands and objects away from moving parts
3. Use emergency stop if unexpected behavior occurs
4. Start with slow speeds when testing new movements
5. Never use massage demonstrations on humans
6. Supervise pet interactions at all times

## License

This MCP server is licensed under the MIT License. See LICENSE file for details.

---

<a name="chinese"></a>
## 概述

RobotArm MCP P340 是一个基于模型上下文协议（MCP）的服务器实现，为大象机器人 MyCobot 系列机械臂提供自然语言控制功能（特别针对 ultraArmP340 进行了优化）。通过对话式 AI 控制机械臂，让机器人技术人人可用。

## 功能特点

- 🤖 支持多种 MyCobot 型号（ultraArmP340、MyCobot280、MyCobot320）
- 🎮 通过 MCP 协议实现自然语言控制机械臂
- 🔧 模拟模式支持无硬件开发
- 🛡️ 包含紧急停止等安全功能
- 📊 实时状态监控

## 组件说明

### 工具（Tools）

服务器提供以下控制工具：

#### 连接管理
- **connect_robot** - 连接机械臂
  - 输入：`model`（字符串）：机器人型号
  - 输入：`port`（字符串）：串口号
  - 返回：连接状态

#### 状态监控
- **get_robot_status** - 获取机器人当前状态
  - 返回：当前角度、坐标、夹爪/吸泵状态、运动状态

#### 运动控制
- **move_to_angles** - 移动关节到指定角度
  - 输入：`angles`（数组）：各关节目标角度
  - 输入：`speed`（整数）：运动速度
  - 返回：运动确认

- **move_to_coords** - 移动到指定坐标
  - 输入：`coords`（数组）：目标坐标
  - 输入：`speed`（整数）：运动速度
  - 返回：运动确认

#### 末端执行器控制
- **control_gripper** - 控制夹爪开合
- **control_pump** - 控制吸泵开关

#### 系统命令
- **go_zero** - 回零位
- **emergency_stop** - 紧急停止

#### 高级运动控制
- **execute_action_sequence** - 执行自定义动作序列
  - 输入：`sequence_name`（字符串）：动作序列的描述性名称
  - 输入：`actions`（数组）：动作列表，每个动作包含：
    - `type`：动作类型（"angles"、"coords"、"gripper"、"pump"、"wait"）
    - `angles/coords`：目标位置（根据类型）
    - `speed`：移动速度（可选，默认50）
    - `duration`：动作持续时间（秒，可选）
    - `gripper_action`："open"或"close"（夹爪类型）
    - `pump_action`："on"或"off"（吸泵类型）
  - 输入：`default_interval`（浮点数）：动作间默认间隔（可选，默认0.5秒）
  - 返回：执行状态及完成的动作数
  - 注意：此工具可实现逗猫、画圆、跳舞等复杂行为，通过动作序列组合实现各种创意动作


### 资源（Resources）

- **status://current** - 实时机器人状态信息

### 提示（Prompts）

- **robot_control_guide** - 机器人控制交互指南
  - 参数：`task`（任务类型）
  - 提供分步骤操作指导

- **design_action_sequence** - 设计自定义动作序列的模板
  - 参数：
    - `task_description`：任务描述（如"跳舞"、"逗猫"、"按摩"等）
  - 提供结构化的动作序列设计指导
  - 帮助设计流畅连续的动作及合理的时间安排

## 快速开始

### 安装配置

1. 确保已安装 Python 3.10
2. 安装依赖：
```bash
pip install robotarm-mcp-p340
```

### Cursor 配置方法

有三种方法在 Cursor 中配置 MCP：

#### 方法 1：Python 模块配置（推荐用于已安装的包）

如果您已通过 pip 安装了包：
```json
{
  "mcpServers": {
    "mycobot": {
      "command": "填写安装了robotarm-mcp-p340的虚拟环境文件夹下的python路径",
      "args": ["-u", "-m", "mycobot_mcp"],
      "env": {
        "SIMULATE": "1"
      }
    }
  }
}

示例如下：

{
  "mcpServers": {
    "mycobot": {
      "command": "D:\\anaconda3\\envs\\test-robotarm\\python.exe",
      "args": ["-u", "-m", "mycobot_mcp"],
      "env": {
        "SIMULATE": "1"
      }
    }
  }
}
```

#### 方法 2：开发配置（用于从 GitHub 克隆的项目）

如果您从 GitHub 克隆并正在开发：

```json
{
  "mcpServers": {
    "mycobot": {
      "command": "填写安装了该项目虚拟环境文件夹下的python路径",
      "args": [
        "-u",
        "-m",
        "mycobot_mcp"
      ],
      "env": {
        "SIMULATE": "1",
        "PYTHONPATH": "填写 src 文件夹的绝对路径"
      },
      "cwd": "填写项目根目录的绝对路径"
    }
  }
}

示例如下：

{
  "mcpServers": {
    "mycobot": {
      "command": "D:\\Anaconda3\\envs\\mycobot-mcp\\python.exe",
      "args": [
        "-u",
        "-m",
        "mycobot_mcp"
      ],
      "env": {
        "SIMULATE": "1",
        "PYTHONPATH": "D:\\AI\\mycobot-mcp\\src"
      },
      "cwd": "D:\\AI\\mycobot-mcp"
    }
  }
}
```

**重要说明：**
- "SIMULATE": "1"为无硬件设备的模拟测试，实机测试需要把SIMULATE值设置为"0"
- 方法二需要在项目虚拟环境中安装requirements.txt中的项目依赖
- 必须使用 `-u` 参数禁用 Python 输出缓冲
- 设置 `PYTHONPATH` 包含 src 目录
- 根据您的安装路径调整路径


#### 方法 3：批处理文件配置（Windows）

1. 创建批处理文件 `start_mcp_server.bat`：
```batch
@echo off
cd /d D:\AI\mycobot-mcp
set PYTHONPATH=D:\AI\mycobot-mcp\src
set SIMULATE=1
D:\Anaconda3\envs\mycobot-mcp\python.exe -u -m mycobot_mcp
```

2. 配置 Cursor：
```json
{
  "mcpServers": {
    "mycobot": {
      "command": "D:\\AI\\mycobot-mcp\\start_mcp_server.bat"
    }
  }
}
```


#### 配置步骤

1. 打开 Cursor 设置（Ctrl+,）
2. 搜索 "MCP" 或 "Model Context Protocol"
3. 使用上述方法之一添加配置
4. 重启 Cursor 使配置生效

#### 验证配置

配置成功后，您应该看到：
- ✅ MCP 状态显示 "9 tools enabled"
- ✅ 聊天中可用工具：`connect_robot`、`get_robot_status` 等

### 使用示例

1. **连接机器人：**
   - "连接我的 ultraArm P340 机械臂"
   - "初始化 COM3 端口的机器人"（根据您设备的实际 COM 端口调整数字，默认是 3）

2. **基础运动：**
   - "移动机械臂到位置 [200, 0, 150]"
   - "设置关节角度为 [45, 30, -20]"
   - "回到零位"

3. **夹爪控制：**
   - "打开夹爪"
   - "闭合夹爪抓取物体"
   - "开启吸泵"

4. **复杂任务：**
   - "用机械臂逗猫"
   - "在桌上画个圆"
   - "演示如何写汉字"
   - "让机器人跟着音乐跳舞"
   - "创建一个自定义的挥手动作序列"

### 开发模式

设置 `SIMULATE=1` 无需硬件测试：
```bash
export SIMULATE=1  # Linux/Mac
set SIMULATE=1     # Windows
```

### 故障排除

如果工具加载失败：

1. **检查 Cursor 的 MCP 日志：**
   - 视图 → 输出 → 选择 "MCP" 通道
   - 查看错误信息

2. **本地测试服务器：**
   ```bash
   # 对于已安装的包
   python -m mycobot_mcp
   
   # 对于开发模式（从项目根目录）
   cd D:\AI\mycobot-mcp
   set PYTHONPATH=src
   python -m mycobot_mcp
   ```

3. **常见问题和解决方案：**
   - **"No module named 'mycobot_mcp'"**：
     - 开发模式：确保 `PYTHONPATH` 包含 `src` 文件夹
     - 已安装：从项目根目录运行 `pip install -e .`
   
   - **"工具未加载"**：
     - 检查是否使用 `-m mycobot_mcp` 而不是 `-m mycobot_mcp.server`
     - 验证开发模式下 `cwd` 设置为项目根目录
   
   - **配置提示：**
     - ✅ 始终使用 `-u` 标志实现无缓冲输出
     - ✅ 设置 `PYTHONPATH` 为 `src` 文件夹（而不是 `src/mycobot_mcp`）
     - ✅ 使用 `cwd` 为开发设置工作目录
     - ❌ 不要再直接运行 `server.py`

## 安全指南

⚠️ **重要安全信息：**

1. 确保机器人周围有足够空间
2. 运动时远离机械部件
3. 出现异常立即使用紧急停止
4. 测试新动作时使用低速
5. 按摩演示仅用于展示，勿用于真人
6. 与宠物互动时全程监督

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。 