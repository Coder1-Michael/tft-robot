import pyautogui
import keyboard
import mouse
import time
from config.config import ACTION_DELAY, KEYBOARD_DELAY, MOUSE_DELAY, CARD_SELECT_REGION
from utils.logger import logger
from core.game_state import game_state

class ActionExecution:
    def __init__(self):
        self.action_delay = ACTION_DELAY
        self.keyboard_delay = KEYBOARD_DELAY
        self.mouse_delay = MOUSE_DELAY
        logger.info("操作执行模块初始化成功")

    def click(self, x, y):
        """点击指定坐标
        Args:
            x: x坐标
            y: y坐标
        """
        try:
            pyautogui.moveTo(x, y, duration=self.mouse_delay)
            pyautogui.click()
            time.sleep(self.action_delay)
            logger.info(f"点击坐标: ({x}, {y})")
        except Exception as e:
            logger.error(f"点击操作失败: {str(e)}")

    def double_click(self, x, y):
        """双击指定坐标
        Args:
            x: x坐标
            y: y坐标
        """
        try:
            pyautogui.moveTo(x, y, duration=self.mouse_delay)
            pyautogui.doubleClick()
            time.sleep(self.action_delay)
            logger.info(f"双击坐标: ({x}, {y})")
        except Exception as e:
            logger.error(f"双击操作失败: {str(e)}")

    def press_key(self, key):
        """按下指定按键
        Args:
            key: 按键名称
        """
        try:
            keyboard.press(key)
            time.sleep(self.keyboard_delay)
            keyboard.release(key)
            time.sleep(self.action_delay)
            logger.info(f"按下按键: {key}")
        except Exception as e:
            logger.error(f"按键操作失败: {str(e)}")

    def buy_champion(self, champion_name):
        """购买指定英雄
        Args:
            champion_name: 英雄名称
        """
        try:
            # 在游戏状态中查找英雄位置
            for champion in game_state.champions:
                if champion["name"] == champion_name:
                    x, y = champion["position"]
                    # 点击英雄
                    self.click(x + champion["size"][0] // 2, y + champion["size"][1] // 2)
                    logger.info(f"购买英雄: {champion_name}")
                    return True

            logger.warning(f"未找到英雄: {champion_name}")
            return False
        except Exception as e:
            logger.error(f"购买英雄失败: {str(e)}")
            return False

    def sell_champion(self, champion_name):
        """出售指定英雄
        Args:
            champion_name: 英雄名称
        """
        try:
            # 假设出售英雄需要拖动到指定区域
            sell_region = (1800, 500, 100, 100)  # 出售区域坐标和大小
            sell_x, sell_y = sell_region[0] + sell_region[2] // 2, sell_region[1] + sell_region[3] // 2

            # 在棋盘或替补席上查找英雄
            # 这里简化处理，实际需要根据游戏状态中的board和bench信息查找
            for champion in game_state.champions:
                if champion["name"] == champion_name:
                    x, y = champion["position"]
                    # 拖动英雄到出售区域
                    pyautogui.moveTo(x + champion["size"][0] // 2, y + champion["size"][1] // 2, duration=self.mouse_delay)
                    mouse.press()
                    time.sleep(self.action_delay)
                    pyautogui.moveTo(sell_x, sell_y, duration=self.mouse_delay)
                    mouse.release()
                    time.sleep(self.action_delay)
                    logger.info(f"出售英雄: {champion_name}")
                    return True

            logger.warning(f"未找到英雄: {champion_name}")
            return False
        except Exception as e:
            logger.error(f"出售英雄失败: {str(e)}")
            return False

    def upgrade_level(self):
        """升级等级"""
        try:
            # 假设升级等级的按钮在指定位置
            upgrade_button = (1800, 300, 50, 50)  # 升级按钮坐标和大小
            x, y = upgrade_button[0] + upgrade_button[2] // 2, upgrade_button[1] + upgrade_button[3] // 2
            self.click(x, y)
            logger.info("升级等级")
            return True
        except Exception as e:
            logger.error(f"升级等级失败: {str(e)}")
            return False

    def refresh_shop(self):
        """刷新商店"""
        try:
            # 假设刷新商店的按钮在指定位置
            refresh_button = (1600, 600, 50, 50)  # 刷新按钮坐标和大小
            x, y = refresh_button[0] + refresh_button[2] // 2, refresh_button[1] + refresh_button[3] // 2
            self.click(x, y)
            logger.info("刷新商店")
            return True
        except Exception as e:
            logger.error(f"刷新商店失败: {str(e)}")
            return False

    def equip_item(self, champion_name, item_name):
        """给指定英雄装备指定物品
        Args:
            champion_name: 英雄名称
            item_name: 物品名称
        """
        try:
            # 在游戏状态中查找英雄和物品位置
            champion_pos = None
            for champion in game_state.champions:
                if champion["name"] == champion_name:
                    champion_pos = (champion["position"][0] + champion["size"][0] // 2,
                                  champion["position"][1] + champion["size"][1] // 2)
                    break

            item_pos = None
            for item in game_state.items:
                if item["name"] == item_name:
                    item_pos = (item["position"][0] + item["size"][0] // 2,
                              item["position"][1] + item["size"][1] // 2)
                    break

            if not champion_pos or not item_pos:
                logger.warning(f"未找到英雄或物品: {champion_name}, {item_name}")
                return False

            # 拖动物品到英雄身上
            pyautogui.moveTo(item_pos[0], item_pos[1], duration=self.mouse_delay)
            mouse.press()
            time.sleep(self.action_delay)
            pyautogui.moveTo(champion_pos[0], champion_pos[1], duration=self.mouse_delay)
            mouse.release()
            time.sleep(self.action_delay)
            logger.info(f"给英雄 {champion_name} 装备物品 {item_name}")
            return True
        except Exception as e:
            logger.error(f"装备物品失败: {str(e)}")
            return False

    def execute_decision(self, decision):
        """执行决策
        Args:
            decision: 决策信息字典
        Returns:
            bool: 是否成功执行
        """
        try:
            if not decision:
                logger.warning("没有决策可执行")
                return False

            success = True

            # 购买英雄
            if decision["buy_champion"]:
                if not self.buy_champion(decision["buy_champion"]):
                    success = False

            # 出售英雄
            if decision["sell_champion"]:
                if not self.sell_champion(decision["sell_champion"]):
                    success = False

            # 升级英雄 (这里简化处理，实际可能需要特定操作)
            if decision["upgrade_champion"]:
                logger.info(f"升级英雄: {decision["upgrade_champion"]}")
                # 实际游戏中升级英雄通常需要拥有三个相同英雄，这里假设已经满足条件
                # 找到英雄并点击
                for champion in game_state.champions:
                    if champion["name"] == decision["upgrade_champion"]:
                        x, y = champion["position"]
                        self.click(x + champion["size"][0] // 2, y + champion["size"][1] // 2)
                        break

            # 装备物品
            if decision["equip_item"]:
                if not self.equip_item(
                    decision["equip_item"]["champion"],
                    decision["equip_item"]["item"]
                ):
                    success = False

            # 刷新商店
            if decision["refresh_shop"]:
                if not self.refresh_shop():
                    success = False

            # 升级等级
            if decision["upgrade_level"]:
                if not self.upgrade_level():
                    success = False

            # 输出其他建议
            for suggestion in decision["other_suggestions"]:
                logger.info(f"其他建议: {suggestion}")

            return success
        except Exception as e:
            logger.error(f"执行决策失败: {str(e)}")
            return False

# 单例模式
action_execution = ActionExecution()