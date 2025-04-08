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

class Chest(pygame.sprite.Sprite):
    from levels import level
    def __init__(self, _level: "level.Level", pos, isLocked = None) -> None:
        super().__init__()
        self._level = _level
        self.isLocked = isLocked if isLocked != None else random.choice([True, False])
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/CHEST_SHEET.pixil", 1, constant.TILE_SIZE
        ).frames[int(self.isLocked)]
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.isClosed = True
        self.collision_time = None
        self.alpha = 255
        self.LockedText = TextElement("LOCKED!", "White", 8, int(self.pos[0])+8, int(self.pos[1]), "midleft")
        self.TextTime = None

    # def random_pos(self):
    #     self.pos = pygame.Vector2(
    #         random.randint(
    #             constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES + 1,
    #             (
    #                 SCREEN_WIDTH_TILES
    #                 - constant.LEFT_RIGHT_BORDER_TILES
    #                 - 3
    #                 - constant.WALL_TILES
    #             ),
    #         )
    #         * TILE_SIZE,
    #         random.randint(
    #             constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES + 1,
    #             (
    #                 SCREEN_HEIGHT_TILES
    #                 - constant.TOP_BOTTOM_BORDER_TILES
    #                 - 3
    #                 - constant.WALL_TILES
    #             ),
    #         )
    #         * TILE_SIZE,
    #     )

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
                    # self.FadeOut(self.image)

    # def FadeOut(self, sprite:pygame.Surface):
    #     self.alpha = max(0,self.alpha-5)
    #     sprite = sprite.copy()
    #     sprite.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
    #     if self.alpha <= 0:  # Kill the sprite when the alpha is <= 0.
    #         self.kill()


    def __is_collision_with_snake(self):
        return self.rect and not self._level.snake.is_dead and self.rect.colliderect(self._level.snake.blocks[0].rect)
    
    def OpenChest(self):
        self.isClosed = False
        item, rarity = LootPool((0, 0, 0, 0, 300, 300, 300)).get_item()
        if item == LootItem.COIN:
            self._level.item_group.add(CoinEntity(self.level, self.rect, 1, random.randint(1, 5)))
        elif item == LootItem.FOOD:
            self._level.item_group.add(FoodEntity(self.level, self.rect, 1))
        elif item == LootItem.EMPTY:
            print("Empty pot")
        # else:
            # ItemRegistry.create_item(item, rarity, self.level, self.rect)

        self.collision_time = time()

    def on_collision(self):
        if self.isClosed:
            if not self.isLocked:
                self.OpenChest()
            else:
                if self._level.snake.keys > 0:
                    self._level.snake.keys -= 1
                    self.OpenChest()
                else:
                    self._level.add(self.LockedText)
                    self.TextTime = time()