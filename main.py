import os
import threading
import time
import signal
import sys

import cv2
import numpy as np

from core.overlay_window import run
from core.round_area_box import draw_round_area_box
from core.screen_capture import ScreenCapture
from core.decision_making import decision_making
from core.action_execution import action_execution
from utils.logger import logger
from config.config import CAPTURE_INTERVAL
import tkinter as tk
from tkinter import messagebox
from skimage.metrics import structural_similarity as ssim

class TFTBot:
    def __init__(self):
        self.capture_thread = None
        self.draw_thread = None
        self.handle_exit = None
        self.running = False
        self.screen_capture_stop_event = threading.Event()  # 截图线程停止事件
        self.round_area_stop_event = threading.Event()  # 停止回合区域绘制的线程标志
        self.store_area = (0, 0, 0, 0)  # 商店区域
        self.store_area_confirm = False  # 商店区域确认标志
        self.round_area = (0, 0, 0, 0)  # 商店区域
        self.round_area_thread = None  # 当前回合区域绘制的线程
        self.cards_dir = r"D:\project\tft-robot\assets\cards"
        self.screenshot_dir = r"D:\project\tft-robot\assets\screen_shots"
        self.image_error = False
        logger.info("云顶之弈自动对战程序初始化成功")

    def start(self):
        if self.running:
            logger.warning("程序已经在运行中")
            return

        self.running = True
        self.screen_capture_stop_event.clear()

        # 启动绘制矩形线程 用于选择商店区域 拖拽结束触发draw_finsh回调
        threading.Thread(target=run, args=(self.draw_finsh,), daemon=True).start()

        # 阻塞主线程 等待用户确认商店区域
        while True:
            time.sleep(1)
            # 如果确认了商店区域 启动屏幕捕获线程
            if self.store_area_confirm:
                self.capture_thread = threading.Thread(
                    target=lambda: ScreenCapture().capture_loop(self.on_screen_captured, self.screen_capture_stop_event,
                                                                self.store_area),
                    daemon=True
                )
                break
        logger.info("开始计算回合区域")
        self.calculate_round_area()

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
        self.screen_capture_stop_event.set()

        # 等待线程结束
        if hasattr(self, 'capture_thread') and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=5.0)

        logger.info("程序已停止")

    def load_card_images(self):
        """加载所有卡片图像"""
        card_images = []
        for filename in os.listdir(self.cards_dir):
            card_path = os.path.join(self.cards_dir, filename)
            if os.path.isfile(card_path) and filename.endswith(".png"):  # 只加载 .png 文件
                card_image = cv2.imread(card_path)
                card_images.append(card_image)
        return card_images

    def on_screen_captured(self, frame):
        """屏幕捕获回调函数"""
        screenshot_height, screenshot_width = frame.shape[:2]
        screenshot_dir = r"D:\project\tft-robot\assets\screen_shots"
        cards_dir = r"D:\project\tft-robot\assets\cards"  # 存放卡片图像的目录

        sub_width = screenshot_width // 5  # 横向切割成五份

        for i in range(5):
            left = i * sub_width
            right = (i + 1) * sub_width if i < 4 else screenshot_width
            timestamp = int(time.time())  # 使用当前时间戳
            sub_image = frame[:, left:right]

            match_found = False
            for card_name in os.listdir(cards_dir):
                card_path = os.path.join(cards_dir, card_name)
                if not os.path.isfile(card_path):
                    continue  # 如果不是文件，跳过

                card_image = cv2.imread(card_path, cv2.IMREAD_COLOR)
                if card_image is None:
                    continue  # 如果无法读取卡片图像，跳过

                # 将 card_image 和 sub_image 调整为相同的尺寸
                card_image_resized = cv2.resize(card_image, (sub_image.shape[1], sub_image.shape[0]))

                # 计算像素点差异比率
                diff_ratio = np.sum(
                    np.abs(sub_image.astype(np.float32) - card_image_resized.astype(np.float32)) > 10) / float(
                    sub_image.size)

                if diff_ratio < 0.5:  # 设置阈值判断为相似图像
                    match_found = True
                    break

            if not match_found:
                if not os.path.exists(self.cards_dir):
                    os.makedirs(self.cards_dir)

                sub_image_path = os.path.join(self.cards_dir, f"screenshot_{timestamp}_{i}.png")
                if not cv2.imwrite(sub_image_path, sub_image):
                    print(f"截图保存失败：{sub_image_path}")
                print(f"小图已保存：{sub_image_path}")
            else:
                print(f"小图{i}找到匹配，未保存。")

    def draw_finsh(self, x1, y1, x2, y2):
        """屏幕捕获回调函数"""
        # 截取方框区域的屏幕截图
        self.store_area = (x1, y1, x2, y2)
        logger.info(f"商店区域确认: {self.store_area}")

        # 创建确认对话框
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口

        # 显示确认对话框
        confirmed = tk.messagebox.askyesno("确认", "是否确认当前选择的商店区域？")
        if confirmed:
            logger.info("用户已确认商店区域")
            self.store_area_confirm = True

            # 计算回合数区域并重新绘制
            self.calculate_round_area()
            # 启动回合区域绘制线程
            self.round_area_thread = threading.Thread(target=draw_round_area_box, args=(self.round_area,), daemon=True)
            self.round_area_thread.start()

            return True
        else:
            logger.info("用户取消确认，请重新选择")
            self.store_area_confirm = False

            # 如果用户取消确认商店区域，清空回合区域并重新绘制
            self.round_area = (0, 0, 0, 0)
            if self.round_area_thread is not None and self.round_area_thread.is_alive():
                logger.info("停止之前的回合区域绘制线程")
                self.round_area_thread.join()
            self.round_area_thread = threading.Thread(target=draw_round_area_box, args=(self.round_area,), daemon=True)
            self.round_area_thread.start()

            return False

    def calculate_round_area(self):
        """
        根据确认后的商店区域计算回合区域的坐标。
        假设回合数区域位于商店区域的上方或者下方。
        """
        if not self.store_area_confirm:
            logger.error("商店区域尚未确认，无法计算回合区域")
            return

        # 获取商店区域的坐标
        x1, y1, x2, y2 = self.store_area
        shop_height = y2 - y1

        # 假设回合数区域位于商店区域上方
        # 偏移量可以根据实际情况进行调整，这里设定为商店区域高度的10%
        round_area_top = (x1, y1 - int(shop_height * 6.2))  # 回合数区域上方
        round_area_bottom = (x2, y1 - int(shop_height * 6.2) + int(shop_height * 0.2))  # 回合数区域的下边界，假设高度为商店区域的20%

        # 打印回合区域的坐标
        logger.info(f"回合数区域坐标: {round_area_top} -> {round_area_bottom}")

        self.round_area = (round_area_top[0], round_area_top[1], round_area_bottom[0], round_area_bottom[1])

        return self.round_area

    def main_loop(self):
        """主循环"""
        logger.info("程序已启动，开始自动对战...")
        try:
            while self.running and not self.screen_capture_stop_event.is_set():
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
