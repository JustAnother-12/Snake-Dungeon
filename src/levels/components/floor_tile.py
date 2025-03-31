import random
import pygame

import constant
import pixil


class Floor_Tile(pygame.sprite.Sprite):

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/FLOOR_SHEET.pixil", 1).frames[random.choices(range(0, 5), [20, 20, 1, 1, 1])[0]]
        self.rect = self.image.get_rect(topleft=pygame.Vector2(pos))

class Floor(pygame.sprite.AbstractGroup):
    def __init__(self) -> None:
        super().__init__()
        self.add_floor_tiles()

    def add_floor_tiles(self):
        for x in range(constant.MAP_LEFT, constant.MAP_RIGHT + 1, constant.TILE_SIZE):
            for y in range(constant.MAP_TOP, constant.MAP_BOTTOM + 1, constant.TILE_SIZE):
                self.add(Floor_Tile((x, y)))