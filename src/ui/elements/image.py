import pygame

class ImageElement(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image: pygame.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
