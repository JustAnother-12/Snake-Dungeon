
from .GameObject import GameObject
import pygame

class Sprite(GameObject):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.topleft = (self.position.x, self.position.y)

    def render(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)