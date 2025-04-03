from typing import Tuple
from enum import Enum
import random
from re import L

class LootPool:
    def __init__(self, pot: Tuple = (50, 35, 15), chest: Tuple = (45, 35, 20)):
        self.loot_table = {
            "POT": {
                "first_roll": {
                    LootItem.EMPTY: 30,
                    LootItem.NON_EMPTY: 70
                },
                "second_roll": {
                    LootItem.COIN: pot[0],
                    LootItem.FOOD: pot[1],
                    LootItem.ITEM_INSTANT: pot[2]
                }
            },
            "CHEST": {
                "first_roll": {
                    LootItem.COIN: 1
                },
                "second_roll": {
                    LootItem.CONSUMABLE: chest[0],
                    LootItem.EQUIPMENT: chest[1],
                    LootItem.SKILL: chest[2]
                }
            }}
    def add_item(self, item, rate):
        """Thêm vật phẩm với tỉ lệ xuất hiện (%)"""
        self.loot_table[item] = rate

    def remove_item(self, item):
        """Xóa vật phẩm khỏi danh sách"""
        if item in self.loot_table:
            del self.loot_table[item]

    def set_rate(self, item, rate):
        """Chỉnh sửa tỉ lệ xuất hiện của vật phẩm"""
        if item in self.loot_table:
            self.loot_table[item] = rate

    def get_item(self, source: str):
        """Mở rương và chọn ngẫu nhiên vật phẩm dựa trên tỉ lệ
        - source: "POT" hoặc "CHEST"
        """
        match source:
            case "POT":
                # first_roll
                items = list(self.loot_table["POT"]["first_roll"].keys())
                rates = list(self.loot_table["POT"]["first_roll"].values())
                choice = random.choices(items, weights=rates, k=1)[0]
                if choice == LootItem.NON_EMPTY:
                    # second_roll
                    items = list(self.loot_table["POT"]["second_roll"].keys())
                    rates = list(self.loot_table["POT"]["second_roll"].values())
                    return random.choices(items, weights=rates, k=1)[0]
                else:
                    return LootItem.EMPTY
            case "CHEST":
                items = list(self.loot_table["CHEST"]["second_roll"].keys())
                rates = list(self.loot_table["CHEST"]["second_roll"].values())
                return random.randint(20, 25) ,random.choices(items, weights=rates, k=1)[0]
            case _:
                return LootItem.EMPTY
    def show_loot_table(self):
        """Hiển thị danh sách vật phẩm và tỉ lệ"""
        for item, rate in self.loot_table.items():
            print(f"{item}: {rate}%")

class Rarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"

class LootItem(Enum):
    EMPTY = "Empty"
    NON_EMPTY = "Non Empty"
    COIN = "Coin"
    FOOD = "Food"
    ITEM_INSTANT = "Item Instant"
    CONSUMABLE = "Consumable"
    EQUIPMENT = "Equipment"
    SKILL = "Skill"
