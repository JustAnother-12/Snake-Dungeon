
from dataclasses import dataclass
from enum import Enum, auto
from unicodedata import category


class Rarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon" 
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"

class ItemCategory(Enum):
    # Item nhận hiệu ứng ngay (coin, food) - không vào inventory
    INSTANT = auto()
    
    # Item dùng 1 lần và có thể stack (health potion, bomb)
    CONSUMABLE = auto()
    
    # Item dùng nhiều lần, không stack (skills, equipment)
    EQUIPMENT = auto()

@dataclass
class ItemType:
    id: str
    name: str
    category: ItemCategory
    rarity: Rarity
    texture_path: str
    max_stack: int = 1
    value: int = 1
    colldown: float = 0
    description: str = ""
    price: int = 0
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, ItemType):
            return self.id == value.id
        return False
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __post_init__(self):
        # Tự động điều chỉnh max_stack dựa trên category
        if self.category == ItemCategory.EQUIPMENT:
            self.max_stack = 1
        elif self.category == ItemCategory.INSTANT:
            self.max_stack = 0
            
        # Tự động gán giá dựa trên rarity nếu chưa được chỉ định
        if self.price == 0:
            rarities = {
                Rarity.COMMON: 5,
                Rarity.UNCOMMON: 15,
                Rarity.RARE: 50,
                Rarity.EPIC: 150,
                Rarity.LEGENDARY: 500
            }
            self.price = rarities[self.rarity]
    
    