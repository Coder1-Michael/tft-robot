import os
import threading
import time
import signal
import sys

import cv2
from core.overlay_window import ResizableDraggableBox, run
from core.screen_capture import ScreenCapture
from core.decision_making import decision_making
from core.action_execution import action_execution
from utils.logger import logger
from config.config import CAPTURE_INTERVAL
import tkinter as tk
from tkinter import messagebox


class TFTBot:
    def __init__(self):
        self.capture_thread = None
        self.draw_thread = None
        self.handle_exit = None
        self.running = False
        self.stop_event = threading.Event()
        self.debug_mode = True
        self.bbox = (0, 0, 1920, 1080)  # 设置默认的截图区域
        self.rec_confirm = False
        logger.info("云顶之弈自动对战程序初始化成功")


    def start(self):
        if self.running:
            logger.warning("程序已经在运行中")
            return

        self.running = True
        self.stop_event.clear()

        # 启动绘制矩形线程
        threading.Thread(target=run, args=(self.on_rec_changed,), daemon=True).start()

        # 阻塞主线程 等待用户确认商店区域
        while True:
            time.sleep(0.5)  # 避免CPU占用过高
            # 如果确认了商店区域 启动屏幕捕获线程
            if self.rec_confirm:
                self.capture_thread = threading.Thread(
                    target=lambda: ScreenCapture().capture_loop(self.on_screen_captured, self.stop_event, self.bbox),
                    daemon=True
                )
                break


        self.capture_thread.daemon = True
        self.capture_thread.start()

        # 启动主循环
        self.main_loop()

    def stop(self):
        """停止程序"""
        if not self.running:
            logger.warning("程序已经停止")
            return

        logger.info("正在停止程序...")
        self.running = False
        self.stop_event.set()

        # 等待线程结束
        if hasattr(self, 'capture_thread') and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=5.0)

        logger.info("程序已停止")

    def on_screen_captured(self, frame):
        """屏幕捕获回调函数"""
        # 使用 frame.shape 获取图像的高度和宽度
        screenshot_height, screenshot_width = frame.shape[:2]  # 获取 (height, width)

        # 计算每一小图的宽度（纵向高度保持不变）
        sub_width = screenshot_width // 5  # 横向切割成五份

        # 切割并保存小图
        for i in range(5):
            left = i * sub_width
            right = (i + 1) * sub_width if i < 4 else screenshot_width  # 最后一块图的右边界
            # 截取每一块小图，保持原高度
            sub_image = frame[:, left:right]  # 使用 numpy 切割图像
            screenshot_dir = r"D:\project\tft-robot\assets\screen_shots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            timestamp = int(time.time())  # 使用当前时间戳
            sub_image_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}_{i}.png")
            # 将 numpy 数组保存为图片
            if not cv2.imwrite(sub_image_path, sub_image):
                logger.error(f"截图保存失败：{sub_image_path}")
            print(f"小图已保存：{sub_image_path}")

    def on_rec_changed(self, x1, y1, x2, y2):
        """屏幕捕获回调函数"""
        # 截取方框区域的屏幕截图
        self.bbox = (x1, y1, x2, y2)
        print("边框变化=========》",self.bbox)
        
        # 创建确认对话框
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        # 显示确认对话框
        confirmed = tk.messagebox.askyesno("确认", "是否确认当前选择的商店区域？")
        if confirmed:
            print("用户已确认商店区域")
            return True
        else:
            print("用户取消确认，请重新选择")
            return False

    def main_loop(self):
        """主循环"""
        logger.info("程序已启动，开始自动对战...")
        try:
            while self.running and not self.stop_event.is_set():
                # 做出决策
                decision = decision_making.make_decision()

                # 执行决策
                if decision:
                    action_execution.execute_decision(decision)

                # 等待一段时间
                time.sleep(CAPTURE_INTERVAL)
        except Exception as e:
            logger.error(f"主循环异常: {str(e)}")
            self.stop()

def signal_handler(sig, frame):
    """信号处理函数"""
    logger.info("接收到停止信号，正在退出...")
    if 'bot' in globals():
        bot.stop()
    sys.exit(0)

# 注册信号处理
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    try:
        bot = TFTBot()
        bot.start()
    except Exception as e:
        logger.error(f"程序启动失败: {str(e)}")
        sys.exit(1)

# 访问 https://github.com 以获取更多信息
