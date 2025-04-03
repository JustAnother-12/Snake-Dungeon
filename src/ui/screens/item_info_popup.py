

from typing import Any

from pygame import Event
import pygame
from config.constant import SCREEN_WIDTH_TILES, SCREEN_HEIGHT_TILES, TILE_SIZE
from ui.elements.button import ButtonElement
from ui.elements.image import ImageElement
from ui.screens.state import State
from ui.elements.text import TextElement
from utils.pixil import Pixil


class ItemInfoPopup(State):
    def __init__(self, level, item_entity):
        super().__init__(self)
        self.level = level
        self.item_entity = item_entity
        self.bg = Pixil.load("game-assets/graphics/pixil/ITEM_DESCRIPTION_BOX.pixil", 2).frames[0]
        self.bg_rect = ImageElement((SCREEN_WIDTH_TILES/2)*TILE_SIZE, (SCREEN_HEIGHT_TILES/2)*TILE_SIZE, self.bg)
        
        self.item_name = TextElement(item_entity.item_type.name, 'white', 14, int((SCREEN_WIDTH_TILES/2-6.5)*TILE_SIZE), int((SCREEN_HEIGHT_TILES/2-2.5)*TILE_SIZE), "midleft")

        self.button = ButtonElement(int((SCREEN_WIDTH_TILES/2)*TILE_SIZE), int((SCREEN_HEIGHT_TILES/2+6.5)*TILE_SIZE), "CONFIRM", "white", 11, width=100, height=30)
        
        self.add(self.bg_rect,self.item_name, self.button)
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        # if self.button.on_hover():
        #     self.level.snake.add_item(self.item_stack)
            
        return super().update(*args, **kwargs)
    
    def get_event(self, event: Event):
        # TODO: sửa lại
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button.isHovered():
                self.level.snake.add_item(self.item_entity.to_item_stack())
                self.item_entity.kill()
                print('ok')
                self.level.interaction_manager.unregister_interact(self.item_entity)
                self.level.game.state_stack.pop()
        return super().get_event(event)