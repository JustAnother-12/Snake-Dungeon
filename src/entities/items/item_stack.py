import time
from typing import Any, Callable
import typing

from entities.items.item_type import ItemCategory, ItemType

F = Callable[[Any], Any]

class ItemStack:
    """Item Stack - Đại diện cho vật phẩm trong inventory có khả năng ghi đè runtime"""
    def __init__(self, item_type: ItemType, quantity=1):
        self.item_type = item_type
        self.quantity = min(quantity, item_type.max_stack) if item_type.max_stack > 0 else quantity
        self.active = False
        self.last_used_time = 0

    def use(self, snake):
        """Sử dụng item"""
        current_time = time.time()
        
        # Kiểm tra cooldown cho equipment
        if (self.item_type.category == ItemCategory.EQUIPMENT and 
            current_time - self.last_used_time < self.item_type.cooldown):
            return False
            
        # Gọi hiệu ứng của item
        self.apply_effect(snake)
        self.last_used_time = current_time
        
        # Giảm số lượng nếu là consumable
        if self.item_type.category == ItemCategory.CONSUMABLE:
            self.quantity -= 1
            if self.quantity <= 0:
                snake.remove_item(self)
                
        return True
    
    def apply_effect(self, snake):
        """Áp dụng hiệu ứng của item - được ghi đè bởi lớp con"""
        pass
        
    def get_cooldown_remaining(self):
        """Trả về thời gian cooldown còn lại"""
        if self.item_type.category != ItemCategory.EQUIPMENT:
            return 0
        
        elapsed = time.time() - self.last_used_time
        remaining = max(0, self.item_type.cooldown - elapsed)
        return remaining
    
    def can_stack_with(self, other):
        """Kiểm tra xem có thể stack với item khác không"""
        return (self.item_type.id == other.item_type.id and 
                self.item_type.category == ItemCategory.CONSUMABLE and
                self.quantity < self.item_type.max_stack)
        
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
