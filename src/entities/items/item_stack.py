from __future__ import annotations
from typing import Any, Callable
import typing

from entities.items.item_type import ItemCategory, ItemType
from utils.help import Share

F = Callable[[Any], Any]

class ItemStack:
    """Item Stack - Đại diện cho vật phẩm trong inventory có khả năng ghi đè runtime"""
    def __init__(self, item_type: ItemType, quantity=1):
        self.item_type = item_type
        self.quantity = min(quantity, item_type.max_stack) if item_type.max_stack > 0 else quantity
        self.active = False
        self.cool_down = 0

    from entities import Player
    def use(self, snake: "Player.Snake"):
        """Sử dụng item"""
        self.last_use_time = Share.clock.get_time()
        self.active = True
        # Equipment tự đông kích hoạt hiệu ứng
        if self.item_type.category == ItemCategory.EQUIPMENT:
            return False
        
        # Kiểm tra cooldown
        # if current_time - self.last_used_time < self.item_type.cooldown:
        #     return False
        if self.cool_down > 0:
            return False
        
        # kiểm tra xem còn thanh năng lượng không
        if snake.stamina < self.item_type.energy_usage:
            return False
        
        # Trừ năng lượng của người trơi
        snake.stamina -= self.item_type.energy_usage
            
        # Gọi hiệu ứng của item
        self.apply_effect(snake)
        self.cool_down = self.item_type.cooldown
        
        # Giảm số lượng nếu là consumable
        if self.item_type.category == ItemCategory.CONSUMABLE:
            self.quantity -= 1
            
        return True
    
    def apply_effect(self, snake: "Player.Snake"):
        """Áp dụng hiệu ứng của item - được ghi đè bởi lớp con"""
        pass

    def remove_effect(self, snake):
        """Ghi đè hiệu ứng của item - được ghi đè bởi lớp con"""
        pass
        
    def get_cooldown_remaining(self):
        """Trả về thời gian cooldown còn lại"""        
        return self.cool_down
    
    def can_stack_with(self, other: ItemStack):
        """Kiểm tra xem có thể stack với item khác không"""
        return (self.item_type.id == other.item_type.id and 
                self.item_type.category == ItemCategory.CONSUMABLE and
                self.quantity + other.quantity <= self.item_type.max_stack)
        
    def stack(self, other: ItemStack):
        if self.can_stack_with(other):
            self.quantity += other.quantity
            return True
        
        return False
        
    def add_runtime_overriding(self, snake, fun_name: str, pos: typing.Literal['after', 'return', 'before'], fun):
        if fun_name not in snake.run_time_overriding:
            snake.run_time_overriding[fun_name] = {
                "after": [],
                "return" : [],
                "before" : []
            }
        
        snake.run_time_overriding[fun_name][pos].append(fun)
    
    def remove_runtime_overriding(self,snake, fun_name: str, pos: typing.Literal['after', 'return', 'before'], fun):
        if fun_name in snake.run_time_overriding:
            if fun in snake.run_time_overriding[fun_name][pos]:
                snake.run_time_overriding[fun_name][pos].remove( fun)

    def __eq__(self, other):
        if not isinstance(other, ItemStack):
            return False
        return self.item_type == other.item_type
    
    def get_item_entity_class(self):
        from entities.items.item_entity import ItemEntity
        return ItemEntity

    def update(self, inventory_manager):
        self.cool_down = max(0, self.cool_down - Share.clock.get_time() / 1000)
        if self.quantity <= 0 and self.cool_down <= 0:
                inventory_manager.remove_item(self)
    