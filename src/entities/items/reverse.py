

from entities.Player import Snake
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemType, Rarity


REVERSE_TYPE = ItemType(
    "reverse",
    "Reverse",
    ItemCategory.CONSUMABLE,
    Rarity.COMMON,
    description="Reverse head and tail after 3 seconds come back to normal",
    max_stack=3,
    cooldown=10,
)

class ReverseStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(REVERSE_TYPE, quantity)
    
    def apply_effect(self, snake: Snake):
        print("ok")

    def get_item_entity_class(self):
        return ReverseEntity


class ReverseEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, REVERSE_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return ReverseStack(self.quantity)
    def get_item_entity_class(self):
        return ReverseStack(self.quantity)