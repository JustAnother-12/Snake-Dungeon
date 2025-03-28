import random
from constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
import constant
import pixil
import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, level) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/OBSTACLE_TILE.pixil", 2).frames[0]
        self.random_pos()
        self.rect = self.image.get_rect(topleft=self.pos)

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(
                constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
                (
                    SCREEN_WIDTH_TILES
                    - constant.LEFT_RIGHT_BORDER_TILES
                    - 2
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
            random.randint(
                constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
                (
                    SCREEN_HEIGHT_TILES
                    - constant.TOP_BOTTOM_BORDER_TILES
                    - 2
                    - constant.WALL_TILES
                ),
            )
            * TILE_SIZE,
        )

    # def update(self):
    #     if self.__is_collision_with_snake():
    #         self.on_collision()
    
    # def __is_collision_with_snake(self):
    #     return pygame.sprite.spritecollideany(self, self.level.snake.blocks)
    
    # def on_collision(self):
    #     return True

class Obstacle_group(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity) -> None:
        super().__init__()
        self.level = level
        for _ in range(quantity):
            self.add(Obstacle(self.level))

    # def update(self):
    #     for obstacle in self.sprites():
    #         obstacle.update()
