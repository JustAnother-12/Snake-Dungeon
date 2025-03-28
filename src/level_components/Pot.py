import random
from constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
import constant
import pixil
from time import time
import pygame

class Pot(pygame.sprite.Sprite):
    def __init__(self, level, pos) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/POTS_SPRITE_SHEET.pixil", 1).frames[random.randint(0,3)]

        self.pos = pos
        self.rect = self.image.get_rect(topleft = self.pos)
        self.collision_time = None
        self.alpha = 255
        self.isClosed = True


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
        return self.rect and self.rect.colliderect(self.level.snake.blocks[0].rect)
    
    def open(self):
        self.isClosed = False
        print("Break pot!")
        self.level.coins.add_coin(random.randint(1, 3), self, 1)
        if self.collision_time == None:
            self.collision_time = time()

    def on_collision(self):
        if self.isClosed:
            self.open()

class Pot_group(pygame.sprite.AbstractGroup):
    def __init__(self, level, pots_pos) -> None:
        super().__init__()
        self.level = level
        self.pots_pos = pots_pos
        for x, y in self.pots_pos:
            self.add(Pot(self.level, (x,y)))

    def update(self):
        for pot in self.sprites():
            pot.update()