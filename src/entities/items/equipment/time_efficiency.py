

from config import constant
from entities.Player import Snake
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity
from utils.help import Share
from stats import StatType, Stats


TIME_EFFICIENCY_TYPE = ItemType(
    'time_efficiency',
    'Time Efficiency',
    ItemCategory.EQUIPMENT,
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.time_efficiency,
    ),
    description=r"-20% cooldown for item with greater than 10s cooldown",
    price=150,
)

class TimeEfficiencyStack(ItemStack):
    def __init__(self):
        super().__init__(TIME_EFFICIENCY_TYPE, 1)
        self.item_list = []

    def apply_effect(self, snake: Snake):
        for item in snake.level.item_group:
            if item.item_type.cooldown > 10:
                self.item_list.append(item)
                item.item_type.cooldown *= 0.8

    def remove_effect(self, snake):
        for item in self.item_list:
            item.item_type.cooldown *= 1.25
            
    def get_item_entity_class(self):
        return TimeEfficiencyEntity
    
class TimeEfficiencyEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, TIME_EFFICIENCY_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return TimeEfficiencyStack()
        