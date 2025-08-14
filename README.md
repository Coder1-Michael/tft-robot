# 云顶之弈自动对战程序

这是一个使用大模型进行图像识别的云顶之弈自动对战程序。该程序能够自动捕获游戏画面，识别游戏状态，并做出相应的决策和操作。

## 项目架构

项目采用模块化设计，遵循Python包结构最佳实践：

```
TFT-AI/
├── tft_ai/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── screen_capture.py     # 屏幕捕获模块
│   │   ├── image_recognition.py  # 图像识别模块
│   │   ├── game_state.py         # 游戏状态管理
│   │   ├── decision_making.py    # 决策模块
│   │   └── action_execution.py   # 操作执行模块
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py             # 配置文件
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── utils.py              # 工具函数
│   │   ├── logger.py             # 日志记录
│   │   └── model_loader.py       # 模型加载器
│   └── models/
│       └── __init__.py
├── main.py                       # 主程序入口
├── requirements.txt              # 依赖包列表
├── pyproject.toml                # 项目配置
├── README.md                     # 项目说明
├── examples/
│   └── basic_usage.py            # 使用示例
├── docs/                         # 文档
└── tests/                        # 测试
```

### 核心模块
- **core.screen_capture**: 负责捕获游戏屏幕画面
- **core.image_recognition**: 使用大模型进行图像识别
- **core.game_state**: 存储和管理游戏状态
- **core.decision_making**: 根据识别结果做出游戏决策
- **core.action_execution**: 执行游戏操作

### 配置和工具模块
- **config.config**: 包含程序配置参数
- **utils.utils**: 提供通用工具函数
- **utils.logger**: 处理日志记录
- **utils.model_loader**: 负责加载和管理AI模型

## 安装指南

1. 克隆项目
2. 安装依赖: `uv sync`
3. 配置模型路径和游戏设置 (在 `tft_ai/config/config.py` 中)
4. 运行主程序: `python main.py`

## 使用方法

### 基本使用
1. 确保云顶之弈游戏窗口处于激活状态
2. 运行程序: `python main.py`
3. 程序会自动开始识别和操作

### 使用示例
查看 `examples/basic_usage.py` 了解如何使用API:
```python
from tft_ai import TFTBot
import signal
import time

def main():
    # 创建TFTBot实例
    bot = TFTBot()

    # 设置信号处理
    signal.signal(signal.SIGINT, bot.handle_exit)
    signal.signal(signal.SIGTERM, bot.handle_exit)

    try:
        # 启动机器人
        bot.start()
        print("云顶之弈AI自动玩程序已启动。按Ctrl+C停止...")

        # 保持程序运行
        while bot.running:
            time.sleep(1)

    except Exception as e:
        print(f"程序异常: {str(e)}")
    finally:
        # 确保停止机器人
        bot.stop()
        print("程序已停止")

if __name__ == "__main__":
    main()
```

## 注意事项

1. 本程序仅供学习和研究使用，请勿用于商业用途
2. 使用前请确保已关闭游戏内的反作弊系统
3. 不同分辨率可能需要调整屏幕捕获参数
4. 首次运行可能需要下载模型，请确保网络连接正常