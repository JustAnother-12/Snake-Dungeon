
from typing import Any
import pygame

from utils import pixil



class ItemSlot(pygame.sprite.Sprite):
    from entities.items.item_stack import ItemStack
    def __init__(self, x_pos, y_pos, item_stake: ItemStack | None = None):
        super().__init__()
        self._image = pixil.Pixil.load("game-assets/graphics/pixil/ITEM_SLOTS.pixil", 1).frames[0]
        self.image = self._image.copy()
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.__item_stake = item_stake
        if item_stake:
            self.item_img = pixil.Pixil.load(item_stake.item_type.texture_path, 3).frames[0]
        else: 
            self.item_img = None
    
    @property
    def item_stake(self):
        return self.__item_stake
    
    @item_stake.setter
    def item_stake(self, item_stake):
        self.__item_stake = item_stake
        if item_stake:
            self.item_img = pixil.Pixil.load(item_stake.item_type.texture_path, 3).frames[0]
        else:
            self.item_img = None
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image.fill((0,0,0,0)) # type: ignore
        self.image.blit(self._image) # type: ignore
        if self.item_img:
            t = ((64) - (16 * 3)) // 2
            self.image.blit(self.item_img, (t, t)) # type: ignore
        return super().update(*args, **kwargs) 
    

        
    
        