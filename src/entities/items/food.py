import pygame
from config import constant
from entities.items.item_entity import ItemEntity
from entities.items.item_type import ActivationType, ItemCategory, ItemTexture, ItemType, Rarity


FOOD_TYPE = ItemType(
    'coin', 
    'Coin', 
    ItemCategory.INSTANT, 
    Rarity.COMMON,
    ItemTexture(
        constant.Texture.apple,
    ),
    "",
    1,
    activation_type=ActivationType.ON_COLLISION
)

class FoodEntity(ItemEntity):
    def __init__(self, level, area=None, r=2, quantity=1):
        super().__init__(level, FOOD_TYPE, area, r, quantity)
        self.eaten_by = self.level.snake
    
    def apply_instant_effect(self):
        self.eaten_by.grow_up(self.quantity)

    def update(self):
        if self.level.snake.is_dead:
            return
        if self._is_collision_with_snake() or self._is_collision_with_monster():
            self.on_collision()

    def _is_collision_with_monster(self):
        for monster in self.level.monsters:
            if pygame.sprite.spritecollideany(self, monster.blocks):
                self.eaten_by = monster
                return True
        return False
    