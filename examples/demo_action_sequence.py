"""
动作序列演示 - 展示如何使用execute_action_sequence工具
"""

# 舞蹈动作序列示例
dance_sequence = {
    "sequence_name": "机械臂优雅舞蹈",
    "actions": [
        # 开场造型
        {"type": "angles", "angles": [-60, 45, 30], "speed": 90, "duration": 1.0},
        
        # 左右摇摆
        {"type": "angles", "angles": [60, 45, 30], "speed": 80, "duration": 1.2},
        {"type": "angles", "angles": [-60, 45, 30], "speed": 80, "duration": 1.2},
        
        # 上下律动
        {"type": "angles", "angles": [0, 80, 60], "speed": 70, "duration": 1.0},
        {"type": "angles", "angles": [0, 20, -30], "speed": 70, "duration": 1.0},
        
        # 夹爪配合
        {"type": "gripper", "gripper_action": "open", "speed": 80, "duration": 0.5},
        {"type": "angles", "angles": [45, 60, 45], "speed": 100, "duration": 0.8},
        {"type": "gripper", "gripper_action": "close", "speed": 80, "duration": 0.5},
        
        # 旋转动作
        {"type": "angles", "angles": [90, 40, 40], "speed": 90, "duration": 1.0},
        {"type": "angles", "angles": [180, 40, 40], "speed": 90, "duration": 1.0},
        {"type": "angles", "angles": [270, 40, 40], "speed": 90, "duration": 1.0},
        {"type": "angles", "angles": [360, 40, 40], "speed": 90, "duration": 1.0},
        
        # 结束造型
        {"type": "angles", "angles": [0, 60, 90], "speed": 60, "duration": 1.5}
    ],
    "default_interval": 0.5
}

# 逗猫动作序列示例
cat_play_sequence = {
    "sequence_name": "智能逗猫动作",
    "actions": [
        # 准备姿势
        {"type": "angles", "angles": [0, 45, 60], "speed": 80, "duration": 0.8},
        
        # 快速左右摆动（吸引注意）
        {"type": "angles", "angles": [-30, 45, 60], "speed": 150, "duration": 0.3},
        {"type": "angles", "angles": [30, 45, 60], "speed": 150, "duration": 0.3},
        {"type": "angles", "angles": [-30, 45, 60], "speed": 150, "duration": 0.3},
        {"type": "angles", "angles": [30, 45, 60], "speed": 150, "duration": 0.3},
        
        # 慢速诱导
        {"type": "angles", "angles": [45, 30, 45], "speed": 40, "duration": 2.0},
        {"type": "wait", "duration": 0.5},
        
        # 突然快速移动
        {"type": "angles", "angles": [-60, 60, 30], "speed": 180, "duration": 0.5},
        
        # 上下跳动
        {"type": "angles", "angles": [-60, 80, 60], "speed": 120, "duration": 0.5},
        {"type": "angles", "angles": [-60, 40, 20], "speed": 120, "duration": 0.5},
        {"type": "angles", "angles": [-60, 80, 60], "speed": 120, "duration": 0.5},
        
        # 缓慢潜行
        {"type": "angles", "angles": [0, 30, 30], "speed": 30, "duration": 2.5},
        
        # 最终扑击
        {"type": "angles", "angles": [0, 70, 80], "speed": 200, "duration": 0.4}
    ],
    "default_interval": 0.3
}

# 按摩动作序列示例（仅供演示）
massage_sequence = {
    "sequence_name": "按摩演示动作",
    "actions": [
        # 初始位置
        {"type": "coords", "coords": [200, 0, 100], "speed": 60, "duration": 1.0},
        
        # 圆周揉按动作
        {"type": "coords", "coords": [200, 30, 100], "speed": 40, "duration": 1.0},
        {"type": "coords", "coords": [170, 30, 100], "speed": 40, "duration": 1.0},
        {"type": "coords", "coords": [170, -30, 100], "speed": 40, "duration": 1.0},
        {"type": "coords", "coords": [200, -30, 100], "speed": 40, "duration": 1.0},
        {"type": "coords", "coords": [200, 0, 100], "speed": 40, "duration": 1.0},
        
        # 点按动作
        {"type": "coords", "coords": [200, 0, 80], "speed": 30, "duration": 0.5},
        {"type": "coords", "coords": [200, 0, 100], "speed": 30, "duration": 0.5},
        {"type": "coords", "coords": [200, 0, 80], "speed": 30, "duration": 0.5},
        {"type": "coords", "coords": [200, 0, 100], "speed": 30, "duration": 0.5},
        
        # 直线推拿
        {"type": "coords", "coords": [250, 0, 90], "speed": 25, "duration": 2.0},
        {"type": "coords", "coords": [150, 0, 90], "speed": 25, "duration": 2.0},
        {"type": "coords", "coords": [200, 0, 90], "speed": 25, "duration": 1.0}
    ],
    "default_interval": 0.5
}

# 使用方法：
# 1. 在AI对话中说："给我跳个舞"
# 2. AI会自动调用execute_action_sequence工具，使用类似dance_sequence的动作序列
# 3. 机械臂会连续流畅地执行所有动作，没有停顿

# 动作类型说明：
# - "angles": 控制各关节角度
# - "coords": 控制笛卡尔坐标
# - "gripper": 控制夹爪开合
# - "pump": 控制吸泵开关
# - "wait": 等待指定时间

# 参数说明：
# - speed: 移动速度 (0-200)
# - duration: 动作持续时间（秒）
# - 速度和时间的配合决定了动作的流畅度 