

from typing import Any

from pygame import Event
import pygame
from ui.elements import button
from ui.elements.button import ButtonElement
from ui.screens.state import State
from ui.elements.text import TextElement


class ItemInfoPopup(State):
    def __init__(self, level, item_entity):
        super().__init__(self)
        self.level = level
        self.item_entity = item_entity
        
        self.item_name = TextElement(item_entity.item_type.name, 'white', 20, 20, 20)

        self.button = ButtonElement(100, 100, "ok", "white")
        
        self.add(self.item_name, self.button)
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        # if self.button.on_hover():
        #     self.level.snake.add_item(self.item_stack)
            
        return super().update(*args, **kwargs)
    
    def get_event(self, event: Event):
        # TODO: sửa lại
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button.on_hover():
                self.level.snake.add_item(self.item_entity.to_item_stack())
                self.item_entity.kill()
                print('ok')
                self.level.interaction_manager.remove_register_interact(self.item_entity)
                self.level.game.state_stack.pop()
        return super().get_event(event)