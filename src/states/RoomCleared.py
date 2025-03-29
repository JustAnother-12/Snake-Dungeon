from typing import Any
import pygame
import constant
from time import time
from states.state import State
from gui_element.description_class import DecriptionElement


class RoomCleared(State):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.RoomCleared_text = DecriptionElement("ROOM CLEARED!", 
                                                  "white", 
                                                  45, 
                                                  (int(constant.SCREEN_WIDTH_TILES/2))*constant.TILE_SIZE, 
                                                  (int(constant.SCREEN_HEIGHT_TILES/2))*constant.TILE_SIZE, 
                                                  constant.SCREEN_WIDTH_TILES*constant.TILE_SIZE, 
                                                  9*constant.TILE_SIZE, 
                                                  (47,53,84), 
                                                  constant.TILE_SIZE,
                                                  0, 
                                                  choice='center'
                                                  )
        self.timer = time()
        self.add(self.RoomCleared_text)

    def update(self) -> None:
        if time() - self.timer > 1:
            self.game.state_stack.pop()
        return super().update()