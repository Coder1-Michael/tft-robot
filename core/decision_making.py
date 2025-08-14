import time
from config.config import PRIORITY_CHAMPIONS, PRIORITY_ITEMS, MAX_TOKENS, TEMPERATURE
from utils.logger import logger
from core.game_state import game_state
from utils.model_loader import model_loader

class DecisionMaking:
    def __init__(self):
        self.priority_champions = PRIORITY_CHAMPIONS
        self.priority_items = PRIORITY_ITEMS
        logger.info("决策模块初始化成功")

    def make_decision(self):
        """根据当前游戏状态做出决策
        Returns:
            dict: 包含决策信息的字典
        """
        try:
            if not game_state.timestamp:
                logger.warning("游戏状态未更新，无法做出决策")
                return {}

            # 获取游戏状态摘要
            state_summary = game_state.get_state_summary()
            logger.info(f"基于以下状态做出决策:\n{state_summary}")

            # 构建提示
            prompt = f"你是一个云顶之弈游戏专家，请根据以下游戏状态信息，提供最佳决策建议:\n{state_summary}\n\n"
            prompt += "请考虑以下优先事项:\n"
            prompt += f"1. 优先选择英雄: {self.priority_champions}\n"
            prompt += f"2. 优先选择物品: {self.priority_items}\n\n"
            prompt += "请提供具体的决策建议，包括但不限于:\n"
            prompt += "- 是否购买英雄，如果是，购买哪个英雄\n"
            prompt += "- 是否出售英雄，如果是，出售哪个英雄\n"
            prompt += "- 是否升级英雄，如果是，升级哪个英雄\n"
            prompt += "- 是否装备物品，如果是，给谁装备什么物品\n"
            prompt += "- 是否刷新商店\n"
            prompt += "- 是否升级等级\n"
            prompt += "- 其他战术建议\n"
            prompt += "请以简洁明了的方式提供建议，避免冗长的解释。"

            # 使用大模型生成决策
            decision = model_loader.generate_text(prompt, max_length=MAX_TOKENS, temperature=TEMPERATURE)

            if not decision:
                logger.error("决策生成失败")
                return {}

            logger.info(f"决策结果: {decision}")

            # 解析决策结果
            parsed_decision = self._parse_decision(decision)

            return parsed_decision
        except Exception as e:
            logger.error(f"决策制定失败: {str(e)}")
            return {}

    def _parse_decision(self, decision):
        """解析决策结果
        Args:
            decision: 大模型生成的决策文本
        Returns:
            dict: 解析后的决策信息
        """
        parsed = {
            "buy_champion": None,
            "sell_champion": None,
            "upgrade_champion": None,
            "equip_item": None,
            "refresh_shop": False,
            "upgrade_level": False,
            "other_suggestions": []
        }

        try:
            lines = decision.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # 检查是否购买英雄
                if "购买英雄" in line:
                    for champion in self.priority_champions:
                        if champion in line:
                            parsed["buy_champion"] = champion
                            break

                # 检查是否出售英雄
                if "出售英雄" in line:
                    for champion in [c["name"] for c in game_state.champions]:
                        if champion in line:
                            parsed["sell_champion"] = champion
                            break

                # 检查是否升级英雄
                if "升级英雄" in line:
                    for champion in [c["name"] for c in game_state.champions]:
                        if champion in line:
                            parsed["upgrade_champion"] = champion
                            break

                # 检查是否装备物品
                if "装备物品" in line:
                    for item in self.priority_items:
                        if item in line:
                            for champion in [c["name"] for c in game_state.champions]:
                                if champion in line:
                                    parsed["equip_item"] = {
                                        "champion": champion,
                                        "item": item
                                    }
                                    break
                            break

                # 检查是否刷新商店
                if "刷新商店" in line:
                    parsed["refresh_shop"] = True

                # 检查是否升级等级
                if "升级等级" in line:
                    parsed["upgrade_level"] = True

                # 其他建议
                if any(keyword in line for keyword in ["建议", "应该", "需要"]):
                    parsed["other_suggestions"].append(line)
        except Exception as e:
            logger.error(f"决策解析失败: {str(e)}")

        return parsed

# 单例模式
decision_making = DecisionMaking()