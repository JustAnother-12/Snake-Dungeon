from typing import Any
import pygame
import config.constant as constant


import utils.pixil as pixil
pygame.init()
text_font = pygame.font.Font("game-assets/font/default-pixilart-text.ttf", 30)

class ButtonElement(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, text_input, text_color) -> None:
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

        self.isSelected = -1 
        '''
        isSelected:
            -1: Cho phép dùng chuột
             0: Không được chọn
             1: Được chọn
        '''

    def update(self)-> None:
        if self.checkForInputs(pygame.mouse.get_pos()) or self.isSelected == 1:
            self.image = self.images.frames[1]
        else:
            self.image = self.images.frames[0]

    def checkForInputs(self, mouse_pos) -> bool:
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            return self.isSelected == -1
        return False
    
    def on_hover(self) -> bool:
        return self.checkForInputs(pygame.mouse.get_pos()) or self.isSelected == 1
    
    def set_selected(self, mode):
        self.isSelected = mode