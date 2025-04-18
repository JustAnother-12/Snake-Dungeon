from re import L
from typing import Tuple
from enum import Enum
import random

from entities.items.item_type import Rarity
from stats import StatType, Stats


class LootItem(Enum):
    EMPTY = 1
    COIN = 2
    FOOD = 3
    KEY = 4
    INSTANT = 5
    CONSUMABLE = 6
    EQUIPMENT = 7
    SKILL = 8


class LootPool:
    def __init__(self, item_rate: Tuple[int, int, int, int, int, int, int, int] = (0, 0, 0, 0, 0, 0, 0, 0), rarity_rate: Tuple[int, int, int] = (45, 35, 20)):
        """Khởi tạo LootPool với tỉ lệ xuất hiện của các vật phẩm
        - item_rate: tuple chứa tỉ lệ xuất hiện của các vật phẩm trong loot pool
            + item_rate[0]: EMPTY
            + item_rate[1]: COIN
            + item_rate[2]: FOOD
            + item_rate[3]: KEY
            + item_rate[4]: ITEM_INSTANT
            + item_rate[5]: CONSUMABLE
            + item_rate[6]: EQUIPMENT
            + item_rate[7]: SKILL
        - rarity_rate: tuple chứa tỉ lệ của các độ hiếm
            + rarity_rate[0]: COMMON
            + rarity_rate[1]: UNCOMMON
            + rarity_rate[2]: RARE
        """
        self.loot_table = {
            LootItem.EMPTY: item_rate[0],
            LootItem.COIN: item_rate[1],
            LootItem.FOOD: item_rate[2],
            LootItem.KEY: item_rate[3],
            LootItem.INSTANT: item_rate[3],
            LootItem.CONSUMABLE: item_rate[4],
            LootItem.EQUIPMENT: item_rate[5],
            LootItem.SKILL: item_rate[6]
        }
        self.rarity_table = {
            Rarity.COMMON: max(0, rarity_rate[0] - Stats.getValue(StatType.LUCK)/2),
            Rarity.UNCOMMON: rarity_rate[1] + Stats.getValue(StatType.LUCK)/3,
            Rarity.RARE: rarity_rate[2] + Stats.getValue(StatType.LUCK)/6
        }

    def add_item(self, item, rate):
        """Thêm vật phẩm với tỉ lệ xuất hiện (%)"""
        self.loot_table[item] = rate

    def add_rarity(self, rarity, rate):
        """Thêm độ hiếm với tỉ lệ xuất hiện (%)"""
        self.rarity_table[rarity] = rate

    def remove_item(self, item):
        """Xóa vật phẩm khỏi danh sách"""
        if item in self.loot_table:
            del self.loot_table[item]

    def remove_rarity(self, rarity):
        """Xóa độ hiếm khỏi danh sách"""
        if rarity in self.rarity_table:
            del self.rarity_table[rarity]

    def set_rate(self, item_rate=None, rarity_rate=None):
        """Chỉnh sửa tỉ lệ xuất hiện của vật phẩm"""
        if item_rate:
            for index, value in enumerate(self.loot_table):
                self.loot_table[value] = item_rate[index]
        if rarity_rate:
            for index, value in enumerate(self.rarity_table):
                self.rarity_table[value] = rarity_rate[index]

    def get_item(self) -> Tuple[LootItem, Rarity]:
        '''
        Lấy vật phẩm từ loot pool
        - Trả về tuple (LootItem, Rarity)
        - LootItem: vật phẩm được chọn [EMPTY, COIN, FOOD, INSTANT, CONSUMABLE, EQUIPMENT, SKILL]
        - Rarity: độ hiếm của vật phẩm
        '''
        keys = list(self.loot_table.keys())
        values = list(self.loot_table.values())
        choices = random.choices(
            keys, values, k=1 + Stats.getValue(StatType.LUCK)//10)
        result = sorted(choices, key=lambda x: x.value, reverse=True)[0]
        if result == LootItem.INSTANT or result == LootItem.CONSUMABLE or result == LootItem.EQUIPMENT or result == LootItem.SKILL:
            rarity = random.choices(list(self.rarity_table.keys()), list(
                self.rarity_table.values()))[0]
            return result, rarity
        return result, Rarity.COMMON
