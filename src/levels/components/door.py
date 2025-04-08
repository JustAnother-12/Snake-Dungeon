
import random
from config.constant import TILE_SIZE
import config.constant as constant
from entities.items.instant.coin import CoinEntity
from entities.items.instant.food import FoodEntity
from entities.items.item_registry import ItemRegistry
from loot import LootItem, LootPool
from ui.elements.text import TextElement
import utils.pixil as pixil
from time import time
import pygame

class Door(pygame.sprite.Sprite):
    from levels import level
    def __init__(self, _level: "level.Level", pos, index) -> None:
        super().__init__()
        self._level = _level
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)) 
        self.image.fill((255, 0, 0))  # Placeholder for the door image
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.isClosed = True
        self.collision_time = None
        self.alpha = 255
        self.LockedText = TextElement("LOCKED!", "White", 8, int(self.pos[0])+8, int(self.pos[1]), "midleft")
        self.TextTime = None
        self._index = index


    def update(self) -> None:
        if self.TextTime != None:
            if time() - self.TextTime > 2:
                self.LockedText.kill()
        if self.__is_collision_with_snake():
            self.on_collision()
        if not self.isClosed:
            self.image = pixil.Pixil.load(
                "game-assets/graphics/pixil/CHEST_SHEET.pixil", 1, constant.TILE_SIZE
            ).frames[2]
        if not self.collision_time == None:
            if(time() - self.collision_time > 2):
                if not self.image == None:
                    self.alpha = max(0,self.alpha-5)
                    self.image = self.image.copy()
                    self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
                    if self.alpha <= 0:  # Kill the sprite when the alpha is <= 0.
                        self.kill()


    def __is_collision_with_snake(self):
        return self.rect and not self._level.snake.is_dead and self.rect.colliderect(self._level.snake.blocks[0].rect)

    def on_collision(self):
        print("Collision with door")
        self._level.next_level(self._index)
        self.kill()