import os
import cv2
import numpy as np
import time
from utils.logger import logger

class Utils:
    @staticmethod
    def ensure_dir(path):
        """确保目录存在
        Args:
            path: 目录路径
        """
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(f"创建目录: {path}")

    @staticmethod
    def save_image(image, path):
        """保存图像
        Args:
            image: 图像数据
            path: 保存路径
        Returns:
            bool: 是否保存成功
        """
        try:
            # 确保目录存在
            dir_path = os.path.dirname(path)
            Utils.ensure_dir(dir_path)

            # 保存图像
            cv2.imwrite(path, image)
            logger.info(f"图像已保存: {path}")
            return True
        except Exception as e:
            logger.error(f"保存图像失败: {str(e)}")
            return False

    @staticmethod
    def load_image(path):
        """加载图像
        Args:
            path: 图像路径
        Returns:
            numpy.ndarray: 加载的图像，如果失败则返回None
        """
        try:
            if not os.path.exists(path):
                logger.warning(f"图像文件不存在: {path}")
                return None

            image = cv2.imread(path)
            if image is None:
                logger.warning(f"无法加载图像: {path}")
                return None

            logger.info(f"图像已加载: {path}")
            return image
        except Exception as e:
            logger.error(f"加载图像失败: {str(e)}")
            return None

    @staticmethod
    def preprocess_image(image):
        """预处理图像
        Args:
            image: 输入图像
        Returns:
            numpy.ndarray: 预处理后的图像
        """
        try:
            # 转换为灰度图
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # 高斯模糊
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # 自适应阈值
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
            )

            return thresh
        except Exception as e:
            logger.error(f"图像预处理失败: {str(e)}")
            return image

    @staticmethod
    def get_center(region):
        """获取区域中心点
        Args:
            region: 区域 (x, y, width, height)
        Returns:
            tuple: 中心点坐标 (x, y)
        """
        x, y, w, h = region
        return (x + w // 2, y + h // 2)

    @staticmethod
    def timeit(func):
        """计时装饰器
        Args:
            func: 要计时的函数
        Returns:
            function: 包装后的函数
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"函数 {func.__name__} 执行时间: {elapsed_time:.4f} 秒")
            return result
        return wrapper

utils = Utils()