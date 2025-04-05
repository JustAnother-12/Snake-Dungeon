from enum import Enum
import random
from config.constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
import config.constant as constant
from utils.help import Share
import utils.pixil as pixil
import pygame

class BombState(Enum):
    APPEAR = 1
    ACTIVE = 2
    EXPLOSION = 3
    DISAPPEAR = 4

class Bomb(pygame.sprite.Sprite):
    def __init__(self, level, pos = None, state: BombState = BombState.APPEAR) -> None:
        super().__init__()
        self.level = level
        self.bomb_sheet = pixil.Pixil.load(
            "game-assets/graphics/pixil/BOMB_SHEET.pixil", 1
        )
        self.image = self.bomb_sheet.frames[0]
        self.state = state
        self.pos = pos if pos != None else self.random_pos()
        self.rect = self.image.get_rect(topleft=self.pos)
        self.time = 0
        self.animation_sheet = pixil.Pixil.load(
            "game-assets/graphics/pixil/EXPLOSION_ANIMATION.pixil", 1
        )
        self.key_time = {
            BombState.APPEAR: 0,
            BombState.ACTIVE: 1,
            BombState.EXPLOSION: 1,
            BombState.DISAPPEAR: 0.5,
        }

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

        return self.pos

    def __is_collision_with_snake(self):
        return self.rect and len(self.level.snake) > 0 and self.rect.colliderect(self.level.snake.blocks[0].rect)

    def update(self):
        if self.__is_collision_with_snake():
            self.on_collision()

        if self.state == BombState.APPEAR:
            return
        
        self.time += Share.clock.get_time() / 1000
        if self.state == BombState.ACTIVE:
            
            # 2: nhấp nháy 2 lần
            self.image = self.bomb_sheet.frames[
                int(self.time / (self.key_time[self.state] / 2) * len(self.bomb_sheet.frames)) % len(self.bomb_sheet.frames)
            ]
            self.rect = self.image.get_rect(topleft=self.pos)

            if self.time > self.key_time[BombState.ACTIVE]:
                self.state = BombState.EXPLOSION
                self.time = 0
        
        if self.state == BombState.EXPLOSION:
            frame = self.animation_sheet.frames[
                min(int(self.time / self.key_time[self.state] * len(self.animation_sheet.frames)), len(self.animation_sheet.frames) - 1)
            ]
            self.image = frame
            self.rect = self.image.get_rect(topleft=self.pos - pygame.Vector2(TILE_SIZE, TILE_SIZE))
            if self.time > self.key_time[BombState.EXPLOSION]:
                self.state = BombState.DISAPPEAR
                self.time = 0
        
        if self.state == BombState.DISAPPEAR and self.time > self.key_time[BombState.DISAPPEAR]:
            self.kill()

    def on_collision(self):
        if self.state == BombState.APPEAR:
            self.state = BombState.ACTIVE

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