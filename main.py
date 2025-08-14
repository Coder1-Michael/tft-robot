import threading
import time
import signal
import sys
from core.screen_capture import screen_capture
from core.image_recognition import image_recognition
from core.game_state import game_state
from core.decision_making import decision_making
from core.action_execution import action_execution
from utils.logger import logger
from config.config import CAPTURE_INTERVAL

class TFTBot:
    def __init__(self):
        self.handle_exit = None
        self.running = False
        self.stop_event = threading.Event()
        logger.info("云顶之弈自动对战程序初始化成功")

    def start(self):
        """启动程序"""
        if self.running:
            logger.warning("程序已经在运行中")
            return

        # 加载模型
        # if not image_recognition.load_model():
        #     logger.error("模型加载失败，无法启动程序")
        #     return

        self.running = True
        self.stop_event.clear()

        # 启动屏幕捕获线程
        self.capture_thread = threading.Thread(
            target=screen_capture.capture_loop,
            args=(self.on_screen_captured, self.stop_event)
        )
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
        # 分析游戏状态
        state_data = image_recognition.analyze_game_state(frame)

        # 更新游戏状态
        game_state.update(state_data)

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
