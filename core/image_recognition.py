import os

import cv2
import numpy as np
import pytesseract
import time
import requests

from config import CARD_SELECT_REGION
from config.config import CONFIDENCE_THRESHOLD, RECOGNITION_TIMEOUT, GAME_REGION, CARD_SELECT_REGION, ITEM_SELECT_REGION, DIFY_API_KEY, DIFY_API_ENDPOINT
from utils.logger import logger

tesseract_config = r'--oem 3 --psm 6'

class ImageRecognition:
    def __init__(self):
        self.model_loaded = False
        logger.info("图像识别模块初始化成功")

    def load_model(self):
        """加载识别模型"""
        self.model_loaded = True
        return True

    def recognize_text(self, image):
        """识别图像中的文本
        Args:
            image: 输入图像
        Returns:
            str: 识别的文本
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray, config=tesseract_config)
            return text.strip()
        except Exception as e:
            logger.error(f"文本识别失败: {str(e)}")
            return ""

    def detect_cards(self, image):
        """检测图像中的商店中的卡牌
        Args:
            image: 输入图像
        Returns:
            list: 检测到的卡牌列表
        """
        try:
            # 提取卡牌选择区域
            x, y, w, h = CARD_SELECT_REGION
            card_region = image[y:y+h, x:x+w]

            # 预处理图像
            gray = cv2.cvtColor(card_region, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # 寻找轮廓
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            champions = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # 过滤小轮廓
                    x1, y1, w1, h1 = cv2.boundingRect(contour)
                    champion_roi = card_region[y1:y1+h1, x1:x1+w1]

                    # 使用OCR识别卡牌名称
                    name = self.recognize_text(champion_roi)
                    if name:
                        champions.append({
                            "name": name,
                            "position": (x + x1, y + y1),
                            "size": (w1, h1)
                        })

            return champions
        except Exception as e:
            logger.error(f"卡牌检测失败: {str(e)}")
            return []

    def detect_items(self, image):
        """检测图像中的物品
        Args:
            image: 输入图像
        Returns:
            list: 检测到的物品列表
        """
        if not self.model_loaded:
            logger.error("模型未加载，无法检测物品")
            return []

        try:
            # 提取物品选择区域
            x, y, w, h = ITEM_SELECT_REGION
            item_region = image[y:y+h, x:x+w]

            # 预处理图像
            gray = cv2.cvtColor(item_region, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # 寻找轮廓
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            items = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # 过滤小轮廓
                    x1, y1, w1, h1 = cv2.boundingRect(contour)
                    item_roi = item_region[y1:y1+h1, x1:x1+w1]

                    # 使用OCR识别物品名称
                    name = self.recognize_text(item_roi)
                    if name:
                        items.append({
                            "name": name,
                            "position": (x + x1, y + y1),
                            "size": (w1, h1)
                        })

            return items
        except Exception as e:
            logger.error(f"物品检测失败: {str(e)}")
            return []

    def analyze_game_state(self, image):
        """分析游戏状态
        Args:
            image: 输入图像
        Returns:
            dict: 游戏状态信息
        """
        try:
            start_time = time.time()
            # 保存传入的图片到本地以便分析
            os.makedirs("assets/screen_shots", exist_ok=True)
            timestamp = int(time.time())
            screenshot_path = f"assets/screen_shots/screenshot_{timestamp}.png"
            cv2.imwrite(screenshot_path, image)
            logger.info(f"游戏截图已保存到: {screenshot_path}")
            # 提取游戏区域
            x, y, w, h = GAME_REGION
            game_region = image[y:y+h, x:x+w]

            # 检测卡牌
            cards = self.detect_cards(image)

            # 检测物品
            items = self.detect_items(image)

            # 使用Dify API进行更高级的分析
            prompt = f"分析以下游戏画面信息并提供决策建议:\n检测到的卡牌: {[c['name'] for c in cards]}\n检测到的物品: {[i['name'] for i in items]}\n"
            # 这里留出Dify API调用接口，具体实现由用户完成
            analysis = ""  # 用户在此处实现Dify API调用

            elapsed_time = time.time() - start_time
            if elapsed_time > RECOGNITION_TIMEOUT:
                logger.warning(f"游戏状态分析超时: {elapsed_time:.2f}秒")

            return {
                "champions": cards,
                "items": items,
                "analysis": analysis,
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"游戏状态分析失败: {str(e)}")
            return {}

# 单例模式
image_recognition = ImageRecognition()