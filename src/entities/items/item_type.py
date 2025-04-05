
from dataclasses import dataclass
from enum import Enum, auto
from tkinter import NO
from unicodedata import category

from utils import pixil


class Rarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon" 
    RARE = "Rare"

class ItemCategory(Enum):
    # Item nhận hiệu ứng ngay (coin, food) - không vào inventory
    INSTANT = auto()
    
    # Item dùng 1 lần và có thể stack (health potion, bomb)
    CONSUMABLE = auto()
    
    # Item passive, tự kích hoạt hiệu ứng
    EQUIPMENT = auto()

    # Item dùng nhiều lần, không stack
    SKILL = auto()

class ActivationType(Enum):
    # Kích hoạt khi va chạm với item
    ON_COLLISION = auto()
    
    # Kích hoạt khi nhặt item
    ON_PICKUP = auto()
    
    # Kích hoạt khi người dùng chọn dùng từ slot
    ON_USE = auto()

    AUTO = auto()

@dataclass
class ItemTexture:
    pixil_path: str
    frame: int = 0
    scale: int = 1

@dataclass
class ItemType:
    id: str
    name: str
    category: ItemCategory
    rarity: Rarity
    texture: ItemTexture
    description: str = ""
    max_stack: int = 1
    value: int = 1
    cooldown: float = 0
    price: int = 0
    energy_usage: int = 0
    activation_type: ActivationType = ActivationType.AUTO
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, ItemType):
            return self.id == value.id
        return False
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __post_init__(self):
        # Tự động điều chỉnh max_stack dựa trên category
        if self.category == ItemCategory.EQUIPMENT or self.category == ItemCategory.SKILL:
            self.max_stack = 1
        elif self.category == ItemCategory.INSTANT:
            self.max_stack = 0

        if self.activation_type == ActivationType.AUTO:
            match self.category:
                case ItemCategory.INSTANT | ItemCategory.EQUIPMENT:
                    self.activation_type = ActivationType.ON_PICKUP
                case ItemCategory.CONSUMABLE | ItemCategory.SKILL:
                    self.activation_type = ActivationType.ON_USE

        # chỉ có SKILL mới có energy_usage
        if self.category != ItemCategory.SKILL and self.energy_usage:
            raise ValueError("Chỉ có skill mới có energu_usage")
            
        # Tự động gán giá dựa trên rarity nếu chưa được chỉ định
        if self.price == 0:
            rarities = {
                Rarity.COMMON: 50,
                Rarity.UNCOMMON: 100,
                Rarity.RARE: 150,
            }
            self.price = rarities[self.rarity]
    
    