import random
from config.constant import LEFT_RIGHT_BORDER_TILES, SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE, TOP_BOTTOM_BORDER_TILES, WALL_TILES
import utils.pixil as pixil
import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, type, angle=0) -> None:
        super().__init__()
        self.image = pixil.Pixil.load(
            "game-assets/graphics/pixil/WALL_SHEETS.pixil", 1
        ).frames[type]
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(topleft=pos)


class Walls(pygame.sprite.AbstractGroup):
    def __init__(self) -> None:
        super().__init__()
        self.empty()
        top = TOP_BOTTOM_BORDER_TILES * TILE_SIZE
        left = LEFT_RIGHT_BORDER_TILES * TILE_SIZE
        bottom = (
            SCREEN_HEIGHT_TILES - TOP_BOTTOM_BORDER_TILES - WALL_TILES
        ) * TILE_SIZE
        right = (
            SCREEN_WIDTH_TILES - LEFT_RIGHT_BORDER_TILES - WALL_TILES
        ) * TILE_SIZE
        for y in range(
            top + WALL_TILES * TILE_SIZE,
            bottom,
            WALL_TILES * TILE_SIZE,
        ):
            self.add(Wall((left, y), random.randint(0, 4), 90))
            self.add(Wall((right, y), random.randint(0, 4), 270))

        for x in range(
            left + WALL_TILES * TILE_SIZE,
            right,
            WALL_TILES * TILE_SIZE,
        ):
            self.add(Wall((x, top), random.randint(0, 4)))
            self.add(Wall((x, bottom), random.randint(0, 4), 180))

        self.add(Wall((left, top), 5))
        self.add(Wall((left, bottom), 5, 90))
        self.add(Wall((right, bottom), 5, 180))
        self.add(Wall((right, top), 5, 270))