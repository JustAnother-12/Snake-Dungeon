from gc import callbacks
from typing import Any
import pygame
import config.constant as constant


from utils.help import Share
import utils.pixil as pixil
pygame.init()

class ButtonElement(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, text_input, text_color,text_size=30, callback = None, width = None, height = None) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.images = pixil.Pixil.load(constant.Texture.button, 2)
        if(self.width != None and self.height != None):
            for i in range(len(self.images.frames)):
                self.images.frames[i]=pygame.transform.scale(self.images.frames[i], (self.width, self.height))
        self.image = self.images.frames[0]
        self.x_pos = x_pos
        self.y_pos = y_pos
        
        self.text_input = text_input
        self.text_font = pygame.font.Font("game-assets/font/default-pixilart-text.ttf", text_size)
        self.text_color = text_color
        self.text = self.text_font.render(self.text_input, True, self.text_color)

        
        self.rect: pygame.rect.Rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        # center the text
        self.text_rect = self.text.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.callback = callback
        
    def update(self) -> None:
        self.text = self.text_font.render(self.text_input, True, self.text_color)
        if self.isHovered():
            self.image = self.images.frames[1]
        else:
            self.image = self.images.frames[0]
        self.image.blit(self.text, self.text_rect)
    
    def isHovered(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def on_click(self) -> None:
        Share.audio.play_sound("click")
        if self.callback != None:
            self.callback()
    
    def add_action(self, callback):
        self.callback = callback