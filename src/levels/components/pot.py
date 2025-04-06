import random
import config.constant as constant
from entities.items.instant.coin import CoinEntity
from entities.items.instant.food import FoodEntity
from entities.items.item_registry import ItemRegistry
from entities.items.item_type import ItemCategory, Rarity
import utils.pixil as pixil
from time import time
import pygame
from loot import LootItem, LootPool

class Pot(pygame.sprite.Sprite):
    def __init__(self, level,pos) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/POTS_SPRITE_SHEET.pixil", 1).frames[random.randint(0,3)]

        self.pos = pos
        self.rect = self.image.get_rect(topleft = self.pos)
        self.collision_time = None
        self.alpha = 255
        self.isClosed = True

    def update(self):
        if self.__is_collision_with_snake():
            self.on_collision()
        if not self.isClosed:
            self.image = pixil.Pixil.load("game-assets/graphics/pixil/POTS_SPRITE_SHEET.pixil", 1).frames[4]
        if not self.collision_time == None:
            if(time() - self.collision_time > 2):
                if not self.image == None:
                    self.alpha = max(0,self.alpha-5)
                    self.image = self.image.copy()
                    self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
                    if self.alpha <= 0:  # Kill the sprite when the alpha is <= 0.
                        self.kill()

    def __is_collision_with_snake(self):
        return self.rect and not self.level.snake.is_dead and self.rect.colliderect(self.level.snake.blocks[0].rect)
    
    def open(self):
        self.isClosed = False
        # item, rarity = LootPool((300, 350, 245, 105, 0, 0, 0)).get_item()
        # if item == LootItem.COIN:
        #     self.level.item_group.add(CoinEntity(self.level, self.rect, 1, random.randint(1, 5)))
        # elif item == LootItem.FOOD:
        #     self.level.item_group.add(FoodEntity(self.level, self.rect, 1))
        # elif item == LootItem.EMPTY:
        #     print("Empty pot")
        # else:
        #     print(f"[{rarity.value}]: {item.value} item")
    
        item, rarity = ItemCategory.INSTANT, Rarity.COMMON
        ItemRegistry.create_item(item, rarity, self.level, self.rect)
        if self.collision_time == None:
            self.collision_time = time()

    def on_collision(self):
        if self.isClosed:
            self.open()

class Pot_group(pygame.sprite.AbstractGroup):
    def __init__(self, level, pots_pos) -> None:
        super().__init__()
        self.empty()
        for x,y in pots_pos:
            self.add(Pot(level, (x,y)))

    def update(self):
        for pot in self.sprites():
            pot.update()