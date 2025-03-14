from ast import Tuple
import pygame
from pygame.math import Vector2
import random
from const import TILE_SIZE, WINDOW_SIZE, APPLE_IMG, check_collision
import pixil




class Food(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.image: pygame.Surface = pygame.transform.scale(APPLE_IMG.convert_alpha(), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(0,0))
        # self.random_pos()
        self.visible = True

    def random_pos(self, snake_blocks):
        self.pos = Vector2(
            random.randint(0, WINDOW_SIZE // TILE_SIZE - 1) * TILE_SIZE,
            random.randint(0, WINDOW_SIZE // TILE_SIZE - 1) * TILE_SIZE,
        )
        self.rect = self.image.get_rect(topleft=self.pos)
        if check_collision(self, snake_blocks):
            self.random_pos(snake_blocks)

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    def __init__(self, *group: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*group)
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/GOLD_LEVEL.pixil", 1).frames[0].convert_alpha()
        self.random_pos()
        self.rect = self.image.get_rect(center = self.pos)

    def random_pos(self):
        self.pos = Vector2(
            random.randint(0 + TILE_SIZE//2, WINDOW_SIZE - TILE_SIZE//2),
            random.randint(0 + TILE_SIZE//2, WINDOW_SIZE - TILE_SIZE//2)
        )

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Key(pygame.sprite.Sprite):
    '''
    Key to open looked chest
    '''

    def __init__(self, *group: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*group)
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/KEY_SPRITE(1).pixil", 2).frames[0].convert_alpha()
        self.random_pos()
        self.rect = self.image.get_rect(center = self.pos)

    def random_pos(self):
        self.pos = Vector2(
            random.randint(0 + TILE_SIZE//2, WINDOW_SIZE - TILE_SIZE//2),
            random.randint(0 + TILE_SIZE//2, WINDOW_SIZE - TILE_SIZE//2)
        )

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
