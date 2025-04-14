import pygame

from config import constant


class FireBreak(pygame.sprite.Sprite):
    def __init__(self, level, length = 3):
        super().__init__()
        self.level = level
        self.length = length
        self.image = pygame.Surface((constant.TILE_SIZE, constant.TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
    def update_pos(self, pos, direction: pygame.Vector2):
        self.image = pygame.Surface((max(self.length * abs(direction[0]), 1) * constant.TILE_SIZE, max(self.length * abs(direction[1]), 1) * constant.TILE_SIZE), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))
        if direction == pygame.Vector2(1, 0):
            pos = (pos[0] + (constant.TILE_SIZE * (self.length + 1))//2, pos[1])
        elif direction == pygame.Vector2(-1, 0):
            pos = (pos[0] - (constant.TILE_SIZE * (self.length + 1))//2, pos[1])
        elif direction == pygame.Vector2(0, 1):
            pos = (pos[0], pos[1] + (constant.TILE_SIZE * (self.length + 1))//2)
        elif direction == pygame.Vector2(0, -1):
            pos = (pos[0], pos[1] - (constant.TILE_SIZE * (self.length + 1))//2)
            
        self.rect = self.image.get_rect(center=pos)
        print(self.rect)
        self.update()