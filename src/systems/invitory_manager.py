

import time
import pygame
from entities.items.item_entity import ItemEntity
from entities.items.item_stack import F, ItemStack
from entities.items.item_type import ItemCategory


class InvitoryManager:
    from entities import Player
    def __init__(self, snake: "Player.Snake") -> None:

        self.slots: list[ItemStack | None] = [None, None, None, None, None, None]
        self.slots_map_type = [
            ItemCategory.CONSUMABLE,
            ItemCategory.CONSUMABLE, 
            ItemCategory.EQUIPMENT, 
            ItemCategory.EQUIPMENT,
            ItemCategory.EQUIPMENT, 
            ItemCategory.SKILL
        ]
        self.snake = snake
        self.keys_map = [
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_COMMA
        ]
        self.time_pess: list[float] = [0, 0, 0, 0, 0, 0]
        self.pess_time = 0.5
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        for index, key in enumerate(self.keys_map):
            if self.time_pess[index] == 0 and keys[key]:
                self.time_pess[index] = time.time()
            
            elif self.time_pess[index] and keys[key]:
                print(time.time() - self.time_pess[index])
                if time.time() - self.time_pess[index] > self.pess_time:
                    self.drop(index)

            elif self.time_pess[index] and not keys[key]:
                if not self.slots[index] is None:
                    self.slots[index].use(self.snake) # type: ignore
                self.time_pess[index] = 0

    def _check_item_exits(self, item: ItemStack):
        '''chả về vị trị của item đó trong mảng Không thấy thì nó trả về -1'''
        for index, value in enumerate(self.slots):
            if value is None: continue
            
            if value.item_type.id == item.item_type.id:
                return index
        
        return -1

    def add_item(self, item: ItemStack) -> bool:

        # nếu item đã tồn tại
        index = self._check_item_exits(item)
        if index >= 0:
            if item.item_type.category == ItemCategory.EQUIPMENT:
                return False
            
            return self.slots[index].stack(item) # type: ignore
        
        # tìm lot trống
        for index, value in enumerate(self.slots):

            # bỏ qua những slot khác loại
            if self.slots_map_type[index] != item.item_type.category:
                continue

            if value is None: 
                self.slots[index] = item
                return True
        
        return False
            
    def remove_item(self, item: ItemStack, quantity: int = -1):
        index = self._check_item_exits(item)
        if index < 0:
            return False
        
        if quantity == -1 or (self.slots[index].quantity - quantity) == 0: # type: ignore
            self.slots[index] = None
            return True
        
        if self.slots[index].quantity - quantity < 0: # type: ignore
            return False
        
        self.slots[index].quantity -= quantity # type: ignore
    
    def drop(self, index: int):
        # self.snake.level.item_group.add(ItemEntity())
        if self.slots[index] is None:
            return False
        
        item_entity_class = self.slots[index].get_item_entity_class() # type: ignore
        self.snake.level.item_group.add(item_entity_class(self.snake.level, self.snake.blocks[1].rect, 2, self.slots[index].quantity)) # type: ignore
        self.slots[index] = None
        return True