import random
from constant import LEFT_RIGHT_BORDER_TILES, SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE, COIN_VALUE, TOP_BOTTOM_BORDER_TILES
import constant
import pixil
import pygame

class Key(pygame.sprite.Sprite):
    """
    Key to open the locked chest
    """

    def __init__(self,  level) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/KEY_SPRITE.pixil", 2
        ).frames[0]
        self.random_pos()
        self.rect = self.image.get_rect(center=self.pos)

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(
                constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES + 1,
                (
                    SCREEN_WIDTH_TILES
                    - constant.LEFT_RIGHT_BORDER_TILES
                    - 3
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
            random.randint(
                constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES + 1,
                (
                    SCREEN_HEIGHT_TILES
                    - constant.TOP_BOTTOM_BORDER_TILES
                    - 3
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
        )

    def update(self):
        if self.__is_collision_with_snake():
            self.on_collision()

    def __is_collision_with_snake(self):
        return pygame.sprite.spritecollideany(self, self.level.snake.blocks)
    
    def on_collision(self):
        self.kill()
        self.level.snake.keys += 1

class Keys(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity) -> None:
        super().__init__()
        for _ in range(quantity):
            self.add(Key(level))

    def update(self) -> None:
        for key in self.sprites():
            key.update()
