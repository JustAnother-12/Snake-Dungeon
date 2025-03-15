import random
import pygame
from time import time
import pixil
from const import WINDOW_SIZE, TILE_SIZE


class Trap(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.random_pos()
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1).frames[0]
        self.rect = self.image.get_rect(topleft = self.pos)
        self.isActive = False
        self.collisionTime = None

    def reset(self):
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1).frames[0]
        self.isActive = False
        self.collisionTime = None

    def random_pos(self):
        self.pos = pygame.Vector2(
            random.randint(0, WINDOW_SIZE//TILE_SIZE - 2) * TILE_SIZE,
            random.randint(0, WINDOW_SIZE//TILE_SIZE - 2) * TILE_SIZE
        )

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def collision(self):
        self.collisionTime = time()
    
    def active(self):
        self.isActive = True
        self.image = pixil.Pixil.load("game-assets/graphics/pixil/TRAP_SPIKE_SHEET.pixil", 1).frames[1]

    def update(self):
        if self.collisionTime:
            if time() - self.collisionTime > 2:
                self.reset()
            elif time() - self.collisionTime > 1:
                self.active()
