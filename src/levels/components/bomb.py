import random
from config.constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
import config.constant as constant
import utils.pixil as pixil
from time import time
import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self, level, pos = None) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/BOMB_SHEET.pixil", 1
        ).frames[0]
        if pos == None:
            self.random_pos()
        else:
            self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.activeTime = None
        self.timeAppear = time()

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(
                constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
                (
                    SCREEN_WIDTH_TILES
                    - constant.LEFT_RIGHT_BORDER_TILES
                    - 1
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
            random.randint(
                constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
                (
                    SCREEN_HEIGHT_TILES
                    - constant.TOP_BOTTOM_BORDER_TILES
                    - 1
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
        )

    def __is_collision_with_snake(self):
        return self.rect and len(self.level.snake) > 0 and self.rect.colliderect(self.level.snake.blocks[0].rect)

    def update(self):
        if self.__is_collision_with_snake():
            self.on_collision()
        if self.activeTime != None:
            if time() - self.activeTime < 1:
                self.image = pixil.Pixil.load(
                    "game-assets/graphics/pixil/EXPLOSION_ANIMATION.pixil", 1
                ).frames[int((time() - self.activeTime) * 7)]
                self.rect = self.image.get_rect(topleft=self.pos- pygame.Vector2(TILE_SIZE, TILE_SIZE))
            else:
                self.kill()
        elif time() - self.timeAppear > 3:
            self.activeTime = time()

    def on_collision(self):
        if not self.activeTime:
            self.activeTime = time()

class BombGroup(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity = 0) -> None:
        super().__init__()
        self.empty()
        self.level = level
        for _ in range(quantity):
            self.add(Bomb(self.level))
        
    def update(self):
        for bomb in self.sprites():
            bomb.update()