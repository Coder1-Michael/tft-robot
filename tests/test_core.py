#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
云顶之弈AI自动玩程序核心功能测试
"""

import unittest
from core.game_state import GameState
from core.decision_making import DecisionMaking
from config.config import PRIORITY_CHAMPIONS, PRIORITY_ITEMS

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()

    def test_reset(self):
        """测试游戏状态重置"""
        self.game_state.champions = [{'name': '亚索', 'position': (100, 200), 'size': (50, 50)}]
        self.game_state.items = [{'name': '无尽之刃', 'position': (300, 400), 'size': (30, 30)}]
        self.game_state.round = 5
        self.game_state.gold = 50
        self.game_state.health = 80
        self.game_state.level = 6

        self.game_state.reset()

        self.assertEqual(self.game_state.champions, [])
        self.assertEqual(self.game_state.items, [])
        self.assertEqual(self.game_state.round, 0)
        self.assertEqual(self.game_state.gold, 0)
        self.assertEqual(self.game_state.health, 0)
        self.assertEqual(self.game_state.level, 0)

    def test_update(self):
        """测试游戏状态更新"""
        state_data = {
            'champions': [{'name': '亚索', 'position': (100, 200), 'size': (50, 50)}],
            'items': [{'name': '无尽之刃', 'position': (300, 400), 'size': (30, 30)}],
            'analysis': '当前回合3，金币20，生命值90，等级4',
            'timestamp': 1234567890
        }

        self.game_state.update(state_data)

        self.assertEqual(len(self.game_state.champions), 1)
        self.assertEqual(self.game_state.champions[0]['name'], '亚索')
        self.assertEqual(len(self.game_state.items), 1)
        self.assertEqual(self.game_state.items[0]['name'], '无尽之刃')
        self.assertEqual(self.game_state.round, 3)
        self.assertEqual(self.game_state.gold, 20)
        self.assertEqual(self.game_state.health, 90)
        self.assertEqual(self.game_state.level, 4)

class TestDecisionMaking(unittest.TestCase):
    def setUp(self):
        self.decision_making = DecisionMaking()
        self.game_state = GameState()

    def test_parse_decision(self):
        """测试决策解析"""
        # 设置游戏状态
        self.game_state.champions = [
            {'name': '亚索', 'position': (100, 200), 'size': (50, 50)},
            {'name': '盖伦', 'position': (150, 200), 'size': (50, 50)}
        ]

        # 测试购买英雄
        decision = "购买英雄：亚索"
        parsed = self.decision_making._parse_decision(decision)
        self.assertEqual(parsed['buy_champion'], '亚索')

        # 测试出售英雄
        decision = "出售英雄：盖伦"
        parsed = self.decision_making._parse_decision(decision)
        self.assertEqual(parsed['sell_champion'], '盖伦')

        # 测试刷新商店
        decision = "刷新商店"
        parsed = self.decision_making._parse_decision(decision)
        self.assertTrue(parsed['refresh_shop'])

        # 测试升级等级
        decision = "升级等级"
        parsed = self.decision_making._parse_decision(decision)
        self.assertTrue(parsed['upgrade_level'])

        # 测试装备物品
        decision = "给亚索装备无尽之刃"
        parsed = self.decision_making._parse_decision(decision)
        self.assertEqual(parsed['equip_item']['champion'], '亚索')
        self.assertEqual(parsed['equip_item']['item'], '无尽之刃')

if __name__ == '__main__':
    unittest.main()