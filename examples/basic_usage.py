#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
云顶之弈AI自动玩程序示例
"""

import signal
import time

from main import TFTBot


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