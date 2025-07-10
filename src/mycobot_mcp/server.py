"""
MyCobot MCP Server - Control ElephantRobotics robotic arms via natural language
"""
import os
import json
import time
import random
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 模拟开关：家中调试设为 1，真机部署设为 0
SIMULATE = os.getenv("SIMULATE", "1") != "0"

# 初始化 MCP 服务
mcp = FastMCP("MyCobot Control Service")

# 全局变量存储机械臂状态
robot_state = {
    "connected": False,
    "model": "ultraArmP340",  # 默认型号
    "port": "COM3",  # Windows 默认端口
    "current_angles": [0.0, 0.0, 0.0],
    "current_coords": [0.0, 0.0, 0.0],
    "gripper_state": 0,  # 0: 张开, 1: 闭合
    "pump_state": 0,  # 0: 关闭, 1: 开启
    "is_moving": False
}

# 机械臂实例（真机模式下使用）
mycobot = None

# 模拟器类
class MyCobotSimulator:
    """模拟机械臂行为的类"""
    
    def __init__(self):
        self.angles = [0.0, 0.0, 0.0]
        self.coords = [0.0, 0.0, 0.0]
        self.gripper_state = 0
        self.pump_state = 0
        self.is_moving = False
        
    def go_zero(self):
        logger.info("[模拟] 机械臂回零")
        self.angles = [0.0, 0.0, 0.0]
        self.coords = [0.0, 0.0, 0.0]
        time.sleep(0.5)  # 模拟运动时间
        
    def get_angles_info(self):
        return self.angles
        
    def set_angles(self, angles, speed):
        logger.info(f"[模拟] 设置角度: {angles}, 速度: {speed}")
        self.is_moving = True
        time.sleep(0.5)  # 模拟运动时间
        self.angles = angles
        self.is_moving = False
        
    def get_coords_info(self):
        return self.coords
        
    def set_coords(self, coords, speed):
        logger.info(f"[模拟] 设置坐标: {coords}, 速度: {speed}")
        self.is_moving = True
        time.sleep(0.5)  # 模拟运动时间
        self.coords = coords
        self.is_moving = False
        
    def set_gpio_state(self, state):
        logger.info(f"[模拟] 设置吸泵状态: {state}")
        self.pump_state = state
        
    def set_gripper_state(self, state, speed=50):
        logger.info(f"[模拟] 设置夹爪状态: {state}, 速度: {speed}")
        self.gripper_state = state
        
    def is_moving_end(self):
        return 0 if self.is_moving else 1
        
    def power_on(self):
        logger.info("[模拟] 机械臂上电")
        
    def release_all_servos(self):
        logger.info("[模拟] 机械臂掉电")

# 初始化函数
def initialize_robot(model: str = "ultraArmP340", port: str = "COM3") -> bool:
    """初始化机械臂连接"""
    global mycobot, robot_state
    
    try:
        if SIMULATE:
            logger.info(f"[模拟模式] 初始化 {model} 机械臂")
            mycobot = MyCobotSimulator()
        else:
            # 真机模式
            if model == "ultraArmP340":
                from pymycobot.ultraArmP340 import ultraArmP340
                mycobot = ultraArmP340(port, 115200)
            elif model == "MyCobot280":
                from pymycobot import MyCobot280
                mycobot = MyCobot280(port, 115200)
            elif model == "MyCobot320":
                from pymycobot import MyCobot320
                mycobot = MyCobot320(port, 115200)
            else:
                raise ValueError(f"不支持的机械臂型号: {model}")
                
        # 更新状态
        robot_state["connected"] = True
        robot_state["model"] = model
        robot_state["port"] = port
        
        # 初始化机械臂
        mycobot.go_zero()
        time.sleep(0.5)
        
        return True
        
    except Exception as e:
        logger.error(f"初始化机械臂失败: {str(e)}")
        robot_state["connected"] = False
        return False

# MCP Tools 定义

@mcp.tool()
def connect_robot(model: str = "ultraArmP340", port: str = "COM3") -> Dict[str, Any]:
    """连接机械臂
    
    Args:
        model: 机械臂型号 (ultraArmP340, MyCobot280, MyCobot320)
        port: 串口号 (Windows: COM3, Linux: /dev/ttyUSB0)
    """
    success = initialize_robot(model, port)
    return {
        "success": success,
        "message": "机械臂连接成功" if success else "机械臂连接失败",
        "simulate_mode": SIMULATE
    }

