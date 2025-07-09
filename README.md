# MyCobot MCP Server

[English](#english) | [中文](#chinese)

<a name="english"></a>
## Overview

A Model Context Protocol (MCP) server implementation that provides natural language control for ElephantRobotics MyCobot series robotic arms. This server enables controlling robotic arms through conversational AI, making robotics accessible to everyone.

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

## QuickStart/Usage with MCP Client

### Installation

1. Ensure Python 3.10 is installed
2. Install dependencies:
```bash
pip install mycobot-mcp
```

### Configuration for Cursor

There are two methods to configure MCP in Cursor:

#### Method 1: Direct Python Configuration

Add to your Cursor MCP settings:

```json

{
  "mcpServers": {
    "mycobot": {
      "command": "Fill in the absolute path to the Python interpreter in your conda environment",
      "args": [
        "-u",
        "Fill in the absolute path to the main MCP project file server.py"
      ],
      "env": {
        "SIMULATE": "1",
        "PYTHONPATH": "Fill in the absolute path to the parent folder of the server.py folder"
      }
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
        "D:\\AI\\mycobot-mcp\\src\\mycobot_mcp\\server.py"
      ],
      "env": {
        "SIMULATE": "1",
        "PYTHONPATH": "D:\\AI\\mycobot-mcp\\src"
      }
    }
  }
}
```

**Important Notes:**
- "SIMULATE": "1" is for simulation testing without hardware. For real device testing, set SIMULATE to "0"
- Must use `-u` flag to disable Python output buffering
- Set `PYTHONPATH` to include the src directory
- Adjust paths according to your installation

#### Method 2: Batch File Configuration (Windows)

1. Create a batch file `start_mcp_server.bat`:
```batch
@echo off
cd /d D:\AI\mycobot-mcp
set PYTHONPATH=D:\AI\mycobot-mcp\src
set SIMULATE=1
D:\Anaconda3\envs\mycobot-mcp\python.exe -u src\mycobot_mcp\server.py
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

2. **Test server communication:**
   ```python
   python test_mcp_stdio.py
   ```

3. **Common issues:**
   - ❌ Don't run server directly: `python server.py`
   - ✅ Let MCP client manage the server lifecycle
   - ✅ Ensure Python path includes `-u` flag
   - ✅ Set PYTHONPATH environment variable

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

MyCobot MCP Server 是一个基于模型上下文协议（MCP）的服务器实现，为大象机器人 MyCobot 系列机械臂提供自然语言控制功能。通过对话式 AI 控制机械臂，让机器人技术人人可用。

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
pip install mycobot-mcp
```

### Cursor 配置方法

有两种方法在 Cursor 中配置 MCP：

#### 方法 1：直接 Python 配置

在 Cursor MCP 设置中添加：

```json

{
  "mcpServers": {
    "mycobot": {
      "command": "填写你运行项目的conda环境下的python解释器目录的绝对路径",
      "args": [
        "-u",
        "填写开发的mcp项目主文件server.py的绝对路径"
      ],
      "env": {
        "SIMULATE": "1",
        "PYTHONPATH": "填写server.py所在文件夹的上一级文件夹绝对路径"
      }
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
        "D:\\AI\\mycobot-mcp\\src\\mycobot_mcp\\server.py"
      ],
      "env": {
        "SIMULATE": "1",
        "PYTHONPATH": "D:\\AI\\mycobot-mcp\\src"
      }
    }
  }
}
```

**重要说明：**
- "SIMULATE": "1"为无硬件设备的模拟测试，实机测试需要把SIMULATE值设置为"0"
- 必须使用 `-u` 参数禁用 Python 输出缓冲
- 设置 `PYTHONPATH` 包含 src 目录
- 根据您的安装路径调整路径

#### 方法 2：批处理文件配置（Windows）

1. 创建批处理文件 `start_mcp_server.bat`：
```batch
@echo off
cd /d D:\AI\mycobot-mcp
set PYTHONPATH=D:\AI\mycobot-mcp\src
set SIMULATE=1
D:\Anaconda3\envs\mycobot-mcp\python.exe -u src\mycobot_mcp\server.py
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
   - "初始化 COM3 端口的机器人" (需要根据自己设备连接的COM端口是多少去更改数字，这里预设是3)

2. **基础运动：**
   - "移动机械臂到坐标 [200, 0, 150]"
   - "设置关节角度为 [45, 30, -20]"
   - "回到原点"

3. **夹爪控制：**
   - "打开夹爪"
   - "闭合夹爪抓取物体"
   - "开启吸泵"

4. **复杂任务：**
   - "用机械臂逗猫"
   - "在桌上画个圆"
   - "演示如何写汉字"
   - "让机器人跳舞"
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

2. **测试服务器通信：**
   ```python
   python test_mcp_stdio.py
   ```

3. **常见问题：**
   - ❌ 不要直接运行服务器：`python server.py`
   - ✅ 让 MCP 客户端管理服务器生命周期
   - ✅ 确保 Python 命令包含 `-u` 参数
   - ✅ 设置 PYTHONPATH 环境变量

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