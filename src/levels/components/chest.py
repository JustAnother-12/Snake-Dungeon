import random
from config.constant import TILE_SIZE
import config.constant as constant
from ui.elements.text import TextElement
import utils.pixil as pixil
from time import time
import pygame

class Chest(pygame.sprite.Sprite):
    def __init__(self, level, pos, isLocked = None) -> None:
        super().__init__()
        self.level = level
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
        return self.rect and not self.level.snake.isDeath and self.rect.colliderect(self.level.snake.blocks[0].rect)
    
    def OpenChest(self):
        self.isClosed = False
        print("Open chest")
        self.level.coins.add_coin(random.randint(7, 15), self)
        self.collision_time = time()

    def on_collision(self):
        if self.isClosed:
            if not self.isLocked:
                self.OpenChest()
            else:
                if self.level.snake.keys > 0:
                    self.level.snake.keys -= 1
                    self.OpenChest()
                else:
                    self.level.add(self.LockedText)
                    self.TextTime = time()

class ChestGroup(pygame.sprite.AbstractGroup):
    def __init__(self, level, chests_pos) -> None:
        super().__init__()
        self.empty()
        for x,y in chests_pos:
            self.add(Chest(level, (x-TILE_SIZE,y-TILE_SIZE)))

    def update(self) -> None:
        for chest in self.sprites():
            chest.update()
