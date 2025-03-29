import random
from config.constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
import config.constant as constant
import utils.pixil as pixil
import pygame

class Food(pygame.sprite.Sprite):

    def __init__(self, level, area: pygame.Rect | None, r = 2) -> None:
        super().__init__()
        self.image: pygame.Surface = pygame.transform.scale(
            pixil.Pixil.load(constant.Texture.apple, 1).frames[0],  # type: ignore
            (constant.TILE_SIZE, constant.TILE_SIZE),
        )
        self.level = level
        self.random_pos(area, r)
        self.rect = self.image.get_rect(topleft=self.pos)

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


class Food_Group(pygame.sprite.AbstractGroup):
    def __init__(self, level) -> None:
        super().__init__()
        self.empty()
        self.level = level

    def update(self):
        for food in self.sprites():
            food.update()

    def add_food(self, source, quantity = 1, r = 1):
        for _ in range(quantity):
            self.add(Food(self.level, source.rect, r))
        self.level.add(self.sprites())