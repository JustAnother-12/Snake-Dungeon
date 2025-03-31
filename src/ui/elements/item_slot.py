
from ast import arg
from typing import Any
import pygame

from config import constant
from entities.items.item_type import ItemCategory
from utils import pixil

class ItemSlot(pygame.sprite.Sprite):
    from entities.items.item_stack import ItemStack
    def __init__(self, x_pos, y_pos, item_stake: ItemStack | None = None):
        super().__init__()
        self._image = pixil.Pixil.load("game-assets/graphics/pixil/ITEM_SLOTS.pixil", 1).frames[0]
        self.image = self._image.copy()
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.__item_stake = item_stake
        self._item_cooldown = pixil.Pixil.load("game-assets/graphics/pixil/ITEM_SLOT_COOLDOWN.pixil", 1).frames[0]
        self.font = pygame.font.Font(constant.PIXEL_FONT, 15)
        if item_stake:
            self.item_img = pixil.Pixil.load(item_stake.item_type.texture.pixil_path, 3).frames[item_stake.item_type.texture.frame]
        else: 
            self.item_img = None
    
    @property
    def item_stake(self):
        return self.__item_stake
    
    @item_stake.setter
    def item_stake(self, item_stake: ItemStack):
        self.__item_stake = item_stake
        if item_stake:
            self.item_img = pixil.Pixil.load(item_stake.item_type.texture.pixil_path, 3).frames[item_stake.item_type.texture.frame]
        else:
            self.item_img = None
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image.fill((0,0,0,0)) # type: ignore
        self.image.blit(self._image) # type: ignore
        if not self.item_img: 
            super().update(*args, **kwargs)
            return

        t = ((64) - (16 * 3)) // 2
        self.image.blit(self.item_img, (t, t)) # type: ignore

        if self.item_stake.item_type.category == ItemCategory.CONSUMABLE: # type: ignore
            s = self.font.render(str(self.item_stake.quantity), True, 'white') # type: ignore
            self.image.blit(s, (40, 30)) # type: ignore

        if self.item_stake.item_type.cooldown: # type: ignore
            p = (self.item_stake.get_cooldown_remaining() / self.item_stake.item_type.cooldown) # type: ignore
            height = int(p * 65)
            top = 64 - height
            self.image.blit(self._item_cooldown, (0, top), (0, top, 64, height)) # type: ignore

        return super().update(*args, **kwargs) 
    

        
    
        