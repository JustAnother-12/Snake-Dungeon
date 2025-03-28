import random
from constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE, COIN_VALUE
import constant
import pixil
import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self,  level, area: pygame.Rect | None = None, r = 2) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/GOLD_LEVEL.pixil", 1
        ).frames[0]
        self.random_pos(area, r)
        self.rect = self.image.get_rect(center=self.pos)

    def random_pos(self, area: pygame.Rect | None, r = 2):
        if not area:
            self.pos = pygame.Vector2(
                random.randint(
                    constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES,
                    (
                        SCREEN_WIDTH_TILES
                        - constant.LEFT_RIGHT_BORDER_TILES
                        - constant.WALL_TILES
                    ),
                )
                * TILE_SIZE,
                random.randint(
                    constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES,
                    (
                        SCREEN_HEIGHT_TILES
                        - constant.TOP_BOTTOM_BORDER_TILES
                        - constant.WALL_TILES
                    ),
                )
                * TILE_SIZE,
            )
        else:
            R = int(r * constant.TILE_SIZE)
            x = random.randint(
                area.centerx - R - area.width // 2,
                area.centerx + R + area.width // 2,
            )
            if (
                x < area.centerx - area.width // 2
                or x > area.centerx + area.width // 2
            ):
                y = random.randint(
                    area.centery - R - area.height // 2,
                    area.centery + R + area.height // 2,
                )
            else:
                y = random.choice(
                    [
                        random.randint(
                            area.centery - R - area.height // 2,
                            area.centery - area.height // 2,
                        ),
                        random.randint(
                            area.centery + area.height // 2,
                            area.centery + R + area.height // 2,
                        ),
                    ]
                )
            self.pos = pygame.Vector2(x, y)
            if (
                x < (constant.LEFT_RIGHT_BORDER_TILES + constant.WALL_TILES) * TILE_SIZE + 4
                or x > (SCREEN_WIDTH_TILES - constant.LEFT_RIGHT_BORDER_TILES - constant.WALL_TILES) * TILE_SIZE - 4
                or y < (constant.TOP_BOTTOM_BORDER_TILES + constant.WALL_TILES) * TILE_SIZE + 4
                or y > (SCREEN_HEIGHT_TILES - constant.TOP_BOTTOM_BORDER_TILES - constant.WALL_TILES) * TILE_SIZE - 4
            ):
                self.random_pos(area)

    def update(self):
        if self.__is_collision_with_snake():
            self.on_collision()

    def __is_collision_with_snake(self):
        return pygame.sprite.spritecollideany(self, self.level.snake.blocks)
    
    def on_collision(self):
        self.kill()
        self.level.snake.gold += COIN_VALUE


class Coins(pygame.sprite.AbstractGroup):
    def __init__(self, level, quantity: int = 0) -> None:
        super().__init__()
        self.level = level
        for _ in range(quantity):
            self.add(Coin(self.level))

    def add_coin(self, quantity, source, r = 2):
        for _ in range(quantity):
            self.add(Coin(self.level, source.rect, r))
        self.level.add(self.sprites())

    def update(self):
        for coin in self.sprites():
            coin.update()