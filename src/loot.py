from typing import Tuple
from enum import Enum
import random
from re import L
from unittest import result

from entities.items.item_type import Rarity
from stats import StatType, Stats

class LootPool:
    def __init__(self, item_rate: Tuple[int, int, int, int, int, int, int] = (0, 0, 0, 0, 0, 0, 0), rarity_rate: Tuple[int, int, int] = (50, 35, 15)):
        """Khởi tạo LootPool với tỉ lệ xuất hiện của các vật phẩm
        - item_rate: tuple chứa tỉ lệ xuất hiện của các vật phẩm trong loot pool
            + item_rate[0]: EMPTY
            + item_rate[1]: COIN
            + item_rate[2]: FOOD
            + item_rate[3]: ITEM_INSTANT
            + item_rate[4]: CONSUMABLE
            + item_rate[5]: EQUIPMENT
            + item_rate[6]: SKILL
        - rarity_rate: tuple chứa tỉ lệ xuất hiện của các độ hiếm trong ITEM_INSTANT
            + rarity_rate[0]: COMMON
            + rarity_rate[1]: UNCOMMON
            + rarity_rate[2]: RARE
        """
        self.loot_table = {   
            LootItem.EMPTY: item_rate[0],
            LootItem.COIN: item_rate[1],
            LootItem.FOOD: item_rate[2],
            LootItem.ITEM_INSTANT: item_rate[3],
            LootItem.CONSUMABLE: item_rate[4],
            LootItem.EQUIPMENT: item_rate[5],
            LootItem.SKILL: item_rate[6]
        }
        self.rarity_table = {
            Rarity.COMMON: rarity_rate[0],
            Rarity.UNCOMMON: rarity_rate[1],
            Rarity.RARE: rarity_rate[2]
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

    def set_rate(self, item_rate = None, rarity_rate = None):
        """Chỉnh sửa tỉ lệ xuất hiện của vật phẩm"""
        if item_rate:
            for index, value in enumerate(self.loot_table):
                self.loot_table[value] = item_rate[index]
        if rarity_rate:
            for index, value in enumerate(self.rarity_table):
                self.rarity_table[value] = rarity_rate[index]

    def get_item(self):
        keys = list(self.loot_table.keys())
        values = list(self.loot_table.values())
        choices = random.choices(keys, values, k = 1 + Stats.getValue(StatType.LUCK)//10)
        result = sorted(choices, key = lambda x: x.value, reverse=True)[0]
        if result == LootItem.ITEM_INSTANT:
            # Chọn ngẫu nhiên độ hiếm của ITEM_INSTANT
            rarity = random.choices(list(self.rarity_table.keys()), list(self.rarity_table.values()))[0]
            return rarity
        return result

class LootItem(Enum):
    EMPTY = 1
    COIN = 2
    FOOD = 3
    ITEM_INSTANT = 4
    CONSUMABLE = 5
    EQUIPMENT = 6
    SKILL = 7
