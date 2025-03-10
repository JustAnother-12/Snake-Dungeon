from typing import Any
import pygame

pygame.init()
text_font = pygame.font.Font("game-assets/font/default-pixilart-text.ttf", 30)
class Button(pygame.sprite.Sprite):
    def __init__(self, img, x_pos, y_pos, text_input, text_color) -> None:
        super().__init__()
        self.image = img
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect: pygame.rect.Rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = text_font.render(self.text_input, True, text_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # def update(self, display)-> None:
    #     display.blit(self.img, self.rect)
    #     display.blit(self.text, self.text_rect)

    def checkForInputs(self, mouse_pos) -> bool:
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False