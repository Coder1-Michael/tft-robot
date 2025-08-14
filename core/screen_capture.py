import pyautogui
import cv2
import numpy as np
import time
from config import SCREENSHOT_REGION, CAPTURE_INTERVAL
from logger import logger

class ScreenCapture:
    def __init__(self):
        self.region = SCREENSHOT_REGION
        self.capture_interval = CAPTURE_INTERVAL
        logger.info("屏幕捕获模块初始化成功")

    def capture_screen(self,bbox, region=None):
        """捕获屏幕画面
        Args:
            region: 捕获区域 (left, top, width, height)
        Returns:
            numpy.ndarray: 捕获的图像
        """
        print("box================>",bbox)
        try:
            if region is None:
                region = bbox
            screenshot = pyautogui.screenshot(region=region)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            return frame
        except Exception as e:
            logger.error(f"屏幕捕获失败: {str(e)}")
            return None

    def capture_loop(self,callback, stop_event,bbox):
        """持续捕获屏幕画面并调用回调函数
        Args:
            callback: 回调函数，接收捕获的图像
            stop_event: 停止事件
        """
        logger.info("开始屏幕捕获循环")
        while not stop_event.is_set():
            start_time = time.time()
            frame = self.capture_screen(bbox)
            if frame is not None:
                callback(frame)
            # 控制捕获频率
            elapsed_time = time.time() - start_time
            wait_time = max(0, self.capture_interval - elapsed_time)
            time.sleep(wait_time)
        logger.info("屏幕捕获循环已停止")

# 单例模式
screen_capture = ScreenCapture()