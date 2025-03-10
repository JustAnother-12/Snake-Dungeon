
import pygame


class TextElement(pygame.sprite.Sprite):
    def __init__(self, text, color, size, x_pos, y_pos) -> None:
        super().__init__()
        self.text = text
        self.color = color
        self.size = size
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = pygame.font.Font("game-assets/font/default-pixilart-text.ttf", self.size)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))