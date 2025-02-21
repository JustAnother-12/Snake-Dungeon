
from .Sprite import Sprite
import pygame

class Player(Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, image_path)
        self.speed = 5
        self.health = 100

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.position.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.position.x += self.speed
        if keys[pygame.K_UP]:
            self.position.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.position.y += self.speed

    def update(self):
        self.handle_input()
        super().update()