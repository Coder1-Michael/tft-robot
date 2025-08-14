import logging
import os
from config import LOG_LEVEL, LOG_FILE

# 确保日志目录存在
log_dir = os.path.dirname(LOG_FILE)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志记录器
logger = logging.getLogger("TFT-AI")
logger.setLevel(LOG_LEVEL)

# 创建文件处理器
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(LOG_LEVEL)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加处理器到记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 测试日志
if __name__ == '__main__':
    logger.info("日志记录器初始化成功")
    logger.warning("这是一个警告信息")
    logger.error("这是一个错误信息")