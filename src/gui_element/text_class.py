
import pygame


class TextElement(pygame.sprite.Sprite):
    def __init__(self, text, color, size, x_pos, y_pos, choice) -> None:
        super().__init__()
        self.text = text
        self.color = color
        self.size = size
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = pygame.font.Font("game-assets/font/default-pixilart-text.ttf", self.size)
        self.image = self.font.render(self.text, True, self.color)
        if choice == "midleft":
            self.rect = self.image.get_rect(midleft=(self.x_pos, self.y_pos))
        elif choice == "center":
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        elif choice == "midright":
            self.rect = self.image.get_rect(midright=(self.x_pos, self.y_pos))