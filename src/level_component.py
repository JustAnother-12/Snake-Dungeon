import random
from constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
import constant
import pixil
from time import time
import pygame

class Trap(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.random_pos()
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1).frames[0]
        self.rect = self.image.get_rect(topleft = self.pos)
        self.isActive = False
        self.collisionTime = None

    def random_pos(self):
        self.pos = pygame.Vector2(
            (random.randint(0, SCREEN_WIDTH_TILES - 2) + constant.LEFT_RIGHT_BORDER_TILES) * TILE_SIZE,
            (random.randint(0, SCREEN_HEIGHT_TILES - 2) + constant.TOP_BOTTOM_BORDER_TILES) * TILE_SIZE
        )
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def reset(self):
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1).frames[0]
        self.isActive = False
        self.collisionTime = None

    def collision(self):
        self.collisionTime = time()
    
    def active(self):
        self.isActive = True
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1).frames[1]

    def update(self):
        if not self.collisionTime == None:
            if time() - self.collisionTime > 1.5:
                self.reset()
            elif time() - self.collisionTime > 1:
                self.active()

class Traps(pygame.sprite.AbstractGroup):
    def __init__(self, quantity) -> None:
        super().__init__()
        self.items: list[Trap] = []
        for _ in range(quantity):
            self.items.append(Trap())

        for trap in self.items:
            self.add(trap)

    def update(self) -> None:
        for trap in self.items:
            trap.update()

class Coin(pygame.sprite.Sprite):
    def __init__(self, *group: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*group)
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/GOLD_LEVEL.pixil", 1).frames[0].convert_alpha()
        self.random_pos()
        self.rect = self.image.get_rect(center = self.pos)

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(0 + TILE_SIZE//2, SCREEN_WIDTH_TILES - TILE_SIZE//2),
            random.randint(0 + TILE_SIZE//2, SCREEN_HEIGHT_TILES - TILE_SIZE//2)
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
        self.pos = pygame.Vector2(
            random.randint(0 + TILE_SIZE//2, SCREEN_WIDTH_TILES - TILE_SIZE//2),
            random.randint(0 + TILE_SIZE//2, SCREEN_HEIGHT_TILES - TILE_SIZE//2)
        )

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
