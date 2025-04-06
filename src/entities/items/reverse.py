

import pygame
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
    cooldown=1,
)

class ReverseStack(ItemStack):
    def __init__(self, quantity=1):
        super().__init__(REVERSE_TYPE, quantity)
    
    def apply_effect(self, snake: Snake):
        snake._block_positions.reverse()
        for index, pos in enumerate(snake._block_positions):
            snake.blocks[index].pos = pos
        
        print(snake.direction)
        v = snake._block_positions[0] - snake._block_positions[1]
        v.scale_to_length(1)
        print(v)
        snake._last_direction = -v
        snake.direction = v

    def get_item_entity_class(self):
        return ReverseEntity

class ReverseEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, REVERSE_TYPE, area, r, quantity)
    
    def to_item_stack(self):
        return ReverseStack(self.quantity)

    def get_item_entity_class(self):
        return ReverseStack