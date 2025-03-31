from gc import callbacks
from typing import Any
import pygame
import constant


import pixil
pygame.init()
text_font = pygame.font.Font("game-assets/font/default-pixilart-text.ttf", 30)

class ButtonElement(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, text_input, text_color, callback = None) -> None:
        super().__init__()
        self.images = pixil.Pixil.load(constant.Texture.button, 2)
        self.image = self.images.frames[0]
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect: pygame.rect.Rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = text_font.render(self.text_input, True, text_color)
        # center the text
        self.text_rect = self.text.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        for i in range(len(self.images.frames)):
            self.images.frames[i].blit(self.text, self.text_rect)
        
        self.callback = callback

    def update(self) -> None:
        if self.isHovered():
            self.image = self.images.frames[1]
        else:
            self.image = self.images.frames[0]
    
    def isHovered(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def on_click(self) -> None:
        if self.callback != None:
            self.callback()
    
    def add_action(self, callback):
        self.callback = callback