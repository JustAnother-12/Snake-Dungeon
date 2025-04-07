from tkinter import N
from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import ItemStack
from entities.items.item_type import ItemCategory, ItemTexture, ItemType, Rarity


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
        self.item_list = [] # lưu trữ các item đã giảm cooldown

    def apply_effect(self, snake):
        print(f"TimeEfficiency: Applying effect to {snake.inventory.slots} items")
        self.add_runtime_overriding(snake, 'update', 'before', self.reduce_cooldown)
    
    def reduce_cooldown(self, snake, *args, **kwargs):
        for item in snake.inventory.slots:
            if item is None or item.item_type.category == ItemCategory.EQUIPMENT:
                continue
            # print(item)
            if item.item_type.cooldown > 10 and item not in self.item_list:
                self.item_list.append(item)
                item.item_type.cooldown *= 0.8
                print(f"Reduced cooldown for {item.item_type.name} to {item.item_type.cooldown}s")
        
        return args, kwargs

    def remove_effect(self, snake):
        for item in self.item_list:
            item.item_type.cooldown *= 1.25
        self.remove_runtime_overriding(snake, 'update', 'before', self.reduce_cooldown)
            
    def get_item_entity_class(self):
        return TimeEfficiencyEntity
    
class TimeEfficiencyEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, TIME_EFFICIENCY_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return TimeEfficiencyStack()
        