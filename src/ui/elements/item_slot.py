
from typing import Any
import pygame

from config import constant
from entities.items.item_type import ItemCategory
from utils import pixil

class ItemSlot(pygame.sprite.Sprite):
    from entities.items.item_stack import ItemStack
    def __init__(self, x_pos, y_pos, scale=1, item_stack: ItemStack | None = None):
        super().__init__()
        self._image = pixil.Pixil.load("game-assets/graphics/pixil/EQUIPMENT_SLOTS.pixil", scale).frames[0]
        self._empty_slot = pixil.Pixil.load("game-assets/graphics/pixil/EMPTY_SLOTS.pixil", scale).frames[0]
        self.image = self._empty_slot.copy()
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.__item_stack = item_stack
        self._item_cooldown = pixil.Pixil.load("game-assets/graphics/pixil/ITEM_SLOT_COOLDOWN.pixil", scale).frames[0]
        self.font = pygame.font.Font(constant.PIXEL_FONT, 15)
        if item_stack:
            self.item_img = pixil.Pixil.load(item_stack.item_type.texture.pixil_path, 3).frames[item_stack.item_type.texture.stack_frame]
        else: 
            self.item_img = None
    
    @property
    def item_stack(self):
        return self.__item_stack
    
    @item_stack.setter
    def item_stack(self, item_stack: ItemStack):
        self.__item_stack = item_stack
        if item_stack:
            if item_stack.item_type.category != ItemCategory.SKILL:
                self.item_img = pixil.Pixil.load(item_stack.item_type.texture.pixil_path, 2).frames[item_stack.item_type.texture.stack_frame]
            else:
                self.item_img = pixil.Pixil.load(item_stack.item_type.texture.pixil_path, 4).frames[item_stack.item_type.texture.stack_frame]
        else:
            self.item_img = None
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image.fill((0,0,0,0)) # type: ignore
        if self.item_stack is None:
            self.image.blit(self._empty_slot) # type: ignore
        else:
            # self.image.blit(self._image) # type: ignore
            pass
        if not self.item_img: 
            super().update(*args, **kwargs)
            return

        # t = ((64) - (16 * 3)) // 2
        if self.__item_stack.item_type.category != ItemCategory.SKILL: # type:ignore
            self.image.blit(self.item_img, (0, 0)) # type: ignore
        else:
            self.image.blit(self.item_img, (0, 0)) # type: ignore

        if self.item_stack.item_type.category == ItemCategory.CONSUMABLE: # type: ignore
            if self.item_stack.quantity == self.item_stack.item_type.max_stack: # type: ignore
                s=self.font.render(str(self.item_stack.quantity), True, 'cyan') # type: ignore
            else: s = self.font.render(str(self.item_stack.quantity), True, 'white') # type: ignore
            self.image.blit(s, (40, 30)) # type: ignore

        if self.item_stack.item_type.cooldown: # type: ignore
            p = (self.item_stack.get_cooldown_remaining() / self.item_stack.item_type.cooldown) # type: ignore
            
            if self.__item_stack.item_type.category != ItemCategory.SKILL: # type:ignore
                height = int(p * 65)
                top = 64 - height
                self.image.blit(self._item_cooldown, (0, top), (0, top, 64, height)) # type: ignore
            else:
                height = int(p * 128)
                top = 128 - height
                self.image.blit(self._item_cooldown, (0, top), (0, top, 128, height)) # type: ignore

        return super().update(*args, **kwargs) 
    

        
    
        