@mcp.tool()
def get_robot_status() -> Dict[str, Any]:
    """获取机械臂当前状态"""
    if not robot_state["connected"]:
        return {"error": "机械臂未连接"}
        
    angles = mycobot.get_angles_info()
    coords = mycobot.get_coords_info()
    is_moving = mycobot.is_moving_end() == 0
    
    return {
        "connected": robot_state["connected"],
        "model": robot_state["model"],
        "angles": angles,
        "coords": coords,
        "is_moving": is_moving,
        "gripper_state": robot_state["gripper_state"],
        "pump_state": robot_state["pump_state"],
        "simulate_mode": SIMULATE
    }

@mcp.tool()
def move_to_angles(angles: List[float], speed: int = 50) -> Dict[str, Any]:
    """移动机械臂到指定角度
    
    Args:
        angles: 各关节角度列表 [joint1, joint2, joint3]
        speed: 移动速度 (0-200 mm/s)
    """
    if not robot_state["connected"]:
        return {"error": "机械臂未连接"}
        
    try:
        mycobot.set_angles(angles, speed)
        robot_state["current_angles"] = angles
        return {
            "success": True,
            "message": f"正在移动到角度: {angles}",
            "angles": angles
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def move_to_coords(coords: List[float], speed: int = 50) -> Dict[str, Any]:
    """移动机械臂到指定坐标
    
    Args:
        coords: 坐标列表 [x, y, z]
        speed: 移动速度 (0-200 mm/s)
    """
    if not robot_state["connected"]:
        return {"error": "机械臂未连接"}
        
    try:
        mycobot.set_coords(coords, speed)
        robot_state["current_coords"] = coords
        return {
            "success": True,
            "message": f"正在移动到坐标: {coords}",
            "coords": coords
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def control_gripper(action: str) -> Dict[str, Any]:
    """控制夹爪
    
    Args:
        action: "open" 或 "close"
    """
    if not robot_state["connected"]:
        return {"error": "机械臂未连接"}
        
    try:
        state = 0 if action == "open" else 1
        speed = 50  # 默认夹爪速度
        mycobot.set_gripper_state(state, speed)
        robot_state["gripper_state"] = state
        return {
            "success": True,
            "message": f"夹爪已{('张开' if action == 'open' else '闭合')}",
            "gripper_state": state
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def control_pump(action: str) -> Dict[str, Any]:
    """控制吸泵
    
    Args:
        action: "on" 或 "off"
    """
    if not robot_state["connected"]:
        return {"error": "机械臂未连接"}
        
    try:
        state = 1 if action == "on" else 0
        mycobot.set_gpio_state(state)
        robot_state["pump_state"] = state
        return {
            "success": True,
            "message": f"吸泵已{('开启' if action == 'on' else '关闭')}",
            "pump_state": state
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def go_zero() -> Dict[str, Any]:
    """让机械臂回到零位"""
    if not robot_state["connected"]:
        return {"error": "机械臂未连接"}
        
    try:
        mycobot.go_zero()
        return {
            "success": True,
            "message": "机械臂正在回零"
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def emergency_stop() -> Dict[str, Any]:
    """紧急停止机械臂运动"""
    if not robot_state["connected"]:
        return {"error": "机械臂未连接"}
        
    try:
        mycobot.release_all_servos()
        return {
            "success": True,
            "message": "机械臂已紧急停止"
        }
    except Exception as e:
        return {"error": str(e)}



# 新增：通用动作序列执行工具
@mcp.tool()
def execute_action_sequence(
    sequence_name: str,
    actions: List[Dict[str, Any]],
    default_interval: float = 0.5
) -> Dict[str, Any]:
    """执行一个完整的动作序列，支持连续流畅的动作组合
    
    Args:
        sequence_name: 动作序列名称（如"舞蹈"、"逗猫"、"按摩"等）
        actions: 动作序列列表，每个动作包含：
            - type: 动作类型 ("angles", "coords", "gripper", "pump", "wait")
            - angles/coords: 目标位置（根据type）
            - speed: 移动速度（可选，默认50）
            - duration: 该动作持续时间（可选，默认使用default_interval）
            - gripper_action: 夹爪动作 ("open" 或 "close")
            - pump_action: 吸泵动作 ("on" 或 "off")
        default_interval: 默认动作间隔时间（秒）
    
    Example:
        actions = [
            {"type": "angles", "angles": [45, 60, 30], "speed": 80, "duration": 1.0},
            {"type": "gripper", "gripper_action": "open"},
            {"type": "coords", "coords": [200, 0, 100], "speed": 60},
            {"type": "wait", "duration": 0.5},
            {"type": "angles", "angles": [-45, 60, 30], "speed": 100}
        ]
    """
    if not robot_state["connected"]:
        return {"error": "机械臂未连接"}
        
    try:
        logger.info(f"开始执行动作序列: {sequence_name}")
        total_actions = len(actions)
        completed_actions = 0
        
        for i, action in enumerate(actions):
            action_type = action.get("type")
            duration = action.get("duration", default_interval)
            
            # 根据动作类型执行相应操作
            if action_type == "angles":
                angles = action.get("angles", [0, 0, 0])
                speed = action.get("speed", 50)
                mycobot.set_angles(angles, speed)
                robot_state["current_angles"] = angles
                logger.info(f"[{i+1}/{total_actions}] 移动到角度: {angles}, 速度: {speed}")
                
            elif action_type == "coords":
                coords = action.get("coords", [0, 0, 0])
                speed = action.get("speed", 50)
                mycobot.set_coords(coords, speed)
                robot_state["current_coords"] = coords
                logger.info(f"[{i+1}/{total_actions}] 移动到坐标: {coords}, 速度: {speed}")
                
            elif action_type == "gripper":
                gripper_action = action.get("gripper_action", "open")
                state = 0 if gripper_action == "open" else 1
                speed = action.get("speed", 50)  # 夹爪速度
                mycobot.set_gripper_state(state, speed)
                robot_state["gripper_state"] = state
                logger.info(f"[{i+1}/{total_actions}] 夹爪: {gripper_action}")
                
            elif action_type == "pump":
                pump_action = action.get("pump_action", "off")
                state = 1 if pump_action == "on" else 0
                mycobot.set_gpio_state(state)
                robot_state["pump_state"] = state
                logger.info(f"[{i+1}/{total_actions}] 吸泵: {pump_action}")
                
            elif action_type == "wait":
                logger.info(f"[{i+1}/{total_actions}] 等待: {duration}秒")
                
            else:
                logger.warning(f"未知的动作类型: {action_type}")
                continue
            
            # 等待动作完成
            time.sleep(duration)
            completed_actions += 1
            
        return {
            "success": True,
            "message": f"动作序列 '{sequence_name}' 执行完成",
            "total_actions": total_actions,
            "completed_actions": completed_actions,
            "final_state": {
                "angles": robot_state["current_angles"],
                "coords": robot_state["current_coords"],
                "gripper": robot_state["gripper_state"],
                "pump": robot_state["pump_state"]
            }
        }
        
    except Exception as e:
        logger.error(f"执行动作序列失败: {str(e)}")
        return {
            "error": str(e),
            "completed_actions": completed_actions,
            "total_actions": total_actions
        }

# Resources 定义
@mcp.resource("status://current")
def get_current_status() -> str:
    """获取机械臂当前状态资源"""
    if not robot_state["connected"]:
        return json.dumps({"error": "机械臂未连接"})
        
    status = {
        "model": robot_state["model"],
        "angles": mycobot.get_angles_info(),
        "coords": mycobot.get_coords_info(),
        "gripper": robot_state["gripper_state"],
        "pump": robot_state["pump_state"],
        "is_moving": mycobot.is_moving_end() == 0,
        "simulate_mode": SIMULATE
    }
    return json.dumps(status, indent=2)

# Prompts 定义
@mcp.prompt()
def robot_control_guide(task: str = "general") -> str:
    """机械臂控制指南
    
    Args:
        task: 任务类型 (general, cat_play, writing, massage)
    """
    guides = {
        "general": """
我是您的机械臂控制助手。以下是基本操作指南：

1. 首先连接机械臂：使用 connect_robot 工具
   - 支持型号：ultraArmP340, MyCobot280, MyCobot320
   - 默认端口：Windows(COM3), Linux(/dev/ttyUSB0)

2. 控制机械臂移动：
   - move_to_angles: 按角度控制 [joint1, joint2, joint3]
   - move_to_coords: 按坐标控制 [x, y, z]
   - 速度范围：0-200 mm/s

3. 控制末端执行器：
   - control_gripper: 控制夹爪 (open/close)
   - control_pump: 控制吸泵 (on/off)

4. 系统操作：
   - go_zero: 回零位
   - emergency_stop: 紧急停止
   - get_robot_status: 查看状态

5. 高级功能：
   - execute_action_sequence: 执行复杂动作序列
   - 支持连续流畅的动作组合
   - 可创建舞蹈、逗猫、画画等创意动作

请告诉我您想让机械臂做什么？
""",
        "cat_play": """
逗猫模式已准备就绪！🐱

我将控制机械臂执行一系列模拟逗猫棒的动作：
- 左右摆动吸引猫咪注意
- 上下移动模拟猎物
- 快慢结合的节奏变化
- 突然停顿诱发扑击欲望

您可以：
1. 直接说"开始逗猫"
2. 自定义动作序列
3. 调整速度和幅度

建议动作模式：
- 慢速引诱（40-60速度）
- 快速逃避（150-200速度）
- 策略性停顿
- 变化多端的角度

注意：请确保猫咪在安全距离外！

请告诉我您想写什么？
""",
        "massage": """
按摩模式说明：

⚠️ 安全提示：此模式仅供演示，请勿用于真人按摩！

演示动作包括：
1. 圆周运动 - 模拟揉按
   - 半径：30-50mm
   - 速度：40-60 mm/s
   
2. 直线推动 - 模拟推拿
   - 行程：100-150mm
   - 速度：30-50 mm/s
   
3. 点按动作 - 模拟指压
   - 深度：10-20mm
   - 频率：1-2次/秒

4. 组合动作：
   - 螺旋按摩
   - 波浪推拿
   - 节奏性敲击

可在软垫或模型上演示。
"""
    }
    
    return guides.get(task, guides["general"])

@mcp.prompt()
def design_action_sequence(task_description: str) -> str:
    """设计动作序列的提示模板
    
    Args:
        task_description: 用户描述的任务（如"跳舞"、"逗猫"、"按摩"等）
    """
    return f"""
您需要为以下任务设计一个完整的机械臂动作序列：{task_description}

请按照以下要求设计：

1. **一次性设计完整序列**：
   - 在开始执行前，完整规划所有动作步骤
   - 考虑动作的连贯性和流畅性
   - 合理安排每个动作的速度和持续时间

2. **动作序列格式**：
   使用 execute_action_sequence 工具，提供以下参数：
   - sequence_name: 动作序列的描述性名称
   - actions: 动作列表，每个动作包含：
     * type: "angles"（角度控制）、"coords"（坐标控制）、"gripper"（夹爪）、"pump"（吸泵）或"wait"（等待）
     * 相应的参数（angles/coords/gripper_action/pump_action）
     * speed: 移动速度（0-200）
     * duration: 动作持续时间（秒）

3. **设计原则**：
   - 动作幅度要合理，避免极限位置
   - 速度变化要自然，快慢结合
   - 考虑机械臂的物理限制
   - 不需要开始和结束时归零

4. **创意建议**：
   - 可以结合角度和坐标控制
   - 利用夹爪和吸泵增加表现力
   - 通过速度变化营造节奏感
   - 适当的停顿可以增强效果

示例动作序列结构：
```
actions = [
    {{"type": "angles", "angles": [45, 60, 30], "speed": 80, "duration": 1.0}},
    {{"type": "gripper", "gripper_action": "open", "duration": 0.3}},
    {{"type": "coords", "coords": [200, 0, 100], "speed": 60, "duration": 1.5}},
    {{"type": "wait", "duration": 0.5}},
    {{"type": "angles", "angles": [-45, 60, 30], "speed": 100, "duration": 1.0}}
]
```

请根据任务 "{task_description}" 设计创意动作序列！
"""

# 自动初始化（模拟模式）
if SIMULATE:
    logger.info(f"启动 MyCobot MCP 服务器 (模拟模式: {SIMULATE})")
    initialize_robot()
