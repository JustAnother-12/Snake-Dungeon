import random
from config.constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
import config.constant as constant
import utils.pixil as pixil
import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, level, pos) -> None:
        super().__init__()
        self.level = level
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/OBSTACLE_TILE.pixil", 2).frames[0]
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)

