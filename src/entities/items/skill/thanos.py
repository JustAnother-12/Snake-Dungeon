

from pygame import Rect
from config import constant
from entities import Monster
from entities.Player import Snake
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity


THANOS_TYPE = ItemType(
    "thanos",
    "Thanos",
    ItemCategory.SKILL,
    Rarity.RARE,
    ItemTexture(
        constant.Texture.infinity_gauntlet
    ),
)


class ThanosItemStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(THANOS_TYPE, quantity)
    
    def apply_effect(self, snake: Snake):
        print("Thanos effect applied")
        print(snake.level.snake_group._sub_group__)
        for i in snake.level.snake_group._sub_group__:
            if isinstance(i, Monster.Monster):
                i.is_dead = True
    
    def get_item_entity_class(self):
        return ThanosEntity
    

class ThanosEntity(ItemEntity):
    from levels import level
    def __init__(self, level: "level.Level", area: Rect | None = None, r=2, quantity=1):
        super().__init__(level, THANOS_TYPE, area, r, quantity)
    
    
    def to_item_stack(self):
        return ThanosItemStack(self.quantity)