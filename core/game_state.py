import time
from utils.logger import logger

class GameState:
    def __init__(self):
        self.reset()
        logger.info("游戏状态模块初始化成功")

    def reset(self):
        """重置游戏状态"""
        self.champions = []  # 检测到的英雄
        self.items = []  # 检测到的物品
        self.analysis = ""  # 大模型分析结果
        self.timestamp = 0  # 状态更新时间戳
        self.round = 0  # 当前回合
        self.gold = 0  # 当前金币
        self.health = 0  # 当前生命值
        self.level = 0  # 当前等级
        self.board = []  # 棋盘上的英雄
        self.bench = []  # 替补席上的英雄

    def update(self, state_data):
        """更新游戏状态
        Args:
            state_data: 包含游戏状态数据的字典
        """
        try:
            if "champions" in state_data:
                self.champions = state_data["champions"]

            if "items" in state_data:
                self.items = state_data["items"]

            if "analysis" in state_data:
                self.analysis = state_data["analysis"]

            if "timestamp" in state_data:
                self.timestamp = state_data["timestamp"]
            else:
                self.timestamp = time.time()

            # 解析大模型分析结果，提取更多游戏状态信息
            self._parse_analysis()

            logger.info(f"游戏状态已更新: 回合 {self.round}, 金币 {self.gold}, 生命值 {self.health}, 等级 {self.level}")
        except Exception as e:
            logger.error(f"游戏状态更新失败: {str(e)}")

    def _parse_analysis(self):
        """解析大模型分析结果"""
        if not self.analysis:
            return

        try:
            # 从分析结果中提取回合信息
            if "回合" in self.analysis:
                for part in self.analysis.split():  # 遍历分析结果中的每个部分
                    if "回合" in part and part.replace("回合", "").isdigit():
                        self.round = int(part.replace("回合", ""))
                        break

            # 从分析结果中提取金币信息
            if "金币" in self.analysis:
                for part in self.analysis.split():  # 遍历分析结果中的每个部分
                    if "金币" in part and part.replace("金币", "").isdigit():
                        self.gold = int(part.replace("金币", ""))
                        break

            # 从分析结果中提取生命值信息
            if "生命值" in self.analysis:
                for part in self.analysis.split():  # 遍历分析结果中的每个部分
                    if "生命值" in part and part.replace("生命值", "").isdigit():
                        self.health = int(part.replace("生命值", ""))
                        break

            # 从分析结果中提取等级信息
            if "等级" in self.analysis:
                for part in self.analysis.split():  # 遍历分析结果中的每个部分
                    if "等级" in part and part.replace("等级", "").isdigit():
                        self.level = int(part.replace("等级", ""))
                        break
        except Exception as e:
            logger.error(f"分析结果解析失败: {str(e)}")

    def get_state_summary(self):
        """获取游戏状态摘要
        Returns:
            str: 游戏状态摘要
        """
        summary = f"回合: {self.round}, 金币: {self.gold}, 生命值: {self.health}, 等级: {self.level}\n"
        summary += f"检测到的英雄: {[c['name'] for c in self.champions]}\n"
        summary += f"检测到的物品: {[i['name'] for i in self.items]}\n"
        summary += f"分析结果: {self.analysis[:100]}..."
        return summary

# 单例模式
game_state = GameState()