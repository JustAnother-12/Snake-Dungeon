from enum import Enum
import random

class LootPool:
    def __init__(self):
        self.loot_table = {}  # Lưu tỉ lệ xuất hiện của vật phẩm

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

    def get_item(self):
        """Mở rương và chọn ngẫu nhiên vật phẩm dựa trên tỉ lệ"""
        items = list(self.loot_table.keys())
        rates = list(self.loot_table.values())
        
        # Chọn ngẫu nhiên dựa trên tỉ lệ
        return random.choices(items, weights=rates, k=1)[0]

    def show_loot_table(self):
        """Hiển thị danh sách vật phẩm và tỉ lệ"""
        for item, rate in self.loot_table.items():
            print(f"{item}: {rate}%")

class Rarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"

class LootItem(Enum):
    FOOD = "Food"
    COIN = "Coin"

